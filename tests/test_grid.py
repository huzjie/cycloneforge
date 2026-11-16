# -*- coding: utf-8 -*-
"""球面网格测试。"""
from cycloneforge.grid.icosphere import icosphere


def test_icosphere_node_count():
    g = icosphere(level=3)
    assert g.n_nodes == 642


def test_icosphere_level0():
    g = icosphere(level=0)
    assert g.n_nodes == 12


def test_neighbors():
    g = icosphere(level=2)
    adj = g.neighbors()
    for i in range(g.n_nodes):
        assert len(adj[i]) >= 4
