"""
plotify.auto
============

Smart chart picker. Given a dataframe and an ``(x, y, color)`` triple the
:func:`suggest` function returns a ranked list of chart suggestions based
on the inferred kinds (numeric / datetime / categorical / boolean) of the
chosen columns. :func:`auto` is a convenience wrapper that picks the top
suggestion and instantiates it.

The output of :func:`suggest` is a list of :class:`Suggestion` objects;
each carries the chart class, the kwargs to construct it with, a score in
``[0, 1]``, and a one-line reason explaining the rule that fired.
"""

from dataclasses import dataclass

import pandas as pd

from plotify._inference import ColKind, summarise_columns

# We import every chart class lazily inside _build_candidates so that
# importing ``plotify.auto`` doesn't drag in every dependency in the
# package — useful for users who only want the inference utilities.


@dataclass
class Suggestion:
    """A single chart suggestion produced by :func:`suggest`.

    Attributes
    ----------
    chart_class : type
        The Plotify chart class to instantiate.
    kwargs : dict
        Keyword arguments to pass to ``chart_class`` (besides ``df`` and
        ``backend``).
    score : float
        Confidence in this suggestion, ``0..1``. The decision rules assign
        rough scores; ranking is the consumer-facing contract.
    reason : str
        Human-readable one-line explanation of why this chart was picked.
    """

    chart_class: type
    kwargs: dict
    score: float
    reason: str


def suggest(
    df: pd.DataFrame,
    x: str | None = None,
    y: str | None = None,
    color: str | None = None,
    intent: str | None = None,
    top_k: int = 5,
) -> list[Suggestion]:
    """Return ranked chart suggestions for ``df`` and the chosen columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data.
    x, y, color : str, optional
        Column names. ``y`` is the value axis; ``color`` is the grouping
        column. Single-column inputs (just ``x``) are also handled.
    intent : str, optional
        High-level user intent — currently understood values are
        ``"distribution"`` (force violin/box family) and
        ``"comparison"`` (force bars).
    top_k : int, default=5
        Maximum number of suggestions to return.

    Returns
    -------
    list[Suggestion]
        Up to ``top_k`` suggestions, ordered by descending score. Empty
        list if no rule matched.
    """
    summaries = summarise_columns(df, [x, y, color])

    candidates = _build_candidates(
        x_summary=summaries.get(x) if x else None,
        y_summary=summaries.get(y) if y else None,
        color_summary=summaries.get(color) if color else None,
        intent=intent,
        x_name=x,
        y_name=y,
        color_name=color,
    )

    candidates.sort(key=lambda s: s.score, reverse=True)
    return candidates[:top_k]


def auto(
    df: pd.DataFrame,
    x: str | None = None,
    y: str | None = None,
    color: str | None = None,
    intent: str | None = None,
    backend: str = "seaborn",
    **plot_kwargs,
):
    """Pick the top-scoring chart for ``df`` and instantiate it.

    Equivalent to ``suggest(df, ...)[0].chart_class(df, **kwargs)`` with
    the suggestion's ``kwargs`` merged with ``plot_kwargs`` (the latter
    wins on conflict).

    Returns
    -------
    BasePlot
        The instantiated plot.

    Raises
    ------
    ValueError
        If no rule matched the supplied columns.
    """
    suggestions = suggest(df, x=x, y=y, color=color, intent=intent, top_k=1)
    if not suggestions:
        raise ValueError(
            "Could not infer an appropriate chart from the supplied columns."
        )
    top = suggestions[0]
    merged = {**top.kwargs, **plot_kwargs}
    return top.chart_class(df, backend=backend, **merged)


