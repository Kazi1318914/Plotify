"""Tests for the plotify.theme system."""

import matplotlib as mpl
import plotly.io as pio
import pytest

from plotify import theme


@pytest.fixture(autouse=True)
def _reset_theme_after_test():
    """Restore the publication theme after each test so we don't leak state."""
    yield
    theme.set("publication")


def test_default_theme_is_publication():
    assert theme.get_current().name == "publication"


def test_set_by_name():
    t = theme.set("none")
    assert t.name == "none"
    assert theme.get_current().name == "none"


def test_set_unknown_name_raises():
    with pytest.raises(ValueError):
        theme.set("does-not-exist")


def test_set_with_theme_instance():
    custom = theme.Theme(name="rose", palette=("#FF1493",))
    theme.register(custom)
    theme.set("rose")
    assert theme.get_current() is custom


def test_apply_seaborn_updates_rcparams():
    theme.set("publication")
    theme.apply_current("seaborn")
    # Spines collapse to left/bottom; the publication theme drops top/right.
    assert mpl.rcParams["axes.spines.top"] is False
    assert mpl.rcParams["axes.spines.right"] is False
    # Palette first colour matches the Okabe-Ito blue.
    cycle_colors = mpl.rcParams["axes.prop_cycle"].by_key()["color"]
    assert cycle_colors[0].lower() == "#0072b2"


def test_apply_plotly_registers_template():
    theme.set("publication")
    theme.apply_current("plotly")
    assert "plotify" in pio.templates
    assert pio.templates.default == "plotify"


def test_none_theme_is_noop():
    theme.set("publication")
    theme.apply_current("seaborn")
    rc_before = dict(mpl.rcParams)
    theme.set("none")
    theme.apply_current("seaborn")
    # The "none" theme intentionally leaves rcParams alone.
    assert mpl.rcParams["axes.spines.top"] == rc_before["axes.spines.top"]


def test_smart_formatter_examples():
    fmt = theme.smart_formatter()
    assert fmt(0, 0) == "0"
    assert fmt(500, 0) == "500"
    assert fmt(1500, 0) == "1.5K"
    assert fmt(2_500_000, 0) == "2.5M"
    assert fmt(3_400_000_000, 0) == "3.4B"
