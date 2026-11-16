# 可视化

```python
from cycloneforge.viz.track_plot import plot_track_svg
svg = plot_track_svg(track)
Path('track.svg').write_text(svg)
```

零依赖 SVG 输出，可直接嵌入网页或报告。
