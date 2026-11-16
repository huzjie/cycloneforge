# -*- coding: utf-8 -*-
"""cycloneforge Python 客户端（调用 /v1/forecast）。"""
from __future__ import annotations

import json
import urllib.request


class CycloneClient:
    """HTTP 客户端。"""

    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def health(self) -> dict:
        return self._get("/health")

    def forecast(self, features: list, n_steps: int = 20, n_members: int = 0,
                 perturb_scale: float = 0.1) -> dict:
        payload = {"features": features, "n_steps": n_steps,
                   "n_members": n_members, "perturb_scale": perturb_scale}
        return self._post("/v1/forecast", payload)

    def _get(self, path: str) -> dict:
        with urllib.request.urlopen(self.base_url + path, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))

    def _post(self, path: str, payload: dict) -> dict:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.base_url + path, data=data,
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode("utf-8"))
