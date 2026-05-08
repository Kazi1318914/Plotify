"""Tests for StackedAreaChart across both backends and both input shapes."""

import os

import pytest

from plotify.timeseries import StackedAreaChart


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_stacked_area_long(timeseries_df, tmp_path, backend, ext):
    plot = StackedAreaChart(
        timeseries_df, x="date", y="value", hue="group", backend=backend
    )
    out = plot.save_plot(f"sa_long.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_stacked_area_wide(timeseries_wide_df, tmp_path, backend, ext):
    plot = StackedAreaChart(
        timeseries_wide_df, x="date", y=["A", "B", "C"], backend=backend
    )
    out = plot.save_plot(f"sa_wide.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_stacked_area_rejects_single_y_without_hue(timeseries_df):
    with pytest.raises(ValueError):
        StackedAreaChart(timeseries_df, x="date", y="value")
