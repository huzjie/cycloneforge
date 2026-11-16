# -*- coding: utf-8 -*-
"""风场图：把节点风速场画成 SVG 色块。"""
from __future__ import annotations


def plot_windfield_svg(nodes: list, field: list, width: int = 400, height: int = 300) -> str:
    """nodes: [(lat, lon)]; field: 平行风速列表。"""
    if not nodes:
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>'
    lats = [p[0] for p in nodes]
    lons = [p[1] for p in nodes]
    vmax = max(field) or 1.0

    def sx(lon):
        return 20 + (lon - min(lons)) / ((max(lons) - min(lons)) or 1.0) * (width - 40)

    def sy(lat):
        return height - 20 - (lat - min(lats)) / ((max(lats) - min(lats)) or 1.0) * (height - 40)

    cells = []
    for (lat, lon), v in zip(nodes, field):
        ratio = v / vmax
        # 由风速映射到红蓝（暖色强风）
        r = int(230 * ratio + 20)
        g = int(230 * (1 - ratio) + 20)
        b = int(230 * (1 - ratio) + 20)
        cells.append(f'<circle cx="{sx(lon):.1f}" cy="{sy(lat):.1f}" r="3" '
                     f'fill="rgb({r},{g},{b})"/>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'<rect width="100%" height="100%" fill="#0a0a14"/>'
        f'{"".join(cells)}</svg>'
    )
