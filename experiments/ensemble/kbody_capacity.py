#!/usr/bin/env python3
"""Report §4c (Part VI): for which K are K random conformers on {-1,1}^n (modulo the global flip) exactly the set
of ground states of an energy with interactions of even order at most 2d (a simplicial face of the polytope of
2d-body data)?  Exact decision by a cutting-plane linear programme over all 2^{n-1} states:

    maximise t  s.t.  q.psi(x^a) = 0 (conformers),  q.psi(y) >= t (y in a growing constraint set),  |q| <= 1,

psi = all monomials of degree <= 2d in z_j = x_1 x_j (the constant included).  After each solve the energies of
all states are computed; "face" as soon as every other state is above zero by a margin, "not a face" as soon as
a relaxation has optimum t <= 0.  Also reported: whether the conformers are lift-isolated for the degree-d lift
(the span of their vectors z^{<=d} contains no other such vector), which is when the sum-of-squares certificate
of Theorem E18 exists.

Control: with "dg" in place of d (e.g. "2g") the feature vectors of the states are replaced by independent
Gaussian vectors of the same dimension (first coordinate one): the face threshold of a Gaussian point cloud
with the same number of points and the same dimension (the Donoho-Tanner weak threshold for non-negative
vectors), to compare with the cube.

Usage: python3 kbody_capacity.py n d trials K [K ...]
Numerical evidence only [N].
"""
import itertools, sys, time
from math import comb
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(20261203)


def zstates(m):
    N = 1 << m
    idx = np.arange(N, dtype=np.int64)
    return np.where((idx[:, None] >> np.arange(m)) & 1, 1, -1).astype(np.int8)


def monomials(Z, d):
    m = Z.shape[1]; cols = [np.ones(Z.shape[0], dtype=np.float32)]
    for k in range(1, d + 1):
        for A in itertools.combinations(range(m), k):
            cols.append(np.prod(Z[:, A], axis=1).astype(np.float32))
    return np.array(cols).T


def lift_isolated(Xi, idx):
    B = Xi[idx].T.astype(float)
    s = np.linalg.svd(B, compute_uv=False)
    if len(idx) > B.shape[0] or s[-1] < 1e-9 * s[0]:
        return False
    Q, _ = np.linalg.qr(B)
    res = np.linalg.norm(Xi - (Xi @ Q) @ Q.T, axis=1)
    return int((res < 1e-6).sum()) == len(idx)


def is_face(G, idx, start=600):
    """Exact decision (up to floating point) whether the states idx are a simplicial face: is there q with
    q.psi = 0 on idx and q.psi > 0 on every other state?  The equalities are eliminated: q = B y with B an
    orthonormal basis of the null space of psi(idx), so the energies of all states are H y, H = G B."""
    N, D = G.shape; K = len(idx)
    GS = G[idx].astype(float)
    _, sv, Vt = np.linalg.svd(GS, full_matrices=True)
    if K > D or sv[-1] < 1e-9 * sv[0]:
        return False, 0                                   # affinely dependent features: not a simplex
    if K == D:
        return False, 0                                   # the conformers span everything: no certificate
    B = Vt[K:].T                                          # D x (D - K)
    H = G.astype(float) @ B                               # N x (D - K)
    inS = np.zeros(N, dtype=bool); inS[idx] = True
    others = np.nonzero(~inS)[0]
    cons = set(rng.choice(others, size=min(start, len(others)), replace=False).tolist())
    r = D - K
    for it in range(1, 400):
        ck = np.fromiter(cons, dtype=np.int64)
        c = np.zeros(r + 1); c[-1] = -1.0
        A_ub = np.hstack([-H[ck], np.ones((len(ck), 1))])
        res = linprog(c, A_ub=A_ub, b_ub=np.zeros(len(ck)), bounds=[(-1, 1)] * r + [(None, 1.0)], method="highs")
        if res.status != 0 or res.x[-1] <= 1e-7:
            return False, it                              # a relaxation has no certificate with a margin
        y, t = res.x[:r], res.x[-1]
        E = H @ y
        E[inS] = np.inf
        if E.min() > 1e-6:
            return True, it                               # every other state is strictly above the conformers
        viol = np.argsort(E)[:300]
        viol = viol[E[viol] < t - 1e-7]
        new = set(viol.tolist()) - cons
        if not new:
            return bool(E.min() > 1e-8), it
        cons |= new
    return None, 400


def main():
    gaussian = sys.argv[2].endswith("g")
    n, d, trials = int(sys.argv[1]), int(sys.argv[2].rstrip("g")), int(sys.argv[3]); Ks = [int(a) for a in sys.argv[4:]]
    m = n - 1
    Z = zstates(m); N = Z.shape[0]
    G = monomials(Z, 2 * d); Xi = monomials(Z, d).astype(float)
    d_odd = sum(comb(m, j) for j in range(1, 2 * d, 2))
    print(f"n = {n}, data of even order <= {2 * d}: {N} states modulo flip, {G.shape[1]} features (constant included); "
          f"lift dimension C(n-1,<={d}) = {Xi.shape[1]}; Cover-type bound 2*D_odd = {2 * d_odd}", flush=True)
    if gaussian:
        G = rng.normal(size=G.shape).astype(np.float32); G[:, 0] = 1.0
        print("   GAUSSIAN CONTROL: the feature vectors are replaced by independent Gaussian vectors "
              "(same number of points, same dimension); the lift-isolated column still refers to the cube", flush=True)
    for K in Ks:
        t0 = time.time(); face = iso = und = its = 0
        for _ in range(trials):
            idx = rng.choice(N, size=K, replace=False)
            ans, it = is_face(G, idx); its += it
            if ans is None:
                und += 1
            else:
                face += ans
            iso += lift_isolated(Xi, idx)
        print(f"   K = {K:5d}   face frequency = {face / trials:5.3f}   lift-isolated = {iso / trials:5.3f}   "
              f"(undecided {und}; mean iterations {its / trials:.1f}; {time.time() - t0:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
