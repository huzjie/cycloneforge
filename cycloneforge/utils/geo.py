# -*- coding: utf-8 -*-
"""球面几何：距离/方位/坐标变换（纯标准库）。"""
from __future__ import annotations

import math

EARTH_RADIUS_KM = 6371.0


def _rad(d: float) -> float:
    return math.radians(d)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """两点间大圆距离（km）。"""
    dlat = _rad(lat2 - lat1)
    dlon = _rad(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(_rad(lat1)) * math.cos(_rad(lat2)) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(min(1.0, math.sqrt(a)))


def bearing_deg(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """初始方位角（度，0=北，顺时针）。"""
    p1, p2 = _rad(lat1), _rad(lat2)
    dl = _rad(lon2 - lon1)
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return (math.degrees(math.atan2(y, x)) + 360.0) % 360.0


def latlon_to_xyz(lat: float, lon: float) -> tuple[float, float, float]:
    """经纬度 -> 单位球三维笛卡尔坐标。"""
    p, l = _rad(lat), _rad(lon)
    return (math.cos(p) * math.cos(l), math.cos(p) * math.sin(l), math.sin(p))


def xyz_to_latlon(x: float, y: float, z: float) -> tuple[float, float]:
    """单位球三维笛卡尔坐标 -> 经纬度。"""
    lat = math.degrees(math.asin(max(-1.0, min(1.0, z))))
    lon = math.degrees(math.atan2(y, x))
    return lat, lon
