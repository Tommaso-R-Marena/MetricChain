#!/usr/bin/env python3
"""Referee checks for Part III (E9-E12) and for the statements of the report's Section 5 about pair data."""
import itertools, sys, math
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(31415926)


_CUBE = {}


def cube_mod_flip(n):
    if n not in _CUBE:
        N = 1 << (n - 1)
        idx = np.arange(N)
        X = np.ones((N, n), dtype=int)
        for j in range(1, n):
            X[:, j] = np.where((idx >> (n - 1 - j)) & 1, 1, -1)
        _CUBE[n] = X
    return _CUBE[n]


def pair_features(X):
    n = X.shape[1]; iu = np.triu_indices(n, 1)
    return (X[:, iu[0]] * X[:, iu[1]]).astype(float)       # N x C(n,2)


def simplicial_face(G, idx):
    """G: N x (m+1) rows (1, phi(x)).  (i) independence on idx, (ii) certificate = 0 on idx, >= 1 elsewhere."""
    N = G.shape[0]
    if np.linalg.matrix_rank(G[idx], tol=1e-9) < len(idx):
        return False
    mask = np.ones(N, bool); mask[idx] = False
    if not mask.any():
        return True
    res = linprog(np.zeros(G.shape[1]), A_ub=-G[mask], b_ub=-np.ones(mask.sum()), A_eq=G[idx],
                  b_eq=np.zeros(len(idx)), bounds=[(None, None)] * G.shape[1], method="highs")
    return res.status == 0


def fibre_point(G, mu):
    """direct test: is mu the only probability vector with the same pair correlations?"""
    N = G.shape[0]; b = G.T @ mu
    S = np.nonzero(mu > 0)[0]
    c = -np.ones(N); c[S] = 0
    res = linprog(c, A_eq=G.T, b_eq=b, bounds=[(0, None)] * N, method="highs")
    if -res.fun > 1e-8:
        return False
    return np.linalg.matrix_rank(G[S], tol=1e-9) == len(S)


# ------------------------------------------------------------------ E9
def test_E9():
    out = []
    X = cube_mod_flip(4); G = np.hstack([np.ones((8, 1)), pair_features(X)])
    H = np.array([[1, 1, 1, 1], [1, -1, -1, 1], [1, -1, 1, -1], [1, 1, -1, -1]])
    idx = [int(np.nonzero((X == h).all(axis=1))[0][0]) for h in H]
    C = sum(np.outer(h, h) for h in H) / 4
    mu = np.zeros(8); mu[idx] = 0.25
    out.append(f"E9(b): C of the Hadamard ensemble = I: {np.allclose(C, np.eye(4))}; simplicial face: "
               f"{simplicial_face(G, idx)}; identified (fibre LP): {fibre_point(G, mu)}")
    for n in (4, 5, 6, 7):
        X = cube_mod_flip(n); G = np.hstack([np.ones((X.shape[0], 1)), pair_features(X)]); N = X.shape[0]
        base = N - 1
        tri = [simplicial_face(G, [base, i, j]) for i in range(N - 1) for j in range(i + 1, N - 1)]
        out.append(f"E9(a): n={n}: triples through a fixed vertex that are simplicial faces: {sum(tri)}/{len(tri)}")
    return out


# ------------------------------------------------------------------ Section 5.3 claim
def test_rank_claim():
    """'an identified K-conformer ensemble has correlation rank K' (report, Section 5, item 3) -- false."""
    out = []
    for n in (3, 4, 5):
        X = cube_mod_flip(n); G = np.hstack([np.ones((X.shape[0], 1)), pair_features(X)]); N = X.shape[0]
        best = None
        if n == 3:
            cands = [list(range(N))]
        elif n == 4:
            # vertices of the triangle facet x1x2 + x1x3 + x2x3 >= -1 with equality
            cands = [[k for k in range(N) if X[k, 0] * X[k, 1] + X[k, 0] * X[k, 2] + X[k, 1] * X[k, 2] == -1]]
        else:
            cands = [sorted(rng.choice(N, size=K, replace=False).tolist()) for K in (6, 7, 8) for _ in range(300)]
        for idx in cands:
            if simplicial_face(G, idx):
                r = np.linalg.matrix_rank(X[idx].astype(float))
                if len(idx) > r and (best is None or len(idx) - r > best[0] - best[1]):
                    best = (len(idx), r, idx)
        if best:
            K, r, idx = best
            mu = np.zeros(N); mu[idx] = 1.0 / K
            out.append(f"n={n}: identified ensemble with K={K} conformers and correlation rank {r} < K "
                       f"(fibre LP confirms identification: {fibre_point(G, mu)}); conformers: "
                       f"{[''.join('+' if v > 0 else '-' for v in X[k]) for k in idx]}")
    return out


