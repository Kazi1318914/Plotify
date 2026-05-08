"""Tests for Dendrogram across both backends."""

import os

import pytest

from plotify.categorical import Dendrogram


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_dendrogram(numeric_only_df, tmp_path, backend, ext):
    matrix = numeric_only_df[["w", "x", "y", "z"]]
    plot = Dendrogram(
        matrix, labels=[f"row{i}" for i in range(len(matrix))], backend=backend
    )
    out = plot.save_plot(f"dendro.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
