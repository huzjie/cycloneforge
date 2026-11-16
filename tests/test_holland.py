# -*- coding: utf-8 -*-
"""Holland 风场测试。"""
from cycloneforge.data.holland import wind_speed, wind_radius, wind_radii


def test_wind_speed_at_rmw():
    v = wind_speed(50.0, 40.0, 1.4, 40.0)
    assert abs(v - 50.0) < 1e-6


def test_wind_radius_monotonic():
    r34, r50, r64 = wind_radii(50.0, 40.0, 1.4)
    assert r64 < r50 < r34
