"""
run_live.py
用真实Arduino串口数据常驻运行整条链路：
  串口读数(serial_sensor) -> 感官加权(SensoryMapper) -> CfC情感核心(LifeAgent) -> 表达映射

跟 run_demo.py 的关系：run_demo.py 是硬件接线前用假数据验证链路通不通的脚本，
本文件是接线完成后真正长期跑的版本，数据源换成了 SerialSensorStream。

每次tick会把最新状态写入 live_state.json（覆盖写），这个文件就是后续
dashboard读取展示数据的接口——dashboard不需要直接依赖torch/ncps这些重依赖，
只需要定期读这个轻量JSON文件即可。

用法：
  python run_live.py genomes/indoor_air.json
  python run_live.py genomes/tomato_soil.json /dev/ttyUSB0
"""

import json
import sys
import time
import logging

from life_core import LifeAgent
from expression_mapper import emotion_to_expression
from serial_sensor import SerialSensorStream

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("run_live")

STATE_FILE = "live_state.json"


def write_state(genome_display_name, reading, result, expr):
    state = {
        "timestamp": time.time(),
        "genome": genome_display_name,
        "raw_readings": result["raw_recorded"],
        "sensory_vector": result["sensory_vector"],
        "warnings": result["warnings"],
        "emotion": result["emotion"],
        "expression": {
            "rgb": list(expr["rgb"]),
            "breathe_hz": expr["breathe_hz"],
            "steadiness": expr["steadiness"],
            "pulse_alert": expr["pulse_alert"],
        },
    }
    # 先写临时文件再替换，避免dashboard读到写了一半的半截JSON
    tmp_path = STATE_FILE + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    import os
    os.replace(tmp_path, STATE_FILE)


def main():
    genome_path = sys.argv[1] if len(sys.argv) > 1 else "genomes/indoor_air.json"
    port = sys.argv[2] if len(sys.argv) > 2 else "/dev/ttyUSB0"

    logger.info(f"加载基因组: {genome_path}")
    agent = LifeAgent(genome_path)
    logger.info(f"基因组载入完成: {agent.mapper.display_name}")

    logger.info(f"打开串口: {port}")
    stream = SerialSensorStream(port=port)

    logger.info("开始常驻读取真实传感器数据，按 Ctrl+C 停止")
    tick_count = 0
    try:
        for reading in stream.stream():
            result = agent.tick(reading, dt_seconds=2.0)
            expr = emotion_to_expression(result["emotion"])
            write_state(agent.mapper.display_name, reading, result, expr)

            tick_count += 1
            e = result["emotion"]
            logger.info(
                f"tick{tick_count} raw={reading} "
                f"valence={e['valence']:+.2f} arousal={e['arousal']:+.2f} "
                f"safety={e['safety']:+.2f} rgb={expr['rgb']}"
            )
            if result["warnings"]:
                for w in result["warnings"]:
                    logger.debug(w)
    except KeyboardInterrupt:
        logger.info("收到停止信号，退出")
    finally:
        stream.close()


if __name__ == "__main__":
    main()
