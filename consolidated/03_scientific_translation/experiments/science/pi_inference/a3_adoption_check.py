#!/usr/bin/env python3
"""Coordinator's own check of the three statements of workstream A3 that addendum A17 adopts.

Written independently of experiments/science/ws_A3/check_math.py (nothing imported from it).

 (1) A3.2: on a product reference measure pi with one-site oscillations c_i of the remainder r,
         D_p(pi_g || pi)  <=  sum_i [ (p-1) c_i^2/8 + L(c_i) ]  <=  p K/8,     K = sum_i c_i^2,
     against A17.6's  p^2 K/(8(p-1)).   Exact enumeration, 50-digit arithmetic for the divergence.
 (2) the second-order sandwich of the Jensen gap  K = ln E e^{-(r-Er)}:
         ln(1 + Var (e^{-a} - 1 + a)/a^2)  <=  K  <=  W(b, Var)  <=  ln(1 + (Var/b^2)(e^b - 1 - b))  <=  (Var/b^2)(e^b - 1 - b)
     for a law with  E r - b <= r <= E r + a.
 (3) A3.3(a): the rule "stop when the first N(v) values of the remainder are all equal to v" at the
     centre of a constant box: the count N(0) and its exact failure probability against two-level
     and three-level members of the box.

Run:  python3 a3_adoption_check.py > a3_adoption_check.log     (about a minute)
"""
import itertools
import math
import sys

import mpmath as mp
import numpy as np

mp.mp.dps = 50
rng = np.random.default_rng(20261126)


def L(w):
    """log of Specht's ratio: the largest Jensen gap of a variable of range w."""
    if w < 1e-8:
        return w * w / 8.0
    return math.log(math.expm1(w) / w) - 1.0 + w / math.expm1(w)


def W_sharp(b, s2):
    if b < 1e-12 or s2 < 1e-300:
        return 0.0
    return math.log1p((b * b * math.expm1(-s2 / b) + s2 * math.expm1(b)) / (b * b + s2))


# ---------------------------------------------------------------------------------------------
print("# (1) A3.2 on product measures: D_p <= sum[(p-1)c_i^2/8 + L(c_i)] <= pK/8")


def one_site_osc(r, shape):
    """c_i = max over the other coordinates of the oscillation of r in coordinate i."""
    c = []
    for i in range(len(shape)):
        c.append(float((r.max(axis=i) - r.min(axis=i)).max()))
    return c


def renyi_mp(pi, r, p):
    """D_p(pi_g || pi) with pi_g ∝ pi e^{-r}, in 50 digits.  p = 1 is Kullback-Leibler."""
    piv = [mp.mpf(float(x)) for x in pi.ravel()]
    rv = [mp.mpf(float(x)) for x in r.ravel()]
    mu = mp.fsum(a * mp.e ** (-b) for a, b in zip(piv, rv))
    if p == 1:
        return mp.fsum(a * mp.e ** (-b) / mu * (-b - mp.log(mu)) for a, b in zip(piv, rv))
    m_p = mp.fsum(a * mp.e ** (-p * b) for a, b in zip(piv, rv))
    return (mp.log(m_p) - p * mp.log(mu)) / (p - 1)


def random_member(shape, kind, scale):
    n = len(shape)
    if kind == "table":                      # an arbitrary table: strongly non-additive
        return scale * rng.standard_normal(shape)
    if kind == "additive":
        r = np.zeros(shape)
        for i in range(n):
            v = scale * rng.standard_normal(shape[i])
            sl = [None] * n
            sl[i] = slice(None)
            r = r + v[tuple(sl)]
        return r
    if kind == "min":                        # minimum of two additive functions (a basin)
        return np.minimum(random_member(shape, "additive", scale), random_member(shape, "additive", scale) + scale)
    if kind == "pair":                       # additive plus nearest-neighbour pair tables
        r = random_member(shape, "additive", scale)
        for i in range(n - 1):
            t = scale * rng.standard_normal((shape[i], shape[i + 1]))
            sl = [None] * n
            sl[i] = slice(None)
            sl[i + 1] = slice(None)
            r = r + t[tuple(sl)]
        return r
    raise ValueError(kind)


