# -*- coding: utf-8 -*-
"""API schema（pydantic）。"""
from __future__ import annotations

from typing import Optional

try:
    from pydantic import BaseModel, Field
except ImportError:  # 内核零依赖：无 pydantic 时用轻量占位
    class BaseModel:  # type: ignore[no-redef]
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    def Field(default=None, **kwargs):  # type: ignore[misc]
        return default


class ForecastRequest(BaseModel):
    features: list = Field(default_factory=list, description="10 维台风状态特征")
    n_steps: int = Field(default=20, description="滚动步数（默认 20 步 = 5 天 × 6h）")
    n_members: int = Field(default=0, description="集合成员数（0 = 单成员）")
    perturb_scale: float = Field(default=0.1)


class ForecastResponse(BaseModel):
    track: list = []
    intensity: list = []
    wind: list = []
    n_steps: int = 0


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
