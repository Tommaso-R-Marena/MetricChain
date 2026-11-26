"""Synthetic instance generators (Level 0–2 controls of the benchmark plan).

Every generator is deterministic in its seed and returns an exact :class:`PairModel`.
"""
from __future__ import annotations

import random

import numpy as np

from .model import PairModel

__all__ = ["random_pair_model", "random_contact_model"]


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


def random_contact_model(seed: int, n: int, kmax: int, scale_bits: int = 10, contact_radius: float = 1.5,
                         strong: float = 4.0, weak: float = 0.05, clash: float = 30.0,
                         clash_probability: float = 0.08, kmin: int = 2) -> PairModel:
    """A crude protein-like synthetic model (Level 2 control; *not* a physical energy function).

    Sites sit on a self-avoiding lattice walk in 3-D ("residues").  Every pair of sites has a
    table (no cutoff): pairs within `contact_radius` lattice units ("strong pairs", listed in
    `meta["strong_pairs"]`) get state-specific couplings of standard deviation `strong` with
    occasional `clash` entries; every other pair gets a smooth coupling of order `weak / d**2`
    that is mostly additive in the two states, as long-range electrostatics is.  Unary terms make
    state 0 the reference state.  The generator reproduces the structure that decides
    certification cost on real side-chain problems — a sparse graph of strong couplings inside a
    dense graph of weak ones, with heterogeneous domain sizes — at sizes where exact ground truth
    is available.
    """
    rng = random.Random(seed)
    nprng = np.random.default_rng(seed)
    steps = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    pos = [(0, 0, 0)]
    occupied = {pos[0]}
    base = pos[0]
    while len(pos) < n:
        cand = [tuple(p + d for p, d in zip(base, s)) for s in steps]
        cand = [c for c in cand if c not in occupied]
        if not cand:                       # trapped: continue the walk from another occupied site
            base = rng.choice(pos)
            continue
        base = rng.choice(cand)
        pos.append(base)
        occupied.add(base)
    xyz = np.array(pos, dtype=float)
    sizes = [rng.randint(kmin, kmax) for _ in range(n)]
    scale = 2 ** scale_bits
    feat = [nprng.normal(size=(k, 3)) for k in sizes]          # one 3-vector per state
    unary_f = [np.concatenate(([0.0], nprng.uniform(0.2, 3.0, size=k - 1))) for k in sizes]
    pair_f, strong_pairs = {}, []
    for i in range(n):
        for j in range(i + 1, n):
            d = float(np.linalg.norm(xyz[i] - xyz[j]))
            if d <= contact_radius:
                table = strong * nprng.normal(size=(sizes[i], sizes[j]))
                table = np.where(nprng.random(size=table.shape) < clash_probability, clash, table)
                table[0, 0] = min(table[0, 0], 0.0)            # the reference pair of states never clashes
                table[-1, -1] = max(table[-1, -1], table[0, 0] + strong)   # and the table is never flat
                strong_pairs.append([i, j])
            else:
                u = (xyz[j] - xyz[i]) / d
                fi = np.tanh(feat[i] @ u)
                fj = np.tanh(feat[j] @ u)
                table = weak * (fi[:, None] - fj[None, :]) / d ** 2 + 0.3 * weak * np.outer(fi, fj) / d ** 3
            pair_f[(i, j)] = table
    unary = [np.rint(u * scale).astype(np.int64) for u in unary_f]
    pair = {key: np.rint(t * scale).astype(np.int64) for key, t in pair_f.items()}
    return PairModel(unary=unary, pair=pair, scale_bits=scale_bits,
                     meta={"generator": "random_contact_model", "seed": seed, "n": n, "kmax": kmax,
                           "contact_radius": contact_radius, "strong": strong, "weak": weak, "clash": clash,
                           "clash_probability": clash_probability, "strong_pairs": strong_pairs})
