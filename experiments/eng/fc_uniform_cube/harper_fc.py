#!/usr/bin/env python3
"""Exact fractional hitting numbers over ALL sensitive sets on the uniform cube, via Harper's theorem.

Context: THY-REQ-0006.  Setting (docs/workstreams/A_REPORT.md section 2.0, theory report Theorem
11.22): cube {0,1}^n, uniform measure, slack c * Hamming distance, u = beta*c, zero residual.
For D a proper subset of the cube and C its complement, the largest admissible perturbation
supported in D is h_D(y) = c * dist(y, C), and D is *sensitive at level eps* iff

    W(C) := 2^-n * sum_y exp(u * dist(y, C))  >  exp(eps).

The instance is vertex-transitive, so the uniform sampler is optimal and

    FC_n(eps) = 2^n / min{|D| : D sensitive} = 2^n / (2^n - M*),   M* = max{|C| : W(C) > e^eps}.

Claim checked here.  For every size M the maximum of W over sets of size M is attained by the
initial segment I_M of the simplicial order: W(C) = 1 + 2^-n sum_{r>=1} (e^{ur} - e^{u(r-1)})
(2^n - |Gamma_{r-1}(C)|), and by Harper's theorem initial segments minimise every neighbourhood
|Gamma_t(C)| simultaneously (the neighbourhood of an initial segment is an initial segment).
Hence M* is found by a search over M alone, for every n -- no linear programme is needed -- and
the single-dip value FC_dip (D restricted to Hamming balls) differs from FC only by the partial
shell of the simplicial order: 1 <= FC / FC_dip < |B(k)| / |B(k-1)|, k the radius of the smallest
sensitive ball.

    python harper_fc.py --check      brute force over all subsets for n <= 4 (must agree)
    python harper_fc.py              table of FC, FC_dip and their ratio for n <= 16
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def simplicial_order(n: int) -> np.ndarray:
    """Vertices of the n-cube in simplicial order: by weight, and among sets of equal size A
    precedes B when the smallest element of the symmetric difference lies in A.
    (Bit i of the integer is coordinate i.)
    """
    import functools

    def cmp(a: int, b: int) -> int:
        wa, wb = bin(a).count("1"), bin(b).count("1")
        if wa != wb:
            return -1 if wa < wb else 1
        if a == b:
            return 0
        low = (a ^ b) & -(a ^ b)                 # lowest differing coordinate
        return -1 if a & low else 1

    return np.array(sorted(range(1 << n), key=functools.cmp_to_key(cmp)), dtype=np.int64)


def dist_to_set(n: int, members: np.ndarray) -> np.ndarray:
    """Hamming distance of every vertex to the set (multi-source breadth-first search)."""
    size = 1 << n
    dist = np.full(size, -1, dtype=np.int64)
    dist[members] = 0
    frontier = members
    d = 0
    while frontier.size:
        d += 1
        nxt = []
        for i in range(n):
            cand = frontier ^ (1 << i)
            cand = cand[dist[cand] < 0]
            if cand.size:
                cand = np.unique(cand)
                dist[cand] = d
                nxt.append(cand)
        frontier = np.concatenate(nxt) if nxt else np.empty(0, dtype=np.int64)
    return dist


def W_of_set(n: int, members: np.ndarray, u: float) -> float:
    d = dist_to_set(n, members)
    counts = np.bincount(d, minlength=n + 1).astype(float)
    return float((counts * np.exp(u * np.arange(len(counts)))).sum() / (1 << n))


def harper_Mstar(n: int, u: float, eps: float, order: np.ndarray) -> int:
    """Largest M >= 1 with W(I_M) > exp(eps); 0 if even a single point is not sensitive."""
    thr = math.exp(eps)
    lo, hi = 0, (1 << n) - 1                       # C must be a proper subset's complement: 1 <= M <= 2^n - 1
    if W_of_set(n, order[:1], u) <= thr:
        return 0
    lo = 1
    while lo < hi:                                # W(I_M) is nonincreasing in M
        mid = (lo + hi + 1) // 2
        if W_of_set(n, order[:mid], u) > thr:
            lo = mid
        else:
            hi = mid - 1
    return lo


def ball_size(n: int, k: int) -> int:
    return sum(math.comb(n, j) for j in range(0, k + 1))


def dip_radius(n: int, u: float, eps: float) -> int | None:
    """Smallest k such that the dip on the ball B(k) (complement = ball of radius n-k-1) is sensitive."""
    thr = math.exp(eps)
    for k in range(0, n):
        # C = B(antipode, n-k-1): dist(y, C) = max(0, |y| - (n-k-1)) for y measured from the antipode
        r = n - k - 1
        w = sum(math.comb(n, j) * math.exp(u * max(0, j - r)) for j in range(n + 1)) / (1 << n)
        if w > thr:
            return k
    return None


_BRUTE_CACHE: dict[int, tuple[np.ndarray, np.ndarray]] = {}


def brute_force_Mstar(n: int, u: float, eps: float) -> int:
    """max |C| over ALL nonempty proper subsets C with W(C) > exp(eps) (n <= 4: 2^16 subsets)."""
    size = 1 << n
    if n not in _BRUTE_CACHE:
        masks = np.arange(1 << size, dtype=np.int64)
        dist_pt = np.array([[bin(a ^ b).count("1") for b in range(size)] for a in range(size)], dtype=np.int64)
        D = np.full((1 << size, size), n + 1, dtype=np.int64)         # D[mask, y] = dist(y, C_mask)
        for a in range(size):
            has = ((masks >> a) & 1).astype(bool)
            D[has] = np.minimum(D[has], dist_pt[a][None, :])
        pop = np.zeros(1 << size, dtype=np.int64)
        for a in range(size):
            pop += (masks >> a) & 1
        _BRUTE_CACHE[n] = (D, pop)
    D, pop = _BRUTE_CACHE[n]
    proper = (pop >= 1) & (pop <= size - 1)
    W = np.exp(u * D[proper]).sum(axis=1) / size
    sens = W > math.exp(eps)
    return int(pop[proper][sens].max()) if sens.any() else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--nmax", type=int, default=16)
    args = ap.parse_args()

    if args.check:
        ok = True
        cases = 0
        for n in (2, 3, 4):
            order = simplicial_order(n)
            for u in (0.5, 1.0, 2.0):
                for eps in (0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.2, 2.0):
                    a, b = harper_Mstar(n, u, eps, order), brute_force_Mstar(n, u, eps)
                    cases += 1
                    if a != b:
                        ok = False
                        print(f"MISMATCH n={n} u={u} eps={eps}: Harper {a}, brute force {b}")
        print(f"brute force over all subsets vs simplicial initial segments: {cases} cases, "
              f"{'all agree' if ok else 'DISAGREEMENT'}")
        return 0 if ok else 1

    rows = []
    print(" n    u  eps |  M*      min|D|   FC      | dip radius k  |B(k)|  FC_dip  | FC/FC_dip  |B(k)|/|B(k-1)|")
    for u, eps in ((1.0, 0.3), (1.0, 1.0), (2.0, 0.3), (0.5, 0.3)):
        for n in range(2, args.nmax + 1):
            order = simplicial_order(n)
            M = harper_Mstar(n, u, eps, order)
            if M == 0:
                continue
            dmin = (1 << n) - M
            k = dip_radius(n, u, eps)
            bk = ball_size(n, k)
            ratio_cap = bk / ball_size(n, k - 1) if k >= 1 else float("inf")
            rows.append({"n": n, "u": u, "eps": eps, "M_star": M, "min_sensitive_size": dmin,
                         "FC": (1 << n) / dmin, "dip_radius": k, "ball_size": bk, "FC_dip": (1 << n) / bk,
                         "ratio": bk / dmin})
            print(f"{n:2d} {u:4.1f} {eps:4.1f} | {M:6d} {dmin:8d} {(1 << n) / dmin:9.3f} | {k:6d} {bk:12d} {(1 << n) / bk:9.3f} |"
                  f" {bk / dmin:7.3f}   {ratio_cap:8.3f}")
        print()
    (HERE / "harper_fc_table.json").write_text(json.dumps(rows, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
