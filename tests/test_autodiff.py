# -*- coding: utf-8 -*-
"""反向传播测试。"""
from cycloneforge.nn.autodiff import Value


def test_add_backward():
    a, b = Value(2.0), Value(3.0)
    (a + b).backward()
    assert a.grad == 1.0 and b.grad == 1.0


def test_mul_backward():
    a, b = Value(2.0), Value(3.0)
    (a * b).backward()
    assert a.grad == 3.0 and b.grad == 2.0


def test_chain():
    a, b = Value(2.0), Value(-3.0)
    c = a * b + b.tanh()
    c.backward()
    assert abs(a.grad - (-3.0)) < 1e-9


def test_tanh_grad():
    x = Value(0.0)
    x.tanh().backward()
    assert x.grad == 1.0
