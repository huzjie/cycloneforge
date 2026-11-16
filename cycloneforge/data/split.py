# -*- coding: utf-8 -*-
"""数据切分：按年份 / 按比例。"""
from __future__ import annotations

from .._core import RNG


def split_by_year(records: list, train_years, val_years, test_years) -> tuple:
    """按年份切分（records 需带 year 字段）。"""
    tr = [r for r in records if r.get("year") in train_years]
    va = [r for r in records if r.get("year") in val_years]
    te = [r for r in records if r.get("year") in test_years]
    return tr, va, te


def split_ratio(records: list, ratios=(0.7, 0.15, 0.15), seed=0) -> tuple:
    """按比例随机切分（确定性 shuffle）。"""
    rng = RNG(seed)
    idx = list(range(len(records)))
    rng.shuffle(idx)
    n = len(records)
    i1 = int(n * ratios[0])
    i2 = int(n * (ratios[0] + ratios[1]))
    tr = [records[i] for i in idx[:i1]]
    va = [records[i] for i in idx[i1:i2]]
    te = [records[i] for i in idx[i2:]]
    return tr, va, te
