# 快速开始

## 三步跑通

```bash
# 1. 安装（内核零依赖，pip 只装服务端可选依赖）
pip install -e .

# 2. 自检 9 项
python -m cycloneforge.cli.main doctor

# 3. 训练 -> 预测 -> 评估
python -m cycloneforge.cli.main train --config config.example.yaml
python -m cycloneforge.cli.main forecast --config config.example.yaml --out forecast.json
python -m cycloneforge.cli.main eval --config config.example.yaml
```

## 环境要求

- Python >= 3.9，无第三方依赖即可跑内核
- 可选 `pip install -e ".[serve]"` 启用 FastAPI 服务
- 可选 `pip install -e ".[dev]"` 启用测试与 lint

## 下一步

- [架构总览](architecture.md)
- [训练第一个模型](tutorials/train-first-model.md)
