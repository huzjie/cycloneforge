# -*- coding: utf-8 -*-
"""轨迹图：把 (lon, lat) 序列画成 SVG 折线。"""
from __future__ import annotations


def _scale(vals, lo, hi, pad=0.1):
    vmin, vmax = min(vals), max(vals)
    span = (vmax - vmin) or 1.0
    return [lo + (pad + (v - vmin) / span * (1 - 2 * pad)) * (hi - lo) for v in vals]


def plot_track_svg(track: list, width: int = 400, height: int = 300) -> str:
    """track: [[lat, lon], ...] -> SVG 字符串。"""
    lats = [p[0] for p in track]
    lons = [p[1] for p in track]
    xs = _scale(lons, 20, width - 20)
    ys = _scale(lats, height - 20, 20)  # 纬度反向（北在上）
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    circles = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#E60012"/>' for x, y in zip(xs, ys)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'<rect width="100%" height="100%" fill="#ffffff"/>'
        f'<polyline points="{pts}" fill="none" stroke="#E60012" stroke-width="2"/>'
        f'{circles}</svg>'
    )
