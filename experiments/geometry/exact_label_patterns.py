"""Exact (modular) computations for label patterns (docs/geometry/LABEL_PATTERNS.md).

Only the points of a subset S of a chain are observed.  The statewise equality constraints among
them are the labelled pairs at chain separation 1 or 2; c(S) is their number, D_K = 3K(3K+1)/2.

(1) Conic rank.  For random label patterns, and for arbitrary subsets of the 2n - 3 constrained
    pairs of a chain, the rank of the conic system at a rational witness equals
    min(c, D_K - K + 1) -- which proves that value for generic chains, pattern by pattern
    (the rank cannot exceed it).  One exception is exhibited: for ONE state, two labelled triples
    give rank 5, not 6 (the edge directions lie on a pair of planes).
(2) Quartic certificate (Proposition 6.2) for patterns of two states: h_4 = K for patterns in
    general position with c(S) >= 17, and h_4 = K + dim L when the labelled bond vectors are
    covered by two hyperplanes (one structural point).

Rigour as in exact_conic_rank.py and exact_demix4.py: ranks modulo a prime at witnesses with
rational torsion parameters; only lower bounds on ranks are used.

Usage: exact_label_patterns.py            (about a minute)
       exact_label_patterns.py --mutate   planted error: one constraint too few must not certify
"""
import itertools
import math
import random
import sys

import numpy as np

import exact_demix4 as X4
from exact_conic_rank import witness
from geomlib import Mod, rank_mod_p


def needed(K):
    return 3 * K * (3 * K + 1) // 2 - (K - 1)


def pattern_pairs(S):
    S = sorted(S)
    return [(S[a], S[b]) for a in range(len(S)) for b in range(a + 1, len(S)) if S[b] - S[a] in (1, 2)]


def conic_rank(K, n, pairs, geometry="rational", seed=0):
    """Rank mod p of the functionals S -> e^T S e on Sym(3K), e the stacked vectors of `pairs`."""
    _, Z = witness(K, n, geometry, seed)
    p = Mod.p
    m = len(Z[0])
    rows = []
    for (i, j) in pairs:
        e = [(Z[j][c] - Z[i][c]) % p for c in range(m)]
        rows.append([(e[a] * e[b] * (1 if a == b else 2)) % p for a in range(m) for b in range(a, m)])
    return rank_mod_p(rows, p) if rows else 0


def quartic(K, n, S, geometry="rational", seed=0, p=X4.PRIMES[0]):
    """dim L and h_4 for the label pattern S (exact, mod p)."""
    _, Z, ell2 = X4.witness(K, n, geometry, seed, p)
    N = 3 * K
    idx = [(i, j) for i in range(N) for j in range(i, N)]
    A = []
    for (a, b) in pattern_pairs(S):
        e = (Z[b] - Z[a]) % p
        l = 1 if b - a == 1 else ell2
        A.append([int(e[i] * e[j] * (1 if i == j else 2) % p) for (i, j) in idx] + [(-l) % p])
    rank, ker = X4.nullspace_mod_p(A, p)
    assert rank == len(A), "the constraints are dependent modulo p"
    B = np.zeros((len(ker), N, N), dtype=np.int64)
    for q, v in enumerate(ker):
        for t, (i, j) in enumerate(idx):
            B[q, i, j] = B[q, j, i] = v[t]
    m = len(B)
    nmon = math.comb(m + 3, 4)
    T = np.random.default_rng(1000 + seed).integers(0, p, size=(nmon + 8, m), dtype=np.int64)
    mn = X4.Minors(B, T, p)
    ech = X4.Echelon(nmon + 8, p, nmon - K)
    for ia in np.random.default_rng(1).permutation(len(mn.combos)):
        rows = mn.rows(int(ia))
        for s in range(0, len(rows), 128):
            ech.add(rows[s:s + 128])
            if ech.rank == nmon - K:
                break
        if ech.rank == nmon - K:
            break
    return len(A), m, nmon - ech.rank


def runs(lengths, gap=6):
    out, pos = [], 0
    for r in lengths:
        out += list(range(pos, pos + r))
        pos += r + gap
    return out


def main():
    mutate = "--mutate" in sys.argv
    ok = True
    rnd = random.Random(1)
    print("(1) conic rank = min(c, D_K - K + 1) at rational witnesses")
    for K, trials in ((1, 40), (2, 40), (3, 20)):
        bad = 0
        for trial in range(trials):
            n = rnd.randint(3 * K + 4, 40 if K < 3 else 70)
            geo = rnd.choice(["rational", "tetrahedral"])
            if trial % 2 == 0:                                  # a label pattern
                S = [i for i in range(n) if rnd.random() < rnd.choice([0.3, 0.5, 0.7, 0.85])]
                prs = pattern_pairs(S)
            else:                                               # an arbitrary set of constrained pairs
                allp = [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]
                prs = rnd.sample(allp, rnd.randint(1, min(len(allp), needed(K) + 6)))
            bad += conic_rank(K, n, prs, geo, seed=trial) != min(len(prs), needed(K))
        ok &= bad == 0
        print(f"    K = {K}: {trials} random patterns and subsets (two bond angles): exceptions {bad}")
    r6 = conic_rank(1, 20, pattern_pairs([0, 1, 2, 10, 11, 12]))
    r7 = conic_rank(1, 20, pattern_pairs([0, 1, 2, 10, 11, 12, 16, 17]))
    ok &= r6 == 5 and r7 == 6
    print(f"    the exception for one state: two labelled triples, c = 6: rank {r6} (a pair of planes); with one more "
          f"labelled bond, c = 7: rank {r7}")
    print("(2) quartic certificate for patterns of two states (dim L = 22 - c)")
    cases = [("5 triples + 2 pairs", runs([3, 3, 3, 3, 3, 2, 2]), 2, "K"),
             ("runs of 5, 5, 3", runs([5, 5, 3]), 2, "K"),
             ("every second point, 18 labels", list(range(0, 36, 2)), 2, "K"),
             ("6 triples", runs([3] * 6), 2, "K"),
             ("two runs of 6 (covered by two hyperplanes)", runs([6, 6]), 2, "K+m"),
             ("runs of 5 and 6 and a pair (covered by two hyperplanes)", runs([5, 6, 2]), 2, "K+m"),
             ("5 triples + 1 pair (one constraint fewer)", runs([3, 3, 3, 3, 3, 2]), 2, "none")]
    for name, S, K, want in cases:
        if mutate and want != "none":
            continue
        c, m, h4 = quartic(K, max(S) + 3, S)
        verdict = "K" if h4 == K else ("K+m" if h4 == K + m else "none")
        good = verdict == want
        ok &= good
        print(f"    {name:52s} c = {c}, dim L = {m}, h_4 = {h4}: "
              f"{'certified (h_4 = K)' if verdict == 'K' else 'certified modulo one structural point (h_4 = K + dim L)' if verdict == 'K+m' else 'not certified'}"
              f"   {'OK' if good else 'FAIL'}")
        if mutate:
            print("mutation (c = 16 claimed to certify):", "caught" if verdict == "none" else "NOT caught")
            return 1 if verdict == "none" else 0
    print("ALL OK" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
