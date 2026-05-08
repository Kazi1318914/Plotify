"""
plotify.numerical.density_plot
==============================

Dual-backend kernel-density / density-contour plot.
"""

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from plotify.base import BasePlot


class DensityPlot(BasePlot):
    """
    Kernel density estimate (1D) or density contour (2D) plot.

    On the Seaborn backend this wraps :func:`seaborn.kdeplot`. On the Plotly
    backend it uses :func:`plotly.express.density_contour` (bivariate) or
    :func:`plotly.express.histogram` with ``marginal="violin"`` for univariate
    cases.
    """

    def __init__(
        self,
        df,
        x=None,
        y=None,
        hue=None,
        weights=None,
        palette=None,
        hue_order=None,
        hue_norm=None,
        fill=False,
        color=None,
        multiple="layer",
        common_norm=True,
        common_grid=False,
        cumulative=False,
        bw_method="scott",
        bw_adjust=1,
        warn_singular=True,
        log_scale=None,
        levels=10,
        thresh=0.05,
        gridsize=200,
        cut=3,
        clip=None,
        legend=True,
        cbar=False,
        cbar_ax=None,
        cbar_kws=None,
        ax=None,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create density plot figures.

        Parameters mirror :func:`seaborn.kdeplot`. See that function's
        documentation for exhaustive descriptions. The ``backend`` parameter
        selects between Seaborn/Matplotlib and Plotly.

        Parameters
        ----------
        df : pandas.DataFrame
            Data for the plot.
        x, y : str, optional
            Variables to map to the x and y axes. Pass ``y`` as well to obtain
            a bivariate density.
        hue : str, optional
            Variable to map to color.
        backend : {"seaborn", "plotly"}, default="seaborn"
            Rendering backend.
        **kwargs :
            Extra keyword arguments forwarded to the underlying library.

        Returns
        -------
        None
        """
        self.__df = df
        self.__x = x
        self.__y = y
        self.__hue = hue
        self.__weights = weights
        self.__palette = palette
        self.__hue_order = hue_order
        self.__hue_norm = hue_norm
        self.__fill = fill
        self.__color = color
        self.__multiple = multiple
        self.__common_norm = common_norm
        self.__common_grid = common_grid
        self.__cumulative = cumulative
        self.__bw_method = bw_method
        self.__bw_adjust = bw_adjust
        self.__warn_singular = warn_singular
        self.__log_scale = log_scale
        self.__levels = levels
        self.__thresh = thresh
        self.__gridsize = gridsize
        self.__cut = cut
        self.__clip = clip
        self.__legend = legend
        self.__cbar = cbar
        self.__cbar_ax = cbar_ax
        self.__cbar_kws = cbar_kws
        self.__ax = ax
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using :func:`seaborn.kdeplot`."""
        sns.kdeplot(
            data=self.__df,
            x=self.__x,
            y=self.__y,
            hue=self.__hue,
            weights=self.__weights,
            palette=self.__palette,
            hue_order=self.__hue_order,
            hue_norm=self.__hue_norm,
            fill=self.__fill,
            color=self.__color,
            multiple=self.__multiple,
            common_norm=self.__common_norm,
            common_grid=self.__common_grid,
            cumulative=self.__cumulative,
            bw_method=self.__bw_method,
            bw_adjust=self.__bw_adjust,
            warn_singular=self.__warn_singular,
            log_scale=self.__log_scale,
            levels=self.__levels,
            thresh=self.__thresh,
            gridsize=self.__gridsize,
            cut=self.__cut,
            clip=self.__clip,
            legend=self.__legend,
            cbar=self.__cbar,
            cbar_ax=self.__cbar_ax,
            cbar_kws=self.__cbar_kws,
            ax=self.__ax,
            **self.__kwargs,
        )
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using Plotly Express.

        Picks ``density_contour`` when both x and y are supplied, falls back
        to a KDE-style ``histogram`` with marginal violin otherwise.
        """
        if self.__x is not None and self.__y is not None:
            # Bivariate: a density contour is the closest Plotly analogue.
            fig = px.density_contour(
                self.__df,
                x=self.__x,
                y=self.__y,
                color=self.__hue,
                title=self._title,
                **self.__kwargs,
            )
            if self.__fill:
                fig.update_traces(contours_coloring="fill")
        else:
            # Univariate: Plotly does not have a first-class KDE; approximate
            # with a normalised histogram and a violin marginal.
            axis = self.__x if self.__x is not None else self.__y
            fig = px.histogram(
                self.__df,
                x=axis,
                color=self.__hue,
                histnorm="probability density",
                marginal="violin",
                title=self._title,
                **self.__kwargs,
            )
        self._fig = fig
