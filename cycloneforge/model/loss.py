# -*- coding: utf-8 -*-
"""损失：MSE 与三头加权总损失。"""
from __future__ import annotations

from ..nn.autodiff import Value


def mse(pred: list, target: list) -> Value:
    """均方误差（pred 为 Value，target 为 float）。"""
    n = len(pred)
    if n == 0:
        return Value(0.0)
    s = Value(0.0)
    for p, t in zip(pred, target):
        s = s + (p - float(t)) ** 2
    return s * (1.0 / n)


def total_loss(outputs: dict, targets: dict, weights=None) -> Value:
    """三头加权总损失。targets 结构同 outputs。"""
    weights = weights or {"track": 1.0, "intensity": 1.0, "wind": 1.0}
    loss = Value(0.0)
    for key in ("track", "intensity", "wind"):
        if key in outputs and key in targets:
            loss = loss + mse(outputs[key], targets[key]) * weights[key]
    return loss
