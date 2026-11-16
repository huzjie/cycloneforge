# Holland 风场模型

轴对称台风风廓线：`V(r) = Vmax · (RMW/r)^B · exp(1 - (RMW/r)^B)`。

- 用于合成台风数据、反解风圈半径 R34/R50/R64
- 反解：令 `(RMW/r)^B = x`，对 `Vt/Vmax = x·exp(1-x)` 二分求 x，再 r = RMW/x^(1/B)
- 实现见 `data/holland.py`
