"""
plotify.categorical
===================

Plots for categorical data: BarPlot, LollipopChart, RadarChart (alias
SpiderChart), ParallelCoordinates, WordCloudPlot, PieChart, DoughnutChart,
Treemap, CircularPacking, SunburstDiagram, VennDiagram, Dendrogram.
"""

from plotify.categorical.bar_plot import BarPlot
from plotify.categorical.circular_packing import CircularPacking
from plotify.categorical.dendrogram import Dendrogram
from plotify.categorical.doughnut_chart import DoughnutChart
from plotify.categorical.lollipop_chart import LollipopChart
from plotify.categorical.parallel_coordinates import ParallelCoordinates
from plotify.categorical.pie_chart import PieChart
from plotify.categorical.radar_chart import RadarChart, SpiderChart
from plotify.categorical.sunburst_diagram import SunburstDiagram
from plotify.categorical.treemap import Treemap
from plotify.categorical.venn_diagram import VennDiagram
from plotify.categorical.word_cloud import WordCloudPlot

__all__ = [
    "BarPlot",
    "CircularPacking",
    "Dendrogram",
    "DoughnutChart",
    "LollipopChart",
    "ParallelCoordinates",
    "PieChart",
    "RadarChart",
    "SpiderChart",
    "SunburstDiagram",
    "Treemap",
    "VennDiagram",
    "WordCloudPlot",
]
