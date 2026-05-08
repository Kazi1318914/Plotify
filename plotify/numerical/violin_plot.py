"""
plotify.numerical.violin_plot
=============================

Dual-backend violin plot wrapping :func:`seaborn.violinplot` and
:func:`plotly.express.violin`.
"""

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from plotify.base import BasePlot


class Violinplot(BasePlot):
    """
    Violin plot: a KDE mirrored around a central axis, optionally with an
    inner box/quartile/stick representation of the raw data.
    """

    def __init__(
        self,
        df,
        x=None,
        y=None,
        hue=None,
        order=None,
        hue_order=None,
        bw="scott",
        cut=2,
        scale="area",
        scale_hue=True,
        gridsize=100,
        width=0.8,
        inner="box",
        split=False,
        dodge=True,
        orient=None,
        linewidth=None,
        color=None,
        palette=None,
        saturation=0.75,
        ax=None,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create violinplot figures.

        Parameters mirror :func:`seaborn.violinplot` where applicable; refer
        there for detail. ``backend`` selects between Seaborn and Plotly.

        Parameters
        ----------
        df : pandas.DataFrame or array-like
            The data to plot. DataFrame preferred.
        x, y, hue : str, optional
            Variables used for plotting.
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
        self.__bw = bw
        self.__cut = cut
        self.__scale = scale
        self.__scale_hue = scale_hue
        self.__gridsize = gridsize
        self.__width = width
        self.__inner = inner
        self.__split = split
        self.__dodge = dodge
        self.__orient = orient
        self.__linewidth = linewidth
        self.__color = color
        self.__palette = palette
        self.__saturation = saturation
        self.__ax = ax
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using :func:`seaborn.violinplot`."""
        # Newer seaborn versions renamed ``bw`` to ``bw_method``. We pass via
        # kwargs after catching the legacy name so older installs still work.
        sns.violinplot(
            x=self.__x,
            y=self.__y,
            hue=self.__hue,
            data=self.__df,
            order=self.__order,
            hue_order=self.__hue_order,
            cut=self.__cut,
            gridsize=self.__gridsize,
            width=self.__width,
            inner=self.__inner,
            split=self.__split,
            dodge=self.__dodge,
            orient=self.__orient,
            linewidth=self.__linewidth,
            color=self.__color,
            palette=self.__palette,
            saturation=self.__saturation,
            ax=self.__ax,
            **self.__kwargs,
        )
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.violin`."""
        # Plotly's violin supports ``box`` and ``points`` toggles; map the
        # seaborn ``inner`` to the closest equivalent.
        inner_box = self.__inner == "box"
        points = "all" if self.__inner in ("point", "stick") else False

        fig = px.violin(
            self.__df,
            x=self.__x,
            y=self.__y,
            color=self.__hue,
            box=inner_box,
            points=points,
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
