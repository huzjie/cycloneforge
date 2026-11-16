# -*- coding: utf-8 -*-
"""运行状态：一次训练/预测任务的轻量状态记录。"""
from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class RunRecord:
    """一次运行的记录。"""

    task: str = ""
    status: str = "pending"   # pending / running / done / failed
    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None
    meta: dict = field(default_factory=dict)

    def finish(self, status: str = "done", **meta):
        self.status = status
        self.finished_at = time.time()
        self.meta.update(meta)


class RunState:
    """进程内运行状态仓库（简化，生产可换 Redis/DB）。"""

    def __init__(self):
        self._records: dict[str, RunRecord] = {}

    def start(self, task: str) -> RunRecord:
        rec = RunRecord(task=task, status="running")
        self._records[task] = rec
        return rec

    def get(self, task: str) -> RunRecord | None:
        return self._records.get(task)
