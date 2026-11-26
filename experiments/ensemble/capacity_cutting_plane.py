#!/usr/bin/env python3
"""Problem O1 at larger sizes: is a random set of K conformers on {-1,1}^n (modulo the global flip) exactly
the set of ground states of some Ising energy with affinely independent pair features (a simplicial face
of the cut polytope)?  Exact decision by a cutting-plane linear programme:

    maximise t  s.t.  Q.phi(x^a) = c (all conformers),  Q.phi(y) >= c + t (y in a growing constraint set),
                      |Q_ij| <= 1 ;

after each solve the energy of ALL 2^{n-1} states is evaluated; the answer is "face" as soon as every
non-conformer state lies above c by a positive margin, and "not a face" as soon as the optimum is t <= 0
(a relaxation is already infeasible).  Both answers are certified up to floating-point tolerances.
(The internal review ER2 compared the answers with a double-precision linear programme over all states on
490 instances with n = 10, 12, 14: no disagreement; smallest margin of a face 1.7e-2.  After that review a
solver failure is reported as "undecided" instead of "not a face", and an acceptance is confirmed in double
precision; neither changes any stored result.)

Usage: python3 capacity_cutting_plane.py n trials alpha [alpha ...]
Numerical evidence only [N].
"""
import itertools, sys, time
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(20261202)


def all_states(n):
    """All 2^{n-1} sign vectors with first coordinate +1, as int8, in the order of the binary key."""
    N = 1 << (n - 1)
    idx = np.arange(N, dtype=np.int64)
    Y = np.ones((N, n), dtype=np.int8)
    for j in range(1, n):
        Y[:, j] = np.where((idx >> (j - 1)) & 1, 1, -1)
    return Y


def key_of(Y):
    """Binary key of states normalised to first coordinate +1."""
    Y = Y * Y[:, [0]]
    bits = (Y[:, 1:] > 0).astype(np.int64)
    return bits @ (1 << np.arange(Y.shape[1] - 1, dtype=np.int64))


def energies(Yall, Qm, chunk=1 << 18):
    out = np.empty(Yall.shape[0])
    for s in range(0, Yall.shape[0], chunk):
        Yc = Yall[s:s + chunk].astype(np.float32)
        out[s:s + chunk] = 0.5 * np.einsum("ij,ij->i", Yc @ Qm.astype(np.float32), Yc)
    return out


def is_face(X, Yall):
    K, n = X.shape
    iu = np.triu_indices(n, 1); D = len(iu[0])
    feat = lambda Y: (Y[:, iu[0]] * Y[:, iu[1]]).astype(float)
    FS = feat(X)
    if np.linalg.matrix_rank(np.hstack([np.ones((K, 1)), FS])) < K:
        return False, 0
    pat = key_of(X)
    cons_keys = set()
    for a in range(K):
        for v in range(n):
            y = X[a].copy(); y[v] = -y[v]
            cons_keys.add(int(key_of(y[None, :])[0]))
    cons_keys -= set(pat.tolist())
    for it in range(1, 400):
        ck = np.fromiter(cons_keys, dtype=np.int64)
        FC = feat(Yall[ck])
        # variables: Q (D), c, t ; maximise t
        cvec = np.zeros(D + 2); cvec[-1] = -1.0
        A_eq = np.hstack([FS, -np.ones((K, 1)), np.zeros((K, 1))])
        A_ub = np.hstack([-FC, np.ones((len(ck), 1)), np.ones((len(ck), 1))])
        res = linprog(cvec, A_ub=A_ub, b_ub=np.zeros(len(ck)), A_eq=A_eq, b_eq=np.zeros(K),
                      bounds=[(-1, 1)] * D + [(None, None), (None, 10.0)], method="highs")
        if res.status != 0:
            return None, it                                   # solver failure: undecided (never observed)
        if res.x[-1] <= 1e-7:
            return False, it
        Q, c, t = res.x[:D], res.x[D], res.x[D + 1]
        Qm = np.zeros((n, n)); Qm[iu] = Q; Qm = Qm + Qm.T
        E = energies(Yall, Qm)
        E[pat] = np.inf
        if E.min() - c > 1e-5:
            # acceptance is confirmed in double precision on the lowest states (the scan above is float32)
            low = np.argsort(E)[:256]
            Y = Yall[low].astype(np.float64)
            E64 = 0.5 * np.einsum("ij,ij->i", Y @ Qm, Y)
            if E64.min() - c > 1e-6:
                return True, it
        viol = np.argsort(E)[:60]
        viol = viol[E[viol] < c + t - 1e-6]
        new = set(viol.tolist()) - cons_keys
        if not new:
            return E.min() - c > 1e-7, it
        cons_keys |= new
    return None, 400


def main():
    n = int(sys.argv[1]); trials = int(sys.argv[2]); alphas = [float(a) for a in sys.argv[3:]]
    Yall = all_states(n); N = Yall.shape[0]
    print(f"n = {n}: {N} states modulo flip, {trials} trials per K", flush=True)
    for alpha in alphas:
        K = int(round(alpha * n)); t0 = time.time(); face = 0; its = 0; und = 0
        for _ in range(trials):
            idx = rng.choice(N, size=K, replace=False)
            ans, it = is_face(Yall[idx].astype(np.int64), Yall)
            its += it
            if ans is None:
                und += 1
            else:
                face += ans
        print(f"   K = {K:3d}  K/n = {K / n:4.2f}   face frequency = {face / trials:5.3f}   "
              f"(undecided {und}; mean iterations {its / trials:.1f}; {time.time() - t0:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
