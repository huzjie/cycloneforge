# -*- coding: utf-8 -*-
"""台风路径模型：β 漂移 + 引导气流（确定性 ODE）。"""
from __future__ import annotations

import math


def beta_drift(lat: float, f: float = 1.0) -> tuple[float, float]:
    """β 效应导致的西北向漂移（随纬度增强）。"""
    beta = f * (1.0 + abs(lat) / 30.0)
    dlat = beta * 0.5          # 向北
    dlon = -beta * 0.3         # 向西
    return dlat, dlon


def step_track(lat: float, lon: float, steer_u: float, steer_v: float, beta: float = 1.0) -> tuple[float, float]:
    """一步（6h）路径推进：引导气流 + β 漂移。"""
    bdlat, bdlon = beta_drift(lat, beta)
    new_lat = lat + steer_v + bdlat
    new_lon = lon + steer_u + bdlon
    return new_lat, new_lon
