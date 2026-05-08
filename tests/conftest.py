"""Shared pytest fixtures for the Plotify test suite."""

import matplotlib
import numpy as np
import pandas as pd
import pytest

# Use a non-interactive backend so tests run headless on Windows/Linux CI.
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  (must come after backend selection)


@pytest.fixture(autouse=True)
def _close_figures_between_tests():
    """Close every matplotlib figure between tests.

    Plotify creates a fresh figure inside ``BasePlot._render`` for the
    Seaborn backend (so plots do not inherit stale axis state). Without an
    explicit teardown those figures accumulate and trigger matplotlib's
    "More than 20 figures opened" warning during the suite.
    """
    yield
    plt.close("all")


@pytest.fixture
def sample_df():
    """A small mixed numeric + categorical dataframe."""
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {
            "cat": ["A", "A", "B", "B", "C", "C", "A", "B", "C", "A"],
            "val": rng.normal(0, 1, size=10),
            "val2": rng.normal(5, 2, size=10),
            "size": rng.integers(1, 10, size=10),
        }
    )


@pytest.fixture
def numeric_only_df():
    """A purely numeric dataframe suitable for parallel coordinates / dendrogram."""
    rng = np.random.default_rng(7)
    df = pd.DataFrame(rng.normal(size=(8, 4)), columns=list("wxyz"))
    df["class"] = np.repeat([0, 1], 4)
    return df


@pytest.fixture
def category_value_df():
    """A simple (category, value) dataframe used by bar/pie/doughnut/lollipop/treemap."""
    return pd.DataFrame({"cat": ["A", "B", "C", "D"], "val": [10, 20, 15, 8]})


@pytest.fixture
def geo_points_df():
    """A handful of geo-located points with associated values."""
    return pd.DataFrame(
        {
            "city": ["Paris", "London", "Berlin", "Rome", "Madrid"],
            "lat": [48.8566, 51.5074, 52.5200, 41.9028, 40.4168],
            "lon": [2.3522, -0.1278, 13.4050, 12.4964, -3.7038],
            "pop": [2.1, 8.9, 3.7, 2.8, 3.3],
        }
    )


@pytest.fixture
def grouped_df():
    """A primary × secondary category dataframe for grouped/stacked plots."""
    rng = np.random.default_rng(3)
    rows = []
    for region in ["North", "South", "East"]:
        for product in ["Widgets", "Gadgets"]:
            rows.append(
                {"region": region, "product": product, "sales": int(rng.integers(10, 100))}
            )
    return pd.DataFrame(rows)


@pytest.fixture
def timeseries_df():
    """A small time-series dataframe with three groups."""
    rng = np.random.default_rng(11)
    dates = pd.date_range("2024-01-01", periods=12, freq="MS")
    rows = []
    for group in ["A", "B", "C"]:
        values = rng.integers(10, 50, size=len(dates))
        for d, v in zip(dates, values):
            rows.append({"date": d, "group": group, "value": int(v)})
    return pd.DataFrame(rows)


@pytest.fixture
def timeseries_wide_df(timeseries_df):
    """Same series in wide form — one column per group."""
    return timeseries_df.pivot(index="date", columns="group", values="value").reset_index()


@pytest.fixture
def hierarchy_df():
    """Hierarchical data for sunburst / nested treemaps."""
    return pd.DataFrame(
        {
            "level1": ["X", "X", "Y", "Y"],
            "level2": ["a", "b", "c", "d"],
            "val": [3, 5, 4, 6],
        }
    )
