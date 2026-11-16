# -*- coding: utf-8 -*-
"""二十面体递归细分生成近均匀球面网格（icosphere）。"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from ..utils.geo import xyz_to_latlon

# 正二十面体 12 顶点（单位球坐标，归一化后）
_T = (1.0 + math.sqrt(5.0)) / 2.0
_ICO_VERTS = [
    (-1, _T, 0), (1, _T, 0), (-1, -_T, 0), (1, -_T, 0),
    (0, -1, _T), (0, 1, _T), (0, -1, -_T), (0, 1, -_T),
    (_T, 0, -1), (_T, 0, 1), (-_T, 0, -1), (-_T, 0, 1),
]
_ICO_FACES = [
    (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
    (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
    (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
    (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1),
]


def _norm(v):
    x, y, z = v
    n = math.sqrt(x * x + y * y + z * z)
    return (x / n, y / n, z / n)


def _mid(a, b):
    return _norm(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2))


@dataclass
class SphereGrid:
    """球面网格：节点经纬度 + 三角形面。"""

    nodes: list = field(default_factory=list)   # [(lat, lon), ...]
    faces: list = field(default_factory=list)   # [(i, j, k), ...]

    @property
    def n_nodes(self) -> int:
        return len(self.nodes)

    def neighbors(self) -> dict[int, list[int]]:
        """从三角形面派生邻接表。"""
        adj: dict[int, set[int]] = {i: set() for i in range(len(self.nodes))}
        for a, b, c in self.faces:
            adj[a].update((b, c))
            adj[b].update((a, c))
            adj[c].update((a, b))
        return {i: sorted(s) for i, s in adj.items()}


def icosphere(level: int = 3) -> SphereGrid:
    """生成 level 级细分的 icosphere。

    level=0：12 顶点 20 面；level=n：每条边对半，顶点数 = 10*4^n + 2。
    level=3 -> 642 顶点，近均匀覆盖球面，无经纬度极点畸变。
    """
    verts = [_norm(v) for v in _ICO_VERTS]
    faces = list(_ICO_FACES)
    cache: dict[tuple[int, int], int] = {}

    def get_mid(i: int, j: int) -> int:
        key = (min(i, j), max(i, j))
        if key in cache:
            return cache[key]
        verts.append(_mid(verts[i], verts[j]))
        idx = len(verts) - 1
        cache[key] = idx
        return idx

    for _ in range(level):
        new_faces = []
        for a, b, c in faces:
            ab, bc, ca = get_mid(a, b), get_mid(b, c), get_mid(c, a)
            new_faces += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
        faces = new_faces

    nodes = [xyz_to_latlon(*v) for v in verts]
    return SphereGrid(nodes=nodes, faces=faces)


def build(level: int = 3) -> tuple[list, dict]:
    """便捷接口：返回 (nodes, adjacency)。"""
    g = icosphere(level)
    return g.nodes, g.neighbors()
