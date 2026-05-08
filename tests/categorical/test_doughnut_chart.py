"""Tests for DoughnutChart across both backends."""

import os

import pytest

from plotify.categorical import DoughnutChart


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_doughnut(category_value_df, tmp_path, backend, ext):
    plot = DoughnutChart(category_value_df, names="cat", values="val", backend=backend)
    out = plot.save_plot(f"doughnut.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_doughnut_rejects_bad_hole(category_value_df):
    with pytest.raises(ValueError):
        DoughnutChart(category_value_df, names="cat", values="val", hole=1.5)
