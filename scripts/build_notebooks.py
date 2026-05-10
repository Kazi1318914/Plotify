"""
Build the demo notebooks under ``notebooks/``.

Run from the repo root::

    # Build cleanly (no rendered outputs)
    python scripts/build_notebooks.py

    # Build AND execute so rendered outputs are embedded — recommended
    # whenever the API or demo data has changed
    python scripts/build_notebooks.py --execute

Each notebook is generated from a list of (kind, source) pairs; the helpers
below wrap nbformat so the per-notebook builders read like prose.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

import nbformat as nbf

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"


# ----------------------------- helpers ----------------------------------
def md(source: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(source.strip("\n"))


def code(source: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(source.strip("\n"))


def build(name: str, cells: list[nbf.NotebookNode]) -> None:
    """Assemble ``cells`` into a notebook and write it to disk."""
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python"},
    }
    NOTEBOOKS_DIR.mkdir(exist_ok=True)
    path = NOTEBOOKS_DIR / name
    nbf.write(nb, path)
    print(f"wrote {path.relative_to(NOTEBOOKS_DIR.parent)}")


# ----------------------------- common setup -----------------------------
COMMON_IMPORTS = """
import numpy as np
import pandas as pd

# Plotly inline rendering for notebook viewers.
import plotly.io as pio
pio.renderers.default = "notebook"
"""


# ----------------------------- 00 quickstart ----------------------------
def quickstart() -> None:
    cells = [
        md(
            """
# Plotify — quickstart

This notebook is a five-minute tour of Plotify's headline features:

1. **`plotify.auto`** — give it a dataframe and column names; it picks the
   right chart from the inferred data shape.
2. **`plotify.suggest`** — same inference, but returns a *ranked list* of
   suggestions with one-line reasons.
3. **`plotify.theme`** — every chart ships with a colourblind-safe,
   publication-ready theme on both backends.

Each per-category notebook (`01_numerical.ipynb`, `02_categorical.ipynb`,
…) walks through the chart classes themselves.
"""
        ),
        code(COMMON_IMPORTS + "\nimport plotify\nplotify.__version__"),
        md("## A small mixed dataframe\n\nDates, a numeric value, and a low-cardinality group — the most common shape in business data."),
        code(
            """
rng = np.random.default_rng(42)
dates = pd.date_range("2024-01-01", periods=12, freq="MS")
df = pd.DataFrame({
    "date": np.tile(dates, 3),
    "region": np.repeat(["North", "South", "West"], len(dates)),
    "sales": np.concatenate([
        rng.integers(120, 320, size=len(dates)),
        rng.integers(80, 220, size=len(dates)),
        rng.integers(160, 380, size=len(dates)),
    ]),
})
df.head()
"""
        ),
        md("## `suggest` — what would Plotify pick, and why?"),
        code(
            """
for s in plotify.suggest(df, x="date", y="sales", color="region"):
    print(f"{s.score:.2f}  {s.chart_class.__name__:<20}  {s.reason}")
"""
        ),
        md("## `auto` — one line to a beautiful chart\n\n`plotify.auto` runs the picker and instantiates the top match."),
        code('plot = plotify.auto(df, x="date", y="sales", color="region", backend="plotly")\nplot.fig'),
        md("Same call, Seaborn backend:"),
        code('plotify.auto(df, x="date", y="sales", color="region", backend="seaborn")\nNone'),
        md("## Intent override\n\nWhen the data shape is ambiguous, pass `intent=` to nudge the picker."),
        code(
            """
distribution_df = pd.DataFrame({
    "team": np.repeat(["A", "B", "C"], 30),
    "score": np.concatenate([
        rng.normal(70, 8, 30),
        rng.normal(75, 5, 30),
        rng.normal(72, 12, 30),
    ]),
})
plotify.auto(distribution_df, x="team", y="score", intent="distribution", backend="plotly").fig
"""
        ),
        md(
            """
## Themes — beautiful by default

Every Plotify plot is automatically themed. The default `"publication"`
theme uses the Okabe-Ito colourblind-safe palette, smart tick formatting
(1.2K / 3.4M / 5B), minimalist spines, and consistent typography on both
backends.

Switch to `"none"` to opt out and get matplotlib/Plotly defaults:
"""
        ),
        code(
            """
