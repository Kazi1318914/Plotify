"""
plotify.numerical.scatter_plot
==============================

Dual-backend scatter plot, optionally with a regression line.
"""

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from plotify.base import BasePlot


class ScatterPlot(BasePlot):
    """
    Scatter plot with optional regression overlay.

    The ``style`` parameter selects the Seaborn variant:

    * ``"scatter"`` → :func:`seaborn.scatterplot` (default)
    * ``"reg"``     → :func:`seaborn.regplot`
    * ``"lm"``      → :func:`seaborn.lmplot`

    On the Plotly backend, any ``style != "scatter"`` is rendered through
    :func:`plotly.express.scatter` with ``trendline="ols"``.
    """

    def __init__(
        self,
        df,
        x=None,
        y=None,
        plots=None,
        style="scatter",
        ax=None,
        title=None,
        default_style=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create scatter plots using seaborn or plotly.

        Parameters
        ----------
        df : pandas.DataFrame
            The data to plot.
        x, y : str, optional
            Column names for the x- and y-axes (used for a single basic plot).
        plots : list[dict], optional
            List of per-series parameter dicts. Each dict must contain at
            minimum ``"x"`` and ``"y"`` keys.
        style : {"scatter", "reg", "lm"}, default="scatter"
            Which Seaborn function / Plotly trendline to use.
        ax : matplotlib.axes.Axes, optional
            Pre-existing axes for the seaborn backend.
        title : str, optional
            Plot title.
        default_style : dict, optional
            Shared keyword arguments merged into each plot spec when ``plots``
            is not provided and a single ``(x, y)`` is used.
        backend : {"seaborn", "plotly"}, default="seaborn"
            Rendering backend.
        **kwargs :
            Forwarded to the underlying library function.

        Returns
        -------
        None
        """
        self.__df = df
        self.__plots = plots or []
        self.__style = style
        self.__ax = ax
        self.__default_style = default_style or {}
        self.__kwargs = kwargs

        # When only x/y are supplied, build a single-entry spec list so both
        # backends can iterate the same way.
        if x and y:
            self.__plots = [{"x": x, "y": y, **self.__default_style, **kwargs}]

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render via Seaborn using the chosen ``style``."""
        sns.set_style("darkgrid")

        for plot in self.__plots:
            # Copy so we don't mutate the caller's dict across renders.
            spec = dict(plot)
            x = spec.pop("x")
            y = spec.pop("y")

            if self.__style == "lm":
                # lmplot creates its own figure — no ax= allowed.
                sns.lmplot(x=x, y=y, data=self.__df, **spec)
            elif self.__style == "reg":
                sns.regplot(
                    x=self.__df[x], y=self.__df[y], ax=self.__ax, **spec
                )
            else:
                sns.scatterplot(
                    x=self.__df[x], y=self.__df[y], ax=self.__ax, **spec
                )

        if self._title and self.__ax is not None:
            self.__ax.set_title(self._title)
        elif self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render via Plotly Express, overlaying every series onto one figure."""
        fig = None
        # Build one figure layering each spec as a separate series.
        for plot in self.__plots:
            spec = dict(plot)
            x = spec.pop("x")
            y = spec.pop("y")

            # Regression overlays use px's built-in OLS trendline.
            trendline = "ols" if self.__style in ("reg", "lm") else None

            series_fig = px.scatter(
                self.__df,
                x=x,
                y=y,
                trendline=trendline,
                title=self._title,
            )
            if fig is None:
                fig = series_fig
            else:
                # Append each trace from the second+ spec onto the primary fig.
                for trace in series_fig.data:
                    fig.add_trace(trace)

        self._fig = fig
