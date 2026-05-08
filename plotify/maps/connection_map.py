"""
plotify.maps.connection_map
===========================

Connection map — lines or arcs drawn between geographic points to show
flows or relationships.
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go

from plotify.base import BasePlot


class ConnectionMap(BasePlot):
    """
    Connection map.

    Pass two parallel lists/arrays of points: ``starts`` and ``ends``, each
    containing ``(lon, lat)`` tuples. The Plotly backend renders proper
    geodesic arcs via :class:`plotly.graph_objects.Scattergeo`; the Seaborn
    backend draws straight line segments on a bare lat/lon plane.
    """

    def __init__(
        self,
        starts,
        ends,
        labels=None,
        line_color="darkblue",
        line_width=1.5,
        scope="world",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a connection map.

        Parameters
        ----------
        starts : list[tuple[float, float]]
            Starting ``(lon, lat)`` for each connection.
        ends : list[tuple[float, float]]
            Ending ``(lon, lat)`` for each connection.
        labels : list[str], optional
            Optional labels for each connection (Plotly hover text).
        line_color : str, default="darkblue"
            Line colour.
        line_width : float, default=1.5
            Line width.
        scope : str, default="world"
            Plotly geographic scope.
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
        if len(starts) != len(ends):
            raise ValueError("`starts` and `ends` must have the same length.")

        self.__starts = list(starts)
        self.__ends = list(ends)
        self.__labels = labels
        self.__line_color = line_color
        self.__line_width = line_width
        self.__scope = scope
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Draw straight line segments on a bare (lon, lat) plane."""
        for (lon0, lat0), (lon1, lat1) in zip(self.__starts, self.__ends):
            plt.plot(
                [lon0, lon1],
                [lat0, lat1],
                color=self.__line_color,
                linewidth=self.__line_width,
                alpha=0.6,
            )
            # Endpoint markers help orient the reader.
            plt.scatter([lon0, lon1], [lat0, lat1], color=self.__line_color, s=20)

        plt.xlabel("lon")
        plt.ylabel("lat")
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Draw great-circle arcs with :class:`plotly.graph_objects.Scattergeo`."""
        fig = go.Figure()
        for i, ((lon0, lat0), (lon1, lat1)) in enumerate(
            zip(self.__starts, self.__ends)
        ):
            fig.add_trace(
                go.Scattergeo(
                    lon=[lon0, lon1],
                    lat=[lat0, lat1],
                    mode="lines",
                    line=dict(width=self.__line_width, color=self.__line_color),
                    name=self.__labels[i] if self.__labels else None,
                )
            )
        fig.update_layout(
            geo=dict(scope=self.__scope),
            title=self._title,
            showlegend=bool(self.__labels),
        )
        self._fig = fig