def random_product(shape):
    pi = np.ones(shape)
    for i, k in enumerate(shape):
        v = rng.dirichlet(np.ones(k) * rng.choice([0.3, 1.0, 5.0]))
        sl = [None] * len(shape)
        sl[i] = slice(None)
        pi = pi * v[tuple(sl)]
    return pi


orders = [1, 1.05, 1.5, 2, 3, 6, 12]
worst_ref = {p: 0.0 for p in orders}       # D_p / refined bound
worst_pk8 = {p: 0.0 for p in orders}       # D_p / (pK/8)
worst_a176 = {p: 0.0 for p in orders if p > 1}   # D_p / (p^2 K/(8(p-1)))
count = 0
for trial in range(900):
    n = int(rng.integers(2, 7))
    k = int(rng.choice([2, 2, 3]))
    if k == 3 and n > 5:
        n = 5
    shape = (k,) * n
    kind = ["table", "additive", "min", "pair"][trial % 4]
    scale = float(rng.choice([0.05, 0.2, 0.6, 1.5, 3.0]))
    r = random_member(shape, kind, scale)
    pi = random_product(shape)
    c = one_site_osc(r, shape)
    K = sum(x * x for x in c)
    if K < 1e-3:
        continue
    count += 1
    for p in orders:
        d = float(renyi_mp(pi, r, p))
        ref = sum((p - 1) * x * x / 8.0 + L(x) for x in c)
        assert ref <= p * K / 8.0 * (1 + 1e-12)
        worst_ref[p] = max(worst_ref[p], d / ref)
        worst_pk8[p] = max(worst_pk8[p], d / (p * K / 8.0))
        if p > 1:
            worst_a176[p] = max(worst_a176[p], d / (p * p * K / (8.0 * (p - 1))))
        if d > ref * (1 + 1e-9):
            print("   VIOLATION", trial, kind, shape, p, d, ref)
            sys.exit(1)
print(f"   {count} random members (tables, additive, minima of two additive functions, chains of pair tables) on {{0,1}}^n, n <= 6, and {{0,1,2}}^n, n <= 5; random product measures; exact enumeration, 50 digits")
print("   order p:                         " + "  ".join(f"{p:>6}" for p in orders))
print("   largest D_p / refined bound:     " + "  ".join(f"{worst_ref[p]:6.4f}" for p in orders))
print("   largest D_p / (pK/8):            " + "  ".join(f"{worst_pk8[p]:6.4f}" for p in orders))
print("   largest D_p / (p^2 K/(8(p-1))):  " + "  ".join(("   -  " if p == 1 else f"{worst_a176[p]:6.4f}") for p in orders) + "     (the bound of A17.6 as first written)")
assert max(worst_ref.values()) <= 1.0

print("   additive instance r = u|x| on the uniform cube (per site, exact):")
for u in [0.01, 0.1, 0.5, 1.0, 2.0, 4.0]:
    d2 = math.log1p(math.tanh(u / 2) ** 2)
    ref2 = u * u / 8 + L(u)
    print(f"      u = {u:5.2f}:  D_2 = {d2:.6e},  refined bound = {ref2:.6e} (ratio {d2/ref2:.4f}),  K/4 = {u*u/4:.6e},  K/2 = {u*u/2:.6e}")
    assert d2 <= ref2 * (1 + 1e-12)

