"""
plotify.maps.choropleth_map
===========================

Choropleth map — regions coloured by a numeric value.

Both backends are implemented. The Seaborn backend uses a GeoDataFrame's
``plot`` method; the Plotly backend uses :func:`plotly.express.choropleth`
with either a GeoJSON or a built-in ``locationmode`` such as
``"country names"``.
"""

import matplotlib.pyplot as plt
import plotly.express as px

from plotify.base import BasePlot


class ChoroplethMap(BasePlot):
    """
    Region-level choropleth map.

    Two input modes:

    * **GeoDataFrame** (both backends) — pass a ``geopandas.GeoDataFrame``
      via ``df`` and the name of the numeric column via ``value``.
    * **Location name** (Plotly only) — pass a regular DataFrame plus
      ``locations`` (column name) and ``locationmode="country names"`` (or
      any mode :func:`plotly.express.choropleth` accepts) in ``kwargs``.
    """

    def __init__(
        self,
        df,
        value,
        locations=None,
        geojson=None,
        cmap="viridis",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a choropleth map.

        Parameters
        ----------
        df : pandas.DataFrame or geopandas.GeoDataFrame
            Input data.
        value : str
            Numeric column used for colouring.
        locations : str, optional
            Column with location identifiers (Plotly mode).
        geojson : dict or str, optional
            GeoJSON object or path (Plotly mode).
        cmap : str, default="viridis"
            Colormap name.
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
        self.__value = value
        self.__locations = locations
        self.__geojson = geojson
        self.__cmap = cmap
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render via GeoDataFrame.plot (requires a GeoDataFrame)."""
        # Duck-type: any object with a ``plot`` method accepting a ``column``
        # kwarg works (i.e. geopandas.GeoDataFrame).
        if not hasattr(self.__df, "plot"):
            raise TypeError(
                "Seaborn backend requires a GeoDataFrame for ChoroplethMap."
            )
        ax = self.__df.plot(
            column=self.__value,
            cmap=self.__cmap,
            legend=True,
            **self.__kwargs,
        )
        ax.set_axis_off()
        if self._title:
            ax.set_title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.choropleth`."""
        fig = px.choropleth(
            self.__df,
            locations=self.__locations,
            color=self.__value,
            geojson=self.__geojson,
            color_continuous_scale=self.__cmap,
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
