"""
plotify.network.sankey_diagram
==============================

Dual-backend Sankey diagram — a flow diagram where band width encodes
quantity.

The Plotly backend uses :class:`plotly.graph_objects.Sankey`. The Seaborn
backend renders a custom layered layout: nodes are placed in columns by
graph depth (BFS from the sources), each node's vertical extent is
proportional to its flow throughput, and flows are drawn as cubic Bezier
ribbons connecting source to target. This is much cleaner than the
output of :class:`matplotlib.sankey.Sankey`, which is built around
per-block flow conservation and produces overlapping shapes for
arbitrary bipartite / multi-stage flows.
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from matplotlib.path import Path

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
        """Render a layered Sankey using matplotlib primitives directly.

        Compute per-node throughput, lay out nodes in columns by graph
        depth, then draw each flow as a cubic-Bezier ribbon whose width
        encodes its value. Avoids :class:`matplotlib.sankey.Sankey`,
        which produces poor output for non-trivial multi-stage flows.
        """
        n = len(self.__labels)

        # ---- Per-node incoming and outgoing throughput totals. -----------
        in_totals = [0.0] * n
        out_totals = [0.0] * n
        for s, t, v in zip(self.__source, self.__target, self.__value):
            out_totals[s] += v
            in_totals[t] += v

        # ---- Assign each node to a column via a longest-path pass. -------
        # Sources (no incoming edges) are level 0. Each downstream node sits
        # at max(predecessor levels) + 1. The fixed-point loop terminates
        # because levels only increase.
        levels: dict[int, int] = {
            i: 0 for i in range(n) if in_totals[i] == 0
        }
        changed = True
        while changed:
            changed = False
            for s, t in zip(self.__source, self.__target):
                if s in levels:
                    candidate = levels[s] + 1
                    if t not in levels or levels[t] < candidate:
                        levels[t] = candidate
                        changed = True
        # Any node still unassigned (cyclic graph) — pin to the last column.
        max_level = max(levels.values(), default=0)
        for i in range(n):
            levels.setdefault(i, max_level + 1)
        max_level = max(levels.values())

        by_level: dict[int, list[int]] = {}
        for i, level in levels.items():
            by_level.setdefault(level, []).append(i)

        # ---- Compute node positions in a [0, 1] x [0, 1] viewport. -------
        # Node height ∝ max(in, out) so every flow has equal width on both
        # ends of the ribbon.
        heights = {i: max(in_totals[i], out_totals[i]) for i in range(n)}
        gap = 0.02
        node_width = 0.025
        positions: dict[int, tuple[float, float, float]] = {}  # node -> (x, y_top, y_bot)
        n_levels = max_level + 1
        for level, nodes in sorted(by_level.items()):
            total = sum(heights[i] for i in nodes)
            usable = 1.0 - gap * max(len(nodes) - 1, 0)
            scale = usable / total if total else 0
            x = level / max(n_levels - 1, 1) if n_levels > 1 else 0.5
            y = 1.0
            for n_id in nodes:
                h = heights[n_id] * scale
                positions[n_id] = (x, y, y - h)
                y -= h + gap

        # ---- Draw. -------------------------------------------------------
        fig, ax = plt.subplots()
        ax.set_xlim(-0.18, 1.18)
        ax.set_ylim(-0.05, 1.08)
        ax.axis("off")

        cmap = plt.get_cmap("tab10")

        # Track running fill offsets so multiple flows out of (or into) a
        # node stack neatly without overlapping.
        out_used = {i: 0.0 for i in range(n)}
        in_used = {i: 0.0 for i in range(n)}

        # Flow ribbons first so node rectangles overlay them.
        for s, t, v in zip(self.__source, self.__target, self.__value):
            xs, y_s_top, y_s_bot = positions[s]
            xt, y_t_top, y_t_bot = positions[t]
            scale_s = (y_s_top - y_s_bot) / out_totals[s] if out_totals[s] else 0
            scale_t = (y_t_top - y_t_bot) / in_totals[t] if in_totals[t] else 0
            v_s = v * scale_s
            v_t = v * scale_t
            s_top = y_s_top - out_used[s]
            s_bot = s_top - v_s
            t_top = y_t_top - in_used[t]
            t_bot = t_top - v_t
            out_used[s] += v_s
            in_used[t] += v_t

            mid_x = (xs + xt) / 2
            x_left = xs + node_width / 2
            x_right = xt - node_width / 2

            # Build a closed path: top edge (left → right) as a Bezier, a
            # straight line down at the right node, bottom edge (right → left)
            # as a Bezier, and a straight line up at the left node.
            verts = [
                (x_left, s_top),
                (mid_x, s_top), (mid_x, t_top), (x_right, t_top),
                (x_right, t_bot),
                (mid_x, t_bot), (mid_x, s_bot), (x_left, s_bot),
                (x_left, s_top),
            ]
            codes = [
                Path.MOVETO,
                Path.CURVE4, Path.CURVE4, Path.CURVE4,
                Path.LINETO,
                Path.CURVE4, Path.CURVE4, Path.CURVE4,
                Path.CLOSEPOLY,
            ]
            ax.add_patch(
                patches.PathPatch(
                    Path(verts, codes),
                    facecolor=cmap(s % 10),
                    alpha=0.35,
                    edgecolor="none",
                )
            )

        # Node rectangles + labels.
        for n_id, (x, y_top, y_bot) in positions.items():
            ax.add_patch(
                patches.Rectangle(
                    (x - node_width / 2, y_bot),
                    node_width,
                    y_top - y_bot,
                    facecolor=cmap(n_id % 10),
                    edgecolor="black",
                    linewidth=0.5,
                )
            )
            label = self.__labels[n_id]
            level = levels[n_id]
            if level == 0:
                ax.text(
                    x - node_width, (y_top + y_bot) / 2, label,
                    ha="right", va="center", fontsize=9,
                )
            elif level == max_level:
                ax.text(
                    x + node_width, (y_top + y_bot) / 2, label,
                    ha="left", va="center", fontsize=9,
                )
            else:
                ax.text(
                    x, y_top + 0.012, label,
                    ha="center", va="bottom", fontsize=8,
                )

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
