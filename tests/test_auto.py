"""Tests for plotify.auto.suggest() / auto()."""

import os

import pandas as pd
import pytest

from plotify.auto import auto, suggest
from plotify.categorical import BarPlot
from plotify.num_cat import GroupedBarPlot, GroupedScatter
from plotify.numerical import Boxplot, DensityPlot, ScatterPlot, Violinplot
from plotify.timeseries import LineChart


def test_suggest_returns_ranked_list():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    suggestions = suggest(df, x="a", y="b")
    assert len(suggestions) >= 1
    # Scores are non-increasing.
    scores = [s.score for s in suggestions]
    assert scores == sorted(scores, reverse=True)


def test_suggest_two_numeric_picks_scatter():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    top = suggest(df, x="a", y="b")[0]
    assert top.chart_class is ScatterPlot


def test_suggest_two_numeric_with_color_picks_grouped_scatter():
    df = pd.DataFrame(
        {"a": [1, 2, 3, 4], "b": [5, 6, 7, 8], "c": ["x", "y", "x", "y"]}
    )
    top = suggest(df, x="a", y="b", color="c")[0]
    assert top.chart_class is GroupedScatter


def test_suggest_datetime_numeric_picks_line():
    df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=10, freq="D"),
            "val": range(10),
        }
    )
    top = suggest(df, x="date", y="val")[0]
    assert top.chart_class is LineChart


def test_suggest_categorical_numeric_picks_bar():
    df = pd.DataFrame({"cat": list("AABBCC"), "val": [1, 2, 3, 4, 5, 6]})
    top = suggest(df, x="cat", y="val")[0]
    assert top.chart_class is BarPlot


def test_suggest_two_categoricals_picks_grouped_bar():
    df = pd.DataFrame(
        {
            "region": ["N", "N", "S", "S"],
            "product": ["W", "G", "W", "G"],
            "sales": [10, 20, 30, 40],
        }
    )
    top = suggest(df, x="region", y="sales", color="product")[0]
    assert top.chart_class is GroupedBarPlot


def test_suggest_single_numeric_picks_density():
    df = pd.DataFrame({"v": [1.0, 2.0, 3.0, 4.0, 5.0]})
    top = suggest(df, x="v")[0]
    assert top.chart_class is DensityPlot


def test_suggest_distribution_intent_picks_violin():
    df = pd.DataFrame({"cat": list("AABB"), "val": [1, 2, 3, 4]})
    top = suggest(df, x="cat", y="val", intent="distribution")[0]
    assert top.chart_class is Violinplot


def test_suggest_includes_a_reason():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    top = suggest(df, x="a", y="b")[0]
    assert isinstance(top.reason, str) and len(top.reason) > 0


def test_auto_renders_and_saves(tmp_path):
    df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=8, freq="D"),
            "val": [1, 3, 2, 5, 4, 6, 7, 8],
        }
    )
    plot = auto(df, x="date", y="val", backend="plotly")
    out = plot.save_plot("auto.html", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_auto_with_unknown_columns_raises():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    with pytest.raises(KeyError):
        auto(df, x="missing", y="b")


def test_auto_extra_kwargs_override_suggestion():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    plot = auto(df, x="a", y="b", title="my plot")
    assert plot._title == "my plot"


def test_suggest_distribution_with_only_numeric():
    df = pd.DataFrame({"v": [1.0, 2.0, 3.0]})
    top = suggest(df, x="v", intent="distribution")[0]
    assert top.chart_class is DensityPlot


def test_suggest_returns_empty_for_unhandled_combo():
    # Single high-cardinality categorical (>MID_THRESHOLD unique) hits no
    # rule and returns an empty list.
    df = pd.DataFrame({"a": [f"id_{i}" for i in range(100)]})
    suggestions = suggest(df, x="a")
    assert suggestions == []
