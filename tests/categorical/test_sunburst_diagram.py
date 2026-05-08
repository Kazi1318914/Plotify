"""Tests for SunburstDiagram across both backends."""

import os

import pytest

from plotify.categorical import SunburstDiagram


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_sunburst(hierarchy_df, tmp_path, backend, ext):
    plot = SunburstDiagram(
        hierarchy_df,
        path=["level1", "level2"],
        values="val",
        backend=backend,
    )
    out = plot.save_plot(f"sun.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_sunburst_requires_path(hierarchy_df):
    with pytest.raises(ValueError):
        SunburstDiagram(hierarchy_df, path=[], values="val")
