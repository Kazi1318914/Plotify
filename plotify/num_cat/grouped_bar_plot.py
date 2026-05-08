"""
plotify.num_cat.grouped_bar_plot
================================

Grouped (side-by-side) bar plot for comparing a numeric value across one
categorical axis and one sub-group axis.
"""

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from plotify.base import BasePlot


class GroupedBarPlot(BasePlot):
    """
    Grouped bar plot.

    A primary category on the x axis, a secondary category that splits each
    primary bar into side-by-side sub-bars, and a numeric y axis.
    """

    def __init__(
        self,
        df,
        x,
        y,
        hue,
        order=None,
        hue_order=None,
        palette=None,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a grouped bar plot.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        x : str
            Primary categorical column.
        y : str
            Numeric value column.
        hue : str
            Sub-group categorical column — each value becomes a sub-bar.
        order, hue_order : list, optional
            Explicit category ordering.
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
        self.__order = order
        self.__hue_order = hue_order
        self.__palette = palette
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using :func:`seaborn.barplot` with ``dodge=True``."""
        sns.barplot(
            data=self.__df,
            x=self.__x,
            y=self.__y,
            hue=self.__hue,
            order=self.__order,
            hue_order=self.__hue_order,
            palette=self.__palette,
            dodge=True,
            **self.__kwargs,
        )
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.bar` with ``barmode='group'``."""
        fig = px.bar(
            self.__df,
            x=self.__x,
            y=self.__y,
            color=self.__hue,
            barmode="group",
            category_orders={
                self.__x: self.__order,
                self.__hue: self.__hue_order,
            }
            if (self.__order or self.__hue_order)
            else None,
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
