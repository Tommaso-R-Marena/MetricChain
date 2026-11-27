#!/usr/bin/env python3
"""ER4 (internal AI review) -- Part VII of the report (b654396, section 4d): Propositions E23, E24, Theorems E25, E26.
Own code, written from the statements; nothing imported from experiments/ensemble/.

STATUS: parts A and B were run to the end (output: out_part7_parts_A_B_only.txt).  Part C (E25) was still running
after more than eighteen minutes when the review was wound down and was stopped without output; part D (E26) was
therefore never reached.  Parts C and D are UNVERIFIED code: nothing in the review report rests on them.

A  E23(b): 'determined up to a positive factor'  <=>  (i) Phi linearly independent on the support and (ii) a
   combination of the observables without constant term, non-negative with zero set the support.
   Both sides decided EXACTLY (rational arithmetic, vertex enumeration), 2 000 random integer instances; the role
   of the hypothesis y != 0; instances with a zero feature vector.
B  E23(b) with a tolerance: convexity of {nu : |y_i - c E_nu phi_i| <= tau_i for some c > 0}; data within the
   tolerance of zero; the Charnes-Cooper programme and its boundary case c -> infinity.
C  E25(d): the two stability bounds at the least length -- the TRUE maxima over {|E Phi| <= r_min + tau}
   (cutting planes until the optimiser is feasible to 1e-12, not a relaxation), by type of the nearest face;
   the conditions for attainment (facet / vertex / lower-dimensional face / moment body without interior).
   E25(c): the bound tau/gamma' at the largest length.  E25(b): d = 1.
D  E26(b): the two reductions by brute force (signs x linear feasibility) against subset sums / exact covers;
   and a reduction showing that IDENTIFICATION from squared means is coNP-hard (so a claimed answer 'determined'
   is not checked in polynomial time from signs unless NP = coNP).
"""
import itertools
import sys
from fractions import Fraction as Fr

import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(271126)


# ------------------------------------------------------------------ exact linear algebra
def solve_exact(cols, b):
    """cols: list of column vectors (lists of Fraction), b: list.  Returns the unique x with sum x_j cols_j = b if the
    columns are linearly independent and b is in their span, else None."""
    n, k = len(b), len(cols)
    A = [[cols[j][i] for j in range(k)] + [b[i]] for i in range(n)]
    piv = []
    r = 0
    for c in range(k):
        p = next((i for i in range(r, n) if A[i][c] != 0), None)
        if p is None:
            return None                           # dependent columns
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(n):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    for i in range(r, n):
        if A[i][k] != 0:
            return None                           # inconsistent
    return [A[i][k] for i in range(k)]


def rank_exact(rows):
    A = [list(r) for r in rows]
    r = 0
    if not A:
        return 0
    for c in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        r += 1
        if r == len(A):
            break
    return r


def vertices_exact(cols, b):
    """all vertices of {x >= 0 : sum x_j cols_j = b} (exact): supports with independent columns"""
    n, k = len(b), len(cols)
    verts = set()
    for size in range(0, min(n, k) + 1):
        for B in itertools.combinations(range(k), size):
            x = solve_exact([cols[j] for j in B], b)
            if x is None or any(v <= 0 for v in x):
                continue
            full = [Fr(0)] * k
            for j, v in zip(B, x):
                full[j] = v
            verts.add(tuple(full))
    return verts


def feasible_exact(cols, b):
    n, k = len(b), len(cols)
    for size in range(0, min(n, k) + 1):
        for B in itertools.combinations(range(k), size):
            x = solve_exact([cols[j] for j in B], b)
            if x is not None and all(v >= 0 for v in x):
                return True
    return False


# ------------------------------------------------------------------ A: E23(b)
def determined_up_to_factor_exact(Phi, mu):
    """Phi: m x M integer matrix (lists), mu: list of Fractions.  Q = {(nu, t) >= 0 : Phi nu = t z, sum nu = 1}.
    mu is the only compatible ensemble iff Q is the single point (mu, 1)  (see the review text)."""
    m, M = len(Phi), len(Phi[0])
    z = [sum(Fr(Phi[i][x]) * mu[x] for x in range(M)) for i in range(m)]
    cols = [[Fr(Phi[i][x]) for i in range(m)] + [Fr(1)] for x in range(M)]
    cols.append([-z[i] for i in range(m)] + [Fr(0)])
    b = [Fr(0)] * m + [Fr(1)]
    V = vertices_exact(cols, b)
    target = tuple(list(mu) + [Fr(1)])
    return V == {target}, z


