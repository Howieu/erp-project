"""Quality Arena benchmark orchestrator.

For each (dataset x method x params x seed) cell, fit the clustering,
evaluate the standard quality bundle, and write two CSVs:

    metrics_raw.csv   one row per (dataset, method, params, seed)
    metrics_agg.csv   mean +/- std collapsed over the seed dimension

Run from the repo root:
    python -m src.benchmark.run_benchmark --output-dir results/benchmark_v1

Notes on seed usage:
- KMeans++ varies on `random_state` — runs once per seed.
- DBSCAN / Hierarchical-Ward / CLASSIX are deterministic given their params;
  they run once and the same row is duplicated across seeds so the aggregate
  layer can treat all rows uniformly (std == 0 for these methods is meaningful:
  it certifies determinism rather than masking instability).
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # allow `python script.py`

from src.benchmark import datasets, methods
from src.benchmark.metrics import evaluate

SEEDS = (0, 1, 2, 3, 4)


def run_all(seeds=SEEDS) -> pd.DataFrame:
    rows: list[dict] = []

    for dataset in datasets.load_all():
        X = StandardScaler().fit_transform(dataset.X)
        true_k = dataset.n_classes

        # Deterministic methods: run once, then replay across all seeds for uniform aggregation.
        det_runs: list[methods.Run] = []
        det_runs.extend(methods.run_hierarchical(X, true_k))
        det_runs.extend(methods.run_dbscan(X))
        det_runs.extend(methods.run_classix(X))

        for seed in seeds:
            # KMeans varies with seed
            for run in methods.run_kmeans(X, true_k, seed):
                rows.append(_row(dataset, run, seed, X))

            # Deterministic methods: replay
            for run in det_runs:
                rows.append(_row(dataset, run, seed, X, deterministic=True))

    return pd.DataFrame(rows)


def _row(dataset, run: methods.Run, seed: int, X, deterministic: bool = False) -> dict:
    return {
        "dataset": dataset.name,
        "dataset_kind": dataset.kind,
        "n_samples": dataset.n_samples,
        "n_features": dataset.n_features,
        "true_k": dataset.n_classes,
        "method": run.method,
        "params": json.dumps(run.params, sort_keys=True),
        "seed": seed,
        "deterministic": deterministic,
        "runtime_seconds": run.runtime_s,
        **evaluate(X, dataset.y, run.labels),
    }


METRIC_COLS = (
    "ari",
    "nmi",
    "silhouette",
    "davies_bouldin",
    "calinski_harabasz",
    "n_clusters_excluding_noise",
    "n_noise",
    "runtime_seconds",
)


def aggregate(raw: pd.DataFrame) -> pd.DataFrame:
    grouped = raw.groupby(["dataset", "method", "params"], dropna=False)
    agg_records: list[dict] = []
    for (dataset, method, params), sub in grouped:
        rec = {
            "dataset": dataset,
            "method": method,
            "params": params,
            "n_runs": len(sub),
            "deterministic": bool(sub["deterministic"].iloc[0]),
        }
        for col in METRIC_COLS:
            rec[f"{col}_mean"] = sub[col].mean(skipna=True)
            rec[f"{col}_std"] = sub[col].std(ddof=0, skipna=True)
        agg_records.append(rec)
    return pd.DataFrame(agg_records)


def write_outputs(raw: pd.DataFrame, agg: pd.DataFrame, output_dir: Path, started_at: str, elapsed: float) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw.to_csv(output_dir / "metrics_raw.csv", index=False)
    agg.to_csv(output_dir / "metrics_agg.csv", index=False)

    meta = {
        "started_at_utc": started_at,
        "elapsed_seconds": elapsed,
        "n_raw_rows": len(raw),
        "n_agg_rows": len(agg),
        "seeds": list(SEEDS),
        "datasets": list(datasets.REGISTRY),
        "method_grids": {
            "dbscan_eps": list(methods.DBSCAN_EPS_GRID),
            "dbscan_min_samples": list(methods.DBSCAN_MIN_SAMPLES_GRID),
            "classix_radius": list(methods.CLASSIX_RADIUS_GRID),
            "classix_minPts": list(methods.CLASSIX_MIN_PTS_GRID),
            "classix_group_merging": list(methods.CLASSIX_MERGING_GRID),
        },
        "python": sys.version,
        "platform": platform.platform(),
    }
    (output_dir / "run_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="results/benchmark_v1")
    args = parser.parse_args()

    started_at = datetime.now(timezone.utc).isoformat()
    t0 = time.perf_counter()
    raw = run_all()
    agg = aggregate(raw)
    elapsed = time.perf_counter() - t0

    output_dir = Path(args.output_dir)
    write_outputs(raw, agg, output_dir, started_at, elapsed)

    print(f"Wrote {output_dir / 'metrics_raw.csv'} ({len(raw)} rows)")
    print(f"Wrote {output_dir / 'metrics_agg.csv'} ({len(agg)} rows)")
    print(f"Wrote {output_dir / 'run_meta.json'}")
    print(f"Total elapsed: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
