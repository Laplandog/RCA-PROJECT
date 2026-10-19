"""
led_driver.py
把生命的情感状态，实时翻译成 WS2812 呼吸灯的颜色与节奏。

设计：
- 五种"心情"对应五种颜色（与 App 顶部的 mood 判定一致）：
    serene(舒展·安稳)     -> 青绿
    calm(平稳·接近舒适)   -> 湖蓝青
    alert(警觉·环境有变)  -> 琥珀黄
    discomfort(不适)      -> 橙
    threat(紧绷·感到胁迫) -> 红
- 颜色在心情切换时平滑过渡（线性插值），不硬跳。
- 亮度按"呼吸"正弦起伏；呼吸频率由 arousal(expression.breathe_hz) 决定，越唤醒越快。
- 安全感低(steadiness 低)时叠加轻微抖动，表现"不安"。
- 没有活跃生命时，灯进入极暗的缓慢"休眠"呼吸。

独立线程运行，异常不影响主程序。
"""

import threading
import time
import math
import random

MOOD_COLORS = {
    "serene":     (0, 210, 140),   # 青绿：愉悦且安稳
    "calm":       (40, 150, 175),  # 湖蓝青：平静
    "alert":      (255, 165, 25),  # 琥珀黄：警觉
    "discomfort": (255, 85, 20),   # 橙：不适
    "threat":     (255, 35, 35),   # 红：胁迫
    "dormant":    (24, 34, 52),    # 极暗蓝：无生命/休眠
}


def classify_mood(emotion):
    v = emotion.get("valence", 0.0)
    a = emotion.get("arousal", 0.0)
    s = emotion.get("safety", 0.0)
    if v > 0.15 and s > 0:
        return "serene"
    if v < -0.15 and s < 0:
        return "threat"
    if a > 0.3:
        return "alert"
    if v < -0.15:
        return "discomfort"
    return "calm"


class LEDController:
    def __init__(self, get_state, num=30, max_brightness=0.80, fps=50):
        from led_ws2812 import WS2812
        self.strip = WS2812(num=num)
        self.get_state = get_state
        self.num = num
        self.maxb = max_brightness
        self.dt = 1.0 / fps
        self._run = False
        self._base = [MOOD_COLORS["dormant"][i] * 1.0 for i in range(3)]
        self._phase = 0.0
        self._t = None

    def start(self):
        self._run = True
        self._t = threading.Thread(target=self._loop, daemon=True)
        self._t.start()

    def stop(self):
        self._run = False
        try:
            self.strip.clear()
        except Exception:
            pass

    def _loop(self):
        last = time.time()
        while self._run:
            now = time.time()
            dt = min(0.1, now - last)
            last = now

            try:
                st = self.get_state() or {}
            except Exception:
                st = {}
            born = st.get("born", False)
            emo = st.get("emotion", {}) or {}
            expr = st.get("expression", {}) or {}

            if not born:
                mood = "dormant"
                led_hz = 0.12
                bmin, bmax = 0.06, 0.28
                steady = 1.0
            else:
                mood = classify_mood(emo)
                hz = expr.get("breathe_hz", 1.0) or 1.0
                led_hz = max(0.12, min(0.55, hz * 0.30))
                bmin, bmax = 0.16, self.maxb
                if mood == "threat":
                    bmin, bmax = 0.28, self.maxb   # 胁迫时更醒目
                steady = expr.get("steadiness", 1.0)

            target = MOOD_COLORS.get(mood, MOOD_COLORS["calm"])
            alpha = 0.06                            # 颜色平滑过渡速度
            for i in range(3):
                self._base[i] += (target[i] - self._base[i]) * alpha

            self._phase += 2 * math.pi * led_hz * dt
            b = bmin + (bmax - bmin) * (0.5 - 0.5 * math.cos(self._phase))

            if born and steady < 0.4:               # 安全感低 -> 轻微不安抖动
                b *= (1.0 - random.uniform(0.0, 0.12))

            r = max(0, min(255, int(self._base[0] * b)))
            g = max(0, min(255, int(self._base[1] * b)))
            bl = max(0, min(255, int(self._base[2] * b)))
            try:
                self.strip.fill((r, g, bl))
                self.strip.show()
            except Exception:
                pass

            time.sleep(self.dt)


if __name__ == "__main__":
    # 独立自测：轮流演示五种心情
    demo = [
        ("serene",     {"valence": 0.5, "arousal": 0.0, "safety": 0.6}),
        ("calm",       {"valence": 0.0, "arousal": 0.0, "safety": 0.1}),
        ("alert",      {"valence": 0.0, "arousal": 0.6, "safety": 0.0}),
        ("discomfort", {"valence": -0.4, "arousal": 0.1, "safety": 0.2}),
        ("threat",     {"valence": -0.6, "arousal": 0.5, "safety": -0.5}),
    ]
    idx = {"i": 0}

    def fake_state():
        name, emo = demo[idx["i"] % len(demo)]
        return {"born": True, "emotion": emo,
                "expression": {"breathe_hz": 1.0 + emo["arousal"], "steadiness": (emo["safety"] + 1) / 2}}

    c = LEDController(fake_state, num=30)
    c.start()
    for name, _ in demo * 2:
        print("演示心情:", name)
        time.sleep(4)
        idx["i"] += 1
    c.stop()