plotify.theme.set("none")
plotify.auto(df, x="date", y="sales", color="region", backend="seaborn")
plotify.theme.set("publication")  # restore the default
None
"""
        ),
        md("### Custom themes\n\nRegister your own `Theme` and `set` it by name:"),
        code(
            """
plotify.theme.register(plotify.theme.Theme(
    name="brand",
    palette=("#FF1493", "#00CED1", "#FFD700"),
    background="#FAFAFA",
))
plotify.theme.set("brand")
plotify.auto(df, x="date", y="sales", color="region", backend="plotly").fig
"""
        ),
        code('plotify.theme.set("publication")  # restore default for the rest of the notebook'),
        md(
            """
## Where to next

Each subpackage has its own notebook with every chart class shown on both
backends:

- `01_numerical.ipynb` — Boxplot, DensityPlot, Violinplot, Scatter, ConnectedScatter
- `02_categorical.ipynb` — Bar, Lollipop, Radar/Spider, Parallel coords, WordCloud, Pie, Doughnut, Treemap, Circular packing, Sunburst, Venn, Dendrogram
- `03_num_cat.ipynb` — GroupedBar, StackedBar, GroupedScatter, BoxPlotByGroup
- `04_timeseries.ipynb` — Line, Area, StackedArea, StreamGraph
- `05_network.ipynb` — Network, Chord, Sankey, Arc, HierarchicalEdgeBundling
- `06_maps.ipynb` — Choropleth, Bubble, Hexbin, Cartogram, Connection
"""
        ),
    ]
    build("00_quickstart.ipynb", cells)


# ----------------------------- helpers for chart sections ---------------
def chart_section(
    title: str,
    description: str,
    seaborn_code: str | None,
    plotly_code: str | None,
) -> list[nbf.NotebookNode]:
    """Build a chart demo: header + description + one cell per supported backend."""
    section: list[nbf.NotebookNode] = [md(f"## {title}\n\n{description}")]
    if seaborn_code is not None:
        section.append(md("**Seaborn backend**"))
        section.append(code(seaborn_code))
    if plotly_code is not None:
        section.append(md("**Plotly backend**"))
        section.append(code(plotly_code))
    return section


# ----------------------------- 01 numerical -----------------------------
def numerical() -> None:
    setup = code(
        COMMON_IMPORTS
        + """
from plotify.numerical import (
    Boxplot,
    DensityPlot,
    Violinplot,
    ScatterPlot,
    ConnectedScatterPlot,
)

rng = np.random.default_rng(0)
df = pd.DataFrame({
    "group": np.repeat(["A", "B", "C"], 50),
    "x": rng.normal(size=150),
    "y": rng.normal(loc=2, scale=1.5, size=150),
})
df.head()
"""
    )

    cells = [
        md(
            """
# Numerical plots

Charts for purely numeric variables. Five classes, all dual-backend.
"""
        ),
        setup,
        *chart_section(
            "Boxplot",
            "Summarises a distribution by quartiles, median, and whisker reach.",
            'Boxplot(df, x="group", y="x")\nNone',
            'Boxplot(df, x="group", y="x", backend="plotly").fig',
        ),
        *chart_section(
            "DensityPlot",
            "Kernel density estimate of one (or two) numeric variable(s).",
            'DensityPlot(df, x="x", hue="group", fill=True)\nNone',
            'DensityPlot(df, x="x", hue="group", backend="plotly").fig',
        ),
        *chart_section(
            "Violinplot",
            "A KDE mirrored around a central axis with an inner box.",
            'Violinplot(df, x="group", y="x")\nNone',
            'Violinplot(df, x="group", y="x", backend="plotly").fig',
        ),
        *chart_section(
            "ScatterPlot",
            "Two numeric columns. `style='reg'` overlays a regression line.",
            'ScatterPlot(df, x="x", y="y", style="reg")\nNone',
            'ScatterPlot(df, x="x", y="y", style="reg", backend="plotly").fig',
        ),
        *chart_section(
            "ConnectedScatterPlot",
            "Scatter where points are joined by line segments — useful for trajectories.",
            'small = df.sort_values("x").head(20).reset_index(drop=True)\nConnectedScatterPlot(small, x="x", y="y")\nNone',
            'small = df.sort_values("x").head(20).reset_index(drop=True)\nConnectedScatterPlot(small, x="x", y="y", backend="plotly").fig',
        ),
    ]
    build("01_numerical.ipynb", cells)


# ----------------------------- 02 categorical ---------------------------
def categorical() -> None:
    setup = code(
        COMMON_IMPORTS
        + """
