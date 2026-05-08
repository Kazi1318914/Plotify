"""
plotify.categorical.dendrogram
==============================

Dendrogram — tree diagram produced by hierarchical clustering.
"""

import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff
from scipy.cluster import hierarchy

from plotify.base import BasePlot


class Dendrogram(BasePlot):
    """
    Dendrogram from a numeric matrix.

    Seaborn backend uses :func:`scipy.cluster.hierarchy.linkage` + dendrogram;
    Plotly backend uses :func:`plotly.figure_factory.create_dendrogram`.
    """

    def __init__(
        self,
        df,
        labels=None,
        method="single",
        metric="euclidean",
        orientation="top",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a dendrogram.

        Parameters
        ----------
        df : pandas.DataFrame or array-like
            Observation matrix — rows are observations, columns are features.
        labels : list[str], optional
            Leaf labels, one per row.
        method : str, default="single"
            Linkage method (see :func:`scipy.cluster.hierarchy.linkage`).
        metric : str, default="euclidean"
            Pair-wise distance metric.
        orientation : {"top", "bottom", "left", "right"}, default="top"
            Dendrogram orientation.
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
        self.__method = method
        self.__metric = metric
        self.__orientation = orientation
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using scipy + matplotlib."""
        data = np.asarray(self.__df)
        # linkage expects the condensed distance or the raw matrix.
        Z = hierarchy.linkage(data, method=self.__method, metric=self.__metric)
        hierarchy.dendrogram(
            Z,
            labels=self.__labels,
            orientation=self.__orientation,
            **self.__kwargs,
        )
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render using :func:`plotly.figure_factory.create_dendrogram`."""
        data = np.asarray(self.__df)
        fig = ff.create_dendrogram(
            data,
            labels=self.__labels,
            linkagefun=lambda x: hierarchy.linkage(
                data, method=self.__method, metric=self.__metric
            ),
            orientation=self.__orientation,
        )
        if self._title:
            fig.update_layout(title=self._title)
        self._fig = fig
