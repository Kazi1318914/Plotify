"""
plotify.network.chord_diagram
=============================

Chord diagram — nodes arranged on a circle, with chords representing flows
between them. Plotly has no native chord primitive, so only the
Seaborn/Matplotlib backend is implemented.
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

from plotify.base import BasePlot


class ChordDiagram(BasePlot):
    """
    Chord diagram from a symmetric connection matrix.

    The input is a square (N × N) matrix where cell ``(i, j)`` is the
    strength of the connection between node ``i`` and node ``j``.
    """

    # Plotly has no native chord primitive.
    SUPPORTED_BACKENDS = ("seaborn",)

    def __init__(
        self,
        matrix,
        labels=None,
        colors=None,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a chord diagram.

        Parameters
        ----------
        matrix : 2D array-like
            Square symmetric matrix of connection strengths.
        labels : list[str], optional
            Node labels. Defaults to ``"0", "1", ...``.
        colors : list[str], optional
            Colour per node.
        title : str, optional
            Plot title.
        backend : {"seaborn"}
            Only the Seaborn/Matplotlib backend is supported.
        **kwargs :
            Currently unused — accepted for forward compatibility.

        Returns
        -------
        None
        """
        mat = np.asarray(matrix, dtype=float)
        if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
            raise ValueError("`matrix` must be a square 2D array.")

        self.__matrix = mat
        self.__labels = labels or [str(i) for i in range(mat.shape[0])]
        self.__colors = colors
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Draw nodes on a circle and chords as quadratic Bezier curves."""
        n = self.__matrix.shape[0]
        # Evenly spaced node angles around the unit circle.
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
        positions = np.column_stack([np.cos(angles), np.sin(angles)])

        cmap = plt.get_cmap("tab10")
        node_colors = self.__colors or [cmap(i % 10) for i in range(n)]

        fig, ax = plt.subplots()
        ax.set_aspect("equal")
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.axis("off")

        # Chords: for each unordered pair (i<j) with non-zero strength, draw
        # a Bezier curve whose control point is the origin.
        max_strength = self.__matrix.max() or 1.0
        for i in range(n):
            for j in range(i + 1, n):
                strength = self.__matrix[i, j]
                if strength == 0:
                    continue
                path_data = [
                    (patches.Path.MOVETO, positions[i]),
                    (patches.Path.CURVE3, (0, 0)),
                    (patches.Path.CURVE3, positions[j]),
                ]
                codes, verts = zip(*path_data)
                path = patches.Path(verts, codes)
                patch = patches.PathPatch(
                    path,
                    facecolor="none",
                    edgecolor=node_colors[i],
                    linewidth=1 + 4 * strength / max_strength,
                    alpha=0.6,
                )
                ax.add_patch(patch)

        # Node markers + labels.
        for i, (x, y) in enumerate(positions):
            ax.plot(x, y, "o", color=node_colors[i], markersize=10)
            # Offset label outwards from the node.
            lx, ly = 1.12 * x, 1.12 * y
            ax.text(lx, ly, self.__labels[i], ha="center", va="center", fontsize=9)

        if self._title:
            ax.set_title(self._title)
