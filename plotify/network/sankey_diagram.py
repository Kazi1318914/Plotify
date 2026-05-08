"""
plotify.network.sankey_diagram
==============================

Dual-backend Sankey diagram — a flow diagram where band width encodes
quantity. Plotly's :class:`plotly.graph_objects.Sankey` gives a clean
implementation; the Seaborn backend uses :class:`matplotlib.sankey.Sankey`
for a simpler but readable rendering.
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from matplotlib.sankey import Sankey as MplSankey

from plotify.base import BasePlot


class SankeyDiagram(BasePlot):
    """
    Sankey flow diagram.

    Provide the flows as three parallel lists — ``source``, ``target``, and
    ``value`` — plus ``labels``. ``source`` and ``target`` contain integer
    indices into ``labels``.
    """

    def __init__(
        self,
        source,
        target,
        value,
        labels,
        colors=None,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a Sankey diagram.

        Parameters
        ----------
        source : list[int]
            Index of the source node for each flow.
        target : list[int]
            Index of the target node for each flow.
        value : list[float]
            Magnitude of each flow.
        labels : list[str]
            Node labels; ``source`` and ``target`` index into this list.
        colors : list[str], optional
            Colour per node (Plotly only).
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
        if not (len(source) == len(target) == len(value)):
            raise ValueError("`source`, `target`, and `value` must all have the same length.")

        self.__source = list(source)
        self.__target = list(target)
        self.__value = list(value)
        self.__labels = list(labels)
        self.__colors = colors
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Render using :class:`matplotlib.sankey.Sankey`.

        matplotlib's Sankey is per-diagram rather than per-flow, so we
        approximate the flow structure by adding one box per source/target
        pair. This is a rough rendering — Plotly produces much cleaner output.
        """
        fig, ax = plt.subplots()
        ax.axis("off")
        sankey = MplSankey(ax=ax, scale=0.01, unit=None)

        # Group flows by source so each source becomes one Sankey "block".
        # This is a simplified rendering — matplotlib's Sankey wasn't designed
        # for arbitrary bipartite structure.
        unique_sources = sorted(set(self.__source))
        for src in unique_sources:
            flows = []
            labels_out = []
            for s, t, v in zip(self.__source, self.__target, self.__value):
                if s == src:
                    flows.append(-v)
                    labels_out.append(self.__labels[t])
            # The source itself is an inflow.
            total_out = sum(-f for f in flows)
            flows.insert(0, total_out)
            labels_out.insert(0, self.__labels[src])
            sankey.add(flows=flows, labels=labels_out)

        sankey.finish()
        if self._title:
            ax.set_title(self._title)

    def _plot_plotly(self):
        """Render using :class:`plotly.graph_objects.Sankey`."""
        node_dict = dict(label=self.__labels)
        if self.__colors:
            node_dict["color"] = self.__colors

        fig = go.Figure(
            data=[
                go.Sankey(
                    node=node_dict,
                    link=dict(
                        source=self.__source,
                        target=self.__target,
                        value=self.__value,
                    ),
                )
            ]
        )
        if self._title:
            fig.update_layout(title=self._title)
        self._fig = fig
