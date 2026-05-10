# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

While the package is on `0.x` the API may change between minor releases.

## [Unreleased]

## [0.1.0] - 2026-05-10

### Added
- Initial public release.
- Dual-backend (Seaborn/Matplotlib + Plotly) plot classes across six categories:
  - **Numerical** — `Boxplot`, `DensityPlot`, `Violinplot`, `ScatterPlot`, `ConnectedScatterPlot`.
  - **Categoric** — `BarPlot`, `LollipopChart`, `RadarChart` (alias `SpiderChart`),
    `ParallelCoordinates`, `WordCloudPlot`, `PieChart`, `DoughnutChart`, `Treemap`,
    `CircularPacking`, `SunburstDiagram`, `VennDiagram`, `Dendrogram`.
  - **Num & Cat** — `GroupedBarPlot`, `StackedBarPlot`, `GroupedScatter`, `BoxPlotByGroup`.
  - **Time series** — `LineChart`, `AreaChart`, `StackedAreaChart`, `StreamGraph`.
  - **Network** — `NetworkDiagram`, `ChordDiagram`, `SankeyDiagram`, `ArcDiagram`,
    `HierarchicalEdgeBundling`.
  - **Maps** — `ChoroplethMap`, `BubbleMap`, `HexbinMap`, `Cartogram`, `ConnectionMap`.
- `plotify.auto()` and `plotify.suggest()` smart chart picker — infers an appropriate
  chart from inferred dataframe column kinds (numeric / datetime / categorical / boolean),
  with optional `intent=` overrides.
- `plotify.theme` system — auto-applied colourblind-safe Okabe-Ito **publication** theme on
  both backends; `theme.set("none")` to opt out, `theme.register(Theme(...))` for custom
  themes.
- Smart matplotlib tick formatting (1.2K / 3.4M / 5.6B) for numeric axes.
- 7 demo notebooks under `notebooks/` covering every chart class on both backends, with
  rendered outputs committed.
- `scripts/build_notebooks.py --execute` to regenerate the notebook suite.
- 125 pytest tests across all subpackages.

[Unreleased]: https://github.com/Kazi1318914/Plotify/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Kazi1318914/Plotify/releases/tag/v0.1.0
