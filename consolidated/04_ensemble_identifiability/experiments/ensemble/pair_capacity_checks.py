#!/usr/bin/env python3
"""Numerical checks for Part III of docs/ensemble/ENSEMBLE_REPORT.md (pair data on the cube {-1,1}^n).

C1  Littlewood-Offord lemma used in Theorem E9: for c in R^K not of the form +-e_a,
    P(|<c, s>| = 1) <= 3/4 for a uniform sign vector s (exhaustive over a rational grid, exact arithmetic).
C2  Sign vectors in the span of K random sign vectors (exact enumeration): frequency of a spurious sign
    vector against Odlyzko's 4*C(K,3)*(3/4)^n.
C3  The projector certificate f(x) = |P_perp x|^2: on small cubes its zero set is +-S exactly when the span
    has no spurious sign vector, and then the fibre LP confirms that the ensemble is determined by its pair
    correlations among all ensembles; the gap min_{x not in +-S} f(x) is reported.
C4  Worst case: every 3 vertices of the cut polytope form a face (n = 5, 6, by LP); 4 vertices need not.
C5  Non-identifiability for K >= 6.34 n (uniform weights): sin(pi C / 2) is positive definite, so the pair
    correlations are those of a sign-of-Gaussian ensemble with full support.
C6  Adaptivity: pivoted Cholesky determines the pair-correlation matrix of a K-conformer ensemble from
    K n - K(K+1)/2 adaptively chosen entries; two two-conformer ensembles agree on all pairs but one.
Exit code 0 iff every check passes.
"""
import itertools, sys
from fractions import Fraction
from math import comb
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(20261128)


# ---------------------------------------------------------------- C1
def test_C1():
    grid = [Fraction(k, 2) for k in range(-4, 5)]
    worst = Fraction(0); worst_c = None; n_checked = 0
    for K in (2, 3, 4):
        signs = list(itertools.product((-1, 1), repeat=K))
        for c in itertools.product(grid, repeat=K):
            nz = [v for v in c if v != 0]
            if len(nz) <= 1:
                continue                      # c = 0 or a multiple of e_a (trivial when the multiple is +-1)
            hits = sum(1 for s in signs if abs(sum(a * b for a, b in zip(c, s))) == 1)
            p = Fraction(hits, len(signs)); n_checked += 1
            if p > worst:
                worst, worst_c = p, c
    # multiples of e_a other than +-e_a give probability 0
    return worst <= Fraction(3, 4), [f"    {n_checked} coefficient vectors with >= 2 non-zero entries: "
                                       f"largest probability {worst} at c = {tuple(str(v) for v in worst_c)}"]


# ---------------------------------------------------------------- C2
def spurious_count(S):
    """S: n x K sign matrix of rank K. Number of sign vectors in its column span other than +- columns (mod +-)."""
    n, K = S.shape
    # choose K independent rows
    rows = []
    for i in range(n):
        if np.linalg.matrix_rank(S[rows + [i]]) == len(rows) + 1:
            rows.append(i)
        if len(rows) == K:
            break
    B = S[rows].astype(float)
    eps = np.array(list(itertools.product((-1.0, 1.0), repeat=K - 1)))
    eps = np.hstack([np.ones((eps.shape[0], 1)), eps])              # mod global sign
    Cc = np.linalg.solve(B, eps.T)                                   # K x 2^{K-1}
    V = S @ Cc                                                       # n x 2^{K-1}
    good = np.all(np.abs(np.abs(V) - 1.0) < 1e-7, axis=0)
    trivial = np.sum(np.abs(Cc) > 1e-7, axis=0) == 1
    return int(np.sum(good & ~trivial))


def test_C2():
    out = []; ok = True
    for n, K, trials in ((16, 5, 4000), (20, 6, 4000), (24, 8, 2000), (30, 10, 1500), (36, 12, 600)):
        hit = 0; tot = 0
        while tot < trials:
            S = rng.choice((-1, 1), size=(n, K))
            if np.linalg.matrix_rank(S) < K:
                continue
            tot += 1; hit += spurious_count(S) > 0
        pred = 4 * comb(K, 3) * 0.75 ** n
        out.append(f"    n = {n}, K = {K}: spurious sign vector in {hit}/{tot} = {hit / tot:.4f}; "
                   f"4*C(K,3)*(3/4)^n = {pred:.4f}")
        # 4*C(K,3)*(3/4)^n is the expected number of spurious vectors of the dominant kind (a union bound),
        # so the frequency lies below it up to sampling error, and agrees with it only where it is small.
        # Where pred < 0.1 (the two sizes quoted in the report) the test is agreement within sampling error
        # plus the second-order term pred^2; elsewhere only "below, and of the same order" (review ER1, F18).
        se = 4 * np.sqrt(pred / tot) + 2 / tot
        if pred < 0.1:
            ok &= abs(hit / tot - pred) < se + pred ** 2
        else:
            ok &= 0.5 * pred < hit / tot < pred + se
    return ok, out


