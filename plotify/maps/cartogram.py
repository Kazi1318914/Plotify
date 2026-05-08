"""
plotify.maps.cartogram
======================

Cartogram — geographic regions distorted in size to encode a numeric
variable. Building a "true" continuous-area cartogram is non-trivial; this
class implements the simpler **Dorling cartogram** variant where each
region is replaced by a circle whose area is proportional to the value,
positioned at the region centroid.

Plotly has no native cartogram primitive, so only the Seaborn/Matplotlib
backend is implemented.
"""

import matplotlib.pyplot as plt
import numpy as np

from plotify.base import BasePlot


class Cartogram(BasePlot):
    """
    Dorling-style cartogram.

    Pass a list of ``(label, lon, lat, value)`` tuples or a dataframe with
    those four columns. Circle areas are scaled so that the largest value
    fits within ``max_radius``.
    """

    # No native Plotly cartogram primitive.
    SUPPORTED_BACKENDS = ("seaborn",)

    def __init__(
        self,
        df,
        label,
        lon,
        lat,
        value,
        max_radius=10.0,
        cmap="tab20",
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a Dorling cartogram.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data.
        label : str
            Column with region labels.
        lon, lat : str
            Centroid longitude / latitude column names.
        value : str
            Numeric column driving circle size.
        max_radius : float, default=10.0
            Radius (in lon/lat units) of the circle representing the
            maximum value.
        cmap : str, default="tab20"
            Colormap used for per-region colours.
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
        self.__df = df
        self.__label = label
        self.__lon = lon
        self.__lat = lat
        self.__value = value
        self.__max_radius = max_radius
        self.__cmap = cmap
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Draw one matplotlib Circle per region, sized by ``value``."""
        values = self.__df[self.__value].astype(float).values
        max_val = values.max() or 1.0
        # Area-proportional radius — sqrt keeps perceived area linear in value.
        radii = self.__max_radius * np.sqrt(values / max_val)

        cmap = plt.get_cmap(self.__cmap)
        fig, ax = plt.subplots()
        ax.set_aspect("equal")

        for i, (_, row) in enumerate(self.__df.iterrows()):
            x = row[self.__lon]
            y = row[self.__lat]
            r = radii[i]
            # Use facecolor explicitly so it does not clash with edgecolor.
            ax.add_patch(
                plt.Circle(
                    (x, y),
                    r,
                    facecolor=cmap(i % 20),
                    alpha=0.7,
                    edgecolor="black",
                )
            )
            ax.text(x, y, str(row[self.__label]), ha="center", va="center", fontsize=8)

        # Auto-scale the axis to fit all bubbles.
        ax.set_xlim(
            self.__df[self.__lon].min() - self.__max_radius,
            self.__df[self.__lon].max() + self.__max_radius,
        )
        ax.set_ylim(
            self.__df[self.__lat].min() - self.__max_radius,
            self.__df[self.__lat].max() + self.__max_radius,
        )
        ax.set_xlabel("lon")
        ax.set_ylabel("lat")
        if self._title:
            ax.set_title(self._title)
