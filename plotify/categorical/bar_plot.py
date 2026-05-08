"""
plotify.categorical.bar_plot
============================

Dual-backend bar plot wrapping :func:`seaborn.barplot` and
:func:`plotly.express.bar`.
"""

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from plotify.base import BasePlot


class BarPlot(BasePlot):
    """
    Represent categorical entities with bars whose length encodes a numeric value.
    """

    def __init__(
        self,
        df,
        x=None,
        y=None,
        hue=None,
        order=None,
        hue_order=None,
        orient=None,
        color=None,
        palette=None,
        estimator="mean",
        ci=95,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a bar plot.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        x, y : str, optional
            Column names for the categorical axis and numeric axis.
        hue : str, optional
            Column name for colour grouping.
        order, hue_order : list, optional
            Category ordering.
        orient : {"v", "h"}, optional
            Orientation (Seaborn only).
        color : str, optional
            A single colour override (Seaborn only).
        palette : str or list, optional
            Colour palette.
        estimator : str or callable, default="mean"
            Aggregation applied when multiple observations share a category
            (Seaborn only).
        ci : float, default=95
            Confidence interval size for the error bars (Seaborn only).
        title : str, optional
            Plot title.
        backend : {"seaborn", "plotly"}, default="seaborn"
            Rendering backend.
        **kwargs :
            Forwarded to the underlying library function.

        Returns
        -------
        None
        """
        self.__df = df
        self.__x = x
        self.__y = y
        self.__hue = hue
        self.__order = order
        self.__hue_order = hue_order
        self.__orient = orient
        self.__color = color
        self.__palette = palette
        self.__estimator = estimator
        self.__ci = ci
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using :func:`seaborn.barplot`."""
        sns.barplot(
            data=self.__df,
            x=self.__x,
            y=self.__y,
            hue=self.__hue,
            order=self.__order,
            hue_order=self.__hue_order,
            orient=self.__orient,
            color=self.__color,
            palette=self.__palette,
            estimator=self.__estimator,
            **self.__kwargs,
        )
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.bar`."""
        fig = px.bar(
            self.__df,
            x=self.__x,
            y=self.__y,
            color=self.__hue,
            orientation=(self.__orient if self.__orient in ("h", "v") else None),
            category_orders=(
                {self.__x: self.__order} if self.__order and self.__x else None
            ),
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
