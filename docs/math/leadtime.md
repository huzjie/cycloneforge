# 提前量数学

给定预测轨迹 P(t) 与真值 T(t)，提前量 = 第一个使球面距离
`haversine(P(t), T(t)) > threshold` 的 t 值（小时）。

实现见 `forecast/leadtime.py`，距离用大圆公式 `utils/geo.py`。
