# -*- coding: utf-8 -*-
"""示例：训练一个 cycloneforge 模型并打印 loss 曲线。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cycloneforge.config import load_config
from cycloneforge.engine.pipeline import Pipeline


def main():
    cfg = load_config("config.example.yaml")
    result = Pipeline(cfg).train()
    print(f"样本数={result['n_samples']}  最终 train loss={result['final_train_loss']:.4f}")
    print("loss 曲线：")
    for h in result["history"]:
        print(f"  epoch {h['epoch']:>4}  train={h['train']:.4f}  val={h['val']:.4f}")


if __name__ == "__main__":
    main()
