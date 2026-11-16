# -*- coding: utf-8 -*-
"""优化器：SGD / 带动量 SGD。"""
from __future__ import annotations


class SGD:
    """朴素随机梯度下降。"""

    def __init__(self, params, lr: float):
        self.params = params
        self.lr = lr

    def step(self):
        for p in self.params:
            p.data -= self.lr * p.grad


class SGDMomentum:
    """带动量 SGD（对抖动目标更稳）。"""

    def __init__(self, params, lr: float, momentum: float = 0.9):
        self.params = params
        self.lr = lr
        self.momentum = momentum
        self.v = [0.0] * len(params)

    def step(self):
        for i, p in enumerate(self.params):
            self.v[i] = self.momentum * self.v[i] + p.grad
            p.data -= self.lr * self.v[i]
