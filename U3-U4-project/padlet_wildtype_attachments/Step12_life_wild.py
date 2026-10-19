#!/usr/bin/env python3
"""
life_wild.py — AI生命体 · 实验A 野生型 (Wild Type)
=====================================================
纯物理传感器驱动 · 无语言模型 · 无叙事层

与实验B (life_v2.py) 的关键差异:
  - 感知来源: Arduino物理传感器 (8通道) 替代 LLM模拟世界 (15通道)
  - CfC输入: 22维 (vs 36维)
  - 移除: LLMPlaywright, Worldbook, EventTranslator
  - 新增: ArduinoSensorBridge, InternalSymbolTracker
  - 保留: CfC情绪核心, 预测引擎, 身体预算, 自主神经, 昼夜节律, 基因组, Phase1-4发育

依赖:  pip install torch ncps
       pip install pyserial  (仅Arduino真实模式)
运行:  python life_wild.py              # 模拟模式
       python life_wild.py --real COM3   # Arduino真实模式
"""

import time, math, random, datetime, os, signal, sys, json, argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# Windows GBK 终端 UTF-8 输出
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

try:
    from ncps.torch import CfC
    from ncps.wirings import AutoNCP
except ImportError:
    print("错误: 缺少 ncps 库 / missing ncps. Run: pip install ncps")
    sys.exit(1)

from sensor_bridge import (
    ArduinoSensorBridge, CH_NAMES_WILD, CH_RANGE_WILD,
    CH_DEV_WILD, SENS_DIMS_WILD, norm_wild,
)
from symbol_tracker import InternalSymbolTracker

# ═══════════════════════════════════════════════════════════════
#  全局配置
# ═══════════════════════════════════════════════════════════════

CYCLE_SEC    = 3.0   # 帧间隔(秒) —— 这是"虚拟时间"，用于发育进度/昼夜节律计算，不受下面SPEED_FACTOR影响
CFC_NEURONS  = 64
EMO_DIMS     = 5
INPUT_DIMS   = 22    # 8感觉 + 8预测误差 + 3身体预算 + 1自主 + 2昼夜
EMA_ALPHA    = 0.25
FIVE_DAYS    = int(5 * 86400 / CYCLE_SEC)   # dev_progress达到1.0(=="lifelong"/成年)所需帧数 ≈144000
SAVE_EVERY   = 200
LOG_MAX      = 5000

# 时间加速倍率：压缩"真实等待时间"，虚拟时间(昼夜节律/发育进度)不受影响。
# 25x下，跑满FIVE_DAYS帧只需 144000*3/25/3600 ≈ 4.8小时真实时间即可到达"lifelong"(成年)阶段。
SPEED_FACTOR = 25

_HERE        = os.path.dirname(os.path.abspath(__file__))
WEIGHT_FILE  = os.path.join(_HERE, "emotion_weights_wild.pt")
LOG_FILE     = os.path.join(_HERE, "wild_log.jsonl")

GROWTH_STATUS_FILE     = os.path.join(_HERE, "growth_status_wild.json")
GROWTH_MILESTONES_FILE = os.path.join(_HERE, "growth_milestones_wild.jsonl")
#   growth_timeline_wild.jsonl —— 永久成长时间线(只追加、不裁剪)，每次快照留档，
#                                 含情绪/身体/自主 + 涌现符号化指标，专供离线数据分析(对齐实验B)
GROWTH_TIMELINE_FILE   = os.path.join(_HERE, "growth_timeline_wild.jsonl")
GROWTH_SNAPSHOT_EVERY  = 50

# ═══════════════════════════════════════════════════════════════
#  基因组 (与实验B完全相同，保证先天条件一致)
# ═══════════════════════════════════════════════════════════════

GENOME = {
    "sensory_threshold_multiplier": 0.65,
    "arousal_baseline": 8.0,
    "emotional_inertia": 1.35,
    "approach_bias": 8.0,
    "novelty_valence": -4.0,
    "emotional_reactivity": 1.35,
    "safety_recovery_rate": 0.65,
    "social_need_intensity": 1.05,
}

