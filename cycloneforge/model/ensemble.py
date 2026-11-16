# -*- coding: utf-8 -*-
"""集合预报：扰动初始场跑多成员，量化不确定度。"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

from .._core import RNG


@dataclass
class Ensemble:
    """集合预报结果：成员轨迹 + 强度 + 风场。"""

    tracks: list = field(default_factory=list)       # [member][step][lat, lon]
    intensities: list = field(default_factory=list)  # [member][step][vmax, pmin]
    winds: list = field(default_factory=list)        # [member][step][r34, r50, r64]

    @property
    def n_members(self) -> int:
        return len(self.tracks)


def perturb(features: list, scale: float, rng: random.Random) -> list:
    """给特征加高斯扰动（模拟初始场不确定度）。"""
    return [f + rng.gauss(0.0, scale) for f in features]


def run_ensemble(model, initial_features: list, n_members: int, perturb_scale: float,
                 n_steps: int, seed: int | str = 0) -> Ensemble:
    """扰动初始场跑 n_members 个成员的滚动自回归。"""
    from ..forecast.rollout import rollout_track

    rng = RNG(seed)
    ens = Ensemble()
    for _ in range(n_members):
        feats = perturb(initial_features, perturb_scale, rng._rng)
        track, intensity, wind = rollout_track(model, feats, n_steps)
        ens.tracks.append(track)
        ens.intensities.append(intensity)
        ens.winds.append(wind)
    return ens
