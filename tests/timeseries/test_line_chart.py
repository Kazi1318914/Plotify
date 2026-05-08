"""Tests for LineChart across both backends."""

import os

import pytest

from plotify.timeseries import LineChart


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_line_chart(timeseries_df, tmp_path, backend, ext):
    plot = LineChart(timeseries_df, x="date", y="value", hue="group", backend=backend)
    out = plot.save_plot(f"line.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
