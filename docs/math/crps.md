# CRPS 数学

`CRPS(F, y) = ∫ [F(x) - 1{x ≥ y}]² dx`

经验估计（能量评分式）：

`CRPS = (1/n)Σ|x_i - y| - (1/(2n²))Σ_i Σ_j |x_i - x_j|`
