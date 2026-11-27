#!/usr/bin/env python3
"""Referee checks for Theorem E4 (Renyi-Heppes for r-determining features) and its sharpness construction."""
import itertools, sys
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(424242)


def fibre_is_point(T, mu):
    """T: (m, N) integer array of feature values on a finite X = range(N).  Is mu the only nu >= 0 with the
    same law of every feature?  LP: for every x, max and min of nu(x) over the fibre."""
    m, N = T.shape
    rows = []; rhs = []
    for j in range(m):
        for t in np.unique(T[j]):
            r = (T[j] == t).astype(float); rows.append(r); rhs.append(r @ mu)
    A = np.array(rows); b = np.array(rhs)
    S = np.nonzero(mu > 0)[0]
    # (1) max mass off S
    c = -np.ones(N); c[S] = 0
    res = linprog(c, A_eq=A, b_eq=b, bounds=[(0, None)] * N, method="highs")
    assert res.status == 0
    if -res.fun > 1e-8:
        return False, res.x
    for x in S:
        for s in (1, -1):
            c = np.zeros(N); c[x] = s
            res = linprog(c, A_eq=A, b_eq=b, bounds=[(0, None)] * N, method="highs")
            if abs(res.x[x] - mu[x]) > 1e-8:
                return False, res.x
    return True, None


def agree_count(T):
    m, N = T.shape
    worst = 0
    for x in range(N):
        worst = max(worst, int(np.max(np.sum(T == T[:, [x]], axis=0)[np.arange(N) != x], initial=0)))
    return worst            # family is r-determining iff worst < r


def affine_plane_family(q, m):
    """X = F_q^2, features: x + j*y (j = 0..q-1) and y.  Two distinct points agree on exactly one of the q+1."""
    pts = [(x, y) for x in range(q) for y in range(q)]
    feats = [[(x + j * y) % q for (x, y) in pts] for j in range(q)] + [[y for (x, y) in pts]]
    idx = rng.choice(q + 1, size=m, replace=False)
    return np.array([feats[i] for i in idx])


def moment_curve_family(q, m):
    """X = F_q^3, features: <(1,t,t^2), x> (t in F_q) and <(0,0,1), x>: any 3 are independent => 3-determining."""
    pts = list(itertools.product(range(q), repeat=3))
    P = np.array(pts)
    feats = [(P @ np.array([1, t, t * t])) % q for t in range(q)] + [P[:, 2] % q]
    idx = rng.choice(q + 1, size=m, replace=False)
    return np.array([feats[i] for i in idx])


def random_code_family(N, m, q, r, tries=4000):
    """random code of length m over an alphabet of size q, greedily pruned so that two words agree in < r places."""
    words = []
    for _ in range(tries):
        w = rng.integers(q, size=m)
        if all(np.sum(w == u) < r for u in words):
            words.append(w)
        if len(words) == N:
            break
    return np.array(words).T


def test_main_statement():
    """search for counterexamples to E4 at m = K(r-1)+1; and show failures at m = K(r-1)."""
    out = []
    tot = bad = 0; below = below_bad = 0
    # r = 2 : affine planes
    for q in (3, 5):
        for K in range(1, 4 if q == 3 else 5):
            for m, tag in ((K + 1, "at"), (K, "below")):
                if m > q + 1 or m < 1:
                    continue
                for _ in range(60):
                    T = affine_plane_family(q, m)
                    assert agree_count(T) < 2
                    N = T.shape[1]
                    S = rng.choice(N, size=K, replace=False)
                    mu = np.zeros(N); w = rng.random(K) + 0.1; mu[S] = w / w.sum()
                    if rng.random() < 0.5:
                        mu[S] = 1.0 / K
                    ok, _ = fibre_is_point(T, mu)
                    if tag == "at":
                        tot += 1; bad += (not ok)
                    else:
                        below += 1; below_bad += (not ok)
    out.append(f"r=2 (affine planes F_3^2, F_5^2): m = K+1: {bad} counterexamples in {tot}; m = K: non-unique in {below_bad}/{below}")
    # r = 3 : moment curve in F_5^3
    tot = bad = below = below_bad = 0
    q = 5
    for K in (1, 2):
        for m, tag in ((2 * K + 1, "at"), (2 * K, "below")):
            if m > q + 1:
                continue
            for _ in range(25):
                T = moment_curve_family(q, m)
                assert agree_count(T) < 3
                N = T.shape[1]
                S = rng.choice(N, size=K, replace=False)
                mu = np.zeros(N); mu[S] = 1.0 / K
                if rng.random() < 0.5:
                    w = rng.random(K) + 0.1; mu[S] = w / w.sum()
                ok, _ = fibre_is_point(T, mu)
                if tag == "at":
                    tot += 1; bad += (not ok)
                else:
                    below += 1; below_bad += (not ok)
    out.append(f"r=3 (moment curve in F_5^3): m = 2K+1: {bad} counterexamples in {tot}; m = 2K: non-unique in {below_bad}/{below}")
    # random codes
    tot = bad = 0
    for _ in range(300):
        r = int(rng.integers(2, 4)); K = int(rng.integers(1, 4)); m = K * (r - 1) + 1; q = int(rng.integers(2, 5))
        T = random_code_family(int(rng.integers(6, 30)), m, q, r)
        if T.ndim != 2 or T.shape[1] < K + 1:
            continue
        assert agree_count(T) < r
        N = T.shape[1]
        S = rng.choice(N, size=K, replace=False)
        mu = np.zeros(N); w = rng.random(K) + 0.1; mu[S] = w / w.sum()
        ok, _ = fibre_is_point(T, mu); tot += 1; bad += (not ok)
    out.append(f"random r-determining codes, m = K(r-1)+1: {bad} counterexamples in {tot}")
    return out


