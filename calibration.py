"""
calibration.py
用部署头几天的真实观测数据，自动校准每个通道的舒适区间，
替代genome JSON里手写的文献估计值。
"""

import json
import numpy as np
import logging

logger = logging.getLogger("calibration")


def calibrate_comfort_band(readings, margin_std=1.0, stress_std=3.0):
    """
    readings: 某个通道过去N天的原始读数列表(list of float)
    返回该通道校准后的 (lo, hi, stress_lo, stress_hi)
    """
    if len(readings) < 10:
        raise ValueError("样本数太少，无法可靠校准，至少需要10个读数点")
    arr = np.array(readings, dtype=float)
    mean = float(np.mean(arr))
    std = float(np.std(arr))
    if std < 1e-6:
        # 极端情况：这段时间读数几乎不变，给一个最小容差避免舒适区宽度为0
        std = abs(mean) * 0.05 + 1e-3
    lo = mean - margin_std * std
    hi = mean + margin_std * std
    stress_lo = mean - stress_std * std
    stress_hi = mean + stress_std * std
    return lo, hi, stress_lo, stress_hi


def calibrate_genome_from_log(genome_path, log_readings_by_channel, min_samples=10,
                                margin_std=1.0, stress_std=3.0, output_path=None):
    """
    genome_path: 现有基因组json路径（读取active/weight配置，只更新数值区间）
    log_readings_by_channel: {"temperature": [22.1, 22.4, ...], "moisture": [...], ...}
                              只需要包含想要校准的通道，其余通道维持原值不变
    output_path: 若指定，写出校准后的新json；否则返回dict不落盘

    返回: (更新后的genome dict, 校准报告list)
    """
    with open(genome_path, "r", encoding="utf-8") as f:
        genome = json.load(f)

    report = []
    for ch, readings in log_readings_by_channel.items():
        if ch not in genome["channels"]:
            report.append(f"跳过未知通道 '{ch}'")
            continue
        if not genome["channels"][ch].get("active", False):
            report.append(f"跳过inactive通道 '{ch}'（物理不适用，无需校准）")
            continue
        if len(readings) < min_samples:
            report.append(
                f"通道 '{ch}' 样本数({len(readings)})不足{min_samples}，"
                f"保留原有默认值，标记为'校准中'"
            )
            continue
        try:
            lo, hi, stress_lo, stress_hi = calibrate_comfort_band(
                readings, margin_std=margin_std, stress_std=stress_std
            )
        except ValueError as e:
            report.append(f"通道 '{ch}' 校准失败: {e}")
            continue

        old = genome["channels"][ch]
        report.append(
            f"通道 '{ch}' 校准完成: "
            f"lo {old['lo']}->{lo:.2f}, hi {old['hi']}->{hi:.2f}, "
            f"stress_lo {old['stress_lo']}->{stress_lo:.2f}, "
            f"stress_hi {old['stress_hi']}->{stress_hi:.2f}"
        )
        genome["channels"][ch]["lo"] = round(lo, 3)
        genome["channels"][ch]["hi"] = round(hi, 3)
        genome["channels"][ch]["stress_lo"] = round(stress_lo, 3)
        genome["channels"][ch]["stress_hi"] = round(stress_hi, 3)

    genome["_calibration_status"] = "field-calibrated from real sensor observation"

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(genome, f, ensure_ascii=False, indent=2)
        report.append(f"已写出校准后的基因组文件: {output_path}")

    return genome, report


if __name__ == "__main__":
    # 自测：用随机模拟数据校准一次tomato_soil，验证流程跑通不报错
    rng = np.random.default_rng(42)
    fake_log = {
        "temperature": list(rng.normal(23, 2, 200)),
        "moisture": list(rng.normal(55, 8, 200)),
    }
    genome, report = calibrate_genome_from_log(
        "genomes/tomato_soil.json", fake_log,
        output_path="genomes/tomato_soil_calibrated_TEST.json"
    )
    for line in report:
        print(line)
