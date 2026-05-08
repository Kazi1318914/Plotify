"""
plotify.network.network_diagram
===============================

Dual-backend generic network / graph visualization using :mod:`networkx`
for the layout.
"""

import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go

from plotify.base import BasePlot


class NetworkDiagram(BasePlot):
    """
    Generic node-link network diagram.

    Accepts either a :class:`networkx.Graph` directly or an edge list
    (list of ``(u, v)`` or ``(u, v, weight)`` tuples).
    """

    def __init__(
        self,
        graph=None,
        edges=None,
        layout="spring",
        node_color="steelblue",
        node_size=300,
        edge_color="gray",
        with_labels=True,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a network diagram.

        Parameters
        ----------
        graph : networkx.Graph, optional
            Pre-built graph. Mutually exclusive with ``edges``.
        edges : list[tuple], optional
            Edge list. Each entry is ``(u, v)`` or ``(u, v, weight)``.
        layout : {"spring", "circular", "kamada_kawai", "random", "shell"}, default="spring"
            Node-placement algorithm.
        node_color : str, default="steelblue"
            Node colour.
        node_size : int, default=300
            Node size (matplotlib units).
        edge_color : str, default="gray"
            Edge colour.
        with_labels : bool, default=True
            Draw node labels.
        title : str, optional
            Plot title.
        backend : {"seaborn", "plotly"}, default="seaborn"
            Rendering backend.
        **kwargs :
            Forwarded to :func:`networkx.draw` (Seaborn backend only).

        Returns
        -------
        None
        """
        if (graph is None) == (edges is None):
            raise ValueError("Provide exactly one of `graph` or `edges`.")

        # Normalise to a networkx graph so both render paths are the same.
        if graph is None:
            g = nx.Graph()
            for edge in edges:
                if len(edge) == 2:
                    g.add_edge(edge[0], edge[1])
                elif len(edge) == 3:
                    g.add_edge(edge[0], edge[1], weight=edge[2])
            graph = g

        self.__graph = graph
        self.__layout = layout
        self.__node_color = node_color
        self.__node_size = node_size
        self.__edge_color = edge_color
        self.__with_labels = with_labels
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _compute_positions(self):
        """Map the ``layout`` name to the corresponding networkx function."""
        layouts = {
            "spring": nx.spring_layout,
            "circular": nx.circular_layout,
            "kamada_kawai": nx.kamada_kawai_layout,
            "random": nx.random_layout,
            "shell": nx.shell_layout,
        }
        if self.__layout not in layouts:
            raise ValueError(
                f"Unknown layout {self.__layout!r}. Choose from {list(layouts)}."
            )
        return layouts[self.__layout](self.__graph)

    def _plot_seaborn(self):
        """Render using :func:`networkx.draw`."""
        pos = self._compute_positions()
        nx.draw(
            self.__graph,
            pos=pos,
            node_color=self.__node_color,
            node_size=self.__node_size,
            edge_color=self.__edge_color,
            with_labels=self.__with_labels,
            **self.__kwargs,
        )
        if self._title:
            plt.title(self._title)

    def _plot_plotly(self):
        """Render with Plotly by building edge + node scatter traces."""
        pos = self._compute_positions()

        # One edge trace: all edges drawn as a single scatter with None
        # separators so we only issue a single add_trace for all edges.
        edge_x, edge_y = [], []
        for u, v in self.__graph.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1, color=self.__edge_color),
            hoverinfo="none",
            mode="lines",
        )

        # Node trace carries labels via text / hovertext.
        node_x, node_y, node_text = [], [], []
        for node in self.__graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(str(node))

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text" if self.__with_labels else "markers",
            text=node_text,
            textposition="top center",
            marker=dict(size=12, color=self.__node_color),
            hoverinfo="text",
        )

        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            title=self._title,
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
        )
        self._fig = fig
