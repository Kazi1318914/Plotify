"""Tests for AreaChart across both backends."""

import os

import pytest

from plotify.timeseries import AreaChart


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_area_chart(timeseries_df, tmp_path, backend, ext):
    single_group = timeseries_df[timeseries_df["group"] == "A"]
    plot = AreaChart(single_group, x="date", y="value", backend=backend)
    out = plot.save_plot(f"area.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