# ---------------------------------------------------------------- C3
def cube_mod_flip(n):
    X = np.array(list(itertools.product((-1, 1), repeat=n - 1)))
    return np.hstack([np.ones((X.shape[0], 1), dtype=int), X])       # first coordinate +1


def pair_features(X):
    n = X.shape[1]
    return np.array([X[:, i] * X[:, j] for i in range(n) for j in range(i + 1, n)], dtype=float)


def fibre_is_point(F, mu):
    N = F.shape[1]
    A_eq = np.vstack([np.ones((1, N)), F]); b_eq = A_eq @ mu
    # one LP: maximise the mass off the support; then check the weights on the support
    S = np.nonzero(mu > 0)[0]
    c = -np.ones(N); c[S] = 0
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * N, method="highs")
    if res.status != 0 or -res.fun > 1e-8:
        return False
    return np.linalg.matrix_rank(A_eq[:, S], tol=1e-9) == len(S)


def test_C3():
    out = []; ok = True
    n = 9; X = cube_mod_flip(n); F = pair_features(X)
    agree = tot = ident = 0; gaps = []
    for K in (2, 3, 4, 5, 6):
        for _ in range(40):
            idx = rng.choice(X.shape[0], size=K, replace=False)
            S = X[idx].T.astype(float)                               # n x K
            if np.linalg.matrix_rank(S) < K:
                continue
            P = S @ np.linalg.pinv(S)
            f = np.sum((X - X @ P) ** 2, axis=1)                     # |P_perp x|^2 for every x (mod flip)
            zero = np.nonzero(f < 1e-9)[0]
            cert = set(zero.tolist()) == set(idx.tolist())
            mu = np.zeros(X.shape[0]); w = rng.random(K) + 0.2; mu[idx] = w / w.sum()
            fib = fibre_is_point(F, mu)
            tot += 1; ident += fib
            # certificate => identified (the converse may fail: the certificate is sufficient only)
            agree += (not cert) or fib
            if cert:
                gaps.append(np.min(f[f > 1e-9]))
    out.append(f"    n = {n}: {tot} random supports (K = 2..6); certificate implies fibre is a point in {agree}/{tot}; "
               f"identified by the fibre LP: {ident}; smallest certificate gap: {min(gaps):.3f}")
    ok &= agree == tot and len(gaps) > 20
    return ok, out


# ---------------------------------------------------------------- C4
def is_face(F, idx):
    """exists a in R^{m+1}: a.(1,F(x)) = 0 for x in idx, >= 1 otherwise."""
    N = F.shape[1]
    G = np.vstack([np.ones((1, N)), F])
    comp = [x for x in range(N) if x not in idx]
    res = linprog(np.zeros(G.shape[0]), A_ub=-G[:, comp].T, b_ub=-np.ones(len(comp)),
                  A_eq=G[:, idx].T, b_eq=np.zeros(len(idx)), bounds=[(None, None)] * G.shape[0], method="highs")
    return res.status == 0


def test_C4():
    out = []; ok = True
    for n in (5, 6):
        X = cube_mod_flip(n); F = pair_features(X); N = X.shape[0]
        # by the switching symmetry of the cut polytope one vertex may be fixed: x = (1,...,1) is index N-1
        base = N - 1
        assert np.all(X[base] == 1)
        tri = [is_face(F, [base, i, j]) for i in range(N - 1) for j in range(i + 1, N - 1)]
        quad_idx = [(i, j, k) for i in range(N - 1) for j in range(i + 1, N - 1) for k in range(j + 1, N - 1)]
        if len(quad_idx) > 1500:
            sel = rng.choice(len(quad_idx), size=1500, replace=False); quad_idx = [quad_idx[t] for t in sel]
        quad = [is_face(F, [base, i, j, k]) for i, j, k in quad_idx]
        bad = next(((base,) + q for q, v in zip(quad_idx, quad) if not v), None)
        out.append(f"    n = {n}: triples containing a fixed vertex that are faces: {sum(tri)}/{len(tri)}; "
                   f"4-sets: {sum(quad)}/{len(quad)}"
                   + (f"; a 4-set that is not a face: {[''.join('+' if v > 0 else '-' for v in X[t]) for t in bad]}"
                      if bad else ""))
        ok &= all(tri) and (not all(quad))
    return ok, out


