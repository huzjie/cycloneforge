# -*- coding: utf-8 -*-
"""示例：生成一条合成台风并打印状态。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cycloneforge.data.synthetic import SyntheticCyclone


def main():
    cyc = SyntheticCyclone("demo", n_steps=10).generate()
    print("step |   lat    |   lon    | vmax | pmin  |  R34  |  R50  |  R64")
    for i, s in enumerate(cyc):
        print(f"{i:>4} | {s.lat:>8.2f} | {s.lon:>8.2f} | {s.vmax:>4.1f} | "
              f"{s.pmin:>5.0f} | {s.r34:>5.0f} | {s.r50:>5.0f} | {s.r64:>5.0f}")


if __name__ == "__main__":
    main()
