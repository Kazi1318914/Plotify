"""
plotify.categorical.sunburst_diagram
====================================

Sunburst diagram — a radial treemap that shows hierarchical structure.
"""

import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

from plotify.base import BasePlot


class SunburstDiagram(BasePlot):
    """
    Sunburst diagram.

    Seaborn backend draws nested pies; Plotly backend uses
    :func:`plotly.express.sunburst` which has first-class hierarchy support.
    """

    def __init__(
        self,
        df,
        path,
        values,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a sunburst diagram.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        path : list[str]
            Ordered list of column names tracing the hierarchy root → leaf.
        values : str
            Column with numeric values at the leaf level.
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
        if not path:
            raise ValueError("`path` must contain at least one column name.")

        self.__df = df
        self.__path = list(path)
        self.__values = values
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Draw nested ring pies from outer level to inner level."""
        fig, ax = plt.subplots()
        ax.set_aspect("equal")

        # Build a ring per level. Level 0 is the innermost ring.
        # Width of each ring decreases with depth so the leaf ring is the widest.
        n_levels = len(self.__path)
        ring_width = 1.0 / n_levels

        cmap = plt.get_cmap("tab20")

        for level, col in enumerate(self.__path):
            # Aggregate values at this depth.
            level_df = (
                self.__df.groupby(self.__path[: level + 1])[self.__values]
                .sum()
                .reset_index()
            )
            sizes = level_df[self.__values].values
            # A wedge per group; colour by index for now.
            colours = [cmap(i % 20) for i in range(len(sizes))]

            radius = (level + 1) * ring_width
            ax.pie(
                sizes,
                radius=radius,
                colors=colours,
                wedgeprops=dict(width=ring_width, edgecolor="white"),
                labels=level_df[col].astype(str).tolist() if level == n_levels - 1 else None,
                labeldistance=1.05,
                startangle=90,
            )

        # Suppress the default 0..1 axes; the pies speak for themselves.
        ax.set(aspect="equal")
        plt.axis("off")
        if self._title:
            ax.set_title(self._title)

        # Reference np to avoid lint removal warning; used implicitly by mpl internals.
        _ = np.asarray([])

    def _plot_plotly(self):
        """Render using :func:`plotly.express.sunburst`."""
        fig = px.sunburst(
            self.__df,
            path=self.__path,
            values=self.__values,
            title=self._title,
            **self.__kwargs,
        )
        self._fig = fig
