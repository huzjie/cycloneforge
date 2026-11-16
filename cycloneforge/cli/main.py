# -*- coding: utf-8 -*-
"""CLI 主入口：doctor / train / forecast / eval / serve。"""
from __future__ import annotations

import argparse
import sys

from ..config import load_config
from .commands import cmd_doctor, cmd_train, cmd_forecast, cmd_eval, cmd_serve


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cycloneforge", description="神经网络热带气旋预测引擎")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="自检 9 项（网格/图/前向/三头/反向/滚动/集合/评估/可复现）")

    sp = sub.add_parser("train", help="训练模型")
    sp.add_argument("--config", default="config.example.yaml")
    sp.add_argument("--epochs", type=int, default=None)

    sp = sub.add_parser("forecast", help="滚动自回归预测")
    sp.add_argument("--config", default="config.example.yaml")
    sp.add_argument("--out", default=None)

    sp = sub.add_parser("eval", help="评估五张牌")
    sp.add_argument("--config", default="config.example.yaml")

    sp = sub.add_parser("serve", help="启动 FastAPI 服务")
    sp.add_argument("--host", default=None)
    sp.add_argument("--port", type=int, default=None)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        return cmd_doctor()
    cfg = load_config(args.config)
    if args.command == "train":
        if args.epochs is not None:
            cfg.train.epochs = args.epochs
        return cmd_train(cfg)
    if args.command == "forecast":
        return cmd_forecast(cfg, args.out)
    if args.command == "eval":
        return cmd_eval(cfg)
    if args.command == "serve":
        return cmd_serve(cfg, args.host, args.port)
    return 1


if __name__ == "__main__":
    sys.exit(main())
