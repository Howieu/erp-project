"""RFM-analog feature engineering for the RetailRocket dataset (robustness cross-check).

RetailRocket (Kaggle: retailrocket/ecommerce-dataset) is an event stream
(view / addtocart / transaction), NOT priced transactions. So unlike UCI Online
Retail there is no clean Monetary — it is built from a quantity proxy:

  events.csv columns: timestamp(ms), visitorid, event, itemid, transactionid

Pipeline (mirrors src/domain/rfm.py, minus price):
  1. clean    keep "customers" = visitors with >=1 transaction event.
  2. RFM      per visitor:
                Recency   days since last event, vs snapshot = max ts + 1 day
                Frequency # distinct transactionid (orders)            <- like #invoices
                Monetary  # transaction-event rows (items purchased)   <- quantity proxy,
                          honest stand-in for Sum(Qty*Price) when Price is absent.
  3. emit     data/processed/rfm_retailrocket.csv (visitorid + R/F/M), SAME column
              schema (recency/frequency/monetary) as rfm.csv so explanation_arena.py
              and domain_quality.py run unchanged on it.

ponytail: M is a quantity proxy (items bought), not money — RetailRocket has no
price. Distinct from F (orders). If a priced field ever appears, swap M here only.

Run:  conda run -n exkmc python -m src.domain.rfm_retailrocket
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW = Path("data/raw/retailrocket/events.csv")
OUT = Path("data/processed/rfm_retailrocket.csv")


def load_clean(path: Path = RAW) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["ts"] = pd.to_datetime(df["timestamp"], unit="ms")
    buyers = df.loc[df["event"] == "transaction", "visitorid"].unique()
    return df[df["visitorid"].isin(buyers)].copy()


def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    snapshot = df["ts"].max() + pd.Timedelta(days=1)
    txn = df[df["event"] == "transaction"]
    rfm = pd.DataFrame({
        "recency": df.groupby("visitorid")["ts"].apply(lambda s: (snapshot - s.max()).days),
        "frequency": txn.groupby("visitorid")["transactionid"].nunique(),
        "monetary": txn.groupby("visitorid").size(),  # # items purchased = quantity proxy
    }).reset_index()
    return rfm


def main() -> None:
    df = load_clean()
    rfm = compute_rfm(df)
    # self-check: schema + sanity (every buyer has >=1 order and >=1 item)
    assert list(rfm.columns) == ["visitorid", "recency", "frequency", "monetary"]
    assert (rfm["frequency"] >= 1).all() and (rfm["monetary"] >= rfm["frequency"]).all()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rfm.to_csv(OUT, index=False)
    print(f"Wrote {OUT}  ({len(rfm)} buyers)")
    print(rfm[["recency", "frequency", "monetary"]].describe().round(1).to_string())


if __name__ == "__main__":
    main()
