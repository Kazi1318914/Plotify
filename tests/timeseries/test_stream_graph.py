"""Tests for StreamGraph. Seaborn-only."""

import os

import pytest

from plotify.timeseries import StreamGraph


def test_stream_graph(timeseries_df, tmp_path):
    plot = StreamGraph(timeseries_df, x="date", y="value", hue="group")
    out = plot.save_plot("stream.png", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_stream_graph_plotly_unsupported(timeseries_df):
    with pytest.raises(ValueError):
        StreamGraph(timeseries_df, x="date", y="value", hue="group", backend="plotly")
