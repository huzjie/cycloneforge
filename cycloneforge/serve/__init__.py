# -*- coding: utf-8 -*-
"""HTTP 服务：FastAPI。"""
from .app import create_app
from .routes import router
from .schemas import ForecastRequest, ForecastResponse, HealthResponse

__all__ = ["create_app", "router", "ForecastRequest", "ForecastResponse", "HealthResponse"]
