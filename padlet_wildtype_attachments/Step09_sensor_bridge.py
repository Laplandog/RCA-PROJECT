#!/usr/bin/env python3
"""
sensor_bridge.py — Arduino 物理传感器串口桥
=============================================
实验A（野生型）的感知来源。

硬件接线:
  BH1750  (光照)     → I²C (SDA/SCL)
  MAX9814 (声级)     → A0 (ADC)
  DHT22   (温湿度)   → D2 (Digital)
  HC-SR501(人体红外) → D3 (Digital)
  FSR402  (压力)     → A1 (ADC)
  MPU6050 (加速度计) → I²C (SDA/SCL)

串口协议: Arduino 每 CYCLE_SEC 秒发送一行 JSON:
  {"lux":320,"db":45,"temp":24.5,"hum":60,"pir":1,"prs":512,"ax":0.1,"ay":-0.02,"az":9.8}

本模块支持两种模式:
  1. 真实模式 (real)  — 从USB串口读取Arduino数据
  2. 模拟模式 (sim)   — 用真实时钟+噪声生成伪传感器数据（无Arduino时调试用）

依赖: pip install pyserial (仅真实模式需要)
"""

import time, math, random, json, sys, os, datetime, threading
from collections import deque

# ═══════════════════════════════════════════════════════════════
#  8通道定义（野生型感知空间）
# ═══════════════════════════════════════════════════════════════

CH_NAMES_WILD = [
    'luminance',       # 光照强度 (lux)         ← BH1750
    'sound_level',     # 声压级 (dB proxy)       ← MAX9814
    'temperature',     # 温度 (°C)              ← DHT22
    'humidity',        # 湿度 (%)               ← DHT22
    'presence',        # 人体存在 (0/1 → 0~1)   ← HC-SR501
    'pressure',        # 接触压力 (0~1023 ADC)   ← FSR402
    'motion',          # 运动量 (加速度向量模)   ← MPU6050
    'novelty',         # 新奇度 (变化率, 计算得出)
]

CH_RANGE_WILD = {
    'luminance':    (0, 1000),    # lux
    'sound_level':  (0, 120),     # dB proxy
    'temperature':  (10, 45),     # °C
    'humidity':     (10, 100),    # %
    'presence':     (0, 1),       # binary→continuous
    'pressure':     (0, 100),     # mapped from ADC
    'motion':       (0, 50),      # m/s² magnitude
    'novelty':      (0, 100),     # computed
}

# 发育组: 触觉/压力立即可用, 听觉稍后, 视觉最晚
CH_DEV_WILD = {
    'luminance':   'V',   # 视觉 — 晚开
    'sound_level': 'H',   # 听觉 — 中
    'temperature': 'T',   # 体感 — 立即
    'humidity':    'T',
    'presence':    'T',   # 红外(体感代理) — 立即
    'pressure':    'T',
    'motion':      'T',   # 本体感觉 — 立即
    'novelty':     'H',   # 跟随听觉发育
}

SENS_DIMS_WILD = len(CH_NAMES_WILD)  # 8


def norm_wild(name, val):
    """归一化到 [0,1]"""
    lo, hi = CH_RANGE_WILD[name]
    return max(0.0, min(1.0, (val - lo) / (hi - lo + 1e-8)))


# ═══════════════════════════════════════════════════════════════
#  Arduino 串口读取器 (真实模式)
# ═══════════════════════════════════════════════════════════════

class ArduinoSerialReader:
    """
    后台线程持续读串口，主循环随时取最新一帧。
    丢包/超时自动用上一帧填充。
    """

    def __init__(self, port='COM3', baud=115200, timeout=2.0):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.latest = None
        self._lock = threading.Lock()
        self._running = False
        self._thread = None
        self._serial = None
        self._fail_count = 0
        self._total_reads = 0

    def start(self):
        try:
            import serial
            self._serial = serial.Serial(self.port, self.baud, timeout=self.timeout)
            time.sleep(2)  # Arduino reset delay
            self._running = True
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()
            print(f"[SensorBridge] 串口已连接 / Serial connected: {self.port}@{self.baud}")
            return True
        except Exception as e:
            print(f"[SensorBridge] 串口连接失败 / Serial failed: {e}")
            return False

    def stop(self):
        self._running = False
        if self._serial and self._serial.is_open:
            self._serial.close()

    def _loop(self):
        while self._running:
            try:
                line = self._serial.readline().decode('utf-8', errors='replace').strip()
                if not line:
                    continue
                data = json.loads(line)
                self._total_reads += 1
                with self._lock:
                    self.latest = data
                    self._fail_count = 0
            except json.JSONDecodeError:
                self._fail_count += 1
            except Exception:
                self._fail_count += 1
                time.sleep(0.5)

    def get(self):
        """获取最新一帧，线程安全"""
        with self._lock:
            return self.latest.copy() if self.latest else None

    def stats(self):
        return {'reads': self._total_reads, 'fails': self._fail_count}


