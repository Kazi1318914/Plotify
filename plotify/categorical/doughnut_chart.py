"""
plotify.categorical.doughnut_chart
==================================

Doughnut chart — a pie with a hole.
"""

import matplotlib.pyplot as plt
import plotly.express as px

from plotify.base import BasePlot


class DoughnutChart(BasePlot):
    """
    Doughnut chart.

    Seaborn backend uses :func:`matplotlib.pyplot.pie` with ``wedgeprops`` to
    carve out the centre; Plotly backend uses :func:`plotly.express.pie`
    with ``hole=``.
    """

    def __init__(
        self,
        df,
        names,
        values,
        hole=0.4,
        colors=None,
        startangle=90,
        autopct="%1.1f%%",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a doughnut chart.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        names : str
            Column with slice labels.
        values : str
            Column with slice values.
        hole : float, default=0.4
            Fraction of the radius to cut out of the centre (0 → full pie,
            1 → no chart at all). Applied in both backends.
        colors : list[str], optional
            Colour for each slice (Seaborn only).
        startangle : float, default=90
            Start angle of the first slice (Seaborn only).
        autopct : str, default="%1.1f%%"
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
        if not 0 <= hole < 1:
            raise ValueError("`hole` must be in [0, 1).")

        self.__df = df
        self.__names = names
        self.__values = values
        self.__hole = hole
        self.__colors = colors
        self.__startangle = startangle
        self.__autopct = autopct
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render the doughnut using matplotlib's pie + wedgeprops trick."""
        plt.pie(
            self.__df[self.__values],
            labels=self.__df[self.__names],
            colors=self.__colors,
            startangle=self.__startangle,
            autopct=self.__autopct,
            # The wedge-width trick: drawing each wedge with a finite inner
            # radius creates the characteristic doughnut hole.
            wedgeprops=dict(width=1 - self.__hole),
            **self.__kwargs,
        )
        plt.axis("equal")
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.pie` with ``hole`` set."""
        fig = px.pie(
            self.__df,
            names=self.__names,
            values=self.__values,
            hole=self.__hole,
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
