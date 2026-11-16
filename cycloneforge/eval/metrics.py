# -*- coding: utf-8 -*-
"""误差指标：轨迹（km）/ 强度（m/s, hPa）/ 风场结构（km）。"""
from __future__ import annotations

from ..utils.geo import haversine_km


def track_error_km(pred: list, truth: list) -> float:
    """单时次轨迹误差（大圆距离 km）。"""
    return haversine_km(pred[0], pred[1], truth[0], truth[1])


def intensity_error(pred: list, truth: list) -> tuple[float, float]:
    """强度误差：返回 (vmax 误差 m/s, pmin 误差 hPa) 的绝对值。"""
    return abs(pred[0] - truth[0]), abs(pred[1] - truth[1])


def wind_error(pred: list, truth: list) -> tuple[float, float, float]:
    """风场结构误差：R34/R50/R64 的绝对误差 (km)。"""
    return (abs(pred[0] - truth[0]), abs(pred[1] - truth[1]), abs(pred[2] - truth[2]))


def summarize_errors(pred_track: list, truth_track: list) -> dict:
    """整条轨迹的平均误差。"""
    n = min(len(pred_track), len(truth_track))
    if n == 0:
        return {"mean_track_km": 0.0, "max_track_km": 0.0}
    errs = [track_error_km(p, t) for p, t in zip(pred_track, truth_track)]
    return {"mean_track_km": sum(errs) / n, "max_track_km": max(errs)}
