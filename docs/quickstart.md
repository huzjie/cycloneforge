# 快速上手

1. 克隆仓库，`pip install -e .`
2. 复制 `config.example.yaml` 为 `config.yaml`，按需改模型/预报参数
3. `python -m cycloneforge.cli.main doctor` 自检
4. `python -m cycloneforge.cli.main train --config config.yaml`
5. 查看 `docs/` 下各模块文档深入学习
