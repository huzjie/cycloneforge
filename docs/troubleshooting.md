# 排错

| 现象 | 可能原因 | 解决 |
|---|---|---|
| import 失败 | 未 `pip install -e .` | 安装后重试 |
| serve 起不来 | 缺 fastapi/uvicorn | `pip install -e ".[serve]"` |
| doctor 网格项失败 | 顶点数不符 | 检查 icosphere 实现 |
| 训练 loss 不降 | lr 过大/目标量程错 | 调 lr、对齐 TARGET_SCALES |
