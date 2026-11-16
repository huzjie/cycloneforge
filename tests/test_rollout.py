# -*- coding: utf-8 -*-
"""滚动自回归测试。"""
from cycloneforge.model.cyclone_net import CycloneNet
from cycloneforge.data.synthetic import SyntheticCyclone
from cycloneforge.forecast.rollout import rollout_track


def test_rollout_length():
    net = CycloneNet(dim=16, processor_layers=2, seed=1)
    cyc = SyntheticCyclone("r", n_steps=10).generate()
    tracks, intensities, winds = rollout_track(net, cyc[0].features(), 4)
    assert len(tracks) == 5
    assert len(winds) == 4
