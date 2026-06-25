"""New Ch4 figures for the dual-lens revision.

fig4-5: realistic (label-free silhouette) vs oracle (best-over-grid) ARI per
        method — visualises the §4.1 dual-lens finding and the oracle gap.
fig4-6: CLASSIX cluster scatter on `spiral` at the silhouette-selected radius
        vs the ARI-optimal radius — a CLASSIX-repo-style 2D scatter showing why
        silhouette misguides CLASSIX's radius (§4.1.3).

Env: conda `exkmc` — `conda run -n exkmc python -m src.benchmark.refresh_figures`
"""
from __future__ import annotations

import contextlib
import io
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

from classix import CLASSIX  # noqa: E402
from src.benchmark import datasets  # noqa: E402

OUT = Path("results/benchmark_v3/figures")
SEL = Path("results/benchmark_v3/selection_refresh.csv")


def fig_dual_lens() -> None:
    sel = pd.read_csv(SEL)
    order = ["classix", "dbscan", "hierarchical_ward", "kmeans++"]
    m = sel.groupby("method")[["realistic_ari", "oracle_ari"]].mean().reindex(order)
    x = np.arange(len(order))
    w = 0.38
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.bar(x - w / 2, m["oracle_ari"], w, label="optimal tuning (best-over-grid)", color="#4C72B0")
    ax.bar(x + w / 2, m["realistic_ari"], w, label="realistic (label-free silhouette)", color="#DD8452")
    for xi, (o, r) in enumerate(zip(m["oracle_ari"], m["realistic_ari"])):
        ax.annotate(f"gap {o - r:.2f}", (xi, max(o, r) + 0.02), ha="center", fontsize=7, color="grey")
    ax.set_xticks(x)
    ax.set_xticklabels(["CLASSIX", "DBSCAN", "Ward", "K-Means++"])
    ax.set_ylabel("mean ARI")
    ax.set_ylim(0, 1.0)
    ax.set_title("Quality under optimal vs realistic selection")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / "fig4-5_realistic_vs_oracle_ari.png", dpi=200)
    fig.savefig(OUT / "fig4-5_realistic_vs_oracle_ari.pdf")
    plt.close(fig)


def _classix_labels(X, radius, min_pts, merging):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        clx = CLASSIX(radius=radius, minPts=min_pts, group_merging=merging, verbose=0)
        clx.fit(X)
    return np.asarray(clx.labels_)


def fig_spiral_scatter() -> None:
    ds = next(d for d in datasets.load_all() if d.name == "spiral")
    X = StandardScaler().fit_transform(ds.X)
    panels = [
        ("silhouette-selected\nradius=0.05  (ARI ≈ 0.00)", 0.05, 10),
        ("ARI-optimal\nradius=0.25  (ARI = 1.00)", 0.25, 0),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.7), sharex=True, sharey=True)
    for ax, (title, r, mp) in zip(axes, panels):
        lab = _classix_labels(X, r, mp, "density")
        ax.scatter(X[:, 0], X[:, 1], c=lab, cmap="tab10", s=10, linewidths=0)
        ax.set_title(title, fontsize=9)
        ax.set_xticks([]); ax.set_yticks([])
        ax.text(0.02, 0.98, f"{len(set(lab.tolist()))} clusters", transform=ax.transAxes,
                va="top", fontsize=8, color="grey")
    fig.suptitle("CLASSIX on spiral: silhouette picks the wrong radius", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "fig4-6_classix_spiral_radius.png", dpi=200)
    fig.savefig(OUT / "fig4-6_classix_spiral_radius.pdf")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig_dual_lens()
    fig_spiral_scatter()
    print(f"wrote {OUT}/fig4-5_realistic_vs_oracle_ari.png/.pdf")
    print(f"wrote {OUT}/fig4-6_classix_spiral_radius.png/.pdf")


if __name__ == "__main__":
    main()
