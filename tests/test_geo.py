# -*- coding: utf-8 -*-
"""球面几何测试。"""
import math
from cycloneforge.utils.geo import haversine_km, bearing_deg, latlon_to_xyz, xyz_to_latlon


def test_haversine_zero():
    assert haversine_km(0, 0, 0, 0) == 0.0


def test_haversine_known():
    # 赤道上经度差 1 度约 111.19 km
    d = haversine_km(0, 0, 0, 1)
    assert abs(d - 111.19) < 0.5


def test_xyz_roundtrip():
    x, y, z = latlon_to_xyz(30, 120)
    lat, lon = xyz_to_latlon(x, y, z)
    assert abs(lat - 30) < 1e-9
    assert abs(lon - 120) < 1e-9


def test_bearing_north():
    b = bearing_deg(0, 0, 10, 0)
    assert abs(b - 0) < 1e-6