def virtual_age(step, cycle_sec=3.0):
    real_hours = step * cycle_sec / 3600
    virtual_months = (real_hours / 120.0) * 24.0
    virtual_days = virtual_months * 30.44
    if virtual_days < 30:
        txt = f"Day {max(0,virtual_days):.0f}"
    elif virtual_months < 12:
        w = (virtual_days % 30.44) / 7
        txt = f"{virtual_months:.0f}m {w:.0f}w"
    else:
        y = int(virtual_months // 12)
        m = int(virtual_months % 12)
        txt = f"{y}y {m}m"
    return virtual_days, txt

# ═══════════════════════════════════════════════════════════════
#  发育门控
# ═══════════════════════════════════════════════════════════════

def _dev_maturity(group, progress):
    if group == 'T': return 1.0
    if group == 'H': return min(1.0, max(0.0, (progress - 0.05) / 0.15))
    if group == 'V': return min(1.0, max(0.0, (progress - 0.10) / 0.25))
    return 1.0

# ═══════════════════════════════════════════════════════════════
#  感觉预处理（习惯化/敏感化 + 发育门控）
# ═══════════════════════════════════════════════════════════════

class DualProcess:
    __slots__ = ('hab', 'sen')
    def __init__(self):
        self.hab = 1.0
        self.sen = 1.0
    def update(self, intensity, arousal):
        if intensity < 0.6:
            self.hab *= 0.997
        else:
            self.hab = min(1.0, self.hab + 0.04)
        self.hab += 0.001 * (1.0 - self.hab)
        if arousal > 70 and intensity > 0.5:
            self.sen = min(1.8, self.sen + 0.015)
        else:
            self.sen += 0.003 * (1.0 - self.sen)
    def apply(self, val):
        return val * self.hab * self.sen


class SensoryPreprocessor:
    def __init__(self):
        self.dp = {c: DualProcess() for c in CH_NAMES_WILD}

    def process(self, raw_dict, arousal, dev_progress):
        result = []
        raw_norm = []
        for c in CH_NAMES_WILD:
            nv = norm_wild(c, raw_dict[c])
            raw_norm.append(nv)
            m = _dev_maturity(CH_DEV_WILD[c], dev_progress)
            if m < 0.05:
                result.append(0.0)
                continue
            gated = nv * m + random.gauss(0, 0.02 * (1 - m))
            self.dp[c].update(gated, arousal)
            processed = self.dp[c].apply(gated)
            result.append(max(0.0, min(1.0, processed)))
        return (torch.tensor(result, dtype=torch.float32),
                torch.tensor(raw_norm, dtype=torch.float32))

# ═══════════════════════════════════════════════════════════════
#  预测引擎 (8通道版)
# ═══════════════════════════════════════════════════════════════

class PredictionEngine(nn.Module):
    def __init__(self):
        super().__init__()
        # 输入: sensory(8) + emotion(5) = 13
        self.net = nn.Sequential(
            nn.Linear(13, 32), nn.ReLU(),
            nn.Linear(32, 24), nn.ReLU(),
            nn.Linear(24, SENS_DIMS_WILD), nn.Sigmoid(),
        )
        self.optim = optim.Adam(self.parameters(), lr=0.005)
        self.prev_sensory = None
        self.prev_emotions = None
        self.prev_pred = None

    def step(self, sensory_norm, emotion_norm, lr=None):
        if lr is not None:
            for pg in self.optim.param_groups:
                pg['lr'] = lr
        pred_loss = 0.0
        if self.prev_pred is not None:
            with torch.no_grad():
                errors = sensory_norm - self.prev_pred
            x = torch.cat([self.prev_sensory, self.prev_emotions]).unsqueeze(0)
            pred = self.net(x).squeeze(0)
            loss = F.mse_loss(pred, sensory_norm.detach())
            self.optim.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(self.parameters(), 1.0)
            self.optim.step()
            pred_loss = loss.item()
        else:
            errors = torch.zeros(SENS_DIMS_WILD)
        self.prev_sensory = sensory_norm.detach().clone()
        self.prev_emotions = emotion_norm.detach().clone()
        with torch.no_grad():
            x = torch.cat([sensory_norm, emotion_norm]).unsqueeze(0)
            self.prev_pred = self.net(x).squeeze(0).clone()
        return errors, pred_loss

# ═══════════════════════════════════════════════════════════════
#  情绪核心 (CfC + AutoNCP) — 22维输入版
# ═══════════════════════════════════════════════════════════════

class EmotionCore:
    def __init__(self):
        self.wiring   = AutoNCP(CFC_NEURONS, EMO_DIMS)
        self.cfc      = CfC(INPUT_DIMS, self.wiring, batch_first=True,
                            return_sequences=True)
        self.hidden   = torch.zeros(1, CFC_NEURONS)
        self.smoothed = torch.tensor([0.0, 50.0, 50.0, 50.0, 50.0])
        self.step_count = 0
        self.optim    = optim.Adam(self.cfc.parameters(), lr=0.008)

    def _lr(self):
        p = self.step_count / FIVE_DAYS
        if   p < 0.15: return (0.0080, 0.0020, 0.0060)
        elif p < 0.35: return (0.0080, 0.0040, 0.0050)
        elif p < 0.55: return (0.0040, 0.0030, 0.0030)
        elif p < 0.75: return (0.0020, 0.0010, 0.0020)
        elif p < 1.00: return (0.0008, 0.0005, 0.0010)
        else:          return (0.0003, 0.0002, 0.0005)

    def dev_progress(self):
        return min(1.0, self.step_count / FIVE_DAYS)

    def _hebbian_update(self, reward):
        _, hebb_lr, _ = self._lr()
        if abs(reward) < 0.01 or hebb_lr < 1e-7:
            return
        for name, param in self.cfc.named_parameters():
            if 'weight' in name and param.dim() == 2 and param.shape[0] == EMO_DIMS:
                with torch.no_grad():
                    param.data += hebb_lr * reward * 0.005 * torch.sign(param.data)
                    param.data *= (1.0 - 1e-5)

    def _prune_weights(self):
        p = self.step_count / FIVE_DAYS
        if p < 0.35 or self.step_count % 1000 != 0:
            return
        prune_rate = min(0.08, (p - 0.35) / 0.65 * 0.08)
        for name, param in self.cfc.named_parameters():
            if 'weight' in name and param.dim() == 2:
                with torch.no_grad():
                    thresh = torch.quantile(param.data.abs(), prune_rate)
                    param.data *= (param.data.abs() > thresh).float()

    def forward_and_learn(self, sensory, pred_errors, target,
                          body_tensor, autonomic_tensor, circ_tensor,
                          reward=0.0):
        self.step_count += 1
        readout_lr, _, _ = self._lr()
        for pg in self.optim.param_groups:
            pg['lr'] = readout_lr

        # 组装22维输入
        x = torch.cat([sensory, pred_errors, body_tensor,
                       autonomic_tensor, circ_tensor])
        x = x.unsqueeze(0).unsqueeze(0)

        self.cfc.train()
        raw_out, h_new = self.cfc(x, self.hidden)
        self.hidden = h_new.detach()
        raw = raw_out.squeeze(0).squeeze(0)

        scaled = torch.empty(5)
        scaled[0] = torch.tanh(raw[0]) * 100.0
        scaled[1:] = torch.sigmoid(raw[1:]) * 100.0

        loss = F.mse_loss(scaled, target)
        self.optim.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.cfc.parameters(), 1.0)
        self.optim.step()

        self._hebbian_update(reward)
        self._prune_weights()

        sd = scaled.detach()
        ema_a = EMA_ALPHA / GENOME.get('emotional_inertia', 1.0)
        self.smoothed = ema_a * sd + (1 - ema_a) * self.smoothed
        self.smoothed[0] = max(-100, min(100, self.smoothed[0].item()))
        for i in range(1, 5):
            self.smoothed[i] = max(0, min(100, self.smoothed[i].item()))
        self.smoothed = torch.tensor([
            self.smoothed[i].item() if isinstance(self.smoothed[i], torch.Tensor)
            else self.smoothed[i] for i in range(5)
        ])

        return self.smoothed.clone(), loss.item(), readout_lr

