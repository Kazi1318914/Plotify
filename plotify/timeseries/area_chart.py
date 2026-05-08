"""
plotify.timeseries.area_chart
=============================

Dual-backend single-series area chart — a line chart with the region under
the curve filled.
"""

import matplotlib.pyplot as plt
import plotly.express as px

from plotify.base import BasePlot


class AreaChart(BasePlot):
    """
    Single-series filled area chart.

    For multiple stacked series, see :class:`StackedAreaChart`.
    """

    def __init__(
        self,
        df,
        x,
        y,
        color="steelblue",
        alpha=0.4,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create an area chart.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        x : str
            Column for the x axis.
        y : str
            Numeric column whose values are filled to the x axis.
        color : str, default="steelblue"
            Fill colour.
        alpha : float, default=0.4
            Fill transparency (Seaborn only).
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
        self.__color = color
        self.__alpha = alpha
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using :func:`matplotlib.pyplot.fill_between`."""
        x_vals = self.__df[self.__x]
        y_vals = self.__df[self.__y]

        # Draw the outline first so that the fill does not wash out the line.
        plt.plot(x_vals, y_vals, color=self.__color)
        plt.fill_between(x_vals, y_vals, color=self.__color, alpha=self.__alpha)
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.area`."""
        fig = px.area(
            self.__df,
            x=self.__x,
            y=self.__y,
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
