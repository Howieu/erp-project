"""RFM feature engineering for the UCI Online Retail dataset.

Online Retail (Chen, 2015; UCI id 352) is transaction-level e-commerce data with
genuine UnitPrice x Quantity, so Monetary is real money (the reason it is the
primary domain dataset over RetailRocket, whose event stream has no clean price).

Pipeline:
  1. clean    drop missing CustomerID; remove cancellations (InvoiceNo 'C...'),
              non-positive Quantity / UnitPrice.
  2. RFM      per customer: Recency (days since last purchase, vs snapshot =
              max date + 1 day), Frequency (# distinct invoices), Monetary
              (sum of Quantity*UnitPrice).
  3. emit     data/processed/rfm.csv (CustomerID + R/F/M).

Run:  python -m src.domain.rfm
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW = Path("data/raw/Online Retail.xlsx")
OUT = Path("data/processed/rfm.csv")


def load_clean(path: Path = RAW) -> pd.DataFrame:
    df = pd.read_excel(path, engine="openpyxl")
    df = df.dropna(subset=["CustomerID"]).copy()
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]  # drop cancellations
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
    df["CustomerID"] = df["CustomerID"].astype(int)
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    return df


def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    snapshot = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("CustomerID").agg(
        recency=("InvoiceDate", lambda s: (snapshot - s.max()).days),
        frequency=("InvoiceNo", "nunique"),
        monetary=("TotalPrice", "sum"),
    )
    return rfm.reset_index()


def main() -> None:
    df = load_clean()
    rfm = compute_rfm(df)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rfm.to_csv(OUT, index=False)
    print(f"Wrote {OUT}  ({len(rfm)} customers)")
    print(rfm[["recency", "frequency", "monetary"]].describe().round(1).to_string())


if __name__ == "__main__":
    main()
