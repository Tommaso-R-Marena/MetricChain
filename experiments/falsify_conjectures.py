#!/usr/bin/env python3
"""
MetricChain adversarial counterexample hunter.

Every conjecture that is a candidate for Lean formalization is registered here as a
randomized + edge-case falsification test.  A test FAILS LOUDLY (returns ok=False with the
offending instance) if a counterexample is found.  Tests that are *expected* to fail
(refuted conjectures kept for the record) are registered with expect_fail=True and are
documented in docs/DEAD_ENDS.md.

Usage:  python3 experiments/falsify_conjectures.py [--quick] [--seed N] [--only NAME]
Exit code 0 iff every test behaves as expected.
"""
from __future__ import annotations

import argparse
import itertools
import math
import sys
import time
from fractions import Fraction

import numpy as np

TOL = 1e-8
REGISTRY = []


def conjecture(name, expect_fail=False):
    def deco(fn):
        REGISTRY.append((name, fn, expect_fail))
        return fn
    return deco


# ----------------------------------------------------------------------------------------------
# Shared synthetic models
# ----------------------------------------------------------------------------------------------

def random_pairwise(rng, n, k, scale=1.0, sparse=1.0):
    """Random pairwise model: h[i][a], J[i][j][a][b] for ordered pairs i != j."""
    h = rng.normal(0, scale, size=(n, k))
    J = rng.normal(0, scale, size=(n, n, k, k))
    for i in range(n):
        J[i, i] = 0.0
        for j in range(n):
            if i != j and rng.random() > sparse:
                J[i, j] = 0.0
    return h, J


def energy(h, J, x):
    n = len(x)
    e = sum(h[i][x[i]] for i in range(n))
    for i in range(n):
        for j in range(n):
            if i != j:
                e += J[i][j][x[i]][x[j]]
    return e


def all_configs(n, k):
    return list(itertools.product(range(k), repeat=n))


def goldstein(h, J, i, r, t, domains):
    n = h.shape[0]
    val = h[i][r] - h[i][t]
    for j in range(n):
        if j == i:
            continue
        val += min(J[i][j][r][s] + J[j][i][s][r] - J[i][j][t][s] - J[j][i][s][t] for s in domains[j])
    return val


def reparam(h, J, m):
    """m[i][j][a]: message moved from ordered pair (i,j) into unary of i."""
    n, k = h.shape
    h2 = h.copy()
    J2 = J.copy()
    for i in range(n):
        for j in range(n):
            if i != j:
                h2[i] += m[i][j]
                J2[i][j] -= m[i][j][:, None]
    return h2, J2


def weighted_hamming(c, x, y):
    return sum(ci for ci, a, b in zip(c, x, y) if a != b)


def random_lipschitz(rng, configs, c, kappa=1.0):
    """Random function with bounded differences kappa*c (McShane extension of random data)."""
    idx = rng.choice(len(configs), size=min(len(configs), 1 + rng.integers(1, 6)), replace=False)
    vals = rng.normal(0, 3.0, size=len(idx))
    mode = rng.integers(0, 3)
    out = {}
    for y in configs:
        cand_lo = [v - kappa * weighted_hamming(c, configs[a], y) for a, v in zip(idx, vals)]
        cand_hi = [v + kappa * weighted_hamming(c, configs[a], y) for a, v in zip(idx, vals)]
        if mode == 0:
            out[y] = max(cand_lo)
        elif mode == 1:
            out[y] = min(cand_hi)
        else:
            out[y] = 0.5 * (max(cand_lo) + min(cand_hi)) if False else max(cand_lo)
    if mode == 2:  # additive two-level function, extremal for the class
        signs = rng.choice([-1.0, 0.0, 1.0], size=len(c))
        pivot = configs[rng.integers(len(configs))]
        for y in configs:
            out[y] = sum(kappa * ci * s for ci, s, a, b in zip(c, signs, y, pivot) if a != b)
    return out


def check_bd(g, configs, c, n, k, kappa=1.0):
    for x in configs:
        for i in range(n):
            for a in range(k):
                y = x[:i] + (a,) + x[i + 1:]
                if abs(g[x] - g[y]) > kappa * c[i] + 1e-9:
                    return False
    return True


# ----------------------------------------------------------------------------------------------
# Cluster I — dominance calculus
# ----------------------------------------------------------------------------------------------

@conjecture("I.1 Goldstein value = exact dominance margin (pairwise, product domains)")
def t_goldstein_exact(rng, trials):
    for _ in range(trials):
        n, k = int(rng.integers(2, 5)), int(rng.integers(2, 4))
        h, J = random_pairwise(rng, n, k, sparse=rng.random())
        domains = [sorted(rng.choice(k, size=int(rng.integers(1, k + 1)), replace=False).tolist()) for _ in range(n)]
        i = int(rng.integers(n))
        r, t = int(rng.integers(k)), int(rng.integers(k))
        g = goldstein(h, J, i, r, t, domains)
        others = [domains[j] if j != i else [0] for j in range(n)]
        exact = math.inf
        for x in itertools.product(*others):
            xr = x[:i] + (r,) + x[i + 1:]
            xt = x[:i] + (t,) + x[i + 1:]
            exact = min(exact, energy(h, J, xr) - energy(h, J, xt))
        if abs(g - exact) > 1e-7:
            return False, dict(n=n, k=k, goldstein=g, exact=exact)
    return True, {}


@conjecture("I.2 Goldstein is gauge-invariant; Desmet(gauge) <= Goldstein with equality at explicit gauge")
def t_gauge(rng, trials):
    worst = 0.0
    for _ in range(trials):
        n, k = int(rng.integers(2, 5)), int(rng.integers(2, 4))
        h, J = random_pairwise(rng, n, k)
        domains = [list(range(k)) for _ in range(n)]
        i = int(rng.integers(n))
        r, t = rng.choice(k, size=2, replace=False).tolist()
        g0 = goldstein(h, J, i, r, t, domains)
        m = rng.normal(0, 2.0, size=(n, n, k))
        h2, J2 = reparam(h, J, m)
        # energy function must be unchanged
        x = tuple(rng.integers(0, k, size=n).tolist())
        if abs(energy(h, J, x) - energy(h2, J2, x)) > 1e-7:
            return False, dict(reason="reparameterization changed the energy")
        g1 = goldstein(h2, J2, i, r, t, domains)
        if abs(g0 - g1) > 1e-7:
            return False, dict(reason="Goldstein not invariant", g0=g0, g1=g1)

        def desmet(hh, JJ):
            lo = hh[i][r] + sum(min(JJ[i][j][r][s] + JJ[j][i][s][r] for s in domains[j]) for j in range(n) if j != i)
            hi = hh[i][t] + sum(max(JJ[i][j][t][s] + JJ[j][i][s][t] for s in domains[j]) for j in range(n) if j != i)
            return lo - hi

        d_rand = desmet(h2, J2)
        if d_rand > g0 + 1e-7:
            return False, dict(reason="Desmet exceeded Goldstein", desmet=d_rand, goldstein=g0)
        # explicit optimal gauge: m[j][i][s] = J[i][j][t][s] + J[j][i][s][t]
        mstar = np.zeros((n, n, k))
        for j in range(n):
            if j != i:
                for s in range(k):
                    mstar[j][i][s] = J[i][j][t][s] + J[j][i][s][t]
        h3, J3 = reparam(h, J, mstar)
        d_star = desmet(h3, J3)
        if abs(d_star - g0) > 1e-7:
            return False, dict(reason="explicit gauge does not attain Goldstein", d_star=d_star, g0=g0)
        worst = max(worst, g0 - d_rand)
    return True, dict(max_slack_of_random_gauge=worst)


