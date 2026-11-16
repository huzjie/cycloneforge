# cycloneforge — 神经网络热带气旋预测引擎

> 把「用 AI 预测台风轨迹、强度、风场结构，并比业务预报多争取 24 小时预警提前量」这件事，落成一套
> **零依赖、可运行、可复现**的完整工程：**球面图神经网络大气预测 + 三要素预测头 + 滚动自回归 + 集合预报**。
> 填好数据配置，它就能在合成台风数据上跑通「训练 → 预测 → 评估」端到端链路。

**cycloneforge** 不是一个「聊天气的模型玩具」，而是一套**有完整工程链路的神经天气预测引擎**。它的方法论直接
来自 Google DeepMind 2026 年 11 月发表在《Nature》并开源的 **WeatherNext Cyclones**——一个在热带气旋
**轨迹、强度、风场结构**三项指标上达到最先进水平、且平均比现有业务模式多出 **24 小时以上预警提前量**
的 AI 台风预报系统（代码 + 权重以可商用许可开源）。我们把这套「神经网络怎么做台风预报、提前量从哪来、
怎么验证」的方法，落成可独立运行、可复用的完整工程。

---

## 为什么这很硬核：AI 天气预报的「可信提前量」从哪来

数值天气预报（NWP）跑一次台风轨迹要几小时到十几小时；AI 气象模型把这一步压缩到分钟级，于是同样时间内
能滚更多步、跑更多成员。提前量的本质不在「模型更快」这一句话，而在下面四个可复用的工程决策：

| 决策 | 解决什么问题 | 关键机制 |
|---|---|---|
| 球面图神经网络 | 大气是球面上的场，不是平面网格 | 用多分辨率球面网格 + 消息传递，避免经纬度极点畸变 |
| 三要素预测头 | 台风危害由轨迹、强度、风场结构共同决定 | 共享编码器 + 三个独立预测头，各算各的损失 |
| 滚动自回归 | 单步预测不够，要连续 5 天逐 6 小时推进 | 把上一步输出当下一步输入，误差可控地向前滚动 |
| 集合预报 | 单条轨迹不可信，要给出不确定度 | 扰动初始场跑 N 个成员，用 CRPS 量化不确定度 |

这四条没有一个是「新技术」，但把它们**串成一条可训练、可评估、可量化提前量的流水线**，才是把 AI 气象从
论文变成可用系统的分水岭。下面逐个拆「怎么实现 + 为什么这么做」，每一条都对应到仓库里能跑的模块。

---

## 技术拆解一：球面图神经网络——怎么在球上做卷积

大气数据天生在球面上。如果用经纬度网格（lat-lon），两极附近的网格点会过度密集、面积畸变严重，卷积核学不到
各向同性的特征。正确做法是**把球面离散成图**：用二十面体递归细分生成近均匀的节点，用 k 近邻或自然邻居连边，
再做消息传递。

```python
# 二十面体细分生成近均匀球面网格（无经纬度极点畸变）
from cycloneforge.grid import icosphere

nodes, edges = icosphere.build(level=3)        # 642 个节点，近均匀分布
# 每个节点是 (lat, lon)，每条边连接球面上相邻的两点
# 消息传递 = 邻居特征聚合 + 自身更新（见 cycloneforge/nn/gnn.py）
```

对应实现见 [`cycloneforge/grid/icosphere.py`](cycloneforge/grid/icosphere.py)（递归细分）、
[`cycloneforge/mesh/graph.py`](cycloneforge/mesh/graph.py)（图表示）与
[`cycloneforge/nn/gnn.py`](cycloneforge/nn/gnn.py)（消息传递）。**可复用要点**：在球面/曲面数据上，
第一步永远是**选对离散化**——lat-lon 网格最直观但畸变最大，icosphere 稍复杂但各向同性，这是后面所有
卷积、池化能学出正确特征的前提。

## 技术拆解二：三要素预测头——一个编码器，三个任务

