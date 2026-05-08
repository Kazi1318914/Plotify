"""
plotify.timeseries.stream_graph
===============================

Stream graph — a stacked area variant where layers flow around a central
baseline, producing the characteristic "ribbon" appearance.

Plotly has no native streamgraph primitive, so only the Seaborn/Matplotlib
backend is implemented.
"""

import matplotlib.pyplot as plt

from plotify.base import BasePlot


class StreamGraph(BasePlot):
    """
    Stream graph.

    Uses :func:`matplotlib.pyplot.stackplot` with ``baseline='wiggle'`` to
    produce the signature symmetric flow.
    """

    # Plotly has no native streamgraph.
    SUPPORTED_BACKENDS = ("seaborn",)

    def __init__(
        self,
        df,
        x,
        y,
        hue=None,
        colors=None,
        alpha=0.9,
        baseline="wiggle",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a stream graph.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        x : str
            Column for the x axis (typically time).
        y : str or list[str]
            Either one value column (long form — requires ``hue``) or a list
            of column names to stack directly (wide form).
        hue : str, optional
            Group column for long-form input.
        colors : list[str], optional
            Colour per layer.
        alpha : float, default=0.9
            Fill transparency.
        baseline : {"wiggle", "sym", "zero", "weighted_wiggle"}, default="wiggle"
            Stackplot baseline algorithm; ``"wiggle"`` gives the canonical
            stream shape.
        title : str, optional
            Plot title.
        backend : {"seaborn"}
            Only the Seaborn/Matplotlib backend is supported.
        **kwargs :
            Forwarded to :func:`matplotlib.pyplot.stackplot`.

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
        self.__baseline = baseline
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Stack the series with a wiggled baseline."""
        if isinstance(self.__y, list):
            x_vals = self.__df[self.__x]
            layers = [self.__df[c] for c in self.__y]
            labels = self.__y
        else:
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
            baseline=self.__baseline,
            **self.__kwargs,
        )
        # Stream graphs do not usually show a y-axis — the relative widths
        # carry the information, absolute values do not.
        plt.gca().set_yticks([])
        plt.legend(loc="upper left")
        if self._title:
            plt.title(self._title)
