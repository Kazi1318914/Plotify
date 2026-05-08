"""Tests for StackedBarPlot across both backends."""

import os

import pytest

from plotify.num_cat import StackedBarPlot


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_stacked_bar(grouped_df, tmp_path, backend, ext):
    plot = StackedBarPlot(
        grouped_df, x="region", y="sales", hue="product", backend=backend
    )
    out = plot.save_plot(f"stacked_bar.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_stacked_bar_normalised(grouped_df, tmp_path, backend, ext):
    plot = StackedBarPlot(
        grouped_df, x="region", y="sales", hue="product", normalize=True, backend=backend
    )
    out = plot.save_plot(f"stacked_bar_norm.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
