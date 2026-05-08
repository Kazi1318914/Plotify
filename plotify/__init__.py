"""
Plotify
=======

A dual-backend (Seaborn/Matplotlib + Plotly) plotting package.

Top-level convenience imports re-export the plot classes from each
subpackage. For larger applications, prefer importing from the relevant
subpackage directly (e.g. ``from plotify.network import SankeyDiagram``).
"""

__version__ = "0.1.0"

from plotify.categorical import (
    BarPlot,
    CircularPacking,
    Dendrogram,
    DoughnutChart,
    LollipopChart,
    ParallelCoordinates,
    PieChart,
    RadarChart,
    SpiderChart,
    SunburstDiagram,
    Treemap,
    VennDiagram,
    WordCloudPlot,
)
from plotify.maps import (
    BubbleMap,
    Cartogram,
    ChoroplethMap,
    ConnectionMap,
    HexbinMap,
)
from plotify.network import (
    ArcDiagram,
    ChordDiagram,
    HierarchicalEdgeBundling,
    NetworkDiagram,
    SankeyDiagram,
)
from plotify.num_cat import (
    BoxPlotByGroup,
    GroupedBarPlot,
    GroupedScatter,
    StackedBarPlot,
)
from plotify.numerical import (
    Boxplot,
    ConnectedScatterPlot,
    DensityPlot,
    ScatterPlot,
    Violinplot,
)
from plotify.timeseries import (
    AreaChart,
    LineChart,
    StackedAreaChart,
    StreamGraph,
)

__all__ = [
    "__version__",
    # numerical
    "Boxplot",
    "ConnectedScatterPlot",
    "DensityPlot",
    "ScatterPlot",
    "Violinplot",
    # categorical
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
    # num_cat
    "BoxPlotByGroup",
    "GroupedBarPlot",
    "GroupedScatter",
    "StackedBarPlot",
    # timeseries
    "AreaChart",
    "LineChart",
    "StackedAreaChart",
    "StreamGraph",
    # network
    "ArcDiagram",
    "ChordDiagram",
    "HierarchicalEdgeBundling",
    "NetworkDiagram",
    "SankeyDiagram",
    # maps
    "BubbleMap",
    "Cartogram",
    "ChoroplethMap",
    "ConnectionMap",
    "HexbinMap",
]
