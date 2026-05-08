"""
plotify.num_cat.box_plot_by_group
=================================

Box plots grouped by a secondary categorical variable — one cluster of
boxes per primary category.
"""

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from plotify.base import BasePlot


class BoxPlotByGroup(BasePlot):
    """
    Box plots split by a secondary (hue) categorical variable.

    Equivalent to :class:`plotify.numerical.Boxplot` with mandatory ``hue``;
    exposed as its own class to keep numeric-only and grouped use cases
    discoverable from separate subpackages.
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
        This is used to create box plots grouped by a sub-category.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        x : str
            Primary categorical axis.
        y : str
            Numeric column being summarised.
        hue : str
            Secondary categorical column — produces parallel boxes within
            each primary category.
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
        """Render using :func:`seaborn.boxplot` with hue grouping."""
        sns.boxplot(
            data=self.__df,
            x=self.__x,
            y=self.__y,
            hue=self.__hue,
            order=self.__order,
            hue_order=self.__hue_order,
            palette=self.__palette,
            **self.__kwargs,
        )
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.box`."""
        fig = px.box(
            self.__df,
            x=self.__x,
            y=self.__y,
            color=self.__hue,
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
