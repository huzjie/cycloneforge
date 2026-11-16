# -*- coding: utf-8 -*-
"""多分辨率网格：粗细网格混合，粗网格抓大尺度、细网格抓局地。"""
from __future__ import annotations

from dataclasses import dataclass

from .icosphere import icosphere


@dataclass
class MultiResGrid:
    """多层 icosphere：level 递增，分辨率递增。"""

    levels: list

    @classmethod
    def build(cls, base_level: int = 2, top_level: int = 4):
        return cls(levels=[icosphere(l) for l in range(base_level, top_level + 1)])

    @property
    def total_nodes(self) -> int:
        return sum(g.n_nodes for g in self.levels)