# ═══════════════════════════════════════════════════════════════
#  训练信号生成器 (野生型 — 无社交事件)
# ═══════════════════════════════════════════════════════════════

class WildTargetGenerator:
    """
    野生型训练信号。
    与实验B的TargetGenerator核心规则相同，但:
    - 连接感完全由PIR(人体红外)驱动而非叙事社交信号
    - 无"照顾者进入"等事件，只有物理存在/不存在
    - 喂食信号不存在，body_budget只靠时间衰减+光照恢复(模拟昼夜新陈代谢)
    """

    def __init__(self):
        self.prev_raw = None
        self.no_presence_count = 0
        self.prev_val_t = 0.0
        self.valence_neg_count = 0
        self.seeking_frustration = 0

    def compute(self, raw_dict, raw_norm, pred_errors, emotions,
                autonomic_zone=2, body_infl=(0,0,0), circ_mod=(0.5,0.5)):
        G = GENOME
        re = G['emotional_reactivity']
        st = G['sensory_threshold_multiplier']
        pa_mod, aro_circ = circ_mod

        val_t, aro_t, saf_t, con_t, see_t = 0.0, 50.0, 50.0, 50.0, 50.0

        # ── 效价 ──
        # 温度偏离舒适区
        temp = raw_dict['temperature']
        val_t += -0.15 * (temp - 25) ** 2 * re
        # 压力刺激 (中等压力=舒适)
        prs = raw_dict['pressure']
        val_t += max(-20, -(prs - 40) ** 2 / 120 + 15) * re
        # 预测误差影响效价
        pe_mean = pred_errors.mean().item()
        val_t += pe_mean * 40 * re
        # 昼夜节律
        val_t += (pa_mod - 0.5) * 15

        # ── 唤醒度 ──
        aro_t = 40.0 + G['arousal_baseline']
        if self.prev_raw is not None:
            delta = (raw_norm - self.prev_raw).abs()
            # 8通道权重 (声音和运动变化对唤醒影响最大)
            weights = torch.tensor([0.8, 2.0, 0.5, 0.3, 1.5, 0.5, 1.0, 0.8])
            thresholds = torch.tensor([0.10, 0.12, 0.08, 0.10, 0.15, 0.15, 0.10, 0.15]) * st
            surprises = torch.relu(delta - thresholds) * weights
            aro_t += surprises.sum().item() * 80 * re
        aro_t += (raw_dict['luminance'] / 1000) * 12
        aro_t += (aro_circ - 0.5) * 10
        aro_t = max(0, min(100, aro_t))

        # ── 安全感 ──
        saf_t = 65.0
        if self.prev_raw is not None:
            # 声音突变
            db_delta = abs(raw_norm[1].item() - self.prev_raw[1].item())
            if db_delta > 0.2 * st and raw_dict['sound_level'] > 60 * st:
                saf_t -= 30 * re
            # 运动突变
            mot_delta = abs(raw_norm[6].item() - self.prev_raw[6].item())
            if mot_delta > 0.2 * st:
                saf_t -= 20 * re
        if raw_dict['luminance'] < 30:
            saf_t -= 8 * re
        if raw_dict['temperature'] < 15 or raw_dict['temperature'] > 40:
            saf_t -= 25 * re
        novelty = pred_errors.abs().mean().item()
        saf_t += G['novelty_valence'] * novelty * 30
        saf_t = max(0, min(100, saf_t))

        # ── 连接感 (纯PIR驱动) ──
        presence = raw_dict['presence']
        if presence > 0.5:
            self.no_presence_count = 0
            con_t = 50 + presence * 30
            # 如果有压力+温暖(被抱持的物理信号)
            if raw_dict['pressure'] > 20 and raw_dict['temperature'] > 28:
                con_t = min(100, con_t + 20)
        else:
            self.no_presence_count += 1
            self.no_presence_count = min(self.no_presence_count, 400)
            ns = self.no_presence_count
            if ns <= 50:
                con_t = max(10, 50 - ns * 0.8)
                aro_t = min(100, aro_t + 5 * re)
            elif ns <= 200:
                con_t = max(5, 10 - (ns - 50) * 0.3)
                val_t -= 5 * re
            else:
                con_t = min(con_t, 14)
        con_t = max(0, min(100, con_t))

        # ── 探索欲 ──
        safe_curious = emotions[2].item() > 45 and 25 < emotions[1].item() < 75
        see_t = 45.0 + G['approach_bias']
        if safe_curious:
            if novelty > 0.08:
                see_t += novelty * 200 * re
            elif novelty < 0.02:
                see_t += 8
                self.seeking_frustration += 1
        else:
            see_t -= 10
            self.seeking_frustration = max(0, self.seeking_frustration - 1)
        if self.seeking_frustration > 50:
            val_t -= min(15, self.seeking_frustration * 0.1) * re
        see_t = max(0, min(100, see_t))

        # ── 交叉调制规则 (保留核心5条) ──
        emo = [x.item() if isinstance(x, torch.Tensor) else x for x in emotions]

        # 低安全→放大唤醒
        if emo[2] < 40:
            gain = 1.0 + ((40 - emo[2]) / 40) ** 2
            aro_t = min(100, 50 + (aro_t - 50) * gain)

        # 低安全+负效价→效价螺旋
        if emo[2] < 40 and val_t < 0:
            val_t *= 1.0 + 0.6 * ((40 - emo[2]) / 40)

        # 身体预算缺口
        b_val, b_aro, b_saf = body_infl
        val_t += b_val
        aro_t = min(100, aro_t + b_aro)
        saf_t = max(0, saf_t + b_saf)

        # 预测误差门控
        if novelty > 0.15:
            if emo[2] > 55:
                see_t = min(100, see_t + novelty * 30)
            else:
                aro_t = min(100, aro_t + novelty * 20)
                val_t -= novelty * 10

        # 持续负效价抑制
        if val_t < -10:
            self.valence_neg_count += 1
        else:
            self.valence_neg_count = max(0, self.valence_neg_count - 1)
        if self.valence_neg_count > 20:
            see_t = max(0, see_t - min(20, self.valence_neg_count * 0.3))
            con_t = max(0, con_t - min(10, self.valence_neg_count * 0.15))

        # ── 自主神经门控 ──
        if autonomic_zone == 0:
            val_t = val_t * 0.3 - 30.0
            aro_t = aro_t * 0.5 + 10.0
            saf_t *= 0.3; con_t *= 0.3; see_t *= 0.2
        elif autonomic_zone == 1:
            if val_t < 0: val_t *= 1.4
            aro_t = min(100.0, aro_t + 20.0)
            con_t *= 0.7; see_t *= 0.6

        # 钳位
        val_t = max(-100, min(100, val_t))
        aro_t = max(0, min(100, aro_t))
        saf_t = max(0, min(100, saf_t))
        con_t = max(0, min(100, con_t))
        see_t = max(0, min(100, see_t))

        reward = (val_t - self.prev_val_t) * 0.01
        self.prev_val_t = val_t
        self.prev_raw = raw_norm.clone()

        return (torch.tensor([val_t, aro_t, saf_t, con_t, see_t], dtype=torch.float32),
                reward)

