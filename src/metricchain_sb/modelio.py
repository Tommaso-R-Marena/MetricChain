"""Instance files: a :class:`PairModel` stored as a compressed numpy archive.

The archive holds the published instance exactly (integer tables, scale) plus its metadata as a
JSON string.  `mincert.model_sha256` of the loaded model is the identity of the instance: a
certificate that does not embed its instance names this checksum, and is meaningless for any
other instance.
"""
from __future__ import annotations

import json

import numpy as np

from .model import PairModel

__all__ = ["save_model", "load_model"]


def _as_int64(arr: np.ndarray) -> np.ndarray:
    if arr.dtype == object:
        raise ValueError("instance files hold int64 tables; entries beyond 2**62 are not supported")
    return arr.astype(np.int64)


def save_model(model: PairModel, path) -> None:
    arrays = {"scale_bits": np.array(model.scale_bits, dtype=np.int64),
              "meta_json": np.array(json.dumps(model.meta, sort_keys=True)),
              "n": np.array(model.n, dtype=np.int64),
              "pairs": np.array(sorted(model.pair), dtype=np.int64).reshape(-1, 2)}
    for i, u in enumerate(model.unary):
        arrays[f"u{i}"] = _as_int64(u)
    for (i, j), t in model.pair.items():
        arrays[f"p{i}_{j}"] = _as_int64(t)
    with open(path, "wb") as fh:
        np.savez_compressed(fh, **arrays)


def load_model(path) -> PairModel:
    with np.load(path, allow_pickle=False) as z:
        n = int(z["n"])
        unary = [z[f"u{i}"] for i in range(n)]
        pair = {(int(i), int(j)): z[f"p{int(i)}_{int(j)}"] for i, j in z["pairs"]}
        return PairModel(unary=unary, pair=pair, scale_bits=int(z["scale_bits"]),
                         meta=json.loads(str(z["meta_json"])))
