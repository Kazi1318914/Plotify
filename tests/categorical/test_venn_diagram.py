"""Tests for VennDiagram. Seaborn-only."""

import os

import pytest

from plotify.categorical import VennDiagram


def test_venn2(tmp_path):
    plot = VennDiagram(sets=[{1, 2, 3}, {2, 3, 4}])
    out = plot.save_plot("venn2.png", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_venn3(tmp_path):
    plot = VennDiagram(sets=[{1, 2}, {2, 3}, {3, 4}])
    out = plot.save_plot("venn3.png", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_venn_plotly_unsupported():
    with pytest.raises(ValueError):
        VennDiagram(sets=[{1}, {2}], backend="plotly")


def test_venn_rejects_wrong_number_of_sets():
    with pytest.raises(ValueError):
        VennDiagram(sets=[{1}])
