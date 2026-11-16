# -*- coding: utf-8 -*-
"""极简标量自动微分引擎（micrograd 风格，纯标准库）。

这是本项目「零依赖也能做反向传播」的核心：一个标量 Value 携带梯度，
通过闭包记录局部求导规则，backward 用拓扑排序反传。工程上这是理解
PyTorch/JAX 自动微分的最小可运行原型，也是「手写反向传播」的教学样板。
"""
from __future__ import annotations

import math


class Value:
    """标量节点：data 存值，grad 存梯度，_backward 存局部反向传播。"""

    __slots__ = ("data", "grad", "_prev", "_backward", "label")

    def __init__(self, data, _children=(), label=""):
        self.data = float(data)
        self.grad = 0.0
        # 用有序元组而非 set：set 的迭代顺序依赖对象 id() 哈希，跨进程不可复现，
        # 会让 backward 的拓扑序、进而浮点累加顺序漂移，破坏「训练确定性可复现」。
        self._prev = tuple(dict.fromkeys(_children))
        self._backward = lambda: None
        self.label = label

    # ---- 前向算子 ----
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward():
            self.grad += out.grad
            other.grad += out.grad

        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = _backward
        return out

    def __pow__(self, other):
        assert isinstance(other, (int, float)), "仅支持数值幂"
        out = Value(self.data ** other, (self,), f"**{other}")

        def _backward():
            self.grad += (other * self.data ** (other - 1)) * out.grad

        out._backward = _backward
        return out

    def exp(self):
        x = self.data
        out = Value(math.exp(x), (self,), "exp")

        def _backward():
            self.grad += out.data * out.grad

        out._backward = _backward
        return out

    def tanh(self):
        x = self.data
        t = math.tanh(x)
        out = Value(t, (self,), "tanh")

        def _backward():
            self.grad += (1 - t * t) * out.grad

        out._backward = _backward
        return out

    def relu(self):
        out = Value(self.data if self.data > 0 else 0.0, (self,), "relu")

        def _backward():
            self.grad += (1.0 if self.data > 0 else 0.0) * out.grad

        out._backward = _backward
        return out

    def sigmoid(self):
        s = 1.0 / (1.0 + math.exp(-self.data))
        out = Value(s, (self,), "sigmoid")

        def _backward():
            self.grad += s * (1 - s) * out.grad

        out._backward = _backward
        return out

    # ---- 反向便捷算子 ----
    def __neg__(self):
        return self * -1.0

    def __sub__(self, other):
        return self + (-other)

    def __truediv__(self, other):
        return self * (other ** -1)

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other

    def __rsub__(self, other):
        return other + (-self)

    def __rtruediv__(self, other):
        return other * (self ** -1)

    def __repr__(self):
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"

    # ---- 反向传播 ----
    def backward(self):
        topo = []
        visited = set()

        def build(v):
            if v not in visited:
                visited.add(v)
                for p in v._prev:
                    build(p)
                topo.append(v)

        build(self)
        self.grad = 1.0
        for v in reversed(topo):
            v._backward()

    def zero_grad(self):
        """递归清空所有参与节点梯度（训练循环用）。"""
        seen = set()

        def rec(v):
            if v in seen:
                return
            seen.add(v)
            v.grad = 0.0
            for p in v._prev:
                rec(p)

        rec(self)


def tanh(x):
    return x.tanh() if isinstance(x, Value) else math.tanh(x)


def relu(x):
    return x.relu() if isinstance(x, Value) else max(0.0, x)


def sigmoid(x):
    return x.sigmoid() if isinstance(x, Value) else 1.0 / (1.0 + math.exp(-x))


def leaky_relu(x, slope=0.01):
    if isinstance(x, Value):
        return x.relu() - (slope * (-x).relu())
    return x if x > 0 else slope * x
