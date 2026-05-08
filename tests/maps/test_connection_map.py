"""Tests for ConnectionMap across both backends."""

import os

import pytest

from plotify.maps import ConnectionMap

STARTS = [(2.35, 48.86), (-0.13, 51.51), (13.40, 52.52)]
ENDS = [(-3.70, 40.42), (12.50, 41.90), (2.35, 48.86)]


@pytest.mark.parametrize("backend,ext", [("seaborn", "png"), ("plotly", "html")])
def test_connection_map(tmp_path, backend, ext):
    plot = ConnectionMap(starts=STARTS, ends=ENDS, backend=backend)
    out = plot.save_plot(f"conn.{ext}", folder=str(tmp_path))
    assert os.path.exists(out) and os.path.getsize(out) > 0


def test_connection_rejects_unequal_lengths():
    with pytest.raises(ValueError):
        ConnectionMap(starts=[(0, 0)], ends=[(1, 1), (2, 2)])
