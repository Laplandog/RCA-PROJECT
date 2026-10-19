"""
led_ws2812.py
纯 spidev 驱动 WS2812/WS2812B/WS2812E 灯带（不依赖 Adafruit Blinka）。

原理：SPI 时钟 2.4MHz，每个 WS2812 数据位用 3 个 SPI 位表示：
    逻辑 1 -> 110，逻辑 0 -> 100（约 1.25us/位，符合 WS2812 时序）。
颜色顺序 GRB。末尾追加低电平字节作为 reset（>50us）。

接线：DIN->GPIO10(物理19脚, SPI MOSI)，GND->6脚，+5V->2脚。

用法：
    from led_ws2812 import WS2812
    strip = WS2812(num=30)
    strip.fill((0, 40, 34)); strip.show()
"""

import spidev

_LUT = {0: 0b100, 1: 0b110}


class WS2812:
    def __init__(self, num=30, bus=0, device=0, speed_hz=2400000):
        self.num = num
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = speed_hz
        self.spi.mode = 0
        self.buf = [(0, 0, 0)] * num

    def _encode(self):
        bits = []
        for (r, g, b) in self.buf:
            for byte in (g, r, b):            # WS2812 是 GRB 顺序
                for i in range(7, -1, -1):    # 高位在前
                    code = _LUT[(byte >> i) & 1]
                    bits.append((code >> 2) & 1)
                    bits.append((code >> 1) & 1)
                    bits.append(code & 1)
        while len(bits) % 8:
            bits.append(0)
        out = bytearray()
        for i in range(0, len(bits), 8):
            v = 0
            for j in range(8):
                v = (v << 1) | bits[i + j]
            out.append(v)
        out += bytes(60)                      # reset 拖尾（>50us）
        return list(out)

    def set(self, i, color):
        if 0 <= i < self.num:
            self.buf[i] = color

    def fill(self, color):
        self.buf = [color] * self.num

    def show(self):
        self.spi.writebytes(self._encode())

    def clear(self):
        self.fill((0, 0, 0))
        self.show()


if __name__ == "__main__":
    import sys
    import time
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    s = WS2812(num=n)
    print(f"[test] N={n}")

    print("[test] A) 首颗亮红（验证数据线+方向）")
    s.clear()
    s.set(0, (60, 0, 0))
    s.show()
    time.sleep(1.5)

    print("[test] B) 全部点亮 暗青色（验证整条）")
    s.fill((0, 45, 38))
    s.show()
    time.sleep(1.5)

    print("[test] C) 跑马灯（验证可寻址）")
    for k in range(n):
        s.clear()
        s.set(k, (0, 60, 50))
        s.show()
        time.sleep(0.04)

    print("[test] D) 呼吸 3 次")
    import math
    for cyc in range(3):
        for t in range(0, 100, 3):
            b = (math.sin(t / 100 * math.pi)) ** 2
            v = int(70 * b)
            s.fill((int(v * 0.35), v, int(v * 0.85)))
            s.show()
            time.sleep(0.02)

    print("[test] 结束，留一档暗青常亮")
    s.fill((0, 30, 25))
    s.show()