# ═══════════════════════════════════════════════════════════════
#  昼夜节律振荡器 (与实验B相同)
# ═══════════════════════════════════════════════════════════════

class CircadianOscillator:
    def get(self, dev_progress):
        h = datetime.datetime.now()
        hour = h.hour + h.minute / 60.0
        pa_phase = (hour - 10.0) / 24.0 * 2 * math.pi
        pa_mod = math.sin(pa_phase) * 0.5 + 0.5
        aro_phase = (hour - 15.0) / 24.0 * 2 * math.pi
        aro_mod = math.sin(aro_phase) * 0.3 + 0.5
        mat = min(1.0, dev_progress / 0.25)
        pa_mod = 0.5 * (1 - mat) + pa_mod * mat
        aro_mod = 0.5 * (1 - mat) + aro_mod * mat
        return pa_mod, aro_mod

    def as_tensor(self, dev_progress):
        pa, ar = self.get(dev_progress)
        return torch.tensor([pa, ar], dtype=torch.float32)

# ═══════════════════════════════════════════════════════════════
#  身体预算系统 (野生型适配)
# ═══════════════════════════════════════════════════════════════

class BodyBudgetSystem:
    """
    野生型身体预算。
    与实验B不同: 没有"喂奶"事件，能量通过昼夜周期自然恢复。
    模拟一个自主维持新陈代谢的有机体。
    """
    def __init__(self):
        self.energy = 0.80
        self.hydration = 0.85
        self.thermal = 0.80

    def update(self, raw_dict):
        dt = CYCLE_SEC / 3600.0
        # 自然代谢消耗
        self.energy -= 0.015 * dt
        self.hydration -= 0.012 * dt
        # 光照驱动能量恢复 (模拟光合作用般的基础代谢节律)
        lux = raw_dict['luminance']
        if lux > 100:
            self.energy = min(1.0, self.energy + 0.005 * dt * 60)
        # 低光=睡眠恢复
        if lux < 50 and raw_dict['sound_level'] < 35:
            self.energy = min(1.0, self.energy + 0.008 * dt * 60)
            self.hydration = min(1.0, self.hydration + 0.003 * dt * 60)
        # 温度调节
        temp = raw_dict['temperature']
        if 22 <= temp <= 30:
            self.thermal = min(1.0, self.thermal + 0.004)
        elif temp < 15 or temp > 40:
            self.thermal -= 0.020
        else:
            self.thermal -= 0.001
        # 钳位
        self.energy = max(0.10, min(1.0, self.energy))
        self.hydration = max(0.10, min(1.0, self.hydration))
        self.thermal = max(0.10, min(1.0, self.thermal))

    def as_tensor(self):
        return torch.tensor([self.energy, self.hydration, self.thermal], dtype=torch.float32)

    def deficit(self):
        return 1.0 - (self.energy + self.hydration + self.thermal) / 3.0

    def emotion_influence(self):
        d = self.deficit()
        return (-d * 30.0, d * 20.0, -d * 15.0)

