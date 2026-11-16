# 集合预报

```python
from cycloneforge.model.ensemble import run_ensemble
ens = run_ensemble(model, init_features, n_members=50, perturb_scale=0.1, n_steps=20)
```

扰动初始场跑 50 个成员，用 `ens.tracks` 看轨迹散布。
