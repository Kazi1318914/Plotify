"""
plotify.num_cat.stacked_bar_plot
================================

Stacked bar plot — bars subdivided by a second categorical variable.
"""

import matplotlib.pyplot as plt
import plotly.express as px

from plotify.base import BasePlot


class StackedBarPlot(BasePlot):
    """
    Stacked bar plot.

    On the Seaborn backend this is drawn by pivoting the dataframe to wide
    form and calling :meth:`pandas.DataFrame.plot.bar` with ``stacked=True``.
    On the Plotly backend, :func:`plotly.express.bar` with
    ``barmode='stack'`` handles it directly.
    """

    def __init__(
        self,
        df,
        x,
        y,
        hue,
        normalize=False,
        palette=None,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a stacked bar plot.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        x : str
            Primary categorical column (one stack per value).
        y : str
            Numeric value column.
        hue : str
            Sub-group column — each value becomes one segment of each stack.
        normalize : bool, default=False
            If True, scale each stack to sum to 1 (100% stacked bar).
        palette : str or list, optional
            Colour palette.
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
        self.__x = x
        self.__y = y
        self.__hue = hue
        self.__normalize = normalize
        self.__palette = palette
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Pivot and use pandas' stacked bar plotting."""
        # Aggregate to wide form — one column per hue level.
        wide = (
            self.__df.pivot_table(
                index=self.__x,
                columns=self.__hue,
                values=self.__y,
                aggfunc="sum",
            )
            .fillna(0)
        )
        if self.__normalize:
            wide = wide.div(wide.sum(axis=1), axis=0)

        # pandas .plot.bar wraps matplotlib and cleanly supports stacked bars.
        ax = wide.plot.bar(
            stacked=True,
            color=self.__palette,
            **self.__kwargs,
        )
        ax.set_ylabel(self.__y)
        if self._title:
            ax.set_title(self._title)

    def _plot_plotly(self):
        """Render with :func:`plotly.express.bar` using ``barmode='stack'``."""
        data = self.__df.copy()
        if self.__normalize:
            # Compute per-x totals, divide each row by its total.
            totals = data.groupby(self.__x)[self.__y].transform("sum")
            data[self.__y] = data[self.__y] / totals

        fig = px.bar(
            data,
            x=self.__x,
            y=self.__y,
            color=self.__hue,
            barmode="stack",
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