def criterion_exact(Phi, S):
    m, M = len(Phi), len(Phi[0])
    if rank_exact([[Fr(Phi[i][s]) for i in range(m)] for s in S]) < len(S):
        return False
    off = [x for x in range(M) if x not in S]
    if not off:
        return True
    # (ii) fails iff some g >= 0, sum g = 1 on the complement has sum g Phi in span Phi(S)   (Stiemke / Farkas)
    cols = [[Fr(Phi[i][x]) for i in range(m)] + [Fr(1)] for x in off]
    for s in S:
        cols.append([Fr(Phi[i][s]) for i in range(m)] + [Fr(0)])
        cols.append([-Fr(Phi[i][s]) for i in range(m)] + [Fr(0)])
    b = [Fr(0)] * m + [Fr(1)]
    return not feasible_exact(cols, b)


def part_A():
    print("A. E23(b), exact: 'determined up to a positive factor' against the criterion (i) + (ii)")
    agree = yes = used = zero = 0
    zero_det_but_criterion_false = 0
    with_zero_feature = 0
    for trial in range(2000):
        M = int(rng.integers(2, 7))
        m = int(rng.integers(1, 4))
        Phi = [[int(v) for v in rng.integers(-2, 3, size=M)] for _ in range(m)]
        K = int(rng.integers(1, min(M, 3) + 1))
        S = sorted(int(v) for v in rng.choice(M, size=K, replace=False))
        wts = [int(v) for v in rng.integers(1, 6, size=K)]
        mu = [Fr(0)] * M
        for s, wv in zip(S, wts):
            mu[s] = Fr(wv, sum(wts))
        det, z = determined_up_to_factor_exact(Phi, mu)
        crit = criterion_exact(Phi, S)
        if all(v == 0 for v in z):
            zero += 1
            # with zero data the compatible ensembles are {nu : E_nu Phi = 0}; mu may be the only one although (i) fails
            cols = [[Fr(Phi[i][x]) for i in range(m)] + [Fr(1)] for x in range(M)]
            V = vertices_exact(cols, [Fr(0)] * m + [Fr(1)])
            if V == {tuple(mu)} and not crit:
                zero_det_but_criterion_false += 1
            continue
        used += 1
        agree += int(det == crit)
        yes += int(det)
        with_zero_feature += int(any(all(Phi[i][x] == 0 for i in range(m)) for x in range(M)))
    print(f"    {used} random integer instances with non-zero data (2 to 6 configurations, 1 to 3 observables with values "
          f"in -2..2): agreement in {agree}/{used}; determined up to the factor: {yes}; instances containing a "
          f"configuration with zero feature vector: {with_zero_feature}")
    print(f"    {zero} instances with zero data set aside; in {zero_det_but_criterion_false} of them the ensemble is the only "
          f"one with E Phi = 0 although the criterion fails (so the hypothesis y != 0 is needed, as stated)")
    # the example of the text
    Phi = [[1, 0, 1], [0, 1, 1]]
    ex1 = determined_up_to_factor_exact(Phi, [Fr(1, 2), Fr(1, 2), Fr(0)])[0]
    ex2 = determined_up_to_factor_exact(Phi, [Fr(1), Fr(0), Fr(0)])[0]
    print(f"    example of the text: (1/2, 1/2, 0) determined up to the factor: {ex1} (text: no); delta_a: {ex2} (text: yes)")
    return agree == used and (not ex1) and ex2


# ------------------------------------------------------------------ B: tolerance
def c_interval(a, y, tau):
    """{c > 0 : |y_i - c a_i| <= tau_i for all i} as an interval (lo, hi) (possibly empty: lo > hi), closed"""
    lo, hi = 0.0, np.inf
    for ai, yi, ti in zip(a, y, tau):
        if abs(ai) < 1e-15:
            if abs(yi) > ti:
                return 1.0, 0.0
            continue
        l, h = sorted(((yi - ti) / ai, (yi + ti) / ai))
        lo, hi = max(lo, l), min(hi, h)
    return lo, hi


