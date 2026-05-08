"""Tests for Cartogram. Seaborn-only."""

import os

import pytest

from plotify.maps import Cartogram


def test_cartogram(geo_points_df, tmp_path):
    plot = Cartogram(
        geo_points_df, label="city", lon="lon", lat="lat", value="pop", max_radius=2
    )
    out = plot.save_plot("cart.png", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_cartogram_plotly_unsupported(geo_points_df):
    with pytest.raises(ValueError):
        Cartogram(
            geo_points_df,
            label="city",
            lon="lon",
            lat="lat",
            value="pop",
            backend="plotly",
        )
