"""Tests for Boxplot across both backends."""

import os

import pytest

from plotify.numerical import Boxplot


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_boxplot_renders_and_saves(sample_df, tmp_path, backend, ext):
    """Boxplot should instantiate and produce a non-empty saved file."""
    plot = Boxplot(sample_df, x="cat", y="val", backend=backend)
    out = plot.save_plot(f"box.{ext}", folder=str(tmp_path))
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0
