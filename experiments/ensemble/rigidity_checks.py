#!/usr/bin/env python3
"""Numerical checks for Part II of docs/ensemble/ENSEMBLE_REPORT.md (laws of observables; ensemble rigidity).

R1  Rigidity matroids: rank function from the rigidity matrix at a random configuration; connectivity
    test r(J) + r(E \\ J) > r(E) for every proper non-empty J.
R2  Chimeras for complete graphs K_{d+2} in R^d (Cayley-Menger determinant): for random conformers every
    non-constant splice of their squared edge lengths has a non-zero Cayley-Menger determinant, hence is
    not realisable.  K = 2 and K = 3 conformers; d = 2 and d = 3.
R3  Chimeras for a globally rigid graph that is not complete (the wheel W_5 in the plane): least squares
    from many starts never realises a non-constant splice.
R4  Negative controls: (a) the triangle in the plane (globally rigid, 3 < d + 2 vertices, free matroid):
    splices are realisable and two different two-conformer ensembles have the same edge-length laws;
    (b) K_4 plus a vertex of degree two (two coloops): realisable chimeras.
R5  The explicit dual certificate f(p) = sum_e prod_i (l_e(p)^2 - l_e(x_i)^2)^2 for K_4 in the plane:
    every zero found by multi-start minimisation has the edge lengths of one of the conformers.
R6  Two toy feature maps R^2 -> R^4: connected matroid (no splice on the variety) and a direct sum
    (every splice realisable).
Exit code 0 iff every check passes.
"""
import itertools, sys
import numpy as np
from scipy.optimize import least_squares

rng = np.random.default_rng(20261127)


