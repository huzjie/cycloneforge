# -*- coding: utf-8 -*-
"""边索引：邻接表与 (srcs, dsts) 双列表互转。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EdgeIndex:
    srcs: list
    dsts: list

    @property
    def size(self) -> int:
        return len(self.srcs)

    def as_tuples(self) -> list[tuple[int, int]]:
        return list(zip(self.srcs, self.dsts))

    def reverse(self) -> "EdgeIndex":
        return EdgeIndex(self.dsts[:], self.srcs[:])


def edges_from_adjacency(adjacency: dict[int, list[int]], directed: bool = False) -> EdgeIndex:
    """邻接表 -> 边索引。

    directed=False（默认，无向图）：为每条邻接关系生成 (i→j) 与 (j→i) 两个方向，
        再按首次出现顺序去重，适配「邻接表已双向列出」的输入（不会重复加边）。
    directed=True（有向图）：仅按邻接表原样生成 (i→j)。
    """
    pairs: list[tuple[int, int]] = []
    for i, nbrs in adjacency.items():
        for j in nbrs:
            pairs.append((i, j))
            if not directed:
                pairs.append((j, i))
    seen: set[tuple[int, int]] = set()
    srcs, dsts = [], []
    for s, d in pairs:
        if (s, d) not in seen:
            seen.add((s, d))
            srcs.append(s)
            dsts.append(d)
    return EdgeIndex(srcs, dsts)
