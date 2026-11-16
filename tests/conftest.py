# -*- coding: utf-8 -*-
"""pytest 配置：确保仓库根目录在 sys.path。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
