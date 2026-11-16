# 从合成数据迁移到真实数据

保持 `make_dataset` 返回 (xs, ys) 的契约不变，替换数据来源即可。关键：

1. 特征顺序必须与 `data/synthetic.py` 的 features() 一致
2. 目标量程要与 `train/trainer.py` 的 TARGET_SCALES 对齐
3. 真实数据先归一化到同一量程，避免训练发散