def edges_complete(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def sqlen(p, E):
    return np.array([np.sum((p[i] - p[j]) ** 2) for i, j in E])


def rigidity_matrix(p, E):
    n, d = p.shape
    R = np.zeros((len(E), n * d))
    for k, (i, j) in enumerate(E):
        R[k, i * d:(i + 1) * d] = p[i] - p[j]
        R[k, j * d:(j + 1) * d] = p[j] - p[i]
    return R


def rank_fn(E, n, d):
    p = rng.normal(size=(n, d))
    R = rigidity_matrix(p, E)
    cache = {}

    def r(J):
        J = tuple(sorted(J))
        if J not in cache:
            cache[J] = 0 if not J else int(np.linalg.matrix_rank(R[list(J)], tol=1e-9))
        return cache[J]
    return r


def matroid_connected(E, n, d):
    r = rank_fn(E, n, d)
    m = len(E); full = r(range(m))
    for mask in range(1, 2 ** (m - 1)):          # J and its complement: fix element m-1 in the complement
        J = [k for k in range(m) if mask >> k & 1]
        Jc = [k for k in range(m) if not mask >> k & 1]
        if r(J) + r(Jc) == full:
            return False, full
    return True, full


def cayley_menger(sq, n):
    """sq: dict/array of squared distances in the order of edges_complete(n)."""
    D = np.zeros((n, n)); E = edges_complete(n)
    for k, (i, j) in enumerate(E):
        D[i, j] = D[j, i] = sq[k]
    M = np.ones((n + 1, n + 1)); M[0, 0] = 0; M[1:, 1:] = D
    return np.linalg.det(M)


def test_R1():
    ok = True
    out = []
    K4 = edges_complete(4); K5 = edges_complete(5); K3 = edges_complete(3)
    wheel = [(0, i) for i in range(1, 6)] + [(i, i % 5 + 1) for i in range(1, 6)]
    k4pend = K4 + [(4, 0), (4, 1)]
    diamond = [e for e in K4 if e != (2, 3)]
    cases = [("K4 in R^2", K4, 4, 2, True, 5), ("K5 in R^3", K5, 5, 3, True, 9),
             ("wheel W5 in R^2", wheel, 6, 2, True, 9), ("K3 in R^2", K3, 3, 2, False, 3),
             ("K4 + degree-2 vertex in R^2", k4pend, 5, 2, False, 7), ("K4 - e in R^2", diamond, 4, 2, False, 5),
             ("K5 in R^2", K5, 5, 2, True, 7), ("K6 in R^3", edges_complete(6), 6, 3, True, 12)]
    for name, E, n, d, expect, rk in cases:
        c, full = matroid_connected(E, n, d)
        out.append(f"    {name}: rank {full}, connected = {c}")
        ok &= (c == expect) and (full == rk)
    return ok, out


def test_R2():
    ok = True; out = []
    for d, n, K in ((2, 4, 2), (2, 4, 3), (3, 5, 2), (3, 5, 3)):
        E = edges_complete(n); m = len(E)
        smallest = np.inf; count = 0; base = 0.0
        for _ in range(20 if K == 2 else 4):
            conf = [rng.normal(size=(n, d)) for _ in range(K)]
            L = np.array([sqlen(p, E) for p in conf])               # K x m
            for p in conf:
                base = max(base, abs(cayley_menger(sqlen(p, E), n)))  # should be ~ 0 (realisable)
            if K ** m <= 20000:
                cols = itertools.product(range(K), repeat=m)
            else:
                cols = (tuple(rng.integers(K, size=m)) for _ in range(20000))
            for a in cols:
                if len(set(a)) == 1:
                    continue
                q = L[list(a), range(m)]
                cm = abs(cayley_menger(q, n))
                smallest = min(smallest, cm); count += 1
        out.append(f"    K_{n} in R^{d}, {K} conformers: {count} non-constant splices, smallest |CM| = {smallest:.3e}; "
                   f"largest |CM| at true conformers = {base:.1e}")
        ok &= smallest > 1e4 * base and base < 1e-8
    return ok, out


def realise(E, n, d, q, starts=25, first=None):
    """min_p sum (l_e(p)^2 - q_e)^2 by multi-start least squares; returns the best residual norm.
    `first`: an optional first starting point (used where the theory predicts a solution nearby)."""
    best = np.inf
    for s in range(starts):
        x0 = first.ravel().copy() if (s == 0 and first is not None) else rng.normal(size=n * d) * 1.5
        res = least_squares(lambda x: sqlen(x.reshape(n, d), E) - q, x0, method="trf", xtol=1e-14, ftol=1e-14,
                            gtol=1e-14)
        best = min(best, np.linalg.norm(res.fun))
        if best < 1e-9:
            break
    return best


def test_R3():
    n, d = 6, 2
    wheel = [(0, i) for i in range(1, 6)] + [(i, i % 5 + 1) for i in range(1, 6)]
    m = len(wheel)
    worst = np.inf; sanity = 0.0
    for _ in range(3):
        x1 = rng.normal(size=(n, d)); x2 = rng.normal(size=(n, d))
        L = np.array([sqlen(x1, wheel), sqlen(x2, wheel)])
        sanity = max(sanity, realise(wheel, n, d, L[0]))
        for _ in range(60):
            a = rng.integers(2, size=m)
            if len(set(a.tolist())) == 1:
                continue
            q = L[a, range(m)]
            worst = min(worst, realise(wheel, n, d, q))
    return worst > 1e-6 and worst > 1e6 * sanity and sanity < 1e-8, [f"    wheel W5 in R^2: smallest least-squares residual over 180 random splices "
                                             f"= {worst:.3e} (true conformer: {sanity:.1e})"]


def test_R4():
    out = []; ok = True
    # (a) triangle: two ensembles with the same three edge-length laws
    A = np.array([3.0, 4.0, 5.0]); B = np.array([4.0, 5.0, 6.0])       # lengths (12, 13, 23)
    Cc = np.array([3.0, 5.0, 6.0]); Dd = np.array([4.0, 4.0, 5.0])     # splices; both satisfy the triangle inequality
    for t in (A, B, Cc, Dd):
        ok &= t[0] < t[1] + t[2] and t[1] < t[0] + t[2] and t[2] < t[0] + t[1]
    same = all(sorted([A[e], B[e]]) == sorted([Cc[e], Dd[e]]) for e in range(3))
    ok &= same and not (np.allclose(sorted(map(tuple, [A, B])), sorted(map(tuple, [Cc, Dd]))))
    out.append(f"    triangle: {{(3,4,5),(4,5,6)}} and {{(3,5,6),(4,4,5)}} have equal edge-length laws: {same}")
    # (b) K4 + a vertex of degree two in the plane: splice the two coloops
    K4 = edges_complete(4); E = K4 + [(4, 0), (4, 1)]
    n, d = 5, 2; cnt = 0; tot = 0; agree = 0
    for t in range(40):
        x1 = rng.normal(size=(n, d)); x2 = x1 + (0.05 if t < 20 else 1.0) * rng.normal(size=(n, d))
        L = np.array([sqlen(x1, E), sqlen(x2, E)])
        a = np.array([0] * 6 + [1, 1])                                   # K4 from x1, the pendant edges from x2
        q = L[a, range(len(E))]
        # exact criterion: circles of radii r0, r1 about x1[0], x1[1] meet iff |r0 - r1| <= |x1[0]-x1[1]| <= r0 + r1
        r0, r1 = np.sqrt(q[6]), np.sqrt(q[7]); base = np.linalg.norm(x1[0] - x1[1])
        exact = abs(r0 - r1) < base < r0 + r1
        found = realise(E, n, d, q, first=x1) < 1e-9
        tot += 1; cnt += found; agree += (found == exact)
    out.append(f"    K4 + degree-2 vertex: {cnt}/{tot} splices along the separator realised "
               f"(20 nearby pairs, 20 independent pairs); agreement with the two-circle criterion {agree}/{tot}")
    ok &= agree == tot and cnt >= 20
    return ok, out


def test_R5():
    n, d = 4, 2; E = edges_complete(n)
    x = [rng.normal(size=(n, d)) for _ in range(2)]
    L = np.array([sqlen(p, E) for p in x])

    def resid(v):
        l = sqlen(v.reshape(n, d), E)
        return (l - L[0]) * (l - L[1])
    hits = {0: 0, 1: 0}; other = 0; zeros = 0
    for _ in range(400):
        res = least_squares(resid, rng.normal(size=n * d) * 1.5, method="trf", xtol=1e-15, ftol=1e-15, gtol=1e-15)
        if np.linalg.norm(res.fun) < 1e-10:
            zeros += 1
            l = sqlen(res.x.reshape(n, d), E)
            m0 = np.allclose(l, L[0], atol=1e-5); m1 = np.allclose(l, L[1], atol=1e-5)
            if m0: hits[0] += 1
            elif m1: hits[1] += 1
            else: other += 1
    return other == 0 and hits[0] > 0 and hits[1] > 0, \
        [f"    certificate for K4, two conformers: {zeros} zeros found in 400 starts; "
         f"{hits[0]} at conformer 1, {hits[1]} at conformer 2, {other} elsewhere"]


def test_R6():
    ok = True
    # connected: F(x,y) = (x, y, x^2+y^2, xy); variety: y3 = y1^2 + y2^2, y4 = y1 y2
    F = lambda v: np.array([v[0], v[1], v[0] ** 2 + v[1] ** 2, v[0] * v[1]])
    viol = np.inf
    for _ in range(200):
        a, b = rng.normal(size=2), rng.normal(size=2)
        Fa, Fb = F(a), F(b)
        for col in itertools.product(range(2), repeat=4):
            if len(set(col)) == 1:
                continue
            q = np.array([(Fa, Fb)[c][k] for k, c in enumerate(col)])
            viol = min(viol, abs(q[2] - q[0] ** 2 - q[1] ** 2) + abs(q[3] - q[0] * q[1]))
    ok &= viol > 1e-6
    # direct sum: G(x,y) = (x, x^2, y, y^3): every splice along {1,2} | {3,4} is G(x_a, y_b)
    return ok, [f"    connected toy map: smallest violation of the equations of the variety over all splices = {viol:.2e}",
                "    direct-sum toy map (x, x^2, y, y^3): the splice of (x1,y1), (x2,y2) along {1,2}|{3,4} is G(x1,y2) (exact)"]


def main():
    allok = True
    for name, fn in (("R1 rigidity matroids", test_R1), ("R2 chimeras, complete graphs", test_R2),
                     ("R3 chimeras, wheel", test_R3), ("R4 negative controls", test_R4),
                     ("R5 explicit certificate", test_R5), ("R6 toy feature maps", test_R6)):
        ok, out = fn()
        print(f"{name}: {'ok' if ok else 'FAILED'}")
        for line in out:
            print(line)
        allok &= ok
    print("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
