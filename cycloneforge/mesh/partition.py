# -*- coding: utf-8 -*-
"""图分区：把球面节点按纬度带切块（简化多 GPU/分片场景）。"""
from __future__ import annotations


def balanced_partition(n_nodes: int, n_parts: int) -> list[list[int]]:
    """把 n 个节点均匀分成 n_parts 份（连续区间）。"""
    parts = [[] for _ in range(n_parts)]
    for i in range(n_nodes):
        parts[i % n_parts].append(i)
    return parts


def lat_band_partition(node_pos: list, n_bands: int = 8) -> list[list[int]]:
    """按纬度带分区（真实天气模型常用纬度分片减少通信）。"""
    if not node_pos:
        return balanced_partition(len(node_pos), n_bands)
    lats = sorted(range(len(node_pos)), key=lambda i: node_pos[i][0])
    bands = [[] for _ in range(n_bands)]
    for idx, node in enumerate(lats):
        bands[idx * n_bands // len(lats)].append(node)
    return bands