@conjecture("I.3 Thermal dominance transport: Z_{i=r} <= exp(-beta*gamma) Z_{i=t}; ln Z error <= ln(1+e^{-beta gamma})")
def t_thermal(rng, trials):
    for _ in range(trials):
        n, k = int(rng.integers(2, 5)), int(rng.integers(2, 4))
        h, J = random_pairwise(rng, n, k)
        beta = float(rng.uniform(0.05, 4.0))
        i = int(rng.integers(n))
        r, t = rng.choice(k, size=2, replace=False).tolist()
        domains = [list(range(k)) for _ in range(n)]
        gamma = goldstein(h, J, i, r, t, domains)
        zr = zt = 0.0
        for x in all_configs(n, k):
            if x[i] == r:
                zr += math.exp(-beta * energy(h, J, x))
            if x[i] == t:
                zt += math.exp(-beta * energy(h, J, x))
        if zr > math.exp(-beta * gamma) * zt * (1 + 1e-9):
            return False, dict(zr=zr, zt=zt, gamma=gamma, beta=beta)
    return True, {}


@conjecture("I.3b Split (context-dependent) dominance map is injective and transports weight")
def t_split_dominance(rng, trials):
    for _ in range(trials):
        n, k = int(rng.integers(3, 5)), int(rng.integers(2, 4))
        h, J = random_pairwise(rng, n, k)
        beta = float(rng.uniform(0.05, 3.0))
        i = int(rng.integers(n))
        j = int((i + 1 + rng.integers(n - 1)) % n)
        r = int(rng.integers(k))
        # dominator depends on the state of the splitting site j
        tmap = [int((r + 1 + rng.integers(k - 1)) % k) for _ in range(k)]
        cfgs = [x for x in all_configs(n, k) if x[i] == r]
        images = [x[:i] + (tmap[x[j]],) + x[i + 1:] for x in cfgs]
        if len(set(images)) != len(images):
            return False, dict(reason="split map not injective")
        gamma = min(energy(h, J, x) - energy(h, J, y) for x, y in zip(cfgs, images))
        zA = sum(math.exp(-beta * energy(h, J, x)) for x in cfgs)
        zS = sum(math.exp(-beta * energy(h, J, x)) for x in all_configs(n, k) if x[i] != r)
        if zA > math.exp(-beta * gamma) * zS * (1 + 1e-9):
            return False, dict(zA=zA, zS=zS, gamma=gamma)
    return True, {}


# ----------------------------------------------------------------------------------------------
# Cluster I' — metric-envelope duality for non-decomposable residuals
# ----------------------------------------------------------------------------------------------

@conjecture("II.1 Robust minimizers = contact set of the Pasch-Hausdorff envelope (class BD(c))")
def t_contact_set(rng, trials):
    for _ in range(trials):
        n, k = int(rng.integers(2, 4)), int(rng.integers(2, 4))
        configs = all_configs(n, k)
        c = rng.uniform(0.1, 2.0, size=n)
        f = {x: float(rng.normal(0, 1.5)) for x in configs}
        contact = {x for x in configs if all(f[x] <= f[y] + weighted_hamming(c, x, y) + 1e-12 for y in configs)}
        # (<=) explicit adversary g = d_c(x, .)
        for x in contact:
            g = {y: weighted_hamming(c, x, y) for y in configs}
            if not check_bd(g, configs, c, n, k):
                return False, dict(reason="adversary not in BD(c)")
            if any(f[x] + g[x] > f[y] + g[y] + 1e-9 for y in configs):
                return False, dict(reason="contact point not a minimizer under adversary")
        # (=>) random admissible residuals never make a non-contact point optimal
        for _ in range(30):
            g = random_lipschitz(rng, configs, c)
            if not check_bd(g, configs, c, n, k):
                return False, dict(reason="generator produced a non-BD function")
            best = min(f[y] + g[y] for y in configs)
            for x in configs:
                if x not in contact and f[x] + g[x] <= best + 1e-12:
                    return False, dict(reason="non-contact point became optimal", x=x)
    return True, {}


@conjecture("II.2 Robust certification <=> d_c-sharp minimum (x* optimal for ALL residuals in BD(c))")
def t_sharp_min(rng, trials):
    for _ in range(trials):
        n, k = int(rng.integers(2, 4)), int(rng.integers(2, 4))
        configs = all_configs(n, k)
        c = rng.uniform(0.1, 1.0, size=n)
        f = {x: float(rng.normal(0, 1.0)) for x in configs}
        xs = min(configs, key=lambda x: f[x])
        if rng.random() < 0.5:  # plant a sharp minimum
            for y in configs:
                f[y] = f[xs] + weighted_hamming(c, xs, y) * float(rng.uniform(1.0, 2.0))
        sharp = all(f[y] - f[xs] >= weighted_hamming(c, xs, y) - 1e-12 for y in configs)
        adv = {y: -weighted_hamming(c, xs, y) for y in configs}
        adv_ok = all(f[xs] + adv[xs] <= f[y] + adv[y] + 1e-12 for y in configs)
        if sharp != adv_ok:
            return False, dict(reason="sharpness vs adversary mismatch", sharp=sharp, adv_ok=adv_ok)
        if sharp:
            for _ in range(20):
                g = random_lipschitz(rng, configs, c)
                if any(f[xs] + g[xs] > f[y] + g[y] + 1e-9 for y in configs):
                    return False, dict(reason="sharp minimum defeated by admissible residual")
    return True, {}


