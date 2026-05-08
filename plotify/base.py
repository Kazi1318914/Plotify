"""
plotify.base
============

Base class that every Plotify plot inherits from.

The class provides:

* A **dual backend** dispatch — every concrete plot class ships two render
  implementations, ``_plot_seaborn`` (Matplotlib / Seaborn) and
  ``_plot_plotly`` (Plotly). The backend is chosen at construction time.
* A common ``save_plot`` helper that knows how to write both matplotlib
  figures (``.png`` / ``.svg`` / ``.pdf`` via ``matplotlib.figure.Figure``)
  and Plotly figures (static via ``kaleido`` or interactive ``.html``).
* A consistent lifecycle that preserves the "plot on instantiation" behaviour
  of the original :mod:`numerical` module, so user code such as
  ``Boxplot(df, x="cat", y="val")`` continues to render immediately.

A subclass only needs to implement :py:meth:`_plot_seaborn` and
:py:meth:`_plot_plotly` (either one may raise :class:`NotImplementedError` if
that backend has no sensible equivalent — e.g. Venn diagrams in Plotly).
"""

import os

import matplotlib.pyplot as plt


class BasePlot:
    """
    Abstract base class for every Plotify plot.

    Parameters
    ----------
    backend : {"seaborn", "plotly"}, default="seaborn"
        Which rendering engine to use. ``"seaborn"`` uses Seaborn/Matplotlib
        and produces static images; ``"plotly"`` produces interactive figures.
    title : str, optional
        Optional title applied after rendering.

    Attributes
    ----------
    SUPPORTED_BACKENDS : tuple[str, ...]
        Backends this class can render on. Subclasses may override this to
        advertise that they only support a subset (e.g. Word Cloud supports
        only ``"seaborn"``).
    _fig : matplotlib.figure.Figure | plotly.graph_objects.Figure | None
        The rendered figure, populated by :py:meth:`_render`.
    """

    # The set of backends this *class* can render on. Subclasses with
    # single-backend support should override this so the base validator
    # raises a clear message (rather than letting the render method fail).
    SUPPORTED_BACKENDS = ("seaborn", "plotly")

    def __init__(self, backend="seaborn", title=None):
        """
        Initialise the base plot.

        Parameters
        ----------
        backend : {"seaborn", "plotly"}, default="seaborn"
            The rendering backend for this instance.
        title : str, optional
            Plot title. Applied uniformly across both backends.

        Raises
        ------
        ValueError
            If ``backend`` is not one of ``self.SUPPORTED_BACKENDS``.
        """
        # Validate early — easier to debug than a KeyError deep in a render path.
        if backend not in self.SUPPORTED_BACKENDS:
            raise ValueError(
                f"Backend {backend!r} not supported by {type(self).__name__}. "
                f"Supported: {self.SUPPORTED_BACKENDS}"
            )

        self._backend = backend
        self._title = title
        self._fig = None  # populated by _render() in the concrete subclass

    # ------------------------------------------------------------------ #
    # Render dispatch
    # ------------------------------------------------------------------ #
    def _render(self):
        """
        Dispatch to the correct backend render method.

        Subclasses should call this at the end of their ``__init__`` after
        all plot-specific attributes have been stored.
        """
        # Single place that routes to one of the two private render methods.
        # Each subclass implements them; if a backend is unsupported it can
        # either raise NotImplementedError inside that method or narrow
        # ``SUPPORTED_BACKENDS`` so the ValueError is raised in ``__init__``.
        if self._backend == "seaborn":
            # Open a fresh matplotlib figure so we never inherit stale axis
            # state (e.g., a categorical converter set by a prior plot)
            # from whatever was last drawn onto pyplot's global state.
            plt.figure()
            self._plot_seaborn()
        else:
            self._plot_plotly()

    def _plot_seaborn(self):
        """Render using Seaborn / Matplotlib. Must be implemented by subclasses."""
        raise NotImplementedError(
            f"{type(self).__name__} does not implement a Seaborn/Matplotlib backend."
        )

    def _plot_plotly(self):
        """Render using Plotly. Must be implemented by subclasses."""
        raise NotImplementedError(
            f"{type(self).__name__} does not implement a Plotly backend."
        )

    # ------------------------------------------------------------------ #
    # Saving
    # ------------------------------------------------------------------ #
    def save_plot(self, file_name, folder=None, size=(10, 6)):
        """
        Save the rendered figure to disk.

        Parameters
        ----------
        file_name : str
            The target file name. Extension determines the output format:

            * Seaborn backend: ``.png``, ``.jpg``, ``.pdf``, ``.svg`` — anything
              :func:`matplotlib.pyplot.savefig` accepts.
            * Plotly backend: ``.html`` writes an interactive figure,
              anything else is treated as a static image and rendered via
              :mod:`kaleido`.
        folder : str, optional
            Directory to place the file in. Created if missing.
        size : tuple[float, float], default=(10, 6)
            Figure size in inches (Seaborn) or the ``(width, height)`` pair
            passed to Plotly's ``write_image``/``update_layout`` — inches are
            converted to pixels at 100 DPI.

        Returns
        -------
        str
            The absolute or relative path the file was written to.
        """
        # Resolve final path, creating the folder if needed.
        if folder:
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_name = os.path.join(folder, file_name)

        # Dispatch based on backend so callers do not need to care which one
        # produced the figure.
        if self._backend == "seaborn":
            self._save_seaborn(file_name, size)
        else:
            self._save_plotly(file_name, size)

        return file_name

    def _save_seaborn(self, file_name, size):
        """Persist the current Matplotlib state to ``file_name``.

        The concrete subclass already called ``self._plot_seaborn()`` during
        ``__init__`` which drew onto the current pyplot state. Here we simply
        resize the active figure and save it, then close it to keep notebook
        environments tidy.
        """
        # Re-render onto a fresh figure so that saving does not depend on
        # whatever state the caller's notebook left behind.
        fig = plt.figure(figsize=size)
        self._plot_seaborn()
        plt.savefig(file_name)
        plt.close(fig)  # prevent figure from popping up in notebooks
        plt.ion()  # restore interactive mode for any subsequent plots

    def _save_plotly(self, file_name, size):
        """Persist the stored Plotly figure to ``file_name``."""
        if self._fig is None:
            # Defensive: concrete subclasses should always populate _fig.
            raise RuntimeError(
                "Plotly figure has not been constructed; did _plot_plotly() run?"
            )

        # Convert the (width, height) inch tuple to pixels at 100 DPI so that
        # a size of (10, 6) maps to 1000×600 — consistent with matplotlib defaults.
        width_px = int(size[0] * 100)
        height_px = int(size[1] * 100)

        # ``.html`` -> interactive; anything else -> static image via kaleido.
        if file_name.lower().endswith(".html"):
            self._fig.update_layout(width=width_px, height=height_px)
            self._fig.write_html(file_name)
        else:
            self._fig.write_image(file_name, width=width_px, height=height_px)
