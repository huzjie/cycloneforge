# -*- coding: utf-8 -*-
"""CycloneNet：编码器 -> 共享主干 -> 三要素预测头。"""
from __future__ import annotations

import random

from ..nn.autodiff import Value
from ..nn.encoder import Standardizer, FEATURE_DIM
from ..nn.processor import Processor
from ..nn.decoder import TrackHead, IntensityHead, WindHead


class CycloneNet:
    """神经网络热带气旋预测模型。

    共享编码器把台风状态压成隐表示，三个独立预测头分别输出：
    - track:     下一步位移 (dlat, dlon)
    - intensity: 下一步强度 (vmax, pmin)
    - wind:      下一步风圈 (R34, R50, R64)
    """

    def __init__(self, dim: int = 32, processor_layers: int = 4, seed: int = 0,
                 n_track: int = 2, n_intensity: int = 2, n_wind: int = 3):
        rng = random.Random(seed)
        self.dim = dim
        self.encoder = Standardizer()
        self.processor = Processor(FEATURE_DIM, dim, processor_layers, rng=rng)
        self.track_head = TrackHead(dim, n_track, rng=rng)
        self.intensity_head = IntensityHead(dim, n_intensity, rng=rng)
        self.wind_head = WindHead(dim, n_wind, rng=rng)
        # 输出量程（训练时由 trainer 按目标量程设定，predict 据此反归一化回物理量）
        self.output_scales = {
            "track": [1.0] * n_track,
            "intensity": [1.0] * n_intensity,
            "wind": [1.0] * n_wind,
        }

    def forward(self, features: list) -> dict:
        """前向（可训练）：features(10 维 float) -> {track,intensity,wind} 的 Value 列表。"""
        x = [Value(v) for v in self.encoder.encode(features)]
        z = self.processor.forward(x)
        return {
            "track": self.track_head.forward(z),
            "intensity": self.intensity_head.forward(z),
            "wind": self.wind_head.forward(z),
        }

    def predict(self, features: list) -> dict:
        """推理（无梯度）：返回物理量（按 output_scales 反归一化）。"""
        out = self.forward(features)
        return {k: [v.data * s for v, s in zip(vs, self.output_scales[k])]
                for k, vs in out.items()}

    def parameters(self):
        return (
            self.processor.parameters()
            + self.track_head.parameters()
            + self.intensity_head.parameters()
            + self.wind_head.parameters()
        )

    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0.0
