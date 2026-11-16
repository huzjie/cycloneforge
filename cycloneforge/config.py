# -*- coding: utf-8 -*-
"""配置加载：yaml -> Config 数据类，缺省值兜底。"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class DataConfig:
    source: str = "synthetic"
    train_years: list = field(default_factory=lambda: [2018, 2019, 2020])
    val_years: list = field(default_factory=lambda: [2021])
    test_years: list = field(default_factory=lambda: [2022])
    data_dir: str = "./data"


@dataclass
class ModelConfig:
    dim: int = 16
    processor_layers: int = 2
    grid_level: int = 3
    heads: list = field(default_factory=lambda: ["track", "intensity", "wind"])


@dataclass
class ForecastConfig:
    horizon_hours: int = 120
    step_hours: int = 6
    leadtime_threshold_km: float = 120.0


@dataclass
class EnsembleConfig:
    n_members: int = 50
    perturb_scale: float = 0.1


@dataclass
class TrainConfig:
    epochs: int = 60
    lr: float = 0.02
    seed: int = 20261116
    val_every: int = 20


@dataclass
class ServeConfig:
    host: str = "127.0.0.1"
    port: int = 8000


@dataclass
class Config:
    data: DataConfig = field(default_factory=DataConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    forecast: ForecastConfig = field(default_factory=ForecastConfig)
    ensemble: EnsembleConfig = field(default_factory=EnsembleConfig)
    train: TrainConfig = field(default_factory=TrainConfig)
    serve: ServeConfig = field(default_factory=ServeConfig)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Config":
        cfg = cls()
        if not d:
            return cfg
        for section, sub in d.items():
            if section == "data":
                cfg.data = DataConfig(**{**cfg.data.__dict__, **sub})
            elif section == "model":
                cfg.model = ModelConfig(**{**cfg.model.__dict__, **sub})
            elif section == "forecast":
                cfg.forecast = ForecastConfig(**{**cfg.forecast.__dict__, **sub})
            elif section == "ensemble":
                cfg.ensemble = EnsembleConfig(**{**cfg.ensemble.__dict__, **sub})
            elif section == "train":
                cfg.train = TrainConfig(**{**cfg.train.__dict__, **sub})
            elif section == "serve":
                cfg.serve = ServeConfig(**{**cfg.serve.__dict__, **sub})
        return cfg


def load_config(path: str | os.PathLike | None = None) -> Config:
    """从 yaml 加载配置；文件不存在或为空时返回缺省配置。"""
    if path is None:
        return Config()
    p = Path(path)
    if not p.exists():
        return Config()
    text = p.read_text(encoding="utf-8")
    if not text.strip():
        return Config()
    data = _parse_simple_yaml(text)
    return Config.from_dict(data)


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    """极简 yaml 子集解析：只处理本工程用到的 section/标量/列表。

    零依赖，仅够解析 config.example.yaml 的结构。
    """
    import re

    root: dict[str, Any] = {}
    current: dict[str, Any] | None = None
    current_key: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        stripped = line.strip()
        if not line[0].isspace():
            # 顶层 section
            key = stripped.rstrip(":").strip()
            current = {}
            root[key] = current
            current_key = key
            continue
        # 子键
        m = re.match(r"^\s+([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        v = v.split("#")[0].strip()
        if v.startswith("[") and v.endswith("]"):
            items = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
            parsed = []
            for it in items:
                try:
                    parsed.append(int(it))
                except ValueError:
                    parsed.append(it)
            current[k] = parsed
        elif v == "":
            current[k] = None
        else:
            try:
                current[k] = int(v)
            except ValueError:
                try:
                    current[k] = float(v)
                except ValueError:
                    current[k] = v.strip("'\"")
    return root
