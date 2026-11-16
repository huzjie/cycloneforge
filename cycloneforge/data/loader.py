# -*- coding: utf-8 -*-
"""真实数据加载：CSV/JSON 直接读，NetCDF 走外部依赖（文档化接口）。"""
from __future__ import annotations

import csv
import json
from pathlib import Path


def load_csv(path: str) -> list[dict]:
    """从 CSV 加载历史台风记录（列名：lat,lon,vmax,pmin,rmw,sst,shear,humidity）。"""
    rows = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({k: float(v) for k, v in r.items()})
    return rows


def load_json(path: str) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_netcdf(path: str):
    """NetCDF/GRIB 加载（需额外安装 netCDF4 / cfgrib，内核保持零依赖）。

    生产环境建议：pip install "cycloneforge[data]" 后接入 IBTrACS / ERA5 再分析数据。
    本函数仅做接口占位，返回文档说明。
    """
    try:
        import netCDF4  # noqa: F401
    except ImportError:
        raise RuntimeError(
            "加载 NetCDF 需要 netCDF4：pip install netCDF4。"
            "教学场景请先用 synthetic 数据跑通全链路。"
        )
    raise NotImplementedError("请实现具体变量提取，见 docs/data-pipeline.md")
