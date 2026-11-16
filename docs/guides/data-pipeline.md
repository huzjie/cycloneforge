# 数据管道接入真实数据

1. 教学场景用 `synthetic` 数据（零依赖）跑通全链路
2. 生产接 IBTrACS（历史台风）/ ERA5（再分析）：
   - `pip install netCDF4 cfgrib`
   - 实现 `data/loader.py` 的 `load_netcdf`，提取 10 维特征
   - 目标：lat, lon, vmax, pmin, dlat, dlon, sst, shear, rmw, humidity
