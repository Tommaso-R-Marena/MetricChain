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


@conjecture("XI.14 Normal form: with f^d = min_x [f(x) + d(x, .)], sigma(a,y) = d(a,y) + f^d(a) - f^d(y) >= 0 and E^d = f^d + g, min(f + g') = min(f^d + g') on the admissible class, and for every evaluated set A the certified lower bound and the value upper bound of (d, f, g) are the lower bound and the incumbent of the instance (sigma, 0, E^d) without known part; s(a,y) - gap^d(y) = sigma(a,y) - gap^d(a)")
def t_normal_form(rng, trials):
    stats = dict(sets=0, instances=0, strict_point_gap=0)
    for _ in range(max(20, trials // 3)):
        n, d, kappa, f, g, eps = cg_instance(rng, nmax=7)
        if rng.random() < 0.5:
            f = f * float(rng.uniform(1.0, 4.0))          # known parts that are far from d-Lipschitz
        fd = np.min(f[:, None] + d, axis=0)               # Pasch-Hausdorff envelope f^d(y) = min_x [f(x) + d(x, y)]
        phi = fd                                          # the potential of the normal form
        sig = d + phi[:, None] - phi[None, :]
        Ed = phi + g
        if sig.min() < -1e-9 or np.max(np.abs(np.diag(sig))) > 1e-12 or not np.all(sig[:, None, :] <= sig[:, :, None] + sig[None, :, :] + 1e-9):
            return False, dict(reason="the reduced envelope is not a quasi-metric")
        if np.any(Ed[:, None] - Ed[None, :] > sig + 1e-9):
            return False, dict(reason="E^d is not admissible for the reduced envelope")
        for _ in range(6):                                # the minimum is unchanged on the class
            gp = cg_lipschitz(rng, d, 1.0) + float(rng.normal())
            if abs(float(np.min(f + gp)) - float(np.min(fd + gp))) > 1e-9:
                return False, dict(reason="min(f + g') differs from min(f^d + g')")
        s = cg_slack(d, g)
        gapd = Ed - float(np.min(Ed))
        if np.max(np.abs((s - gapd[None, :]) - (sig - gapd[:, None]))) > 1e-9:
            return False, dict(reason="client form and centre form of the covering relation differ")
        zero = np.zeros(n)
        for mask in range(1, 2 ** n):
            A = [a for a in range(n) if mask >> a & 1]
            lb, ubval, ubpt, _, _ = cg_bounds(d, f, g, A)
            lb2, ubval2, ubpt2, _, _ = cg_bounds(sig, zero, Ed, A)
            if abs(lb - lb2) > 1e-9 or abs(ubval - ubval2) > 1e-9 or abs(ubval - ubpt2) > 1e-9:
                return False, dict(reason="certified bounds of the normal form differ from those of the instance", lb=lb, lb_nf=lb2,
                                   value_ub=ubval, value_ub_nf=ubval2, incumbent_nf=ubpt2)
            stats["sets"] += 1
            stats["strict_point_gap"] += ubpt > ubval + 1e-9
        stats["instances"] += 1
    if stats["strict_point_gap"] == 0:
        return False, dict(reason="coverage: point and value upper bounds never differed in the original instances")
    return True, stats


def so_class_lp(n, c, A, y, sign=1.0):
    """max of sign * h(y) over h on {0,1}^n with all mixed second differences in [-c, c] and h = 0 on A (linear programme)."""
    from scipy.optimize import linprog
    N = 2 ** n
    rows, rhs = [], []
    for i in range(n):
        for j in range(i + 1, n):
            for x in range(N):
                if not (x >> i & 1) and not (x >> j & 1):
                    r = np.zeros(N)
                    r[x], r[x | 1 << i], r[x | 1 << j], r[x | 1 << i | 1 << j] = 1.0, -1.0, -1.0, 1.0
                    rows += [r, -r]
                    rhs += [c, c]
    obj = np.zeros(N)
    obj[y] = -sign
    res = linprog(obj, A_ub=np.array(rows), b_ub=np.array(rhs), bounds=[(0.0, 0.0) if x in A else (None, None) for x in range(N)],
                  method="highs")
    if res.status == 3:
        return float("inf")                               # A does not pin down the additive part
    if res.status != 0:
        raise RuntimeError("second-order class LP failed")
    return float(-res.fun)


@conjecture("XI.15 Dense second-order class on the cube: the dip c * C(r - d_H(x,y), 2)_+ has all mixed second differences in [0, c] up to sign, equals c C(r,2) at its centre and vanishes outside the ball of radius r - 2; hence the largest value at y of a class member vanishing on A is at least c C(d(y,A) + 1, 2), and for a union of stars it is exactly c C(d(y, centres), 2): stars do not combine")
def t_second_order_dip(rng, trials):
    stats = dict(dips=0, lp_sets=0, star_unions=0, tight=0)
    c = 1.0
    for n in (3, 4, 5, 6):
        N = 2 ** n
        pop = np.array([bin(x).count("1") for x in range(N)])
        for _ in range(4):
            y = int(rng.integers(N))
            r = int(rng.integers(0, n + 3))
            dist = pop[np.arange(N) ^ y]
            b = c * np.array([math.comb(max(r - int(t), 0), 2) for t in dist], dtype=float)
            if abs(b[y] - c * math.comb(r, 2)) > 1e-12 or np.any(b[dist >= r - 1] != 0):
                return False, dict(reason="dip has the wrong centre value or support")
            for i in range(n):
                for j in range(i + 1, n):
                    for x in range(N):
                        if not (x >> i & 1) and not (x >> j & 1):
                            m = b[x | 1 << i | 1 << j] - b[x | 1 << i] - b[x | 1 << j] + b[x]
                            if abs(m) > c + 1e-12:
                                return False, dict(reason="dip violates the mixed second difference bound", n=n, r=r)
            stats["dips"] += 1
    for _ in range(max(6, trials // 10)):                 # the whole class, by linear programming
        n = int(rng.integers(3, 6))
        N = 2 ** n
        pop = np.array([bin(x).count("1") for x in range(N)])
        a0 = int(rng.integers(N))                         # a star (pins down the additive part) and a few more points
        A = {a0} | {a0 ^ (1 << i) for i in range(n)} | set(int(a) for a in rng.choice(N, size=int(rng.integers(0, 4)), replace=False))
        for y in rng.choice(N, size=4, replace=False):
            y = int(y)
            if y in A:
                continue
            dA = min(int(pop[y ^ a]) for a in A)
            w = so_class_lp(n, c, A, y)
            if w < c * math.comb(dA + 1, 2) - 1e-7:
                return False, dict(reason="uncertainty below the dip bound c C(d+1, 2)", n=n, d=dA, lp=w)
            stats["lp_sets"] += 1
            stats["tight"] += abs(w - c * math.comb(dA + 1, 2)) < 1e-7
        centres = [int(a) for a in rng.choice(N, size=int(rng.integers(1, 3)), replace=False)]
        A = set(centres) | {a ^ (1 << i) for a in centres for i in range(n)}
        for y in range(N):
            if y not in A:
                d0 = min(int(pop[y ^ a]) for a in centres)
                w = so_class_lp(n, c, A, y)
                if abs(w - c * math.comb(d0, 2)) > 1e-7:
                    return False, dict(reason="union of stars: uncertainty differs from c C(d(y, centres), 2)", n=n, d=d0, lp=w)
                stats["star_unions"] += 1
    if stats["lp_sets"] == 0 or stats["tight"] == 0 or stats["star_unions"] == 0:
        return False, dict(reason="coverage: no linear programme, no tight case or no union of stars", **stats)
    return True, stats


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


def qc_lip_vertices(s, tol=1e-9):
    """Vertices of the Lipschitz polytope {phi : phi[a] - phi[b] <= s[a, b]} of a quasi-metric s on k points,
    normalised by phi[0] = 0 (brute force over the k-1 tight constraints; k <= 5)."""
    s = np.asarray(s, dtype=float)
    k = len(s)
    pairs = [(a, b) for a in range(k) for b in range(k) if a != b]
    verts = []
    for comb in itertools.combinations(pairs, k - 1):
        A = np.zeros((k, k))
        rhs = np.zeros(k)
        A[0, 0] = 1.0
        for i, (a, b) in enumerate(comb):
            A[i + 1, a], A[i + 1, b], rhs[i + 1] = 1.0, -1.0, s[a, b]
        if abs(np.linalg.det(A)) < 1e-9:
            continue
        phi = np.linalg.solve(A, rhs)
        if all(phi[a] - phi[b] <= s[a, b] + tol for a, b in pairs) and not any(np.allclose(phi, v, atol=1e-7) for v in verts):
            verts.append(phi)
    return verts


def qc_soft(pi, phi, beta):
    """Lambda(phi) = -ln E_pi exp(-beta phi)."""
    return -math.log(float(np.sum(pi * np.exp(-beta * np.asarray(phi)))))


def qc_game_min_col_max_row(K):
    """min over mixed columns M of max over rows a of sum_j M_j K[a, j]  (value of the matrix game)."""
    from scipy.optimize import linprog
    na, nj = K.shape
    c = np.r_[np.zeros(nj), 1.0]
    A = np.c_[K, -np.ones(na)]
    res = linprog(c, A_ub=A, b_ub=np.zeros(na), A_eq=[np.r_[np.ones(nj), 0.0]], b_eq=[1.0],
                  bounds=[(0, None)] * nj + [(None, None)], method="highs")
    if res.status != 0:
        raise RuntimeError("game LP failed")
    return float(res.fun)


def qc_site_exponent(pi, cols, beta, eps1, tmax_factor=1.5, grid=301):
    """max over t in [0, tmax_factor * beta] of -ln val(K_t) - t eps1 / beta, K_t[a, phi] = exp(-t (phi[a] - Lambda(phi)/beta)):
    the single-letter lower bound on the randomised exponent for the family `cols` of slack-Lipschitz site functions."""
    sig = np.array([np.asarray(phi) - qc_soft(pi, phi, beta) / beta for phi in cols]).T      # [a, phi]
    best, tbest = 0.0, 0.0
    for t in np.linspace(0.0, tmax_factor * beta, grid)[1:]:
        val = -math.log(qc_game_min_col_max_row(np.exp(-t * sig))) - t * eps1 / beta
        if val > best:
            best, tbest = val, float(t)
    return best, tbest


def qc_site_threshold(pi, cols, beta):
    """min over reference laws Q of max over the site functions phi in `cols` of beta E_Q phi - Lambda(phi); returns (value, Q)."""
    from scipy.optimize import linprog
    k = len(pi)
    M = np.array([[beta * phi[a] - qc_soft(pi, phi, beta) for phi in cols] for a in range(k)])      # [a, phi]
    c = np.r_[np.zeros(k), 1.0]
    A = np.c_[M.T, -np.ones(len(cols))]
    res = linprog(c, A_ub=A, b_ub=np.zeros(len(cols)), A_eq=[np.r_[np.ones(k), 0.0]], b_eq=[1.0],
                  bounds=[(0, None)] * k + [(None, None)], method="highs")
    if res.status != 0:
        raise RuntimeError("threshold LP failed")
    return float(res.fun), res.x[:k]


@conjecture("XII.9 Generalised dips: for every centre function Phi that is Lipschitz for the slack (Phi(x) - Phi(y) <= s(x,y)) the residual g - (r - Phi)_+ is admissible, differs from g only on {Phi < r}, and raises ln Z by at least beta r - Lambda(Phi), Lambda(Phi) = -ln E_pi e^{-beta Phi}; hence every certificate of ln Z meets {Phi < r} whenever beta r > Lambda(Phi) + eps")
def t_generalised_dips(rng, trials):
    stats = dict(dips=0, certificates=0)
    for _ in range(max(12, trials // 4)):
        n, d, kappa, f, g, _ = cg_instance(rng, nmax=7, kappas=(0.0, 0.3, 0.7))
        beta = float(rng.choice([0.5, 1.5, 4.0]))
        eps = float(rng.choice([0.1, 0.5, 1.5]))
        E = f + g
        Emin = float(E.min())
        s = cg_slack(d, g)
        w = np.exp(-beta * (E - Emin))
        Z = float(w.sum())
        supports = []
        for j in range(6):
            if j % 2 == 0:                                # inf-convolution: Phi(x) = min_y [a_y + s(x, y)]
                Phi = (rng.uniform(0.0, 1.5, size=n)[None, :] + s).min(axis=1)
            else:                                         # slack distance to a random set of centres
                B = rng.random(n) < 0.4
                B[int(rng.integers(n))] = True
                Phi = s[:, B].min(axis=1)
            if np.any(Phi[:, None] - Phi[None, :] > s + 1e-9):
                raise RuntimeError("sanity: centre function is not Lipschitz for the slack")
            lam = math.log(Z) - math.log(float((w * np.exp(-beta * Phi)).sum()))
            r = (lam + eps) / beta + 1e-7                 # a radius with beta r > Lambda(Phi) + eps
            gp = g - np.maximum(0.0, r - Phi)
            if not qc_admissible(d, gp):
                return False, dict(reason="a generalised dip is not admissible")
            if np.any((np.abs(gp - g) > 1e-12) & ~(Phi < r)):
                return False, dict(reason="a generalised dip differs from g outside {Phi < r}")
            effect = math.log(float(np.exp(-beta * (f + gp - Emin)).sum()) / Z)
            if effect < beta * r - lam - 1e-9 or effect <= eps:
                return False, dict(reason="a generalised dip beyond its soft-gap radius is not sensitive", effect=effect,
                                   eps=eps)
            supports.append(Phi < r)
            stats["dips"] += 1
        for mask in range(1, 2 ** n):
            A = [a for a in range(n) if mask >> a & 1]
            _, _, _, L, U = cg_bounds(d, f, g, A)
            width = math.log(float(np.exp(-beta * (f + L - Emin)).sum())) - math.log(float(np.exp(-beta * (f + U - Emin)).sum()))
            if width <= eps:
                stats["certificates"] += 1
                if not all(any(D[a] for a in A) for D in supports):
                    return False, dict(reason="a certificate of ln Z misses the support of a sensitive generalised dip",
                                       size=len(A))
    if stats["certificates"] == 0:
        return False, dict(reason="coverage: no certificate")
    return True, stats


@conjecture("XII.10 Two-reference sandwich: with gamma(Q) = max over the vertices of the Lipschitz polytope of a site of [beta E_Q phi - Lambda(phi)], every admissible profile h on S^n has ln E_{pi^n} e^{beta h} <= beta E_{Q^n} h + n gamma(Q), with equality for an additive profile; hence Q^n(D) >= (ln E e^{beta h_D} - n gamma(Q)) / (n beta s_max) for every proper subset D")
def t_two_measure(rng, trials):
    stats = dict(profiles=0, vertex_profiles=0, sets=0)
    for trial in range(max(10, trials // 6)):
        k = 2 if trial % 2 == 0 else 3
        n = int(rng.integers(2, 5 if k == 2 else 4))
        beta = float(rng.choice([0.5, 1.0, 2.5]))
        phi_site = rng.uniform(0.0, 2.0, size=k)          # known part of one site
        gam = rng.uniform(-0.4, 0.4, size=k)              # additive residual of one site (admissible for c = 1)
        if trial == 1:
            phi_site, gam, beta = np.array([0.0, 0.0, 2.0]), np.zeros(3), 1.0    # a site on which non-dip vertices matter
        s1 = (1 - np.eye(k)) - gam[:, None] + gam[None, :]
        pi = np.exp(-beta * (phi_site + gam))
        pi /= pi.sum()
        Q = rng.dirichlet(np.ones(k)) if trial != 1 else np.array([0.47, 0.47, 0.06])
        V = qc_lip_vertices(s1)
        G = V                                             # the family that defines gamma(Q)
        gamma = max(beta * float(Q @ v) - qc_soft(pi, v, beta) for v in G)
        Xa = np.array(list(itertools.product(range(k), repeat=n)))
        N = len(Xa)
        piN, QN = np.prod(pi[Xa], axis=1), np.prod(Q[Xa], axis=1)
        sN = sum(s1[Xa[:, i][:, None], Xa[:, i][None, :]] for i in range(n))      # sN[x, y]
        smax = float(s1.max())

        def sides(h):
            return math.log(float(piN @ np.exp(beta * h))), beta * float(QN @ h) + n * gamma

        for _ in range(6):                                # random admissible profiles (inf-convolutions)
            a = rng.uniform(0.0, 3.0 * n, size=N) * (rng.random(N) < 0.5) + float(rng.uniform(-2, 2))
            h = (a[:, None] + sN).min(axis=0)
            if np.any(h[None, :] - h[:, None] > sN + 1e-9):
                raise RuntimeError("sanity: profile is not admissible")
            lhs, rhs = sides(h)
            if lhs > rhs + 1e-9:
                return False, dict(reason="two-measure bound violated by an admissible profile", lhs=lhs, rhs=rhs)
            stats["profiles"] += 1
        worst = -float("inf")
        for v in V:                                       # additive profiles from every vertex of the site polytope
            lhs, rhs = sides(-v[Xa].sum(axis=1))
            if lhs > rhs + 1e-8:
                return False, dict(reason="two-measure bound violated by an additive vertex profile", lhs=lhs, rhs=rhs, k=k)
            worst = max(worst, lhs - rhs)
            stats["vertex_profiles"] += 1
        if worst < -1e-8:
            return False, dict(reason="the constant n gamma(Q) is not attained by an additive profile", slack=worst)
        for _ in range(40):                               # sets: the largest profile vanishing off D, and the hitting bound
            D = rng.random(N) < float(rng.uniform(0.05, 0.9))
            if D.all() or not D.any():
                continue
            hD = sN[~D, :].min(axis=0)
            lhs, rhs = sides(hD)
            if lhs > rhs + 1e-9:
                return False, dict(reason="two-measure bound violated by the extremal profile of a set")
            if float(QN[D].sum()) < (lhs - n * gamma) / (n * beta * smax) - 1e-9:
                return False, dict(reason="a set has smaller Q^n-mass than the hitting bound")
            stats["sets"] += 1
    return True, stats


@conjecture("XII.11 Single-letter lower bounds for ln Z on product landscapes: the game over all vertices of the Lipschitz polytope of a site dominates the game over its distance functions (R^gen >= R^rand), with equality for two-state sites; on flat k-state sites it equals max_m D(rho_m || 1 - m/k)_+ and exceeds the dip exponent for k = 4, u = 1; the optimal t is at most beta; and R^gen is positive below and zero above the threshold min_Q max_phi [beta E_Q phi - Lambda(phi)]")
def t_single_letter(rng, trials):
    stats = dict(binary=0, flat=0, ternary=0, strict=0)
    kl = lambda a, b: a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b))
    for _ in range(3):                                    # two-state sites: the polytope is a segment
        s1 = np.array([[0.0, float(rng.uniform(0.3, 2.0))], [float(rng.uniform(0.3, 2.0)), 0.0]])
        pi = rng.dirichlet(np.ones(2) * 3)
        beta = float(rng.choice([0.5, 1.0, 3.0]))
        V = qc_lip_vertices(s1)
        dist = [s1[:, b] for b in range(2)]
        if len(V) != 2:
            return False, dict(reason="the Lipschitz polytope of a two-point space should be a segment")
        rg, _ = qc_site_exponent(pi, V, beta, 0.0, grid=121)
        rr, _ = qc_site_exponent(pi, dist, beta, 0.0, grid=121)
        if abs(rg - rr) > 1e-7:
            return False, dict(reason="two-state site: vertex game differs from the dip game", gen=rg, dips=rr)
        stats["binary"] += 1
    for k, u in ((3, 1.0), (4, 0.5), (4, 1.0), (4, 2.0)):  # flat sites (c = 1, beta = u)
        s1 = np.ones((k, k)) - np.eye(k)
        pi = np.ones(k) / k
        V = qc_lip_vertices(s1)
        if len(V) != 2 ** k - 2:
            return False, dict(reason="Hamming site: expected one vertex per proper nonempty subset", k=k, found=len(V))
        rg, tg = qc_site_exponent(pi, V, u, 0.0, grid=241)
        rr, _ = qc_site_exponent(pi, [s1[:, b] for b in range(k)], u, 0.0, grid=241)
        closed = 0.0
        for m in range(1, k):
            rho = -math.log(m / k + (1 - m / k) * math.exp(-u)) / u
            if rho < 1 - m / k:
                closed = max(closed, kl(rho, 1 - m / k))
        if abs(rg - closed) > 2e-5 or rg < rr - 1e-7 or tg > u + 1e-9:
            return False, dict(reason="flat site: vertex game differs from the closed form, or t* > beta", k=k, u=u, game=rg,
                               closed=closed, t_star=tg)
        if (k, u) == (4, 1.0):
            if not (rg > rr + 5e-4 and abs(rg - 0.02914) < 2e-5 and abs(rr - 0.02841) < 2e-5):
                return False, dict(reason="flat four-state site: boxes of pairs should beat single dips (0.02914 > 0.02841)",
                                   gen=rg, dips=rr)
            stats["strict"] += 1
        stats["flat"] += 1
    for _ in range(max(2, trials // 30)):                 # random three-state sites with an additive residual
        gam = rng.uniform(-0.4, 0.4, size=3)
        s1 = (1 - np.eye(3)) - gam[:, None] + gam[None, :]
        beta = float(rng.choice([0.7, 1.5]))
        pi = np.exp(-beta * (rng.uniform(0.0, 2.0, size=3) + gam))
        pi /= pi.sum()
        V = qc_lip_vertices(s1)
        dist = [s1[:, b] for b in range(3)]
        thr, _ = qc_site_threshold(pi, V, beta)
        rg, tg = qc_site_exponent(pi, V, beta, 0.0, grid=121)
        rr, _ = qc_site_exponent(pi, dist, beta, 0.0, grid=121)
        below, _ = qc_site_exponent(pi, V, beta, 0.6 * thr, grid=121)
        above, _ = qc_site_exponent(pi, V, beta, 1.05 * thr + 0.005, grid=121)
        if rg < rr - 1e-7 or tg > beta + 1e-9 or not below > 1e-7 or above > 1e-9:
            return False, dict(reason="three-state site: ordering, range of t, or threshold of the vertex game is wrong",
                               gen=rg, dips=rr, t_star=tg, below=below, above=above, threshold=thr)
        stats["ternary"] += 1
        stats["strict"] += rg > rr + 1e-5
    return True, stats


@conjecture("XII.12 Identical two-state sites without a hint: with P(theta) = ln(1 + e^{-beta(e + theta)}) the dip threshold at the additive instance theta*M is the chord gap G(theta) of P over [-c, c]; max_theta G = min_theta max(D(c; theta), D(-c; theta)) =: eps*; and with the reference tilted to theta* every c-Lipschitz residual g on {0,1}^n satisfies 0 <= ln Z(f + g) - [ln Z(f + theta* M) - beta E_{pi_theta*}(g - theta* M)] <= n eps*, with equality for g = c M and g = -c M")
def t_hint_free_threshold(rng, trials):
    stats = dict(instances=0, residuals=0)
    c = 1.0
    for trial in range(max(8, trials // 8)):
        e = 0.0 if trial == 0 else float(rng.uniform(-1.5, 1.5))
        beta = float(rng.choice([0.5, 1.0, 2.0, 4.0]))
        P = lambda th: math.log1p(math.exp(-beta * (e + th)))
        p1 = lambda th: 1.0 / (1.0 + math.exp(beta * (e + th)))          # probability of the excited state; P' = -beta p1
        G = lambda th: ((c + th) * P(c) + (c - th) * P(-c)) / (2 * c) - P(th)
        Dv = lambda tp, th: P(tp) - P(th) + (tp - th) * beta * p1(th)
        q = (P(-c) - P(c)) / (2 * c * beta)               # tangent parallel to the chord: p1(theta*) = q
        th_star = -e - math.log(q / (1 - q)) / beta
        eps_star = G(th_star)
        thetas = np.linspace(-c, c, 2001)
        if (max(G(t) for t in thetas) > eps_star + 1e-10 or min(max(Dv(c, t), Dv(-c, t)) for t in thetas) < eps_star - 1e-10
                or abs(Dv(c, th_star) - eps_star) > 1e-10 or abs(Dv(-c, th_star) - eps_star) > 1e-10):
            return False, dict(reason="chord gap and Bregman widths do not meet at theta*", e=e, beta=beta)
        if trial == 0 and (abs(th_star) > 1e-12 or abs(eps_star - math.log(math.cosh(beta * c / 2))) > 1e-12):
            return False, dict(reason="uniform cube: threshold should be ln cosh(u/2) at theta* = 0")
        for th in rng.uniform(-0.95 * c, 0.95 * c, size=4):               # the dip game at the instance theta M
            pi = np.array([1 - p1(th), p1(th)])
            s1 = np.array([[0.0, c + th], [c - th, 0.0]])                 # s(0,1) = c + theta, s(1,0) = c - theta
            crit, _ = qc_site_threshold(pi, [s1[:, 0], s1[:, 1]], beta)
            if abs(crit - G(float(th))) > 1e-7:
                return False, dict(reason="dip threshold at theta M differs from the chord gap", game=crit, chord=G(float(th)))
        n = int(rng.integers(2, 5))
        Xa = np.array(list(itertools.product((0, 1), repeat=n)))
        M = Xa.sum(axis=1).astype(float)
        dH = (Xa[:, None, :] != Xa[None, :, :]).sum(axis=2).astype(float)
        f = e * M
        ref = th_star                                     # slope of the reference instance
        wT = np.exp(-beta * (f + ref * M))
        lnZref = math.log(float(wT.sum()))
        piT = wT / wT.sum()
        cands = [c * M, -c * M] + [c * (Xa @ sg) for sg in rng.choice([-1.0, 1.0], size=(3, n))]
        for _ in range(8):
            a = rng.uniform(-2.0, 2.0, size=len(Xa))
            lo = (a[None, :] + c * dH).min(axis=1)        # c-Lipschitz for the Hamming distance
            cands += [lo, -lo]
        for j, g in enumerate(cands):
            if np.any(np.abs(g[:, None] - g[None, :]) > c * dH + 1e-9):
                raise RuntimeError("sanity: residual is not c-Lipschitz")
            low = lnZref - beta * float(piT @ (g - ref * M))
            val = math.log(float(np.exp(-beta * (f + g)).sum()))
            if val < low - 1e-9 or val > low + n * eps_star + 1e-9:
                return False, dict(reason="tilted sandwich violated", excess=val - low, width=n * eps_star, e=e, beta=beta)
            if j < 2 and abs(val - low - n * eps_star) > 1e-8:
                return False, dict(reason="the additive extremes should attain the width n eps*", excess=val - low,
                                   width=n * eps_star)
            stats["residuals"] += 1
        stats["instances"] += 1
    return True, stats


def qc_tilted_pressure(Q, psi, f1, beta):
    """F_Q(psi) = ln sum_a exp(-beta (f1(a) + psi(a))) + beta E_Q psi  (invariant under adding a constant to psi)."""
    return math.log(float(np.sum(np.exp(-beta * (f1 + psi))))) + beta * float(Q @ psi)


def qc_min_tilted_pressure(Q, d1, f1, beta):
    """min of the convex function F_Q over the Lipschitz polytope {psi(a) - psi(b) <= d1[a, b]} (normalised psi(0) = 0)."""
    from scipy.optimize import minimize
    k = len(f1)
    cons = [{"type": "ineq", "fun": (lambda z, a=a, b=b: d1[a, b] - (np.r_[0.0, z][a] - np.r_[0.0, z][b]))}
            for a in range(k) for b in range(k) if a != b]
    free = -np.log(np.maximum(Q, 1e-12)) / beta - f1       # unconstrained minimiser: the law of f1 + psi is Q
    best = float("inf")
    for start in (np.zeros(k - 1), np.clip(free[1:] - free[0], -5.0, 5.0)):
        res = minimize(lambda z: qc_tilted_pressure(Q, np.r_[0.0, z], f1, beta), start, constraints=cons, method="SLSQP",
                       options=dict(ftol=1e-13, maxiter=500))
        if np.all([c["fun"](res.x) >= -1e-9 for c in cons]):
            best = min(best, float(res.fun))
    return best


@conjecture("XII.13 One reference law, no hint, any alphabet: with F_Q(psi) = ln sum_a e^{-beta(f1 + psi)} + beta E_Q psi, m(Q) and M(Q) its least and largest value over the Lipschitz polytope of a site, every admissible residual g on S^n satisfies n m(Q) <= ln Z(f + g) + beta E_{Q^n} g <= n M(Q), with both ends attained by additive residuals; and min_Q [M(Q) - m(Q)] equals the supremum over additive instances of the instance threshold min_Q max_psi [F_Q(psi) - F_Q(gamma)] (for two-state sites: the chord gap of the pressure)")
def t_one_reference_sandwich(rng, trials):
    from scipy.optimize import minimize
    stats = dict(residuals=0, sites=0, minimax=0)
    for trial in range(max(6, trials // 10)):             # (a) the sandwich on small products, random quasi-metric site envelopes
        k = 2 if trial % 2 == 0 else 3
        n = int(rng.integers(2, 5 if k == 2 else 4))
        beta = float(rng.choice([0.5, 1.0, 2.5]))
        f1 = np.r_[0.0, rng.uniform(-1.0, 2.0, size=k - 1)]
        d1 = rng.uniform(0.3, 1.5, size=(k, k))
        np.fill_diagonal(d1, 0.0)
        for _ in range(k):                                # shortest paths: a quasi-metric
            d1 = np.array([[min(d1[a, b], min(d1[a, c] + d1[c, b] for c in range(k))) for b in range(k)] for a in range(k)])
        Q = rng.dirichlet(np.ones(k))
        if trial == 1:                                    # a site on which a vertex that is not a distance function is extremal
            f1, d1, beta, Q = np.array([0.0, 0.0, 2.0]), np.ones((3, 3)) - np.eye(3), 1.0, np.array([0.48, 0.48, 0.04])
        V = qc_lip_vertices(d1)
        Mq = max(qc_tilted_pressure(Q, v, f1, beta) for v in V)
        mq = qc_min_tilted_pressure(Q, d1, f1, beta)
        Xa = np.array(list(itertools.product(range(k), repeat=n)))
        fN, QN = f1[Xa].sum(axis=1), np.prod(Q[Xa], axis=1)
        dN = sum(d1[Xa[:, i][:, None], Xa[:, i][None, :]] for i in range(n))
        cands = [v[Xa].sum(axis=1) for v in V]
        for _ in range(8):
            a = rng.uniform(-3.0, 3.0, size=len(Xa))
            cands += [(a[None, :] + dN).min(axis=1), -(a[:, None] + dN).min(axis=0)]
        hi = lo = None
        for g in cands:
            if np.any(g[:, None] - g[None, :] > dN + 1e-9):
                raise RuntimeError("sanity: residual is not admissible")
            val = math.log(float(np.exp(-beta * (fN + g)).sum())) + beta * float(QN @ g)
            if val > n * Mq + 1e-8 or val < n * mq - 1e-6:
                return False, dict(reason="one-reference sandwich violated", value=val, lower=n * mq, upper=n * Mq, k=k, n=n)
            hi = val if hi is None else max(hi, val)
            lo = val if lo is None else min(lo, val)
            stats["residuals"] += 1
        if abs(hi - n * Mq) > 1e-8:
            return False, dict(reason="the upper end n M(Q) is not attained by an additive vertex residual", gap=n * Mq - hi)
        stats["sites"] += 1

    def width(d1, f1, beta, V):                           # min over Q of M(Q) - m(Q)  (convex in Q)
        obj = lambda z: (lambda Q: max(qc_tilted_pressure(Q, v, f1, beta) for v in V) - qc_min_tilted_pressure(Q, d1, f1, beta))(
            np.exp(z - z.max()) / np.exp(z - z.max()).sum())
        return min(float(minimize(obj, z0, method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-11, maxiter=3000)).fun)
                   for z0 in (np.zeros(len(f1)), -beta * f1))

    for e, beta in ((0.0, 1.0), (0.5, 1.0), (-1.0, 2.0)):  # (b) two-state sites: the chord gap of the pressure
        P = lambda th: math.log1p(math.exp(-beta * (e + th)))
        q = (P(-1.0) - P(1.0)) / (2 * beta)
        th = -e - math.log(q / (1 - q)) / beta
        chord = ((1 + th) * P(1.0) + (1 - th) * P(-1.0)) / 2 - P(th)
        d1 = np.ones((2, 2)) - np.eye(2)
        w = width(d1, np.array([0.0, e]), beta, qc_lip_vertices(d1))
        if abs(w - chord) > 1e-6:
            return False, dict(reason="two-state site: min_Q [M - m] differs from the chord gap", width=w, chord=chord)
    d1 = np.ones((3, 3)) - np.eye(3)                      # (c) three-state sites: the minimax identity
    V = qc_lip_vertices(d1)
    for f1, beta in ((np.array([0.0, 0.0, 2.0]), 1.0), (np.r_[0.0, rng.uniform(-1.5, 2.0, size=2)], float(rng.choice([0.7, 1.5])))):
        w = width(d1, f1, beta, V)
        p = lambda psi: math.log(float(np.sum(np.exp(-beta * (f1 + psi)))))

        def thr(gam):                                     # instance threshold at the additive instance gam: an LP in Q
            from scipy.optimize import linprog
            res = linprog(np.r_[np.zeros(3), 1.0], A_ub=np.array([np.r_[beta * (v - gam), -1.0] for v in V]),
                          b_ub=np.array([-(p(v) - p(gam)) for v in V]), A_eq=[np.r_[np.ones(3), 0.0]], b_eq=[1.0],
                          bounds=[(0, None)] * 3 + [(None, None)], method="highs")
            return float(res.fun)

        best = max(((thr(np.array([0.0, g1, g2])), g1, g2) for g1 in np.linspace(-1, 1, 21) for g2 in np.linspace(-1, 1, 21)
                    if abs(g1 - g2) <= 1 + 1e-12))
        inside = lambda z: abs(z[0]) <= 1 and abs(z[1]) <= 1 and abs(z[0] - z[1]) <= 1
        res = minimize(lambda z: -thr(np.array([0.0, z[0], z[1]])) if inside(z) else 1.0, best[1:], method="Nelder-Mead",
                       options=dict(xatol=1e-7, fatol=1e-11))
        sup_thr = max(best[0], -float(res.fun))
        if abs(w - sup_thr) > 2e-5 or thr(np.zeros(3)) > w + 1e-7:
            return False, dict(reason="hint-free width differs from the supremum of the instance thresholds", width=w,
                               sup_threshold=sup_thr, threshold_at_zero=thr(np.zeros(3)))
        stats["minimax"] += 1
    return True, stats


@conjecture("XII.14 The constant of the soft-gap sampler does not depend on the residual: E_pi e^Lambda = sum_y e^{-beta f(y)} / sum_a e^{-beta (f(a) + d(a,y))} for every admissible g; and it is at most e^{beta r} times the number of cells of any partition into cells of envelope diameter at most r")
def t_spot_check_constant(rng, trials):
    stats = dict(instances=0, partitions=0)
    for _ in range(trials):
        n, d, kappa, f, g, _ = cg_instance(rng)
        beta = float(rng.choice([0.3, 1.0, 2.5]))
        E = f + g
        w = np.exp(-beta * (E - E.min()))
        Z = float(w.sum())
        s = cg_slack(d, g)
        Lam = np.array([math.log(Z) - math.log(float((w * np.exp(-beta * s[:, y])).sum())) for y in range(n)])
        lhs = float((w * np.exp(Lam)).sum()) / Z
        rhs = float(sum(math.exp(-beta * f[y]) / float(np.exp(-beta * (f + d[:, y])).sum()) for y in range(n)))
        if abs(lhs - rhs) > 1e-9 * max(1.0, rhs):
            return False, dict(reason="E_pi e^Lambda depends on the residual", with_residual=lhs, residual_free=rhs)
        cells = rng.integers(0, int(rng.integers(1, n + 1)), size=n)
        r = max(float(d[a, y]) for a in range(n) for y in range(n) if cells[a] == cells[y])
        if rhs > math.exp(beta * r) * len(set(cells.tolist())) * (1 + 1e-9):
            return False, dict(reason="spot-check constant exceeds the metric-entropy bound")
        stats["instances"] += 1
        stats["partitions"] += len(set(cells.tolist())) > 1
    return True, stats


@conjecture("XII.15 Second-order droplets and continuum sites: the droplet -c C(r + 1 - d_H(x,y), 2)_+ multiplies Z on the cube by 2^{-n} sum_k C(n,k) e^{beta c C(r+1-k, 2)}; the Curie-Weiss function max_m [w m^2/8 - I(m)] is positive iff w > 4; and on the circle the tent has Jensen gap ln(sinh b / b), b = beta L pi / 2, the largest among Lipschitz functions")
def t_droplets_and_circle(rng, trials):
    stats = dict(droplets=0, lipschitz=0)
    for n in (4, 6, 8, 10):
        N = 2 ** n
        pop = np.array([bin(x).count("1") for x in range(N)])
        for _ in range(3):
            r, bc = int(rng.integers(1, n + 1)), float(rng.uniform(0.05, 0.6))
            y = int(rng.integers(N))
            dist = pop[np.arange(N) ^ y]
            drop = -np.array([math.comb(max(r + 1 - int(t), 0), 2) for t in dist], dtype=float)
            brute = float(np.exp(-bc * drop).sum()) / N
            closed = sum(math.comb(n, k) * math.exp(bc * math.comb(max(r + 1 - k, 0), 2)) for k in range(n + 1)) / N
            if abs(brute - closed) > 1e-9 * closed or np.any(drop[dist >= r] != 0):
                return False, dict(reason="droplet partition function or support is wrong", n=n, r=r)
            stats["droplets"] += 1
    hb = lambda x: 0.0 if x <= 0 or x >= 1 else -x * math.log(x) - (1 - x) * math.log(1 - x)
    fcw = lambda w: max(w * m * m / 8 - (math.log(2) - hb((1 + m) / 2)) for m in np.linspace(0.0, 0.999, 4000))
    if fcw(3.0) > 1e-12 or fcw(4.0) > 1e-9 or not fcw(4.5) > 1e-4 or not fcw(8.0) > 0.1:
        return False, dict(reason="Curie-Weiss free energy does not change sign at w = 4", values=[fcw(3.0), fcw(4.0), fcw(4.5)])
    M = 720                                               # the circle, discretised
    ang = np.minimum(np.arange(M), M - np.arange(M)) * 2 * math.pi / M        # geodesic distance to the point 0
    for beta, L in ((1.0, 0.5), (1.0, 2.0), (0.5, 3.0)):
        b = beta * L * math.pi / 2
        gap = lambda phi: math.log(float(np.mean(np.exp(-beta * (phi - phi.mean())))))
        tent = gap(L * ang)
        if abs(tent - math.log(math.sinh(b) / b)) > 2e-3:
            return False, dict(reason="Jensen gap of the tent differs from ln(sinh b / b)", tent=tent, formula=math.log(math.sinh(b) / b))
        dcirc = np.minimum(np.abs(np.arange(M)[:, None] - np.arange(M)[None, :]), M - np.abs(np.arange(M)[:, None] - np.arange(M)[None, :])) * 2 * math.pi / M
        for _ in range(6):
            idx = rng.choice(M, size=int(rng.integers(1, 6)), replace=False)
            a = rng.uniform(0.0, 2.0 * L, size=len(idx))
            phi = (a[None, :] + L * dcirc[:, idx]).min(axis=1)      # L-Lipschitz on the circle
            for sign in (1.0, -1.0):
                if gap(sign * phi) > tent + 1e-9:
                    return False, dict(reason="a Lipschitz function on the circle has a larger Jensen gap than the tent")
                stats["lipschitz"] += 1
    return True, stats


# ----------------------------------------------------------------------------------------------
# XIII. Algorithms without a hint on the cube (theory report 11.16)
# ----------------------------------------------------------------------------------------------

def na_cube(n):
    """Hamming distance matrix of the n-cube (vertices = integers, bits = coordinates)."""
    N = 2 ** n
    idx = np.arange(N)
    pop = np.array([bin(x).count("1") for x in range(N)])
    return pop[idx[:, None] ^ idx[None, :]]


def na_rand_lipschitz(rng, n, u, D, kind):
    """A u-Lipschitz function on the n-cube: 0 upper envelope of random data, 1 lower envelope, 2 a convex
    combination of both, 3 a truncated cone on a flat background, 4 the Lipschitz regularisation of noise."""
    N = D.shape[0]
    m = int(rng.integers(1, 9))
    idx = rng.choice(N, size=min(m, N), replace=False)
    scale = u * n * float(rng.choice([0.2, 0.5, 1.0, 2.0]))
    v = rng.uniform(0, scale, size=len(idx))
    if kind == 0:
        return (v[:, None] + u * D[idx, :]).min(0)
    if kind == 1:
        return (v[:, None] - u * D[idx, :]).max(0)
    if kind == 2:
        a = (v[:, None] + u * D[idx, :]).min(0)
        b = (v[::-1][:, None] - u * D[idx, :]).max(0)
        lam = float(rng.uniform())
        return lam * a + (1 - lam) * b
    if kind == 3:
        return u * np.minimum(D[int(rng.integers(N))], int(rng.integers(0, n + 1))).astype(float)
    z = rng.normal(0, u * n * 0.3, size=N)
    return (z[:, None] + u * D).min(0)


def na_kl(a, b):
    r = 0.0
    if a > 0:
        r += a * math.log(a / b)
    if a < 1:
        r += (1 - a) * math.log((1 - a) / (1 - b))
    return r


def na_theta_na(u, e1):
    """min{KL(rho || 1/2) : KL(rho || p_u) <= e1}: the exponent of non-adaptive algorithms."""
    pu = 1 / (1 + math.exp(u))
    if e1 >= na_kl(0.5, pu):
        return 0.0
    lo, hi = pu, 0.5
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if na_kl(mid, pu) <= e1 else (lo, mid)
    return na_kl(lo, 0.5)


def na_theta_hint(u, e1):
    rho = (math.log(2 / (1 + math.exp(-u))) + e1) / u
    return na_kl(rho, 0.5) if rho < 0.5 else 0.0


def na_log_T(n, u, k):
    """ln T_n(k), T_n(k) = sum_j C(n,j) e^{-u (j-k)_+}: the least value of sum_x e^{-u dist(x, S)} over |S| >= |B(k)|."""
    terms = [math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) - u * max(j - k, 0) for j in range(n + 1)]
    mx = max(terms)
    return mx + math.log(sum(math.exp(t - mx) for t in terms))


def na_log_gamma2(logex, n, u, r):
    """ln Gamma'_n(r), Gamma'_n(r) = sum_{j<=r} C(n,j)(e^{u(r+1-j)} - 1) / T_n(r-1)  (Gamma'_n(0) = 0): the two-sided
    tail lemma (fifth referee)."""
    if r == 0:
        return -math.inf
    return logex[r] + n * math.log(2) - na_log_T(n, u, r - 1)


def na_log_gamma(logex, logball, n, r):
    """ln Gamma_n(r), Gamma_n(r) = sum_{j<=r} C(n,j)(e^{u(r+1-j)} - 1) / |B(n, r-1)|  (Gamma_n(0) = 0)."""
    if r == 0:
        return -math.inf
    return logex[r] + n * math.log(2) - logball[r - 1]


@conjecture("XIII.1 Tail lemma on the cube: for every u-Lipschitz psi, w = e^{-psi}, and every threshold t, w(x) <= t e^{u dist(x, {w <= t})} above the threshold, and sum_{w > t} (w - t) <= t sum_{j <= r} C(n,j)(e^{u(r+1-j)} - 1) whenever |{w > t}| <= |B(n,r)| (Harper); truncated cones attain equality")
def t_tail_lemma_cube(rng, trials):
    stats = dict(checks=0, tight=0, worst=0.0)
    for n in (4, 6, 8):
        N = 2 ** n
        D = na_cube(n)
        for u in (0.4, 1.0, 2.2):
            logex, logball = qc_cube_log_excess(n, u)
            exc = [N * math.exp(v) for v in logex]
            balls = [math.exp(v) for v in logball]
            for tr in range(max(5, trials // 12)):
                psi = na_rand_lipschitz(rng, n, u, D, tr % 5)
                if not (np.abs(psi[:, None] - psi[None, :]) <= u * D + 1e-9).all():
                    return False, dict(reason="generator is not Lipschitz")
                w = np.exp(-(psi - psi.min()))
                for t in np.unique(w)[:-1]:
                    above = w > t
                    m = int(above.sum())
                    dist = D[np.ix_(above, ~above)].min(axis=1)
                    if (w[above] > t * np.exp(u * dist) * (1 + 1e-9)).any():
                        return False, dict(reason="pointwise tail bound violated", n=n, u=u)
                    r = next(k for k in range(n + 1) if balls[k] >= m - 1e-9)
                    lhs = float((w[above] - t).sum())
                    mid = float(t * (np.exp(u * dist) - 1).sum())
                    rhs = t * exc[r]
                    if lhs > mid * (1 + 1e-9) or mid > rhs * (1 + 1e-9):
                        return False, dict(reason="tail lemma violated", n=n, u=u, size=m, radius=r, lhs=lhs, geometric=mid, ball=rhs)
                    stats["checks"] += 1
                    stats["tight"] += lhs >= rhs * (1 - 1e-9)
                    stats["worst"] = max(stats["worst"], lhs / rhs)
    if stats["tight"] == 0:
        return False, dict(reason="no instance attains the ball bound: the test has no power")
    return True, stats


@conjecture("XIII.2 Monte Carlo on the whole class: with t* the upper q-quantile of w under the uniform measure and r the least radius with |B(n,r)| >= 2^n q, E[w] <= E[min(w,t*)] (1 + Gamma_n(r)), Gamma_n(r) = sum_{j<=r} C(n,j)(e^{u(r+1-j)}-1)/|B(n,r-1)|; the same with Gamma'_n(r) = (numerator)/T_n(r-1) <= Gamma_n(r), T_n(k) = sum_j C(n,j) e^{-u(j-k)_+} (two-sided tail lemma: 2^n E min(w,t) >= t T_n(k) when |{w >= t}| >= |B(k)|); hence K/q uniform samples give ln Ahat - ln A >= -ln(2(1+Gamma'_n(r))) outside an event of probability e^{-K/8}; n^{-1} ln Gamma and n^{-1} ln Gamma' -> KL(rho || p_u) above p_u; below p_u the minimum of Gamma over r tends to 4 e^u (e^u - 1) > 0 (so the first bound is void at bounded accuracy) while n^{-1} ln Gamma' -> -KL(rho || p_u)")
def t_monte_carlo_whole_class(rng, trials):
    stats = dict(deterministic=0, simulated=0, min_margin=math.inf)
    for n in (5, 7, 9):
        N = 2 ** n
        D = na_cube(n)
        for u in (0.5, 1.3):
            logex, logball = qc_cube_log_excess(n, u)
            for tr in range(max(5, trials // 12)):
                psi = na_rand_lipschitz(rng, n, u, D, tr % 5)
                w = np.sort(np.exp(-(psi - psi.min())))[::-1]
                A = float(w.mean())
                for m in sorted({1, 2, 3, n + 1, N // 8, N // 3, N // 2, N - 1}):
                    if not 1 <= m <= N:
                        continue
                    q = m / N
                    tstar = float(w[m - 1])                       # sup{t : |{w >= t}| >= 2^n q}
                    r = next(k for k in range(n + 1) if math.exp(logball[k]) >= m - 1e-9)
                    G = math.exp(na_log_gamma(logex, logball, n, r)) if r > 0 else 0.0
                    trunc = float(np.minimum(w, tstar).mean())
                    if trunc < tstar * q * (1 - 1e-12) or A > trunc * (1 + G) * (1 + 1e-9):
                        return False, dict(reason="truncated mean does not control the mean", n=n, u=u, m=m, A=A, truncated=trunc, Gamma=G)
                    # two-sided lemma: |{w >= t*}| >= m > |B(r-1)|  =>  2^n E min(w,t*) >= t* T_n(r-1);  A <= (1 + Gamma') E min(w,t*)
                    G2 = math.exp(na_log_gamma2(logex, n, u, r)) if r > 0 else 0.0
                    if r > 0 and N * trunc < tstar * math.exp(na_log_T(n, u, r - 1)) * (1 - 1e-9):
                        return False, dict(reason="truncated mass below the Harper value of the ball", n=n, u=u, m=m)
                    if G2 > G * (1 + 1e-9) or A > trunc * (1 + G2) * (1 + 1e-9):
                        return False, dict(reason="two-sided tail lemma violated", n=n, u=u, m=m, A=A, truncated=trunc, Gamma2=G2)
                    stats["deterministic"] += 1
                    stats["min_margin"] = min(stats["min_margin"], trunc * (1 + G2) / A)
    # the probabilistic statement at cones (the extremal instances), n = 40, weights sampled through the binomial law
    # of the distance; small K, so that the Chernoff event does occur and a wrong constant would be seen
    n = 40
    reps, seen = 1500, 0.0
    pj = np.array([math.comb(n, j) for j in range(n + 1)], dtype=float) / 2.0 ** n
    cdf = np.cumsum(pj)
    for u, K, M in [(uu, KK, MM) for uu in (1.0, 4.0) for KK in (2.0, 4.0, 8.0) for MM in (200, 5000)]:
        logex, logball = qc_cube_log_excess(n, u)
        lnA = n * math.log((1 + math.exp(-u)) / 2)
        if True:
            r = next(k for k in range(n + 1) if logball[k] >= n * math.log(2) + math.log(K / M) - 1e-12)
            lg2 = na_log_gamma2(logex, n, u, r)
            j0 = int(np.searchsorted(cdf, K / M - 1e-15))            # t* = e^{-u j0}: the upper K/M-quantile of the weight
            tstar = math.exp(-u * j0)
            etrunc = float((pj * np.minimum(np.exp(-u * np.arange(n + 1)), tstar)).sum())
            dist = rng.binomial(n, 0.5, size=(reps, M))
            wts = np.exp(-u * dist)
            est = np.log(wts.mean(axis=1)) - lnA
            lower_end = math.log(0.5) - (math.log1p(math.exp(lg2)) if lg2 < 30 else lg2)
            if float((est < lower_end).mean()) > math.exp(-K / 8) + 4 * math.sqrt(math.exp(-K / 8) / reps):
                return False, dict(reason="Monte Carlo falls below the certified lower end too often", K=K, M=M)
            chern = float((np.minimum(wts, tstar).mean(axis=1) < 0.5 * etrunc).mean())   # the Chernoff event itself
            bound = math.exp(-K / 8)
            if chern > bound + 4 * math.sqrt(bound * (1 - bound) / reps):
                return False, dict(reason="truncated mean falls below half its expectation too often", K=K, M=M, frequency=chern, bound=bound)
            if float((est > math.log(1 / 0.05)).mean()) > 0.05 + 4 * math.sqrt(0.05 * 0.95 / reps):
                return False, dict(reason="Markov bound for the upper tail violated", K=K, M=M)
            seen = max(seen, chern)
            stats["simulated"] += 1
    if seen < 0.05:
        return False, dict(reason="the Chernoff event is too rare: the simulation has no power")
    stats["largest_chernoff_frequency"] = seen
    n, u = 2000, 1.0
    pu = 1 / (1 + math.exp(u))
    logex, logball = qc_cube_log_excess(n, u)
    for rho in (0.30, 0.38, 0.45):
        val = na_log_gamma(logex, logball, n, int(rho * n)) / n
        val2 = na_log_gamma2(logex, n, u, int(rho * n)) / n
        if abs(val - na_kl(rho, pu)) > 0.01 or abs(val2 - na_kl(rho, pu)) > 0.01:
            return False, dict(reason="exponent of Gamma_n differs from KL(rho || p_u)", rho=rho, value=val, kl=na_kl(rho, pu))
    for rho in (0.05, 0.15, 0.22):                         # below p_u: Gamma stays bounded away from 0, Gamma' vanishes
        val = na_log_gamma(logex, logball, n, int(rho * n)) / n
        val2 = na_log_gamma2(logex, n, u, int(rho * n)) / n
        if abs(val) > 0.01 or abs(val2 + na_kl(rho, pu)) > 0.01:
            return False, dict(reason="below p_u the exponents are not 0 and -KL(rho || p_u)", rho=rho, gamma=val, gamma2=val2)
    if min(na_log_gamma(logex, logball, n, r) for r in range(1, n + 1)) < math.log(4 * math.exp(u) * math.expm1(u)) - 0.05:
        return False, dict(reason="the minimum of Gamma_n is far below 4 e^u (e^u - 1): the first bound would not be void at bounded accuracy")
    return True, stats


@conjecture("XIII.3 Non-adaptive lower bound: the flattened cone max(u d(.,s), uR) is u-Lipschitz, differs from the cone exactly on the open ball {d(.,s) < R} and lowers ln Z by ln[(1+e^{-u})^n / sum_j C(n,j) e^{-u max(j,R)}]; a query set that misses that ball cannot separate the two (both lie between the McShane envelopes of the answers); every query set Q meets the balls of at most |Q| |B(n,R-1)| centres; a point with its n neighbours determines the centre of a cone; and n + 3 evaluations (the centre and its antipode in addition) certify a cone exactly while no other member of the class passes that test")
def t_nonadaptive_lower_bound(rng, trials):
    stats = dict(pairs=0, query_sets=0, centres=0, certificates=0)
    for n in (3, 5, 7, 8):
        N = 2 ** n
        D = na_cube(n)
        for u in (0.6, 1.5):
            for R in range(1, n + 1):
                s = int(rng.integers(N))
                cone = u * D[s].astype(float)
                flat = np.maximum(cone, u * R)
                if not (np.abs(flat[:, None] - flat[None, :]) <= u * D + 1e-9).all():
                    return False, dict(reason="flattened cone is not Lipschitz")
                diff = flat != cone
                if not (diff == (D[s] < R)).all():
                    return False, dict(reason="difference set is not the open ball", n=n, R=R)
                drop = math.log(float(np.exp(-cone).sum())) - math.log(float(np.exp(-flat).sum()))
                closed = n * math.log1p(math.exp(-u)) - math.log(sum(math.comb(n, j) * math.exp(-u * max(j, R)) for j in range(n + 1)))
                if abs(drop - closed) > 1e-9:
                    return False, dict(reason="closed form of the drop of ln Z is wrong", brute=drop, closed=closed)
                ball = sum(math.comb(n, j) for j in range(R))
                for _ in range(4):
                    Q = rng.choice(N, size=int(rng.integers(1, min(N, 12) + 1)), replace=False)
                    hit = int((D[np.ix_(Q, np.arange(N))] < R).any(axis=0).sum())      # centres whose ball Q meets
                    if hit > len(Q) * ball:
                        return False, dict(reason="a query set meets too many balls")
                    if not (D[s][Q] < R).any():
                        up = (cone[Q][:, None] + u * D[Q, :]).min(axis=0)
                        lo = (cone[Q][:, None] - u * D[Q, :]).max(axis=0)
                        if (flat > up + 1e-9).any() or (flat < lo - 1e-9).any() or (flat[Q] != cone[Q]).any():
                            return False, dict(reason="flattened cone is excluded by answers outside its ball")
                        width = math.log(float(np.exp(-lo).sum())) - math.log(float(np.exp(-up).sum()))
                        if width < drop - 1e-9:
                            return False, dict(reason="bracket narrower than the drop although the ball was missed")
                    stats["query_sets"] += 1
                stats["pairs"] += 1
            for _ in range(5):
                s, x0 = int(rng.integers(N)), int(rng.integers(N))
                cone = u * D[s].astype(float)
                rec = 0
                for i in range(n):
                    bit = x0 >> i & 1
                    rec |= (bit if cone[x0 ^ (1 << i)] > cone[x0] else 1 - bit) << i
                if rec != s:
                    return False, dict(reason="centre of a cone not recovered from n + 1 evaluations")
                stats["centres"] += 1

            def cone_certificate(g, x0):
                """n + 3 evaluations: x0, its neighbours, the candidate centre and its antipode.  Returns the centre if
                g(antipode) - g(centre) = u n (then both McShane envelopes of these two values coincide), else None."""
                cand = 0
                for i in range(n):
                    dg = g[x0 ^ (1 << i)] - g[x0]
                    if abs(abs(dg) - u) > 1e-9:
                        return None
                    bit = x0 >> i & 1
                    cand |= (bit if dg > 0 else 1 - bit) << i
                return cand if abs(g[cand ^ (N - 1)] - g[cand] - u * n) < 1e-9 else None

            for _ in range(6):
                s, x0 = int(rng.integers(N)), int(rng.integers(N))
                cone = u * D[s].astype(float) + float(rng.normal())
                if cone_certificate(cone, x0) != s:
                    return False, dict(reason="the adaptive certificate does not accept a cone")
                up = cone[s] + u * D[s]                                 # largest member with these two values ...
                lo = cone[s ^ (N - 1)] - u * D[s ^ (N - 1)]              # ... and the smallest: equal, so g is determined
                if np.abs(up - lo).max() > 1e-9 or np.abs(up - cone).max() > 1e-9:
                    return False, dict(reason="two evaluations do not determine a cone")
                others = [np.maximum(cone, cone[s] + u * int(rng.integers(1, n + 1))), na_rand_lipschitz(rng, n, u, D, int(rng.integers(5)))]
                for g in others:
                    acc = cone_certificate(g, x0)
                    if acc is not None and np.abs(g - (g[acc] + u * D[acc])).max() > 1e-9:
                        return False, dict(reason="the adaptive certificate accepts a member that is not a cone")
                stats["certificates"] += 1
    return True, stats


@conjecture("XIII.5 Certified bracket from two independent uniform samples of size M >= 2K: with t the ceil(K)-th largest weight of the first sample, Ahat_t the mean of min(w, t) over the second and r the least radius with |B(r)| >= 2^{n+1} K/M, the interval [Ahat_t/1.5, 2 Ahat_t + t (e^{Delta_r} - 1)] contains A outside an event of probability delta for K = 24 ln(4/delta), on every member of the class; at the zero residual its logarithmic width is ln(3/2) + ln(1 + e^{Delta_r})")
def t_certified_bracket(rng, trials):
    stats = dict(runs=0, misses=0, widest=0.0)
    n, u, delta = 40, 1.0, 0.2
    K = 24 * math.log(4 / delta)
    logex, logball = qc_cube_log_excess(n, u)
    pj = np.array([math.comb(n, j) for j in range(n + 1)], dtype=float) / 2.0 ** n
    jj = np.arange(n + 1)
    profiles = dict(zero=np.zeros(n + 1), cone=u * jj, truncated=u * np.minimum(jj, 12), flattened=u * np.maximum(jj, 14),
                    spike=u * np.minimum(jj, 3), far=u * np.abs(jj - 30.0))      # functions of the distance to a centre
    reps = 60 if trials < 200 else 300
    for name, psi in profiles.items():
        w_of = np.exp(-(psi - psi.min()))
        A = float((pj * w_of).sum())
        for M in (300, 3000, 30000):
            if M < 2 * K:
                continue
            r = next(k for k in range(n + 1) if logball[k] >= (n + 1) * math.log(2) + math.log(K / M) - 1e-12)
            tail = math.exp(logex[r]) if r > 0 else 0.0                     # e^{Delta_r} - 1 (dropped at r = 0)
            miss = 0
            for _ in range(reps):
                w1 = w_of[rng.binomial(n, 0.5, size=M)]
                w2 = w_of[rng.binomial(n, 0.5, size=M)]
                t = float(np.sort(w1)[-int(math.ceil(K))])
                ahat = float(np.minimum(w2, t).mean())
                lo_end, hi_end = ahat / 1.5, 2 * ahat + t * tail
                miss += not (lo_end <= A * (1 + 1e-12) and A <= hi_end * (1 + 1e-12))
                if name == "zero":
                    width = math.log(hi_end / lo_end)
                    if abs(width - (math.log(1.5) + math.log(2 + tail))) > 1e-9:
                        return False, dict(reason="width at the zero residual is not ln(3/2) + ln(1 + e^{Delta_r})", width=width)
                    stats["widest"] = max(stats["widest"], width)
            if miss / reps > delta:
                return False, dict(reason="certified bracket misses the truth too often", instance=name, M=M, misses=miss, runs=reps)
            stats["runs"] += reps
            stats["misses"] += miss
    return True, stats


@conjecture("XIII.4 Exponents without a hint on the cube: theta_na(eps1) = min{KL(rho||1/2) : KL(rho||p_u) <= eps1} is strictly above the hinted exponent KL((Lambda1+eps1)/u || 1/2) for 0 < eps1 < ln cosh(u/2) = KL(1/2||p_u), both vanish there, theta_na(0+) = KL(p_u||1/2); and at finite n the non-adaptive lower bound and the Monte Carlo upper bound are ordered and approach theta_na")
def t_exponents_without_hint(rng, trials):
    stats = dict(pairs=0, finite=0, max_gap=0.0)
    for u in (0.3, 0.5, 1.0, 2.0, math.log(16.0)):
        pu = 1 / (1 + math.exp(u))
        thr = math.log(math.cosh(u / 2))
        if abs(na_kl(0.5, pu) - thr) > 1e-12 or abs(na_theta_na(u, 0.0) - na_kl(pu, 0.5)) > 1e-7:
            return False, dict(reason="threshold or zero-accuracy value is wrong", u=u)
        for frac in (0.02, 0.1, 0.3, 0.5, 0.7, 0.9, 0.98):
            a, b = na_theta_hint(u, frac * thr), na_theta_na(u, frac * thr)
            if not 0 < a < b:
                return False, dict(reason="hinted exponent is not strictly below the non-adaptive one", u=u, frac=frac, hinted=a, nonadaptive=b)
            stats["pairs"] += 1
        if na_theta_na(u, thr * (1 + 1e-12)) != 0.0 or na_theta_hint(u, thr * (1 + 1e-12)) != 0.0 or na_theta_na(u, thr * (1 - 1e-6)) > 1e-9:
            return False, dict(reason="exponents do not vanish at the threshold", u=u)
    n = 1600 if trials < 200 else 6400
    d1 = d2 = dq = 0.05
    for u, frac in ((1.0, 0.25), (2.0, 0.5)):
        eps = n * frac * math.log(math.cosh(u / 2))
        logc = [math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) for j in range(n + 1)]
        logex, logball = qc_cube_log_excess(n, u)
        lz_cone = n * math.log1p(math.exp(-u))

        def lz_flat(R):
            terms = [logc[j] - u * max(j, R) for j in range(n + 1)]
            mx = max(terms)
            return mx + math.log(sum(math.exp(t - mx) for t in terms))

        Rstar = next(R for R in range(1, n + 1) if lz_cone - lz_flat(R) > eps)
        lower = (math.log(1 - 2 * dq) + n * math.log(2) - logball[Rstar - 1]) / n
        budget, r0, worst = eps - math.log(2 / d2), None, -math.inf
        for r in range(1, n + 1):
            g = na_log_gamma(logex, logball, n, r)
            worst = max(worst, g + math.log1p(math.exp(-g)) if g > 0 else math.log1p(math.exp(g)))
            if worst > budget:
                break
            r0 = r
        if r0 is None:
            return False, dict(reason="Monte Carlo bound is void at this size", n=n, u=u)
        upper = (math.log(8 * math.log(1 / d1)) + n * math.log(2) - logball[r0]) / n
        th = na_theta_na(u, frac * math.log(math.cosh(u / 2)))
        tol = 0.012 if n == 1600 else 0.004
        if not (lower <= upper + 1e-12 and abs(lower - th) < tol and abs(upper - th) < tol):
            return False, dict(reason="finite-n bounds are not ordered or far from the exponent", n=n, u=u, lower=lower, upper=upper, theta_na=th)
        stats["finite"] += 1
        stats["max_gap"] = max(stats["max_gap"], upper - lower)
    return True, stats


# ----------------------------------------------------------------------------------------------
# XIV. Correlated uncertainty: classes that are linear in features (theory report 11.17)
# ----------------------------------------------------------------------------------------------

def lc_span_bracket(F, theta0, w, A, v, y):
    """Primal and dual value of sup{ theta.F[y] : |theta - theta0| <= w, F[A] theta = v } (linear programs).
    Dual (Smolyak): min_lam [ lam.v + theta0.r + w.|r| ],  r = F[y] - F[A]^T lam."""
    from scipy.optimize import linprog
    p = F.shape[1]
    prim = linprog(-F[y], A_eq=F[A], b_eq=v, bounds=list(zip(theta0 - w, theta0 + w)), method="highs")
    k = len(A)
    # variables: lam (k, free), rp (p) >= 0, rm (p) >= 0;  rp - rm + F[A]^T lam = F[y]
    c = np.concatenate([v, theta0 + w, -theta0 + w])
    Aeq = np.hstack([F[A].T, np.eye(p), -np.eye(p)])
    dual = linprog(c, A_eq=Aeq, b_eq=F[y], bounds=[(None, None)] * k + [(0, None)] * (2 * p), method="highs")
    return (-prim.fun if prim.status == 0 else None), (dual.fun if dual.status == 0 else None)


@conjecture("XIV.1 Linear classes g = theta.F, |theta - theta0| <= w: without evaluations sup (g(x) - g(y)) = centre + sum_a w_a |F_a(x) - F_a(y)| (attained); after evaluations on A the largest consistent value at y is min_lam [lam.v + theta0.r + w.|r|] and the smallest max_lam [lam.v + theta0.r - w.|r|], r = F(y) - sum_i lam_i F(x_i) (linear-programming duality at both ends, also for data at a vertex of the box; every lam gives a valid bound); the width is at most twice the weighted l1 distance of F(y) to the span, with equality at the central data and strict inequality in general; the value is determined exactly when F(y) lies in the span of the evaluated feature vectors; and with a first-order remainder the upper end gains the transport term sum_i (lam_i^+ d(y,x_i) + lam_i^- d(x_i,y)) and the lower end the transposed one, for coefficients summing to one")
def t_linear_class_span_bracket(rng, trials):
    from scipy.optimize import linprog
    stats = dict(pairs=0, brackets=0, exact=0, nontrivial=0, remainder=0, narrower=0)
    for _ in range(max(20, trials // 4)):
        N, p = int(rng.integers(5, 12)), int(rng.integers(2, 6))
        F = rng.integers(-2, 4, size=(N, p)).astype(float)
        theta0 = rng.normal(0, 1, size=p)
        w = rng.uniform(0.0, 1.5, size=p) * (rng.uniform(size=p) < 0.85)
        for _ in range(4):
            x, y = int(rng.integers(N)), int(rng.integers(N))
            env = float((w * np.abs(F[x] - F[y])).sum())
            brute = max(float((np.array(sg) * w) @ (F[x] - F[y])) for sg in itertools.product((-1.0, 1.0), repeat=p))
            if abs(brute - env) > 1e-9:                                   # the supremum over the box is at a vertex
                return False, dict(reason="feature envelope differs from the largest difference over the vertices of the box", brute=brute, formula=env)
            for _ in range(5):
                th = theta0 + w * rng.uniform(-1, 1, size=p)
                if (th - theta0) @ (F[x] - F[y]) > env + 1e-9:
                    return False, dict(reason="a member of the class exceeds the feature envelope")
            stats["pairs"] += 1
        mode = int(rng.integers(3))                                  # 0 interior data, 1 central data, 2 data at a vertex of the box
        truth = theta0 + w * (rng.uniform(-1, 1, size=p) if mode == 0 else (np.zeros(p) if mode == 1 else rng.choice([-1.0, 1.0], size=p)))
        k = int(rng.integers(1, p + 1)) if rng.uniform() < 0.8 else int(rng.integers(1, min(N, p + 2)))   # mostly fewer evaluations than features
        A = [int(a) for a in rng.choice(N, size=k, replace=False)]
        v = F[A] @ truth
        rankA = np.linalg.matrix_rank(F[A])
        for y in range(N):
            up, dual = lc_span_bracket(F, theta0, w, A, v, y)
            lo_neg, dual_neg = lc_span_bracket(-F, theta0, w, A, -v, y)   # sup of -g(y) over the same coefficients, and its dual
            if up is None or dual is None or lo_neg is None or dual_neg is None:
                return False, dict(reason="linear program failed on a feasible instance")
            if abs(up - dual) > 1e-6 * (1 + abs(up)) or abs(lo_neg - dual_neg) > 1e-6 * (1 + abs(lo_neg)):
                return False, dict(reason="span bracket (dual) differs from the consistent range (primal)", primal=up, dual=dual)
            # the width is at most twice the weighted l1 distance to the span, with equality at the central data
            dist_lp = linprog(np.concatenate([np.zeros(k), w, w]), A_eq=np.hstack([F[A].T, np.eye(p), -np.eye(p)]), b_eq=F[y],
                              bounds=[(None, None)] * k + [(0, None)] * (2 * p), method="highs")
            if dist_lp.status != 0 or up + lo_neg > 2 * dist_lp.fun + 1e-6 or (mode == 1 and abs(up + lo_neg - 2 * dist_lp.fun) > 1e-6):
                return False, dict(reason="width is not bounded by twice the distance to the span (or not equal at central data)",
                                   width=up + lo_neg, distance=float(dist_lp.fun), mode=mode)
            stats["narrower"] += up + lo_neg < 2 * dist_lp.fun - 1e-6
            val = float(F[y] @ truth)
            if val > up + 1e-7 or val < -lo_neg - 1e-7:
                return False, dict(reason="true value outside the bracket")
            lam = rng.normal(0, 1, size=k)                           # any coefficients give a valid bound
            r = F[y] - F[A].T @ lam
            if val > lam @ v + theta0 @ r + w @ np.abs(r) + 1e-7 or val < lam @ v + theta0 @ r - w @ np.abs(r) - 1e-7:
                return False, dict(reason="a linear combination of evaluations gives an invalid bound")
            in_span = np.linalg.matrix_rank(np.vstack([F[A], F[y]])) == rankA
            if in_span:
                if up + lo_neg > 1e-6:
                    return False, dict(reason="value not determined although the feature vector is in the span", width=up + lo_neg)
                stats["exact"] += 1
            stats["nontrivial"] += up + lo_neg > 1e-6
            stats["brackets"] += 1
        # linear part plus a first-order remainder: the remainder is transported with the absolute coefficients
        Dm = rng.uniform(0.2, 2.0, size=(N, N))
        np.fill_diagonal(Dm, 0.0)
        for mid in range(N):
            Dm = np.minimum(Dm, Dm[:, [mid]] + Dm[[mid], :])
        rho = (rng.uniform(0, 1, size=N)[None, :] + Dm).min(axis=1)          # admissible: rho(x) - rho(y) <= Dm[x, y]
        lam = rng.normal(0, 1, size=k)
        lam += (1 - lam.sum()) / k
        transport = lambda co, pts, y: sum(max(l, 0.0) * Dm[y, a] + max(-l, 0.0) * Dm[a, y] for l, a in zip(co, pts))
        for y in range(N):
            r = F[y] - F[A].T @ lam
            if F[y] @ truth + rho[y] > lam @ (v + rho[A]) + theta0 @ r + w @ np.abs(r) + transport(lam, A, y) + 1e-7:
                return False, dict(reason="span bracket with a first-order remainder is violated")
            transposed = sum(max(l, 0.0) * Dm[a, y] + max(-l, 0.0) * Dm[y, a] for l, a in zip(lam, A))
            if F[y] @ truth + rho[y] < lam @ (v + rho[A]) + theta0 @ r - w @ np.abs(r) - transposed - 1e-7:
                return False, dict(reason="lower end of the span bracket with a remainder (transposed envelope) is violated")
            a = A[0]                                                    # one evaluated point: the bound is attained
            ext = theta0 + w * np.where(F[y] - F[a] >= 0, 1.0, -1.0)
            r1 = F[y] - F[a]
            lhs = F[y] @ ext + Dm[y, a]                                 # remainder rho = Dm[., a], rho(a) = 0
            rhs = F[a] @ ext + theta0 @ r1 + w @ np.abs(r1) + transport([1.0], [a], y)
            if abs(lhs - rhs) > 1e-9:
                return False, dict(reason="one-point bracket with a remainder is not attained", lhs=lhs, rhs=rhs)
            low = theta0 - w * np.where(F[y] - F[a] >= 0, 1.0, -1.0)   # lower end: remainder rho = -Dm[a, .], opposite vertex
            lower_term = lambda co, pts, yy: sum(max(l, 0.0) * Dm[b, yy] + max(-l, 0.0) * Dm[yy, b] for l, b in zip(co, pts))
            if abs((F[y] @ low - Dm[a, y]) - (F[a] @ low + theta0 @ r1 - w @ np.abs(r1) - lower_term([1.0], [a], y))) > 1e-9:
                return False, dict(reason="one-point lower bracket with a remainder is not attained with the transposed envelope")
        stats["remainder"] += 1
    if stats["exact"] == 0 or stats["nontrivial"] == 0 or stats["narrower"] == 0:
        return False, dict(reason="the test has no power (no exact, no open, or no bracket narrower than twice the distance)")
    return True, stats


@conjecture("XIV.2 Pair-additive residuals g(x) = sum_k phi(s_k) cnt_k(x) with phi = 0 at the cutoff and |phi(s_k) - phi(s_{k+1})| <= L (s_{k+1} - s_k): g(x) = sum_k (phi_k - phi_{k+1}) N_k(x) with N the cumulative pair counts; sup (g(x) - g(y)) = L sum_k Delta_k |N_k(x) - N_k(y)| (a transport distance between pair-distance distributions, attained); after evaluations the largest consistent value at y is min_lam [lam.v + L sum_k Delta_k |N_k(y) - sum_i lam_i N_k(x_i)|]; and for a radial function that vanishes at the cutoff and is nondecreasing, a configuration whose cumulative profile dominates another one has the smaller energy")
def t_pair_additive_profiles(rng, trials):
    from scipy.optimize import linprog
    stats = dict(identities=0, envelopes=0, brackets=0, open_brackets=0, dominances=0)
    for _ in range(max(8, trials // 6)):
        N, m = int(rng.integers(4, 10)), int(rng.integers(2, 8))
        L = float(rng.uniform(0.3, 2.0))
        grid = np.sort(rng.uniform(0.5, 6.0, size=m + 1))            # s_0 < ... < s_m = cutoff
        Delta = np.diff(grid)
        cnt = rng.integers(0, 5, size=(N, m)).astype(float)          # pairs at s_0..s_{m-1}
        j = int(rng.integers(m - 1))
        cnt[1] = cnt[0]                                              # configuration 1: one pair of configuration 0 moved outwards
        cnt[0, j] += 1.0
        cnt[1, j + 1] += 1.0
        cum = np.cumsum(cnt, axis=1)
        mono = np.concatenate([-np.cumsum(rng.uniform(0.1, 1, size=m)[::-1])[::-1], [0.0]])   # nondecreasing, zero at the cutoff
        e = cnt @ mono[:m]
        for x in range(N):
            for y in range(N):
                if (cum[x] >= cum[y]).all():
                    if e[x] > e[y] + 1e-9:
                        return False, dict(reason="a dominating profile has the larger energy under an attractive radial function")
                    stats["dominances"] += x != y
        incr = L * Delta * rng.uniform(-1, 1, size=m)                # phi_k - phi_{k+1}
        phi = np.concatenate([np.cumsum(incr[::-1])[::-1], [0.0]])   # phi_m = 0
        g = cnt @ phi[:m]
        if np.abs(g - cum @ incr).max() > 1e-9:
            return False, dict(reason="summation by parts fails")
        stats["identities"] += 1
        for _ in range(4):
            x, y = int(rng.integers(N)), int(rng.integers(N))
            env = float(L * (Delta * np.abs(cum[x] - cum[y])).sum())
            if g[x] - g[y] > env + 1e-9:
                return False, dict(reason="pair-additive residual exceeds the profile envelope")
            brute = max(float((np.array(sg) * L * Delta) @ (cum[x] - cum[y])) for sg in itertools.product((-1.0, 1.0), repeat=m))
            if abs(brute - env) > 1e-9:                               # extreme radial functions: increments +-L Delta_k
                return False, dict(reason="profile envelope differs from the supremum over the extreme radial functions", brute=brute, formula=env)
            stats["envelopes"] += 1
        k = int(rng.integers(1, min(N, m + 1)))
        A = [int(a) for a in rng.choice(N, size=k, replace=False)]
        v = g[A]
        for y in range(N):
            # primal: maximise incr'.cum[y] over |incr'_k| <= L Delta_k with cum[A] incr' = v
            prim = linprog(-cum[y], A_eq=cum[A], b_eq=v, bounds=list(zip(-L * Delta, L * Delta)), method="highs")
            c = np.concatenate([v, L * Delta, L * Delta])
            Aeq = np.hstack([cum[A].T, np.eye(m), -np.eye(m)])
            dual = linprog(c, A_eq=Aeq, b_eq=cum[y], bounds=[(None, None)] * k + [(0, None)] * (2 * m), method="highs")
            if prim.status != 0 or dual.status != 0:
                return False, dict(reason="linear program failed on a feasible instance")
            if abs(-prim.fun - dual.fun) > 1e-6 * (1 + abs(dual.fun)) or g[y] > dual.fun + 1e-7:
                return False, dict(reason="profile span bracket differs from the largest consistent value", primal=-prim.fun, dual=dual.fun)
            mcshane = min(v[i] + L * (Delta * np.abs(cum[y] - cum[a])).sum() for i, a in enumerate(A))
            if dual.fun > mcshane + 1e-7:
                return False, dict(reason="span bracket worse than McShane")
            stats["open_brackets"] += dual.fun < mcshane - 1e-6
            stats["brackets"] += 1
    if stats["open_brackets"] == 0:
        return False, dict(reason="linear combinations never improved on McShane: the test has no power")
    return True, stats


@conjecture("XIV.3 Linear-residual kernel (LinearKernel.lean): on a coefficient box [lo, hi] with nonnegative features, min_x (E0 + lo.F)(x) + lam.v - sum_a max(lo_a c_a, hi_a c_a), c = F(A)^T lam, is a lower bound on min_x (E0 + theta.F)(x) for every theta of the box that is consistent with the anchors, for every lam; on boxes that contradict the anchors the data term is unbounded; and on small boxes around a consistent theta the bound approaches the true minimum")
def t_linear_kernel_leaf(rng, trials):
    from scipy.optimize import linprog
    stats = dict(leaves=0, contradicted=0, tight=0, improved=0)
    for _ in range(max(10, trials // 5)):
        N, p = int(rng.integers(4, 17)), int(rng.integers(1, 4))
        E0 = rng.normal(0, 2, size=N)
        F = rng.integers(0, 4, size=(N, p)).astype(float)
        lo0 = rng.uniform(-2, 0.5, size=p)
        hi0 = lo0 + rng.uniform(0.5, 3, size=p)
        truth = lo0 + (hi0 - lo0) * rng.uniform(0.1, 0.9, size=p)
        A = [int(a) for a in rng.choice(N, size=int(rng.integers(1, 3)), replace=False)]
        v = F[A] @ truth

        def robust_min(lo, hi):
            """min over x and over theta in [lo, hi] with F[A] theta = v of E0[x] + F[x].theta (inf if no such theta)."""
            best = math.inf
            for x in range(N):
                res = linprog(F[x], A_eq=F[A], b_eq=v, bounds=list(zip(lo, hi)), method="highs")
                if res.status == 0:
                    best = min(best, E0[x] + res.fun)
                elif res.status != 2:
                    return None
            return best

        def leaf_bound(lo, hi, lam):
            c = F[A].T @ lam
            return float((E0 + F @ lo).min()) + float(lam @ v) - float(np.maximum(lo * c, hi * c).sum())

        for kind in range(4):
            if kind == 0:                                   # the whole box
                lo, hi = lo0.copy(), hi0.copy()
            elif kind == 1:                                 # a small box around the truth
                lo, hi = np.maximum(lo0, truth - 1e-3), np.minimum(hi0, truth + 1e-3)
            elif kind == 2:                                 # a random sub-box containing the truth
                lo = lo0 + (truth - lo0) * rng.uniform(size=p)
                hi = hi0 - (hi0 - truth) * rng.uniform(size=p)
            else:                                           # a sub-box that excludes the truth in one coordinate
                lo, hi = lo0.copy(), hi0.copy()
                a = int(rng.integers(p))
                hi[a] = lo0[a] + 0.5 * (truth[a] - lo0[a])
            true_min = robust_min(lo, hi)
            if true_min is None:
                return False, dict(reason="linear program failed")
            # best multipliers by linear programming: maximise lam.v - sum t, t >= lo c, t >= hi c, |lam| <= 50
            k = len(A)
            cost = np.concatenate([-v, np.ones(p)])
            Aub = np.vstack([np.hstack([lo[:, None] * F[A].T, -np.eye(p)]), np.hstack([hi[:, None] * F[A].T, -np.eye(p)])])
            res = linprog(cost, A_ub=Aub, b_ub=np.zeros(2 * p), bounds=[(-50, 50)] * k + [(None, None)] * p, method="highs")
            if res.status != 0:
                return False, dict(reason="multiplier program failed")
            lam_best = res.x[:k]
            for lam in (np.zeros(k), lam_best, rng.normal(0, 3, size=k)):
                b = leaf_bound(lo, hi, lam)
                if true_min < math.inf and b > true_min + 1e-6:
                    return False, dict(reason="leaf bound exceeds the robust minimum", bound=b, robust_min=true_min, kind=kind)
            b0, b1 = leaf_bound(lo, hi, np.zeros(k)), leaf_bound(lo, hi, lam_best)
            if true_min == math.inf:
                # Farkas: some multipliers separate the box from the data, and the data term is positively homogeneous
                # in them, so it is unbounded (the size of the gain at |lam| <= 50 depends on the margin of the contradiction)
                gain = b1 - b0
                if gain <= 1e-7:
                    return False, dict(reason="no multipliers separate a box that contradicts the anchors", gain=gain)
                far = leaf_bound(lo, hi, 1000.0 * lam_best) - b0
                if far < 999.0 * gain or abs(far - 1000.0 * gain) > 1e-6 * (1.0 + 1000.0 * gain):
                    return False, dict(reason="data term is not unbounded on a box that contradicts the anchors", gain=gain, far=far)
                stats["contradicted"] += 1
                stats["smallest_gain"] = min(stats.get("smallest_gain", math.inf), gain)
            if kind == 1:
                if true_min - b1 > 0.05 * (1 + float(np.abs(F).max())):
                    return False, dict(reason="bound on a small consistent box is far from the minimum", gap=true_min - b1)
                stats["tight"] += 1
            stats["improved"] += b1 > b0 + 1e-6
            stats["leaves"] += 1
    if stats["contradicted"] == 0 or stats["improved"] == 0:
        return False, dict(reason="the test has no power")
    return True, stats


def lc_square_lattice_walks(nbeads):
    """All self-avoiding walks with `nbeads` beads on the square lattice whose first step is (1, 0)."""
    walks, steps = [], ((1, 0), (-1, 0), (0, 1), (0, -1))

    def extend(path):
        if len(path) == nbeads:
            walks.append(list(path))
            return
        x, y = path[-1]
        for dx, dy in steps:
            q = (x + dx, y + dy)
            if q not in path:
                path.append(q)
                extend(path)
                path.pop()

    extend([(0, 0), (1, 0)])
    return walks


@conjecture("XIV.4 Pair-distance profiles on real chains (self-avoiding walks on the square lattice, squared distances, cutoff S_c): for an L-Lipschitz radial function with phi(S_c) = 0 the pair-additive energy is -int phi' N^x; the envelope L int |N^x - N^y| equals L times the l1 distance of the sorted squared distances truncated at the cutoff and the supremum over the extreme radial functions; mirror images and reversed chains have equal profiles; and (entropy lemma of Proposition 11.49) rounding a nondecreasing function of total mass M on [0, S] to G levels and G grid points changes it by at most 2SM/G in L1 and leaves at most C(2G, G) functions")
def t_profiles_on_chains(rng, trials):
    stats = dict(walks=0, profiles=0, pairs=0, rounded=0, worst_rounding=0.0)
    for nbeads, Sc in ((7, 5.0), (8, 5.0), (8, 10.0)):
        walks = lc_square_lattice_walks(nbeads)
        pairs = [(a, b) for a in range(nbeads) for b in range(a + 2, nbeads)]
        sq = np.array([[(wk[a][0] - wk[b][0]) ** 2 + (wk[a][1] - wk[b][1]) ** 2 for a, b in pairs] for wk in walks], dtype=float)
        grid = sorted(set(sq[sq < Sc].tolist())) + [Sc]                     # occurring squared distances below the cutoff, then the cutoff
        Delta = np.diff(grid)
        cum = np.array([[float((row <= g).sum()) for g in grid[:-1]] for row in sq])   # N^x on the cells [g_k, g_{k+1})
        L = float(rng.uniform(0.3, 2.0))
        stats["walks"] += len(walks)
        stats["profiles"] += len({tuple(c) for c in cum.tolist()})
        # an L-Lipschitz radial function, piecewise linear between the grid points, zero from the cutoff on
        incr = L * Delta * rng.uniform(-1, 1, size=len(Delta))              # phi(g_k) - phi(g_{k+1})
        phi_grid = np.concatenate([np.cumsum(incr[::-1])[::-1], [0.0]])
        phi = lambda t: float(np.interp(min(t, Sc), grid, phi_grid))
        for i in rng.choice(len(walks), size=min(len(walks), 40), replace=False):
            direct = sum(phi(t) for t in sq[i])
            if abs(direct - float(cum[i] @ incr)) > 1e-9:
                return False, dict(reason="pair-additive energy differs from the integral of the profile against -phi'")
        for _ in range(60):
            i, j = int(rng.integers(len(walks))), int(rng.integers(len(walks)))
            dP = L * float((Delta * np.abs(cum[i] - cum[j])).sum())
            sorted_l1 = L * float(np.abs(np.sort(np.minimum(sq[i], Sc)) - np.sort(np.minimum(sq[j], Sc))).sum())
            brute = max(float((np.array(sg) * L * Delta) @ (cum[i] - cum[j])) for sg in itertools.product((-1.0, 1.0), repeat=len(Delta)))
            if abs(dP - sorted_l1) > 1e-9 or abs(dP - brute) > 1e-9:
                return False, dict(reason="profile envelope differs from the sorted-distance form or from the supremum over radial functions",
                                   integral=dP, sorted=sorted_l1, brute=brute)
            stats["pairs"] += 1
        index = {tuple(map(tuple, wk)): t for t, wk in enumerate(walks)}
        for i in rng.choice(len(walks), size=min(len(walks), 30), replace=False):
            wk = walks[i]
            mirror = tuple((x, -y) for x, y in wk)
            last, prev = wk[-1], wk[-2]
            rev = [(x - last[0], y - last[1]) for x, y in reversed(wk)]      # reversed chain, rotated so that its first step is (1, 0)
            dx, dy = rev[1]
            rot = {(1, 0): lambda q: q, (-1, 0): lambda q: (-q[0], -q[1]), (0, 1): lambda q: (q[1], -q[0]), (0, -1): lambda q: (-q[1], q[0])}[(dx, dy)]
            rev = tuple(rot(q) for q in rev)
            for other in (mirror, rev):
                if other not in index or not np.array_equal(cum[index[other]], cum[i]):
                    return False, dict(reason="mirror image or reversed chain has a different profile")
    # entropy lemma: rounding to multiples of q = M/G and moving every jump up to the next of G grid points
    for _ in range(max(40, trials)):
        G, S, M = int(rng.integers(2, 9)), float(rng.uniform(1, 6)), float(rng.uniform(1, 10))
        kind = int(rng.integers(3))
        njump = int(rng.integers(1, 30))
        pos = np.sort(rng.uniform(0, S, size=njump)) if kind < 2 else np.sort((np.floor(rng.uniform(0, G, size=njump)) + 1e-6) * S / G)
        hts = rng.dirichlet(np.ones(njump)) * M * (1.0 if kind else rng.uniform(0.2, 1.0))
        ts = np.linspace(0, S, 4001)[:-1] + S / 8000                         # quadrature points
        Fv = np.array([hts[pos <= t].sum() for t in ts])
        q = M / G
        rounded = np.floor(Fv / q + 1e-12) * q
        levels = np.arange(1, G + 1) * q                                    # level l*q is first reached at the point u_l ...
        reach = np.array([ts[np.argmax(rounded >= lv - 1e-12)] if (rounded >= lv - 1e-12).any() else S for lv in levels])
        moved = np.minimum(np.ceil(reach / (S / G) - 1e-12) * (S / G), S)   # ... and the jump is moved up to the next grid point
        Fr = np.array([q * float((moved <= t).sum()) for t in ts])
        err = float(np.abs(Fv - Fr).mean() * S)
        if err > 2 * S * M / G * (1 + 1e-3) + 1e-9:
            return False, dict(reason="rounding error exceeds 2SM/G", error=err, bound=2 * S * M / G)
        stats["rounded"] += 1
        stats["worst_rounding"] = max(stats["worst_rounding"], err / (2 * S * M / G))
    if stats["profiles"] >= stats["walks"]:
        return False, dict(reason="every walk has its own profile: the fibres of the pseudometric were expected to be large")
    return True, stats

# ---------------------------------------------------------------------------------------------------------------
# XV. Adaptive algorithms without a hint (theory report 11.18): the level recursion and the two-level bracket
# ---------------------------------------------------------------------------------------------------------------

def lv_consts(u):
    """(p_u, Lambda1, eps*, a, h) of theory report 11.16 / 11.18."""
    pu = 1 / (1 + math.exp(u))
    lam = math.log(2 / (1 + math.exp(-u)))
    return pu, lam, math.log(math.cosh(u / 2)), na_kl(pu, 0.5), na_kl(lam / u, 0.5)


def lv_bracket_value(u, T, g, phi, beta, ngam=400):
    """sup over gamma >= beta of min(gamma, mu) + (1 - phi) T(gamma/(1 - phi)), mu = phi theta_na((g - beta)/phi),
    for a nonincreasing function T (the supremum is over [beta, max(beta, mu)])."""
    mu = phi * na_theta_na(u, (g - beta) / phi)
    top = max(beta, mu)
    gam = np.unique(np.concatenate([[beta, top], np.linspace(beta, top, ngam)]))
    return max(min(x, mu) + (1 - phi) * T(x / (1 - phi)) for x in gam), mu


@conjecture("XV.1 The identity behind the adaptive exponent (theory report 11.18): KL(rho||p_u) = KL(rho||1/2) + u rho - Lambda1, hence theta_hint(e) = theta_na(e + theta_hint(e)) on [0, eps*) and theta_na(h) = h with 0 < h < a; e + theta_hint(e) is nondecreasing, theta_hint lies above its tangent at 0, whose slope is above -1, theta_na is nonincreasing, at most a and vanishes continuously at eps*; and one step of the level recursion from theta_hint reproduces theta_hint at phi = g/(g + theta_hint(g)), beta -> 0, and is never below it for other parameters (theta_hint is a fixed point)")
def t_hint_identity(rng, trials):
    stats = dict(identities=0, steps=0, closest=math.inf, largest_slope=0.0)
    for _ in range(max(6, trials // 10)):
        u = float(rng.choice([0.1, 0.3, 1.0, 2.0, 4.0, 8.0]) * rng.uniform(0.8, 1.25))
        pu, lam, estar, a, h = lv_consts(u)
        hint = lambda e: na_theta_hint(u, e)
        # (a) the identity between the two relative entropies
        for rho in rng.uniform(1e-3, 1 - 1e-3, size=20):
            if abs(na_kl(rho, pu) - (na_kl(rho, 0.5) + u * rho - lam)) > 1e-12:
                return False, dict(reason="KL(rho||p_u) != KL(rho||1/2) + u rho - Lambda1", u=u, rho=float(rho))
        # (11.18.1) and the properties used by the convergence theorem
        if abs(na_theta_na(u, h) - h) > 1e-10 or not (0 < h < a) or abs(na_theta_na(u, 1e-16 * a) - a) > 1e-6 * a:
            return False, dict(reason="theta_na(h) != h or the order 0 < h < a = theta_na(0+) fails", u=u)
        es = np.concatenate([[0.0], np.sort(rng.uniform(0, 1, size=40))[:-1] * estar, [estar * (1 - 1e-9)]])
        prev_s, prev_na = -math.inf, math.inf
        slope0 = math.log((1 - lam / u) / (lam / u)) / u           # -theta_hint'(0)
        stats["largest_slope"] = max(stats["largest_slope"], slope0)
        if not slope0 < 1:
            return False, dict(reason="slope of theta_hint at 0 is not above -1", u=u)
        for e in es:
            th = hint(e)
            if abs(na_theta_na(u, e + th) - th) > 1e-10:
                return False, dict(reason="theta_na(e + theta_hint(e)) != theta_hint(e)", u=u, e=float(e))
            if e + th < prev_s - 1e-12 or th < h - slope0 * e - 1e-12 or th < -1e-15:
                return False, dict(reason="e + theta_hint(e) not nondecreasing, or theta_hint below its tangent at 0", u=u, e=float(e))
            na = na_theta_na(u, e)
            if na > a + 1e-12 or na > prev_na + 1e-12 or na < th - 1e-12:
                return False, dict(reason="theta_na not within [theta_hint, a] or not nonincreasing", u=u, e=float(e))
            prev_s, prev_na = e + th, na
            stats["identities"] += 1
        for x in (estar * (1 - 1e-6), estar, 1.5 * estar):        # continuity of theta_na at and beyond the threshold
            if na_theta_na(u, x) > 1e-5 * a:
                return False, dict(reason="theta_na does not vanish continuously at eps*", u=u)
        # (b) one step from theta_hint: equality at phi* with beta -> 0, never below for other parameters
        for _ in range(8):
            g = float(rng.uniform(0.02, 0.98)) * estar
            th = hint(g)
            val, mu = lv_bracket_value(u, hint, g, g / (g + th), 1e-9 * g)
            if abs(val - th) > 1e-7 * a or abs(mu - th * g / (g + th)) > 1e-7 * a:
                return False, dict(reason="the step with phi = g/(g + theta_hint) does not reproduce theta_hint", u=u, g=g, value=val, hint=th)
            phi = float(rng.uniform(0.01, 0.99))
            beta = g * float(rng.choice([1e-6, 1e-3, 0.05, 0.3, 0.7, 0.99]))
            val, _ = lv_bracket_value(u, hint, g, phi, beta, ngam=120)
            if val < th - 1e-9 * a:
                return False, dict(reason="a step from theta_hint goes below theta_hint", u=u, g=g, phi=phi, beta=beta, value=val, hint=th)
            stats["closest"] = min(stats["closest"], (val - th) / a)
            stats["steps"] += 1
    return True, stats


class LvRecursion:
    """T_1 = theta_na, T_{k+1} = min(T_k, R[T_k]) on a grid of accuracies (piecewise-linear interpolation)."""
    def __init__(self, u, G=120, P=48, B=18, C=48):
        self.u = u
        self.pu, self.lam, self.estar, self.a, self.h = lv_consts(u)
        self.g = np.unique(np.concatenate([np.geomspace(1e-4, 0.05, G // 3), np.linspace(0.05, 1.0, 2 * G // 3)])) * self.estar
        self.nax = np.concatenate([[0.0], np.geomspace(1e-9, 1.0, 3000) * self.estar])
        self.nay = np.array([self.a] + [na_theta_na(u, x) for x in self.nax[1:]])
        self.T = np.interp(self.g, self.nax, self.nay)
        self.hint = np.array([na_theta_hint(u, x) for x in self.g])
        self.P, self.B, self.C = P, B, C
        self.levels = 1
    def th_na(self, x):
        return np.interp(x, self.nax, self.nay, right=0.0)
    def Tv(self, x):
        out = np.interp(x, self.g, self.T, left=self.T[0], right=0.0)
        return np.where(x >= self.estar, 0.0, out)
    def step_value(self, g, phi, beta):
        """the bracket of (11.18.2) for arrays phi[P,1], beta[1,B]; returns the array of values [P,B]"""
        mu = phi * self.th_na((g - beta) / phi)
        top = np.maximum(mu, beta)
        frac = np.concatenate([np.linspace(0, 1, self.C), np.geomspace(1e-5, 1, 16)])[None, None, :]
        gam = beta[..., None] + (top - beta)[..., None] * frac
        val = np.minimum(gam, mu[..., None]) + (1 - phi)[..., None] * self.Tv(gam / (1 - phi)[..., None])
        return val.max(axis=2)
    def step(self):
        new = self.T.copy()
        for i, g in enumerate(self.g):
            phis = list(np.linspace(0.01, 0.99, self.P))
            th = self.hint[i]
            if th > 0:
                phis.append(g / (g + th))
            if g < self.h:
                phis.append(g / self.h)
            phi = np.array(phis)[:, None]
            beta = (g * np.geomspace(1e-5, 0.999, self.B))[None, :]
            new[i] = min(new[i], float(self.step_value(g, phi, beta).min()))
        self.T = np.minimum.accumulate(new)
        self.levels += 1


@conjecture("XV.2 Level recursion T_1 = theta_na, T_{k+1} = min(T_k, R[T_k]), R[T](g) = inf_{phi, beta} sup_{gamma >= beta} [min(gamma, phi theta_na((g - beta)/phi)) + (1 - phi) T(gamma/(1 - phi))]: the levels are nonincreasing in k and in the accuracy and never below theta_hint; the second level at vanishing accuracy is min_phi max((1 - phi) a, phi a + (1 - phi) theta_na(phi a/(1 - phi))), about a/2, and improves on theta_na by at least 10% up to half the threshold; step (iii) of the convergence proof, D_{k+1}(g) <= (1 - phi*(g)) max_{x <= g} D_k(x), holds; and after six levels the excess over theta_hint is below 3.5% of a (below 2% after nine)")
def t_level_recursion(rng, trials):
    stats = dict(runs=0, T2_over_a=0.0, worst_excess_after=0.0, levels=0)
    us = [1.0] if trials < 100 else [0.5, 1.0, 2.0]
    depth = 6 if trials < 100 else 9
    for u in us:
        r = LvRecursion(u)
        a, h, estar = r.a, r.h, r.estar
        # closed form of the second level at vanishing accuracy: min over phi of max((1-phi) a, phi a + (1-phi) theta_na(phi a/(1-phi)))
        phis = np.linspace(0.01, 0.99, 981)
        closed = min(max((1 - p) * a, p * a + (1 - p) * na_theta_na(u, p * a / (1 - p))) for p in phis)
        prev = r.T.copy()
        for k in range(2, depth + 1):
            r.step()
            if np.any(r.T > prev + 1e-12) or np.any(np.diff(r.T) > 1e-12):
                return False, dict(reason="the levels are not nonincreasing in k and in the accuracy", u=u, k=k)
            if np.any(r.T < r.hint - 2e-4 * a):
                return False, dict(reason="a level of the recursion is below the hinted exponent", u=u, k=k, deficit=float(np.max(r.hint - r.T)) / a)
            if k == 2:
                t2 = float(r.T[0])
                stats["T2_over_a"] = t2 / a
                if abs(t2 - closed) > 0.02 * a or not (t2 < 0.56 * a):
                    return False, dict(reason="second level at small accuracy is not the closed form (about a/2)", u=u, T2=t2 / a, closed=closed / a)
                # adaptivity helps: strictly below theta_na for accuracies up to half the threshold
                mask = r.g <= 0.5 * estar
                if np.any(r.T[mask] > 0.9 * prev[mask]):
                    return False, dict(reason="the second level does not improve on theta_na by 10% below eps*/2", u=u)
            # the contraction used in the proof, step (iii): D_{k+1}(g) <= (1 - phi*(g)) max_{x <= g} D_k(x) (up to interpolation error)
            D_prev = np.maximum.accumulate(prev - r.hint)
            fac = r.hint / (r.g + r.hint + 1e-300)
            if np.any((r.T - r.hint) > fac * D_prev + 3e-3 * a):
                return False, dict(reason="step (iii) of the convergence proof fails numerically", u=u, k=k)
            prev = r.T.copy()
        excess = float(np.max(r.T - r.hint)) / a
        stats["worst_excess_after"] = max(stats["worst_excess_after"], excess)
        stats["levels"] = depth
        if excess > (0.035 if depth == 6 else 0.02):
            return False, dict(reason="the recursion does not approach the hinted exponent", u=u, excess=excess, depth=depth)
        stats["runs"] += 1
    return True, stats


def lv_ball_tables(n, u):
    """|B(n, r)| for r = -1..n (index r + 1) and E_r(n) = sum_{j <= r} C(n, j) (e^{u (r + 1 - j)} - 1) for r = 0..n."""
    binom = [math.comb(n, j) for j in range(n + 1)]
    ball = [0] + list(np.cumsum(binom))
    E = [sum(binom[j] * (math.exp(u * (r + 1 - j)) - 1) for j in range(r + 1)) for r in range(n + 1)]
    return ball, E


def lv_two_level(rng, vals, probs, s0, n_o, n, u, b, G, K, mode, step=0.5):
    """Outer loop of the two-level algorithm of Theorem 11.52.  The fibre average of a uniform outer point takes the
    value vals[t] with probability probs[t] (all 2^{n_o} points with equal weights, or the shells of a radial outer
    landscape).  The inner procedure is simulated: a call at accuracy x returns a bracket [L, U], U = L e^x, around the
    true value, placed at random (mode 0), with the value at its top (1) or at its bottom (2).  Returns a record."""
    ball, E = lv_ball_tables(n_o, u)
    No = 2 ** n_o
    J = math.ceil(2 * u * n + b + n_o * math.log(2) + 10)
    xs = np.array(list(np.arange(2 * u * (n - n_o), b, -step)) + [b * (1 - 1e-9)])   # ladder of inner accuracies, ending below b
    cdf = np.cumsum(probs)
    Wl = np.zeros(0); L = np.zeros(0); U = np.zeros(0); acc = np.zeros(0, dtype=np.int64)
    ell = s0
    levels = []                                                      # (s_j, M_j, q_j, populated, ell at entry)
    for j in range(J + 1):
        s = s0 * math.exp(j)
        ell_in = ell
        Mneg = 2 * K * J * math.e * s / (ell_in * math.exp(b))
        M = K
        while True:
            if len(Wl) < M:                                           # extend the list of independent uniform outer points
                extra = M - len(Wl)
                Wl = np.concatenate([Wl, vals[np.minimum(np.searchsorted(cdf, rng.uniform(size=extra)), len(vals) - 1)]])
                L = np.concatenate([L, np.zeros(extra)]); U = np.concatenate([U, np.full(extra, np.inf)])
                acc = np.concatenate([acc, np.full(extra, -1, dtype=np.int64)])
            while True:                                               # classify the first M points at this level
                und = np.nonzero((U[:M] > s) & (L[:M] <= s * math.exp(-b)))[0]
                if len(und) == 0:
                    break
                if np.any(acc[und] >= len(xs) - 1):
                    return dict(error="classification does not end at the last accuracy of the ladder")
                acc[und] += 1
                x = xs[acc[und]]
                t = rng.uniform(size=len(und)) if mode == 0 else (np.ones(len(und)) if mode == 1 else np.zeros(len(und)))
                L[und] = np.maximum(L[und], Wl[und] * np.exp(-t * x))
                U[und] = np.minimum(U[und], Wl[und] * np.exp((1 - t) * x))
            N = int((U[:M] > s).sum())                                # the points that are not low are high
            q = min(1.0, 2 * max(N, K) / M)
            if N >= K:
                ell = max(ell, s * math.exp(-b) * N / (2 * M))
            if No * q < 1:
                tail, r = 0.0, -1
            else:
                r = next(rr for rr in range(n_o + 1) if ball[rr + 1] >= No * q)
                # the tail lemma needs a point outside the super-level set: no closure while the ball is the whole cube
                tail = s * E[r] / No if r < n_o else math.inf
            if tail <= math.exp(G) * ell:
                upper = s0 + sum(lv[0] * math.e * lv[2] for lv in levels) + tail
                return dict(ell=ell, upper=upper, levels=levels, last=(s, M, q, r, tail), J=J, Wl=Wl)
            if N >= K or M >= Mneg:
                levels.append((s, M, q, N >= K, ell_in))
                break
            M *= 2
    return dict(error="no closure within J levels")


def lv_check_run(run, vals, probs, s0, n_o, n, u, b, G, K, stats):
    """The statements of the proof of Theorem 11.52 on one run: validity, width, sample sizes, counts."""
    A = float((vals * probs).sum())
    J, ell, upper = run["J"], run["ell"], run["upper"]
    if not (ell <= A * (1 + 1e-12) and A <= upper * (1 + 1e-12)):
        return dict(reason="the bracket of the two-level algorithm does not contain the mean", ell=ell, A=A, upper=upper, b=b)
    width = math.log(upper / ell)
    if width > G + math.log(4 * math.e * J + 3) + 1e-9:
        return dict(reason="the bracket is wider than g n + ln(4 e J + 3)", width=width, bound=G + math.log(4 * math.e * J + 3))
    stats["widest"] = max(stats["widest"], width - G)
    ball, E = lv_ball_tables(n_o, u)
    gam = [math.exp(u) - 1] + [E[r] / ball[r] for r in range(1, n_o + 1)]              # Gamma~(r) = E_r / |B(r - 1)|
    rdag = -1
    while rdag + 1 <= n_o - 1 and gam[rdag + 1] <= math.exp(G - b) / 4:
        rdag += 1
    Mdag = 2 * K * 2 ** n_o / ball[rdag + 1] if rdag >= 0 else math.inf     # no bound on the samples if even Gamma~(0) is too large
    exceed = lambda thr: float(probs[vals > thr].sum())
    Wl = run["Wl"]
    seq = run["levels"] + [(run["last"][0], run["last"][1], run["last"][2], None, ell)]
    for jj, (s, M, q, pop, ell_in) in enumerate(seq):
        if exceed(s) > q + 1e-12:
            return dict(reason="a certified exceedance probability is too small", level=jj, p=exceed(s), q=q)
        if M > 8 * J * math.e ** 2 * Mdag:
            return dict(reason="a sample is larger than 8 J e^2 M_dagger", level=jj, M=M, Mdag=Mdag)
        if rdag >= 0:
            stats["largest_M"] = max(stats["largest_M"], M / (8 * J * math.e ** 2 * Mdag))
        Mneg = 2 * K * J * math.e * s / (ell_in * math.exp(b))
        if M > max(K, 2 * Mneg):
            return dict(reason="a sample is larger than twice the negligibility threshold", level=jj)
        for i, (si, Mi, qi, popi, _) in enumerate(run["levels"][:jj]):
            if si * qi > 4 * math.exp(b) * ell_in * (1 + 1e-12):
                return dict(reason="an earlier level violates s_i q_i <= 4 e^b ell", level=jj, earlier=i)
        x, checks = b, 0
        while s * math.exp(-x) >= s0 * (1 - 1e-12):
            bound = 8 * K * J * math.e ** 2 * math.exp(x)
            lhs = Mneg * exceed(s * math.exp(-x))
            if lhs > bound * (1 + 1e-9):
                return dict(reason="the count of points close to a level exceeds 8 K J e^2 e^x", level=jj, x=x, lhs=lhs, bound=bound)
            stats["tightest_count"] = max(stats["tightest_count"], lhs / bound)
            if checks < 6 and jj >= len(seq) - 5:
                cnt = int((Wl[:M] > s * math.exp(-x)).sum())
                if cnt > 4 * bound + 4 * K:
                    return dict(reason="more sampled points close to a level than 32 K J e^2 e^x + 4K", level=jj, x=x, count=cnt)
                checks += 1
            x += 1.0
        if pop is not None:
            stats["populated" if pop else "negligible"] += 1
    stats["most_levels"] = max(stats["most_levels"], len(seq))
    stats["runs"] += 1
    return None


def lv_radial_instance(rng, n_o, u, kind):
    """Fibre averages that depend on the outer distance d to a centre: (values over d = 0..n_o, binomial probabilities)."""
    d = np.arange(n_o + 1)
    if kind == 0:
        F = np.zeros(n_o + 1)                                         # flat
    elif kind == 1:
        F = -u * np.maximum(int(rng.integers(2, 5)) - d, 0)           # flat bulk with a bump
    elif kind == 2:
        F = u * d.astype(float)                                       # cone
    else:
        F = u * np.minimum(d, int(rng.integers(1, n_o // 2))).astype(float)   # flattened cone
    probs = np.array([math.comb(n_o, int(k)) for k in d], dtype=float) / 2.0 ** n_o
    return np.exp(-F + float(rng.uniform(-2, 2))), probs


@conjecture("XV.3 Two-level bracket of Theorem 11.52, outer loop with a simulated inner procedure (valid brackets of the requested accuracy, placed adversarially): on arbitrary Lipschitz functions of a small cube and on steep radial outer landscapes the bracket contains the mean and is at most G + ln(4eJ + 3) wide; every certified exceedance probability is valid; no sample exceeds 8 J e^2 M_dagger or twice the negligibility threshold; earlier levels satisfy s_i q_i <= 4 e^b ell; the count of points within a factor e^x of a level obeys M_neg p(s e^{-x}) <= 8 K J e^2 e^x; levels are left as populated and as negligible; and the closure test is not applied while the ball of the tail lemma is the whole cube")
def t_two_level_logic(rng, trials):
    stats = dict(runs=0, widest=0.0, tightest_count=0.0, most_levels=0, largest_M=0.0, populated=0, negligible=0)
    # (i) arbitrary Lipschitz functions on a small cube, all fibre averages enumerated
    n_o, n_i, u = 6, 4, 1.0
    n = n_o + n_i
    D = na_cube(n)
    for rep in range(max(6, trials // 10)):
        kind = rep % 6
        psi = na_rand_lipschitz(rng, n, u, D, kind) if kind < 5 else u * D[int(rng.integers(2 ** n))].astype(float)
        psi = psi + float(rng.uniform(-3, 3))
        vals = np.exp(-psi).reshape(2 ** n_o, 2 ** n_i).mean(axis=1)   # the outer coordinates are the high bits
        probs = np.full(2 ** n_o, 2.0 ** -n_o)
        s0 = math.exp(-float(psi[int(rng.integers(2 ** n))]) - u * n)  # one query at a reference point
        if not (s0 <= vals.min() * (1 + 1e-12) and vals.max() <= s0 * math.exp(2 * u * n) * (1 + 1e-12)):
            return False, dict(reason="the reference level is not below all fibre averages")
        b = float(rng.choice([1.0, 2.0, 4.0]))
        G = b + math.log(4 * (math.exp(u) - 1)) + float(rng.choice([0.5, 2.0, 4.0]))
        K = math.ceil(24 * math.log(2 ** (n + 6) * n ** 3 / 0.05))
        run = lv_two_level(rng, vals, probs, s0, n_o, n, u, b, G, K, mode=rep % 3)
        if "error" in run:
            return False, dict(reason=run["error"], kind=kind)
        bad = lv_check_run(run, vals, probs, s0, n_o, n, u, b, G, K, stats)
        if bad:
            return False, dict(bad, kind=kind, part=1)
    # (ii) radial outer landscapes with a steep slope and an accuracy so small that the first level above the bulk
    # cannot be closed before it is declared negligible (K below the value of the proof: the events of the proof
    # still hold with overwhelming probability, and the run is fixed by the seed)
    n_o, n_i, u, K = 12, 2, 4.0, 200
    n = n_o + n_i
    ball, E = lv_ball_tables(n_o, u)
    for rep in range(2 if trials < 100 else 8):
        vals, probs = lv_radial_instance(rng, n_o, u, (0, 1, 0, 1, 2, 3, 2, 3)[rep])
        b = float(rng.choice([2.0, 4.0]))
        # a reference level well below the bulk, as at large n; on the flat landscape the bulk sits at e^{0.9} times a level
        s0 = float(vals.min()) * math.exp(-b - (3.9 if rep % 2 == 0 and rep < 4 else float(rng.uniform(3, 4))))
        J = math.ceil(2 * u * n + b + n_o * math.log(2) + 10)
        r_neg = next(rr for rr in range(n_o + 1) if ball[rr + 1] >= 2 ** n_o / (2 * J * math.e ** 2))
        G = b + math.log(2 * math.e * E[r_neg] / 2 ** n_o) - 0.3
        if G <= b:
            return False, dict(reason="parameters of the test: no accuracy between the tolerance and the closure threshold")
        run = lv_two_level(rng, vals, probs, s0, n_o, n, u, b, G, K, mode=1 + rep % 2)
        if "error" in run:
            return False, dict(reason=run["error"], kind=rep, part=2)
        bad = lv_check_run(run, vals, probs, s0, n_o, n, u, b, G, K, stats)
        if bad:
            return False, dict(bad, kind=rep, part=2)
    if stats["negligible"] == 0 or stats["populated"] == 0:
        return False, dict(reason="the test has no power", **stats)
    return True, stats


def lv_radial_profile(rng, n, u, kind):
    """A radial profile f(0..n) with |f(j+1) - f(j)| <= u: 0 random walk, 1 two-periodic in the middle with steep caps,
    2 the alternating profile, 3 flat with a dip, 4 cone flattened at a random radius, 5 two-periodic with random caps."""
    if kind == 0:
        f = np.concatenate([[0.0], np.cumsum(rng.uniform(-u, u, size=n))])
    elif kind in (1, 5):
        amp = float(rng.uniform(0, u))
        f = np.array([amp * (j % 2) for j in range(n + 1)], dtype=float)
        w = int(rng.integers(1, n // 3))
        for j in range(w - 1, -1, -1):                                # caps: as steep as allowed (1) or random (5)
            f[j] = f[j + 1] - (u if kind == 1 else float(rng.uniform(-u, u)))
            f[n - j] = f[n - j - 1] - (u if kind == 1 else float(rng.uniform(-u, u)))
    elif kind == 2:
        f = np.array([(u / 2) * (-1) ** j for j in range(n + 1)])
    elif kind == 3:
        R = int(rng.integers(1, n // 3))
        f = -u * np.maximum(R - np.arange(n + 1), 0).astype(float)
    else:
        f = u * np.minimum(np.arange(n + 1), int(rng.integers(0, n + 1))).astype(float)
    return f + float(rng.uniform(-2, 2))


def lv_radial_algorithm(rng, n, f, s, M):
    """The algorithm of Theorem 11.51 on psi(x) = f(dist(x, s)), x in {0..2^n - 1}: returns (branch, value, queries, sample)."""
    psi = lambda x: f[bin(x ^ s).count("1")]
    xs = [int(v) for v in rng.integers(0, 2 ** n, size=M)]
    queries = 0
    for x in xs:
        nb = [psi(x ^ (1 << i)) for i in range(n)]
        queries += n + 1
        vals = sorted(set(nb))
        if len(vals) >= 2:
            if len(vals) > 2:
                return "error", None, queries, xs
            c = x
            for i in range(n):                                        # flip the coordinates of one of the two value classes
                if nb[i] == vals[0]:
                    c ^= 1 << i
            F, y = [psi(c)], c                                        # a monotone path from c to its antipode
            for i in range(n):
                y ^= 1 << i
                F.append(psi(y))
            queries += n + 1
            logs = [math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) - F[k] for k in range(n + 1)]
            mx = max(logs)
            return "exact", mx + math.log(sum(math.exp(t - mx) for t in logs)) - n * math.log(2), queries, xs
    alpha, beta = psi(xs[0]), psi(xs[0] ^ 1)
    return "bracket", math.log((math.exp(-alpha) + math.exp(-beta)) / 2), queries, xs


def lv_radial_bracket(n, u, r, binom, ball):
    """[1 - 4B/2^n, 1 + 4 E_{r-2}(n)/2^n + 8B/2^n], B = |B(n, r-2)|: the bracket of A/A_0 in the proof of Theorem 11.51."""
    B = float(ball[r - 2])
    E = sum(binom[j] * (math.exp(u * (r - 1 - j)) - 1) for j in range(r - 1))            # E_{r-2}(n)
    return 1 - 4 * B / 2 ** n, 1 + 4 * E / 2 ** n + 8 * B / 2 ** n


@conjecture("XV.4 Radial instances psi = f(dist(., s)) (Theorem 11.51): two distinct neighbour values at a sampled point reveal the centre or its antipode, a monotone path then gives ln A exactly with at most (n+1) M + 2n + 1 evaluations; otherwise, if every shell r..n-r was sampled and the first point lies in [r-1, n-r+1], the profile is two-periodic there and A/A_0 lies in [1 - 4B/2^n, 1 + 4 (e^{Delta_{r-2}} - 1) + 8B/2^n], B = |B(n, r-2)|; the alternating profile is never resolved by neighbour values")
def t_radial_adaptive(rng, trials):
    stats = dict(exact=0, brackets=0, good=0, tightest_upper=0.0, widest=0.0)
    n = 16
    binom = [math.comb(n, j) for j in range(n + 1)]
    ball = np.cumsum(binom)
    for rep in range(max(12, trials // 3)):
        u = float(rng.choice([0.5, 1.0, 2.0]))
        kind = rep % 6
        f = lv_radial_profile(rng, n, u, kind)
        if np.max(np.abs(np.diff(f))) > u + 1e-12:
            return False, dict(reason="the test profile is not Lipschitz")
        s = int(rng.integers(0, 2 ** n))
        M = int(rng.choice([4, 16, 64, 256]))
        logA = math.log(sum(binom[j] * math.exp(-f[j]) for j in range(n + 1))) - n * math.log(2)
        branch, val, queries, xs = lv_radial_algorithm(rng, n, f, s, M)
        if branch == "error" or queries > (n + 1) * M + 2 * n + 1:
            return False, dict(reason="more than two neighbour values at a point of a radial function, or too many queries", kind=kind)
        if branch == "exact":
            if abs(val - logA) > 1e-9:
                return False, dict(reason="the exact branch of the radial algorithm is wrong", kind=kind, value=val, truth=logA)
            stats["exact"] += 1
            continue
        stats["brackets"] += 1
        # the bracket of the proof holds whenever every shell r..n-r was sampled and the first point lies in [r-1, n-r+1]
        dist = [bin(x ^ s).count("1") for x in xs]
        seen = set(dist)
        r = next((rr for rr in range(2, n // 2 + 1) if all(j in seen for j in range(rr, n - rr + 1))), None)
        if r is None or not (r - 1 <= dist[0] <= n - r + 1):
            continue
        stats["good"] += 1
        lo, hi = lv_radial_bracket(n, u, r, binom, ball)
        ratio = math.exp(logA - val)
        if not (lo * (1 - 1e-12) <= ratio <= hi * (1 + 1e-12)):
            return False, dict(reason="the bracket of the radial algorithm fails on its good event", kind=kind, ratio=ratio, lo=lo, hi=hi, r=r)
        stats["tightest_upper"] = max(stats["tightest_upper"], (ratio - 1) / (hi - 1))
        stats["widest"] = max(stats["widest"], math.log(hi / max(lo, 1e-300)) if lo > 0 else math.inf)
    if stats["exact"] == 0 or stats["good"] == 0:
        return False, dict(reason="the test has no power", **stats)
    # the bound on the caps is within a constant of the truth: a constant middle part with the steepest caps
    for r in range(2, 7):
        for u in (1.0, 3.0):
            f = np.zeros(n + 1)
            for j in range(r - 2, -1, -1):
                f[j] = f[j + 1] - u
                f[n - j] = f[n - j - 1] - u
            ratio = sum(binom[j] * math.exp(-f[j]) for j in range(n + 1)) / 2 ** n      # A / A_0 with A_0 = 1
            lo, hi = lv_radial_bracket(n, u, r, binom, ball)
            if not (lo <= ratio <= hi):
                return False, dict(reason="the bracket of the radial algorithm fails for the steepest caps", r=r, u=u, ratio=ratio, hi=hi)
            stats["tightest_upper"] = max(stats["tightest_upper"], (ratio - 1) / (hi - 1))
    if stats["tightest_upper"] < 0.3:
        return False, dict(reason="the bound on the caps is never within a factor 3 of the truth", **stats)
    # the alternating profile is never resolved by neighbours: the second branch is needed
    f = np.array([(1.0 / 2) * (-1) ** j for j in range(n + 1)])
    if lv_radial_algorithm(rng, n, f, 5, 64)[0] != "bracket":
        return False, dict(reason="the alternating profile was resolved by neighbour values")
    return True, stats


# ----------------------------------------------------------------------------------------------
# XVI. Every bounded accuracy: the two-sided ratio, the level at accuracy zero, Algorithm 2L+ (theory report 11.19)
# ----------------------------------------------------------------------------------------------

def ba_exact_tables(m, u, rmax):
    """Exact tables on Q_m: binom, ball[r + 1] = |B(m, r)| (python integers), E_r(m) for r <= rmax, and T_m(k)."""
    binom = [math.comb(m, j) for j in range(m + 1)]
    ball = [0] + list(itertools.accumulate(binom))
    E = [math.fsum(binom[j] * (math.exp(u * (r + 1 - j)) - 1) for j in range(r + 1)) for r in range(rmax + 1)]
    T = lambda k: math.fsum(binom[j] * math.exp(-u * max(j - k, 0)) for j in range(m + 1))
    return binom, ball, E, T


def ba_kappa(ball, c_eta, r):
    """kappa(r): the largest k >= 0 with |B(m, k)| <= max{1, c_eta |B(m, r - 1)|} (c_eta a Fraction: exact)."""
    target = max(Fraction(1), c_eta * ball[r])
    k = 0
    while ball[k + 2] <= target:
        k += 1
    return k


@conjecture("XVI.1 Lemma 11.55 on exact tables of Q_m: the one-sided ratio Gamma~(r) = E_r/|B(r-1)| is at most 2 e^u m for r <= p_u (m+1) and is never small (at least e^u (e^u - 1) for 1 <= r <= m/2); kappa(r) >= r - 1 - m_0, m_0 = ceil(ln(1/c_eta)/u); and the two-sided ratio Gamma''(r) = E_r/T_m(kappa(r)) is at most 2 e^{u (m_0 + 2)} P(Bin(m, p_u) <= r) for r <= p_u m, hence exponentially small in (p_u m - r)^2/m")
def t_two_sided_ratio(rng, trials):
    stats = dict(cases=0, largest_a=0.0, largest_b=0.0, smallest_one_sided=math.inf)
    for m in ((20, 57, 150) if trials < 100 else (20, 57, 150, 400)):
        for u in (0.5, 1.0, 2.0):
            pu = 1 / (1 + math.exp(u))
            binom, ball, E, T = ba_exact_tables(m, u, m // 2)
            binle = list(itertools.accumulate(binom[j] * pu ** j * (1 - pu) ** (m - j) for j in range(m + 1)))
            gam1 = [math.exp(u) - 1] + [E[r] / ball[r] for r in range(1, m // 2 + 1)]
            for r in range(0, int(pu * (m + 1)) + 1):
                stats["largest_a"] = max(stats["largest_a"], gam1[r] / (2 * math.exp(u) * m))
                if gam1[r] > 2 * math.exp(u) * m * (1 + 1e-12):
                    return False, dict(reason="Gamma~(r) > 2 e^u m at a radius below p_u (m+1)", m=m, u=u, r=r)
            low = min(gam1[1:])
            stats["smallest_one_sided"] = min(stats["smallest_one_sided"], low / (math.exp(u) * (math.exp(u) - 1)))
            if low < math.exp(u) * (math.exp(u) - 1):
                return False, dict(reason="the one-sided ratio is small somewhere", m=m, u=u, value=low)
            for eta in (0.25, 0.5):
                c_eta = Fraction(1 - Fraction(eta)) / (1 + Fraction(eta))
                m0 = math.ceil(math.log(1 / float(c_eta)) / u)
                for r in range(1, min(int(pu * (m + 1)) + 1, m // 2) + 1):
                    if ba_kappa(ball, c_eta, r) < r - 1 - m0:
                        return False, dict(reason="kappa(r) < r - 1 - m_0", m=m, u=u, eta=eta, r=r)
                for r in range(0, int(pu * m) + 1):
                    gam2 = E[r] / T(ba_kappa(ball, c_eta, r))
                    bound = 2 * math.exp(u * (m0 + 2)) * binle[r]
                    stats["largest_b"] = max(stats["largest_b"], gam2 / bound)
                    if gam2 > bound * (1 + 1e-9):
                        return False, dict(reason="Gamma''(r) exceeds 2 e^{u(m_0+2)} P(Bin(m, p_u) <= r)", m=m, u=u, eta=eta, r=r,
                                           ratio=gam2 / bound)
                    stats["cases"] += 1
    return True, stats


@conjecture("XVI.2 The level recursion at accuracy zero (Proposition 11.57): the bracket sup_{gamma >= 0} [min(gamma, phi a) + (1 - phi) T(gamma/(1 - phi))] built on T = theta_hint is at least h for every outer fraction phi (no level undercuts the lower bound), and so is the two-rung bound max{phi a + (1 - phi) T(xi), (1 - phi)(xi + h)}; the first level from the non-adaptive exponent, min_phi max((1 - phi) a, phi a + (1 - phi) theta_na(phi a/(1 - phi))), lies between max(h, a/2) and a, and below 0.51 a for slopes u <= 2.5 (it is 0.58 a at u = 4.5); and the iteration t -> max{phi a + (1 - phi)(h + eta), (1 - phi)(xi + t)} with phi = min(1/2, eta/a), xi = min(eps*/2, phi eta), started at a, stays below eta + max(h + eta, (1 - phi)^m a) and is below h + 2 eta after ln(a/h)/phi + 1 steps")
def t_level_at_zero(rng, trials):
    stats = dict(checks=0, closest=math.inf, tau2_over_a=0.0, steps=0)
    for _ in range(max(6, trials // 10)):
        u = float(rng.choice([0.3, 1.0, 2.0, 4.0]) * rng.uniform(0.8, 1.25))
        pu, lam, estar, a, h = lv_consts(u)
        T = lambda x: na_theta_hint(u, x)
        for _ in range(20):
            phi = float(rng.uniform(0.005, 0.995))
            top = phi * a
            val = max(min(g, top) + (1 - phi) * T(g / (1 - phi)) for g in np.linspace(0.0, top, 200))
            stats["closest"] = min(stats["closest"], val / h - 1)
            if val < h * (1 - 1e-12):
                return False, dict(reason="the bracket at accuracy zero built on theta_hint is below h", u=u, phi=phi, value=val, h=h)
            xi = float(rng.uniform(0, 1)) * estar
            two = max(phi * a + (1 - phi) * T(xi), (1 - phi) * (xi + h))
            if two < h * (1 - 1e-12):
                return False, dict(reason="the two-rung bound built on theta_hint is below h", u=u, phi=phi, xi=xi)
            stats["checks"] += 1
        tau2 = min(max((1 - f) * a, f * a + (1 - f) * na_theta_na(u, f * a / (1 - f))) for f in np.linspace(0.3, 0.7, 801))
        stats["tau2_over_a"] = max(stats["tau2_over_a"], tau2 / a)
        if not (max(h, 0.5 * a) - 1e-12 <= tau2 <= (0.51 * a if u <= 2.5 else a)):
            return False, dict(reason="the first level at accuracy zero is not between max(h, a/2) and 0.51 a (a for steep slopes)", u=u,
                               tau2_over_a=float(tau2 / a))
        eta = float(rng.uniform(0.02, 0.5)) * h
        phi = min(0.5, eta / a)
        xi = min(estar / 2, phi * eta)
        t, m = a, 0
        while t > h + 2 * eta:
            t = max(phi * a + (1 - phi) * (h + eta), (1 - phi) * (xi + t))
            m += 1
            if t > eta + max(h + eta, (1 - phi) ** m * a) + 1e-12:
                return False, dict(reason="the two-rung iteration leaves its envelope", u=u, eta=eta, m=m)
            if m > math.log(a / h) / phi + 1:
                return False, dict(reason="the two-rung iteration does not reach h + 2 eta in time", u=u, eta=eta, m=m)
        stats["steps"] = max(stats["steps"], m)
    return True, stats


def ba_constants(n_o, n, u, par, nladder):
    """The constants of Algorithm 2L+ (theory report Theorem 11.56; workstream K, section 2.2)."""
    lam, eta, etap, theta, nu1, b, delta = (par[k] for k in ("lam", "eta", "etap", "theta", "nu1", "b", "delta"))
    c_eta = (1 - eta) / (1 + eta)
    J = math.ceil((2 * u * n + b + n_o * math.log(2)) / lam)
    nu0 = max((J + 1) * (math.exp(lam) - 1) / etap, nu1) / (1 - eta)
    binom, ball, E, T = ba_exact_tables(n_o, u, n_o)
    Tk = [T(k) for k in range(n_o + 1)]
    gam1 = [math.exp(u) - 1] + [E[r] / ball[r] for r in range(1, n_o + 1)]
    cfrac = Fraction(1 - Fraction(eta)) / (1 + Fraction(eta))
    gam2 = [E[r] / Tk[ba_kappa(ball, cfrac, r)] for r in range(n_o)]
    rdag = -1
    while rdag + 1 <= n_o - 1 and gam1[rdag + 1] <= theta * (1 - eta) * nu0 and min(gam1[rdag + 1] / c_eta, gam2[rdag + 1]) <= theta:
        rdag += 1
    pidag = ball[rdag + 1] / 2 ** n_o if rdag >= 0 else 2.0 ** (-n_o - 1)
    m_max = math.ceil(math.log2(2 * (1 + eta) * math.exp(lam) * nu0 / ((1 - eta) * pidag)))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(2 * (J + 1) * (m_max + 1) * (nladder + 2) / delta))
    Mdag = K / ((1 - eta) * pidag)
    return dict(c_eta=c_eta, J=J, nu0=nu0, nu=K * nu0, K=K, m_max=m_max, rdag=rdag, Mdag=Mdag,
                Mbar=2 * (1 + eta) * math.exp(lam) * nu0 * Mdag, ball=ball, E=E, Tk=Tk)


def ba_two_level_plus(rng, vals, probs, lnw_ref, n_o, n, u, par, mode, max_points=4_200_000):
    """Outer loop of Algorithm 2L+.  The fibre average of a uniform outer point takes the value vals[t] with probability
    probs[t]; lnw_ref = -psi at the reference point (one query).  The inner procedure is simulated: a call at accuracy x
    returns a valid bracket of ratio e^x around the true value, placed at random (mode 0), with the value at its top (1)
    or at its bottom (2).  Returns a record, or a record with the key "error"."""
    lam, eta, etap, theta, b = (par[k] for k in ("lam", "eta", "etap", "theta", "b"))
    xs = [2 * u * (n - n_o)]
    while xs[-1] / 2 > b:
        xs.append(xs[-1] / 2)
    xs = np.array(xs[1:] + [b * (1 - 1e-9)])                           # inner accuracies x_1 > ... > x_L <= b
    C = ba_constants(n_o, n, u, par, len(xs))
    K, nu, J, ball, E, Tk = C["K"], C["nu"], C["J"], C["ball"], C["E"], C["Tk"]
    No = 2 ** n_o
    s0 = math.exp(lnw_ref - u * n)
    ell = math.exp(lnw_ref) * ((1 + math.exp(-u)) / 2) ** n            # the cone around the reference point
    Sigma = 0.0
    cdf = np.cumsum(probs)
    Wl = np.zeros(0); L = np.zeros(0); U = np.zeros(0); acc = np.zeros(0, dtype=np.int64)
    levels = []                                                       # dicts: s, M, q, pbar, pop, ell_in, r, Mneg
    for j in range(J + 1):
        s = s0 * math.exp(j * lam)
        ell_in = ell
        Mneg = nu * s / (ell_in * math.exp(b))
        M = K
        while True:
            if M > max_points or M > K * 2 ** C["m_max"]:
                return dict(error="sample beyond the cap of the test" if M <= K * 2 ** C["m_max"] else "abort: M > K 2^{m_max}", C=C)
            if len(Wl) < M:
                extra = M - len(Wl)
                Wl = np.concatenate([Wl, vals[np.minimum(np.searchsorted(cdf, rng.uniform(size=extra)), len(vals) - 1)]])
                L = np.concatenate([L, np.zeros(extra)]); U = np.concatenate([U, np.full(extra, np.inf)])
                acc = np.concatenate([acc, np.full(extra, -1, dtype=np.int64)])
            while True:                                               # classify the first M points at this level
                und = np.nonzero((U[:M] > s) & (L[:M] <= s * math.exp(-b)))[0]
                if len(und) == 0:
                    break
                if np.any(acc[und] >= len(xs) - 1):
                    return dict(error="classification does not end at the last accuracy of the ladder", C=C)
                acc[und] += 1
                x = xs[acc[und]]
                t = rng.uniform(size=len(und)) if mode == 0 else (np.ones(len(und)) if mode == 1 else np.zeros(len(und)))
                L[und] = np.maximum(L[und], Wl[und] * np.exp(-t * x))
                U[und] = np.minimum(U[und], Wl[und] * np.exp((1 - t) * x))
            N = int((U[:M] > s).sum())                                # the points that are not low are high
            q = min(1.0, max(N, K) / ((1 - eta) * M))
            pop = N >= K
            pbar = N / ((1 + eta) * M) if pop else 0.0
            if pop:
                k = 0
                while ball[k + 2] <= max(1.0, No * pbar):
                    k += 1
                ell = max(ell, s * math.exp(-b) * pbar, s * math.exp(-b) * Tk[k] / No)       # Markov, and the Harper term
            if No * q < 1:
                tail, r = 0.0, -1
            else:
                r = next(rr for rr in range(n_o + 1) if ball[rr + 1] >= No * q)
                tail = s * E[r] / No if r < n_o else math.inf         # no closure while the ball is the whole cube
            rec = dict(s=s, M=M, q=q, pbar=pbar, pop=pop, ell_in=ell_in, r=r, Mneg=Mneg)
            if tail <= theta * math.exp(b) * ell:
                lower = max(ell, Sigma + (1 - math.exp(-lam)) * math.exp(-b) * s * pbar)
                upper = s0 + sum((math.exp(lam) - 1) * lv["s"] * lv["q"] for lv in levels) + tail
                return dict(lower=lower, upper=upper, levels=levels, last=rec, C=C, xs=xs, Wl=Wl, s0=s0)
            if pop or M >= Mneg:
                levels.append(rec)
                Sigma += (1 - math.exp(-lam)) * math.exp(-b) * s * pbar
                break
            M *= 2
    return dict(error="no closure within J levels", C=C)


def ba_check_run(run, vals, probs, n_o, n, u, par, stats):
    """The claims of Theorem 11.56 on one run: validity, width, certificates, closing radius, sample sizes, the count."""
    lam, eta, etap, theta, b = (par[k] for k in ("lam", "eta", "etap", "theta", "b"))
    C = run["C"]
    A = float((vals * probs).sum())
    if not (run["lower"] <= A * (1 + 1e-12) and A <= run["upper"] * (1 + 1e-12)):
        return dict(reason="the bracket of Algorithm 2L+ does not contain the mean", lower=run["lower"], A=A, upper=run["upper"])
    width = math.log(run["upper"] / run["lower"])
    bound = math.log((2 / (1 + math.exp(u))) ** n + math.exp(b) * (math.exp(lam) * (1 + eta) / (1 - eta) + etap + theta))
    if width > bound + 1e-9:
        return dict(reason="the bracket is wider than ln[(2 p_u)^n + e^b (e^lam (1+eta)/(1-eta) + eta' + theta)]", width=width, bound=bound)
    stats["widest"] = max(stats["widest"], width / bound)
    exceed = lambda thr: float(probs[vals > thr].sum())
    for jj, lv in enumerate(run["levels"] + [run["last"]]):
        left = jj < len(run["levels"])
        if exceed(lv["s"]) > lv["q"] + 1e-12:
            return dict(reason="a certified upper bound q on an exceedance probability is too small", level=jj, p=exceed(lv["s"]), q=lv["q"])
        if lv["pop"] and lv["pbar"] > exceed(lv["s"] * math.exp(-b)) + 1e-12:
            return dict(reason="a certified lower bound on an exceedance probability is too large", level=jj)
        if left and lv["r"] <= C["rdag"]:
            return dict(reason="a level was left although its closing radius is at most r_dagger", level=jj, r=lv["r"], rdag=C["rdag"])
        if lv["M"] > max(C["K"], 2 * lv["Mneg"]) or lv["M"] > C["Mbar"] * (1 + 1e-12):
            return dict(reason="a sample is larger than max(K, 2 M_neg) or than M_bar", level=jj, M=lv["M"])
        if lv["Mneg"] > (1 + eta) * math.exp(lam) * C["nu0"] * C["Mdag"] * (1 + 1e-12):
            return dict(reason="a negligibility threshold exceeds (1+eta) e^lam nu_0 M_dagger", level=jj)
        for x in [2 * u * (n - n_o)] + list(run["xs"][:-1]):
            lhs = lv["Mneg"] * exceed(lv["s"] * math.exp(-x))
            cap = C["nu"] * math.exp(lam + x) / C["c_eta"]
            if lhs > cap * (1 + 1e-9):
                return dict(reason="the count of points close to a level exceeds e^lam nu e^x / c_eta", level=jj, x=x, ratio=lhs / cap)
            stats["tightest_count"] = max(stats["tightest_count"], lhs / cap)
        stats["populated" if lv["pop"] else "unpopulated"] += 1
    stats["runs"] += 1
    return None


def ba_radial(n_o, u, kind):
    """Radial outer landscapes f(dist(a, 0)) with slopes at most u: 0 flat, 1 cone, 2 'staircase' with
    e^{-f(d)} |B(n_o, d)| constant wherever the slope allows (many levels carry the same mass)."""
    binom = [math.comb(n_o, j) for j in range(n_o + 1)]
    ball = list(itertools.accumulate(binom))
    if kind == 0:
        f = np.zeros(n_o + 1)
    elif kind == 1:
        f = u * np.arange(n_o + 1, dtype=float)
    else:
        f = np.concatenate([[0.0], np.cumsum([min(u, math.log(ball[d + 1] / ball[d])) for d in range(n_o)])])
    return np.exp(-f), np.array(binom, dtype=float) / 2 ** n_o, float(-f[0])


@conjecture("XVI.3 Algorithm 2L+ (Theorem 11.56), outer loop with a simulated inner procedure and the constants of the theorem: on arbitrary Lipschitz functions of a small cube and on radial outer landscapes (flat, cone, staircase) the bracket contains the mean and is at most ln[(2 p_u)^n + e^b (e^lam (1+eta)/(1-eta) + eta' + theta)] wide; every certificate is true; every level that is left has closing radius above r_dagger; samples stay below max(K, 2 M_neg) and M_bar; and the count of points within a factor e^x of a level obeys M_neg p(s e^{-x}) <= e^lam nu e^x / c_eta")
def t_two_level_plus(rng, trials):
    stats = dict(runs=0, widest=0.0, tightest_count=0.0, populated=0, unpopulated=0, skipped=0)
    def one(vals, probs, lnw_ref, n_o, n, u, par, mode, tag):
        run = ba_two_level_plus(rng, vals, probs, lnw_ref, n_o, n, u, par, mode)
        if "error" in run:
            if run["error"].startswith("sample beyond"):
                stats["skipped"] += 1
                return None
            return dict(reason=run["error"], tag=tag)
        bad = ba_check_run(run, vals, probs, n_o, n, u, par, stats)
        return dict(bad, tag=tag) if bad else None
    # (i) arbitrary Lipschitz functions on a small cube, all fibre averages enumerated
    n_o, n_i = 6, 4
    n = n_o + n_i
    D = na_cube(n)
    for rep in range(max(6, trials // 10)):
        u = float(rng.choice([0.5, 1.0, 2.0]))
        kind = rep % 6
        psi = na_rand_lipschitz(rng, n, u, D, kind) if kind < 5 else u * D[int(rng.integers(2 ** n))].astype(float)
        psi = psi + float(rng.uniform(-3, 3))
        vals = np.exp(-psi).reshape(2 ** n_o, 2 ** n_i).mean(axis=1)
        probs = np.full(2 ** n_o, 2.0 ** -n_o)
        par = dict(lam=float(rng.choice([0.5, 1.0])), eta=float(rng.choice([0.25, 0.5])), etap=float(rng.choice([0.5, 1.0])),
                   theta=float(rng.choice([0.5, 2.0, 20.0])), b=float(rng.choice([0.5, 1.0, 3.0])), delta=0.01, nu1=1.0)
        if rep % 2:
            par["nu1"] = 2 * math.exp(u) * n_o / par["theta"]
        bad = one(vals, probs, -float(psi[int(rng.integers(2 ** n))]), n_o, n, u, par, rep % 3, ("cube", kind))
        if bad:
            return False, bad
    # (ii) radial outer landscapes; on the staircase a lower end without the layer-cake sum is too small
    radial = [(40, 1.0, 0, dict(lam=0.5, eta=0.25, etap=0.5, theta=0.5, b=1.0, delta=0.01, nu1=1.0)),
              (24, 1.0, 1, dict(lam=0.5, eta=0.25, etap=0.5, theta=2.0, b=0.5, delta=0.01, nu1=1.0)),
              (24, 1.0, 2, dict(lam=0.125, eta=0.25, etap=0.1, theta=1.0, b=0.25, delta=0.01, nu1=1.0)),
              (20, 1.0, 1, dict(lam=0.5, eta=0.25, etap=0.5, theta=0.5, b=1.0, delta=0.01, nu1=1.0)),
              (40, 2.0, 0, dict(lam=1.0, eta=0.5, etap=1.0, theta=2.0, b=3.0, delta=0.01, nu1=1.0)),
              (28, 1.0, 2, dict(lam=0.25, eta=0.25, etap=0.1, theta=1.0, b=0.5, delta=0.01, nu1=1.0))]
    for rep, (n_o, u, kind, par) in enumerate(radial[:3] if trials < 100 else radial):
        vals, probs, lnw_ref = ba_radial(n_o, u, kind)
        bad = one(vals, probs, lnw_ref, n_o, n_o + 2, u, par, rep % 3, ("radial", n_o, kind))
        if bad:
            return False, bad
    if stats["populated"] == 0 or stats["unpopulated"] == 0 or stats["skipped"] > 0:
        return False, dict(reason="the test has no power", **stats)
    return True, stats


# ----------------------------------------------------------------------------------------------
# XVII. With a known part (a field): the p-biased cube (theory report 11.20)
# ----------------------------------------------------------------------------------------------

def fd_consts(p, u):
    """(q, Lambda(0), Lambda(1)): soft gaps of the two centre letters at the zero residual."""
    q = 1 - p
    return q, -math.log(q + p * math.exp(-u)), -math.log(p + q * math.exp(-u))


def fd_game(p, u, g, t):
    """Closed form of the game function F(gamma, t) of the additive instance gamma |x| (Theorem 11.59(b))."""
    q, L0, L1 = fd_consts(p, u)
    return (-t * math.log(q + p * math.exp(-g))
            + math.log((1 - math.exp(-t * (u + g))) * math.exp(-t * L0) + (1 - math.exp(-t * (u - g))) * math.exp(-t * (L1 + g)))
            - math.log(1 - math.exp(-2 * t * u)))


def fd_game_value(p, u, g, t):
    """-ln val of K(a, b) = exp(-t [u 1[a != b] - Lambda(b) - gamma a - ln Z_gamma]) computed from the definition: the minimum
    over mixtures of the two centre letters of the larger row sum (two lines in the mixing weight: an end or the crossing)."""
    q, L0, L1 = fd_consts(p, u)
    lz, Lam = math.log(q + p * math.exp(-g)), (L0, L1)
    K = [[math.exp(-t * (u * (a != b) - Lam[b] - g * a - lz)) for b in (0, 1)] for a in (0, 1)]
    cands = [0.0, 1.0]
    den = (K[0][0] - K[0][1]) - (K[1][0] - K[1][1])
    if den != 0 and 0 <= (K[1][1] - K[0][1]) / den <= 1:
        cands.append((K[1][1] - K[0][1]) / den)
    return -math.log(min(max(K[0][0] * w + K[0][1] * (1 - w), K[1][0] * w + K[1][1] * (1 - w)) for w in cands))


def fd_fstar(p, u, T, ngam=401):
    """F*(t) = max over |gamma| <= u of F(gamma, t) on the grid T, F(0, t), and the maximising gamma."""
    q, L0, L1 = fd_consts(p, u)
    gam = np.linspace(-u * (1 - 1e-9), u * (1 - 1e-9), ngam)
    G, TT = np.meshgrid(gam, T, indexing="ij")
    Fv = (-TT * np.log(q + p * np.exp(-G)) + np.log((1 - np.exp(-TT * (u + G))) * np.exp(-TT * L0)
          + (1 - np.exp(-TT * (u - G))) * np.exp(-TT * (L1 + G))) - np.log(1 - np.exp(-2 * TT * u)))
    return Fv.max(axis=0), Fv[ngam // 2], gam[Fv.argmax(axis=0)]


def fd_hinted(Fv, T, e):
    """max over 0 <= t <= 1 of F(t) - t e (the value 0 at t = 0 included)."""
    return max(0.0, float((Fv - T * e).max()))


def fd_theta_na(Fv, T, x):
    """sup over tau < 1 of (F(tau) - tau x)/(1 - tau): the non-adaptive exponent in terms of the game function."""
    return max(0.0, float(((Fv - T * x) / (1 - T)).max()))


@conjecture("XVII.1 Exponent functions with a field (Theorems 11.59, 11.64, Lemma 11.60): the closed form of the game function F(gamma, t) equals -ln of the 2x2 game value computed from its definition and vanishes at t = 1; the shift identity D(P_{X|S} || pi_s | P_S) = I(S;X) + KL(P_X || pi) + u P(X != S) - Lambda(P_S) holds at every profile; the hinted exponent of the zero residual is max_m [h(m) - h((Lambda_m + e)/u)]_+; at p = 1/2 the largest hinted exponent is KL((Lambda_1 + e)/u || 1/2) and the hardest instance is the zero residual; for p != 1/2 it is strictly larger than the hinted exponent of the zero residual, the class threshold exceeds that of the zero residual, and the hardest additive residual works against the field; and the non-adaptive exponent sup_{tau < 1} (F*(tau) - tau x)/(1 - tau) satisfies theta_na(e + R^max(e)) = R^max(e)")
def t_field_exponents(rng, trials):
    stats = dict(games=0, identities=0, pairs=0, smallest_gain=math.inf, largest_gain=0.0)
    T = np.concatenate([np.linspace(1e-4, 0.99, 2500), np.linspace(0.99, 1 - 1e-7, 1500)[1:]])
    h2 = lambda z: 0.0 if z <= 0 or z >= 1 else -(z * math.log(z) + (1 - z) * math.log(1 - z))
    for rep in range(max(6, trials // 10)):
        p = 0.5 if rep % 3 == 0 else float(rng.uniform(0.04, 0.96))
        u = float(rng.uniform(0.3, 3.0))
        q, L0, L1 = fd_consts(p, u)
        for _ in range(10):                                           # closed form against the definition
            g, t = float(rng.uniform(-0.95, 0.95)) * u, float(rng.uniform(0.02, 0.99))
            if abs(fd_game(p, u, g, t) - fd_game_value(p, u, g, t)) > 1e-9 or abs(fd_game(p, u, g, 1.0)) > 1e-9:
                return False, dict(reason="closed form of the game function != -ln val, or F(gamma, 1) != 0", p=p, u=u, gamma=g, t=t)
            stats["games"] += 1
        eta1, eta0 = q * math.exp(-u) / (p + q * math.exp(-u)), p * math.exp(-u) / (q + p * math.exp(-u))
        for _ in range(10):                                           # the shift identity at a random profile
            m, x, y = (float(v) for v in rng.uniform(0.02, 0.98, size=3))     # P(S=1), P(X=0|S=1), P(X=1|S=0)
            kap, rho, Lm = m * (1 - x) + (1 - m) * y, m * x + (1 - m) * y, (1 - m) * L0 + m * L1
            I = h2(kap) - m * h2(x) - (1 - m) * h2(y)
            cone = m * na_kl(x, eta1) + (1 - m) * na_kl(y, eta0)
            if abs(cone - (I + na_kl(kap, p) + u * rho - Lm)) > 1e-10:
                return False, dict(reason="shift identity with a field fails", p=p, u=u, m=m, x=x, y=y)
            stats["identities"] += 1
        Fs, F0, gstar = fd_fstar(p, u, T)
        E, E0 = float((Fs / T).max()), float((F0 / T).max())
        ms = np.linspace(1e-4, 1 - 1e-4, 20001)
        for frac in (0.0, 0.3, 0.6):
            e = frac * E0
            r0, rm = fd_hinted(F0, T, e), fd_hinted(Fs, T, e)
            rho = ((1 - ms) * L0 + ms * L1 + e) / u
            ok = rho <= np.minimum(ms, 1 - ms)
            hh = lambda z: -(z * np.log(z) + (1 - z) * np.log1p(-z))
            ball = float(np.max(np.where(ok, hh(ms) - hh(np.clip(rho, 1e-12, 0.5)), 0.0)))
            if abs(r0 - ball) > 2e-6 + 1e-4 * r0:
                return False, dict(reason="hinted exponent at the zero residual != max_m [h(m) - h((Lambda_m + e)/u)]", p=p, u=u, e=e, game=r0, ball=ball)
            if p == 0.5:
                lam1 = math.log(2 / (1 + math.exp(-u)))
                if abs(rm - na_kl((lam1 + e) / u, 0.5)) > 2e-6 or abs(rm - r0) > 1e-9:
                    return False, dict(reason="at p = 1/2 the exponents are not those of the uniform cube", u=u, e=e)
            elif frac == 0.0:
                gain = rm / r0 - 1
                stats["smallest_gain"], stats["largest_gain"] = min(stats["smallest_gain"], gain), max(stats["largest_gain"], gain)
                gam0 = float(gstar[int(np.argmax(Fs))])
                if not (rm > r0 * (1 + 1e-7) and E > E0 and gam0 * (0.5 - p) < 0):
                    return False, dict(reason="with a field the hardest additive instance is not strictly harder than the zero residual, or its residual does not work against the field", p=p, u=u, R0=r0, Rmax=rm, gamma=gam0)
        for frac in (0.1, 0.4):                                       # the pair (theta_na, R^max)
            e = frac * E
            r = fd_hinted(Fs, T, e)
            th = fd_theta_na(Fs, T, e + r)
            if abs(th - r) > 2e-4 * r + 1e-7:
                return False, dict(reason="theta_na(e + R^max(e)) != R^max(e)", p=p, u=u, e=e, theta_na=th, hinted=r)
            stats["pairs"] += 1
    return True, stats


@conjecture("XVII.2 Theorem 11.61(a): for every u-Lipschitz weight on the cube the type-wise upper q-quantiles t_kappa (the smallest value of w on the type class above which w has density at most q there) satisfy t_{kappa +- 1} <= e^u t_kappa; hence the truncated function max(psi, -ln t_{|x|}) is u-Lipschitz and differs from psi on a set of density at most q in every type class")
def t_typewise_quantiles(rng, trials):
    stats = dict(pairs=0, functions=0, tightest=0.0)
    for n in ((5, 7) if trials < 100 else (5, 7, 9)):
        D = na_cube(n)
        wt = D[0]
        nbr = [[x ^ (1 << i) for i in range(n)] for x in range(2 ** n)]
        for rep in range(max(6, trials // 20)):
            u = float(rng.choice([0.5, 1.0, 2.0]))
            kind = rep % 6
            psi = na_rand_lipschitz(rng, n, u, D, kind) if kind < 5 else u * D[int(rng.integers(2 ** n))].astype(float)
            w = np.exp(-psi)
            for qq in (0.03, 0.2, 0.6):
                tk = []
                for kappa in range(n + 1):
                    ws = np.sort(w[wt == kappa])
                    tk.append(float(next(tau for tau in ws if (ws > tau).mean() <= qq)))
                for kappa in range(n):
                    ratio = max(tk[kappa + 1] / tk[kappa], tk[kappa] / tk[kappa + 1])
                    stats["tightest"] = max(stats["tightest"], ratio / math.exp(u))
                    if ratio > math.exp(u) * (1 + 1e-12):
                        return False, dict(reason="adjacent type-wise quantiles differ by more than e^u", n=n, u=u, q=qq, kappa=kappa)
                    stats["pairs"] += 1
                tr = np.maximum(psi, -np.log(np.array(tk))[wt])
                if any(abs(tr[x] - tr[y]) > u * (1 + 1e-12) for x in range(2 ** n) for y in nbr[x]):
                    return False, dict(reason="the function truncated at its type-wise quantiles is not u-Lipschitz", n=n, u=u, q=qq)
                if any((tr[wt == kappa] > psi[wt == kappa] + 1e-12).mean() > qq + 1e-12 for kappa in range(n + 1)):
                    return False, dict(reason="the truncation changes more than a fraction q of a type class", n=n, u=u, q=qq)
            stats["functions"] += 1
    return True, stats


def fd_reference_tables(p, u, n, D):
    """The flat-histogram reference on Q_n: psi_H = -n v(|x|/n), its Gibbs law mu_H, the slack s_H, and for every nonempty
    proper subset (bit mask) its measure and its effect Phi_H(D) = sum_{x in D} mu_H(x) (e^{s_H(x -> D^c)} - 1)."""
    q = 1 - p
    gam = np.linspace(-u, u, 4001)
    wt = D[0]
    v = np.array([float(np.max(-gam * (k / n) - np.log(q + p * np.exp(-gam)))) for k in range(n + 1)])
    psiH = -n * v[wt]
    mu = p ** wt * q ** (n - wt) * np.exp(-psiH)
    mu = mu / mu.sum()
    slack = u * D + psiH[:, None] - psiH[None, :]
    N = 2 ** n
    masks = np.arange(1, 2 ** N - 1, dtype=np.int64)
    B = ((masks[:, None] >> np.arange(N)) & 1).astype(bool)
    phi = np.zeros(len(masks))
    for x in range(N):
        exit_slack = np.where(~B, slack[x][None, :], np.inf).min(axis=1)
        phi += np.where(B[:, x], mu[x] * (np.exp(exit_slack) - 1), 0.0)
    meas = B @ mu
    order = np.argsort(meas, kind="stable")
    return psiH, mu, slack, masks, B, phi, meas, meas[order], np.maximum.accumulate(phi[order]), order


@conjecture("XVII.3 Lemma 11.62 on the 4-cube with the exact tail function of the flat-histogram reference H (all 65534 subsets): the slack u d(x,y) + psi_H(x) - psi_H(y) is nonnegative; for every u-Lipschitz psi and every level t, E_{mu_H} (w/w_H - t)_+ <= t Xi_H(mu_H(w/w_H > t)); and there is equality at t = 1 for the deepest dip of H on a maximising set")
def t_reference_tail_lemma(rng, trials):
    stats = dict(levels=0, tightest=0.0, equalities=0)
    n = 4
    D = na_cube(n)
    for rep in range(2 if trials < 100 else 5):
        p, u = [(0.1, 2.0), (0.3, 1.0), (0.2, 1.5), (0.7, 1.0), (0.5, 1.0)][rep]
        psiH, mu, slack, masks, B, phi, meas, meas_sorted, tailmax, order = fd_reference_tables(p, u, n, D)
        if slack.min() < -1e-12:
            return False, dict(reason="the slack of the flat-histogram reference is negative", p=p, u=u)
        Xi = lambda qq: float(tailmax[np.searchsorted(meas_sorted, qq * (1 + 1e-12), side="right") - 1]) if qq >= meas_sorted[0] else 0.0
        for k in range(max(12, trials // 5)):
            kind = k % 6
            psi = na_rand_lipschitz(rng, n, u, D, kind) if kind < 5 else u * D[int(rng.integers(2 ** n))].astype(float)
            what = np.exp(-psi + psiH)                                # w / w_H
            for t in np.unique(what)[:-1]:
                above = what > t
                qq = float(mu[above].sum())
                lhs = float((mu[above] * (what[above] - t)).sum())
                rhs = t * Xi(qq)
                stats["tightest"] = max(stats["tightest"], lhs / rhs if rhs > 0 else 0.0)
                if lhs > rhs * (1 + 1e-9) + 1e-15:
                    return False, dict(reason="tail lemma relative to the flat-histogram reference violated", p=p, u=u, t=float(t), lhs=lhs, rhs=rhs)
                stats["levels"] += 1
        for qq in (0.05, 0.2, 0.5):                                   # equality: the deepest dip of H on a maximising set
            j = int(np.searchsorted(meas_sorted, qq, side="right")) - 1
            if j < 0:
                continue
            best = order[int(np.argmax(phi[order[:j + 1]]))]
            inside = B[best]
            dip = np.where(inside, np.max(np.where(~inside[None, :], psiH[None, :] - u * D, -np.inf), axis=1), psiH)
            what = np.exp(-dip + psiH)
            lhs = float((mu[inside] * (what[inside] - 1)).sum())
            if abs(lhs - Xi(float(meas[best]))) > 1e-9 * max(lhs, 1e-12):
                return False, dict(reason="no equality at the deepest dip of the reference on a maximising set", p=p, u=u, q=qq)
            stats["equalities"] += 1
    return True, stats


@conjecture("XVII.4 Proposition 11.65(b): a field always helps.  In the cosh form F(gamma, t) = ln[I_theta(theta + gamma)/C(theta + gamma)^t] the ratio is unimodal in gamma on the window; for theta > 0 its maximiser gamma* is negative (the hardest residual works against the field); F*(t; theta) is nonincreasing in theta >= 0; and at the maximiser ln cosh Q - ln cosh P >= (1 - t)[ln cosh((theta+u)/2) - ln cosh((theta-u)/2)] with P = (theta-u)/2 + t(u-gamma*)/2, Q = (theta+u)/2 - t(u+gamma*)/2 (the comparison of interval averages of tanh to which the proof reduces dF*/dtheta <= 0)")
def t_field_monotone(rng, trials):
    stats = dict(cases=0, largest_increase=-math.inf, smallest_margin=math.inf)
    lc = lambda z: np.log(np.cosh(z))
    for _ in range(max(6, trials // 10)):
        u, t = float(rng.uniform(0.3, 4.0)), float(rng.uniform(0.03, 0.97))
        s = np.linspace(-u, u, 40001)[1:-1]
        prev = None
        for theta in np.linspace(0.0, 6.0, 25):
            la, lb = t * np.log(2 * np.cosh((theta - u) / 2)), t * np.log(2 * np.cosh((theta + u) / 2))
            ph = (np.logaddexp(np.log(np.sinh(t * (u - s) / 2)) + la, np.log(np.sinh(t * (u + s) / 2)) + lb)
                  - math.log(math.sinh(t * u)) - t * np.log(2 * np.cosh((theta + s) / 2)))
            d = np.diff(ph)
            sg = np.sign(d[np.abs(d) > 1e-14])
            if int((np.diff(sg) != 0).sum()) > 1 or (len(sg) and sg[0] < 0 and sg[-1] > 0):
                return False, dict(reason="the ratio is not unimodal on the window", u=u, t=t, theta=float(theta))
            i = int(ph.argmax())
            if theta > 0.2 and s[i] > 1e-9:
                return False, dict(reason="the hardest residual does not work against the field", u=u, t=t, theta=float(theta), gamma=float(s[i]))
            if prev is not None:
                stats["largest_increase"] = max(stats["largest_increase"], float(ph[i] - prev))
                if ph[i] > prev + 1e-10:
                    return False, dict(reason="F*(t; theta) increases with theta", u=u, t=t, theta=float(theta))
            prev = float(ph[i])
            P, Q = (theta - u) / 2 + t * (u - s[i]) / 2, (theta + u) / 2 - t * (u + s[i]) / 2
            margin = float((lc(Q) - lc(P)) - (1 - t) * (lc((theta + u) / 2) - lc((theta - u) / 2)))
            stats["smallest_margin"] = min(stats["smallest_margin"], margin)
            if margin < -1e-7:
                return False, dict(reason="the comparison of interval averages of tanh fails at the maximiser", u=u, t=t, theta=float(theta), margin=margin)
            stats["cases"] += 1
    return True, stats


# ----------------------------------------------------------------------------------------------
# XVIII. Chains in the thermodynamic limit: profile sets of the diamond-lattice chain (theory report §11.22)
# ----------------------------------------------------------------------------------------------

LS_BV = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
LS_DISP = {d: [v for v in itertools.product(range(-3, 4), repeat=3) if v[0] ** 2 + v[1] ** 2 + v[2] ** 2 == d]
           for d in (3, 8, 11)}
# rows (c3, c8, c11; b; M) of Proposition 11.72(b)
LS_ROWS = [((-1, 0, 0), 0, Fraction(1, 2)), ((4, -1, 0), 0, 5), ((6, -1, 0), 1, 6), ((-2, 1, 0), 3, 2), ((-1, 1, -1), 0, 3),
           ((-1, 2, -1), 3, 4), ((-4, 2, -1), 2, 6), ((3, 4, -3), 5, 6), ((6, -2, 1), 2, 6), ((0, -1, 2), 7, 1),
           ((-3, 0, 2), 9, 3)]
# integer multipliers of the six star relations and y0 for the rows above (workstream S, exact certificates)
LS_CERT = {(-4, 2, -1): ([0, -6, -6, 0, -18, -6], 0), (-3, 0, 2): ([-6, -18, -12, 0, -30, -18], 6),
           (-2, 1, 0): ([0, -3, -3, 0, -15, -7], 2), (-1, 0, 0): ([0, 0, 0, 0, -3, -1], -1),
           (-1, 1, -1): ([0, -3, -3, 0, -3, -3], 0), (-1, 2, -1): ([0, -6, -6, 0, -6, -2], 4),
           (0, -1, 2): ([-6, -15, -9, 0, -15, -9], 6), (3, 4, -3): ([0, -12, -12, 0, 12, 0], 12),
           (4, -1, 0): ([0, 3, 3, 0, 12, 6], 3), (6, -2, 1): ([-3, -3, 0, 0, 15, 9], 6), (6, -1, 0): ([0, 3, 3, 0, 21, 9], 6)}
LS_STAR_KEYS = [(0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 1)]


def ls_is_a(p):
    return p[0] % 2 == 0 and p[1] % 2 == 0 and p[2] % 2 == 0 and (p[0] + p[1] + p[2]) % 4 == 0


def ls_nbrs(p):
    s = 1 if ls_is_a(p) else -1
    return [(p[0] + s * a[0], p[1] + s * a[1], p[2] + s * a[2]) for a in LS_BV]


def ls_sq(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2


def ls_valid_walk(w):
    if len(set(w)) != len(w):
        return False
    if not all(ls_is_a(p) or ls_is_a((p[0] - 1, p[1] - 1, p[2] - 1)) for p in w):
        return False
    return all(w[i + 1] in ls_nbrs(w[i]) for i in range(len(w) - 1))


def ls_profile(w):
    """(h3, h8, h11, gauche) from the definition: pairs p < q with q - p >= 3 at squared distance 3, 8, 11."""
    idx = {p: i for i, p in enumerate(w)}
    h = [0, 0, 0]
    for i, p in enumerate(w):
        for k, d in enumerate((3, 8, 11)):
            for v in LS_DISP[d]:
                j = idx.get((p[0] + v[0], p[1] + v[1], p[2] + v[2]))
                if j is not None and j - i >= 3:
                    h[k] += 1
    g = sum(1 for i in range(len(w) - 3) if ls_sq(w[i], w[i + 3]) == 11)
    return (h[0], h[1], h[2], g)


def ls_site_counts(S):
    """(e3, e8, e11, n_E, local e3, local e8, number of ordered gauche four-site paths) of a finite site set."""
    S = set(S)
    e = []
    for d in (3, 8, 11):
        e.append(sum(1 for p in S for v in LS_DISP[d] if (p[0] + v[0], p[1] + v[1], p[2] + v[2]) in S) // 2)
    deg = {}
    for p in S:
        for q in ls_nbrs(p):
            deg[q] = deg.get(q, 0) + 1
    n_e = sum(1 for p in S if deg.get(p, 0) < 2)
    loc3 = sum(deg.get(p, 0) for p in S)                       # = 2 e3
    loc8 = sum(dd * (dd - 1) // 2 for dd in deg.values())      # sum over ALL lattice sites of C(d, 2)
    paths = 0
    for u_ in S:
        for v_ in ls_nbrs(u_):
            for w_ in ls_nbrs(v_):
                if w_ == u_:
                    continue
                for z_ in ls_nbrs(w_):
                    if z_ != v_ and z_ in S and ls_sq(u_, z_) == 11:
                        paths += 1
    return e[0], e[1], e[2], n_e, loc3, loc8, paths


def ls_is_bridge(w):
    y0, yl = w[0][1], w[-1][1]
    return all(p[1] > y0 for p in w[1:]) and all(p[1] <= yl for p in w)


def ls_cnorm(d):
    return 5 * abs(d[0]) + 3 * abs(d[0] + d[1]) + abs(d[0] + d[1] + d[2])


def ls_wnorm(d):
    return 9 * abs(d[0]) + 4 * abs(d[1]) + abs(d[2])


def ls_enum(nbeads, bridge=False):
    """all walks with nbeads beads from the origin with first bond +a_0, or (bridge=True) all bridges from the origin"""
    out, w, occ = [], [(0, 0, 0)], {(0, 0, 0)}

    def rec():
        if len(w) == nbeads:
            if (not bridge) or all(p[1] <= w[-1][1] for p in w):
                out.append(list(w))
            return
        for q in ls_nbrs(w[-1]):
            if q in occ or (bridge and q[1] <= 0) or ((not bridge) and len(w) == 1 and q != (1, 1, 1)):
                continue
            occ.add(q); w.append(q)
            rec()
            occ.discard(q); w.pop()

    rec()
    return out


def ls_lamella(M, Q, ell):
    """rung-folded lamella (Proposition 11.72(d)): M x Q block of all-trans stems of ell periods in snake order"""
    def site(m, q, t):
        k, r = divmod(t, 2)
        return (2 * m + 2 * q + r, 2 * m + 2 * k + r, 2 * q + 2 * k + r)
    order = []
    for q in range(Q):
        order += [(m, q) for m in (range(M) if q % 2 == 0 else range(M - 1, -1, -1))]
    w, up, t = [], True, -2
    for i, (m, q) in enumerate(order):
        if i == len(order) - 1:
            t_end = 2 * ell + 1
        else:
            m2, q2 = order[i + 1]
            plus = (m2 - m, q2 - q) in ((1, 0), (0, 1))
            k = ell - 1 if up else 0
            t_end = 2 * k + 1 if plus else 2 * k
        step = 1 if up else -1
        while True:
            w.append(site(m, q, t))
            if t == t_end:
                break
            t += step
        if i < len(order) - 1:
            t = 2 * k if plus else 2 * k + 1
            up = not up
    return w


@conjecture("XVIII.1 Lemma 11.67, Proposition 11.72(a),(b), Proposition 11.73 (diamond-lattice chain, cutoff 12): for every walk the profile from the definition is h3 = e3(S) - (N-1), h8 = e8(S) - (N-2), h11 = e11(S) with S its site set; for every finite site set e3 = (1/2) sum_S d(m), e8 = sum over ALL lattice sites of C(d(m),2), and two sites at squared distance 11 are joined by exactly two three-bond paths; every walk satisfies h8 >= 4h3 - 2, h8 >= 6h3 - N - 4, h8 <= 2h3 + 3N + 3; every finite site set satisfies the eleven inequalities c3(e3-N) + c8(e8-N) + c11 e11 <= bN + 2M n_E; and e3 <= 2N - 2^(-2/3) N^(2/3), e8 <= 6N - 3N^(2/3), hence 9h3 + 4h8 + h11 <= 35N - 17.6 N^(2/3) + 17")
def t_ls_site_sets(rng, trials):
    stats = dict(walks=0, sets=0, tightest_row_slack=10 ** 9, largest_density=0.0)
    sets = []
    for N in range(4, (9 if trials < 100 else 10) + 1):
        for w in ls_enum(N):
            h3, h8, h11, g = ls_profile(w)
            e3, e8, e11, n_e, loc3, loc8, paths = ls_site_counts(w)
            if (h3, h8, h11) != (e3 - (N - 1), e8 - (N - 2), e11):
                return False, dict(reason="the profile is not the site-set formula", N=N)
            if not (h8 >= 4 * h3 - 2 and h8 >= 6 * h3 - N - 4 and h8 <= 2 * h3 + 3 * N + 3):
                return False, dict(reason="a by-hand inequality of Proposition 11.72(a) fails", N=N, h=(h3, h8, h11))
            if n_e > 2:
                return False, dict(reason="a walk has more than two sites with fewer than two occupied neighbours", N=N)
            sets.append((w, (e3, e8, e11, n_e, loc3, loc8, paths)))
            stats["walks"] += 1
    # lamellae and random finite site sets (arbitrary degrees): the finite-set forms
    for (M, Q, ell) in ((3, 1, 5), (5, 1, 9), (3, 3, 4), (5, 5, 6), (7, 7, 8)):
        w = ls_lamella(M, Q, ell)
        if not (ls_valid_walk(w) and ls_is_bridge(w)) or ls_profile(w)[3] > 3 * (M * Q - 1):
            return False, dict(reason="a rung-folded lamella is not a bridge with at most 3(MQ-1) gauche torsions", M=M, Q=Q, ell=ell)
        sets.append((w, ls_site_counts(w)))
    box = [p for p in itertools.product(range(0, 7), repeat=3) if ls_is_a(p) or ls_is_a((p[0] - 1, p[1] - 1, p[2] - 1))]
    for rep in range(max(12, trials // 10)):
        rho = float(rng.choice([0.25, 0.5, 0.75, 0.95, 1.0]))
        S = [p for p in box if rng.random() < rho]
        if len(S) >= 2:
            sets.append((S, ls_site_counts(S)))
    for S, (e3, e8, e11, n_e, loc3, loc8, paths) in sets:
        N = len(S)
        if loc3 != 2 * e3 or loc8 != e8 or paths != 4 * e11:
            return False, dict(reason="a local counting formula fails", N=N)
        for (c, b, M_) in LS_ROWS:
            slack = b * N + 2 * M_ * n_e - (c[0] * (e3 - N) + c[1] * (e8 - N) + c[2] * e11)
            if slack < 0:
                return False, dict(reason="one of the eleven inequalities fails on a finite site set", N=N, row=c)
            stats["tightest_row_slack"] = min(stats["tightest_row_slack"], float(slack))
        if e3 > 2 * N - 2 ** (-2 / 3) * N ** (2 / 3) + 1e-9 or e8 > 6 * N - 3 * N ** (2 / 3) + 1e-9:
            return False, dict(reason="an isoperimetric bound of Proposition 11.73 fails", N=N, e3=e3, e8=e8)
        if 9 * (e3 - N + 1) + 4 * (e8 - N + 2) + e11 > 35 * N - 17.6 * N ** (2 / 3) + 17 + 1e-9 and e11 <= 6 * N:
            return False, dict(reason="the surface bound on the profile norm fails", N=N)
        stats["largest_density"] = max(stats["largest_density"], (9 * (e3 - N) + 4 * (e8 - N) + e11) / N)
        stats["sets"] += 1
    return True, stats


LS_SIGNED_PERMS = [(perm, sg) for perm in itertools.permutations(range(3)) for sg in itertools.product((1, -1), repeat=3)]


def ls_concat(x1, x2, which=0, force_other=False):
    """the bridge of Lemma 11.68 built from x1, three linker beads and the copy of x2 that continues the zigzag;
    returns (walk, b' is a down-bond, number of admissible copies)"""
    P = x1[-1]
    b = tuple(x1[-1][i] - x1[-2][i] for i in range(3))
    bp = tuple(x1[-2][i] - x1[-3][i] for i in range(3))
    down = (bp[1] == -1)
    ups = [tuple(q[i] - P[i] for i in range(3)) for q in ls_nbrs(P) if q[1] == P[1] + 1]
    if down:
        c1 = ups[which]
    elif force_other:
        c1 = [v for v in ups if v != bp][0]
    else:
        c1 = bp
    add = lambda p, v: (p[0] + v[0], p[1] + v[1], p[2] + v[2])
    l1 = add(P, c1); l2 = add(l1, b); l3 = add(l2, c1); Q = add(l3, b)
    copies = []
    for perm, sg in LS_SIGNED_PERMS:
        if (perm[1], sg[1]) != (1, 1):
            continue                                   # must fix the y-axis
        img = []
        for p in x2:
            v = (p[0] - x2[0][0], p[1] - x2[0][1], p[2] - x2[0][2])
            img.append(add((sg[0] * v[perm[0]], sg[1] * v[perm[1]], sg[2] * v[perm[2]]), Q))
        if tuple(img[1][i] - img[0][i] for i in range(3)) != c1 or tuple(img[2][i] - img[1][i] for i in range(3)) != b:
            continue
        if ls_valid_walk(img):
            copies.append(img)
    return (x1 + [l1, l2, l3] + copies[0]) if copies else None, down, len(copies)


@conjecture("XVIII.2 Lemma 11.68 (concatenation of bridges on the diamond lattice): for bridges x1, x2 with at least 3 beads the copy of x2 that continues the linker zigzag by a height-preserving lattice symmetry exists and is unique; x1, three linker beads and the copy form a bridge with N1 + N2 + 3 beads whose (h3, h8, h11, gauche) exceeds the sum by (d3, d8, d11, dg) with 0 <= d3 <= 1, 0 <= d8 <= 9, 0 <= d11 <= 14 and dg = [the second-to-last bond of x1 is a down-bond]; appending one bead to a bridge changes them by a vector in [0,1]x[0,3]x[0,6]x[0,1]")
def t_ls_concatenation(rng, trials):
    nfull, nsamp = (5, 8) if trials < 100 else (6, 9)
    br = {N: ls_enum(N, bridge=True) for N in range(3, nsamp + 1)}
    pr = {N: [ls_profile(w) for w in br[N]] for N in br}
    stats = dict(concatenations=0, max_d8=0, max_d11=0, gauche_linkers=0)
    for N in br:
        for w, p in zip(br[N], pr[N]):
            bp = w[-2][1] - w[-3][1]
            P = w[-1]
            cs = [tuple(w[-2][i] - w[-3][i] for i in range(3))] if bp == 1 else \
                [tuple(q[i] - P[i] for i in range(3)) for q in ls_nbrs(P) if q[1] == P[1] + 1]
            for c1 in cs:
                x = w + [(P[0] + c1[0], P[1] + c1[1], P[2] + c1[2])]
                if not (ls_valid_walk(x) and ls_is_bridge(x)):
                    return False, dict(reason="appending the prescribed bead does not give a bridge", N=N)
                q_ = ls_profile(x)
                d = tuple(q_[i] - p[i] for i in range(4))
                if not (0 <= d[0] <= 1 and 0 <= d[1] <= 3 and 0 <= d[2] <= 6 and d[3] == (0 if bp == 1 else 1)):
                    return False, dict(reason="one more bead changes the counts by more than (1, 3, 6; 1)", N=N, d=d)

    def check(N1, i, N2, j):
        x1, x2 = br[N1][i], br[N2][j]
        for which in ((0, 1) if x1[-2][1] - x1[-3][1] == -1 else (0,)):
            x, down, ncopies = ls_concat(x1, x2, which)
            if ncopies != 1:
                return dict(reason="the placing symmetry is not unique", copies=ncopies)
            if not (ls_valid_walk(x) and ls_is_bridge(x) and len(x) == N1 + N2 + 3):
                return dict(reason="the concatenation is not a bridge with N1 + N2 + 3 beads")
            p = ls_profile(x)
            d = tuple(p[k] - pr[N1][i][k] - pr[N2][j][k] for k in range(4))
            if not (0 <= d[0] <= 1 and 0 <= d[1] <= 9 and 0 <= d[2] <= 14):
                return dict(reason="a concatenation error is outside the proved interval", d=d)
            if d[3] != (1 if down else 0):
                return dict(reason="the gauche error is not [b' is a down-bond]", d=d, down=down)
            stats["concatenations"] += 1
            stats["max_d8"] = max(stats["max_d8"], d[1]); stats["max_d11"] = max(stats["max_d11"], d[2])
            stats["gauche_linkers"] += d[3]
        return None

    for N1 in range(3, nfull + 1):
        for N2 in range(3, nfull + 1):
            for i in range(len(br[N1])):
                for j in range(len(br[N2])):
                    bad = check(N1, i, N2, j)
                    if bad:
                        return False, bad
    for _ in range(max(150, trials)):
        N1, N2 = int(rng.integers(3, nsamp + 1)), int(rng.integers(3, nsamp + 1))
        bad = check(N1, int(rng.integers(len(br[N1]))), N2, int(rng.integers(len(br[N2]))))
        if bad:
            return False, bad
    return True, stats


def ls_cover_number(F, L, e, eps, norm):
    """least number of centres among the first components of F such that every (p, g) in F has a centre a with
    L |a - p| <= e g + eps  (brute force over subsets by increasing size)"""
    cents = sorted(set(p for p, _ in F))
    covers = [[i for i, (p, g) in enumerate(F) if L * norm(a, p) <= e * g + eps + 1e-12] for a in cents]
    full = set(range(len(F)))
    if set().union(*[set(c) for c in covers]) != full:
        return math.inf
    for k in range(1, len(cents) + 1):
        for comb in itertools.combinations(range(len(cents)), k):
            if set().union(*[set(covers[i]) for i in comb]) == full:
                return k
    return math.inf


@conjecture("XVIII.3 Lemma 11.70 (stability of covering numbers with position-dependent radii and internal centres): N(F, eps) is unchanged when points (p, t) with t above the lower boundary are added; if every point of F is within eta of F' and conversely (distance max(|dp|, |dg|)), then N(F', eps + (2L+e) eta) <= N(F, eps) <= N(F', eps - (2L+e) eta), and the constant 2L + e cannot be improved; and at a jump of eps -> N(F, eps) the covering numbers of a convergent sequence need not converge: F = {(0,0), (1,0)}, F_N = {(0,0), (1 + 1/N, 0)}, eps = L")
def t_ls_cover_stability(rng, trials):
    stats = dict(instances=0, strict_changes=0)
    l1 = lambda a, b: float(sum(abs(x - y) for x, y in zip(a, b)))
    for rep in range(max(40, trials // 2)):
        dim = int(rng.integers(1, 3))
        m = int(rng.integers(3, 8))
        L, e = float(rng.choice([0.5, 1.0, 2.0])), float(rng.choice([0.0, 0.5, 1.0]))
        F = [(tuple(float(v) for v in np.round(rng.uniform(0, 4, size=dim), 2)), float(np.round(rng.uniform(0, 1), 2)))
             for _ in range(m)]
        eps = float(rng.uniform(0.2, 2.5))
        eta = float(rng.choice([0.02, 0.1, 0.3]))
        n0 = ls_cover_number(F, L, e, eps, l1)
        # (a) the truncated epigraph: add points above existing ones
        Fup = F + [(p, min(1.5, g + float(rng.uniform(0, 1)))) for p, g in F[: m // 2 + 1]]
        if ls_cover_number(Fup, L, e, eps, l1) != n0:
            return False, dict(reason="adding points above the lower boundary changes the covering number")
        # (b) a perturbation within Hausdorff distance eta: move every point (adversarially: by exactly +-eta in one
        #     coordinate of p and by +-eta in g), and duplicate some points nearby
        F2 = []
        for p, g in F:
            k = int(rng.integers(dim))
            p2 = tuple(p[i] + (eta * float(rng.choice([-1.0, 1.0])) if i == k else 0.0) for i in range(dim))
            F2.append((p2, max(0.0, g + eta * float(rng.choice([-1.0, 0.0, 1.0])))))
        for p, g in F[:2]:
            F2.append((tuple(p[i] + (eta * float(rng.uniform(-1, 1)) if i == 0 else 0.0) for i in range(dim)), g))
        shift = (2 * L + e) * eta
        lo = ls_cover_number(F2, L, e, eps + shift, l1)
        hi = ls_cover_number(F2, L, e, eps - shift, l1)
        if not (lo <= n0 <= hi):
            return False, dict(reason="the two-sided stability inequality fails", n0=n0, lo=lo, hi=hi, L=L, e=e, eta=eta)
        stats["strict_changes"] += int(lo < n0) + int(n0 < hi)
        stats["instances"] += 1
    # the constant 2L + e cannot be improved: two points on the line, the client moved away by 2 eta in all and its
    # gauche credit lowered by eta
    l1s = lambda a, b: abs(a[0] - b[0])
    for (L, e, x, g, eta) in ((1.0, 1.0, 2.0, 0.5, 0.1), (0.5, 2.0, 3.0, 0.4, 0.05), (2.0, 0.5, 1.0, 0.6, 0.2)):
        eps = L * x - e * g
        F = [((0.0,), 0.0), ((x,), g)]
        F2 = [((-eta,), 0.0), ((x + eta,), g - eta)]
        shift = (2 * L + e) * eta
        if ls_cover_number(F, L, e, eps, l1s) != 1 or ls_cover_number(F2, L, e, eps + shift, l1s) > 1:
            return False, dict(reason="the stability inequality fails on the extremal two-point instance", L=L, e=e, eta=eta)
        if ls_cover_number(F2, L, e, eps + (2 * L + e) * eta - 0.01 * eta, l1s) != 2:
            return False, dict(reason="the constant 2L + e is not attained on the two-point instance", L=L, e=e, eta=eta)
    # the exceptional accuracy
    L = 1.0
    if ls_cover_number([((0.0,), 0.0), ((1.0,), 0.0)], L, 1.0, L, l1s) != 1:
        return False, dict(reason="the limit set at the jump accuracy is not covered by one centre")
    for N in (10, 1000, 10 ** 6):
        FN = [((0.0,), 0.0), ((1.0 + 1.0 / N,), 0.0)]
        if ls_cover_number(FN, L, 1.0, L, l1s) != 2:
            return False, dict(reason="the approximating sets are covered by one centre at the jump accuracy")
        if ls_cover_number(FN, L, 1.0, 1.01 * L, l1s) != (1 if N >= 1000 else 2):
            return False, dict(reason="off the jump the covering numbers do not converge as predicted", N=N)
    return True, stats


@conjecture("XVIII.4 The profile distance of the lattice chain (Theorem 11.48(b) with three distances 3, 8, 11 below the cutoff 12): the L1 distance of the cumulative pair-count functions on [0, 12) is ||dh||_c = 5|dh3| + 3|dh3 + dh8| + |dh3 + dh8 + dh11|; it is at most 9|dh3| + 4|dh8| + |dh11| with equality if and only if no two of the three differences have opposite signs; for a single profile both are 9h3 + 4h8 + h11")
def t_ls_profile_norm(rng, trials):
    stats = dict(pairs=0, strict=0)
    grid = np.arange(0, 12, 0.5) + 0.25                       # midpoints of half-unit cells on [0, 12)

    def cum(h):
        return (grid >= 3) * h[0] + (grid >= 8) * h[1] + (grid >= 11) * h[2]
    profs = sorted(set(ls_profile(w)[:3] for N in (8, 9) for w in ls_enum(N)))
    cand = [(profs[int(rng.integers(len(profs)))], profs[int(rng.integers(len(profs)))]) for _ in range(max(200, trials))]
    cand += [(tuple(int(v) for v in rng.integers(0, 9, size=3)), tuple(int(v) for v in rng.integers(0, 9, size=3)))
             for _ in range(max(200, trials))]
    for h, k in cand:
        d = (h[0] - k[0], h[1] - k[1], h[2] - k[2])
        l1 = float(np.abs(cum(h) - cum(k)).sum() * 0.5)
        if abs(l1 - ls_cnorm(d)) > 1e-9:
            return False, dict(reason="the cumulative norm is not the L1 distance of the cumulative profiles", h=h, k=k)
        if ls_cnorm(d) > ls_wnorm(d):
            return False, dict(reason="the cumulative norm exceeds the weighted form", d=d)
        mixed = any(d[i] * d[j] < 0 for i in range(3) for j in range(i + 1, 3))
        if (ls_cnorm(d) == ls_wnorm(d)) == mixed:
            return False, dict(reason="equality with the weighted form does not match the sign condition", d=d)
        if ls_cnorm(h) != 9 * h[0] + 4 * h[1] + h[2]:
            return False, dict(reason="the norm of a single profile is not 9h3 + 4h8 + h11", h=h)
        stats["pairs"] += 1; stats["strict"] += int(mixed)
    return True, stats


def ls_torsion_walk(states):
    """walk from torsion states: 't' or 0/1 (the two gauche continuations in increasing order of the bond index)"""
    b = [0, 1]
    for s in states:
        i, j = b[-2], b[-1]
        b.append(i if s == 't' else [k for k in range(4) if k not in (i, j)][s])
    p = (0, 0, 0)
    w = [p]
    for i in b:
        s = 1 if ls_is_a(p) else -1
        p = (p[0] + s * LS_BV[i][0], p[1] + s * LS_BV[i][1], p[2] + s * LS_BV[i][2])
        w.append(p)
    return w


@conjecture("XVIII.5 Proposition 11.74 (single-flip constants of the lattice chain): for the hairpin t^a g g g t^b (two adjacent stems) and the conformation with its middle fold torsion set to trans, the profile distance D satisfies -15 <= D - 14 d <= -5 with d = min(a, b) + 2, whenever d >= 5; and for every pair of conformations that differ in one torsion j the profile distance is at most 70 (d_j + 3), d_j = min(j, n + 1 - j)")
def t_ls_single_flip(rng, trials):
    stats = dict(hairpins=0, lo=10 ** 9, hi=-10 ** 9, flips=0, largest_ratio=0.0)
    amax = 10 if trials < 100 else 14
    for a in range(3, amax + 1):
        for b_ in range(3, amax + 1):
            best = None
            for fold in itertools.product((0, 1), repeat=3):
                w = ls_torsion_walk(['t'] * a + list(fold) + ['t'] * b_)
                if ls_valid_walk(w):
                    p = ls_profile(w)
                    if best is None or p[0] > best[0][0]:
                        best = (p, fold)
            p, fold = best
            w2 = ls_torsion_walk(['t'] * a + [fold[0], 't', fold[2]] + ['t'] * b_)
            if not ls_valid_walk(w2):
                return False, dict(reason="the opened hairpin is not self-avoiding", a=a, b=b_)
            p2 = ls_profile(w2)
            D = ls_cnorm((p[0] - p2[0], p[1] - p2[1], p[2] - p2[2]))
            d = min(a, b_) + 2
            if d >= 5:
                if not (-15 <= D - 14 * d <= -5):
                    return False, dict(reason="the hairpin flip is outside 14 d - 15 ... 14 d - 5", a=a, b=b_, D=D)
                stats["lo"] = min(stats["lo"], D - 14 * d); stats["hi"] = max(stats["hi"], D - 14 * d)
                stats["hairpins"] += 1
    # random single flips of random self-avoiding conformations
    n = 9
    for _ in range(max(300, trials)):
        st = [('t' if rng.random() < 0.4 else int(rng.integers(2))) for _ in range(n)]
        w = ls_torsion_walk(st)
        if not ls_valid_walk(w):
            continue
        j = int(rng.integers(n))
        alt = [s for s in ('t', 0, 1) if s != st[j]]
        st2 = list(st); st2[j] = alt[int(rng.integers(2))]
        w2 = ls_torsion_walk(st2)
        if not ls_valid_walk(w2):
            continue
        p, p2 = ls_profile(w), ls_profile(w2)
        D = ls_cnorm((p[0] - p2[0], p[1] - p2[1], p[2] - p2[2]))
        dj = min(j + 1, n - j)
        if D > 70 * (dj + 3):
            return False, dict(reason="a single flip changes the profile by more than 70 (d_j + 3)", D=D, dj=dj)
        stats["largest_ratio"] = max(stats["largest_ratio"], D / (70.0 * (dj + 3)))
        stats["flips"] += 1
    return True, stats


@conjecture("XVIII.6 Proposition 11.72(b), exact certificates: on the eight-site cluster of a lattice bond (v, w; u1..u3; z1..z3) with integer multipliers y1..y6 of the star relations P(v, w=1, u1=0, u2, u3) = P(v, w=0, u1=1, u2, u3) and y0 = b + c3 + c8, the function c3*2[v][w] + c8*(C(d_v,2) + C(d_w,2))/2 + c11*sum_{j != k} u_j z_k - sum_k y_k r_k - y0 [v], averaged over the 12 symmetries of the cluster, is <= 0 on every pattern whose occupied centres have at least two occupied neighbours and <= M on the others — in exact rational arithmetic, for each of the eleven rows")
def t_ls_exact_certificates(rng, trials):
    V_, W_, U_, Z_ = 0, 1, (2, 3, 4), (5, 6, 7)
    ex = {V_: W_, W_: V_}
    for j in range(3):
        ex[U_[j]] = Z_[j]; ex[Z_[j]] = U_[j]
    syms = []
    for pj in itertools.permutations(range(3)):
        m = list(range(8))
        for j in range(3):
            m[U_[j]] = U_[pj[j]]; m[Z_[j]] = Z_[pj[j]]
        syms.append(m)
        syms.append([ex[m[s]] for s in range(8)])
    dv = lambda s: s[W_] + s[2] + s[3] + s[4]
    dw = lambda s: s[V_] + s[5] + s[6] + s[7]

    def star(k, s):
        v, u2, u3 = LS_STAR_KEYS[k]
        base = s[V_] == v and s[U_[1]] == u2 and s[U_[2]] == u3
        return int(base and s[W_] == 1 and s[U_[0]] == 0) - int(base and s[W_] == 0 and s[U_[0]] == 1)

    def gfun(s, c, y, y0):
        val = Fraction(c[0] * 2 * s[V_] * s[W_]) + Fraction(c[1] * (math.comb(dv(s), 2) + math.comb(dw(s), 2)), 2)
        val += c[2] * sum(s[U_[j]] * s[Z_[k]] for j in range(3) for k in range(3) if j != k)
        return val - sum(y[k] * star(k, s) for k in range(6)) - y0 * s[V_]
    stats = dict(rows=0, tight_patterns=0)
    for (c, b, M_) in LS_ROWS:
        y, y0 = LS_CERT[c]
        if y0 != b + c[0] + c[1]:
            return False, dict(reason="y0 is not b + c3 + c8", row=c)
        for s in itertools.product((0, 1), repeat=8):
            if not any(s):
                continue
            avg = sum(gfun(tuple(s[m[i]] for i in range(8)), c, y, y0) for m in syms) / 12
            forbidden = (s[V_] and dv(s) < 2) or (s[W_] and dw(s) < 2)
            if avg > (M_ if forbidden else 0):
                return False, dict(reason="a dual certificate fails on a cluster pattern", row=c, pattern=s)
            stats["tight_patterns"] += int(avg == 0 and not forbidden)
        stats["rows"] += 1
    return True, stats


# ----------------------------------------------------------------------------------------------
# XIX. Known parts that are functions of the type (mean-field models; theory report 11.23)
# ----------------------------------------------------------------------------------------------

def mf_hb(x):
    """Binary entropy in nats (vectorised)."""
    x = np.clip(np.asarray(x, float), 1e-300, 1 - 1e-16)
    return -(x * np.log(x) + (1 - x) * np.log1p(-x))


def mf_model(bJ, bB, u, K=40001):
    """Curie-Weiss known part f = n phi(|x|/n), phi(k) = -(bJ/2)(2k-1)^2 - bB(2k-1): rate function I = phi - h - min and its
    largest u-Lipschitz minorant v (tables on a grid of K points; I also exactly)."""
    kap = np.linspace(0, 1, K)
    phi = lambda k: -(bJ / 2) * (2 * np.asarray(k, float) - 1) ** 2 - bB * (2 * np.asarray(k, float) - 1)
    raw = phi(kap) - mf_hb(kap)
    c = float(raw.min())
    Ik = raw - c
    v = np.minimum(np.minimum.accumulate(Ik - u * kap) + u * kap, np.minimum.accumulate((Ik + u * kap)[::-1])[::-1] - u * kap)
    return dict(u=u, kap=kap, Ik=Ik, vk=v, I=lambda x: phi(x) - mf_hb(x) - c, v=lambda x: np.interp(x, kap, v), phi=phi)


def mf_MI(lam, nu):
    """Mutual information between the block label and the letter: h(type) - sum_j lam_j h(nu_j) (last axis = blocks)."""
    nu = np.asarray(nu, float)
    return mf_hb((nu * lam).sum(axis=-1)) - (mf_hb(nu) * lam).sum(axis=-1)


def mf_alpha(M, lam, mu):
    return float(mf_MI(lam, mu) + M["I"](float((np.asarray(mu) * lam).sum())))


def mf_golden(f, a, b, tol=1e-12):
    """Golden-section minimisation of a unimodal function on [a, b]; returns (minimum value seen, its argument)."""
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d)
    best = min((fc, c), (fd, d))
    while b - a > tol:
        if fc <= fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = f(c)
            best = min(best, (fc, c))
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = f(d)
            best = min(best, (fd, d))
    return best


def mf_inner(M, lam, mu, B, G=1500):
    """V(mu, B) = min{ MI(nu) : u dist(nu, mu) + v(type of nu) <= B } over clippings nu_j = clip(mu_j, c_lo, c_hi) (Lemma
    11.77(a)); the constraint is nonincreasing in c_hi, so for every c_lo the best c_hi is the smallest feasible one
    (bisection); scan over c_lo, golden-section refinement at every local minimum of the scan (plateaus count once)."""
    lam = np.asarray(lam, float)
    mu = np.asarray(mu, float)
    u = M["u"]

    def g_mi(clo, chi):
        nu = np.clip(mu[None, :], clo[:, None], chi[:, None])
        return u * (np.abs(nu - mu[None, :]) * lam).sum(axis=1) + M["v"]((nu * lam).sum(axis=1)) - B, mf_MI(lam, nu)

    def best_for(clo):
        lo, hi = clo.copy(), np.ones_like(clo)
        feas = g_mi(clo, hi)[0] <= 0
        full = g_mi(clo, lo)[0] <= 0
        for _ in range(48):
            mid = 0.5 * (lo + hi)
            ok = g_mi(clo, mid)[0] <= 0
            hi = np.where(ok, mid, hi)
            lo = np.where(ok, lo, mid)
        mi = np.where(full, 0.0, g_mi(clo, hi)[1])
        return np.where(feas, mi, np.inf)

    clo = np.linspace(0, 1, G)
    val = best_for(clo)
    if not np.isfinite(val).any():
        return float("inf")
    cand = [i for i in range(G) if np.isfinite(val[i]) and (i == 0 or not np.isfinite(val[i - 1]) or val[i] <= val[i - 1])
            and (i == G - 1 or val[i] <= val[i + 1])]
    runs = []
    for i in cand:
        if runs and i == runs[-1][-1] + 1:
            runs[-1].append(i)
        else:
            runs.append([i])
    best = float(val.min())
    for run in sorted(runs, key=lambda r: val[r[0]])[:6]:
        for i in {run[0], run[-1]}:
            a, b = clo[max(i - 2, 0)], clo[min(i + 2, G - 1)]
            best = min(best, mf_golden(lambda c: float(best_for(np.array([c]))[0]), a, b, tol=1e-11)[0])
    return best


def mf_r(M, lam, mu, e, G=1500):
    """r_mu(e) = V(mu, e + alpha(mu))."""
    return mf_inner(M, lam, mu, e + mf_alpha(M, lam, mu), G)


def mf_grid2(M, lam, mu, B, G, use_I):
    """The same minimum for two blocks on a full G x G grid of exit profiles (no clipping lemma), with v or with I in the
    constraint; returns the minimum over the feasible grid points."""
    ax = np.linspace(0, 1, G)
    N1, N0 = np.meshgrid(ax, ax, indexing="ij")
    nb = lam[0] * N1 + lam[1] * N0
    mi = mf_hb(nb) - lam[0] * mf_hb(N1) - lam[1] * mf_hb(N0)
    pen = M["I"](nb) if use_I else M["v"](nb)
    feas = M["u"] * (lam[0] * np.abs(N1 - mu[0]) + lam[1] * np.abs(N0 - mu[1])) + pen <= B
    return float(mi[feas].min()) if feas.any() else float("inf")


def mf_kl(a, p):
    return a * math.log(a / p) + (1 - a) * math.log((1 - a) / (1 - p))


def mf_R_unif(e, u):
    """Hinted exponent of the uniform cube: KL((Lambda_1 + e)/u || 1/2), Lambda_1 = ln(2/(1 + e^-u))."""
    rho = (math.log(2 / (1 + math.exp(-u))) + e) / u
    return mf_kl(rho, 0.5) if 0 < rho < 0.5 else 0.0


@conjecture("XIX.1 Theorem 11.76(c) (the flat-histogram instance is the hardest symmetric instance, for every n and every exchangeable known part): with J_t = -ln pi(T_t), V_n = the largest u-Lipschitz minorant of J, an instance g(|x|), its landscape Lambda_g(t) = -g(t) + min_t'[J_t' + g(t')] and Z_g = sum_t e^{-(J_t - Lambda_g(t))}: Lambda_g <= V_n with equality for H = -V_n, 1 <= Z_g <= n+1, the deepest dip on a set D is in L_u, A(dip)/A = 1 + Phi_g(D) with Phi_g(D) + mu_g(D) = Z_g^{-1} sum_{x in D} pi(x) exp(min_{y not in D}[u d(x,y) + Lambda_g(|y|)]), and Z_g Phi_g^+(D) <= Z_H Phi_H^+(D), hence Phi_g^+(D) <= (n+1) Phi_H^+(D); the factor cannot be dropped")
def t_mf_hardest_symmetric(rng, trials):
    stats = dict(sets=0, worst_ratio=0.0, largest_over_H=0.0)
    for n in (4, 5, 6):
        D = na_cube(n)
        wt = D[0]
        N = 2 ** n
        nbr = [[x ^ (1 << i) for i in range(n)] for x in range(N)]
        binom = np.array([math.comb(n, t) for t in range(n + 1)], float)
        for rep in range(max(8, trials // 12)):
            u = float(rng.choice([0.3, 0.5, 1.0, 2.0]))
            kind = rep % 4
            if kind == 0:      # two wells
                J = np.array([1.5 * n * (2 * t / n - 1) ** 2 * (-1) + 0.0 for t in range(n + 1)]) * 0.3 + rng.normal(0, 0.2, n + 1)
            elif kind == 1:    # flat over the types
                J = np.zeros(n + 1)
            elif kind == 2:    # binomial (uniform cube)
                J = -np.log(binom / 2 ** n)
            else:
                J = rng.uniform(0, 2.5 * u, n + 1)
            p = np.exp(-J)
            p = p / p.sum()
            J = -np.log(p)
            pi = (p / binom)[wt]
            tt = np.arange(n + 1)
            Vn = (J[None, :] + u * np.abs(tt[:, None] - tt[None, :])).min(axis=1)
            if np.any(Vn > J + 1e-12) or np.any(np.abs(np.diff(Vn)) > u + 1e-12) or abs((J - Vn).min()) > 1e-12:
                return False, dict(reason="V_n is not a u-Lipschitz minorant of J touching it", n=n)
            gs = [-Vn, np.zeros(n + 1), float(rng.uniform(-u, u)) * tt, u * np.abs(tt - n // 2).astype(float),
                  np.concatenate([[0.0], np.cumsum(rng.uniform(-u, u, n))])]
            ZH = float(np.exp(-(J - Vn)).sum())
            for gi, g in enumerate(gs):
                Lam = -g + (J + g).min()
                Zg = float(np.exp(-(J - Lam)).sum())
                if np.any(Lam > Vn + 1e-10) or np.any(np.abs(np.diff(Lam)) > u + 1e-10):
                    return False, dict(reason="the landscape of an instance is not a u-Lipschitz function below V_n", n=n, instance=gi)
                if gi == 0 and np.abs(Lam - Vn).max() > 1e-10:
                    return False, dict(reason="the landscape of H is not V_n", n=n)
                if not (1 - 1e-12 <= Zg <= n + 1 + 1e-12):
                    return False, dict(reason="Z_g outside [1, n+1]", n=n, Z=Zg)
                psi = g[wt]
                A = float((pi * np.exp(-psi)).sum())
                mug = pi * np.exp(-psi) / A
                for srep in range(4):
                    if srep == 0:
                        mask = rng.random(N) < rng.uniform(0.05, 0.6)
                    elif srep == 1:
                        mask = D[int(rng.integers(N))] <= int(rng.integers(0, n // 2 + 1))
                    elif srep == 2:
                        c = int(rng.integers(N))
                        r = int(rng.integers(1, n))
                        mask = (D[c] >= r) & (D[c] <= r + 1) & (rng.random(N) < 0.8)
                    else:
                        mask = np.zeros(N, bool)
                        mask[int(rng.choice(np.flatnonzero(wt == n // 2)))] = True
                    if not mask.any() or mask.all():
                        continue
                    out = ~mask

                    def dip_and_plus(psi_, Lam_, Z_, A_):
                        dip = psi_.copy()
                        dip[mask] = (psi_[None, out] - u * D[np.ix_(mask, out)]).max(axis=1)
                        if np.any(dip > psi_ + 1e-12) or any(abs(dip[x] - dip[y]) > u + 1e-10 for x in range(N) for y in nbr[x]):
                            return None
                        phi = float((pi * np.exp(-dip)).sum()) / A_ - 1
                        plus = phi + float((pi * np.exp(-psi_))[mask].sum()) / A_
                        form = float((pi[mask] * np.exp((u * D[np.ix_(mask, out)] + Lam_[wt][None, out]).min(axis=1))).sum()) / Z_
                        return plus, form
                    rg = dip_and_plus(psi, Lam, Zg, A)
                    psiH = -Vn[wt]
                    rH = dip_and_plus(psiH, Vn, ZH, float((pi * np.exp(-psiH)).sum()))
                    if rg is None or rH is None:
                        return False, dict(reason="the deepest dip is not a member of L_u below the instance", n=n, instance=gi)
                    if abs(rg[0] - rg[1]) > 1e-9 * max(1.0, rg[0]) or abs(rH[0] - rH[1]) > 1e-9 * max(1.0, rH[0]):
                        return False, dict(reason="formula for Phi^+ in terms of the landscape", n=n, instance=gi, direct=rg[0], formula=rg[1])
                    if Zg * rg[0] > ZH * rH[0] * (1 + 1e-9):
                        return False, dict(reason="Z_g Phi_g^+(D) > Z_H Phi_H^+(D)", n=n, instance=gi)
                    if rg[0] > (n + 1) * rH[0] * (1 + 1e-9):
                        return False, dict(reason="Phi_g^+(D) > (n+1) Phi_H^+(D)", n=n, instance=gi)
                    stats["worst_ratio"] = max(stats["worst_ratio"], rg[0] / ((n + 1) * rH[0]))
                    stats["largest_over_H"] = max(stats["largest_over_H"], rg[0] / rH[0])
                    stats["sets"] += 1
    if stats["largest_over_H"] <= 1.02:
        return False, dict(reason="no instance with Phi_g^+ > Phi_H^+ was seen: the factor would be superfluous", **stats)
    return True, stats


@conjecture("XIX.2 Lemma 11.77 (the inner problem of the single-letter theory): for a block profile mu and a budget B the minimum of MI(nu) over {u dist(nu, mu) + v(type) <= B} is attained at a clipping nu_j = clip(mu_j, c_lo, c_hi) and is the same with the rate function I in place of its largest u-Lipschitz minorant v (two blocks: against full grids of exit profiles); thinning a profile to a type kappa* (nu_j kappa*/type, or the mirror image upwards) moves it by exactly |type - kappa*| and does not increase MI")
def t_mf_inner_problem(rng, trials):
    stats = dict(profiles=0, positive=0, worst_gap=0.0, thinnings=0)
    G = 420
    for (bJ, bB, u) in ((1.5, 0.0, 1.0), (0.5, 0.3, 1.0), (2.0, 0.1, 0.5)):
        M = mf_model(bJ, bB, u)
        done = 0
        while done < (4 if trials < 100 else 8):
            m = float(rng.uniform(0.3, 0.7))
            lam = np.array([m, 1 - m])
            mu = np.array([1 - rng.uniform(0.15, 0.4), rng.uniform(0.15, 0.4)])
            e = float(rng.choice([-0.03, 0.0, 0.01, 0.03]))
            B = e + mf_alpha(M, lam, mu)
            if B < float(M["v"]((lam * mu).sum())):
                continue
            fast = mf_inner(M, lam, mu, B)
            gv = mf_grid2(M, lam, mu, B, G, False)
            gI = mf_grid2(M, lam, mu, B, G, True)
            # a grid point within one cell of the minimiser is feasible up to the slack 2u/G; allow for it through B
            gv_lo = mf_grid2(M, lam, mu, B + 2.5 * u / G, G, False)
            gI_lo = mf_grid2(M, lam, mu, B + 2.5 * u / G + 2e-3, G, True)
            if fast > min(gv, gI) + 1e-7:
                return False, dict(reason="a grid profile beats every clipping", model=(bJ, bB, u), fast=fast, grid_v=gv, grid_I=gI)
            if fast < gv_lo - 6.0 / G or fast < gI_lo - 6.0 / G:
                return False, dict(reason="the clipping value is below the grid minimum by more than the resolution", model=(bJ, bB, u), fast=fast, grid_v=gv_lo, grid_I=gI_lo)
            stats["worst_gap"] = max(stats["worst_gap"], min(gv, gI) - fast)
            stats["profiles"] += 1
            stats["positive"] += fast > 1e-4
            done += 1
    if stats["positive"] < 4:
        return False, dict(reason="too few profiles with a positive value (the test would be void)", **stats)
    for _ in range(trials):
        k = int(rng.integers(2, 6))
        lam = rng.dirichlet(np.ones(k))
        nu = rng.uniform(0.01, 0.99, k)
        t = float((lam * nu).sum())
        ks = float(rng.uniform(0.01, 0.99))
        if ks <= t:
            nu2 = nu * ks / t
        else:
            nu2 = nu + (1 - nu) * (ks - t) / (1 - t)
        if abs(float((lam * nu2).sum()) - ks) > 1e-12 or abs(float((lam * np.abs(nu2 - nu)).sum()) - abs(ks - t)) > 1e-12:
            return False, dict(reason="thinning does not move the profile by |type - kappa*|")
        if float(mf_MI(lam, nu2)) > float(mf_MI(lam, nu)) + 1e-12:
            return False, dict(reason="thinning increased the mutual information", k=k)
        stats["thinnings"] += 1
    return True, stats


MF_TWO_PHASE = dict(R0=0.0251012, x0=0.29803, R002=0.0152765, x002=0.30553, S3=(0.2774, 0.1408, 0.016155), cone_at_S0=0.0020379)


@conjecture("XIX.3 Two phases (Curie-Weiss, beta J = 1.5, B = 0, u = 1; theory report 11.23, Proposition 11.82): the symmetric shell (1/2; x, x) in the barrier type class with x = 0.29803 has r_mu(0) = 0.0251012 and is a local maximum over binary centres; every profile evaluated stays below the uniform cube's KL(Lambda_1/u || 1/2) = 0.0291391 (Proposition 11.81(a)); e + r_mu(e) is increasing near 0 and n_mu(S(0)) = min{r_mu(e') : e' + r_mu(e') <= S(0)} = r_mu(0) (pair identity, Theorem 11.79(b)); the truncated cone around the shell attains the same value at accuracy S(0) while the truncated cone around a point gives 0.00204; the cone formula gives about 0.0107; and at e = 0.02 the three-block profile with a free block of weight 0.1408 at type 1/2 and shells x = 0.2774 has r = 0.016155, above the best binary centre 0.0152765")
def t_mf_two_phase(rng, trials):
    M = mf_model(1.5, 0.0, 1.0)
    c = MF_TWO_PHASE
    half = np.array([0.5, 0.5])
    shell = lambda x: np.array([1 - x, x])
    r0 = mf_r(M, half, shell(c["x0"]), 0.0)
    if abs(r0 - c["R0"]) > 4e-7:
        return False, dict(reason="value of the barrier shell at e = 0", value=r0)
    Ru = mf_R_unif(0.0, 1.0)
    if abs(Ru - 0.0291391) > 1e-7:
        return False, dict(reason="uniform cube", value=Ru)
    worst = 0.0
    for dm, da, db in ((0, 0.004, 0.004), (0, -0.004, -0.004), (0, 0.003, -0.003), (0.01, 0, 0), (-0.01, 0.002, 0), (0.006, -0.003, 0.003)):
        lam = np.array([0.5 + dm, 0.5 - dm])
        val = mf_r(M, lam, np.array([1 - c["x0"] - da, c["x0"] + db]), 0.0)
        worst = max(worst, val)
        if val > r0 + 1e-7:
            return False, dict(reason="a neighbouring binary centre beats the symmetric shell", shift=(dm, da, db), value=val)
        if val > Ru + 1e-9:
            return False, dict(reason="a profile of a ferromagnet beats the uniform cube", value=val)
    # pair identity through r_mu
    es = np.linspace(-0.003, 0.003, 13)
    rv = np.array([mf_r(M, half, shell(c["x0"]), float(e)) for e in es])
    S = es + rv
    if np.any(np.diff(S) <= 0) or np.any(np.diff(rv) >= 0):
        return False, dict(reason="e + r_mu(e) is not increasing, or r_mu not decreasing, near e = 0")
    X = c["R0"]
    n_mu = float(rv[S <= X + 2e-7].min())
    if abs(n_mu - r0) > 1e-6:
        return False, dict(reason="pair identity at the barrier shell", n_mu=n_mu, r=r0)
    # shell-cones on a grid: theta_shell(X; mu0) = min{MI : G_mu0 - min G_mu0 <= X}
    G = 700
    ax = np.linspace(0, 1, G)
    N1, N0 = np.meshgrid(ax, ax, indexing="ij")
    nb = 0.5 * (N1 + N0)
    mi = mf_hb(nb) - 0.5 * mf_hb(N1) - 0.5 * mf_hb(N0)

    def theta_shell(mu0):
        Gf = mi + M["I"](nb) + 0.5 * (np.abs(N1 - mu0[0]) + np.abs(N0 - mu0[1]))
        return float(mi[Gf - Gf.min() <= X].min())
    ts, tc = theta_shell(shell(c["x0"])), theta_shell(np.array([1.0, 0.0]))
    if abs(ts - r0) > 2.5e-4:
        return False, dict(reason="the truncated cone around the barrier shell does not attain the dip exponent", value=ts)
    if abs(tc - c["cone_at_S0"]) > 1.5e-4 or tc > 0.1 * r0:
        return False, dict(reason="the truncated cone around a point", value=tc)
    # cone formula at centre type 1/2: min{MI(z) : u rho + v(kappa_z) - Lambda_m <= 0}
    A_, B_ = 1 - N1, N0
    rho = 0.5 * (A_ + B_)
    Lam = float((mi + M["I"](nb) + rho).min())
    feas = rho + M["v"](nb) - Lam <= 0
    cone = float(mi[feas].min())
    if not (0.0100 <= cone <= 0.0114):
        return False, dict(reason="cone formula", value=cone)
    # the free block at e = 0.02
    x3, lf, v3 = c["S3"]
    s3 = mf_r(M, np.array([(1 - lf) / 2, lf, (1 - lf) / 2]), np.array([1 - x3, 0.5, x3]), 0.02)
    b2 = -mf_golden(lambda x: -mf_r(M, half, shell(x), 0.02), 0.295, 0.315, tol=2e-5)[0]
    if abs(s3 - v3) > 3e-6 or abs(b2 - c["R002"]) > 5e-7:
        return False, dict(reason="values at e = 0.02", three_blocks=s3, binary=b2)
    if s3 < 1.05 * b2:
        return False, dict(reason="the free block does not beat the binary centre by 5% at e = 0.02", three_blocks=s3, binary=b2)
    # at e = 0 the same construction loses
    s30 = max(mf_r(M, np.array([(1 - l) / 2, l, (1 - l) / 2]), np.array([1 - x, 0.5, x]), 0.0) for (x, l) in ((0.2715, 0.14), (0.285, 0.07), (0.295, 0.02)))
    if s30 > r0 + 1e-7:
        return False, dict(reason="a free block beats the binary shell at e = 0", value=s30)
    return True, dict(shell=r0, uniform=Ru, n_mu=n_mu, shell_cone=ts, point_cone=tc, cone_formula=cone, three_blocks=s3, binary_002=b2, free_block_at_0=s30)


@conjecture("XIX.4 Proposition 11.81(b) (the junction with the uniform cube is at beta J* = 1 + u c2/(2L) > 1, not at the critical coupling; B = 0, u = 1, e = 0: rho = Lambda_1/u, c2 = 1/(2 rho (1 - rho)) - 2, L = ln((1 - rho)/rho), beta J* = 1.12498): at the uniform cube's optimal shell (1/2; p_u, p_u) the single-letter value equals KL(rho || 1/2) = 0.0291391 for beta J = 0.6, 1.0, 1.08, 1.12 and is strictly smaller for beta J = 1.13, 1.14, 1.2, 1.5; for beta J < beta J* the exit profile (rho-bar - t, rho-bar + t) on the constraint curve has MI increasing in |t|, for beta J > beta J* decreasing at small |t|")
def t_mf_junction(rng, trials):
    u = 1.0
    rho = math.log(2 / (1 + math.exp(-u))) / u
    c2 = 1 / (2 * rho * (1 - rho)) - 2
    L = math.log((1 - rho) / rho)
    bstar = 1 + u * c2 / (2 * L)
    if abs(bstar - 1.12498) > 2e-5:
        return False, dict(reason="value of beta J*", value=bstar)
    pu = 1 / (1 + math.exp(u))
    Ru = mf_R_unif(0.0, u)
    half = np.array([0.5, 0.5])
    mu = np.array([1 - pu, pu])
    out = {}
    for bJ in (0.6, 1.0, 1.08, 1.12, 1.13, 1.14, 1.2, 1.5):
        M = mf_model(bJ, 0.0, u, K=80001)
        val = mf_r(M, half, mu, 0.0, G=3000)
        out[bJ] = val
        if val > Ru + 1e-8:
            return False, dict(reason="a ferromagnet above the uniform cube", bJ=bJ, value=val)
        if (bJ < bstar) != (abs(val - Ru) < 2e-7):
            return False, dict(reason="equality with the uniform cube holds exactly below beta J*", bJ=bJ, value=val, uniform=Ru, bstar=bstar)
        # second-order test along the constraint curve: exits (a', b') = (rb - t, rb + t) in the coordinates of the centre,
        # i.e. nu = (1 - rb + t, rb + t): type 1/2 + t, dist = |rb - pu|; the constraint u dist + I(1/2 + t) = e + alpha fixes rb
        B = mf_alpha(M, half, mu)
        def mi_on_curve(t):
            rb = pu + (B - float(M["I"](0.5 + t))) / u
            return float(mf_MI(half, np.array([1 - rb + t, rb + t])))
        t = 0.01
        curv = mi_on_curve(t) + mi_on_curve(-t) - 2 * mi_on_curve(0.0)
        pred = 2 * t * t * (c2 + 2 * (1 - bJ) * L / u)
        if abs(curv - pred) > 0.05 * abs(pred) + 2e-9:
            return False, dict(reason="second-order coefficient c2 + 2(1 - beta J) L/u", bJ=bJ, numerical=curv, predicted=pred)
        if (curv > 0) != (bJ < bstar):
            return False, dict(reason="the symmetric exit is a local minimum exactly below beta J*", bJ=bJ)
    return True, dict(bstar=bstar, uniform=Ru, at_1_12=out[1.12], at_1_14=out[1.14], at_1_5=out[1.5])


def mf_classes(n, k):
    """Classes (i, j) around a centre of type k on Q_n: i = number of ones of the centre set to zero, j = number of its zeros
    set to one; type t = k - i + j; number of points C(k, i) C(n - k, j)."""
    ii, jj = np.meshgrid(np.arange(k + 1), np.arange(n - k + 1), indexing="ij")
    logc = np.array([[math.lgamma(k + 1) - math.lgamma(i + 1) - math.lgamma(k - i + 1) + math.lgamma(n - k + 1) - math.lgamma(j + 1) - math.lgamma(n - k - j + 1)
                      for j in range(n - k + 1)] for i in range(k + 1)])
    return ii, jj, k - ii + jj, logc


def mf_l1_transform(cost, u):
    """T(i, j) = min over (i', j') of [cost(i', j') + u(|i - i'| + |j - j'|)] (two-pass l1 distance transform, exact)."""
    T = cost.copy()
    for axis in (0, 1):
        T = np.moveaxis(T, axis, 0)
        for a in range(1, T.shape[0]):
            T[a] = np.minimum(T[a], T[a - 1] + u)
        for a in range(T.shape[0] - 2, -1, -1):
            T[a] = np.minimum(T[a], T[a + 1] + u)
        T = np.moveaxis(T, 0, axis)
    return T


@conjecture("XIX.5 Theorem 11.78(a) on exact sums (every n): for the flat-histogram instance of a Curie-Weiss known part, a centre of type k with classes (i, j) and the budget neighbourhood D = {classes with u l1((i,j),(i0,j0)) + V_n(type) < nB} of the class of a profile mu: the class-level formulas dens_t(D) = sum C(k,i)C(n-k,j)/C(n,t) and Phi^+(D) = Z^{-1} sum pi(class) e^{T(i,j)}, T the l1 distance transform of V_n over the classes outside D, agree with brute force on the full cube (n = 8, 10); and for n = 60, 120: ln(1 + Phi(D)) >= n(B - alpha_n(mu)) - ln 2 - ln Z and maxdens(D) <= (n+1)^2 exp(-n V(mu, B))")
def t_mf_exact_sums(rng, trials):
    stats = dict(brute=0, bounds=0, tightest_dens=-1e9, tightest_phi=1e9)

    def setup(n, bJ, bB, u):
        t = np.arange(n + 1)
        logbin = np.array([math.lgamma(n + 1) - math.lgamma(a + 1) - math.lgamma(n - a + 1) for a in t])
        lw = logbin + n * ((bJ / 2) * (2 * t / n - 1) ** 2 + bB * (2 * t / n - 1))
        J = -(lw - (lw.max() + math.log(np.exp(lw - lw.max()).sum())))
        Vn = (J[None, :] + u * np.abs(t[:, None] - t[None, :])).min(axis=1)
        return J, Vn, logbin

    def class_level(n, k, J, Vn, logbin, u, i0, j0, nB):
        ii, jj, tt, logc = mf_classes(n, k)
        inD = u * (np.abs(ii - i0) + np.abs(jj - j0)) + Vn[tt] < nB
        if inD.all() or not inD.any():
            return None
        T = mf_l1_transform(np.where(inD, np.inf, Vn[tt]), u)
        logpi = -J[tt] - logbin[tt] + logc            # ln pi(class)
        ZH = float(np.exp(-(J - Vn)).sum())
        plus = float(np.exp(logpi[inD] + T[inD]).sum()) / ZH
        muD = float(np.exp(logpi[inD] + Vn[tt][inD]).sum()) / ZH
        dens = np.zeros(n + 1)
        np.add.at(dens, tt[inD], np.exp(logc[inD] - logbin[tt[inD]]))
        return inD, plus, plus - muD, float(dens.max()), ZH, logpi

    # (1) brute force on full cubes
    for n in (8, 10):
        D = na_cube(n)
        wt = D[0]
        N = 2 ** n
        for rep in range(3 if trials < 100 else 6):
            bJ, bB, u = [(1.5, 0.0, 1.0), (0.5, 0.3, 1.0), (2.0, 0.1, 0.5)][rep % 3]
            J, Vn, logbin = setup(n, bJ, bB, u)
            k = int(rng.integers(n // 2 - 1, n // 2 + 2))
            s = sum(1 << b for b in rng.choice(n, size=k, replace=False))
            i0, j0 = int(rng.integers(1, max(2, k // 2 + 1))), int(rng.integers(1, max(2, (n - k) // 2 + 1)))
            nB = float(Vn[k - i0 + j0] + u * rng.uniform(0.6, 2.6))
            res = class_level(n, k, J, Vn, logbin, u, i0, j0, nB)
            if res is None:
                continue
            inD, plus, phi, dens, ZH, _ = res
            x = np.arange(N)
            ci = np.array([bin(v & s).count("1") for v in x])        # ones of the centre kept
            cj = wt - ci                                              # ones outside the centre
            mask = inD[k - ci, cj]
            pi = np.exp(-J[wt] - logbin[wt])
            psiH = -Vn[wt]
            A = float((pi * np.exp(-psiH)).sum())
            out = ~mask
            dip = psiH.copy()
            dip[mask] = (psiH[None, out] - u * D[np.ix_(mask, out)]).max(axis=1)
            phi_b = float((pi * np.exp(-dip)).sum()) / A - 1
            dens_b = max(float(mask[wt == a].mean()) for a in range(n + 1))
            if abs(phi_b - phi) > 1e-9 * max(1.0, abs(phi)) or abs(dens_b - dens) > 1e-12:
                return False, dict(reason="class-level formulas against brute force", n=n, model=(bJ, bB, u), phi=phi, brute=phi_b, dens=dens, dens_brute=dens_b)
            stats["brute"] += 1
    # (2) the bounds of Theorem 11.78(a)
    for n in (60, 120):
        for (bJ, bB, u) in ((1.5, 0.0, 1.0), (0.5, 0.3, 1.0)):
            M = mf_model(bJ, bB, u)
            J, Vn, logbin = setup(n, bJ, bB, u)
            k = n // 2
            for (fa, fb, e) in ((0.3, 0.3, 0.0), (0.3, 0.3, 0.02), (0.25, 0.35, 0.01), (0.2, 0.2, -0.02)):
                i0, j0 = round(fa * k), round(fb * (n - k))
                lam = np.array([k / n, 1 - k / n])
                mu = np.array([1 - i0 / k, j0 / (n - k)])
                ii, jj, tt, logc = mf_classes(n, k)
                alpha_n = float(J[k - i0 + j0] + logbin[k - i0 + j0] - logc[i0, j0]) / n      # -ln pi(class)/n
                nB = n * (e + alpha_n)
                if nB <= Vn[k - i0 + j0] + math.log(2):
                    continue
                res = class_level(n, k, J, Vn, logbin, u, i0, j0, nB)
                if res is None:
                    continue
                inD, plus, phi, dens, ZH, _ = res
                lhs = math.log1p(phi)
                rhs = n * e - math.log(2) - math.log(ZH)
                if lhs < rhs - 1e-9:
                    return False, dict(reason="ln(1 + Phi(D)) below n(B - alpha_n) - ln 2 - ln Z", n=n, model=(bJ, bB, u), lhs=lhs, rhs=rhs)
                # the lattice instance has the landscape V_n/n, within c ln(n+1)/n of v: compare with V at a slightly larger budget
                slack = float(np.abs(Vn / n - M["v"](np.arange(n + 1) / n)).max())
                V = mf_inner(M, lam, mu, nB / n + slack)
                if math.log(dens) > 2 * math.log(n + 1) - n * V + 1e-9:
                    return False, dict(reason="maxdens(D) above (n+1)^2 exp(-n V)", n=n, model=(bJ, bB, u), ln_dens=math.log(dens), V=V)
                stats["tightest_dens"] = max(stats["tightest_dens"], (math.log(dens) + n * V) / math.log(n + 1))
                stats["tightest_phi"] = min(stats["tightest_phi"], lhs - rhs)
                stats["bounds"] += 1
    if stats["brute"] < 4 or stats["bounds"] < 8:
        return False, dict(reason="too few instances", **stats)
    return True, stats


@conjecture("XIX.6 Theorem 11.79(a) (cones around shells; beta J = 1.5, B = 0, u = 1): a shell (1/2; x, x) in the barrier type class is its own Gibbs shell (min_nu [MI + I + u dist(nu, mu)] = alpha(mu)) exactly when x >= p_u = 1/(1 + e^u), the local condition |phi'(type) + logit(mu_j)| <= u; hence the exponent of non-adaptive algorithms at vanishing accuracy is at least MI of the shell at p_u, KL(p_u || 1/2) = 0.110944 = the uniform cube's value; for every centre mu0 the minimiser mu* of G_mu0 is self-consistent, and the truncated cone around mu0 is not better than the truncated cone around mu*: theta_shell(X; mu0) <= theta_shell(X; mu*) (both by the triangle inequality alone, hence exactly on a grid; equality whenever the truncation shell lies beyond the Gibbs shell)")
def t_mf_shells(rng, trials):
    u = 1.0
    M = mf_model(1.5, 0.0, u)
    pu = 1 / (1 + math.exp(u))
    if abs(mf_kl(pu, 0.5) - 0.110944) > 1e-6:
        return False, dict(reason="KL(p_u || 1/2)")
    G = 800
    ax = np.linspace(0, 1, G + 1)
    N1, N0 = np.meshgrid(ax, ax, indexing="ij")

    def tables(lam):
        nb = lam[0] * N1 + lam[1] * N0
        mi = mf_hb(nb) - lam[0] * mf_hb(N1) - lam[1] * mf_hb(N0)
        return mi, mi + M["I"](nb)
    half = np.array([0.5, 0.5])
    mi, base = tables(half)
    stats = dict(consistent=0, inconsistent=0, centres=0, worst=-1.0, strict=0)
    for x in (0.2, 0.24, 0.26, 0.2675, 0.27, 0.28, 0.3, 0.35, 0.45):
        mu = np.array([1 - x, x])
        Gf = base + u * 0.5 * (np.abs(N1 - mu[0]) + np.abs(N0 - mu[1]))
        gap = mf_alpha(M, half, mu) - float(Gf.min())
        local = abs(float(np.log(mu[1] / (1 - mu[1])))) <= u + 1e-12
        if (x >= pu) != local:
            return False, dict(reason="local criterion against x >= p_u", x=x)
        if x >= pu and gap > 2e-6:
            return False, dict(reason="a shell beyond p_u is not its own Gibbs shell", x=x, gap=gap)
        if x < pu - 0.005 and gap < 2e-6:
            return False, dict(reason="a shell inside p_u is self-consistent", x=x, gap=gap)
        stats["consistent" if x >= pu else "inconsistent"] += 1
    for rep in range(6 if trials < 100 else 12):
        m = float(rng.uniform(0.35, 0.65))
        lam = np.array([m, 1 - m])
        mi_l, base_l = tables(lam)
        mu0 = np.array([1 - rng.uniform(0.0, 0.3), rng.uniform(0.0, 0.3)]) if rep % 3 else np.array([1.0, 0.0])
        dist = lambda c: u * (lam[0] * np.abs(N1 - c[0]) + lam[1] * np.abs(N0 - c[1]))
        G0 = base_l + dist(mu0)
        idx = np.unravel_index(np.argmin(G0), G0.shape)
        mus = np.array([ax[idx[0]], ax[idx[1]]])
        Gs = base_l + dist(mus)
        # both statements are consequences of the triangle inequality alone, so they hold exactly on the grid
        if float(Gs[idx]) - float(Gs.min()) > 1e-12:
            return False, dict(reason="the Gibbs shell of a cone is not self-consistent", centre=mu0.tolist(), shell=mus.tolist(), gap=float(Gs[idx]) - float(Gs.min()))
        for X in (0.01, 0.03, 0.06, 0.15, 0.3):
            t0 = float(mi_l[G0 - G0.min() <= X].min())
            ts = float(mi_l[Gs - Gs.min() <= X].min())
            stats["worst"] = max(stats["worst"], t0 - ts)
            stats["strict"] += t0 < ts - 1e-6
            if t0 > ts + 1e-12:
                return False, dict(reason="a truncated cone beats the truncated cone around its own Gibbs shell", centre=mu0.tolist(), X=X, cone=t0, shell=ts)
        stats["centres"] += 1

    return True, stats


# ----------------------------------------------------------------------------------------------
# XX. Rounds of adaptivity (theory report 11.24)
# ----------------------------------------------------------------------------------------------

def rd_setup(u, G=200001):
    """Exponent functions of the uniform cube: f = KL(.||1/2), k = KL(.||p_u), a, h, theta_na, theta_hint, and the inverse
    functions D(theta) = u f^{-1}(theta) - Lambda_1 (accuracy rate certified with a hint) and x_na = D + theta."""
    pu = 1 / (1 + math.exp(u))
    L1 = math.log(2 / (1 + math.exp(-u)))
    f = lambda r: np.asarray(r, float) * np.log(2 * np.asarray(r, float)) + (1 - np.asarray(r, float)) * np.log(2 * (1 - np.asarray(r, float)))
    rho = np.linspace(pu, 0.5, G)
    kk, ff = f(rho) + u * rho - L1, f(rho)
    estar = float(kk[-1])
    rfull = np.linspace(1e-9, 0.5, 4 * G)
    ffull = f(rfull)
    finv = lambda th: np.interp(th, ffull[::-1], rfull[::-1])

    def theta_na(e):
        e = np.asarray(e, float)
        return np.where(e >= estar, 0.0, np.interp(np.clip(e, 0, estar), kk, ff))

    def theta_hint(e):
        r = (L1 + np.asarray(e, float)) / u
        return np.where(r >= 0.5, 0.0, f(np.clip(r, 1e-12, 0.5)))
    D = lambda th: u * finv(th) - L1
    return dict(u=u, pu=pu, L1=L1, f=f, finv=finv, a=float(ff[0]), h=float(f(L1 / u)), estar=estar, theta_na=theta_na, theta_hint=theta_hint,
                D=D, xna=lambda th: D(th) + np.asarray(th, float))


def rd_logbinom(n):
    d = np.arange(n + 1)
    return np.array([math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) for i in d]) - n * math.log(2)


def rd_lip_minorant(t, u):
    v = t.copy()
    for i in range(1, len(v)):
        v[i] = min(v[i], v[i - 1] + u)
    for i in range(len(v) - 2, -1, -1):
        v[i] = min(v[i], v[i + 1] + u)
    return v


def rd_logsumexp(x):
    x = np.asarray(x, float).ravel()
    m = x.max()
    return float(m + math.log(np.exp(x - m).sum()))


def rd_twins(n1, n2, T, u, cap=True):
    """The twins of Theorem 11.86 on the grid of types (d1, d2): returns F_D, F_S, the sets W1 (what a blind batch of
    e^T points sees) and W2 (V2 = all d1 x W2: what a batch that knows the first centre sees), g1, and the log-weights."""
    lp1, lp2 = rd_logbinom(n1), rd_logbinom(n2)
    g1 = -rd_lip_minorant(lp1.max() - lp1, u)          # flat histogram of block 1
    g2 = -rd_lip_minorant(lp2.max() - lp2, u)
    W1 = (-lp1[:, None] - lp2[None, :]) <= T
    W2 = -lp2 <= T
    if not W1.any() or W2.all():
        return None
    F = np.where(W1, g1[:, None] * np.ones((1, n2 + 1)), -np.inf)      # lower McShane envelope of g1 from W1
    for axis in (0, 1):
        F = np.moveaxis(F, axis, 0)
        for i in range(1, F.shape[0]):
            F[i] = np.maximum(F[i], F[i - 1] - u)
        for i in range(F.shape[0] - 2, -1, -1):
            F[i] = np.maximum(F[i], F[i + 1] - u)
        F = np.moveaxis(F, 0, axis)
    Fcap = np.maximum(F, g1[:, None] + g2[None, :]) if cap else F
    idx = np.flatnonzero(W2)
    d2 = np.arange(n2 + 1)
    b = np.clip(d2, idx[0], idx[-1])
    dist = np.abs(d2 - b)
    FD = Fcap[:, b] - u * dist[None, :]
    FS = Fcap[:, b] + u * dist[None, :]
    return FD, FS, W1, W2, g1, lp1[:, None] + lp2[None, :], lp2


def rd_hinted_exponent(n, u, eps):
    """Theorem 11.25(a) at the zero residual of the uniform cube: with k the least radius of a dip of depth u k whose effect
    exceeds eps, every algorithm needs (1 - 2 delta) 2^n/|B(n, k-1)| evaluations; returns ln(2^n/|B(n, k-1)|)/n."""
    lp = rd_logbinom(n)
    d = np.arange(n + 1)
    for k in range(1, n):
        x = u * (k - d[:k])
        if np.logaddexp(0.0, rd_logsumexp(lp[:k] + x + np.log1p(-np.exp(-x)))) > eps:
            return -rd_logsumexp(lp[:k]) / n
    return 0.0


@conjecture("XX.1 Theorem 11.86 (the twins that two rounds cannot tell apart; types (d1, d2) on two blocks, budget T): with W1 = {c1(d1) + c2(d2) <= T} (what a blind batch sees), V2 = {c2(d2) <= T} (what a batch that knows the first centre sees), g_j the flat histogram of block j, F_cap = max(lower McShane envelope of g1 from W1, g1 + g2), and F_D / F_S its continuation outside V2 at slope -u / +u: both are u-Lipschitz in each argument, coincide on V2 which contains W1, equal g1(d1) on W1, F_S >= F_D, every type has mass at most one under F_S (so A(F_S) <= (n1+1)(n2+1)); on whole cubes Q_12 with random centres the block-radial functions have largest edge difference at most u and ln A equals the sum over types; and at u = 1, n = 800 (n1 = 360, T = 0.0421 n) the gap ln A(F_D) - ln A(F_S) exceeds 1 while -ln(p1 + p2)/n exceeds the exponent of the lower bound for all algorithms at accuracy 1")
def t_rounds_twins(rng, trials):
    stats = dict(grids=0, cubes=0)
    cases = [(1.0, 60, 30, 5.0), (1.0, 120, 70, 9.0), (2.0, 80, 36, 14.0), (0.5, 150, 90, 7.5), (1.0, 800, 360, 0.0421 * 800)]
    for (u, n, n1, T) in cases:
        r = rd_twins(n1, n - n1, T, u)
        if r is None:
            return False, dict(reason="degenerate case in the test", case=(u, n, n1, T))
        FD, FS, W1, W2, g1, lw, lp2 = r
        for G_ in (FD, FS):
            if np.abs(np.diff(G_, axis=0)).max() > u + 1e-9 or np.abs(np.diff(G_, axis=1)).max() > u + 1e-9:
                return False, dict(reason="a twin is not u-Lipschitz in each argument", case=(u, n, n1, T))
        if not np.all(W1 <= W2[None, :]):
            return False, dict(reason="W1 is not contained in V2", case=(u, n, n1, T))
        if not np.array_equal(FD[:, W2], FS[:, W2]) or np.any(FS < FD - 1e-12):
            return False, dict(reason="the twins differ on V2, or F_S < F_D", case=(u, n, n1, T))
        if np.abs((FD - g1[:, None])[W1]).max() > 1e-9:
            return False, dict(reason="on W1 the twins are not the flat histogram of the first block", case=(u, n, n1, T))
        if (lw - FS).max() > 1e-9:
            return False, dict(reason="a type has mass above one under F_S", case=(u, n, n1, T), excess=float((lw - FS).max()))
        if not np.any(FD[:, ~W2] < FS[:, ~W2] - 1e-9):
            return False, dict(reason="the twins do not differ anywhere", case=(u, n, n1, T))
        stats["grids"] += 1
        if n == 800:
            gap = rd_logsumexp(lw - FD) - rd_logsumexp(lw - FS)
            E = -float(np.logaddexp(rd_logsumexp(lw[~W1]), rd_logsumexp(lp2[~W2]))) / n
            he = rd_hinted_exponent(n, u, 1.0)
            stats.update(gap=gap, two_round_exponent=E, all_algorithms=he)
            if gap <= 1.0 or E <= he + 0.001:
                return False, dict(reason="no separation at n = 800", **stats)
    # whole cubes
    for (n1, n2, u, T) in ((6, 6, 1.0, 3.2), (7, 5, 2.0, 3.4), (5, 7, 0.5, 3.0)):
        r = rd_twins(n1, n2, T, u)
        if r is None:
            return False, dict(reason="degenerate cube case in the test")
        FD, FS, W1, W2, g1, lw, lp2 = r
        n = n1 + n2
        N = 2 ** n
        x = np.arange(N)
        pop = np.array([bin(v).count("1") for v in range(2 ** max(n1, n2))])
        s1, s2 = int(rng.integers(2 ** n1)), int(rng.integers(2 ** n2))
        d1 = pop[(x & (2 ** n1 - 1)) ^ s1]
        d2 = pop[(x >> n1) ^ s2]
        for Fm in (FD, FS):
            psi = Fm[d1, d2]
            if max(float(np.abs(psi - psi[x ^ (1 << i)]).max()) for i in range(n)) > u + 1e-9:
                return False, dict(reason="a block-radial twin is not u-Lipschitz on the cube", blocks=(n1, n2))
            lnA = math.log(float(np.exp(-psi).mean()))
            if abs(lnA - rd_logsumexp(lw - Fm)) > 1e-9:
                return False, dict(reason="ln A by enumeration against the sum over types", blocks=(n1, n2))
        if not np.array_equal(FD[d1, d2][W2[d2]], FS[d1, d2][W2[d2]]):
            return False, dict(reason="twins differ at a point whose type is in V2", blocks=(n1, n2))
        stats["cubes"] += 1
    return True, stats


@conjecture("XX.2 Theorem 11.86, asymptotic form: with D(theta) = u f^{-1}(theta) - Lambda_1, x_na = D + theta and E_theta(c) = phi1 x_na(c/phi1) + phi2 D((theta - c)/phi2): E_theta(c) >= c + D(theta) (convexity of f); Xi(h, phi1) = min_c E_h(c) > 0 for every split; hence theta2* = sup{theta : Xi(theta, phi1) > 0, theta < phi2 a} > h, with theta2*/a = 0.349, 0.359, 0.394 at u = 0.5, 1, 2 (best phi1 = 0.65, 0.64, 0.61), below the two-round upper bound T2(0); and Lemma 11.85 on the type process: a second batch that knows the first centre and chooses d1 adversarially sees a type outside V2 with probability at most M2 p2")
def t_rounds_lower(rng, trials):
    stats = {}
    for u, want in ((0.5, 0.3493), (1.0, 0.3592), (2.0, 0.3938)):
        S = rd_setup(u, G=40001)
        a, h = S["a"], S["h"]

        def Xi(theta, phi1, npts=2001):
            c = np.linspace(0, min(theta, phi1 * a), npts)
            E = phi1 * S["xna"](c / phi1) + (1 - phi1) * S["D"]((theta - c) / (1 - phi1))
            return float(E.min()), E, c
        for phi1 in (0.1, 0.3, 0.5, 0.65, 0.8):
            for theta in (h, 1.2 * h, 0.5 * min(a * (1 - phi1), a)):
                if theta >= (1 - phi1) * math.log(2):
                    continue
                _, E, c = Xi(theta, phi1)
                if np.any(E < c + float(S["D"](theta)) - 1e-7):
                    return False, dict(reason="E_theta(c) < c + D(theta)", u=u, phi1=phi1, theta=theta)
            if Xi(h, phi1)[0] <= 0:
                return False, dict(reason="Xi(h, phi1) is not positive", u=u, phi1=phi1)
        best = 0.0
        for phi1 in np.linspace(0.5, 0.75, 51):
            lo, hi = h, (1 - phi1) * a
            if Xi(hi, phi1, 801)[0] > 0:
                root = hi
            else:
                for _ in range(40):
                    mid = 0.5 * (lo + hi)
                    if Xi(mid, phi1, 801)[0] > 0:
                        lo = mid
                    else:
                        hi = mid
                root = lo
            best = max(best, min(root, (1 - phi1) * a))
        stats[f"theta2_over_a_u{u}"] = best / a
        if abs(best / a - want) > 0.002:
            return False, dict(reason="value of theta2*", u=u, value=best / a, expected=want)
        if not (h < best):
            return False, dict(reason="theta2* does not exceed h", u=u)
        # two-round upper bound
        xi = np.linspace(1e-6, S["estar"], 1201)[None, :]
        ph = np.linspace(0.01, 0.99, 491)[:, None]
        T2 = float(np.maximum(ph * a + (1 - ph) * S["theta_na"](xi), np.minimum(ph * a, (1 - ph) * xi) + (1 - ph) * a).min())
        if not (best < T2 < a):
            return False, dict(reason="lower bound for two rounds above the upper bound, or upper bound not below a", u=u, lower=best, upper=T2)
    # Lemma 11.85 on the type process (two blocks): batch 2 knows s1 and may give its points any d1
    n1, n2, u, T = 14, 14, 1.0, 6.0
    FD, FS, W1, W2, g1, lw, lp2 = rd_twins(n1, n2, T, u)
    p2 = float(np.exp(rd_logsumexp(lp2[~W2])))
    M2 = max(1, int(0.3 / p2))
    runs = 400 if trials < 100 else 2000
    bad = 0
    for _ in range(runs):
        d2 = rng.binomial(n2, 0.5, size=M2)
        bad += bool(np.any(~W2[d2]))        # whatever d1 the batch chooses, the twins differ only where d2 is outside W2
    freq = bad / runs
    stats.update(freq=freq, bound=M2 * p2)
    if freq > M2 * p2 + 4 * math.sqrt(M2 * p2 / runs):
        return False, dict(reason="a second batch sees the difference more often than M2 p2", **stats)
    return True, stats


@conjecture("XX.3 Theorem 11.84(b),(c) (round-limited ladders at bounded accuracy): T2(0) = min_{phi, xi} max{phi a + (1 - phi) theta_na(xi), min(phi a, (1 - phi) xi) + (1 - phi) a} is 0.6197 a, 0.6243 a, 0.6413 a at u = 0.5, 1, 2 and tends to the golden ratio (sqrt 5 - 1)/2 for small slopes; for fixed xi with (1 - phi) xi <= phi a the two terms balance at the value a (a + xi)/(2a + xi - theta_na(xi)), which is (a + h)/2 at xi = h; the three-rung ladder gives T3(0) <= 0.542 a at u = 1; and the two-round function T2(g) stays above the hinted exponent theta_hint(g) at every accuracy (no level undercuts the lower bound)")
def t_rounds_upper(rng, trials):
    out = {}
    for u, want in ((0.05, (math.sqrt(5) - 1) / 2), (0.5, 0.6197), (1.0, 0.6243), (2.0, 0.6413)):
        S = rd_setup(u, G=40001)
        a, h = S["a"], S["h"]
        xi = np.linspace(1e-7 * a, S["estar"], 3001)[None, :]
        ph = np.linspace(0.005, 0.995, 991)[:, None]
        v = np.maximum(ph * a + (1 - ph) * S["theta_na"](xi), np.minimum(ph * a, (1 - ph) * xi) + (1 - ph) * a)
        T2 = float(v.min())
        out[f"T2_over_a_u{u}"] = T2 / a
        if abs(T2 / a - want) > 0.0012:
            return False, dict(reason="two-round value", u=u, value=T2 / a, expected=want)
        # balance formula
        for x in (h, 0.5 * h, 2 * h, 0.4 * a):
            if x >= S["estar"]:
                continue
            tn = float(S["theta_na"](x))
            one_minus_phi = a / (2 * a + x - tn)
            phi = 1 - one_minus_phi
            if one_minus_phi * x > phi * a:
                continue
            t1, t2 = phi * a + one_minus_phi * tn, one_minus_phi * x + one_minus_phi * a
            val = a * (a + x) / (2 * a + x - tn)
            if abs(t1 - t2) > 1e-9 * a or abs(t1 - val) > 1e-9 * a:
                return False, dict(reason="balance of the two rungs", u=u, xi=x)
            col = np.maximum(ph[:, 0] * a + (1 - ph[:, 0]) * tn, np.minimum(ph[:, 0] * a, (1 - ph[:, 0]) * x) + (1 - ph[:, 0]) * a)
            if abs(float(col.min()) - val) > 2e-3 * a:
                return False, dict(reason="minimum over phi at fixed xi against the balance value", u=u, xi=x, grid=float(col.min()), formula=val)
        if abs(a * (a + h) / (2 * a + h - float(S["theta_na"](h))) - (a + h) / 2) > 2e-4 * a:
            return False, dict(reason="theta_na(h) = h, so the balance value at xi = h is (a + h)/2", u=u)
    S = rd_setup(1.0, G=40001)
    a, h, es = S["a"], S["h"], S["estar"]
    p3 = np.linspace(0.02, 0.98, 97)[:, None, None]
    x1 = np.linspace(1e-6, es, 150)[None, :, None]
    x2 = np.linspace(1e-6, es, 150)[None, None, :]
    m3 = p3 * a
    v3 = np.maximum(np.maximum(m3 + (1 - p3) * S["theta_na"](x1), np.minimum(m3, (1 - p3) * x1) + (1 - p3) * S["theta_na"](x2)),
                    np.minimum(m3, (1 - p3) * x2) + (1 - p3) * a)
    T3 = float(np.where(x1 > x2, v3, np.inf).min())
    out["T3_over_a"] = T3 / a
    if not (0.52 * a < T3 < 0.542 * a):
        return False, dict(reason="three-rung value at u = 1", value=T3 / a)
    # lower barrier for T2(g), g > 0
    worst = 1.0
    ph = np.linspace(0.03, 0.97, 48)[:, None, None]
    for g in np.linspace(0.05, 0.95, 10) * es:
        be = np.linspace(0.02 * g, 0.98 * g, 40)[None, None, :]
        xi2 = be / (1 - ph)
        mu = ph * S["theta_na"]((g - be) / ph)
        fr = np.linspace(0.0, 1.0, 60)[None, :, None]
        xi1 = xi2 + fr * np.maximum(es - xi2, 0.0)
        v = np.maximum(mu + (1 - ph) * S["theta_na"](xi1), np.minimum(mu, (1 - ph) * xi1) + (1 - ph) * S["theta_na"](xi2))
        T2g = min(float(S["theta_na"](g)), float(v.min()))
        hint = float(S["theta_hint"](g))
        worst = min(worst, T2g - hint)
        if T2g < hint - 1e-9:
            return False, dict(reason="a two-round ladder undercuts the hinted exponent", g=float(g), T2=T2g, hint=hint)
    out["least_margin_over_hint"] = worst
    return True, out


@conjecture("XX.4 Proposition 11.88(a),(b): (a) conditional covering — for a ball of radius kappa n whose centre is uniform on the sphere of radius sigma n around a known point, a point at distance t n from the known point hits with probability sum_{i >= (t + sigma - kappa) n/2} C(tn, i) C((1-t)n, sigma n - i)/C(n, sigma n), at most |B(n, kappa n)|/C(n, sigma n) for every t, and at t* = (sigma - kappa)/(1 - 2 kappa) within a factor n of it: the exponent is KL(kappa || 1/2) - KL(sigma || 1/2); (b) shadows — for psi = min(-D + u (d(., s1) - R)_+, -D - uK + u d(., s2)): if d(s1, s2) + K <= R the two functions differ only inside the open ball B(s2, K), and if d(s1, s2) + K >= R + 3 then psi is the cone at the antipode of s1 and at its n neighbours")
def t_rounds_covering_shadows(rng, trials):
    stats = dict(pairs=0, shadows=0, worst_ratio=0.0)
    for n in (300, 600):
        for (sig, kap) in ((0.45, 0.38), (0.4, 0.3), (0.5, 0.35), (0.3, 0.2), (0.35, 0.1)):
            sn, kn = round(sig * n), round(kap * n)
            lC = lambda N, k: math.lgamma(N + 1) - math.lgamma(k + 1) - math.lgamma(N - k + 1) if 0 <= k <= N else -math.inf
            lball = rd_logsumexp([lC(n, j) for j in range(kn + 1)])
            dual = lball - lC(n, sn)
            best = -math.inf
            for tn in range(0, n + 1, max(1, n // 200)):
                # i = number of coordinates among the tn in which the centre differs from the known point as well
                terms = [lC(tn, i) + lC(n - tn, sn - i) for i in range(max(0, sn - (n - tn)), min(tn, sn) + 1) if tn + sn - 2 * i <= kn]
                lp = rd_logsumexp(terms) - lC(n, sn) if terms else -math.inf
                if lp > dual + 1e-9:
                    return False, dict(reason="a point hits with probability above |B|/C(n, sigma n)", n=n, sigma=sig, kappa=kap, t=tn)
                best = max(best, lp)
            ts = round((sig - kap) / (1 - 2 * kap) * n)
            terms = [lC(ts, i) + lC(n - ts, sn - i) for i in range(max(0, sn - (n - ts)), min(ts, sn) + 1) if ts + sn - 2 * i <= kn]
            lps = rd_logsumexp(terms) - lC(n, sn)
            stats["worst_ratio"] = max(stats["worst_ratio"], (dual - lps) / math.log(n))
            if lps < dual - 1.0 * math.log(n) or lps < best - 0.6 * math.log(n):
                return False, dict(reason="the sphere of radius t* n does not attain the counting bound up to the factor n", n=n, sigma=sig, kappa=kap)
            rate = mf_kl(kn / n, 0.5) - mf_kl(sn / n, 0.5)
            if abs(-lps / n - rate) > 1.2 * math.log(n) / n:
                return False, dict(reason="exponent of the conditional covering", n=n, sigma=sig, kappa=kap, exact=-lps / n, formula=rate)
            stats["pairs"] += 1
    for n in (8, 9, 10):
        D = na_cube(n)
        N = 2 ** n
        for _ in range(max(10, trials // 8)):
            u = float(rng.choice([0.5, 1.0, 2.0]))
            s1, s2 = int(rng.integers(N)), int(rng.integers(N))
            R, K, Dp = int(rng.integers(1, n)), int(rng.integers(1, n)), float(rng.uniform(0, 3))
            psi1 = -Dp + u * np.maximum(D[s1] - R, 0)
            psi2 = -Dp - u * K + u * D[s2]
            dd = int(D[s1, s2])
            if dd + K <= R:
                if np.any((psi2 < psi1 - 1e-12) & (D[s2] >= K)):
                    return False, dict(reason="a dip inside the plateau is visible outside its ball", n=n)
                stats["shadows"] += 1
            elif dd + K >= R + 3:
                anti = (N - 1) ^ s1
                pts = [anti] + [anti ^ (1 << i) for i in range(n)]
                if any(psi2[x] > psi1[x] + 1e-12 for x in pts):
                    return False, dict(reason="a dip that sticks out of the plateau is not seen at the antipode", n=n)
                stats["shadows"] += 1
    if stats["shadows"] < 10:
        return False, dict(reason="too few shadow instances", **stats)
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


@conjecture("DEAD.17 On the line best-first search needs at most 4 N_point + 1 evaluations also when there is a known part (the one-dimensional theorem of Hansen-Jaumard-Lu extends)", expect_fail=True)
def t_dead_line_known_part(rng, trials):
    """Refuted (workstream C, Proposition C5; family B' of its reviewer).  Points x* = -D, the hub c = 0, a grid
    t_j = j h to the right of the hub and one far point y0; known part f(x*) = D, f(0) = G, f(t) = G + (1 - eta) t,
    residual g = -|x| (extremal), eps = 0.01 G.  {x*, c, y0} is a point certificate, but best-first search, started at
    the minimiser of the known part, walks back from the far end in steps of length D: about 1.3 / eta evaluations."""
    eta, G = 0.05, 1.0
    D, eps = 0.75 * G, 0.01 * G
    h = D / 8
    M = int(round(0.98 * G / eta / h))
    X = np.array([-D, 0.0] + [j * h for j in range(1, M + 1)] + [-D - 2 * G])
    f = np.array([D, G] + [G + (1 - eta) * j * h for j in range(1, M + 1)] + [D + 1.4 * G])
    g = -np.abs(X)
    g[-1] = g[0] + 2 * G
    d = np.abs(X[:, None] - X[None, :])
    if np.any(np.abs(g[:, None] - g[None, :]) > d + 1e-12):
        raise RuntimeError("sanity: residual is not admissible")
    cert = [0, 1, len(X) - 1]
    lb, _, ubpt, _, _ = cg_bounds(d, f, g, cert)
    evaluated = cg_best_first(d, f, g, eps, int(np.argmin(f)))
    if ubpt - lb <= eps + 1e-12 and len(evaluated) > 4 * len(cert) + 1:
        return False, dict(reason="best-first search far exceeds 4 N_point + 1 on a line instance with a known part",
                           certificate_size=len(cert), best_first_evaluations=len(evaluated), eta=eta)
    return True, {}


# ----------------------------------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------------------------------

@conjecture("DEAD.18 The profile distance of the diamond-lattice chain is the weighted form 9|dh3| + 4|dh8| + |dh11| (the coordinator's brief for workstream S: 'equivalently the L1 distance of cumulative profiles')", expect_fail=True)
def t_dead_weighted_profile_norm(rng, trials):
    """Refuted (workstream S; D48): the L1 distance of the cumulative pair-count functions is 5|dh3| + 3|dh3 + dh8| +
    |dh3 + dh8 + dh11|, which is strictly smaller than the weighted form for pairs of conformations whose differences
    have opposite signs — and such pairs exist already among chains with 9 beads."""
    grid = np.arange(0, 12, 0.5) + 0.25
    cum = lambda h: (grid >= 3) * h[0] + (grid >= 8) * h[1] + (grid >= 11) * h[2]
    for N in (7, 8, 9, 10):
        profs = sorted(set(ls_profile(w)[:3] for w in ls_enum(N)))
        for h in profs:
            for k in profs:
                d = (h[0] - k[0], h[1] - k[1], h[2] - k[2])
                l1 = float(np.abs(cum(h) - cum(k)).sum() * 0.5)
                if abs(l1 - ls_wnorm(d)) > 1e-9:
                    return False, dict(reason="two conformations whose cumulative-profile distance is not the weighted form",
                                       beads=N, h=h, k=k, cumulative=l1, weighted=float(ls_wnorm(d)))
    return True, {}


@conjecture("DEAD.19 With two phases binary centres still suffice: the dip exponent of the flat-histogram instance is attained by sets around one centre (as for convex rate functions, Theorem 11.80(b), and as the coordinator's brief for workstream T assumed)", expect_fail=True)
def t_dead_binary_centres(rng, trials):
    M = mf_model(1.5, 0.0, 1.0)
    x3, lf, _ = MF_TWO_PHASE["S3"]
    s3 = mf_r(M, np.array([(1 - lf) / 2, lf, (1 - lf) / 2]), np.array([1 - x3, 0.5, x3]), 0.02)
    best2 = 0.0
    for m, xs in ((0.5, np.linspace(0.285, 0.325, 9)), (0.47, (0.295, 0.305, 0.315)), (0.53, (0.295, 0.305, 0.315))):
        for x in xs:
            for dx in ((0.0, 0.008, -0.008) if m == 0.5 else (0.0,)):
                best2 = max(best2, mf_r(M, np.array([m, 1 - m]), np.array([1 - x - dx, x - dx]), 0.02, G=600))
    if s3 > best2 + 1e-4:
        return False, dict(reason="a profile with a free block (86% of the coordinates constrained) beats every binary centre at e = 0.02", three_blocks=s3, best_binary=best2)
    return True, dict(three_blocks=s3, best_binary=best2)


@conjecture("DEAD.20 With two phases the cone formula max_m min{MI : u rho + v - Lambda_m <= e} is the dip exponent of the flat-histogram instance, and truncated cones around points attain the non-adaptive exponent (pair identity with cones, as for convex rate functions)", expect_fail=True)
def t_dead_cones_two_phase(rng, trials):
    M = mf_model(1.5, 0.0, 1.0)
    r0 = mf_r(M, np.array([0.5, 0.5]), np.array([1 - MF_TWO_PHASE["x0"], MF_TWO_PHASE["x0"]]), 0.0)
    G = 500
    ax = np.linspace(0, 1, G)
    A_, B_ = np.meshgrid(ax, ax, indexing="ij")
    best_cone, best_trunc = 0.0, 0.0
    for m in np.linspace(0.3, 0.7, 9):
        kap = m * (1 - A_) + (1 - m) * B_
        rho = m * A_ + (1 - m) * B_
        mi = mf_hb(kap) - m * mf_hb(A_) - (1 - m) * mf_hb(B_)
        J = mi + M["I"](kap) + rho
        Lam = float(J.min())
        best_cone = max(best_cone, float(mi[rho + M["v"](kap) - Lam <= 0].min()))
        best_trunc = max(best_trunc, float(mi[J - Lam <= r0].min()))
    if best_cone < 0.6 * r0 or best_trunc < 0.6 * r0:
        return False, dict(reason="cones around points fall short of shells in the barrier class", shell=r0, cone_formula=best_cone, truncated_cone=best_trunc)
    return True, dict(shell=r0, cone_formula=best_cone, truncated_cone=best_trunc)


@conjecture("DEAD.21 Two rounds of adaptivity reach the adaptive exponent on the cube class (as they do on radial instances, Theorem 11.51): no family of instances forces a two-round algorithm to more evaluations than the lower bound for all algorithms", expect_fail=True)
def t_dead_two_rounds(rng, trials):
    u, n, n1 = 1.0, 1600, 800
    best = None
    for T in np.linspace(0.036, 0.0405, 10) * n:
        r = rd_twins(n1, n - n1, float(T), u)
        if r is None:
            continue
        FD, FS, W1, W2, g1, lw, lp2 = r
        if rd_logsumexp(lw - FD) - rd_logsumexp(lw - FS) > 1.0:
            best = -float(np.logaddexp(rd_logsumexp(lw[~W1]), rd_logsumexp(lp2[~W2]))) / n
    he = rd_hinted_exponent(n, u, 1.0)
    if best is not None and best > he + 0.003:
        return False, dict(reason="twins that differ by more than 1 in ln A and are seen by two batches of e^{nE} points with probability below 1 - 2 delta", two_round_exponent=best, all_algorithms=he)
    return True, dict(two_round_exponent=best if best is not None else 0.0, all_algorithms=he)


@conjecture("DEAD.22 With two phases cones around profile classes attain the exponent R_H o S^{-1} of non-adaptive algorithms (the pair identity n_mu(e + R(e)) = R(e) for some shell) whenever the top of the barrier is a contact point, as they do at u = 1", expect_fail=True)
def t_dead_pair_identity_threshold(rng, trials):
    u = 0.30
    M = mf_model(1.5, 0.0, u)
    half = np.array([0.5, 0.5])
    shell = lambda x: np.array([1 - x, x])
    R0, x0 = mf_golden(lambda x: -mf_r(M, half, shell(x), 0.0, G=1200), 0.40, 0.49, tol=1e-5)
    R0 = -R0

    def n_mu(x):
        """min{r_mu(e) : e + r_mu(e) <= X} at X = S(0) = R0: the value of r_mu at the largest feasible e <= X"""
        al = mf_alpha(M, half, shell(x))
        rr = lambda e: mf_inner(M, half, shell(x), e + al, G=1200)
        if rr(R0) <= 1e-12:
            return 0.0
        es = np.linspace(max(float(M["v"](0.5)) - al, -0.004), R0, 17)       # the feasible accuracies include e <= 0
        g = [e + rr(float(e)) - R0 for e in es]
        ok = [i for i in range(len(es)) if g[i] <= 0]
        if not ok:
            return float("inf")
        a, b = float(es[ok[-1]]), float(es[min(ok[-1] + 1, len(es) - 1)])
        for _ in range(9):
            m_ = 0.5 * (a + b)
            if m_ + rr(m_) - R0 <= 0:
                a = m_
            else:
                b = m_
        return rr(a)
    vals = {round(x, 4): n_mu(x) for x in (x0, x0 + 0.005, x0 + 0.0105, x0 + 0.015)}
    best = max(v for v in vals.values() if math.isfinite(v))
    if best < 0.9 * R0:
        return False, dict(reason="at u = 0.30 the best cone around a barrier shell certifies only 81% of the dip exponent at the accuracy S(0); the cone around the optimal dip shell certifies nothing", dip_exponent=R0, shell=x0, best_cone=best, at_dip_shell=vals[round(x0, 4)])
    return True, dict(dip_exponent=R0, shell=x0, best_cone=best)


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
