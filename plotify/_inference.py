"""
plotify._inference
==================

Column-kind inference used by :mod:`plotify.auto`. Given a pandas Series we
classify it into one of a small set of "kinds" (numeric, datetime, low- /
mid- / high-cardinality categorical, text, boolean) so the suggestion
engine can make decisions without hard-coding pandas dtype strings.
"""

from dataclasses import dataclass
from enum import Enum

import numpy as np
import pandas as pd


class ColKind(str, Enum):
    """Categorical bucket assigned to each column."""

    NUMERIC = "numeric"
    DATETIME = "datetime"
    BOOLEAN = "boolean"
    CATEGORICAL_LOW = "categorical_low"   # <= LOW_THRESHOLD unique values
    CATEGORICAL_MID = "categorical_mid"   # LOW < n_unique <= MID
    CATEGORICAL_HIGH = "categorical_high"  # > MID unique values
    TEXT = "text"
    UNKNOWN = "unknown"


# Thresholds used to bucket categorical columns. Tuned for "looks readable
# on a chart" rather than statistical correctness:
#   - <= 10  : fits in a legend / x-axis without truncation
#   - <= 50  : usable but crowded; wide+long shapes start to matter
LOW_THRESHOLD = 10
MID_THRESHOLD = 50


@dataclass
class ColumnSummary:
    """Compact description of a single column.

    Used by the suggestion engine — fields cover what the rule set actually
    consults, not full descriptive statistics.
    """

    name: str
    kind: ColKind
    n_unique: int
    n_total: int
    n_missing: int

    @property
    def is_categorical(self) -> bool:
        return self.kind in (
            ColKind.CATEGORICAL_LOW,
            ColKind.CATEGORICAL_MID,
            ColKind.CATEGORICAL_HIGH,
            ColKind.BOOLEAN,
        )

    @property
    def is_numeric_like(self) -> bool:
        return self.kind == ColKind.NUMERIC


def infer_kind(series: pd.Series) -> ColKind:
    """Classify a pandas Series into a :class:`ColKind`.

    The order of checks matters: datetime must be tested before numeric
    (pandas datetimes are technically int64 under the hood) and boolean
    must be tested before numeric (booleans pass numeric checks).
    """
    if pd.api.types.is_datetime64_any_dtype(series):
        return ColKind.DATETIME
    if pd.api.types.is_bool_dtype(series):
        return ColKind.BOOLEAN
    if pd.api.types.is_numeric_dtype(series):
        return ColKind.NUMERIC

    # Anything left is object / string / category dtype. Bucket by cardinality.
    n_unique = int(series.nunique(dropna=True))
    if n_unique <= LOW_THRESHOLD:
        return ColKind.CATEGORICAL_LOW
    if n_unique <= MID_THRESHOLD:
        return ColKind.CATEGORICAL_MID

    # Rough heuristic: if the average string length is high, treat as free
    # text rather than a categorical. Used so e.g. tweet bodies don't get
    # plotted as a 10k-bar chart.
    #
    # ``is_string_dtype`` (rather than ``series.dtype == object``) is needed
    # because newer pandas versions store string-only columns under
    # ``StringDtype`` instead of ``object`` by default — checking ``object``
    # alone misses them.
    if pd.api.types.is_string_dtype(series):
        try:
            avg_len = series.dropna().astype(str).str.len().mean()
            if avg_len and avg_len > 30:
                return ColKind.TEXT
        except Exception:
            pass
    return ColKind.CATEGORICAL_HIGH


def summarise(series: pd.Series, name: str | None = None) -> ColumnSummary:
    """Return a :class:`ColumnSummary` for ``series``."""
    return ColumnSummary(
        name=name or (series.name if series.name is not None else ""),
        kind=infer_kind(series),
        n_unique=int(series.nunique(dropna=True)),
        n_total=int(len(series)),
        n_missing=int(series.isna().sum()),
    )


def summarise_columns(
    df: pd.DataFrame, columns: list[str | None]
) -> dict[str, ColumnSummary]:
    """Summarise the given columns (skipping any ``None`` entries)."""
    out: dict[str, ColumnSummary] = {}
    for col in columns:
        if col is None:
            continue
        if col not in df.columns:
            raise KeyError(f"Column {col!r} not found in dataframe.")
        out[col] = summarise(df[col], name=col)
    return out


# Used by tests and downstream callers that want a stable list of kinds.
__all__ = [
    "ColKind",
    "ColumnSummary",
    "LOW_THRESHOLD",
    "MID_THRESHOLD",
    "infer_kind",
    "summarise",
    "summarise_columns",
]


# Reference numpy to avoid linter warnings — pandas uses it internally.
_ = np.asarray([])
