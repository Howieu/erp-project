"""Domain-study clustering quality (Ch4 §4.3) on UCI Online Retail RFM.

The benchmark (Ch4 §4.2) selects the best configuration per method by ARI,
because those datasets have ground-truth labels. The domain study has NO
labels, so:
  - KMeans++ / Ward run at the RFM-convention k = 4 (the same k that Ch5's
    Explanation Arena builds its threshold-tree rules over);
  - DBSCAN / CLASSIX have no k, so their knobs are selected by the standard
    unsupervised criterion — highest silhouette over a grid, guarded to
    sensible labelings (2..12 clusters, noise < 50%);
  - CLASSIX is ALSO reported at radius = 0.9 (the operating point Ch5 actually
    explains), so Ch4's quality numbers tie to Ch5's explanation numbers.

Only internal metrics are defined without labels: silhouette, Davies-Bouldin,
Calinski-Harabasz (no ARI/NMI). Preprocessing (log1p + StandardScaler) is
identical to src/domain/explanation_arena.py so the two chapters describe the
same feature space.

Env:  conda `exkmc` (py3.10) — `conda run -n exkmc python -m src.domain.domain_quality`
"""

from __future__ import annotations

import contextlib
import io
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler

from classix import CLASSIX

from src.benchmark.metrics import _internal_metrics_valid, count_clusters

FEATS = ["recency", "frequency", "monetary"]
RFM_CSV = Path("data/processed/rfm.csv")
OUT = Path("results/domain_uci")

K = 4  # RFM-convention cluster count; matches Ch5 Explanation Arena
DBSCAN_EPS_GRID = tuple(round(0.10 + 0.05 * i, 2) for i in range(23))  # 0.10..1.20
CLASSIX_RADIUS_GRID = tuple(round(0.05 + 0.05 * i, 2) for i in range(30))  # 0.05..1.50


def load_scaled():
    rfm = pd.read_csv(RFM_CSV)
    sc = StandardScaler()
    Xs = sc.fit_transform(np.log1p(rfm[FEATS].values))
    return rfm, Xs


def internal_metrics(X: np.ndarray, labels: np.ndarray) -> dict:
    """Internal metrics only — no ground truth in the domain study.

    Computed over the labels as given (including any noise class) to match the
    benchmark's practice in src/benchmark/metrics.py.
    """
    out = {
        "n_clusters": count_clusters(labels),
        "n_noise": int(np.sum(labels == -1)),
        "silhouette": None,
        "davies_bouldin": None,
        "calinski_harabasz": None,
    }
    if _internal_metrics_valid(labels):
        out["silhouette"] = round(float(silhouette_score(X, labels)), 4)
        out["davies_bouldin"] = round(float(davies_bouldin_score(X, labels)), 4)
        out["calinski_harabasz"] = round(float(calinski_harabasz_score(X, labels)), 1)
    return out


def _silhouette_guarded(X: np.ndarray, labels: np.ndarray) -> float:
    """Selection score: silhouette, but reject degenerate labelings."""
    n_clusters = count_clusters(labels)
    noise_frac = float(np.mean(labels == -1))
    if not (2 <= n_clusters <= 12) or noise_frac >= 0.50 or not _internal_metrics_valid(labels):
        return -np.inf
    return float(silhouette_score(X, labels))


def _run_classix(X: np.ndarray, radius: float) -> np.ndarray:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        clx = CLASSIX(radius=radius, verbose=0)
        clx.fit(X)
    return np.asarray(clx.labels_)


def select_dbscan(X: np.ndarray) -> tuple[dict, np.ndarray]:
    best_score, best = -np.inf, None
    for eps in DBSCAN_EPS_GRID:
        labels = DBSCAN(eps=eps, min_samples=5).fit_predict(X)
        score = _silhouette_guarded(X, labels)
        if score > best_score:
            best_score, best = score, ({"eps": eps, "min_samples": 5}, labels)
    return best


def select_classix(X: np.ndarray) -> tuple[dict, np.ndarray]:
    best_score, best = -np.inf, None
    for radius in CLASSIX_RADIUS_GRID:
        labels = _run_classix(X, radius)
        score = _silhouette_guarded(X, labels)
        if score > best_score:
            best_score, best = score, ({"radius": radius}, labels)
    return best


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rfm, Xs = load_scaled()
    print(f"UCI Online Retail RFM: {Xs.shape[0]} customers, {Xs.shape[1]} features (log1p + StandardScaler)\n")

    rows = []

    km = KMeans(n_clusters=K, init="k-means++", n_init=10, random_state=0).fit_predict(Xs)
    rows.append({"method": "kmeans++", "params": f"k={K}", **internal_metrics(Xs, km)})

    ward = AgglomerativeClustering(n_clusters=K, linkage="ward").fit_predict(Xs)
    rows.append({"method": "hierarchical_ward", "params": f"k={K}", **internal_metrics(Xs, ward)})

    db_params, db_labels = select_dbscan(Xs)
    rows.append({"method": "dbscan", "params": f"eps={db_params['eps']} (best silhouette)", **internal_metrics(Xs, db_labels)})

    cx_params, cx_labels = select_classix(Xs)
    rows.append({"method": "classix", "params": f"radius={cx_params['radius']} (best silhouette)", **internal_metrics(Xs, cx_labels)})

    cx09 = _run_classix(Xs, 0.9)
    rows.append({"method": "classix", "params": "radius=0.9 (Ch5 operating point)", **internal_metrics(Xs, cx09)})

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "domain_quality.csv", index=False)
    print("=== Ch4 §4.3 domain quality (internal metrics; higher silhouette/CH, lower DB = better) ===")
    print(df.to_string(index=False))
    print(f"\nwrote {OUT / 'domain_quality.csv'}")


if __name__ == "__main__":
    main()
