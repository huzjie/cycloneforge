# -*- coding: utf-8 -*-
"""连续分级概率评分（CRPS）：量化集合预报的不确定度。"""
from __future__ import annotations


def crps(samples: list, truth: float) -> float:
    """经验 CRPS（能量评分式）。

    CRPS = (1/n) Σ|x_i - y| - (1/(2 n^2)) Σ_i Σ_j |x_i - x_j|
    值越低越好；既奖励成员准确、又奖励散布合理（不过度自信、不过度发散）。
    """
    n = len(samples)
    if n == 0:
        return float("inf")
    term1 = sum(abs(x - truth) for x in samples) / n
    term2 = 0.0
    for i in range(n):
        for j in range(n):
            term2 += abs(samples[i] - samples[j])
    term2 = term2 / (2.0 * n * n)
    return term1 - term2


def ensemble_crps(ensemble: list, truths: list) -> float:
    """多时次集合 CRPS 取平均。ensemble: [时次][成员值]；truths: [时次] 真值。"""
    n = min(len(ensemble), len(truths))
    if n == 0:
        return float("inf")
    return sum(crps(ensemble[i], truths[i]) for i in range(n)) / n
