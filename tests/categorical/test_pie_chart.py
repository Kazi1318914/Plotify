"""Tests for PieChart across both backends."""

import os

import pytest

from plotify.categorical import PieChart


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_pie(category_value_df, tmp_path, backend, ext):
    plot = PieChart(category_value_df, names="cat", values="val", backend=backend)
    out = plot.save_plot(f"pie.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
