#!/usr/bin/env python3
"""R12 item 2 — the 17 grid x order cases of the support lemma that were too large for the exhaustive
search of r12_02_support.py: a FALSIFICATION ATTEMPT, not a proof.

For each case we look for a non-zero function of order <= d with support smaller than
s* = product of the n - d smallest alphabet sizes, by
  (1) random sparse integer combinations of the cylinder basis (coefficients in {-2,-1,1,2}, 1 to 6 terms);
  (2) hill climbing on integer coefficient vectors (one coefficient changed by +-1 per step, accepted if
      the support does not grow and the function stays non-zero), from random sparse starts;
  (3) differences and sums of two cylinder indicators on at most d sites (the natural candidates for
      cancellation).
All arithmetic is in integers (exact).  The script reports the least support found; a value below s*
would refute the lemma (the lemma is proved by induction in R12_REPORT par. 2.2, so none is expected).

One command:  python3 r12_02b_support_search.py
"""
import itertools
import math
import time

import numpy as np

T0 = time.time()
rng = np.random.default_rng(2026112612)


def grid_points(ks):
    return np.array(list(itertools.product(*[range(k) for k in ks])), dtype=np.int64)


def basis_matrix(ks, d):
    X = grid_points(ks)
    n = len(ks)
    cols = []
    for size in range(0, min(d, n) + 1):
        for U in itertools.combinations(range(n), size):
            for s in itertools.product(*[range(1, ks[i]) for i in U]):
                col = np.ones(len(X), dtype=np.int64)
                for i, si in zip(U, s):
                    col &= (X[:, i] == si)
                cols.append(col)
    return X, np.stack(cols, axis=1)


def s_star(ks, d):
    order = sorted(ks)
    return math.prod(order[:len(ks) - d])


CASES = [((3, 4, 4), 1), ((4, 4, 4), 1), ((2, 2, 4, 4), 1), ((2, 3, 3, 4), 1), ((2, 3, 4, 4), 1),
         ((2, 4, 4, 4), 1), ((2, 4, 4, 4), 2), ((3, 3, 3, 3), 1), ((3, 3, 3, 3), 2), ((3, 3, 3, 4), 1),
         ((3, 3, 3, 4), 2), ((3, 3, 4, 4), 1), ((3, 3, 4, 4), 2), ((3, 4, 4, 4), 1), ((3, 4, 4, 4), 2),
         ((4, 4, 4, 4), 1), ((4, 4, 4, 4), 2)]

total_trials = 0
refuted = 0
attained = 0
for ks, d in CASES:
    X, E = basis_matrix(ks, d)
    size, N = E.shape
    target = s_star(ks, d)
    best = size
    trials = 0
    # (1) random sparse integer combinations
    for _ in range(10):
        B = 20000
        C = np.zeros((B, N), dtype=np.int64)
        nt = rng.integers(1, 7, size=B)
        for b in range(B):
            idx = rng.choice(N, size=min(N, int(nt[b])), replace=False)
            C[b, idx] = rng.choice([-2, -1, 1, 2], size=len(idx))
        H = C @ E.T
        supp = np.count_nonzero(H, axis=1)
        supp = supp[supp > 0]
        best = min(best, int(supp.min()))
        trials += B
    # (2) hill climbing
    for start in range(200):
        c = np.zeros(N, dtype=np.int64)
        idx = rng.choice(N, size=min(N, int(rng.integers(1, 5))), replace=False)
        c[idx] = rng.choice([-1, 1], size=len(idx))
        h = E @ c
        cur = int(np.count_nonzero(h))
        if cur == 0:
            continue
        for step in range(400):
            j = int(rng.integers(N))
            delta = int(rng.choice([-1, 1]))
            h2 = h + delta * E[:, j]
            s2 = int(np.count_nonzero(h2))
            trials += 1
            if 0 < s2 <= cur:
                c[j] += delta
                h, cur = h2, s2
        best = min(best, cur)
    # (3) sums and differences of two cylinders on at most d sites
    n = len(ks)
    cyl = []
    for sz in range(1, d + 1):
        for U in itertools.combinations(range(n), sz):
            for s in itertools.product(*[range(ks[i]) for i in U]):
                v = np.ones(size, dtype=np.int64)
                for i, si in zip(U, s):
                    v &= (X[:, i] == si)
                cyl.append(v)
    cyl = np.array(cyl)
    if len(cyl) <= 600:
        for a in range(len(cyl)):
            for sign in (1, -1):
                H = cyl[a][None, :] + sign * cyl
                supp = np.count_nonzero(H, axis=1)
                supp = supp[supp > 0]
                if len(supp):
                    best = min(best, int(supp.min()))
                trials += len(cyl)
    else:
        for _ in range(200000 // 1000):
            ia = rng.integers(len(cyl), size=1000)
            ib = rng.integers(len(cyl), size=1000)
            for sign in (1, -1):
                H = cyl[ia] + sign * cyl[ib]
                supp = np.count_nonzero(H, axis=1)
                supp = supp[supp > 0]
                if len(supp):
                    best = min(best, int(supp.min()))
            trials += 2000
    total_trials += trials
    verdict = "s* attained, nothing below" if best == target else ("REFUTED" if best < target else "s* not reached by the search")
    refuted += best < target
    attained += best == target
    print("grid %-13s d=%d N_ball=%-3d |X|=%-3d s*=%-3d least support found=%-3d  (%d candidates)  %s" % (
        str(ks), d, N, size, target, best, trials, verdict), flush=True)
print()
print("cases: %d; candidates examined: %d; supports below s*: %d; cases in which s* was attained by the search: %d" % (
    len(CASES), total_trials, refuted, attained))
print("total elapsed %.1f s" % (time.time() - T0))
print("R12_02B_DONE")
