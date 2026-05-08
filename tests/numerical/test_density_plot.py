"""Tests for DensityPlot across both backends."""

import os

import pytest

from plotify.numerical import DensityPlot


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_density_univariate(sample_df, tmp_path, backend, ext):
    plot = DensityPlot(sample_df, x="val", backend=backend)
    out = plot.save_plot(f"density.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_density_bivariate(sample_df, tmp_path, backend, ext):
    plot = DensityPlot(sample_df, x="val", y="val2", backend=backend)
    out = plot.save_plot(f"density2d.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0
