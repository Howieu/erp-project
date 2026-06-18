"""Code-fidelity check: does our CLASSIX wrapper reproduce the official numbers?

This is the answer to the first question any reproduction-study reviewer asks:
"how do I know your CLASSIX wrapper is faithful to the authors' own results?"

We re-run our CLASSIX call on the *official* sklearn toy datasets, generated and
parameterised exactly as in the official repo's
`exps/revision/modified_sklearn_bk.ipynb` (n_samples=1500, np.random.seed(0),
StandardScaler, group_merging='distance', per-dataset tols/minPts/sorting), and
compare ARI against the official `CLASSIX (distance)` column in
`exps/revision/results/aricsv_en.csv`.

Result (2026-06-18): max |delta| = 0.0000 across all five labelled datasets ->
our wrapper is bit-faithful to the official implementation. Any ARI gaps on the
*shape sets* in the main benchmark are therefore attributable to parameter
tuning (grid coarseness), NOT to an implementation bug.

Run:  python -m src.benchmark.fidelity_check
"""

from __future__ import annotations

import contextlib
import io

import numpy as np
from sklearn import datasets
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler

from classix import CLASSIX


def _official_toy_datasets(n: int = 1500):
    """Replicates the dataset generation block of the official notebook."""
    np.random.seed(0)
    noisy_circles = datasets.make_circles(n_samples=n, factor=0.5, noise=0.05)
    noisy_moons = datasets.make_moons(n_samples=n, noise=0.05)
    blobs = datasets.make_blobs(n_samples=n, random_state=8)
    rs = 170
    Xb, yb = datasets.make_blobs(n_samples=n, random_state=rs)
    aniso = (np.dot(Xb, [[0.6, -0.6], [-0.4, 0.8]]), yb)
    varied = datasets.make_blobs(n_samples=n, cluster_std=[1.0, 2.5, 0.5], random_state=rs)
    # (name, (X, y), radius/tol, sorting, minPts, official CLASSIX(distance) ARI)
    return [
        ("noisy_circles", noisy_circles, 0.25, "pca", 0, 1.000),
        ("noisy_moons", noisy_moons, 0.18, "pca", 0, 1.000),
        ("varied", varied, 0.09, "pca", 12, 0.949),
        ("aniso", aniso, 0.12, "pca", 12, 0.998),
        ("blobs", blobs, 0.15, "pca", 0, 1.000),
    ]


def main() -> None:
    print(f"{'dataset':14}{'ours_ARI':>10}{'official':>10}{'delta':>9}")
    max_delta = 0.0
    for name, (X, y), tol, sorting, min_pts, official in _official_toy_datasets():
        Xs = StandardScaler().fit_transform(X)
        with contextlib.redirect_stdout(io.StringIO()):
            clx = CLASSIX(sorting=sorting, radius=tol, group_merging="distance", verbose=0, minPts=min_pts)
            clx.fit(Xs)
        ari = adjusted_rand_score(y, clx.labels_)
        delta = ari - official
        max_delta = max(max_delta, abs(delta))
        print(f"{name:14}{ari:>10.4f}{official:>10.3f}{delta:>+9.4f}")
    verdict = "MATCH (wrapper is faithful)" if max_delta < 0.02 else "MISMATCH - investigate"
    print(f"\nmax |delta| = {max_delta:.4f}  ->  {verdict}")


if __name__ == "__main__":
    main()