# ═══════════════════════════════════════════════════════════════
#  自主神经控制器 (与实验B相同)
# ═══════════════════════════════════════════════════════════════

class AutonomicController:
    def __init__(self):
        self.state = 2.0
        self.zone = 2

    def update(self, safety, arousal, presence):
        if safety > 60 and arousal < 70:
            target = 2.0
        elif safety > 35 or arousal < 85:
            target = 1.0
        else:
            target = 0.0
        if presence > 0.5:
            target = min(2.0, target + 0.5)
        self.state += 0.05 * (target - self.state)
        self.zone = max(0, min(2, round(self.state)))

    def as_tensor(self):
        return torch.tensor([self.state / 2.0], dtype=torch.float32)

    def zone_name(self):
        return ['DorsalVagal(freeze)', 'Sympathetic(fight)', 'VentralVagal(safe)'][self.zone]

# ═══════════════════════════════════════════════════════════════
#  显示工具
# ═══════════════════════════════════════════════════════════════

EMO_NAMES = ['Val', 'Aro', 'Saf', 'Con', 'See']

def _dev_stage(p):
    if   p < 0.15: return "synaptogenesis"
    elif p < 0.35: return "critical_period"
    elif p < 0.55: return "pruning_start"
    elif p < 0.75: return "pruning_accel"
    elif p < 1.00: return "maturation"
    else:          return "lifelong"

def _ts():
    return datetime.datetime.now().strftime("%H:%M:%S")

def _json_default(o):
    """JSON 序列化兜底：把 numpy 标量/数组转成原生 Python 类型。
    symbol_tracker 里的 symbol_score/structure_ratio 等是 numpy.float32，
    json 无法直接序列化会抛 TypeError，之前被 except 吞掉导致日志静默写坏。"""
    import numpy as _np
    if isinstance(o, _np.integer):
        return int(o)
    if isinstance(o, _np.floating):
        return float(o)
    if isinstance(o, _np.ndarray):
        return o.tolist()
    if isinstance(o, _np.bool_):
        return bool(o)
    return str(o)

def append_growth_milestone(entry: dict):
    """向 growth_milestones_wild.jsonl 追加一条永久记录（发育阶段跃迁/会话起止等）"""
    entry = dict(entry)
    entry["real_ts"] = datetime.datetime.now().isoformat(timespec="seconds")
    try:
        with open(GROWTH_MILESTONES_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False, default=_json_default) + '\n')
    except Exception:
        pass

def append_growth_timeline(entry: dict):
    """向 growth_timeline_wild.jsonl 追加一条永久成长时间线记录(每50帧)，只增不删，供离线数据分析。"""
    entry = dict(entry)
    entry["real_ts"] = datetime.datetime.now().isoformat(timespec="seconds")
    try:
        with open(GROWTH_TIMELINE_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False, default=_json_default) + '\n')
    except Exception:
        pass

def write_growth_status(status: dict):
    """覆盖写 growth_status_wild.json —— 当前成长状态快照。
    先写临时文件再原子替换，避免读取方读到写了一半的半截 JSON。"""
    status = dict(status)
    status["real_ts"] = datetime.datetime.now().isoformat(timespec="seconds")
    try:
        tmp = GROWTH_STATUS_FILE + ".tmp"
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2, default=_json_default)
        os.replace(tmp, GROWTH_STATUS_FILE)
    except Exception:
        pass

