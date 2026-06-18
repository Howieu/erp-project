"""Dataset loaders for the Quality Arena benchmark.

Sources are the official CLASSIX repo bundled in this project at
~/erp-project/official_classix/exps/data/. Using their exact files lets
us compare apples-to-apples with the CLASSIX paper.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

DATA_ROOT = Path(__file__).resolve().parents[2] / "official_classix" / "exps" / "data"
SHAPE_DIR = DATA_ROOT / "Shape sets"
REAL_DIR = DATA_ROOT / "Real_data"


@dataclass(frozen=True)
class Dataset:
    name: str
    kind: str  # "shape" or "real"
    X: np.ndarray
    y: np.ndarray

    @property
    def n_samples(self) -> int:
        return int(self.X.shape[0])

    @property
    def n_features(self) -> int:
        return int(self.X.shape[1])

    @property
    def n_classes(self) -> int:
        return int(len(np.unique(self.y)))


def _load_shape(name: str) -> Dataset:
    path = SHAPE_DIR / f"{name}.txt"
    df = pd.read_csv(path, sep=r"\s+", header=None, engine="python")
    X = df.iloc[:, :-1].to_numpy(dtype=float)
    y = df.iloc[:, -1].to_numpy()
    # shape labels may be float in source; cast to int for cleanliness
    y = y.astype(int)
    return Dataset(name=name.lower(), kind="shape", X=X, y=y)


def _load_iris() -> Dataset:
    df = pd.read_csv(REAL_DIR / "Iris.csv")
    X = df[["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]].to_numpy(dtype=float)
    y = pd.Categorical(df["Species"]).codes.astype(int)
    return Dataset(name="iris", kind="real", X=X, y=y)


def _load_wine() -> Dataset:
    # header row is just numeric placeholders 1..14; last column is the class label
    df = pd.read_csv(REAL_DIR / "Wine.csv")
    arr = df.to_numpy(dtype=float)
    X = arr[:, :-1]
    y = arr[:, -1].astype(int)
    return Dataset(name="wine", kind="real", X=X, y=y)


def _load_seeds() -> Dataset:
    df = pd.read_csv(REAL_DIR / "Seeds.csv")
    arr = df.to_numpy(dtype=float)
    X = arr[:, :-1]
    y = arr[:, -1].astype(int)
    return Dataset(name="seeds", kind="real", X=X, y=y)


REGISTRY: dict[str, Callable[[], Dataset]] = {
    # Shape (synthetic, 2-D, with ground truth) — picked to cover varied shape & density
    "aggregation": lambda: _load_shape("Aggregation"),
    "compound": lambda: _load_shape("Compound"),
    "jain": lambda: _load_shape("Jain"),
    "pathbased": lambda: _load_shape("Pathbased"),
    "r15": lambda: _load_shape("R15"),
    "spiral": lambda: _load_shape("Spiral"),
    # Real (UCI, varied dimensionality)
    "iris": _load_iris,
    "wine": _load_wine,
    "seeds": _load_seeds,
}


def load_all() -> list[Dataset]:
    return [loader() for loader in REGISTRY.values()]


def load(name: str) -> Dataset:
    if name not in REGISTRY:
        raise KeyError(f"unknown dataset {name!r}; known: {sorted(REGISTRY)}")
    return REGISTRY[name]()


if __name__ == "__main__":
    for d in load_all():
        print(f"{d.name:14s} kind={d.kind:5s} n={d.n_samples:5d} d={d.n_features:2d} k={d.n_classes}")
