# -*- coding: utf-8 -*-
"""评估测试。"""
from cycloneforge.eval.metrics import track_error_km, summarize_errors
from cycloneforge.eval.crs import crps


def test_track_error_zero():
    assert track_error_km([0, 0], [0, 0]) == 0.0


def test_crps_perfect():
    # 所有成员都等于真值 -> CRPS = 0
    assert crps([5.0, 5.0, 5.0], 5.0) == 0.0


def test_crps_positive():
    assert crps([4.0, 6.0], 5.0) > 0.0
