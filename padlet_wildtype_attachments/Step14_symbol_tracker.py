#!/usr/bin/env python3
"""
symbol_tracker.py — 内部符号涌现监测器
=========================================
实验A（野生型）最核心的观测工具。

功能:
  1. 持续记录CfC隐藏状态 h(t) ∈ R^64
  2. 在线K-Means聚类：检测隐藏状态是否自发形成稳定的"吸引子"
  3. 转换频率矩阵：追踪状态之间的转移模式
  4. 符号稳定性指标：量化内部表征的结构化程度

理论依据:
  如果CfC在没有语言介入的情况下，仅通过感官-情绪闭环学习，
  其隐藏状态空间中自发涌现出离散的、可重复访问的区域，
  那么这些区域就是"原始符号"——无需人类语言的内部范畴。

  这是实验A vs 实验B最关键的比较点:
  - 实验B的符号空间被语言锚定（语言是外部范畴化工具）
  - 实验A的符号空间（如果存在的话）完全是内生的
"""

import torch
import numpy as np
import json, os, datetime, threading
from collections import deque

# ═══════════════════════════════════════════════════════════════
#  在线 Mini-Batch K-Means
# ═══════════════════════════════════════════════════════════════

class OnlineKMeans:
    """
    轻量在线K-Means，不需要sklearn。
    随着新数据到来逐步更新聚类中心。
    """

    def __init__(self, k=8, dim=64, lr=0.01):
        self.k = k
        self.dim = dim
        self.lr = lr
        self.centers = None          # (k, dim) 延迟初始化
        self.counts = np.zeros(k)    # 每个簇被访问次数
        self._init_buffer = []       # 前k个样本用于初始化
        self._initialized = False

    def update(self, x):
        """
        x: numpy array (dim,) — 单个隐藏状态向量
        返回: 最近簇的索引 (0 ~ k-1)
        """
        x = np.asarray(x, dtype=np.float32)

        if not self._initialized:
            self._init_buffer.append(x.copy())
            if len(self._init_buffer) >= self.k * 3:
                # 用前 k*3 个样本的K-Means++初始化
                self._kmeans_pp_init()
                self._initialized = True
            return 0  # 初始化期间返回0

        # 找最近中心
        dists = np.linalg.norm(self.centers - x, axis=1)
        idx = np.argmin(dists)
        self.counts[idx] += 1

        # 在线更新中心（学习率随访问次数衰减）
        effective_lr = self.lr / (1 + self.counts[idx] * 0.001)
        self.centers[idx] += effective_lr * (x - self.centers[idx])

        return int(idx)

    def _kmeans_pp_init(self):
        """K-Means++ 初始化"""
        data = np.stack(self._init_buffer)
        n = len(data)
        centers = [data[np.random.randint(n)]]

        for _ in range(1, self.k):
            dists = np.min([np.linalg.norm(data - c, axis=1)**2 for c in centers], axis=0)
            probs = dists / (dists.sum() + 1e-10)
            idx = np.random.choice(n, p=probs)
            centers.append(data[idx])

        self.centers = np.stack(centers)
        self._init_buffer = []  # 释放内存

    def get_stats(self):
        if not self._initialized:
            return {'initialized': False, 'buffer_size': len(self._init_buffer)}
        return {
            'initialized': True,
            'cluster_counts': self.counts.tolist(),
            'cluster_activity': (self.counts > 0).sum(),
            'total_visits': int(self.counts.sum()),
        }


# ═══════════════════════════════════════════════════════════════
#  转移矩阵追踪器
# ═══════════════════════════════════════════════════════════════

class TransitionTracker:
    """
    记录状态之间的转移频率。
    如果某些转移路径的频率远高于随机水平，
    说明系统形成了内部"语法"——状态序列有结构。
    """

    def __init__(self, k=8):
        self.k = k
        self.matrix = np.zeros((k, k), dtype=np.float64)
        self.prev_state = None
        self.sequence = deque(maxlen=500)  # 最近500步的状态序列

    def update(self, state_idx):
        self.sequence.append(state_idx)
        if self.prev_state is not None:
            self.matrix[self.prev_state, state_idx] += 1
        self.prev_state = state_idx

    def get_transition_probs(self):
        """返回转移概率矩阵"""
        row_sums = self.matrix.sum(axis=1, keepdims=True)
        row_sums = np.where(row_sums == 0, 1, row_sums)
        return self.matrix / row_sums

    def entropy(self):
        """
        转移矩阵的平均条件熵。
        低熵 = 高度结构化（形成了内部"语法"）
        高熵 = 随机跳转（没有稳定的内部模式）
        理论最大值 = log2(k) ≈ 3.0 (k=8)
        """
        probs = self.get_transition_probs()
        entropies = []
        for row in probs:
            row = row[row > 0]
            if len(row) > 0:
                h = -np.sum(row * np.log2(row + 1e-10))
                entropies.append(h)
        return np.mean(entropies) if entropies else np.log2(self.k)

    def dominant_sequences(self, length=3, top_n=5):
        """找出最频繁的状态子序列（长度=length）"""
        if len(self.sequence) < length:
            return []
        seq_counts = {}
        seq = list(self.sequence)
        for i in range(len(seq) - length + 1):
            sub = tuple(seq[i:i+length])
            seq_counts[sub] = seq_counts.get(sub, 0) + 1
        sorted_seqs = sorted(seq_counts.items(), key=lambda x: -x[1])
        return sorted_seqs[:top_n]


