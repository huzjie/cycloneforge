# REST API

- `GET /health`：健康检查
- `POST /v1/forecast`：入参 features(10 维) + n_steps + n_members + perturb_scale，
  返回轨迹/强度/风场

示例：
```bash
curl -X POST http://127.0.0.1:8000/v1/forecast \
  -H 'Content-Type: application/json' \
  -d '{"features":[10,130,20,1000,1,-1,29,10,50,0.8],"n_steps":20,"n_members":50}'
```
