# -*- coding: utf-8 -*-
"""基准报告：跑完整评估，输出五张牌。"""
from __future__ import annotations

from dataclasses import dataclass

from ..model.ensemble import run_ensemble
from ..forecast.leadtime import mean_leadtime
from .metrics import summarize_errors
from .crs import ensemble_crps
from .skill import skill_score, persistence_baseline


@dataclass
class Benchmark:
    """评估结果。"""

    mean_track_km: float = 0.0
    max_track_km: float = 0.0
    mean_leadtime_h: float = 0.0
    crps: float = 0.0
    skill: float = 0.0

    def as_dict(self) -> dict:
        return {
            "mean_track_km": round(self.mean_track_km, 2),
            "max_track_km": round(self.max_track_km, 2),
            "mean_leadtime_h": round(self.mean_leadtime_h, 2),
            "crps": round(self.crps, 4),
            "skill": round(self.skill, 4),
        }


def run_benchmark(model, initial_features: list, truth_track: list,
                  n_steps: int, step_hours: float, threshold_km: float,
                  n_members: int = 50, perturb_scale: float = 0.1, seed: int = 0) -> Benchmark:
    """跑一次完整评估。"""
    from ..forecast.rollout import rollout_track

    ens = run_ensemble(model, initial_features, n_members, perturb_scale, n_steps, seed)
    # 集合均值轨迹
    mean_track = []
    for step in range(n_steps + 1):
        lats = [ens.tracks[m][step][0] for m in range(n_members)]
        lons = [ens.tracks[m][step][1] for m in range(n_members)]
        mean_track.append([sum(lats) / n_members, sum(lons) / n_members])

    errs = summarize_errors(mean_track, truth_track)
    lt = mean_leadtime(ens.tracks, truth_track, step_hours, threshold_km)
    # 集合 CRPS（对轨迹纬度）
    ens_lat = [[ens.tracks[m][s][0] for m in range(n_members)] for s in range(n_steps + 1)]
    truth_lat = [t[0] for t in truth_track]
    c = ensemble_crps(ens_lat, truth_lat)
    ss = skill_score(mean_track, truth_track, persistence_baseline(truth_track))

    return Benchmark(
        mean_track_km=errs["mean_track_km"],
        max_track_km=errs["max_track_km"],
        mean_leadtime_h=lt,
        crps=c,
        skill=ss,
    )
