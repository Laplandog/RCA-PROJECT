"""
sensory_mapper.py
两层感官加权变换：舒适度曲线 -> 基因组权重
把原始传感器读数转成喂给CfC核心的加权偏离向量。

不依赖任何机器学习库，纯Python+可选numpy，可以脱离硬件独立测试。
"""

import json
import os
import logging

logger = logging.getLogger("sensory_mapper")

# 固定的通道顺序，任何地方引用这个向量都按这个顺序
CHANNEL_ORDER = [
    "temperature", "moisture", "voc", "humidity_air",
    "light", "sound", "ph", "ec"
]


def comfort_deviation(value, lo, hi, stress_lo, stress_hi):
    """
    返回有符号偏离度，范围裁剪到 [-1, 1]。
    0 = 完全舒适；负值 = 低于舒适区(越负越严重)；正值 = 高于舒适区(越正越严重)。
    """
    if lo <= value <= hi:
        return 0.0
    elif value < lo:
        if value <= stress_lo:
            return -1.0
        # 防止 lo == stress_lo 导致除零
        denom = (lo - stress_lo) or 1e-6
        return max(-1.0, -(lo - value) / denom)
    else:  # value > hi
        if value >= stress_hi:
            return 1.0
        denom = (stress_hi - hi) or 1e-6
        return min(1.0, (value - hi) / denom)


class SensoryMapper:
    """
    加载一个基因组配置文件，把原始传感器读数字典转成加权偏离向量。
    """

    def __init__(self, genome_path):
        self.genome_path = genome_path
        with open(genome_path, "r", encoding="utf-8") as f:
            self.genome = json.load(f)
        self._validate_genome()

    def _validate_genome(self):
        missing = [ch for ch in CHANNEL_ORDER if ch not in self.genome.get("channels", {})]
        if missing:
            raise ValueError(
                f"基因组文件 {self.genome_path} 缺少通道配置: {missing}"
            )

    @property
    def genome_id(self):
        return self.genome.get("genome_id", os.path.basename(self.genome_path))

    @property
    def display_name(self):
        return self.genome.get("display_name", self.genome_id)

    @property
    def baseline_params(self):
        return self.genome.get("baseline_params", {})

    def process(self, raw_readings: dict) -> dict:
        """
        raw_readings: {"temperature": 22.3, "moisture": 55.0, ...}
                      缺失的字段可以直接不在dict里出现
        返回: {
            "vector": [8个float，加权后的偏离向量，顺序固定按CHANNEL_ORDER],
            "raw_recorded": dict，全通道的原始读数（含inactive通道，用于日志/未来校准），
            "warnings": list，本次处理中的异常提示
        }
        """
        vector = []
        warnings = []
        raw_recorded = {}
        deviations = {}  # 每通道有符号偏离度(未乘权重)，供叙事引擎判断"舒适<->胁迫"转变

        for ch in CHANNEL_ORDER:
            cfg = self.genome["channels"][ch]
            raw_value = raw_readings.get(ch)
            raw_recorded[ch] = raw_value  # 无论active与否都记录，供未来校准/环境检测使用

            if not cfg.get("active", False):
                vector.append(0.0)
                deviations[ch] = None
                continue

            if raw_value is None:
                warnings.append(f"通道'{ch}'读数缺失，本tick按中性值(0)处理")
                vector.append(0.0)
                deviations[ch] = None
                continue

            try:
                raw_value = float(raw_value)
            except (TypeError, ValueError):
                warnings.append(f"通道'{ch}'读数非法({raw_value!r})，按中性值处理")
                vector.append(0.0)
                deviations[ch] = None
                continue

            dev = comfort_deviation(
                raw_value, cfg["lo"], cfg["hi"], cfg["stress_lo"], cfg["stress_hi"]
            )
            deviations[ch] = dev
            vector.append(cfg["weight"] * dev)

        if warnings:
            for w in warnings:
                logger.warning(w)

        return {
            "vector": vector,
            "raw_recorded": raw_recorded,
            "deviations": deviations,
            "warnings": warnings,
        }


if __name__ == "__main__":
    # 自测：拿一个还不存在的假读数跑一遍，验证异常处理不会崩
    import sys
    if len(sys.argv) > 1:
        mapper = SensoryMapper(sys.argv[1])
        test_reading = {"temperature": 22.0, "moisture": 999}  # 故意给一个超范围值+一个缺失字段
        result = mapper.process(test_reading)
        print("genome:", mapper.display_name)
        print("vector:", result["vector"])
        print("warnings:", result["warnings"])
    else:
        print("用法: python sensory_mapper.py <genome.json路径>  来做快速自测")
