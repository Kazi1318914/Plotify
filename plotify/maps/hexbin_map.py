"""
plotify.maps.hexbin_map
=======================

Dual-backend hexagonal binning of geographic point data.
"""

import matplotlib.pyplot as plt
import plotly.figure_factory as ff

from plotify.base import BasePlot


class HexbinMap(BasePlot):
    """
    Hexbin aggregation of (lat, lon) points.

    Seaborn backend uses :func:`matplotlib.pyplot.hexbin`. Plotly backend
    uses :func:`plotly.figure_factory.create_hexbin_mapbox` if Mapbox tiles
    are available, falling back to a projected hexbin otherwise.
    """

    def __init__(
        self,
        df,
        lat,
        lon,
        gridsize=25,
        cmap="viridis",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a hexbin map.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        lat, lon : str
            Latitude / longitude column names.
        gridsize : int, default=25
            Number of hex bins along the x axis.
        cmap : str, default="viridis"
            Colormap.
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
        self.__lat = lat
        self.__lon = lon
        self.__gridsize = gridsize
        self.__cmap = cmap
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using :func:`matplotlib.pyplot.hexbin`."""
        plt.hexbin(
            self.__df[self.__lon],
            self.__df[self.__lat],
            gridsize=self.__gridsize,
            cmap=self.__cmap,
            **self.__kwargs,
        )
        plt.colorbar(label="count")
        plt.xlabel("lon")
        plt.ylabel("lat")
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.figure_factory.create_hexbin_mapbox`."""
        fig = ff.create_hexbin_mapbox(
            data_frame=self.__df,
            lat=self.__lat,
            lon=self.__lon,
            nx_hexagon=self.__gridsize,
            opacity=0.6,
            color_continuous_scale=self.__cmap,
            **self.__kwargs,
        )
        # Use OpenStreetMap tiles to avoid needing a Mapbox token.
        fig.update_layout(mapbox_style="open-street-map", title=self._title)
        self._fig = fig
