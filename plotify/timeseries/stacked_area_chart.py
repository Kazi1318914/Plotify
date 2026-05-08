"""
plotify.timeseries.stacked_area_chart
=====================================

Dual-backend stacked area chart — multiple series stacked vertically.
"""

import matplotlib.pyplot as plt
import plotly.express as px

from plotify.base import BasePlot


class StackedAreaChart(BasePlot):
    """
    Stacked area chart.

    Accepts data in one of two shapes:

    * **Wide** — pass ``y=[col1, col2, ...]`` so each named column becomes a
      stacked layer.
    * **Long** — pass ``y=<value_col>`` and ``hue=<group_col>``; the data is
      reshaped internally.
    """

    def __init__(
        self,
        df,
        x,
        y,
        hue=None,
        colors=None,
        alpha=0.7,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a stacked area chart.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        x : str
            Column for the x axis.
        y : str or list[str]
            Either one value column (long form — requires ``hue``) or a list
            of column names to stack directly (wide form).
        hue : str, optional
            Group column for long-form input.
        colors : list[str], optional
            Fill colours, one per layer (Seaborn only).
        alpha : float, default=0.7
            Fill transparency (Seaborn only).
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
        if isinstance(y, str) and hue is None:
            raise ValueError("When ``y`` is a single column, ``hue`` is required.")

        self.__df = df
        self.__x = x
        self.__y = y
        self.__hue = hue
        self.__colors = colors
        self.__alpha = alpha
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using :func:`matplotlib.pyplot.stackplot`."""
        if isinstance(self.__y, list):
            # Wide form — stack each named column directly.
            x_vals = self.__df[self.__x]
            layers = [self.__df[c] for c in self.__y]
            labels = self.__y
        else:
            # Long form — pivot to wide for stackplot.
            wide = self.__df.pivot_table(
                index=self.__x, columns=self.__hue, values=self.__y, aggfunc="sum"
            ).fillna(0)
            x_vals = wide.index
            layers = [wide[col] for col in wide.columns]
            labels = list(wide.columns)

        plt.stackplot(
            x_vals,
            *layers,
            labels=labels,
            colors=self.__colors,
            alpha=self.__alpha,
        )
        plt.legend(loc="upper left")
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.area` with stacking enabled."""
        if isinstance(self.__y, list):
            # Wide form — melt to long so px.area can stack.
            long_df = self.__df.melt(
                id_vars=[self.__x], value_vars=self.__y,
                var_name="series", value_name="value",
            )
            fig = px.area(
                long_df,
                x=self.__x,
                y="value",
                color="series",
                title=self._title,
                **self.__kwargs,
            )
        else:
            fig = px.area(
                self.__df,
                x=self.__x,
                y=self.__y,
                color=self.__hue,
                title=self._title,
                **self.__kwargs,
            )
        self._fig = fig
