# -*- coding: utf-8 -*-
"""技能评分：相对基线（持续性预报）的改进比例。"""
from __future__ import annotations

from .metrics import summarize_errors


def skill_score(pred_track: list, truth_track: list, baseline_track: list) -> float:
    """SS = 1 - err(pred)/err(baseline)。>0 表示优于基线。"""
    e_pred = summarize_errors(pred_track, truth_track)["mean_track_km"]
    e_base = summarize_errors(baseline_track, truth_track)["mean_track_km"]
    if e_base == 0.0:
        return 0.0
    return 1.0 - e_pred / e_base


def persistence_baseline(truth_track: list) -> list:
    """持续性基线：每个时次都预报「不移动」（沿用上一时次位置）。"""
    return [truth_track[0]] * len(truth_track)
