# -*- coding: utf-8 -*-
"""CLI 各子命令实现。"""
from __future__ import annotations

import json
import sys

from ..utils.logging import setup_logging, get_logger

log = get_logger("cycloneforge")


def cmd_doctor() -> int:
    """自检 9 项，全绿返回 0。"""
    from ..model.cyclone_net import CycloneNet
    from ..grid.icosphere import icosphere
    from ..mesh.graph import build_graph
    from ..nn.gnn import GCNLayer
    from ..nn.autodiff import Value
    from ..data.synthetic import SyntheticCyclone, make_dataset
    from ..forecast.rollout import rollout_track
    from ..model.ensemble import run_ensemble
    from ..eval.benchmark import run_benchmark
    from ..train.trainer import Trainer

    checks = []

    def check(name, fn):
        try:
            fn()
            checks.append((name, True, ""))
        except Exception as e:  # noqa: BLE001
            checks.append((name, False, repr(e)))

    # 1. 球面网格
    def c1():
        g = icosphere(3)
        assert g.n_nodes == 642, g.n_nodes
    check("球面网格 icosphere", c1)

    # 2. 图结构
    def c2():
        g = icosphere(2)
        adj = g.neighbors()
        graph = build_graph([[0.0] * 4] * g.n_nodes, adj)
        assert graph.n_edges > 0
    check("图结构 graph", c2)

    # 3. 前向
    def c3():
        net = CycloneNet(dim=16, processor_layers=2, seed=1)
        out = net.forward([10.0, 130.0, 20.0, 1000.0, 1.0, -1.0, 29.0, 10.0, 50.0, 0.8])
        assert set(out) == {"track", "intensity", "wind"}
    check("模型前向 forward", c3)

    # 4. 三头
    def c4():
        net = CycloneNet(dim=16, processor_layers=2, seed=1)
        out = net.forward([10.0, 130.0, 20.0, 1000.0, 1.0, -1.0, 29.0, 10.0, 50.0, 0.8])
        assert len(out["track"]) == 2 and len(out["intensity"]) == 2 and len(out["wind"]) == 3
    check("三要素预测头", c4)

    # 5. 反向传播
    def c5():
        a, b = Value(2.0), Value(-3.0)
        c = a * b + b.tanh()
        c.backward()
        assert abs(a.grad - (-3.0)) < 1e-9
    check("标准库反向传播 autodiff", c5)

    # 6. 滚动自回归
    def c6():
        net = CycloneNet(dim=16, processor_layers=2, seed=1)
        cyc = SyntheticCyclone("doctor", n_steps=10).generate()
        tracks, _, _ = rollout_track(net, cyc[0].features(), 4)
        assert len(tracks) == 5
    check("滚动自回归 rollout", c6)

    # 7. 集合预报
    def c7():
        net = CycloneNet(dim=16, processor_layers=2, seed=1)
        cyc = SyntheticCyclone("doctor", n_steps=10).generate()
        ens = run_ensemble(net, cyc[0].features(), 5, 0.1, 4, 0)
        assert ens.n_members == 5
    check("集合预报 ensemble", c7)

    # 8. 评估
    def c8():
        net = CycloneNet(dim=16, processor_layers=2, seed=1)
        cyc = SyntheticCyclone("doctor", n_steps=10).generate()
        truth = [[s.lat, s.lon] for s in cyc]
        bench = run_benchmark(net, cyc[0].features(), truth, 4, 6.0, 120.0, 5, 0.1, 0)
        assert bench.mean_track_km >= 0
    check("评估 benchmark", c8)

    # 9. 训练可复现（确定性）
    def c9():
        xs, ys = make_dataset(n_cyclones=2, seed_base=7)
        n1 = CycloneNet(dim=16, processor_layers=2, seed=3)
        t1 = Trainer(n1, xs, ys, lr=0.01, epochs=3, val_every=2)
        r1 = t1.train()
        n2 = CycloneNet(dim=16, processor_layers=2, seed=3)
        t2 = Trainer(n2, xs, ys, lr=0.01, epochs=3, val_every=2)
        r2 = t2.train()
        assert r1["final_train_loss"] == r2["final_train_loss"]
    check("训练确定性可复现", c9)

    ok = 0
    for name, passed, err in checks:
        if passed:
            ok += 1
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name}: {err}")
    print(f"doctor 自检：{ok}/{len(checks)} 通过")
    return 0 if ok == len(checks) else 1


def cmd_train(cfg) -> int:
    setup_logging()
    from ..engine.pipeline import Pipeline

    print("开始训练...")
    result = Pipeline(cfg).train()
    hist = result["history"]
    print(f"样本数={result['n_samples']}  初始 train loss={hist[0]['train']:.4f}  最终={result['final_train_loss']:.4f}")
    print("loss 曲线（每 %d epoch）：" % cfg.train.val_every)
    for h in hist:
        print(f"  epoch {h['epoch']:>4}  train={h['train']:.4f}  val={h['val']:.4f}")
    return 0


def cmd_forecast(cfg, out_path) -> int:
    setup_logging()
    from ..engine.pipeline import Pipeline

    print("训练并预测...")
    trained = Pipeline(cfg).train()
    result = Pipeline(cfg).forecast(trained["model"], out_path)
    print(f"滚动 {result['n_steps']} 步，轨迹首点={result['track'][0]}")
    if out_path:
        print(f"预测已写 {out_path}")
    return 0


def cmd_eval(cfg) -> int:
    setup_logging()
    from ..engine.pipeline import Pipeline

    print("训练并评估...")
    trained = Pipeline(cfg).train()
    bench = Pipeline(cfg).eval(trained["model"])
    print("评估五张牌：")
    print(json.dumps(bench, ensure_ascii=False, indent=2))
    return 0


def cmd_serve(cfg, host, port) -> int:
    setup_logging()
    try:
        import uvicorn  # noqa: F401
    except ImportError:
        print("启动服务需要 fastapi/uvicorn：pip install -e '.[serve]'", file=sys.stderr)
        return 1
    from ..serve.app import create_app

    app = create_app(cfg)
    uvicorn.run(app, host=host or cfg.serve.host, port=port or cfg.serve.port)
    return 0