def sharpness(K, r, trials=3):
    """The report's construction: regular 2K-gon in a plane Pi of R^r, K(r-1) functionals theta_k + v_{k,i}."""
    res = []
    for _ in range(trials):
        ang = np.pi * np.arange(2 * K) / K
        V = np.zeros((2 * K, r)); V[:, 0] = np.cos(ang); V[:, 1] = np.sin(ang)
        A, B = V[0::2], V[1::2]
        # normals to the K classes of parallel edges: edge j joins vertex j and j+1; its normal is the bisector direction
        thetas = []
        for k in range(K):
            e = V[(k + 1) % (2 * K)] - V[k]
            thetas.append(np.array([-e[1], e[0]] + [0.0] * (r - 2)) / np.linalg.norm(e))
        W = []
        for k in range(K):
            for i in range(r - 1):
                v = np.zeros(r); v[2:] = rng.normal(size=r - 2)
                W.append(thetas[k] + v)
        W = np.array(W)                                    # K(r-1) x r
        # (1) r-determining on R^r  <=>  any r of the functionals are linearly independent
        mindet = min(abs(np.linalg.det(W[list(c)])) for c in itertools.combinations(range(len(W)), r))
        # (2) equal laws: multisets of <w, a> over the two colour classes
        worst = 0.0
        for w in W:
            worst = max(worst, np.max(np.abs(np.sort(A @ w) - np.sort(B @ w))))
        # (3) the two ensembles are different
        diff = min(np.linalg.norm(a - b) for a in A for b in B)
        res.append((mindet, worst, diff))
    return res


def explicit_r3_K2():
    """K = 2, r = 3 in R^3: square in the plane z = 0; four functionals (1,0,a), (1,0,b), (0,1,c), (0,1,d)."""
    a, b, c, d = 1.0, -1.0, 2.0, 0.5
    W = np.array([[1, 0, a], [1, 0, b], [0, 1, c], [0, 1, d]], dtype=float)
    A = np.array([[1, 1, 0], [-1, -1, 0]], dtype=float); B = np.array([[1, -1, 0], [-1, 1, 0]], dtype=float)
    dets = [np.linalg.det(W[list(cmb)]) for cmb in itertools.combinations(range(4), 3)]
    laws = [(sorted((A @ w).tolist()), sorted((B @ w).tolist())) for w in W]
    return dets, laws


if __name__ == "__main__":
    for line in test_main_statement():
        print("E4:", line)
    dets, laws = explicit_r3_K2()
    print("E4 sharpness, explicit K=2, r=3: 3x3 minors of the 4 functionals:", np.round(dets, 3).tolist())
    print("   laws under mu / nu per functional:", laws)
    for K, r in ((2, 2), (3, 2), (5, 2), (2, 3), (3, 3), (4, 3), (2, 4), (3, 4), (2, 5), (3, 5)):
        res = sharpness(K, r)
        print(f"E4 sharpness K={K}, r={r}: {K*(r-1)} functionals; min |det| over all r-subsets: "
              f"{min(x[0] for x in res):.2e}; max law mismatch: {max(x[1] for x in res):.1e}; "
              f"min distance between the two supports: {min(x[2] for x in res):.3f}")
