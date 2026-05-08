"""Tests for GroupedScatter across both backends."""

import os

import pytest

from plotify.num_cat import GroupedScatter


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_grouped_scatter(sample_df, tmp_path, backend, ext):
    plot = GroupedScatter(sample_df, x="val", y="val2", hue="cat", backend=backend)
    out = plot.save_plot(f"gs.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
