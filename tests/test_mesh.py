# -*- coding: utf-8 -*-
"""图结构测试。"""
from cycloneforge.mesh.graph import build_graph
from cycloneforge.mesh.edges import edges_from_adjacency


def test_build_graph():
    adj = {0: [1, 2], 1: [0], 2: [0]}
    g = build_graph([[0.0, 0.0]] * 3, adj)
    assert g.n_nodes == 3
    # 无向图双向边去重：0-1、0-2 两条无向边 → 4 条有向边（0→1,1→0,0→2,2→0）
    assert g.n_edges == 4


def test_edges_from_adjacency_undirected():
    adj = {0: [1], 1: [0]}
    e = edges_from_adjacency(adj)
    assert e.size == 2