# ═══════════════════════════════════════════════════════════════
#  符号稳定性指标
# ═══════════════════════════════════════════════════════════════

class StabilityMetrics:
    """
    量化内部表征的结构化程度。
    三个核心指标:
      1. 簇紧致度 (Compactness): 簇内方差越小 → 符号越清晰
      2. 簇分离度 (Separation): 簇间距离越大 → 符号越独立
      3. 时间稳定性 (Temporal Stability): 聚类结果随时间的一致性
    """

    def __init__(self, window=200):
        self.window = window
        self.recent_states = deque(maxlen=window)
        self.recent_vectors = deque(maxlen=window)
        self._prev_assignment = None

    def update(self, vector, cluster_idx):
        self.recent_vectors.append(vector.copy())
        self.recent_states.append(cluster_idx)

    def compute(self, kmeans):
        """计算并返回所有稳定性指标"""
        if not kmeans._initialized or len(self.recent_vectors) < 50:
            return {
                'compactness': 0.0,
                'separation': 0.0,
                'temporal_stability': 0.0,
                'symbol_score': 0.0,
                'ready': False,
            }

        vectors = np.stack(list(self.recent_vectors))
        states = np.array(list(self.recent_states))

        # 1. 紧致度: 平均簇内距离（越小越好）
        compactness = 0.0
        n_clusters_used = 0
        for i in range(kmeans.k):
            mask = states == i
            if mask.sum() > 1:
                cluster_vecs = vectors[mask]
                center = kmeans.centers[i]
                avg_dist = np.mean(np.linalg.norm(cluster_vecs - center, axis=1))
                compactness += avg_dist
                n_clusters_used += 1
        if n_clusters_used > 0:
            compactness /= n_clusters_used
        # 归一化: 越小越好 → 反转
        compactness_score = max(0, 1.0 - compactness / 5.0)

        # 2. 分离度: 簇间平均距离（越大越好）
        if n_clusters_used > 1:
            active_centers = kmeans.centers[kmeans.counts > 0]
            dists = []
            for i in range(len(active_centers)):
                for j in range(i+1, len(active_centers)):
                    dists.append(np.linalg.norm(active_centers[i] - active_centers[j]))
            separation = np.mean(dists) if dists else 0.0
        else:
            separation = 0.0
        separation_score = min(1.0, separation / 10.0)

        # 3. 时间稳定性: 连续相同状态的比例
        if len(states) > 1:
            same_count = sum(1 for i in range(1, len(states))
                           if states[i] == states[i-1])
            temporal_stability = same_count / (len(states) - 1)
        else:
            temporal_stability = 0.0

        # 综合符号分数 (0~1)
        # 高分 = 清晰的、稳定的、分离的内部符号
        symbol_score = (compactness_score * 0.35 +
                       separation_score * 0.35 +
                       temporal_stability * 0.30)

        return {
            'compactness': round(compactness_score, 4),
            'separation': round(separation_score, 4),
            'temporal_stability': round(temporal_stability, 4),
            'symbol_score': round(symbol_score, 4),
            'n_active_clusters': n_clusters_used,
            'ready': True,
        }


# ═══════════════════════════════════════════════════════════════
#  InternalSymbolTracker (主类)
# ═══════════════════════════════════════════════════════════════

