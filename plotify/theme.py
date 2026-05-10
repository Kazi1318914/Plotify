"""
plotify.theme
=============

The Plotify theme system. A *theme* bundles up colour palette, fonts,
spine visibility, gridlines, and tick formatting in one place; calling
:func:`apply_current` translates the current theme into the global state
of whichever backend is about to render.

The shipped ``"publication"`` theme is applied automatically — every
Plotify plot picks it up unless the caller disables theming via
``theme.set("none")``. Custom themes can be registered with
:func:`register`.
"""

from dataclasses import dataclass, field

import matplotlib as mpl
import matplotlib.ticker as mticker
import plotly.graph_objects as go
import plotly.io as pio


@dataclass(frozen=True)
class Theme:
    """A single visual theme.

    Attributes are intentionally backend-agnostic — the ``_apply_*`` helpers
    below translate them into matplotlib rcParams or a Plotly template.
    """

    name: str
    palette: tuple[str, ...]
    background: str = "white"
    grid_color: str = "#E5E5E5"
    font_family: str = "DejaVu Sans"
    title_size: int = 14
    label_size: int = 11
    tick_size: int = 10
    # Which spines (axes borders) to keep visible.
    spines: tuple[str, ...] = ("left", "bottom")
    # If True, format large numeric ticks as 1.2K / 3.4M / 5B etc.
    smart_ticks: bool = True
    # Extra metadata set by helpers — not user-facing but lets the theme be
    # extended without breaking the dataclass signature.
    extras: dict = field(default_factory=dict)


# Okabe & Ito 2008 — colourblind-safe qualitative palette. Order chosen so
# the first 4 colours look good on bar charts, the remaining 4 fill in
# without overwhelming.
_OKABE_ITO = (
    "#0072B2",  # blue
    "#E69F00",  # orange
    "#009E73",  # green
    "#D55E00",  # vermilion
    "#56B4E9",  # sky blue
    "#F0E442",  # yellow
    "#CC79A7",  # purple
    "#000000",  # black
)


PUBLICATION = Theme(
    name="publication",
    palette=_OKABE_ITO,
    background="white",
    grid_color="#E5E5E5",
    font_family="DejaVu Sans",
    title_size=14,
    label_size=11,
    tick_size=10,
    spines=("left", "bottom"),
    smart_ticks=True,
)


# A no-op theme that resets matplotlib/Plotly to their library defaults.
NONE = Theme(
    name="none",
    palette=(),
    background="white",
    grid_color="#CCCCCC",
    spines=("left", "bottom", "top", "right"),
    smart_ticks=False,
)


# ---- registry -----------------------------------------------------------

_REGISTRY: dict[str, Theme] = {
    PUBLICATION.name: PUBLICATION,
    NONE.name: NONE,
}

# Module-level current theme. Defaulted to PUBLICATION so a fresh
# `import plotify` immediately produces the polished output.
_CURRENT: Theme = PUBLICATION


def register(theme: Theme) -> None:
    """Register a custom theme so it can be selected by name."""
    _REGISTRY[theme.name] = theme


def get_current() -> Theme:
    """Return the currently active theme."""
    return _CURRENT


def set(name_or_theme) -> Theme:  # noqa: A001  (deliberately shadows builtin `set`)
    """Switch the active theme.

    Parameters
    ----------
    name_or_theme : str or Theme
        Either the registered name of a theme (``"publication"`` /
        ``"none"`` / any name passed to :func:`register`) or a
        :class:`Theme` instance.

    Returns
    -------
    Theme
        The newly active theme.
    """
    global _CURRENT
    if isinstance(name_or_theme, Theme):
        _CURRENT = name_or_theme
    else:
        if name_or_theme not in _REGISTRY:
            raise ValueError(
                f"Unknown theme {name_or_theme!r}. Registered: {list(_REGISTRY)}"
            )
        _CURRENT = _REGISTRY[name_or_theme]
    return _CURRENT


# ---- apply --------------------------------------------------------------

def apply_current(backend: str) -> None:
    """Apply the current theme to a backend's global state.

    Called by :class:`plotify.base.BasePlot._render` immediately before
    rendering, so the most recent ``set()`` always wins.
    """
    if _CURRENT.name == "none":
        # Skip mutation entirely so the user's pre-existing matplotlib /
        # Plotly settings are preserved.
        return
    if backend == "seaborn":
        _apply_matplotlib(_CURRENT)
    else:
        _apply_plotly(_CURRENT)


