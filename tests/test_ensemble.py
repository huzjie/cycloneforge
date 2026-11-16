# -*- coding: utf-8 -*-
"""集合预报测试。"""
from cycloneforge.model.cyclone_net import CycloneNet
from cycloneforge.data.synthetic import SyntheticCyclone
from cycloneforge.model.ensemble import run_ensemble


def test_ensemble_members():
    net = CycloneNet(dim=16, processor_layers=2, seed=1)
    cyc = SyntheticCyclone("e", n_steps=10).generate()
    ens = run_ensemble(net, cyc[0].features(), 7, 0.1, 4, 0)
    assert ens.n_members == 7
