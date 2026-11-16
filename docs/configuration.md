# 配置说明

配置文件为 YAML，分 6 节：

- `data`：数据源（synthetic / netcdf）、训练/验证/测试年份
- `model`：隐层维度、GNN 层数、球面网格细分层、启用预测头
- `forecast`：预报时长、步长、提前量误差阈值
- `ensemble`：集合成员数、扰动尺度
- `train`：训练轮数、学习率、确定性种子
- `serve`：服务 host/port

详见 `config.example.yaml` 注释。
