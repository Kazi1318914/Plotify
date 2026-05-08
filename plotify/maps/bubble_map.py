"""
plotify.maps.bubble_map
=======================

Dual-backend bubble map — markers placed at geographic coordinates, sized
(and optionally coloured) by a numeric value.
"""

import matplotlib.pyplot as plt
import plotly.express as px

from plotify.base import BasePlot


class BubbleMap(BasePlot):
    """
    Bubble map.

    Seaborn backend draws a scatter on a bare (lat, lon) plane. Plotly
    backend uses :func:`plotly.express.scatter_geo` with real geographic
    projection.
    """

    def __init__(
        self,
        df,
        lat,
        lon,
        size,
        color=None,
        hover_name=None,
        scope="world",
        projection="natural earth",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a bubble map.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        lat, lon : str
            Latitude / longitude column names.
        size : str
            Column used to scale marker size.
        color : str, optional
            Column used to colour-encode markers.
        hover_name : str, optional
            Column used for Plotly hover labels.
        scope : str, default="world"
            Plotly geographic scope.
        projection : str, default="natural earth"
            Plotly projection.
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
        self.__size = size
        self.__color = color
        self.__hover_name = hover_name
        self.__scope = scope
        self.__projection = projection
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render a plain scatter of (lon, lat) sized by ``size``.

        This is a non-projected rendering — no coastlines or country
        borders are drawn. For proper geography, prefer the Plotly backend.
        """
        plt.scatter(
            self.__df[self.__lon],
            self.__df[self.__lat],
            s=self.__df[self.__size],
            c=self.__df[self.__color] if self.__color else None,
            alpha=0.6,
            **self.__kwargs,
        )
        plt.xlabel("lon")
        plt.ylabel("lat")
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.scatter_geo`."""
        fig = px.scatter_geo(
            self.__df,
            lat=self.__lat,
            lon=self.__lon,
            size=self.__size,
            color=self.__color,
            hover_name=self.__hover_name,
            scope=self.__scope,
            projection=self.__projection,
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