def part_B():
    print("B. E23(b) with a tolerance")
    bad = pairs = 0
    everything = 0
    for trial in range(300):
        M = int(rng.integers(3, 7))
        m = int(rng.integers(1, 4))
        Phi = rng.normal(size=(m, M))
        mu0 = rng.dirichlet(np.ones(M))
        c0 = rng.uniform(0.3, 3.0)
        y = c0 * Phi @ mu0
        tau = rng.uniform(0.02, 0.3, size=m) * np.abs(y).max()
        W = rng.dirichlet(np.ones(M) * 0.5, size=4000)
        feas = []
        for wv in W:
            lo, hi = c_interval(Phi @ wv, y, tau)
            if hi > max(lo, 0.0) + 1e-12 and hi > 1e-12:
                feas.append(wv)
        feas = feas[:60]
        for i in range(len(feas)):
            for j in range(i + 1, len(feas)):
                for s in (0.25, 0.5, 0.75):
                    wv = s * feas[i] + (1 - s) * feas[j]
                    lo, hi = c_interval(Phi @ wv, y, tau)
                    pairs += 1
                    if not (hi >= max(lo, 0.0) - 1e-9 and hi > 0):
                        bad += 1
        if np.all(np.abs(y) < tau):
            everything += 1
    print(f"    convexity: {pairs} convex combinations of pairs of compatible ensembles (300 random instances): "
          f"not compatible: {bad}")
    # data within the tolerance of zero: every ensemble is compatible (c -> 0)
    Phi = rng.normal(size=(2, 5))
    y = np.array([0.01, -0.02])
    tau = np.array([0.05, 0.05])
    W = rng.dirichlet(np.ones(5), size=2000)
    allc = all(c_interval(Phi @ wv, y, tau)[1] > 0 for wv in W)
    print(f"    data within the tolerance of zero (|y_i| < tau_i): all of 2 000 sampled ensembles compatible: {allc} "
          f"(the datum then says nothing; the set is still convex)")
    # the Charnes-Cooper programme with s = 1/c >= 0: the boundary s = 0 (c = infinity)
    # X = {a, b}, phi(a) = 1, phi(b) = -1, y = 1, tau = 0.1: compatible nu need c (nu_a - nu_b) in [0.9, 1.1], c > 0:
    # every nu with nu_a > nu_b.  The uniform ensemble (nu_a = nu_b) is NOT compatible, but it is feasible for the
    # linear programme with s >= 0 (s = 0): the programme returns the closure.
    res = linprog([1.0, 0.0, 0.0], A_ub=[[-1.0, 1.0, 0.9], [1.0, -1.0, -1.1]], b_ub=[0.0, 0.0],
                  A_eq=[[1.0, 1.0, 0.0]], b_eq=[1.0], bounds=[(0, None)] * 3, method="highs")
    print(f"    Charnes-Cooper with s = 1/c >= 0 on a two-point example: least nu_a = {res.x[0]:.3f} with s = {res.x[2]:.3f}"
          f" -- the infimum 1/2 is not attained by a compatible ensemble (c = infinity): the programme gives the"
          f" closure of the range")
    return bad == 0 and allc


# ------------------------------------------------------------------ C: E25
def nearest_point(P):
    """nearest point of conv(P) to the origin by enumeration of faces (exact up to round-off): for every affinely
    independent subset of at most dim+1 points project the origin on its affine hull; keep the feasible ones."""
    M, dim = P.shape
    best = (np.inf, None, None)
    for size in range(1, dim + 2):
        for B in itertools.combinations(range(M), size):
            Q = P[list(B)]
            # minimise |Q^T w|^2 with sum w = 1: KKT system
            G = Q @ Q.T
            K = np.block([[2 * G, np.ones((size, 1))], [np.ones((1, size)), np.zeros((1, 1))]])
            rhs = np.zeros(size + 1)
            rhs[-1] = 1.0
            try:
                sol = np.linalg.solve(K, rhs)
            except np.linalg.LinAlgError:
                continue
            wv = sol[:size]
            if np.any(wv < -1e-12) or not np.all(np.isfinite(wv)):
                continue
            z = wv @ Q
            nz = np.linalg.norm(z)
            if nz < best[0] - 1e-13:
                best = (nz, z, (B, wv))
    return best[1], best[0], best[2]


