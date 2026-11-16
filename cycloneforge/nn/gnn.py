# -*- coding: utf-8 -*-
"""图卷积层：消息传递 = 邻居聚合 + 自身/邻居可训练变换。"""
from __future__ import annotations

import random

from .autodiff import Value


def aggregate_neighbors(node_feats: list, adjacency: dict, mode: str = "mean"):
    """确定性邻居聚合：把每个节点邻居特征聚合成一个向量。"""
    n = len(node_feats)
    dim = len(node_feats[0]) if n else 0
    agg = []
    for i in range(n):
        nbrs = adjacency.get(i, [])
        if not nbrs:
            agg.append([0.0] * dim)
            continue
        if mode == "mean":
            row = [sum(node_feats[j][k] for j in nbrs) / len(nbrs) for k in range(dim)]
        elif mode == "max":
            row = [max(node_feats[j][k] for j in nbrs) for k in range(dim)]
        else:  # sum
            row = [sum(node_feats[j][k] for j in nbrs) for k in range(dim)]
        agg.append(row)
    return agg


class GCNLayer:
    """一层图卷积：h_i' = tanh( W_self h_i + W_neigh mean(h_j) + b )。

    在 Value 上可训练，是「球面图神经网络」的最小可运行实现。
    """

    def __init__(self, in_dim: int, out_dim: int, rng: random.Random | None = None, scale: float = 0.1):
        self.in_dim = in_dim
        self.out_dim = out_dim
        rng = rng or random.Random(0)
        self.W_self = [[Value(rng.uniform(-scale, scale)) for _ in range(out_dim)] for _ in range(in_dim)]
        self.W_neigh = [[Value(rng.uniform(-scale, scale)) for _ in range(out_dim)] for _ in range(in_dim)]
        self.b = [Value(rng.uniform(-scale, scale)) for _ in range(out_dim)]

    def forward(self, node_feats, adjacency):
        """node_feats: list[list[Value]]; 返回 list[list[Value]]。"""
        agg = aggregate_neighbors(
            [[v.data for v in row] for row in node_feats], adjacency, mode="mean"
        )
        out = []
        for i, h in enumerate(node_feats):
            row = []
            for j in range(self.out_dim):
                s = self.b[j]
                for k in range(self.in_dim):
                    s = s + self.W_self[k][j] * h[k]
                    s = s + self.W_neigh[k][j] * Value(agg[i][k])
                row.append(s.tanh())
            out.append(row)
        return out

    def parameters(self):
        return [p for row in self.W_self for p in row] + [p for row in self.W_neigh for p in row] + self.b[:]

    def __call__(self, node_feats, adjacency):
        return self.forward(node_feats, adjacency)
