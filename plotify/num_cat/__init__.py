"""
plotify.num_cat
===============

Plots combining numeric and categorical variables: GroupedBarPlot,
StackedBarPlot, GroupedScatter, BoxPlotByGroup.
"""

from plotify.num_cat.box_plot_by_group import BoxPlotByGroup
from plotify.num_cat.grouped_bar_plot import GroupedBarPlot
from plotify.num_cat.grouped_scatter import GroupedScatter
from plotify.num_cat.stacked_bar_plot import StackedBarPlot

__all__ = [
    "BoxPlotByGroup",
    "GroupedBarPlot",
    "GroupedScatter",
    "StackedBarPlot",
]
