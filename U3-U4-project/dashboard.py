"""
dashboard.py
生态环境情感化转译设备 —— 生命监护 App 后端 (all-in-one)

一个进程同时做两件事：
  1. 后台线程跑完整链路：串口读数 -> 感官加权 -> CfC情感核心 -> 表达映射 -> 叙事引擎
  2. Flask 网页服务：把这条生命的实时状态 / 经历日记 / 历史推给手机浏览器

核心概念：
  基因组 = 一条生命的先天本质，出生时选定，终身不变。
  一个时刻最多有【一条活跃生命】，另有一个【冷冻库】封存任意多条暂停的生命。

  生命管理动作：
  - 出生 birth：选生态位，诞生一条新的活跃生命。
  - 冷冻 freeze：不删数据，暂停当前生命成长，封存进冷冻库(保留全部记忆/日记)。
  - 唤醒 resume：把冷冻库里的某条生命解冻为活跃生命，继续成长。
  - 重生 rebirth：清空【当前活跃】这条生命的数据，重新选基因组诞生新生命(冷冻库不动)。
  - 死亡 death：清空【全部】数据(活跃 + 整个冷冻库)，回到出生主界面。

  年龄 = 累计"存活(活跃)时长"，冷冻期间与断电期间都不计入，符合"成长被暂停"的语义。
  活跃生命的选择/记忆(CfC隐藏状态)/日记都持久化，断电重启自动复活同一条活跃生命。

用法：
  python dashboard.py                 # 串口 /dev/ttyUSB0
  python dashboard.py /dev/ttyUSB0
  python dashboard.py --mock          # 无硬件时用模拟数据

依赖：flask, torch, ncps, pyserial
"""

import os
import sys
import glob
import json
import time
import shutil
import threading
from collections import deque

import torch
from flask import Flask, jsonify, request, render_template, send_from_directory

from life_core import LifeAgent, EMOTION_DIMS
from sensory_mapper import CHANNEL_ORDER
from expression_mapper import emotion_to_expression
from narrative import NarrativeEngine, birth_line, birth_line_en, en_for_zh

# ---------------- 配置 ----------------
GENOME_DIR = "genomes"
HISTORY_LEN = 360
EVENTS_LEN = 120
TICK_DT = 2.0
DEFAULT_PORT = "/dev/ttyUSB0"

STATE_DIR = "life_state"
ACTIVE_DIR = os.path.join(STATE_DIR, "active")
FROZEN_DIR = os.path.join(STATE_DIR, "frozen")

F_META = "meta.json"
F_HIDDEN = "hidden.pt"
F_HISTORY = "history.json"
F_EVENTS = "events.json"
F_NARR = "narrative.json"

CHANNEL_META = {
    "temperature":  {"label": "温度",     "label_en": "Temperature",   "unit": "°C",  "icon": "temp"},
    "moisture":     {"label": "土壤湿度", "label_en": "Soil moisture", "unit": "%",   "icon": "drop"},
    "voc":          {"label": "空气异味", "label_en": "Air odor",      "unit": "ppm", "icon": "wind"},
    "humidity_air": {"label": "空气湿度", "label_en": "Air humidity",  "unit": "%",   "icon": "cloud"},
    "light":        {"label": "光照",     "label_en": "Light",         "unit": "lux", "icon": "sun"},
    "sound":        {"label": "声音",     "label_en": "Sound",         "unit": "",    "icon": "sound"},
    "ph":           {"label": "酸碱 pH",  "label_en": "pH",            "unit": "",    "icon": "ph"},
    "ec":           {"label": "养分 EC",  "label_en": "Nutrient EC",   "unit": "ppm", "icon": "ec"},
}
EMOTION_META = {
    "valence":    {"label": "效价",   "label_en": "Valence",    "pos": "愉悦",   "neg": "不适",   "pos_en": "pleasant", "neg_en": "distress"},
    "arousal":    {"label": "唤醒",   "label_en": "Arousal",    "pos": "激动",   "neg": "平静",   "pos_en": "aroused",  "neg_en": "calm"},
    "safety":     {"label": "安全感", "label_en": "Safety",     "pos": "安稳",   "neg": "警觉",   "pos_en": "secure",   "neg_en": "wary"},
    "connection": {"label": "联结",   "label_en": "Connection", "pos": "被响应", "neg": "孤立",   "pos_en": "responded","neg_en": "isolated"},
    "seeking":    {"label": "探索",   "label_en": "Seeking",    "pos": "渴求",   "neg": "满足",   "pos_en": "yearning", "neg_en": "content"},
}

