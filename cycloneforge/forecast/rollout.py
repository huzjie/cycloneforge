# -*- coding: utf-8 -*-
"""滚动自回归：把上一步预测写回状态，作为下一步输入。"""
from __future__ import annotations

# 特征索引（与 data/synthetic.py 的 features() 对齐）
IDX = {"lat": 0, "lon": 1, "vmax": 2, "pmin": 3, "dlat": 4, "dlon": 5,
       "sst": 6, "shear": 7, "rmw": 8, "humidity": 9}


def advance_state(features: list, pred: dict) -> list:
    """把一步预测写回状态，得到下一步输入特征。"""
    f = list(features)
    dlat, dlon = pred["track"][0], pred["track"][1]
    vmax, pmin = pred["intensity"][0], pred["intensity"][1]
    f[IDX["lat"]] = f[IDX["lat"]] + dlat
    f[IDX["lon"]] = f[IDX["lon"]] + dlon
    f[IDX["vmax"]] = vmax
    f[IDX["pmin"]] = pmin
    f[IDX["dlat"]] = dlat
    f[IDX["dlon"]] = dlon
    return f


def rollout_track(model, initial_features: list, n_steps: int):
    """滚动自回归 n_steps 步。返回 (tracks, intensities, winds)。"""
    tracks = [[initial_features[IDX["lat"]], initial_features[IDX["lon"]]]]
    intensities = [[initial_features[IDX["vmax"]], initial_features[IDX["pmin"]]]]
    winds = []
    feats = list(initial_features)
    for _ in range(n_steps):
        pred = model.predict(feats)
        feats = advance_state(feats, pred)
        tracks.append([feats[IDX["lat"]], feats[IDX["lon"]]])
        intensities.append([feats[IDX["vmax"]], feats[IDX["pmin"]]])
        winds.append(list(pred["wind"]))
    return tracks, intensities, winds
