# -*- coding: utf-8 -*-
"""Holland 风场模型：轴对称台风风廓线（用于合成风圈半径）。"""
from __future__ import annotations

import math

from ..utils.units import ms_to_kt


def wind_speed(vmax: float, rmw: float, b: float, r: float) -> float:
    """Holland 风场：距中心 r (km) 处的风速 (m/s)。

    V(r) = Vmax * (RMW/r)^B * exp(1 - (RMW/r)^B)
    """
    if r <= 0:
        return vmax
    x = (rmw / r) ** b
    return vmax * x * math.exp(1.0 - x)


def wind_radius(vmax: float, rmw: float, b: float, target_kt: float) -> float:
    """反解：找到风速降到 target_kt 的半径 (km)。

    令 (RMW/r)^B = x，则 Vt/Vmax = x * exp(1-x)，对 x 二分，再 r = RMW / x^(1/B)。
    """
    target_ms = target_kt / 1.943844  # kt -> m/s
    ratio = target_ms / vmax
    if ratio >= 1.0:
        return rmw
    lo, hi = 1e-6, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2.0
        val = mid * math.exp(1.0 - mid)
        if val > ratio:
            hi = mid
        else:
            lo = mid
    x = (lo + hi) / 2.0
    return rmw / (x ** (1.0 / b))


def pressure_from_vmax(vmax: float, p_env: float = 1010.0) -> float:
    """由最大风速估中心气压（简化经验式，hPa）。"""
    return p_env - 1.35 * vmax


def wind_radii(vmax: float, rmw: float, b: float) -> tuple[float, float, float]:
    """返回 (R34, R50, R64) 三档风圈半径 (km)。"""
    r34 = wind_radius(vmax, rmw, b, 34.0)
    r50 = wind_radius(vmax, rmw, b, 50.0)
    r64 = wind_radius(vmax, rmw, b, 64.0)
    return r34, r50, r64
