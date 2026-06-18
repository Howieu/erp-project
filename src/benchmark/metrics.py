"""Cluster-quality metrics with safe handling of degenerate labelings."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    normalized_mutual_info_score,
    silhouette_score,
)


def _internal_metrics_valid(labels: np.ndarray) -> bool:
    """Silhouette / DB / CH require 2 <= n_clusters < n_samples."""
    n_unique = len(set(labels.tolist()))
    return 1 < n_unique < len(labels)


def count_clusters(labels: np.ndarray) -> int:
    """Exclude DBSCAN/CLASSIX-style noise label (-1)."""
    return len(set(labels.tolist()) - {-1})


def evaluate(X: np.ndarray, y_true: np.ndarray, labels: np.ndarray) -> dict:
    """Compute the standard quality bundle.

    Internal metrics (silhouette / DB / CH) are computed over the labels as
    given — including the noise class — to match the published practice in
    the CLASSIX paper. Records None when the labeling collapses to a single
    cluster (metrics undefined).
    """
    out = {
        "n_clusters_excluding_noise": count_clusters(labels),
        "n_noise": int(np.sum(labels == -1)),
        "ari": float(adjusted_rand_score(y_true, labels)),
        "nmi": float(normalized_mutual_info_score(y_true, labels)),
        "silhouette": None,
        "davies_bouldin": None,
        "calinski_harabasz": None,
    }
    if _internal_metrics_valid(labels):
        out["silhouette"] = float(silhouette_score(X, labels))
        out["davies_bouldin"] = float(davies_bouldin_score(X, labels))
        out["calinski_harabasz"] = float(calinski_harabasz_score(X, labels))
    return out