# ---------------- 全局共享状态 ----------------
_lock = threading.Lock()

_life = {
    "born": False,
    "life_id": None,
    "genome_path": None,
    "genome_id": None,
    "genome_display": None,
    "born_at": None,
    "lived_seconds": 0.0,      # 到 last_resume_at 为止累计的存活时长
    "last_resume_at": None,    # 本次成为活跃的时刻(运行时)
}
_state = {
    "timestamp": None,
    "raw_readings": {},
    "active_channels": {},
    "sensory_vector": [],
    "emotion": {d: 0.0 for d in EMOTION_DIMS},
    "expression": {"rgb": [150, 150, 150], "breathe_hz": 1.0, "steadiness": 1.0, "pulse_alert": False},
    "warnings": [],
    "connected": False,
    "tick": 0,
}
_history = deque(maxlen=HISTORY_LEN)
_events = deque(maxlen=EVENTS_LEN)

# 生命管理请求，由后台线程串行执行(避免torch跨线程/文件竞争)
_pending = {"action": None, "genome_path": None, "life_id": None}


# ---------------- 文件工具 ----------------
def ensure_dirs():
    os.makedirs(ACTIVE_DIR, exist_ok=True)
    os.makedirs(FROZEN_DIR, exist_ok=True)


def _ap(name):
    return os.path.join(ACTIVE_DIR, name)


def fold_lived(now=None):
    """当前累计存活时长(含本次活跃已过时间)"""
    now = now or time.time()
    base = _life["lived_seconds"]
    if _life["born"] and _life["last_resume_at"]:
        base += now - _life["last_resume_at"]
    return base


