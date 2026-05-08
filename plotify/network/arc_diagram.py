"""
plotify.network.arc_diagram
===========================

Arc diagram — nodes arranged on a horizontal axis, edges drawn as semi-
circular arcs above (or below) the axis.

Plotly has no native arc-diagram primitive, so only the Seaborn/Matplotlib
backend is implemented.
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from plotify.base import BasePlot


class ArcDiagram(BasePlot):
    """
    Arc diagram.

    Accepts either a networkx graph or an edge list.
    """

    # Plotly has no built-in arc diagram.
    SUPPORTED_BACKENDS = ("seaborn",)

    def __init__(
        self,
        graph=None,
        edges=None,
        node_order=None,
        node_color="steelblue",
        edge_color="gray",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create an arc diagram.

        Parameters
        ----------
        graph : networkx.Graph, optional
            Pre-built graph. Mutually exclusive with ``edges``.
        edges : list[tuple], optional
            Edge list — each entry is ``(u, v)``.
        node_order : list, optional
            Explicit left-to-right ordering of nodes along the axis.
        node_color : str, default="steelblue"
            Node marker colour.
        edge_color : str, default="gray"
            Colour of the arcs.
        title : str, optional
            Plot title.
        backend : {"seaborn"}
            Only the Seaborn/Matplotlib backend is supported.
        **kwargs :
            Currently unused.

        Returns
        -------
        None
        """
        if (graph is None) == (edges is None):
            raise ValueError("Provide exactly one of `graph` or `edges`.")

        if graph is None:
            g = nx.Graph()
            g.add_edges_from(edges)
            graph = g

        self.__graph = graph
        self.__node_order = node_order or list(graph.nodes())
        self.__node_color = node_color
        self.__edge_color = edge_color
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Draw nodes along y=0 and edges as semicircular arcs above."""
        order = self.__node_order
        positions = {node: i for i, node in enumerate(order)}

        fig, ax = plt.subplots()
        # Arcs are drawn as matplotlib Arc patches — one per edge.
        max_distance = 1
        for u, v in self.__graph.edges():
            x_u = positions[u]
            x_v = positions[v]
            centre = (x_u + x_v) / 2
            width = abs(x_v - x_u)
            max_distance = max(max_distance, width)
            arc = patches.Arc(
                (centre, 0),
                width=width,
                height=width,
                angle=0,
                theta1=0,
                theta2=180,
                color=self.__edge_color,
                linewidth=1.5,
            )
            ax.add_patch(arc)

        # Plot the node markers on the horizontal axis.
        xs = [positions[n] for n in order]
        ax.scatter(xs, [0] * len(xs), color=self.__node_color, s=80, zorder=3)
        for node, x in positions.items():
            ax.text(x, -0.05 * max_distance, str(node), ha="center", va="top", fontsize=9)

        ax.set_xlim(-1, len(order))
        ax.set_ylim(-0.1 * max_distance, max_distance / 2 + 1)
        ax.set_aspect("equal")
        ax.axis("off")
        if self._title:
            ax.set_title(self._title)

        # Silence unused-import warning: numpy is used implicitly by matplotlib.
        _ = np.asarray([])
