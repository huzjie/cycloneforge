# 启动服务

```bash
pip install -e ".[serve]"
python -m cycloneforge.cli.main serve
```

然后 `curl http://127.0.0.1:8000/health` 验证。
