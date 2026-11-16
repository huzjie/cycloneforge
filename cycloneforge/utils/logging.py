# -*- coding: utf-8 -*-
"""日志工具。"""
from __future__ import annotations

import logging
import sys

_FMT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO), format=_FMT, stream=sys.stderr)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
