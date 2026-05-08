"""Tests for ParallelCoordinates across both backends."""

import os

import pytest

from plotify.categorical import ParallelCoordinates


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_parallel_coords(numeric_only_df, tmp_path, backend, ext):
    plot = ParallelCoordinates(numeric_only_df, class_column="class", backend=backend)
    out = plot.save_plot(f"parallel.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
