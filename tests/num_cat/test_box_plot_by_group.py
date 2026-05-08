"""Tests for BoxPlotByGroup across both backends."""

import os

import pytest

from plotify.num_cat import BoxPlotByGroup


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_box_by_group(grouped_df, tmp_path, backend, ext):
    plot = BoxPlotByGroup(
        grouped_df, x="region", y="sales", hue="product", backend=backend
    )
    out = plot.save_plot(f"box_by.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