# ═══════════════════════════════════════════════════════════════
#  物理环境模拟器 (无Arduino时的替代)
# ═══════════════════════════════════════════════════════════════

class PhysicalSimulator:
    """
    基于真实时钟的传感器数据模拟。
    和实验B的AmbientEngine类似，但输出8通道而非15通道，
    且不含任何社会事件/叙事——纯物理环境。
    """

    def __init__(self, cycle_sec=3.0):
        self.cycle_sec = cycle_sec
        # 虚拟时钟：不跟随真实时间流逝，每次 step() 只前进 cycle_sec 秒，
        # 这样加速运行时昼夜节律/事件调度仍与"虚拟帧"保持一致（不会被真实挂钟拖慢）。
        self.virtual_time = datetime.datetime.now()
        self.virtual_t = self.virtual_time.timestamp()
        self.prev_raw = None
        # 随机"人来过"事件的下一次触发时间
        self._next_presence = self.virtual_t + random.uniform(300, 1800)
        self._presence_until = 0
        # 随机压力事件（风吹、物体碰撞传感器等）
        self._next_pressure = self.virtual_t + random.uniform(600, 3600)
        self._pressure_until = 0

    def step(self):
        """生成一帧模拟传感器数据"""
        self.virtual_time += datetime.timedelta(seconds=self.cycle_sec)
        self.virtual_t += self.cycle_sec
        now = self.virtual_time
        hour = now.hour + now.minute / 60.0
        t = self.virtual_t

        # ── 光照: 昼夜节律 ──
        sunrise, sunset = 5.83, 18.33
        if hour < sunrise - 0.5 or hour > sunset + 0.5:
            lux = random.uniform(0, 3)
        elif hour < sunrise + 1:
            frac = (hour - sunrise + 0.5) / 1.5
            lux = frac * 120
        elif hour > sunset - 1:
            frac = (sunset + 0.5 - hour) / 1.5
            lux = frac * 100
        else:
            noon_d = abs(hour - 13.0) / 5.0
            lux = 200 + 500 * max(0, 1 - noon_d)
        lux += random.gauss(0, 8)  # 云层/树影波动
        lux = max(0, lux)

        # ── 声级: 环境噪声 ──
        # 基础: 夜间安静20dB, 白天35dB
        base_db = 20 + 15 * max(0, min(1, (hour - 6) / 2) * min(1, (22 - hour) / 2))
        # 随机突发: 鸟叫、车流、门响
        burst = 0
        if random.random() < 0.03:  # 3%概率突发声音
            burst = random.uniform(15, 45)
        db = base_db + burst + random.gauss(0, 3)
        db = max(5, min(100, db))

        # ── 温度: 室内缓慢变化 ──
        temp_outdoor = 28 + 4 * math.sin((hour - 9) * math.pi / 12)
        temp_indoor = 25.5 + 0.5 * math.sin((hour - 9) * math.pi / 12)
        temp = temp_indoor + random.gauss(0, 0.3)

        # ── 湿度 ──
        hum = 55 + 10 * math.sin((hour - 3) * math.pi / 12) + random.gauss(0, 2)
        hum = max(20, min(95, hum))

        # ── 人体存在 (PIR): 随机事件 ──
        if t > self._next_presence:
            self._presence_until = t + random.uniform(30, 600)
            self._next_presence = t + random.uniform(300, 2400)
        presence = 1.0 if t < self._presence_until else 0.0
        # PIR有短暂延迟/震荡
        if abs(t - self._presence_until) < 5:
            presence = random.choice([0.0, 1.0])

        # ── 压力 (FSR): 偶发接触 ──
        if t > self._next_pressure:
            self._pressure_until = t + random.uniform(5, 60)
            self._next_pressure = t + random.uniform(600, 3600)
        if t < self._pressure_until:
            prs = random.uniform(15, 70)
        else:
            prs = random.uniform(0, 3)

        # ── 运动 (加速度): 大部分时间静止 ──
        motion = 9.81 + random.gauss(0, 0.05)  # 静止时≈g
        if presence > 0.5 and random.random() < 0.1:
            motion += random.uniform(0.5, 5)  # 有人时偶尔被移动

        # ── 新奇度: 基于变化率计算 ──
        raw = {
            'luminance': lux,
            'sound_level': db,
            'temperature': temp,
            'humidity': hum,
            'presence': presence,
            'pressure': prs,
            'motion': motion,
            'novelty': 0,  # 先填0，下面计算
        }

        if self.prev_raw is not None:
            deltas = []
            for ch in CH_NAMES_WILD[:7]:  # 前7个通道的变化率
                prev_n = norm_wild(ch, self.prev_raw[ch])
                curr_n = norm_wild(ch, raw[ch])
                deltas.append(abs(curr_n - prev_n))
            raw['novelty'] = min(100, sum(deltas) / len(deltas) * 500)
        self.prev_raw = raw.copy()

        return raw


