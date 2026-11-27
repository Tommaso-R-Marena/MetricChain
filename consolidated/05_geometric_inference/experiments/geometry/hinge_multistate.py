"""Exploration for HINGE_ENSEMBLES.md section 6: K states that differ at the same s hinges.

Conjecture: the chains that are linear images of the stacked configuration are finitely many
(and then the mixture is identifiable) iff s >= ceil(3(K-1)/2).  For K = 3 this script looks
at s = 2 (expected: a positive-dimensional family, not identifiable) and s = 3 (expected:
finitely many, identifiable), by a multi-start search over all chains for affine images of
the stack and a linear programme over the classes found.  Numerical evidence only.

Usage: python3 hinge_multistate.py [seed] [nstart]
"""
import sys
import numpy as np
from scipy.optimize import least_squares, linprog
from geomlib import chain, edm, stack
from hinge_pairs import THETA


def run(K, s, rng, nstart, seglen=5):
    hinges = [seglen - 3 + (seglen - 2) * j for j in range(s)]
    n = hinges[-1] + seglen + 1
    t0 = rng.uniform(-np.pi, np.pi, n - 3)
    tors = [t0.copy()]
    for k in range(1, K):
        t = t0.copy()
        for h in hinges:
            t[h] += rng.uniform(0.6, 2.4) * rng.choice([-1, 1])
        tors.append(t)
    Xs = [chain(n, t, theta=THETA) for t in tors]
    w = rng.dirichlet(np.ones(K) * 4)
    z = stack(Xs, w)
    zc = z - z.mean(0)
    rank = np.linalg.matrix_rank(zc, tol=1e-9)
    B = np.hstack([np.ones((n, 1)), zc])
    Qb, sv, _ = np.linalg.svd(B, full_matrices=False)
    Qb = Qb[:, sv > 1e-9 * sv[0]]

    def res(t):
        X = chain(n, t, theta=THETA)
        return (X - Qb @ (Qb.T @ X)).ravel()
    found = [edm(X) for X in Xs]
    chains = list(Xs)
    conv = 0
    for _ in range(nstart):
        r = least_squares(res, rng.uniform(-np.pi, np.pi, n - 3), method="lm", xtol=1e-15, ftol=1e-15)
        if np.abs(r.fun).max() < 1e-9:
            conv += 1
            Y = chain(n, r.x, theta=THETA)
            D = edm(Y)
            if min(np.abs(D - F).max() for F in found) > 1e-6:
                found.append(D)
                chains.append(Y)
    M = sum(wk * edm(X) for wk, X in zip(w, Xs))
    iu = np.triu_indices(n, 1)
    A = np.vstack([np.array([D[iu] for D in found]).T, np.ones(len(found))])
    b = np.append(M[iu], 1.0)
    off = 0.0
    c = np.zeros(len(found))
    c[K:] = -1.0
    check = ""
    if len(found) > K:
        r = linprog(c, A_eq=A, b_eq=b, bounds=(0, None), method="highs")
        off = -r.fun if r.status == 0 else float("nan")
        if r.status == 0 and off > 1e-6:
            v = r.x
            Mv = sum(vi * D for vi, D in zip(v, found))
            used = [i for i in range(len(v)) if v[i] > 1e-9]
            far = min(min(np.abs(found[i] - found[k]).max() for k in range(K)) for i in used if i >= K)
            check = (f"; the competing ensemble: {len(used)} chains, weights on the states "
                     f"{np.round(v[:K], 4).tolist()} (true {np.round(w, 4).tolist()}), max|M - M(mu)| = "
                     f"{np.abs(Mv - M).max():.1e}, its other chains differ from every state by at least "
                     f"{far:.2f} in a squared distance")
    print(f"K = {K}, s = {s}, n = {n}: rank of the stack {rank}; {conv} of {nstart} starts converged; "
          f"{len(found) - K} classes of affine images besides the {K} states; "
          f"largest total weight a competing ensemble can put on them: {off:.4f}{check}", flush=True)
    return len(found) - K, off


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    nstart = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    rng = np.random.default_rng(seed)
    run(2, 2, rng, nstart)
    run(3, 2, rng, nstart)
    run(3, 3, rng, nstart)
    run(3, 4, rng, nstart)
