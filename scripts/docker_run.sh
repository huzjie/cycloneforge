#!/usr/bin/env bash
# 构建并启动 Docker 服务
set -e
cd "$(dirname "$0")/.."
docker build -f deploy/Dockerfile -t cycloneforge:latest .
docker run --rm -p 8000:8000 cycloneforge:latest