# ═══════════════════════════════════════════════════════════════
#  权重保存/加载
# ═══════════════════════════════════════════════════════════════

def save_all(core, pred, preproc, tgt, body, auto, tracker):
    torch.save({
        'cfc': core.cfc.state_dict(),
        'cfc_optim': core.optim.state_dict(),
        'hidden': core.hidden,
        'smoothed': core.smoothed,
        'step_count': core.step_count,
        'pred_net': pred.state_dict(),
        'pred_optim': pred.optim.state_dict(),
        'dp_states': {c: (dp.hab, dp.sen) for c, dp in preproc.dp.items()},
        'tgt_state': {
            'no_presence': tgt.no_presence_count,
            'prev_val_t': tgt.prev_val_t,
            'valence_neg_cnt': tgt.valence_neg_count,
            'seek_frust': tgt.seeking_frustration,
        },
        'body': {
            'energy': body.energy,
            'hydration': body.hydration,
            'thermal': body.thermal,
        },
        'auto_state': auto.state,
    }, WEIGHT_FILE)
    tracker.save_state()


def load_all(core, pred, preproc, tgt, body, auto, tracker):
    if not os.path.exists(WEIGHT_FILE):
        print(f"[Init] No checkpoint, starting fresh")
        return
    ckpt = torch.load(WEIGHT_FILE, weights_only=False)
    core.cfc.load_state_dict(ckpt['cfc'])
    core.optim.load_state_dict(ckpt['cfc_optim'])
    core.hidden = ckpt['hidden']
    core.smoothed = ckpt['smoothed']
    core.step_count = ckpt['step_count']
    pred.load_state_dict(ckpt['pred_net'])
    pred.optim.load_state_dict(ckpt['pred_optim'])
    for c, (h, s) in ckpt.get('dp_states', {}).items():
        if c in preproc.dp:
            preproc.dp[c].hab = h
            preproc.dp[c].sen = s
    ts = ckpt.get('tgt_state', {})
    tgt.no_presence_count = ts.get('no_presence', 0)
    tgt.prev_val_t = ts.get('prev_val_t', 0.0)
    tgt.valence_neg_count = ts.get('valence_neg_cnt', 0)
    tgt.seeking_frustration = ts.get('seek_frust', 0)
    bb = ckpt.get('body', {})
    body.energy = bb.get('energy', 0.8)
    body.hydration = bb.get('hydration', 0.85)
    body.thermal = bb.get('thermal', 0.8)
    auto.state = float(ckpt.get('auto_state', 2.0))
    auto.zone = max(0, min(2, round(auto.state)))
    tracker.load_state()
    h = core.step_count * CYCLE_SEC / 3600
    print(f"[Init] Checkpoint loaded — {core.step_count} steps ({h:.1f}h)")

