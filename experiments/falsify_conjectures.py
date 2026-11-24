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
import warnings
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


@conjecture("I.5 Thermal pruning changes any Boltzmann average of |f| <= B by at most 2 B exp(-beta*gamma)")
def t_observable_error(rng, trials):
    worst = 0.0
    for _ in range(trials):
        n, k = int(rng.integers(2, 5)), int(rng.integers(2, 4))
        h, J = random_pairwise(rng, n, k)
        beta = float(rng.uniform(0.05, 4.0))
        i = int(rng.integers(n))
        r, t = rng.choice(k, size=2, replace=False).tolist()
        domains = [list(range(k)) for _ in range(n)]
        gamma = goldstein(h, J, i, r, t, domains)
        configs = all_configs(n, k)
        fvals = {x: float(rng.uniform(-1, 1)) for x in configs}
        B = max(abs(v) for v in fvals.values())
        wts = {x: math.exp(-beta * energy(h, J, x)) for x in configs}
        full = sum(wts[x] * fvals[x] for x in configs) / sum(wts.values())
        keep = [x for x in configs if x[i] != r]
        pruned = sum(wts[x] * fvals[x] for x in keep) / sum(wts[x] for x in keep)
        bound = 2 * B * math.exp(-beta * gamma)
        if abs(full - pruned) > bound * (1 + 1e-9) + 1e-12:
            return False, dict(diff=abs(full - pruned), bound=bound, gamma=gamma, beta=beta)
        if bound > 0:
            worst = max(worst, abs(full - pruned) / bound)
    return True, dict(max_fraction_of_bound=worst)


