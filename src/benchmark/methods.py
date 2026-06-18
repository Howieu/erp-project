"""Method runners for the Quality Arena.

Each `run_*` returns a list of (params_dict, labels, runtime_seconds) tuples
covering the parameter grid for that method.

Design notes:
- KMeans++ / Hierarchical-Ward consume `true_k` because they require k.
  KMeans is randomised through `random_state`; Hierarchical (Ward) is
  deterministic given X, so we run it once per (dataset, seed-tag) and the
  seed dimension just records the redundant call for cross-method symmetry.
- DBSCAN / CLASSIX do NOT consume k; they sweep eps / radius grids on
  standardised data (after StandardScaler). min_samples=5 / minPts=5 is a
  middle ground that lets DBSCAN survive on the small UCI datasets.
"""

from __future__ import annotations

import contextlib
import io
import time
from dataclasses import dataclass

import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans

from classix import CLASSIX

# v3 (2026-06-18): FULL fair search. v2 only swept the primary knob with one
# secondary setting; that under-tuned CLASSIX on real/high-d data (Wine, Seeds).
# v3 sweeps each density method over BOTH its knobs, same budget/spirit for both:
#   DBSCAN  : eps x min_samples
#   CLASSIX : radius x minPts x group_merging
# As in Chen & Guttel (2024), CLASSIX's two merging modes are reported as two
# variants (recorded in params -> split at analysis time into distance/density).
# KMeans/Ward have no tunable knob (k given). The fidelity check
# (src/benchmark/fidelity_check.py) already proved the CLASSIX wrapper is faithful,
# so any residual gap vs the official real-data table is preprocessing/scaling,
# not implementation.
DBSCAN_EPS_GRID = tuple(round(0.10 + 0.05 * i, 2) for i in range(23))  # 0.10..1.20
DBSCAN_MIN_SAMPLES_GRID = (3, 5, 10)
CLASSIX_RADIUS_GRID = tuple(round(0.05 + 0.05 * i, 2) for i in range(30))  # 0.05..1.50
CLASSIX_MIN_PTS_GRID = (0, 5, 10)
CLASSIX_MERGING_GRID = ("distance", "density")


@dataclass(frozen=True)
class Run:
    method: str
    params: dict
    labels: np.ndarray
    runtime_s: float


def _timed_fit_predict(estimator, X: np.ndarray) -> tuple[np.ndarray, float]:
    start = time.perf_counter()
    if hasattr(estimator, "fit_predict"):
        labels = estimator.fit_predict(X)
    else:
        estimator.fit(X)
        labels = estimator.labels_
    elapsed = time.perf_counter() - start
    return np.asarray(labels), elapsed


def run_kmeans(X: np.ndarray, true_k: int, seed: int) -> list[Run]:
    """`seed` is recorded in the row's `seed` column, not in `params`, so the
    aggregate layer can collapse seeds into a single (dataset, method, params)
    cell."""
    labels, elapsed = _timed_fit_predict(
        KMeans(n_clusters=true_k, init="k-means++", n_init=10, random_state=seed),
        X,
    )
    return [Run("kmeans++", {"n_clusters": true_k, "n_init": 10}, labels, elapsed)]


def run_hierarchical(X: np.ndarray, true_k: int) -> list[Run]:
    labels, elapsed = _timed_fit_predict(
        AgglomerativeClustering(n_clusters=true_k, linkage="ward"),
        X,
    )
    return [Run("hierarchical_ward", {"n_clusters": true_k, "linkage": "ward"}, labels, elapsed)]


def run_dbscan(X: np.ndarray) -> list[Run]:
    runs: list[Run] = []
    for eps in DBSCAN_EPS_GRID:
        for min_samples in DBSCAN_MIN_SAMPLES_GRID:
            labels, elapsed = _timed_fit_predict(
                DBSCAN(eps=eps, min_samples=min_samples), X
            )
            runs.append(Run("dbscan", {"eps": eps, "min_samples": min_samples}, labels, elapsed))
    return runs


def run_classix(X: np.ndarray) -> list[Run]:
    runs: list[Run] = []
    for radius in CLASSIX_RADIUS_GRID:
        for min_pts in CLASSIX_MIN_PTS_GRID:
            for merging in CLASSIX_MERGING_GRID:
                # CLASSIX prints to stdout by default; silence it for clean logs
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    labels, elapsed = _timed_fit_predict(
                        CLASSIX(radius=radius, minPts=min_pts, group_merging=merging, verbose=0), X
                    )
                runs.append(
                    Run("classix", {"radius": radius, "minPts": min_pts, "group_merging": merging}, labels, elapsed)
                )
    return runs
