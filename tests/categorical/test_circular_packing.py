"""Tests for CircularPacking. Seaborn-only class."""

import os

import pytest

from plotify.categorical import CircularPacking


def test_circular_packing(category_value_df, tmp_path):
    plot = CircularPacking(category_value_df, labels="cat", values="val")
    out = plot.save_plot("circ.png", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_circular_packing_plotly_unsupported(category_value_df):
    with pytest.raises(ValueError):
        CircularPacking(
            category_value_df, labels="cat", values="val", backend="plotly"
        )
