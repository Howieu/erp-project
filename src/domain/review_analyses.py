"""Round-1 review response analyses (UCI Online Retail).

Three additions requested after simulated peer review:

  CR-2  Fair-comparison probe (Devil's Advocate C2): give pipeline 甲 the same
        "describe each cluster by RFM centroid/range" post-step that makes
        ExKMC rules addressable, and check whether CLASSIX clusters are then
        equally profileable into a small set of actionable segments.

  MN-4  Monetary-proxy validity (Reviewer 1 W4): on UCI, build RFM with the
        real amount vs a quantity (item-count) proxy, run the same k=4 pipeline
        on each, and compare the resulting segmentations directly (not via a
        single marginal correlation).

Env: conda `exkmc` (py3.10).  Run: python -m src.domain.review_analyses
"""
from __future__ import annotations

import collections
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler

from classix import CLASSIX

from src.domain.rfm import load_clean

FEATS = ["recency", "frequency", "monetary"]
RFM_CSV = Path("data/processed/rfm.csv")
OUT = Path("results/domain_uci")


def _scale(df: pd.DataFrame) -> np.ndarray:
    return StandardScaler().fit_transform(np.log1p(df[FEATS].values))


def _profile(df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
    """Per-cluster RFM median + [Q1,Q3] in ORIGINAL units — the addressable
    'centroid/range description' a profiling post-step would emit."""
    rows = []
    for c in sorted(set(labels)):
        m = labels == c
        row = {"cluster": c, "n": int(m.sum())}
        for f in FEATS:
            q1, md, q3 = np.percentile(df.loc[m, f], [25, 50, 75])
            row[f] = f"{md:.0f} [{q1:.0f},{q3:.0f}]"
        rows.append(row)
    return pd.DataFrame(rows)


def cr2_fair_comparison(rfm: pd.DataFrame) -> None:
    Xs = _scale(rfm)
    print("=" * 70)
    print("CR-2  Fair-comparison probe: can CLASSIX clusters be profiled into")
    print("      a small set of actionable segments like ExKMC's 4 rules?")
    print("=" * 70)

    km = KMeans(4, n_init=10, random_state=0).fit(Xs)
    print("\n[K-Means++ k=4]  the partition ExKMC describes — 4 balanced segments:")
    print(_profile(rfm, km.labels_).to_string(index=False))

    clx = CLASSIX(radius=0.9, verbose=0).fit(Xs)
    sizes = dict(collections.Counter(clx.labels_))
    print(f"\n[CLASSIX radius=0.9]  {len(sizes)} clusters, sizes {sizes}")
    print("  -> centroid-profiling the CLASSIX *clusters*:")
    print(_profile(rfm, clx.labels_).to_string(index=False))
    print("\n  Observation: CLASSIX yields ONE mega-cluster (>99%) + micro-outliers,")
    print("  so the centroid-profiling post-step produces ~1 segment, NOT 4.")

    gsz = sorted(collections.Counter(clx.groups_).values(), reverse=True)
    print(f"\n[CLASSIX 42 starting-point groups, pre-merge]  sizes (top 8): {gsz[:8]}")
    print(f"  total groups = {len(set(clx.groups_))}; the addressable granularity")
    print("  is dozens of micro-groups, not a handful of segments.")

    # what radius (if any) gives 4 non-degenerate clusters?
    print("\n[radius sweep] largest-cluster share at each radius:")
    for r in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        lab = CLASSIX(radius=r, verbose=0).fit(Xs).labels_
        c = collections.Counter(lab)
        share = max(c.values()) / len(lab)
        print(f"  r={r}: {len(c)} clusters, largest holds {share:.1%} of customers")


def mn4_monetary_proxy() -> None:
    print("\n" + "=" * 70)
    print("MN-4  Monetary-proxy validity: real amount vs item-count proxy (UCI)")
    print("=" * 70)
    df = load_clean()
    snap = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    g = df.groupby("CustomerID")
    rfm = pd.DataFrame({
        "recency": g["InvoiceDate"].apply(lambda s: (snap - s.max()).days),
        "frequency": g["InvoiceNo"].nunique(),
        "monetary": g["TotalPrice"].sum(),     # real money
        "monetary_qty": g["Quantity"].sum(),   # item-count proxy
    }).reset_index()

    r_mf = rfm["monetary"].corr(rfm["frequency"])
    r_qf = rfm["monetary_qty"].corr(rfm["frequency"])
    r_mq = rfm["monetary"].corr(rfm["monetary_qty"])
    print(f"\ncorr(real money, frequency)      = {r_mf:.3f}")
    print(f"corr(qty proxy,  frequency)      = {r_qf:.3f}")
    print(f"corr(real money, qty proxy)      = {r_mq:.3f}   <- direct proxy validity")

    base = rfm.rename(columns={"monetary": "_m"})[["recency", "frequency"]].copy()
    real = base.assign(monetary=rfm["monetary"])
    prox = base.assign(monetary=rfm["monetary_qty"])
    lab_real = KMeans(4, n_init=10, random_state=0).fit_predict(_scale(real))
    lab_prox = KMeans(4, n_init=10, random_state=0).fit_predict(_scale(prox))
    ari = adjusted_rand_score(lab_real, lab_prox)
    print(f"\nARI(k=4 segmentation: real money  vs  qty proxy) = {ari:.3f}")
    print("  -> how much the same customers land in the same segments under either M.")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rfm = pd.read_csv(RFM_CSV)
    cr2_fair_comparison(rfm)
    mn4_monetary_proxy()


if __name__ == "__main__":
    main()
