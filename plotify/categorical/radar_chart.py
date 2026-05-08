"""
plotify.categorical.radar_chart
===============================

Radar (a.k.a. spider) chart — multiple quantitative axes radiating from a
common origin, one per category.
"""

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

from plotify.base import BasePlot


class RadarChart(BasePlot):
    """
    Radar / spider chart.

    Expects each row of ``df`` to represent one "series" (e.g. a person, a
    product) and each column (except ``group_col``) to be one axis of the
    chart.
    """

    def __init__(
        self,
        df,
        categories,
        group_col=None,
        fill=True,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a radar chart.

        Parameters
        ----------
        df : pandas.DataFrame
            Data — one row per series.
        categories : list[str]
            Column names to treat as axes of the radar.
        group_col : str, optional
            Column identifying the series label used in the legend. If
            ``None`` each row is labelled by its index.
        fill : bool, default=True
            If True, fill the polygon area; otherwise only the outline is drawn.
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
        self.__categories = list(categories)
        self.__group_col = group_col
        self.__fill = fill
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render onto a Matplotlib polar axis."""
        # Angles for each axis, closed by repeating the first angle at the end.
        n = len(self.__categories)
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
        angles += angles[:1]

        ax = plt.gcf().add_subplot(111, polar=True)
        for idx, row in self.__df.iterrows():
            values = [row[c] for c in self.__categories]
            values += values[:1]  # close the polygon
            label = row[self.__group_col] if self.__group_col else str(idx)
            ax.plot(angles, values, label=label)
            if self.__fill:
                ax.fill(angles, values, alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(self.__categories)
        ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
        if self._title:
            ax.set_title(self._title)

    def _plot_plotly(self):
        """Render using :class:`plotly.graph_objects.Scatterpolar`."""
        fig = go.Figure()
        for idx, row in self.__df.iterrows():
            values = [row[c] for c in self.__categories]
            values += values[:1]
            theta = self.__categories + self.__categories[:1]
            label = row[self.__group_col] if self.__group_col else str(idx)
            fig.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=theta,
                    fill="toself" if self.__fill else None,
                    name=str(label),
                )
            )
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            title=self._title,
            showlegend=True,
        )
        self._fig = fig


# Spider chart and radar chart are the same plot under different names.
SpiderChart = RadarChart
