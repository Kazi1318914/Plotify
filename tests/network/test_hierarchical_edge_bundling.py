"""Tests for HierarchicalEdgeBundling. Seaborn-only."""

import os

import pytest

from plotify.network import HierarchicalEdgeBundling

LEAVES = list("ABCDEFGH")
CONNECTIONS = [("A", "E"), ("B", "F"), ("C", "G"), ("D", "H"), ("A", "D")]


def test_heb(tmp_path):
    plot = HierarchicalEdgeBundling(leaves=LEAVES, connections=CONNECTIONS)
    out = plot.save_plot("heb.png", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_heb_plotly_unsupported():
    with pytest.raises(ValueError):
        HierarchicalEdgeBundling(leaves=LEAVES, connections=CONNECTIONS, backend="plotly")


def test_heb_bad_bundle_strength():
    with pytest.raises(ValueError):
        HierarchicalEdgeBundling(leaves=LEAVES, connections=CONNECTIONS, bundle_strength=2)
