"""
plotify.timeseries.line_chart
=============================

Dual-backend line chart — evolution of one or more numeric series over time.
"""

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from plotify.base import BasePlot


class LineChart(BasePlot):
    """
    Line chart.

    Wraps :func:`seaborn.lineplot` (Seaborn backend) and
    :func:`plotly.express.line` (Plotly backend).
    """

    def __init__(
        self,
        df,
        x,
        y,
        hue=None,
        style=None,
        markers=False,
        dashes=True,
        palette=None,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a line chart.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        x : str
            Column for the x axis (typically a time column).
        y : str
            Column for the numeric y axis.
        hue : str, optional
            Column for colour grouping — one line per group.
        style : str, optional
            Column for line-style grouping (Seaborn only).
        markers : bool, default=False
            Whether to overlay point markers on each line.
        dashes : bool, default=True
            Whether to use dashed lines when ``style`` is set (Seaborn only).
        palette : str or list, optional
            Colour palette.
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
        self.__hue = hue
        self.__style = style
        self.__markers = markers
        self.__dashes = dashes
        self.__palette = palette
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using :func:`seaborn.lineplot`."""
        sns.lineplot(
            data=self.__df,
            x=self.__x,
            y=self.__y,
            hue=self.__hue,
            style=self.__style,
            markers=self.__markers,
            dashes=self.__dashes,
            palette=self.__palette,
            **self.__kwargs,
        )
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.line`."""
        fig = px.line(
            self.__df,
            x=self.__x,
            y=self.__y,
            color=self.__hue,
            line_dash=self.__style,
            markers=self.__markers,
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
