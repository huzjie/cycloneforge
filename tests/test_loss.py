# -*- coding: utf-8 -*-
"""损失测试。"""
from cycloneforge.nn.autodiff import Value
from cycloneforge.model.loss import mse, total_loss


def test_mse_zero():
    loss = mse([Value(1.0), Value(2.0)], [1.0, 2.0])
    assert loss.data == 0.0


def test_mse_positive():
    loss = mse([Value(1.0)], [2.0])
    assert loss.data == 1.0
