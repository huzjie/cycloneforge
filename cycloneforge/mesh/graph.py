# -*- coding: utf-8 -*-
"""图表示：节点特征 + 边索引。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Graph:
    """消息传递图。"""

    node_feats: list = field(default_factory=list)   # [[f0, f1, ...], ...] 每节点特征
    edge_index: tuple = field(default_factory=tuple)  # (srcs, dsts) 两个平行列表
    node_pos: list = field(default_factory=list)      # [(lat, lon), ...] 可选，用于几何信息

    @property
    def n_nodes(self) -> int:
        return len(self.node_feats)

    @property
    def n_edges(self) -> int:
        return len(self.edge_index[0]) if self.edge_index else 0

    def neighbors(self) -> dict[int, list[int]]:
        """从边索引派生邻接表。"""
        srcs, dsts = self.edge_index
        adj: dict[int, list[int]] = {i: [] for i in range(self.n_nodes)}
        for s, d in zip(srcs, dsts):
            adj[s].append(d)
        return adj


def build_graph(node_feats: list, adjacency: dict[int, list[int]], node_pos=None) -> Graph:
    """从邻接表构建无向图（边去重、双向）。"""
    from .edges import edges_from_adjacency

    ei = edges_from_adjacency(adjacency, directed=False)
    return Graph(node_feats=node_feats, edge_index=(ei.srcs, ei.dsts), node_pos=node_pos or [])
