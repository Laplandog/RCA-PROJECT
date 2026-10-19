# 串口数据契约（Arduino → RPi）
## 这是硬件端和软件端唯一需要提前对齐的接口，请在开始接线/编代码前先看这份文件

---

## 1. 数据格式：每行一个 JSON 对象，通过 USB 串口发送

Arduino 每隔固定周期（建议 2 秒）向串口打印**一行 JSON**，以换行符 `\n` 结尾：

```
{"temperature":22.3,"moisture":55.0,"voc":12.4,"humidity_air":48.0,"light":15200,"sound":8.2,"ph":6.4,"ec":1120}
```

**字段名固定，顺序不重要，缺失的字段直接不写这个key（不要写null/None）。**

| 字段名 | 对应传感器 | 单位 | 类型 |
|---|---|---|---|
| `temperature` | DS18B20 | °C | float |
| `moisture` | 电容式土壤湿度 | 百分比(0-100，或原始ADC值，见下方"标定"说明) | float |
| `voc` | BME680 | ppm(近似) | float |
| `humidity_air` | BME680 | 百分比RH | float |
| `light` | BH1750 | lux | float |
| `sound` | 声音传感器 | 相对强度(0-100) | float |
| `ph` | PH-4502C | pH值 | float |
| `ec` | TDS模块 | ppm | float |

## 2. 波特率

`115200`，Arduino 和 Python 两端必须一致。Arduino代码里 `Serial.begin(115200);`，Python端 `pyserial` 打开时指定同样的波特率。

## 3. 字段缺失/传感器未接的处理

如果某个基因组场景下某个传感器物理上没插（比如空气场景没接pH探头），Arduino **直接不发送这个字段**，而不是发 `null` 或 `0`。软件端会把缺失字段当作"暂时读不到"处理（喂中性值0，见 SensoryMapper 设计），而不是当作"读到了0"（0对pH来说是一个极端错误值，不能这样处理）。

## 4. 数值范围与标定说明（Arduino端做基础换算，不要发原始ADC值）

Arduino 端应该已经把 ADC 原始值换算成物理单位再发送，不要把 `analogRead()` 的 0-1023 原始值直接发过来。换算公式（土壤湿度、pH、EC这几个模拟传感器）需要各自标定，硬件调试阶段Arduino代码里应包含这层换算，软件端假设收到的已经是物理量。

## 5. Python 端读取示例（软件端已实现，仅供硬件端理解对接方式）

```python
import serial, json

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=2)
while True:
    line = ser.readline().decode('utf-8').strip()
    if not line:
        continue
    try:
        reading = json.loads(line)   # 得到 {"temperature": 22.3, ...}
    except json.JSONDecodeError:
        continue  # 丢弃损坏的行，不要让程序崩
    # reading 直接喂给 SensoryMapper.process(reading)
```

## 6. 联调前的检查清单

- [ ] Arduino串口监视器里，能看到规范的单行JSON持续打印，波特率115200
- [ ] 每个基因组场景下，不适用的传感器字段确实被跳过（不是发0/null）
- [ ] 所有数值都已经是物理单位（°C、lux、pH等），不是ADC原始值
- [ ] JSON格式合法（可以用在线JSON校验器粘贴一行验证）
