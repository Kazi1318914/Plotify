"""Tests for ChordDiagram. Seaborn-only."""

import os

import pytest

from plotify.network import ChordDiagram

MATRIX = [
    [0, 5, 3, 2],
    [5, 0, 4, 1],
    [3, 4, 0, 6],
    [2, 1, 6, 0],
]


def test_chord_diagram(tmp_path):
    plot = ChordDiagram(matrix=MATRIX, labels=["A", "B", "C", "D"])
    out = plot.save_plot("chord.png", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_chord_plotly_unsupported():
    with pytest.raises(ValueError):
        ChordDiagram(matrix=MATRIX, backend="plotly")


def test_chord_rejects_non_square():
    with pytest.raises(ValueError):
        ChordDiagram(matrix=[[1, 2, 3], [4, 5, 6]])
