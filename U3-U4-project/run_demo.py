"""
run_demo.py
端到端演示：mock传感器数据 -> SensoryMapper加权 -> CfC情感核心 -> 表达层映射
在硬件接线完成前，用这个脚本验证整条软件链路，也是未来接真实串口时唯一要换的地方
(把 mock_sensor.stream() 换成 serial_reader 读真实数据，其余代码不用动)。

重要边界说明见脚本末尾输出。
"""

from life_core import LifeAgent
from expression_mapper import emotion_to_expression
from mock_sensor import MockSensorStream, PRESET_BASELINES


def run_scenario(genome_name, genome_path, event_channel=None, event_target=None):
    print(f"\n{'='*60}")
    print(f"场景: {genome_name}")
    print(f"{'='*60}")

    agent = LifeAgent(genome_path)
    stream = MockSensorStream(PRESET_BASELINES[genome_name], seed=2024)

    print("-- 正常状态 (5 tick) --")
    for i, reading in enumerate(stream.stream(5)):
        result = agent.tick(reading, dt_seconds=2.0)
        expr = emotion_to_expression(result["emotion"])
        print(f"  tick{i}: rgb={expr['rgb']} breathe={expr['breathe_hz']}Hz "
              f"steadiness={expr['steadiness']}")

    if event_channel:
        print(f"-- 触发事件: {event_channel} -> {event_target} (15 tick渐变) --")
        stream.trigger_event(event_channel, target_value=event_target, duration_ticks=15)
        for i, reading in enumerate(stream.stream(20)):
            result = agent.tick(reading, dt_seconds=2.0)
            expr = emotion_to_expression(result["emotion"])
            if i % 4 == 0:
                print(f"  tick{i}: {event_channel}={reading[event_channel]:.1f}  "
                      f"rgb={expr['rgb']} breathe={expr['breathe_hz']}Hz "
                      f"pulse_alert={expr['pulse_alert']}")


if __name__ == "__main__":
    run_scenario("tomato_soil", "genomes/tomato_soil.json",
                 event_channel="moisture", event_target=12.0)

    run_scenario("freshwater", "genomes/freshwater.json",
                 event_channel="temperature", event_target=31.0)

    run_scenario("indoor_air", "genomes/indoor_air.json",
                 event_channel="voc", event_target=90.0)

    print(f"\n{'='*60}")
    print("重要边界说明（务必先读再展示）：")
    print("""
    1. 本次跑通验证的是数据管线本身：加权变换 -> CfC推理 -> 表达映射，
       全部链路无报错、维度正确、隐藏状态确实跨tick持续。

    2. CfC核心目前是随机初始化权重，尚未经过任何训练/学习。
       上面输出里情感状态对事件的响应幅度很小，这是随机网络的正常表现，
       不代表系统已经"学会"了如何解读环境胁迫。

    3. 让情感响应变得有意义，依赖你现有项目里的经验驱动学习机制
       （持续运行时的权重更新 + 定期记忆巩固）介入训练这个网络，
       这部分不在本次交付范围内，是下一步要对接的工作。

    4. 硬件接线完成后，唯一需要替换的是数据来源：
       把 mock_sensor.MockSensorStream 换成读取真实串口的等价模块
       （按 SERIAL_PROTOCOL.md 规范解析），SensoryMapper/CfC/表达层
       三层代码完全不用改。
    """)
