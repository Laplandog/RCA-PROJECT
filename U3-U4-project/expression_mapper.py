"""
expression_mapper.py
把五维情感状态转成物理表达参数(LED颜色+呼吸节奏)。
硬件端还没有RGB灯环时，这里先输出数值+模拟打印，
接线完成后直接把 rgb 三元组发给 Arduino 控制 WS2812 即可，逻辑不用改。
"""


def emotion_to_expression(emotion: dict) -> dict:
    """
    emotion: {"valence":..., "arousal":..., "safety":..., "connection":..., "seeking":...}
             每个值范围约 [-1, 1] (来自life_core.py的tanh输出)
    返回: {"rgb": (r,g,b), "breathe_hz": float, "steadiness": float}
    """
    valence = emotion["valence"]
    arousal = emotion["arousal"]
    safety = emotion["safety"]
    seeking = emotion["seeking"]

    # valence -> 色相：负向偏红橙，正向偏青绿
    if valence >= 0:
        r = int(255 * (1 - valence) * 0.5)
        g = int(180 + 75 * valence)
        b = int(150 + 60 * valence)
    else:
        r = int(180 + 75 * (-valence))
        g = int(120 * (1 + valence))
        b = int(90 * (1 + valence))
    r, g, b = (max(0, min(255, c)) for c in (r, g, b))

    # arousal -> 呼吸频率：-1时约0.2Hz(缓慢)，+1时约2Hz(急促)
    breathe_hz = 0.2 + (arousal + 1) / 2 * 1.8

    # safety -> 稳定度：越低越"抖动"，供硬件端决定要不要加闪烁噪声
    steadiness = max(0.0, min(1.0, (safety + 1) / 2))

    # seeking -> 是否触发脉冲升级信号（简化：超过阈值就标记）
    pulse_alert = seeking > 0.5

    return {
        "rgb": (r, g, b),
        "breathe_hz": round(breathe_hz, 2),
        "steadiness": round(steadiness, 2),
        "pulse_alert": pulse_alert,
    }


if __name__ == "__main__":
    tests = [
        {"valence": 0.6, "arousal": 0.1, "safety": 0.8, "connection": 0.2, "seeking": 0.1},
        {"valence": -0.7, "arousal": 0.6, "safety": -0.5, "connection": -0.2, "seeking": 0.7},
    ]
    for e in tests:
        print(e, "->", emotion_to_expression(e))