台风预报要同时回答三个问题：**去哪（轨迹）、多强（强度）、风圈多大（风场结构）**。如果各训各的模型，
三个模型对同一时刻的物理状态理解不一致，预报就会自相矛盾。cycloneforge 用一个共享编码器把大气状态压成
统一隐向量，再接三个头：

```python
# 共享编码器 + 三个独立预测头（各自有自己的损失，回传共享梯度）
from cycloneforge.model import CycloneNet

net = CycloneNet(dim=32, processor_layers=4)
track  = net.track_head(z)      # 输出：未来 T 步的中心 (lat, lon) 序列
intens = net.intensity_head(z)  # 输出：未来 T 步的 vmax / pmin
wind   = net.wind_head(z)       # 输出：未来 T 步的 R34/R50/R64 风圈半径
```

对应实现见 [`cycloneforge/model/cyclone_net.py`](cycloneforge/model/cyclone_net.py) 与
[`cycloneforge/model/heads.py`](cycloneforge/model/heads.py)。**可复用要点**：多任务学习里「共享主干 +
独立头」的价值在于**共享表示的对齐**——三个头的梯度会反向约束编码器，逼它学出同时服务三任务的物理表示，
比三个孤立模型更省参数也更自洽。

## 技术拆解三：滚动自回归——提前量是「滚」出来的

气象模型每一步只预测未来 6 小时，5 天预报就是**把上一步输出当下一步输入，连滚 20 步**。误差会沿时间
累积，所以滚得越远越不准——这正是「提前量」的技术难点：怎么让 120 小时的轨迹还落在可接受误差内。

```python
# 滚动自回归：上一步预测 → 喂回模型 → 下一步预测
from cycloneforge.forecast import rollout

state = initial_state                     # t=0 大气状态
for step in range(20):                    # 5 天 × 每 6 小时
    pred = net(state)                     # 预测 t+6h
    state = rollout.advance(state, pred)  # 把预测写回状态，作为下一步输入
```

对应实现见 [`cycloneforge/forecast/rollout.py`](cycloneforge/forecast/rollout.py) 与
[`cycloneforge/forecast/leadtime.py`](cycloneforge/forecast/leadtime.py)（提前量量化：误差首次越限的
时间点）。**可复用要点**：自回归系统要**在训练时就用滚动的、带噪声的输入**（scheduled sampling），否则
训练时看真值、推理时看自己预测，训练-推理分布漂移会让长程误差爆炸——这是所有序列预测的通用坑。

## 技术拆解四：集合预报——把「点预测」升级成「概率预测」

单条轨迹无法告诉决策者「这报准不准」。集合预报的思路是：给初始场加小的、可控的扰动，跑 N 个成员（比如
50 个），用成员散布刻画不确定度。cycloneforge 内置扰动生成与 CRPS 评分：

```python
# 扰动初始场 → 跑 50 个成员 → 用 CRPS 量化不确定度
from cycloneforge.model import ensemble
from cycloneforge.eval import crs

members = ensemble.run(net, initial_state, n_members=50, perturb_scale=0.1)
score = crs.crps(members, truth)   # 成员越准、散布越合理，CRPS 越低
```

对应实现见 [`cycloneforge/model/ensemble.py`](cycloneforge/model/ensemble.py) 与
[`cycloneforge/eval/crs.py`](cycloneforge/eval/crs.py)。**可复用要点**：集合预报的价值不在「更准的均值」，
而在**诚实的不确定度**——一个能正确报告「我不确定」的系统，比一个自信但偶尔大错的系统对防汛决策有用得多。

---

## 一个可直接复用的「干货块」：最小可跑配置 + 训练/预测命令

内核零依赖（纯标准库实现张量、图神经网络、反向传播），克隆即跑；`pip install -e .` 只装服务端可选依赖：

