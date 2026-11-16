# -*- coding: utf-8 -*-
"""流水线测试。"""
from cycloneforge.config import load_config
from cycloneforge.engine.pipeline import Pipeline


def test_train():
    result = Pipeline(load_config()).train()
    assert result["n_samples"] > 0


def test_eval():
    cfg = load_config()
    cfg.train.epochs = 5
    cfg.ensemble.n_members = 5
    trained = Pipeline(cfg).train()
    bench = Pipeline(cfg).eval(trained["model"])
    assert bench["mean_track_km"] >= 0
