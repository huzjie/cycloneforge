# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-11-16

### Added
- 球面网格：icosphere（二十面体递归细分）/ latlon / multires / neighbors (`grid/`)
- 图结构：graph / edges / partition (`mesh/`)
- 神经网络：标准库手写反向传播 autodiff / layers / gnn / encoder / processor / decoder (`nn/`)
- 数据管道：Holland 风场 + 台风动力学合成数据 / loader / normalize / split (`data/`)
- 模型：cyclone_net / 三要素预测头（轨迹·强度·风场）/ loss / ensemble (`model/`)
- 预测：滚动自回归 rollout / 涡旋定位追踪 tracker / 提前量 leadtime (`forecast/`)
- 评估：轨迹/强度/风场误差 metrics / CRPS / skill / benchmark (`eval/`)
- 训练：trainer / optimizer / scheduler / checkpoint (`train/`)
- CLI（doctor / train / forecast / eval / serve）+ FastAPI + Python/TS SDK + 可视化 + Web 控制台
- 提示词模板、60+ 篇技术文档、示例、Docker/K8s/Helm/Terraform/CI
