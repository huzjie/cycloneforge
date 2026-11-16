# -*- coding: utf-8 -*-
"""示例：滚动自回归预测 + 集合预报 + SVG 轨迹图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cycloneforge.config import load_config
from cycloneforge.engine.pipeline import Pipeline
from cycloneforge.model.ensemble import run_ensemble
from cycloneforge.data.synthetic import SyntheticCyclone
from cycloneforge.viz.track_plot import plot_track_svg
from cycloneforge.viz.ensemble_plot import plot_ensemble_svg


def main():
    cfg = load_config("config.example.yaml")
    trained = Pipeline(cfg).train()
    model = trained["model"]

    cyc = SyntheticCyclone(f"{cfg.train.seed}:demo", n_steps=40).generate()
    init = cyc[0].features()
    n_steps = cfg.forecast.horizon_hours // cfg.forecast.step_hours

    ens = run_ensemble(model, init, cfg.ensemble.n_members, cfg.ensemble.perturb_scale, n_steps, cfg.train.seed)
    print(f"集合成员数={ens.n_members}")

    svg = plot_ensemble_svg(ens.tracks)
    out = Path("examples/ensemble.svg")
    out.write_text(svg, encoding="utf-8")
    print(f"集合轨迹图已写 {out}")


if __name__ == "__main__":
    main()