from plotify.categorical import (
    BarPlot, LollipopChart, RadarChart, SpiderChart, ParallelCoordinates,
    WordCloudPlot, PieChart, DoughnutChart, Treemap, CircularPacking,
    SunburstDiagram, VennDiagram, Dendrogram,
)

# A simple (category, value) frame for bar/pie/lollipop/treemap.
cat_df = pd.DataFrame({"product": ["Widgets", "Gadgets", "Gizmos", "Doohickeys"],
                       "revenue": [42, 31, 28, 19]})

# Hierarchical data for sunburst / nested treemaps.
hier_df = pd.DataFrame({
    "region": ["EMEA", "EMEA", "AMER", "AMER", "APAC", "APAC"],
    "country": ["UK", "DE", "US", "BR", "JP", "AU"],
    "sales": [50, 40, 80, 25, 60, 30],
})

# Multivariate data for radar / parallel-coordinates / dendrogram.
rng = np.random.default_rng(2)
multi_df = pd.DataFrame(rng.normal(size=(8, 4)), columns=list("WXYZ"))
multi_df["class"] = np.repeat([0, 1], 4)

cat_df
"""
    )

    cells = [
        md(
            """
# Categoric plots

All twelve categoric chart types.

Single-backend classes (Plotly has no native equivalent): `WordCloudPlot`,
`CircularPacking`, `VennDiagram`. Each section shows a Plotly cell only
when both backends are supported.
"""
        ),
        setup,
        *chart_section(
            "BarPlot",
            "The workhorse — bar length encodes a numeric value per category.",
            'BarPlot(cat_df, x="product", y="revenue")\nNone',
            'BarPlot(cat_df, x="product", y="revenue", backend="plotly").fig',
        ),
        *chart_section(
            "LollipopChart",
            "A lighter alternative to bars when bars feel visually heavy.",
            'LollipopChart(cat_df, x="product", y="revenue")\nNone',
            'LollipopChart(cat_df, x="product", y="revenue", backend="plotly").fig',
        ),
        *chart_section(
            "RadarChart (alias: SpiderChart)",
            "Multiple quantitative axes radiating from the origin. Good for comparing a few entities across many dimensions.",
            'radar = pd.DataFrame({"player": ["Alice", "Bob"], "STR": [7, 5], "SPD": [6, 8], "STA": [5, 7], "AGI": [8, 6]})\nRadarChart(radar, categories=["STR", "SPD", "STA", "AGI"], group_col="player")\nNone',
            'radar = pd.DataFrame({"player": ["Alice", "Bob"], "STR": [7, 5], "SPD": [6, 8], "STA": [5, 7], "AGI": [8, 6]})\nSpiderChart(radar, categories=["STR", "SPD", "STA", "AGI"], group_col="player", backend="plotly").fig',
        ),
        *chart_section(
            "ParallelCoordinates",
            "One vertical axis per variable, one polyline per observation. Good for clustering at a glance.",
            'ParallelCoordinates(multi_df, class_column="class")\nNone',
            'ParallelCoordinates(multi_df, class_column="class", backend="plotly").fig',
        ),
        *chart_section(
            "WordCloudPlot (Seaborn-only)",
            "Word size encodes frequency. Plotly has no native equivalent.",
            'WordCloudPlot(text="plotify is a python plotting library plotify auto suggests beautiful charts")\nNone',
            None,
        ),
        *chart_section(
            "PieChart",
            "Proportional slices. Use sparingly — humans read angles poorly. A bar chart is almost always clearer.",
            'PieChart(cat_df, names="product", values="revenue")\nNone',
            'PieChart(cat_df, names="product", values="revenue", backend="plotly").fig',
        ),
        *chart_section(
            "DoughnutChart",
            "A pie with the centre carved out — often easier to read than a true pie.",
            'DoughnutChart(cat_df, names="product", values="revenue")\nNone',
            'DoughnutChart(cat_df, names="product", values="revenue", backend="plotly").fig',
        ),
        *chart_section(
            "Treemap",
            "Nested rectangles whose areas are proportional to a numeric value.",
            'Treemap(cat_df, labels="product", values="revenue")\nNone',
            'Treemap(hier_df, labels="country", values="sales", parents="region", backend="plotly").fig',
        ),
        *chart_section(
            "CircularPacking (Seaborn-only)",
            "Hierarchical circles inside circles. Plotly has no native equivalent.",
            'CircularPacking(cat_df, labels="product", values="revenue")\nNone',
            None,
        ),
        *chart_section(
            "SunburstDiagram",
            "A radial treemap that shows hierarchical structure level by level.",
            'SunburstDiagram(hier_df, path=["region", "country"], values="sales")\nNone',
            'SunburstDiagram(hier_df, path=["region", "country"], values="sales", backend="plotly").fig',
        ),
        *chart_section(
            "VennDiagram (Seaborn-only)",
            "Overlapping circles for two- or three-set intersections.",
            'VennDiagram(sets=[{1,2,3,4}, {3,4,5,6}, {5,6,7,1}])\nNone',
            None,
        ),
        *chart_section(
            "Dendrogram",
            "Hierarchical clustering of a numeric matrix.",
            'Dendrogram(multi_df[["W","X","Y","Z"]], labels=[f"obs{i}" for i in range(8)])\nNone',
            'Dendrogram(multi_df[["W","X","Y","Z"]], labels=[f"obs{i}" for i in range(8)], backend="plotly").fig',
        ),
    ]
    build("02_categorical.ipynb", cells)


# ----------------------------- 03 num & cat -----------------------------
def num_cat() -> None:
    setup = code(
        COMMON_IMPORTS
        + """
