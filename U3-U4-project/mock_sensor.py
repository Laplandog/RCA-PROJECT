"""
mock_sensor.py
生成符合 SERIAL_PROTOCOL.md 格式的模拟传感器读数流。
在硬件接线完成前，用这个模块生成假数据跑通整条链路（感官加权->CfC->情绪输出）。

同时支持"制造一次胁迫事件"，用于测试系统能否对突发环境变化产生合理的情绪响应，
对应我们之前讨论过的"demo现场可信演示的是短时突变事件"这条设计边界。
"""

import time
import random


class MockSensorStream:
    """
    围绕一组"正常基线值"生成带噪声的读数，可以按需触发某个通道的阶跃式偏移
    （模拟真实的干旱/涝渍/温度骤变等短时事件）。
    """

    def __init__(self, baseline: dict, noise_std: dict = None, seed=None):
        """
        baseline: {"temperature": 23, "moisture": 55, ...} 正常状态下的中心值
        noise_std: 每个通道的噪声标准差，不传则默认用baseline值的3%
        """
        self.baseline = dict(baseline)
        self.noise_std = noise_std or {
            k: max(abs(v) * 0.03, 0.1) for k, v in baseline.items()
        }
        self.rng = random.Random(seed)
        self._active_events = {}  # {channel: (target_value, ticks_remaining)}

    def trigger_event(self, channel, target_value, duration_ticks=20):
        """
        制造一次渐进式的阶跃事件，比如模拟"几天不浇水"导致moisture缓慢下降到目标值。
        duration_ticks: 从当前值线性过渡到target_value所需的tick数
        """
        if channel not in self.baseline:
            raise ValueError(f"未知通道: {channel}")
        start_value = self.baseline[channel]
        self._active_events[channel] = {
            "start": start_value,
            "target": target_value,
            "total_ticks": duration_ticks,
            "ticks_done": 0,
        }

    def _step_events(self):
        finished = []
        for ch, ev in self._active_events.items():
            ev["ticks_done"] += 1
            progress = min(1.0, ev["ticks_done"] / ev["total_ticks"])
            self.baseline[ch] = ev["start"] + (ev["target"] - ev["start"]) * progress
            if progress >= 1.0:
                finished.append(ch)
        for ch in finished:
            del self._active_events[ch]

    def read(self) -> dict:
        """返回一次模拟读数，格式与真实Arduino发来的dict一致"""
        self._step_events()
        reading = {}
        for ch, center in self.baseline.items():
            noise = self.rng.gauss(0, self.noise_std.get(ch, 0.1))
            reading[ch] = round(center + noise, 3)
        return reading

    def stream(self, n_ticks, interval_sec=0.0):
        """生成器：连续产出n_ticks次读数，interval_sec>0时会真实sleep(用于演示节奏)"""
        for _ in range(n_ticks):
            yield self.read()
            if interval_sec > 0:
                time.sleep(interval_sec)


# 三个基因组各自的"正常基线"，用于快速构造对应场景的模拟数据流
PRESET_BASELINES = {
    "tomato_soil": {
        "temperature": 23.0, "moisture": 55.0, "voc": 15.0, "humidity_air": 55.0,
        "light": 18000.0, "sound": 20.0, "ph": 6.4, "ec": 1100.0,
    },
    "freshwater": {
        "temperature": 21.0, "voc": 10.0, "light": 8000.0,
        "sound": 10.0, "ph": 7.0, "ec": 300.0,
    },
    "indoor_air": {
        "temperature": 23.0, "voc": 8.0, "humidity_air": 50.0,
        "light": 800.0, "sound": 25.0,
    },
}


if __name__ == "__main__":
    # 自测：番茄场景，正常运行10 tick后触发一次干旱事件
    stream = MockSensorStream(PRESET_BASELINES["tomato_soil"], seed=1)
    print("--- 正常状态 5 tick ---")
    for i, r in enumerate(stream.stream(5)):
        print(i, r)

    print("--- 触发干旱事件(moisture 55 -> 15，20 tick内完成) ---")
    stream.trigger_event("moisture", target_value=15.0, duration_ticks=20)
    for i, r in enumerate(stream.stream(25)):
        if i % 5 == 0:
            print(i, "moisture=", r["moisture"])