def max_over_ball(P, c, rho, zhat, maxit=400):
    """max c.w over the simplex with |P^T w| <= rho, by cutting planes; returns (value, w, final |mean| - rho)"""
    M, dim = P.shape
    U = [zhat]
    for k in range(2 * dim):
        e = np.zeros(dim)
        e[k // 2] = 1.0 if k % 2 == 0 else -1.0
        U.append(e)
    wv = None
    for it in range(maxit):
        A = np.array(U) @ P.T
        res = linprog(-c, A_ub=A, b_ub=rho * np.ones(len(U)), A_eq=np.ones((1, M)), b_eq=[1.0],
                      bounds=[(0, None)] * M, method="highs")
        if res.status != 0:
            return np.nan, None, np.nan
        wv = res.x
        z = wv @ P
        nz = np.linalg.norm(z)
        if nz <= rho + 1e-13:
            return -res.fun, wv, nz - rho
        U.append(z / nz)
    return -res.fun, wv, nz - rho


def part_C():
    print("C. E25(d): true maxima over {|E Phi| <= r_min + tau}, by type of the face nearest to the origin")
    stats = {}
    for trial in range(400):
        dim = int(rng.choice((2, 3)))
        M = int(rng.integers(5, 10))
        P = rng.normal(size=(M, dim))
        P[:, 0] = np.abs(P[:, 0]) + rng.uniform(0.3, 1.0)
        zs, r, (B, wB) = nearest_point(P)
        f = P @ zs - r * r
        assert f.min() > -1e-9
        Z = np.nonzero(f < 1e-9)[0]
        off = np.nonzero(f >= 1e-9)[0]
        if len(off) == 0:
            continue
        gamma = f[off].min()
        facedim = np.linalg.matrix_rank(np.hstack([np.ones((len(Z), 1)), P[Z]]), tol=1e-8) - 1
        interior = np.all(wB > 1e-9)
        if facedim == 0:
            kind = "vertex"
        elif facedim == dim - 1:
            kind = "facet (relative interior)"
        else:
            kind = "edge in space (not a facet)"
        for tau in (1e-4, 1e-3, 1e-2):
            c = np.zeros(M)
            c[off] = 1.0
            val, wv, slack = max_over_ball(P, c, r + tau, zs / r)
            ratio_mass = val / (r * tau / gamma)
            # largest displacement of the mean: maximise v.(E Phi) for many directions v, keep feasible optimisers
            best = 0.0
            for k in range(24 if dim == 2 else 60):
                if dim == 2:
                    v = np.array([np.cos(2 * np.pi * k / 24), np.sin(2 * np.pi * k / 24)])
                else:
                    v = rng.normal(size=3)
                    v /= np.linalg.norm(v)
                val2, w2, _ = max_over_ball(P, P @ v, r + tau, zs / r)
                if w2 is not None:
                    best = max(best, np.linalg.norm(w2 @ P - zs))
            if facedim >= 1:
                # along the face: the two directions of an edge of the face
                for a in Z:
                    v = P[a] - zs
                    if np.linalg.norm(v) > 1e-9:
                        val2, w2, _ = max_over_ball(P, P @ v, r + tau, zs / r)
                        if w2 is not None:
                            best = max(best, np.linalg.norm(w2 @ P - zs))
            ratio_mean = best / np.sqrt(2 * r * tau + tau * tau)
            key = (kind, tau)
            st = stats.setdefault(key, {"n": 0, "mass_min": np.inf, "mass_max": 0.0, "mean_min": np.inf, "mean_max": 0.0,
                                        "mass_eq": 0, "mean_eq": 0})
            st["n"] += 1
            st["mass_min"] = min(st["mass_min"], ratio_mass)
            st["mass_max"] = max(st["mass_max"], ratio_mass)
            st["mean_min"] = min(st["mean_min"], ratio_mean)
            st["mean_max"] = max(st["mean_max"], ratio_mean)
            st["mass_eq"] += int(ratio_mass > 1 - 1e-7)
            st["mean_eq"] += int(ratio_mean > 1 - 1e-6)
    ok = True
    print("    type of nearest face           tau     clouds   (mass off Z)/(r tau/gamma): min, max, attained   "
          "|mean - z*|/sqrt(2 r tau + tau^2): min, max, attained")
    for key in sorted(stats):
        st = stats[key]
        print(f"    {key[0]:28s}  {key[1]:7.0e}   {st['n']:4d}     {st['mass_min']:.6f}  {st['mass_max']:.6f}  "
              f"{st['mass_eq']:4d}/{st['n']:<4d}                   {st['mean_min']:.6f}  {st['mean_max']:.6f}  "
              f"{st['mean_eq']:4d}/{st['n']}")
        ok &= st["mass_max"] <= 1 + 1e-7 and st["mean_max"] <= 1 + 1e-6
    # a moment body without interior points: a triangle in the plane z_3 = 1 of R^3, nearest point inside an edge
    P = np.array([[1.0, -1.0, 1.0], [1.0, 2.0, 1.0], [3.0, 0.5, 1.0]])
    zs, r, (B, wB) = nearest_point(P)
    f = P @ zs - r * r
    off = np.nonzero(f >= 1e-9)[0]
    gamma = f[off].min()
    print(f"    a triangle in the plane z_3 = 1 of R^3 (no interior points), nearest point {np.round(zs, 4)} in the "
          f"relative interior of an edge (a facet of the triangle):")
    for tau in (1e-4, 1e-3, 1e-2):
        c = np.zeros(3)
        c[off] = 1.0
        val, wv, slack = max_over_ball(P, c, r + tau, zs / r)
        print(f"        tau = {tau:.0e}: (largest mass off Z)/(r tau/gamma) = {val / (r * tau / gamma):.6f}")
    # E25(c): the largest length
    worst = 0.0
    attained = 0
    n = 0
    for trial in range(200):
        M = int(rng.integers(5, 10))
        P = rng.normal(size=(M, 2))
        norms = np.linalg.norm(P, axis=1)
        k = int(np.argmax(norms))
        gp = norms[k] - np.sort(norms)[-2]
        for frac in (0.2, 0.5, 1.0):
            tau = frac * gp
            best = 0.0
            for a in range(1440):
                u = np.array([np.cos(2 * np.pi * a / 1440), np.sin(2 * np.pi * a / 1440)])
                c = np.zeros(M)
                c[k] = 1.0
                res = linprog(c, A_ub=-(P @ u)[None, :], b_ub=[-(norms[k] - tau)], A_eq=np.ones((1, M)), b_eq=[1.0],
                              bounds=[(0, None)] * M, method="highs")
                if res.status == 0:
                    best = max(best, 1 - res.fun)
            worst = max(worst, best / (tau / gp))
            n += 1
            attained += int(best / (tau / gp) > 1 - 1e-6)
    print(f"    E25(c): 200 clouds in the plane, tau = 0.2, 0.5, 1.0 times gamma': largest (mass off x*)/(tau/gamma') = "
          f"{worst:.4f}; equal to one in {attained}/{n} cases (tau = gamma': the second farthest configuration itself)")
    ok &= worst <= 1 + 1e-6
    # E25(b), d = 1: a segment
    print("    E25(b) for d = 1 (not covered by the 'iff'): segment from (1,0) to (1,2): every length in [1, sqrt 5] "
          "determines the mean vector; segment from (1,-1) to (1,2): lengths in (1, sqrt 2] are shared by two mean vectors")
    return ok


# ------------------------------------------------------------------ D: E26
def lp_feasible(Aeq, beq, n):
    res = linprog(np.zeros(n), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * n, method="highs")
    return res.status == 0, res


def partition_reduction_consistent(a):
    m, A, n = len(a), float(sum(a)), 2 * len(a)
    for s in itertools.product((1, -1), repeat=m):
        Aeq = np.zeros((m + 2, n))
        beq = np.zeros(m + 2)
        for i in range(m):
            Aeq[i, 2 * i], Aeq[i, 2 * i + 1], beq[i] = A, -A, s[i] * a[i]
            Aeq[m, 2 * i], Aeq[m, 2 * i + 1] = A, -A
        Aeq[m + 1, :] = 1.0
        beq[m + 1] = 1.0
        if lp_feasible(Aeq, beq, n)[0]:
            return True
    return False


def has_partition(a):
    tot = sum(a)
    return tot % 2 == 0 and any(sum(a[i] for i in range(len(a)) if mask >> i & 1) * 2 == tot
                                for mask in range(1 << len(a)))


def x3c_reduction_consistent(triples, U):
    n = len(triples)
    for s in itertools.product((1, -1), repeat=n):
        Aeq = np.zeros((n + U + 1, 2 * n))
        beq = np.zeros(n + U + 1)
        for j in range(n):
            Aeq[j, 2 * j], Aeq[j, 2 * j + 1], beq[j] = n, -n, s[j]
        for u in range(U):
            deg = sum(u in T for T in triples)
            for j in range(n):
                if u in triples[j]:
                    Aeq[n + u, 2 * j] += n
                    Aeq[n + u, 2 * j + 1] -= n
            beq[n + u] = 2 - deg
        Aeq[n + U, :] = 1.0
        beq[n + U] = 1.0
        if lp_feasible(Aeq, beq, 2 * n)[0]:
            return True
    return False


def has_exact_cover(triples, U):
    n = len(triples)
    for mask in range(1 << n):
        cov = sorted(x for j in range(n) if mask >> j & 1 for x in triples[j])
        if cov == list(range(U)):
            return True
    return False


def identification_reduction(a):
    """X = {1..m} x {+,-} and one more configuration o;  phi_i(j, +-) = +-A [i = j], phi_i(o) = a_i;
    psi(j, +-) = +-A, psi(o) = 0;  data (E phi_i)^2 = a_i^2, (E psi)^2 = 0.  delta_o has the data.
    Returns the largest mass that a compatible ensemble can put off o (maximum over the 2^m sign vectors)."""
    m, A, n = len(a), float(sum(a)), 2 * len(a) + 1
    best = 0.0
    for s in itertools.product((1, -1), repeat=m):
        Aeq = np.zeros((m + 2, n))
        beq = np.zeros(m + 2)
        for i in range(m):
            Aeq[i, 2 * i], Aeq[i, 2 * i + 1], Aeq[i, n - 1], beq[i] = A, -A, a[i], s[i] * a[i]
            Aeq[m, 2 * i], Aeq[m, 2 * i + 1] = A, -A
        Aeq[m + 1, :] = 1.0
        beq[m + 1] = 1.0
        c = np.zeros(n)
        c[n - 1] = 1.0                                  # minimise the mass at o
        res = linprog(c, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * n, method="highs")
        if res.status == 0:
            best = max(best, 1 - res.fun)
    return best


def part_D():
    print("D. E26(b): the reductions, by brute force")
    agree = yes = 0
    for trial in range(120):
        m = int(rng.integers(2, 9))
        a = [int(v) for v in rng.integers(1, 15, size=m)]
        c, p = partition_reduction_consistent(a), has_partition(a)
        agree += int(c == p)
        yes += int(p)
    print(f"    partition: 120 random lists of 2 to 8 integers in 1..14: consistency of the squared-mean data agrees with "
          f"the existence of an equal-sum split in {agree}/120 ({yes} with a split)")
    ok = agree == 120
    xagree = xyes = 0
    maxnum = 0
    for trial in range(120):
        U = int(rng.choice((3, 6)))
        n = int(rng.integers(2, 8))
        triples = [tuple(sorted(int(v) for v in rng.choice(U, 3, replace=False))) for _ in range(n)]
        if trial % 3 == 0 and U == 6:
            perm = [int(v) for v in rng.permutation(U)]
            triples[0], triples[1] = tuple(sorted(perm[:3])), tuple(sorted(perm[3:]))
        c, e = x3c_reduction_consistent(triples, U), has_exact_cover(triples, U)
        xagree += int(c == e)
        xyes += int(e)
        for u in range(U):
            deg = sum(u in T for T in triples)
            maxnum = max(maxnum, (n + abs(deg - 2)) / (2 * n))
    print(f"    exact cover by 3-sets: 120 random families (2 to 7 triples of a set with 3 or 6 elements; repeated triples "
          f"and uncovered elements included): agreement in {xagree}/120 ({xyes} with a cover); largest "
          f"|number in the instance| / (2n) = {maxnum:.3f}")
    ok &= xagree == 120 and maxnum <= 1.0
    iagree = iyes = 0
    for trial in range(80):
        m = int(rng.integers(2, 8))
        a = [int(v) for v in rng.integers(1, 12, size=m)]
        off = identification_reduction(a)
        p = has_partition(a)
        iagree += int((off > 1e-7) == p)
        iyes += int(p)
    print(f"    identification (review's reduction): 80 random lists: 'delta_o is NOT the only ensemble with the squared-mean"
          f" data' agrees with the existence of an equal-sum split in {iagree}/80 ({iyes} with a split) -- deciding"
          f" 'determined' is coNP-hard")
    ok &= iagree == 80
    return ok


def main():
    ok = True
    for fn in (part_A, part_B, part_C, part_D):
        r = fn()
        print(f"  -> {'ok' if r else 'CHECK FAILED'}", flush=True)
        ok &= bool(r)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
