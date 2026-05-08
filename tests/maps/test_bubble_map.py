"""Tests for BubbleMap across both backends."""

import os

import pytest

from plotify.maps import BubbleMap


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_bubble_map(geo_points_df, tmp_path, backend, ext):
    plot = BubbleMap(
        geo_points_df, lat="lat", lon="lon", size="pop", backend=backend
    )
    out = plot.save_plot(f"bubble.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