# ------------------------------------------------------------------ E10
def sign_vectors_in_span(S):
    """S: n x K (+-1).  Returns (independent?, number of sign vectors in the span modulo +-, all found by
    brute force over the cube modulo flip -- an implementation independent of the report's)."""
    n, K = S.shape
    if np.linalg.matrix_rank(S) < K:
        return False, None
    P = S @ np.linalg.pinv(S)
    X = cube_mod_flip(n).astype(np.float64)
    f = n - np.einsum("ij,ij->i", X @ P, X)
    return True, int(np.sum(f < 1e-7))


def test_E10a(n=8, trials=150):
    X = cube_mod_flip(n); G = np.hstack([np.ones((X.shape[0], 1)), pair_features(X)])
    ok = bad = other = 0
    for _ in range(trials):
        K = int(rng.integers(2, n))
        S = rng.choice((-1, 1), size=(n, K))
        ind, cnt = sign_vectors_in_span(S)
        if not ind:
            continue
        idx = sorted(set(int(np.nonzero((X == (S[:, a] * S[0, a])).all(axis=1))[0][0]) for a in range(K)))
        onE = (cnt == K) and len(idx) == K
        # every ensemble supported on the conformers: full support with skewed weights AND a sub-support
        mu = np.zeros(X.shape[0]); w = rng.random(len(idx)) ** 4 + 1e-3; mu[idx] = w / w.sum()
        sub = idx[: max(1, len(idx) // 2)]
        mu2 = np.zeros(X.shape[0]); mu2[sub] = 1.0 / len(sub)
        a = fibre_point(G, mu) and fibre_point(G, mu2)
        if onE:
            ok += a; bad += (not a)
        else:
            other += 1
    return f"E10(a): n={n}: on the event E: identified (two weightings incl. a sub-support) in {ok}, failures {bad}; off E: {other} supports"


def lemma1_random(trials=200000):
    worst = 0.0
    for _ in range(trials):
        K = int(rng.integers(2, 7))
        kind = rng.integers(4)
        if kind == 0:
            c = rng.integers(-3, 4, size=K).astype(float)
        elif kind == 1:
            c = rng.integers(-4, 5, size=K) / 2.0
        elif kind == 2:
            c = rng.integers(-6, 7, size=K) / 3.0
        else:
            c = rng.choice([0, 1, -1, 2, 0.5, 1 / 3, 2 / 3], size=K)
        nz = np.count_nonzero(c)
        if nz == 0 or (nz == 1 and abs(abs(c[np.nonzero(c)[0][0]]) - 1) < 1e-12):
            continue
        Sg = np.array(list(itertools.product((-1, 1), repeat=K)))
        p = np.mean(np.abs(np.abs(Sg @ c) - 1) < 1e-9)
        worst = max(worst, p)
    return f"E10 Lemma 1: largest P(|<c,s>| = 1) over {trials} random rational c (not +-e_a): {worst:.4f} (claim <= 0.75)"


def lemma2_sim(trials=20000):
    out = []
    for K, t in ((3, 0), (3, 2), (5, 1), (6, 3), (8, 2)):
        fail = 0
        for _ in range(trials):
            M = rng.choice((-1, 1), size=(K + t, K))
            fail += np.linalg.matrix_rank(M) < K
        out.append(f"K={K},t={t}: P(rank<K)={fail / trials:.4f} <= 2^-t={2.0 ** -t:.4f}")
    return "E10 Lemma 2: " + "; ".join(out)


def test_E10b(trials=3000):
    out = []
    for n, K in ((12, 3), (14, 3), (14, 4), (16, 4)):
        bad = dep = 0
        for _ in range(trials):
            S = rng.choice((-1, 1), size=(n, K))
            ind, cnt = sign_vectors_in_span(S)
            if not ind:
                bad += 1; dep += 1
            elif cnt != K:
                bad += 1
        bound = min(2.0 ** -t + 2.0 ** (K + t) * 0.75 ** (n - K - t) for t in range(0, n - K + 1))
        out.append(f"n={n},K={K}: P(E^c)={bad / trials:.4f} (dependent: {dep / trials:.4f}); 4C(K,3)(3/4)^n="
                   f"{4 * math.comb(K, 3) * 0.75 ** n:.4f}; bound (b) min over t = {bound:.3f}")
    return "E10(b),(c): " + " | ".join(out)


# ------------------------------------------------------------------ E11
def test_E11():
    out = []
    n = 6
    X = cube_mod_flip(n); F = pair_features(X); N = X.shape[0]
    iu = np.triu_indices(n, 1)
    for K in (40, 80):
        S = rng.choice((-1.0, 1.0), size=(n, K)); C = S @ S.T / K
        R = np.sin(np.pi * C / 2); np.fill_diagonal(R, 1.0)
        lam = np.linalg.eigvalsh(R)[0]
        msg = f"n={n}, K={K}: lambda_min(sin(pi C/2)) = {lam:+.3f}"
        if lam > 1e-6:
            g = rng.multivariate_normal(np.zeros(n), R, size=2_000_000)
            s = np.sign(g); Chat = s.T @ s / len(s)
            msg += f"; max |corr(sign g) - C| = {np.max(np.abs(Chat - C)):.1e} (MC error ~ {1 / np.sqrt(len(s)):.0e})"
            # all 2^n sign patterns occur?
            keys = ((s > 0) @ (1 << np.arange(n))).astype(int)
            msg += f"; distinct sign patterns observed: {len(np.unique(keys))}/{2 ** n}"
        # exact: is C in the interior of the cut polytope?  max t : sum nu_x phi(x) = C, nu_x >= t
        A_eq = np.vstack([np.ones((1, N)), F.T]); A_eq = np.hstack([A_eq, np.zeros((A_eq.shape[0], 1))])
        b_eq = np.concatenate([[1.0], C[iu]])
        A_ub = np.hstack([-np.eye(N), np.ones((N, 1))])
        c = np.zeros(N + 1); c[-1] = -1
        res = linprog(c, A_ub=A_ub, b_ub=np.zeros(N), A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * N + [(None, None)],
                      method="highs")
        msg += f"; LP: largest t with a representation nu >= t on all of the cube: {res.x[-1]:.4f}"
        # other weights on the SAME support
        w = rng.random(K) ** 3 + 1e-3; w /= w.sum(); Cw = (S * w) @ S.T
        b_eq = np.concatenate([[1.0], Cw[iu]])
        res = linprog(c, A_ub=A_ub, b_ub=np.zeros(N), A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * N + [(None, None)],
                      method="highs")
        msg += f"; same for skewed weights on the same conformers: {res.x[-1]:.4f}"
        out.append("E11: " + msg)
    return out


# ------------------------------------------------------------------ capacity: Cover's count gives alpha <= 2
def separable_site(Xs, v):
    """is the dichotomy -x^a_v of the points x^a_{-v} strictly homogeneously linearly separable?"""
    K, n = Xs.shape
    js = [j for j in range(n) if j != v]
    A = (Xs[:, [v]] * Xs[:, js]).astype(float)        # need  A q <= -1
    res = linprog(np.zeros(n - 1), A_ub=A, b_ub=-np.ones(K), bounds=[(None, None)] * (n - 1), method="highs")
    return res.status == 0


def test_capacity(ns=(9, 10, 11), trials=60):
    out = []
    for n in ns:
        X = cube_mod_flip(n); G = np.hstack([np.ones((X.shape[0], 1)), pair_features(X)]); N = X.shape[0]
        row = []
        for alpha in (0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0):
            K = int(round(alpha * n)); face = nec = 0
            for _ in range(trials):
                idx = rng.choice(N, size=K, replace=False)
                fc = simplicial_face(G, idx)
                sep = all(separable_site(X[idx], v) for v in range(n))
                assert (not fc) or sep or any(np.sum(X[i] != X[j]) in (1, n - 1) for i in idx for j in idx if i < j), \
                    "face without single-flip separability"
                face += fc; nec += sep
            cover = sum(math.comb(K - 1, i) for i in range(0, n - 1)) * 2.0 / 2 ** K
            row.append(f"K/n={alpha}: face {face / trials:.2f}, all sites separable {nec / trials:.2f}, "
                       f"Cover bound for one site {min(1.0, cover):.2f}")
        out.append(f"capacity n={n} ({trials} trials): " + " | ".join(row))
    return out


def cover_bound_large():
    out = []
    for n in (50, 200, 1000):
        for alpha in (2.0, 2.2, 2.5, 3.0):
            K = int(alpha * n)
            # P(one fixed site separable) <= P(Bin(K-1,1/2) <= n-2)
            logp = math.log(sum(Fraction(math.comb(K - 1, i), 2 ** (K - 1)) for i in range(0, n - 1)) + Fraction(1, 10 ** 300))
            out.append(f"n={n},K={alpha}n: ln P <= {logp:.1f}")
    return "Cover/Schlaefli bound P(Bin(K-1,1/2) <= n-2) for one site: " + "; ".join(out)


# ------------------------------------------------------------------ E12
def test_E12a():
    bad = 0; tot = 0
    for n in range(2, 8):
        for i, j in itertools.combinations(range(n), 2):
            s = rng.choice((-1, 1), size=n)
            def ens(sign):
                a = s.copy(); a[i] = 1; a[j] = sign
                b = s.copy(); b[i] = -1; b[j] = -sign
                return (np.outer(a, a) + np.outer(b, b)) / 2, {tuple(a * a[0]), tuple(b * b[0])}
            Cp, Sp = ens(1); Cm, Sm = ens(-1)
            D = np.abs(Cp - Cm) > 1e-12
            exp = np.zeros((n, n), bool); exp[i, j] = exp[j, i] = True
            tot += 1; bad += not (np.array_equal(D, exp) and Sp != Sm and len(Sp) <= 2 and len(Sm) <= 2)
    return f"E12(a): {tot} (n, pair) cases, n = 2..7: mu_+ and mu_- differ exactly on the pair and are different modulo flip; failures: {bad}"


def pivoted_cholesky_exact(C, rule):
    """exact rational pivoted Cholesky (outer-product form), reading whole columns; returns (#entries read, ok, r)."""
    n = len(C)
    R = [[Fraction(0)] * n for _ in range(n)]            # reconstructed matrix sum of rank-one terms
    d = [Fraction(1)] * n
    read = set(); terms = []
    while any(x > 0 for x in d):
        cand = [i for i in range(n) if d[i] > 0]
        p = cand[0] if rule == "first" else (cand[-1] if rule == "last" else max(cand, key=lambda i: d[i]))
        col = []
        for i in range(n):
            if i != p:
                read.add((min(i, p), max(i, p)))
            col.append(C[i][p] - R[i][p])                # residual column: needs only column p of C
        piv = col[p]
        assert piv == d[p] and piv > 0
        for i in range(n):
            for j in range(n):
                R[i][j] += col[i] * col[j] / piv
        d = [C[i][i] - R[i][i] for i in range(n)]
        assert all(x >= 0 for x in d), "negative residual diagonal: matrix not PSD"
        terms.append(p)
    ok = all(R[i][j] == C[i][j] for i in range(n) for j in range(n))
    return len(read), ok, len(terms)


def test_E12b():
    out = []; allok = True
    n = 10
    for name in ("3 conformers", "soft: all sign vectors with x_{2k}=x_{2k+1} (rank 5, 32 states, random weights)",
                 "soft: x_3 = x_1 x_2 on 3 blocks... full rank", "dependent conformers (K=6, rank 4)"):
        if name.startswith("3"):
            S = [rng.choice((-1, 1), size=n) for _ in range(3)]; w = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)]
        elif name.startswith("soft: all"):
            S = []
            for bits in itertools.product((-1, 1), repeat=n // 2):
                S.append(np.repeat(bits, 2))
            ww = rng.integers(1, 50, size=len(S)); w = [Fraction(int(v), int(ww.sum())) for v in ww]
        elif name.startswith("soft: x_3"):
            S = [np.array(x) for x in itertools.product((-1, 1), repeat=n) if x[2] == x[0] * x[1]]
            ww = rng.integers(1, 50, size=len(S)); w = [Fraction(int(v), int(ww.sum())) for v in ww]
        else:
            B = [rng.choice((-1, 1), size=n) for _ in range(3)]
            a, b, c = B
            maj = np.sign(a + b + c).astype(int)                 # a 4th sign vector in span{a,b,c}?  only if a+b+c has no +-3
            S = [a, b, c, -a, rng.choice((-1, 1), size=n), a * 1]
            w = [Fraction(1, 6)] * 6
        C = [[sum(wk * int(s[i]) * int(s[j]) for wk, s in zip(w, S)) for j in range(n)] for i in range(n)]
        r = np.linalg.matrix_rank(np.array(C, dtype=float), tol=1e-9)
        for rule in ("first", "last", "max"):
            nread, ok, steps = pivoted_cholesky_exact(C, rule)
            good = ok and steps == r and nread == r * n - r * (r + 1) // 2
            allok &= good
        out.append(f"E12(b) [{name}]: rank {r}; entries read {nread} = rn - r(r+1)/2 = {r * n - r * (r + 1) // 2}; "
                   f"exact reconstruction with three pivot rules: {good}")
    return out, allok


def cover_count(points):
    """number of strictly homogeneously separable dichotomies of the given points, by LP over all labelings."""
    K, D = points.shape; cnt = 0
    for lab in itertools.product((-1, 1), repeat=K - 1):
        y = np.array((1,) + lab)
        res = linprog(np.zeros(D), A_ub=-(y[:, None] * points), b_ub=-np.ones(K), bounds=[(None, None)] * D, method="highs")
        cnt += 2 * (res.status == 0)
    return cnt


def test_E12c():
    out = []
    worst = -10 ** 9
    for _ in range(40):
        K = int(rng.integers(3, 10)); D = int(rng.integers(1, 5))
        pts = rng.choice((-1.0, 1.0), size=(K, D))               # sign points: far from general position
        cnt = cover_count(pts); bound = 2 * sum(math.comb(K - 1, i) for i in range(D))
        worst = max(worst, cnt - bound)
    out.append(f"E12(c): Cover/Schlaefli bound for sign points NOT in general position: max(count - bound) = {worst} (must be <= 0)")
    H = lambda b: -b * math.log(b) - (1 - b) * math.log(1 - b)
    def bracket(beta, gamma):
        return beta * math.log(math.e / (beta * gamma)) + H(beta) - math.log(2)
    out.append("E12(c): exponent beta ln(en/(beta K)) + H(beta) - ln 2 at gamma = 1/4: " +
               ", ".join(f"beta={b}: {bracket(b, 0.25):+.4f}" for b in (0.05, 0.08, 0.083, 0.085, 0.09, 0.1)))
    # largest beta with a negative bracket
    for gamma in (1.0, 0.5, 0.25, 0.1, 0.01):
        lo, hi = 1e-6, 0.5
        for _ in range(60):
            mid = (lo + hi) / 2
            if bracket(mid, gamma) < 0: lo = mid
            else: hi = mid
        out.append(f"   gamma = K/n = {gamma}: largest admissible beta = {lo:.4f};  beta*ln(e/gamma) = {lo * math.log(math.e / gamma):.3f}")
    # exact (non-asymptotic) union bound n*C(n-1,D)*2*sum_{i<D} C(K-1,i)/2^K at gamma = 1/4, beta = 0.08
    for K in (100, 400, 1000, 4000):
        n = 4 * K; D = int(0.08 * K)
        lg = math.log(n) + math.lgamma(n) - math.lgamma(D + 1) - math.lgamma(n - D) + \
            math.log(2 * sum(math.comb(K - 1, i) for i in range(D))) - K * math.log(2)
        out.append(f"   exact union bound at gamma=1/4, beta=0.08, K={K}: ln(bound) = {lg:.1f}")
    return out


if __name__ == "__main__":
    parts = sys.argv[1:] or ["e9", "rank", "e10", "e11", "e12", "cap"]
    if "e9" in parts:
        for line in test_E9():
            print(line, flush=True)
    if "rank" in parts:
        for line in test_rank_claim():
            print("Sec.5(3) counterexample:", line, flush=True)
    if "e10" in parts:
        print(test_E10a(), flush=True)
        print(lemma1_random(), flush=True)
        print(lemma2_sim(), flush=True)
        print(test_E10b(), flush=True)
    if "e11" in parts:
        for line in test_E11():
            print(line, flush=True)
        print(cover_bound_large(), flush=True)
    if "e12" in parts:
        print(test_E12a(), flush=True)
        o, ok = test_E12b()
        for line in o:
            print(line, flush=True)
        for line in test_E12c():
            print(line, flush=True)
    if "cap" in parts:
        for line in test_capacity():
            print(line, flush=True)
