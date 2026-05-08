"""
plotify.network.hierarchical_edge_bundling
==========================================

Hierarchical edge bundling — leaves arranged on the circumference of a
circle in hierarchical order; connections between leaves are drawn as
curves that bundle together along the implied tree structure.

Plotly has no native hierarchical-edge-bundling primitive, so only the
Seaborn/Matplotlib backend is implemented. The tree is unused in this
simplified version beyond the leaf ordering.
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

from plotify.base import BasePlot


class HierarchicalEdgeBundling(BasePlot):
    """
    Simplified hierarchical edge bundling.

    Leaves (nodes) are placed on the unit circle. Each connection is drawn
    as a cubic Bezier curve with control points biased towards the circle
    centre, producing the characteristic "bundled" look.
    """

    # Plotly has no native equivalent.
    SUPPORTED_BACKENDS = ("seaborn",)

    def __init__(
        self,
        leaves,
        connections,
        bundle_strength=0.75,
        leaf_color="steelblue",
        edge_color="gray",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a hierarchical edge bundling plot.

        Parameters
        ----------
        leaves : list
            Leaf labels in circular order.
        connections : list[tuple]
            List of ``(source_label, target_label)`` pairs.
        bundle_strength : float, default=0.75
            How strongly to pull Bezier control points towards the centre.
            ``0`` = straight lines; ``1`` = full bundling through the origin.
        leaf_color : str, default="steelblue"
            Leaf marker colour.
        edge_color : str, default="gray"
            Curve colour.
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
        if not 0 <= bundle_strength <= 1:
            raise ValueError("`bundle_strength` must be in [0, 1].")

        self.__leaves = list(leaves)
        self.__connections = list(connections)
        self.__bundle_strength = bundle_strength
        self.__leaf_color = leaf_color
        self.__edge_color = edge_color
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Place leaves on a circle, draw bundled Bezier edges between them."""
        n = len(self.__leaves)
        # Even angular spacing around the circle.
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
        positions = {
            leaf: np.array([np.cos(a), np.sin(a)])
            for leaf, a in zip(self.__leaves, angles)
        }

        fig, ax = plt.subplots()
        ax.set_aspect("equal")
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.axis("off")

        # Each edge is a cubic Bezier whose two control points are the
        # source and target positions scaled toward the origin.
        s = 1 - self.__bundle_strength
        for u, v in self.__connections:
            if u not in positions or v not in positions:
                continue
            p0 = positions[u]
            p3 = positions[v]
            p1 = p0 * s
            p2 = p3 * s
            verts = [tuple(p0), tuple(p1), tuple(p2), tuple(p3)]
            codes = [
                patches.Path.MOVETO,
                patches.Path.CURVE4,
                patches.Path.CURVE4,
                patches.Path.CURVE4,
            ]
            path = patches.Path(verts, codes)
            ax.add_patch(
                patches.PathPatch(
                    path,
                    facecolor="none",
                    edgecolor=self.__edge_color,
                    linewidth=0.8,
                    alpha=0.6,
                )
            )

        # Leaf markers and labels placed just outside the circle.
        for leaf, pos in positions.items():
            ax.plot(pos[0], pos[1], "o", color=self.__leaf_color, markersize=6)
            ax.text(
                pos[0] * 1.1,
                pos[1] * 1.1,
                str(leaf),
                ha="center",
                va="center",
                fontsize=8,
            )

        if self._title:
            ax.set_title(self._title)