class InternalSymbolTracker:
    """
    野生型实验A的核心观测工具。

    每帧接收CfC隐藏状态 h ∈ R^64，执行:
      1. 在线聚类 → 分配到符号索引
      2. 更新转移矩阵
      3. 计算稳定性指标
      4. 定期写入日志

    用法:
        tracker = InternalSymbolTracker(save_dir='./wild_logs')
        ...
        # 每帧
        symbol_idx = tracker.step(hidden_state_tensor)
        ...
        # 查看状态
        report = tracker.report()
    """

    def __init__(self, n_clusters=8, hidden_dim=64, save_dir=None, log_every=500):
        self.kmeans = OnlineKMeans(k=n_clusters, dim=hidden_dim)
        self.transitions = TransitionTracker(k=n_clusters)
        self.stability = StabilityMetrics()
        self.step_count = 0
        self.log_every = log_every

        # 日志
        self.save_dir = save_dir or os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(self.save_dir, 'symbol_log.jsonl')

    def step(self, hidden_state):
        """
        处理一帧。
        hidden_state: torch.Tensor (1, hidden_dim) 或 (hidden_dim,)
        返回: 当前符号索引 (int)
        """
        self.step_count += 1

        # 转numpy
        if isinstance(hidden_state, torch.Tensor):
            h = hidden_state.detach().cpu().numpy().flatten()
        else:
            h = np.asarray(hidden_state).flatten()

        # 聚类
        symbol_idx = self.kmeans.update(h)

        # 转移追踪
        self.transitions.update(symbol_idx)

        # 稳定性更新
        self.stability.update(h, symbol_idx)

        # 定期日志
        if self.step_count % self.log_every == 0:
            self._write_log(symbol_idx)

        return symbol_idx

    def report(self):
        """生成当前状态报告"""
        metrics = self.stability.compute(self.kmeans)
        kmeans_stats = self.kmeans.get_stats()
        entropy = self.transitions.entropy()
        max_entropy = np.log2(self.kmeans.k)
        structure_ratio = 1.0 - entropy / max_entropy if max_entropy > 0 else 0.0

        dominant = self.transitions.dominant_sequences(length=3, top_n=3)
        dominant_str = [f"{'→'.join(map(str, seq))}({cnt})"
                       for seq, cnt in dominant]

        return {
            'step': self.step_count,
            'symbol_score': metrics.get('symbol_score', 0),
            'compactness': metrics.get('compactness', 0),
            'separation': metrics.get('separation', 0),
            'temporal_stability': metrics.get('temporal_stability', 0),
            'n_active_clusters': metrics.get('n_active_clusters', 0),
            'transition_entropy': round(entropy, 4),
            'structure_ratio': round(structure_ratio, 4),
            'dominant_sequences': dominant_str,
            'cluster_counts': kmeans_stats.get('cluster_counts', []),
            'ready': metrics.get('ready', False),
        }

    def _write_log(self, current_symbol):
        """写入JSONL日志"""
        report = self.report()
        report['timestamp'] = datetime.datetime.now().isoformat()
        report['current_symbol'] = current_symbol
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(report, ensure_ascii=False) + '\n')
        except Exception:
            pass

    def save_state(self):
        """保存聚类状态（用于断点续训）"""
        state = {
            'kmeans_centers': self.kmeans.centers.tolist() if self.kmeans._initialized else None,
            'kmeans_counts': self.kmeans.counts.tolist(),
            'transition_matrix': self.transitions.matrix.tolist(),
            'step_count': self.step_count,
        }
        path = os.path.join(self.save_dir, 'symbol_state.json')
        with open(path, 'w') as f:
            json.dump(state, f)

    def load_state(self):
        """加载聚类状态"""
        path = os.path.join(self.save_dir, 'symbol_state.json')
        if not os.path.exists(path):
            return False
        try:
            with open(path, 'r') as f:
                state = json.load(f)
            if state.get('kmeans_centers') is not None:
                self.kmeans.centers = np.array(state['kmeans_centers'], dtype=np.float32)
                self.kmeans.counts = np.array(state['kmeans_counts'], dtype=np.float64)
                self.kmeans._initialized = True
            self.transitions.matrix = np.array(state['transition_matrix'], dtype=np.float64)
            self.step_count = state.get('step_count', 0)
            print(f"[SymbolTracker] 已加载状态 / State loaded (step {self.step_count})")
            return True
        except Exception as e:
            print(f"[SymbolTracker] 加载失败 / Load failed: {e}")
            return False


# ═══════════════════════════════════════════════════════════════
#  测试入口
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=== InternalSymbolTracker 测试 ===\n")
    tracker = InternalSymbolTracker(n_clusters=8, hidden_dim=64)

    # 模拟CfC隐藏状态
    for i in range(200):
        # 制造3个有结构的区域 + 噪声
        region = i % 3
        base = np.zeros(64)
        base[region*20:(region+1)*20] = 1.0
        h = base + np.random.randn(64) * 0.3
        symbol = tracker.step(h)

        if (i+1) % 50 == 0:
            r = tracker.report()
            print(f"[Step {i+1}] symbol={symbol} | "
                  f"score={r['symbol_score']:.3f} "
                  f"entropy={r['transition_entropy']:.3f} "
                  f"structure={r['structure_ratio']:.3f} "
                  f"active={r['n_active_clusters']}")

    print("\n最终报告:")
    report = tracker.report()
    for k, v in report.items():
        print(f"  {k}: {v}")
