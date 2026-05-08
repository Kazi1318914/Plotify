"""Tests for HexbinMap across both backends."""

import os

import numpy as np
import pandas as pd
import pytest

from plotify.maps import HexbinMap


@pytest.fixture
def random_geo_df():
    """A larger random sample of geo points so hexbin produces visible bins."""
    rng = np.random.default_rng(0)
    return pd.DataFrame(
        {
            "lat": rng.uniform(40, 55, size=200),
            "lon": rng.uniform(-5, 15, size=200),
        }
    )


def test_hexbin_seaborn(random_geo_df, tmp_path):
    plot = HexbinMap(random_geo_df, lat="lat", lon="lon", backend="seaborn")
    out = plot.save_plot("hex.png", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_hexbin_plotly(random_geo_df, tmp_path):
    plot = HexbinMap(random_geo_df, lat="lat", lon="lon", backend="plotly")
    out = plot.save_plot("hex.html", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
