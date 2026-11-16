# -*- coding: utf-8 -*-
"""处理器：共享主干 MLP（把编码特征映射到隐表示）。"""
from __future__ import annotations

import random

from .layers import MLP


class Processor:
    """共享主干：dim -> hidden -> hidden。"""

    def __init__(self, in_dim: int, dim: int, depth: int = 2, rng: random.Random | None = None):
        dims = [in_dim] + [dim] * depth
        self.mlp = MLP(dims, rng=rng, activation="tanh")

    def forward(self, x):
        return self.mlp.forward(x)

    def parameters(self):
        return self.mlp.parameters()

    def __call__(self, x):
        return self.forward(x)
