"""Tests for plotify._inference column-kind detection."""

import numpy as np
import pandas as pd
import pytest

from plotify._inference import ColKind, infer_kind, summarise


def test_numeric_kind():
    s = pd.Series([1.0, 2.0, 3.0])
    assert infer_kind(s) == ColKind.NUMERIC


def test_datetime_kind():
    s = pd.to_datetime(pd.Series(["2024-01-01", "2024-01-02"]))
    assert infer_kind(s) == ColKind.DATETIME


def test_boolean_kind():
    s = pd.Series([True, False, True])
    assert infer_kind(s) == ColKind.BOOLEAN


@pytest.mark.parametrize(
    "values, expected",
    [
        (list("AABBCC"), ColKind.CATEGORICAL_LOW),
        ([f"x{i}" for i in range(15)], ColKind.CATEGORICAL_MID),
        ([f"x{i}" for i in range(60)], ColKind.CATEGORICAL_HIGH),
    ],
)
def test_categorical_buckets(values, expected):
    assert infer_kind(pd.Series(values)) == expected


def test_text_detected_for_long_strings():
    # Need >MID_THRESHOLD unique long strings — duplicates get bucketed as
    # CATEGORICAL_LOW because cardinality is checked before string length.
    long = [f"a long sentence number {i} with plenty of padding text" for i in range(60)]
    assert infer_kind(pd.Series(long)) == ColKind.TEXT


def test_summarise_fields():
    s = pd.Series([1, 2, np.nan, 2])
    summary = summarise(s, name="x")
    assert summary.name == "x"
    assert summary.kind == ColKind.NUMERIC
    assert summary.n_total == 4
    assert summary.n_missing == 1
    assert summary.n_unique == 2
    assert summary.is_numeric_like
    assert not summary.is_categorical