# ------------------------------------------------------------------ #
# Decision rules
# ------------------------------------------------------------------ #
def _build_candidates(
    x_summary,
    y_summary,
    color_summary,
    intent,
    x_name,
    y_name,
    color_name,
):
    """Apply the decision rules and return a list of :class:`Suggestion`.

    The rules are intentionally readable, not algorithmic — adding a new
    chart usually means adding a new ``if`` branch here.
    """
    # Lazy imports — see module docstring for reasoning.
    from plotify.categorical import BarPlot, LollipopChart, PieChart
    from plotify.num_cat import (
        BoxPlotByGroup,
        GroupedBarPlot,
        GroupedScatter,
        StackedBarPlot,
    )
    from plotify.numerical import Boxplot, DensityPlot, ScatterPlot, Violinplot
    from plotify.timeseries import AreaChart, LineChart, StackedAreaChart

    out: list[Suggestion] = []

    xk = x_summary.kind if x_summary else None
    yk = y_summary.kind if y_summary else None
    ck = color_summary.kind if color_summary else None
    has_color = color_summary is not None

    # Helpers for readability of the ladder below.
    is_low_cat = (xk == ColKind.CATEGORICAL_LOW or xk == ColKind.BOOLEAN)
    color_is_low_cat = ck in (ColKind.CATEGORICAL_LOW, ColKind.BOOLEAN)

    # ------ Intent overrides — applied first so they always rank highest.
    if intent == "distribution" and yk == ColKind.NUMERIC and is_low_cat:
        out.append(
            Suggestion(
                Violinplot,
                {"x": x_name, "y": y_name},
                0.97,
                "intent=distribution + categorical x + numeric y → violin plot",
            )
        )
        out.append(
            Suggestion(
                Boxplot,
                {"x": x_name, "y": y_name},
                0.92,
                "intent=distribution + categorical x + numeric y → box plot",
            )
        )
        return out

    if intent == "distribution" and xk == ColKind.NUMERIC and y_summary is None:
        out.append(
            Suggestion(
                DensityPlot, {"x": x_name}, 0.95, "intent=distribution + numeric → KDE"
            )
        )
        out.append(
            Suggestion(
                Violinplot, {"y": x_name}, 0.85, "intent=distribution + numeric → violin"
            )
        )
        return out

    # ------ Time-series patterns: datetime x + numeric y ---------------
    if xk == ColKind.DATETIME and yk == ColKind.NUMERIC:
        if has_color and color_is_low_cat:
            out.append(
                Suggestion(
                    LineChart,
                    {"x": x_name, "y": y_name, "hue": color_name},
                    0.96,
                    "datetime x + numeric y + low-cardinality group → multi-series line chart",
                )
            )
            out.append(
                Suggestion(
                    StackedAreaChart,
                    {"x": x_name, "y": y_name, "hue": color_name},
                    0.72,
                    "stacked area variant for compositional time series",
                )
            )
        else:
            out.append(
                Suggestion(
                    LineChart,
                    {"x": x_name, "y": y_name},
                    0.95,
                    "datetime x + numeric y → line chart",
                )
            )
            out.append(
                Suggestion(
                    AreaChart,
                    {"x": x_name, "y": y_name},
                    0.65,
                    "filled area variant for the same series",
                )
            )
        return out

    # ------ Two numeric columns ----------------------------------------
    if xk == ColKind.NUMERIC and yk == ColKind.NUMERIC:
        if has_color and color_is_low_cat:
            out.append(
                Suggestion(
                    GroupedScatter,
                    {"x": x_name, "y": y_name, "hue": color_name},
                    0.95,
                    "two numeric + low-cardinality group → grouped scatter",
                )
            )
        else:
            out.append(
                Suggestion(
                    ScatterPlot,
                    {"x": x_name, "y": y_name},
                    0.95,
                    "two numeric → scatter plot",
                )
            )
        return out

    # ------ Categorical x + numeric y ----------------------------------
    if is_low_cat and yk == ColKind.NUMERIC:
        if has_color and color_is_low_cat:
            out.append(
                Suggestion(
                    GroupedBarPlot,
                    {"x": x_name, "y": y_name, "hue": color_name},
                    0.92,
                    "two categoricals + numeric → grouped bar",
                )
            )
            out.append(
                Suggestion(
                    BoxPlotByGroup,
                    {"x": x_name, "y": y_name, "hue": color_name},
                    0.85,
                    "use box plots if individual observations carry meaning",
                )
            )
            out.append(
                Suggestion(
                    StackedBarPlot,
                    {"x": x_name, "y": y_name, "hue": color_name},
                    0.7,
                    "stacked alternative if values compose a whole",
                )
            )
        else:
            out.append(
                Suggestion(
                    BarPlot,
                    {"x": x_name, "y": y_name},
                    0.9,
                    "low-cardinality x + numeric y → bar plot",
                )
            )
            out.append(
                Suggestion(
                    LollipopChart,
                    {"x": x_name, "y": y_name},
                    0.7,
                    "lollipop alternative when bars feel heavy",
                )
            )
            out.append(
                Suggestion(
                    Boxplot,
                    {"x": x_name, "y": y_name},
                    0.72,
                    "box plot if there are multiple observations per category",
                )
            )
        return out

    # ------ Single numeric column → distribution -----------------------
    if xk == ColKind.NUMERIC and y_summary is None:
        out.append(
            Suggestion(
                DensityPlot,
                {"x": x_name},
                0.9,
                "single numeric column → KDE density plot",
            )
        )
        out.append(
            Suggestion(
                Boxplot,
                {"y": x_name},
                0.7,
                "box plot summary alternative",
            )
        )
        out.append(
            Suggestion(
                Violinplot,
                {"y": x_name},
                0.7,
                "violin plot alternative",
            )
        )
        return out

    # ------ Single low-cardinality categorical → counts ----------------
    if is_low_cat and y_summary is None:
        out.append(
            Suggestion(
                PieChart,
                {"names": x_name, "values": x_name},
                0.4,
                "single categorical → pie chart of counts (consider df.value_counts())",
            )
        )

    return out


__all__ = ["Suggestion", "auto", "suggest"]
