# -*- coding: utf-8 -*-
"""单位换算。"""
from __future__ import annotations


def ms_to_kt(v: float) -> float:
    """米/秒 -> 节（1 m/s = 1.943844 kn）。"""
    return v * 1.943844


def kt_to_ms(v: float) -> float:
    """节 -> 米/秒。"""
    return v / 1.943844


def hPa_to_kPa(p: float) -> float:
    """百帕 -> 千帕。"""
    return p / 10.0
