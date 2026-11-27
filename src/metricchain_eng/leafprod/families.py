"""Seeded generators of synthetic instances (integer tables of magnitude up to ``R = 1000``).

    instance = make("grid", n=36, k=3, seed=seed_of("leafcert-bench-v1", "grid", 3, 36, 0))

Every generator is a function of its arguments and of one integer seed, through ``random.Random(seed)``
only (the Mersenne Twister of the standard library, whose output for a given seed is part of its
documented behaviour); :func:`digest` gives a checksum of an instance so that a regenerated instance can be
compared with a stored one.  Families (``k`` is an alphabet size, or ``"mixed"``: every site draws its
alphabet from ``MIXED``):

``chain``      sites on a path; ``tree``: a random recursive tree with shuffled labels;
``band2``, ``band3``  pairs ``|i - j| <= w``; ``grid``: a two-dimensional grid with open boundary
               (``n = rows x cols``, as square as ``n`` allows); ``cubic``: a random 3-regular graph;
``complete``   all pairs.  In these seven every entry of every field and pair table is uniform in
               ``{-R, ..., R}``, independently ("random signed couplings").
``potts``      the grid with attractive Potts couplings ``J_ij(a, b) = -w_ij [a = b]``, ``w_ij`` uniform in
               ``{1, ..., R}``, and uniform fields.
"""
from __future__ import annotations

import hashlib
import json
import random

R = 1000
MIXED = (2, 3, 5, 10)
FAMILIES = ("chain", "tree", "band2", "band3", "grid", "cubic", "complete", "potts")


def seed_of(master, family, k, n, index):
    """The seed of instance ``index`` of a cell: the first 8 bytes of sha256 of the cell's name."""
    text = f"{master}|{family}|k={k}|n={n}|r={index}"
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:8], "big")


def digest(instance):
    """sha256 of the instance in a canonical text form (fields, and the pair tables that are not zero)."""
    J = {key: table for key, table in instance["J"].items() if any(any(row) for row in table)}
    text = json.dumps({"H": instance["H"], "J": J}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode()).hexdigest()


def grid_shape(n):
    """``(rows, cols)`` with ``rows * cols = n`` and ``rows <= cols`` as close as possible."""
    rows = int(n ** 0.5)
    while n % rows:
        rows -= 1
    return rows, n // rows


def _edges(family, n, rng):
    if family == "chain":
        return [(i, i + 1) for i in range(n - 1)]
    if family in ("band2", "band3"):
        w = int(family[-1])
        return [(i, j) for i in range(n) for j in range(i + 1, min(n, i + w + 1))]
    if family == "complete":
        return [(i, j) for i in range(n) for j in range(i + 1, n)]
    if family in ("grid", "potts"):
        rows, cols = grid_shape(n)
        out = []
        for r in range(rows):
            for c in range(cols):
                i = r * cols + c
                if c + 1 < cols:
                    out.append((i, i + 1))
                if r + 1 < rows:
                    out.append((i, i + cols))
        return out
    if family == "tree":
        label = list(range(n))
        rng.shuffle(label)
        return sorted((min(label[t], label[p]), max(label[t], label[p]))
                      for t in range(1, n) for p in [rng.randrange(t)])
    if family == "cubic":
        if n % 2 or n < 4:
            raise ValueError("a 3-regular graph needs an even number of sites, at least 4")
        while True:                                     # pairing model, rejecting loops and double edges
            stubs = [i for i in range(n) for _ in range(3)]
            rng.shuffle(stubs)
            pairs = {(min(stubs[q], stubs[q + 1]), max(stubs[q], stubs[q + 1])) for q in range(0, 3 * n, 2)}
            if len(pairs) == 3 * n // 2 and all(u != v for u, v in pairs):
                return sorted(pairs)
    raise ValueError(f"unknown family {family!r}")


def make(family, n, k, seed):
    """The instance ``{"H": ..., "J": {...}}`` (pairs that are not edges are omitted from ``J``) with the
    annotations ``family``, ``n``, ``k``, ``seed``, ``edges``."""
    rng = random.Random(seed)
    shape = [rng.choice(MIXED) for _ in range(n)] if k == "mixed" else [int(k)] * n
    edges = _edges(family, n, rng)
    H = [[rng.randint(-R, R) for _ in range(shape[i])] for i in range(n)]
    J = {}
    for i, j in edges:
        if family == "potts":
            w = rng.randint(1, R)
            J[f"{i},{j}"] = [[-w if a == b else 0 for b in range(shape[j])] for a in range(shape[i])]
        else:
            J[f"{i},{j}"] = [[rng.randint(-R, R) for _ in range(shape[j])] for _ in range(shape[i])]
    return {"H": H, "J": J, "family": family, "n": n, "k": k, "seed": seed, "edges": len(edges)}
