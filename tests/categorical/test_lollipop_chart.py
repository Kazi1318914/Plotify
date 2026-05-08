"""Tests for LollipopChart across both backends."""

import os

import pytest

from plotify.categorical import LollipopChart


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_lollipop(category_value_df, tmp_path, backend, ext):
    plot = LollipopChart(category_value_df, x="cat", y="val", backend=backend)
    out = plot.save_plot(f"loll.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
