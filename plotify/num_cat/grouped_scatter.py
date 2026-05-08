"""
plotify.num_cat.grouped_scatter
===============================

Grouped scatter plot — scatter with colour (and optionally marker style)
encoding a categorical group.
"""

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from plotify.base import BasePlot


class GroupedScatter(BasePlot):
    """
    Scatter plot coloured by a categorical group column.

    Equivalent to :class:`plotify.numerical.ScatterPlot` with mandatory
    ``hue`` semantics — exposed as a separate class so numeric-only and
    grouped use cases are discoverable from separate subpackages.
    """

    def __init__(
        self,
        df,
        x,
        y,
        hue,
        style=None,
        size=None,
        palette=None,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a grouped scatter plot.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        x, y : str
            Numeric columns mapped to the axes.
        hue : str
            Categorical column mapped to colour.
        style : str, optional
            Column mapped to marker shape (Seaborn only).
        size : str, optional
            Column mapped to marker size.
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
        self.__size = size
        self.__palette = palette
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using :func:`seaborn.scatterplot` with hue/style mappings."""
        sns.scatterplot(
            data=self.__df,
            x=self.__x,
            y=self.__y,
            hue=self.__hue,
            style=self.__style,
            size=self.__size,
            palette=self.__palette,
            **self.__kwargs,
        )
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.scatter`."""
        fig = px.scatter(
            self.__df,
            x=self.__x,
            y=self.__y,
            color=self.__hue,
            symbol=self.__style,
            size=self.__size,
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
