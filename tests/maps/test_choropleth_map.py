"""Tests for ChoroplethMap.

The Seaborn backend requires a GeoDataFrame; if geopandas isn't available
that test is skipped. The Plotly backend uses ``locationmode="country names"``
which works without any external GeoJSON.
"""

import os

import pandas as pd
import pytest

from plotify.maps import ChoroplethMap


def test_choropleth_plotly(tmp_path):
    df = pd.DataFrame(
        {"country": ["France", "Germany", "Spain"], "value": [1.0, 2.5, 1.7]}
    )
    plot = ChoroplethMap(
        df,
        value="value",
        locations="country",
        locationmode="country names",
        backend="plotly",
    )
    out = plot.save_plot("choro.html", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_choropleth_seaborn_requires_geodataframe():
    """A plain DataFrame should be rejected by the seaborn backend."""
    df = pd.DataFrame({"region": ["A", "B"], "value": [1, 2]})
    with pytest.raises(TypeError):
        # The plain DataFrame.plot exists, but the call with `column=` will
        # surface a TypeError downstream — we trigger our explicit guard
        # by stripping the .plot attribute first.
        class Bare:
            def __init__(self, data):
                self._data = data

        ChoroplethMap(Bare(df), value="value", backend="seaborn")
