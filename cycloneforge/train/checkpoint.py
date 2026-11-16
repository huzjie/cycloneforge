# -*- coding: utf-8 -*-
"""检查点：模型权重存/取（JSON，无二进制依赖）。"""
from __future__ import annotations

import json
from pathlib import Path


def save_checkpoint(model, path: str) -> None:
    """保存模型权重与输出量程到 JSON。"""
    data = {
        "parameters": [p.data for p in model.parameters()],
        "output_scales": model.output_scales,
        "dim": model.dim,
    }
    Path(path).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def load_checkpoint(model, path: str) -> None:
    """从 JSON 恢复权重（参数顺序需与保存时一致）。"""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for p, val in zip(model.parameters(), data["parameters"]):
        p.data = float(val)
    model.output_scales = data.get("output_scales", model.output_scales)