def write_active(agent, narr):
    """把当前活跃生命的完整状态落盘到 active/ 目录"""
    if not _life["born"]:
        return
    ensure_dirs()
    now = time.time()
    meta = {
        "life_id": _life["life_id"],
        "genome_path": _life["genome_path"],
        "genome_id": _life["genome_id"],
        "genome_display": _life["genome_display"],
        "born_at": _life["born_at"],
        "lived_seconds": fold_lived(now),   # 落盘的是折算后的累计时长，重启安全
        "tick": _state["tick"],
    }
    try:
        with open(_ap(F_META), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        with open(_ap(F_HISTORY), "w", encoding="utf-8") as f:
            json.dump(list(_history), f, ensure_ascii=False)
        with open(_ap(F_EVENTS), "w", encoding="utf-8") as f:
            json.dump(list(_events), f, ensure_ascii=False)
        with open(_ap(F_NARR), "w", encoding="utf-8") as f:
            json.dump(narr.snapshot(), f, ensure_ascii=False)
        if agent is not None and agent.hidden is not None:
            torch.save(agent.hidden, _ap(F_HIDDEN))
    except Exception as e:
        print(f"[dashboard] 写活跃状态失败: {e}")


def read_meta(d):
    p = os.path.join(d, F_META)
    if not os.path.exists(p):
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def load_active_into_memory(agent_holder, narr):
    """从 active/ 读取到内存(_life/_history/_events/narr/hidden)，返回 agent 或 None"""
    meta = read_meta(ACTIVE_DIR)
    if not meta or not meta.get("genome_path") or not os.path.exists(meta["genome_path"]):
        return None
    try:
        agent = LifeAgent(meta["genome_path"])
        hp = _ap(F_HIDDEN)
        if os.path.exists(hp):
            agent.hidden = torch.load(hp)
        _history.clear()
        _events.clear()
        if os.path.exists(_ap(F_HISTORY)):
            with open(_ap(F_HISTORY), "r", encoding="utf-8") as f:
                for p in json.load(f):
                    _history.append(p)
        if os.path.exists(_ap(F_EVENTS)):
            with open(_ap(F_EVENTS), "r", encoding="utf-8") as f:
                for e in json.load(f):
                    _events.append(e)
        if os.path.exists(_ap(F_NARR)):
            with open(_ap(F_NARR), "r", encoding="utf-8") as f:
                narr.restore(json.load(f))
        with _lock:
            _life.update({
                "born": True,
                "life_id": meta.get("life_id"),
                "genome_path": meta["genome_path"],
                "genome_id": meta.get("genome_id"),
                "genome_display": meta.get("genome_display"),
                "born_at": meta.get("born_at"),
                "lived_seconds": meta.get("lived_seconds", 0.0),
                "last_resume_at": time.time(),   # 断电期间不计入年龄
            })
            _state["tick"] = meta.get("tick", 0)
        return agent
    except Exception as e:
        print(f"[dashboard] 载入活跃生命失败: {e}")
        return None


def clear_active_dir():
    shutil.rmtree(ACTIVE_DIR, ignore_errors=True)
    os.makedirs(ACTIVE_DIR, exist_ok=True)


def reset_life_struct():
    with _lock:
        _life.update({
            "born": False, "life_id": None, "genome_path": None,
            "genome_id": None, "genome_display": None, "born_at": None,
            "lived_seconds": 0.0, "last_resume_at": None,
        })
        _history.clear()
        _events.clear()
        _state["tick"] = 0


def freeze_active_to_store(agent, narr):
    """把当前活跃生命封存进冷冻库"""
    if not _life["born"]:
        return
    write_active(agent, narr)  # 先落盘最新状态(已折算lived_seconds)
    ensure_dirs()
    lid = _life["life_id"] or str(int(time.time() * 1000))
    dest = os.path.join(FROZEN_DIR, lid)
    shutil.rmtree(dest, ignore_errors=True)
    try:
        shutil.move(ACTIVE_DIR, dest)
    except Exception as e:
        print(f"[dashboard] 冷冻移动失败: {e}")
    os.makedirs(ACTIVE_DIR, exist_ok=True)
    # 记录冷冻时刻
    m = read_meta(dest) or {}
    m["frozen_at"] = time.time()
    try:
        with open(os.path.join(dest, F_META), "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    reset_life_struct()


def resume_from_store(life_id):
    """把冷冻库中的某条生命解冻为活跃生命(移回 active/)"""
    src = os.path.join(FROZEN_DIR, life_id)
    if not os.path.isdir(src):
        return False
    clear_active_dir()
    shutil.rmtree(ACTIVE_DIR, ignore_errors=True)
    try:
        shutil.move(src, ACTIVE_DIR)
        return True
    except Exception as e:
        print(f"[dashboard] 解冻失败: {e}")
        return False


def list_frozen():
    out = []
    if not os.path.isdir(FROZEN_DIR):
        return out
    for lid in os.listdir(FROZEN_DIR):
        d = os.path.join(FROZEN_DIR, lid)
        if not os.path.isdir(d):
            continue
        m = read_meta(d)
        if not m:
            continue
        n_events = 0
        ep = os.path.join(d, F_EVENTS)
        if os.path.exists(ep):
            try:
                with open(ep, "r", encoding="utf-8") as f:
                    n_events = len(json.load(f))
            except Exception:
                pass
        out.append({
            "life_id": m.get("life_id", lid),
            "genome_id": m.get("genome_id"),
            "genome_display": m.get("genome_display"),
            "born_at": m.get("born_at"),
            "lived_seconds": m.get("lived_seconds", 0.0),
            "frozen_at": m.get("frozen_at"),
            "events": n_events,
        })
    out.sort(key=lambda x: x.get("frozen_at") or 0, reverse=True)
    return out


def wipe_everything():
    shutil.rmtree(STATE_DIR, ignore_errors=True)
    ensure_dirs()
    reset_life_struct()


# ---------------- 基因组 ----------------
def _genome_intro(gid):
    return {
        "tomato_soil": "扎根土壤的作物视角。在乎水分、温度、养分与光照，最怕干旱与涝渍。",
        "freshwater": "浸没水中的水生生命。对水温、酸碱与水质变化极敏感，怕缺氧与污染。",
        "indoor_air": "与人共享的室内空气本身。在乎通风、湿度与噪音，怕闷塞与嘈杂。",
    }.get(gid, "一种生态位视角。")


def _genome_intro_en(gid):
    return {
        "tomato_soil": "A soil-rooted crop's perspective. It cares about moisture, temperature, nutrients and light; it dreads drought and waterlogging.",
        "freshwater": "An aquatic life submerged in water. Acutely sensitive to water temperature, pH and water quality; it fears oxygen loss and pollution.",
        "indoor_air": "The indoor air itself, shared with people. It cares about ventilation, humidity and noise; it dreads stuffiness and clamor.",
    }.get(gid, "An ecological-niche perspective.")


def _genome_display_en(gid):
    return {
        "tomato_soil": "Soil Crop",
        "freshwater": "Freshwater Being",
        "indoor_air": "Indoor Air",
    }.get(gid, gid)


def list_genomes():
    genomes = []
    for path in sorted(glob.glob(os.path.join(GENOME_DIR, "*.json"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                g = json.load(f)
            gid = g.get("genome_id", os.path.basename(path))
            genomes.append({
                "id": gid,
                "display_name": g.get("display_name", os.path.basename(path)),
                "display_name_en": _genome_display_en(gid),
                "path": path,
                "intro": _genome_intro(gid),
                "intro_en": _genome_intro_en(gid),
            })
        except Exception:
            continue
    return genomes


def genome_path_by_id(gid):
    for g in list_genomes():
        if g["id"] == gid:
            return g["path"]
    return None


def genome_display_by_id(gid):
    for g in list_genomes():
        if g["id"] == gid:
            return g["display_name"]
    return gid


# ---------------- 后台链路 ----------------
def _make_stream(port, use_mock, genome_id):
    if use_mock:
        from mock_sensor import MockSensorStream, PRESET_BASELINES
        baseline = PRESET_BASELINES.get(genome_id, PRESET_BASELINES["indoor_air"])
        return MockSensorStream(baseline, seed=None)
    from serial_sensor import SerialSensorStream
    return SerialSensorStream(port=port)


def _do_birth(genome_path, fresh_narr):
    """创建一条全新的活跃生命(active/为空的前提下)"""
    agent = LifeAgent(genome_path)
    with open(genome_path, "r", encoding="utf-8") as f:
        g = json.load(f)
    gid = g.get("genome_id")
    born_at = time.time()
    with _lock:
        _life.update({
            "born": True,
            "life_id": str(int(born_at * 1000)),
            "genome_path": genome_path,
            "genome_id": gid,
            "genome_display": g.get("display_name"),
            "born_at": born_at,
            "lived_seconds": 0.0,
            "last_resume_at": born_at,
        })
        _state["tick"] = 0
        _history.clear()
        _events.clear()
        _events.append({"t": born_at, "text": birth_line(gid), "text_en": birth_line_en(gid),
                        "tone": "birth", "channel": None})
    write_active(agent, fresh_narr)
    return agent, gid


def pipeline_loop(port, use_mock):
    agent = None
    narr = NarrativeEngine()
    stream = None
    last_persist = 0

    ensure_dirs()
    # 启动时复活已有活跃生命
    resumed = load_active_into_memory(None, narr)
    if resumed is not None:
        agent = resumed
        stream = _make_stream(port, use_mock, _life["genome_id"])
        print(f"[dashboard] 复活活跃生命: {_life['genome_display']} (id={_life['life_id']})")

    while True:
        with _lock:
            action = _pending["action"]
            gpath = _pending["genome_path"]
            lid = _pending["life_id"]
            _pending["action"] = None

        if action:
            try:
                if action == "birth":
                    clear_active_dir()
                    narr = NarrativeEngine()
                    agent, gid = _do_birth(gpath, narr)
                    if stream is None:
                        stream = _make_stream(port, use_mock, gid)
                    elif use_mock:
                        from mock_sensor import PRESET_BASELINES
                        if gid in PRESET_BASELINES:
                            stream.baseline = dict(PRESET_BASELINES[gid])
                    print(f"[dashboard] 出生: {_life['genome_display']}")

                elif action == "rebirth":
                    clear_active_dir()          # 只清当前活跃，冷冻库不动
                    narr = NarrativeEngine()
                    agent, gid = _do_birth(gpath, narr)
                    if use_mock:
                        from mock_sensor import PRESET_BASELINES
                        if gid in PRESET_BASELINES:
                            stream.baseline = dict(PRESET_BASELINES[gid])
                    print(f"[dashboard] 重生: {_life['genome_display']}")

                elif action == "freeze":
                    if _life["born"]:
                        freeze_active_to_store(agent, narr)
                        agent = None
                        narr = NarrativeEngine()
                        print("[dashboard] 已冷冻当前生命")

                elif action == "resume":
                    # 先把当前活跃(若有)冷冻，避免丢失
                    if _life["born"]:
                        freeze_active_to_store(agent, narr)
                        agent = None
                    narr = NarrativeEngine()
                    if resume_from_store(lid):
                        agent = load_active_into_memory(None, narr)
                        if agent is not None:
                            gid = _life["genome_id"]
                            if stream is None:
                                stream = _make_stream(port, use_mock, gid)
                            elif use_mock:
                                from mock_sensor import PRESET_BASELINES
                                if gid in PRESET_BASELINES:
                                    stream.baseline = dict(PRESET_BASELINES[gid])
                            print(f"[dashboard] 已唤醒: {_life['genome_display']}")

                elif action == "death":
                    wipe_everything()
                    agent = None
                    narr = NarrativeEngine()
                    print("[dashboard] 死亡: 已清空全部数据")
            except Exception as e:
                print(f"[dashboard] 动作 {action} 失败: {e}")

        # 无活跃生命：空转等待
        if agent is None or stream is None:
            time.sleep(0.5)
            continue

        try:
            reading = stream.read()
        except Exception as e:
            print(f"[dashboard] 读取失败: {e}")
            time.sleep(1.0)
            continue

        result = agent.tick(reading, dt_seconds=TICK_DT)
        expr = emotion_to_expression(result["emotion"])
        genome_channels = agent.mapper.genome.get("channels", {})
        new_events = narr.observe(result["deviations"], genome_channels, result["emotion"])

        now = time.time()
        with _lock:
            _state.update({
                "timestamp": now,
                "raw_readings": result["raw_recorded"],
                "active_channels": genome_channels,
                "sensory_vector": result["sensory_vector"],
                "emotion": result["emotion"],
                "expression": {
                    "rgb": list(expr["rgb"]),
                    "breathe_hz": expr["breathe_hz"],
                    "steadiness": expr["steadiness"],
                    "pulse_alert": expr["pulse_alert"],
                },
                "warnings": result["warnings"],
                "connected": True,
                "tick": _state["tick"] + 1,
            })
            hp = {"t": now}
            for ch in CHANNEL_ORDER:
                hp[ch] = result["raw_recorded"].get(ch)
            for d in EMOTION_DIMS:
                hp[d] = result["emotion"][d]
            _history.append(hp)
            for ev in new_events:
                _events.append(ev)

        if now - last_persist > 20:
            write_active(agent, narr)
            last_persist = now

        if use_mock:
            time.sleep(TICK_DT)


# ---------------- Flask ----------------
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json", mimetype="application/manifest+json")


@app.route("/sw.js")
def sw():
    return send_from_directory("static", "sw.js", mimetype="application/javascript")


@app.route("/api/state")
def api_state():
    with _lock:
        life = dict(_life)
        state = dict(_state)
        history = list(_history)
        events = list(_events)

    fresh = state["timestamp"] is not None and (time.time() - state["timestamp"] < 6)
    state["fresh"] = fresh
    age = fold_lived() if life["born"] else None

    # 给旧事件（升级前生成、缺英文）补英文，保证英文界面日记也是纯英文
    for ev in events:
        if not ev.get("text_en"):
            ev["text_en"] = en_for_zh(ev.get("text", "")) or ev.get("text", "")

    return jsonify({
        "life": {
            "born": life["born"],
            "life_id": life["life_id"],
            "genome_id": life["genome_id"],
            "genome_display": life["genome_display"],
            "born_at": life["born_at"],
            "age_seconds": age,
        },
        "frozen": list_frozen(),
        "state": state,
        "history": history,
        "events": list(reversed(events)),
        "genomes": list_genomes(),
        "channel_meta": CHANNEL_META,
        "emotion_meta": EMOTION_META,
        "channel_order": CHANNEL_ORDER,
        "emotion_dims": EMOTION_DIMS,
    })


def led_state_snapshot():
    """给 LED 呼吸灯线程用的当前状态快照"""
    with _lock:
        return {
            "born": _life["born"],
            "emotion": dict(_state["emotion"]),
            "expression": dict(_state["expression"]),
        }


def _queue(action, genome_path=None, life_id=None):
    with _lock:
        _pending["action"] = action
        _pending["genome_path"] = genome_path
        _pending["life_id"] = life_id


@app.route("/api/birth", methods=["POST"])
def api_birth():
    gid = request.get_json(force=True).get("genome_id")
    path = genome_path_by_id(gid)
    if not path:
        return jsonify({"ok": False, "error": f"未知基因组: {gid}"}), 400
    with _lock:
        if _life["born"]:
            return jsonify({"ok": False, "error": "已有活跃生命"}), 409
    _queue("birth", genome_path=path)
    return jsonify({"ok": True})


@app.route("/api/rebirth", methods=["POST"])
def api_rebirth():
    gid = request.get_json(force=True).get("genome_id")
    path = genome_path_by_id(gid)
    if not path:
        return jsonify({"ok": False, "error": f"未知基因组: {gid}"}), 400
    _queue("rebirth", genome_path=path)
    return jsonify({"ok": True})


@app.route("/api/freeze", methods=["POST"])
def api_freeze():
    with _lock:
        if not _life["born"]:
            return jsonify({"ok": False, "error": "当前没有活跃生命"}), 409
    _queue("freeze")
    return jsonify({"ok": True})


@app.route("/api/resume", methods=["POST"])
def api_resume():
    lid = request.get_json(force=True).get("life_id")
    if not lid or not os.path.isdir(os.path.join(FROZEN_DIR, str(lid))):
        return jsonify({"ok": False, "error": "冷冻库中找不到该生命"}), 404
    _queue("resume", life_id=str(lid))
    return jsonify({"ok": True})


@app.route("/api/death", methods=["POST"])
def api_death():
    _queue("death")
    return jsonify({"ok": True})


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    use_mock = "--mock" in sys.argv
    port = args[0] if len(args) > 0 else DEFAULT_PORT

    print(f"[dashboard] 串口={port} mock={use_mock}")
    t = threading.Thread(target=pipeline_loop, args=(port, use_mock), daemon=True)
    t.start()

    # 呼吸灯（WS2812），失败不影响主程序
    try:
        from led_driver import LEDController
        led = LEDController(led_state_snapshot, num=int(os.environ.get("LED_NUM", "30")))
        led.start()
        print("[dashboard] LED 呼吸灯已启动")
    except Exception as e:
        print(f"[dashboard] LED 未启用: {e}")

    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)


if __name__ == "__main__":
    main()
