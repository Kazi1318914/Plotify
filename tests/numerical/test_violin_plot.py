"""Tests for Violinplot across both backends."""

import os

import pytest

from plotify.numerical import Violinplot


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_violin_renders_and_saves(sample_df, tmp_path, backend, ext):
    plot = Violinplot(sample_df, x="cat", y="val", backend=backend)
    out = plot.save_plot(f"violin.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