# ═══════════════════════════════════════════════════════════════
#  主循环
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='AI Life Wild Type')
    parser.add_argument('--real', type=str, default=None,
                       help='Arduino串口 (e.g. COM3, /dev/ttyUSB0)')
    parser.add_argument('--baud', type=int, default=115200)
    args = parser.parse_args()

    mode = 'real' if args.real else 'sim'
    port = args.real or 'COM3'

    _eta_h = FIVE_DAYS * CYCLE_SEC / SPEED_FACTOR / 3600

    print("=" * 70)
    print("  AI Life · Experiment A · WILD TYPE")
    print(f"  CfC({CFC_NEURONS}) + AutoNCP | 5D-emo | 8ch sensors | NO LANGUAGE")
    print(f"  Sensor mode: {mode.upper()}" + (f" ({port})" if mode == 'real' else " (simulated)"))
    print(f"  Frame: {CYCLE_SEC}s | 5-day cycle: {FIVE_DAYS} frames")
    print(f"  时间加速 Speed-up: {SPEED_FACTOR}x | 预计到达'lifelong'(成年)阶段所需真实时间 "
          f"ETA to adulthood: ≈{_eta_h:.1f}h")
    print("  Ctrl+C to exit")
    print("=" * 70)
    print()

    # 初始化
    bridge   = ArduinoSensorBridge(mode=mode, port=port, cycle_sec=CYCLE_SEC)
    preproc  = SensoryPreprocessor()
    pred     = PredictionEngine()
    core     = EmotionCore()
    tgt      = WildTargetGenerator()
    circ     = CircadianOscillator()
    body     = BodyBudgetSystem()
    auto     = AutonomicController()
    tracker  = InternalSymbolTracker(
        n_clusters=8, hidden_dim=CFC_NEURONS, save_dir=_HERE
    )

    bridge.start()
    load_all(core, pred, preproc, tgt, body, auto, tracker)

    running = [True]
    def on_exit(sig, frame):
        running[0] = False
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)

    emo_norm = torch.tensor([0.0, 0.5, 0.5, 0.5, 0.5])

    prev_stage = [_dev_stage(core.dev_progress())]
    _, _v_age_txt0 = virtual_age(core.step_count, CYCLE_SEC)
    append_growth_milestone({
        "type": "session_start",
        "step": core.step_count,
        "dev_progress": round(core.dev_progress(), 4),
        "stage": prev_stage[0],
        "virtual_age": _v_age_txt0,
        "speed_factor": SPEED_FACTOR,
    })

    while running[0]:
        t0 = time.time()

        # ① 传感器读取
        raw_dict = bridge.step()

        # ② 感觉预处理
        dp = core.dev_progress()
        aro = core.smoothed[1].item() if isinstance(core.smoothed[1], torch.Tensor) else core.smoothed[1]
        processed, raw_norm = preproc.process(raw_dict, aro, dp)

        # ③ 子系统更新
        pa_mod, aro_circ = circ.get(dp)
        circ_tensor = circ.as_tensor(dp)
        body.update(raw_dict)
        body_tensor = body.as_tensor()
        body_infl = body.emotion_influence()
        emo_list = [x.item() if isinstance(x, torch.Tensor) else x for x in core.smoothed]
        auto.update(safety=emo_list[2], arousal=emo_list[1],
                   presence=raw_dict.get('presence', 0))
        auto_tensor = auto.as_tensor()

        # ④ 预测引擎
        _, _, pred_lr = core._lr()
        pred_errors, pred_loss = pred.step(processed, emo_norm, lr=pred_lr)

        # ⑤ 训练信号
        target, reward = tgt.compute(
            raw_dict, raw_norm, pred_errors, core.smoothed,
            autonomic_zone=auto.zone,
            body_infl=body_infl,
            circ_mod=(pa_mod, aro_circ),
        )

        # ⑥ 情绪核心
        emotions, emo_loss, lr = core.forward_and_learn(
            processed, pred_errors, target,
            body_tensor, auto_tensor, circ_tensor,
            reward=reward,
        )

        emo_norm = torch.tensor([emotions[i].item() / 100.0 for i in range(5)])

        # ⑦ 符号追踪
        symbol_idx = tracker.step(core.hidden)

        # ⑧ 控制台输出
        e = [x.item() if isinstance(x, torch.Tensor) else x for x in emotions]
        stage = _dev_stage(dp)
        ts = _ts()
        _, v_age = virtual_age(core.step_count, CYCLE_SEC)
        sym_report = tracker.report()

        print(f"[{ts}] Lux{raw_dict['luminance']:5.0f} dB{raw_dict['sound_level']:4.0f} "
              f"T{raw_dict['temperature']:4.1f}C H{raw_dict['humidity']:3.0f}% "
              f"PIR{'ON' if raw_dict['presence']>0.5 else '--'} "
              f"Prs{raw_dict['pressure']:4.1f} Mot{raw_dict['motion']:5.2f}")
        print(f"[{ts}] Val{e[0]:+6.1f} Aro{e[1]:5.1f} Saf{e[2]:5.1f} "
              f"Con{e[3]:5.1f} See{e[4]:5.1f}")
        print(f"[{ts}] EL:{emo_loss:.4f} PL:{pred_loss:.4f} lr:{lr:.5f} "
              f"#{core.step_count} [{stage}] {v_age}")
        print(f"[{ts}] {auto.zone_name()} | "
              f"Nrg{body.energy:.2f} H2O{body.hydration:.2f} Thm{body.thermal:.2f}")
        print(f"[{ts}] Symbol={symbol_idx} | "
              f"score={sym_report['symbol_score']:.3f} "
              f"entropy={sym_report['transition_entropy']:.3f} "
              f"struct={sym_report['structure_ratio']:.3f} "
              f"active={sym_report['n_active_clusters']}")
        if sym_report.get('dominant_sequences'):
            print(f"[{ts}] TopSeq: {' | '.join(sym_report['dominant_sequences'][:3])}")
        print()

        # ⑨ JSONL日志
        log_entry = {
            "t": ts, "step": core.step_count, "stage": stage,
            "emo_loss": round(emo_loss, 5), "pred_loss": round(pred_loss, 5),
            "lr": round(lr, 6), "dev": round(dp, 4),
            "e": [round(x, 1) for x in e],
            "s": {c: round(raw_dict[c], 2) for c in CH_NAMES_WILD},
            "v_age": v_age,
            "auto_zone": auto.zone,
            "body": [round(body.energy, 3), round(body.hydration, 3), round(body.thermal, 3)],
            "circ_pa": round(pa_mod, 3),
            "reward": round(reward, 4),
            "symbol": symbol_idx,
            "symbol_score": sym_report.get('symbol_score', 0),
            "structure_ratio": sym_report.get('structure_ratio', 0),
            "mode": bridge.get_mode(),
        }
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False, default=_json_default) + '\n')
            if core.step_count % 500 == 0:
                try:
                    with open(LOG_FILE, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    if len(lines) > LOG_MAX:
                        with open(LOG_FILE, 'w', encoding='utf-8') as f:
                            f.writelines(lines[-LOG_MAX:])
                except: pass
        except: pass

        # ⑨.5 成长记录 —— 阶段跃迁永久记录 + 周期性状态快照
        if stage != prev_stage[0]:
            append_growth_milestone({
                "type": "stage_transition",
                "step": core.step_count,
                "dev_progress": round(dp, 4),
                "from_stage": prev_stage[0],
                "to_stage": stage,
                "virtual_age": v_age,
                "emotion": {"valence": round(e[0], 1), "arousal": round(e[1], 1),
                            "safety": round(e[2], 1), "connection": round(e[3], 1),
                            "seeking": round(e[4], 1)},
                "symbol_score": round(sym_report.get('symbol_score', 0), 4),
                "is_adulthood": stage == "lifelong",
            })
            if stage == "lifelong":
                print("\n" + "★" * 70)
                print(f"[{ts}] 已进入'lifelong'阶段 —— 发育进度100%，视为成年 "
                      f"/ Reached 'lifelong' stage — 100% developed, treated as adulthood")
                print("★" * 70 + "\n")
            prev_stage[0] = stage

        if core.step_count % GROWTH_SNAPSHOT_EVERY == 0:
            write_growth_status({
                "step": core.step_count,
                "dev_progress": round(dp, 4),
                "stage": stage,
                "virtual_age": v_age,
                "emotion": {"valence": round(e[0], 1), "arousal": round(e[1], 1),
                            "safety": round(e[2], 1), "connection": round(e[3], 1),
                            "seeking": round(e[4], 1)},
                "autonomic_zone": auto.zone_name(),
                "body": {"energy": round(body.energy, 3), "hydration": round(body.hydration, 3),
                          "thermal": round(body.thermal, 3)},
                "symbol_score": round(sym_report.get('symbol_score', 0), 4),
                "transition_entropy": round(sym_report.get('transition_entropy', 0), 4),
                "structure_ratio": round(sym_report.get('structure_ratio', 0), 4),
                "n_active_clusters": sym_report.get('n_active_clusters', 0),
                "sensor_mode": bridge.get_mode(),
                "speed_factor": SPEED_FACTOR,
            })

            # 永久成长时间线：同频追加一条不裁剪的完整快照，专供离线数据分析(对齐实验B)
            append_growth_timeline({
                "step": core.step_count,
                "runtime_hours": round(core.step_count * CYCLE_SEC / 3600, 2),
                "virtual_age": v_age,
                "dev_progress": round(dp, 4),
                "dev_stage": stage,
                "emotion": {"valence": round(e[0], 1), "arousal": round(e[1], 1),
                            "safety": round(e[2], 1), "connection": round(e[3], 1),
                            "seeking": round(e[4], 1)},
                "autonomic_zone": auto.zone_name(),
                "body_budget": {"energy": round(body.energy, 3),
                                 "hydration": round(body.hydration, 3),
                                 "thermal": round(body.thermal, 3)},
                # 涌现符号化指标(实验A特有：无语言，观察内部符号系统自组织)
                "symbol": symbol_idx,
                "symbol_score": round(sym_report.get('symbol_score', 0), 4),
                "transition_entropy": round(sym_report.get('transition_entropy', 0), 4),
                "structure_ratio": round(sym_report.get('structure_ratio', 0), 4),
                "n_active_clusters": sym_report.get('n_active_clusters', 0),
                "sensor_mode": bridge.get_mode(),
            })

        # ⑩ 自动保存
        if core.step_count % SAVE_EVERY == 0:
            save_all(core, pred, preproc, tgt, body, auto, tracker)
            print(f"    [Save] Checkpoint saved (step {core.step_count})\n")

        # ⑩.5 发育封顶自动优雅停止：到达 lifelong(2岁/14.4万步)即停，不再空烧到6岁
        if core.step_count >= FIVE_DAYS:
            append_growth_milestone({
                "type": "session_end_at_maturation",
                "step": core.step_count,
                "dev_progress": round(dp, 4),
                "stage": stage,
                "virtual_age": v_age,
                "reason": "reached developmental cap (dev=1.0, ~2岁)",
            })
            print(f"\n[{_ts()}] 发育封顶(step={core.step_count}, dev=1.0, ≈2岁) —— 自动结束训练，不再空烧。\n")
            running[0] = False

        # 等待下一帧（真实等待时间被SPEED_FACTOR压缩，虚拟时间/发育进度不受影响）
        elapsed = time.time() - t0
        sleep_t = max(0, CYCLE_SEC / SPEED_FACTOR - elapsed)
        if sleep_t > 0 and running[0]:
            time.sleep(sleep_t)

    # 退出
    print(f"\n[{_ts()}] Exiting — saving...")
    bridge.stop()
    save_all(core, pred, preproc, tgt, body, auto, tracker)
    h = core.step_count * CYCLE_SEC / 3600
    _, v = virtual_age(core.step_count, CYCLE_SEC)
    append_growth_milestone({
        "type": "session_end",
        "step": core.step_count,
        "dev_progress": round(core.dev_progress(), 4),
        "stage": prev_stage[0],
        "virtual_age": v,
    })
    print(f"[{_ts()}] Saved → {WEIGHT_FILE} ({h:.1f}h / {core.step_count} steps / {v})")


if __name__ == "__main__":
    main()
