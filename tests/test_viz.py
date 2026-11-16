# -*- coding: utf-8 -*-
"""可视化测试。"""
from cycloneforge.viz.track_plot import plot_track_svg
from cycloneforge.viz.ensemble_plot import plot_ensemble_svg


def test_track_svg():
    svg = plot_track_svg([[0, 0], [1, 1], [2, 2]])
    assert svg.startswith("<svg")


def test_ensemble_svg():
    tracks = [[[0, 0], [1, 1]], [[0.5, 0.5], [1.5, 1.5]]]
    svg = plot_ensemble_svg(tracks)
    assert svg.startswith("<svg")
