#!/usr/bin/env python3
"""R12 item 2 — brute-force test of the support-fraction claim used in Proposition 11.18e(c):

    "A function of order below m that is not identically zero is non-zero on a fraction at
     least k^{-(m-1)} of the configurations (k states at every site ...; attained by the
     indicator of a cylinder on m - 1 sites)."

and of two other claims of the proposition: the dimension N_ball and the unisolvence of the
Hamming ball of radius m - 1 around EVERY reference.

Notation: grid = (k_1, ..., k_n); d = m - 1; P_d = span of functions of at most d sites;
N = dim P_d.  Conjectured least support (R12, for unequal alphabets):

    s*(grid, d) = product of the n - d smallest k_i   (fraction 1 / product of the d largest k_i).

Two exhaustive methods, both exact.

PRIMAL (hyperplanes).  The zero set of a non-zero h in P_d of least support is a maximal
proper flat of the evaluation vectors; it is spanned by N - 1 independent points.  State
relabellings act transitively on the grid and preserve P_d, so the largest zero set may be
assumed to contain the origin.  We enumerate every (N-2)-subset B' of the other points, compute the
integer null vector of the (N-1) x N evaluation matrix of {0} + B' by cofactors (0/1 matrices,
determinants rounded to integers, |det| << 2^53), form h on the whole grid in integer
arithmetic and count its zeros.  The least support is |X| - (largest number of zeros).

DUAL (spark).  h in P_d  <=>  (I - Pi) h = 0 with Pi the orthogonal projector on P_d.  A non-zero
h in P_d supported inside S exists iff the principal submatrix (I - Pi)[S, S] is singular.  We
enumerate every subset S of size s* - 1 containing the origin (transitivity again) and check
that the least eigenvalue of (I - Pi)[S, S] is positive.  (D^w det is a non-zero integer for
D = prod k_i, w = |S|, and all eigenvalues are <= 1, so a non-singular submatrix has least
eigenvalue >= D^{-w}; the threshold used is 1e-11 and D^{-w} is printed.)  Then no non-zero
member of P_d has support smaller than s*, and the cylinder on the d largest sites has support
exactly s*.

One command:  python3 r12_02_support.py
"""
import itertools
import math
import sys
import time

import numpy as np

T0 = time.time()
BUDGET_PRIMAL = 2.0e8   # subsets x N (determinants)
BUDGET_DUAL = 6.0e7     # subsets
CHUNK = 100000


def grid_points(ks):
    return np.array(list(itertools.product(*[range(k) for k in ks])), dtype=np.int64)


def basis_matrix(ks, d):
    """E[x, (U, s)] = prod_{i in U} [x_i = s_i], |U| <= d, s_i != 0: the cylinder basis of P_d."""
    X = grid_points(ks)
    n = len(ks)
    cols = []
    labels = []
    for size in range(0, min(d, n) + 1):
        for U in itertools.combinations(range(n), size):
            for s in itertools.product(*[range(1, ks[i]) for i in U]):
                col = np.ones(len(X), dtype=np.int64)
                for i, si in zip(U, s):
                    col &= (X[:, i] == si)
                cols.append(col)
                labels.append((U, s))
    return X, np.stack(cols, axis=1), labels


def n_ball(ks, d):
    n = len(ks)
    return sum(math.prod(ks[i] - 1 for i in U) for size in range(0, min(d, n) + 1)
               for U in itertools.combinations(range(n), size))


def projector(ks, d):
    """Orthogonal projector on P_d: sum over |U| <= d of tensor_i (i in U ? I - J/k_i : J/k_i)."""
    n = len(ks)
    size = math.prod(ks)
    Pi = np.zeros((size, size))
    for sz in range(0, min(d, n) + 1):
        for U in itertools.combinations(range(n), sz):
            M = np.ones((1, 1))
            for i in range(n):
                J = np.ones((ks[i], ks[i])) / ks[i]
                M = np.kron(M, (np.eye(ks[i]) - J) if i in U else J)
            Pi += M
    return Pi


def comb_chunks(pool, r, chunk):
    it = itertools.combinations(pool, r)
    while True:
        block = list(itertools.islice(it, chunk))
        if not block:
            return
        yield np.array(block, dtype=np.int64).reshape(len(block), r)


