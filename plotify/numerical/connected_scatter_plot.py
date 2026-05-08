"""
plotify.numerical.connected_scatter_plot
========================================

Dual-backend connected scatter plot — scatter points joined by line
segments, useful for showing the trajectory of paired observations.
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go

from plotify.base import BasePlot


class ConnectedScatterPlot(BasePlot):
    """
    Draw one or more connected scatter plots.

    Each series may be described by a dict in ``plots`` containing at least
    ``'x'`` and ``'y'`` and optionally ``'linestyle'``, ``'marker'``,
    ``'color'``, ``'linewidth'``, ``'label'``.
    """

    def __init__(
        self,
        df,
        x=None,
        y=None,
        plots=None,
        ax=None,
        title=None,
        default_style=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create one or more connected scatter plots.

        Parameters
        ----------
        df : pandas.DataFrame
            The data to plot.
        x, y : str, optional
            Column names for a single basic plot.
        plots : list[dict], optional
            List of per-series parameter dicts.
        ax : matplotlib.axes.Axes, optional
            Pre-existing axes (seaborn backend only).
        title : str, optional
            Plot title.
        default_style : dict, optional
            Default styling merged into the single-plot spec when ``plots``
            is not provided.
        backend : {"seaborn", "plotly"}, default="seaborn"
            Rendering backend.
        **kwargs :
            Extra style keys merged into the single-plot spec (seaborn
            backend) or ignored (plotly).

        Returns
        -------
        None
        """
        self.__df = df
        self.__plots = plots or []
        self.__ax = ax
        self.__default_style = default_style or {}

        # Promote a single (x, y) call to a one-entry plots list so both
        # render paths share the same loop structure.
        if x and y:
            self.__plots = [{"x": x, "y": y, **self.__default_style, **kwargs}]

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using :func:`matplotlib.axes.Axes.plot`."""
        if self.__ax is None:
            self.__ax = plt.gca()

        for plot in self.__plots:
            # Copy to avoid consuming the caller's dict on repeat renders.
            spec = dict(plot)
            x = spec.pop("x")
            y = spec.pop("y")
            self.__ax.plot(self.__df[x], self.__df[y], **spec)

        if self._title:
            self.__ax.set_title(self._title)

        # Only draw a legend if at least one trace carried a label.
        handles, labels = self.__ax.get_legend_handles_labels()
        if labels:
            self.__ax.legend()

    def _plot_plotly(self):
        """Render using Plotly ``go.Scatter`` traces with ``mode='lines+markers'``."""
        fig = go.Figure()
        for plot in self.__plots:
            spec = dict(plot)
            x_col = spec.pop("x")
            y_col = spec.pop("y")
            fig.add_trace(
                go.Scatter(
                    x=self.__df[x_col],
                    y=self.__df[y_col],
                    mode="lines+markers",
                    name=spec.get("label", y_col),
                    line=dict(
                        color=spec.get("color"),
                        width=spec.get("linewidth"),
                        dash=spec.get("linestyle"),
                    ),
                    marker=dict(symbol=spec.get("marker", "circle")),
                )
            )
        if self._title:
            fig.update_layout(title=self._title)
        self._fig = fig
