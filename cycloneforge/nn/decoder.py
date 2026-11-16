# -*- coding: utf-8 -*-
"""解码器：三个预测头（轨迹 / 强度 / 风场结构）。"""
from __future__ import annotations

import random

from .layers import Linear


class TrackHead:
    """轨迹头：隐表示 -> 未来 T 步 (lat, lon) 展平序列。"""

    def __init__(self, dim: int, out_dim: int, rng: random.Random | None = None):
        self.linear = Linear(dim, out_dim, rng=rng)

    def forward(self, z):
        return self.linear.forward(z)

    def parameters(self):
        return self.linear.parameters()

    def __call__(self, z):
        return self.forward(z)


class IntensityHead:
    """强度头：隐表示 -> 未来 T 步 (vmax, pmin)。"""

    def __init__(self, dim: int, out_dim: int, rng: random.Random | None = None):
        self.linear = Linear(dim, out_dim, rng=rng)

    def forward(self, z):
        return self.linear.forward(z)

    def parameters(self):
        return self.linear.parameters()

    def __call__(self, z):
        return self.forward(z)


class WindHead:
    """风场结构头：隐表示 -> 未来 T 步 (R34, R50, R64) 风圈半径。"""

    def __init__(self, dim: int, out_dim: int, rng: random.Random | None = None):
        self.linear = Linear(dim, out_dim, rng=rng)

    def forward(self, z):
        return self.linear.forward(z)

    def parameters(self):
        return self.linear.parameters()

    def __call__(self, z):
        return self.forward(z)