def primal(ks, d):
    X, E, _ = basis_matrix(ks, d)
    size, N = E.shape
    if N == 1:
        return size, 1, 0  # constants: support = everything
    if N == size:
        return 1, 0, 0
    Ef = E.astype(float)
    best_zeros = 0
    count = 0
    dependent = 0
    for block in comb_chunks(range(1, size), N - 2, CHUNK):
        idx = np.concatenate([np.zeros((len(block), 1), dtype=np.int64), block], axis=1)
        M = Ef[idx]                       # (b, N-1, N)
        nv = np.empty((len(block), N))
        for j in range(N):
            cols = [c for c in range(N) if c != j]
            nv[:, j] = ((-1) ** j) * np.linalg.det(M[:, :, cols])
        nvi = np.rint(nv).astype(np.int64)
        assert np.max(np.abs(nv - nvi)) < 1e-6
        h = nvi @ E.T                     # (b, size) exact integers
        nonzero_vec = np.any(nvi != 0, axis=1)
        zeros = np.sum(h == 0, axis=1)
        zeros = np.where(nonzero_vec, zeros, -1)
        dependent += int(np.sum(~nonzero_vec))
        best_zeros = max(best_zeros, int(zeros.max()))
        count += len(block)
    return size - best_zeros, count, dependent


def dual(ks, d, s_star):
    size = math.prod(ks)
    Mfull = np.eye(size) - projector(ks, d)
    w = s_star - 1
    if w <= 0:
        return True, 0, None
    count = 0
    min_eig = math.inf
    for block in comb_chunks(range(1, size), w - 1, CHUNK):
        idx = np.concatenate([np.zeros((len(block), 1), dtype=np.int64), block], axis=1)
        sub = Mfull[idx[:, :, None], idx[:, None, :]]
        ev = np.linalg.eigvalsh(sub)[:, 0]
        min_eig = min(min_eig, float(ev.min()))
        count += len(block)
    return (min_eig > 1e-11), count, min_eig


def cylinder_support(ks, d):
    order = sorted(range(len(ks)), key=lambda i: -ks[i])
    top = order[:d]
    return math.prod(ks[i] for i in range(len(ks)) if i not in top)


def ball(X, x0, radius):
    return np.nonzero(np.sum(X != x0, axis=1) <= radius)[0]


print("=" * 118)
print("PART 1 — dimension N_ball and unisolvence of the Hamming ball of radius d = m - 1 around EVERY reference")
print("=" * 118)
grids_small = [(2, 2), (2, 3), (3, 3), (2, 4), (3, 4), (4, 4), (2, 2, 2), (2, 2, 3), (2, 3, 3), (3, 3, 3),
               (2, 3, 4), (2, 4, 4), (3, 3, 4), (3, 4, 4), (4, 4, 4), (2, 2, 2, 2), (2, 2, 2, 3), (2, 2, 3, 3),
               (2, 3, 3, 3), (3, 3, 3, 3), (2, 2, 3, 4), (2, 3, 4, 4), (2, 2, 2, 2, 2), (2, 2, 2, 2, 3)]
bad = 0
checked = 0
for ks in grids_small:
    n = len(ks)
    for d in range(0, n + 1):
        X, E, _ = basis_matrix(ks, d)
        N = E.shape[1]
        assert N == n_ball(ks, d)
        rank_all = np.linalg.matrix_rank(E.astype(float))
        ok_dim = (rank_all == N)
        ok_ball = True
        for x0 in X:
            b = ball(X, x0, d)
            if len(b) != N or np.linalg.matrix_rank(E[b].astype(float)) != N:
                ok_ball = False
        checked += 1
        if not (ok_dim and ok_ball):
            bad += 1
            print("  FAIL", ks, "d =", d, "dim ok:", ok_dim, "ball unisolvent for every reference:", ok_ball)
print("grids x orders checked: %d; failures: %d  (dimension of the span = N_ball = size of the ball, and the "
      "ball around every one of the |X| references has an invertible evaluation matrix)" % (checked, bad))

# how special is the ball?  count unisolvent N-subsets in two tiny cases
for ks, d in (((2, 2, 2), 1), ((2, 2, 2), 2), ((3, 3), 1), ((2, 2, 3), 1)):
    X, E, _ = basis_matrix(ks, d)
    N = E.shape[1]
    tot = uni = 0
    for S in itertools.combinations(range(len(X)), N):
        tot += 1
        if abs(np.linalg.det(E[list(S)].astype(float))) > 0.5:
            uni += 1
    print("  grid %s, d = %d: N_ball = %d; unisolvent N-subsets: %d of %d (the |X| = %d Hamming balls are among them)" % (
        ks, d, N, uni, tot, len(X)))
print("elapsed %.1f s" % (time.time() - T0))

print()
print("=" * 118)
print("PART 2 — least support of a non-zero function of order <= d (exhaustive); conjecture s* = product of the n - d "
      "smallest k_i")
