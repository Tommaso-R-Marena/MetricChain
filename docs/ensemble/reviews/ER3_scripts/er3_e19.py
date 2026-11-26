#!/usr/bin/env python3
"""ER3 review, Theorem E19 (b)-(d).  Reviewer's own code.

L.  Lift isolation for the degree-2 lift (= flat isolation for pair data), n = 10 and 12: frequencies for the K of the
    division's check L1, with the reviewer's implementation, and the numerical gap that makes the floating-point
    decision safe (smallest non-zero distance of a lifted vertex from the span, over all trials).
C.  E19(d): Cover's count for points that are NOT in general position.  For K random conformers and a site v the
    points are the vectors of odd monomials of degree <= 2d-1 of the other sites; the number of labellings realised
    by a strict homogeneous linear threshold function is counted by brute force (one LP per labelling) and compared
    with 2 sum_{i<D} C(K-1, i).  Also the fraction of label vectors -x_v realised, against the binomial bound, by
    Monte Carlo (the labels are the coordinate x_v, the points depend on the other coordinates only).
P.  E19(c) at n = 6 (15 pair observables, 32 states), K = 13, 14 > 2n: flat-isolated supports, random weights.  The
    ensembles with the same pair data form a polytope whose vertices have at most 16 atoms; a twin with at most K
    atoms would be a vertex with at most K atoms.  Vertices are sampled by LPs with random objectives.
"""
import itertools, sys
from math import comb
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(31108)


def cube_mod_flip(n):
    Z = np.array(list(itertools.product((1, -1), repeat=n - 1)))
    return np.hstack([np.ones((len(Z), 1), dtype=int), Z])


def pair_lift(Y):
    n = Y.shape[1]; iu = np.triu_indices(n, 1)
    return np.hstack([np.ones((len(Y), 1)), (Y[:, iu[0]] * Y[:, iu[1]]).astype(float)])


