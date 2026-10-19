"""
narrative.py
叙事引擎：把冰冷的传感器偏离，转译成这条生命的"经历日记"。

设计原则（呼应项目核心）：
- 变化率/状态转变优先于绝对值：只在"舒适<->胁迫"状态发生转变时记一笔，
  而不是每个tick都碎碎念，这样日记读起来像真实经历而非日志刷屏。
- 基因组感知：同样的读数，不同生态位的"感受"不同（番茄怕干、鱼怕水温），
  措辞由通道方向 + 该基因组是否在乎(active/weight)共同决定。
- 情感只作调味：CfC核心尚未训练，情感值近似随机，所以叙事主干由
  有明确物理含义的"舒适区偏离"驱动，保证"翻译得准"。
"""

import time

# 舒适度分级阈值（对 comfort_deviation 的绝对值）
COMFORT_BAND = 0.15   # < 此值算舒适
STRESS_BAND = 0.60    # > 此值算明显胁迫

# 每条生命经历之间的最小间隔（秒），避免刷屏
MIN_EVENT_GAP = 12

# 长时间平稳后，偶尔记一笔"安好"的间隔（秒）
CALM_NOTE_GAP = 180


# 通道方向化的措辞：{channel: {"low": ..., "high": ..., "recover": ...}}
PHRASES = {
    "temperature": {
        "low":  "温度在下沉，一阵寒意漫过来",
        "high": "周围在升温，热意包裹着我",
        "recover": "温度回到了舒适的范围，我安定下来",
    },
    "moisture": {
        "low":  "土壤在变干，我开始感到口渴",
        "high": "水分太多了，根部有些发闷",
        "recover": "湿度回到了刚刚好的程度",
    },
    "voc": {
        "low":  "空气重新变得清透",
        "high": "空气里浮起一丝异样的气味",
        "recover": "那股气味散去了",
    },
    "humidity_air": {
        "low":  "空气变得干燥",
        "high": "空气变得潮湿而闷重",
        "recover": "空气的湿润回到了舒适区",
    },
    "light": {
        "low":  "光在消退，世界暗了下来",
        "high": "光变得强烈而刺眼",
        "recover": "光线柔和了下来，正合适",
    },
    "sound": {
        "low":  "四周安静了下来",
        "high": "外界的声响变得喧嚣",
        "recover": "喧嚣退去，重归安宁",
    },
    "ph": {
        "low":  "酸碱在向酸的一侧偏移",
        "high": "酸碱在向碱的一侧偏移",
        "recover": "酸碱重新平衡了",
    },
    "ec": {
        "low":  "养分/矿物浓度在变稀薄",
        "high": "养分/矿物浓度在升高",
        "recover": "养分浓度回到了适宜的水平",
    },
}

# 通道方向化的措辞（英文）
PHRASES_EN = {
    "temperature": {
        "low":  "The temperature is sinking; a chill washes over me.",
        "high": "The warmth is rising, wrapping itself around me.",
        "recover": "The temperature has returned to a comfortable range, and I settle.",
    },
    "moisture": {
        "low":  "The soil is drying out; I begin to feel thirsty.",
        "high": "There is too much water; my roots feel waterlogged.",
        "recover": "The moisture has returned to just the right level.",
    },
    "voc": {
        "low":  "The air turns clear again.",
        "high": "A strange scent drifts through the air.",
        "recover": "That odor has dispersed.",
    },
    "humidity_air": {
        "low":  "The air is turning dry.",
        "high": "The air grows damp and heavy.",
        "recover": "The air's moisture is back in the comfort zone.",
    },
    "light": {
        "low":  "The light is fading; the world dims around me.",
        "high": "The light grows harsh and glaring.",
        "recover": "The light softens, just right.",
    },
    "sound": {
        "low":  "Everything around me falls quiet.",
        "high": "The outside world grows loud and restless.",
        "recover": "The noise recedes; calm returns.",
    },
    "ph": {
        "low":  "The pH is drifting toward the acidic side.",
        "high": "The pH is drifting toward the alkaline side.",
        "recover": "The pH has balanced out again.",
    },
    "ec": {
        "low":  "The nutrient/mineral concentration is thinning out.",
        "high": "The nutrient/mineral concentration is climbing.",
        "recover": "The nutrient level has returned to a suitable range.",
    },
}

# 各基因组出生时的第一句话
BIRTH_WORDS = {
    "tomato_soil": "我在土壤中苏醒，根须初次舒展，开始感受这片土地。",
    "freshwater":  "我在水中睁开感官，凉意包裹周身，开始聆听这片水域。",
    "indoor_air":  "我作为这片空气苏醒，与呼吸它的人共享同一个空间。",
}
BIRTH_DEFAULT = "我睁开了感官，第一次感受到周围的世界。"

BIRTH_WORDS_EN = {
    "tomato_soil": "I awaken in the soil, my roots unfurling for the first time, beginning to feel this earth.",
    "freshwater":  "I open my senses in the water, coolness wrapping around me, beginning to listen to these waters.",
    "indoor_air":  "I awaken as this air itself, sharing the same space with those who breathe it.",
}
BIRTH_DEFAULT_EN = "I opened my senses and felt the world around me for the first time."


def birth_line(genome_id):
    return BIRTH_WORDS.get(genome_id, BIRTH_DEFAULT)


