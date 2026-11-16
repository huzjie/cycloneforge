# -*- coding: utf-8 -*-
"""经纬度网格：规则 lat-lon 网格（用于对比与简单场景）。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LatLonGrid:
    """规则经纬度网格。"""

    lat_start: float = -90.0
    lat_end: float = 90.0
    lon_start: float = -180.0
    lon_end: float = 180.0
    n_lat: int = 73
    n_lon: int = 144

    @property
    def lats(self) -> list:
        step = (self.lat_end - self.lat_start) / max(1, self.n_lat - 1)
        return [self.lat_start + i * step for i in range(self.n_lat)]

    @property
    def lons(self) -> list:
        step = (self.lon_end - self.lon_start) / max(1, self.n_lon - 1)
        return [self.lon_start + i * step for i in range(self.n_lon)]

    @property
    def shape(self) -> tuple[int, int]:
        return (self.n_lat, self.n_lon)

    def nodes(self) -> list:
        return [(lat, lon) for lat in self.lats for lon in self.lons]


def build(n_lat: int = 73, n_lon: int = 144) -> LatLonGrid:
    return LatLonGrid(n_lat=n_lat, n_lon=n_lon)