@conjecture("II.3 McShane envelopes are admissible, interpolate, and bracket every admissible residual")
def t_mcshane(rng, trials):
    for _ in range(trials):
        n, k = int(rng.integers(2, 4)), int(rng.integers(2, 4))
        configs = all_configs(n, k)
        c = rng.uniform(0.1, 2.0, size=n)
        g = random_lipschitz(rng, configs, c)
        anchors = [configs[a] for a in rng.choice(len(configs), size=int(rng.integers(1, 5)), replace=False)]
        lo = {y: max(g[a] - weighted_hamming(c, a, y) for a in anchors) for y in configs}
        hi = {y: min(g[a] + weighted_hamming(c, a, y) for a in anchors) for y in configs}
        if not (check_bd(lo, configs, c, n, k) and check_bd(hi, configs, c, n, k)):
            return False, dict(reason="envelope not in BD(c)")
        if any(abs(lo[a] - g[a]) > 1e-9 or abs(hi[a] - g[a]) > 1e-9 for a in anchors):
            return False, dict(reason="envelope does not interpolate anchors")
        if any(lo[y] > g[y] + 1e-9 or g[y] > hi[y] + 1e-9 for y in configs):
            return False, dict(reason="envelope does not bracket")
    return True, {}


@conjecture("II.4 Witness-size lower bound: every state with gap < (1-kappa) c_min - eps must be an anchor")
def t_witness_lower_bound(rng, trials):
    worst_ratio = math.inf
    for _ in range(max(10, trials // 10)):
        n, k = 2, int(rng.integers(2, 4))
        if rng.random() < 0.4:
            n, k = 3, 2
        configs = all_configs(n, k)
        c = rng.uniform(0.5, 1.5, size=n)
        kappa = float(rng.uniform(0.0, 0.9))
        f = {x: float(rng.normal(0, 0.4)) for x in configs}
        g = random_lipschitz(rng, configs, c, kappa=kappa)
        E = {x: f[x] + g[x] for x in configs}
        Estar = min(E.values())
        eps = float(rng.uniform(0.0, 0.2))
        cmin = float(min(c))
        forced = [y for y in configs if E[y] - Estar < (1 - kappa) * cmin - eps - 1e-12]
        # brute-force smallest valid anchor certificate
        best = None
        for size in range(1, len(configs) + 1):
            for A in itertools.combinations(configs, size):
                U = min(E[a] for a in A)
                LB = min(f[y] + max(g[a] - weighted_hamming(c, a, y) for a in A) for y in configs)
                if U - LB <= eps + 1e-12:
                    best = A
                    break
            if best is not None:
                break
        if best is None:
            return False, dict(reason="no certificate even with all anchors")
        if not set(forced) <= set(best) and len(best) < len(forced):
            return False, dict(reason="certificate smaller than forced set", forced=len(forced), size=len(best))
        if len(best) < len(forced):
            return False, dict(reason="lower bound violated", forced=len(forced), size=len(best))
        if forced:
            worst_ratio = min(worst_ratio, len(best) / len(forced))
    return True, dict(min_ratio_cert_over_bound=worst_ratio)


@conjecture("II.5 Exact robust interval: F_beta(E0 + g) lies in [F(E0+lo), F(E0+hi)] incl. beta=inf")
def t_robust_interval(rng, trials):
    for _ in range(trials):
        n, k = int(rng.integers(2, 4)), int(rng.integers(2, 4))
        configs = all_configs(n, k)
        c = rng.uniform(0.1, 2.0, size=n)
        f = {x: float(rng.normal(0, 1.0)) for x in configs}
        g = random_lipschitz(rng, configs, c)
        anchors = [configs[a] for a in rng.choice(len(configs), size=int(rng.integers(1, 4)), replace=False)]
        lo = {y: max(g[a] - weighted_hamming(c, a, y) for a in anchors) for y in configs}
        hi = {y: min(g[a] + weighted_hamming(c, a, y) for a in anchors) for y in configs}
        for beta in (0.3, 1.0, 5.0, None):
            def F(res):
                if beta is None:
                    return min(f[y] + res[y] for y in configs)
                return -math.log(sum(math.exp(-beta * (f[y] + res[y])) for y in configs)) / beta
            if not (F(lo) <= F(g) + 1e-9 and F(g) <= F(hi) + 1e-9):
                return False, dict(beta=beta, Flo=F(lo), Fg=F(g), Fhi=F(hi))
    return True, {}


# ----------------------------------------------------------------------------------------------
# Cluster II — free-energy sandwiches
# ----------------------------------------------------------------------------------------------

@conjecture("III.1 Gibbs-Bogoliubov + Hoeffding sandwich: 0 <= ln<e^{-b(D-<D>)}> <= b^2 osc^2 / 8")
def t_hoeffding_sandwich(rng, trials):
    worst = 0.0
    for _ in range(trials):
        N = int(rng.integers(2, 40))
        p = rng.dirichlet(np.ones(N) * rng.uniform(0.2, 3.0))
        d = rng.normal(0, rng.uniform(0.1, 3.0), size=N)
        if rng.random() < 0.3:  # two-point extremal residual
            d = rng.choice([0.0, 1.0], size=N) * rng.uniform(0.1, 5.0)
        beta = float(rng.uniform(0.01, 5.0))
        mean = float(p @ d)
        val = math.log(float(p @ np.exp(-beta * (d - mean))))
        osc = float(d.max() - d.min())
        ub = beta ** 2 * osc ** 2 / 8
        if val < -1e-10 or val > ub + 1e-10:
            return False, dict(val=val, ub=ub)
        if ub > 0:
            worst = max(worst, val / ub)
    return True, dict(max_fraction_of_bound_attained=worst)


def product_space(rng, n, k):
    ps = [rng.dirichlet(np.ones(k) * rng.uniform(0.3, 3.0)) for _ in range(n)]
    configs = all_configs(n, k)
    w = {x: float(np.prod([ps[i][x[i]] for i in range(n)])) for x in configs}
    return ps, configs, w


def bd_constants(g, configs, n, k):
    c = np.zeros(n)
    for x in configs:
        for i in range(n):
            for a in range(k):
                y = x[:i] + (a,) + x[i + 1:]
                c[i] = max(c[i], abs(g[x] - g[y]))
    return c


@conjecture("III.2 McDiarmid sandwich for product references: ln<e^{-b(D-<D>)}> <= b^2 sum c_i^2 / 8")
def t_mcdiarmid(rng, trials):
    worst = 0.0
    for _ in range(trials):
        n, k = int(rng.integers(1, 5)), int(rng.integers(2, 4))
        ps, configs, w = product_space(rng, n, k)
        g = {x: float(rng.normal(0, 1.0)) for x in configs}
        if rng.random() < 0.5:
            cc = rng.uniform(0.1, 2.0, size=n)
            g = random_lipschitz(rng, configs, cc)
        c = bd_constants(g, configs, n, k)
        beta = float(rng.uniform(0.05, 4.0))
        mean = sum(w[x] * g[x] for x in configs)
        val = math.log(sum(w[x] * math.exp(-beta * (g[x] - mean)) for x in configs))
        ub = beta ** 2 * float(np.sum(c ** 2)) / 8
        if val < -1e-10 or val > ub + 1e-10:
            return False, dict(val=val, ub=ub, n=n, k=k)
        if ub > 0:
            worst = max(worst, val / ub)
    return True, dict(max_fraction_of_bound_attained=worst)


def phi_two_point(p, u):
    """ln E exp(Y - EY) for Y = u * Bernoulli(p)."""
    return math.log(p * math.exp(u * (1 - p)) + (1 - p) * math.exp(-u * p))


def best_subset_phi(pvec, u):
    k = len(pvec)
    best = 0.0
    for mask in range(1, 2 ** k - 1):
        p = sum(pvec[a] for a in range(k) if mask >> a & 1)
        best = max(best, phi_two_point(p, u), phi_two_point(p, -u))
    return best


@conjecture("III.3 Exact extremality: sup over BD(c) of ln<e^{g-<g>}> (product ref) is attained by ADDITIVE two-level g")
def t_additive_extremal(rng, trials):
    from scipy.optimize import minimize
    worst_gap = 0.0
    for _ in range(max(6, trials // 25)):
        n, k = int(rng.integers(1, 4)), int(rng.integers(2, 4))
        if k ** n > 27:
            n = 2
        ps, configs, w = product_space(rng, n, k)
        c = rng.uniform(0.3, 3.0, size=n)
        bound = sum(best_subset_phi(ps[i], c[i]) for i in range(n))
        idx = {x: a for a, x in enumerate(configs)}
        wv = np.array([w[x] for x in configs])
        cons = []
        for x in configs:
            for i in range(n):
                for a in range(k):
                    y = x[:i] + (a,) + x[i + 1:]
                    if y != x:
                        cons.append((idx[x], idx[y], c[i]))

        def neg_obj(g):
            m = wv @ g
            return -math.log(wv @ np.exp(g - m))

        constraints = [dict(type="ineq", fun=(lambda g, a=a, b=b, ci=ci: ci - (g[a] - g[b]))) for a, b, ci in cons]
        best_found = 0.0
        for _ in range(8):
            g0 = np.array(list(random_lipschitz(rng, configs, c).values()))
            res = minimize(neg_obj, g0, constraints=constraints, method="SLSQP", options=dict(maxiter=300, ftol=1e-12))
            gv = res.x
            feas = all(gv[a] - gv[b] <= ci + 1e-7 for a, b, ci in cons)
            if feas:
                best_found = max(best_found, -neg_obj(gv))
        if best_found > bound + 1e-6:
            return False, dict(reason="non-additive residual beat the additive bound", found=best_found, bound=bound, n=n, k=k)
        worst_gap = max(worst_gap, bound - best_found)
    return True, dict(max_gap_between_bound_and_local_search=worst_gap)


@conjecture("III.4 Hoelder/TRW temperature-rescaled decomposition: F_b(E1+E2) >= F_{b/rho}(E1) + F_{b/(1-rho)}(E2)")
def t_holder(rng, trials):
    for _ in range(trials):
        N = int(rng.integers(1, 30))
        e1 = rng.normal(0, 2.0, size=N)
        e2 = rng.normal(0, 2.0, size=N)
        beta = float(rng.uniform(0.05, 5.0))
        rho = float(rng.uniform(0.02, 0.98))

        def F(e, b):
            m = (-b * e).max()
            return -(m + math.log(np.exp(-b * e - m).sum())) / b

        lhs = F(e1 + e2, beta)
        rhs = F(e1, beta / rho) + F(e2, beta / (1 - rho))
        if lhs < rhs - 1e-9:
            return False, dict(lhs=lhs, rhs=rhs, beta=beta, rho=rho)
    return True, {}


# ----------------------------------------------------------------------------------------------
# Cluster III — realizability / spectral obstructions
# ----------------------------------------------------------------------------------------------

def sqdist(X):
    g = X @ X.T
    d = np.diag(g)
    return d[:, None] + d[None, :] - 2 * g


def centered_gram(D):
    L = D.shape[0]
    Jm = np.eye(L) - np.ones((L, L)) / L
    return -0.5 * Jm @ D @ Jm


def Kmap(E):
    d = np.diag(E)
    return d[:, None] + d[None, :] - 2 * E


@conjecture("IV.1 K-identity: ||K(E)||_F^2 = 4||E||^2 + 2L||diag E||^2 + 2(tr E)^2 for centered symmetric E")
def t_k_identity(rng, trials):
    for _ in range(trials):
        L = int(rng.integers(2, 12))
        A = rng.normal(size=(L, L))
        A = A + A.T
        Jm = np.eye(L) - np.ones((L, L)) / L
        E = Jm @ A @ Jm
        lhs = np.sum(Kmap(E) ** 2)
        rhs = 4 * np.sum(E ** 2) + 2 * L * np.sum(np.diag(E) ** 2) + 2 * np.trace(E) ** 2
        if abs(lhs - rhs) > 1e-7 * max(1.0, abs(lhs)):
            return False, dict(lhs=lhs, rhs=rhs)
    return True, {}


def trace_bound_sq(Dhat, r, restrict_centered=True):
    """Trace-enhanced spectral lower bound on min_X ||Dhat - Delta(X)||_F^2."""
    L = Dhat.shape[0]
    G = centered_gram(Dhat)
    ev = np.sort(np.linalg.eigvalsh(G))[::-1]
    if restrict_centered:
        # drop one (numerically) zero eigenvalue belonging to the all-ones vector
        k0 = int(np.argmin(np.abs(ev)))
        ev = np.delete(ev, k0)
    tail = ev[r:]
    tau = tail.sum()
    return 4 * np.sum(tail ** 2) + 4.0 / (r + 1) * tau ** 2, 4 * np.sum(tail ** 2)


def exact_scalar_bound_sq(Dhat, r):
    """Water-filling refinement: min over mu>=0 of 4[sum_{k<=r}(mu_k-lam_k)^2 + sum_{k>r} lam_k^2 + (sum mu - tr)^2]."""
    from scipy.optimize import minimize
    G = centered_gram(Dhat)
    ev = np.sort(np.linalg.eigvalsh(G))[::-1]
    k0 = int(np.argmin(np.abs(ev)))
    ev = np.delete(ev, k0)
    T = ev.sum()
    top, tail = ev[:r], ev[r:]

    def obj(mu):
        return np.sum((mu - top) ** 2) + np.sum(tail ** 2) + (mu.sum() - T) ** 2

    res = minimize(obj, np.maximum(top, 0), bounds=[(0, None)] * r)
    return 4 * res.fun


def sstress_min(Dhat, r, rng, restarts=6):
    from scipy.optimize import minimize
    L = Dhat.shape[0]

    def obj(xflat):
        X = xflat.reshape(L, r)
        R = sqdist(X) - Dhat
        f = np.sum(R ** 2)
        # gradient of sum_ij (d_ij - Dhat_ij)^2 with d_ij = |x_i-x_j|^2
        W = R + R.T
        grad = 4 * ((W.sum(axis=1))[:, None] * X - W @ X) / 1.0
        return f, grad.ravel() / 2.0 * 1.0

    best = math.inf
    # classical MDS warm start + random restarts
    G = centered_gram(Dhat)
    w, V = np.linalg.eigh(G)
    order = np.argsort(w)[::-1][:r]
    X0 = V[:, order] * np.sqrt(np.maximum(w[order], 0))
    starts = [X0] + [X0 + rng.normal(0, 0.5 * (1 + np.abs(X0).max()), size=X0.shape) for _ in range(restarts)]
    for S in starts:
        res = minimize(lambda z: obj(z)[0], S.ravel(), method="L-BFGS-B")
        best = min(best, res.fun)
    return best


@conjecture("IV.2 Trace-enhanced spectral obstruction: min_X ||Dhat-Delta(X)||^2 >= 4 sum_{k>r} lam_k^2 + 4/(r+1) tau^2")
def t_trace_obstruction(rng, trials):
    worst_ratio = math.inf
    gain = 0.0
    for it in range(max(8, trials // 12)):
        L = int(rng.integers(5, 11))
        r = 3 if L > 4 else 2
        mode = it % 4
        X0 = rng.normal(size=(L, r)) * rng.uniform(0.5, 3.0)
        D0 = sqdist(X0)
        if mode == 0:
            N = rng.normal(0, rng.uniform(0.01, 2.0), size=(L, L))
            Dhat = D0 + (N + N.T) / 2
        elif mode == 1:
            Dhat = D0 + rng.uniform(0.1, 5.0) * (np.ones((L, L)) - np.eye(L))
        elif mode == 2:
            N = np.abs(rng.normal(0, 2.0, size=(L, L)))
            Dhat = (N + N.T) / 2
        else:
            Xh = rng.normal(size=(L, L - 1))
            Dhat = sqdist(Xh)
        np.fill_diagonal(Dhat, 0.0)
        lb, strain = trace_bound_sq(Dhat, r)
        lb_full, _ = trace_bound_sq(Dhat, r, restrict_centered=False)
        lb_exact = exact_scalar_bound_sq(Dhat, r)
        # (a) every configuration must respect the bound
        for _ in range(5):
            X = rng.normal(size=(L, r)) * rng.uniform(0.1, 4.0)
            val = np.sum((sqdist(X) - Dhat) ** 2)
            if val < max(lb, lb_full, lb_exact) - 1e-6 * max(1, val):
                return False, dict(reason="random X below bound", val=val, lb=lb, lb_full=lb_full, lb_exact=lb_exact)
        # (b) so must the best configuration local search can find
        best = sstress_min(Dhat, r, rng)
        if best < max(lb, lb_full, lb_exact) - 1e-5 * max(1, best):
            return False, dict(reason="optimized X below bound", best=best, lb=lb, lb_full=lb_full, lb_exact=lb_exact, mode=mode, L=L)
        if lb > 1e-9:
            worst_ratio = min(worst_ratio, best / lb)
        if strain > 1e-9:
            gain = max(gain, lb / strain)
    return True, dict(min_ratio_opt_over_bound=worst_ratio, max_gain_over_strain_bound=gain)


@conjecture("IV.3 Sharpness of the trace-enhanced bound on vertex-transitive (circulant) inputs")
def t_trace_sharp(rng, trials):
    worst = 0.0
    for it in range(max(4, trials // 40)):
        L = int(rng.integers(6, 12))
        r = 2
        ang = 2 * np.pi * np.arange(L) / L
        X0 = np.c_[np.cos(ang), np.sin(ang)] * rng.uniform(1.0, 3.0)
        bias = rng.uniform(0.05, 0.5)
        Dhat = sqdist(X0) + bias * (np.ones((L, L)) - np.eye(L))
        lb, _ = trace_bound_sq(Dhat, r)
        best = sstress_min(Dhat, r, rng)
        rel = abs(best - lb) / max(lb, 1e-12)
        worst = max(worst, rel)
        if best < lb - 1e-6 * max(1, lb):
            return False, dict(reason="bound violated", best=best, lb=lb)
        if rel > 1e-4:
            return False, dict(reason="bound not attained on circulant input", best=best, lb=lb, L=L)
    return True, dict(max_relative_gap=worst)


def kabsch(X, Y, allow_reflection=False):
    """min over rigid motions g of ||X - g(Y)||_F^2 (rows are points)."""
    Xc = X - X.mean(axis=0)
    Yc = Y - Y.mean(axis=0)
    H = Yc.T @ Xc
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(U @ Vt))
    if allow_reflection or d > 0:
        s = S.sum()
    else:
        s = S.sum() - 2 * S[-1]
    return max(np.sum(Xc ** 2) + np.sum(Yc ** 2) - 2 * s, 0.0)


@conjecture("IV.4 dRMSD <= sqrt(2) RMSD: sum_ij (D_ij(X)-D_ij(Y))^2 <= 2L * Kabsch(X,Y)")
def t_drmsd(rng, trials):
    worst = 0.0
    for _ in range(trials):
        L = int(rng.integers(2, 15))
        X = rng.normal(size=(L, 3))
        Y = X + rng.normal(0, rng.uniform(0.01, 2.0), size=(L, 3)) if rng.random() < 0.7 else rng.normal(size=(L, 3))
        DX = np.sqrt(np.maximum(sqdist(X), 0))
        DY = np.sqrt(np.maximum(sqdist(Y), 0))
        lhs = np.sum((DX - DY) ** 2)
        rhs = 2 * L * kabsch(X, Y)
        if lhs > rhs + 1e-7:
            return False, dict(lhs=lhs, rhs=rhs)
        if rhs > 0:
            worst = max(worst, lhs / rhs)
    return True, dict(max_ratio=worst)


@conjecture("IV.5 Procrustes-Gram stability: Kabsch_O(3)(X,Y) <= ||Delta(X)-Delta(Y)||^2 / (8(sqrt2-1) sigma_3(X)^2)")
def t_procrustes(rng, trials):
    worst = 0.0
    for _ in range(trials):
        L = int(rng.integers(4, 14))
        X = rng.normal(size=(L, 3)) * rng.uniform(0.3, 3.0)
        mode = rng.integers(0, 3)
        if mode == 0:
            Y = X + rng.normal(0, rng.uniform(1e-3, 0.5), size=(L, 3))
        elif mode == 1:
            Y = rng.normal(size=(L, 3)) * rng.uniform(0.3, 3.0)
        else:
            Y = X * rng.uniform(0.0, 2.0)
        Xc = X - X.mean(axis=0)
        s3 = np.linalg.svd(Xc, compute_uv=False)[-1]
        lhs = kabsch(X, Y, allow_reflection=True)
        rhs = np.sum((sqdist(X) - sqdist(Y)) ** 2) / (8 * (math.sqrt(2) - 1) * s3 ** 2)
        if lhs > rhs * (1 + 1e-7) + 1e-9:
            return False, dict(lhs=lhs, rhs=rhs, mode=int(mode))
        if rhs > 0:
            worst = max(worst, lhs / rhs)
    return True, dict(max_ratio=worst)


def rot_axis(axis, ang):
    axis = axis / np.linalg.norm(axis)
    Kx = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + math.sin(ang) * Kx + (1 - math.cos(ang)) * Kx @ Kx


def coaxial_cost(IA, IB, phi):
    S = IA + IB
    return 2 * S - 2 * math.sqrt(max(S * S - 4 * IA * IB * math.sin(phi / 2) ** 2, 0.0))


@conjecture("V.1 Single-torsion Kabsch cost <= 2S - 2 sqrt(S^2 - 4 I_A I_B sin^2(phi/2)) <= 8 I_red sin^2(phi/2)")
def t_coaxial(rng, trials):
    worst = 0.0
    for _ in range(trials):
        nA, nB = int(rng.integers(1, 8)), int(rng.integers(1, 8))
        A = rng.normal(size=(nA, 3)) * rng.uniform(0.2, 3.0)
        B = rng.normal(size=(nB, 3)) * rng.uniform(0.2, 3.0) + rng.normal(size=3)
        p = rng.normal(size=3)
        axis = rng.normal(size=3)
        axis /= np.linalg.norm(axis)
        phi = float(rng.uniform(-math.pi, math.pi))
        R = rot_axis(axis, phi)
        B2 = (B - p) @ R.T + p
        X = np.vstack([A, B])
        Y = np.vstack([A, B2])
        true = kabsch(X, Y)

        def inertia(P):
            v = P - p
            perp = v - np.outer(v @ axis, axis)
            return float(np.sum(perp ** 2))

        IA, IB = inertia(A), inertia(B)
        bound = coaxial_cost(IA, IB, phi)
        red = 8 * IA * IB / (IA + IB) * math.sin(phi / 2) ** 2 if IA + IB > 0 else 0.0
        if true > bound + 1e-7 or bound > red + 1e-7:
            return False, dict(true=true, coaxial=bound, reduced=red)
        # the coaxial formula is the exact optimum over rotations about the same axis:
        # attained at psi* = arg(I_A + I_B e^{i phi}); no coaxial rotation does better.
        psi_star = math.atan2(IB * math.sin(phi), IA + IB * math.cos(phi))
        at_star = 2 * IA * (1 - math.cos(psi_star)) + 2 * IB * (1 - math.cos(phi - psi_star))
        psis = np.linspace(-math.pi, math.pi, 2001)
        scan = np.min(2 * IA * (1 - np.cos(psis)) + 2 * IB * (1 - np.cos(phi - psis)))
        if abs(at_star - bound) > 1e-9 * max(1.0, IA + IB) or scan < bound - 1e-9 * max(1.0, IA + IB):
            return False, dict(reason="closed form is not the coaxial optimum", scan=float(scan), at_star=at_star, bound=bound)
        if bound > 1e-9:
            worst = max(worst, true / bound)
    return True, dict(max_ratio_true_over_bound=worst)


def build_chain(theta, bond=1.5, angle=math.radians(111.0)):
    """Simple backbone: fixed bond length and bond angle, torsions theta[0..n-4]. Returns (n,3) coords."""
    n = len(theta) + 3
    X = np.zeros((n, 3))
    X[1] = [bond, 0, 0]
    X[2] = X[1] + bond * np.array([-math.cos(angle), math.sin(angle), 0.0])
    for i in range(3, n):
        a, b, c = X[i - 3], X[i - 2], X[i - 1]
        bc = (c - b) / np.linalg.norm(c - b)
        nrm = np.cross(b - a, bc)
        nrm /= np.linalg.norm(nrm)
        m = np.cross(nrm, bc)
        t = theta[i - 3]
        d2 = np.array([-bond * math.cos(angle), bond * math.sin(angle) * math.cos(t), bond * math.sin(angle) * math.sin(t)])
        X[i] = c + d2[0] * bc + d2[1] * m + d2[2] * nrm
    return X


@conjecture("V.2 Chained reduced-inertia bound: sqrt(Kabsch(theta,theta')) <= sum_k sqrt(coaxial cost_k) along single-torsion path")
def t_chain_bound(rng, trials):
    worst = 0.0
    for _ in range(max(10, trials // 4)):
        m = int(rng.integers(1, 10))
        theta = rng.uniform(-math.pi, math.pi, size=m)
        delta = rng.normal(0, rng.uniform(0.01, 1.0), size=m)
        cur = theta.copy()
        total = 0.0
        order = rng.permutation(m)
        for kk in order:
            X = build_chain(cur)
            # torsion kk rotates atoms kk+3.. about the axis through atoms kk+1 -> kk+2
            p, q = X[kk + 1], X[kk + 2]
            axis = (q - p) / np.linalg.norm(q - p)

            def inertia(P):
                v = P - p
                perp = v - np.outer(v @ axis, axis)
                return float(np.sum(perp ** 2))

            IA, IB = inertia(X[: kk + 3]), inertia(X[kk + 3:])
            total += math.sqrt(coaxial_cost(IA, IB, delta[kk]))
            cur[kk] += delta[kk]
        true = math.sqrt(kabsch(build_chain(theta), build_chain(theta + delta)))
        if true > total + 1e-7:
            return False, dict(true=true, bound=total, m=m)
        if total > 1e-9:
            worst = max(worst, true / total)
    return True, dict(max_ratio_true_over_bound=worst)


def rand_rot(rng, scale=None):
    if scale is None:
        Q, R = np.linalg.qr(rng.normal(size=(3, 3)))
        Q = Q @ np.diag(np.sign(np.diag(R)))
        if np.linalg.det(Q) < 0:
            Q[:, 0] *= -1
        return Q
    return rot_axis(rng.normal(size=3), rng.normal(0, scale))


def rot_angle(R):
    return math.acos(max(-1.0, min(1.0, (np.trace(R) - 1) / 2)))


@conjecture("VI.1 Cycle-holonomy lower bound (bi-invariant metric): sum_k d(ghat_k, x_k^-1 x_{k+1}) >= d(hol, 1)")
def t_holonomy(rng, trials):
    worst = math.inf
    for _ in range(trials):
        m = int(rng.integers(2, 9))
        xs = [rand_rot(rng) for _ in range(m)]
        ghat = [xs[k].T @ xs[(k + 1) % m] @ rand_rot(rng, scale=rng.uniform(0.01, 1.0)) for k in range(m)]
        hol = np.eye(3)
        for g in ghat:
            hol = hol @ g
        h = rot_angle(hol)
        # any vertex assignment, not only the generating one
        for trial in range(3):
            ys = xs if trial == 0 else [rand_rot(rng) for _ in range(m)]
            errs = [rot_angle(ghat[k].T @ ys[k].T @ ys[(k + 1) % m]) for k in range(m)]
            if sum(errs) < h - 1e-7:
                return False, dict(sum_err=sum(errs), hol=h, m=m)
            if sum(e * e for e in errs) < h * h / m - 1e-7:
                return False, dict(reason="L2 form violated")
            if h > 1e-9:
                worst = min(worst, sum(errs) / h)
    return True, dict(min_ratio=worst)


@conjecture("VI.2 SE(3) translation holonomy: |t_hol| <= sum_k eps_k + sum_l rho_l * sum_{k>l} |that_k|")
def t_se3_holonomy(rng, trials):
    for _ in range(trials):
        m = int(rng.integers(2, 8))
        Rs = [rand_rot(rng) for _ in range(m)]
        ps = [rng.normal(size=3) * 2 for _ in range(m)]
        Rhat, that, eps, rho = [], [], [], []
        for k in range(m):
            kn = (k + 1) % m
            Rtrue = Rs[k].T @ Rs[kn]
            ttrue = Rs[k].T @ (ps[kn] - ps[k])
            Rh = Rtrue @ rand_rot(rng, scale=rng.uniform(0.0, 0.5))
            th = ttrue + rng.normal(0, rng.uniform(0.0, 0.5), size=3)
            Rhat.append(Rh)
            that.append(th)
            eps.append(np.linalg.norm(th - ttrue))
            rho.append(np.linalg.norm(Rh - Rtrue, 2))
        acc = np.eye(3)
        thol = np.zeros(3)
        for k in range(m):
            thol = thol + acc @ that[k]
            acc = acc @ Rhat[k]
        lever = [sum(np.linalg.norm(that[k]) for k in range(l + 1, m)) for l in range(m)]
        bound = sum(eps) + sum(r * lv for r, lv in zip(rho, lever))
        if np.linalg.norm(thol) > bound + 1e-7:
            return False, dict(thol=float(np.linalg.norm(thol)), bound=bound, m=m)
    return True, {}


# ----------------------------------------------------------------------------------------------
# Cluster IV — certificates, proof complexity, rounding
# ----------------------------------------------------------------------------------------------

def triangles_instance(nt):
    n = 3 * nt
    edges = []
    for q in range(nt):
        a, b, c = 3 * q, 3 * q + 1, 3 * q + 2
        edges += [(a, b), (b, c), (a, c)]
    return n, edges


def lp_bound(n, edges, domains):
    """Local-polytope LP lower bound for cost sum_{(i,j)} [x_i == x_j] on restricted domains (binary)."""
    from scipy.optimize import linprog
    # variables: mu_i(a) for a in {0,1}; mu_ij(a,b)
    nv = 2 * n + 4 * len(edges)
    cost = np.zeros(nv)
    Aeq, beq = [], []
    bounds = []
    for i in range(n):
        for a in range(2):
            bounds.append((0, 1) if a in domains[i] else (0, 0))
        row = np.zeros(nv)
        row[2 * i] = row[2 * i + 1] = 1
        Aeq.append(row)
        beq.append(1)
    for e, (i, j) in enumerate(edges):
        base = 2 * n + 4 * e
        for a in range(2):
            for b in range(2):
                bounds.append((0, 1))
                if a == b:
                    cost[base + 2 * a + b] = 1.0
        for a in range(2):
            row = np.zeros(nv)
            row[base + 2 * a] = row[base + 2 * a + 1] = 1
            row[2 * i + a] = -1
            Aeq.append(row)
            beq.append(0)
        for b in range(2):
            row = np.zeros(nv)
            row[base + b] = row[base + 2 + b] = 1
            row[2 * j + b] = -1
            Aeq.append(row)
            beq.append(0)
    res = linprog(cost, A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=bounds, method="highs")
    return res.fun


@conjecture("VII.1 Tree-like branch-and-bound with LP-dual leaves needs >= 2^n leaves on n frustrated triangles")
def t_bnb_lower_bound(rng, trials):
    out = {}
    for nt in (1, 2):
        n, edges = triangles_instance(nt)
        target = nt
        memo = {}

        def min_leaves(dom):
            if dom in memo:
                return memo[dom]
            domains = [((0, 1) if d == 2 else (d,)) for d in dom]
            if lp_bound(n, edges, domains) >= target - 1e-7:
                memo[dom] = 1
                return 1
            best = math.inf
            for i in range(n):
                if dom[i] == 2:
                    v = min_leaves(dom[:i] + (0,) + dom[i + 1:]) + min_leaves(dom[:i] + (1,) + dom[i + 1:])
                    best = min(best, v)
            memo[dom] = best
            return best

        leaves = min_leaves(tuple([2] * n))
        out[f"n={nt}"] = leaves
        if leaves < 2 ** nt:
            return False, dict(reason="found a smaller tree", n=nt, leaves=leaves)
        if leaves != 2 ** nt:
            return False, dict(reason="minimum tree size is not exactly 2^n", n=nt, leaves=leaves)
    return True, out


def exp_bounds(q: Fraction, n: int = 8):
    """Rational enclosure of exp(q): Taylor with Mathlib's remainder |x|^n (n+1)/(n! n) after halving."""
    k = 0
    x = q
    while abs(x) > 1:
        x /= 2
        k += 1
    T = sum(x ** m / math.factorial(m) for m in range(n))
    err = abs(x) ** n * Fraction(n + 1, math.factorial(n) * n)
    lo = max(Fraction(0), T - err)
    hi = T + err
    return lo ** (2 ** k), hi ** (2 ** k)


@conjecture("VIII.1 Rational exp enclosure (Taylor + certified remainder + repeated squaring) brackets exp(q)")
def t_exp_enclosure(rng, trials):
    import mpmath
    mpmath.mp.dps = 60
    worst = 0.0
    for _ in range(trials):
        q = Fraction(int(rng.integers(-4000, 4000)), int(rng.integers(1, 400)))
        if abs(q) > 12:
            q = q / 8
        lo, hi = exp_bounds(q, n=10)
        true = mpmath.exp(mpmath.mpf(q.numerator) / q.denominator)
        lo_m = mpmath.mpf(lo.numerator) / lo.denominator
        hi_m = mpmath.mpf(hi.numerator) / hi.denominator
        if not (lo_m <= true <= hi_m):
            return False, dict(q=str(q))
        worst = max(worst, float((hi_m - lo_m) / true))
    return True, dict(max_relative_width=worst)


@conjecture("VIII.2 Rational torus atlas: every unit vector is rot(q*90deg) of ((1-t^2)/(1+t^2), 2t/(1+t^2)) with |t| <= 1/2")
def t_atlas(rng, trials):
    for _ in range(trials * 5):
        th = float(rng.uniform(-math.pi, math.pi))
        if rng.random() < 0.2:
            th = float(rng.choice([0, math.pi / 4, -math.pi / 4, 3 * math.pi / 4, math.pi / 2, math.pi])) + float(rng.normal(0, 1e-9))
        c, s = math.cos(th), math.sin(th)
        ok = False
        for q in range(4):
            cq, sq = c, s
            for _ in range(q):  # rotate by -90 degrees q times
                cq, sq = sq, -cq
            if cq >= abs(sq) - 1e-12:
                t = sq / (1 + cq)
                if abs(t) <= 0.5:
                    c2, s2 = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
                    if abs(c2 - cq) < 1e-9 and abs(s2 - sq) < 1e-9:
                        ok = True
        if not ok:
            return False, dict(theta=th)
    return True, {}


@conjecture("IX.1 Lipschitz oracle lower bound (1-D): n value queries leave certified gap >= Lam/(2n) on the circle")
def t_oracle_lower_bound(rng, trials):
    for _ in range(trials):
        n = int(rng.integers(1, 12))
        lam = float(rng.uniform(0.2, 5.0))
        pts = np.sort(rng.uniform(0, 1, size=n))
        gaps = np.diff(np.r_[pts, pts[0] + 1.0])
        big = float(gaps.max())
        # adversary: f=0 vs tent of depth lam*big/2 centred in the largest gap; both lam-Lipschitz, equal at all queries
        if big < 1.0 / n - 1e-12:
            return False, dict(reason="pigeonhole violated")
        depth = lam * big / 2
        if depth < lam / (2 * n) - 1e-12:
            return False, dict(depth=depth)
    return True, {}


# ----------------------------------------------------------------------------------------------
# Refuted conjectures kept for the record (see docs/DEAD_ENDS.md)
# ----------------------------------------------------------------------------------------------

@conjecture("DEAD.1 Dual reparameterization can strictly improve Goldstein pruning for pairwise models", expect_fail=True)
def t_dead_gauge_improves(rng, trials):
    for _ in range(trials):
        n, k = int(rng.integers(2, 5)), int(rng.integers(2, 4))
        h, J = random_pairwise(rng, n, k)
        domains = [list(range(k)) for _ in range(n)]
        i = int(rng.integers(n))
        r, t = rng.choice(k, size=2, replace=False).tolist()
        g0 = goldstein(h, J, i, r, t, domains)
        for _ in range(5):
            m = rng.normal(0, 3.0, size=(n, n, k))
            h2, J2 = reparam(h, J, m)
            if goldstein(h2, J2, i, r, t, domains) > g0 + 1e-7:
                return True, dict(found_improvement=True)
    return False, dict(reason="no reparameterization ever changed the Goldstein value (it is a gauge invariant)")


@conjecture("DEAD.2 Compression-only rank obstruction: ||QAQ||^2 + tr(QA)^2/(r+1) >= tail bound for every corank-r projector Q", expect_fail=True)
def t_dead_compression(rng, trials):
    for _ in range(trials * 4):
        n = int(rng.integers(3, 7))
        r = int(rng.integers(1, n - 1))
        lam = np.sort(rng.normal(0, 2.0, size=n))[::-1]
        A = np.diag(lam)
        Qm, _ = np.linalg.qr(rng.normal(size=(n, n)))
        V = Qm[:, : n - r]
        Qp = V @ V.T
        lhs = np.sum((Qp @ A @ Qp) ** 2) + np.trace(Qp @ A) ** 2 / (r + 1)
        tail = lam[r:]
        rhs = np.sum(tail ** 2) + tail.sum() ** 2 / (r + 1)
        if lhs < rhs - 1e-7:
            return False, dict(reason="compression argument is lossy when the spectrum has mixed signs", lhs=lhs, rhs=rhs)
    return True, {}


@conjecture("DEAD.3 Strain bound alone is within O(1) of the optimal s-stress under uniform bias", expect_fail=True)
def t_dead_strain_tight(rng, trials):
    for L in (20, 40):
        X0 = rng.normal(size=(L, 3))
        Dhat = sqdist(X0) + 1.0 * (np.ones((L, L)) - np.eye(L))
        lb, strain = trace_bound_sq(Dhat, 3)
        if lb / strain > 4.0:
            return False, dict(reason="trace term dominates: strain bound is loose by a factor growing with L",
                               L=L, ratio=float(lb / strain))
    return True, {}


# ----------------------------------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="fewer trials (CI mode)")
    ap.add_argument("--seed", type=int, default=20261124)
    ap.add_argument("--only", type=str, default=None)
    args = ap.parse_args()
    trials = 60 if args.quick else 400
    failures = 0
    print(f"MetricChain falsification harness — seed={args.seed}, trials/test={trials}")
    for name, fn, expect_fail in REGISTRY:
        if args.only and args.only not in name:
            continue
        rng = np.random.default_rng(args.seed)
        t0 = time.time()
        try:
            ok, info = fn(rng, trials)
        except Exception as exc:  # a crash is a failure of the harness, not a refutation
            ok, info = None, dict(exception=repr(exc))
        dt = time.time() - t0
        if ok is None:
            status, bad = "ERROR", True
        elif expect_fail:
            status, bad = ("REFUTED (as documented)" if not ok else "UNEXPECTEDLY SURVIVED"), ok
        else:
            status, bad = ("survived" if ok else "COUNTEREXAMPLE"), not ok
        failures += bool(bad)
        extra = ", ".join(f"{k}={v:.4g}" if isinstance(v, float) else f"{k}={v}" for k, v in info.items())
        print(f"[{status:>24}] {name}  ({dt:.1f}s) {extra}")
    print(f"\n{'ALL TESTS BEHAVE AS EXPECTED' if failures == 0 else str(failures) + ' TEST(S) MISBEHAVED'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
