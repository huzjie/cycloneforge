# -*- coding: utf-8 -*-
"""图卷积测试。"""
import random
from cycloneforge.nn.gnn import GCNLayer
from cycloneforge.nn.autodiff import Value


def test_gcn_forward():
    layer = GCNLayer(3, 2, rng=random.Random(0))
    feats = [[Value(0.1), Value(0.2), Value(0.3)] for _ in range(4)]
    adj = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}
    out = layer.forward(feats, adj)
    assert len(out) == 4
    assert len(out[0]) == 2
