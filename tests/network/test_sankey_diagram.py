"""Tests for SankeyDiagram across both backends."""

import os

import pytest

from plotify.network import SankeyDiagram

SOURCE = [0, 1, 0, 2, 3, 3]
TARGET = [2, 3, 3, 4, 4, 5]
VALUE = [8, 4, 2, 8, 4, 2]
LABELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_sankey(tmp_path, backend, ext):
    plot = SankeyDiagram(
        source=SOURCE, target=TARGET, value=VALUE, labels=LABELS, backend=backend
    )
    out = plot.save_plot(f"sankey.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_sankey_rejects_unequal_lengths():
    with pytest.raises(ValueError):
        SankeyDiagram(source=[0, 1], target=[1], value=[1], labels=["x", "y"])
