# -*- coding: utf-8 -*-
"""训练器：把合成数据喂进模型，标准库反向传播 + SGD。"""
from __future__ import annotations

from ..model.loss import total_loss
from ..model.cyclone_net import CycloneNet

# 目标量程：与 data/synthetic.py 的目标物理量程对齐，用于归一化训练 / 反归一化推理
TARGET_SCALES = {
    "track": [5.0, 5.0],                 # dlat / dlon（度）
    "intensity": [90.0, 1010.0],         # vmax (m/s) / pmin (hPa)
    "wind": [500.0, 500.0, 500.0],       # R34 / R50 / R64 (km)
}


def split_target(y: list) -> dict:
    """把 7 维扁平目标切成三头，并归一化到 [0,1] 量级。"""
    return {
        "track": [y[0] / TARGET_SCALES["track"][0], y[1] / TARGET_SCALES["track"][1]],
        "intensity": [y[2] / TARGET_SCALES["intensity"][0], y[3] / TARGET_SCALES["intensity"][1]],
        "wind": [y[4] / TARGET_SCALES["wind"][0], y[5] / TARGET_SCALES["wind"][1],
                 y[6] / TARGET_SCALES["wind"][2]],
    }


class Trainer:
    """确定性 SGD 训练：loss 单调下降，可复现。"""

    def __init__(self, model: CycloneNet, xs: list, ys: list, lr: float = 0.01,
                 epochs: int = 200, val_every: int = 20, momentum: float = 0.9):
        self.model = model
        self.xs = xs
        self.ys = ys
        self.lr = lr
        self.epochs = epochs
        self.val_every = val_every
        self.momentum = momentum
        self.history = []

    def train(self) -> dict:
        """跑完整训练，返回历史 loss 曲线。"""
        model = self.model
        # 训练/推理统一输出量程
        model.output_scales = TARGET_SCALES

        # 切分训练/验证（按 80/20）
        n = len(self.xs)
        split = int(n * 0.8)
        tr_x, tr_y = self.xs[:split], self.ys[:split]
        va_x, va_y = self.xs[split:], self.ys[split:]

        v = [0.0] * len(model.parameters())
        for epoch in range(self.epochs):
            # 训练
            train_loss = 0.0
            for x, y in zip(tr_x, tr_y):
                outputs = model.forward(x)
                targets = split_target(y)
                loss = total_loss(outputs, targets)
                loss.backward()
                params = model.parameters()
                for i, p in enumerate(params):
                    v[i] = self.momentum * v[i] + p.grad
                    p.data -= self.lr * v[i]
                    p.grad = 0.0
                train_loss += loss.data
            train_loss /= max(1, len(tr_x))

            if epoch == 0 or (epoch + 1) % self.val_every == 0 or epoch == self.epochs - 1:
                val_loss = self._evaluate(va_x, va_y)
                self.history.append({"epoch": epoch + 1, "train": train_loss, "val": val_loss})
        return {"history": self.history, "final_train_loss": self.history[-1]["train"]}

    def _evaluate(self, xs, ys) -> float:
        if not xs:
            return 0.0
        total = 0.0
        for x, y in zip(xs, ys):
            outputs = self.model.forward(x)
            targets = split_target(y)
            total += total_loss(outputs, targets).data
        return total / len(xs)
