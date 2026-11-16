# 自定义预测头

在 `model/cyclone_net.py` 增加新头，三步：

1. 在 `nn/decoder.py` 加头类（继承 Linear 读出的模式）
2. 在 CycloneNet.__init__ 实例化
3. 在 `train/trainer.py` 的 TARGET_SCALES 加对应量程

三头共享主干的梯度会自动约束新头。
