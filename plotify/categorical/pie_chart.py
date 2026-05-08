"""
plotify.categorical.pie_chart
=============================

Pie chart.
"""

import matplotlib.pyplot as plt
import plotly.express as px

from plotify.base import BasePlot


class PieChart(BasePlot):
    """
    Pie chart.

    Wraps :func:`matplotlib.pyplot.pie` on the Seaborn backend and
    :func:`plotly.express.pie` on the Plotly backend.
    """

    def __init__(
        self,
        df,
        names,
        values,
        colors=None,
        explode=None,
        startangle=90,
        autopct="%1.1f%%",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a pie chart.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        names : str
            Column containing slice labels.
        values : str
            Column containing slice values.
        colors : list[str], optional
            Colour for each slice (Seaborn only).
        explode : list[float], optional
            Fraction by which to offset each slice (Seaborn only).
        startangle : float, default=90
            Start angle for the first slice (Seaborn only).
        autopct : str or callable, default="%1.1f%%"
            Value-label format (Seaborn only).
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
        self.__names = names
        self.__values = values
        self.__colors = colors
        self.__explode = explode
        self.__startangle = startangle
        self.__autopct = autopct
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using :func:`matplotlib.pyplot.pie`."""
        plt.pie(
            self.__df[self.__values],
            labels=self.__df[self.__names],
            colors=self.__colors,
            explode=self.__explode,
            startangle=self.__startangle,
            autopct=self.__autopct,
            **self.__kwargs,
        )
        plt.axis("equal")  # ensures the pie is a circle, not an ellipse
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.pie`."""
        fig = px.pie(
            self.__df,
            names=self.__names,
            values=self.__values,
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