# ---------------------------------------------------------------- C5
def test_C5():
    out = []; ok = True
    n = 300
    for alpha in (2.0, 4.0, 5.5, 6.34, 7.0, 9.0, 12.0):
        K = int(alpha * n)
        X = rng.choice((-1.0, 1.0), size=(n, K))
        C = X @ X.T / K
        R = np.sin(np.pi * C / 2); np.fill_diagonal(R, 1.0)
        lam = np.linalg.eigvalsh(R)[0]
        x = np.sqrt(n / K); pred = 1 - (np.pi / 2) * (2 * x - x * x)
        out.append(f"    n = {n}, K = {alpha} n: smallest eigenvalue of sin(pi C/2) = {lam:+.4f} "
                   f"(first-order prediction {pred:+.4f})")
        if alpha >= 7.0:
            ok &= lam > 0
            # the Gaussian-sign ensemble reproduces C exactly: (2/pi) arcsin(R) = C
            ok &= np.max(np.abs(2 / np.pi * np.arcsin(np.clip(R, -1, 1)) - C)) < 1e-12
        if alpha <= 4.0:
            ok &= lam < 0
    return ok, out


# ---------------------------------------------------------------- C6
def adaptive_cholesky(oracle, n, tol=1e-9):
    """Pivoted Cholesky of an n x n PSD matrix with unit diagonal, reading entries through oracle(i, j).
    Returns the factor L (n x r), the list of pivots and the number of off-diagonal entries read."""
    d = np.ones(n); L = np.zeros((n, 0)); piv = []; read = set()
    while d.max() > tol:
        p = int(np.argmax(d)); piv.append(p)
        col = np.empty(n)
        for i in range(n):
            if i == p:
                col[i] = 1.0
            else:
                col[i] = oracle(i, p); read.add((min(i, p), max(i, p)))
        new = (col - L @ L[p]) / np.sqrt(d[p])
        L = np.hstack([L, new[:, None]])
        d = np.maximum(d - new ** 2, 0.0)
    return L, piv, len(read)


def test_C6():
    out = []; ok = True
    n = 60
    for K in (1, 2, 3, 5, 8):
        X = rng.choice((-1.0, 1.0), size=(n, K)); w = rng.random(K) + 0.2; w /= w.sum()
        C = (X * w) @ X.T
        L, piv, nread = adaptive_cholesky(lambda i, j: C[i, j], n)
        err = np.max(np.abs(L @ L.T - C)); r = np.linalg.matrix_rank(C, tol=1e-9)
        bound = r * n - r * (r + 1) // 2
        out.append(f"    n = {n}, {K} conformers (rank {r}): {nread} entries read (r n - r(r+1)/2 = {bound}; "
                   f"all pairs: {n * (n - 1) // 2}); reconstruction error {err:.1e}")
        ok &= err < 1e-8 and nread <= bound and len(piv) == r
    # non-adaptive lower bound: two two-conformer ensembles that differ only in the correlation of sites 0, 1
    n = 7; s = rng.choice((-1.0, 1.0), size=n - 2)
    A = [np.concatenate([[1, 1], s]), np.concatenate([[-1, -1], s])]
    B = [np.concatenate([[1, -1], s]), np.concatenate([[-1, 1], s])]
    CA = sum(np.outer(v, v) for v in A) / 2; CB = sum(np.outer(v, v) for v in B) / 2
    diff = np.argwhere(np.abs(CA - CB) > 1e-12)
    ok &= sorted(map(tuple, diff.tolist())) == [(0, 1), (1, 0)]
    out.append(f"    two two-conformer ensembles: their pair-correlation matrices differ exactly at {sorted(set(map(tuple, np.sort(diff, axis=1).tolist())))}")
    return ok, out


def main():
    allok = True
    for name, fn in (("C1 Littlewood-Offord lemma", test_C1), ("C2 sign vectors in random spans", test_C2),
                     ("C3 projector certificate", test_C3), ("C4 worst case (cut polytope)", test_C4),
                     ("C5 Gaussian rounding", test_C5), ("C6 adaptivity", test_C6)):
        ok, out = fn()
        print(f"{name}: {'ok' if ok else 'FAILED'}")
        for line in out:
            print(line)
        allok &= ok
    print("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
