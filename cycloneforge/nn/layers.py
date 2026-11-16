# -*- coding: utf-8 -*-
"""可训练线性层与多层感知机（基于 autodiff.Value）。"""
from __future__ import annotations

import random

from .autodiff import Value


class Linear:
    """全连接层：out = x @ W + b，权重为 Value 可训练。"""

    def __init__(self, in_dim: int, out_dim: int, rng: random.Random | None = None, scale: float = 0.1):
        self.in_dim = in_dim
        self.out_dim = out_dim
        rng = rng or random.Random(0)
        self.W = [[Value(rng.uniform(-scale, scale)) for _ in range(out_dim)] for _ in range(in_dim)]
        self.b = [Value(rng.uniform(-scale, scale)) for _ in range(out_dim)]

    def forward(self, x):
        """x: list[Value] (in_dim) -> list[Value] (out_dim)。"""
        out = []
        for j in range(self.out_dim):
            s = self.b[j]
            for i in range(self.in_dim):
                s = s + self.W[i][j] * x[i]
            out.append(s)
        return out

    def parameters(self):
        params = [p for row in self.W for p in row] + self.b[:]
        return params

    def __call__(self, x):
        return self.forward(x)


class MLP:
    """多层感知机：若干 Linear + 激活堆叠。"""

    def __init__(self, dims: list[int], rng: random.Random | None = None, activation="tanh"):
        self.dims = dims
        self.layers = []
        rng = rng or random.Random(0)
        for i in range(len(dims) - 1):
            self.layers.append(Linear(dims[i], dims[i + 1], rng=rng))
        self.activation = activation

    def _act(self, x):
        if self.activation == "tanh":
            return x.tanh()
        if self.activation == "relu":
            return x.relu()
        return x

    def forward(self, x):
        for i, layer in enumerate(self.layers):
            x = layer.forward(x)
            if i < len(self.layers) - 1:
                x = [self._act(v) for v in x]
        return x

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]

    def __call__(self, x):
        return self.forward(x)
