# -*- coding: utf-8 -*-
"""学习率调度。"""
from __future__ import annotations

import math


class StepDecay:
    """每隔 step_size 个 epoch 乘 gamma。"""

    def __init__(self, lr: float, step_size: int = 50, gamma: float = 0.5):
        self.lr = lr
        self.step_size = step_size
        self.gamma = gamma

    def __call__(self, epoch: int) -> float:
        return self.lr * (self.gamma ** (epoch // self.step_size))


class CosineDecay:
    """余弦退火到 min_lr。"""

    def __init__(self, lr: float, total_epochs: int, min_lr: float = 1e-4):
        self.lr = lr
        self.total_epochs = total_epochs
        self.min_lr = min_lr

    def __call__(self, epoch: int) -> float:
        t = min(1.0, epoch / max(1, self.total_epochs))
        return self.min_lr + 0.5 * (self.lr - self.min_lr) * (1 + math.cos(math.pi * t))
