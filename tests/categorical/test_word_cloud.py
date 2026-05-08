"""Tests for WordCloudPlot. Only Seaborn backend is supported."""

import os

import pytest

from plotify.categorical import WordCloudPlot


def test_word_cloud_seaborn(tmp_path):
    plot = WordCloudPlot(
        text="plotify is a python plotting package for python developers plotify",
    )
    out = plot.save_plot("wc.png", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_word_cloud_plotly_unsupported():
    with pytest.raises(ValueError):
        WordCloudPlot(text="x y z", backend="plotly")


def test_word_cloud_requires_exactly_one_input():
    with pytest.raises(ValueError):
        WordCloudPlot()
    with pytest.raises(ValueError):
        WordCloudPlot(text="a", frequencies={"a": 1})