# ---------------------------------------------------------------------------------------------
print("# (2) second-order sandwich of the Jensen gap under a floor b and a ceiling a (both measured from the mean)")
worst_low = 0.0
worst_up = 0.0
worst_mid = 0.0
worst_weak = 0.0
used = 0
for trial in range(30000):
    m = int(rng.integers(2, 8))
    q = rng.dirichlet(np.ones(m) * rng.choice([0.2, 1.0, 4.0]))
    x = rng.standard_normal(m) * float(rng.choice([0.05, 0.3, 1.0, 3.0]))
    mean = float(q @ x)
    xc = x - mean
    xc = xc - float(q @ xc)                 # remove the rounding residue of the centring
    var = float(q @ (xc * xc))
    b = float(-xc.min())                    # floor below the mean
    a = float(xc.max())                     # ceiling above the mean
    if var < 1e-6 or b < 1e-3 or a < 1e-3:
        continue
    used += 1
    gap = float(mp.log(mp.fsum(mp.mpf(float(qq)) * mp.e ** (-mp.mpf(float(v))) for qq, v in zip(q, xc))))
    low = math.log1p(var * (math.expm1(-a) + a) / (a * a))
    up = W_sharp(b, var)
    mid = math.log1p(var / (b * b) * (math.expm1(b) - b))
    weak = var / (b * b) * (math.expm1(b) - b)
    worst_low = max(worst_low, low / gap)
    worst_up = max(worst_up, gap / up)
    worst_mid = max(worst_mid, up / mid)
    worst_weak = max(worst_weak, mid / weak)
print(f"   {used} random laws with 2-7 atoms:  largest lower/gap = {worst_low:.6f},  largest gap/W = {worst_up:.6f},  largest W/middle = {worst_mid:.6f},  largest middle/weak = {worst_weak:.6f}   (all must be <= 1)")
assert max(worst_low, worst_up, worst_mid, worst_weak) <= 1 + 1e-9
# the two-point extremal laws
for b, s2 in [(0.5, 0.01), (2.0, 0.3), (5.0, 1.0)]:
    pfl = s2 / (b * b + s2)
    gap = math.log(pfl * math.exp(b) + (1 - pfl) * math.exp(-s2 / b))
    print(f"   two-point law with a state at the floor, b = {b}, variance {s2}: gap = {gap:.10f}, W = {W_sharp(b, s2):.10f}")
    assert abs(gap - W_sharp(b, s2)) < 1e-12

# ---------------------------------------------------------------------------------------------
print("# (3) A3.3(a): certification at the centre of a constant box without a hint")


def q_of(v, rho_minus, eta):
    first = math.inf if rho_minus + v <= 0 else (math.expm1(eta)) / (math.expm1(rho_minus + v))
    return min(first, 1.0 - math.exp(-eta))


def N_of(v, rho_minus, eta, delta):
    return math.ceil(math.log(1.0 / delta) / q_of(v, rho_minus, eta)) + 1


for rho_minus, rho_plus, eta, delta in [(3.0, 3.0, 0.1, 0.05), (1.0, 1.0, 0.05, 0.05), (5.0, 2.0, 0.2, 0.01)]:
    N0 = N_of(0.0, rho_minus, eta, delta)
    hinted = math.ceil(2 * math.log(1 / delta) * math.expm1(rho_minus) / math.expm1(eta))
    # exact probability that the rule outputs a value off by more than eta, for members with
    # values in a three-point set {v1, v2, v3} of the box and every law on them (grid)
    worst = 0.0
    levels = [-rho_minus, -rho_minus / 2, 0.0, rho_plus / 2, rho_plus]
    grid = np.linspace(0.0, 1.0, 201)
    for trip in itertools.combinations(levels, 3):
        Ns = [N_of(v, rho_minus, eta, delta) for v in trip]
        for p1 in grid:
            for p2 in grid:
                p3 = 1.0 - p1 - p2
                if p3 < -1e-12:
                    continue
                p3 = max(p3, 0.0)
                ps = (p1, p2, p3)
                mu = sum(p * math.exp(-v) for p, v in zip(ps, trip))
                fail = 0.0
                for p, v, N in zip(ps, trip, Ns):
                    if p > 0 and abs(math.log(mu) + v) > eta:
                        fail += p ** N
                worst = max(worst, fail)
    print(f"   rho- = {rho_minus}, rho+ = {rho_plus}, eta = {eta}, delta = {delta}:  N(0) = {N0} evaluations without a hint  (hinted spot check with a half-and-half mixture: {hinted});  largest exact failure probability over three-level members = {worst:.4f}  (must be <= {delta})")
    assert worst <= delta * (1 + 1e-9)
print("ALL OK")
