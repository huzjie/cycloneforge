# -*- coding: utf-8 -*-
"""训练测试。"""
from cycloneforge.model.cyclone_net import CycloneNet
from cycloneforge.data.synthetic import make_dataset
from cycloneforge.train.trainer import Trainer


def test_loss_decreases():
    xs, ys = make_dataset(n_cyclones=3, seed_base=7)
    net = CycloneNet(dim=16, processor_layers=2, seed=3)
    t = Trainer(net, xs, ys, lr=0.02, epochs=40, val_every=10)
    r = t.train()
    first = r["history"][0]["train"]
    last = r["history"][-1]["train"]
    assert last < first


def test_train_deterministic():
    xs, ys = make_dataset(n_cyclones=2, seed_base=7)
    n1 = CycloneNet(dim=16, processor_layers=2, seed=3)
    r1 = Trainer(n1, xs, ys, lr=0.01, epochs=3, val_every=2).train()
    n2 = CycloneNet(dim=16, processor_layers=2, seed=3)
    r2 = Trainer(n2, xs, ys, lr=0.01, epochs=3, val_every=2).train()
    assert r1["final_train_loss"] == r2["final_train_loss"]
