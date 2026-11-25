#!/usr/bin/env python3
"""Workstream L3 -- numerical attempts to FALSIFY the formal statements before proving them.

Own code; nothing imported from the other workstreams.  Everything is exhaustive over the cube
{0,1}^iota for small site sets iota; the hypotheses are exactly those of the Lean statements in
`Compensation.lean` / `TheoremA.lean` (which are more general than the paper's: an arbitrary
transitive SET of site permutations for Lemma 3, an arbitrary finite group acting on itself by
translation for Theorem A, two arbitrary probability vectors for Lemma 2).

Run:  python3 experiments/science/ws_L3/sanity_numerics.py      (about a minute)
"""
import itertools
import math
import random

import numpy as np

rng = np.random.default_rng(20261125)
random.seed(20261125)


# ----------------------------------------------------------------------------- cube helpers
def cube(n):
    return list(itertools.product((0, 1), repeat=n))


def act(x, sigma):
    """(x o sigma)(i) = x(sigma(i))."""
    return tuple(x[sigma[i]] for i in range(len(x)))


def mass(nu):
    return sum(nu.values())


def one(nu, i):
    return sum(v for x, v in nu.items() if x[i] == 1)


def marg(nu, i):
    return one(nu, i) / mass(nu)


def dens(nu, n):
    return sum(v * sum(x) for x, v in nu.items()) / (n * mass(nu))


def symmetrise(f, G, X):
    """average of f over the closure of G (G must be a group here)"""
    return {x: sum(f[act(x, s)] for s in G) / len(G) for x in X}


# ----------------------------------------------------------------------------- groups
def group_tables():
    """finite groups as (name, elements, op) -- sites are the group elements, shift a: i -> i + a"""
    out = []
    for n in (2, 3, 4, 5, 6):
        out.append((f"Z{n}", list(range(n)), lambda a, b, n=n: (a + b) % n))
    v4 = [(a, b) for a in (0, 1) for b in (0, 1)]
    out.append(("Z2xZ2", v4, lambda a, b: ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)))
    s3 = list(itertools.permutations(range(3)))
    out.append(("S3", s3, lambda a, b: tuple(a[b[i]] for i in range(3))))  # non-abelian
    return out


def shift_perms(elems, op):
    """for each a the site permutation i -> i + a, as index tuples"""
    idx = {e: j for j, e in enumerate(elems)}
    return [tuple(idx[op(e, a)] for e in elems) for a in elems]


