# -*- coding: utf-8 -*-
"""REST 路由。"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .schemas import ForecastRequest, ForecastResponse, HealthResponse
from ..model.cyclone_net import CycloneNet
from ..forecast.rollout import rollout_track
from ..model.ensemble import run_ensemble

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", version="0.1.0")


@router.post("/v1/forecast", response_model=ForecastResponse)
def forecast(req: ForecastRequest):
    if len(req.features) != 10:
        raise HTTPException(400, "features 必须为 10 维")
    net = CycloneNet(dim=32, processor_layers=4, seed=0)
    if req.n_members <= 0:
        tracks, intensities, winds = rollout_track(net, req.features, req.n_steps)
    else:
        ens = run_ensemble(net, req.features, req.n_members, req.perturb_scale, req.n_steps, 0)
        tracks = [[sum(m[s][0] for m in ens.tracks) / req.n_members,
                   sum(m[s][1] for m in ens.tracks) / req.n_members] for s in range(req.n_steps + 1)]
        intensities = [[sum(m[s][0] for m in ens.intensities) / req.n_members,
                        sum(m[s][1] for m in ens.intensities) / req.n_members]
                       for s in range(req.n_steps + 1)]
        winds = ens.winds[0] if ens.winds else []
    return ForecastResponse(track=tracks, intensity=intensities, wind=winds, n_steps=req.n_steps)
