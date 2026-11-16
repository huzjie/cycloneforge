# 训练第一个模型

```python
from cycloneforge.config import load_config
from cycloneforge.engine.pipeline import Pipeline

cfg = load_config("config.example.yaml")
result = Pipeline(cfg).train()
print(result["final_train_loss"])
```

训练用合成数据（Holland 风场 + 台风动力学），标准库反向传播 + 动量 SGD，
loss 单调下降、确定性可复现。
