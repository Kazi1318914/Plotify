"""
plotify.categorical.venn_diagram
================================

Venn diagram — overlapping circles showing set intersections. Plotly has no
native Venn support, so only the Matplotlib backend (via
:mod:`matplotlib_venn`) is implemented.
"""

import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3

from plotify.base import BasePlot


class VennDiagram(BasePlot):
    """
    Two- or three-set Venn diagram.

    Pass either two or three sets via ``sets``. Set labels are taken from
    the ``labels`` argument (defaulting to ``("A", "B")`` or
    ``("A", "B", "C")``).
    """

    # matplotlib_venn has no Plotly equivalent.
    SUPPORTED_BACKENDS = ("seaborn",)

    def __init__(
        self,
        sets,
        labels=None,
        colors=None,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a Venn diagram.

        Parameters
        ----------
        sets : list[set]
            List of two or three Python :class:`set` objects.
        labels : list[str], optional
            Labels for the sets. Defaults to letters.
        colors : list[str], optional
            Fill colour per set.
        title : str, optional
            Plot title.
        backend : {"seaborn"}
            Only the Seaborn/Matplotlib backend is supported.
        **kwargs :
            Forwarded to :mod:`matplotlib_venn`.

        Returns
        -------
        None
        """
        if len(sets) not in (2, 3):
            raise ValueError("matplotlib-venn supports only 2-set or 3-set Venn diagrams.")

        self.__sets = [set(s) for s in sets]
        self.__labels = labels
        self.__colors = colors
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Dispatch to ``venn2`` or ``venn3`` based on set count."""
        n = len(self.__sets)
        default_labels = ("A", "B", "C")[:n]
        labels = tuple(self.__labels) if self.__labels else default_labels

        if n == 2:
            venn2(
                subsets=self.__sets,
                set_labels=labels,
                set_colors=self.__colors or ("red", "blue"),
                **self.__kwargs,
            )
        else:
            venn3(
                subsets=self.__sets,
                set_labels=labels,
                set_colors=self.__colors or ("red", "blue", "green"),
                **self.__kwargs,
            )

        if self._title:
            plt.title(self._title)
