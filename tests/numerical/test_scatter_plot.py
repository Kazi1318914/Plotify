"""Tests for ScatterPlot across both backends."""

import os

import pytest

from plotify.numerical import ScatterPlot


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_scatter_basic(sample_df, tmp_path, backend, ext):
    plot = ScatterPlot(sample_df, x="val", y="val2", backend=backend)
    out = plot.save_plot(f"scatter.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_scatter_with_regression(sample_df, tmp_path, backend, ext):
    plot = ScatterPlot(sample_df, x="val", y="val2", style="reg", backend=backend)
    out = plot.save_plot(f"scatter_reg.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