# ----------------------------------------------------------------------------- S1, S2: Lemma 3
def check_lemma3(trials=300):
    worst_i = worst_ii = worst_ratio = 0.0
    n_cases = 0
    for name, elems, op in group_tables():
        n = len(elems)
        X = cube(n)
        G = shift_perms(elems, op)
        for _ in range(trials // 7 + 1):
            # reference weight: G-invariant, positive, NOT a product measure
            pi = symmetrise({x: rng.uniform(0.2, 2.0) for x in X}, G, X)
            w = symmetrise({x: rng.uniform(0.2, 2.0) for x in X}, G, X)
            Dl = symmetrise({x: max(rng.uniform(-1.0, 1.0), 0.0) for x in X}, G, X)
            wt = symmetrise({x: rng.uniform(0.2, 2.0) for x in X}, G, X)
            nw = {x: pi[x] * w[x] for x in X}
            nD = {x: pi[x] * Dl[x] for x in X}
            nt = {x: pi[x] * wt[x] for x in X}
            mt = mass(nt)
            wt = {x: wt[x] / mt for x in X}
            nt = {x: pi[x] * wt[x] for x in X}
            Aw, AD = mass(nw), mass(nD)
            if AD == 0:
                continue
            cw, cD, p2 = dens(nw, n), dens(nD, n), dens(nt, n)
            # (i): all marginals equal the density; marginals of a sum
            for i in range(n):
                worst_i = max(worst_i, abs(marg(nw, i) - cw), abs(marg(nD, i) - cD), abs(marg(nt, i) - p2))
                ns = {x: nw[x] + nD[x] for x in X}
                worst_i = max(worst_i, abs(marg(ns, i) - (Aw * cw + AD * cD) / (Aw + AD)))
            # (ii): the linear equation (identities need only p2 != cD, p2 != cw and non-zero masses)
            if abs(p2 - cD) < 1e-3 or abs(p2 - cw) < 1e-3:
                continue
            b = Aw * (cD - cw) / (p2 - cD)
            n0 = {x: nw[x] + b * nt[x] for x in X}
            n1 = {x: nw[x] + nD[x] + b * nt[x] for x in X}
            if abs(mass(n0)) < 1e-3 or abs(mass(n1)) < 1e-3:
                continue
            for i in range(n):
                worst_ii = max(worst_ii, abs(marg(n0, i) - cD), abs(marg(n1, i) - cD))
            worst_ratio = max(worst_ratio,
                              abs(mass(n1) / mass(n0) - (1 + (AD / Aw) * (p2 - cD) / (p2 - cw))))
            # b > 0 iff cD strictly between cw and p2 (given the sign pattern)
            between = (cw < cD < p2) or (p2 < cD < cw)
            if between:
                assert b > 0
            n_cases += 1
    print(f"S1 Lemma 3(i)  [7 groups, non-product invariant reference weights]: worst |marg - dens| = {worst_i:.2e}")
    print(f"S2 Lemma 3(ii) [{n_cases} cases]: worst |marg(w0,w1) - c_Delta| = {worst_ii:.2e}; "
          f"worst error of the mass-ratio formula = {worst_ratio:.2e}")


def check_transitive_set_not_group():
    """Lemma 3(i) needs only: for all i, j a permutation sigma with sigma(i)=j under which nu is invariant.
    Here: nu invariant under the cyclic group; G = the n-1 non-trivial rotations plus nothing else (not a group)."""
    n = 5
    X = cube(n)
    rots = [tuple((i + a) % n for i in range(n)) for a in range(n)]
    nu = symmetrise({x: rng.uniform(0.1, 1.0) for x in X}, rots, X)
    G = rots[1:]  # no identity: a transitive set, not a group
    assert all(any(s[i] == j for s in G) for i in range(n) for j in range(n) if i != j)
    worst = max(abs(marg(nu, i) - dens(nu, n)) for i in range(n))
    print(f"S1' transitive set that is not a group (n=5, rotations without the identity): worst = {worst:.2e}")


# ----------------------------------------------------------------------------- S3: Lemma 0 (window)
def flip(x, i):
    return x[:i] + (1 - x[i],) + x[i + 1:]


def random_cone_member(n, u):
    """a random member of W_u: w = exp(-psi), psi = min_y (a_y + u d(x,y)) (McShane) -- Lipschitz with constant u"""
    X = cube(n)
    a = {y: rng.uniform(0, 3 * u * n) for y in X}
    psi = {x: min(a[y] + u * sum(xi != yi for xi, yi in zip(x, y)) for y in X) for x in X}
    return {x: math.exp(-psi[x]) for x in X}


def bern_ref(n, p):
    return {x: math.prod(p if xi else 1 - p for xi in x) for x in cube(n)}


def p_tilt(p, g):
    return p * math.exp(-g) / (1 - p + p * math.exp(-g))


def check_window(trials=200):
    worst = 0.0
    for _ in range(trials):
        n = int(rng.integers(1, 6))
        p = rng.uniform(0.05, 0.95)
        u = rng.uniform(0.1, 2.5)
        X = cube(n)
        pi = bern_ref(n, p)
        w = random_cone_member(n, u)
        # membership of the cone, as defined in Lean (two-sided single-flip condition)
        for x in X:
            for i in range(n):
                assert math.exp(-u) * w[x] <= w[flip(x, i)] * (1 + 1e-12)
                assert w[flip(x, i)] <= math.exp(u) * w[x] * (1 + 1e-12)
        nu = {x: pi[x] * w[x] for x in X}
        lo, hi = p_tilt(p, u), p_tilt(p, -u)
        for i in range(n):
            m = marg(nu, i)
            worst = max(worst, lo - m, m - hi)
    print(f"S3 Lemma 0 (window) [{trials} random class members, n <= 5]: worst violation = {worst:.2e}")


# ----------------------------------------------------------------------------- S4: Lemma 2 (abstract)
def check_lemma2(trials=20000):
    worst_mass = worst_dens = -1.0
    for _ in range(trials):
        N = int(rng.integers(1, 9))
        P1 = rng.dirichlet(np.ones(N) * rng.uniform(0.1, 2))
        P2 = rng.dirichlet(np.ones(N) * rng.uniform(0.1, 2))
        R = 1 + rng.exponential(1.0) + 1e-6
        f = rng.uniform(0, 1, N)
        if rng.uniform() < 0.3:
            f = (f > 0.5).astype(float)
        D = np.maximum(R * P1 - P2, 0)
        E = D.sum()
        worst_mass = max(worst_mass, (R - 1) - E, E - R)
        worst_dens = max(worst_dens, abs((D * f).sum() / E - (P1 * f).sum()) - 1 / (R - 1))
    print(f"S4 Lemma 2 (abstract; {trials} random pairs of probability vectors): worst violation of "
          f"R-1 <= E <= R: {worst_mass:.2e}; of |c - c0| <= 1/(R-1): {worst_dens:.2e}")


# ----------------------------------------------------------------------------- S5: Theorem A, concrete
def tilt_w(p, gam, x):
    """w~ for site-dependent fields gam[i]"""
    return math.prod((math.exp(-gam[i]) if x[i] else 1.0) / (1 - p + p * math.exp(-gam[i])) for i in range(len(x)))


def check_theoremA():
    rows = []
    for name, elems, op in group_tables():
        n = len(elems)
        if n < 2:
            continue
        X = cube(n)
        G = shift_perms(elems, op)
        for (p, u, gam) in ((0.3, 1.0, 0.2), (0.1, 2.0, -0.7), (0.5, 1.5, 0.0), (0.7, 3.0, 3.0)):
            pi = bern_ref(n, p)
            pm, pp = p_tilt(p, u), p_tilt(p, -u)
            om = pp - pm
            for k in range(1, n):
                mlow = min(k, n - k) / n
                om_m = om * mlow
                for extra in (0.05, 1.0):
                    r = math.log(1 + 1 / om_m) + extra          # (e^r - 1) om_m > 1
                    kap = om_m - 1 / (math.exp(r) - 1)
                    beta = om / kap
                    assert kap > 0
                    Tk = [s for s in X if sum(s) == k]
                    base = {x: tilt_w(p, [gam] * n, x) for x in X}
                    cone = {s: {x: tilt_w(p, [(-u if s[i] else u) for i in range(n)], x) for x in X} for s in Tk}
                    dip = {s: {x: max(math.exp(r) * cone[s][x] - base[x], 0.0) for x in X} for s in Tk}
                    # masses and densities of the dips: the same for all s in T_k; Lemma 2 bounds
                    Es = [mass({x: pi[x] * dip[s][x] for x in X}) for s in Tk]
                    cs = [dens({x: pi[x] * dip[s][x] for x in X}, n) for s in Tk]
                    assert max(Es) - min(Es) < 1e-9 * max(Es) and max(cs) - min(cs) < 1e-9
                    E, c = Es[0], cs[0]
                    c0 = ((n - k) * pm + k * pp) / n
                    assert math.exp(r) - 1 <= E * (1 + 1e-12) and E <= math.exp(r) * (1 + 1e-12)
                    assert abs(c - c0) <= 1 / (math.exp(r) - 1) + 1e-12
                    assert pm + kap <= c + 1e-12 and c <= pp - kap + 1e-12
                    # averaged excess over the translations of the site group
                    bar = {s: {x: sum(dip[act(s, g)][x] for g in G) / n for x in X} for s in Tk}
                    pg = p_tilt(p, gam)
                    if c > pg:
                        g2, p2 = -u, pp
                    else:
                        g2, p2 = u, pm
                    b = 0.0 if c == pg else (c - pg) / (p2 - c)
                    assert -1e-12 <= b <= beta
                    comp = {x: tilt_w(p, [g2] * n, x) for x in X}
                    w0 = {x: base[x] + b * comp[x] for x in X}
                    A0 = mass({x: pi[x] * w0[x] for x in X})
                    worst_marg = 0.0
                    worst_cone = 0.0
                    gap_min = float("inf")
                    cnt = {x: 0 for x in X}
                    cnt_plain = {x: 0 for x in X}
                    for s in Tk:
                        w1 = {x: w0[x] + bar[s][x] for x in X}
                        n1 = {x: pi[x] * w1[x] for x in X}
                        for i in range(n):
                            worst_marg = max(worst_marg, abs(marg(n1, i) - c),
                                             abs(marg({x: pi[x] * w0[x] for x in X}, i) - c))
                        for x in X:
                            for i in range(n):
                                worst_cone = max(worst_cone, w1[flip(x, i)] / w1[x] - math.exp(u),
                                                 w0[flip(x, i)] / w0[x] - math.exp(u))
                            if bar[s][x] > 0:
                                cnt[x] += 1
                            if dip[s][x] > 0:
                                cnt_plain[x] += 1
                        gap_min = min(gap_min, math.log(mass(n1)) - math.log(A0))
                    assert worst_marg < 1e-9, worst_marg
                    assert worst_cone < 1e-9, worst_cone
                    assert gap_min >= math.log(1 + (math.exp(r) - 1) / (1 + beta)) - 1e-12
                    assert max(cnt.values()) <= n * max(cnt_plain.values())
                    rows.append((name, p, u, gam, k, r, b, beta, gap_min,
                                 max(cnt.values()), n * max(cnt_plain.values()), len(Tk)))
    print(f"S5 Theorem A, every finite ingredient, {len(rows)} parameter sets over 7 site groups "
          f"(Z2..Z6, Z2xZ2, S3): all assertions passed")
    print("    sample rows (group, p, u, gamma, k, r, b, beta, gap, max count, n*max plain count, |T_k|):")
    for row in rows[:: max(1, len(rows) // 6)]:
        print("    " + ", ".join(f"{v:.4g}" if isinstance(v, float) else str(v) for v in row))


# ----------------------------------------------------------------------------- S6: A16.5 core
def check_a16(trials=20000):
    worst_a = worst_b = worst_c = worst_d = -1.0
    for _ in range(trials):
        N = int(rng.integers(1, 8))
        t = np.exp(rng.uniform(-3, 3, N))
        U0 = rng.uniform(-2, 2)
        eta = rng.uniform(0, 3)
        phi = (t * np.log(t)).sum() + U0 * t.sum()
        f = lambda s: (1 - eta * U0) * s - eta * s * np.log(s)
        # (a) identity
        worst_a = max(worst_a, abs(t.sum() - f(t).sum() - eta * phi))
        # (b) concavity / maximiser
        if eta > 1e-3:
            sstar = math.exp(1 / eta - 1 - U0)
            s = np.exp(rng.uniform(-5, 5, 50))
            worst_b = max(worst_b, (f(s) - f(sstar)).max())
        # (c), (d): F(rho) = max of f over [e^{-u rho}, e^{u rho}] = f(clip(s*)); monotone in rho
        u = rng.uniform(0.1, 2)
        rho = np.sort(rng.uniform(0, 3, 2))

        def F(r):
            lo, hi = math.exp(-u * r), math.exp(u * r)
            if eta <= 1e-12:
                return f(hi) if True else None
            sstar_ = 1 / eta - 1 - U0
            sc = math.exp(min(max(sstar_, -u * r), u * r))
            grid = np.exp(np.linspace(-u * r, u * r, 400))
            worst = (f(grid)).max() - f(sc)
            return f(sc), worst

        if eta > 1e-9:
            (F0, e0), (F1, e1) = F(rho[0]), F(rho[1])
            worst_c = max(worst_c, F0 - F1, e0, e1)
            # (d) assembly
            rr = rng.uniform(0, 3, N)
            tt = np.exp(rng.uniform(-1, 1, N) * u * rr)
            worst_d = max(worst_d, (f(tt) - np.array([F(r)[0] for r in rr])).max())
    print(f"S6 A16.5 core [{trials} cases]: (a) identity error {worst_a:.2e}; (b) max of f - f(s*) = {worst_b:.2e}; "
          f"(c) F monotone / clipped level is the maximiser: worst {worst_c:.2e}; (d) f(t) - F(rho): worst {worst_d:.2e}")


if __name__ == "__main__":
    check_lemma3()
    check_transitive_set_not_group()
    check_window()
    check_lemma2()
    check_theoremA()
    check_a16()
