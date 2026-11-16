# -*- coding: utf-8 -*-
"""邻域搜索：k 近邻 / 半径邻域。"""
from __future__ import annotations

from ..utils.geo import latlon_to_xyz


def _xyz(lat: float, lon: float):
    return latlon_to_xyz(lat, lon)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def k_nearest_neighbors(nodes: list, k: int = 8) -> list[list[int]]:
    """对每个节点求 k 个最近邻（用内积当球面距离代理，越大越近）。"""
    xyz = [_xyz(lat, lon) for lat, lon in nodes]
    result = []
    for i, p in enumerate(xyz):
        scored = sorted(
            (j for j in range(len(nodes)) if j != i),
            key=lambda j: -_dot(p, xyz[j]),
        )
        result.append(scored[:k])
    return result


def radius_neighbors(nodes: list, radius_deg: float = 10.0) -> list[list[int]]:
    """半径邻域：把经纬度球面距离 <= radius_deg 的点连起来。"""
    import math

    result = []
    for i in range(len(nodes)):
        lat_i, lon_i = nodes[i]
        nbrs = []
        for j in range(len(nodes)):
            if i == j:
                continue
            lat_j, lon_j = nodes[j]
            # 球面角距离（内积反余弦）
            p, q = latlon_to_xyz(lat_i, lon_i), latlon_to_xyz(lat_j, lon_j)
            d = math.degrees(math.acos(max(-1.0, min(1.0, _dot(p, q)))))
            if d <= radius_deg:
                nbrs.append(j)
        result.append(nbrs)
    return result
