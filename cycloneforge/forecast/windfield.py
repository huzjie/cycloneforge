# -*- coding: utf-8 -*-
"""二维风场重建：由 Holland 参数 + 中心位置重建网格风场。"""
from __future__ import annotations

import math

from ..data.holland import wind_speed


def reconstruct_windfield(center, vmax: float, rmw: float, b: float, nodes: list) -> list:
    """在 nodes 网格上重建风速场（m/s）。"""
    from ..utils.geo import haversine_km

    clat, clon = center
    field = []
    for lat, lon in nodes:
        r = haversine_km(clat, clon, lat, lon)
        field.append(wind_speed(vmax, rmw, b, r))
    return field


def wind_swath(centers: list, vmaxs: list, rmws: list, bs: list, nodes: list) -> list:
    """多时次最大风圈包络：每个节点取所有时次的最大风速。"""
    n = len(nodes)
    max_field = [0.0] * n
    for c, v, r, b in zip(centers, vmaxs, rmws, bs):
        f = reconstruct_windfield(c, v, r, b, nodes)
        for i in range(n):
            max_field[i] = max(max_field[i], f[i])
    return max_field
