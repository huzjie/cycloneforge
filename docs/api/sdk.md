# SDK

- Python：`sdk/python/client.py` 的 CycloneClient
- TypeScript：`sdk/typescript/index.ts` 的 CycloneClient（fetch）

```python
from sdk.python.client import CycloneClient
c = CycloneClient("http://127.0.0.1:8000")
print(c.forecast([10,130,20,1000,1,-1,29,10,50,0.8], n_steps=20))
```
