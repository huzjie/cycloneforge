# 安装

```bash
pip install -e .                # 内核（零依赖）
pip install -e ".[serve]"       # + FastAPI 服务
pip install -e ".[dev]"         # + pytest/ruff
```

## 真实数据（可选）

接入 IBTrACS / ERA5 需要 `netCDF4` / `cfgrib`，见 [数据管道](guides/data-pipeline.md)。
