# 评估

```python
from cycloneforge.eval.benchmark import run_benchmark
bench = run_benchmark(model, init, truth, n_steps, step_hours, threshold_km, n_members, perturb_scale)
print(bench.as_dict())
```

输出五张牌：平均轨迹误差、最大轨迹误差、平均提前量、CRPS、技能评分。
