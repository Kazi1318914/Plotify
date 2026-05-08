"""Tests for GroupedBarPlot across both backends."""

import os

import pytest

from plotify.num_cat import GroupedBarPlot


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_grouped_bar(grouped_df, tmp_path, backend, ext):
    plot = GroupedBarPlot(
        grouped_df, x="region", y="sales", hue="product", backend=backend
    )
    out = plot.save_plot(f"grouped_bar.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
