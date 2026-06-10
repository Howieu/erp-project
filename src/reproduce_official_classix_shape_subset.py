#!/usr/bin/env python3
"""Reproduce a lightweight subset of the official CLASSIX shape benchmark.

The official repository's full `exps/run_exp_main.py` requires HDBSCAN and a
compiled Quickshift++ implementation. For a dissertation sprint, this script
reproduces the directly relevant subset from `exps/run_shape_bk.py`:

- k-means++
- DBSCAN
- CLASSIX with distance merging
- CLASSIX with density merging

It uses the official shape datasets, official parameters, and compares the
computed ARI/AMI values against the official CSV files shipped in the repo.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
import warnings
from dataclasses import dataclass
from pathlib import Path

SEED = 0
os.environ.setdefault("LOKY_MAX_CPU_COUNT", str(os.cpu_count() or 1))
warnings.filterwarnings("ignore", category=UserWarning)

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.cluster import DBSCAN, KMeans


@dataclass(frozen=True)
class ShapeConfig:
    dataset: str
    classix_density_radius: float
    classix_density_minpts: int
    classix_distance_radius: float
    classix_distance_minpts: int
    dbscan_eps: float
    dbscan_min_samples: int


SHAPE_CONFIGS = [
    ShapeConfig("Aggregation", 0.25, 6, 0.10, 0, 0.125, 5),
    ShapeConfig("Compound", 0.125, 6, 0.10, 2, 0.200, 6),
    ShapeConfig("D31", 0.05, 10, 0.025, 21, 0.080, 3),
    ShapeConfig("Flame", 0.20, 3, 0.20, 9, 0.275, 5),
    ShapeConfig("Jain", 0.425, 0, 0.30, 0, 0.300, 4),
    ShapeConfig("Pathbased", 0.25, 9, 0.15, 10, 0.225, 8),
    ShapeConfig("R15", 0.135, 4, 0.15, 4, 0.100, 5),
    ShapeConfig("Spiral", 0.325, 0, 0.25, 5, 0.325, 5),
]


OFFICIAL_TO_LOCAL_COLUMNS = {
    "k-means++": "k-means++",
    "DBSCAN": "DBSCAN",
    "CLASSIX - distance": "CLASSIX - distance",
    "CLASSIX - density": "CLASSIX - density",
}


def import_official_classix(repo_root: Path):
    sys.path.insert(0, str(repo_root))
    import classix

    classix.__enable_cython__ = False
    from classix import CLASSIX, __version__, cython_is_available

    return CLASSIX, __version__, cython_is_available


def load_shape_data(repo_root: Path, dataset: str) -> pd.DataFrame:
    path = repo_root / "exps" / "data" / "Shape sets" / f"{dataset}.txt"
    return pd.read_csv(path, sep=r"\s+", header=None)


def zscore_like_official(data: pd.DataFrame) -> pd.DataFrame:
    return (data - data.mean(axis=0)) / data.std(axis=0)


def score(y_true: pd.Series, labels: np.ndarray) -> tuple[float, float]:
    ari = metrics.adjusted_rand_score(y_true, labels)
    ami = metrics.adjusted_mutual_info_score(y_true, labels)
    return ari, ami


def run_one_dataset(CLASSIX, repo_root: Path, config: ShapeConfig) -> list[dict[str, object]]:
    data = load_shape_data(repo_root, config.dataset)
    X_raw = data[[0, 1]]
    y = data[2]
    X_scaled = zscore_like_official(X_raw)
    rows: list[dict[str, object]] = []

    start = time.perf_counter()
    kmeans = KMeans(n_clusters=len(np.unique(y)), random_state=SEED, n_init=10)
    kmeans.fit(X_scaled)
    runtime = time.perf_counter() - start
    ari, ami = score(y, kmeans.labels_)
    rows.append({"Dataset": config.dataset, "Clustering": "k-means++", "ARI": ari, "AMI": ami, "Time": runtime})

    start = time.perf_counter()
    dbscan = DBSCAN(eps=config.dbscan_eps, min_samples=config.dbscan_min_samples)
    dbscan.fit(X_scaled)
    runtime = time.perf_counter() - start
    ari, ami = score(y, dbscan.labels_)
    rows.append({"Dataset": config.dataset, "Clustering": "DBSCAN", "ARI": ari, "AMI": ami, "Time": runtime})

    start = time.perf_counter()
    classix_distance = CLASSIX(
        sorting="pca",
        radius=config.classix_distance_radius,
        group_merging="distance",
        minPts=config.classix_distance_minpts,
        verbose=0,
        post_alloc=True,
    )
    classix_distance.fit_transform(X_raw)
    runtime = time.perf_counter() - start
    ari, ami = score(y, classix_distance.labels_)
    rows.append({"Dataset": config.dataset, "Clustering": "CLASSIX - distance", "ARI": ari, "AMI": ami, "Time": runtime})

    start = time.perf_counter()
    classix_density = CLASSIX(
        sorting="pca",
        radius=config.classix_density_radius,
        group_merging="density",
        minPts=config.classix_density_minpts,
        verbose=0,
        post_alloc=True,
    )
    classix_density.fit_transform(X_raw)
    runtime = time.perf_counter() - start
    ari, ami = score(y, classix_density.labels_)
    rows.append({"Dataset": config.dataset, "Clustering": "CLASSIX - density", "ARI": ari, "AMI": ami, "Time": runtime})

    return rows


def pivot_metric(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    return df.pivot(index="Dataset", columns="Clustering", values=metric).loc[[c.dataset for c in SHAPE_CONFIGS]]


def compare_with_official(repo_root: Path, reproduced: pd.DataFrame, metric: str) -> pd.DataFrame:
    official_path = repo_root / "exps" / "results" / "exp4" / f"shape_{metric.lower()}.csv"
    official = pd.read_csv(official_path, index_col=0)
    current = pivot_metric(reproduced, metric)

    rows = []
    for dataset in current.index:
        for official_col, local_col in OFFICIAL_TO_LOCAL_COLUMNS.items():
            expected = official.loc[dataset, official_col]
            observed = current.loc[dataset, local_col]
            rows.append(
                {
                    "Dataset": dataset,
                    "Clustering": local_col,
                    "Metric": metric,
                    "Official": expected,
                    "Reproduced": observed,
                    "AbsDiff": abs(expected - observed),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default="official_classix", help="Path to the cloned nla-group/classix repository.")
    parser.add_argument("--output-dir", default="results/official_classix_shape_subset", help="Where to write reproduction outputs.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    np.random.seed(SEED)
    CLASSIX, version, cython_is_available = import_official_classix(repo_root)
    print(f"Using CLASSIX {version} from {repo_root}")
    print(f"Cython available: {cython_is_available(verbose=0)}")

    rows = []
    for config in SHAPE_CONFIGS:
        rows.extend(run_one_dataset(CLASSIX, repo_root, config))

    reproduced = pd.DataFrame(rows)
    reproduced.to_csv(output_dir / "shape_subset_reproduced_long.csv", index=False)
    pivot_metric(reproduced, "ARI").to_csv(output_dir / "shape_subset_reproduced_ari.csv")
    pivot_metric(reproduced, "AMI").to_csv(output_dir / "shape_subset_reproduced_ami.csv")

    comparisons = pd.concat(
        [
            compare_with_official(repo_root, reproduced, "ARI"),
            compare_with_official(repo_root, reproduced, "AMI"),
        ],
        ignore_index=True,
    )
    comparisons.to_csv(output_dir / "shape_subset_compare_with_official.csv", index=False)

    max_diff = comparisons["AbsDiff"].max()
    print(f"Wrote outputs to {output_dir}")
    print(f"Max absolute ARI/AMI difference versus official CSV: {max_diff:.12g}")
    print(comparisons.to_string(index=False))


if __name__ == "__main__":
    main()
