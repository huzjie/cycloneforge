# -*- coding: utf-8 -*-
"""FastAPI 应用工厂。"""
from __future__ import annotations

from fastapi import FastAPI

from .routes import router


def create_app(config=None) -> FastAPI:
    app = FastAPI(
        title="cycloneforge",
        description="神经网络热带气旋预测引擎（WeatherNext Cyclones 方法论参考实现）",
        version="0.1.0",
    )
    app.include_router(router)
    app.state.config = config
    return app


app = create_app()
