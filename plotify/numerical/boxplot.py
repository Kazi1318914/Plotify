"""
plotify.numerical.boxplot
=========================

Dual-backend Boxplot class. Wraps :func:`seaborn.boxplot` on the Seaborn
backend and :func:`plotly.express.box` on the Plotly backend.
"""

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from plotify.base import BasePlot


class Boxplot(BasePlot):
    """
    Create a boxplot using either Seaborn/Matplotlib or Plotly.

    A boxplot summarises the distribution of a numeric variable using the
    first, second (median) and third quartiles, plus whiskers that extend
    to the furthest non-outlier observations.
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
        saturation=0.75,
        width=0.8,
        dodge=True,
        fliersize=5,
        linewidth=None,
        whis=1.5,
        ax=None,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create boxplot figures using seaborn or plotly.

        Parameters
        ----------
        df : pandas.DataFrame
            The dataframe containing the data to plot.
        x, y : str, optional
            The names of two columns in df. The box plots will be for the y
            column grouped by x column values.
        hue : str, optional
            Column name for grouping the data by color/hue.
        order, hue_order : list, optional
            Order to plot the categorical levels in.
        orient : str, optional
            Orientation of the plot. ``'v'`` or ``'h'``. (Seaborn only.)
        color : str, optional
            Color for all of the elements. (Seaborn only.)
        palette : str, optional
            Colors to use for the different levels of the hue variable.
        saturation : float, optional
            Proportion of the original saturation to draw colors. (Seaborn only.)
        width : float, optional
            Width of a full element.
        dodge : bool, optional
            Whether elements should be shifted along the categorical axis
            when hue nesting is used. (Seaborn only.)
        fliersize : float, optional
            Size of the markers used to indicate outlier observations.
            (Seaborn only.)
        linewidth : float, optional
            Line width of the box outlines. (Seaborn only.)
        whis : float, optional
            Proportion of the IQR past the low and high quartiles to extend
            the plot whiskers. (Seaborn only.)
        ax : matplotlib.axes, optional
            Pre-existing axes. (Seaborn only.)
        title : str, optional
            Title for the plot.
        backend : {"seaborn", "plotly"}, default="seaborn"
            Rendering backend.
        **kwargs :
            Additional keyword arguments forwarded to the underlying library
            function (``sns.boxplot`` or ``plotly.express.box``).

        Returns
        -------
        None
        """
        # Store everything as private attributes so render methods can read them.
        self.__df = df
        self.__x = x
        self.__y = y
        self.__hue = hue
        self.__order = order
        self.__hue_order = hue_order
        self.__orient = orient
        self.__color = color
        self.__palette = palette
        self.__saturation = saturation
        self.__width = width
        self.__dodge = dodge
        self.__fliersize = fliersize
        self.__linewidth = linewidth
        self.__whis = whis
        self.__ax = ax
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render the boxplot using :func:`seaborn.boxplot`."""
        sns.boxplot(
            x=self.__x,
            y=self.__y,
            hue=self.__hue,
            data=self.__df,
            order=self.__order,
            hue_order=self.__hue_order,
            orient=self.__orient,
            color=self.__color,
            palette=self.__palette,
            saturation=self.__saturation,
            width=self.__width,
            dodge=self.__dodge,
            fliersize=self.__fliersize,
            linewidth=self.__linewidth,
            whis=self.__whis,
            ax=self.__ax,
            **self.__kwargs,
        )
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render the boxplot using :func:`plotly.express.box`."""
        # Plotly ignores most of the Seaborn-only cosmetic params; we forward
        # the ones that map cleanly and let **kwargs carry anything extra.
        fig = px.box(
            self.__df,
            x=self.__x,
            y=self.__y,
            color=self.__hue,
            color_discrete_sequence=(
                [self.__palette] if isinstance(self.__palette, str) else None
            ),
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
