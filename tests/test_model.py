# -*- coding: utf-8 -*-
"""模型前向/推理测试。"""
from cycloneforge.model.cyclone_net import CycloneNet


def test_forward_keys():
    net = CycloneNet(dim=16, processor_layers=2, seed=1)
    out = net.forward([10, 130, 20, 1000, 1, -1, 29, 10, 50, 0.8])
    assert set(out) == {"track", "intensity", "wind"}


def test_predict_shapes():
    net = CycloneNet(dim=16, processor_layers=2, seed=1)
    out = net.predict([10, 130, 20, 1000, 1, -1, 29, 10, 50, 0.8])
    assert len(out["track"]) == 2 and len(out["intensity"]) == 2 and len(out["wind"]) == 3
