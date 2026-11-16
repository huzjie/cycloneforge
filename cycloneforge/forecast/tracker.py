# -*- coding: utf-8 -*-
"""台风定位追踪：从风场/气压场找涡旋中心。"""
from __future__ import annotations


def locate_center(pressure_field: list, nodes: list) -> tuple[float, float]:
    """在气压场中定位最低气压点（近似涡旋中心）。

    pressure_field: 与 nodes 平行的气压列表（hPa）；nodes: [(lat, lon)]。
    """
    if not pressure_field:
        return (0.0, 0.0)
    idx = min(range(len(pressure_field)), key=lambda i: pressure_field[i])
    return nodes[idx]


def track_centers(pressure_fields: list, nodes: list) -> list[tuple[float, float]]:
    """逐时次定位中心，形成轨迹。pressure_fields: [时次][节点] 气压。"""
    return [locate_center(pf, nodes) for pf in pressure_fields]
