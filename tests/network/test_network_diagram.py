"""Tests for NetworkDiagram across both backends."""

import os

import pytest

from plotify.network import NetworkDiagram

EDGES = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("D", "A")]


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_network_diagram(tmp_path, backend, ext):
    plot = NetworkDiagram(edges=EDGES, layout="circular", backend=backend)
    out = plot.save_plot(f"net.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_network_rejects_both_inputs():
    with pytest.raises(ValueError):
        NetworkDiagram()


def test_network_bad_layout():
    with pytest.raises(ValueError):
        NetworkDiagram(edges=EDGES, layout="galactic")
