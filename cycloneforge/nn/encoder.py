# -*- coding: utf-8 -*-
"""编码器：把台风状态特征标准化为 [0,1] 区间。"""
from __future__ import annotations


class Standardizer:
    """确定性特征标准化（按固定物理量程映射，保证可复现）。"""

    # 每个特征的 (min, max) 物理量程
    RANGES = [
        (-90.0, 90.0),      # lat
        (-180.0, 180.0),    # lon
        (0.0, 90.0),        # vmax (m/s)
        (880.0, 1020.0),    # pmin (hPa)
        (-30.0, 30.0),      # 过去 6h 经向移动 (km/h 归一)
        (-30.0, 30.0),      # 过去 6h 纬向移动
        (20.0, 32.0),       # 海温 SST (°C)
        (0.0, 40.0),        # 垂直风切变 (m/s)
        (10.0, 200.0),      # 最大风半径 RMW (km)
        (0.0, 1.0),         # 环境湿度
    ]

    @classmethod
    def encode(cls, feats: list) -> list:
        """按量程线性映射到 [0,1]。"""
        out = []
        for f, (lo, hi) in zip(feats, cls.RANGES):
            out.append(max(0.0, min(1.0, (f - lo) / (hi - lo))))
        return out

    @classmethod
    def decode(cls, normed: list) -> list:
        out = []
        for v, (lo, hi) in zip(normed, cls.RANGES):
            out.append(lo + v * (hi - lo))
        return out


FEATURE_DIM = 10