print("=" * 118)
grids = [(2, 2), (2, 3), (2, 4), (3, 3), (3, 4), (4, 4),
         (2, 2, 2), (2, 2, 3), (2, 2, 4), (2, 3, 3), (2, 3, 4), (2, 4, 4), (3, 3, 3), (3, 3, 4), (3, 4, 4), (4, 4, 4),
         (2, 2, 2, 2), (2, 2, 2, 3), (2, 2, 2, 4), (2, 2, 3, 3), (2, 2, 3, 4), (2, 2, 4, 4), (2, 3, 3, 3), (2, 3, 3, 4),
         (2, 3, 4, 4), (2, 4, 4, 4), (3, 3, 3, 3), (3, 3, 3, 4), (3, 3, 4, 4), (3, 4, 4, 4), (4, 4, 4, 4),
         (2, 2, 2, 2, 2), (2, 2, 2, 2, 3)]
rows = []
n_done = n_skipped = n_refuted = 0
for ks in grids:
    n = len(ks)
    size = math.prod(ks)
    for d in range(0, n + 1):
        N = n_ball(ks, d)
        s_star = cylinder_support(ks, d)
        frac_equal_k = max(ks) ** (-d)          # the report's k^{-(m-1)} read with k = largest alphabet
        t1 = time.time()
        cost_primal = math.comb(size - 1, N - 2) * N if 2 <= N < size else 1
        cost_dual = math.comb(size - 1, max(s_star - 2, 0)) if s_star >= 2 else 1
        if d == 0:
            res, method, cnt = size, "trivial (constants)", 0
        elif d >= n:
            res, method, cnt = 1, "trivial (all functions)", 0
        elif cost_dual <= BUDGET_DUAL and cost_dual * 5 <= cost_primal:
            ok, cnt, mineig = dual(ks, d, s_star)
            res = s_star if ok else -1
            method = "dual  (least eigenvalue %.2e; D^-w = %.1e)" % (mineig if mineig is not None else float("nan"),
                                                                    float(size) ** (-(s_star - 1)))
        elif cost_primal <= BUDGET_PRIMAL:
            res, cnt, dep = primal(ks, d)
            method = "primal (%d dependent subsets skipped)" % dep
        elif cost_dual <= BUDGET_DUAL:
            ok, cnt, mineig = dual(ks, d, s_star)
            res = s_star if ok else -1
            method = "dual  (least eigenvalue %.2e; D^-w = %.1e)" % (mineig, float(size) ** (-(s_star - 1)))
        else:
            res, method, cnt = None, "NOT DONE (primal %.1e, dual %.1e subsets)" % (cost_primal / max(N, 1), cost_dual), 0
        dt = time.time() - t1
        if res is None:
            n_skipped += 1
            verdict = "skipped"
        else:
            n_done += 1
            if res == s_star:
                verdict = "= s*"
            else:
                verdict = "REFUTED (least support %s, s* = %d)" % (res, s_star)
                n_refuted += 1
        rows.append((ks, d, N, size, s_star, res, verdict, method, cnt, dt))
        print("grid %-16s d=%d (m=%d) N_ball=%-4d |X|=%-4d s*=%-4d least support=%-5s fraction=%-9s k_max^-d=%-9.4g %-8s %s, %d subsets, %.1f s" % (
            str(ks), d, d + 1, N, size, s_star, str(res),
            ("%.5f" % (res / size)) if res else "-", frac_equal_k, verdict, method, cnt, dt), flush=True)
print()
print("cases done exhaustively: %d; skipped (too large for the budget): %d; refutations of s*: %d" % (
    n_done, n_skipped, n_refuted))
viol_report = [r for r in rows if r[5] is not None and r[5] / r[3] < max(r[0]) ** (-r[1]) - 1e-12]
print("cases in which the least support fraction is below k_max^{-(m-1)} (the report's bound read with k = largest "
      "alphabet): %d" % len(viol_report))
strict = [r for r in rows if r[5] is not None and 0 < r[1] < len(r[0]) and r[5] / r[3] > max(r[0]) ** (-r[1]) + 1e-12]
print("cases (0 < d < n) in which the least fraction is strictly ABOVE k_max^{-(m-1)} (unequal alphabets: the right "
      "constant is 1/(product of the m-1 largest k_i)): %d" % len(strict))
for r in strict[:8]:
    print("   e.g. grid %s d=%d: least fraction %.5f = 1/%d  >  k_max^-d = %.5f" % (
        r[0], r[1], r[5] / r[3], r[3] // r[5], max(r[0]) ** (-r[1])))
print("total elapsed %.1f s" % (time.time() - T0))
print("R12_02_DONE")
