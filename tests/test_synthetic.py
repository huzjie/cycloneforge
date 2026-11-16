# -*- coding: utf-8 -*-
"""合成台风测试。"""
from cycloneforge.data.synthetic import SyntheticCyclone, make_dataset


def test_generate_length():
    cyc = SyntheticCyclone("t", n_steps=20).generate()
    assert len(cyc) == 20


def test_features_dim():
    cyc = SyntheticCyclone("t", n_steps=5).generate()
    assert len(cyc[0].features()) == 10


def test_make_dataset_deterministic():
    xs1, ys1 = make_dataset(n_cyclones=2, seed_base=7)
    xs2, ys2 = make_dataset(n_cyclones=2, seed_base=7)
    assert xs1 == xs2 and ys1 == ys2
