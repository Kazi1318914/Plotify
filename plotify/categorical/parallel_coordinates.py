"""
plotify.categorical.parallel_coordinates
========================================

Parallel coordinates plot — each vertical axis is one variable and each
polyline is one observation. Good for comparing samples across many
numeric dimensions at once.
"""

import matplotlib.pyplot as plt
import pandas.plotting as pdp
import plotly.express as px

from plotify.base import BasePlot


class ParallelCoordinates(BasePlot):
    """
    Parallel coordinates plot.

    Wraps :func:`pandas.plotting.parallel_coordinates` on the Seaborn backend
    and :func:`plotly.express.parallel_coordinates` on the Plotly backend.
    """

    def __init__(
        self,
        df,
        class_column,
        cols=None,
        color=None,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a parallel coordinates plot.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        class_column : str
            Column name used to group/colour the polylines. On the Plotly
            backend this must be numeric (Plotly uses a continuous colour
            scale); on Seaborn it may be categorical or numeric.
        cols : list[str], optional
            Subset of columns to plot as axes. Defaults to all numeric columns
            other than ``class_column``.
        color : list or str, optional
            Colour specification forwarded to the underlying function.
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
        self.__class_column = class_column
        self.__cols = cols
        self.__color = color
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render with pandas' own parallel_coordinates helper."""
        ax = pdp.parallel_coordinates(
            self.__df,
            class_column=self.__class_column,
            cols=self.__cols,
            color=self.__color,
            **self.__kwargs,
        )
        if self._title:
            ax.set_title(self._title)

    def _plot_plotly(self):
        """Render with :func:`plotly.express.parallel_coordinates`."""
        # px requires a numeric ``color`` column. We use the caller's
        # ``class_column`` directly.
        fig = px.parallel_coordinates(
            self.__df,
            color=self.__class_column,
            dimensions=self.__cols,
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
