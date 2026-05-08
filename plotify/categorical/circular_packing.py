"""
plotify.categorical.circular_packing
====================================

Circular packing — hierarchical data displayed as circles inside circles.
Plotly has no built-in equivalent, so only the Seaborn/Matplotlib backend
is implemented.
"""

import circlify
import matplotlib.pyplot as plt

from plotify.base import BasePlot


class CircularPacking(BasePlot):
    """
    Circular packing chart.

    Uses the :mod:`circlify` library to compute a nested-circle layout and
    Matplotlib to render it.
    """

    # Plotly has no circular-packing primitive; advertise this at class level.
    SUPPORTED_BACKENDS = ("seaborn",)

    def __init__(
        self,
        df,
        labels,
        values,
        show_enclosure=False,
        cmap="tab20",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a circular packing chart.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data — one row per leaf circle.
        labels : str
            Column with circle labels.
        values : str
            Column with numeric sizes.
        show_enclosure : bool, default=False
            Whether to draw the outer bounding circle.
        cmap : str, default="tab20"
            Matplotlib colormap used for per-circle colours.
        title : str, optional
            Plot title.
        backend : {"seaborn"}
            Only the Seaborn/Matplotlib backend is supported.
        **kwargs :
            Forwarded to :func:`circlify.circlify`.

        Returns
        -------
        None
        """
        self.__df = df
        self.__labels = labels
        self.__values = values
        self.__show_enclosure = show_enclosure
        self.__cmap = cmap
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Compute the packing layout and draw it."""
        # circlify packs in descending size order, so sort for stable output.
        sorted_df = self.__df.sort_values(self.__values, ascending=False)

        circles = circlify.circlify(
            sorted_df[self.__values].tolist(),
            show_enclosure=self.__show_enclosure,
            target_enclosure=circlify.Circle(x=0, y=0, r=1),
            **self.__kwargs,
        )

        fig, ax = plt.subplots()
        ax.set_aspect("equal")
        # circlify returns coordinates in [-1, 1] — pad slightly for labels.
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.axis("off")

        cmap = plt.get_cmap(self.__cmap)
        labels = sorted_df[self.__labels].tolist()
        for i, circle in enumerate(circles):
            x, y, r = circle.x, circle.y, circle.r
            ax.add_patch(
                plt.Circle(
                    (x, y), r, alpha=0.6, edgecolor="black", facecolor=cmap(i % 20)
                )
            )
            # Only label circles big enough to read.
            if r > 0.05:
                ax.text(x, y, labels[i], ha="center", va="center", fontsize=8)

        if self._title:
            ax.set_title(self._title)