def birth_line_en(genome_id):
    return BIRTH_WORDS_EN.get(genome_id, BIRTH_DEFAULT_EN)


def _band(dev):
    """把有符号偏离度分档: comfortable / mild / stressed，并带方向"""
    a = abs(dev)
    if a < COMFORT_BAND:
        return "comfortable", 0
    level = "stressed" if a > STRESS_BAND else "mild"
    return level, (1 if dev > 0 else -1)


class NarrativeEngine:
    """
    维护每个通道上一次的舒适状态，检测状态转变并产出经历条目。
    """

    def __init__(self):
        # {channel: {"level": str, "dir": int}}
        self._last = {}
        self._last_event_t = 0
        self._last_calm_t = 0

    def observe(self, deviations: dict, active_channels: dict, emotion: dict, now=None):
        """
        deviations: {channel: signed_deviation}  已按舒适区算好的有符号偏离
        active_channels: {channel: {active, weight, ...}} 当前基因组配置
        emotion: 五维情感（调味用）
        返回: 本次新产生的经历条目列表 [{t, text, tone, channel}]
        """
        now = now or time.time()
        events = []

        for ch, dev in deviations.items():
            cfg = active_channels.get(ch, {})
            if not cfg.get("active"):
                continue
            if dev is None:
                continue

            level, direction = _band(dev)
            prev = self._last.get(ch, {"level": "comfortable", "dir": 0})
            self._last[ch] = {"level": level, "dir": direction}

            # 只在"变糟"或"恢复"的转变点记一笔
            worsened = _severity(level) > _severity(prev["level"])
            recovered = level == "comfortable" and prev["level"] != "comfortable"

            if now - self._last_event_t < MIN_EVENT_GAP:
                continue

            phr = PHRASES.get(ch, {})
            phr_en = PHRASES_EN.get(ch, {})
            if worsened and direction != 0:
                key = "high" if direction > 0 else "low"
                text = phr.get(key)
                if text:
                    tone = "alarm" if level == "stressed" else "unease"
                    events.append({"t": now, "text": text, "text_en": phr_en.get(key, text),
                                   "tone": tone, "channel": ch})
                    self._last_event_t = now
            elif recovered:
                text = phr.get("recover")
                if text:
                    events.append({"t": now, "text": text, "text_en": phr_en.get("recover", text),
                                   "tone": "relief", "channel": ch})
                    self._last_event_t = now

        # 长时间无事发生 + 整体舒适 -> 偶尔记一笔平静
        if not events:
            all_comfortable = all(
                self._last.get(ch, {}).get("level", "comfortable") == "comfortable"
                for ch, cfg in active_channels.items() if cfg.get("active")
            )
            if all_comfortable and now - self._last_calm_t > CALM_NOTE_GAP and self._last_calm_t_ready():
                idx = _calm_idx(emotion)
                events.append({
                    "t": now,
                    "text": CALM_LINES[idx],
                    "text_en": CALM_LINES_EN[idx],
                    "tone": "calm",
                    "channel": None,
                })
                self._last_calm_t = now
                self._last_event_t = now

        return events

    def _last_calm_t_ready(self):
        # 首次运行别立刻蹦"安好"，等系统先观察一会儿
        if self._last_calm_t == 0:
            self._last_calm_t = time.time()
            return False
        return True

    def snapshot(self):
        return {"last": self._last, "last_event_t": self._last_event_t, "last_calm_t": self._last_calm_t}

    def restore(self, snap):
        if not snap:
            return
        self._last = snap.get("last", {})
        self._last_event_t = snap.get("last_event_t", 0)
        self._last_calm_t = snap.get("last_calm_t", 0)


def _severity(level):
    return {"comfortable": 0, "mild": 1, "stressed": 2}.get(level, 0)


CALM_LINES = [
    "一切安好，我在静静地生长。",
    "此刻没有什么打扰，只是安然地存在着。",
    "周围的一切都在舒适的节律里，我很平静。",
]

CALM_LINES_EN = [
    "All is well; I am quietly growing.",
    "Nothing disturbs this moment; I simply exist, at peace.",
    "Everything around me moves in a comfortable rhythm; I am calm.",
]


def _calm_idx(emotion):
    # 用valence微调选哪句，纯调味
    v = emotion.get("valence", 0)
    idx = 0 if v >= 0 else 1
    return min(idx, len(CALM_LINES) - 1)


def _calm_line(emotion):
    return CALM_LINES[_calm_idx(emotion)]


# 中文 -> 英文 反查表：用于给旧的（升级前生成、只有中文的）经历条目补上英文
_ZH2EN = {}
for _ch, _d in PHRASES.items():
    _den = PHRASES_EN.get(_ch, {})
    for _k, _zh in _d.items():
        if _den.get(_k):
            _ZH2EN[_zh] = _den[_k]
for _gid, _zh in BIRTH_WORDS.items():
    if BIRTH_WORDS_EN.get(_gid):
        _ZH2EN[_zh] = BIRTH_WORDS_EN[_gid]
_ZH2EN[BIRTH_DEFAULT] = BIRTH_DEFAULT_EN
for _i, _zh in enumerate(CALM_LINES):
    if _i < len(CALM_LINES_EN):
        _ZH2EN[_zh] = CALM_LINES_EN[_i]


def en_for_zh(text):
    """已知中文叙事句 -> 英文；未知返回 None。"""
    return _ZH2EN.get(text)
