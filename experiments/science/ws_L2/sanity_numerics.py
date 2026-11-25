#!/usr/bin/env python3
"""Workstream L2 -- sanity numerics for the statements that are formalised in Lean.

Purpose (COMMON.md rule 3, "numerics before theory"): try to falsify, on small random
instances, the *formal statements* (with the hypotheses exactly as they are stated in the
Lean files), before proving them.  The theorems themselves are proved in Lean, not
inferred from these numbers.

Run:  python3 sanity_numerics.py      (seed fixed; about 20 s)
"""
import itertools
import math
import random
import sys
from fractions import Fraction

import numpy as np

rng = np.random.default_rng(20261125)
random.seed(20261125)
TOL = 1e-10


# --------------------------------------------------------------------------- A11
def cube(n):
    return [tuple(b) for b in itertools.product((0, 1), repeat=n)]


def join(x, y):
    return tuple(max(a, b) for a, b in zip(x, y))


def meet(x, y):
    return tuple(min(a, b) for a, b in zip(x, y))


def dist(x, y, cup, cdn):
    return sum(cup[i] for i in range(len(x)) if x[i] == 1 and y[i] == 0) + \
        sum(cdn[i] for i in range(len(x)) if x[i] == 0 and y[i] == 1)


def random_submodular(n):
    """additive + non-positive pair couplings + concave function of a non-negative
    weighted sum (all submodular)."""
    a = rng.normal(size=n)
    J = -np.abs(rng.normal(size=(n, n)))
    w = np.abs(rng.normal(size=n))
    kind = rng.integers(0, 3)

    def f(x):
        v = float(np.dot(a, x))
        for i in range(n):
            for j in range(i + 1, n):
                v += J[i, j] * x[i] * x[j]
        if kind == 1:
            v += math.sqrt(1.0 + float(np.dot(w, x)))  # a concave function of a modular one is submodular
        if kind == 2:
            v += min(1.5, float(np.dot(w, x)))
        return v
    return f


def random_admissible(n, cup, cdn, X):
    """McShane-type: g(x) = min_a (v(a) + d(x, a)); admissible when d satisfies the
    triangle inequality, i.e. when cup_i + cdn_i >= 0 for all i."""
    k = int(rng.integers(1, 5))
    anchors = [X[int(rng.integers(0, len(X)))] for _ in range(k)]
    v = rng.normal(scale=2.0, size=k)
    return {x: min(v[j] + dist(x, anchors[j], cup, cdn) for j in range(k)) for x in X}