def _apply_matplotlib(theme: Theme) -> None:
    """Translate ``theme`` into matplotlib rcParams + a default cycler."""
    spines_visible = {s: (s in theme.spines) for s in ("top", "right", "left", "bottom")}

    palette = list(theme.palette) or mpl.rcParams["axes.prop_cycle"].by_key().get(
        "color", []
    )

    rc = {
        # Spines
        "axes.spines.top": spines_visible["top"],
        "axes.spines.right": spines_visible["right"],
        "axes.spines.left": spines_visible["left"],
        "axes.spines.bottom": spines_visible["bottom"],
        # Grid
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": theme.grid_color,
        "grid.alpha": 0.6,
        "grid.linewidth": 0.7,
        # Type
        "font.family": theme.font_family,
        "axes.titlesize": theme.title_size,
        "axes.titleweight": "bold",
        "axes.labelsize": theme.label_size,
        "xtick.labelsize": theme.tick_size,
        "ytick.labelsize": theme.tick_size,
        # Background
        "figure.facecolor": theme.background,
        "axes.facecolor": theme.background,
        # Margins
        "axes.titlepad": 12,
        "axes.labelpad": 6,
    }
    if palette:
        rc["axes.prop_cycle"] = mpl.cycler(color=palette)

    mpl.rcParams.update(rc)


def _apply_plotly(theme: Theme) -> None:
    """Build a Plotly template that mirrors ``theme`` and make it the default.

    Notes
    -----
    We deliberately do **not** set ``tickformat`` on the axes. Setting a
    numeric format such as ``"~s"`` here would apply globally and break
    date axes (they would render as ``"~s"`` literals). Plotly already
    auto-detects axis types and formats accordingly; users who want SI
    suffixes on a specific numeric axis can opt in per-plot via
    ``fig.update_yaxes(tickformat="~s")``.
    """
    template = go.layout.Template()
    template.layout = go.Layout(
        colorway=list(theme.palette),
        plot_bgcolor=theme.background,
        paper_bgcolor=theme.background,
        font=dict(family=theme.font_family, size=theme.label_size),
        title=dict(
            font=dict(family=theme.font_family, size=theme.title_size),
        ),
        xaxis=dict(
            gridcolor=theme.grid_color,
            zeroline=False,
            showline="bottom" in theme.spines,
            linecolor="#444444",
        ),
        yaxis=dict(
            gridcolor=theme.grid_color,
            zeroline=False,
            showline="left" in theme.spines,
            linecolor="#444444",
        ),
    )
    pio.templates["plotify"] = template
    pio.templates.default = "plotify"


# ---- helpers ------------------------------------------------------------

def smart_formatter() -> mticker.Formatter:
    """Return a matplotlib formatter that prints ``1.2K`` / ``3.4M`` / ``5B``.

    Plotly applies ``tickformat="~s"`` directly via the template so this is
    only used by the seaborn / matplotlib path.
    """

    def _fmt(value: float, _pos: int) -> str:
        if value == 0:
            return "0"
        absval = abs(value)
        # Sub-unit values: keep significant figures, no SI prefix.
        if absval < 1:
            return f"{value:.2g}"
        if absval < 1_000:
            # Drop trailing .0 for ints.
            if float(value).is_integer():
                return f"{int(value)}"
            return f"{value:g}"
        if absval < 1_000_000:
            return f"{value / 1_000:.1f}K".replace(".0K", "K")
        if absval < 1_000_000_000:
            return f"{value / 1_000_000:.1f}M".replace(".0M", "M")
        return f"{value / 1_000_000_000:.1f}B".replace(".0B", "B")

    return mticker.FuncFormatter(_fmt)


def apply_smart_ticks_to_current_axes() -> None:
    """Apply :func:`smart_formatter` to numeric tick axes of every open axes.

    Called after a seaborn render so the tick formatting reflects the theme
    even though it lives in axis-formatter space (which rcParams cannot
    express directly). Wrapped in try/except per-axis so we never break a
    chart that uses non-numeric ticks (dates, categories).
    """
    if not _CURRENT.smart_ticks or _CURRENT.name == "none":
        return
    import matplotlib.pyplot as plt  # local: avoids import-time backend lock

    for ax in plt.gcf().get_axes():
        for axis in (ax.xaxis, ax.yaxis):
            try:
                # Only override if the axis currently uses a default scalar
                # formatter — preserves date/category formatters.
                if isinstance(axis.get_major_formatter(), mticker.ScalarFormatter):
                    axis.set_major_formatter(smart_formatter())
            except Exception:
                continue


__all__ = [
    "Theme",
    "PUBLICATION",
    "NONE",
    "register",
    "get_current",
    "set",
    "apply_current",
    "apply_smart_ticks_to_current_axes",
    "smart_formatter",
]
