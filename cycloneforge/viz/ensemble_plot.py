# -*- coding: utf-8 -*-
"""集合图：多成员轨迹 + 均值轨迹。"""
from __future__ import annotations

from .track_plot import _scale


def plot_ensemble_svg(tracks: list, width: int = 400, height: int = 300) -> str:
    """tracks: [成员][步][lat, lon]。"""
    all_lats = [p[0] for m in tracks for p in m]
    all_lons = [p[1] for m in tracks for p in m]

    def sx(lon):
        return 20 + (lon - min(all_lons)) / ((max(all_lons) - min(all_lons)) or 1.0) * (width - 40)

    def sy(lat):
        return height - 20 - (lat - min(all_lats)) / ((max(all_lats) - min(all_lats)) or 1.0) * (height - 40)

    lines = []
    for m in tracks:
        pts = " ".join(f"{sx(p[1]):.1f},{sy(p[0]):.1f}" for p in m)
        lines.append(f'<polyline points="{pts}" fill="none" stroke="#88aacc" '
                     f'stroke-opacity="0.4" stroke-width="1"/>')
    # 均值轨迹
    n = max(len(m) for m in tracks)
    mean = []
    for s in range(n):
        members = [m[s] for m in tracks if s < len(m)]
        mean.append([sum(p[0] for p in members) / len(members),
                     sum(p[1] for p in members) / len(members)])
    pts = " ".join(f"{sx(p[1]):.1f},{sy(p[0]):.1f}" for p in mean)
    lines.append(f'<polyline points="{pts}" fill="none" stroke="#E60012" stroke-width="2"/>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'<rect width="100%" height="100%" fill="#ffffff"/>'
        f'{"".join(lines)}</svg>'
    )
