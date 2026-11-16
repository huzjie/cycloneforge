# -*- coding: utf-8 -*-
"""线性层测试。"""
import random
from cycloneforge.nn.layers import Linear, MLP
from cycloneforge.nn.autodiff import Value


def test_linear_shape():
    layer = Linear(4, 3, rng=random.Random(0))
    out = layer.forward([Value(1.0), Value(2.0), Value(3.0), Value(4.0)])
    assert len(out) == 3


def test_mlp_shape():
    mlp = MLP([4, 8, 2], rng=random.Random(0))
    out = mlp.forward([Value(1.0)] * 4)
    assert len(out) == 2