@conjecture("I.4 Exact dominance with chain-local 3-body terms factorises over the blocks of the link graph")
def t_block_separable(rng, trials):
    for _ in range(max(20, trials // 4)):
        n, k = 6, int(rng.integers(2, 4))
        h, J = random_pairwise(rng, n, k, sparse=0.6)
        T = rng.normal(0, 1.0, size=(n - 2, k, k, k))  # T[j] couples sites j, j+1, j+2

        def E(x):
            return energy(h, J, x) + sum(T[j][x[j]][x[j + 1]][x[j + 2]] for j in range(n - 2))

        i = int(rng.integers(n))
        r, t = rng.choice(k, size=2, replace=False).tolist()
        # exact margin by brute force over all contexts
        exact = math.inf
        for x in itertools.product(range(k), repeat=n):
            if x[i] != 0:
                continue  # the value at site i is irrelevant: enumerate contexts once
            xr = x[:i] + (r,) + x[i + 1:]
            xt = x[:i] + (t,) + x[i + 1:]
            exact = min(exact, E(xr) - E(xt))
        # block decomposition: one block for the chain neighbours within distance 2, singletons otherwise
        block = [j for j in (i - 2, i - 1, i + 1, i + 2) if 0 <= j < n]
        singles = [j for j in range(n) if j != i and j not in block]

        def pair_link(j, s):
            return J[i][j][r][s] + J[j][i][s][r] - J[i][j][t][s] - J[j][i][s][t]

        total = h[i][r] - h[i][t] + sum(min(pair_link(j, s) for s in range(k)) for j in singles)
        best_block = math.inf
        for vals in itertools.product(range(k), repeat=len(block)):
            ctx = dict(zip(block, vals))
            v = sum(pair_link(j, ctx[j]) for j in block)
            for j in range(n - 2):
                if j <= i <= j + 2:
                    trip_r = [r if q == i else ctx[q] for q in (j, j + 1, j + 2)]
                    trip_t = [t if q == i else ctx[q] for q in (j, j + 1, j + 2)]
                    v += T[j][trip_r[0]][trip_r[1]][trip_r[2]] - T[j][trip_t[0]][trip_t[1]][trip_t[2]]
            best_block = min(best_block, v)
        total += best_block
        if abs(total - exact) > 1e-7:
            return False, dict(block_formula=total, brute_force=exact, i=i, k=k)
    return True, {}


# ----------------------------------------------------------------------------------------------
# Cluster I' — metric-envelope duality for non-decomposable residuals
# ----------------------------------------------------------------------------------------------

@conjecture("I.6 Many-to-one thermal transport: Z(A) <= m e^{-beta*gamma} Z(S) for an m-to-one energy-lowering map; Z(A u S) <= (1 + m e^{-beta*gamma}) Z(S)")
def t_transport_fibers(rng, trials):
    """Lean: partition_transport_fibers, partition_prune_bracket_fibers.  Power check: the injective
    formula (m replaced by 1) must be violated on instances with a non-injective map."""
    worst = 0.0
    injective_formula_violations = 0
    multi_fibre_instances = 0
    for trial in range(trials):
        N = int(rng.integers(3, 12))
        E = rng.normal(0.0, 1.5, size=N)
        beta = float(rng.uniform(0.0, 3.0))
        nS = int(rng.integers(1, N))
        perm = rng.permutation(N)
        S, A = perm[:nS].tolist(), perm[nS:].tolist()
        T = {x: S[int(rng.integers(nS))] for x in A}
        if trial == 0:  # planted: three degenerate states mapped to one survivor
            E = np.array([0.0, 0.0, 0.0, 0.0])
            S, A, T, beta = [0], [1, 2, 3], {1: 0, 2: 0, 3: 0}, 1.0
        gamma = min(E[x] - E[T[x]] for x in A)  # largest admissible margin (may be negative)
        if rng.random() < 0.5:
            gamma -= float(rng.uniform(0.0, 1.0))  # any smaller margin is admissible as well
        fibres = {}
        for x in A:
            fibres[T[x]] = fibres.get(T[x], 0) + 1
        m = max(fibres.values())
        ZA = sum(math.exp(-beta * E[x]) for x in A)
        ZS = sum(math.exp(-beta * E[x]) for x in S)
        bound = m * math.exp(-beta * gamma) * ZS
        if ZA > bound * (1 + 1e-12):
            return False, dict(reason="transport bound violated", ZA=ZA, bound=bound, m=m)
        if not (ZS <= (ZA + ZS) * (1 + 1e-12) and ZA + ZS <= (1 + m * math.exp(-beta * gamma)) * ZS * (1 + 1e-12)):
            return False, dict(reason="pruning bracket violated", ZA=ZA, ZS=ZS, m=m)
        worst = max(worst, ZA / bound)
        if m > 1:
            multi_fibre_instances += 1
            if ZA > math.exp(-beta * gamma) * ZS * (1 + 1e-9):
                injective_formula_violations += 1
    if multi_fibre_instances == 0 or injective_formula_violations == 0:
        return False, dict(reason="test has no power: the injective formula was never violated",
                           multi_fibre_instances=multi_fibre_instances)
    return True, dict(max_fraction_of_bound=worst, multi_fibre_instances=multi_fibre_instances,
                      injective_formula_violated=injective_formula_violations)


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


def _witness_instance(rng, it):
    """Instance for II.4: configurations, cost matrix D[a, y] = d(a, y), Lipschitz factor kappa, white-box
    part f, residual g with g(x) - g(y) <= kappa d(x, y) (arrays over the configurations), tolerance eps.
    d is the weighted Hamming envelope, except on every fourth instance where it is an arbitrary
    asymmetric cost with zero diagonal (`anchor_necessary` assumes nothing else about d)."""
    if it == 0:
        # Planted tight instance (two binary sites, c = (1, 1), kappa = 1/2, eps = 1/10, tent residual
        # g = -kappa d(00, .)).  A = {00} is a valid eps-certificate and y = 01 has gap 0.45: above the
        # true threshold (1 - kappa) * 1 - eps = 0.4, below the two mutated thresholds 0.6 and 0.9.
        configs = all_configs(2, 2)
        D = np.array([[weighted_hamming((1.0, 1.0), x, y) for y in configs] for x in configs])
        return configs, D, 0.5, np.array([0.0, 0.95, 0.95, 2.5]), -0.5 * D[0], 0.1
    n, k = 2, int(rng.integers(2, 4))
    if rng.random() < 0.4:
        n, k = 3, 2
    configs = all_configs(n, k)
    N = len(configs)
    if it % 4 == 3:      # arbitrary asymmetric cost: d(x, y) = (g(x) - g(y)) / kappa + slack(x, y), slack >= 0
        kappa = float(rng.uniform(0.1, 0.9))
        g = rng.normal(0, 0.5, size=N)
        D = (g[:, None] - g[None, :]) / kappa + rng.uniform(0.0, 1.5, size=(N, N)) * (rng.random(size=(N, N)) < 0.7)
        np.fill_diagonal(D, 0.0)
    else:                # weighted Hamming envelope, g a McShane-type function with factor kappa
        c = rng.uniform(0.5, 1.5, size=n)
        if rng.random() < 0.15:
            c[:] = c[0]
        kappa = float(rng.uniform(0.0, 0.9))
        u = rng.random()
        if u < 0.08:
            kappa = 0.0
        elif u < 0.14:
            kappa = 1.0
        gd = random_lipschitz(rng, configs, c, kappa=kappa)
        g = np.array([gd[x] for x in configs])
        D = np.array([[weighted_hamming(c, x, y) for y in configs] for x in configs])
    eps = float(rng.uniform(0.0, 0.2))
    if rng.random() < 0.15:
        eps = 0.0
    mode = it % 3
    if mode == 0:        # generic landscape
        f = rng.normal(0, 0.4, size=N)
    elif mode == 1:      # nearly flat total energy: many configurations with a small gap
        f = -g + rng.normal(0, 0.15, size=N)
    else:                # a random anchor set is planted as an (almost) tight eps-certificate
        f = rng.normal(0, 0.4, size=N)
        A0 = rng.choice(N, size=int(rng.integers(1, 4)), replace=False)
        U0 = min(f[a] + g[a] for a in A0)
        for y in range(N):
            if y not in A0:
                low = max(g[a] - D[a, y] for a in A0)
                f[y] = U0 - eps - low + float(rng.uniform(0.0, 0.3)) * float(rng.random() < 0.7)
    return configs, D, kappa, f, g, eps


@conjecture("II.4 Witness-size lower bound: every state with gap < (1-kappa) sigma - eps must be an anchor of every eps-certificate")
def t_witness_lower_bound(rng, trials):
    """Exhaustive form of `anchor_necessary` / `anchor_card_lower_bound` (EnvelopeDuality.lean).

    For E = f + g with g(x) - g(y) <= kappa d(x, y), kappa <= 1 (d: weighted Hamming envelope, or an
    arbitrary asymmetric cost), a non-empty anchor set A is an eps-certificate iff
        min_A E - eps <= f(y) + max_{a in A} (g(a) - d(a, y))    for ALL y.
    The theorem: for every eps-certificate A, every y with
        E(y) - Estar < (1 - kappa) * sigma - eps,    sigma <= d(a, y) for all a in A, a != y,
    belongs to A (Estar any lower bound on E over A).  The test enumerates ALL non-empty subsets A of the
    configuration space, keeps the valid certificates and checks the conclusion for each of them with
      * the sharpest admissible separation sigma_y(A) = min_{a in A, a != y} d(a, y) (per-y form),
      * the uniform separation sigma = min_{a != y} d(a, y), which is min_i c_i for the weighted Hamming
        envelope (the cardinality bound |A| >= #forced),
      * Estar = global minimum of E and Estar = min_A E (the largest admissible value),
      * the nominal kappa and the smallest admissible kappa (the exact Lipschitz constant of g).
    Power: the same enumeration must refute two mutated thresholds, (1 - kappa) sigma + eps (sign of
    eps flipped) and sigma - eps (kappa replaced by 0 although the true kappa is positive)."""
    st = dict(instances=0, asymmetric_cost_instances=0, valid_certificates=0, forced_nonempty=0,
              forced_nonempty_uniform=0, wrong_eps_sign_caught=0, kappa_zero_caught=0)
    tight = tight_u = math.inf
    largest_tight = 0
    masks = {}
    for it in range(max(40, trials)):
        configs, D, kappa, f, g, eps = _witness_instance(rng, it)
        N = len(configs)
        E = f + g
        if (g[:, None] - g[None, :] - kappa * D).max() > 1e-9:
            return False, dict(reason="generator produced a residual that is not kappa-Lipschitz")
        off = ~np.eye(N, dtype=bool)
        pos = off & (D > 1e-12)
        kappa_eff = max(0.0, float(((g[:, None] - g[None, :])[pos] / D[pos]).max())) if pos.any() else 0.0
        if (g[:, None] - g[None, :] - kappa_eff * D).max() > 1e-9:
            kappa_eff = kappa
        if N not in masks:
            r = np.arange(1, 2 ** N)
            masks[N] = ((r[:, None] >> np.arange(N)) & 1).astype(bool)
        Mk = masks[N]                                                    # Mk[A, a]  <=>  a in A
        sizes = Mk.sum(axis=1)
        lowenv = np.where(Mk[:, :, None], (g[:, None] - D)[None, :, :], -np.inf).max(axis=1)
        U = np.where(Mk, E[None, :], np.inf).min(axis=1)                 # best evaluated value
        valid = U - eps <= (f[None, :] + lowenv).min(axis=1) + 1e-12     # eps-certificate, all y
        if not valid[-1]:
            return False, dict(reason="the full anchor set is not a certificate (it always is)")
        sigma = np.where(Mk[:, :, None], np.where(off, D, np.inf)[None, :, :], np.inf).min(axis=1)
        sigma_u = float(D[off].min())                                    # uniform separation
        gap_global = np.broadcast_to(E - E.min(), sigma.shape)           # Estar = global minimum
        gap_anchor = E[None, :] - U[:, None]                             # Estar = min_A E

        def forced_sets(kap, gap, sig, eps_sign=-1.0):
            """forced[A, y]: the hypothesis `gap < (1 - kap) sig - eps` holds (with a safety margin)."""
            if 1.0 - kap > 0.0:
                thr = (1.0 - kap) * sig + eps_sign * eps                 # sig = inf (A = {y}): any sigma works
            else:
                thr = np.full(np.shape(sig), eps_sign * eps)
            return gap < thr - 1e-9

        for kap in (kappa, kappa_eff):
            for gap in (gap_global, gap_anchor):
                for sig, label in ((sigma, "per-y separation"), (sigma_u, "uniform separation")):
                    bad = valid[:, None] & forced_sets(kap, gap, sig) & ~Mk
                    if bad.any():
                        A, y = (int(v) for v in np.argwhere(bad)[0])
                        sg = float(sigma[A, y]) if label.startswith("per") else sigma_u
                        return False, dict(reason="forced configuration missing from a valid certificate (" + label + ")",
                                           n_configs=N, d=D.tolist(), kappa=kap, eps=eps, f=f.tolist(), g=g.tolist(),
                                           anchors=[configs[a] for a in range(N) if Mk[A, a]], y=configs[y],
                                           gap=float(gap[A, y]), threshold=(1 - kap) * sg - eps)
        st["instances"] += 1
        st["asymmetric_cost_instances"] += not np.allclose(D, D.T)
        nv = int(valid.sum())
        st["valid_certificates"] += nv
        forced = forced_sets(kappa_eff, gap_global, sigma)               # per-y forced sets (subsets of A)
        nf = forced.sum(axis=1)
        sel = valid & (nf > 0)
        st["forced_nonempty"] += int(sel.sum())
        if sel.any():
            tight = min(tight, float((sizes[sel] / nf[sel]).min()))
        nfu = int(forced_sets(kappa_eff, E - E.min(), sigma_u).sum())    # uniform forced set (same for all A)
        if nfu > 0:
            st["forced_nonempty_uniform"] += nv
            smallest = int(sizes[valid].min())
            tight_u = min(tight_u, smallest / nfu)
            if smallest == nfu:
                largest_tight = max(largest_tight, nfu)
        # power: mutated thresholds must be refuted by some valid certificate
        if eps > 0:
            wrong = valid[:, None] & forced_sets(kappa_eff, gap_global, sigma, eps_sign=+1.0) & ~Mk
            st["wrong_eps_sign_caught"] += int(wrong.any(axis=1).sum())
        if kappa_eff > 1e-9:
            wrong = valid[:, None] & forced_sets(0.0, gap_global, sigma) & ~Mk
            st["kappa_zero_caught"] += int(wrong.any(axis=1).sum())
    if st["valid_certificates"] == 0 or st["forced_nonempty"] == 0 or st["forced_nonempty_uniform"] == 0:
        return False, dict(reason="vacuous: no valid certificate with a non-empty forced set was generated", **st)
    if st["wrong_eps_sign_caught"] == 0 or st["kappa_zero_caught"] == 0:
        return False, dict(reason="powerless: a mutated threshold was never refuted", **st)
    return True, dict(min_cert_over_forced=tight, min_cert_over_forced_uniform=tight_u,
                      largest_forced_set_met_with_equality=largest_tight, **st)


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


@conjecture("II.6 Query-model contact theorem: x optimal for some admissible g matching anchors <=> (contact) & (lower(x) <= upper(y))")
def t_query_model(rng, trials):
    for _ in range(trials):
        n, k = int(rng.integers(2, 4)), int(rng.integers(2, 4))
        configs = all_configs(n, k)
        c = rng.uniform(0.1, 2.0, size=n)
        f = {x: float(rng.normal(0, 1.0)) for x in configs}
        g = random_lipschitz(rng, configs, c)
        anchors = [configs[a] for a in rng.choice(len(configs), size=int(rng.integers(1, 4)), replace=False)]
        lo = {y: max(g[a] - weighted_hamming(c, a, y) for a in anchors) for y in configs}
        hi = {y: min(g[a] + weighted_hamming(c, a, y) for a in anchors) for y in configs}
        pred = {x for x in configs
                if all(f[x] <= f[y] + weighted_hamming(c, y, x) + 1e-12 for y in configs)
                and all(f[x] + lo[x] <= f[y] + hi[y] + 1e-12 for y in configs)}
        # necessity: the true residual's minimisers must be predicted
        best = min(f[y] + g[y] for y in configs)
        for x in configs:
            if f[x] + g[x] <= best + 1e-12 and x not in pred:
                return False, dict(reason="a true minimiser violates the criterion", x=x)
        # sufficiency: explicit extremal residual makes every predicted x optimal
        for x in pred:
            gx = {y: min(hi[y], lo[x] + weighted_hamming(c, y, x)) for y in configs}
            if not check_bd(gx, configs, c, n, k):
                return False, dict(reason="extremal residual not admissible")
            if any(abs(gx[a] - g[a]) > 1e-9 for a in anchors):
                return False, dict(reason="extremal residual does not match anchors")
            if any(f[x] + gx[x] > f[y] + gx[y] + 1e-9 for y in configs):
                return False, dict(reason="predicted x not optimal under extremal residual")
        # randomized necessity: other admissible residuals consistent with the anchors
        for _ in range(10):
            lam = rng.uniform(0, 1)
            g2 = {y: lam * lo[y] + (1 - lam) * hi[y] for y in configs}  # convex combination stays admissible
            b2 = min(f[y] + g2[y] for y in configs)
            for x in configs:
                if f[x] + g2[x] <= b2 + 1e-12 and x not in pred:
                    return False, dict(reason="minimiser of an admissible consistent residual not predicted")
    return True, {}


def _residual_data(rng, n, configs, plant=None):
    """Random published residual data for II.7: envelope constants c (multiples of 1/8, occasionally one
    negative) and a list of anchors (configuration, value), with values that are multiples of 1/8 so that
    consistency is decided exactly in floating point.  Sources of anchor values: an admissible hidden
    function, the same with one corrupted value, unconstrained random values, a chain of anchors exactly
    at (or one step beyond) the envelope limit; sometimes a configuration is listed twice.
    `plant` forces one kind of data: "consistent", "negative_c", "beyond_limit", "conflicting_duplicate"."""
    N = len(configs)
    c = rng.integers(0, 17, size=n) / 8.0
    if plant == "negative_c" or (plant is None and rng.random() < 0.12):
        c[int(rng.integers(n))] = -int(rng.integers(1, 9)) / 8.0
    cabs = np.abs(c)
    na = int(rng.integers(0, 5)) if plant in (None, "negative_c") else int(rng.integers(2, 5))
    pts = [configs[a] for a in rng.choice(N, size=na, replace=False)]
    mode = {None: int(rng.integers(0, 4)), "beyond_limit": 3}.get(plant, 0)
    if mode in (0, 1):       # values of a hidden function with bounded differences |c|
        seeds = [(configs[int(rng.integers(N))], int(rng.integers(-16, 17)) / 8.0) for _ in range(int(rng.integers(1, 4)))]
        vals = [max(u - weighted_hamming(cabs, b, a) for b, u in seeds) for a in pts]
        if mode == 1 and pts:    # corrupt one value
            j = int(rng.integers(len(pts)))
            vals[j] += int(rng.choice([-1, 1])) * int(rng.integers(1, 33)) / 8.0
    elif mode == 2:          # unconstrained values
        vals = [int(rng.integers(-8, 9)) / 8.0 for _ in pts]
    else:                    # chain exactly at the envelope limit, optionally one step (1/8) beyond it
        vals, sign = [], int(rng.choice([-1, 1]))
        for j, a in enumerate(pts):
            vals.append(int(rng.integers(-8, 9)) / 8.0 if j == 0 else vals[0] + sign * weighted_hamming(cabs, pts[0], a))
        if len(pts) >= 2 and (plant == "beyond_limit" or rng.random() < 0.5):
            vals[-1] += sign / 8.0
    anchors = [(a, float(v)) for a, v in zip(pts, vals)]
    duplicated = False
    if anchors and plant != "beyond_limit" and (plant == "conflicting_duplicate" or rng.random() < 0.25):
        a, v = anchors[int(rng.integers(len(anchors)))]
        same = plant == "consistent" or (plant is None and rng.random() < 0.5)
        anchors.append((a, v if same else v + int(rng.choice([-1, 1])) / 8.0))
        duplicated = True
    return c, anchors, duplicated


@conjecture("II.7 Residual data are consistent <=> the anchored bounded-difference class is non-empty (McShane witness / LP infeasibility)")
def t_consistent_iff_nonempty(rng, trials):
    """`RProblem.consistent_iff_nonempty` (CertificateAlgebra.lean).  Data: envelope constants c_i and
    anchors (a_p, v_p).  Consistent := all c_i >= 0 and v_p - v_q <= sum_i c_i [a_p,i != a_q,i] for all
    pairs of anchors.  Class := functions g on all k^n configurations with g(x[i -> s]) - g(x) <= c_i for
    all x, i, s (s = x_i included, which forces c_i >= 0) and g(a_p) = v_p for all anchors.
    (=>) for consistent data both McShane envelopes are verified to lie in the class, constraint by
    constraint; (<=) for inconsistent data the class is shown to be empty by LP infeasibility."""
    from scipy.optimize import linprog
    st = dict(consistent=0, inconsistent=0, by_negative_c=0, by_anchor_pair=0, by_duplicate_anchor=0,
              consistent_no_anchor=0, consistent_duplicate=0, consistent_tight_pair=0)
    planted = ("consistent", "negative_c", "beyond_limit", "conflicting_duplicate")
    for it in range(trials):
        n, k = int(rng.integers(2, 4)), int(rng.integers(2, 4))
        configs = all_configs(n, k)
        idx = {x: a for a, x in enumerate(configs)}
        N = len(configs)
        c, anchors, duplicated = _residual_data(rng, n, configs, plant=planted[it] if it < len(planted) else None)
        consistent = bool(np.all(c >= 0)) and all(vp - vq <= weighted_hamming(c, ap, aq)
                                                    for ap, vp in anchors for aq, vq in anchors)
        # the class as a linear feasibility problem in the k^n unknowns g(x)
        rows, rhs = [], []
        for x in configs:
            for i in range(n):
                for s in range(k):
                    row = np.zeros(N)
                    row[idx[x[:i] + (s,) + x[i + 1:]]] += 1.0
                    row[idx[x]] -= 1.0
                    rows.append(row)
                    rhs.append(c[i])
        A_ub, b_ub = np.array(rows), np.array(rhs)
        A_eq = b_eq = None
        if anchors:
            A_eq = np.zeros((len(anchors), N))
            for p, (a, _) in enumerate(anchors):
                A_eq[p, idx[a]] = 1.0
            b_eq = np.array([v for _, v in anchors])

        def in_class(gv, tol):
            return bool(np.all(A_ub @ gv <= b_ub + tol)) and (A_eq is None or bool(np.all(np.abs(A_eq @ gv - b_eq) <= tol)))

        res = linprog(np.zeros(N), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(None, None)] * N, method="highs")
        if res.status not in (0, 2):
            return False, dict(reason="LP solver did not decide feasibility", status=int(res.status))
        feasible = res.status == 0
        data = dict(n=n, k=k, c=c.tolist(), anchors=[(list(a), v) for a, v in anchors])
        if consistent != feasible:
            return False, dict(reason="Consistent and non-emptiness of the class disagree", consistent=consistent,
                               lp_feasible=feasible, **data)
        if anchors:
            lower = np.array([max(v - weighted_hamming(c, a, y) for a, v in anchors) for y in configs])
            upper = np.array([min(v + weighted_hamming(c, a, y) for a, v in anchors) for y in configs])
        else:
            lower = upper = np.zeros(N)
        if consistent:
            if not in_class(lower, 1e-12):
                return False, dict(reason="consistent data, but the lower McShane envelope is not in the class", **data)
            if not in_class(upper, 1e-12):
                return False, dict(reason="consistent data, but the upper McShane envelope is not in the class", **data)
            if not in_class(res.x, 1e-6):
                return False, dict(reason="LP solution is not in the class", **data)
            if anchors and (np.any(res.x < lower - 1e-6) or np.any(res.x > upper + 1e-6)):
                return False, dict(reason="a member of the class leaves the McShane bracket", **data)
            st["consistent"] += 1
            st["consistent_no_anchor"] += not anchors
            st["consistent_duplicate"] += duplicated
            st["consistent_tight_pair"] += any(ap != aq and vp - vq == weighted_hamming(c, ap, aq)
                                               for ap, vp in anchors for aq, vq in anchors)
        else:
            if in_class(lower, 1e-12) or in_class(upper, 1e-12):
                return False, dict(reason="inconsistent data, but a McShane envelope is in the class", **data)
            st["inconsistent"] += 1
            bad = [(ap == aq) for ap, vp in anchors for aq, vq in anchors if vp - vq > weighted_hamming(c, ap, aq)]
            st["by_negative_c"] += bool(np.any(c < 0))
            st["by_anchor_pair"] += any(not same for same in bad)
            st["by_duplicate_anchor"] += any(bad)
    if min(st["consistent"], st["by_negative_c"], st["by_anchor_pair"], st["by_duplicate_anchor"]) == 0:
        return False, dict(reason="a branch (consistent / negative constant / incompatible pair / conflicting "
                                  "duplicate) was never exercised", **st)
    return True, st


@conjecture("II.8 The robust interval is exact: every value between the envelope optima is attained by an admissible residual (convex combination of the McShane envelopes)")
def t_robust_interval_exact(rng, trials):
    """`robust_min_interval_exact` / `robust_partition_interval_exact` (EnvelopeDuality.lean), setting of
    II.3 / II.5.  For consistent anchor data and g_lam = (1 - lam) lower + lam upper, lam in [0, 1]:
    g_lam is admissible (g(x) - g(y) <= d(x, y) for all pairs) and matches the anchors; every target in
    [min_S (f + lower), min_S (f + upper)] is the minimum of f + g_lam over S for some lam, and every target
    in [Z_beta(f + upper), Z_beta(f + lower)] is the partition function of f + g_lam over S for some lam
    (found by bisection: both maps are continuous and monotone in lam)."""
    err_min = err_z = 0.0
    targets = nondegenerate = 0
    for _ in range(trials):
        n, k = int(rng.integers(2, 4)), int(rng.integers(2, 4))
        configs = all_configs(n, k)
        N = len(configs)
        c = rng.uniform(0.1, 2.0, size=n)
        f = rng.normal(0, 1.0, size=N)
        gd = random_lipschitz(rng, configs, c)
        g = np.array([gd[x] for x in configs])
        A = rng.choice(N, size=int(rng.integers(1, 4)), replace=False)
        D = np.array([[weighted_hamming(c, x, y) for y in configs] for x in configs])
        if (g[A][:, None] - g[A][None, :] - D[np.ix_(A, A)]).max() > 1e-9:
            return False, dict(reason="generator produced inconsistent anchor data")
        lo = (g[A][:, None] - D[A, :]).max(axis=0)
        hi = (g[A][:, None] + D[A, :]).min(axis=0)
        S = np.arange(N) if rng.random() < 0.5 else rng.choice(N, size=int(rng.integers(1, N + 1)), replace=False)
        beta = float(rng.uniform(0.05, 4.0))

        def g_of(lam):
            return (1.0 - lam) * lo + lam * hi

        def fmin(lam):
            return float((f + g_of(lam))[S].min())

        def zfun(lam):
            return float(np.exp(-beta * (f + g_of(lam))[S]).sum())

        def bisect(fun, target, increasing):
            a, b = 0.0, 1.0                                  # invariant: target lies between fun(a) and fun(b)
            for _ in range(64):
                mid = 0.5 * (a + b)
                if (fun(mid) < target) == increasing:
                    a = mid
                else:
                    b = mid
            return b

        t_lo, t_hi = fmin(0.0), fmin(1.0)
        z_lo, z_hi = zfun(1.0), zfun(0.0)
        if t_lo > t_hi + 1e-12 or z_lo > z_hi * (1 + 1e-12):
            return False, dict(reason="envelope optima are not ordered", t_lo=t_lo, t_hi=t_hi, z_lo=z_lo, z_hi=z_hi)
        nondegenerate += t_hi - t_lo > 1e-6
        u = rng.uniform(size=2)
        cases = [(fmin, t, True, 1.0) for t in (t_lo, t_hi, 0.5 * (t_lo + t_hi), *(t_lo + u * (t_hi - t_lo)))]
        cases += [(zfun, z, False, max(1.0, z)) for z in (z_lo, z_hi, math.sqrt(z_lo * z_hi), *(z_lo + u * (z_hi - z_lo)))]
        for fun, target, increasing, scale in cases:
            lam = bisect(fun, target, increasing)
            gl = g_of(lam)
            if (gl[:, None] - gl[None, :] - D).max() > 1e-9:
                return False, dict(reason="interpolated residual is not admissible", lam=lam)
            if np.abs(gl[A] - g[A]).max() > 1e-9:
                return False, dict(reason="interpolated residual does not match the anchors", lam=lam)
            err = abs(fun(lam) - target) / scale
            if err > 1e-9:
                return False, dict(reason="target value inside the robust interval is not attained", target=target,
                                   attained=fun(lam), lam=lam, kind="minimum" if increasing else "partition function",
                                   beta=beta, n=n, k=k)
            if increasing:
                err_min = max(err_min, err)
            else:
                err_z = max(err_z, err)
            targets += 1
    if nondegenerate == 0:
        return False, dict(reason="vacuous: every robust interval was a single point")
    return True, dict(targets_attained=targets, nondegenerate_intervals=nondegenerate,
                      max_abs_error_minimum=err_min, max_rel_error_partition=err_z)


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


@conjecture("III.5 Sandwich gap = KL(reference || target): ln<e^{-b D}> + b<D> = sum w ln(w / tilt)")
def t_kl_identity(rng, trials):
    worst = 0.0
    for _ in range(trials):
        N = int(rng.integers(2, 30))
        w = rng.dirichlet(np.ones(N) * rng.uniform(0.2, 3.0))
        if rng.random() < 0.3:
            w[rng.integers(N)] = 0.0
            w = w / w.sum()
        d = rng.normal(0, rng.uniform(0.1, 3.0), size=N)
        beta = float(rng.uniform(0.01, 5.0))
        tilt = w * np.exp(-beta * d)
        tilt = tilt / tilt.sum()
        mask = w > 0
        kl = float(np.sum(w[mask] * (np.log(w[mask]) - np.log(tilt[mask]))))
        gap = math.log(float(w @ np.exp(-beta * d))) + beta * float(w @ d)
        worst = max(worst, abs(kl - gap))
        if abs(kl - gap) > 1e-8 * max(1.0, abs(gap)):
            return False, dict(kl=kl, gap=gap)
    return True, dict(max_abs_diff=worst)


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


def correlated_reference(rng, n, k, kinds=("gibbs", "markov", "atoms")):
    """Random NON-product reference measure on {0..k-1}^n; returns (configs, weights, kind).
      "gibbs"   pairwise Gibbs measure with strong couplings;
      "markov"  sticky Markov chain (each site copies a relabelling of its predecessor with high probability);
      "atoms"   mixture of a few configurations (perfect correlations, most weights are exactly zero)."""
    configs = all_configs(n, k)
    N = len(configs)
    kind = kinds[int(rng.integers(len(kinds)))]
    if kind == "gibbs":
        h, J = random_pairwise(rng, n, k, scale=float(rng.uniform(0.5, 3.0)))
        e = np.array([energy(h, J, x) for x in configs])
        w = np.exp(-(e - e.min()))
    elif kind == "markov":
        p0 = rng.dirichlet(np.ones(k))
        w = np.array([p0[x[0]] for x in configs])
        for i in range(1, n):
            stick = 1.0 - float(rng.uniform(0.0, 0.3)) ** 2          # close to (sometimes numerically) 1
            T = stick * np.eye(k)[rng.permutation(k)] + (1.0 - stick) * rng.dirichlet(np.ones(k), size=k)
            w = w * np.array([T[x[i - 1], x[i]] for x in configs])
    else:
        w = np.zeros(N)
        atoms = rng.choice(N, size=int(rng.integers(2, 4)), replace=False)
        w[atoms] = rng.dirichlet(np.ones(len(atoms)) * 2.0)
    return configs, w / w.sum(), kind


def log_mgf_centered(w, g, beta):
    """ln E_w[exp(beta (g - E_w g))] (stable; zero weights allowed)."""
    dev = beta * (g - float(w @ g))
    top = float(dev[w > 0].max())
    return top + math.log(float(w[w > 0] @ np.exp(dev[w > 0] - top)))


def random_bd_function(rng, configs, n, k):
    """Random function on the configurations (array) together with its EXACT bounded-difference constants."""
    mode = int(rng.integers(0, 3))
    if mode == 0:       # additive: the extremal shape when the sites are positively correlated
        u = rng.normal(0, 1.0, size=(n, k))
        gd = {x: float(sum(u[i][x[i]] for i in range(n))) for x in configs}
    elif mode == 1:     # McShane-type function
        gd = random_lipschitz(rng, configs, rng.uniform(0.1, 2.0, size=n))
    else:               # unstructured
        gd = {x: float(rng.normal(0, 1.0)) for x in configs}
    return np.array([gd[x] for x in configs]), bd_constants(gd, configs, n, k)


@conjecture("III.6 Hoeffding sandwich for arbitrary (correlated) references uses the full range: ln<e^{β(g-<g>)}> ≤ β² (Σ c_i)² / 8")
def t_hoeffding_correlated(rng, trials):
    """For EVERY reference measure (no independence): 0 <= ln E[exp(beta (g - E g))] <= beta^2 (sum_i c_i)^2 / 8,
    because osc(g) <= sum_i c_i (Hoeffding's lemma) and by Jensen.  The stronger bounded-difference form
    with sum_i c_i^2 is false for correlated references (DEAD.5); the ratio against it is reported."""
    worst = worst_sq = 0.0
    kinds = {}
    for it in range(trials):
        n, k = int(rng.integers(2, 5)), int(rng.integers(2, 4))
        configs, w, kind = correlated_reference(rng, n, k)
        g, c = random_bd_function(rng, configs, n, k)
        beta = float(rng.choice([-1.0, 1.0])) * float(np.exp(rng.uniform(math.log(0.01), math.log(4.0))))
        if it % 10 == 0:
            # extremal shape: two antipodal atoms of equal weight, g additive with full range sum_i c_i
            kind = "antipodal"
            x0 = configs[int(rng.integers(len(configs)))]
            x1 = tuple((a + 1) % k for a in x0)
            w = np.array([0.5 if x in (x0, x1) else 0.0 for x in configs])
            cc = rng.uniform(0.1, 2.0, size=n)
            gd = {x: float(sum(cc[i] for i in range(n) if x[i] == x0[i])) for x in configs}
            g, c = np.array([gd[x] for x in configs]), bd_constants(gd, configs, n, k)
        val = log_mgf_centered(w, g, beta)
        ub = beta ** 2 * float(np.sum(c)) ** 2 / 8
        if val < -1e-10 or val > ub * (1 + 1e-9) + 1e-12:
            return False, dict(val=val, ub=ub, n=n, k=k, beta=beta, reference=kind)
        kinds[kind] = kinds.get(kind, 0) + 1
        if ub > 0:
            worst = max(worst, val / ub)
            worst_sq = max(worst_sq, val / (beta ** 2 * float(np.sum(c ** 2)) / 8))
    return True, dict(max_fraction_of_bound_attained=worst, max_ratio_against_sum_of_squares=worst_sq,
                      references=" ".join(f"{a}:{b}" for a, b in sorted(kinds.items())))


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


@conjecture("IV.3 Trace-enhanced bound is attained when the top-r eigenspace is symmetry-invariant (regular polygons, r = 2)")
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


def leaf_rule_best_bound(h, J, domains):
    """Largest bound L that the kernel's dual-leaf rule `LeafOK I D L u p m` (CertificateAlgebra.lean) accepts
    on the box D for SOME claimed values (u, p) and messages m, i.e. the LP
        maximise   sum_i u_i + sum_{i != j} p_ij
        subject to u_i <= h_i(a) + sum_{j != i} m_ij(a)                       for all i, a in D_i,
                   2 p_ij <= J_ij(a, b) + J_ji(b, a) - m_ij(a) - m_ji(b)       for all i != j, a in D_i, b in D_j
    (messages on every ordered pair of sites, exactly as in the Lean definition)."""
    from scipy.optimize import linprog
    n, k = h.shape
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    pos = {pr: q for q, pr in enumerate(pairs)}
    nv = n + len(pairs) * (1 + k)                     # u_i | p_ij | m_ij(a)

    def P(i, j):
        return n + pos[i, j]

    def M(i, j, a):
        return n + len(pairs) + pos[i, j] * k + a

    rows, rhs = [], []
    for i in range(n):
        for a in domains[i]:
            row = np.zeros(nv)
            row[i] = 1.0
            for j in range(n):
                if j != i:
                    row[M(i, j, a)] = -1.0
            rows.append(row)
            rhs.append(h[i][a])
    for i, j in pairs:
        for a in domains[i]:
            for b in domains[j]:
                row = np.zeros(nv)
                row[P(i, j)] = 2.0
                row[M(i, j, a)] += 1.0
                row[M(j, i, b)] += 1.0
                rows.append(row)
                rhs.append(J[i][j][a][b] + J[j][i][b][a])
    cost = np.zeros(nv)
    cost[: n + len(pairs)] = -1.0
    res = linprog(cost, A_ub=np.array(rows), b_ub=np.array(rhs), bounds=[(None, None)] * nv, method="highs")
    return -res.fun


def triangles_tables(nt):
    """Tables (h, J) of `triangles nt` in the convention of the certificate kernel: every unordered
    in-block pair is stored once, in the orientation i < j, with cost 1 on equal states."""
    n, edges = triangles_instance(nt)
    h = np.zeros((n, 2))
    J = np.zeros((n, n, 2, 2))
    for i, j in edges:
        J[i, j, 0, 0] = J[i, j, 1, 1] = 1.0
    return n, edges, h, J


def _box(dom):
    """Domains of a box; per site 0 / 1 = fixed to that state, 2 = both states available."""
    return [((0, 1) if s == 2 else (s,)) for s in dom]


def triangle_block_tables():
    """Per-triangle tables over the 27 domain states of ONE frustrated triangle, computed from the rules
    of the certificate kernel:
    leaf[state]        best bound of a dual leaf on the box (`LeafOK`, see `leaf_rule_best_bound`);
    prune[state, i, r] dead-end elimination of state r at site i (dominator t = 1 - r) passes `PruneOK`
                       with margin 0 on the box (best link bounds = Goldstein margin >= 0) and removes
                       something (site i still has both states)."""
    n, edges, h, J = triangles_tables(1)
    leaf, prune = {}, {}
    for state in itertools.product(range(3), repeat=3):
        leaf[state] = leaf_rule_best_bound(h, J, _box(state))
        for i in range(3):
            for r in range(2):
                prune[state, i, r] = state[i] == 2 and goldstein(h, J, i, r, 1 - r, _box(state)) >= -1e-9
    return leaf, prune


def bnb_min_leaves_joint(nt, target, use_prune, lp_cache, block_leaf=None):
    """Least number of leaves visited by the kernel over all sum-free certificates (`leaf`, `branch` and,
    if `use_prune`, `prune`) accepted for the bound `target` on `triangles nt`.  Exhaustive memoised
    search over ALL boxes of the joint instance (joint LP per box, joint Goldstein margins): no
    decomposition and no symmetry is used.  (With `block_leaf` the joint LP solve is replaced by the sum
    of the per-triangle LP bounds; the boxes and the dominance checks stay joint.)
    Rules, as in `verify` / `Cert.visited`:
      leaf    closes the box at cost 1 iff the best dual-leaf bound of the box (= its local-polytope LP,
              `lp_bound`; the equality with `leaf_rule_best_bound` is checked in VII.1) is >= target;
      branch  on a site with both states: both children are visited, costs add up;
      prune   state r of a site with both states, dominated by t = 1 - r with Goldstein margin >= 0 over the
              current box: ONE child (r removed), which must certify the same target; no leaf is charged.
    (Branching or pruning on a site that is already fixed does not change the box.)"""
    n, edges, h, J = triangles_tables(nt)
    memo = {}

    def rec(dom):
        if dom in memo:
            return memo[dom]
        if dom not in lp_cache:
            lp_cache[dom] = (lp_bound(n, edges, _box(dom)) if block_leaf is None
                             else sum(block_leaf[dom[3 * q: 3 * q + 3]] for q in range(nt)))
        best = math.inf
        if lp_cache[dom] >= target - 1e-7:
            best = 1
        else:
            for i in range(n):
                if dom[i] != 2:
                    continue
                kids = [dom[:i] + (a,) + dom[i + 1:] for a in range(2)]
                best = min(best, rec(kids[0]) + rec(kids[1]))
                if use_prune:
                    for r in range(2):
                        if goldstein(h, J, i, r, 1 - r, _box(dom)) >= -1e-9:
                            best = min(best, rec(kids[1 - r]))
        memo[dom] = best
        return best

    return rec((2,) * n)


def bnb_min_leaves_blocks(nt, target, use_prune, leaf, prune, unsound_prune=False):
    """The same minimum for larger nt.  A box is described by the multiset of its per-triangle domain
    states (the triangles are interchangeable); the leaf bound is the sum of the per-triangle LP bounds and
    the dominance check only involves the triangle of the pruned site (`triangle_block_tables`; both facts
    are validated against the joint instance in VII.1).  `unsound_prune` (mutation used as a power check)
    allows every elimination regardless of the dominance margin."""
    memo = {}

    def rec(state):
        if state in memo:
            return memo[state]
        best = math.inf
        if sum(leaf[s] for s in state) >= target - 1e-7:
            best = 1
        else:
            for q, s in enumerate(state):
                if q and state[q - 1] == s:
                    continue                          # same moves as on the previous, identical triangle
                rest = state[:q] + state[q + 1:]
                for i in range(3):
                    if s[i] != 2:
                        continue
                    kids = [tuple(sorted(rest + (s[:i] + (a,) + s[i + 1:],))) for a in range(2)]
                    best = min(best, rec(kids[0]) + rec(kids[1]))
                    if use_prune:
                        for r in range(2):
                            if unsound_prune or prune[s, i, r]:
                                best = min(best, rec(kids[1 - r]))
        memo[state] = best
        return best

    return rec(((2, 2, 2),) * nt)


@conjecture("VII.1 Tree-like branch-and-bound with LP-dual leaves and dead-end elimination needs exactly 2^m leaves on m frustrated triangles (2m with decomposition)")
def t_bnb_lower_bound(rng, trials):
    """`sumFree_exponential` / `sumFree_complexity` / `sum_linear` (ProofComplexity.lean; rules of
    `verify` in CertificateAlgebra.lean).  On m disjoint frustrated triangles the least number of leaves
    visited by a certificate without the `sum` rule for the bound K <= m is exactly 2^K, with and without
    the dead-end-elimination rule `prune`; with decomposition over the triangles 2m leaves suffice.
    Exhaustive minimum-leaf search: on the joint instance for m <= 2, on all boxes for m = 3, on
    per-triangle states for m <= 4 (m <= 5 in the full run)."""
    full = trials > 100
    leaf, prune = triangle_block_tables()
    # (0) on random joint boxes: best bound of the kernel's leaf rule = local-polytope LP = sum of the
    #     per-triangle leaf bounds, and the dominance check only involves the triangle of the pruned site
    n_boxes = max(12, trials // 4)
    for b in range(n_boxes):
        nt = 2 + b % 2
        n, edges, h, J = triangles_tables(nt)
        dom = tuple(int(v) for v in rng.choice(3, size=n, p=[0.2, 0.2, 0.6]))
        blocks = [dom[3 * q: 3 * q + 3] for q in range(nt)]
        lp_primal = lp_bound(n, edges, _box(dom))                    # local-polytope LP on the edges
        lp_kernel = leaf_rule_best_bound(h, J, _box(dom))             # the kernel's leaf rule on the joint instance
        lp_blocks = sum(leaf[s] for s in blocks)
        if abs(lp_primal - lp_blocks) > 1e-7 or abs(lp_kernel - lp_blocks) > 1e-7:
            return False, dict(reason="leaf bound does not decompose over the triangles", box=dom, lp_primal=lp_primal,
                               leaf_rule=lp_kernel, sum_of_blocks=lp_blocks)
        for i in range(n):
            for r in range(2):
                joint_ok = dom[i] == 2 and goldstein(h, J, i, r, 1 - r, _box(dom)) >= -1e-9
                if joint_ok != prune[blocks[i // 3], i % 3, r]:
                    return False, dict(reason="dominance check does not decompose over the triangles", box=dom, site=i, r=r)
    # (1) exact sum-free complexity 2^K for every bound K <= m, with and without dead-end elimination:
    #     "joint"  all boxes, joint LP and joint dominance margins (m <= 2);
    #     "boxes"  all boxes and joint dominance margins, leaf bound summed over the triangles (m = 3, K = 3);
    #     "blocks" multisets of per-triangle states (m <= 4, m <= 5 in the full run).
    lp_cache, sum_cache = {}, {}
    searches = [("joint", 1, None), ("joint", 2, None), ("boxes", 3, 3)]
    searches += [("blocks", nt, None) for nt in range(1, (5 if full else 4) + 1)]
    free, pruned, n_searches = {}, {}, 0
    for kind, nt, only_K in searches:
        for K in (range(nt + 1) if only_K is None else [only_K]):
            for use_prune in (False, True):
                if kind == "joint":
                    got = bnb_min_leaves_joint(nt, K, use_prune, lp_cache)
                elif kind == "boxes":
                    got = bnb_min_leaves_joint(nt, K, use_prune, sum_cache, block_leaf=leaf)
                else:
                    got = bnb_min_leaves_blocks(nt, K, use_prune, leaf, prune)
                if got != 2 ** K:
                    return False, dict(reason="least number of leaves of a sum-free certificate is not 2^K", m=nt, K=K,
                                       prune_rule=use_prune, leaves=got, search=kind)
                n_searches += 1
                if K == nt:
                    (pruned if use_prune else free)[nt] = got
    for dom, val in lp_cache.items():                # every box met by the joint searches: joint LP = sum of blocks
        if abs(val - sum(leaf[dom[3 * q: 3 * q + 3]] for q in range(len(dom) // 3))) > 1e-7:
            return False, dict(reason="leaf bound does not decompose over the triangles", box=dom, lp_joint=val)
    n_boxes += len(lp_cache)
    def show(d):
        return " ".join(f"m={a}:{b}" for a, b in sorted(d.items()))

    # (2) power: with an UNSOUND elimination rule (dominance margin ignored) the search must find fewer leaves
    mutated = {nt: bnb_min_leaves_blocks(nt, nt, True, leaf, prune, unsound_prune=True) for nt in sorted(free)}
    if any(mutated[nt] >= 2 ** nt for nt in mutated):
        return False, dict(reason="powerless: an unsound elimination rule did not reduce the number of leaves",
                           leaves=show(mutated))
    # (3) with decomposition (`sum` rule, as in `peelCert`): the instance is the termwise sum of its triangles;
    #     each triangle alone is certified for the bound 1 by one branching and two dual leaves (never by a
    #     single leaf), so the bound m = 1 + ... + 1 costs 2m leaves
    per_triangle = bnb_min_leaves_blocks(1, 1, True, leaf, prune)
    with_sum = {}
    for nt in sorted(free):
        n, edges = triangles_instance(nt)
        parts = [edges[3 * q: 3 * q + 3] for q in range(nt)]
        if sorted(e for part in parts for e in part) != sorted(edges):
            return False, dict(reason="the triangles do not add up to the instance", m=nt)
        for q, sub in enumerate(parts):
            if lp_bound(n, sub, _box((2,) * n)) >= 1 - 1e-7:
                return False, dict(reason="a single leaf certifies a frustrated triangle", m=nt, triangle=q)
            for a in range(2):
                dom = (2,) * (3 * q) + (a,) + (2,) * (n - 3 * q - 1)
                if lp_bound(n, sub, _box(dom)) < 1 - 1e-7:
                    return False, dict(reason="two-leaf certificate of one triangle is rejected", m=nt, triangle=q, state=a)
        with_sum[nt] = nt * per_triangle
        if with_sum[nt] != 2 * nt or (nt >= 3 and with_sum[nt] >= free[nt]):
            return False, dict(reason="decomposed certificate does not have 2m leaves", m=nt, leaves=with_sum[nt])
    return True, dict(sum_free=show(free), sum_free_with_prune=show(pruned), with_decomposition=show(with_sum),
                      exhaustive_searches_equal_to_2_pow_K=n_searches, joint_boxes_validated=n_boxes,
                      valid_eliminations_per_triangle=int(sum(prune.values())), unsound_prune_mutation=show(mutated))


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


@conjecture("VII.2 Description length: the peeling certificate with `sum` has dataSize < 147 m^3, and 147 m^3 < 2^m for m >= 21 (sum nodes charged for embedded sub-instances)")
def t_description_length(rng, trials):
    """Lean: Cert.dataSize, peelCert_dataSize, sum_rule_separation_dataSize.  The certificate tree is
    rebuilt here and measured with the Lean definition of dataSize, independently of the closed form."""
    def data_size(node, n, k):
        kind = node[0]
        if kind == "leaf":
            return 1 + n + n * n + n * n * k
        if kind == "branch":
            return 1 + sum(data_size(c, n, k) for c in node[1])
        if kind == "prune":
            return 1 + n + data_size(node[1], n, k)
        if kind == "sum":
            return 1 + 2 * (n * k + n * n * k * k) + data_size(node[1], n, k) + data_size(node[2], n, k)
        raise ValueError(kind)

    def size(node):
        kind = node[0]
        if kind == "leaf":
            return 1
        if kind == "branch":
            return 1 + sum(size(c) for c in node[1])
        if kind == "prune":
            return 1 + size(node[1])
        return 1 + size(node[1]) + size(node[2])

    block = ("branch", [("leaf",), ("leaf",)])

    def peel(j):
        return block if j == 1 else ("sum", block, peel(j - 1))

    threshold = None
    for m in range(1, 41):
        n, k = 3 * m, 2
        cert = peel(m)
        ds = data_size(cert, n, k)
        block_cost = 1 + 2 * (1 + n + n * n + n * n * 2)
        sum_cost = 1 + 2 * (n * 2 + n * n * 2 * 2)
        if ds + sum_cost != m * (block_cost + sum_cost):
            return False, dict(reason="closed form of peelCert_dataSize is wrong", m=m, ds=ds)
        if size(cert) + 1 != 4 * m:
            return False, dict(reason="node count of the peeling certificate is not 4m - 1", m=m)
        if ds > 147 * m ** 3:
            return False, dict(reason="dataSize exceeds 147 m^3", m=m, ds=ds)
        if m >= 21 and not 147 * m ** 3 < 2 ** m:
            return False, dict(reason="147 m^3 < 2^m fails", m=m)
        if m >= 4 and not 4 * m <= 2 ** m:
            return False, dict(reason="4 m <= 2^m fails", m=m)
        if threshold is None and ds < 2 ** m and m > 4:
            threshold = m
    # the stated threshold 21 is where the *bound* 147 m^3 drops below 2^m; the actual crossover is earlier
    if not (147 * 20 ** 3 >= 2 ** 20):
        return False, dict(reason="threshold m >= 21 for the constant 147 is not sharp any more")
    return True, dict(actual_crossover_m=threshold, bound_crossover_m=21)


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
    """Continuous analogue of `anchor_card_lower_bound` (classical, not formalized): two
    Lam-Lipschitz functions on the circle agree on all n queries yet their minima differ by
    Lam * (largest gap) / 2 >= Lam / (2n), so no certificate from these queries can be tighter."""
    grid = np.linspace(0.0, 1.0, 4001, endpoint=False)

    def circ_dist(a, b):
        d = np.abs(a - b) % 1.0
        return np.minimum(d, 1.0 - d)

    for _ in range(trials):
        n = int(rng.integers(1, 12))
        lam = float(rng.uniform(0.2, 5.0))
        pts = np.sort(rng.uniform(0, 1, size=n))
        gaps = np.diff(np.r_[pts, pts[0] + 1.0])
        j = int(np.argmax(gaps))
        big = float(gaps[j])
        if big < 1.0 / n - 1e-12:
            return False, dict(reason="pigeonhole violated")
        centre = (pts[j] + big / 2) % 1.0
        f0 = np.zeros_like(grid)
        f1 = -np.maximum(0.0, lam * (big / 2 - circ_dist(grid, centre)))  # tent inside the largest gap
        # (i) both functions are Lam-Lipschitz on the grid (finite-difference check with wrap-around)
        step = grid[1] - grid[0]
        slope = np.abs(np.diff(np.r_[f1, f1[0]])) / step
        if slope.max() > lam * (1 + 1e-6):
            return False, dict(reason="adversary is not Lam-Lipschitz", slope=float(slope.max()), lam=lam)
        # (ii) they agree at every query point
        at_queries = -np.maximum(0.0, lam * (big / 2 - circ_dist(pts, centre)))
        if np.abs(at_queries).max() > 1e-9:
            return False, dict(reason="adversary differs from f0 at a query", val=float(np.abs(at_queries).max()))
        # (iii) their minima differ by at least Lam/(2n)
        depth = float(f0.min() - f1.min())
        if depth < lam / (2 * n) - lam * step:
            return False, dict(depth=depth, required=lam / (2 * n))
    return True, {}


def _cos_range(a, b):
    """Exact range (min, max) of cos on the interval [a, b]."""
    two_pi = 2.0 * math.pi
    top = 1.0 if math.ceil(a / two_pi) <= math.floor(b / two_pi) else max(math.cos(a), math.cos(b))
    bot = -1.0 if math.ceil((a - math.pi) / two_pi) <= math.floor((b - math.pi) / two_pi) else min(math.cos(a), math.cos(b))
    return bot, top


def _gauss_legendre_box(fun, lo, hi, order):
    """Tensor Gauss-Legendre rule with `order` nodes per axis for fun(X), X of shape (..., d), on prod_i [lo_i, hi_i]."""
    nodes, weights = np.polynomial.legendre.leggauss(order)
    d = len(lo)
    xs = [0.5 * (hi[i] - lo[i]) * nodes + 0.5 * (hi[i] + lo[i]) for i in range(d)]
    X = np.stack(np.meshgrid(*xs, indexing="ij"), axis=-1)
    W = np.ones(X.shape[:-1])
    for i in range(d):
        shape = [1] * d
        shape[i] = -1
        W = W * (0.5 * (hi[i] - lo[i]) * weights).reshape(shape)
    return float(np.sum(W * fun(X)))


def _voxel_energy(amp, freq, kappa):
    """E(x) = sum_i amp_i cos(freq_i x_i) + kappa * prod_i sin(x_i), vectorised over X of shape (..., d)."""
    return lambda X: (amp * np.cos(freq * X)).sum(axis=-1) + kappa * np.prod(np.sin(X), axis=-1)


def _voxel_integral(lo, hi, beta, amp, freq, kappa):
    """int_box exp(-beta E) by two independent methods that do not share the product structure of the
    envelope integrals: adaptive nested Gauss-Kronrod quadrature (scipy nquad, error-controlled) and
    tensor Gauss-Legendre rules of two different orders (their difference is the error estimate).
    Returns (value, absolute tolerance covering both error estimates and the disagreement of the two
    methods, relative disagreement of the two methods)."""
    from scipy import integrate
    d = len(lo)
    amp_l, freq_l = [float(v) for v in amp], [float(v) for v in freq]

    def boltzmann(*x):
        s, p = 0.0, kappa
        for i in range(d):
            s += amp_l[i] * math.cos(freq_l[i] * x[i])
            p *= math.sin(x[i])
        return math.exp(-beta * (s + p))

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", integrate.IntegrationWarning)
        v_nq, e_nq = integrate.nquad(boltzmann, [(float(lo[i]), float(hi[i])) for i in range(d)],
                                     opts=dict(epsabs=0.0, epsrel=1e-11, limit=200))
    E = _voxel_energy(amp, freq, kappa)
    g1 = _gauss_legendre_box(lambda X: np.exp(-beta * E(X)), lo, hi, 32)
    g2 = _gauss_legendre_box(lambda X: np.exp(-beta * E(X)), lo, hi, 44)
    disagreement = abs(v_nq - g2)
    tol = max(e_nq, abs(g1 - g2), disagreement) + 1e-12 * abs(g2)
    return g2, tol, disagreement / abs(g2)


def _envelope_product(env, lo, hi, beta, split=None):
    """prod_i int_{lo_i}^{hi_i} exp(-beta env_i(t)) dt by adaptive 1-D quadrature (scipy quad).
    Returns (product, bound on its relative error from the quadrature error estimates).  With `split`
    every interval is first cut at lo_i + split * (hi_i - lo_i), which moves all quadrature nodes."""
    from scipy import integrate
    prod, rel = 1.0, 1e-12
    for i, fn in enumerate(env):
        a, b = float(lo[i]), float(hi[i])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", integrate.IntegrationWarning)
            v, e = integrate.quad(lambda t: math.exp(-beta * fn(t)), a, b, epsabs=0.0, epsrel=1e-12, limit=200,
                                  points=None if split is None else [a + split * (b - a)])
        prod *= v
        rel += e / v
    return prod, rel


def _voxel_const_envelopes(amp, freq, offset):
    """phi_i = a_i - offset, psi_i = a_i + offset with a_i(t) = amp_i cos(freq_i t); valid iff the coupling
    term satisfies |kappa prod_i sin(x_i)| <= d * offset on the box (true for offset = kappa/d)."""
    d = len(amp)
    phis = [(lambda t, i=i: amp[i] * np.cos(freq[i] * t) - offset) for i in range(d)]
    psis = [(lambda t, i=i: amp[i] * np.cos(freq[i] * t) + offset) for i in range(d)]
    return phis, psis, np.full(d, 2.0 * offset)


def _voxel_taylor_envelopes(lo, hi, amp, freq, kappa, mode):
    """Second-order separable envelopes of E on the box: Taylor expansion at the centre c with a diagonal
    enclosure of the Hessian over the whole box,
        E(c) + g.u + sum_i (m_i/2) u_i^2  <=  E(c + u)  <=  E(c) + g.u + sum_i (M_i/2) u_i^2,
    m_i <= H_ii - sum_{j != i} |H_ij|  and  M_i >= H_ii + sum_{j != i} |H_ij|  everywhere on the box
    (Lagrange remainder + Gershgorin), with the entries of H enclosed by exact ranges of cos / sin and
    interval products.  Modes:
      "enclosure"  per-axis curvatures m_i, M_i;
      "uniform"    scalar curvatures m = min_i m_i, M = max_i M_i (the form quoted in SeparableVoxel.lean);
      "centre"     INVALID: curvature of the Taylor polynomial at the centre only (no enclosure, m = M);
      "quarter"    INVALID: the enclosure shrunk towards the centre curvature by a factor 4.
    Returns (phis, psis, w) with psi_i - phi_i <= w_i = (M_i - m_i) r_i^2 / 2 on [lo_i, hi_i]."""
    d = len(lo)
    c = 0.5 * (lo + hi)
    r = 0.5 * (hi - lo)
    sin_rng = [_cos_range(lo[i] - math.pi / 2, hi[i] - math.pi / 2) for i in range(d)]
    sin_abs = [max(abs(v) for v in sin_rng[i]) for i in range(d)]
    cos_abs = [max(abs(v) for v in _cos_range(lo[i], hi[i])) for i in range(d)]
    pmin = pmax = 1.0                               # exact range of prod_i sin(x_i) over the box
    for a, b in sin_rng:
        cands = (pmin * a, pmin * b, pmax * a, pmax * b)
        pmin, pmax = min(cands), max(cands)
    sin_c = np.sin(c)
    e_c = float(np.sum(amp * np.cos(freq * c)) + kappa * np.prod(sin_c))
    grad = np.array([-amp[i] * freq[i] * math.sin(freq[i] * c[i])
                     + kappa * math.cos(c[i]) * float(np.prod(np.delete(sin_c, i))) for i in range(d)])
    m, M, h_c = np.zeros(d), np.zeros(d), np.zeros(d)
    for i in range(d):
        a, b = _cos_range(freq[i] * lo[i], freq[i] * hi[i])
        s = amp[i] * freq[i] ** 2                   # H_ii = -s cos(freq_i x_i) - kappa prod_j sin(x_j)
        radius = sum(abs(kappa) * cos_abs[i] * cos_abs[j] * float(np.prod([sin_abs[q] for q in range(d) if q not in (i, j)]))
                     for j in range(d) if j != i)   # |H_ij| = |kappa cos x_i cos x_j prod_{q != i,j} sin x_q|
        m[i] = min(-s * a, -s * b) + min(-kappa * pmin, -kappa * pmax) - radius
        M[i] = max(-s * a, -s * b) + max(-kappa * pmin, -kappa * pmax) + radius
        h_c[i] = -s * math.cos(freq[i] * c[i]) - kappa * float(np.prod(sin_c))
    pad = 1e-12 * (1.0 + np.abs(m) + np.abs(M))     # outward rounding of the enclosure
    m, M = m - pad, M + pad
    if mode == "uniform":
        m, M = np.full(d, m.min()), np.full(d, M.max())
    elif mode == "centre":
        m, M = h_c.copy(), h_c.copy()
    elif mode == "quarter":
        m, M = h_c - 0.25 * (h_c - m), h_c + 0.25 * (M - h_c)
    elif mode != "enclosure":
        raise ValueError(mode)
    phis = [(lambda t, i=i: e_c / d + grad[i] * (t - c[i]) + 0.5 * m[i] * (t - c[i]) ** 2) for i in range(d)]
    psis = [(lambda t, i=i: e_c / d + grad[i] * (t - c[i]) + 0.5 * M[i] * (t - c[i]) ** 2) for i in range(d)]
    return phis, psis, 0.5 * (M - m) * r ** 2


@conjecture("X.1 Separable voxel envelope: prod_i int exp(-b psi_i) <= int_box exp(-b E) <= prod_i int exp(-b phi_i)")
def t_separable_voxel(rng, trials):
    """`separable_voxel_bounds` / `separable_voxel_ratio` (SeparableVoxel.lean) with independent quadrature.

    The d-dimensional integral is computed by tensor Gauss-Legendre rules of two orders (reference value)
    and by adaptive nested Gauss-Kronrod quadrature (`nquad`, error-controlled cross-check); the
    one-dimensional envelope integrals by adaptive `quad` (for the ratio bound the two products are
    computed on different nodes).  The reference value shares no grid with the envelope integrals, so
    the inequalities are compared up to the quadrature error estimates only (a few 1e-11 relative) and
    can fail.  Envelopes: (A) phi_i, psi_i = a_i -+ kappa/d (the coupling is bounded by
    kappa), (B) second-order Taylor envelopes with a diagonal Hessian enclosure; the hypothesis
    sum phi_i <= E <= sum psi_i of both is verified pointwise on sample points of the box.
    Power: deliberately INVALID envelopes (offset kappa/(4d); Taylor polynomial without Hessian
    enclosure; enclosure shrunk by 4) are run through the same comparison; the first two must be caught."""
    n_inst = max(12, trials // 2)
    worst, margin, max_tol, max_disagree, fubini, checks = 0.0, math.inf, 0.0, 0.0, 0.0, 0
    caught = dict(const_quarter=0, taylor_centre=0, taylor_quarter=0)
    for it in range(n_inst):
        d = int(rng.integers(1, 4))
        lo = rng.uniform(-1.0, 0.0, size=d)
        hi = lo + rng.uniform(0.2, 1.5, size=d) * (1.0 if rng.random() < 0.5 else 0.2)   # coarse and fine voxels
        beta = float(rng.uniform(0.1, 4.0))
        amp = rng.normal(0, 1.0, size=d)
        freq = rng.uniform(0.5, 3.0, size=d)
        kappa = float(rng.uniform(0.0, 1.0))
        if it == 0:      # planted: one-signed coupling, kappa * sin(x) < -kappa/4 on the whole box
            d, lo, hi, beta, kappa = 1, np.array([-1.0]), np.array([-0.5]), 2.0, 1.0
            amp, freq = np.array([0.3]), np.array([1.0])
        elif it == 1:    # planted: no coupling, the three quantities coincide (Fubini)
            kappa = 0.0
        # E(x) = sum_i amp_i cos(freq_i x_i) + kappa * prod_i sin(x_i);  |coupling| <= kappa
        E = _voxel_energy(amp, freq, kappa)
        true, tol, disagree = _voxel_integral(lo, hi, beta, amp, freq, kappa)
        if disagree > 1e-9:
            return False, dict(reason="independent integrators disagree on the d-dimensional integral",
                               d=d, value=true, relative_disagreement=disagree)
        max_tol, max_disagree = max(max_tol, tol / true), max(max_disagree, disagree)
        pts = np.vstack([lo + (hi - lo) * rng.uniform(size=(256, d)),
                         np.array(list(itertools.product(*zip(lo, hi)))), 0.5 * (lo + hi)[None, :]])
        e_pts = E(pts)

        def hypothesis_holds(phis, psis):
            low = sum(phis[i](pts[:, i]) for i in range(d))
            upp = sum(psis[i](pts[:, i]) for i in range(d))
            slack = 1e-11 * (1.0 + float(np.abs(e_pts).max()))
            return bool(np.all(low <= e_pts + slack) and np.all(e_pts <= upp + slack))

        def sandwich(phis, psis):
            lower, rl = _envelope_product(psis, lo, hi, beta)
            upper, ru = _envelope_product(phis, lo, hi, beta)
            ok = lower * (1 - rl) <= true + tol and true - tol <= upper * (1 + ru)
            return ok, lower, upper, rl + ru

        taylor_mode = "enclosure" if it % 2 == 0 else "uniform"
        valid = [("offset kappa/d", _voxel_const_envelopes(amp, freq, kappa / d)),
                 ("second-order Taylor, " + taylor_mode, _voxel_taylor_envelopes(lo, hi, amp, freq, kappa, taylor_mode))]
        for label, (phis, psis, w) in valid:
            if not hypothesis_holds(phis, psis):
                return False, dict(reason="envelope hypothesis sum phi_i <= E <= sum psi_i fails pointwise", envelope=label,
                                   d=d, lo=lo.tolist(), hi=hi.tolist(), amp=amp.tolist(), freq=freq.tolist(), kappa=kappa)
            ok, lower, upper, rel = sandwich(phis, psis)
            if not ok:
                return False, dict(envelope=label, lower=lower, true=true, upper=upper, d=d, beta=beta, lo=lo.tolist(),
                                   hi=hi.tolist(), amp=amp.tolist(), freq=freq.tolist(), kappa=kappa, abs_tol=tol)
            # ratio bound: its hypothesis psi_i <= phi_i + w_i is checked on a grid of every factor, and the
            # lower product is recomputed on shifted nodes, so that the two sides of the comparison are not
            # sums over the same quadrature nodes
            for i in range(d):
                t = np.linspace(lo[i], hi[i], 129)
                if float(np.max(psis[i](t) - phis[i](t))) > w[i] + 1e-11 * (1.0 + abs(w[i])):
                    return False, dict(reason="width hypothesis psi_i <= phi_i + w_i fails", envelope=label, axis=i, d=d)
            lower2, rl2 = _envelope_product(psis, lo, hi, beta, split=0.381966)
            if abs(lower2 - lower) > (rel + rl2) * lower:
                return False, dict(reason="1-D quadratures of the same envelope integral disagree", envelope=label,
                                   lower=lower, lower_shifted_nodes=lower2, d=d)
            if upper > math.exp(beta * float(np.sum(w))) * lower2 * (1 + rel + rl2):
                return False, dict(reason="ratio bound exp(beta * sum w_i) violated", envelope=label, lower=lower2,
                                   upper=upper, bound=math.exp(beta * float(np.sum(w))), d=d)
            checks += 1
            worst = max(worst, upper / lower)
            if kappa == 0.0 and label.startswith("offset"):      # equality case: Fubini for a separable energy
                fubini = max(fubini, abs(true - lower) / true, abs(upper - true) / true)
            else:
                margin = min(margin, (true - lower) / true, (upper - true) / true)
        invalid = [("const_quarter", _voxel_const_envelopes(amp, freq, kappa / (4 * d))),
                   ("taylor_centre", _voxel_taylor_envelopes(lo, hi, amp, freq, kappa, "centre")),
                   ("taylor_quarter", _voxel_taylor_envelopes(lo, hi, amp, freq, kappa, "quarter"))]
        for label, (phis, psis, _) in invalid:
            caught[label] += not sandwich(phis, psis)[0]
    if caught["const_quarter"] == 0 or caught["taylor_centre"] == 0:
        return False, dict(reason="powerless: an invalid envelope never violated the claimed inequality",
                           instances=n_inst, **{"invalid_" + k: v for k, v in caught.items()})
    return True, dict(instances=n_inst, sandwiches_checked=checks, max_ratio_upper_over_lower=worst,
                      smallest_relative_margin=margin, max_relative_quadrature_tol=max_tol,
                      max_integrator_disagreement=max_disagree, separable_case_relative_error=fubini,
                      invalid_offset_kappa_4d_caught=caught["const_quarter"],
                      invalid_taylor_no_enclosure_caught=caught["taylor_centre"],
                      invalid_taylor_quarter_enclosure_caught=caught["taylor_quarter"])


# ----------------------------------------------------------------------------------------------
# Cluster XI — certification geometry (cycle 7): slack coverings, LP duals, rates, best-first,
# conditional envelopes, thermal certificates, second-order envelopes, compositional Z rules
# ----------------------------------------------------------------------------------------------

def cg_metric(rng, n, asym=False):
    """Shortest-path closure of random weights: a metric, or a quasi-metric if asym."""
    W = rng.uniform(0.3, 2.0, size=(n, n))
    if not asym:
        W = (W + W.T) / 2
    np.fill_diagonal(W, 0.0)
    for k in range(n):
        W = np.minimum(W, W[:, [k]] + W[[k], :])
    return W


def cg_lipschitz(rng, d, kappa):
    """g with g(x) - g(y) <= kappa d(x,y): a convex combination of the two McShane extensions of random data."""
    n = len(d)
    if kappa == 0:
        return np.zeros(n)
    v = rng.normal(0, 1.0, size=n)
    lo = np.max(v[:, None] - kappa * d, axis=0)          # max_a v(a) - kappa d(a, y)
    hi = np.min(v[None, :] + kappa * d, axis=1)          # min_a v(a) + kappa d(y, a)
    lam = rng.uniform()
    return lam * lo + (1 - lam) * hi


def cg_slack(d, g):
    """s[a, y] = d(a, y) - g(a) + g(y)."""
    return d - g[:, None] + g[None, :]


def cg_bounds(d, f, g, A):
    """What a verifier computes from the evaluations of g on A: (min(f+L), min(f+U), min_A (f+g), L, U)."""
    A = list(A)
    L = np.max(g[A][:, None] - d[A, :], axis=0)
    U = np.min(g[A][None, :] + d[:, A], axis=1)
    return float(np.min(f + L)), float(np.min(f + U)), float(np.min((f + g)[A])), L, U


def cg_min_cover(C):
    """Exact minimum number of rows of the boolean matrix C whose union is everything (brute force)."""
    n, m = C.shape
    masks = [sum(1 << y for y in range(m) if C[a, y]) for a in range(n)]
    full = (1 << m) - 1
    for size in range(1, n + 1):
        for S in itertools.combinations(range(n), size):
            acc = 0
            for a in S:
                acc |= masks[a]
            if acc == full:
                return size
    return None


def cg_frac_cover(C):
    from scipy.optimize import linprog
    res = linprog(np.ones(C.shape[0]), A_ub=-C.T.astype(float), b_ub=-np.ones(C.shape[1]), bounds=(0, None),
                  method="highs")
    return float(res.fun)


def cg_instance(rng, nmax=8, kappas=(0.0, 0.3, 0.7, 1.0), asym_prob=0.4):
    n = int(rng.integers(3, nmax + 1))
    d = cg_metric(rng, n, asym=rng.random() < asym_prob)
    kappa = float(rng.choice(kappas))
    g = cg_lipschitz(rng, d, kappa)
    f = rng.normal(0, 0.8, size=n)
    eps = float(rng.choice([0.0, 0.1, 0.4]))
    return n, d, kappa, f, g, eps


@conjecture("XI.1 Certificates are coverings in the slack quasi-metric: LB(A) = min_y [E(y) - s(A,y)]; certificate <=> cover; N_cov <= N_val <= N* <= N_cov + 1")
def t_cert_cover(rng, trials):
    stats = dict(star_gt_cov=0, instances=0)
    for _ in range(trials):
        n, d, kappa, f, g, eps = cg_instance(rng)
        E = f + g
        s = cg_slack(d, g)
        if s.min() < -1e-9 or np.max(np.abs(np.diag(s))) > 1e-12:
            return False, dict(reason="slack is negative or non-zero on the diagonal")
        if not np.all(s[:, None, :] <= s[:, :, None] + s[None, :, :] + 1e-9):
            return False, dict(reason="slack violates the triangle inequality")
        gap = E - E.min()
        nval = nstar = None
        for size in range(1, n + 1):
            for A in itertools.combinations(range(n), size):
                lb, ubval, ubpt, L, U = cg_bounds(d, f, g, A)
                sA = s[list(A), :].min(axis=0)                     # s(A, y)
                sAt = s[:, list(A)].min(axis=1)                    # s(y, A)
                if np.max(np.abs(L - (g - sA))) > 1e-9 or np.max(np.abs(U - (g + sAt))) > 1e-9:
                    return False, dict(reason="McShane bracket is not [g - s(A,.), g + s(.,A)]")
                if abs(lb - float(np.min(E - sA))) > 1e-9:
                    return False, dict(reason="LB(A) != min_y [E(y) - s(A,y)]")
                is_cert = ubpt - lb <= eps + 1e-12
                is_cover = bool(np.all(sA <= E - ubpt + eps + 1e-12))
                if is_cert != is_cover:
                    return False, dict(reason="certificate <=> covering with radii E(y) - UB + eps fails", A=A)
                if nval is None and ubval - lb <= eps + 1e-12:
                    nval = size
                if nstar is None and is_cert:
                    nstar = size
            if nstar is not None:
                break
        ncov = cg_min_cover(s <= gap[None, :] + eps + 1e-12)
        if not (ncov <= nval <= nstar <= ncov + 1):
            return False, dict(reason="N_cov <= N_val <= N* <= N_cov + 1 fails", ncov=ncov, nval=nval, nstar=nstar)
        stats["star_gt_cov"] += nstar > ncov
        stats["instances"] += 1
    return True, stats


@conjecture("XI.2 Covering LP duality: forced points, fooling sets, volume, exponential-weights and partition-function bounds are <= N_frac <= N_cov <= (1 + ln max|S(a)|) N_frac")
def t_cover_duals(rng, trials):
    best = 0.0
    for it in range(max(5, trials // 2)):
        if it % 5 == 4:       # adversarial family: a cluster of near-degenerate minima closer than eps, far high states
            m, r = int(rng.integers(2, 6)), int(rng.integers(1, 4))
            n = m + r
            delta = float(rng.uniform(0.05, 0.2))
            d = np.full((n, n), float(rng.uniform(1.0, 2.0)))
            d[:m, :m] = delta
            np.fill_diagonal(d, 0.0)
            kappa, g = 0.0, np.zeros(n)
            f = np.concatenate([rng.uniform(0.0, delta / 4, size=m), np.full(r, 3.0)])
            eps = float(rng.uniform(delta, 0.4))
        else:
            n, d, kappa, f, g, eps = cg_instance(rng, nmax=10, kappas=(0.0, 0.3, 0.7))
        E = f + g
        s = cg_slack(d, g)
        gap = E - E.min()
        rho = s - gap[None, :]                                    # a covers y  iff  rho[a, y] <= eps
        C = rho <= eps + 1e-12
        ncov, nfrac = cg_min_cover(C), cg_frac_cover(C)
        if nfrac > ncov + 1e-7 or ncov > (1 + math.log(C.sum(axis=1).max())) * nfrac + 1e-7:
            return False, dict(reason="N_frac <= N_cov <= (1 + ln max|S|) N_frac fails", ncov=ncov, nfrac=nfrac)
        forced = [y for y in range(n) if not any(C[a, y] for a in range(n) if a != y)]
        if len(forced) > nfrac + 1e-7:
            return False, dict(reason="more forced points than the fractional cover number")
        P = []                                                    # greedy fooling set
        for y in rng.permutation(n):
            if all(not np.any(C[:, y] & C[:, z]) for z in P):
                P.append(int(y))
        if len(P) > nfrac + 1e-7:
            return False, dict(reason="fooling set larger than the fractional cover number")
        M = np.array([max(C[a].sum() for a in range(n) if C[a, y]) for y in range(n)])
        if float(np.sum(1.0 / M)) > nfrac + 1e-7:
            return False, dict(reason="volume bound exceeds the fractional cover number")
        for _ in range(20):
            t = float(rng.uniform(0, 20))
            v = rng.dirichlet(np.ones(n) * rng.uniform(0.2, 2.0))
            bound = math.exp(-t * eps) * float(v.sum()) / float(np.max(np.exp(-t * rho) @ v))
            part = math.exp(-t * eps) * float(np.sum(np.exp(-t * gap))) / float(np.max(np.sum(np.exp(-t * s), axis=1)))
            if bound > nfrac + 1e-7 or part > nfrac + 1e-7:
                return False, dict(reason="exponential-weights / partition bound exceeds N_frac", bound=bound, part=part,
                                   nfrac=nfrac)
            best = max(best, bound / nfrac, part / nfrac)
        order = np.argsort(E)                                     # adversarial weights: uniform on the lowest states
        for m_low in range(2, min(n, 5) + 1):
            v = np.zeros(n)
            v[order[:m_low]] = 1.0 / m_low
            for t in (0.5, 2.0, 8.0, 30.0):
                bound = math.exp(-t * eps) / float(np.max(np.exp(-t * rho) @ v))
                if bound > nfrac + 1e-7:
                    return False, dict(reason="exponential-weights bound (low-state weights) exceeds N_frac",
                                       bound=bound, nfrac=nfrac)
                best = max(best, bound / nfrac)
    return True, dict(best_bound_over_Nfrac=best)


@conjecture("XI.3 Product landscapes: one evaluation is an exact certificate iff every site is sharp (c_i <= white-box excitation energies); N_frac >= exp(sum_i r_i - t eps) for all t and all product weights")
def t_product_rate(rng, trials):
    seen = dict(sharp=0, nonsharp=0)
    for it in range(max(4, trials // 2)):
        n = int(rng.integers(2, 5))
        k = int(rng.integers(2, 4)) if n <= 3 else 2
        configs = all_configs(n, k)
        arr = np.array(configs)
        c = rng.uniform(0.2, 1.2, size=n)
        kappa = float(rng.choice([0.0, 0.5]))
        gs = kappa * c[:, None] * rng.uniform(-0.5, 0.5, size=(n, k))             # additive residual, kappa-Lipschitz
        if it % 3 == 0:       # sharp regime: every excitation of the known part costs more than the envelope constant
            phi = c[:, None] * rng.uniform(1.6, 3.0, size=(n, k))
            phi[:, 0] = 0.0
        elif it % 3 == 1:     # borderline regime: excitations within 40% of the envelope constants
            phi = c[:, None] * rng.uniform(0.6, 1.4, size=(n, k))
            phi[:, 0] = 0.0
        else:                 # generic regime (some site is not sharp with overwhelming probability)
            phi = rng.uniform(0.0, 1.0, size=(n, k))
        Es = phi + gs
        ground = Es.argmin(axis=1)
        f = phi[np.arange(n)[None, :], arr].sum(axis=1)
        g = gs[np.arange(n)[None, :], arr].sum(axis=1)
        d = (c[None, None, :] * (arr[:, None, :] != arr[None, :, :])).sum(axis=2)
        E = f + g
        s = cg_slack(d, g)
        gap = E - E.min()
        x0 = int(np.argmin(E))
        lb, _, ubpt, _, _ = cg_bounds(d, f, g, [x0])
        single = ubpt - lb <= 1e-10
        sharp = all(c[i] <= phi[i, a] - phi[i, ground[i]] + 1e-10 for i in range(n) for a in range(k) if a != ground[i])
        if single != sharp:
            return False, dict(reason="single evaluation certifies <=> all sites sharp fails", single=single, sharp=sharp)
        seen["sharp" if sharp else "nonsharp"] += 1
        eps = float(rng.choice([0.0, 0.05]))
        C = s <= gap[None, :] + eps + 1e-12
        nfrac = cg_frac_cover(C)
        if sharp and eps == 0.0 and abs(nfrac - 1.0) > 1e-7:
            return False, dict(reason="sharp landscape with N_frac != 1")
        rho_site = [c[i] * (1 - np.eye(k)) - gs[i][:, None] + gs[i][None, :] - (Es[i] - Es[i].min())[None, :] for i in range(n)]
        for _ in range(15):
            t = float(rng.uniform(0, 12))
            boltz = rng.random() < 0.4
            logb = -t * eps
            for i in range(n):
                v = np.exp(-t * (Es[i] - Es[i].min())) if boltz else rng.dirichlet(np.ones(k))
                logb += math.log(float(v.sum())) - math.log(float(np.max(np.exp(-t * rho_site[i]) @ v)))
            if math.exp(logb) > nfrac + 1e-7:
                return False, dict(reason="product exponential-weights bound exceeds N_frac", bound=math.exp(logb), nfrac=nfrac)
    if seen["sharp"] == 0 or seen["nonsharp"] == 0:
        return False, dict(reason="test did not see both regimes", **seen)
    return True, seen


def cg_best_first(d, f, g, eps, first):
    """Piyavskii-Shubert / optimistic search: evaluate a minimiser of the certified lower bound until certified."""
    A = [first]
    while True:
        lb, _, ubpt, L, _ = cg_bounds(d, f, g, A)
        if ubpt - lb <= eps + 1e-12:
            return A
        y = int(np.argmin(f + L))
        if y in A:
            raise RuntimeError("best-first search re-evaluated a point")
        A.append(y)


@conjecture("XI.4 Best-first search: separation properties (a)-(c) and resource augmentation m <= |C| + 1 for every cover C with radii theta (gap + eps/6), theta = (1-kappa)/(4(1+kappa))")
def t_best_first(rng, trials):
    attained = 0
    for it in range(2 * trials):
        if it % 8 == 7:       # adversarial family: a far minimiser, a hub of huge energy next to shallow leaves
            leaves = int(rng.integers(3, 9))
            n = leaves + 2
            d = np.full((n, n), 2.0)
            d[0, :] = d[:, 0] = float(rng.uniform(4.0, 12.0))
            d[1, 2:] = d[2:, 1] = 1.0
            np.fill_diagonal(d, 0.0)
            kappa = 0.0
            g = np.zeros(n)
            f = np.full(n, float(rng.uniform(1.1, 1.9)))
            f[0], f[1] = 0.0, 100.0
        else:
            n = int(rng.integers(5, 13))
            d = cg_metric(rng, n, asym=False)
            kappa = float(rng.choice([0.0, 0.2, 0.5, 0.8]))
            g = cg_lipschitz(rng, d, kappa)
            f = rng.normal(0, 1.0, size=n) * float(rng.choice([0.2, 1.0, 3.0]))
        E = f + g
        gap = E - E.min()
        s = cg_slack(d, g)
        eps = float(rng.choice([0.05, 0.2, 0.5]))
        A = cg_best_first(d, f, g, eps, int(rng.integers(n)))
        m = len(A)
        for kk in range(1, m):
            for jj in range(kk):
                if not gap[A[kk]] - gap[A[jj]] + eps < s[A[jj], A[kk]] + 1e-9:
                    return False, dict(reason="separation (a) fails")
                if not gap[A[kk]] <= s[A[jj], A[kk]] + 1e-9:
                    return False, dict(reason="separation (b) fails")
                if jj >= 1 and not gap[A[jj]] - gap[A[kk]] <= s[A[kk], A[jj]] + 1e-9:
                    return False, dict(reason="separation (c) fails")
        theta = (1 - kappa) / (4 * (1 + kappa))
        nshr = cg_min_cover(s <= theta * (gap[None, :] + eps / 6) + 1e-12)
        if m > nshr + 1:
            return False, dict(reason="resource augmentation bound violated", m=m, shrunk_cover=nshr, kappa=kappa, eps=eps)
        attained += m == nshr + 1
    return True, dict(bound_attained=attained)


@conjecture("XI.5 Hardness: on the domination instance (f = 1 on V, 0 at a far point; graph metric truncated at 2; zero residual) the minimal exact certificate has 1 + gamma(G) evaluations")
def t_domination(rng, trials):
    for _ in range(max(1, trials // 2)):
        nv = int(rng.integers(3, 8))
        p = float(rng.uniform(0.2, 0.7))
        adj = np.triu(rng.random((nv, nv)) < p, 1)
        adj = adj | adj.T
        n = nv + 1
        d = np.full((n, n), 2.0)
        d[:nv, :nv][adj] = 1.0
        np.fill_diagonal(d, 0.0)
        f = np.ones(n)
        f[nv] = 0.0
        g = np.zeros(n)
        gamma = None
        for size in range(1, nv + 1):
            for S in itertools.combinations(range(nv), size):
                dom = np.zeros(nv, dtype=bool)
                for v in S:
                    dom[v] = True
                    dom |= adj[v]
                if dom.all():
                    gamma = size
                    break
            if gamma:
                break
        nstar = None
        for size in range(1, n + 1):
            for A in itertools.combinations(range(n), size):
                lb, _, ubpt, _, _ = cg_bounds(d, f, g, A)
                if ubpt - lb <= 1e-12:
                    nstar = size
                    break
            if nstar:
                break
        if nstar != gamma + 1:
            return False, dict(reason="minimal certificate != 1 + domination number", nstar=nstar, gamma=gamma)
    return True, {}


@conjecture("XI.6 Conditional envelope: sup of g'(x) - g'(y) over residuals consistent with the evaluations is min(d(x,y), U(x) - L(y)) (LP); max-regret formula; configuration and point certificates differ by at most one evaluation")
def t_conditional_envelope(rng, trials):
    from scipy.optimize import linprog
    stats = dict(conf_lt_point=0, instances=0)
    for _ in range(max(1, trials // 3)):
        n, d, kappa, f, g, eps = cg_instance(rng, nmax=6, kappas=(0.0, 0.5, 1.0))
        E = f + g
        size = int(rng.integers(1, n))
        A = sorted(rng.choice(n, size=size, replace=False).tolist())
        _, _, _, L, U = cg_bounds(d, f, g, A)
        D = np.minimum(d, U[:, None] - L[None, :])               # conditional envelope D_A(x, y)
        np.fill_diagonal(D, 0.0)
        # LP: maximise g'(x) - g'(y) over the admissible class with g' = g on A
        rows, rhs = [], []
        for x in range(n):
            for y in range(n):
                if x != y:
                    r = np.zeros(n)
                    r[x], r[y] = 1, -1
                    rows.append(r)
                    rhs.append(d[x, y])
        Aeq = np.zeros((len(A), n))
        for r_, a in enumerate(A):
            Aeq[r_, a] = 1
        for x in range(n):
            for y in range(n):
                if x == y:
                    continue
                obj = np.zeros(n)
                obj[x], obj[y] = -1, 1
                res = linprog(obj, A_ub=np.array(rows), b_ub=np.array(rhs), A_eq=Aeq, b_eq=g[A], bounds=(None, None),
                              method="highs")
                if res.status != 0 or abs(-res.fun - D[x, y]) > 1e-7:
                    return False, dict(reason="conditional envelope is not the LP optimum", lp=-res.fun, formula=D[x, y])
        if not np.all(D[:, None, :] <= D[:, :, None] + D[None, :, :] + 1e-9):
            return False, dict(reason="conditional envelope violates the triangle inequality")
        # configuration certificates: x is eps-optimal for every consistent residual  <=>  max regret <= eps
        s = cg_slack(d, g)
        nconf = npoint = None
        for sz in range(0, n + 1):
            for B in itertools.combinations(range(n), sz):
                B = list(B)
                if B:
                    lb, _, ubpt, LB_, UB_ = cg_bounds(d, f, g, B)
                    DB = np.minimum(d, UB_[:, None] - LB_[None, :])
                    np.fill_diagonal(DB, 0.0)
                    is_point = ubpt - lb <= eps + 1e-12
                else:
                    DB, is_point = d, False
                regret = np.max(DB + f[:, None] - f[None, :], axis=1)        # max regret of each candidate x
                is_conf = bool(np.min(regret) <= eps + 1e-12)
                if is_point and not is_conf:
                    return False, dict(reason="a point certificate is not a configuration certificate")
                if is_conf:
                    xhat = int(np.argmin(regret))
                    lb2, _, ubpt2, _, _ = cg_bounds(d, f, g, sorted(set(B) | {xhat}))
                    if ubpt2 - lb2 > eps + 1e-9:
                        return False, dict(reason="configuration certificate + its candidate is not a point certificate")
                if nconf is None and is_conf:
                    nconf = sz
                if npoint is None and is_point:
                    npoint = sz
            if npoint is not None:
                break
        if not (nconf <= npoint <= nconf + 1):
            return False, dict(reason="N_conf <= N_point <= N_conf + 1 fails", nconf=nconf, npoint=npoint)
        stats["conf_lt_point"] += nconf < npoint
        stats["instances"] += 1
    return True, stats


@conjecture("XI.7 Thermal contact: over the admissible class the Gibbs probability of x ranges exactly over [1/sum_y e^{-b(f(y)-f(x)-d(x,y))}, 1/sum_y e^{-b(f(y)-f(x)+d(y,x))}] (ends attained; vertex check)")
def t_thermal_contact(rng, trials):
    for _ in range(2 * trials):
        n = int(rng.integers(2, 7))
        d = cg_metric(rng, n, asym=rng.random() < 0.5)
        f = rng.normal(0, 1.0, size=n)
        beta = float(rng.choice([0.2, 1.0, 4.0]))
        x = int(rng.integers(n))
        hi = 1.0 / float(np.sum(np.exp(-beta * (f - f[x] + d[:, x]))))
        lo = 1.0 / float(np.sum(np.exp(-beta * (f - f[x] - d[x, :]))))

        def prob(g):
            w = np.exp(-beta * (f + g - (f + g).min()))
            return float(w[x] / w.sum())

        if abs(prob(d[:, x]) - hi) > 1e-9 * hi or abs(prob(-d[x, :]) - lo) > 1e-9 * lo:
            return False, dict(reason="extremal residuals d(.,x), -d(x,.) do not attain the closed forms")
        for kappa in (0.3, 1.0, 1.0, 1.0):
            p = prob(cg_lipschitz(rng, d, kappa))
            if p > hi * (1 + 1e-9) or p < lo * (1 - 1e-9):
                return False, dict(reason="admissible residual leaves the thermal contact interval", p=p, lo=lo, hi=hi)
        for a in range(n):                                    # tropical vertices d(., a) and -d(a, .)
            for gv in (d[:, a], -d[a, :]):
                p = prob(gv)
                if p > hi * (1 + 1e-9) or p < lo * (1 - 1e-9):
                    return False, dict(reason="a vertex of the class leaves the thermal contact interval")
    return True, {}


@conjecture("XI.8 Free-energy certificates: Z_hi/Z = E_pi e^{b s(A,Y)}, Z_lo/Z = E_pi e^{-b s(Y,A)}; mean-slack, entropy and Hoelder exponential-weights converses hold for every evaluated set")
def t_thermal_certificates(rng, trials):
    best = 0.0
    for _ in range(max(1, trials // 3)):
        n, d, kappa, f, g, _ = cg_instance(rng, nmax=7, kappas=(0.0, 0.3, 0.7))
        beta = float(rng.choice([0.3, 1.0, 3.0]))
        E = f + g
        s = cg_slack(d, g)
        w = np.exp(-beta * (E - E.min()))
        pi = w / w.sum()
        H = float(-np.sum(pi * np.log(pi)))
        params = []
        for _ in range(12):
            p = float(rng.uniform(0.05, 0.95))
            t = beta * (1 - p) / p
            v = rng.dirichlet(np.ones(n) * rng.uniform(0.2, 2.0))
            lhs = float(np.sum(pi ** (1 - p) * v ** p))
            params.append((p, t, v, lhs))
        for size in range(1, n + 1):
            for A in itertools.combinations(range(n), size):
                A = list(A)
                _, _, _, L, U = cg_bounds(d, f, g, A)
                sA = s[A, :].min(axis=0)
                sAt = s[:, A].min(axis=1)
                zhi = float(np.sum(np.exp(-beta * (f + L - E.min()))) / w.sum())
                zlo = float(np.sum(np.exp(-beta * (f + U - E.min()))) / w.sum())
                if abs(zhi - float(np.sum(pi * np.exp(beta * sA)))) > 1e-9 * zhi or \
                        abs(zlo - float(np.sum(pi * np.exp(-beta * sAt)))) > 1e-9:
                    return False, dict(reason="slack forms of the envelope partition functions fail")
                if not (zlo <= 1 + 1e-12 <= zhi + 2e-12):
                    return False, dict(reason="partition bracket fails")
                eps = math.log(zhi)                              # the certificate hypothesis holds with this eps
                if beta * float(np.sum(pi * sA)) > eps + 1e-9:
                    return False, dict(reason="mean-slack bound fails")
                for t in (0.0, 0.5 * beta, beta, 4 * beta):
                    B = float(np.max(np.sum(np.exp(-t * s[A, :]), axis=1)))
                    if H > math.log(size * B) + t * eps / beta + 1e-9:
                        return False, dict(reason="entropy bound fails", H=H, t=t)
                for p, t, v, lhs in params:
                    B = float(np.max(np.exp(-t * s[A, :]) @ v))
                    rhs = (size * B) ** p * math.exp((1 - p) * eps)
                    if lhs > rhs * (1 + 1e-9):
                        return False, dict(reason="Hoelder exponential-weights converse fails", lhs=lhs, rhs=rhs)
                    best = max(best, lhs / rhs)
    return True, dict(best_lhs_over_rhs=best)


def cg_transport(d, nu, mu):
    """W_d(nu, mu) = sup { E_nu g - E_mu g : g(x) - g(y) <= d(x,y) }, with a maximising potential (LP)."""
    from scipy.optimize import linprog
    n = len(d)
    rows, rhs = [], []
    for x in range(n):
        for y in range(n):
            if x != y:
                r = np.zeros(n)
                r[x], r[y] = 1, -1
                rows.append(r)
                rhs.append(d[x, y])
    Aeq = np.zeros((1, n))
    Aeq[0, 0] = 1
    res = linprog(-(nu - mu), A_ub=np.array(rows), b_ub=np.array(rhs), A_eq=Aeq, b_eq=[0.0], bounds=(None, None),
                  method="highs")
    return float(-res.fun), res.x


@conjecture("XI.9 Transport-entropy duality at fixed beta: ln E_mu e^{b(g - E_mu g)} = b(E_nu g - E_mu g) - KL(nu||mu) <= b W_d(nu,mu) - KL(nu||mu) at the tilt nu, and every nu is dominated by its Kantorovich potential")
def t_transport_entropy(rng, trials):
    for _ in range(trials):
        n = int(rng.integers(2, 7))
        d = cg_metric(rng, n, asym=rng.random() < 0.4)
        mu = rng.dirichlet(np.ones(n))
        beta = float(rng.choice([0.3, 1.0, 3.0]))

        def logmgf(g):
            return math.log(float(np.sum(mu * np.exp(beta * (g - np.sum(mu * g))))))

        g = cg_lipschitz(rng, d, 1.0)
        nu = mu * np.exp(beta * g)
        nu /= nu.sum()
        kl = float(np.sum(nu * np.log(nu / mu)))
        W, _ = cg_transport(d, nu, mu)
        lm = logmgf(g)
        if abs(lm - (beta * float(np.sum((nu - mu) * g)) - kl)) > 1e-9:
            return False, dict(reason="tilt identity fails")
        if lm > beta * W - kl + 1e-7:
            return False, dict(reason="log-MGF exceeds beta W - KL at the tilted measure", lm=lm, bound=beta * W - kl)
        nu2 = rng.dirichlet(np.ones(n))
        W2, pot = cg_transport(d, nu2, mu)
        if np.any(pot[:, None] - pot[None, :] > d + 1e-7):
            return False, dict(reason="LP potential is not admissible")
        kl2 = float(np.sum(nu2 * np.log(nu2 / mu)))
        if beta * W2 - kl2 > logmgf(pot) + 1e-7:
            return False, dict(reason="Donsker-Varadhan direction fails", lhs=beta * W2 - kl2, rhs=logmgf(pot))
    return True, {}


def so_mixed_diff(g, x, T, b):
    """Mixed difference of g at the base point x over the coordinates T with target states b[i]."""
    tot = 0.0
    T = list(T)
    for r in range(len(T) + 1):
        for U in itertools.combinations(T, r):
            y = list(x)
            for i in U:
                y[i] = b[i]
            tot += (-1) ** (len(T) - r) * g[tuple(y)]
    return tot


def so_constants(g, n, k, m):
    """Smallest c_T bounding all m-th order mixed differences over T."""
    confs = all_configs(n, k)
    c = {}
    for T in itertools.combinations(range(n), m):
        best = 0.0
        for x in confs:
            for bt in itertools.product(range(k), repeat=m):
                best = max(best, abs(so_mixed_diff(g, x, T, dict(zip(T, bt)))))
        c[T] = best
    return c


def so_interpolant(g, n, k, m, x0):
    """Anchored (cut-HDMR) interpolant of order m - 1 at x0: uses g only on the Hamming ball of radius m - 1."""
    out = {}
    for y in all_configs(n, k):
        S = [i for i in range(n) if y[i] != x0[i]]
        out[y] = sum(so_mixed_diff(g, x0, T, {i: y[i] for i in T})
                     for r in range(0, min(m - 1, len(S)) + 1) for T in itertools.combinations(S, r))
    return out


def so_random_function(rng, n, k, scales):
    confs = all_configs(n, k)
    g = {y: 0.0 for y in confs}
    for order, scale in scales:
        for T in itertools.combinations(range(n), min(order, n)):
            table = rng.normal(0, scale, size=(k,) * len(T))
            for y in confs:
                g[y] += float(table[tuple(y[i] for i in T)])
    return g


@conjecture("XI.10 Order-m anchored remainder (m = 2, 3): |g - I_{m-1} g| <= sum of c_T over the m-subsets T of the changed sites; the extremal function I_{m-1} g - remainder stays in the class with the same ball data")
def t_anchored_remainder(rng, trials):
    worst = 0.0
    for _ in range(max(2, trials // 6)):
        n = int(rng.integers(3, 5))
        k = int(rng.integers(2, 4)) if n == 3 else 2
        m = int(rng.integers(2, 4))
        confs = all_configs(n, k)
        g = so_random_function(rng, n, k, ((1, 1.0), (2, 0.5), (3, 0.3), (n, 0.05)))
        x0 = tuple(int(v) for v in rng.integers(0, k, size=n))
        c = so_constants(g, n, k, m)
        interp = so_interpolant(g, n, k, m, x0)
        h = {}
        for y in confs:
            S = [i for i in range(n) if y[i] != x0[i]]
            rem = sum(c[T] for T in itertools.combinations(S, m))
            err = abs(g[y] - interp[y])
            if err > rem + 1e-9:
                return False, dict(reason="anchored remainder bound violated", m=m, err=err, rem=rem)
            if rem > 0:
                worst = max(worst, err / rem)
            h[y] = interp[y] - rem
        ch = so_constants(h, n, k, m)
        if any(ch[T] > c[T] + 1e-9 for T in c):
            return False, dict(reason="extremal extension leaves the class")
        if any(abs(h[y] - g[y]) > 1e-9 for y in confs if sum(a != b for a, b in zip(y, x0)) < m):
            return False, dict(reason="extremal extension changes the ball data")
    return True, dict(max_err_over_remainder=worst)


@conjecture("XI.11 Second-order envelopes: the star sandwich is the exact envelope (LP over the whole class with star data); x0 is certified for every consistent residual iff it minimises its own lower pairwise model")
def t_star_exact(rng, trials):
    from scipy.optimize import linprog
    seen = dict(certified=0, not_certified=0)
    for _ in range(max(2, trials // 6)):
        n, k = (3, 2) if rng.random() < 0.6 else (3, 3)
        confs = all_configs(n, k)
        idx = {y: j for j, y in enumerate(confs)}
        N = len(confs)
        g = so_random_function(rng, n, k, ((1, 1.0), (2, 0.3), (3, 0.15)))
        f = so_random_function(rng, n, k, ((1, 1.0), (2, 0.4)))
        c = so_constants(g, n, k, 2)
        x0 = min(confs, key=lambda y: f[y] + g[y])
        rows, rhs = [], []
        for (i, j) in itertools.combinations(range(n), 2):
            for x in confs:
                for a in range(k):
                    for b in range(k):
                        if a == x[i] or b == x[j]:
                            continue
                        row = np.zeros(N)
                        for (ua, ub, sgn) in ((1, 1, 1), (1, 0, -1), (0, 1, -1), (0, 0, 1)):
                            y = list(x)
                            if ua:
                                y[i] = a
                            if ub:
                                y[j] = b
                            row[idx[tuple(y)]] += sgn
                        rows += [row, -row]
                        rhs += [c[(i, j)], c[(i, j)]]
        star = [y for y in confs if sum(a != b for a, b in zip(y, x0)) <= 1]
        Aeq = np.zeros((len(star), N))
        for r_, y in enumerate(star):
            Aeq[r_, idx[y]] = 1
        beq = np.array([g[y] for y in star])
        interp = so_interpolant(g, n, k, 2, x0)
        lower = {}
        for y in confs:
            S = [i for i in range(n) if y[i] != x0[i]]
            rem = sum(c[T] for T in itertools.combinations(S, 2))
            lower[y] = interp[y] - rem
            for sign in (1, -1):
                obj = np.zeros(N)
                obj[idx[y]] = sign
                res = linprog(obj, A_ub=np.array(rows), b_ub=np.array(rhs), A_eq=Aeq, b_eq=beq, bounds=(None, None),
                              method="highs")
                if res.status != 0 or abs(sign * res.fun - (interp[y] - sign * rem)) > 1e-7:
                    return False, dict(reason="star envelope is not the LP optimum", lp=sign * res.fun,
                                       formula=interp[y] - sign * rem)
        # certified minimiser:  x0 minimises f + lower  <=>  x0 minimises f + g' for every consistent g' in the class
        own = all(f[y] + lower[y] >= f[x0] + g[x0] - 1e-10 for y in confs)
        robust = True
        for y in confs:                                           # LP: can some consistent g' make y strictly better?
            obj = np.zeros(N)
            obj[idx[y]] = 1
            res = linprog(obj, A_ub=np.array(rows), b_ub=np.array(rhs), A_eq=Aeq, b_eq=beq, bounds=(None, None),
                          method="highs")
            if f[y] + res.fun < f[x0] + g[x0] - 1e-8:
                robust = False
        if own != robust:
            return False, dict(reason="certified-minimiser criterion fails", own=own, robust=robust)
        seen["certified" if own else "not_certified"] += 1
    return True, seen


def zk_weight(w, W, x):
    n = len(w)
    val = 1.0
    for i in range(n):
        val *= w[i][x[i]]
        for j in range(n):
            if j != i:
                val *= W[i][j][x[i], x[j]]
    return val


def zk_Z(w, W, n, k):
    return sum(zk_weight(w, W, x) for x in all_configs(n, k))


@conjecture("XI.12 Partition-function rules: cut bracket Lam Z_S Z_Sc <= Z <= Ups Z_S Z_Sc with the products of cut-factor bounds; eliminating a site with at most two neighbours into one-body / pair factors preserves Z")
def t_partition_rules(rng, trials):
    for _ in range(max(2, trials // 2)):
        n = int(rng.integers(3, 6))
        k = int(rng.integers(2, 4)) if n <= 4 else 2
        w = [rng.uniform(0.2, 2.0, size=k) for _ in range(n)]
        # chain with optional next-nearest neighbour factors; all other pair factors are 1
        W = [[np.ones((k, k)) for _ in range(n)] for _ in range(n)]
        for i in range(n - 1):
            W[i][i + 1] = rng.uniform(0.3, 1.5, size=(k, k))
            if rng.random() < 0.5:
                W[i + 1][i] = rng.uniform(0.3, 1.5, size=(k, k))
        Z = zk_Z(w, W, n, k)
        # --- cut rule
        S = [i for i in range(n) if rng.random() < 0.5] or [0]
        if len(S) == n:
            S = S[:-1]
        Sc = [i for i in range(n) if i not in S]

        def restricted(part):
            w2 = [w[i] if i in part else np.ones(k) for i in range(n)]
            W2 = [[W[i][j] if (i in part and j in part) else np.ones((k, k)) for j in range(n)] for i in range(n)]
            return zk_Z(w2, W2, n, k) / k ** (n - len(part))       # pinned sites contribute one state each
        lam = ups = 1.0
        for i in range(n):
            for j in range(n):
                if i != j and ((i in S) != (j in S)):
                    lam *= W[i][j].min()
                    ups *= W[i][j].max()
        zs, zc = restricted(S), restricted(Sc)
        if not (lam * zs * zc <= Z * (1 + 1e-9) and Z <= ups * zs * zc * (1 + 1e-9)):
            return False, dict(reason="cut bracket fails", lo=lam * zs * zc, Z=Z, hi=ups * zs * zc)
        # --- elimination of an end site (one neighbour) and of an interior site (two neighbours)
        for site in (0, n // 2):
            nb = [j for j in range(n) if j != site and (not np.all(W[site][j] == 1) or not np.all(W[j][site] == 1))]
            if not 1 <= len(nb) <= 2:
                continue
            w2 = [v.copy() for v in w]
            W2 = [[M.copy() for M in row] for row in W]
            if len(nb) == 1:
                j = nb[0]
                T = np.array([sum(w[site][a] * W[site][j][a, b] * W[j][site][b, a] for a in range(k)) for b in range(k)])
                w2[j] = w2[j] * T
            else:
                j, l = nb
                T = np.array([[sum(w[site][a] * W[site][j][a, b] * W[j][site][b, a] * W[site][l][a, c_] * W[l][site][c_, a]
                                   for a in range(k)) for c_ in range(k)] for b in range(k)])
                W2[j][l] = W2[j][l] * T
            w2[site] = np.ones(k)
            for j in range(n):
                W2[site][j] = np.ones((k, k))
                W2[j][site] = np.ones((k, k))
            Z2 = zk_Z(w2, W2, n, k) / k                              # the eliminated site is pinned to one state
            if abs(Z2 - Z) > 1e-9 * Z:
                return False, dict(reason="elimination changes Z", Z=Z, Z2=Z2, neighbours=len(nb))
    return True, {}


@conjecture("XI.13 Sampled free-energy sandwich: for N independent samples of a product reference, P(|empirical mean - mean| >= eta) <= 2 exp(-2 N eta^2 / sum c_i^2), and the sampled interval misses ln(Z/Z0) with at most that probability (exact enumeration of sample tuples)")
def t_sampled_sandwich(rng, trials):
    worst = 0.0
    for _ in range(max(2, trials // 6)):
        n = int(rng.integers(1, 4))
        k = 2
        N = int(rng.integers(1, 4 if n <= 2 else 3))
        configs = all_configs(n, k)
        p = [rng.dirichlet(np.ones(k) * rng.uniform(0.3, 3.0)) for _ in range(n)]
        W = np.array([math.prod(p[i][x[i]] for i in range(n)) for x in configs])
        # residual: additive part plus a small generic part; exact bounded-difference constants
        g = {x: float(sum(rng.normal(0, 1.0, size=(n, k))[i, x[i]] for i in range(n))) for x in configs}
        for x in configs:
            g[x] += 0.3 * float(rng.normal())
        c = np.array([max(abs(g[x] - g[x[:i] + (a,) + x[i + 1:]]) for x in configs for a in range(k)) for i in range(n)])
        C = float(np.sum(c ** 2))
        if C == 0:
            continue
        gv = np.array([g[x] for x in configs])
        m = float(W @ gv)
        beta = float(rng.uniform(-3.0, 3.0))
        L = math.log(float(W @ np.exp(-beta * gv)))
        if not (-beta * m - 1e-9 <= L <= -beta * m + beta ** 2 * C / 8 + 1e-9):
            return False, dict(reason="exact sandwich fails (generator or III.2)")
        etas = [float(rng.uniform(0.05, 1.5) * math.sqrt(C)) for _ in range(4)]
        dev = np.zeros(len(etas))
        bad = np.zeros(len(etas))
        total = 0.0
        for omega in itertools.product(range(len(configs)), repeat=N):
            pw = math.prod(W[j] for j in omega)
            mh = sum(gv[j] for j in omega) / N
            total += pw
            for e_, eta in enumerate(etas):
                if abs(mh - m) >= eta:
                    dev[e_] += pw
                if not (-beta * mh - abs(beta) * eta <= L <= -beta * mh + abs(beta) * eta + beta ** 2 * C / 8):
                    bad[e_] += pw
        if abs(total - 1.0) > 1e-9:
            return False, dict(reason="sample weights do not sum to one")
        for e_, eta in enumerate(etas):
            bound = 2 * math.exp(-2 * N * eta ** 2 / C)
            if dev[e_] > bound + 1e-12 or bad[e_] > bound + 1e-12:
                return False, dict(reason="sampled sandwich violated", deviation=float(dev[e_]), miss=float(bad[e_]),
                                   bound=bound, N=N, n=n)
            worst = max(worst, dev[e_] / bound)
    return True, dict(max_prob_over_bound=worst)


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


@conjecture("DEAD.4 Trace-enhanced bound is attained on EVERY vertex-transitive input", expect_fail=True)
def t_dead_vertex_transitive(rng, trials):
    # regular simplex on L = 5 points, target dimension r = 3: bound L(L-1-r)/(r+1) = 1.25,
    # but the top-3 eigenspace is not invariant under the symmetry group and the optimum is ~1.3043
    L, r = 5, 3
    Dhat = np.ones((L, L)) - np.eye(L)
    lb, _ = trace_bound_sq(Dhat, r)
    best = sstress_min(Dhat, r, rng, restarts=40)
    if best > lb * (1 + 1e-3):
        return False, dict(reason="bound is strict on the regular simplex L=5, r=3", bound=float(lb), optimum=float(best))
    return True, {}


@conjecture("DEAD.5 Bounded-difference (McDiarmid) free-energy sandwich holds for correlated (non-product) references", expect_fail=True)
def t_dead_mcdiarmid_correlated(rng, trials):
    """Refuted claim: ln E_mu[exp(beta (g - E_mu g))] <= beta^2 sum_i c_i^2 / 8 for EVERY reference mu on a
    product space (c_i = exact single-site bounded differences of g).  It needs independence (III.2); for
    correlated references only the full-range form with (sum_i c_i)^2 survives (III.6)."""
    for it in range(5 * trials):
        n, k = int(rng.integers(2, 5)), int(rng.integers(2, 4))
        configs, w, kind = correlated_reference(rng, n, k, kinds=("gibbs", "markov"))
        g, c = random_bd_function(rng, configs, n, k)
        beta = float(rng.uniform(0.05, 4.0))
        rhs = beta ** 2 * float(np.sum(c ** 2)) / 8
        lhs = log_mgf_centered(w, g, beta)
        if rhs > 0 and lhs > rhs * (1 + 1e-9):
            return False, dict(reason="random correlated reference violates the bounded-difference bound", ratio=lhs / rhs,
                               lhs=lhs, rhs=rhs, n=n, k=k, beta=beta, reference=kind, found_at_trial=it + 1)
    # explicit counterexample: two perfectly correlated binary sites, mu uniform on {00, 11}, g = x_1 + x_2
    configs = all_configs(2, 2)
    w = np.array([0.5, 0.0, 0.0, 0.5])
    gd = {x: float(x[0] + x[1]) for x in configs}
    c = bd_constants(gd, configs, 2, 2)
    lhs = log_mgf_centered(w, np.array([gd[x] for x in configs]), 1.0)       # = ln cosh(1) ~ 0.4338
    rhs = float(np.sum(c ** 2)) / 8                                          # = 0.25
    if lhs > rhs * (1 + 1e-9):
        return False, dict(reason="explicit counterexample (random search found none): mu uniform on {00, 11}, g = x1 + x2",
                           ratio=lhs / rhs, lhs=lhs, rhs=rhs, n=2, k=2, beta=1.0)
    return True, {}


@conjecture("DEAD.6 Best-first search needs at most N_cov + 1 evaluations (no radius augmentation)", expect_fail=True)
def t_dead_best_first_optimal(rng, trials):
    """Refuted claim: optimistic (Piyavskii-Shubert) search is within one evaluation of the smallest certificate.
    It is only competitive with covers at shrunk radii (XI.4): a hub that covers many shallow states is never the
    minimiser of the certified lower bound, so the search evaluates the states one by one."""
    for it in range(trials):
        n = int(rng.integers(5, 11))
        d = cg_metric(rng, n, asym=False)
        kappa = float(rng.choice([0.0, 0.2, 0.5]))
        g = cg_lipschitz(rng, d, kappa)
        f = rng.normal(0, 1.0, size=n) * float(rng.choice([0.2, 1.0, 3.0]))
        E = f + g
        eps = float(rng.choice([0.05, 0.2, 0.5]))
        s = cg_slack(d, g)
        ncov = cg_min_cover(s <= (E - E.min())[None, :] + eps + 1e-12)
        m = len(cg_best_first(d, f, g, eps, int(rng.integers(n))))
        if m > ncov + 1:
            return False, dict(reason="random instance: best-first exceeds N_cov + 1", evaluations=m, N_cov=ncov,
                               found_at_trial=it + 1)
    # explicit family: minimiser far away, one hub of huge energy at distance 1 from N leaves (mutual distance 2)
    N, far = 8, 10.0
    n = N + 2
    d = np.full((n, n), 2.0)
    d[0, :] = d[:, 0] = far
    d[1, 2:] = d[2:, 1] = 1.0
    np.fill_diagonal(d, 0.0)
    f = np.full(n, 1.5)
    f[0], f[1] = 0.0, 100.0
    g = np.zeros(n)
    ncov = cg_min_cover(cg_slack(d, g) <= (f - f.min())[None, :] + 0.1 + 1e-12)
    m = len(cg_best_first(d, f, g, 0.1, 0))
    if m > ncov + 1:
        return False, dict(reason="hub instance: best-first evaluates every leaf", evaluations=m, N_cov=ncov)
    return True, {}


@conjecture("DEAD.7 Every certificate of an eps-optimal configuration evaluates every state of the energy shell gap < (1-kappa) sigma - eps", expect_fail=True)
def t_dead_shell_gloss(rng, trials):
    """Refuted gloss of the witness-size bound (II.4 is the true statement, for certificates whose incumbent is an
    evaluated point).  A configuration certificate (every residual consistent with the evaluations makes xhat
    eps-optimal) may miss shell states: states separated from xhat by the white-box part alone cost nothing."""
    for it in range(trials):
        n, d, kappa, f, g, eps = cg_instance(rng, nmax=6, kappas=(0.0, 0.5))
        E = f + g
        gap = E - E.min()
        for size in range(1, n):
            for B in itertools.combinations(range(n), size):
                B = list(B)
                _, _, _, L, U = cg_bounds(d, f, g, B)
                DB = np.minimum(d, U[:, None] - L[None, :])
                np.fill_diagonal(DB, 0.0)
                regret = np.max(DB + f[:, None] - f[None, :], axis=1)
                if np.min(regret) > eps + 1e-12:
                    continue                                       # not a configuration certificate
                for y in range(n):
                    if y in B:
                        continue
                    sigma = min(d[a, y] for a in B)
                    if gap[y] < (1 - kappa) * sigma - eps - 1e-9:
                        return False, dict(reason="configuration certificate misses a shell state", evaluated=len(B),
                                           gap=float(gap[y]), threshold=float((1 - kappa) * sigma - eps),
                                           found_at_trial=it + 1)
    return True, {}


@conjecture("DEAD.8 The transport-entropy (T1) constant is determined at a single inverse temperature: sup_g 2 ln E e^{b(g-Eg)} / b^2 does not depend on b", expect_fail=True)
def t_dead_T1_single_beta(rng, trials):
    """Refuted reading of the Bobkov-Goetze equivalence: it needs the bound for ALL beta.  Two-point space, discrete
    metric, mu = Bernoulli(0.02): the T1 constant is 1/(2 phi(p)), phi(p) = ln((1-p)/p)/(1-2p), while at fixed beta the
    best sub-Gaussian constant is strictly smaller."""
    p = 0.02
    C = (1 - 2 * p) / (2 * math.log((1 - p) / p))

    def K(beta):                                                   # best constant at this beta (g = +-1[x = 1])
        vals = []
        for sgn in (1.0, -1.0):
            lm = math.log((1 - p) * math.exp(-beta * sgn * p) + p * math.exp(beta * sgn * (1 - p)))
            vals.append(2 * lm / beta ** 2)
        return max(vals)

    qs = np.linspace(1e-4, 1 - 1e-4, 40001)
    qs = qs[np.abs(qs - p) > 1e-6]
    t1 = float(np.max((qs - p) ** 2 / (2 * (qs * np.log(qs / p) + (1 - qs) * np.log((1 - qs) / (1 - p))))))
    grid = [K(b) for b in np.linspace(0.05, 60, 2400)]
    if abs(t1 - C) > 1e-4 or max(grid) > C * (1 + 1e-9) or max(grid) < C * (1 - 1e-3):
        raise RuntimeError("sanity: T1 constant of the Bernoulli measure is not 1/(2 phi(p))")
    if K(1.0) < C * (1 - 1e-6):
        return False, dict(reason="fixed-beta constant is smaller than the T1 constant", T1_constant=C, K_beta_0_1=K(0.1),
                           K_beta_1=K(1.0), K_beta_30=K(30.0))
    return True, {}


@conjecture("DEAD.9 For every reference (also dependent ones) the largest Jensen gap ln E e^{b(g-Eg)} over the bounded-difference class is attained by an additive two-level residual", expect_fail=True)
def t_dead_additive_extremal_dependent(rng, trials):
    """Refuted extension of III.3 (which needs a PRODUCT reference).  Two ternary sites, c = (1, 1), beta = 2, with the
    correlated law below (every two-site law is a Markov chain): a non-additive admissible residual has a strictly
    larger gap than every additive one (the best additive residual is two-level, by convexity).  Found by the
    literature check L6 (T3) and re-verified here by enumeration of all {0,1,2}-valued admissible functions."""
    beta = 2.0
    law = np.array([[0.0112, 0.4674, 0.0278], [0.0782, 0.0002, 0.0909], [0.1403, 0.0296, 0.1544]])

    def gap(mu, g):
        return math.log(float(np.sum(mu * np.exp(beta * (g - np.sum(mu * g))))))

    def admissible(g):
        return all(abs(g[a, j] - g[b, j]) <= 1 + 1e-12 and abs(g[j, a] - g[j, b]) <= 1 + 1e-12
                   for a in range(3) for b in range(3) for j in range(3))

    def best_additive(mu):
        return max(gap(mu, s1 * np.array(A1, dtype=float)[:, None] + s2 * np.array(A2, dtype=float)[None, :])
                   for A1 in itertools.product([0, 1], repeat=3) for A2 in itertools.product([0, 1], repeat=3)
                   for s1 in (1, -1) for s2 in (1, -1))

    def best_integer(mu):
        best = -1.0
        for vals in itertools.product([0, 1, 2], repeat=9):
            g = np.array(vals, dtype=float).reshape(3, 3)
            if admissible(g):
                best = max(best, gap(mu, g))
        return best

    mu = law                                                      # the dependent reference under test
    add, full = best_additive(mu), best_integer(mu)
    g_star = np.array([[1, 0, 1], [1, 1, 2], [2, 1, 2]], dtype=float)
    if not admissible(g_star):
        raise RuntimeError("sanity: the recorded extremal residual is not admissible")
    if full > add + 1e-6:
        return False, dict(reason="dependent reference: a non-additive residual beats every additive one",
                           best_additive=add, best_overall=full, recorded_residual=gap(mu, g_star))
    return True, dict(best_additive=add, best_overall=full)


# ----------------------------------------------------------------------------------------------
# Cluster XII — query complexity of every algorithm (cycle 8): dips, sensitive blocks, deterministic
# and randomised lower bounds, spot-checking; refutations found by the second referee (DEAD.10-13)
# ----------------------------------------------------------------------------------------------

def qc_dip(d, g, y, c):
    """The residual g with a dip of depth c at y: a -> min(g(a), g(y) - c + d(a, y))."""
    return np.minimum(g, g[y] - c + d[:, y])


def qc_admissible(d, g, tol=1e-9):
    return bool(np.all(g[:, None] - g[None, :] <= d + tol))


def qc_frac_packing(B):
    """Largest total weight w >= 0 with sum_{y : B[a, y]} w(y) <= 1 for every point a (B[a, y]: a detects y)."""
    from scipy.optimize import linprog
    n, m = B.shape
    res = linprog(-np.ones(m), A_ub=B.astype(float), b_ub=np.ones(n), bounds=(0, None), method="highs")
    return float(-res.fun)


def qc_greedy_cover(sees):
    """Greedy set of points a such that every column y has some chosen a with sees[a, y]."""
    n, m = sees.shape
    uncovered, A = set(range(m)), []
    while uncovered:
        a = max(range(n), key=lambda a: sum(1 for y in uncovered if sees[a, y]))
        if not any(sees[a, y] for y in uncovered):
            raise RuntimeError("sanity: some dip is seen from nowhere")
        A.append(a)
        uncovered -= {y for y in uncovered if sees[a, y]}
    return sorted(A)


def qc_lp_rate(rho, t):
    """max over weights v >= 0 of ln(sum v) subject to sum_s v(s) exp(-t rho(a, s)) <= 1 for every a."""
    from scipy.optimize import linprog
    rho = np.asarray(rho, dtype=float)
    A = np.exp(-t * rho)
    col = A.max(axis=0)
    res = linprog(-1.0 / col, A_ub=A / col, b_ub=np.ones(len(rho)), bounds=(0, None), method="highs")
    if res.status != 0 or -res.fun <= 0:
        return float("-inf")
    return math.log(-res.fun)


def qc_site(phi, gam, c):
    """Single site with known part phi, residual gam, discrete envelope constant c: (gap, slack, credit distortion)."""
    phi, gam = np.asarray(phi, dtype=float), np.asarray(gam, dtype=float)
    E = phi + gam
    gap = E - E.min()
    k = len(phi)
    s = c * (1 - np.eye(k)) - gam[:, None] + gam[None, :]
    return gap, s, s - gap[None, :]


def qc_boltzmann_rate(gap, s, t):
    return math.log(float(np.sum(np.exp(-t * gap)))) - math.log(float(np.max(np.sum(np.exp(-t * s), axis=1))))


def qc_cube_erosions(n):
    """For every subset D of the n-cube (bit mask over its 2^n vertices) the sizes of its erosions
    D_t = {x : dist(x, D^c) > t}, t = 0..n (D_0 = D).  Returns (masks, sizes[len(masks), n + 1])."""
    N = 2 ** n
    masks = np.arange(2 ** N, dtype=np.uint64)
    pc = np.array([bin(i).count("1") for i in range(2 ** N)], dtype=np.int64)
    sizes = np.zeros((2 ** N, n + 1), dtype=np.int64)
    cur = masks.copy()
    for t in range(n + 1):
        sizes[:, t] = pc[cur.astype(np.int64)]
        nxt = cur.copy()
        for i in range(n):
            m1 = sum(1 << v for v in range(N) if v >> i & 1)
            m0 = (2 ** N - 1) ^ m1
            sh = np.uint64(1 << i)
            nxt &= ((cur & np.uint64(m0)) << sh) | ((cur & np.uint64(m1)) >> sh)   # bit v <- bit of the neighbour v ^ 2^i
        cur = nxt
    return masks, sizes


def qc_cube_log_excess(n, u):
    """(logex, logball): logex[k] = ln(e^{Delta_k} - 1), Delta_k the effect on ln Z of the dip of depth c(k+1) at the
    zero residual of the uniform n-cube, e^{Delta_k} - 1 = 2^{-n} sum_{j <= k} C(n, j)(e^{u(k+1-j)} - 1); logball[k] =
    ln |B(k)|.  Log domain, so that exponentially small accuracies can be compared."""
    logc = [math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) for j in range(n + 1)]

    def lse(terms):
        m = max(terms)
        return m + math.log(sum(math.exp(t - m) for t in terms))

    def lexpm1(z):
        return z + math.log1p(-math.exp(-z)) if z > 30.0 else math.log(math.expm1(z))

    logex = [lse([logc[j] + lexpm1(u * (k + 1 - j)) for j in range(k + 1)]) - n * math.log(2) for k in range(n + 1)]
    logball = [lse(logc[: k + 1]) for k in range(n + 1)]
    return logex, logball


def qc_cube_kstar(logex, log_target):
    """Least k with ln(e^{Delta_k} - 1) > log_target, i.e. the smallest ball whose dip is sensitive (len(logex) if none)."""
    for k, v in enumerate(logex):
        if v > log_target:
            return k
    return len(logex)


@conjecture("XII.1 Dips: a dip of depth c at y is admissible, differs from g exactly on the open slack ball {a : s(a,y) < c}, lowers the minimum by at least eps' at depth gap(y)+eps', and multiplies Z by E_pi exp(beta (c - s(.,y))_+) >= exp(beta c - softgap(y)), with 0 <= softgap(y) <= -ln pi(y)")
def t_dips(rng, trials):
    stats = dict(dips=0)
    for _ in range(trials):
        n, d, kappa, f, g, eps = cg_instance(rng)
        E = f + g
        Emin = float(E.min())
        gap = E - Emin
        s = cg_slack(d, g)
        beta = float(rng.choice([0.3, 1.0, 3.0]))
        w = np.exp(-beta * (E - Emin))
        Z = float(w.sum())
        pi = w / Z
        for y in range(n):
            soft = math.log(Z) - math.log(float(np.exp(-beta * (E - Emin + s[:, y])).sum()))
            if soft < -1e-9 or soft > -math.log(pi[y]) + 1e-9:
                return False, dict(reason="soft gap outside [0, -ln pi(y)]", soft=soft, bound=-math.log(pi[y]))
            for c in (float(rng.uniform(0.0, 3.0)), float(gap[y] + 0.25)):
                gd = qc_dip(d, g, y, c)
                if not qc_admissible(d, gd):
                    return False, dict(reason="dip is not admissible")
                if np.max(np.abs(gd - (g - np.maximum(0.0, c - s[:, y])))) > 1e-9:
                    return False, dict(reason="dip is not g minus the positive part of c - slack")
                differs = np.abs(gd - g) > 1e-10
                if np.any(differs & (s[:, y] >= c)) or np.any(~differs & (s[:, y] < c - 1e-9)):
                    return False, dict(reason="difference set of the dip is not the open slack ball")
                ratio = float(np.exp(-beta * (f + gd - Emin)).sum()) / Z
                exact = float(np.sum(pi * np.exp(beta * np.maximum(0.0, c - s[:, y]))))
                if abs(ratio - exact) > 1e-9 * max(1.0, exact):
                    return False, dict(reason="partition function of the dip is not E_pi exp(beta (c - s)_+)")
                if math.log(ratio) < beta * c - soft - 1e-9:
                    return False, dict(reason="effect of the dip is below beta c - softgap", effect=math.log(ratio),
                                       bound=beta * c - soft)
                stats["dips"] += 1
            if float((f + qc_dip(d, g, y, gap[y] + 0.25)).min()) > Emin - 0.25 + 1e-9:
                return False, dict(reason="a dip of depth gap + eps' does not lower the minimum by eps'")
    return True, stats


@conjecture("XII.2 Randomised lower bound (minimum): for mixtures of hint-verifying and blind strategies with error probability delta on the instance and on every dip, (1 - 2 delta) * (fractional packing of the open slack balls of radius gap + eps') <= expected number of evaluations; attained on the uniform metric")
def t_randomized_min(rng, trials):
    """The proof of `expected_queries_ge` uses correctness on the instance and on its dips only; delta is computed on
    exactly these residuals (so the inequality tested is the one the proof establishes, and it is stronger than the
    theorem, whose delta is a maximum over the whole class)."""
    stats = dict(nontrivial=0, tight=0)
    for trial in range(trials):
        uniform = trial % 5 == 0
        if uniform:
            n = int(rng.integers(3, 8))
            d, f, g, eps = np.ones((n, n)) - np.eye(n), np.zeros(n), np.zeros(n), 0.2
        else:
            n, d, kappa, f, g, eps = cg_instance(rng)
        E = f + g
        Emin = float(E.min())
        gap = E - Emin
        s = cg_slack(d, g)
        epsp = eps + float(rng.choice([0.05, 0.3]))
        B = s < (gap[None, :] + epsp)                     # the detection relation claimed by the theorem
        pack = qc_frac_packing(B)
        dips = [qc_dip(d, g, y, gap[y] + epsp) for y in range(n)]
        sees = np.array([[abs(dips[y][a] - g[a]) > 1e-10 for y in range(n)] for a in range(n)])   # what a query reveals
        dipmin = np.array([float((f + dips[y]).min()) for y in range(n)])
        strategies = []                                   # (probability, evaluated set or None, blind output)
        if uniform:
            lam = float(rng.uniform(0.1, 0.9))
            strategies = [(lam, list(range(n)), None), ((1 - lam) / 2, None, Emin), ((1 - lam) / 2, None, Emin - epsp)]
        elif trial % 5 in (1, 2):
            strategies = [(1.0, qc_greedy_cover(sees), None)]   # a deterministic algorithm that sees every dip
        else:
            k = int(rng.integers(1, 5))
            wts = rng.dirichlet(np.ones(k + 2))
            for j in range(k):
                if rng.random() < 0.5:
                    A = list(range(n))
                else:
                    A = sorted(rng.choice(n, size=int(rng.integers(1, n + 1)), replace=False).tolist())
                strategies.append((float(wts[j]), A, None))
            strategies.append((float(wts[k]), None, Emin))
            strategies.append((float(wts[k + 1]), None, float(rng.choice(dipmin))))

        def error_on(target, y):
            """Probability of an output farther than eps/2 from `target`; y is None for the instance itself."""
            err = 0.0
            for p, A, out in strategies:
                if A is None:
                    err += p * (abs(out - target) > eps / 2 + 1e-12)
                elif y is not None and not any(sees[a, y] for a in A):
                    err += p * (abs(Emin - target) > eps / 2 + 1e-12)   # undetected: returns the hint's minimum
            return err

        delta = max([error_on(Emin, None)] + [error_on(dipmin[y], y) for y in range(n)])
        cost = sum(p * len(A) for p, A, out in strategies if A is not None)
        if (1 - 2 * delta) * pack > cost + 1e-7:
            return False, dict(reason="expected evaluations below (1 - 2 delta) * packing", delta=delta, packing=pack,
                               cost=cost)
        stats["nontrivial"] += delta < 0.5
        if uniform:
            if abs((1 - 2 * delta) * pack - cost) > 1e-7:
                return False, dict(reason="the blind mixture on the uniform metric should attain the bound",
                                   lhs=(1 - 2 * delta) * pack, cost=cost)
            stats["tight"] += 1
    if stats["tight"] == 0 or stats["nontrivial"] == 0:
        return False, dict(reason="coverage: no tight or no nontrivial instance", **stats)
    return True, stats


@conjecture("XII.3 Free energy: every evaluated set whose two envelope partition functions agree within e^eps reaches within slack c of every y whenever beta c > softgap(y) + eps; and (1 - 2 delta) * (packing of these thermal detection balls) <= expected evaluations of hint-verifying mixtures")
def t_thermal_query(rng, trials):
    stats = dict(certificates=0, mixtures=0)
    for _ in range(max(12, trials // 4)):
        n, d, kappa, f, g, _ = cg_instance(rng, nmax=7, kappas=(0.0, 0.3, 0.7))
        beta = float(rng.choice([0.5, 1.5, 4.0]))
        eps = float(rng.choice([0.1, 0.5, 1.5]))
        E = f + g
        Emin = float(E.min())
        s = cg_slack(d, g)
        Z = float(np.exp(-beta * (E - Emin)).sum())
        soft = np.array([math.log(Z) - math.log(float(np.exp(-beta * (E - Emin + s[:, y])).sum())) for y in range(n)])
        c = (soft + eps) / beta + 1e-7                    # a depth with beta c > softgap + eps
        for y in range(n):
            effect = math.log(float(np.exp(-beta * (f + qc_dip(d, g, y, c[y]) - Emin)).sum()) / Z)
            if effect <= eps:
                return False, dict(reason="a dip beyond the soft-gap radius is not sensitive", effect=effect, eps=eps)
        B = s < c[None, :]                                # the detection relation claimed by the theorem
        dips = [qc_dip(d, g, y, c[y]) for y in range(n)]
        sees = np.array([[abs(dips[y][a] - g[a]) > 1e-10 for y in range(n)] for a in range(n)])
        for mask in range(1, 2 ** n):
            A = [a for a in range(n) if mask >> a & 1]
            _, _, _, L, U = cg_bounds(d, f, g, A)
            width = math.log(float(np.exp(-beta * (f + L - Emin)).sum())) - math.log(float(np.exp(-beta * (f + U - Emin)).sum()))
            if width <= eps:
                stats["certificates"] += 1
                if not all(any(B[a, y] for a in A) for y in range(n)):
                    return False, dict(reason="a certificate of ln Z misses a thermal detection ball", size=len(A))
        pack = qc_frac_packing(B)
        k = int(rng.integers(1, 5))
        wts = rng.dirichlet(np.ones(k))
        sets = [qc_greedy_cover(sees) if rng.random() < 0.5 else
                sorted(rng.choice(n, size=int(rng.integers(1, n + 1)), replace=False).tolist()) for _ in range(k)]
        delta = max(sum(p for p, A in zip(wts, sets) if not any(sees[a, y] for a in A)) for y in range(n))
        cost = float(sum(p * len(A) for p, A in zip(wts, sets)))
        if (1 - 2 * delta) * pack > cost + 1e-7:
            return False, dict(reason="expected evaluations below (1 - 2 delta) * thermal packing", delta=float(delta),
                               packing=pack, cost=cost)
        stats["mixtures"] += 1
    # The factor 1 - 2 delta (not 1 - delta) is the right one: on the uniform metric the mixture of full evaluation
    # with two blind guesses -- ln Z of the instance, and the common value of ln Z on the dips -- attains the bound.
    for n in (4, 5, 6):
        beta, eps = 1.0, 0.2
        d = np.ones((n, n)) - np.eye(n)
        soft = math.log(n) - math.log(1 + (n - 1) * math.exp(-beta))
        c = (soft + eps) / beta + 1e-7
        if not c < 1:
            raise RuntimeError("sanity: the thermal detection balls of the uniform metric should be singletons")
        lnZ, lnZ_dip = math.log(n), math.log(n - 1 + math.exp(beta * c))
        if not lnZ_dip - lnZ > eps:
            raise RuntimeError("sanity: the dip is not sensitive")
        pack = qc_frac_packing(d < c)
        lam = float(rng.uniform(0.1, 0.9))
        blind = [((1 - lam) / 2, lnZ), ((1 - lam) / 2, lnZ_dip)]
        delta_tight = max(sum(p for p, o in blind if abs(o - lnZ) > eps / 2), sum(p for p, o in blind if abs(o - lnZ_dip) > eps / 2))
        cost_tight = lam * n
        if (1 - 2 * delta_tight) * pack > cost_tight + 1e-7 or abs((1 - 2 * delta_tight) * pack - cost_tight) > 1e-7:
            return False, dict(reason="the blind mixture on the uniform metric should attain (1 - 2 delta) * thermal packing",
                               lhs=(1 - 2 * delta_tight) * pack, cost=cost_tight)
        stats["tight"] = stats.get("tight", 0) + 1
    return True, stats


@conjecture("XII.4 Spot-checking a hint (minimum): every admissible residual whose minimum differs from the hint's by more than eps/2 differs from the hint on a whole closed slack ball {a : s(a,y) <= gap(y) + eps/2} or on all eps/2-minimisers; hence N samples from q miss it with probability at most (1 - p)^N")
def t_spot_check(rng, trials):
    stats = dict(distinguishable=0, lower=0, higher=0)
    for _ in range(trials):
        n, d, kappa, f, g, eps = cg_instance(rng)
        eps = max(eps, 0.1)
        E = f + g
        Emin = float(E.min())
        gap = E - Emin
        s = cg_slack(d, g)
        balls = [np.array([s[a, y] <= gap[y] + eps / 2 + 1e-12 for a in range(n)]) for y in range(n)]
        nearmin = gap <= eps / 2 + 1e-12
        q = rng.dirichlet(np.ones(n))
        p = min([float(q[b].sum()) for b in balls] + [float(q[nearmin].sum())])
        N = int(rng.integers(1, 6))
        for alt in range(12):
            kind = alt % 4
            if kind == 0:
                y = int(rng.integers(n))
                gp = qc_dip(d, g, y, gap[y] + eps / 2 + float(rng.uniform(0.01, 1.0)))
            elif kind == 1:                               # bumps at all near-minimisers
                c = float(rng.uniform(0.0, 1.5))
                gp = g.copy()
                for x in np.nonzero(nearmin)[0]:
                    gp = np.maximum(gp, g[x] + c - d[x, :])
            elif kind == 2:
                gp = cg_lipschitz(rng, d, 1.0) + float(rng.normal(0, 1.0))
            else:
                gp = np.minimum(g, cg_lipschitz(rng, d, 1.0) + float(rng.normal(0, 1.0)))
            if not qc_admissible(d, gp):
                raise RuntimeError("sanity: generated alternative is not admissible")
            dev = float((f + gp).min()) - Emin
            if abs(dev) > eps / 2 + 1e-9:
                D = np.abs(gp - g) > 1e-10
                qD = float(q[D].sum())
                if qD < p - 1e-9:
                    return False, dict(reason="a distinguishable alternative differs from the hint on too small a set",
                                       q_of_difference_set=qD, p=p, deviation=dev)
                if (1 - qD) ** N > (1 - p) ** N + 1e-12:
                    return False, dict(reason="miss probability exceeds (1 - p)^N")
                stats["distinguishable"] += 1
                stats["lower" if dev < 0 else "higher"] += 1
    if stats["lower"] == 0 or stats["higher"] == 0:
        return False, dict(reason="coverage: alternatives of one sign only", **stats)
    return True, stats


@conjecture("XII.5 Uniform cube at finite temperature (Harper step; all supports for n = 3, 4): a perturbation supported on at most |B(k)| points raises Z by at most as much as the dip on the Hamming ball B(k); and for every size m and every t the erosion {x : dist(x, D^c) > t} is largest for the complement of an initial segment of the simplicial order")
def t_cube_blocks(rng, trials):
    stats = dict(sets=0)
    for n in (3, 4):
        N = 2 ** n
        masks, sizes = qc_cube_erosions(n)
        proper = masks < np.uint64(2 ** N - 1)             # D^c nonempty
        card = sizes[:, 0]
        # initial segments of the simplicial order: by weight, then lexicographically by the positions of the ones
        order = sorted(range(N), key=lambda v: (bin(v).count("1"), tuple(i for i in range(n) if v >> i & 1)))
        for m in range(1, N):
            seg = sum(1 << v for v in order[: N - m])      # D^c = initial segment of size N - m
            D = (2 ** N - 1) ^ seg
            best = sizes[proper & (card == m)].max(axis=0)
            if np.any(best > sizes[D]):
                return False, dict(reason="some set has a larger erosion than the complement of a simplicial initial segment",
                                   n=n, size=m, best=best.tolist(), simplicial=sizes[D].tolist())
        for u in (0.5, 1.5):
            layer = np.array([math.exp(u * (t + 1)) - math.exp(u * t) for t in range(n + 1)])
            excess = sizes @ layer                         # sum over x in D of (e^{u dist(x, D^c)} - 1)
            for k in range(n):
                size = sum(math.comb(n, j) for j in range(k + 1))
                ball = sum(1 << v for v in range(N) if bin(v).count("1") <= k)
                ball_excess = float(excess[ball])
                closed = sum(math.comb(n, j) * (math.exp(u * (k + 1 - j)) - 1) for j in range(k + 1))
                if abs(ball_excess - closed) > 1e-9 * max(1.0, closed):
                    return False, dict(reason="closed form of the effect of the dip on a ball is wrong", n=n, k=k)
                sel = proper & (card <= size)
                worst = float(excess[sel].max())
                stats["sets"] += int(sel.sum())
                if worst > ball_excess + 1e-9:
                    return False, dict(reason="a set no larger than the ball has a larger effect than the ball", n=n,
                                       radius=k, ball=ball_excess, best=worst)
    return True, stats


@conjecture("XII.6 Soft-gap sampling: every admissible alternative with Z' >= (1 + eta) Z differs from g on a set of weight >= eta Z for the weights exp(-beta E)((1 + eta) e^Lambda - 1); the soft gap Lambda is beta*slack-Lipschitz; alternatives with a smaller Z differ on Gibbs weight >= Z - Z'")
def t_soft_gap_sampling(rng, trials):
    stats = dict(sets=0, random_alternatives=0, min_ratio=float("inf"))
    for _ in range(max(15, trials // 3)):
        n, d, kappa, f, g, _ = cg_instance(rng, nmax=8, kappas=(0.0, 0.3, 0.7))
        beta = float(rng.choice([0.3, 1.0, 2.0, 5.0]))
        eta = float(rng.choice([0.05, 0.3, 1.0, 5.0]))
        E = f + g
        w = np.exp(-beta * (E - E.min()))
        Z = float(w.sum())
        s = cg_slack(d, g)
        Lam = np.array([math.log(Z) - math.log(float((w * np.exp(-beta * s[:, y])).sum())) for y in range(n)])
        if np.any(Lam[:, None] > Lam[None, :] + beta * s.T + 1e-9):      # Lam[x] <= Lam[z] + beta s[z, x]
            return False, dict(reason="soft gap is not beta*slack-Lipschitz")
        W = w * ((1 + eta) * np.exp(Lam) - 1)
        # (a) the extremal alternative of every set D: g - h_D, h_D(y) = min over x outside D of s(x, y)
        for mask in range(1, 2 ** n - 1):
            D = [y for y in range(n) if mask >> y & 1]
            C = [x for x in range(n) if not mask >> x & 1]
            h = np.zeros(n)
            h[D] = s[np.ix_(C, D)].min(axis=0)
            if float((w * np.exp(beta * h)).sum()) >= (1 + eta) * Z:
                differs = h > 1e-12
                ratio = float(W[differs].sum()) / (eta * Z)
                stats["sets"] += 1
                stats["min_ratio"] = min(stats["min_ratio"], ratio)
                if ratio < 1 - 1e-9:
                    return False, dict(reason="a sensitive set has dip weight below eta Z", ratio=ratio)
        # (b) random admissible alternatives of either sign
        for alt in range(10):
            gp = cg_lipschitz(rng, d, 1.0) + float(rng.normal(0, 1.5))
            if alt % 2:
                gp = np.minimum(g, gp)
            if not qc_admissible(d, gp):
                raise RuntimeError("sanity: generated alternative is not admissible")
            Zp = float(np.exp(-beta * (f + gp - E.min())).sum())
            differs = np.abs(gp - g) > 1e-10
            stats["random_alternatives"] += 1
            if Zp >= (1 + eta) * Z and float(W[differs].sum()) < eta * Z * (1 - 1e-9):
                return False, dict(reason="an alternative with a larger partition function carries too little dip weight")
            if float(w[differs].sum()) < (Z - Zp) * (1 - 1e-9) - 1e-12:
                return False, dict(reason="an alternative with a smaller partition function differs on too little Gibbs weight")
    if stats["sets"] == 0:
        return False, dict(reason="coverage: no sensitive set")
    return True, stats


@conjecture("XII.7 Hedged spot-check and pair detection (minimum): with the output E* - eps/2 + eta, every admissible residual whose minimum is farther than eps/2 from that output differs from the hint on a closed slack ball {a : s(a,y) <= gap(y) + eps - eta} or on all eta-minimisers; mixtures of hedged hint-verifying and blind strategies obey (1 - 2 delta) * packing <= expected evaluations, and detect every pair of residuals whose minima differ by more than eps with probability >= 1 - 2 delta")
def t_hedged(rng, trials):
    stats = dict(outside_window=0, lower=0, higher=0, mixtures=0, pairs=0, tight_pairs=0)
    for trial in range(trials):
        uniform = trial % 5 == 0
        if uniform:
            n = int(rng.integers(3, 8))
            d, f, g, eps = np.ones((n, n)) - np.eye(n), np.zeros(n), np.zeros(n), 0.2
        else:
            n, d, kappa, f, g, eps = cg_instance(rng)
            eps = max(eps, 0.1)
        eta = float(rng.choice([0.1, 0.25, 0.5, 0.9])) * eps
        E = f + g
        Emin = float(E.min())
        gap = E - Emin
        s = cg_slack(d, g)
        hedge = Emin - eps / 2 + eta
        # (a) the window: what a hedged spot-check has to detect
        balls = [np.array([s[a, y] <= gap[y] + eps - eta + 1e-12 for a in range(n)]) for y in range(n)]
        nearmin = gap <= eta + 1e-12
        q = rng.dirichlet(np.ones(n))
        p = min([float(q[b].sum()) for b in balls] + [float(q[nearmin].sum())])
        for alt in range(12):
            kind = alt % 4
            if kind == 0:
                y = int(rng.integers(n))
                gp = qc_dip(d, g, y, gap[y] + eps - eta + float(rng.uniform(0.001, 1.0)) * (eta if alt % 8 == 0 else 1.0))
            elif kind == 1:                               # bumps at all eta-minimisers
                c = float(rng.uniform(0.0, 1.5))
                gp = g.copy()
                for x in np.nonzero(nearmin)[0]:
                    gp = np.maximum(gp, g[x] + c - d[x, :])
            elif kind == 2:
                gp = cg_lipschitz(rng, d, 1.0) + float(rng.normal(0, 1.0))
            else:
                gp = np.minimum(g, cg_lipschitz(rng, d, 1.0) + float(rng.normal(0, 1.0)))
            if not qc_admissible(d, gp):
                raise RuntimeError("sanity: generated alternative is not admissible")
            val = float((f + gp).min())
            if abs(val - hedge) > eps / 2 + 1e-9:
                D = np.abs(gp - g) > 1e-10
                if val < Emin and not any(bool(np.all(D[b])) for b in balls):
                    return False, dict(reason="an alternative below the hedged window does not differ on a whole closed ball",
                                       value=val - Emin, eps=eps, eta=eta)
                if val > Emin and not bool(np.all(D[nearmin])):
                    return False, dict(reason="an alternative above the hedged window agrees with the hint at an eta-minimiser",
                                       value=val - Emin, eps=eps, eta=eta)
                qD = float(q[D].sum())
                if qD < p - 1e-9:
                    return False, dict(reason="an alternative outside the hedged window differs from the hint on too small a set",
                                       q_of_difference_set=qD, p=p, value=val - Emin, eps=eps, eta=eta)
                stats["outside_window"] += 1
                stats["lower" if val < Emin else "higher"] += 1
        # (b) mixtures of hedged hint-verifying strategies and blind guesses, against the instance and its dips
        epsp = eps + float(rng.choice([0.05, 0.3]))
        B = s < (gap[None, :] + epsp)
        pack = qc_frac_packing(B)
        dips = [qc_dip(d, g, y, gap[y] + epsp) for y in range(n)]
        sees = np.array([[abs(dips[y][a] - g[a]) > 1e-10 for y in range(n)] for a in range(n)])
        dipmin = np.array([float((f + dips[y]).min()) for y in range(n)])
        strategies = []                                   # (probability, evaluated set or None, output if nothing is seen)
        if uniform:
            lam = float(rng.uniform(0.1, 0.9))
            strategies = [(lam, list(range(n)), hedge), ((1 - lam) / 2, None, Emin), ((1 - lam) / 2, None, Emin - epsp)]
        else:
            k = int(rng.integers(1, 5))
            wts = rng.dirichlet(np.ones(k + 2))
            for j in range(k):
                A = sorted(rng.choice(n, size=int(rng.integers(1, n + 1)), replace=False).tolist())
                out = float(rng.choice([Emin, hedge, Emin - eps / 2, Emin + eps / 2, Emin - epsp / 2]))
                strategies.append((float(wts[j]), A, out))
            strategies.append((float(wts[k]), None, float(rng.choice([Emin, hedge]))))
            strategies.append((float(wts[k + 1]), None, float(rng.choice(dipmin))))

        def error_on(target, y):
            """Probability of an output farther than eps/2 from `target`; y is None for the instance itself."""
            err = 0.0
            for pr, A, out in strategies:
                if A is None or y is None or not any(sees[a, y] for a in A):
                    err += pr * (abs(out - target) > eps / 2 + 1e-12)   # nothing seen: the fixed output
            return err

        errs = [error_on(Emin, None)] + [error_on(dipmin[y], y) for y in range(n)]
        delta = max(errs)
        cost = sum(pr * len(A) for pr, A, out in strategies if A is not None)
        if (1 - 2 * delta) * pack > cost + 1e-7:
            return False, dict(reason="hedged mixture: expected evaluations below (1 - 2 delta) * packing", delta=delta,
                               packing=pack, cost=cost)
        stats["mixtures"] += 1
        # (c) pairs: two residuals (the instance or dips) whose minima differ by more than eps
        values = [Emin] + dipmin.tolist()
        seen_by = [np.zeros(len(strategies), dtype=bool)] + [
            np.array([A is not None and any(sees[a, y] for a in A) for pr, A, out in strategies]) for y in range(n)]
        probs = np.array([pr for pr, A, out in strategies])
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                if abs(values[i] - values[j]) > eps + 1e-9:
                    detect = float(probs[seen_by[i] | seen_by[j]].sum())
                    if detect < 1 - 2 * delta - 1e-9:
                        return False, dict(reason="a distinguishable pair is detected with probability below 1 - 2 delta",
                                           detection=detect, delta=delta)
                    stats["pairs"] += 1
                    stats["tight_pairs"] += abs(detect - (1 - 2 * delta)) < 1e-9 and delta > 0.01
    if stats["lower"] == 0 or stats["higher"] == 0 or stats["tight_pairs"] == 0:
        return False, dict(reason="coverage: alternatives of one sign only, or no tight pair", **stats)
    return True, stats


@conjecture("XII.8 Cube accuracy diagram at the zero residual (exact ball counts): with k*(eps) the least radius whose dip is sensitive and eta = min(1, eps/2), the radii of the lower bound and of the hedged spot-check differ by at most 1 + ceil(1.46/u) (1 + ceil(1.32/u) for eps < 2), |B(k* - 1)|(e^u - 1) <= 2^n (e^eps - 1), and the exponents are ln 2 - h((Lambda_1 - lam)/u) for eps = e^{-lam n}, lam <= lam_c, and min(lam, ln 2) beyond")
def t_cube_diagram(rng, trials):
    stats = dict(brackets=0, max_log_gap=0.0, exponents=0)
    hb = lambda x: 0.0 if x <= 0 or x >= 1 else -x * math.log(x) - (1 - x) * math.log(1 - x)
    for n in (8, 20, 60, 200):
        for u in (0.3, 1.0, 2.5):
            logex, logball = qc_cube_log_excess(n, u)
            top = n * math.log(math.cosh(u / 2))           # the threshold accuracy
            grid = [10.0 ** e for e in range(-200, 0, 7)] + [0.3, 1.0, 1.9, 2.0, 2.5, 4.0] + \
                   [x * top for x in (0.1, 0.3, 0.6, 0.9, 0.99)]
            for eps in grid:
                eta = min(1.0, eps / 2)
                lt = lambda z: math.log(z) if z < 1e-8 else math.log(math.expm1(z))     # ln(e^z - 1)
                k2 = qc_cube_kstar(logex, lt(eps))                                      # lower bound: 2^n / |B(k2)|
                k1 = qc_cube_kstar(logex, lt(eps - eta)) - 1                            # spot-check: 2^n / |B(k1)|
                if k2 > n:
                    continue                                                            # no sensitive dip on a proper ball
                steps = 1 + math.ceil((1.4587 if eps >= 2 else 1.3133) / u)
                if k2 - k1 > steps:
                    return False, dict(reason="the two radii of the bracket are farther apart than claimed", n=n, u=u,
                                       eps=eps, k_lower=k2, k_upper=k1)
                if k2 >= 1 and logball[k2 - 1] + math.log(math.expm1(u)) > n * math.log(2) + lt(eps) + 1e-9:
                    return False, dict(reason="|B(k* - 1)|(e^u - 1) exceeds 2^n (e^eps - 1)", n=n, u=u, eps=eps)
                log_lb = n * math.log(2) - logball[k2]
                log_ub = min(n * math.log(2), max(n * math.log(2) - (logball[k1] if k1 >= 0 else 0.0),
                                                  -math.log(-math.expm1(-eta))))
                gap_ = log_ub - log_lb
                if gap_ < -1e-9:
                    return False, dict(reason="upper bound below lower bound", n=n, u=u, eps=eps)
                bound = max(steps * math.log(n + 1), math.log(10.2 * (n + 1) / math.expm1(u)))
                if gap_ > bound + 1e-9:
                    return False, dict(reason="the hedged bracket does not close up to the claimed polynomial factor", n=n,
                                       u=u, eps=eps, log_gap=gap_, bound=bound)
                stats["brackets"] += 1
                stats["max_log_gap"] = max(stats["max_log_gap"], gap_)
    # exponents in the exponentially small regimes
    n, u = 600, 1.0
    logex, logball = qc_cube_log_excess(n, u)
    lam1 = math.log(2.0 / (1.0 + math.exp(-u)))
    lam_c = math.log(2) - hb(1.0 / (1.0 + math.exp(u)))
    for lam in (0.02, 0.05, 0.1, 0.3, 0.6, 0.75):
        k = qc_cube_kstar(logex, -lam * n)
        exact = (n * math.log(2) - logball[min(k, n)]) / n
        pred = (math.log(2) - hb((lam1 - lam) / u)) if lam <= lam_c else min(lam, math.log(2))
        if abs(exact - pred) > 0.02:
            return False, dict(reason="exponent of the accuracy diagram differs from the prediction", lam=lam, exact=exact,
                               predicted=pred)
        stats["exponents"] += 1
    return True, stats


@conjecture("DEAD.10 Some proper subset of the configurations certifies ln Z exactly (as the exponent formula R_beta < ln k would require at eps = 0)", expect_fail=True)
def t_dead_exact_free_energy(rng, trials):
    """Refuted (second referee, C1): with positive slack off the diagonal, an exact certificate of ln Z is the whole
    space, so Theorem 11.15 cannot hold for arbitrarily small accuracies (`exact_free_energy_certificate_eq_univ`)."""
    found_proper = False
    for _ in range(6):
        n, d, kappa, f, g, _ = cg_instance(rng, nmax=6, kappas=(0.0, 0.3, 0.7))
        beta = float(rng.choice([0.5, 2.0]))
        Emin = float((f + g).min())
        for mask in range(1, 2 ** n - 1):
            A = [a for a in range(n) if mask >> a & 1]
            _, _, _, L, U = cg_bounds(d, f, g, A)
            width = math.log(float(np.exp(-beta * (f + L - Emin)).sum())) - math.log(float(np.exp(-beta * (f + U - Emin)).sum()))
            if width <= 1e-12:
                found_proper = True
    if not found_proper:
        return False, dict(reason="no proper subset certifies ln Z exactly: N_Z(0) = |X|")
    return True, {}


@conjecture("DEAD.11 In a doubling space the covers at shrunk radii theta (gap + eps/6) are within a constant factor of N_cov, also with a known part f", expect_fail=True)
def t_dead_doubling(rng, trials):
    """Refuted (second referee, M1): X = {0} + {2^-i : i <= m} on the line, f(x) = x, g = 0, eps = 2^(-m-3): the point 0
    covers everything at radius gap + eps, but at the shrunk radius (theta = 1/4) every point is covered only by itself."""
    ratios = []
    for m in (4, 8, 12):
        X = np.array([0.0] + [2.0 ** (-i) for i in range(1, m + 1)])
        eps = 2.0 ** (-m - 3)
        d = np.abs(X[:, None] - X[None, :])
        gap = X - X.min()
        ncov = cg_min_cover(d <= gap[None, :] + eps)
        shrunk = d <= 0.25 * (gap[None, :] + eps / 6)
        forced = int(sum(1 for y in range(len(X)) if shrunk[:, y].sum() == 1))
        ratios.append(forced / ncov)
    if ratios[-1] > ratios[0] + 1 and ratios[-1] >= 10:
        return False, dict(reason="shrunk covers are unboundedly larger than N_cov on a subset of the line",
                           ratio_m4=ratios[0], ratio_m8=ratios[1], ratio_m12=ratios[2])
    return True, {}


@conjecture("DEAD.12 The exponent of Theorem 11.9 is obtained with Boltzmann weights and by maximising over t site by site", expect_fail=True)
def t_dead_boltzmann_weights(rng, trials):
    """Refuted (second referee, M2).  (1) Two binary types (e, c) = (0.5, 1) and (5, 10): per-site maxima add up to
    0.3765 per pair, the common-slope value is 0.2329.  (2) Three states with gaps (0, 0.5, 3), c = 1: optimal weights
    give 0.1882, Boltzmann weights 0.1066.  (3) A binary site with residual: optimal 0.0252, Boltzmann <= 0."""
    ts = np.linspace(0.0, 6.0, 601)
    _, _, rA = qc_site([0, 0.5], [0, 0], 1.0)
    _, _, rB = qc_site([0, 5.0], [0, 0], 10.0)
    valsA = np.array([qc_lp_rate(rA, t) for t in ts])
    valsB = np.array([qc_lp_rate(rB, t) for t in ts])
    per_site, common = float(valsA.max() + valsB.max()), float((valsA + valsB).max())
    ts2 = np.linspace(0.0, 20.0, 801)
    gap3, s3, r3 = qc_site([0, 0.5, 3.0], [0, 0, 0], 1.0)
    opt3 = max(qc_lp_rate(r3, t) for t in ts2)
    boltz3 = max(qc_boltzmann_rate(gap3, s3, t) for t in ts2)
    gap2, s2, r2 = qc_site([0, 0.677], [0, 0.644], 1.0)
    opt2 = max(qc_lp_rate(r2, t) for t in ts2)
    boltz2 = max(qc_boltzmann_rate(gap2, s2, t) for t in ts2)
    if per_site > common + 0.1 and opt3 > boltz3 + 0.05 and opt2 > 0.02 and boltz2 < 1e-9:
        return False, dict(reason="per-site maximisation overshoots; Boltzmann weights are not optimal",
                           per_site_maxima=per_site, common_slope=common, three_state_optimal=float(opt3),
                           three_state_boltzmann=float(boltz3), residual_optimal=float(opt2),
                           residual_boltzmann=float(boltz2))
    return True, {}


@conjecture("DEAD.13 Under a second-order class with dense constants c_ij = c, evaluating the whole Hamming ball of radius 2 (or two opposite stars) determines the residual up to O(c)", expect_fail=True)
def t_dead_dense_second_order(rng, trials):
    """Refuted (second referee, M3): the remainder of the star envelope is quadratic in the Hamming distance.  The
    function -c C(|x| - 1, 2) has all mixed second differences in {0, -c}, vanishes on the ball of radius 2 and equals
    -c (n-1)(n-2)/2 at the far corner; a second explicit member vanishes on two opposite stars."""
    def worst_mixed(n, fn):
        worst = 0.0
        for x in itertools.product((0, 1), repeat=n):
            for i in range(n):
                for j in range(i + 1, n):
                    if x[i] == 0 and x[j] == 0:
                        xi, xj, xij = list(x), list(x), list(x)
                        xi[i] = 1
                        xj[j] = 1
                        xij[i] = xij[j] = 1
                        worst = max(worst, abs(fn(tuple(xij)) - fn(tuple(xi)) - fn(tuple(xj)) + fn(x)))
        return worst

    n = 7
    ball_member = lambda x: -float(math.comb(sum(x) - 1, 2)) if sum(x) >= 1 else 0.0
    on_ball = max(abs(ball_member(x)) for x in itertools.product((0, 1), repeat=n) if sum(x) <= 2)
    far = ball_member((1,) * n)
    w = (n + 2) // 3
    def two_star(x):
        a, b = sum(x[:w]), sum(x[w:])
        return -math.comb(a, 2) * math.comb(n - w - b, 2) / math.comb(n - w, 2)
    on_stars = max(abs(two_star(x)) for x in itertools.product((0, 1), repeat=n) if sum(x) <= 1 or sum(x) >= n - 1)
    at_S = two_star(tuple(1 if i < w else 0 for i in range(n)))
    if (worst_mixed(n, ball_member) <= 1 + 1e-12 and on_ball == 0 and far <= -(n - 1) * (n - 2) / 2 + 1e-9
            and worst_mixed(n, two_star) <= 1 + 1e-12 and on_stars == 0 and at_S <= -math.comb(w, 2) + 1e-9):
        return False, dict(reason="class members vanish on the evaluated sets and are far below zero elsewhere", n=n,
                           ball_member_far_corner=far, two_star_member_at_S=at_S)
    return True, {}


@conjecture("DEAD.14 At finite temperature single dips are the extremal perturbations on every instance: the fractional hitting number of all sensitive sets equals that of the single-dip balls", expect_fail=True)
def t_dead_single_dips(rng, trials):
    """Refuted (own exploration, cycle 8).  Uniform metric on n = 8 points, f = g = 0, beta = 1, eps = 0.3: a set D
    supports a perturbation that changes ln Z by more than eps iff |D| >= 2 (two shallow dips add up), so every correct
    randomised algorithm needs about n/2 evaluations, whereas the only sensitive single dips have depth > 1 and are seen
    from everywhere.  (On the uniform cube balls are extremal: XII.5.)"""
    from scipy.optimize import linprog
    n, beta, eps = 8, 1.0, 0.3
    d = np.ones((n, n)) - np.eye(n)
    blocks = []
    for mask in range(1, 2 ** n - 1):
        D = [x for x in range(n) if mask >> x & 1]
        C = [x for x in range(n) if not mask >> x & 1]
        h = d[np.ix_(D, C)].min(axis=1)                    # largest admissible perturbation supported in D
        if math.log((len(C) + float(np.exp(beta * h).sum())) / n) > eps:
            blocks.append(mask)
    minimal = [m for m in blocks if not any((m & o) == o and o != m for o in blocks)]
    A = np.array([[-(m >> a & 1) for a in range(n)] for m in minimal], dtype=float)
    fc_all = float(linprog(np.ones(n), A_ub=A, b_ub=-np.ones(len(minimal)), bounds=(0, None), method="highs").fun)
    # single dips: depth c <= 1 is supported on one point; its effect ln(1 + (e^{beta c} - 1)/n) never exceeds eps here
    single_point_sensitive = math.log(1 + (math.exp(beta) - 1) / n) > eps
    fc_dip = float(n) if single_point_sensitive else 1.0   # otherwise only full-support dips: one evaluation hits them
    if fc_all > fc_dip + 1e-6:
        return False, dict(reason="unions of shallow dips are sensitive although no local single dip is",
                           fractional_hitting_all=fc_all, fractional_hitting_single_dips=fc_dip)
    return True, {}


@conjecture("DEAD.15 On the cube the soft-gap bound of Theorem 11.25(a) is attained at the zero residual up to a polynomial factor (n^10) for every accuracy eps = o(n), in particular for eps = 0", expect_fail=True)
def t_dead_cube_tiny_accuracy(rng, trials):
    """Refuted (third referee, C1; `cube_exact_randomized`).  At eps = 0 the dip of depth c at a single point is
    sensitive, so every algorithm makes (1 - 2 delta) 2^n evaluations; the soft-gap bound is at most 2^n / |B(k)| with
    k = floor(n Lambda_1 / u), smaller by e^{n h(rho_0)}.  The same error as in DEAD.10 (Theorem 11.15)."""
    eps = 0.0
    n_small, u = 10, 1.0
    N = 2 ** n_small
    dist0 = np.array([bin(x).count("1") for x in range(N)])
    one_point = math.log(float(np.exp(u * np.maximum(0.0, 1 - dist0)).sum())) - n_small * math.log(2)   # dip of depth c at 0
    single_dip_sensitive = one_point > eps
    n = 200
    logex, logball = qc_cube_log_excess(n, u)
    lam1 = math.log(2.0 / (1.0 + math.exp(-u)))
    k_soft = int(math.floor((n * lam1 + eps) / u))                                # the soft-gap radius: u (k+1) > n Lambda_1 + eps
    k_exact = qc_cube_kstar(logex, math.log(math.expm1(eps)) if eps > 0 else float("-inf"))
    log_ratio = logball[k_soft] - logball[min(k_exact, n)]                        # exact-dip bound / soft-gap bound
    if single_dip_sensitive and k_exact == 0 and log_ratio > 10 * math.log(n):
        return False, dict(reason="at eps = 0 the exact-dip bound 2^n exceeds the soft-gap bound by more than n^10",
                           n=n, log_ratio=log_ratio, soft_gap_radius=k_soft)
    if not single_dip_sensitive and log_ratio > 10 * math.log(n):
        return False, dict(reason="the exact-dip bound exceeds the soft-gap bound by more than n^10", log_ratio=log_ratio)
    return True, {}


def qc_flat_box_log_hit(n, k, m, u, eps):
    """Flat k-state site (uniform Gibbs measure, envelope c * Hamming, u = beta c), n sites.  For the dips centred at a
    box prod B_i of m-subsets, h(x) = c (R - #{i : x_i not in B_i})_+, returns (ln(1 / P(a uniform sample lies in the
    support)), R) for the least sensitive radius R, i.e. the least R with ln E e^{beta h} > eps.  Exact binomial tails
    in the log domain.  The class of all such boxes is invariant under a transitive group, so the uniform sampler is
    optimal against it and the first number is the logarithm of its fractional hitting number."""
    p = 1 - m / k
    logpmf = [math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) + j * math.log(p) + (n - j) * math.log(1 - p)
              for j in range(n + 1)]
    lse = lambda a, b: max(a, b) + math.log1p(math.exp(-abs(a - b)))
    log_s, log_cdf = float("-inf"), float("-inf")          # S_R = sum_{j<R} pmf(j) e^{u (R-j)},  cdf_R = P(Bin < R)
    for R in range(1, n + 2):
        log_s = u + lse(log_s, logpmf[R - 1])
        log_cdf = lse(log_cdf, logpmf[R - 1])
        tail = -math.expm1(log_cdf) if log_cdf < 0 else 0.0
        effect = lse(log_s, math.log(tail)) if tail > 0 else log_s
        if effect > eps:
            return -log_cdf, R
    return 0.0, n + 1


@conjecture("DEAD.16 On product landscapes single dips are extremal at the exponential scale for ln Z: hitting every sensitive single dip costs as much, up to e^{o(n)}, as hitting every sensitive admissible perturbation", expect_fail=True)
def t_dead_dips_extremal_on_products(rng, trials):
    """Refuted (workstream A; recomputed here).  Flat k-state sites, zero residual, u = beta c = 1, eps = 1: the dips
    centred at boxes of m-subsets are admissible and sensitive, and under the (optimal) uniform sampler they are
    exponentially harder to hit than single dips: exponents D(rho_m || 1 - m/k), 0.0309 (m = 3) against 0.0194 (m = 1)
    for k = 8, and 0.02914 (m = 2) against 0.02841 for k = 4.  (For two-state sites the conjecture is supported by a
    paper proof of the same workstream; on the uniform cube it is Harper's theorem, XII.5.)"""
    u, eps = 1.0, 1.0
    dip8, _ = qc_flat_box_log_hit(1000, 8, 1, u, eps)
    box8, _ = qc_flat_box_log_hit(1000, 8, 3, u, eps)
    dip4, _ = qc_flat_box_log_hit(20000, 4, 1, u, eps)
    box4, _ = qc_flat_box_log_hit(20000, 4, 2, u, eps)
    kl = lambda a, b: a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b))
    rho = lambda k, m: -math.log(m / k + (1 - m / k) * math.exp(-u)) / u
    limits = (kl(rho(8, 1), 7 / 8), kl(rho(8, 3), 5 / 8), kl(rho(4, 1), 3 / 4), kl(rho(4, 2), 1 / 2))
    if box8 - dip8 > 8 and box4 - dip4 > 8 and limits[1] > limits[0] + 0.01 and limits[3] > limits[2] + 0.0005:
        return False, dict(reason="dips centred at boxes are exponentially harder to hit than single dips",
                           log_ratio_8_states_n1000=box8 - dip8, log_ratio_4_states_n20000=box4 - dip4,
                           exponents_8=(limits[0], limits[1]), exponents_4=(limits[2], limits[3]))
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
