# cycloneforge 服务镜像
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY cycloneforge ./cycloneforge

RUN pip install --no-cache-dir -e ".[serve]"

EXPOSE 8000

CMD ["uvicorn", "cycloneforge.serve.app:app", "--host", "0.0.0.0", "--port", "8000"]
