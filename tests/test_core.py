# -*- coding: utf-8 -*-
"""确定性 RNG 测试。"""
from cycloneforge._core import RNG, seed_from


def test_seed_from_deterministic():
    assert seed_from("abc") == seed_from("abc")
    assert seed_from("abc") != seed_from("abd")


def test_rng_reproducible():
    r1 = RNG("x").randint(0, 1000)
    r2 = RNG("x").randint(0, 1000)
    assert r1 == r2
