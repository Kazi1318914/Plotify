"""Tests for RadarChart across both backends."""

import os

import pandas as pd
import pytest

from plotify.categorical import RadarChart


@pytest.fixture
def radar_df():
    return pd.DataFrame(
        {
            "person": ["Alice", "Bob"],
            "strength": [7, 5],
            "speed": [6, 8],
            "stamina": [5, 7],
            "agility": [8, 6],
        }
    )


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_radar_chart(radar_df, tmp_path, backend, ext):
    plot = RadarChart(
        radar_df,
        categories=["strength", "speed", "stamina", "agility"],
        group_col="person",
        backend=backend,
    )
    out = plot.save_plot(f"radar.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_spider_chart_alias_is_radar_chart():
    """SpiderChart is exported as an alias for RadarChart."""
    from plotify.categorical import RadarChart as _Radar
    from plotify.categorical import SpiderChart

    assert SpiderChart is _Radar