def check_A11(trials=400):
    worst_holley = 0.0
    worst_sandwich = 0.0
    worst_macro = 0.0
    worst_field = 0.0
    strict_seen = 0
    for t in range(trials):
        n = int(rng.integers(1, 5))
        X = cube(n)
        beta = float(rng.uniform(0.0, 2.0))
        if t % 2 == 0:
            cup = np.abs(rng.normal(size=n))
            cdn = np.abs(rng.normal(size=n))
        else:  # signs allowed, only cup_i + cdn_i >= 0
            cup = rng.normal(size=n)
            cdn = -cup + np.abs(rng.normal(size=n))
        f = random_submodular(n)
        fv = {x: f(x) for x in X}
        # submodularity of the generated f
        for x in X:
            for y in X:
                assert fv[join(x, y)] + fv[meet(x, y)] <= fv[x] + fv[y] + 1e-9
        g = random_admissible(n, cup, cdn, X)
        for x in X:
            for y in X:
                assert g[x] - g[y] <= dist(x, y, cup, cdn) + 1e-9
        hup = {x: float(np.dot(cup, x)) for x in X}
        hdn = {x: float(np.dot(cdn, x)) for x in X}
        # the two fields are admissible
        for x in X:
            for y in X:
                worst_field = max(worst_field, hup[x] - hup[y] - dist(x, y, cup, cdn))
                worst_field = max(worst_field, -hdn[x] + hdn[y] - dist(x, y, cup, cdn))
        wlo = {x: math.exp(-beta * (fv[x] + hup[x])) for x in X}
        wg = {x: math.exp(-beta * (fv[x] + g[x])) for x in X}
        whi = {x: math.exp(-beta * (fv[x] - hdn[x])) for x in X}
        # Holley conditions
        for x in X:
            for y in X:
                a, b = meet(x, y), join(x, y)
                worst_holley = max(worst_holley, (wlo[x] * wg[y] - wlo[a] * wg[b]) / (wlo[a] * wg[b]))
                worst_holley = max(worst_holley, (wg[x] * whi[y] - wg[a] * whi[b]) / (wg[a] * whi[b]))
        # sandwich for a random monotone phi (any sign)
        base = rng.normal(size=n)
        phi = {x: max((float(np.dot(np.abs(base), y)) + s
                       for y, s in [(x, 0.0)]), default=0.0) - 1.0 for x in X}
        # a random up-set indicator added
        gens = [X[int(rng.integers(0, len(X)))] for _ in range(2)]
        B = {x for x in X if any(all(x[i] >= z[i] for i in range(n)) for z in gens)}
        for x in X:
            phi[x] += 0.7 * (x in B)

        def E(w, h):
            return sum(h[x] * w[x] for x in X) / sum(w.values())
        e1, e2, e3 = E(wlo, phi), E(wg, phi), E(whi, phi)
        worst_sandwich = max(worst_sandwich, e1 - e2, e2 - e3)
        if e1 < e2 - 1e-9 or e2 < e3 - 1e-9:
            strict_seen += 1
        # macrostates
        A = [x for x in X if x not in B]
        if A and B:
            def Z(w, S):
                return sum(w[x] for x in S)
            # relative violations (the products can be very large)
            worst_macro = max(worst_macro,
                              Z(wg, A) * Z(wlo, B) / (Z(wlo, A) * Z(wg, B)) - 1.0,
                              Z(whi, A) * Z(wg, B) / (Z(wg, A) * Z(whi, B)) - 1.0)
    print(f"A11: {trials} instances, n=1..4, half with signed constants (cup+cdn>=0):")
    print(f"   worst violation of field admissibility      {worst_field:.2e}")
    print(f"   worst relative violation of Holley cond.     {worst_holley:.2e}")
    print(f"   worst violation of E_lo<=E_g<=E_hi           {worst_sandwich:.2e}")
    print(f"   worst relative violation of macrostate products {worst_macro:.2e}")
    print(f"   instances with a strict inequality           {strict_seen}")
    assert worst_field < TOL and worst_holley < TOL and worst_sandwich < TOL and worst_macro < TOL


def check_A11_needs():
    """Hypotheses are needed: (a) beta < 0 reverses; (b) cup+cdn < 0 makes the field
    inadmissible (and the class empty)."""
    n = 2
    X = cube(n)
    cup = np.array([1.0, 0.5])
    cdn = np.array([0.3, 0.2])
    g = {x: 0.0 for x in X}
    fv = {x: 0.0 for x in X}
    hup = {x: float(np.dot(cup, x)) for x in X}
    phi = {x: float(sum(x)) for x in X}
    for beta in (1.0, -1.0):
        wlo = {x: math.exp(-beta * (fv[x] + hup[x])) for x in X}
        wg = {x: math.exp(-beta * (fv[x] + g[x])) for x in X}
        e1 = sum(phi[x] * wlo[x] for x in X) / sum(wlo.values())
        e2 = sum(phi[x] * wg[x] for x in X) / sum(wg.values())
        print(f"A11 needs beta>=0: beta={beta:+.0f}:  E_(f+hup) phi = {e1:.4f},  E_(f+g) phi = {e2:.4f}"
              f"  ({'<=' if e1 <= e2 else '>'})")


