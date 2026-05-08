"""Tests for Treemap across both backends."""

import os

import pytest

from plotify.categorical import Treemap


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_treemap(category_value_df, tmp_path, backend, ext):
    plot = Treemap(category_value_df, labels="cat", values="val", backend=backend)
    out = plot.save_plot(f"treemap.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