from plotify.num_cat import (
    GroupedBarPlot, StackedBarPlot, GroupedScatter, BoxPlotByGroup,
)

rng = np.random.default_rng(7)
# 25 observations per (region, product) so boxplots actually show a
# distribution rather than collapsing to a single line.
records = []
for r in ["North", "South", "East", "West"]:
    for p in ["Widgets", "Gadgets", "Gizmos"]:
        baseline = rng.integers(50, 180)
        for _ in range(25):
            records.append({
                "region": r,
                "product": p,
                "sales": int(max(5, baseline + rng.normal(0, baseline * 0.25))),
            })
sales = pd.DataFrame(records)

points = pd.DataFrame({
    "weight": rng.normal(70, 12, size=120),
    "height": rng.normal(170, 10, size=120),
    "team":   rng.choice(["A", "B", "C"], size=120),
})

sales.head()
"""
    )

    cells = [
        md(
            """
# Numeric × categorical

Charts that combine one numeric column with one or two categoricals.
"""
        ),
        setup,
        *chart_section(
            "GroupedBarPlot",
            "One primary categorical on x, sub-bars from a secondary categorical.",
            'GroupedBarPlot(sales, x="region", y="sales", hue="product")\nNone',
            'GroupedBarPlot(sales, x="region", y="sales", hue="product", backend="plotly").fig',
        ),
        *chart_section(
            "StackedBarPlot",
            "Stacked sub-bars. Pass `normalize=True` for a 100%-stacked variant.",
            'StackedBarPlot(sales, x="region", y="sales", hue="product")\nNone',
            'StackedBarPlot(sales, x="region", y="sales", hue="product", normalize=True, backend="plotly").fig',
        ),
        *chart_section(
            "GroupedScatter",
            "Scatter coloured by a categorical group.",
            'GroupedScatter(points, x="weight", y="height", hue="team")\nNone',
            'GroupedScatter(points, x="weight", y="height", hue="team", backend="plotly").fig',
        ),
        *chart_section(
            "BoxPlotByGroup",
            "Box plots clustered by primary category, sub-grouped by hue.",
            'BoxPlotByGroup(sales, x="region", y="sales", hue="product")\nNone',
            'BoxPlotByGroup(sales, x="region", y="sales", hue="product", backend="plotly").fig',
        ),
    ]
    build("03_num_cat.ipynb", cells)


# ----------------------------- 04 timeseries ----------------------------
def timeseries() -> None:
    setup = code(
        COMMON_IMPORTS
        + """
from plotify.timeseries import LineChart, AreaChart, StackedAreaChart, StreamGraph

rng = np.random.default_rng(11)
dates = pd.date_range("2024-01-01", periods=18, freq="MS")
ts = pd.DataFrame([
    {"date": d, "group": g, "value": int(rng.integers(20, 80) + i * 1.5)}
    for g in ["A", "B", "C"]
    for i, d in enumerate(dates)
])

ts_wide = ts.pivot(index="date", columns="group", values="value").reset_index()
ts.head()
"""
    )

    cells = [
        md(
            """
# Time series

