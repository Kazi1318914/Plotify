"""
plotify.categorical.lollipop_chart
==================================

Lollipop chart — a cleaner alternative to bar charts where each bar is
replaced by a thin stem ending in a dot.
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go

from plotify.base import BasePlot


class LollipopChart(BasePlot):
    """
    Lollipop chart.

    Parameters ``x`` (category) and ``y`` (numeric value) are required in
    ``df``. On the Seaborn backend this is drawn with :func:`matplotlib.pyplot.stem`
    plus a scatter overlay; on the Plotly backend it uses ``go.Scatter``
    markers with per-marker line shapes.
    """

    def __init__(
        self,
        df,
        x,
        y,
        color=None,
        marker_size=8,
        linewidth=2,
        orient="v",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a lollipop chart.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        x : str
            Column containing category labels.
        y : str
            Column containing numeric values.
        color : str, optional
            Colour for stems and markers.
        marker_size : int, default=8
            Size of the lollipop head.
        linewidth : int, default=2
            Thickness of the stem.
        orient : {"v", "h"}, default="v"
            Vertical or horizontal orientation.
        title : str, optional
            Plot title.
        backend : {"seaborn", "plotly"}, default="seaborn"
            Rendering backend.
        **kwargs :
            Forwarded to the underlying library.

        Returns
        -------
        None
        """
        self.__df = df
        self.__x = x
        self.__y = y
        self.__color = color or "steelblue"
        self.__marker_size = marker_size
        self.__linewidth = linewidth
        self.__orient = orient
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using matplotlib's ``vlines`` / ``hlines`` + scatter."""
        ax = plt.gca()
        categories = self.__df[self.__x]
        values = self.__df[self.__y]

        # Draw the stems first, then the markers on top — matches the canonical
        # "lollipop" look.
        if self.__orient == "v":
            ax.vlines(
                x=categories,
                ymin=0,
                ymax=values,
                color=self.__color,
                linewidth=self.__linewidth,
            )
            ax.scatter(
                categories, values, s=self.__marker_size**2, color=self.__color
            )
        else:
            ax.hlines(
                y=categories,
                xmin=0,
                xmax=values,
                color=self.__color,
                linewidth=self.__linewidth,
            )
            ax.scatter(
                values, categories, s=self.__marker_size**2, color=self.__color
            )

        if self._title:
            ax.set_title(self._title)

    def _plot_plotly(self):
        """Render using Plotly ``go.Scatter`` with per-point line shapes."""
        categories = self.__df[self.__x].tolist()
        values = self.__df[self.__y].tolist()

        fig = go.Figure()

        # One line shape per category gives us the stem.
        shapes = []
        for cat, val in zip(categories, values):
            if self.__orient == "v":
                shapes.append(
                    dict(
                        type="line",
                        x0=cat,
                        x1=cat,
                        y0=0,
                        y1=val,
                        line=dict(color=self.__color, width=self.__linewidth),
                    )
                )
            else:
                shapes.append(
                    dict(
                        type="line",
                        y0=cat,
                        y1=cat,
                        x0=0,
                        x1=val,
                        line=dict(color=self.__color, width=self.__linewidth),
                    )
                )

        # Scatter carries the lollipop heads.
        if self.__orient == "v":
            fig.add_trace(
                go.Scatter(
                    x=categories,
                    y=values,
                    mode="markers",
                    marker=dict(size=self.__marker_size, color=self.__color),
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=values,
                    y=categories,
                    mode="markers",
                    marker=dict(size=self.__marker_size, color=self.__color),
                )
            )

        fig.update_layout(shapes=shapes, title=self._title, showlegend=False)
        self._fig = fig
