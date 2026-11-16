# -*- coding: utf-8 -*-
"""强度模型：海温/风切变驱动的强度演变（确定性）。"""
from __future__ import annotations


def potential_intensity(sst: float) -> float:
    """由海温估潜在最大强度（m/s，简化经验式）。"""
    return max(0.0, 8.5 * (sst - 26.0))


def step_intensity(vmax: float, sst: float, shear: float, humidity: float) -> float:
    """一步强度更新：向潜在强度逼近，被风切变/湿度抑制。"""
    v_pot = potential_intensity(sst)
    shear_damp = max(0.0, 1.0 - shear / 30.0)
    target = v_pot * shear_damp * (0.5 + 0.5 * humidity)
    dv = 0.15 * (target - vmax)     # 松弛因子，缓慢逼近
    return max(8.0, vmax + dv)
