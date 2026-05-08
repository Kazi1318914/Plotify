"""
plotify.numerical
=================

Plots for purely numeric variables: Boxplot, DensityPlot, Violinplot,
ScatterPlot, ConnectedScatterPlot.
"""

from plotify.numerical.boxplot import Boxplot
from plotify.numerical.connected_scatter_plot import ConnectedScatterPlot
from plotify.numerical.density_plot import DensityPlot
from plotify.numerical.scatter_plot import ScatterPlot
from plotify.numerical.violin_plot import Violinplot

__all__ = [
    "Boxplot",
    "ConnectedScatterPlot",
    "DensityPlot",
    "ScatterPlot",
    "Violinplot",
]
