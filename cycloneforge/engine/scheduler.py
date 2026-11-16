# -*- coding: utf-8 -*-
"""任务调度：简单 FIFO 任务队列。"""
from __future__ import annotations

from collections import deque


class JobScheduler:
    """顺序执行的任务队列（演示/单机版）。"""

    def __init__(self):
        self._queue = deque()

    def submit(self, fn, *args, **kwargs):
        self._queue.append((fn, args, kwargs))

    def run_all(self):
        results = []
        while self._queue:
            fn, args, kwargs = self._queue.popleft()
            results.append(fn(*args, **kwargs))
        return results

    @property
    def pending(self) -> int:
        return len(self._queue)
