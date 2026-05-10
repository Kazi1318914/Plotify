# Contributing to Plotify

Thanks for your interest! Plotify is a small project and any improvement —
docs, bug fixes, new chart types — is welcome.

## Local setup

```bash
git clone https://github.com/Kazi1318914/Plotify.git
cd Plotify
poetry install --with dev --extras full
```

`--extras full` pulls in the optional `geopandas` dependency used by
`ChoroplethMap`'s seaborn backend. Skip it if you don't need geopandas.

## Run the tests

```bash
poetry run pytest
```

The suite is fast (~10s) and runs entirely offline.

## Regenerate the demo notebooks

The notebooks under `notebooks/` are **generated** from
[`scripts/build_notebooks.py`](scripts/build_notebooks.py) — please don't
hand-edit the `.ipynb` files. After changing an API or a chart class,
rebuild and re-execute in one step:

```bash
python scripts/build_notebooks.py --execute
```

The `--execute` flag runs each notebook via `jupyter nbconvert` so the
rendered outputs are embedded in the committed `.ipynb` files.

## Adding a new chart class

1. Pick the right subpackage (`numerical`, `categorical`, `num_cat`,
   `timeseries`, `network`, or `maps`).
2. Create a new file with one class that subclasses
   [`plotify.base.BasePlot`](plotify/base.py).
3. Implement `_plot_seaborn` and `_plot_plotly`. If only one backend is
   feasible, narrow `SUPPORTED_BACKENDS` at class level — the base class
   will reject unsupported backends with a clear `ValueError`.
4. Re-export the class from the subpackage's `__init__.py` and from
   [`plotify/__init__.py`](plotify/__init__.py).
5. Add a test under `tests/<subpackage>/` that instantiates the class and
   saves a file via `tmp_path`.
6. Add a section to the relevant notebook builder in
   `scripts/build_notebooks.py` and regenerate.
7. If the chart fits an existing `auto`/`suggest` rule, extend
   [`plotify/auto.py`](plotify/auto.py).

## Code style

* PEP 8, four-space indents.
* Docstrings open with `"""This is used to create …"""` and use a
  numpy-style `Parameters`/`Returns` block — see existing classes for the
  pattern.
* Comment the *why*, not the *what*. Explain non-obvious tricks (e.g.
  the orientation flip for Plotly dendrograms in
  [`plotify/categorical/dendrogram.py`](plotify/categorical/dendrogram.py)),
  not what `sns.boxplot` does.

## Pull requests

* One logical change per PR — keep diffs small.
* Run `poetry run pytest` before opening the PR.
* If you touched the API or a chart class, regenerate the notebooks and
  commit the updated outputs.
* Add a brief entry under `## [Unreleased]` in
  [`CHANGELOG.md`](CHANGELOG.md).

That's it — thanks for contributing!
