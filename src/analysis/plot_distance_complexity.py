"""Render fig3-1: CLASSIX distance computations vs n (near-linear vs brute force).

Reads results/analysis/distance_complexity.csv (produced by distance_complexity.py).
Run: conda run -n exkmc python -m src.analysis.plot_distance_complexity
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CSV = Path("results/analysis/distance_complexity.csv")
OUT = Path("results/analysis/fig3-1_distance_complexity")


def make_figure(csv_path: Path, out_stem: Path) -> float:
    df = pd.read_csv(csv_path)
    slope = float(np.polyfit(np.log(df["n"]), np.log(df["nr_dist"]), 1)[0])
    fig, ax = plt.subplots(figsize=(5.0, 3.6))
    ax.loglog(df["n"], df["nr_dist"], "o-", label=f"CLASSIX nr_dist (slope ≈ {slope:.2f})")
    ax.loglog(df["n"], df["brute_force_n2"], "s--", color="grey",
              label="brute force  n(n−1)/2  (slope = 2)")
    ax.set_xlabel("number of points  n")
    ax.set_ylabel("distance computations")
    ax.set_title("CLASSIX aggregation cost is near-linear")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    out_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_stem.with_suffix(".png"), dpi=200)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)
    return slope


def main() -> None:
    slope = make_figure(CSV, OUT)
    print(f"wrote {OUT}.png/.pdf  (fitted slope ≈ {slope:.2f})")


if __name__ == "__main__":
    main()
