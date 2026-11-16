# -*- coding: utf-8 -*-
"""提前量量化：轨迹误差首次越限的时间点。"""
from __future__ import annotations

from ..utils.geo import haversine_km


def leadtime(pred_track: list, truth_track: list, step_hours: float, threshold_km: float) -> float:
    """返回预测轨迹误差首次超过 threshold_km 的提前量（小时）。

    若全程未越限，返回最后一个时次对应的小时数。
    """
    n = min(len(pred_track), len(truth_track))
    for i in range(n):
        err = haversine_km(pred_track[i][0], pred_track[i][1],
                           truth_track[i][0], truth_track[i][1])
        if err > threshold_km:
            return i * step_hours
    return (n - 1) * step_hours


def mean_leadtime(pred_tracks: list, truth_track: list, step_hours: float, threshold_km: float) -> float:
    """集合成员的提前量取平均。"""
    if not pred_tracks:
        return 0.0
    vals = [leadtime(p, truth_track, step_hours, threshold_km) for p in pred_tracks]
    return sum(vals) / len(vals)
