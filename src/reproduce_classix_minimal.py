#!/usr/bin/env python3
"""Minimal CLASSIX reproduction for the ERP clustering project.

This script is intentionally small: it verifies that CLASSIX runs locally,
compares it with K-Means++ and DBSCAN on standard synthetic clustering data,
and saves both metric tables and one CLASSIX explanation output.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import time
import warnings
from dataclasses import dataclass
from pathlib import Path

RANDOM_STATE = 42
os.environ.setdefault("LOKY_MAX_CPU_COUNT", str(os.cpu_count() or 1))
warnings.filterwarnings("ignore", category=UserWarning)
warnings.showwarning = lambda *args, **kwargs: None

import numpy as np
import pandas as pd
from classix import CLASSIX
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    normalized_mutual_info_score,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class Dataset:
    name: str
    X: np.ndarray
    y: np.ndarray


def make_datasets() -> list[Dataset]:
    blobs_2d_X, blobs_2d_y = make_blobs(
        n_samples=900,
        centers=4,
        cluster_std=[0.55, 0.70, 0.60, 0.80],
        n_features=2,
        random_state=RANDOM_STATE,
    )
    blobs_10d_X, blobs_10d_y = make_blobs(
        n_samples=1200,
        centers=5,
        cluster_std=1.2,
        n_features=10,
        random_state=RANDOM_STATE,
    )
    moons_X, moons_y = make_moons(
        n_samples=800,
        noise=0.06,
        random_state=RANDOM_STATE,
    )
    return [
        Dataset("blobs_2d", blobs_2d_X, blobs_2d_y),
        Dataset("blobs_10d", blobs_10d_X, blobs_10d_y),
        Dataset("moons_2d", moons_X, moons_y),
    ]


def valid_for_internal_metrics(labels: np.ndarray) -> bool:
    unique_labels = set(labels.tolist())
    return 1 < len(unique_labels) < len(labels)


def count_clusters(labels: np.ndarray) -> int:
    return len(set(labels.tolist()) - {-1})


def evaluate_labels(X: np.ndarray, y_true: np.ndarray, labels: np.ndarray) -> dict[str, float | int | None]:
    result: dict[str, float | int | None] = {
        "n_clusters_excluding_noise": count_clusters(labels),
        "n_noise": int(np.sum(labels == -1)),
        "ari": adjusted_rand_score(y_true, labels),
        "nmi": normalized_mutual_info_score(y_true, labels),
        "silhouette": None,
        "davies_bouldin": None,
        "calinski_harabasz": None,
    }
    if valid_for_internal_metrics(labels):
        result["silhouette"] = silhouette_score(X, labels)
        result["davies_bouldin"] = davies_bouldin_score(X, labels)
        result["calinski_harabasz"] = calinski_harabasz_score(X, labels)
    return result


def timed_fit_predict(estimator, X: np.ndarray) -> tuple[np.ndarray, float]:
    start = time.perf_counter()
    if hasattr(estimator, "fit_predict"):
        labels = estimator.fit_predict(X)
    else:
        estimator.fit(X)
        labels = estimator.labels_
    elapsed = time.perf_counter() - start
    return np.asarray(labels), elapsed


def run_benchmark(datasets: list[Dataset]) -> pd.DataFrame:
    rows = []
    classix_radius_grid = [0.15, 0.25, 0.40, 0.60]
    dbscan_eps_grid = [0.20, 0.35, 0.50, 0.75]

    for dataset in datasets:
        X = StandardScaler().fit_transform(dataset.X)
        true_k = len(np.unique(dataset.y))

        labels, elapsed = timed_fit_predict(
            KMeans(n_clusters=true_k, init="k-means++", n_init=20, random_state=RANDOM_STATE),
            X,
        )
        rows.append(
            {
                "dataset": dataset.name,
                "method": "kmeans++",
                "parameters": json.dumps({"n_clusters": true_k, "n_init": 20}),
                "runtime_seconds": elapsed,
                **evaluate_labels(X, dataset.y, labels),
            }
        )

        for eps in dbscan_eps_grid:
            labels, elapsed = timed_fit_predict(DBSCAN(eps=eps, min_samples=10), X)
            rows.append(
                {
                    "dataset": dataset.name,
                    "method": "dbscan",
                    "parameters": json.dumps({"eps": eps, "min_samples": 10}),
                    "runtime_seconds": elapsed,
                    **evaluate_labels(X, dataset.y, labels),
                }
            )

        for radius in classix_radius_grid:
            labels, elapsed = timed_fit_predict(
                CLASSIX(radius=radius, minPts=10, verbose=0),
                X,
            )
            rows.append(
                {
                    "dataset": dataset.name,
                    "method": "classix",
                    "parameters": json.dumps({"radius": radius, "minPts": 10}),
                    "runtime_seconds": elapsed,
                    **evaluate_labels(X, dataset.y, labels),
                }
            )

    return pd.DataFrame(rows)


def save_classix_explanation(output_dir: Path, dataset: Dataset) -> None:
    X = StandardScaler().fit_transform(dataset.X)
    clx = CLASSIX(radius=0.25, minPts=10, verbose=0)
    clx.fit(X)

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        clx.explain(data=X)

    (output_dir / "classix_explain_blobs_2d.txt").write_text(buffer.getvalue(), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="results/classix_minimal", help="Directory for CSV and explanation outputs.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets = make_datasets()
    results = run_benchmark(datasets)
    results.to_csv(output_dir / "benchmark_metrics.csv", index=False)
    save_classix_explanation(output_dir, datasets[0])

    print(f"Wrote {output_dir / 'benchmark_metrics.csv'}")
    print(f"Wrote {output_dir / 'classix_explain_blobs_2d.txt'}")
    print(results.sort_values(["dataset", "method", "ari"], ascending=[True, True, False]).to_string(index=False))


if __name__ == "__main__":
    main()
