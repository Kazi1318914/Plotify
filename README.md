# Plotify

[![PyPI version](https://img.shields.io/pypi/v/plotify-charts.svg)](https://pypi.org/project/plotify-charts/)
[![Python versions](https://img.shields.io/pypi/pyversions/plotify-charts.svg)](https://pypi.org/project/plotify-charts/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/Kazi1318914/Plotify/actions/workflows/test.yml/badge.svg)](https://github.com/Kazi1318914/Plotify/actions/workflows/test.yml)

Plotify is a Python plotting package built around two ideas:

1. **Auto-pick** — given a dataframe and column names, Plotify infers the
   right chart from the data shape and types. No need to remember which
   function to call.
2. **Publication-ready by default** — every chart ships with a
   colourblind-safe palette, smart tick formatting (1.2K, 3.4M),
   minimalist spines, and consistent typography on both backends.

Every plot can render on either Seaborn/Matplotlib (static images) or
Plotly (interactive HTML).

The chart catalogue and category split (Numerical, Categoric, Num & Cat,
Time series, Network, Maps) are inspired by
[data-to-viz.com](https://www.data-to-viz.com/).

## Demo notebooks

The fastest way to see what Plotify can do — runnable notebooks under
[`notebooks/`](notebooks/) with every chart class rendered on both backends:

- [`00_quickstart.ipynb`](notebooks/00_quickstart.ipynb) — `auto`, `suggest`, themes
- [`01_numerical.ipynb`](notebooks/01_numerical.ipynb) — Boxplot, Density, Violin, Scatter, ConnectedScatter
- [`02_categorical.ipynb`](notebooks/02_categorical.ipynb) — all 12 categoric charts
- [`03_num_cat.ipynb`](notebooks/03_num_cat.ipynb) — GroupedBar, StackedBar, GroupedScatter, BoxPlotByGroup
- [`04_timeseries.ipynb`](notebooks/04_timeseries.ipynb) — Line, Area, StackedArea, StreamGraph
- [`05_network.ipynb`](notebooks/05_network.ipynb) — Network, Chord, Sankey, Arc, HierarchicalEdgeBundling
- [`06_maps.ipynb`](notebooks/06_maps.ipynb) — Choropleth, Bubble, Hexbin, Cartogram, Connection

Outputs are committed, so the notebooks render fully on GitHub without
running them.

## Two-line example

```python
import pandas as pd, plotify

df = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=12, freq="MS"),
    "sales": [120, 140, 90, 200, 220, 260, 240, 310, 280, 330, 360, 410],
    "region": ["North"] * 6 + ["South"] * 6,
})

plotify.auto(df, x="date", y="sales", color="region", backend="plotly")\
       .save_plot("sales.html")
```

`plotify.auto` looks at the dtypes (datetime, numeric, low-cardinality
group), picks `LineChart`, and returns a beautifully themed figure.

## What `auto` actually picks

```python
plotify.suggest(df, x="date", y="sales", color="region")
# → [Suggestion(LineChart,        score=0.96, reason="datetime x + numeric y + low-cardinality group → multi-series line chart"),
#    Suggestion(StackedAreaChart, score=0.72, reason="stacked area variant for compositional time series")]
```

Suggestions come ranked, each with a one-line reason — useful for
debugging or for showing the user *why* a chart was picked.

You can also pass an `intent` to override the rules:

```python
plotify.auto(df, x="region", y="sales", intent="distribution")
# → Violinplot
```

## Themes

`plotify.theme` controls the look of every chart on both backends.

```python
import plotify

plotify.theme.get_current().name      # "publication" — applied automatically
plotify.theme.set("none")             # opt out, use library defaults
plotify.theme.register(plotify.theme.Theme(name="brand", palette=("#FF1493", "#00CED1")))
plotify.theme.set("brand")
```

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
pip install plotify-charts          # PyPI distribution name
pip install plotify-charts[maps]    # adds geopandas for ChoroplethMap's seaborn path
pip install plotify-charts[full]    # all optional extras
```

The Python import name is `plotify` regardless of which install variant
you pick:

```python
import plotify
```

If you've cloned the repo for development, install with Poetry instead:

```bash
poetry install --with dev --extras full
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

## Development

Run the test suite:

```bash
poetry run pytest
```

The notebooks under [`notebooks/`](notebooks/) are **generated** from
[`scripts/build_notebooks.py`](scripts/build_notebooks.py) — please don't
hand-edit them. After changing an API or a chart class, rebuild and
re-execute in a single step:

```bash
python scripts/build_notebooks.py --execute
```

The `--execute` flag runs each notebook via `jupyter nbconvert` so the
rendered outputs are embedded in the committed `.ipynb` files. The script
sets `PYTHONPATH` to the repo root automatically, so it works without
pip-installing the package.

