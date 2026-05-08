"""Tests for ArcDiagram. Seaborn-only."""

import os

import pytest

from plotify.network import ArcDiagram

EDGES = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]


def test_arc_diagram(tmp_path):
    plot = ArcDiagram(edges=EDGES, node_order=["A", "B", "C", "D", "E"])
    out = plot.save_plot("arc.png", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_arc_plotly_unsupported():
    with pytest.raises(ValueError):
        ArcDiagram(edges=EDGES, backend="plotly")
