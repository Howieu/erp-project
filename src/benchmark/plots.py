"""Figures for the Quality Arena benchmark (Ch4).

Reads results/benchmark_v1/metrics_{raw,agg}.csv and emits four figures to
results/benchmark_v1/figures/ in both PDF (for LaTeX) and PNG (for preview):

    fig4-1_best_ari_per_dataset      headline: who wins where
    fig4-2_dbscan_eps_sweep          DBSCAN tuning sensitivity
    fig4-3_classix_radius_sweep      CLASSIX tuning sensitivity
    fig4-4_runtime_per_dataset       speed comparison (log scale)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Consistent palette across all figures
METHOD_COLORS = {
    "kmeans++":          "#4C72B0",
    "dbscan":            "#DD8452",
    "hierarchical_ward": "#55A868",
    "classix":           "#C44E52",
}
METHOD_LABELS = {
    "kmeans++":          "K-Means++",
    "dbscan":            "DBSCAN",
    "hierarchical_ward": "Hierarchical (Ward)",
    "classix":           "CLASSIX",
}
METHOD_ORDER = ["kmeans++", "hierarchical_ward", "dbscan", "classix"]

# Dataset display ordering: shape first (by difficulty intuition), then real
DATASET_ORDER = [
    "r15", "aggregation", "pathbased",     # easier shape
    "jain", "compound", "spiral",          # harder shape
    "iris", "seeds", "wine",               # real
]
DATASET_LABELS = {
    "aggregation": "Aggregation",
    "compound":    "Compound",
    "jain":        "Jain",
    "pathbased":   "Pathbased",
    "r15":         "R15",
    "spiral":      "Spiral",
    "iris":        "Iris",
    "wine":        "Wine",
    "seeds":       "Seeds",
}


def _apply_style() -> None:
    plt.rcParams.update({
        "font.size": 11,
        "axes.titlesize": 11,
        "axes.labelsize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
    })


def best_per_method(agg: pd.DataFrame) -> pd.DataFrame:
    """For each (dataset, method) cell pick the params config with best ARI."""
    idx = agg.groupby(["dataset", "method"])["ari_mean"].idxmax()
    return agg.loc[idx].copy()


def fig_best_ari(agg: pd.DataFrame, out: Path) -> None:
    """Grouped bar chart: 9 datasets x 4 methods, height = best ARI per cell."""
    best = best_per_method(agg)
    pivot = best.pivot(index="dataset", columns="method", values="ari_mean")
    pivot = pivot.reindex(index=DATASET_ORDER, columns=METHOD_ORDER)

    err = best.pivot(index="dataset", columns="method", values="ari_std")
    err = err.reindex(index=DATASET_ORDER, columns=METHOD_ORDER).fillna(0.0)

    fig, ax = plt.subplots(figsize=(11, 4.6))
    x = np.arange(len(pivot.index))
    width = 0.20

    for i, method in enumerate(METHOD_ORDER):
        offsets = x + (i - 1.5) * width
        ax.bar(
            offsets, pivot[method].values, width,
            yerr=err[method].values, capsize=2,
            label=METHOD_LABELS[method], color=METHOD_COLORS[method],
            edgecolor="white", linewidth=0.5,
        )

    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels([DATASET_LABELS[d] for d in pivot.index], rotation=20, ha="right")
    ax.set_ylabel("Adjusted Rand Index (best config per method)")
    ax.set_ylim(-0.1, 1.05)
    ax.set_axisbelow(True)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=4, frameon=False)
    ax.set_title("Best clustering quality per dataset across four methods")

    # Vertical separator between shape and real datasets (after index 5 = spiral)
    ax.axvline(5.5, color="gray", linewidth=0.5, linestyle=":", alpha=0.5)
    ax.text(2.5, 1.02, "Shape (synthetic)", ha="center", fontsize=9, color="gray")
    ax.text(7, 1.02, "Real (UCI)", ha="center", fontsize=9, color="gray")

    _save(fig, out, "fig4-1_best_ari_per_dataset")


def _sweep_subplot(ax, agg: pd.DataFrame, method: str, param_key: str, xlabel: str, fixed: dict | None = None) -> None:
    """Plot ARI vs param_key for one method across all datasets.

    `fixed` holds the secondary params constant (e.g. min_samples=5) so the sweep
    stays a clean single-knob curve even when the v3 grid sweeps several knobs.
    """
    sub = agg[agg["method"] == method].copy()
    params = sub["params"].apply(json.loads)
    if fixed:
        keep = params.apply(lambda d: all(d.get(k) == v for k, v in fixed.items()))
        sub, params = sub[keep], params[keep]
    sub["param_value"] = params.apply(lambda d: d[param_key])

    cmap = plt.colormaps["tab10"]
    for idx, dataset in enumerate(DATASET_ORDER):
        ds_rows = sub[sub["dataset"] == dataset].sort_values("param_value")
        if ds_rows.empty:
            continue
        ax.plot(
            ds_rows["param_value"], ds_rows["ari_mean"],
            marker="o", markersize=4, linewidth=1.4,
            color=cmap(idx % 10), label=DATASET_LABELS[dataset],
        )

    ax.set_xlabel(xlabel)
    ax.set_ylabel("Adjusted Rand Index")
    ax.set_ylim(-0.1, 1.05)
    ax.axhline(0, color="black", linewidth=0.5, alpha=0.3)
    ax.set_axisbelow(True)


def fig_dbscan_sweep(agg: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.6))
    _sweep_subplot(ax, agg, "dbscan", "eps", r"DBSCAN $\varepsilon$", fixed={"min_samples": 5})
    ax.set_title("DBSCAN: ARI vs. $\\varepsilon$ (min_samples=5)")
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, ncol=1)
    _save(fig, out, "fig4-2_dbscan_eps_sweep")


def fig_classix_sweep(agg: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.6))
    _sweep_subplot(ax, agg, "classix", "radius", "CLASSIX radius", fixed={"minPts": 5, "group_merging": "distance"})
    ax.set_title("CLASSIX: ARI vs. radius (minPts=5, distance merging)")
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, ncol=1)
    _save(fig, out, "fig4-3_classix_radius_sweep")


def fig_runtime(agg: pd.DataFrame, out: Path) -> None:
    """Best-config runtime per (dataset, method). Log y-axis."""
    best = best_per_method(agg)
    pivot = best.pivot(index="dataset", columns="method", values="runtime_seconds_mean")
    pivot = pivot.reindex(index=DATASET_ORDER, columns=METHOD_ORDER)

    fig, ax = plt.subplots(figsize=(11, 4.4))
    x = np.arange(len(pivot.index))
    width = 0.20

    # Convert to milliseconds for readability
    ms = pivot * 1000.0

    for i, method in enumerate(METHOD_ORDER):
        offsets = x + (i - 1.5) * width
        ax.bar(
            offsets, ms[method].values, width,
            label=METHOD_LABELS[method], color=METHOD_COLORS[method],
            edgecolor="white", linewidth=0.5,
        )

    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels([DATASET_LABELS[d] for d in pivot.index], rotation=20, ha="right")
    ax.set_ylabel("Runtime (ms, log scale)")
    ax.set_axisbelow(True)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=4, frameon=False)
    ax.set_title("Wall-clock runtime per dataset (best config per method)")

    _save(fig, out, "fig4-4_runtime_per_dataset")


def _save(fig, out: Path, stem: str) -> None:
    for ext in ("pdf", "png"):
        path = out / f"{stem}.{ext}"
        fig.savefig(path)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="results/benchmark_v1")
    parser.add_argument("--output-dir", default="results/benchmark_v1/figures")
    args = parser.parse_args()

    _apply_style()

    in_dir = Path(args.input_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    agg = pd.read_csv(in_dir / "metrics_agg.csv")

    fig_best_ari(agg, out_dir)
    fig_dbscan_sweep(agg, out_dir)
    fig_classix_sweep(agg, out_dir)
    fig_runtime(agg, out_dir)

    print(f"Wrote 4 figures (PDF + PNG) to {out_dir}")
    for path in sorted(out_dir.iterdir()):
        print(f"  {path.name}")


if __name__ == "__main__":
    main()
