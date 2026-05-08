"""
plotify.categorical.treemap
===========================

Treemap — nested rectangles whose areas are proportional to a numeric
variable.
"""

import matplotlib.pyplot as plt
import plotly.express as px
import squarify

from plotify.base import BasePlot


class Treemap(BasePlot):
    """
    Treemap.

    Seaborn backend builds the layout with :mod:`squarify` and renders via
    Matplotlib. Plotly backend uses :func:`plotly.express.treemap`, which
    supports nested hierarchies directly.
    """

    def __init__(
        self,
        df,
        labels,
        values,
        parents=None,
        color=None,
        palette=None,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a treemap.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        labels : str
            Column containing rectangle labels.
        values : str
            Column containing numeric values (drive rectangle area).
        parents : str, optional
            Column with parent-label references for hierarchical treemaps.
            Seaborn backend ignores this (squarify is flat); Plotly backend
            uses it to build the hierarchy.
        color : str, optional
            Column name used to colour-encode rectangles (Plotly only).
        palette : list[str], optional
            Seaborn colours for the rectangles.
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
        self.__labels = labels
        self.__values = values
        self.__parents = parents
        self.__color = color
        self.__palette = palette
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render a flat treemap with :mod:`squarify`."""
        values = self.__df[self.__values].tolist()
        labels = self.__df[self.__labels].tolist()
        squarify.plot(
            sizes=values,
            label=labels,
            color=self.__palette,
            **self.__kwargs,
        )
        plt.axis("off")  # rectangles carry all the information
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.express.treemap`."""
        # px.treemap requires explicit parent column for hierarchy; if the
        # caller did not provide one, treat all labels as top-level.
        parents_col = (
            self.__df[self.__parents].tolist()
            if self.__parents
            else [""] * len(self.__df)
        )
        fig = px.treemap(
            names=self.__df[self.__labels].tolist(),
            parents=parents_col,
            values=self.__df[self.__values].tolist(),
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
