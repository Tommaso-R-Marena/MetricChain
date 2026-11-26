"""Synthetic instance generators (Level 0–2 controls of the benchmark plan).

Every generator is deterministic in its seed and returns an exact :class:`PairModel`.
"""
from __future__ import annotations

import random

import numpy as np

from .model import PairModel

__all__ = ["random_pair_model"]


def random_pair_model(seed: int, n: int, kmax: int, density: float = 1.0, scale_bits: int = 0,
                      amplitude: int = 12, kmin: int = 1) -> PairModel:
    """Unstructured random instance: sizes uniform in `[kmin, kmax]`, integer entries uniform in
    `[-amplitude, amplitude]`, each pair present with probability `density`."""
    rng = random.Random(seed)
    sizes = [rng.randint(kmin, kmax) for _ in range(n)]
    unary = [np.array([rng.randint(-amplitude, amplitude) for _ in range(k)], dtype=np.int64) for k in sizes]
    pair = {}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < density:
                pair[(i, j)] = np.array([[rng.randint(-amplitude, amplitude) for _ in range(sizes[j])]
                                         for _ in range(sizes[i])], dtype=np.int64)
    return PairModel(unary=unary, pair=pair, scale_bits=scale_bits,
                     meta={"generator": "random_pair_model", "seed": seed, "n": n, "kmax": kmax,
                           "density": density, "amplitude": amplitude})
