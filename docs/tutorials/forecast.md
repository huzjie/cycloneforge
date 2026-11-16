# 滚动自回归预测

```python
from cycloneforge.forecast.rollout import rollout_track
tracks, intensities, winds = rollout_track(model, init_features, n_steps=20)
```

`tracks` 是未来 5 天的中心位置序列，`intensities` 是强度序列，`winds` 是风圈序列。
