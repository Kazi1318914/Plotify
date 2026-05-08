"""Tests for ConnectedScatterPlot across both backends."""

import os

import pytest

from plotify.numerical import ConnectedScatterPlot


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_connected_scatter(sample_df, tmp_path, backend, ext):
    plot = ConnectedScatterPlot(sample_df, x="val", y="val2", backend=backend)
    out = plot.save_plot(f"conn_scatter.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
