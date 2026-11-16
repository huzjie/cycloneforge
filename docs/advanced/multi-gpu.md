# 多 GPU 分片

真实天气模型在数百卡上跑。球面网格天然可按纬度带分片（`mesh/partition.py` 的
lat_band_partition），分片间只交换边界节点特征，通信量随片数线性而非二次。
