"""Explanation Arena (RQ4) on UCI Online Retail RFM segments.

Pipeline 甲 = CLASSIX (self-explaining geometric).
Pipeline 乙 = K-Means++ + ExKMC threshold-tree rules.

Produces, per Ch5 plan:
  - separate complexity profiles (Approach A, no composite score)
  - the ExKMC rules in original RFM units (human-readable)
  - a CLASSIX geometric explanation for one customer
  - the k' trade-off curve: ExKMC max_leaves sweep -> (complexity vs fidelity)

Env: conda `exkmc` (py3.10, numpy 1.26.4 — both ExKMC and CLASSIX importable).
Run:  python -m src.domain.explanation_arena
"""

from __future__ import annotations

import io
import contextlib
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from classix import CLASSIX
from ExKMC.Tree import Tree

FEATS = ["recency", "frequency", "monetary"]
UNITS = ["R(days)", "F(orders)", "M(£)"]
RFM_CSV = Path("data/processed/rfm.csv")
OUT = Path("results/domain_uci")


def load_scaled(csv: Path = RFM_CSV):
    rfm = pd.read_csv(csv)
    sc = StandardScaler()
    Xs = sc.fit_transform(np.log1p(rfm[FEATS].values))
    return rfm, Xs, sc


def _unscale(sc, j, v):
    """scaled-log threshold -> original RFM unit."""
    return np.expm1(v * sc.scale_[j] + sc.mean_[j])


def exkmc_rules(tree, sc) -> list[str]:
    rules: list[str] = []

    def walk(node, path):
        if node.is_leaf():
            rules.append(" AND ".join(path) if path else "(all)")
            return
        f, thr = UNITS[node.feature], _unscale(sc, node.feature, node.value)
        walk(node.left, path + [f"{f} ≤ {thr:.0f}"])
        walk(node.right, path + [f"{f} > {thr:.0f}"])

    walk(tree.tree, [])
    return rules


def kprime_curve(Xs, km, k, kmax_mult=4) -> pd.DataFrame:
    """Sweep ExKMC max_leaves from k upward; record complexity vs fidelity."""
    rows = []
    for max_leaves in range(k, k * kmax_mult + 1):
        t = Tree(k=k, max_leaves=max_leaves)
        t.fit(Xs, km)
        # fidelity = fraction of points whose rule-assignment matches k-means
        fidelity = float((t.predict(Xs) == km.labels_).mean())
        rows.append({
            "max_leaves": max_leaves,
            "n_leaves": max_leaves,
            "depth": t._max_depth(),
            "fidelity_to_kmeans": round(fidelity, 4),
        })
    return pd.DataFrame(rows)


def main(csv: Path = RFM_CSV, out: Path = OUT) -> None:
    out.mkdir(parents=True, exist_ok=True)
    rfm, Xs, sc = load_scaled(csv)
    k = 4

    # Pipeline 乙
    km = KMeans(k, n_init=10, random_state=0).fit(Xs)
    base = Tree(k=k, max_leaves=k)
    base.fit(Xs, km)
    rules = exkmc_rules(base, sc)

    # Pipeline 甲
    clx = CLASSIX(radius=0.9, verbose=0)
    clx.fit(Xs)

    print("=== Complexity profiles (Approach A — separate, no composite) ===")
    print(f"  甲 CLASSIX : starting_points={clx.splist_.shape[0]}  explanation_dim={Xs.shape[1]}  primitive=distance-to-prototype")
    print(f"  乙 ExKMC   : rules(leaves)={k}  tree_nodes={base._size()}  max_conditions/rule(depth)={base._max_depth()}  primitive=single-feature threshold")

    print("\n=== 乙 ExKMC rules (original RFM units, directly actionable) ===")
    for r in rules:
        print(f"  IF {r}")

    top = int(rfm["monetary"].idxmax())
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        clx.explain(Xs, top, plot=False)
    print(f"\n=== 甲 CLASSIX geometric explanation (customer idx {top}) ===")
    print("  " + buf.getvalue().strip().splitlines()[0])

    curve = kprime_curve(Xs, km, k)
    curve.to_csv(out / "exkmc_kprime_curve.csv", index=False)
    print(f"\n=== k' trade-off curve (wrote {out/'exkmc_kprime_curve.csv'}) ===")
    print(curve.to_string(index=False))


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Explanation Arena (default: UCI; --csv/--out for RetailRocket robustness)")
    ap.add_argument("--csv", type=Path, default=RFM_CSV)
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args()
    main(a.csv, a.out)
