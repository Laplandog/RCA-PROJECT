"""
life_core.py
把 SensoryMapper 输出的加权偏离向量，喂入 CfC + AutoNCP 网络，
输出五维情感状态 (valence, arousal, safety, connection, seeking)。

这是我们上次确认过的架构：CfC核心完全不知道"基因组"的存在，
它只是在处理一个每次基因组切换后会变化的输入向量。
基因组的baseline_params(arousal_baseline等)作为初始隐藏状态偏置注入，
不需要重新训练网络。
"""

import torch
import torch.nn as nn
from ncps.torch import CfC
from ncps.wirings import AutoNCP

from sensory_mapper import SensoryMapper, CHANNEL_ORDER

EMOTION_DIMS = ["valence", "arousal", "safety", "connection", "seeking"]


class EmotionCore(nn.Module):
    """
    输入: 8维加权感官向量(来自SensoryMapper)
    输出: 5维情感状态(来自AutoNCP的motor neurons)
    """

    def __init__(self, input_size=8, n_neurons=28, n_outputs=5):
        super().__init__()
        wiring = AutoNCP(n_neurons, n_outputs)
        self.rnn = CfC(input_size, wiring)
        self.hidden_size = wiring.units

    def forward(self, x, hx=None):
        """
        x: (batch, seq_len, input_size) 或 (batch, input_size)单步
        hx: 上一步隐藏状态，用于tick-by-tick的持续推理（不是每次从0开始）
        """
        if x.dim() == 2:
            x = x.unsqueeze(1)  # 补成 (batch, 1, input_size) 单步序列
        output, hn = self.rnn(x, hx)
        return output, hn


class LifeAgent:
    """
    整合 SensoryMapper + EmotionCore 的运行时封装。
    负责：读一次传感器数据 -> 加权 -> 喂进网络 -> 输出情感状态 -> 维护隐藏状态跨tick持续。
    """

    def __init__(self, genome_path):
        self.mapper = SensoryMapper(genome_path)
        self.core = EmotionCore(input_size=len(CHANNEL_ORDER))
        self.core.eval()  # 推理模式；训练/微调是另一个独立脚本的职责，不在这里做
        self.hidden = None  # 跨tick持续的隐藏状态，这就是"活着"的连续性所在

        # 用baseline_params里的arousal_baseline初始化隐藏状态的一个偏置
        # 简化实现：作为初始隐藏状态的常数偏移，不同基因组因此有不同的起始"性情"
        baseline = self.mapper.baseline_params
        arousal_baseline = baseline.get("arousal_baseline", 0.0)
        self._init_hidden(arousal_baseline)

    def _init_hidden(self, arousal_baseline):
        h0 = torch.zeros(1, self.core.hidden_size)
        h0 += arousal_baseline * 0.1  # 温和的初始偏置，量级刻意压低，避免主导网络实际学习到的动态
        self.hidden = h0

    def switch_genome(self, genome_path):
        """
        运行时切换基因组：只替换感觉权重表(SensoryMapper)并重置隐藏状态，
        刻意保留同一个EmotionCore网络权重不变——这样切换的是"此刻在乎什么"
        （不同生态位的视角），而不是换一个完全不同的大脑，符合项目"变色龙"设计。
        """
        self.mapper = SensoryMapper(genome_path)
        baseline = self.mapper.baseline_params
        arousal_baseline = baseline.get("arousal_baseline", 0.0)
        self._init_hidden(arousal_baseline)

    def tick(self, raw_readings: dict, dt_seconds: float = 2.0):
        """
        处理一次传感器读数，返回情感状态和调试信息。
        dt_seconds: 距上一次tick的真实间隔（CfC是连续时间模型，这个参数直接影响时间常数的效果）
        """
        mapped = self.mapper.process(raw_readings)
        vec = torch.tensor([mapped["vector"]], dtype=torch.float32)  # (1, 8)

        with torch.no_grad():
            ts = torch.tensor([[dt_seconds]], dtype=torch.float32)
            output, self.hidden = self.core.rnn(vec.unsqueeze(1), self.hidden, timespans=ts)

        emotion_raw = output.squeeze(0).squeeze(0)  # (5,)
        emotion = {dim: float(torch.tanh(emotion_raw[i])) for i, dim in enumerate(EMOTION_DIMS)}

        return {
            "emotion": emotion,
            "sensory_vector": mapped["vector"],
            "raw_recorded": mapped["raw_recorded"],
            "deviations": mapped["deviations"],
            "warnings": mapped["warnings"],
        }


if __name__ == "__main__":
    # 自测：番茄基因组，跑一段正常状态+干旱事件，观察情感状态是否随之产生合理变化
    from mock_sensor import MockSensorStream, PRESET_BASELINES

    agent = LifeAgent("genomes/tomato_soil.json")
    stream = MockSensorStream(PRESET_BASELINES["tomato_soil"], seed=7)

    print(f"基因组: {agent.mapper.display_name}")
    print("--- 正常状态 ---")
    for i, reading in enumerate(stream.stream(5)):
        result = agent.tick(reading)
        print(f"tick{i} valence={result['emotion']['valence']:+.3f} "
              f"arousal={result['emotion']['arousal']:+.3f} "
              f"safety={result['emotion']['safety']:+.3f}")

    print("--- 触发干旱事件 ---")
    stream.trigger_event("moisture", target_value=12.0, duration_ticks=15)
    for i, reading in enumerate(stream.stream(20)):
        result = agent.tick(reading)
        if i % 4 == 0:
            print(f"tick{i} moisture={reading['moisture']:.1f} "
                  f"valence={result['emotion']['valence']:+.3f} "
                  f"arousal={result['emotion']['arousal']:+.3f} "
                  f"safety={result['emotion']['safety']:+.3f}")
