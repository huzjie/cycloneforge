# -*- coding: utf-8 -*-
"""合成台风生成器：Holland 风场 + 台风动力学，确定性可复现。"""
from __future__ import annotations

from dataclasses import dataclass

from .._core import RNG
from .holland import pressure_from_vmax, wind_radii
from .track_model import step_track
from .intensity_model import step_intensity

# 目标输出量程（用于训练归一化）
TRACK_RANGE = (-5.0, 5.0)       # 每步 dlat / dlon（度）
INTENSITY_RANGE = (8.0, 90.0)   # vmax (m/s)
PRESSURE_RANGE = (880.0, 1010.0)  # pmin (hPa)
WIND_RANGE = (0.0, 500.0)       # 风圈半径 (km)


@dataclass
class CycloneState:
    """单时次台风状态。"""

    lat: float
    lon: float
    vmax: float
    pmin: float
    rmw: float
    b: float
    sst: float
    shear: float
    humidity: float
    dlat: float
    dlon: float
    r34: float
    r50: float
    r64: float

    def features(self) -> list:
        """编码器输入（10 维，与 nn/encoder.py 量程对齐）。"""
        return [self.lat, self.lon, self.vmax, self.pmin,
                self.dlat, self.dlon, self.sst, self.shear, self.rmw, self.humidity]

    def targets(self) -> dict:
        """预测目标：track(dlat,dlon) / intensity(vmax,pmin) / wind(R34,R50,R64)。"""
        return {
            "track": [self.dlat, self.dlon],
            "intensity": [self.vmax, self.pmin],
            "wind": [self.r34, self.r50, self.r64],
        }


class SyntheticCyclone:
    """确定性合成一条台风生命史。"""

    def __init__(self, seed: int | str, n_steps: int = 40):
        self.rng = RNG(seed)
        self.n_steps = n_steps

    def generate(self, basin: str = "nwpac") -> list[CycloneState]:
        rng = self.rng
        # 初始状态（西北太平洋台风季节典型值）
        lat = rng.uniform(5.0, 25.0)
        lon = rng.uniform(115.0, 155.0)
        vmax = rng.uniform(15.0, 25.0)
        rmw = rng.uniform(40.0, 80.0)
        b = rng.uniform(1.2, 1.5)
        sst = rng.uniform(28.0, 30.0)
        shear = rng.uniform(5.0, 15.0)
        humidity = rng.uniform(0.7, 0.9)
        steer_u = rng.uniform(-3.0, 0.0)   # 每步向西分量
        steer_v = rng.uniform(1.0, 4.0)    # 每步向北分量

        states = []
        prev_dlat, prev_dlon = 0.0, 0.0
        for _ in range(self.n_steps):
            pmin = pressure_from_vmax(vmax)
            r34, r50, r64 = wind_radii(vmax, rmw, b)
            states.append(CycloneState(
                lat=lat, lon=lon, vmax=vmax, pmin=pmin, rmw=rmw, b=b,
                sst=sst, shear=shear, humidity=humidity,
                dlat=prev_dlat, dlon=prev_dlon, r34=r34, r50=r50, r64=r64,
            ))
            # 推进路径
            new_lat, new_lon = step_track(lat, lon, steer_u, steer_v, beta=1.0)
            prev_dlat, prev_dlon = new_lat - lat, new_lon - lon
            lat, lon = new_lat, new_lon
            # 推进强度（向极移动海温略降、风切变略增）
            sst = max(26.0, sst - 0.03)
            shear = min(30.0, shear + rng.uniform(-0.5, 0.5))
            vmax = step_intensity(vmax, sst, shear, humidity)
        return states


def make_dataset(cfg=None, n_cyclones: int = 6, seed_base: int = 20261116):
    """生成训练样本：特征 -> 下一步目标。返回 (xs, ys)。"""
    xs, ys = [], []
    for k in range(n_cyclones):
        cyc = SyntheticCyclone(f"{seed_base}:{k}").generate()
        for t in range(len(cyc) - 1):
            xs.append(cyc[t].features())
            tgt = cyc[t + 1].targets()
            ys.append([
                tgt["track"][0], tgt["track"][1],
                tgt["intensity"][0], tgt["intensity"][1],
                tgt["wind"][0], tgt["wind"][1], tgt["wind"][2],
            ])
    return xs, ys
