"""
Generate the 1280x640 social-preview image for the GitHub repo.

Run from the repo root::

    python scripts/build_social_preview.py

Output lands at ``assets/social_preview.png`` — upload that to GitHub at
*Settings → General → Social preview*.

The image is built using Plotify itself (the publication theme + Okabe-Ito
palette) so it's automatically on-brand, and re-running this script after
any theme tweak will regenerate the preview to match.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import plotify  # noqa: F401  — applies publication theme on import

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPO_ROOT / "assets" / "social_preview.png"


def make_demo_data() -> pd.DataFrame:
    """A trending three-series dataset that fills the chart nicely.

    Each series is a noisy upward trend, offset so the lines don't overlap.
    The seed is fixed so the image is reproducible.
    """
    rng = np.random.default_rng(2026)
    months = pd.date_range("2024-01-01", periods=18, freq="MS")
    rows = []
    for offset, region in [(80, "North"), (40, "South"), (120, "West")]:
        trend = np.linspace(0, 220, len(months))
        noise = rng.normal(0, 14, len(months))
        for d, t, n in zip(months, trend, noise):
            rows.append({"date": d, "region": region,
                         "sales": float(offset + t + n)})
    return pd.DataFrame(rows)


def build() -> None:
    OUTPUT.parent.mkdir(exist_ok=True)
    df = make_demo_data()

    # --- Set up the canvas at exactly 1280x640 (= 12.8" x 6.4" at 100 DPI).
    fig = plt.figure(figsize=(12.8, 6.4), dpi=100, facecolor="white")

    # Slight off-white panel for the chart so it pops against pure-white
    # text background. Inset roughly to the centre of the canvas.
    chart_ax = fig.add_axes([0.07, 0.18, 0.86, 0.50])
    chart_ax.set_facecolor("#FAFAFA")

    # --- Plot a multi-series line chart through the publication theme. ----
    # Each region is one line, pulled from the Okabe-Ito palette.
    palette = plotify.theme.PUBLICATION.palette
    for i, (region, sub) in enumerate(df.groupby("region")):
        chart_ax.plot(
            sub["date"], sub["sales"],
            linewidth=3.0, color=palette[i % len(palette)], label=region,
        )

    chart_ax.set_xlabel("")
    chart_ax.set_ylabel("")
    chart_ax.tick_params(labelsize=9, colors="#666")
    for spine in ("top", "right"):
        chart_ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        chart_ax.spines[spine].set_color("#CCCCCC")
    chart_ax.grid(axis="y", color="#EAEAEA", linewidth=0.7)
    chart_ax.legend(
        loc="upper left", frameon=False, fontsize=10, ncol=3,
        bbox_to_anchor=(0.0, -0.05),
    )

    # --- Wordmark (top-left) ----------------------------------------------
    fig.text(
        0.07, 0.85, "plotify",
        fontsize=64, weight="bold", color="#111111",
        family="DejaVu Sans",
    )

    # --- Tagline (under the wordmark) ------------------------------------
    fig.text(
        0.07, 0.78, "beautiful charts, auto-picked from a dataframe",
        fontsize=18, color="#444444", family="DejaVu Sans",
    )

    # --- Code snippet (top-right) — one-liner that captures the value prop
    fig.text(
        0.93, 0.84,
        'plotify.auto(df, x="date", y="sales", color="region")',
        fontsize=13, color="#333333", family="monospace", ha="right",
    )
    fig.text(
        0.93, 0.79,
        "↓",
        fontsize=18, color="#888888", family="monospace", ha="right",
    )

    # --- Install command (bottom-right) ----------------------------------
    fig.text(
        0.93, 0.04, "pip install plotify-charts",
        fontsize=14, color="#666666", family="monospace", ha="right",
    )

    # --- Subtle footer credit (bottom-left) ------------------------------
    fig.text(
        0.07, 0.04,
        "publication-ready  ·  dual backend  ·  smart picker",
        fontsize=11, color="#888888", family="DejaVu Sans",
    )

    fig.savefig(OUTPUT, dpi=100, facecolor="white", bbox_inches=None)
    print(f"wrote {OUTPUT.relative_to(REPO_ROOT)} ({OUTPUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    build()