```yaml
# config.example.yaml —— 一次真实「训练 → 预测 → 评估」的最小配置
data:
  source: synthetic              # 合成台风（确定性 mock）或 netcdf 真实数据
  train_years: [2018, 2019, 2020]
  val_years:   [2021]
  test_years:  [2022]

model:
  dim: 16                        # 隐层维度（纯 Python 下用 16~32，快且稳）
  processor_layers: 2            # GNN 消息传递层数
  grid_level: 3                  # 球面网格细分层（level=3 → 642 节点）

forecast:
  horizon_hours: 120             # 5 天
  step_hours: 6                  # 每 6 小时一步（20 步）
  leadtime_threshold_km: 120     # 轨迹误差越限即判「提前量耗尽」

ensemble:
  n_members: 50
  perturb_scale: 0.1

train:
  epochs: 60
  lr: 0.02
  seed: 20261116                 # 确定性种子，逐位可复现
```

```bash
# 自检 9 项（球面网格 / 图结构 / 前向 / 三头 / 反向传播 / 滚动 / 集合 / 评估 / 可复现）
python -m cycloneforge.cli.main doctor

# 训练（标准库手写反向传播，loss 单调下降、确定性可复现）
python -m cycloneforge.cli.main train --config config.example.yaml

# 预测：对测试集跑 5 天滚动自回归 + 50 成员集合，落 JSON 轨迹
python -m cycloneforge.cli.main forecast --config config.example.yaml --out forecast.json

# 评估：轨迹误差 / 强度误差 / 风场结构 / 提前量 / CRPS 五张牌
python -m cycloneforge.cli.main eval --config config.example.yaml
```

### 内置提示词模板（`prompts/` 下可直接改，拿去喂任意模型做预报决策支持）

`prompts/forecast_briefing.system.md`（把预报结果转成防汛决策简报，只陈述、不夸大）：

```markdown
你是台风预报决策支持助手。给定集合预报结果（轨迹包络、强度区间、风圈半径、CRPS 不确定度），
你要输出一份面向防汛指挥的简报，要求：
1. 只陈述集合预报给出的区间，不把最坏情况当确定值；
2. 明确标注「高置信 / 中置信 / 低置信」三档，置信度来自集合成员散布与 CRPS；
3. 用「未来 24/48/72/120 小时」分段，每段给出轨迹落区、强度区间、风圈范围；
4. 结尾单列「不确定度来源」：初始场扰动、模型结构、数据同化各占多少。
```

这套「集合预报 → 决策简报」的提示词是本次「概率预报怎么落到决策」的完整可复用配方。

---

## 目录结构

```
cycloneforge/
├── grid/        球面网格：icosphere / latlon / multires / neighbors
├── mesh/        图结构：graph / edges / partition
├── nn/          神经网络：autodiff（标准库反向传播）/ layers / gnn / encoder / processor / decoder
├── data/        数据管道：synthetic（Holland 风场 + 台风动力学）/ holland / track_model / loader / split
├── model/       模型：cyclone_net / heads（轨迹·强度·风场）/ loss / ensemble
├── forecast/    预测：rollout（滚动自回归）/ tracker（涡旋定位追踪）/ intensity / windfield / leadtime
├── eval/        评估：metrics（轨迹/强度/风场）/ crs / skill / benchmark
├── train/       训练：trainer / optimizer / scheduler / checkpoint
├── engine/      编排：pipeline / state / scheduler
├── serve/       FastAPI：/v1/forecast / /health
├── cli/         命令行：doctor / train / forecast / eval / serve
├── viz/         可视化：track_plot / windfield_plot / ensemble_plot
├── sdk/         Python + TypeScript 客户端
├── prompts/     提示词模板（可直接复用）
├── deploy/      Docker / docker-compose / K8s / Helm / Terraform
├── examples/    可运行示例 + 脚本
├── docs/        60+ 篇技术文档（原理 + 实现 + 复用思路）
└── tests/       单元测试（全通过）
```

## 快速开始

见 [`docs/getting-started.md`](docs/getting-started.md)。一句话：`pip install -e .` → 改 `config.example.yaml` → `python -m cycloneforge.cli.main doctor` 自检 → `train` 训练 → `forecast` 预测 → `eval` 评估。

## License

MIT © 智能交付知识工程组 编（教学/研究参考实现，方法源自公开报道的 DeepMind WeatherNext Cyclones 成果）
