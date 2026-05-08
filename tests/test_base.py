"""Tests for the BasePlot class."""

import pytest

from plotify.base import BasePlot


def test_invalid_backend_raises():
    """BasePlot should reject unknown backend strings in __init__."""
    with pytest.raises(ValueError):
        BasePlot(backend="ggplot")


def test_unsupported_subclass_backend_raises():
    """A subclass that narrows SUPPORTED_BACKENDS should reject excluded ones."""

    class SeabornOnly(BasePlot):
        SUPPORTED_BACKENDS = ("seaborn",)

    with pytest.raises(ValueError):
        SeabornOnly(backend="plotly")


def test_default_backend_is_seaborn():
    """Default backend matches the original numerical.py behaviour."""
    bp = BasePlot()
    assert bp._backend == "seaborn"


def test_save_without_fig_raises_for_plotly():
    """save_plot on the Plotly backend should complain if _fig was never populated."""
    bp = BasePlot(backend="plotly")
    with pytest.raises(RuntimeError):
        bp._save_plotly("x.html", (10, 6))
