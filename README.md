# Plotify

Plotify is a Python plotting package with a **dual backend**: every plot
renders on either Seaborn/Matplotlib (static images) or Plotly (interactive).

The chart catalogue and category split (Numerical, Categoric, Num & Cat,
Time series, Network, Maps) are inspired by
[data-to-viz.com](https://www.data-to-viz.com/).

## Package structure

```
plotify/
├── base.py              # BasePlot — backend dispatch + save
├── numerical/           # Boxplot, DensityPlot, Violinplot, ScatterPlot, ConnectedScatterPlot
├── categorical/         # BarPlot, PieChart, Treemap, Sunburst, Venn, Dendrogram, etc. (12)
├── num_cat/             # GroupedBarPlot, StackedBarPlot, GroupedScatter, BoxPlotByGroup
├── timeseries/          # LineChart, AreaChart, StackedAreaChart, StreamGraph
├── network/             # NetworkDiagram, ChordDiagram, SankeyDiagram, ArcDiagram, HierarchicalEdgeBundling
└── maps/                # ChoroplethMap, BubbleMap, HexbinMap, Cartogram, ConnectionMap
```

## Installation

```bash
poetry install
```

## Usage

```python
import pandas as pd
from plotify.numerical import Boxplot
from plotify.categorical import BarPlot, PieChart
from plotify.timeseries import LineChart
from plotify.network import SankeyDiagram

df = pd.DataFrame({"cat": list("AAABBB"), "val": [1, 2, 3, 4, 5, 6]})

# Seaborn/Matplotlib backend → static image.
Boxplot(df, x="cat", y="val", backend="seaborn").save_plot("box.png")

# Plotly backend → interactive HTML (or static image via kaleido).
BarPlot(df, x="cat", y="val", backend="plotly").save_plot("bar.html")
PieChart(df, names="cat", values="val", backend="plotly").save_plot("pie.html")

# Sankey flow with explicit source/target/value lists.
SankeyDiagram(
    source=[0, 1, 0],
    target=[2, 2, 3],
    value=[8, 4, 2],
    labels=["A", "B", "C", "D"],
    backend="plotly",
).save_plot("sankey.html")
```

Every plot class accepts `backend="seaborn"` (default) or `backend="plotly"`.
A few classes only support one backend — `WordCloudPlot`, `VennDiagram`,
`CircularPacking`, `StreamGraph`, `ChordDiagram`, `ArcDiagram`,
`HierarchicalEdgeBundling`, and `Cartogram` are Seaborn-only because Plotly
has no native equivalent. Requesting an unsupported backend raises a
`ValueError` at construction time.

## Chart catalogue (all implemented)

| Category | Classes |
|---|---|
| Numerical | `Boxplot`, `DensityPlot`, `Violinplot`, `ScatterPlot`, `ConnectedScatterPlot` |
| Categoric | `BarPlot`, `LollipopChart`, `RadarChart`, `ParallelCoordinates`, `WordCloudPlot`, `PieChart`, `DoughnutChart`, `Treemap`, `CircularPacking`, `SunburstDiagram`, `VennDiagram`, `Dendrogram` |
| Num & Cat | `GroupedBarPlot`, `StackedBarPlot`, `GroupedScatter`, `BoxPlotByGroup` |
| Time series | `LineChart`, `AreaChart`, `StackedAreaChart`, `StreamGraph` |
| Network | `NetworkDiagram`, `ChordDiagram`, `SankeyDiagram`, `ArcDiagram`, `HierarchicalEdgeBundling` |
| Maps | `ChoroplethMap`, `BubbleMap`, `HexbinMap`, `Cartogram`, `ConnectionMap` |

## Running tests

```bash
poetry run pytest
```

## Migration note

The previous `numerical.py` at the repo root has been replaced by the
`plotify.numerical` subpackage. Update imports:

```python
# Before
from numerical import Boxplot

# After
from plotify.numerical import Boxplot
```

The existing `test.ipynb` at the repo root still references the old import
and should be updated by hand if you continue to use it.