# ═══════════════════════════════════════════════════════════════
#  ArduinoSensorBridge (统一接口)
# ═══════════════════════════════════════════════════════════════

class ArduinoSensorBridge:
    """
    统一接口: 不管是真实Arduino还是模拟模式，
    对外都提供 step() → dict(8通道) 的接口。

    用法:
        bridge = ArduinoSensorBridge(mode='sim')  # 或 'real'
        bridge.start()
        ...
        raw = bridge.step()  # {'luminance': 320, 'sound_level': 45, ...}
    """

    def __init__(self, mode='sim', port='COM3', baud=115200, cycle_sec=3.0):
        """
        mode: 'real' = Arduino串口, 'sim' = 物理模拟
        """
        self.mode = mode
        self.prev_raw = None

        if mode == 'real':
            self.reader = ArduinoSerialReader(port=port, baud=baud)
            self.sim = PhysicalSimulator(cycle_sec=cycle_sec)  # 作为fallback
        else:
            self.reader = None
            self.sim = PhysicalSimulator(cycle_sec=cycle_sec)

        self._frame = 0

    def start(self):
        if self.mode == 'real':
            ok = self.reader.start()
            if not ok:
                print("[SensorBridge] 回退到模拟模式 / Falling back to simulation")
                self.mode = 'sim'

    def stop(self):
        if self.reader:
            self.reader.stop()

    def step(self):
        """
        获取一帧传感器数据。返回 dict(8通道原始值)。
        真实模式下如果串口无数据，自动用模拟填充。
        """
        self._frame += 1
        raw = None

        if self.mode == 'real' and self.reader:
            arduino_data = self.reader.get()
            if arduino_data:
                raw = self._parse_arduino(arduino_data)

        if raw is None:
            raw = self.sim.step()

        # 计算novelty（如果Arduino没提供）
        if self.prev_raw is not None and raw.get('novelty', 0) < 0.01:
            deltas = []
            for ch in CH_NAMES_WILD[:7]:
                prev_n = norm_wild(ch, self.prev_raw.get(ch, 0))
                curr_n = norm_wild(ch, raw.get(ch, 0))
                deltas.append(abs(curr_n - prev_n))
            raw['novelty'] = min(100, sum(deltas) / len(deltas) * 500)

        self.prev_raw = raw.copy()
        return raw

    def _parse_arduino(self, data):
        """将Arduino JSON字段映射到标准8通道"""
        return {
            'luminance':   float(data.get('lux', 0)),
            'sound_level': float(data.get('db', 0)),
            'temperature': float(data.get('temp', 25)),
            'humidity':    float(data.get('hum', 50)),
            'presence':    float(data.get('pir', 0)),
            'pressure':    float(data.get('prs', 0)) / 10.23,  # ADC 0-1023 → 0-100
            'motion':      math.sqrt(
                float(data.get('ax', 0))**2 +
                float(data.get('ay', 0))**2 +
                float(data.get('az', 9.81))**2
            ),
            'novelty':     0,  # 由bridge计算
        }

    def get_mode(self):
        return self.mode

    def get_virtual_time(self):
        return self.sim.virtual_time

    def get_stats(self):
        if self.reader:
            return self.reader.stats()
        return {'reads': self._frame, 'fails': 0, 'mode': self.mode}


# ═══════════════════════════════════════════════════════════════
#  测试入口
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=== ArduinoSensorBridge 测试 (模拟模式) ===\n")
    bridge = ArduinoSensorBridge(mode='sim')
    bridge.start()

    for i in range(10):
        raw = bridge.step()
        print(f"[Frame {i+1}]")
        for ch in CH_NAMES_WILD:
            v = raw[ch]
            n = norm_wild(ch, v)
            bar = '█' * int(n * 20)
            print(f"  {ch:15s}: {v:8.2f}  [{n:.2f}] {bar}")
        print()
        time.sleep(1)

    bridge.stop()
    print("Done.")