Line, area, stacked area, and stream graph variants.

`StreamGraph` is Seaborn-only — Plotly has no native streamgraph primitive.
"""
        ),
        setup,
        *chart_section(
            "LineChart",
            "Evolution of one or more series over time.",
            'LineChart(ts, x="date", y="value", hue="group", markers=True)\nNone',
            'LineChart(ts, x="date", y="value", hue="group", markers=True, backend="plotly").fig',
        ),
        *chart_section(
            "AreaChart",
            "A line chart with the region under the curve filled.",
            'one = ts[ts["group"] == "A"]\nAreaChart(one, x="date", y="value")\nNone',
            'one = ts[ts["group"] == "A"]\nAreaChart(one, x="date", y="value", backend="plotly").fig',
        ),
        *chart_section(
            "StackedAreaChart",
            "Multiple series stacked vertically. Accepts both wide and long input.",
            'StackedAreaChart(ts, x="date", y="value", hue="group")\nNone',
            'StackedAreaChart(ts_wide, x="date", y=["A","B","C"], backend="plotly").fig',
        ),
        *chart_section(
            "StreamGraph (Seaborn-only)",
            "Stacked-area variant flowing around a centred baseline.",
            'StreamGraph(ts, x="date", y="value", hue="group")\nNone',
            None,
        ),
    ]
    build("04_timeseries.ipynb", cells)


# ----------------------------- 05 network -------------------------------
def network() -> None:
    setup = code(
        COMMON_IMPORTS
        + """
import networkx as nx
from plotify.network import (
    NetworkDiagram, ChordDiagram, SankeyDiagram, ArcDiagram,
    HierarchicalEdgeBundling,
)

# A small example graph used by Network and Arc demos.
edges = [("A","B"), ("A","C"), ("B","C"), ("C","D"), ("D","E"), ("E","A"), ("B","E")]

# Connection matrix for the chord demo.
chord_matrix = np.array([
    [0, 5, 3, 2],
    [5, 0, 4, 1],
    [3, 4, 0, 6],
    [2, 1, 6, 0],
])

# Sankey flows — a 3-stage energy mix:
#   0 Solar / 1 Wind / 2 Hydro / 3 Coal  →  4 Grid East / 5 Grid West
#                                       →  6 Residential / 7 Industry / 8 Transport
labels = ["Solar", "Wind", "Hydro", "Coal", "Grid E", "Grid W",
          "Resid.", "Industry", "Transport"]
src = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5]
tgt = [4, 5, 4, 5, 4, 5, 4, 5, 6, 7, 8, 6, 7, 8]
val = [30, 20, 15, 25, 10, 20, 40, 20, 40, 35, 20, 30, 40, 15]
"""
    )

    cells = [
        md(
            """
# Network plots

Five chart types covering generic graphs, flow diagrams, and hierarchical
relationships. Plotly is supported only for `NetworkDiagram` and
`SankeyDiagram`; the rest are Seaborn-only.
"""
        ),
        setup,
        *chart_section(
            "NetworkDiagram",
            "Generic node-link diagram. Pass an edge list or a `networkx.Graph`.",
            'NetworkDiagram(edges=edges, layout="kamada_kawai")\nNone',
            'NetworkDiagram(edges=edges, layout="kamada_kawai", backend="plotly").fig',
        ),
        *chart_section(
            "ChordDiagram (Seaborn-only)",
            "Symmetric connections between nodes arranged on a circle.",
            'ChordDiagram(matrix=chord_matrix, labels=["A","B","C","D"])\nNone',
            None,
        ),
        *chart_section(
            "SankeyDiagram",
            "Flow magnitudes encoded as band widths.",
            'SankeyDiagram(source=src, target=tgt, value=val, labels=labels)\nNone',
            'SankeyDiagram(source=src, target=tgt, value=val, labels=labels, backend="plotly").fig',
        ),
        *chart_section(
            "ArcDiagram (Seaborn-only)",
            "Nodes on a horizontal line; edges drawn as semi-circular arcs above.",
            'ArcDiagram(edges=edges, node_order=["A","B","C","D","E"])\nNone',
            None,
        ),
        *chart_section(
            "HierarchicalEdgeBundling (Seaborn-only)",
            "Leaves on a circle; connections drawn as Bezier curves bent toward the centre.",
            'leaves = list("ABCDEFGH")\nconnections = [("A","E"), ("B","F"), ("C","G"), ("D","H"), ("A","D")]\nHierarchicalEdgeBundling(leaves=leaves, connections=connections)\nNone',
            None,
        ),
    ]
    build("05_network.ipynb", cells)


# ----------------------------- 06 maps ----------------------------------
def maps() -> None:
    setup = code(
        COMMON_IMPORTS
        + """