# --------------------------------------------------------------------------- R6.1
def check_R61(trials=2000):
    worst = 0.0
    worstZ = 0.0
    for t in range(trials):
        m = int(rng.integers(1, 9))
        g0 = rng.normal(scale=2.0, size=m)
        T = rng.normal(scale=2.0, size=m)
        if t % 5 == 0:
            T = g0 + np.abs(rng.normal(size=m))  # E = 0, D = 0
        if t % 7 == 0:
            T[: m // 2] = g0[: m // 2]  # ties
        gp = np.minimum(g0, T)
        Z0 = np.exp(-g0).sum()
        U0 = (g0 * np.exp(-g0)).sum() / Z0
        Zp = np.exp(-gp).sum()
        Up = (gp * np.exp(-gp)).sum() / Zp
        E = np.maximum(np.exp(-T) - np.exp(-g0), 0.0).sum()
        D = sum(T[i] * math.exp(-T[i]) - g0[i] * math.exp(-g0[i]) for i in range(m) if T[i] < g0[i])
        worstZ = max(worstZ, abs(Zp - (Z0 + E)) / Zp)
        worst = max(worst, abs((Up - U0) - (D - U0 * E) / (Z0 + E)))
        if E > 1e-12:
            worst = max(worst, abs((Up - U0) - (E / (Z0 + E)) * (D / E - U0)))
        else:
            assert abs(D) < 1e-12 and abs(Up - U0) < 1e-12
    print(f"R6.1: {trials} random pairs (g0,T), up to 8 points: |Z'-(Z0+E)|/Z' <= {worstZ:.1e},"
          f" identity error <= {worst:.1e}")
    assert worst < 1e-9 and worstZ < 1e-12


# --------------------------------------------------------------------------- R5(2)
def check_R52(trials=3000):
    worst = float("inf")
    for t in range(trials):
        m = int(rng.integers(1, 8))
        a = np.abs(rng.normal(size=m))
        s = a.sum() - sum(min(a[i], a[j]) for i in range(m) for j in range(i + 1, m))
        worst = min(worst, a.max() - s)
    print(f"R5(2) max >= sum - pairwise minima, nonneg families: least slack {worst:.2e}")
    assert worst > -1e-12
    a = np.array([0.0, 0.0, -1.0])
    s = a.sum() - sum(min(a[i], a[j]) for i in range(3) for j in range(i + 1, 3))
    print(f"R5(2) without nonnegativity: family (0,0,-1): max = {a.max()}, sum - pairwise minima = {s}"
          f"  -> inequality {'holds' if a.max() >= s else 'FAILS'}")
    # the assembled statement on a small cube
    worst2 = float("inf")
    worst3 = float("inf")
    for t in range(60):
        n = int(rng.integers(3, 9))
        X = np.array(cube(n))
        k = int(rng.integers(1, 5))
        C = X[rng.choice(len(X), size=k, replace=False)]
        u = float(rng.uniform(0.3, 3.0))
        R = int(rng.integers(0, n + 1))
        dC = np.array([[int((x != c).sum()) for c in C] for x in X])  # distances to the centres
        dmin = dC.min(axis=1)
        Zcone = np.exp(-u * dC[:, 0]).sum()
        Zflat = np.exp(-u * np.maximum(dC[:, 0], R)).sum()
        ZconeC = np.exp(-u * dmin).sum()
        ZflatC = np.exp(-u * np.maximum(dmin, R)).sum()
        worst2 = min(worst2, k * Zflat - ZflatC)
        pair = 0.0
        for i in range(k):
            for j in range(i + 1, k):
                D = int((C[i] != C[j]).sum())
                closed = (1 + math.exp(-u)) ** (n - D) * (2 * math.exp(-u / 2)) ** D
                direct = np.exp(-u * (dC[:, i] + dC[:, j]) / 2).sum()
                assert abs(closed - direct) < 1e-9 * closed
                assert abs(closed - Zcone * math.cosh(u / 2) ** (-D)) < 1e-9 * closed
                pair += direct
        worst3 = min(worst3, ZconeC - (k * Zcone - pair))
    print(f"R5(2) on cubes n=3..8, random centre sets: least slack of |C|Z(flat) - Z(flat^C): {worst2:.2e};"
          f" of Z(cone^C) - (|C|Z(cone) - pair sums): {worst3:.2e}")
    assert worst2 > -1e-9 and worst3 > -1e-9


# --------------------------------------------------------------------------- R6.2
def binom(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0


def r62_instance(n, r1, u, D):
    """Exact (floating point, by classes) sums for centres at Hamming distance D.
    Points are classified by (i, j): i = number of the D differing coordinates on which
    x agrees with a' (so disagrees with a0), j = number of the n-D common coordinates on
    which x differs from both.  d0 = i + j, d' = (D - i) + j.  Multiplicity C(D,i)C(n-D,j)."""
    out = {}
    W = sum(binom(n, d) * math.exp(u * (r1 - d)) for d in range(0, r1))
    V = sum(binom(n, d) for d in range(0, r1))
    Z0 = 2.0 ** n + W - V
    Ap = sum(binom(n, d) * u * (r1 - d) * math.exp(u * (r1 - d)) for d in range(0, r1))
    U0 = -Ap / Z0
    for s in (+1, -1):
        E = 0.0
        Dsum = 0.0
        omega = 0.0
        Zp = 0.0
        Nump = 0.0
        for i in range(D + 1):
            for j in range(n - D + 1):
                mult = binom(D, i) * binom(n - D, j)
                d0 = i + j
                dp = (D - i) + j
                g0 = -u * max(r1 - d0, 0)
                T = -u * max(r1 + s - dp, 0)
                gp = min(g0, T)
                Zp += mult * math.exp(-gp)
                Nump += mult * gp * math.exp(-gp)
                E += mult * max(math.exp(-T) - math.exp(-g0), 0.0)
                if T < g0:
                    Dsum += mult * (T * math.exp(-T) - g0 * math.exp(-g0))
                if g0 < 0 and T < 0:
                    omega += mult * math.exp(-T)
        out[s] = dict(E=E, D=Dsum, omega=omega, Zp=Zp, Up=Nump / Zp)
    return W, V, Z0, Ap, U0, out


def check_R62():
    print("R6.2 (exact sums by classes; hypotheses (i) W >= 8 r1 e^u 2^n, (ii) omega_+1 <= e^-u W/(2(r1+1))):")
    rows = 0
    viol = 0
    hyp_true = 0
    for n in (12, 16, 20, 24, 30, 40):
        for r1 in range(1, (n - 1) // 2 + 1):
            for u in (0.5, 1.0, 2.0, 3.0, 4.0, 6.0):
                for D in sorted(set([n, n // 2, (3 * n) // 4, n // 4, 2 * r1, 2 * r1 + 1, 1])):
                    if D < 1 or D > n:
                        continue
                    W, V, Z0, Ap, U0, out = r62_instance(n, r1, u, D)
                    rows += 1
                    hyp_i = W >= 8 * r1 * math.exp(u) * 2.0 ** n
                    hyp_ii = out[+1]["omega"] <= math.exp(-u) * W / (2 * (r1 + 1))
                    # excess identity R6.1 on this instance
                    for s in (+1, -1):
                        o = out[s]
                        assert abs(o["Zp"] - (Z0 + o["E"])) <= 1e-9 * o["Zp"]
                        assert abs((o["Up"] - U0) - (o["D"] - U0 * o["E"]) / (Z0 + o["E"])) <= 1e-9 * (1 + abs(U0))
                    if hyp_i and hyp_ii:
                        hyp_true += 1
                        ok = out[+1]["Up"] < U0 < out[-1]["Up"]
                        # the lower bound on the gain in ln Z at s = -1 (hence at every s >= -1)
                        gain = math.log(out[-1]["Zp"]) - math.log(Z0)
                        ok2 = gain >= math.log(1 + math.exp(-u) * (1 - 1.0 / r1)) - 1e-12
                        if not (ok and ok2):
                            viol += 1
                            print("   VIOLATION", n, r1, u, D, out[+1]["Up"] - U0, out[-1]["Up"] - U0, gain)
    print(f"   {rows} instances (n in 12..40, all r1 < n/2, u in 0.5..6, 7 distances);"
          f" hypotheses hold in {hyp_true}; conclusion violated in {viol}")
    # one explicit instance for the report
    n, r1, u, D = 24, 5, 4.0, 24
    W, V, Z0, Ap, U0, out = r62_instance(n, r1, u, D)
    print(f"   example n={n}, r1={r1}, u={u}, D={D}: W/(8 r1 e^u 2^n) = {W / (8 * r1 * math.exp(u) * 2.0 ** n):.3g},"
          f" omega_+1 = {out[+1]['omega']:.3g}, U'_+1-U0 = {out[+1]['Up'] - U0:+.4f}, U'_-1-U0 = {out[-1]['Up'] - U0:+.4f}")
    assert viol == 0


def check_R62_hypotheses_needed():
    """Is each hypothesis needed for the two signs?  Search instances where exactly one fails."""
    fail_i = None
    fail_ii = None
    for n in (12, 16, 20, 24, 30):
        for r1 in range(1, (n - 1) // 2 + 1):
            for u in (0.25, 0.5, 1.0, 2.0, 3.0, 4.0):
                for D in range(1, n + 1):
                    W, V, Z0, Ap, U0, out = r62_instance(n, r1, u, D)
                    hyp_i = W >= 8 * r1 * math.exp(u) * 2.0 ** n
                    hyp_ii = out[+1]["omega"] <= math.exp(-u) * W / (2 * (r1 + 1))
                    ok = out[+1]["Up"] < U0 < out[-1]["Up"]
                    if not ok:
                        if hyp_ii and not hyp_i and fail_i is None:
                            fail_i = (n, r1, u, D, out[+1]["Up"] - U0, out[-1]["Up"] - U0)
                        if hyp_i and not hyp_ii and fail_ii is None:
                            fail_ii = (n, r1, u, D, out[+1]["Up"] - U0, out[-1]["Up"] - U0)
    print(f"   signs fail with (ii) true, (i) false:  {fail_i}")
    print(f"   signs fail with (i) true, (ii) false:  {fail_ii}")


# --------------------------------------------------------------------------- A1.2
def check_A12(trials=300):
    worst_window = 0.0
    worst_chain = 0.0
    worst_bound = float("inf")
    worst_add = 0.0
    for t in range(trials):
        nsites = int(rng.integers(1, 4))
        sizes = [int(rng.integers(2, 4)) for _ in range(nsites)]
        pis = [rng.dirichlet(np.ones(s)) + 0.02 for s in sizes]
        pis = [p / p.sum() for p in pis]
        Qs = [rng.dirichlet(np.ones(s)) + 0.02 for s in sizes]
        Qs = [q / q.sum() for q in Qs]
        # asymmetric envelopes with triangle inequality: shortest paths of random nonneg matrices
        ds = []
        for s in sizes:
            M = np.abs(rng.normal(size=(s, s)))
            np.fill_diagonal(M, 0.0)
            for k in range(s):
                for i in range(s):
                    for j in range(s):
                        M[i, j] = min(M[i, j], M[i, k] + M[k, j])
            ds.append(M)
        X = list(itertools.product(*[range(s) for s in sizes]))

        def d(x, y):
            return sum(ds[i][x[i], y[i]] for i in range(nsites))
        k = int(rng.integers(1, 4))
        anchors = [X[int(rng.integers(0, len(X)))] for _ in range(k)]
        v = rng.normal(scale=2.0, size=k)
        psi = {x: min(v[j] + d(x, anchors[j]) for j in range(k)) for x in X}
        for x in X:
            for y in X:
                assert psi[x] - psi[y] <= d(x, y) + 1e-9
        w = {x: math.prod(pis[i][x[i]] for i in range(nsites)) * math.exp(-psi[x]) for x in X}
        Zt = sum(w.values())
        nu = {x: w[x] / Zt for x in X}
        Q = {x: math.prod(Qs[i][x[i]] for i in range(nsites)) for x in X}
        KL = sum(nu[x] * math.log(nu[x] / Q[x]) for x in X)
        # item 2: every site, every subset P of the other sites, every pattern on P
        for i in range(nsites):
            others = [j for j in range(nsites) if j != i]
            for rP in range(len(others) + 1):
                for P in itertools.combinations(others, rP):
                    for pat in itertools.product(*[range(sizes[j]) for j in P]):
                        N = np.zeros(sizes[i])
                        for x in X:
                            if all(x[j] == pat[idx] for idx, j in enumerate(P)):
                                N[x[i]] += nu[x]
                        p = N / N.sum()
                        for a in range(sizes[i]):
                            for b in range(sizes[i]):
                                worst_window = max(worst_window,
                                                   pis[i][a] * p[b] - math.exp(ds[i][a, b]) * pis[i][b] * p[a])
        # item 3: chain rule in the natural order, and the bound by window maxima.
        chain = 0.0
        for i in range(nsites):
            for pat in itertools.product(*[range(sizes[j]) for j in range(i)]):
                N = np.zeros(sizes[i])
                for x in X:
                    if x[:i] == pat:
                        N[x[i]] += nu[x]
                mass = N.sum()
                p = N / mass
                chain += mass * sum(p[a] * math.log(p[a] / Qs[i][a]) for a in range(sizes[i]))
        worst_chain = max(worst_chain, abs(chain - KL))
        # window maximum by brute force over a fine grid is expensive; use vertices of the window
        # computed by enumerating spanning tight sets (small alphabets): maximise the convex KL over
        # the Gibbs laws of the extreme points of L (found by LP in random directions).
        from scipy.optimize import linprog
        total = 0.0
        for i in range(nsites):
            s = sizes[i]
            best = 0.0
            # LP over the window in p-coordinates in many random directions gives vertices
            A_ub = []
            b_ub = []
            for a in range(s):
                for b in range(s):
                    if a != b:
                        row = np.zeros(s)
                        row[b] += pis[i][a]
                        row[a] -= math.exp(ds[i][a, b]) * pis[i][b]
                        A_ub.append(row)
                        b_ub.append(0.0)
            for _ in range(40):
                c = rng.normal(size=s)
                res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub), A_eq=np.ones((1, s)), b_eq=[1.0],
                              bounds=[(0, 1)] * s, method="highs")
                assert res.status == 0
                p = np.clip(res.x, 1e-300, 1)
                best = max(best, float(sum(p[a] * math.log(p[a] / Qs[i][a]) for a in range(s))))
            total += best
        worst_bound = min(worst_bound, total - KL)
        # additive instance: equality KL = sum of site KLs
        gam = [rng.normal(size=s) for s in sizes]
        wa = {x: math.prod(pis[i][x[i]] * math.exp(-gam[i][x[i]]) for i in range(nsites)) for x in X}
        Za = sum(wa.values())
        nua = {x: wa[x] / Za for x in X}
        KLa = sum(nua[x] * math.log(nua[x] / Q[x]) for x in X)
        site = 0.0
        for i in range(nsites):
            p = pis[i] * np.exp(-gam[i])
            p = p / p.sum()
            site += float(sum(p[a] * math.log(p[a] / Qs[i][a]) for a in range(sizes[i])))
        worst_add = max(worst_add, abs(KLa - site))
    print(f"A1.2: {trials} instances, 1..3 sites, 2..3 letters, asymmetric envelopes:")
    print(f"   item 2, worst violation of the window inequalities (all sites, all conditioning sets) {worst_window:.2e}")
    print(f"   item 3, chain rule identity error {worst_chain:.1e}; least slack of sum of window maxima - KL {worst_bound:.2e}")
    print(f"   additive instances: |KL - sum of site KLs| <= {worst_add:.1e}")
    assert worst_window < TOL and worst_chain < 1e-9 and worst_bound > -1e-7 and worst_add < 1e-9


if __name__ == "__main__":
    check_A11()
    check_A11_needs()
    check_R61()
    check_R52()
    check_R62()
    check_R62_hypotheses_needed()
    check_A12()
    print("all checks passed")
