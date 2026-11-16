# -*- coding: utf-8 -*-
"""doctor 自检测试。"""
from cycloneforge.cli.commands import cmd_doctor


def test_doctor_passes():
    assert cmd_doctor() == 0
