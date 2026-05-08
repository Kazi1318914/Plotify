"""Tests for BarPlot across both backends."""

import os

import pytest

from plotify.categorical import BarPlot


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_bar_plot(category_value_df, tmp_path, backend, ext):
    plot = BarPlot(category_value_df, x="cat", y="val", backend=backend)
    out = plot.save_plot(f"bar.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
