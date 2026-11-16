terraform {
  required_version = ">= 1.0"
}

# 示例：把 cycloneforge 部署到任意 K8s 集群（占位，替换 provider 配置）
variable "namespace" {
  type    = string
  default = "cycloneforge"
}

resource "kubernetes_namespace" "app" {
  metadata {
    name = var.namespace
  }
}
