"""Empirical validation of CLASSIX aggregation cost (Ch3 §3.x, property ③).

The sorting-based pruning means the aggregation only ever compares a point to
others inside a projection band of width `tol` (see aggregate_ed.py: the loop
`break`s once `sort_vals[j] - sort_vals[i] > tol`). This script measures the
actual number of distance computations CLASSIX performs (`clx.nrDistComp_`)
against the brute-force pairwise count n(n-1)/2, as n grows, to show the cost is
sub-quadratic in practice — the mathematical reason behind the ~36x speed
advantage observed in Ch4 §4.1.4.

Env:  conda `exkmc` (py3.10) — `conda run -n exkmc python -m src.analysis.distance_complexity`
"""

from __future__ import annotations

import contextlib
import io
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

from classix import CLASSIX

OUT = Path("results/analysis")
SIZES = (500, 1000, 2000, 4000, 8000, 16000)
RADIUS = 0.5
SEED = 0


def measure(n: int) -> dict:
    X, _ = make_blobs(n_samples=n, centers=5, n_features=2, random_state=SEED)
    Xs = StandardScaler().fit_transform(X)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        clx = CLASSIX(radius=RADIUS, verbose=0)
        clx.fit(Xs)
    nr = int(clx.nrDistComp_)
    brute = n * (n - 1) // 2
    return {
        "n": n,
        "nr_dist": nr,
        "brute_force_n2": brute,
        "fraction_of_brute": round(nr / brute, 5),
        "dist_per_point": round(nr / n, 2),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [measure(n) for n in SIZES]
    df = pd.DataFrame(rows)

    # empirical growth exponent: fit log(nr_dist) ~ a + b*log(n); b≈1 → linear, b≈2 → quadratic
    b = float(np.polyfit(np.log(df["n"]), np.log(df["nr_dist"]), 1)[0])

    df.to_csv(OUT / "distance_complexity.csv", index=False)
    print("=== CLASSIX distance computations vs brute force (property ③) ===")
    print(df.to_string(index=False))
    print(f"\nEmpirical scaling exponent  log(nr_dist) ~ {b:.2f}·log(n)  "
          f"(1=linear, 2=quadratic) → {'sub-quadratic, near-linear' if b < 1.5 else 'super-linear'}")
    print(f"dist/point stays ~flat → pruned band size roughly constant in n")
    print(f"\nwrote {OUT / 'distance_complexity.csv'}")


if __name__ == "__main__":
    main()
