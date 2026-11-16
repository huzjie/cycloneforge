# -*- coding: utf-8 -*-
"""归一化：最小-最大缩放。"""
from __future__ import annotations


def minmax(v: float, lo: float, hi: float) -> float:
    return max(0.0, min(1.0, (v - lo) / (hi - lo)))


class MinMaxScaler:
    """按给定量程做 min-max 缩放。"""

    def __init__(self, ranges: list):
        self.ranges = ranges  # [(lo, hi), ...]

    def fit(self, _data=None):
        return self

    def transform(self, row: list) -> list:
        return [minmax(v, lo, hi) for v, (lo, hi) in zip(row, self.ranges)]

    def inverse(self, row: list) -> list:
        return [lo + v * (hi - lo) for v, (lo, hi) in zip(row, self.ranges)]
