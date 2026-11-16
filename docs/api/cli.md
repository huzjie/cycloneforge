# CLI 命令

- `doctor`：自检 9 项（网格/图/前向/三头/反向/滚动/集合/评估/可复现）
- `train`：训练模型，打印 loss 曲线
- `forecast`：滚动自回归预测，可 `--out forecast.json`
- `eval`：评估五张牌（轨迹/强度/风场/提前量/CRPS）
- `serve`：启动 FastAPI 服务
