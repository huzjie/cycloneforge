# -*- coding: utf-8 -*-
"""流水线：训练 -> 预测 -> 评估 三段式编排。"""
from __future__ import annotations

import random

from ..model.cyclone_net import CycloneNet
from ..data.synthetic import SyntheticCyclone, make_dataset
from ..train.trainer import Trainer
from ..eval.benchmark import run_benchmark
from ..forecast.rollout import rollout_track


class Pipeline:
    """端到端流水线。"""

    def __init__(self, config=None):
        self.config = config

    def _model(self) -> CycloneNet:
        cfg = self.config
        return CycloneNet(
            dim=cfg.model.dim if cfg else 32,
            processor_layers=cfg.model.processor_layers if cfg else 4,
            seed=cfg.train.seed if cfg else 20261116,
        )

    def train(self) -> dict:
        cfg = self.config
        xs, ys = make_dataset(cfg, n_cyclones=4, seed_base=cfg.train.seed)
        model = self._model()
        trainer = Trainer(model, xs, ys, lr=cfg.train.lr, epochs=cfg.train.epochs,
                          val_every=cfg.train.val_every)
        result = trainer.train()
        return {"model": model, "history": result["history"],
                "final_train_loss": result["final_train_loss"], "n_samples": len(xs)}

    def forecast(self, model=None, out_path=None) -> dict:
        cfg = self.config
        model = model or self._model()
        # 取一条测试台风做 5 天滚动自回归
        cyc = SyntheticCyclone(f"{cfg.train.seed}:test").generate()
        init = cyc[0].features()
        n_steps = cfg.forecast.horizon_hours // cfg.forecast.step_hours
        tracks, intensities, winds = rollout_track(model, init, n_steps)
        result = {"track": tracks, "intensity": intensities, "wind": winds, "n_steps": n_steps}
        if out_path:
            import json
            from pathlib import Path
            Path(out_path).write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        return result

    def eval(self, model=None) -> dict:
        cfg = self.config
        model = model or self._model()
        cyc = SyntheticCyclone(f"{cfg.train.seed}:eval").generate()
        init = cyc[0].features()
        truth = [[s.lat, s.lon] for s in cyc]
        n_steps = cfg.forecast.horizon_hours // cfg.forecast.step_hours
        bench = run_benchmark(
            model, init, truth, n_steps, cfg.forecast.step_hours,
            cfg.forecast.leadtime_threshold_km, cfg.ensemble.n_members,
            cfg.ensemble.perturb_scale, cfg.train.seed,
        )
        return bench.as_dict()