from plotify.maps import (
    ChoroplethMap, BubbleMap, HexbinMap, Cartogram, ConnectionMap,
)

cities = pd.DataFrame({
    "city": ["Paris", "London", "Berlin", "Rome", "Madrid", "Lisbon"],
    "lat":  [48.8566, 51.5074, 52.5200, 41.9028, 40.4168, 38.7223],
    "lon":  [2.3522, -0.1278, 13.4050, 12.4964, -3.7038, -9.1393],
    "pop":  [2.1, 8.9, 3.7, 2.8, 3.3, 0.5],
})

rng = np.random.default_rng(0)
points = pd.DataFrame({
    "lat": rng.uniform(40, 55, size=400),
    "lon": rng.uniform(-5, 15, size=400),
})

countries = pd.DataFrame({
    "country": ["France", "Germany", "Spain", "Italy", "United Kingdom"],
    "value": [1.0, 2.5, 1.7, 2.0, 2.3],
})
cities
"""
    )

    cells = [
        md(
            """
# Maps

Five geographic chart types. The Plotly backend produces proper projected
maps via `plotly.express`; the Seaborn backend uses a bare lat/lon plane
where `geopandas` isn't strictly required, and a `GeoDataFrame` where it
is (`ChoroplethMap`).
"""
        ),
        setup,
        *chart_section(
            "ChoroplethMap (Plotly)",
            "Country / region polygons coloured by a numeric value. The Seaborn backend needs a GeoDataFrame; the Plotly backend can use the built-in country names locationmode shown here.",
            None,
            'ChoroplethMap(countries, value="value", locations="country", locationmode="country names", backend="plotly").fig',
        ),
        *chart_section(
            "BubbleMap",
            "Markers placed at lat/lon, sized by a numeric value.",
            'BubbleMap(cities, lat="lat", lon="lon", size="pop")\nNone',
            'BubbleMap(cities, lat="lat", lon="lon", size="pop", color="pop", hover_name="city", backend="plotly").fig',
        ),
        *chart_section(
            "HexbinMap",
            "Hex aggregation of geographic point data. The Plotly backend draws the hex grid on top of OpenStreetMap tiles, so it needs internet access at render time.",
            'HexbinMap(points, lat="lat", lon="lon")\nNone',
            'HexbinMap(points, lat="lat", lon="lon", backend="plotly").fig',
        ),
        *chart_section(
            "Cartogram (Seaborn-only)",
            "Dorling-style — circles at region centroids sized by a value.",
            'Cartogram(cities, label="city", lon="lon", lat="lat", value="pop", max_radius=2)\nNone',
            None,
        ),
        *chart_section(
            "ConnectionMap",
            "Lines between geographic points — useful for flow / origin-destination.",
            'starts = list(zip(cities["lon"], cities["lat"]))[:3]\nends   = list(zip(cities["lon"], cities["lat"]))[3:6]\nConnectionMap(starts=starts, ends=ends)\nNone',
            'starts = list(zip(cities["lon"], cities["lat"]))[:3]\nends   = list(zip(cities["lon"], cities["lat"]))[3:6]\nConnectionMap(starts=starts, ends=ends, backend="plotly").fig',
        ),
    ]
    build("06_maps.ipynb", cells)


# ----------------------------- main -------------------------------------
def execute_all() -> None:
    """Run every notebook in place via ``jupyter nbconvert --execute``.

    PYTHONPATH is set to the repo root so the kernel can ``import plotify``
    even when the package isn't pip-installed in the environment.
    """
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        f"{REPO_ROOT}{os.pathsep}{existing}" if existing else str(REPO_ROOT)
    )
    for path in sorted(NOTEBOOKS_DIR.glob("*.ipynb")):
        print(f"executing {path.name}...")
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--inplace",
                str(path),
            ],
            env=env,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Run nbconvert on each notebook so rendered outputs get embedded.",
    )
    args = parser.parse_args()

    quickstart()
    numerical()
    categorical()
    num_cat()
    timeseries()
    network()
    maps()

    if args.execute:
        execute_all()


if __name__ == "__main__":
    main()
