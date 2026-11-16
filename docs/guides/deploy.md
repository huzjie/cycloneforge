# 部署

- Docker：`docker build -f deploy/Dockerfile -t cycloneforge .`
- docker-compose：`docker compose -f deploy/docker-compose.yml up`
- K8s：`kubectl apply -f deploy/k8s/`
- Helm：`helm install cycloneforge deploy/helm`
