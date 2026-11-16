# 为什么零依赖

内核只用标准库（math/random/hashlib/json），原因：

1. 克隆即跑，无环境地狱
2. 教学价值：手写 autodiff/图结构，理解底层原理
3. 便于审计：无供应链风险

代价：性能有限，教学规模（dim 16-32）足够，生产请换 PyTorch/JAX。