def test_L():
    print("L. lift isolation, degree-2 lift")
    for n, trials in ((10, 300), (12, 300)):
        Y = cube_mod_flip(n); Xi = pair_lift(Y); N = len(Y); m = n * (n - 1) // 2
        row = []; gap = np.inf; dep = 0
        for K in (2 * n, m // 2, (3 * m) // 4, m - n, m):
            iso = 0
            for _ in range(trials):
                idx = rng.choice(N, size=K, replace=False)
                B = Xi[idx].T
                U, s, _ = np.linalg.svd(B, full_matrices=False)
                if s[-1] < 1e-9 * s[0]:
                    dep += 1; continue
                res = np.linalg.norm(Xi - (Xi @ U) @ U.T, axis=1)
                inspan = res < 1e-7
                if (~inspan).any():
                    gap = min(gap, res[~inspan].min())
                iso += int(inspan.sum()) == K
            row.append((K, iso / trials))
        print(f"   n = {n} ({m} pair observables, lift dimension {m + 1}): " + ", ".join(f"K = {K}: {p:.3f}" for K, p in row)
              + f"; dependent lifted vectors in {dep} trials; smallest non-zero distance from the span: {gap:.2e} "
              f"(tolerance used: 1e-7)")


def odd_monomials(Xo, d):
    """Xo: (K, n-1) sign vectors of the other sites -> odd monomials of degree <= 2d-1."""
    cols = []
    for k in range(1, 2 * d, 2):
        for A in itertools.combinations(range(Xo.shape[1]), k):
            cols.append(np.prod(Xo[:, A], axis=1))
    return np.array(cols, dtype=float).T


def separable(P, lab):
    """Is there c with lab_a <c, P_a> >= 1 for all a ?"""
    A = -(lab[:, None] * P)
    res = linprog(np.zeros(P.shape[1]), A_ub=A, b_ub=-np.ones(len(P)), bounds=[(None, None)] * P.shape[1], method="highs")
    return res.status == 0


def test_C():
    print("C. Cover's count for the points of E19(d) (not in general position)")
    ok = True
    for n, d, K in ((5, 1, 9), (6, 1, 10), (6, 1, 12), (5, 2, 10), (6, 2, 11)):
        worst = -np.inf; eq = 0; reps = 3
        for _ in range(reps):
            X = rng.choice((-1, 1), size=(K, n))                      # independent uniform conformers in {+-1}^n
            P = odd_monomials(X[:, 1:], d); D = P.shape[1]            # site v = 1; points from the other sites
            count = sum(separable(P, np.array(lab)) for lab in itertools.product((-1, 1), repeat=K))
            bound = 2 * sum(comb(K - 1, i) for i in range(D))
            worst = max(worst, count - bound); eq += count == bound
        ok &= worst <= 0
        print(f"   n = {n}, d = {d}: D_odd = {D}, K = {K}: separable labellings minus Cover's bound "
              f"2 sum_(i<D) C(K-1,i) = {bound} (of {2 ** K}): at most {worst}; equality in {eq} of {reps} samples")
    # Monte Carlo: P(labels -x_v strictly separable) against the binomial bound
    for n, d, K, trials in ((7, 1, 14, 400), (7, 1, 18, 400), (8, 1, 20, 300), (6, 2, 36, 200), (6, 2, 44, 200)):
        hits = 0
        for _ in range(trials):
            X = rng.choice((-1, 1), size=(K, n))
            P = odd_monomials(X[:, 1:], d)
            hits += separable(P, -X[:, 0].astype(float))
        D = P.shape[1]
        bound = sum(comb(K - 1, i) for i in range(D)) / 2 ** (K - 1)
        ok &= hits / trials <= bound + 3 * np.sqrt(bound * (1 - bound) / trials) + 1e-9
        print(f"   n = {n}, d = {d}, K = {K} (D_odd = {D}, K / D_odd = {K / D:.2f}): labels -x_1 strictly separable in "
              f"{hits / trials:.3f} of {trials} samples; bound P(Bin(K-1, 1/2) <= D_odd - 1) = {bound:.3f}")
    return ok


def test_P():
    print("P. E19(c) at n = 6: vertices of the polytope of ensembles with the same pair data")
    n = 6; Y = cube_mod_flip(n); G = pair_lift(Y); N = len(Y)
    for K in (13, 14):
        done = 0
        while done < 4:
            idx = np.sort(rng.choice(N, size=K, replace=False))
            B = G[idx].T
            U, s, _ = np.linalg.svd(B, full_matrices=False)
            if s[-1] < 1e-9 * s[0]:
                continue
            res = np.linalg.norm(G - (G @ U) @ U.T, axis=1)
            if int((res < 1e-7).sum()) != K:
                continue                                              # not flat-isolated
            done += 1
            w = rng.dirichlet(3 * np.ones(K)); mu = np.zeros(N); mu[idx] = w
            supports = {}; other = 0
            for _ in range(400):
                c = rng.normal(size=N)
                r = linprog(c, A_eq=G.T, b_eq=G.T @ mu, bounds=[(0, None)] * N, method="highs-ds")
                sup = tuple(np.nonzero(r.x > 1e-10)[0])
                if set(sup) == set(idx.tolist()):
                    continue
                other += 1
                supports[len(sup)] = supports.get(len(sup), 0) + 1
            print(f"   K = {K}, flat-isolated support {done}: {other} of 400 random-objective vertices are not the ensemble "
                  f"itself; their numbers of atoms: {dict(sorted(supports.items()))}  (a twin with at most K atoms would "
                  f"show as a vertex with <= {K} atoms)")


P_MOD = 2147483629                                            # a prime below 2^31: products fit in int64


def nullspace_mod_p(B):
    """Basis of {u : B u = 0} over F_p for an integer matrix B (rows = vectors); also the rank."""
    A = np.mod(B.astype(np.int64), P_MOD); R, C = A.shape
    piv = []; r = 0
    for c in range(C):
        rows = np.nonzero(A[r:, c])[0]
        if len(rows) == 0:
            continue
        j = r + rows[0]
        if j != r:
            A[[r, j]] = A[[j, r]]
        inv = pow(int(A[r, c]), P_MOD - 2, P_MOD)
        A[r] = (A[r] * inv) % P_MOD
        for i in range(R):
            if i != r and A[i, c]:
                A[i] = (A[i] - A[i, c] * A[r]) % P_MOD
        piv.append(c); r += 1
        if r == R:
            break
    free = [c for c in range(C) if c not in piv]
    N = np.zeros((len(free), C), dtype=np.int64)
    for k, f in enumerate(free):
        N[k, f] = 1
        for i, c in enumerate(piv):
            N[k, c] = (-A[i, f]) % P_MOD
    return N, r


def test_X():
    print("X. lift isolation at n = 12 decided exactly (arithmetic modulo a 31-bit prime) against the floating-point test")
    n = 12; Y = cube_mod_flip(n); Xi = pair_lift(Y); N = len(Y); m = n * (n - 1) // 2
    Xi_int = np.rint(Xi).astype(np.int64)
    for K, trials in ((54, 200), (66, 400)):
        iso_exact = iso_float = state_mismatch = trial_mismatch = dep = 0
        for _ in range(trials):
            idx = rng.choice(N, size=K, replace=False)
            Nsp, rank = nullspace_mod_p(Xi_int[idx])
            if rank < K:
                dep += 1; continue
            member_exact = np.all((Xi_int @ Nsp.T) % P_MOD == 0, axis=1)
            U, s, _ = np.linalg.svd(Xi[idx].T, full_matrices=False)
            member_float = np.linalg.norm(Xi - (Xi @ U) @ U.T, axis=1) < 1e-7
            state_mismatch += int((member_exact != member_float).sum())
            e = int(member_exact.sum()) == K; f = int(member_float.sum()) == K
            iso_exact += e; iso_float += f; trial_mismatch += e != f
        print(f"   K = {K}: {trials} supports ({dep} with dependent lifted vectors); lift-isolated: exact {iso_exact / trials:.3f}, "
              f"floating point (tolerance 1e-7) {iso_float / trials:.3f}; supports classified differently: {trial_mismatch}; "
              f"states classified differently: {state_mismatch}")


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "all"
    if part in ("X", "all"):
        test_X()
    if part in ("L", "all"):
        test_L()
    if part in ("C", "all"):
        print("PASS" if test_C() else "FAIL")
    if part in ("P", "all"):
        test_P()
