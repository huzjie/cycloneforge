# 损失函数

三头 MSE 加权：`L = w_track·MSE_track + w_intensity·MSE_intensity + w_wind·MSE_wind`。
目标按量程归一化到 [0,1] 量级，避免量纲差异导致某头主导梯度。
