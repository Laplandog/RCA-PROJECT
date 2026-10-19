"""
serial_sensor.py
读取真实Arduino通过USB串口发来的JSON数据流，替代 mock_sensor.MockSensorStream。

接口特意跟 MockSensorStream 保持一致(.read() / .stream())，
所以 run_demo.py / life_core.py 这些上层代码完全不用改逻辑，
只需要把实例化的类从 MockSensorStream 换成 SerialSensorStream。

数据格式约定见 SERIAL_PROTOCOL.md：每行一个JSON对象，115200波特率。
"""

import json
import logging
import time

import serial

logger = logging.getLogger("serial_sensor")


class SerialSensorStream:
    """
    从真实Arduino串口读取JSON格式的传感器数据。
    """

    def __init__(self, port="/dev/ttyUSB0", baudrate=115200, timeout=2, reconnect_delay=2.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.reconnect_delay = reconnect_delay
        self.ser = None
        self._connect()

    def _connect(self):
        while True:
            try:
                self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
                logger.info(f"已连接串口 {self.port} @ {self.baudrate}")
                return
            except serial.SerialException as e:
                logger.warning(f"串口连接失败({e})，{self.reconnect_delay}秒后重试")
                time.sleep(self.reconnect_delay)

    def _safe_close(self):
        try:
            if self.ser:
                self.ser.close()
        except Exception:
            pass

    def read(self) -> dict:
        """
        阻塞读取一行合法JSON并返回dict。
        自动丢弃损坏/空行；串口意外断开(USB松动等)时自动重连，不会让上层代码崩掉。
        """
        while True:
            try:
                raw_line = self.ser.readline()
            except (serial.SerialException, OSError) as e:
                logger.warning(f"串口读取异常({e})，尝试重连")
                self._safe_close()
                self._connect()
                continue

            if not raw_line:
                continue  # 超时无数据(timeout秒内没收到完整行)，继续等下一行

            try:
                line = raw_line.decode("utf-8", errors="replace").strip()
            except UnicodeDecodeError:
                continue

            if not line:
                continue

            try:
                reading = json.loads(line)
            except json.JSONDecodeError:
                logger.debug(f"丢弃无法解析的行: {line!r}")
                continue

            if not isinstance(reading, dict):
                continue

            return reading

    def stream(self, n_ticks=None, interval_sec=0.0):
        """
        生成器：持续产出传感器读数。
        n_ticks=None 表示无限读下去(树莓派常驻运行场景)，传具体数字则只读n次(调试用)。
        interval_sec 一般不用传：真实数据节奏由Arduino发送频率决定(readline天然是阻塞等待)，
        这个参数只是为了跟 MockSensorStream 签名保持一致。
        """
        count = 0
        while n_ticks is None or count < n_ticks:
            yield self.read()
            count += 1
            if interval_sec > 0:
                time.sleep(interval_sec)

    def close(self):
        self._safe_close()


if __name__ == "__main__":
    # 自测：直接打印读到的真实数据，联调时用来确认能不能读到Arduino发来的数据
    import sys

    logging.basicConfig(level=logging.INFO)
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
    stream = SerialSensorStream(port=port)
    print(f"正在监听 {port} ... 按 Ctrl+C 停止")
    try:
        for reading in stream.stream():
            print(reading)
    except KeyboardInterrupt:
        print("已停止")
    finally:
        stream.close()
