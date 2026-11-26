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
    if res.status != 0:                 # unbounded or infeasible: the rule gives no finite bound.  Report that as a value, so
        return math.inf                 # that a mis-modelled rule shows up as a failed comparison and not as an exception
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
        if not (math.isfinite(lp_kernel) and math.isfinite(lp_blocks)) \
                or abs(lp_primal - lp_blocks) > 1e-7 or abs(lp_kernel - lp_blocks) > 1e-7:
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


def to3_mixed_max(g, T):
    """max over base points and target states of |third mixed difference of g over the sites T| (exact, by broadcasting):
    for each axis of T the operator 'value at the target state minus value at the base state' adds one index."""
    A = np.moveaxis(g, T, (0, 1, 2))
    for ax in (0, 2, 4):                      # after each step the handled axis has become two axes (base, target)
        A = np.expand_dims(np.moveaxis(A, ax, 0), 0) - np.expand_dims(np.moveaxis(A, ax, 0), 1)   # [base, target, ...]
        A = np.moveaxis(A, (0, 1), (ax, ax + 1))
    return float(np.abs(A).max())


@conjecture("XI.16 Third-order classes reduce to pairwise lower models (theory report Theorem 11.18a; ThirdOrderModel.lean: anchoredInterp_three, thirdOrder_pairwise_lower, thirdOrder_pairwise_lower_thirds, thirdOrder_pairwise_lower_pair_thirds — a request of the Scientific Discovery Division, P2-T1): with c_T the exact bound of the third mixed differences of a residual g over the triple T, the interpolant I_2 g of order two around a reference (values of g on the Hamming ball of radius 2) satisfies |g - I_2 g| <= sum of c_T over the triples of changed sites; that sum is at most the pair penalty sum_{changed pairs} gamma_ij, gamma_ij = (1/3) sum_{T containing i, j} c_T, which is at most the site penalty sum_{changed sites} gamma_i, gamma_i = (1/3) sum_{T containing i} c_T; so I_2 g minus either penalty is a pairwise function below g, the pair form being the tighter one, with equality at a pure three-body term")
def t_third_order_pairwise(rng, trials):
    stats = dict(instances=0, configs=0, pair_tighter=0, worst_slack=math.inf, equal_at_triple=0, direct_checks=0)
    for it in range(max(30, trials // 8)):
        n = int(rng.integers(3, 6))
        ks = [int(k) for k in rng.integers(2, 4, size=n)]
        mode = it % 3
        if mode == 0:                                                        # pairwise plus small three-body terms
            g = np.zeros(ks)
            for (i, j) in itertools.combinations(range(n), 2):
                t = rng.normal(size=(ks[i], ks[j]))
                g = g + np.moveaxis(t.reshape([ks[i], ks[j]] + [1] * (n - 2)), (0, 1), (i, j))
            g = g + 0.1 * rng.normal(size=ks)
        elif mode == 1:                                                      # an arbitrary function
            g = rng.normal(size=ks)
        else:                                                                # a pure three-body term on the first three sites
            g = np.zeros(ks)
            idx = tuple([1, 1, 1] + [slice(None)] * (n - 3))
            g[idx] = -float(rng.uniform(0.5, 2.0))
        triples = list(itertools.combinations(range(n), 3))
        c = {T: to3_mixed_max(g, T) for T in triples}
        if n == 3:                                                           # the vectorised constant against its definition
            direct = 0.0
            for x in itertools.product(*[range(k) for k in ks]):
                for b in itertools.product(*[range(k) for k in ks]):
                    direct = max(direct, abs(sum((-1) ** (3 - len(U)) * g[tuple(b[i] if i in U else x[i] for i in range(3))]
                                                 for r in range(4) for U in itertools.combinations(range(3), r))))
            if abs(direct - c[(0, 1, 2)]) > 1e-12:
                return False, dict(reason="third mixed difference: vectorised maximum against the definition", direct=direct, fast=c[(0, 1, 2)])
            stats["direct_checks"] += 1
        gam = [sum(c[T] for T in triples if i in T) / 3 for i in range(n)]
        gam2 = {(i, j): sum(c[T] for T in triples if i in T and j in T) / 3 for (i, j) in itertools.combinations(range(n), 2)}
        x0 = tuple(int(rng.integers(k)) for k in ks) if mode != 2 else tuple([0] * n)
        sub = lambda x, U: tuple(x[i] if i in U else x0[i] for i in range(n))
        tighter = False
        for x in itertools.product(*[range(k) for k in ks]):
            S = [i for i in range(n) if x[i] != x0[i]]
            I2 = g[x0] + sum(g[sub(x, (i,))] - g[x0] for i in S) \
                + sum(g[sub(x, (i, j))] - g[sub(x, (i,))] - g[sub(x, (j,))] + g[x0] for (i, j) in itertools.combinations(S, 2))
            B = sum(c[T] for T in itertools.combinations(S, 3))
            pair = sum(gam2[p] for p in itertools.combinations(S, 2))
            site = sum(gam[i] for i in S)
            r = float(g[x] - I2)
            if abs(r) > B + 1e-9:
                return False, dict(reason="remainder of the interpolant of order two exceeds the sum of the triple constants", n=n, x=x, r=r, B=B)
            if B > pair + 1e-9 or pair > site + 1e-9:
                return False, dict(reason="the penalties are not ordered: triples <= pair form <= site form", n=n, x=x, B=B, pair=pair, site=site)
            if len(S) < 3 and abs(r) > 1e-9:
                return False, dict(reason="the interpolant of order two is not exact on the ball of radius two", x=x, r=r)
            tighter = tighter or pair < site - 1e-9
            stats["worst_slack"] = min(stats["worst_slack"], pair - abs(r))
            stats["configs"] += 1
        if mode == 2:
            x = tuple([1, 1, 1] + [0] * (n - 3))
            T = (0, 1, 2)
            if abs(abs(g[x]) - c[T]) > 1e-12 or abs(gam2[(0, 1)] + gam2[(0, 2)] + gam2[(1, 2)] - c[T]) > 1e-12 \
                    or abs(gam[0] + gam[1] + gam[2] - c[T]) > 1e-12:
                return False, dict(reason="a pure three-body term does not attain both pairwise lower models at its triple", n=n)
            stats["equal_at_triple"] += 1
        stats["pair_tighter"] += int(tighter)
        stats["instances"] += 1
    if stats["pair_tighter"] == 0 or stats["equal_at_triple"] == 0 or stats["direct_checks"] == 0:
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


def sh_feasible(n, edges, cap):
    """Is there a share certificate?  edges: list of (sites, weight); every weight must be split among the sites of its
    edge (nonnegative shares adding up to the weight) so that the load of every site is at most its capacity.  Linear
    programme: maximise the slack t with loads <= cap - t; returns the largest t (>= 0 iff a certificate exists)."""
    from scipy.optimize import linprog
    edges = [(T, w) for (T, w) in edges if w > 0]
    if not edges:
        return float(min(cap))
    nv = sum(len(T) for T, _ in edges)
    A_eq, b_eq, A_ub, col = [], [], np.zeros((n, nv + 1)), 0
    for T, w in edges:
        row = np.zeros(nv + 1)
        for i in T:
            row[col] = 1.0
            A_ub[i, col] = 1.0
            col += 1
        A_eq.append(row); b_eq.append(w)
    A_ub[:, nv] = 1.0                                                       # load_i + t <= cap_i
    cvec = np.zeros(nv + 1); cvec[nv] = -1.0
    res = linprog(cvec, A_ub=A_ub, b_ub=np.asarray(cap, float), A_eq=np.asarray(A_eq), b_eq=np.asarray(b_eq),
                  bounds=[(0, None)] * nv + [(None, None)], method="highs")
    return float(-res.fun) if res.status == 0 else -math.inf


@conjecture("XI.17 Share certificates for sharp-minimum conditions of second and third order (theory report Proposition 11.18b; ShareCertificates.lean: pairSum_le_of_shares, secondOrder_certified_of_shares, secondOrder_certified_of_rowSum, cover_of_site_shares — an answer to request P2-T2 of the Scientific Discovery Division): with an additive known part, least single-site excitation energies Delta_i and pair constants c_ij, the reference is the certified minimiser iff no set S of sites has sum_{i<j in S} c_ij > sum_{i in S} Delta_i (the exact criterion of Theorem 11.17), iff every c_ij can be split between its two sites with loads at most Delta_i (max-flow min-cut); the row-sum condition is the split in halves, sufficient and not necessary; the same with triple constants c_T split among three sites; with a pairwise known part and the deficits w_ij = max over changed states of [c_ij - second difference of the known part]_+ the split is sufficient for the reference to minimise the pairwise lower model")
def t_share_certificates(rng, trials):
    stats = dict(pairs=0, pair_yes=0, rowsum_yes=0, shares_not_rowsum=0, triples=0, triple_yes=0, thirds_yes=0,
                 pairwise=0, pairwise_cert=0, pairwise_exact=0, pairwise_rowsum=0)
    subsets = lambda n: (S for r in range(1, n + 1) for S in itertools.combinations(range(n), r))
    for it in range(max(60, trials // 4)):
        n = int(rng.integers(3, 8))
        c = np.triu(rng.exponential(1.0, size=(n, n)) * (rng.random((n, n)) < 0.6), 1)
        c = c + c.T
        delta = rng.exponential(1.0, size=n) * float(rng.choice([0.6, 1.0, 1.6])) * (n - 1) * 0.3
        over = max(sum(c[i, j] for i, j in itertools.combinations(S, 2)) - sum(delta[i] for i in S) for S in subsets(n))
        if abs(over) < 1e-7:
            continue
        exact = over < 0
        t = sh_feasible(n, [((i, j), c[i, j]) for i, j in itertools.combinations(range(n), 2)], delta)
        if (t >= -1e-9) != exact:
            return False, dict(reason="pairs: a share certificate exists iff no set of sites is over-dense — violated", n=n, over=over, slack=t)
        rowsum = bool((0.5 * c.sum(axis=1) <= delta + 1e-12).all())
        if rowsum and not exact:
            return False, dict(reason="the row-sum condition holds and the exact criterion fails", n=n)
        stats["pairs"] += 1; stats["pair_yes"] += int(exact); stats["rowsum_yes"] += int(rowsum)
        stats["shares_not_rowsum"] += int(exact and not rowsum)
        # triples
        m = int(rng.integers(3, 7))
        triples = list(itertools.combinations(range(m), 3))
        cT = {T: float(rng.exponential(1.0)) * float(rng.random() < 0.7) for T in triples}
        d3 = rng.exponential(1.0, size=m) * float(rng.choice([0.5, 1.0, 2.0])) * len(triples) / m
        over3 = max(sum(cT[T] for T in itertools.combinations(S, 3)) - sum(d3[i] for i in S) for S in subsets(m))
        if abs(over3) >= 1e-7:
            t3 = sh_feasible(m, [(T, cT[T]) for T in triples], d3)
            if (t3 >= -1e-9) != (over3 < 0):
                return False, dict(reason="triples: a share certificate exists iff no set of sites is over-dense — violated", m=m, over=over3, slack=t3)
            thirds = all(sum(cT[T] for T in triples if i in T) / 3 <= d3[i] + 1e-12 for i in range(m))
            if thirds and over3 > 0:
                return False, dict(reason="the rule of thirds holds and the exact criterion fails", m=m)
            stats["triples"] += 1; stats["triple_yes"] += int(over3 < 0); stats["thirds_yes"] += int(thirds)
        # a pairwise known part: the split of the deficits is sufficient for the reference to minimise the lower model
        nn = int(rng.integers(3, 6))
        ks = [int(k) for k in rng.integers(2, 4, size=nn)]
        h = [rng.normal(size=k) + 1.5 * np.arange(k) for k in ks]                # the reference state 0 is favoured
        J = {(i, j): 0.4 * rng.normal(size=(ks[i], ks[j])) for i, j in itertools.combinations(range(nn), 2)}
        cc = np.triu(0.3 * rng.exponential(1.0, size=(nn, nn)), 1); cc = cc + cc.T
        def L(x):                                                              # the pairwise lower model, reference 0
            S = [i for i in range(nn) if x[i] != 0]
            return sum(h[i][x[i]] for i in range(nn)) + sum(J[(i, j)][x[i], x[j]] for i, j in itertools.combinations(range(nn), 2)) \
                - sum(cc[i, j] for i, j in itertools.combinations(S, 2))
        x0 = tuple([0] * nn)
        exc = [min(L(tuple(a if l == i else 0 for l in range(nn))) - L(x0) for a in range(1, ks[i])) for i in range(nn)]
        w = {}
        for i, j in itertools.combinations(range(nn), 2):
            T = J[(i, j)]
            w[(i, j)] = max(max(cc[i, j] - (T[a, b] - T[a, 0] - T[0, b] + T[0, 0]) for a in range(1, ks[i]) for b in range(1, ks[j])), 0.0)
        tt = sh_feasible(nn, [(p, w[p]) for p in w], exc)
        is_min = all(L(x) >= L(x0) - 1e-10 for x in itertools.product(*[range(k) for k in ks]))
        if tt >= 1e-9 and not is_min:
            return False, dict(reason="pairwise known part: a share certificate exists and the reference does not minimise the lower model", nn=nn, slack=tt)
        halves = all(0.5 * sum(w[p] for p in w if i in p) <= exc[i] for i in range(nn))
        if halves and not is_min:
            return False, dict(reason="pairwise known part: the row-sum condition holds and the reference does not minimise the lower model", nn=nn)
        stats["pairwise"] += 1; stats["pairwise_cert"] += int(tt >= 1e-9); stats["pairwise_exact"] += int(is_min)
        stats["pairwise_rowsum"] += int(halves)
    if min(stats["pair_yes"], stats["pairs"] - stats["pair_yes"], stats["shares_not_rowsum"], stats["triple_yes"],
           stats["triples"] - stats["triple_yes"], stats["pairwise_cert"]) == 0:
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


@conjecture("XI.18 Second- and third-order remainders on domains with pairwise exclusions (theory report Proposition 11.18c; an answer to request P2-T3 of the Scientific Discovery Division): let D be a product of site alphabets minus forbidden pairs of states, x0 in D a reference, and D' the configurations of D all of whose changed states are compatible with the reference states of every other site; then D' is closed under resetting any set of sites to the reference, and for every function g on D', with constants c_ij (c_T) taken as the largest second (third) mixed differences over the rectangles (boxes) that lie inside D', |g - star part| <= sum of c_ij over the changed pairs and |g - I_2 g| <= sum of c_T over the changed triples at every point of D'; D itself need not be closed under resetting, and connectivity by single-site moves is not enough: on the three-point domain {00, 01, 11} the second-order class puts no constraint on the value at 11")
def t_remainder_on_domains(rng, trials):
    stats = dict(instances=0, points=0, not_reset_closed=0, strict_subdomain=0, worst2=0.0, worst3=0.0, tight2=0)
    for it in range(max(40, trials // 6)):
        n = int(rng.integers(3, 6))
        ks = [int(k) for k in rng.integers(2, 4, size=n)]
        forb = set()
        for i, j in itertools.combinations(range(n), 2):
            for a in range(ks[i]):
                for b in range(ks[j]):
                    if (a, b) != (0, 0) and rng.random() < (0.10 if a and b else 0.07):
                        forb.add((i, a, j, b))
        ok = lambda x: all((i, x[i], j, x[j]) not in forb for i, j in itertools.combinations(range(n), 2))
        D = [x for x in itertools.product(*[range(k) for k in ks]) if ok(x)]
        good = [[a for a in range(ks[i]) if a == 0 or all((min(i, j), a if i < j else 0, max(i, j), 0 if i < j else a) not in forb
                                                        for j in range(n) if j != i)] for i in range(n)]
        Dp = set(x for x in D if all(x[i] in good[i] for i in range(n)))
        reset = lambda x, U: tuple(x[i] if i in U else 0 for i in range(n))
        chg = lambda x: [i for i in range(n) if x[i] != 0]
        for x in Dp:                                                         # D' is closed under resetting
            S = chg(x)
            for r in range(len(S) + 1):
                for U in itertools.combinations(S, r):
                    if reset(x, U) not in Dp:
                        return False, dict(reason="D' is not closed under resetting sites to the reference", x=x, U=U)
        Dset = set(D)
        stats["not_reset_closed"] += int(any(reset(x, U) not in Dset for x in D for r in range(len(chg(x)) + 1)
                                             for U in itertools.combinations(chg(x), r)))
        stats["strict_subdomain"] += int(len(Dp) < len(D))
        mode = it % 3
        g = {x: float(rng.normal()) for x in Dp}
        if mode == 1:                                                        # nearly additive: small constants
            hh = [rng.normal(size=k) for k in ks]
            g = {x: sum(hh[i][x[i]] for i in range(n)) + 0.05 * float(rng.normal()) for x in Dp}
        # constants from the rectangles and boxes that lie inside D'
        c2 = {p: 0.0 for p in itertools.combinations(range(n), 2)}
        c3 = {T: 0.0 for T in itertools.combinations(range(n), 3)}
        def moved(x, T, b):
            y = list(x)
            for i, v in zip(T, b):
                y[i] = v
            return tuple(y)
        for x in Dp:
            for p in c2:
                for b in itertools.product(*[range(ks[i]) for i in p]):
                    pts = [moved(x, [p[q] for q in U], [b[q] for q in U]) for r in range(3) for U in itertools.combinations(range(2), r)]
                    if all(y in Dp for y in pts):
                        sgn = [(-1) ** (2 - r) for r in range(3) for U in itertools.combinations(range(2), r)]
                        c2[p] = max(c2[p], abs(sum(s * g[y] for s, y in zip(sgn, pts))))
            for T in c3:
                for b in itertools.product(*[range(ks[i]) for i in T]):
                    pts = [moved(x, [T[q] for q in U], [b[q] for q in U]) for r in range(4) for U in itertools.combinations(range(3), r)]
                    if all(y in Dp for y in pts):
                        sgn = [(-1) ** (3 - r) for r in range(4) for U in itertools.combinations(range(3), r)]
                        c3[T] = max(c3[T], abs(sum(s * g[y] for s, y in zip(sgn, pts))))
        x0 = tuple([0] * n)
        for x in Dp:
            S = chg(x)
            star = g[x0] + sum(g[reset(x, (i,))] - g[x0] for i in S)
            I2 = star + sum(g[reset(x, (i, j))] - g[reset(x, (i,))] - g[reset(x, (j,))] + g[x0] for i, j in itertools.combinations(S, 2))
            B2 = sum(c2[p] for p in itertools.combinations(S, 2))
            B3 = sum(c3[T] for T in itertools.combinations(S, 3))
            if abs(g[x] - star) > B2 + 1e-9:
                return False, dict(reason="second-order remainder exceeds the pair constants on a reset-closed domain", x=x, r=g[x] - star, B=B2)
            if abs(g[x] - I2) > B3 + 1e-9:
                return False, dict(reason="third-order remainder exceeds the triple constants on a reset-closed domain", x=x, r=g[x] - I2, B=B3)
            if len(S) == 2 and abs(abs(g[x] - star) - B2) < 1e-12 and B2 > 0:
                stats["tight2"] += 1
            stats["worst2"] = max(stats["worst2"], abs(g[x] - star) - B2)
            stats["worst3"] = max(stats["worst3"], abs(g[x] - I2) - B3)
            stats["points"] += 1
        stats["instances"] += 1
    # connectivity is not enough: D = {00, 01, 11}; no rectangle lies inside D, so every function on D has all its second
    # differences bounded by 0, and the value at 11 is not determined by the values at 00 and 01
    D3 = {(0, 0), (0, 1), (1, 1)}
    rect = [x for x in D3 if all(y in D3 for y in ((x[0], 1 - x[1]), (1 - x[0], x[1]), (1 - x[0], 1 - x[1])))]
    if rect:
        return False, dict(reason="the three-point domain contains a rectangle")
    if stats["not_reset_closed"] == 0 or stats["strict_subdomain"] == 0 or stats["tight2"] == 0:
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


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


@conjecture("XI.19 The remainder of the anchored expansion as an identity, anchored constants and site penalties at every order (theory report Theorem 11.18d; AnchoredRemainder.lean; the statement is Proposition 1 of the Scientific Discovery Division's workstream P3, SCI-MSG-0020): for every function, reference x0, configuration y and order m >= 1, g(y) - I_{m-1} g(y) is the sum over the m-subsets T of the changed sites of the mixed difference over T at the base point that equals y at the changed sites before min T and x0 elsewhere; hence |g - I_{m-1} g| is at most the sum of anchored constants (mixed differences at base points equal to x0 on T), which never exceed the uniform constants, equal them for two states per site and are strictly smaller for some functions with three; the site penalties gamma_i = (1/m) sum over T containing i of c_T cover the m-subsets of every set of sites, with equality for the full set; and I_{m-1} g -/+ the sum of gamma_i over the changed sites is a sandwich of g")
def t_remainder_identity(rng, trials):
    stats = dict(identities=0, worst=0.0, strictly_smaller=0, equal_binary=0, sandwiches=0, tightest=math.inf)
    shapes = [(3, 2), (3, 3), (4, 2), (4, 3), (3, 4), (5, 2), (5, 3)]
    for it in range(max(7, trials // 8)):
        n, k = shapes[it % len(shapes)]
        confs = all_configs(n, k)
        g = so_random_function(rng, n, k, ((1, 1.0), (2, 0.5), (3, 0.3), (n, 0.1)))
        x0 = tuple(int(v) for v in rng.integers(0, k, size=n))
        heavy = (n, k) in ((3, 2), (3, 3), (4, 2), (4, 3))          # constants by enumeration only where cheap
        for m in range(1, n + 1):
            interp = so_interpolant(g, n, k, m, x0)
            for y in confs:
                S = [i for i in range(n) if y[i] != x0[i]]
                total = 0.0
                for T in itertools.combinations(S, m):
                    z = tuple(y[i] if (i in S and i < T[0]) else x0[i] for i in range(n))
                    total += so_mixed_diff(g, z, T, {i: y[i] for i in T})
                err = abs((g[y] - interp[y]) - total)
                stats["worst"] = max(stats["worst"], err)
                stats["identities"] += 1
                if err > 1e-9:
                    return False, dict(reason="the remainder of the anchored expansion is not the sum of the mixed differences at the stated base points",
                                       n=n, k=k, m=m, err=err)
            if not heavy or m > 3:
                continue
            # anchored constants: base points that agree with the reference on T, every context elsewhere, every target
            c_anch, c_unif = {}, so_constants(g, n, k, m)
            for T in itertools.combinations(range(n), m):
                best = 0.0
                for z in confs:
                    if any(z[i] != x0[i] for i in T):
                        continue
                    for bt in itertools.product(range(k), repeat=m):
                        best = max(best, abs(so_mixed_diff(g, z, T, dict(zip(T, bt)))))
                c_anch[T] = best
                if best > c_unif[T] + 1e-9:
                    return False, dict(reason="an anchored constant exceeds the uniform constant", T=T)
                if k == 2:
                    if abs(best - c_unif[T]) > 1e-9:
                        return False, dict(reason="with two states per site the anchored and the uniform constants should coincide", T=T)
                    stats["equal_binary"] += 1
                elif best < c_unif[T] - 1e-6:
                    stats["strictly_smaller"] += 1
            gamma = [sum(c for T, c in c_anch.items() if i in T) / m for i in range(n)]
            for r in range(n + 1):
                for S in itertools.combinations(range(n), r):
                    lhs = sum(c_anch[T] for T in itertools.combinations(S, m))
                    rhs = sum(gamma[i] for i in S)
                    if lhs > rhs + 1e-9:
                        return False, dict(reason="the site penalties do not cover the m-subsets of a set of sites", S=S, m=m)
                    if r == n and abs(lhs - rhs) > 1e-9:
                        return False, dict(reason="for the full set of sites the site penalties should add up to the sum of the constants", m=m)
            for y in confs:
                S = [i for i in range(n) if y[i] != x0[i]]
                rem = sum(c_anch[T] for T in itertools.combinations(S, m))
                pen = sum(gamma[i] for i in S)
                if abs(g[y] - interp[y]) > rem + 1e-9:
                    return False, dict(reason="the remainder exceeds the sum of the anchored constants", m=m)
                if not (interp[y] - pen - 1e-9 <= g[y] <= interp[y] + pen + 1e-9):
                    return False, dict(reason="the sandwich by site penalties is violated", m=m)
                if pen > 0:
                    stats["tightest"] = min(stats["tightest"], (pen - abs(g[y] - interp[y])) / pen)
                stats["sandwiches"] += 1
    if not (stats["identities"] > 500 and stats["strictly_smaller"] > 0 and stats["equal_binary"] > 0 and stats["sandwiches"] > 100):
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


@conjecture("XI.20 The Hamming ball is necessary for a deterministic certificate (theory report Proposition 11.18e; an answer to the Scientific Discovery Division's question P3-T4, SCI-MSG-0020): the functions of order below m form a space of dimension N_ball = sum_{j<m} C(n,j)(k-1)^j on which the evaluations at the ball of radius m - 1 are unisolvent; for every set Q of fewer than N_ball configurations there is a function h of order below m, not identically zero, that vanishes on Q; its mixed differences of order m vanish, so g + t h has the order-m constants of g and the values of g on Q for every t, while its minimum tends to minus infinity; and a function of order below m that is not identically zero is non-zero on a fraction at least k^-(m-1) of the configurations, with equality for the indicator of a cylinder on m - 1 sites — so that a hinted function of order below m is refuted by k^(m-1) ln(1/delta) random evaluations, whatever the number of sites")
def t_ball_necessary(rng, trials):
    stats = dict(cases=0, largest=0, thinnest=math.inf)
    shapes = [(3, 2), (3, 3), (4, 2), (4, 3), (5, 2), (3, 4)]
    for it in range(max(6, trials // 10)):
        n, k = shapes[it % len(shapes)]
        confs = all_configs(n, k)
        x0 = tuple(int(v) for v in rng.integers(0, k, size=n))
        for m in range(1, n + 1):
            # the anchored basis of the functions of order below m: cylinders on fewer than m sites with states off the reference
            basis = []
            for j in range(m):
                for U in itertools.combinations(range(n), j):
                    for a in itertools.product(*[[s for s in range(k) if s != x0[i]] for i in U]):
                        basis.append((U, a))
            n_ball = sum(math.comb(n, j) * (k - 1) ** j for j in range(m))
            if len(basis) != n_ball:
                return False, dict(reason="the number of anchored basis functions is not N_ball", n=n, k=k, m=m)
            M = np.array([[1.0 if all(x[i] == s for i, s in zip(U, a)) else 0.0 for (U, a) in basis] for x in confs])
            if np.linalg.matrix_rank(M) != n_ball:
                return False, dict(reason="the functions of order below m do not have dimension N_ball", n=n, k=k, m=m)
            ball = [idx for idx, x in enumerate(confs) if sum(x[i] != x0[i] for i in range(n)) < m]
            if len(ball) != n_ball or np.linalg.matrix_rank(M[ball]) != n_ball:
                return False, dict(reason="the Hamming ball is not unisolvent for the functions of order below m", n=n, k=k, m=m)
            # a non-zero function of order below m is non-zero on a fraction at least k^-(m-1) of the configurations
            for trial in range(5):
                if trial == 0:
                    idxs, coeffs = np.array([len(basis) - 1]), np.array([1.0])   # a cylinder on m - 1 sites
                else:
                    idxs = rng.choice(len(basis), size=min(len(basis), int(rng.integers(1, 6))), replace=False)
                    coeffs = rng.integers(-2, 3, size=len(idxs)).astype(float)
                f = M[:, idxs] @ coeffs
                if np.abs(f).max() < 1e-9:
                    continue
                frac = float((np.abs(f) > 1e-9).mean())
                if frac < k ** (-(m - 1)) - 1e-12:
                    return False, dict(reason="a non-zero function of order below m vanishes on more than the fraction 1 - k^-(m-1) of the configurations",
                                       n=n, k=k, m=m, frac=frac)
                stats["thinnest"] = min(stats["thinnest"], frac * k ** (m - 1))
            if n_ball < 2:
                continue
            Q = rng.choice(len(confs), size=n_ball - 1, replace=False) if it % 2 else np.array(ball[:-1])
            _, sv, vt = np.linalg.svd(M[Q])
            coeff = vt[-1]                                          # a direction in the kernel of the evaluations on Q
            h = M @ coeff
            if np.abs(M[Q] @ coeff).max() > 1e-9 or np.abs(h).max() < 1e-6:
                return False, dict(reason="no nonzero function of order below m vanishes on a set of fewer than N_ball configurations",
                                   n=n, k=k, m=m)
            hd = {x: float(v) for x, v in zip(confs, h)}
            if m <= n:
                for _ in range(6):
                    T = tuple(sorted(rng.choice(n, size=m, replace=False).tolist()))
                    x = confs[int(rng.integers(len(confs)))]
                    b = {i: int(rng.integers(k)) for i in T}
                    if abs(so_mixed_diff(hd, x, T, b)) > 1e-9:
                        return False, dict(reason="a function of order below m has a nonzero mixed difference of order m", m=m)
            g = rng.normal(0, 1, len(confs))
            if min(float((g + 1e9 * h).min()), float((g - 1e9 * h).min())) > float(g.min()) - 1e3:
                return False, dict(reason="the minimum does not become unbounded along the hidden direction")
            stats["cases"] += 1
            stats["largest"] = max(stats["largest"], n_ball)
    if stats["cases"] < 15 or abs(stats["thinnest"] - 1) > 1e-9:
        return False, dict(reason="cases not exercised, or the bound on the support never attained", **stats)
    return True, stats


@conjecture("XI.21 Share certificates after the Scientific Discovery Division's review SCI-REV-0012 (theory report Propositions 11.18b (d), (e) and 11.18c (a) as corrected; StateShares.lean).  (a) State-dependent shares s_ij(a) >= 0 with s_ij(a) + s_ji(b) >= c_ij - T_ij(a, b) for changed states and loads sum_j s_ij(a) <= A_i(a) certify that the reference minimises the pairwise lower model L(x) - L(x0) = sum_{i changed} A_i(x_i) + sum_{i<j changed} [T_ij(x_i, x_j) - c_ij]; constant shares of the deficits are a special case and strictly weaker (an instance with two sites and three states, the one of stateShare_witness); (b) such shares exist exactly when the reference solves the pairwise linear relaxation (local polytope) of the minimisation of L - they are a dual solution - so they can fail although the reference minimises L (an explicit frustrated triangle with an integrality gap); (c) on a reset-closed domain that is not a product the sound direction survives (shares imply that the reference minimises the lower model over the domain) and completeness does not: two sites with states {0, 1, 2}, the pair of states (1, 1) excluded, excitation energies (1, 10), pair constant 3 - the reference is certified for every member of the class on the domain (linear programme over the class) although the set of both sites is over-dense, 3 > 1 + 1")
def t_state_shares(rng, trials):
    from scipy.optimize import linprog
    stats = dict(instances=0, state=0, const=0, state_not_const=0, minimiser=0, gap=0, domains=0, nonproduct=0,
                 complete_fails=0, sound_domain=0)

    def model_gap(n, k, A, c, T, x):
        S = [i for i in range(n) if x[i] != 0]
        return sum(A[i][x[i]] for i in S) + sum(T[i][j][x[i]][x[j]] - c[i][j] for a, i in enumerate(S) for j in S[a + 1:])

    def state_shares_exist(n, k, A, c, T, signed=False):
        """feasibility of: s_ij(a) >= 0, s_ij(a) + s_ji(b) >= c_ij - T_ij(a, b), sum_j s_ij(a) <= A_i(a)"""
        idx = {}
        for i in range(n):
            for j in range(n):
                if i != j:
                    for a in range(1, k):
                        idx[(i, j, a)] = len(idx)
        rows, rhs = [], []
        for i in range(n):
            for j in range(i + 1, n):
                for a in range(1, k):
                    for b in range(1, k):
                        r = np.zeros(len(idx)); r[idx[(i, j, a)]] = -1; r[idx[(j, i, b)]] = -1
                        rows.append(r); rhs.append(-(c[i][j] - T[i][j][a][b]))
        for i in range(n):
            for a in range(1, k):
                r = np.zeros(len(idx))
                for j in range(n):
                    if j != i:
                        r[idx[(i, j, a)]] = 1
                rows.append(r); rhs.append(A[i][a])
        res = linprog(np.zeros(len(idx)), A_ub=np.array(rows), b_ub=np.array(rhs),
                      bounds=[(None if signed else 0, None)] * len(idx), method="highs")
        return res.status == 0

    def const_shares_exist(n, w, load):
        idx = {(i, j): t for t, (i, j) in enumerate((i, j) for i in range(n) for j in range(n) if i != j)}
        rows, rhs = [], []
        for i in range(n):
            for j in range(i + 1, n):
                r = np.zeros(len(idx)); r[idx[(i, j)]] = -1; r[idx[(j, i)]] = -1
                rows.append(r); rhs.append(-w[i][j])
        for i in range(n):
            r = np.zeros(len(idx))
            for j in range(n):
                if j != i:
                    r[idx[(i, j)]] = 1
            rows.append(r); rhs.append(load[i])
        res = linprog(np.zeros(len(idx)), A_ub=np.array(rows), b_ub=np.array(rhs), bounds=[(0, None)] * len(idx), method="highs")
        return res.status == 0

    def relaxation_value(n, k, A, c, T):
        """min over the local polytope of sum theta_i mu_i + sum theta_ij mu_ij; 0 iff the reference is optimal"""
        ui = {(i, a): i * k + a for i in range(n) for a in range(k)}
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        pi = {(p, a, b): n * k + t * k * k + a * k + b for t, p in enumerate(pairs) for a in range(k) for b in range(k)}
        nv = n * k + len(pairs) * k * k
        cost = np.zeros(nv)
        for i in range(n):
            for a in range(1, k):
                cost[ui[(i, a)]] = A[i][a]
        for (i, j) in pairs:
            for a in range(1, k):
                for b in range(1, k):
                    cost[pi[((i, j), a, b)]] = T[i][j][a][b] - c[i][j]
        rows, rhs = [], []
        for i in range(n):
            r = np.zeros(nv)
            for a in range(k):
                r[ui[(i, a)]] = 1
            rows.append(r); rhs.append(1.0)
        for (i, j) in pairs:
            for a in range(k):
                r = np.zeros(nv); r[ui[(i, a)]] = -1
                for b in range(k):
                    r[pi[((i, j), a, b)]] = 1
                rows.append(r); rhs.append(0.0)
            for b in range(k):
                r = np.zeros(nv); r[ui[(j, b)]] = -1
                for a in range(k):
                    r[pi[((i, j), a, b)]] = 1
                rows.append(r); rhs.append(0.0)
        res = linprog(cost, A_eq=np.array(rows), b_eq=np.array(rhs), bounds=[(0, None)] * nv, method="highs")
        return float(res.fun)

    def analyse(n, k, A, c, T):
        confs = list(itertools.product(range(k), repeat=n))
        mn = min(model_gap(n, k, A, c, T, x) for x in confs)
        st = state_shares_exist(n, k, A, c, T)
        w = [[max(0.0, max(c[i][j] - T[i][j][a][b] for a in range(1, k) for b in range(1, k))) if i != j else 0.0
              for j in range(n)] for i in range(n)]
        cs = const_shares_exist(n, w, [min(A[i][1:]) for i in range(n)])
        lp = relaxation_value(n, k, A, c, T)
        return mn, st, cs, lp

    half = lambda lo, hi, size=None: rng.integers(int(2 * lo), int(2 * hi) + 1, size=size) / 2.0
    for it in range(max(60, trials // 2)):
        n, k = int(rng.integers(2, 5)), int(rng.integers(2, 4))
        A = [[0.0] + [float(v) for v in half(0.5, 4.0, k - 1)] for _ in range(n)]
        c = [[0.0] * n for _ in range(n)]
        T = [[[[0.0] * k for _ in range(k)] for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                c[i][j] = c[j][i] = float(half(0.0, 3.0)) if rng.random() < 0.8 else 0.0
                if rng.random() < 0.6:
                    for a in range(1, k):
                        for b in range(1, k):
                            T[i][j][a][b] = T[j][i][b][a] = float(half(-1.0, 2.5))
        mn, st, cs, lp = analyse(n, k, A, c, T)
        stats["instances"] += 1
        stats["state"] += int(st); stats["const"] += int(cs); stats["minimiser"] += int(mn >= -1e-9)
        stats["state_not_const"] += int(st and not cs); stats["gap"] += int(mn >= -1e-9 and not st)
        if st and mn < -1e-7:
            return False, dict(reason="state-dependent shares exist although the reference does not minimise the lower model",
                               n=n, k=k, mn=mn)
        if cs and not st:
            return False, dict(reason="constant shares of the deficits exist but state-dependent shares do not", n=n, k=k)
        if st != (lp >= -1e-6):
            return False, dict(reason="state-dependent shares do not exist exactly when the reference solves the linear relaxation",
                               n=n, k=k, shares=st, relaxation=lp)

    # the witness of StateShares.lean: two sites, three states, the pair (1, 1) raised by 2 by the known part
    A = [[0.0, 1.0, 10.0], [0.0, 1.0, 10.0]]
    c = [[0.0, 3.0], [3.0, 0.0]]
    T = [[[[0.0] * 3 for _ in range(3)] for _ in range(2)] for _ in range(2)]
    T[0][1][1][1] = T[1][0][1][1] = 2.0
    mn, st, cs, lp = analyse(2, 3, A, c, T)
    if not (st and not cs and mn >= 0):
        return False, dict(reason="the two-site witness: state-dependent shares should exist and constant shares of the deficits not",
                           state=st, const=cs, mn=mn)
    stats["state_not_const"] += 1                                  # the witness is the decisive case; random ones are extra
    # an integrality gap: a frustrated triangle of binary sites; the reference minimises the model and no shares exist
    A = [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]]
    c = [[0.0, 2.0, 2.0], [2.0, 0.0, 0.0], [2.0, 0.0, 0.0]]
    T = [[[[0.0] * 2 for _ in range(2)] for _ in range(3)] for _ in range(3)]
    T[1][2][1][1] = T[2][1][1][1] = 10.0
    mn, st, cs, lp = analyse(3, 2, A, c, T)
    if not (mn >= 0 and not st and lp < -0.4):
        return False, dict(reason="the frustrated triangle: the reference should minimise the model, the relaxation should be negative and no shares should exist",
                           mn=mn, state=st, relaxation=lp)

    # (c) reset-closed domains that are not products: additive known part, constants c_ij
    def domain_case(n, k, A, c, forbidden):
        D = [x for x in itertools.product(range(k), repeat=n)
             if not any(((i, x[i]), (j, x[j])) in forbidden for i in range(n) for j in range(i + 1, n))]
        Z = [[[[0.0] * k for _ in range(k)] for _ in range(n)] for _ in range(n)]
        crit = min(model_gap(n, k, A, c, Z, x) for x in D) >= -1e-9          # the reference minimises the lower model over D
        sh = const_shares_exist(n, c, [min(A[i][1:]) for i in range(n)])
        return D, crit, sh

    for it in range(max(40, trials // 4)):
        n, k = 3, 3
        A = [[0.0] + [float(v) for v in half(0.5, 4.0, k - 1)] for _ in range(n)]
        c = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                c[i][j] = c[j][i] = float(half(0.0, 3.0))
        forbidden = set()
        for i in range(n):
            for j in range(i + 1, n):
                for a in range(1, k):
                    for b in range(1, k):
                        if rng.random() < 0.3:
                            forbidden.add(((i, a), (j, b)))
        D, crit, sh = domain_case(n, k, A, c, forbidden)
        if any(tuple(0 if t in R else x[t] for t in range(n)) not in D for x in D for r in range(n + 1)
               for R in itertools.combinations(range(n), r)):
            return False, dict(reason="a product minus forbidden pairs of changed states is not reset-closed")
        stats["domains"] += 1
        stats["nonproduct"] += int(len(D) < k ** n)
        if sh and not crit:
            return False, dict(reason="shares exist on a reset-closed domain although the reference does not minimise the lower model over it")
        stats["sound_domain"] += int(sh)
        stats["complete_fails"] += int(crit and not sh)

    # the counter-example to completeness (SCI-REV-0012, section 3), with the class on the domain as a linear programme
    A = [[0.0, 1.0, 10.0], [0.0, 1.0, 10.0]]
    c = [[0.0, 3.0], [3.0, 0.0]]
    D, crit, sh = domain_case(2, 3, A, c, {((0, 1), (1, 1))})
    Dfull, crit_full, _ = domain_case(2, 3, A, c, set())
    if not (len(D) == 8 and crit and not sh and not crit_full):
        return False, dict(reason="the two-site counter-example: the criterion should hold on the domain, fail on the product, and no shares should exist",
                           crit=crit, shares=sh, crit_full=crit_full)
    # least value over the class on D of (E0 + g')(x) - (E0 + g')(x0): g' = 0 on the star, mixed differences over the
    # rectangles inside D bounded by c
    pos = {x: t for t, x in enumerate(D)}
    rows, rhs = [], []
    for a, a2 in itertools.combinations(range(3), 2):
        for b, b2 in itertools.combinations(range(3), 2):
            corners = [(a, b), (a, b2), (a2, b), (a2, b2)]
            if all(x in pos for x in corners):
                r = np.zeros(len(D)); r[pos[(a2, b2)]] += 1; r[pos[(a2, b)]] -= 1; r[pos[(a, b2)]] -= 1; r[pos[(a, b)]] += 1
                rows += [r, -r]; rhs += [3.0, 3.0]
    star = [x for x in D if x[0] == 0 or x[1] == 0]
    eq = [np.eye(len(D))[pos[x]] for x in star]
    worst = math.inf
    for x in D:
        obj = np.eye(len(D))[pos[x]]
        res = linprog(obj, A_ub=np.array(rows), b_ub=np.array(rhs), A_eq=np.array(eq), b_eq=np.zeros(len(eq)),
                      bounds=[(None, None)] * len(D), method="highs")
        if res.status != 0:
            return False, dict(reason="the class on the domain is empty or unbounded at a point of the domain", x=x, status=res.status)
        worst = min(worst, A[0][x[0]] + A[1][x[1]] + float(res.fun))
    if worst < -1e-7:
        return False, dict(reason="on the two-site domain the reference is not a minimiser for some member of the class", worst=worst)
    stats["complete_fails"] += 1                                   # the explicit counter-example; random domains are extra
    if not (stats["state"] > 5 and stats["instances"] - stats["state"] > 5 and stats["nonproduct"] > 10
            and stats["sound_domain"] > 0):
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


@conjecture("XI.22 Randomised algorithms and the Hamming ball (theory report Proposition 11.18e(b), (b'), (c) as corrected after the Scientific Discovery Division's review SCI-REV-0013, findings M1 and m8; the counter-algorithm and the support bound for unequal alphabets are that division's).  (a) On the cube every affine function h satisfies |h(s)| >= ||h||_inf/(n + 1) on at least half of the points, with equality for h = 1 + s_1, and n + 1 cannot be replaced by n; (b) hence for g = h + R with |R| <= C every such point x gives ||g||_inf <= (|g(x)| + C)(n + 1) + C (attained), so that ceil(log2(1/delta)) uniformly random evaluations yield a valid finite bound with probability 1 - delta whatever n - five evaluations at delta = 0.05 where the deterministic count is n + 1 - while at a point where h is small the bound fails; (c) on a grid with k_i states at site i the least support of a non-zero function of order below m is exactly |X| / (product of the m - 1 largest k_i) (exhaustive on small grids), attained by a cylinder on the largest sites, so that k_max^-(m-1) is not attained for unequal alphabets; (d) on one site with k states the count of the ball holds for randomised algorithms as well: the algorithm that skips one uniformly random state with probability r and returns a bracket of width L fails with probability exactly r/k on an instance with a needle deeper than L, so failure delta allows k delta skipped evaluations on average and no more - provided the bracket returned after a skip is wrong for at most one skipped state: for ln Z its width must be at least ln 2, and with two equally deep states and a smaller width both skips fail (the Scientific Discovery Division's remark, SCI-RES-0016); in general the bracket of width W is wrong for at most min(k, ceil(1/(1 - e^-W)) - 1) skipped states, k equally deep states attain this, and for the minimum the bound 'least evaluated value minus w' is wrong for at most one skipped state for every slack w >= 0, ties included (that division's review SCI-REV-0015, m1); with needles of L depths that no output serves two at a time, a skip probability above delta (L + 1)/L forces a failure probability above delta on one of the L + 1 instances whatever is returned after a skip")
def t_random_ball(rng, trials):
    stats = dict(affine=0, least_good=math.inf, sharp_n=0, tight=math.inf, bad_fails=0, grids=0, unequal_gap=0, one_site=0, twin=0,
                 count_attained=0, min_slack=0, ladder=0)
    # (a), (b): affine functions on the cube
    for n in range(2, 9):
        S = np.array(list(itertools.product((-1.0, 1.0), repeat=n)))
        P = len(S)
        cands = [(1.0, np.eye(n)[0]), (1.0, np.ones(n)), (0.0, np.eye(n)[0] + np.eye(n)[1])]
        for _ in range(max(6, trials // 20)):
            kind = int(rng.integers(3))
            if kind == 0:
                cands.append((float(rng.normal()), rng.normal(0, 1, n)))
            elif kind == 1:
                cands.append((float(rng.integers(-2, 3)), rng.integers(-2, 3, n).astype(float)))
            else:
                b = np.zeros(n)
                b[rng.choice(n, size=int(rng.integers(1, 3)), replace=False)] = rng.integers(1, 4)
                cands.append((float(rng.integers(0, 3)), b))
        # a hill-climbing adversary on integer coefficients, minimising the number of points where |h| is large
        a_cur, b_cur = float(rng.integers(-3, 4)), rng.integers(-3, 4, n).astype(float)

        def good_fraction(a, b, divisor):
            h = a + S @ b
            top = abs(a) + np.abs(b).sum()
            if top < 1e-12:
                return None
            return float((np.abs(h) >= top / divisor - 1e-9).mean())

        cur = good_fraction(a_cur, b_cur, n + 1)
        for _ in range(40):
            j = int(rng.integers(n + 1))
            step = float(rng.choice([-1.0, 1.0]))
            a_new, b_new = a_cur, b_cur.copy()
            if j == n:
                a_new += step
            else:
                b_new[j] += step
            new = good_fraction(a_new, b_new, n + 1)
            if new is not None and (cur is None or new <= cur):
                a_cur, b_cur, cur = a_new, b_new, new
        cands.append((a_cur, b_cur))
        for a, b in cands:
            frac = good_fraction(a, b, n + 1)
            if frac is None:
                continue
            if frac < 0.5 - 1e-12:
                return False, dict(reason="an affine function is below ||h||/(n + 1) in absolute value on more than half of the cube",
                                   n=n, a=a, b=b.tolist(), frac=frac)
            stats["least_good"] = min(stats["least_good"], frac)
            stats["affine"] += 1
        # n + 1 cannot be replaced by n: h = 1 + sum s_i on an even number of sites
        if n % 2 == 0 and good_fraction(1.0, np.ones(n), n) < 0.5 - 1e-12:
            stats["sharp_n"] += 1
        # (b) the bound from one good point, with a remainder
        for a, b in cands[:6]:
            h = a + S @ b
            top = abs(a) + np.abs(b).sum()
            if top < 1e-12:
                continue
            C = float(rng.uniform(0.05, 0.7))
            R = rng.uniform(-C, C, P)
            if (a, tuple(b)) == (1.0, tuple(np.ones(n))):
                # the extremal remainder: -C where h = 1 (if such a point exists), +C at the maximiser
                R = np.where(np.abs(h - 1.0) < 1e-9, -C, R)
                R[int(np.argmax(h))] = C
            g = h + R
            good = np.abs(h) >= top / (n + 1) - 1e-9
            B = (np.abs(g) + C) * (n + 1) + C
            if (B[good] < np.abs(g).max() - 1e-9).any():
                return False, dict(reason="at a point where |h| >= ||h||/(n + 1) the bound (|g(x)| + C)(n + 1) + C is below ||g||_inf", n=n)
            stats["tight"] = min(stats["tight"], float((B[good] - np.abs(g).max()).min()))
        # at a point where h is small the bound fails: h = 100 (1 + s_1), remainder of size 0.1
        h = 100.0 * (1.0 + S[:, 0])
        g = h + rng.uniform(-0.1, 0.1, P)
        B = (np.abs(g) + 0.1) * (n + 1) + 0.1
        bad = np.abs(h) < 200.0 / (n + 1) - 1e-9
        if bad.mean() != 0.5:
            return False, dict(reason="1 + s_1 is not small on exactly half of the cube")
        stats["bad_fails"] += int((B[bad] < np.abs(g).max()).all())
    q5 = math.ceil(math.log2(1 / 0.05))
    if not (q5 == 5 and 0.5 ** q5 <= 0.05 and all(q5 < 0.95 * (n + 1) for n in range(5, 40))):
        return False, dict(reason="five random evaluations at delta = 0.05: the count", q=q5)
    # (c) least support of a function of order below m, exhaustively: a vector lies in the space iff it is orthogonal
    # to a basis of the complement, so a non-zero function supported in a set exists iff the complement's columns
    # on that set are dependent
    grids = [((2, 2, 3), 3), ((2, 2, 3), 2), ((2, 3, 3), 3), ((3, 3), 2), ((2, 2, 2), 2), ((2, 2, 2), 3), ((2, 3), 2), ((2, 2, 4), 3)]
    for ks, m in grids:
        n = len(ks)
        confs = list(itertools.product(*[range(k) for k in ks]))
        N = len(confs)
        basis = []
        for j in range(m):
            for U in itertools.combinations(range(n), j):
                for a in itertools.product(*[range(1, ks[i]) for i in U]):
                    basis.append((U, a))
        M = np.array([[1.0 if all(x[i] == s for i, s in zip(U, a)) else 0.0 for (U, a) in basis] for x in confs])
        rank = np.linalg.matrix_rank(M)
        n_ball = sum(math.prod(ks[i] - 1 for i in U) for j in range(m) for U in itertools.combinations(range(n), j))
        if rank != n_ball or len(basis) != n_ball:
            return False, dict(reason="dimension of the functions of order below m on a grid with unequal alphabets", ks=ks, m=m)
        Uf, _, _ = np.linalg.svd(M, full_matrices=True)
        D = Uf[:, rank:].T                                           # rows: a basis of the orthogonal complement
        largest = sorted(ks, reverse=True)[:m - 1]
        predicted = N // math.prod(largest) if largest else N
        found = None
        for s in range(1, N + 1):
            for sub in itertools.combinations(range(N), s):
                if D.shape[0] == 0 or np.linalg.matrix_rank(D[:, sub], tol=1e-9) < s:
                    found = s
                    break
            if found is not None:
                break
        if found != predicted:
            return False, dict(reason="the least support of a function of order below m is not |X| / (product of the m - 1 largest alphabet sizes)",
                               ks=ks, m=m, found=found, predicted=predicted)
        # the cylinder on the m - 1 largest sites attains it
        order = sorted(range(n), key=lambda i: -ks[i])[:m - 1]
        cyl = np.array([1.0 if all(x[i] == ks[i] - 1 for i in order) else 0.0 for x in confs])
        coef, res, _, _ = np.linalg.lstsq(M, cyl, rcond=None)
        if np.abs(M @ coef - cyl).max() > 1e-9 or int(cyl.sum()) != predicted:
            return False, dict(reason="the cylinder on the largest sites is not of order below m, or has another support", ks=ks, m=m)
        if len(set(ks)) > 1 and m > 1 and N / max(ks) ** (m - 1) < found - 1e-9:
            stats["unequal_gap"] += 1                               # k_max^-(m-1) is valid and not attained
        stats["grids"] += 1
    # (d) one site with k states: the count of the ball holds for randomised algorithms
    for k in range(2, 7):
        Lw, depth = 3.0, 40.0
        r = float(rng.uniform(0.05, 0.9))
        hvals = rng.normal(0, 1, k)
        a0 = int(rng.integers(k))
        needle = hvals.copy()
        needle[a0] = -depth
        for inst, expect in ((needle, r / k), (np.zeros(k), 0.0)):
            lnZ = math.log(float(np.exp(-inst).sum()))
            fail = 0.0
            for a in range(k):
                seen = math.log(float(np.exp(-np.delete(inst, a)).sum()))
                if not (seen - 1e-12 <= lnZ <= seen + Lw + 1e-12):
                    fail += r / k
            if abs(fail - expect) > 1e-12:
                return False, dict(reason="one site: the failure probability of the algorithm that skips a random state", k=k, fail=fail, expect=expect)
        # the bracket returned after a skip must be wrong for at most one skipped state: with two equally deep states
        # and a width below ln 2 both skips fail (failure probability 2 r/k); from the width ln 2 on neither does
        twin = np.zeros(k)
        twin[a0] = twin[(a0 + 1) % k] = -depth
        for width, expect in ((0.5, 2 * r / k), (math.log(2.0) + 1e-9, 0.0)):
            lnZ = math.log(float(np.exp(-twin).sum()))
            fail = 0.0
            for a in range(k):
                seen = math.log(float(np.exp(-np.delete(twin, a)).sum()))
                if not (seen - 1e-12 <= lnZ <= seen + width + 1e-12):
                    fail += r / k
            if abs(fail - expect) > 1e-12:
                return False, dict(reason="one site, two equally deep states: the width ln 2 of the bracket returned after a skip",
                                   k=k, width=width, fail=fail, expect=expect)
        stats["twin"] += 1
        # the general count (review SCI-REV-0015, m1): after a skip the bracket [ln Z_seen, ln Z_seen + W] is wrong for at
        # most min(k, ceil(1/(1 - e^-W)) - 1) skipped states; k equally deep states attain it (all k skips fail iff
        # W < ln(k/(k - 1)))
        thr = math.log(k / (k - 1.0))
        cases = [(np.full(k, -depth), w_) for w_ in (0.5 * thr, thr - 1e-9, thr + 1e-9, 1.0)]
        cases += [(rng.normal(0, 2, k), float(rng.uniform(0.02, 2.0))) for _ in range(6)]
        for inst, width in cases:
            shift = float(inst.min())
            lnZ = math.log(float(np.exp(-(inst - shift)).sum())) - shift
            nfail = 0
            for a in range(k):
                seen = math.log(float(np.exp(-(np.delete(inst, a) - shift)).sum())) - shift
                nfail += not (seen - 1e-12 <= lnZ <= seen + width + 1e-12)
            cap = min(k, math.ceil(1.0 / (1.0 - math.exp(-width))) - 1)
            if nfail > cap:
                return False, dict(reason="one site: more skipped states make the bracket wrong than min(k, ceil(1/(1 - e^-W)) - 1)",
                                   k=k, width=width, nfail=nfail, cap=cap)
            if np.ptp(inst) == 0 and nfail != (k if width < thr else 0):
                return False, dict(reason="one site, k equally deep states: all skips fail iff W < ln(k/(k - 1))", k=k, width=width,
                                   nfail=nfail)
            stats["count_attained"] += int(nfail == cap and nfail == k)
        # the minimum: 'least evaluated value minus w' is wrong for at most one skipped state, for every slack w >= 0 and
        # with ties (a tied minimiser is still seen); a single needle makes exactly one skip wrong
        for inst in (needle, twin, hvals, np.round(hvals)):
            for w_ in (0.0, 0.3):
                true_min = float(inst.min())
                nfail = sum(1 for a in range(k) if float(np.delete(inst, a).min()) - w_ > true_min + 1e-12)
                if nfail > 1 or (inst is needle and nfail != 1) or (inst is twin and nfail != 0):
                    return False, dict(reason="one site, the minimum: the bound returned after a skip is wrong for more than one skipped state",
                                       k=k, slack=w_, nfail=nfail)
        stats["min_slack"] += 1
        # needles of L depths (review SCI-REV-0015, addition A1): if after a skip the answer for instance j is returned
        # with probability pi_j, the failure probability on instance j is s (1 - pi_j); these sum to s L, so one of
        # them is at least s L/(L + 1): failure at most delta on all L + 1 instances forces s <= delta (L + 1)/L, and
        # the uniform guess attains it
        Ld = k - 1
        pi_guess = rng.dirichlet(np.ones(Ld + 1))
        s_skip = 0.05 * (Ld + 1) / Ld
        if (s_skip * (1 - pi_guess)).max() < 0.05 - 1e-12 or abs((s_skip * (1 - 1.0 / (Ld + 1))) - 0.05) > 1e-12:
            return False, dict(reason="needles of finitely many depths: the bound delta (L + 1)/L on the skip probability", L=Ld)
        if (1.01 * s_skip * (1 - pi_guess)).max() <= 0.05:
            return False, dict(reason="needles of finitely many depths: a skip probability above delta (L + 1)/L was not punished", L=Ld)
        stats["ladder"] += 1
        # failure at most delta on every needle instance forces r <= k delta: the expected number of evaluations
        # k - r is at least (1 - delta) k, the count of Proposition 11.18e(b')
        delta = 0.05
        if abs((k - k * delta) - (1 - delta) * k) > 1e-12:
            return False, dict(reason="arithmetic of the one-site count")
        stats["one_site"] += 1
    if not (stats["affine"] >= 40 and abs(stats["least_good"] - 0.5) < 1e-12 and stats["sharp_n"] >= 3 and abs(stats["tight"]) < 1e-9
            and stats["bad_fails"] >= 7 and stats["grids"] >= 8 and stats["unequal_gap"] >= 2 and stats["one_site"] >= 5
            and stats["twin"] >= 5 and stats["count_attained"] >= 10 and stats["min_slack"] >= 5 and stats["ladder"] >= 5):
        return False, dict(reason="cases not exercised: the half is not attained, the bound not tight, or a constructed case missing", **stats)
    return True, stats


def sl_subsets(n):
    return [frozenset(i for i in range(n) if (mask >> i) & 1) for mask in range(1 << n)]


def sl_level_pen(n, m, c, k, divisor=None):
    """the level-k share model: pen_k(S) = sum over k-subsets K of S of sum_{T contains K} c_T / C(m, k)"""
    div = math.comb(m, k) if divisor is None else divisor
    share = {K: sum(v for T, v in c.items() if set(K) <= T) / div for K in itertools.combinations(range(n), k)}
    return {S: sum(v for K, v in share.items() if set(K) <= S) for S in sl_subsets(n)}, share


def sl_alloc_pen(n, lam):
    """penalty of an allocation lam[(T, K)] >= 0: pen(S) = sum of lam over the pairs (T, K) with K inside S"""
    return {S: sum(v for (T, K), v in lam.items() if K <= S) for S in sl_subsets(n)}


def sl_law(n, p):
    """product law of the changed set: site i is off the anchor with probability p[i]"""
    return {S: math.prod(p[i] if i in S else 1 - p[i] for i in range(n)) for S in sl_subsets(n)}


def sl_upper(law, pen):
    return math.log(sum(law[S] * math.exp(pen[S]) for S in law))


def sl_lower(law, pen):
    return -math.log(sum(law[S] * math.exp(-pen[S]) for S in law))


@conjecture("XI.23 Shares of every level, and the allocation for a law (theory report Theorem 11.18d(c'), Proposition 11.18f; ShareLevels.lean; the pair and triple forms with a band are Lemmas A, A' of the Scientific Discovery Division's workstream P6, SCI-MSG-0025; the questions P6-T1, P5-T3 are that division's).  For constants c_T >= 0 on the m-subsets: (a) charging each constant in equal parts to the k-subsets of T gives penalties pen_k(S) = sum_T c_T C(|T and S|, k)/C(m, k) with env = pen_m <= pen_{m-1} <= ... <= pen_1 <= pen_0 = sum of all constants, pointwise in the changed set S, with equality for the set of all sites and strict inequality elsewhere; (b) shares of level k + 1 outside a window, pushed down in equal parts to their k-subsets, give a penalty between the levels k + 1 and k; (c) every allocation lam_{T,K} >= 0 with sum_K lam_{T,K} = c_T covers; (d) for a law of the changed set the upper end ln E e^{pen} is convex and the lower end -ln E e^{-pen} is concave in the allocation, with gradient the tilted probability that K is changed; so the upper end of an exchangeable instance is least at equal shares, while the lower end is least at a vertex - each constant charged to one k-subset - and the two ends want different allocations; (e) to first order both ends are sum_T sum_K lam_{T,K} P(K changed): charge every constant to its least probable sub-pattern; with independent sites that is the allocation gamma_i = Gamma(sites at least as mobile as i) - Gamma(sites more mobile than i), Gamma(R) the sum of the constants inside R, and on an instance with four nearly frozen sites among six it lowers the upper end 8 times and the lower end 13 times, while on a homogeneous instance it raises the upper end and lowers the lower one - the two ends want different allocations; (f) beyond first order (the Scientific Discovery Division's review SCI-REV-0015, m4, m5, and its message SCI-RES-0017): for independent sites and site penalties the two ends are sums of softplus differences in f_i -+ gamma_i, f_i = ln((1 - p_i)/p_i), a site pays between max(p gamma, gamma - ln(1/p)) and p (e^gamma - 1) at the upper end and at most min(p gamma, -ln(1 - p)) at the lower; for any law and any allocation of level k the lower end is at most C(m, k) times that of equal shares; for any law every covering vector of site penalties has an upper end at least ln(1 + sum_i (lam - p_i)^+), lam the water level with sum_i ln(lam/p_i)^+ = Gamma; among vectors covering the nested sets of an ordering by nondecreasing p the marginal vector has the least first-order cost (CoreGreedy.lean), and not for another ordering; with tied sites the formula read with ties double-charges (sum 4 against Gamma = 2), the upper end is least when the tied sites share (0.0259 against 0.0298 at the vertex), and the upper end of a vertex is not bounded by a multiple of that of equal shares; at the pair level under a product law the least probable pair of T is its two most frozen sites, and the pair penalties of that vertex are second differences Gamma(A + i + j) - Gamma(A + i) - Gamma(A + j) + Gamma(A), A the sites after j (an answer to that division's question A17-T3)")
def t_share_levels(rng, trials):
    stats = dict(cases=0, strict_levels=0, strict_window=0, convex_strict=0, concave_strict=0, vertex_below_uniform=0,
                 greedy_gain_upper=None, greedy_gain_lower=None, two_ends_differ=0)
    for it in range(max(8, trials // 30)):
        n = int(rng.choice([5, 6]))
        m = int(rng.choice([3, 4])) if n == 6 else 3
        subs_m = [frozenset(T) for T in itertools.combinations(range(n), m)]
        c = {T: float(rng.exponential(0.4)) for T in subs_m}
        gamma_all = sum(c.values())
        allS = sl_subsets(n)
        env = {S: sum(v for T, v in c.items() if T <= S) for S in allS}
        pens, shares = [], []
        for k in range(m + 1):
            pk, sk = sl_level_pen(n, m, c, k)
            pens.append(pk)
            shares.append(sk)
        full = frozenset(range(n))
        for S in allS:
            if abs(pens[m][S] - env[S]) > 1e-9 or abs(pens[0][S] - gamma_all) > 1e-9:
                return False, dict(reason="level m is not the envelope, or level 0 is not the sum of all constants")
            for k in range(m + 1):
                count = sum(v * math.comb(len(T & S), k) / math.comb(m, k) for T, v in c.items())
                if abs(pens[k][S] - count) > 1e-9:
                    return False, dict(reason="the level-k penalty is not sum_T c_T C(|T and S|, k)/C(m, k)", k=k)
                if pens[k][S] < env[S] - 1e-9:
                    return False, dict(reason="the shares of a level do not cover the constants of the changed set", k=k, S=sorted(S))
                if k < m and pens[k + 1][S] > pens[k][S] + 1e-9:
                    return False, dict(reason="the penalty of level k + 1 exceeds that of level k", k=k, S=sorted(S))
                if k < m and S != full and len(S) >= 1 and pens[k + 1][S] < pens[k][S] - 1e-9:
                    stats["strict_levels"] += 1
            if S == full and any(abs(pens[k][S] - gamma_all) > 1e-9 for k in range(m + 1)):
                return False, dict(reason="at the set of all sites the levels do not coincide")
        # (b) a window on level k + 1, pushed down to level k
        for k in (1, 2):
            width = int(rng.integers(1, 3))
            in_win = lambda K: max(K) - min(K) <= width
            pushed = {K: sum(v for K2, v in shares[k + 1].items() if set(K) <= set(K2) and not in_win(K2)) / (k + 1) for K in shares[k]}
            for S in allS:
                pw = sum(v for K2, v in shares[k + 1].items() if set(K2) <= S and in_win(K2)) + sum(v for K, v in pushed.items() if set(K) <= S)
                if pw < pens[k + 1][S] - 1e-9 or pw > pens[k][S] + 1e-9:
                    return False, dict(reason="the window form is not between the two levels", k=k, S=sorted(S))
                if pens[k + 1][S] + 1e-9 < pw < pens[k][S] - 1e-9:
                    stats["strict_window"] += 1
        # (c), (d) allocations to sites (k = 1) and a product law
        p = rng.uniform(0.02, 0.5, n)
        law = sl_law(n, p)

        def random_alloc():
            lam = {}
            for T in subs_m:
                w = rng.dirichlet(np.ones(m))
                for i, wi in zip(sorted(T), w):
                    lam[(T, frozenset([i]))] = c[T] * float(wi)
            return lam

        lam0, lam1 = random_alloc(), random_alloc()
        mid = {key: 0.5 * (lam0[key] + lam1[key]) for key in lam0}
        p0, p1, pm = sl_alloc_pen(n, lam0), sl_alloc_pen(n, lam1), sl_alloc_pen(n, mid)
        if any(p0[S] < env[S] - 1e-9 for S in allS):
            return False, dict(reason="an allocation with sum_K lam_{T,K} = c_T does not cover")
        U0, U1, Um = sl_upper(law, p0), sl_upper(law, p1), sl_upper(law, pm)
        L0, L1, Lm = sl_lower(law, p0), sl_lower(law, p1), sl_lower(law, pm)
        if Um > 0.5 * (U0 + U1) + 1e-12:
            return False, dict(reason="the upper end is not convex in the allocation", Um=Um, U0=U0, U1=U1)
        if Lm < 0.5 * (L0 + L1) - 1e-12:
            return False, dict(reason="the lower end is not concave in the allocation", Lm=Lm, L0=L0, L1=L1)
        stats["convex_strict"] += int(Um < 0.5 * (U0 + U1) - 1e-9)
        stats["concave_strict"] += int(Lm > 0.5 * (L0 + L1) + 1e-9)
        # the gradient: d/d lam_{T,i} of the upper end is the tilted probability that i is changed
        zt = sum(law[S] * math.exp(p0[S]) for S in allS)
        key = (subs_m[0], frozenset([min(subs_m[0])]))
        i0 = min(subs_m[0])
        grad = sum(law[S] * math.exp(p0[S]) for S in allS if i0 in S) / zt
        hstep = 1e-6
        lam_h = dict(lam0)
        lam_h[key] += hstep
        if abs((sl_upper(law, sl_alloc_pen(n, lam_h)) - U0) / hstep - grad) > 1e-4:
            return False, dict(reason="the derivative of the upper end is not the tilted probability of the charged site")
        stats["cases"] += 1
    # an exchangeable instance: equal constants, equal probabilities - the upper end is least at equal shares
    n, m = 5, 3
    subs_m = [frozenset(T) for T in itertools.combinations(range(n), m)]
    c = {T: 0.6 for T in subs_m}
    law = sl_law(n, [0.2] * n)
    uniform = {(T, frozenset([i])): c[T] / m for T in subs_m for i in T}
    U_uni = sl_upper(law, sl_alloc_pen(n, uniform))
    for _ in range(40):
        lam = {}
        for T in subs_m:
            w = rng.dirichlet(np.ones(m) * float(rng.choice([0.2, 1.0, 5.0])))
            for i, wi in zip(sorted(T), w):
                lam[(T, frozenset([i]))] = c[T] * float(wi)
        if sl_upper(law, sl_alloc_pen(n, lam)) < U_uni - 1e-12:
            return False, dict(reason="on an exchangeable instance an allocation beats equal shares at the upper end")
    # the lower end is least at a vertex: four sites, triples, all 81 vertices
    n, m = 4, 3
    subs_m = [frozenset(T) for T in itertools.combinations(range(n), m)]
    c = {T: float(rng.uniform(0.3, 1.5)) for T in subs_m}
    law = sl_law(n, rng.uniform(0.1, 0.5, n))
    best_vertex = math.inf
    for choice in itertools.product(*[sorted(T) for T in subs_m]):
        lam = {(T, frozenset([i])): (c[T] if i == ch else 0.0) for T, ch in zip(subs_m, choice) for i in T}
        best_vertex = min(best_vertex, sl_lower(law, sl_alloc_pen(n, lam)))
    uniform = {(T, frozenset([i])): c[T] / m for T in subs_m for i in T}
    L_uni = sl_lower(law, sl_alloc_pen(n, uniform))
    if best_vertex > L_uni + 1e-12:
        return False, dict(reason="the lower end at equal shares is below every vertex")
    stats["vertex_below_uniform"] += int(best_vertex < L_uni - 1e-9)
    for _ in range(40):
        lam = {}
        for T in subs_m:
            w = rng.dirichlet(np.ones(m))
            for i, wi in zip(sorted(T), w):
                lam[(T, frozenset([i]))] = c[T] * float(wi)
        if sl_lower(law, sl_alloc_pen(n, lam)) < best_vertex - 1e-12:
            return False, dict(reason="an interior allocation has a lower end below every vertex")
    # (e) four nearly frozen sites among six, and a homogeneous instance: charge every constant to its most frozen site
    n, m = 6, 3
    subs_m = [frozenset(T) for T in itertools.combinations(range(n), m)]
    for p, cval, hetero in (([0.01, 0.01, 0.01, 0.01, 0.3, 0.3], 0.1, True), ([0.05] * 6, 0.5, False)):
        c = {T: cval for T in subs_m}
        law = sl_law(n, p)
        rank = sorted(range(n), key=lambda i: (p[i], i))            # most frozen first
        pos = {i: r for r, i in enumerate(rank)}
        greedy = {(T, frozenset([i])): (c[T] if i == min(T, key=lambda j: pos[j]) else 0.0) for T in subs_m for i in T}
        uniform = {(T, frozenset([i])): c[T] / m for T in subs_m for i in T}
        gam = lambda R: sum(v for T, v in c.items() if T <= R)
        for i in range(n):
            at_least = frozenset(j for j in range(n) if pos[j] >= pos[i])
            closed = gam(at_least) - gam(at_least - {i})
            direct = sum(v for (T, K), v in greedy.items() if K == frozenset([i]))
            if abs(closed - direct) > 1e-12:
                return False, dict(reason="the site penalties of the greedy allocation are not differences of the closed form on nested sets of sites", i=i)
        pg, pu = sl_alloc_pen(n, greedy), sl_alloc_pen(n, uniform)
        Ug, Uu, Lg2, Lu = sl_upper(law, pg), sl_upper(law, pu), sl_lower(law, pg), sl_lower(law, pu)
        first_g = sum(law[S] * pg[S] for S in law)
        first_u = sum(law[S] * pu[S] for S in law)
        if abs(first_g - sum(c[T] * min(p[j] for j in T) for T in subs_m)) > 1e-12 or first_g > first_u + 1e-12:
            return False, dict(reason="the first-order cost of the greedy allocation is not sum_T c_T min_i p_i, or exceeds that of equal shares")
        if hetero:
            stats["greedy_gain_upper"], stats["greedy_gain_lower"] = Uu / Ug, Lu / Lg2
        else:
            stats["two_ends_differ"] = int(Ug > Uu + 1e-9 and Lg2 < Lu - 1e-9)
    # (f) beyond first order (Proposition 11.18f(c'), (c''))
    sp = lambda z: math.log1p(math.exp(z))
    stats.update(site_forms=0, lower_ratio=0.0, waterfill=0, waterfill_strict=0, greedy_core=0, greedy_unsorted_fails=0)
    for _ in range(12):
        n = 5
        p = rng.uniform(0.02, 0.6, n)
        gs = rng.exponential(1.0, n) * (rng.random(n) < 0.8)
        law = sl_law(n, p)
        pen = {S: sum(gs[i] for i in S) for S in law}
        f = np.log((1 - p) / p)
        U_closed = sum(sp(gs[i] - f[i]) - sp(-f[i]) for i in range(n))
        L_closed = sum(sp(-f[i]) - sp(-f[i] - gs[i]) for i in range(n))
        if abs(U_closed - sl_upper(law, pen)) > 1e-10 or abs(L_closed - sl_lower(law, pen)) > 1e-10:
            return False, dict(reason="independent sites: the two ends are not the softplus sums in f_i -+ gamma_i")
        for i in range(n):
            g_, p_ = float(gs[i]), float(p[i])
            up_i = math.log1p(p_ * math.expm1(g_))
            lo_i = -math.log(1 - p_ + p_ * math.exp(-g_))
            if not (max(p_ * g_, g_ - math.log(1 / p_)) - 1e-12 <= up_i <= p_ * math.expm1(g_) + 1e-12) \
                    or lo_i > min(p_ * g_, -math.log(1 - p_)) + 1e-12:
                return False, dict(reason="independent sites: the bounds for what one site pays at either end", p=p_, gamma=g_)
        stats["site_forms"] += 1
    n, m = 5, 3
    subs_m = [frozenset(T) for T in itertools.combinations(range(n), m)]
    allS = sl_subsets(n)

    def water(pm, Gam):
        lo, hi = min(pm), max(pm) * math.exp(Gam) + 1.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if sum(max(0.0, math.log(mid / q_)) for q_ in pm) < Gam:
                lo = mid
            else:
                hi = mid
        lam_ = 0.5 * (lo + hi)
        return lam_, [max(0.0, math.log(lam_ / q_)) for q_ in pm]

    for it in range(10):
        c = {T: float(rng.exponential(0.7)) for T in subs_m}
        if it % 2:
            law = sl_law(n, rng.uniform(0.02, 0.5, n))
        else:
            law = {S: float(w_) for S, w_ in zip(allS, rng.dirichlet(np.full(len(allS), 0.3)))}     # any law, not a product
        for k in (1, 2):
            equal = {(T, frozenset(K)): c[T] / math.comb(m, k) for T in subs_m for K in itertools.combinations(sorted(T), k)}
            L_eq = sl_lower(law, sl_alloc_pen(n, equal))
            for _ in range(6):
                lam = {}
                for T in subs_m:
                    Ks = [frozenset(K) for K in itertools.combinations(sorted(T), k)]
                    for K, wi in zip(Ks, rng.dirichlet(np.full(len(Ks), 0.2))):
                        lam[(T, K)] = c[T] * float(wi)
                L_lam = sl_lower(law, sl_alloc_pen(n, lam))
                if L_lam > math.comb(m, k) * L_eq + 1e-12:
                    return False, dict(reason="the lower end of an allocation exceeds C(m, k) times that of equal shares", k=k)
                stats["lower_ratio"] = max(stats["lower_ratio"], L_lam / L_eq)
        # the water-filling bound: no covering vector of site penalties has a smaller upper end
        pm = [sum(law[S] for S in allS if i in S) for i in range(n)]
        Gam = sum(c.values())
        lam_w, g_w = water(pm, Gam)
        floor_w = math.log1p(sum(max(0.0, lam_w - q_) for q_ in pm))
        if abs(sum(g_w) - Gam) > 1e-9 or abs(sum(q_ * math.expm1(g_) for q_, g_ in zip(pm, g_w)) - sum(max(0.0, lam_w - q_) for q_ in pm)) > 1e-9:
            return False, dict(reason="the water-filling vector does not sum to Gamma, or its first-order cost is not sum (lam - p_i)^+")
        for _ in range(8):
            lam = {}
            for T in subs_m:
                for i, wi in zip(sorted(T), rng.dirichlet(np.full(m, 0.3))):
                    lam[(T, frozenset([i]))] = c[T] * float(wi)
            gvec = [sum(v for (T, K), v in lam.items() if K == frozenset([i])) for i in range(n)]
            Uv = sl_upper(law, sl_alloc_pen(n, lam))
            mid_b = math.log1p(sum(q_ * math.expm1(g_) for q_, g_ in zip(pm, gvec)))
            if Uv < mid_b - 1e-12 or mid_b < floor_w - 1e-9:
                return False, dict(reason="a covering vector of site penalties has an upper end below the water-filling bound",
                                   U=Uv, middle=mid_b, floor=floor_w)
            stats["waterfill"] += 1
            stats["waterfill_strict"] += int(Uv > floor_w + 1e-9)
    # the greedy vertex (CoreGreedy.lean): among vectors that cover the nested sets of an ordering by nondecreasing p the
    # marginal vector has the least first-order cost; for an ordering that is not by p it need not
    for _ in range(40):
        n = int(rng.integers(2, 8))
        G = np.append(rng.normal(0, 1, n), 0.0)                    # G_j = Gamma(R_j), G_n = 0; no sign or monotonicity is used
        gstar = G[:-1] - G[1:]
        tails = np.append(rng.exponential(0.5, n) * (rng.random(n) < 0.7), 0.0)
        gcov = gstar + (tails[:-1] - tails[1:])                    # tail sums of gcov exceed G_j by tails_j >= 0: it covers
        if any(G[j] > gcov[j:].sum() + 1e-12 for j in range(n)):
            return False, dict(reason="harness: the covering vector does not cover")
        p_sorted = np.sort(rng.uniform(0, 1, n))
        if float(p_sorted @ gstar) > float(p_sorted @ gcov) + 1e-12:
            return False, dict(reason="the marginal vector of the ordering by nondecreasing p does not have the least first-order cost")
        stats["greedy_core"] += 1
        stats["greedy_unsorted_fails"] += int(float(p_sorted[::-1] @ gstar) > float(p_sorted[::-1] @ gcov) + 1e-9)
    # the pair level for a product law (an answer to the division's question A17-T3): the least probable pair of T is its
    # two most frozen sites, and the pair penalties of that vertex are second differences of Gamma on sets of sites
    for _ in range(6):
        n, m = 6, int(rng.integers(3, 5))
        subs_m = [frozenset(T) for T in itertools.combinations(range(n), m)]
        c = {T: float(rng.exponential(0.7)) for T in subs_m}
        p = np.sort(rng.uniform(0.02, 0.6, n))                      # sites numbered most frozen first
        gam = lambda R: sum(v for T, v in c.items() if T <= R)
        first_order = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                after = frozenset(range(j + 1, n))
                closed = gam(after | {i, j}) - gam(after | {i}) - gam(after | {j}) + gam(after)
                direct = sum(v for T, v in c.items() if sorted(T)[:2] == [i, j])
                if abs(closed - direct) > 1e-10:
                    return False, dict(reason="pair level: the penalty of the two most frozen sites is not the second difference of Gamma", i=i, j=j)
                first_order += direct * p[i] * p[j]
        lp_min = sum(v * min(p[a] * p[b] for a, b in itertools.combinations(sorted(T), 2)) for T, v in c.items())
        if abs(first_order - lp_min) > 1e-10:
            return False, dict(reason="pair level, product law: the two most frozen sites are not the least probable pair")
        stats["pair_level"] = stats.get("pair_level", 0) + 1
    # ties (review SCI-REV-0015, m4): four tied frozen sites among six, equal constants on the triples
    n, m = 6, 3
    subs_m = [frozenset(T) for T in itertools.combinations(range(n), m)]
    p = [0.01, 0.01, 0.01, 0.01, 0.3, 0.3]
    c = {T: 0.1 for T in subs_m}
    law = sl_law(n, p)
    gam = lambda R: sum(v for T, v in c.items() if T <= R)
    tie = [gam(frozenset(j for j in range(n) if p[j] >= p[i])) - gam(frozenset(j for j in range(n) if p[j] >= p[i]) - {i}) for i in range(n)]
    pen_tie = {S: sum(tie[i] for i in S) for S in law}
    if np.abs(np.array(tie) - np.array([1, 1, 1, 1, 0, 0])).max() > 1e-12 or abs(gam(frozenset(range(n))) - 2.0) > 1e-12 \
            or abs(sl_upper(law, pen_tie) - 0.068) > 5e-4 or abs(sl_lower(law, pen_tie) - 0.025) > 5e-4:
        return False, dict(reason="ties: the formula read with ties should charge (1, 1, 1, 1, 0, 0), sum 4 against Gamma = 2")
    frozen = {0, 1, 2, 3}
    share = {(T, frozenset([i])): (c[T] / len(T & frozen) if i in frozen else 0.0) for T in subs_m for i in T}
    pos = {i: r for r, i in enumerate(sorted(range(n), key=lambda i: (p[i], i)))}
    vertex = {(T, frozenset([i])): (c[T] if i == min(T, key=lambda j: pos[j]) else 0.0) for T in subs_m for i in T}
    p_sh, p_vx = sl_alloc_pen(n, share), sl_alloc_pen(n, vertex)
    U_sh, U_vx, L_sh, L_vx = sl_upper(law, p_sh), sl_upper(law, p_vx), sl_lower(law, p_sh), sl_lower(law, p_vx)
    zt = sum(law[S] * math.exp(p_sh[S]) for S in law)
    tilt = [sum(law[S] * math.exp(p_sh[S]) for S in law if i in S) / zt for i in range(n)]
    if abs(U_sh - 0.0259) > 5e-5 or abs(U_vx - 0.0298) > 5e-5 or not (U_sh < U_vx and L_vx < L_sh) \
            or max(tilt[:4]) - min(tilt[:4]) > 1e-12 or max(tilt[:4]) >= min(tilt[4:]):
        return False, dict(reason="ties: the upper end should be least when the tied sites share (first-order condition of (b)), the lower end at the vertex",
                           U_share=U_sh, U_vertex=U_vx, L_share=L_sh, L_vertex=L_vx)
    stats["tie_upper"], stats["tie_vertex"] = U_sh, U_vx
    # no bound of the upper end of a vertex by a multiple of that of equal shares: a tied pair with one constant 2 ln(1/p)
    ratios = []
    for pp in (1e-3, 1e-6):
        cc = 2 * math.log(1 / pp)
        ratios.append(math.log1p(pp * math.expm1(cc)) / (2 * math.log1p(pp * math.expm1(cc / 2))))
    if not (4.9 < ratios[0] < 5.1 and 9.9 < ratios[1] < 10.1):
        return False, dict(reason="the tied pair: the ratio of the upper ends should grow like ln(1/p)/(2 ln 2)", ratios=ratios)
    if not (stats["cases"] >= 8 and stats["strict_levels"] > 50 and stats["strict_window"] > 5 and stats["convex_strict"] >= 4
            and stats["concave_strict"] >= 4 and stats["vertex_below_uniform"] == 1 and 7.5 < stats["greedy_gain_upper"] < 8.5
            and 12.5 < stats["greedy_gain_lower"] < 13.5 and stats["two_ends_differ"] == 1 and stats["site_forms"] >= 12
            and stats["lower_ratio"] > 1.05 and stats["waterfill"] >= 80 and stats["waterfill_strict"] >= 40
            and stats["greedy_core"] >= 40 and stats["greedy_unsorted_fails"] >= 5):
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


def to_mixed_diff(g, idx, z, T, y):
    """Delta_T g(z; y_T): the sum over U inside T of (-1)^(|T| - |U|) g(z with the sites of U set to their states in y)"""
    T = list(T)
    tot = 0.0
    for r in range(len(T) + 1):
        for U in itertools.combinations(T, r):
            x = list(z)
            for i in U:
                x[i] = y[i]
            tot += (-1) ** (len(T) - r) * g[idx[tuple(x)]]
    return tot


def to_interp(g, idx, x0, y, m):
    """anchored interpolant of order m - 1: the mixed differences at the reference over the subsets of fewer than m changed sites"""
    S = [i for i in range(len(y)) if y[i] != x0[i]]
    return sum(to_mixed_diff(g, idx, x0, U, y) for r in range(min(m, len(S) + 1)) for U in itertools.combinations(S, r))


def to_base(x0, y, T, rank):
    """base point of the remainder term of T for the order with ranks rank[i]: the states of y at the changed sites that
    precede every site of T, the reference elsewhere"""
    first = min(rank[t] for t in T)
    return tuple(y[i] if (y[i] != x0[i] and rank[i] < first) else x0[i] for i in range(len(y)))


def to_host_constants(g, idx, ks, x0, m, free_of):
    """c_T = max |Delta_T g(z; y_T)| over the target states and over the base points z that are at the reference on T and
    everywhere except on the sites free_of(T)"""
    n = len(ks)
    out = {}
    for T in itertools.combinations(range(n), m):
        free = free_of(T)
        best = 0.0
        for zf in itertools.product(*[range(ks[i]) for i in free]):
            z = list(x0)
            for i, v in zip(free, zf):
                z[i] = v
            for yT in itertools.product(*[range(1, ks[i]) for i in T]):
                y = list(x0)
                for i, v in zip(T, yT):
                    y[i] = v
                best = max(best, abs(to_mixed_diff(g, idx, z, T, y)))
        out[T] = best
    return out


@conjecture("XI.24 Every term in its own order of the sites, and the anchored split of a pair table (theory report Theorem 11.18d(a''), (d'); TermOrders.lean; the statements are the Scientific Discovery Division's, workstream P8 and SCI-MSG-0027, requests P8-T1 and A18-T1).  (a) For g = sum of terms g_t on a product of finite sets, with a separate linear order of the sites for every term: g(y) - I_{m-1} g(y) = sum_t sum over the m-subsets T of the changed sites of Delta_T g_t at the base point of the order of t; (b) if the order of a term puts a set of at most m hosts last, every host outside T is at the reference in the base point of T, and with m + 1 hosts one of them is not; (c) hence the remainder is at most the sum of constants that bound the mixed differences at base points that are at the reference on T and at the hosts outside T - attained with ratio one by products of off-anchor indicators that contain the hosts - while three variants are false on that family: the anchor context alone, m + 1 hosts, and the roles of hosts and other sites exchanged; (d) for a pair table P with anchors a, b: A(x) = P(x, b), B(y) = P(a, y) - P(a, b), D = P - A - B vanishes on the anchor row and column, A + B + min_y D <= P <= A + B + max_y D, exactly on the anchor row, where the split by column means loses the range of the centred anchor row")
def t_term_orders(rng, trials):
    stats = dict(identity=0, hosts_anchor=0, host_moves=0, bound=0, bound_tight=0, ctrl_anchor=0, ctrl_hosts=0, ctrl_swap=0,
                 split=0, colmeans_loss=0)
    for it in range(max(24, trials // 16)):
        n = int(rng.integers(3, 5))
        ks = [int(rng.integers(2, 4)) for _ in range(n)]
        confs = list(itertools.product(*[range(k) for k in ks]))
        idx = {x: t for t, x in enumerate(confs)}
        x0 = tuple([0] * n)
        m = int(rng.integers(1, n + 1))
        # (a) the identity, random tables, a random order for every term
        nt = int(rng.integers(1, 4))
        tabs = [rng.normal(0, 1, len(confs)) for _ in range(nt)]
        ranks = []
        for _ in range(nt):
            perm = list(rng.permutation(n))
            ranks.append({int(site): r for r, site in enumerate(perm)})
        total = np.sum(tabs, axis=0)
        for y in confs:
            S = [i for i in range(n) if y[i] != 0]
            lhs = float(total[idx[y]]) - to_interp(total, idx, x0, y, m)
            rhs = sum(to_mixed_diff(tabs[t], idx, to_base(x0, y, T, ranks[t]), T, y)
                      for t in range(nt) for T in itertools.combinations(S, m))
            if abs(lhs - rhs) > 1e-9:
                return False, dict(reason="the remainder identity with a separate order for every term", n=n, m=m, y=y, lhs=lhs, rhs=rhs)
            stats["identity"] += 1
        # (b) hosts that are last stay at the reference; with m + 1 hosts one of them moves
        for hsize in (int(rng.integers(0, m + 1)), m + 1):
            if hsize > n:
                continue
            H = [int(i) for i in rng.choice(n, size=hsize, replace=False)]
            others = [i for i in range(n) if i not in H]
            order = [int(i) for i in rng.permutation(others)] + [int(i) for i in rng.permutation(H)] if others else \
                [int(i) for i in rng.permutation(H)]
            rank = {site: r for r, site in enumerate(order)}
            moved = False
            for y in confs:
                S = [i for i in range(n) if y[i] != 0]
                for T in itertools.combinations(S, m):
                    base = to_base(x0, y, T, rank)
                    if any(base[h] != 0 for h in H if h not in T):
                        moved = True
            if hsize <= m and moved:
                return False, dict(reason="a host that the order puts last left the reference in a base point", n=n, m=m, hosts=H)
            if hsize <= m:
                stats["hosts_anchor"] += 1
            elif moved:
                stats["host_moves"] += 1
            elif all(k > 1 for k in ks):
                return False, dict(reason="with m + 1 hosts no host left the reference", n=n, m=m, hosts=H)
        # (c) the bound with host-anchored constants: products of off-anchor indicators that contain the hosts, and a
        #     random table with arbitrary hosts
        terms = []
        for _ in range(2):
            hsize = int(rng.integers(0, m + 1))
            H = sorted(int(i) for i in rng.choice(n, size=hsize, replace=False))
            usize = int(rng.integers(max(hsize, 1), n + 1))
            U = sorted(set(H) | set(int(i) for i in rng.choice([i for i in range(n) if i not in H], size=usize - hsize, replace=False))) \
                if usize > hsize else list(H)
            cval = float(rng.choice([-1, 1]) * rng.uniform(0.5, 2.0))
            g = np.array([cval if all(x[i] != 0 for i in U) else 0.0 for x in confs])
            terms.append((g, H, U))
        Hr = sorted(int(i) for i in rng.choice(n, size=int(rng.integers(0, m + 1)), replace=False))
        terms.append((rng.normal(0, 1, len(confs)), Hr, None))
        consts = [to_host_constants(g, idx, ks, x0, m, lambda T, H=H: [i for i in range(n) if i not in T and i not in H])
                  for g, H, U in terms]
        total = np.sum([g for g, H, U in terms], axis=0)
        for y in confs:
            S = [i for i in range(n) if y[i] != 0]
            rem = abs(float(total[idx[y]]) - to_interp(total, idx, x0, y, m))
            bnd = sum(c[T] for c in consts for T in itertools.combinations(S, m))
            if rem > bnd + 1e-9:
                return False, dict(reason="the remainder exceeds the sum of the host-anchored constants", n=n, m=m, y=y, rem=rem, bound=bnd)
            stats["bound"] += 1
        # one product term alone: the bound is attained when the term has exactly m sites, and three variants fail
        g, H, U = terms[0]
        c_host = consts[0]
        c_anchor = to_host_constants(g, idx, ks, x0, m, lambda T: [])
        c_swap = to_host_constants(g, idx, ks, x0, m, lambda T: [i for i in H if i not in T])
        for y in confs:
            S = [i for i in range(n) if y[i] != 0]
            rem = abs(float(g[idx[y]]) - to_interp(g, idx, x0, y, m))
            b_host = sum(c_host[T] for T in itertools.combinations(S, m))
            if rem > 1e-9 and abs(rem - b_host) < 1e-9:
                stats["bound_tight"] += 1
            stats["ctrl_anchor"] += int(rem > sum(c_anchor[T] for T in itertools.combinations(S, m)) + 1e-9)
            stats["ctrl_swap"] += int(rem > sum(c_swap[T] for T in itertools.combinations(S, m)) + 1e-9)
        if m + 1 <= n:
            # m + 1 hosts inside the term: every host-anchored constant vanishes and the remainder does not
            Hbig = [int(i) for i in rng.choice(n, size=m + 1, replace=False)]
            gbig = np.array([1.0 if all(x[i] != 0 for i in Hbig) else 0.0 for x in confs])
            c_big = to_host_constants(gbig, idx, ks, x0, m, lambda T: [i for i in range(n) if i not in T and i not in Hbig])
            y = tuple(1 for _ in range(n))
            rem = abs(float(gbig[idx[y]]) - to_interp(gbig, idx, x0, y, m))
            if max(c_big.values()) < 1e-12 and rem > 0.5:
                stats["ctrl_hosts"] += 1
            else:
                return False, dict(reason="m + 1 hosts: the host-anchored constants should vanish while the remainder is one", n=n, m=m)
        # (d) the anchored split of a pair table
        kx, ky = int(rng.integers(2, 6)), int(rng.integers(2, 6))
        Pt = rng.normal(0, 1, (kx, ky))
        a, b = int(rng.integers(kx)), int(rng.integers(ky))
        A = Pt[:, b]
        B = Pt[a, :] - Pt[a, b]
        D = Pt - A[:, None] - B[None, :]
        lo, hi = D.min(axis=1), D.max(axis=1)
        if np.abs(D[a, :]).max() > 1e-12 or np.abs(D[:, b]).max() > 1e-12:
            return False, dict(reason="the remainder of the anchored split does not vanish on the anchor row and column")
        if (A[:, None] + B[None, :] + lo[:, None] > Pt + 1e-12).any() or (Pt > A[:, None] + B[None, :] + hi[:, None] + 1e-12).any() \
                or abs(lo[a]) > 1e-12 or abs(hi[a]) > 1e-12:
            return False, dict(reason="the anchored split is not a sandwich, or is not exact on the anchor row")
        stats["split"] += 1
        cm = Pt.mean(axis=0)                                        # the split by column means: b(y) plus row extrema of P - b
        stats["colmeans_loss"] += int(np.ptp(Pt[a, :] - cm) > 1e-6)
    if not (stats["identity"] > 100 and stats["hosts_anchor"] >= 10 and stats["host_moves"] >= 3 and stats["bound"] > 100
            and stats["bound_tight"] >= 3 and stats["ctrl_anchor"] >= 3 and stats["ctrl_hosts"] >= 3 and stats["ctrl_swap"] >= 3
            and stats["split"] >= 10 and stats["colmeans_loss"] >= 8):
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


def sb_max(M, w):
    """the least sign-blind bound of the quadratic form: max over sign patterns s of |(s w)^T M (s w)| (exact, by enumeration)"""
    N = len(w)
    best = 0.0
    for mask in range(1 << (N - 1)):                               # a global sign does not matter
        sgn = np.array([1.0 if (mask >> i) & 1 == 0 else -1.0 for i in range(N - 1)] + [1.0])
        v = sgn * w
        best = max(best, abs(float(v @ M @ v)))
    return best


@conjecture("XI.25 The sign-blind loss of a quadratic form in the charges, for a cluster with a net charge (theory report section 12, item 13(a); an answer to the Scientific Discovery Division's question P8-T2, SCI-MSG-0027).  For a symmetric kernel M, charges q with magnitudes w, t = q^T M q and SB = max over sign patterns of |(s w)^T M (s w)| - the least bound that sees the charges through their magnitudes only: with any reference value mbar, e = max |M_ij - mbar| and R = sum |q| / |sum q|, (i) SB <= (|mbar| + e)(sum w)^2 and |t| >= |mbar| (sum q)^2 - e (sum w)^2, so that (ii) SB <= (1 + rho)/(1 - rho R^2) R^2 |t| whenever rho R^2 < 1, rho = e/|mbar|; (iii) for a constant kernel SB = R^2 |t| exactly, so the square of R cannot be replaced by a smaller power; (iv) for two clusters and a bilinear form the loss is at most (1 + rho)/(1 - rho R_a R_b) R_a R_b; (v) without a bound on the variation of the kernel there is no such statement, even for charges of one sign: M = [[1, -1], [-1, 1]], q = (1, 1) has t = 0 and SB = 4")
def t_sign_blind(rng, trials):
    stats = dict(cases=0, tight=0.0, constant=0, bilinear=0, bilinear_tight=0.0, power_one_fails=0)
    for _ in range(max(40, trials // 4)):
        N = int(rng.integers(2, 9))
        mbar = float(rng.choice([-1, 1]) * rng.uniform(0.5, 2.0))
        q = rng.uniform(0.05, 1.0, N) * np.where(rng.random(N) < 0.75, 1.0, -1.0)
        if abs(q.sum()) < 0.05:
            continue
        w = np.abs(q)
        R = float(w.sum() / abs(q.sum()))
        rho = float(rng.uniform(0.0, 0.9)) / R ** 2                # so that rho R^2 < 1
        E = rng.uniform(-1, 1, (N, N))
        E = (E + E.T) / 2
        E *= rho * abs(mbar) / np.abs(E).max()
        M = mbar + E
        t = float(q @ M @ q)
        SB = sb_max(M, w)
        e = float(np.abs(M - mbar).max())
        if SB > (abs(mbar) + e) * w.sum() ** 2 + 1e-9 or abs(t) < abs(mbar) * q.sum() ** 2 - e * w.sum() ** 2 - 1e-9:
            return False, dict(reason="the two elementary bounds for the sign-blind maximum and for the true value", N=N)
        factor = (1 + e / abs(mbar)) / (1 - (e / abs(mbar)) * R ** 2) * R ** 2
        if SB > factor * abs(t) + 1e-9:
            return False, dict(reason="the sign-blind bound exceeds (1 + rho)/(1 - rho R^2) R^2 times the true value", N=N, R=R,
                               rho=e / abs(mbar), SB=SB, t=t)
        stats["tight"] = max(stats["tight"], SB / (factor * abs(t)))
        stats["power_one_fails"] += int(SB > (1 + e / abs(mbar)) / (1 - (e / abs(mbar)) * R ** 2) * R * abs(t) + 1e-9)
        # (iii) the constant kernel: equality
        Mc = np.full((N, N), mbar)
        if abs(sb_max(Mc, w) - R ** 2 * abs(float(q @ Mc @ q))) > 1e-9 * (1 + R ** 2):
            return False, dict(reason="constant kernel: the sign-blind bound is not R^2 times the true value")
        stats["constant"] += 1
        # (iv) two clusters, a bilinear form q_a^T K q_b: the loss is at most (1 + rho)/(1 - rho R_a R_b) R_a R_b
        Na, Nb = int(rng.integers(1, 5)), int(rng.integers(1, 5))
        qa = rng.uniform(0.05, 1.0, Na) * np.where(rng.random(Na) < 0.75, 1.0, -1.0)
        qb = rng.uniform(0.05, 1.0, Nb) * np.where(rng.random(Nb) < 0.75, 1.0, -1.0)
        if abs(qa.sum()) < 0.05 or abs(qb.sum()) < 0.05:
            continue
        Ra, Rb = float(np.abs(qa).sum() / abs(qa.sum())), float(np.abs(qb).sum() / abs(qb.sum()))
        rho2 = float(rng.uniform(0.0, 0.9)) / (Ra * Rb)
        K = mbar * (1 + rho2 * rng.uniform(-1, 1, (Na, Nb)))
        tb = float(qa @ K @ qb)
        SBb = max(abs(float((np.array(sa) * np.abs(qa)) @ K @ (np.array(sb_) * np.abs(qb))))
                  for sa in itertools.product((1.0, -1.0), repeat=Na) for sb_ in itertools.product((1.0, -1.0), repeat=Nb))
        e2 = float(np.abs(K - mbar).max()) / abs(mbar)
        f2 = (1 + e2) / (1 - e2 * Ra * Rb) * Ra * Rb
        if SBb > f2 * abs(tb) + 1e-9:
            return False, dict(reason="two clusters: the sign-blind bound exceeds (1 + rho)/(1 - rho R_a R_b) R_a R_b times the true value")
        stats["bilinear"] += 1
        stats["bilinear_tight"] = max(stats["bilinear_tight"], SBb / (f2 * abs(tb)))
        stats["cases"] += 1
    # (v) no statement without a bound on the variation of the kernel, even for charges of one sign
    Mx = np.array([[1.0, -1.0], [-1.0, 1.0]])
    qx = np.array([1.0, 1.0])
    if abs(float(qx @ Mx @ qx)) > 1e-12 or abs(sb_max(Mx, qx) - 4.0) > 1e-12:
        return False, dict(reason="the counter-instance: t should vanish and the sign-blind maximum be 4")
    if not (stats["cases"] >= 30 and stats["tight"] > 0.5 and stats["constant"] >= 30 and stats["bilinear"] >= 30
            and stats["power_one_fails"] >= 5):
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


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

def lc_site_canon(sites):
    """Canonical form of a finite set of lattice points under the 8 symmetries of the square lattice and translations."""
    best = None
    for sx, sy, sw in itertools.product((1, -1), (1, -1), (0, 1)):
        pts = [((y if sw else x) * sx, (x if sw else y) * sy) for x, y in sites]
        mx, my = min(p[0] for p in pts), min(p[1] for p in pts)
        key = tuple(sorted((p[0] - mx, p[1] - my) for p in pts))
        if best is None or key < best:
            best = key
    return best


def lc_sqdist_multiset(sites):
    return tuple(sorted((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for p, q in itertools.combinations(sites, 2)))


@conjecture("XIV.5 Scattering curves of one conformation are members of the pair-profile class (theory report Theorem 11.48(d); statement of the science division, SCI-REV-0006, Proposition A2.1; Scattering.lean): |sin t - t cos t| <= t^3/3 with the constant attained as t -> 0, hence s -> sinc(q sqrt s) is (q^2/6)-Lipschitz, and for two chains with equally many beads |I_x(q) - I_y(q)| <= (q^2/3) sum_k |s^x_(k) - s^y_(k)| (sorted squared distances of all pairs; the sorted matching is the best one), I_x(q) = N + 2 sum_pairs sinc(q r) the Debye intensity; the bound is attained in the limit q -> 0 against a straight rod.  Homometry: the 6-bead walks through (0,0),(0,1),(0,2),(1,2),(1,3),(2,3) and through (0,0),(0,1),(1,1),(1,2),(1,3),(2,3) have the squared distances 1^5 2^3 4 5^3 8 10 13, are not congruent and have identical curves; with 4 or 5 beads there is no such pair, with 6 beads exactly one (36 walk classes, 18 site sets, 17 distance multisets)")
def t_debye_profile_class(rng, trials):
    def sinc(t):
        t = np.asarray(t, dtype=float)
        small = np.abs(t) < 1e-9
        return np.where(small, 1.0, np.sin(t) / np.where(small, 1.0, t))

    stats = dict(pairs=0, worst_ratio=0.0, rod_ratio=0.0)
    # (1) the scalar inequality behind the Lipschitz constant, and its sharpness at the origin
    ts = np.linspace(1e-3, 300.0, 600001)
    ratio = np.abs(np.sin(ts) - ts * np.cos(ts)) / (ts ** 3 / 3)
    if ratio.max() > 1 + 1e-9:
        return False, dict(reason="|sin t - t cos t| exceeds t^3/3", worst=float(ratio.max()))
    if ratio[0] < 1 - 1e-5:
        return False, dict(reason="the constant 1/3 is not approached at the origin", value=float(ratio[0]))
    # (2) the Lipschitz constant q^2/6 in the squared distance, and its sharpness
    for _ in range(max(300, trials)):
        q = float(rng.uniform(0.01, 8.0))
        s1, s2 = (float(v) for v in rng.uniform(0.0, 60.0, size=2))
        if abs(float(sinc(q * math.sqrt(s1))) - float(sinc(q * math.sqrt(s2)))) > q * q / 6 * abs(s1 - s2) + 1e-12:
            return False, dict(reason="s -> sinc(q sqrt s) is not (q^2/6)-Lipschitz", q=q, s1=s1, s2=s2)
    if (1 - float(sinc(1e-2))) / (1e-4 / 6) < 1 - 1e-4:
        return False, dict(reason="the Lipschitz constant q^2/6 is not approached")

    def chain(n):
        v = rng.normal(size=(n - 1, 3))
        v /= np.linalg.norm(v, axis=1)[:, None]
        return np.vstack([np.zeros(3), np.cumsum(v, axis=0)])

    def sq(P):
        d = P[:, None, :] - P[None, :, :]
        iu = np.triu_indices(len(P), 1)
        return np.sort((d ** 2).sum(-1)[iu])

    def debye(n, s, q):
        return n + 2 * float(sinc(q * np.sqrt(s)).sum())

    # (3) freely jointed chains: the bound, and the sorted matching against a random matching
    for _ in range(max(150, trials)):
        n = int(rng.integers(4, 26))
        sx, sy = sq(chain(n)), sq(chain(n))
        W = float(np.abs(sx - sy).sum())
        if float(np.abs(sx - sy[rng.permutation(len(sy))]).sum()) < W - 1e-9:
            return False, dict(reason="a matching beats the sorted matching")
        for q in (0.02, 0.1, 0.5, 1.5, 4.0):
            lhs = abs(debye(n, sx, q) - debye(n, sy, q))
            if lhs > q * q / 3 * W * (1 + 1e-9) + 1e-9:
                return False, dict(reason="scattering bound violated", n=n, q=q, lhs=lhs, rhs=q * q / 3 * W)
            stats["worst_ratio"] = max(stats["worst_ratio"], lhs / (q * q / 3 * W))
            stats["pairs"] += 1
        # sharpness: a straight rod dominates every chain distance by distance, so the bound is attained as q -> 0
        rod = np.zeros((n, 3))
        rod[:, 0] = np.arange(n)
        sr = sq(rod)
        Wr = float(np.abs(sr - sy).sum())
        stats["rod_ratio"] = max(stats["rod_ratio"], abs(debye(n, sr, 0.01) - debye(n, sy, 0.01)) / (0.01 ** 2 / 3 * Wr))
    if stats["rod_ratio"] < 0.999:
        return False, dict(reason="the bound is not attained in the Guinier regime against a rod", ratio=stats["rod_ratio"])
    # (4) the smallest homometric pair of lattice chains
    A = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
    B = [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 3)]
    for wk in (A, B):
        if len(set(wk)) != 6 or any(abs(wk[i][0] - wk[i + 1][0]) + abs(wk[i][1] - wk[i + 1][1]) != 1 for i in range(5)):
            return False, dict(reason="not a self-avoiding walk")
    if lc_sqdist_multiset(A) != (1, 1, 1, 1, 1, 2, 2, 2, 4, 5, 5, 5, 8, 10, 13) or lc_sqdist_multiset(A) != lc_sqdist_multiset(B):
        return False, dict(reason="the two walks do not have the stated common multiset of squared distances")
    if lc_site_canon(A) == lc_site_canon(B):
        return False, dict(reason="the two site sets are congruent")
    DA = [[(p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for q in A] for p in A]
    DB = [[(p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for q in B] for p in B]
    if any(all(DA[i][j] == DB[pm[i]][pm[j]] for i in range(6) for j in range(i + 1, 6)) for pm in itertools.permutations(range(6))):
        return False, dict(reason="the two site sets are isometric under some bijection")
    sA, sB = np.array(lc_sqdist_multiset(A), dtype=float), np.array(lc_sqdist_multiset(B), dtype=float)
    if max(abs(debye(6, sA, q) - debye(6, sB, q)) for q in np.linspace(0.01, 20, 500)) > 1e-12:
        return False, dict(reason="homometric walks with different scattering curves")
    # (5) exhaustive: no homometric pair with 4 or 5 beads, exactly one group with 6
    expect = {4: (5, 4, 4, 0), 5: (None, None, None, 0), 6: (36, 18, 17, 1)}       # 4 beads: I, L, S, O tetrominoes
    for n in (4, 5, 6):
        walks = lc_square_lattice_walks(n)
        classes = {min(tuple(wk), tuple((x, -y) for x, y in wk)) for wk in walks}       # first step fixed: only the mirror remains
        sets = {lc_site_canon(wk) for wk in walks}
        by_ms = {}
        for st in sets:
            by_ms.setdefault(lc_sqdist_multiset(st), []).append(st)
        groups = sum(1 for v in by_ms.values() if len(v) > 1)
        got = (len(classes), len(sets), len(by_ms), groups)
        stats[f"n{n}"] = got
        if groups != expect[n][3] or (expect[n][0] is not None and got != expect[n]):
            return False, dict(reason="count of walk classes / site sets / distance multisets / homometric groups", n=n, got=got, expected=expect[n])
        if n == 6 and {st for v in by_ms.values() if len(v) > 1 for st in v} != {lc_site_canon(A), lc_site_canon(B)}:
            return False, dict(reason="the homometric group with 6 beads is not the stated pair")
    return True, stats


@conjecture("XIV.6 Residuals in a Hilbert ball: the hypercircle band (theory report Proposition 11.50a; HilbertBall.lean: cauchy_schwarz, hypercircle_band, ball_certificate_sound — the statement proposed by the Scientific Discovery Division, SCI-MSG-0007, X-T1): for a Gram kernel K on a finite set, a member g = K alpha and its interpolant s on an evaluated set A, (g(x) - s(x))^2 <= (|g|^2 - |s|^2) * P_lam(x)^2 for every rule lam supported on A, P_lam(x)^2 = K(x,x) - 2 sum_a lam_a K(a,x) + sum lam lam K the squared power function; with the optimal rule the bound is attained at every x by a member with the same data and the same norm; and a lower bound L <= F + s - r with r >= sqrt(|g|^2 - |s|^2) P is a lower bound of F + g")
def t_hilbert_ball(rng, trials):
    stats = dict(instances=0, points=0, worst=-math.inf, attained=0, sound=0)
    for _ in range(max(40, trials // 5)):
        N = int(rng.integers(6, 15)); m = int(rng.integers(3, N + 2))
        Phi = rng.normal(size=(m, N))
        K = Phi.T @ Phi + 1e-9 * np.eye(N)
        alpha = rng.normal(size=N)
        g = K @ alpha
        nA = int(rng.integers(1, min(m, N - 1) + 1))
        A = rng.choice(N, size=nA, replace=False)
        KAA = K[np.ix_(A, A)]
        if np.linalg.cond(KAA) > 1e8:
            continue
        gamma = np.linalg.solve(KAA, g[A])
        s = K[:, A] @ gamma
        if np.abs(s[A] - g[A]).max() > 1e-7 * (1 + np.abs(g).max()):
            return False, dict(reason="the interpolant does not reproduce the data")
        n2g, n2s = float(alpha @ K @ alpha), float(gamma @ KAA @ gamma)
        if n2s > n2g * (1 + 1e-9) + 1e-9:
            return False, dict(reason="the interpolant has a larger norm than the member", n2g=n2g, n2s=n2s)
        BA2 = max(n2g - n2s, 0.0)
        F = rng.normal(size=N)
        for x in range(N):
            lam_opt = np.linalg.solve(KAA, K[A, x])
            for lam in (lam_opt, lam_opt + 0.3 * rng.normal(size=nA), np.zeros(nA)):
                P2 = float(K[x, x] - 2 * lam @ K[A, x] + lam @ KAA @ lam)
                slack = BA2 * P2 - (g[x] - s[x]) ** 2
                stats["worst"] = max(stats["worst"], -slack / (1 + BA2 * P2))
                if slack < -1e-7 * (1 + BA2 * P2):
                    return False, dict(reason="the band is violated", x=x, lhs=(g[x] - s[x]) ** 2, rhs=BA2 * P2)
            P2 = float(K[x, x] - K[A, x] @ lam_opt)                          # the power function of the optimal rule
            if P2 > 1e-6 and BA2 > 1e-9:
                beta = np.zeros(N); beta[x] = 1.0; beta[A] -= lam_opt          # representer of the error functional
                gstar = s + math.sqrt(BA2 / P2) * (K @ beta)
                coef = np.zeros(N); coef[A] = gamma; coef = coef + math.sqrt(BA2 / P2) * beta
                if np.abs(gstar[A] - g[A]).max() > 1e-6 * (1 + np.abs(g).max()) or abs(float(coef @ K @ coef) - n2g) > 1e-6 * (1 + n2g):
                    return False, dict(reason="the extremal member does not have the data and the norm of the member", x=x)
                if abs((gstar[x] - s[x]) ** 2 - BA2 * P2) > 1e-6 * (1 + BA2 * P2):
                    return False, dict(reason="the band is not attained by the extremal member", x=x)
                stats["attained"] += 1
            stats["points"] += 1
        # soundness of a certified lower bound: r = sqrt(B_A^2) * P (optimal rule), L = min(F + s - r)
        Pv = np.array([max(float(K[x, x] - K[A, x] @ np.linalg.solve(KAA, K[A, x])), 0.0) for x in range(N)])
        L = float((F + s - np.sqrt(BA2 * Pv) - 1e-9).min())
        if L > float((F + g).min()) + 1e-7:
            return False, dict(reason="a certified lower bound exceeds the true minimum", L=L, true=float((F + g).min()))
        stats["sound"] += 1
        stats["instances"] += 1
    if stats["attained"] == 0 or stats["instances"] < 10:
        return False, dict(reason="cases not exercised", **stats)
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


@conjecture("XVI.4 Sample sizes of Algorithm 2L+ (remark after Theorem 11.56; a question of ENG-RES-0008): E_{r-1} <= e^{-u} E_r on exact tables, and with Delta = ceil(lambda/u), pi_ddag = 2^{-n_o} |B(n_o, r_dag - Delta)| and M_ddag = K/((1 - eta) pi_ddag) (K 2^{n_o}/(1 - eta) if r_dag < Delta) every sample of the algorithm is K or smaller than 2 max(e^lambda M_dag, M_ddag) -- in the runs, on outer landscapes 'plateau, then cone' with real fluctuations and three inner behaviours; the cap M_bar of the theorem is larger by a factor of order nu_0")
def t_two_level_plus_sample_sizes(rng, trials):
    # (i) the termwise inequality behind the argument
    for m, u in ((30, 0.5), (60, 1.0), (120, 2.0), (200, 0.3)):
        _, _, E, _ = ba_exact_tables(m, u, m)
        for r in range(1, m + 1):
            if E[r - 1] > math.exp(-u) * E[r] * (1 + 1e-12):
                return False, dict(reason="E_{r-1} <= e^{-u} E_r fails", m=m, u=u, r=r)
    # (ii) runs
    def plateau_cone(n_o, u, d0, frac):
        binom = [math.comb(n_o, j) for j in range(n_o + 1)]
        f = u * frac * np.maximum(np.arange(n_o + 1, dtype=float) - d0, 0.0)
        return np.exp(-f), np.array(binom, dtype=float) / 2 ** n_o, float(-f[0])
    pars = [dict(lam=0.5, eta=0.25, etap=0.5, theta=2.0, b=0.5, delta=0.01, nu1=1.0),
            dict(lam=1.0, eta=0.5, etap=1.0, theta=2.0, b=3.0, delta=0.01, nu1=1.0),
            dict(lam=0.5, eta=0.25, etap=0.5, theta=0.5, b=1.0, delta=0.01, nu1=1.0),
            dict(lam=1.0, eta=0.5, etap=1.0, theta=0.3, b=1.0, delta=0.01, nu1=1.0)]
    stats = dict(runs=0, samples_above_M_dag=0, largest_over_new_cap=0.0, largest_over_M_dag=0.0, smallest_old_cap_over_new=math.inf)
    cells = [(24, 0.5), (20, 1.0), (24, 1.0), (20, 2.0)] if trials < 100 else [(24, 0.5), (20, 1.0), (24, 1.0), (28, 1.0), (20, 2.0), (24, 2.0), (20, 0.5)]
    for n_o, u in cells:
        for par in pars:
            for d0 in (0, 1, 2, 4, 6):
                for frac in (1.0, 0.6):
                    vals, probs, lnw = plateau_cone(n_o, u, d0, frac)
                    mode = int(rng.integers(3))
                    run = ba_two_level_plus(rng, vals, probs, lnw, n_o, n_o + 2, u, par, mode, max_points=1_500_000)
                    if "error" in run:
                        if run["error"].startswith("sample beyond"):
                            continue
                        return False, dict(reason=run["error"], n_o=n_o, u=u, d0=d0)
                    C = run["C"]
                    Delta = math.ceil(par["lam"] / u - 1e-12)
                    if C["rdag"] >= Delta:
                        Mdd = C["K"] / ((1 - par["eta"]) * (C["ball"][C["rdag"] - Delta + 1] / 2 ** n_o))
                    else:
                        Mdd = C["K"] * 2 ** n_o / (1 - par["eta"]) * (1 + 1e-9)
                    cap = 2 * max(math.exp(par["lam"]) * C["Mdag"], Mdd)
                    stats["smallest_old_cap_over_new"] = min(stats["smallest_old_cap_over_new"], C["Mbar"] / cap)
                    for lv in run["levels"] + [run["last"]]:
                        if lv["M"] > C["K"]:
                            if lv["M"] >= cap:
                                return False, dict(reason="a sample is not smaller than 2 max(e^lambda M_dag, M_ddag)", n_o=n_o, u=u, d0=d0, frac=frac, par=par, M=lv["M"], cap=cap, M_dag=C["Mdag"])
                            stats["largest_over_new_cap"] = max(stats["largest_over_new_cap"], lv["M"] / cap)
                            stats["largest_over_M_dag"] = max(stats["largest_over_M_dag"], lv["M"] / C["Mdag"])
                            stats["samples_above_M_dag"] += lv["M"] > C["Mdag"]
                    stats["runs"] += 1
    if stats["runs"] < 40 or stats["samples_above_M_dag"] < 5 or stats["largest_over_new_cap"] < 0.4:
        return False, dict(reason="the test has no power", **stats)
    return True, stats


def q_rho(u, e1):
    """rho_e in [p_u, 1/2] with KL(rho_e || p_u) = min(e1, eps*)"""
    pu = 1 / (1 + math.exp(u))
    if e1 >= na_kl(0.5, pu):
        return 0.5
    lo, hi = pu, 0.5
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if na_kl(mid, pu) <= e1 else (lo, mid)
    return lo


def q_epochs(u, M):
    """the epoch sequences of the rate (RateFull.lean): d_0 = h/(a - h), J_m = ceil(d_m),
    d_{m+1} = d_m (J_m a + h)/(J_m a - h d_m), k_0 = 1, k_{m+1} = k_m + J_m + 1"""
    pu, lam, epsstar, a, h = lv_consts(u)
    d, J, k = [h / (a - h)], [], [1]
    for m in range(M):
        J.append(math.ceil(d[m]))
        d.append(d[m] * (J[m] * a + h) / (J[m] * a - h * d[m]))
        k.append(k[m] + J[m] + 1)
    return d, J, k


@conjecture("XVI.5 The closing radius at an extensive threshold, and the arithmetic of the epoch schedule (theory report Theorem 11.58a and its lemmas; workstream Q, Lemmas Q3, Q4, Propositions Q6, Q7, Theorem Q9; refereed R12).  (a) On exact tables of Q_m: Gamma~(r) <= (m + 1) e^{2u + e^u} e^{m e} for 0 <= r <= min(m, rho_e m + 1), rho_e in [p_u, 1/2] with KL(rho_e || p_u) = min(e, eps*); (b) hence for a threshold theta >= ((1 + eta)/(1 - eta)) (m + 1) e^{2u + e^u + m e} the conditions [N], [P] of Theorem 11.56 hold up to r_1 = min(m - 1, floor(rho_e m) + 1), and ln(2^m/|B(m, r_1)|) <= m theta_na(e) + ln(m + 1): the outer sample of a level with such a threshold costs e^{m theta_na(e)} up to the factor m + 1, and theta_na(h) = h; (c) at a bounded threshold theta = c, with s = sqrt((m/2) ln(2 e^{u(m_0 + 2)}/theta)) <= p_u m/2 - 1, the closing radius is at least floor(p_u m - s) and ln(1/pi) <= m a + u(1 + s) + (4/(3 p_u))(s^2 2/m + 2/m) + ln(m + 1) - a loss of order sqrt(m), which half the s would understate; (d) the epoch sequences satisfy B_0 = a, B_{m+1} = B_m J_m a/(J_m a + h) for B_m = h(1 + 1/d_m), B_m - h <= c_1/(k_m + c_2), phi_m = h/(J_m a + h) <= (1 + kappa)^{-m}/rbar, k_{m+1} < (1 + rbar) k_m, and C_* = 2 sqrt((1 + rbar) c_1 (a/h + 4)) is 4.65, 8.64, 13.5 at u = 1/2, 1, 2; (e) a slope step (lambda = 1, eta = 1/2, eta' = 1, b = 1, theta = e^{x - 1} - (3e + 1) - (2 p_u)^n/e) has certified accuracy exactly x, its theta is at least e^{x-1}/2 and satisfies the hypothesis of (b) at e = h with n_o = floor((x - 1 - c_log(n))/h) outer sites; a drop (lambda = eta = eta' = theta = c <= 1/3, b = alpha - w(c), w(c) = ln(e^c (1 + c)/(1 - c) + 2c) + c <= 6.25 c) has certified accuracy at most alpha once (2 p_u)^n <= 5c/6; (f) the hinted lower bound is n h - O(1) (referee R12, finding m1): with k* the least radius whose dip changes ln Z by more than eps, k* < rho_h n + (eps + ln 2)/u and ln(2^n/|B(n, k*)|) >= n h - ((eps + ln 2)/u) ln((1 - rho_h)/rho_h), rho_h = Lambda_1/u - and numerically it exceeds n h by about (1/2) ln n")
def t_extensive_threshold(rng, trials):
    stats = dict(part_a=0, least_slack_a=math.inf, part_b=0, least_slack_b=math.inf, part_c=0, radius_gap=0.0, half_s_fails=0,
                 epochs=0, slope_steps=0, drops=0)
    quick = trials < 100
    for u in (0.5, 1.0, 2.0):
        pu, lam, epsstar, a, h = lv_consts(u)
        if abs(na_theta_na(u, h) - h) > 1e-9:
            return False, dict(reason="theta_na(h) is not h", u=u)
        for m in ((1, 2, 3, 5, 8, 21, 55) if quick else (1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233)):
            for e in (0.0, 0.25 * epsstar, 0.5 * epsstar, h, 0.9 * epsstar, epsstar, 1.5 * epsstar):
                rho = q_rho(u, e)
                r1 = min(m - 1, math.floor(rho * m) + 1)
                rtop = min(m, math.floor(rho * m + 1))
                binom, ball, E, T = ba_exact_tables(m, u, rtop)
                cap = math.log(m + 1) + 2 * u + math.exp(u) + m * e
                for r in range(rtop + 1):
                    lg = math.log(math.exp(u) - 1) if r == 0 else math.log(E[r]) - math.log(ball[r])
                    if lg > cap + 1e-9:
                        return False, dict(reason="Gamma~(r) exceeds (m + 1) e^{2u + e^u + m e} at a radius up to rho_e m + 1",
                                           u=u, m=m, e=e, r=r)
                    stats["least_slack_a"] = min(stats["least_slack_a"], cap - lg)
                    stats["part_a"] += 1
                # (b) the ball that the level may close with
                if r1 >= 0:
                    lhs = m * math.log(2) - math.log(ball[r1 + 1])
                    rhs = m * na_theta_na(u, e) + math.log(m + 1)
                    if lhs > rhs + 1e-9:
                        return False, dict(reason="ln(2^m/|B(m, r_1)|) exceeds m theta_na(e) + ln(m + 1)", u=u, m=m, e=e, r1=r1)
                    stats["least_slack_b"] = min(stats["least_slack_b"], rhs - lhs)
                    stats["part_b"] += 1
    # (c) a bounded threshold: the closing radius from the definition, on exact tables
    for u, m, c in ((0.5, 120, 0.05), (0.5, 300, 1 / 3), (1.0, 250, 0.05)) + (() if quick else ((0.5, 500, 0.05), (1.0, 700, 0.05), (1.0, 400, 1 / 3))):
        pu, lam, epsstar, a, h = lv_consts(u)
        eta = theta = c
        c_eta = (1 - eta) / (1 + eta)
        cfrac = (1 - Fraction(c).limit_denominator(10 ** 6)) / (1 + Fraction(c).limit_denominator(10 ** 6))
        m0 = math.ceil(math.log(1 / c_eta) / u)
        ell = math.log(2 * math.exp(u * (m0 + 2)) / theta)
        sq = math.sqrt(m * ell / 2)
        if sq > pu * m / 2 - 1:
            return False, dict(reason="harness: the size is below the range of the refined bound", u=u, m=m, c=c)
        nu0 = 2 * math.exp(u) * m / (theta * (1 - eta))
        rmax = int(pu * m)
        binom, ball, E, T = ba_exact_tables(m, u, rmax)
        rdag = -1
        while rdag + 1 <= rmax:
            r = rdag + 1
            g1 = (math.exp(u) - 1) if r == 0 else E[r] / ball[r]
            g2 = E[r] / T(ba_kappa(ball, cfrac, r))
            if not (g1 <= theta * (1 - eta) * nu0 and min(g1 / c_eta, g2) <= theta):
                break
            rdag += 1
        r_plus = math.floor(pu * m - sq)
        if rdag < r_plus:
            return False, dict(reason="bounded threshold: the closing radius is below floor(p_u m - s)", u=u, m=m, c=c, rdag=rdag,
                               r_plus=r_plus)
        ln_inv_pi = m * math.log(2) - math.log(ball[rdag + 1])
        bound = m * a + u * (1 + sq) + (4 / (3 * pu)) * (ell + 2 / m) + math.log(m + 1)
        if ln_inv_pi > bound + 1e-9:
            return False, dict(reason="bounded threshold: ln(1/pi) exceeds m a + u(1 + s) + (4/(3 p_u))(l + 2/m) + ln(m + 1)", u=u, m=m, c=c)
        stats["part_c"] += 1
        stats["radius_gap"] = max(stats["radius_gap"], (pu * m - rdag) / sq)
        stats["half_s_fails"] += int(rdag < math.floor(pu * m - 0.5 * sq))
    # (d) the epoch sequences and the constant of the order
    cstar = {}
    for u in (0.5, 1.0, 2.0, 5.0):
        pu, lam, epsstar, a, h = lv_consts(u)
        kappa = h * h * a / ((a - h) * (a + h) * (2 * a - h))
        c1, c2, rbar = h * (1 + kappa) / kappa, (a + h) * (2 * a - h) / (h * a) - 2, (2 * a - h) / (a - h)
        d, J, k = q_epochs(u, 24 if quick else 36)
        B = [h * (1 + 1 / x) for x in d]
        if abs(B[0] - a) > 1e-12 * a or c2 < 0:
            return False, dict(reason="B_0 is not a, or c_2 is negative", u=u)
        for m in range(len(J)):
            if not (d[m] <= J[m] < d[m] + 1 and J[m] * a - h * d[m] > 0):
                return False, dict(reason="J_m is not the ceiling of d_m, or the recursion is not defined", u=u, m=m)
            if abs(B[m + 1] - B[m] * J[m] * a / (J[m] * a + h)) > 1e-10 * a:
                return False, dict(reason="B_{m+1} is not B_m J_m a/(J_m a + h)", u=u, m=m)
            if B[m] - h > c1 / (k[m] + c2) * (1 + 1e-10):
                return False, dict(reason="B_m - h exceeds c_1/(k_m + c_2)", u=u, m=m)
            if h / (J[m] * a + h) > (1 + kappa) ** (-m) / rbar * (1 + 1e-10):
                return False, dict(reason="the outer fraction of the drop of epoch m exceeds (1 + kappa)^{-m}/rbar", u=u, m=m)
            if not k[m + 1] < (1 + rbar) * k[m]:
                return False, dict(reason="k_{m+1} is not below (1 + rbar) k_m", u=u, m=m)
            stats["epochs"] += 1
        cstar[u] = 2 * math.sqrt((1 + rbar) * c1 * (a / h + 4))
    if abs(cstar[0.5] - 4.65) > 0.01 or abs(cstar[1.0] - 8.64) > 0.01 or abs(cstar[2.0] - 13.5) > 0.05:
        return False, dict(reason="the constant C_* of the order sqrt(n ln n)", values=cstar)
    # (e) the accuracies of the two kinds of level
    for _ in range(60):
        u = float(rng.choice([0.5, 1.0, 2.0]))
        pu, lam, epsstar, a, h = lv_consts(u)
        n = int(rng.integers(2, 4000))
        clog = math.log(n + 1) + math.log(6) + 2 * u + math.exp(u)
        x0n = 1 + clog + h
        if h * n >= x0n:
            x = float(rng.uniform(x0n, h * n))
            theta = math.exp(x - 1) - (3 * math.e + 1) - (2 * pu) ** n / math.e
            xout = math.log((2 * pu) ** n + math.e * (3 * math.e + 1 + theta))
            n_o = math.floor((x - 1 - clog) / h)
            if abs(xout - x) > 1e-9 or theta < math.exp(x - 1) / 2 or not 1 <= n_o <= n - 1:
                return False, dict(reason="slope step: the accuracy is not exactly x, theta is not at least e^{x-1}/2, or the outer block is not admissible",
                                   u=u, n=n, x=x, xout=xout, n_o=n_o)
            if math.log(3 * (n_o + 1)) + 2 * u + math.exp(u) + n_o * h > math.log(theta) + 1e-9:
                return False, dict(reason="slope step: theta is below the threshold of the lemma at e = h", u=u, n=n, x=x)
            stats["slope_steps"] += 1
        c = float(rng.uniform(0.001, 1 / 3))
        alpha = float(rng.uniform(0.05, 1.0))
        w = math.log(math.exp(c) * (1 + c) / (1 - c) + 2 * c) + c
        if w > 6.25 * c + 1e-12 or 5 * c / 6 > 1 - math.exp(-c) + 1e-15:
            return False, dict(reason="drop: w(c) <= 6.25 c or 5c/6 <= 1 - e^{-c} fails", c=c)
        nmin = max(2, math.ceil(math.log(6 / (5 * c)) / math.log((1 + math.exp(u)) / 2)))
        nd = nmin + int(rng.integers(0, 50))
        beta = alpha - w
        xout = math.log((2 * pu) ** nd + math.exp(beta) * (math.exp(c) * (1 + c) / (1 - c) + 2 * c))
        if xout > alpha + 1e-12:
            return False, dict(reason="drop: the certified accuracy exceeds alpha", u=u, n=nd, c=c, alpha=alpha, xout=xout)
        stats["drops"] += 1
    # (f) the hinted lower bound of Theorem 11.25(a) is n h - O(1): exact tables of Q_n
    stats.update(lower=0, lower_min_excess=math.inf, lower_excess_large_n=0.0)
    for u in (0.5, 1.0, 2.0):
        pu, lam, epsstar, a, h = lv_consts(u)
        rho_h = lam / u
        for n in ((10, 40, 160) if quick else (10, 40, 160, 640, 2500)):
            binom = [math.comb(n, j) for j in range(n + 1)]
            ball = list(itertools.accumulate(binom))
            lbin = [math.log(b) for b in binom]                    # logarithms of exact integers: no overflow at large n
            for eps in (0.01, 0.1, 1.0, 10.0):
                target = n * math.log(2) + math.log(math.expm1(eps))
                kstar = None
                for k in range(n // 2 + 1):
                    terms = [lbin[j] + u * (k + 1 - j) + math.log1p(-math.exp(-u * (k + 1 - j))) for j in range(k + 1)]
                    top = max(terms)
                    lE = top + math.log(math.fsum(math.exp(t_ - top) for t_ in terms))
                    if lE > target:
                        kstar = k
                        break
                if kstar is None:
                    continue                                       # the accuracy is too coarse for this size
                if not kstar < rho_h * n + (eps + math.log(2)) / u:
                    return False, dict(reason="hinted lower bound: k* is not below rho_h n + (eps + ln 2)/u", u=u, n=n, eps=eps, kstar=kstar)
                lhs = n * math.log(2) - math.log(ball[kstar])
                rhs = n * h - ((eps + math.log(2)) / u) * math.log((1 - rho_h) / rho_h)
                if lhs < rhs - 1e-9:
                    return False, dict(reason="hinted lower bound: ln(2^n/|B(n, k*)|) is below n h - ((eps + ln 2)/u) ln((1 - rho_h)/rho_h)",
                                       u=u, n=n, eps=eps)
                stats["lower"] += 1
                stats["lower_min_excess"] = min(stats["lower_min_excess"], lhs - rhs)
                if n >= 160 and eps == 1.0 and u == 1.0:
                    stats["lower_excess_large_n"] = max(stats["lower_excess_large_n"], lhs - n * h)
    if not (stats["part_a"] > 500 and stats["least_slack_a"] < 3.0 and stats["part_b"] > 100 and stats["least_slack_b"] < 1e-9
            and stats["lower"] >= 20 and stats["lower_excess_large_n"] > 1.0
            and stats["part_c"] >= 3
            and stats["half_s_fails"] >= 2 and stats["epochs"] >= 90 and stats["slope_steps"] >= 30 and stats["drops"] >= 60):
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


class LdPair:
    """The pair (theta_na, theta_hint) of the level recursion with what the line lemmas use: the cube at slope u, or
    the Gaussian small-slope limit (u = None): theta_na(e) = (1 - sqrt e)^2, theta_hint(y) = (1 - y)^2/4."""

    def __init__(self, u, ngrid=20001):
        self.u = u
        if u is None:
            self.a, self.h, self.estar, self.Lh, self.H2 = 1.0, 0.25, 1.0, 0.5, 0.5
            self.e = np.exp(np.linspace(math.log(1e-9), 0.0, ngrid))
            self.kap = (1 - np.sqrt(self.e)) ** 2
        else:
            pu, lam, epsstar, a, h = lv_consts(u)
            self.pu, self.lam, self.estar, self.a, self.h = pu, lam, epsstar, a, h
            rho_h = lam / u
            self.Lh = math.log((1 - rho_h) / rho_h) / u
            self.H2 = 1 / (u * u * rho_h * (1 - rho_h))
            t = np.linspace(1e-3, 1.0, ngrid)
            rho = pu + (0.5 - pu) * t ** 2
            self.e = rho * np.log(rho / pu) + (1 - rho) * np.log((1 - rho) / (1 - pu))
            self.kap = rho * np.log(2 * rho) + (1 - rho) * np.log(2 * (1 - rho))

    def theta_na(self, e):
        if self.u is None:
            return (1 - math.sqrt(e)) ** 2 if e < 1 else 0.0
        return na_theta_na(self.u, e)

    def theta_hint(self, y):
        if self.u is None:
            return (1 - y) ** 2 / 4 if y < 1 else 0.0
        return na_theta_hint(self.u, y)

    def J(self, t):
        """min over rho of KL(rho||1/2) + t (u rho - Lambda_1): the concave dual of theta_hint."""
        if self.u is None:
            return t - t * t
        L = lambda v: math.log(2 / (1 + math.exp(-v)))
        return L(t * self.u) - t * L(self.u)

    def sigma(self, B, s):
        """the slope map Sigma_B(s) = sup_e [B - (1 - s) theta_na(e)]/e on the grid, and the maximising e."""
        r = (B - (1 - s) * self.kap) / self.e
        j = int(np.argmax(r))
        return float(r[j]), float(self.e[j]), 0 < j < len(r) - 1


def ld_bracket(P, T, g, phi, beta, ngam=300):
    """sup over gamma >= beta of min(gamma, mu) + (1 - phi) T(gamma/(1 - phi)); the grid contains beta and max(beta, mu)."""
    mu = phi * P.theta_na((g - beta) / phi)
    top = max(beta, mu)
    gam = np.unique(np.concatenate([[beta, top], np.linspace(beta, top, ngam)]))
    return max(min(x, mu) + (1 - phi) * T(x / (1 - phi)) for x in gam), mu


def ld_gauss_tau_lb(k):
    """the largest B whose tangent line of the Gaussian theta_na stays regular for k - 1 values of the Moebius orbit,
    from the closed form (k - 1) theta(B) + phi_0(B) = pi (bisection), and from the orbit itself."""
    def angle(B):
        rt = math.sqrt(4 * B - 1)
        th = math.atan2(rt, 1 - 2 * B)
        ph0 = math.atan2((1 - B) * rt, 1 - 3 * B)                     # arccot((1 - 3B)/((1 - B) rt)) in (0, pi)
        return (k - 1) * th + ph0
    lo, hi = 0.25 + 1e-15, 0.5 - 1e-12
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if angle(mid) < math.pi else (lo, mid)
    closed = lo

    def survives(B):
        s = B / (1 - B)
        for _ in range(k - 1):
            if not s < 1 - B:
                return False
            s = B * (1 - s) / (1 - s - B)
        return True
    lo, hi = 0.25 + 1e-15, 0.5 - 1e-12
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if survives(mid) else (lo, mid)
    return closed, lo


@conjecture("XVI.6 The level recursion at the level of lines (theory report Theorem 11.53a; Lean: LineDynamics.lean for (a) and (e)).  (a) Lemma L: if T(x) >= B - sigma x for all x > 0 with 0 <= sigma, and sigma' = Sigma_B(sigma) = sup_e [B - (1 - sigma) theta_na(e)]/e is finite, then for every outer fraction phi and tolerance beta the bracket of the level is at least B - sigma' g - evaluated at gamma = max(beta, mu); and for T equal to the line the infimum over (phi, beta) is B - sigma' g: lines are propagated exactly by the slope map.  (b) The slope map of the cube solves (1 - sigma + sigma') J(sigma'/(1 - sigma + sigma')) = B with J(t) = Lambda(t u) - t Lambda(u), Lambda(v) = ln(2/(1 + e^{-v})); J is the concave dual of theta_hint (theta_hint(x) = max_t [J(t) - t x]), J(L_h) = h = max J, J''(L_h) = -1/theta_hint''(0); the tangent line of theta_na with slope s has the intercept (1 + s) J(s/(1 + s)); and near the bottleneck Sigma_B(sigma) - sigma = [delta + (sigma - L_h)^2/(2 theta_hint''(0))]/h up to 10 per cent for B = h + delta, delta <= 10^{-3} h, |sigma - L_h| <= 0.02.  (c) For the Gaussian pair the slope map is the Moebius map sigma' = B (1 - sigma)/(1 - sigma - B), and the largest intercept B whose tangent line stays regular (slope below 1 - B) through k - 1 values of the orbit is the root of (k - 1) theta(B) + phi_0(B) = pi, theta = arctan(sqrt(4B - 1)/(1 - 2B)), phi_0 = arccot((1 - 3B)/((1 - B) sqrt(4B - 1))): a lower bound tau_k^LB of the exponent of k levels at accuracy zero, 0.381966 at k = 2, within 2 per cent of 1/4 + (pi^2/16)/(k + 1/2)^2 from k = 10 on and within 0.5 per cent from k = 20 on (above it).  (d) For the cube the lower bound from the tangent lines of theta_na is below the machine-checked upper bound h + c_1/(k + c_2) at every k, and k^2 (tau_k^LB - h) approaches 2 pi^2 h^2 theta_hint''(0) (within 5 per cent at k = 40, u = 1/2, 1, 2).  (e) Lemma M: if T is nonincreasing and T(x) <= B - sigma x on (0, R] with sigma <= 1, then for phi = g/e the bracket is at most (1 - phi) B + (1 - sigma) mu whenever mu/(1 - phi) <= R.  (f) Duality for convex majorants: for M the maximum of finitely many lines with slopes in [0, 1], inf_e max_lines [B - (g/e)(B - (1 - s) theta_na(e))] equals the supremum over the convex hull of the lines of the infimum over e (two lines suffice) - the level operator commutes with taking tangent lines")
def t_line_dynamics(rng, trials):
    quick = trials < 100
    stats = dict(lemma_L=0, least_slack_L=math.inf, sharp_L=0, worst_sharp_L=0.0, map_eq=0, worst_map_eq=0.0, dual_J=0,
                 bottleneck=0, worst_bottleneck=0.0, gauss_k=0, cube_k=0, lemma_M=0, least_slack_M=math.inf,
                 duality=0, worst_gap=0.0, mixed_pairs=0)
    pairs = [LdPair(None), LdPair(0.5), LdPair(1.0), LdPair(2.0)]
    # (a) Lemma L by brute force over (phi, beta); the bound is attained for the line itself
    for P in pairs:
        for _ in range(12 if quick else 60):
            sig = rng.uniform(0.0, 0.9)
            B = rng.uniform(0.3, 0.97) * (1 - sig) * P.a
            sp, e_at, interior = P.sigma(B, sig)
            if sp < sig:                              # possible only for lines below the tangents of theta_hint (B < J(sigma) <= h)
                if B >= P.h:
                    return False, dict(reason="Sigma_B(sigma) is below sigma for a line with intercept at least h", pair=P.u, B=B, sigma=sig)
                continue
            w = rng.uniform(0.0, 0.5)
            T = lambda x, B=B, sig=sig, w=w: max(B - sig * x, 0.0) + w * P.theta_na(x)
            for _ in range(8 if quick else 25):
                g = rng.uniform(1e-3, 0.95) * P.estar
                phi = rng.choice([rng.uniform(0.001, 0.999), min(0.999, g / e_at) if e_at > g else rng.uniform(0.001, 0.999)])
                beta = g * rng.choice([1e-6, 1e-3, rng.uniform(0.0, 1.0)])
                beta = min(max(beta, 1e-9), g * (1 - 1e-9))
                val, mu = ld_bracket(P, T, g, phi, beta)
                bound = B - sp * (1 + 1e-6) * g
                if val < bound - 1e-9:
                    return False, dict(reason="Lemma L: a bracket below B - Sigma_B(sigma) g", pair=P.u, B=B, sigma=sig, g=g, phi=phi, beta=beta)
                stats["least_slack_L"] = min(stats["least_slack_L"], val - bound)
                stats["lemma_L"] += 1
            # sharpness: T = the line, phi = g/e*, beta -> 0
            if interior and B >= P.h:
                g = rng.uniform(0.02, 0.6) * e_at
                line = lambda x, B=B, sig=sig: B - sig * x
                val, mu = ld_bracket(P, line, g, g / e_at, 1e-9 * g)
                gap = abs(val - (B - sp * g))
                if gap > 2e-3 * P.a:
                    return False, dict(reason="the slope map is not attained for the line itself", pair=P.u, B=B, sigma=sig, g=g, gap=gap)
                stats["worst_sharp_L"] = max(stats["worst_sharp_L"], gap / P.a)
                stats["sharp_L"] += 1
    # (b) the slope map of the cube and the dual function J
    for P in pairs[1:]:
        u, h, a = P.u, P.h, P.a
        if abs(P.J(P.Lh) - h) > 1e-12 or any(P.J(P.Lh + d) > h + 1e-13 for d in (-0.3, -0.05, -1e-3, 1e-3, 0.05, 0.3)):
            return False, dict(reason="J(L_h) is not h = max J", u=u)
        d = 1e-4
        J2 = (P.J(P.Lh + d) - 2 * P.J(P.Lh) + P.J(P.Lh - d)) / d ** 2
        if abs(J2 * P.H2 + 1) > 1e-4:
            return False, dict(reason="J''(L_h) is not -1/theta_hint''(0)", u=u, J2=J2, H2=P.H2)
        ts = np.linspace(0.0, 1.0, 20001)
        Jt = np.array([P.J(t) for t in ts])
        for x in (0.05, 0.2, 0.5, 0.8):
            xx = x * P.estar
            if abs(float(np.max(Jt - ts * xx)) - P.theta_hint(xx)) > 1e-7:
                return False, dict(reason="theta_hint is not the dual of J", u=u, x=xx)
            stats["dual_J"] += 1
        for s in (0.1, 0.5, 1.0, 3.0):
            inter = float(np.min(P.kap + s * P.e))
            if abs(inter - (1 + s) * P.J(s / (1 + s))) > 1e-6:
                return False, dict(reason="the intercept of the tangent line of theta_na is not (1 + s) J(s/(1 + s))", u=u, s=s)
            stats["dual_J"] += 1
        for _ in range(40 if quick else 200):
            sig = rng.uniform(0.0, 0.9)
            B = rng.uniform(0.3, 0.97) * (1 - sig) * a
            sp, e_at, interior = P.sigma(B, sig)
            if not interior:
                continue
            w = 1 - sig + sp
            err = abs(w * P.J(sp / w) - B)
            if err > 1e-6 * a:
                return False, dict(reason="the slope map does not solve (1 - s + s') J(s'/(1 - s + s')) = B", u=u, B=B, sigma=sig, err=err)
            stats["worst_map_eq"] = max(stats["worst_map_eq"], err / a)
            stats["map_eq"] += 1
        for delta in (1e-3 * h, 1e-4 * h):
            for z in (-0.02, -0.01, 0.0, 0.01, 0.02):
                sp, e_at, interior = P.sigma(h + delta, P.Lh + z)
                pred = (delta + z * z / (2 * P.H2)) / h
                rel = abs((sp - P.Lh - z) / pred - 1)
                if rel > 0.1:
                    return False, dict(reason="bottleneck expansion of the slope map off by more than 10 per cent", u=u, delta=delta, z=z, rel=rel)
                stats["worst_bottleneck"] = max(stats["worst_bottleneck"], rel)
                stats["bottleneck"] += 1
    # (c) the Gaussian pair: Moebius map, closed form of the lower bound
    G = pairs[0]
    for _ in range(40 if quick else 200):
        sig = rng.uniform(0.0, 0.7)
        B = rng.uniform(0.05, 0.95) * (1 - sig)
        sp, e_at, interior = G.sigma(B, sig)
        if abs(sp - B * (1 - sig) / (1 - sig - B)) > 1e-5 * max(1.0, sp):
            return False, dict(reason="the slope map of the Gaussian pair is not the Moebius map", B=B, sigma=sig, sup=sp)
    for k in list(range(2, 13)) + [20, 40, 80]:
        closed, orbit = ld_gauss_tau_lb(k)
        if abs(closed - orbit) > 1e-9:
            return False, dict(reason="closed form and orbit of the Gaussian lower bound differ", k=k, closed=closed, orbit=orbit)
        if k == 2 and abs(closed - (3 - math.sqrt(5)) / 2) > 1e-9:
            return False, dict(reason="tau_2^LB of the Gaussian pair is not (3 - sqrt 5)/2", value=closed)
        rel = (closed - 0.25) * (k + 0.5) ** 2 / (math.pi ** 2 / 16) - 1
        if k >= 10 and not 0 < rel < (0.02 if k < 20 else 0.005):
            return False, dict(reason="Gaussian lower bound against (pi^2/16)/(k + 1/2)^2: not within 2 per cent (k >= 10) / 0.5 per cent (k >= 20), or below it",
                               k=k, value=closed, rel=rel)
        stats["gauss_k"] += 1
    # (d) the cube: lower bound from lines against the machine-checked upper bound, and against the constant
    for P in pairs[1:]:
        u, h, a = P.u, P.h, P.a
        kappa = h * h * a / ((a - h) * (a + h) * (2 * a - h))
        c1, c2 = h * (1 + kappa) / kappa, (a + h) * (2 * a - h) / (h * a) - 2
        const = 2 * math.pi ** 2 * h * h * P.H2

        def s0(B):                                   # slope of the tangent line of theta_na with intercept B
            lo, hi = 1e-9, 1e6
            for _ in range(200):
                mid = math.sqrt(lo * hi)
                lo, hi = (mid, hi) if (1 + mid) * P.J(mid / (1 + mid)) < B else (lo, mid)
            return lo

        def survives(B, k):
            s = s0(B)
            for _ in range(k - 1):
                if not s < 1 - B / a:
                    return False
                s = P.sigma(B, s)[0]
            return True
        for k in ((2, 3, 5, 10, 40) if quick else (2, 3, 4, 5, 7, 10, 15, 20, 40, 80)):
            lo, hi = h * (1 + 1e-12), a
            if not survives(lo, k):
                return False, dict(reason="a line with intercept h does not stay regular", u=u, k=k)
            for _ in range(50):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if survives(mid, k) else (lo, mid)
            if lo > h + c1 / (k + c2) + 1e-12:
                return False, dict(reason="the lower bound from lines exceeds the machine-checked upper bound", u=u, k=k, lb=lo)
            ratio = k * k * (lo - h) / const
            if ratio > 1.0 + 1e-6 or (k >= 40 and ratio < 0.95) or ratio < 0.8:
                return False, dict(reason="k^2 (tau_k^LB - h) against 2 pi^2 h^2 theta_hint''(0)", u=u, k=k, ratio=ratio)
            stats["cube_k"] += 1
    # (e) Lemma M: a majorant line on a range
    for P in pairs:
        for _ in range(40 if quick else 200):
            sig = rng.uniform(0.0, 1.0)
            R = rng.uniform(0.02, 0.6) * P.estar
            B = sig * R + rng.uniform(0.05, 1.0) * P.a
            w = rng.uniform(0.0, 1.0)
            TR = max(0.0, B - (sig + w) * R)
            T = lambda x, B=B, sig=sig, w=w, R=R, TR=TR: max(0.0, B - (sig + w) * x) if x <= R else TR * math.exp(-(x - R))
            e = rng.uniform(0.05, 0.98) * P.estar
            tna = P.theta_na(e)
            if tna <= 0:
                continue
            g = rng.uniform(0.01, 0.99) * R * e / (tna + R)
            phi = g / e
            beta = g * 10 ** rng.uniform(-9, -2)
            val, mu = ld_bracket(P, T, g, phi, beta)
            if mu / (1 - phi) > R:
                continue
            bound = (1 - phi) * B + (1 - sig) * mu
            if val > bound + 1e-9:
                return False, dict(reason="Lemma M: a bracket above (1 - phi) B + (1 - sigma) mu", pair=P.u, B=B, sigma=sig, R=R, g=g, e=e)
            stats["least_slack_M"] = min(stats["least_slack_M"], bound - val)
            stats["lemma_M"] += 1
    # (f) duality for a maximum of lines
    for P in pairs:
        for _ in range(6 if quick else 30):
            nl = int(rng.integers(2, 6))
            lines = [(rng.uniform(0.15, 1.0) * P.a, rng.uniform(0.0, 1.0)) for _ in range(nl)]
            g = rng.uniform(0.01, 0.5) * P.estar
            m = P.e > g * 1.0001
            ee, kk = P.e[m], P.kap[m]
            F = np.array([Bq - (g / ee) * (Bq - (1 - sq) * kk) for Bq, sq in lines])
            primal = float(np.min(np.max(F, axis=0)))
            dual = -math.inf
            lam = np.linspace(0.0, 1.0, 401)[:, None]
            arg = None
            for i in range(nl):
                for j in range(i, nl):
                    v = np.min(lam * F[i][None, :] + (1 - lam) * F[j][None, :], axis=1)
                    q = int(np.argmax(v))
                    if float(v[q]) > dual:
                        dual, arg = float(v[q]), (i, j, float(lam[q, 0]))
            if dual > primal + 1e-9:
                return False, dict(reason="weak duality violated (harness)", pair=P.u)
            gap = (primal - dual) / P.a
            if gap > 2e-3:
                return False, dict(reason="duality gap for a maximum of lines: inf_e max_lines exceeds the supremum over the hull of inf_e",
                                   pair=P.u, lines=lines, g=g, primal=primal, dual=dual)
            stats["worst_gap"] = max(stats["worst_gap"], gap)
            stats["duality"] += 1
            stats["mixed_pairs"] += (arg[0] != arg[1] and 0.0 < arg[2] < 1.0)
    if not (stats["lemma_L"] > 200 and stats["least_slack_L"] < 1e-2 and stats["sharp_L"] >= 20 and stats["map_eq"] >= 60
            and stats["bottleneck"] >= 30 and stats["lemma_M"] >= 60 and stats["least_slack_M"] < 1e-3
            and stats["duality"] >= 20 and stats["mixed_pairs"] >= 3 and stats["gauss_k"] >= 14 and stats["cube_k"] >= 15):
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


@conjecture("XVI.7 [refuted: DEAD_ENDS D64] Propagating the lines of a convex majorant one by one - without the concave hull of the new slopes - and reading off sup min(B, (1 - s) a) gives an upper bound of the next exponent at accuracy zero.  For the Gaussian pair: T_1 = theta_na <= (1 - x)_+ with lines (B, s) = (s, s), the first level is 1/2, the Moebius map sends (s, s) to slope s (1 - s)/(1 - 2s), and the formula gives tau_3 <= 1/3; but tau_3 >= 1/(2 sqrt 2) = 0.3536, because T_2 >= theta_hint and T_2(0+) = 1/2 (lines with s in (0.382, 1/2) jump over the window of slopes [1 - B, 1] in which a line can be dropped)", expect_fail=True)
def t_naive_lines(rng, trials):
    G = LdPair(None)
    s0 = np.linspace(1e-6, 0.5 - 1e-6, 200001)
    slope = s0 * (1 - s0) / (1 - 2 * s0)
    naive = float(np.max(np.minimum(s0, 1 - slope)))
    # tau_3 = inf_phi (1 - phi) sup_{x <= X} (x + T_2(x)), X = phi/(1 - phi); T_2(0+) = 1/2 and T_2 >= theta_hint give
    # tau_3 >= inf_phi max((1 - phi)/2, (1 - phi)(X + theta_hint(X))) = inf_phi max((1 - phi)/2, 1/(4 (1 - phi)))
    phis = np.linspace(1e-6, 1 - 1e-6, 400001)
    X = phis / (1 - phis)
    hint = np.where(X < 1, (1 - X) ** 2 / 4, 0.0)
    lower = float(np.min(np.maximum((1 - phis) / 2, (1 - phis) * (X + hint))))
    # the two ingredients, numerically: the first level is 1/2, and no (phi, beta) on a grid takes R[theta_na](g) below 1/2 - 0.01 at small g
    first = float(np.min(np.maximum(1 - phis, np.where(X <= 1, 0.0, phis))))
    g = 1e-5
    least = math.inf
    for phi in np.linspace(0.02, 0.98, 49):
        for bf in (1e-3, 0.03, 0.3, 0.9):
            val, mu = ld_bracket(G, G.theta_na, g, float(phi), bf * g, ngam=120)
            least = min(least, val)
    if abs(naive - 1 / 3) > 1e-4 or abs(first - 0.5) > 1e-4 or least < 0.49 or abs(lower - 1 / (2 * math.sqrt(2))) > 1e-4:
        return True, dict(reason="harness: an ingredient of the refutation is off", naive=naive, first=first, least=least, lower=lower)
    if naive < lower - 1e-3:
        return False, dict(reason="the naive line formula gives tau_3 <= %.4f for the Gaussian pair, but tau_3 >= %.4f" % (naive, lower),
                           naive=naive, lower_bound_of_tau3=lower, level_two=first)
    return True, dict(naive=naive, lower=lower)


class RtPair:
    """A pair through its dual function J(t) = inf_e [(1 - t) theta_na(e) + t e]: the Gaussian pair (u = None), the cube
    at slope u, or the kinked pair theta_na = max(1 - 3e, 1/2 - e, 0) (u = 'kink').  Exact slope map
    Sigma(B, s) = t'(1 - s)/(1 - t'), Q(t') = B/(1 - s), Q = J/(1 - t); partial derivatives 1/e*, theta_na(e*)/e*
    with e* = J + (1 - t') J', theta_na(e*) = J - t' J'  (docs/workstreams/R_REPORT.md, sections 1-2)."""

    def __init__(self, u):
        self.u = u
        if u is None:
            self.a, self.h, self.L, self.vt = 1.0, 0.25, 0.5, 0.5
        elif u == 'kink':
            self.a, self.h, self.L1, self.L2 = 1.0, 0.25, 0.5, 0.75
        else:
            pu, lam, epsstar, a, h = lv_consts(u)
            self.a, self.h, self.lam = a, h, lam
            rho_h = lam / u
            self.L = math.log((1 - rho_h) / rho_h) / u
            self.vt = 1 / (u * u * rho_h * (1 - rho_h))          # theta_hint''(0)
        if u != 'kink':
            self.const = 2 * math.pi ** 2 * self.h ** 2 * self.vt

    def J(self, t):
        if self.u is None:
            return t - t * t
        if self.u == 'kink':
            return min(1.0 - t, 0.25, 0.5 * t)
        return math.log(2 / (1 + math.exp(-t * self.u))) - t * self.lam

    def dJ(self, t):
        if self.u is None:
            return 1 - 2 * t
        return self.u / (1 + math.exp(t * self.u)) - self.lam

    def theta_na(self, e):
        if self.u is None:
            return (1 - math.sqrt(e)) ** 2 if e < 1 else 0.0
        if self.u == 'kink':
            return max(1 - 3 * e, 0.5 - e, 0.0)
        return na_theta_na(self.u, e)

    def regular(self, B, s):
        if self.u == 'kink':
            return s < 1.0 and B <= (1.0 - s) * self.a           # finite slope at zero: the boundary is regular
        return s < 1.0 and B < (1.0 - s) * self.a

    def tprime(self, y):
        """Q^{-1}(y), Q(t) = J(t)/(1 - t)."""
        if self.u is None:
            return y
        lo, hi = 0.0, 1.0
        for _ in range(90):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if self.J(mid) < y * (1.0 - mid) else (lo, mid)
        return 0.5 * (lo + hi)

    def sigma(self, B, s):
        if not self.regular(B, s):
            return math.inf
        if self.u == 'kink':                                     # piecewise linear: the supremum is at a vertex or a limit
            v = max(0.0, (B - (1 - s) * 0.25) / 0.25, B / 0.5)
            return max(v, 3 * (1 - s)) if B == (1.0 - s) * self.a else v
        tp = self.tprime(B / (1.0 - s))
        return tp * (1.0 - s) / (1.0 - tp)

    def grad(self, B, s):
        tp = self.tprime(B / (1.0 - s))
        e = self.J(tp) + (1 - tp) * self.dJ(tp)
        th = self.J(tp) - tp * self.dJ(tp)
        return tp * (1.0 - s) / (1.0 - tp), 1.0 / e, th / e

    def orbit(self, B, n):
        """p_n(B): n steps of the slope map from the flat line (inf once not regular)."""
        s = 0.0
        for _ in range(n):
            s = self.sigma(B, s)
            if not math.isfinite(s):
                return math.inf
        return s

    def orbit_slope(self, B, n):
        """(p_n(B), dp_n/dB) by the chain rule."""
        p, dp = 0.0, 0.0
        for _ in range(n):
            if not self.regular(B, p):
                return math.inf, math.inf
            p, gB, gs = self.grad(B, p)
            dp = gB + gs * dp
        return p, dp


def rt_chain(P, s_t, b0, jmax):
    """The restarted chain of cut orbit curves (R_REPORT section 6): returns (largest W_{j+1}(b_{j+1}), list of
    (j, b_j), worst excess of m_{j+1}/m_j over its bound)."""
    h, a = P.h, P.a

    def cut(j):
        if P.orbit(b0, j) <= s_t:
            return None
        lo, hi = h, b0
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if P.orbit(mid, j) <= s_t else (lo, mid)
        return lo, P.orbit_slope(lo, j)[1]
    b, worst, bs, excess = b0, 0.0, [], -math.inf
    cur = cut(1)
    for j in range(1, jmax + 1):
        nxt = cut(j + 1)
        if cur is None:
            b_next = b
        else:
            Bt, m = cur
            b_next = min(b, Bt + (1 - s_t - Bt / a) / (m + 1 / a))
        if nxt is None or b_next <= nxt[0]:
            Wn = P.orbit(b_next, j + 1)
        else:
            Wn = s_t + nxt[1] * (b_next - nxt[0])
        if nxt is not None and cur is not None:
            sig1 = P.orbit(nxt[0], j)
            _, gB, gs = P.grad(nxt[0], sig1)
            excess = max(excess, nxt[1] / cur[1] - (gs + gB / cur[1]))
        worst = max(worst, Wn)
        bs.append((j, b))
        b, cur = b_next, nxt
    return worst, bs, excess


def rt_prop_u(P, rng, concave, nB=800):
    """One random case of Proposition U: (R_ref - U)/a, R_ref = the bracket of R at beta -> 0 minimised over phi = g/e
    (grid in z = ln(e/g - 1), then golden section: the function is quasi-convex in e), U = sup_B (B - Sigma(B, W(B)) g)."""
    b = rng.uniform(0.3, 1.0) * P.a
    c1, c2 = sorted([rng.uniform(0, b), rng.uniform(0, b)])
    a1, a2 = rng.uniform(0, 2 / b), rng.uniform(0, 6 / b)
    w0 = [0.0, 0.0, rng.uniform(0, 0.3)][int(rng.integers(0, 3))]
    Bg = np.linspace(0, b, nB)
    W = np.maximum(w0, np.maximum(a1 * (Bg - c1), a2 * (Bg - c2)))
    if W[-1] > 1:
        W = W / W[-1] * rng.uniform(0.5, 1.0)
    if concave:
        W = rng.uniform(0.3, 0.9) * np.sqrt(Bg / b)
    sig = np.array([P.sigma(float(B), float(w)) for B, w in zip(Bg, W)])
    fin = np.isfinite(sig)
    g = rng.uniform(0.01, 1.2) * P.h
    U = float(np.max(Bg[fin] - sig[fin] * g))
    beta = 1e-9 * g

    def fz(z):
        phi = 1.0 / (1.0 + math.exp(z))
        mu = phi * P.theta_na((g - beta) / phi)
        return mu + (1 - phi) * float(np.max(Bg - W * (max(beta, mu) / (1 - phi))))
    zs = [-25 + 37 * i / 160 for i in range(161)]
    best, ib = min((fz(z), i) for i, z in enumerate(zs))
    lo, hi = zs[max(ib - 1, 0)], zs[min(ib + 1, 160)]
    gr = (math.sqrt(5) - 1) / 2
    x1, x2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
    f1, f2 = fz(x1), fz(x2)
    for _ in range(60):
        if f1 <= f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - gr * (hi - lo)
            f1 = fz(x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + gr * (hi - lo)
            f2 = fz(x2)
    return (min(best, f1, f2) - U) / P.a


@conjecture("XVI.8 The rate of the level recursion (theory report Theorem 11.53b; docs/workstreams/R_REPORT.md): lim k^2 (tau_k - h) = 2 pi^2 h^2 theta_hint''(0).  Ingredients, each tested: (a) the slope map Sigma(B, s) = sup_e [B - (1 - s) theta_na(e)]/e is jointly convex and nondecreasing in both arguments; (b) the orbit curves p_j(B) = Sigma(B, p_{j-1}(B)), p_0 = 0, are convex and nondecreasing in B; (c) the bottleneck: Sigma(h + delta, L + v) - (L + v) = [delta + v^2/(2 theta_hint''(0))]/h up to a factor 1 + 8|v| + 0.002 for |v| <= 0.02, delta = 10^{-6} h; (d) the passage time: sqrt(delta) N_t(delta) increases to pi h sqrt(2 theta_hint''(0)) as delta -> 0 (within 6 per cent at delta = 10^{-4} h and 2.5 per cent at 10^{-5} h, from below), N_t the number of steps of the orbit of the flat line with intercept h + delta to exceed the slope L + 0.05; (e) Proposition U: for T the upper envelope of the lines (B, W(B)), W convex nondecreasing with values in [0, 1], the level operator satisfies R[T](g) <= sup_B (B - Sigma(B, W(B)) g), with equality for beta -> 0 - and for a concave W the right side is exceeded (convexity cannot be dropped); (f) the chain of cut orbit curves restarted from a flat majorant b_0 = h + 0.02 at the slope level L + 0.05 (Gaussian pair; the cube at u = 1 from h + 0.003): the cut curve of level j + 1 stays below slope one on [0, b_{j+1}] at every level (the range condition), the ratio of consecutive slopes at the cut is below its bound, j^2 (b_j - h)/(2 pi^2 h^2 theta_hint''(0)) decreases towards one from above - while from the wide start b_0 = h + 0.15 the range condition fails; (g) a kink of theta_na at its fixed point (theta_na = max(1 - 3e, 1/2 - e, 0), J flat on [1/2, 3/4]): the step of the slope map is exactly delta/h on the flat part and the lower bound from lines is at least (L_2 - L_1) h/(k + 2) above h - the rate 1/k; (h) theta_hint''(0) = -1/J''(L) = theta_na''(h)/(1 + |theta_na'(h)|)^3")
def t_rate_theorem(rng, trials):
    quick = trials < 100
    stats = dict(convex=0, curves=0, prop_u=0, chain_levels=0)
    G, C1 = RtPair(None), RtPair(1.0)
    pairs = [G, C1, RtPair(float(rng.uniform(0.5, 2.5)))]
    # (a) joint convexity, monotonicity
    for P in pairs:
        for _ in range(150 if quick else 1200):
            s1, s2 = rng.uniform(0, 0.95), rng.uniform(0, 0.95)
            B1, B2 = rng.uniform(0, (1 - s1) * P.a * 0.98), rng.uniform(0, (1 - s2) * P.a * 0.98)
            lam = rng.uniform(0.05, 0.95)
            v1, v2 = P.sigma(B1, s1), P.sigma(B2, s2)
            vm = P.sigma(lam * B1 + (1 - lam) * B2, lam * s1 + (1 - lam) * s2)
            if vm > lam * v1 + (1 - lam) * v2 + 1e-9 * (1 + v1 + v2):
                return False, dict(reason="the slope map is not jointly convex", pair=P.u, B=(B1, B2), s=(s1, s2), lam=lam)
            dB, ds = rng.uniform(0, 0.01) * P.a, rng.uniform(0, 0.01)
            if P.regular(B1 + dB, s1 + ds) and P.sigma(B1 + dB, s1 + ds) < v1 - 1e-10:
                return False, dict(reason="the slope map is not nondecreasing", pair=P.u, B=B1, s=s1)
            stats["convex"] += 1
    # (b) orbit curves
    for P in pairs:
        Bs = np.linspace(0.2 * P.h, 1.6 * P.h, 81 if quick else 241)
        for j in ((1, 2, 5, 12) if quick else (1, 2, 3, 5, 8, 12, 20, 40)):
            vals = [P.orbit(float(B), j) for B in Bs]
            fin = [v for v in vals if math.isfinite(v)]
            if any(vals[i] > vals[i + 1] + 1e-12 for i in range(len(vals) - 1)):
                return False, dict(reason="an orbit curve is not nondecreasing in B", pair=P.u, j=j)
            for i in range(1, len(fin) - 1):
                if fin[i + 1] - 2 * fin[i] + fin[i - 1] < -1e-9 * max(1.0, abs(fin[i])):
                    return False, dict(reason="an orbit curve is not convex in B", pair=P.u, j=j, B=float(Bs[i]))
            stats["curves"] += 1
    # (c) bottleneck, (d) passage time
    ratios = {}
    for P in pairs:
        d = 1e-6 * P.h
        for v in (-0.02, -0.01, -0.005, 0.0, 0.005, 0.01, 0.02):
            D = P.sigma(P.h + d, P.L + v) - (P.L + v)
            r = D * P.h / (d + v * v / (2 * P.vt))
            if abs(r - 1) > 8 * abs(v) + 2e-3:
                return False, dict(reason="bottleneck expansion of the slope map", pair=P.u, v=v, ratio=r)
        cstar = math.pi * P.h * math.sqrt(2 * P.vt)
        prev = 0.0
        for dd, tol in ((1e-3, 0.2), (1e-4, 0.06)) + (() if quick else ((1e-5, 0.025),)):
            s, n = 0.0, 0
            while s <= P.L + 0.05:
                s = P.sigma(P.h * (1 + dd), s)
                n += 1
            r = math.sqrt(dd * P.h) * n / cstar
            if not (prev < r < 1.0 and 1 - r < tol):
                return False, dict(reason="passage time against pi h sqrt(2 theta_hint''(0)/delta)", pair=P.u, delta_over_h=dd, ratio=r)
            prev = r
        ratios[str(P.u)] = round(prev, 4)
    # (e) Proposition U and its negative control
    worst, least = -math.inf, math.inf
    for P, n in ((G, 6 if quick else 40), (C1, 2 if quick else 10)):
        for _ in range(n):
            r = rt_prop_u(P, rng, False)
            worst, least = max(worst, r), min(least, r)
            stats["prop_u"] += 1
    if worst > 1e-5:
        return False, dict(reason="Proposition U: the level operator exceeds the envelope of the image lines for a convex family", excess_over_a=worst)
    if least < -1e-5:
        return False, dict(reason="Proposition U: the bound is not attained at beta -> 0", deficit_over_a=least)
    ctrl = max(rt_prop_u(G, rng, True) for _ in range(4 if quick else 12))
    if ctrl < 1e-3:
        return True, dict(reason="harness: the negative control (a concave family of lines) shows no excess", ctrl=ctrl)
    # (f) the chain
    jmax = 40 if quick else 120
    wst, bs, exc = rt_chain(G, G.L + 0.05, G.h + 0.02, jmax)
    if wst > 1.0:
        return False, dict(reason="range condition of the chain fails (Gaussian pair, b_0 = h + 0.02)", largest=wst)
    if exc > 1e-9:
        return False, dict(reason="ratio of consecutive slopes at the cut exceeds its bound", excess=exc)
    r20 = [j * j * (b - G.h) / G.const for j, b in bs if j == 20][0]
    rend = bs[-1][0] ** 2 * (bs[-1][1] - G.h) / G.const
    if not (1.0 < rend < r20):
        return False, dict(reason="j^2 (b_j - h)/const does not decrease towards one from above", at_20=r20, at_end=rend)
    stats["chain_levels"] += jmax
    if not quick:
        wst_c, bs_c, exc_c = rt_chain(C1, C1.L + 0.05, C1.h + 0.003, 30)
        if wst_c > 1.0 or exc_c > 1e-9:
            return False, dict(reason="chain for the cube at u = 1", largest=wst_c, excess=exc_c)
        stats["chain_levels"] += 30
    wide, _, _ = rt_chain(G, G.L + 0.05, G.h + 0.15, 30)
    if wide <= 1.0:
        return True, dict(reason="harness: the wide start does not violate the range condition", largest=wide)
    # (g) the kinked pair
    K = RtPair('kink')
    for d in (1e-2, 1e-3):
        w0 = d / K.h
        smax = K.L2 - (1 - K.L2) * w0
        for s in (0.5, 0.55, 0.62, 0.7, smax):
            if abs(K.sigma(K.h + d, s) - s - w0) > 1e-12:
                return False, dict(reason="kinked pair: the step on the flat part is not delta/h", delta=d, s=s)
    for k in ((5, 20) if quick else (5, 20, 80, 200)):
        lo, hi = K.h, K.a
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if math.isfinite(K.orbit(mid, k)) else (lo, mid)
        if lo - K.h < (K.L2 - K.L1) * K.h / (k + 2) - 1e-12:
            return False, dict(reason="kinked pair: lower bound from lines below (L2 - L1) h/(k + 2)", k=k, value=lo - K.h)
    # (h) theta_hint''(0) through theta_na at its fixed point
    for P in pairs:
        e = P.h
        de = 1e-4 * e
        t0, tp, tm = P.theta_na(e), P.theta_na(e + de), P.theta_na(e - de)
        r1, r2 = (tm - tp) / (2 * de), (tp - 2 * t0 + tm) / de ** 2
        if abs(t0 - e) > 1e-9 or abs(r1 / (1 + r1) - P.L) > 1e-5 or abs(r2 / (1 + r1) ** 3 / P.vt - 1) > 1e-3:
            return False, dict(reason="theta_hint''(0) against theta_na''(h)/(1 + |theta_na'(h)|)^3", pair=P.u,
                               fixed_point_error=t0 - e, L=r1 / (1 + r1), ratio=r2 / (1 + r1) ** 3 / P.vt)
        d2 = 1e-4
        J2 = (P.J(P.L + d2) - 2 * P.J(P.L) + P.J(P.L - d2)) / d2 ** 2
        if abs(-1 / J2 / P.vt - 1) > 1e-4 or abs(P.J(P.L) - P.h) > 1e-12:
            return False, dict(reason="theta_hint''(0) against -1/J''(L), or max J against h", pair=P.u)
    stats.update(passage_ratio=ratios, prop_u_excess=worst, control=round(ctrl, 4), range_largest=round(wst, 4),
                 chain_ratio=(round(r20, 4), round(rend, 4)), wide_start=round(wide, 3))
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


@conjecture("XVII.5 Theorem 11.61, product samplers at vanishing accuracy (observation (a) of SCI-REV-0004): with a field p and slope u the Gibbs laws of the cones are the output laws of the binary channel W(.|b) = letter law of a cone whose centre has the letter b, the exponent a of non-adaptive algorithms at vanishing accuracy is its capacity max_m I(S;X), and by capacity = information radius the lower bound max(phi_0, phi_1)(0+) = max_b KL(W(.|b) || Bern(r)) for a product sampler Bern(r)^n has the minimum a over r, attained at the capacity-achieving OUTPUT marginal r* (not at r = p, and not at the optimal input m*): at u = 2 and logit p = -0.5, -1, -2, -3: a = 0.3162, 0.2836, 0.1841, 0.0928, r* = 0.4308, 0.3607, 0.2225, 0.1124, plain Monte Carlo 0.4078, 0.4621, 0.4338, 0.2732; at extensive accuracy the best product sampler is strictly worse than theta_na in the example (p, u, x) = (0.1, 2, 0.25 E)")
def t_field_product_sampler_capacity(rng, trials):
    u = 2.0
    kl = lambda x, y: x * math.log(x / y) + (1 - x) * math.log((1 - x) / (1 - y))
    hb = lambda x: -(x * math.log(x) + (1 - x) * math.log(1 - x))
    table = {-0.5: (0.3162, 0.4308, 0.4078), -1.0: (0.2836, 0.3607, 0.4621), -2.0: (0.1841, 0.2225, 0.4338), -3.0: (0.0928, 0.1124, 0.2732)}
    out = {}
    for lg, (a_ref, r_ref, mc_ref) in table.items():
        p = 1 / (1 + math.exp(-lg))
        q = 1 - p
        w0 = p * math.exp(-u) / (q + p * math.exp(-u))        # P(X = 1 | centre letter 0)
        w1 = p / (p + q * math.exp(-u))                       # P(X = 1 | centre letter 1)
        # capacity by golden section over the input law m = P(S = 1)
        mi = lambda m: hb(m * w1 + (1 - m) * w0) - m * hb(w1) - (1 - m) * hb(w0)
        negC, m_star = mf_golden(lambda m: -mi(m), 1e-9, 1 - 1e-9, tol=1e-13)
        C = -negC
        r_star = m_star * w1 + (1 - m_star) * w0
        # information radius: min over r of the larger divergence
        rad, r_min = mf_golden(lambda r: max(kl(w0, r), kl(w1, r)), w0 + 1e-12, w1 - 1e-12, tol=1e-13)
        mc = max(kl(w0, p), kl(w1, p))
        if abs(C - rad) > 1e-9 or abs(r_min - r_star) > 1e-6:
            return False, dict(reason="capacity = information radius, attained at the capacity-achieving output marginal", logit=lg, capacity=C, radius=rad, r_min=r_min, r_star=r_star)
        if abs(kl(w0, r_star) - C) > 1e-7 or abs(kl(w1, r_star) - C) > 1e-7:
            return False, dict(reason="both divergences equal the capacity at r*", logit=lg)
        if abs(C - a_ref) > 6e-5 or abs(r_star - r_ref) > 6e-5 or abs(mc - mc_ref) > 6e-5:
            return False, dict(reason="tabulated values", logit=lg, a=C, r_star=r_star, plain_monte_carlo=mc)
        if not (mc > C + 0.05 and abs(r_star - p) > 0.04 and abs(r_star - m_star) > 0.02):
            return False, dict(reason="plain Monte Carlo is strictly worse; r* is neither p nor the optimal input law", logit=lg, p=p, r_star=r_star, m_star=m_star)
        out[lg] = (round(C, 5), round(r_star, 5))
    # extensive accuracy: (p, u, x) = (0.1, 2, 0.25 E): the best product sampler has 0.0451 against theta_na = 0.0440 (Theorem 11.61)
    p, q = 0.1, 0.9
    eta0 = p * math.exp(-u) / (q + p * math.exp(-u))          # the letter differs from the centre letter 0
    eta1 = q * math.exp(-u) / (p + q * math.exp(-u))          # the letter differs from the centre letter 1
    E = 0.212295                                              # the threshold of the field case (Theorem 11.59; THY-MSG-0009 section 3.1)
    x = 0.25 * E

    def phi(prior, eta):
        if prior <= eta or kl(prior, eta) <= x:
            return 0.0
        lo, hi = eta, prior
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if kl(mid, eta) < x:
                lo = mid
            else:
                hi = mid
        return kl(0.5 * (lo + hi), prior)
    best, r_best = mf_golden(lambda r: max(phi(r, eta0), phi(1 - r, eta1)), 0.02, 0.6, tol=1e-10)
    if abs(best - 0.0451) > 2e-4 or best < 0.0440 + 5e-4:
        return False, dict(reason="at the extensive accuracy 0.25 E the best product sampler has 0.0451 > theta_na = 0.0440", best=best, r=r_best)
    return True, dict(values=out, best_product_at_extensive_accuracy=best, r=r_best)


@conjecture("XVII.6 The product sampler with the capacity-achieving output marginal is exponent-optimal on the whole class at bounded accuracy (theory report Proposition 11.61a; Proposition A1.1 of the science division, SCI-RES-0001 / SCI-MSG-0011): for the known part Bernoulli(p)^n and every u-Lipschitz residual psi, each conditional law of a coordinate of the Gibbs measure nu_psi given a prefix is Bernoulli with parameter between the letter laws a0 = sigma(logit p - u), a1 = sigma(logit p + u) of the two extreme cones; hence KL(nu_psi || Bernoulli(r)^n) <= n max(KL(a0||r), KL(a1||r)), which at r = r* (equal relative entropies) is n a, a the information radius = the exponent of non-adaptive algorithms at vanishing accuracy, with equality at cones; the increments of the log-likelihood ratio have range at most 2u; and E_Q[rho^2 1{rho <= tau}] <= tau for the density ratio rho (the truncation step of the importance-sampling bound)")
def t_product_sampler_optimal(rng, trials):
    from scipy.optimize import brentq
    sig = lambda t: 1 / (1 + math.exp(-t))
    kl = lambda a, b: a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b))
    stats = dict(instances=0, worst=0.0, cone_ratio=0.0)
    for rep in range(max(120, trials // 2)):
        n = int(rng.integers(3, 10))
        p, u = float(rng.uniform(0.05, 0.6)), float(rng.uniform(0.3, 3.0))
        a0, a1 = sig(math.log(p / (1 - p)) - u), sig(math.log(p / (1 - p)) + u)
        r = brentq(lambda t: kl(a0, t) - kl(a1, t), a0 + 1e-12, a1 - 1e-12)
        a = kl(a0, r)
        vals = [math.log(t / r) for t in (a0, a1)] + [math.log((1 - t) / (1 - r)) for t in (a0, a1)]
        if max(vals) - min(vals) > 2 * u + 1e-9:
            return False, dict(reason="range of the log-likelihood increments exceeds 2u")
        X = np.array(list(itertools.product((0, 1), repeat=n)))
        kind = rep % 4
        centre = X[int(rng.integers(len(X)))]
        dist = np.abs(X - centre).sum(axis=1)
        if kind == 0:
            psi = u * dist                                                     # cone
        elif kind == 1:
            psi = -u * dist                                                    # inverted cone
        elif kind == 2:
            psi = u * np.maximum(dist, int(rng.integers(0, n)))                # truncated cone
        else:                                                                  # lower envelope of random cones
            k = int(rng.integers(1, 8))
            idx = rng.choice(len(X), size=k, replace=False)
            psi = (rng.uniform(-u * n, u * n, size=k)[None, :] + u * np.abs(X[:, None, :] - X[idx][None, :, :]).sum(axis=2)).min(axis=1)
        w = np.exp(-(psi - psi.min())) * np.prod(np.where(X == 1, p, 1 - p), axis=1)
        nu = w / w.sum()
        Q = np.prod(np.where(X == 1, r, 1 - r), axis=1)
        KL = float((nu * np.log(nu / Q)).sum())
        if KL > n * a + 1e-9:
            return False, dict(reason="KL(nu_psi || Bernoulli(r*)^n) exceeds n a", KL=KL, bound=n * a)
        stats["worst"] = max(stats["worst"], KL / (n * a))
        if kind == 0 and (centre.sum() in (0, n)):
            stats["cone_ratio"] = max(stats["cone_ratio"], KL / (n * a))
        for k in range(n):
            keys = X[:, :k] @ (1 << np.arange(k)) if k else np.zeros(len(X), dtype=int)
            s1 = np.bincount(keys, weights=nu * (X[:, k] == 1), minlength=1 << k)
            s0 = np.bincount(keys, weights=nu * (X[:, k] == 0), minlength=1 << k)
            t = s1 / (s0 + s1)
            if t.min() < a0 - 1e-12 or t.max() > a1 + 1e-12:
                return False, dict(reason="a conditional law outside the interval of the two letter laws")
        rho = nu / Q
        for tau in (1.0, math.exp(n * a / 2), math.exp(n * a)):
            if float((Q * rho ** 2 * (rho <= tau)).sum()) > tau + 1e-9:
                return False, dict(reason="truncated second moment exceeds tau")
        stats["instances"] += 1
    # the constant-centre cones attain the bound in the limit (ratio -> 1); and r = p would not do
    if stats["worst"] < 0.9:
        return False, dict(reason="the bound n a is never approached", worst=stats["worst"])
    a0, a1 = sig(math.log(0.1192 / 0.8808) - 2.0), sig(math.log(0.1192 / 0.8808) + 2.0)
    r = brentq(lambda t: kl(a0, t) - kl(a1, t), a0 + 1e-12, a1 - 1e-12)
    if abs(r - 0.2225) > 2e-4 or abs(kl(a0, r) - 0.18409) > 2e-4 or not max(kl(a0, 0.1192), kl(a1, 0.1192)) > 2 * kl(a0, r):
        return False, dict(reason="reference values at p = 0.1192, u = 2", r=r, a=kl(a0, r))
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


@conjecture("XVIII.7 Bridges with clean ends form an exact semigroup (theory report Proposition 11.69b; request T-4 of the Scientific Discovery Division's review SCI-REV-0006): call a bridge clean if the bond before its last bond is an up-bond and neither the linker of Lemma 11.68 placed above it nor the one placed below it has a pair within the cutoff with the bridge beyond the chain neighbours (equivalently: concatenating a three-bead bridge above it, or below it, changes (h, g) by nothing); then the concatenation of two clean bridges is a clean bridge with N1 + N2 + 3 beads and exactly additive (h3, h8, h11, g); every bridge becomes clean when a three-bead bridge is concatenated below and above it, at a cost within the constants of Lemma 11.68; not every bridge is clean, and for some pairs of bridges that are not clean the concatenation error does not vanish (not for all: Scientific Discovery Division, SCI-REV-0011)")
def t_ls_exact_semigroup(rng, trials):
    nmax = 8              # up to 7 beads a bridge is clean iff the bond before its last bond is an up-bond; from 8 beads on not
    br = {N: ls_enum(N, bridge=True) for N in range(3, nmax + 1)}
    z3 = br[3][0]
    prof = lambda w: ls_profile(w)
    diff = lambda a, b, c=None: tuple(a[k] - b[k] - (c[k] if c else 0) for k in range(4))

    def up_before_last(w):
        return w[-2][1] - w[-3][1] == 1

    def clean(w):
        if not up_before_last(w):
            return False
        top, _, n1 = ls_concat(w, z3, 0)
        bot, _, n2 = ls_concat(z3, w, 0)
        return n1 == 1 and n2 == 1 and diff(prof(top), prof(w)) == (0, 0, 0, 0) and diff(prof(bot), prof(w)) == (0, 0, 0, 0)

    if prof(z3) != (0, 0, 0, 0) or not clean(z3):
        return False, dict(reason="the three-bead bridge is not a clean bridge with (h, g) = 0")
    stats = dict(bridges=0, clean=0, pairs=0, made_clean=0, max_cost=(0, 0, 0, 0), dirty_pairs_with_error=0)
    members = []
    for N in br:
        for w in br[N]:
            stats["bridges"] += 1
            if clean(w):
                stats["clean"] += 1
                members.append(w)
            if N <= nmax - 1:                                                # a three-bead bridge below and above
                for which in ((0, 1) if not up_before_last(w) else (0,)):
                    y1, _, _ = ls_concat(z3, w, 0)
                    y, _, _ = ls_concat(y1, z3, which)
                    if not (ls_valid_walk(y) and ls_is_bridge(y) and len(y) == N + 12):
                        return False, dict(reason="head and tail do not give a bridge with N + 12 beads", N=N)
                    if not clean(y):
                        return False, dict(reason="a bridge with a three-bead bridge below and above it is not clean", N=N)
                    d = diff(prof(y), prof(w))
                    if not (0 <= d[0] <= 2 and 0 <= d[1] <= 18 and 0 <= d[2] <= 28 and 0 <= d[3] <= 2):
                        return False, dict(reason="the cost of head and tail exceeds twice the constants of Lemma 11.68", d=d)
                    stats["max_cost"] = tuple(max(a, b) for a, b in zip(stats["max_cost"], d))
                    stats["made_clean"] += 1
    if stats["clean"] in (0, stats["bridges"]):
        return False, dict(reason="clean bridges: none, or all", **stats)
    for _ in range(max(300, 2 * trials)):
        x1, x2 = members[int(rng.integers(len(members)))], members[int(rng.integers(len(members)))]
        y, down, ncop = ls_concat(x1, x2, 0)
        if ncop != 1 or down or not (ls_valid_walk(y) and ls_is_bridge(y) and len(y) == len(x1) + len(x2) + 3):
            return False, dict(reason="the concatenation of two clean bridges is not a bridge with N1 + N2 + 3 beads")
        if diff(prof(y), prof(x1), prof(x2)) != (0, 0, 0, 0):
            return False, dict(reason="(h, g) is not exactly additive on clean bridges", d=diff(prof(y), prof(x1), prof(x2)))
        if len(y) <= 16 and not clean(y):
            return False, dict(reason="the concatenation of two clean bridges is not clean", N=len(y))
        stats["pairs"] += 1
    for x in members:                                                        # every clean bridge of the largest size with itself
        if len(x) == nmax:
            y, down, ncop = ls_concat(x, x, 0)
            if diff(prof(y), prof(x), prof(x)) != (0, 0, 0, 0):
                return False, dict(reason="(h, g) is not exactly additive on clean bridges", d=diff(prof(y), prof(x), prof(x)))
            stats["pairs"] += 1
    dirty = [w for N in br for w in br[N] if not clean(w)]
    stats["up_but_not_clean"] = sum(1 for w in dirty if up_before_last(w))
    if stats["up_but_not_clean"] == 0:
        return False, dict(reason="no bridge whose bond before the last is an up-bond fails to be clean: the two conditions on the ends would be vacuous", **stats)
    for _ in range(200):
        x1, x2 = dirty[int(rng.integers(len(dirty)))], dirty[int(rng.integers(len(dirty)))]
        y, down, ncop = ls_concat(x1, x2, 0)
        stats["dirty_pairs_with_error"] += int(diff(prof(y), prof(x1), prof(x2)) != (0, 0, 0, 0))
    if stats["dirty_pairs_with_error"] == 0:
        return False, dict(reason="no concatenation error among bridges that are not clean: the restriction would be empty", **stats)
    return True, stats


@conjecture("XVIII.8 The concatenation error of bridges is a coboundary (theory report Proposition 11.69b as adopted at the eighteenth checkpoint: Theorem R9.1(a)-(e) of the Scientific Discovery Division, SCI-REV-0009; verified exhaustively up to 14 and 22 beads in experiments/coordinator_checks/limit_shape_review/r9/).  For a bridge x with last bond b and bond before it b', a bond c1 is admissible if c1 = b' when b' is an up-bond and if c1 is an up-bond out of the last bead otherwise; t1 = last + c1, t2 = t1 + b, t3 = t2 + c1 are beads N, N+1, N+2 and s1 = x0 - u2, s2 = s1 - u1, s3 = s2 - u2 beads -1, -2, -3; A(x, c1) counts the pairs (t_j, x_p) at chain separation at least 3 at squared distance 3, 8, 11, followed by [b' is a down-bond], and B(x) the same for the s_j, followed by 0.  Then (a) (h, g)(x1 o x2) = (h, g)(x1) + (h, g)(x2) + A(x1, c1) + B(x2), B(x1 o x2) = B(x1), and A(x1 o x2, phi(c1'')) = A(x2, c1'') for every bond admissible for x2, the phi(c1'') being the bonds admissible for the concatenation: (h, g) + A + B is exactly additive for all bridges; (b) clean bridges (b' up, A = 0, B = 0 - the same set as in XVIII.7) concatenate to clean bridges; (c) a head of two beads and a tail of three turn every bridge into a clean one with (h, g) = (h, g)(x) + A(x, c1) + B(x), a head of one bead fails for a bridge with 8 beads and a tail of two for a bridge with 12; 0 <= A <= (1, 6, 10; 1) and 0 <= B <= (0, 3, 4; 0), both attained, so that the concatenation of a bridge with 21 beads and one with 14 has the error (1, 9, 14; 1) of norm 60; (d) (h, g)/N is within 108/(N + 3) of the exact point ((h, g) + A + B)/(N + 3); (e) five clean bridges with 4, 5, 7, 8, 10 beads have vectors (h3, h8, h11, g; N + 3) of determinant 1")
def t_ls_coboundary(rng, trials):
    add = lambda p, v: (p[0] + v[0], p[1] + v[1], p[2] + v[2])
    sub = lambda p, q: (p[0] - q[0], p[1] - q[1], p[2] - q[2])
    neg = lambda v: (-v[0], -v[1], -v[2])
    vsum = lambda *vs: tuple(sum(v[k] for v in vs) for k in range(4))

    def admissible(x):
        bp = sub(x[-2], x[-3])
        if bp[1] == 1:
            return [bp]
        return [sub(q, x[-1]) for q in ls_nbrs(x[-1]) if q[1] == x[-1][1] + 1]

    def above(x, c1):
        b = sub(x[-1], x[-2])
        t1 = add(x[-1], c1); t2 = add(t1, b); t3 = add(t2, c1)
        return [t1, t2, t3]

    def below(x):
        u1, u2 = sub(x[1], x[0]), sub(x[2], x[1])
        s1 = add(x[0], neg(u2)); s2 = add(s1, neg(u1)); s3 = add(s2, neg(u2))
        return [s1, s2, s3]

    def end_counts(x, sites, index_of_site):
        cnt = [0, 0, 0]
        for j, s in enumerate(sites):
            for p, xp in enumerate(x):
                if abs(index_of_site(j) - p) >= 3:                    # chain separation at least 3
                    d = ls_sq(s, xp)
                    if d in (3, 8, 11):
                        cnt[(3, 8, 11).index(d)] += 1
        return cnt

    def A_of(x, c1):
        N = len(x)
        down = sub(x[-2], x[-3])[1] == -1
        return tuple(end_counts(x, above(x, c1), lambda j: N + j)) + (int(down),)

    def B_of(x):
        return tuple(end_counts(x, below(x), lambda j: -1 - j)) + (0,)

    def is_clean(x):
        bp = sub(x[-2], x[-3])
        return bp[1] == 1 and A_of(x, bp) == (0, 0, 0, 0) and B_of(x) == (0, 0, 0, 0)

    def concat(x1, c1, x2):
        """x1, t1, t2, t3, phi(x2); phi the height-preserving signed permutation that maps the first two bonds of x2 to (c1, b)"""
        b = sub(x1[-1], x1[-2])
        t = above(x1, c1)
        Q = add(t[2], b)
        u1, u2 = sub(x2[1], x2[0]), sub(x2[2], x2[1])
        maps = []
        for perm, sg in LS_SIGNED_PERMS:
            if (perm[1], sg[1]) != (1, 1):
                continue
            phi = lambda v, perm=perm, sg=sg: (sg[0] * v[perm[0]], sg[1] * v[perm[1]], sg[2] * v[perm[2]])
            if phi(u1) == c1 and phi(u2) == b:
                maps.append(phi)
        if len(maps) != 1:
            return None, None
        phi = maps[0]
        return x1 + t + [add(Q, phi(sub(p, x2[0]))) for p in x2], phi

    def extend(x, c1, head, tail):
        s, t = below(x), above(x, c1)
        return list(reversed(s[:head])) + x + t[:tail]

    stats = dict(bridges=0, pairs=0, nonzero_error=0, with_B=0, two_bonds_differ=0, clean_pairs=0, cleaned=0,
                 head1_fails=0, largest_A=(0, 0, 0, 0), largest_B=(0, 0, 0, 0), closest_108=0.0)
    nmax = 9
    br = [w for N in range(3, nmax + 1) for w in ls_enum(N, bridge=True)]
    info = []
    for x in br:
        hg = ls_profile(x)
        ad = admissible(x)
        As = [A_of(x, c) for c in ad]
        Bx = B_of(x)
        info.append((x, hg, ad, As, Bx))
        stats["bridges"] += 1
        if any(a > m for A in As for a, m in zip(A, (1, 6, 10, 1))) or any(a > m for a, m in zip(Bx, (0, 3, 4, 0))) \
                or min(min(A) for A in As) < 0 or min(Bx) < 0:
            return False, dict(reason="an end correction leaves the box [0, (1, 6, 10; 1)] or [0, (0, 3, 4; 0)]", N=len(x))
        for A in As:
            stats["largest_A"] = tuple(max(a, b) for a, b in zip(stats["largest_A"], A))
        stats["largest_B"] = tuple(max(a, b) for a, b in zip(stats["largest_B"], Bx))
        if len(As) == 2 and As[0] != As[1]:
            stats["two_bonds_differ"] += 1
        # (c) head 2 + tail 3; (d) the exact point
        N = len(x)
        for c, A in zip(ad, As):
            head, tail = 2, 3                                            # the claim of (c): two and three beads
            xh = extend(x, c, head, tail)
            if not (ls_valid_walk(xh) and ls_is_bridge(xh) and len(xh) == N + head + tail):
                return False, dict(reason="head and tail do not give a bridge", N=N)
            if not is_clean(xh):
                return False, dict(reason="a bridge with a head of two beads and a tail of three is not clean", N=N, x=x)
            if ls_profile(xh) != vsum(hg, A, Bx):
                return False, dict(reason="(h, g) of the cleaned bridge is not (h, g) + A + B", N=N)
            stats["cleaned"] += 1
            x1h = extend(x, c, 1, 3)
            if not is_clean(x1h):
                stats["head1_fails"] += 1
                if N < 8:
                    return False, dict(reason="a head of one bead fails below 8 beads", N=N)
            q = vsum(hg, A, Bx)
            dlt = [hg[k] / N - q[k] / (N + 3) for k in range(4)]
            dist = ls_cnorm(dlt[:3]) + abs(dlt[3])
            if dist > 108 / (N + 3) + 1e-12:
                return False, dict(reason="(h, g)/N is farther than 108/(N + 3) from the exact point", N=N, dist=dist)
            stats["closest_108"] = max(stats["closest_108"], dist * (N + 3) / 108)
    # the definition of clean agrees with the one of XVIII.7 (a three-bead bridge above or below changes nothing)
    z3 = ls_enum(3, bridge=True)[0]
    for x, hg, ad, As, Bx in info:
        if len(x) > 8:
            continue
        old = False
        if sub(x[-2], x[-3])[1] == 1:
            top, _, n1 = ls_concat(x, z3, 0)
            bot, _, n2 = ls_concat(z3, x, 0)
            old = n1 == 1 and n2 == 1 and ls_profile(top) == hg and ls_profile(bot) == hg
        if old != is_clean(x):
            return False, dict(reason="the two definitions of a clean bridge differ", x=x)

    def check_pair(i1, k1, i2):
        x1, hg1, ad1, As1, B1 = info[i1]
        x2, hg2, ad2, As2, B2 = info[i2]
        c1 = ad1[k1]
        y, phi = concat(x1, c1, x2)
        if y is None or not (ls_valid_walk(y) and ls_is_bridge(y) and len(y) == len(x1) + len(x2) + 3):
            return dict(reason="the concatenation is not a bridge with N1 + N2 + 3 beads, or the symmetry is not unique")
        hy = ls_profile(y)
        if hy != vsum(hg1, hg2, As1[k1], B2):
            return dict(reason="(h, g)(x1 o x2) is not (h, g)(x1) + (h, g)(x2) + A(x1, c1) + B(x2)",
                        got=hy, want=vsum(hg1, hg2, As1[k1], B2))
        if B_of(y) != B1:
            return dict(reason="B(x1 o x2) is not B(x1)")
        ady = admissible(y)
        if sorted(ady) != sorted(phi(c) for c in ad2):
            return dict(reason="the bonds admissible for the concatenation are not the images of those admissible for x2")
        for c2, A2 in zip(ad2, As2):
            if A_of(y, phi(c2)) != A2:
                return dict(reason="A(x1 o x2, phi(c1'')) is not A(x2, c1'')")
        cl = is_clean(y)
        want_clean = B1 == (0, 0, 0, 0) and sub(x2[-2], x2[-3])[1] == 1 and As2[0] == (0, 0, 0, 0)
        if cl != want_clean:
            return dict(reason="the concatenation is clean in the wrong cases")
        stats["pairs"] += 1
        stats["nonzero_error"] += int(vsum(As1[k1], B2) != (0, 0, 0, 0))
        stats["with_B"] += int(B2 != (0, 0, 0, 0))
        if is_clean(x1) and is_clean(x2):
            if not cl or hy != vsum(hg1, hg2):
                return dict(reason="two clean bridges do not concatenate to a clean bridge with exactly additive (h, g)")
            stats["clean_pairs"] += 1
        return None

    small = [i for i, t in enumerate(info) if len(t[0]) <= 5]
    for i1 in small:
        for i2 in small:
            for k1 in range(len(info[i1][2])):
                bad = check_pair(i1, k1, i2)
                if bad:
                    return False, bad
    withB = [i for i, t in enumerate(info) if t[4] != (0, 0, 0, 0)]
    withA = [i for i, t in enumerate(info) if any(A[:3] != (0, 0, 0) for A in t[3])]
    if not withB or not withA:
        return False, dict(reason="no bridge with a nonzero end correction among the bridges tested", **stats)
    todo = [(int(rng.integers(len(info))), int(rng.integers(len(info)))) for _ in range(max(150, trials))]
    todo += [(int(rng.integers(len(info))), i2) for i2 in withB[:: max(1, len(withB) // 40)]]
    todo += [(i1, int(rng.integers(len(info)))) for i1 in withA[:: max(1, len(withA) // 40)]]
    for i1, i2 in todo:
        for k1 in range(len(info[i1][2])):
            bad = check_pair(i1, k1, i2)
            if bad:
                return False, bad

    # (c) a tail of two beads fails for a bridge with 12 beads (Scientific Discovery Division, SCI-REV-0011, section 2)
    x12 = [(0, 0, 0), (1, 1, 1), (0, 2, 2), (1, 3, 3), (2, 2, 4), (3, 3, 5), (4, 2, 6), (5, 1, 5), (6, 2, 4), (5, 3, 3),
           (4, 2, 2), (3, 3, 1)]
    c12 = (-1, 1, 1)
    if not (ls_valid_walk(x12) and ls_is_bridge(x12) and c12 in admissible(x12)):
        return False, dict(reason="the 12-bead example is not a bridge with the stated admissible bond")
    if is_clean(extend(x12, c12, 2, 2)) or not is_clean(extend(x12, c12, 2, 3)):
        return False, dict(reason="for the 12-bead example a tail of two beads should fail and a tail of three succeed")
    # attainment of the bounds, and of beta = 60
    xa = [(0, 0, 0), (1, 1, 1), (0, 2, 2), (-1, 1, 3), (-2, 2, 4), (-3, 3, 3), (-4, 4, 4), (-5, 3, 5), (-4, 2, 6), (-3, 3, 7),
          (-2, 4, 6), (-1, 3, 5), (0, 4, 4), (1, 3, 3), (2, 4, 2), (3, 3, 1), (2, 2, 0), (1, 3, -1), (0, 4, 0), (-1, 3, 1),
          (-2, 4, 2)]
    xb = [(0, 0, 0), (1, 1, 1), (0, 2, 2), (-1, 3, 1), (-2, 2, 0), (-1, 1, -1), (0, 2, -2), (1, 1, -3), (2, 2, -4), (3, 3, -3),
          (4, 2, -2), (3, 1, -1), (2, 2, 0), (1, 3, -1)]
    ca = (1, 1, 1)
    if not (ls_valid_walk(xa) and ls_is_bridge(xa) and ls_valid_walk(xb) and ls_is_bridge(xb) and ca in admissible(xa)):
        return False, dict(reason="the extremal bridges are not bridges")
    if A_of(xa, ca) != (1, 6, 10, 1) or B_of(xb) != (0, 3, 4, 0):
        return False, dict(reason="the bounds (1, 6, 10; 1) and (0, 3, 4; 0) are not attained by the stated bridges",
                           A=A_of(xa, ca), B=B_of(xb))
    y, _ = concat(xa, ca, xb)
    err = tuple(a - b - c for a, b, c in zip(ls_profile(y), ls_profile(xa), ls_profile(xb)))
    if err != (1, 9, 14, 1) or ls_cnorm(err[:3]) + err[3] != 60:
        return False, dict(reason="the concatenation of the extremal pair does not have the error (1, 9, 14; 1) of norm 60", err=err)
    # (e) five clean bridges whose vectors (h3, h8, h11, g; N + 3) have determinant 1
    five = [[(0, 0, 0), (1, 1, 1), (0, 2, 2), (-1, 3, 1)],
            [(0, 0, 0), (1, 1, 1), (0, 2, 2), (1, 3, 3), (2, 4, 2)],
            [(0, 0, 0), (1, 1, 1), (0, 2, 2), (-1, 3, 1), (-2, 2, 0), (-3, 3, -1), (-4, 4, 0)],
            [(0, 0, 0), (1, 1, 1), (0, 2, 2), (1, 3, 3), (2, 2, 4), (3, 1, 3), (4, 2, 2), (5, 3, 3)],
            [(0, 0, 0), (1, 1, 1), (0, 2, 2), (-1, 1, 3), (-2, 2, 4), (-1, 3, 5), (0, 4, 4), (1, 3, 3), (2, 4, 2), (3, 5, 3)]]
    rows = []
    for w in five:
        if not (ls_valid_walk(w) and ls_is_bridge(w) and is_clean(w)):
            return False, dict(reason="one of the five bridges of the lattice certificate is not a clean bridge")
        rows.append([Fraction(v) for v in ls_profile(w)] + [Fraction(len(w) + 3)])
    det = Fraction(1)
    for col in range(5):                                           # exact elimination
        piv = next((r for r in range(col, 5) if rows[r][col] != 0), None)
        if piv is None:
            det = Fraction(0); break
        if piv != col:
            rows[col], rows[piv] = rows[piv], rows[col]; det = -det
        det *= rows[col][col]
        for r in range(col + 1, 5):
            f = rows[r][col] / rows[col][col]
            rows[r] = [a - f * b for a, b in zip(rows[r], rows[col])]
    if abs(det) != 1:
        return False, dict(reason="the five vectors of the lattice certificate do not have determinant +-1", det=str(det))
    if not (stats["nonzero_error"] > 20 and stats["with_B"] > 10 and stats["two_bonds_differ"] > 0 and stats["clean_pairs"] > 50
            and stats["head1_fails"] > 0 and stats["pairs"] > 1000):
        return False, dict(reason="cases not exercised", **stats)
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


def rd_candidate_set(L, U, s, K, m_max, nu, c_eta, eta, b, ell0):
    """Candidate set of the batched schedule (theory report Theorem 11.84): member i (1-based position i + 1) iff for
    some level j: i + 1 <= Mhat_j, U_i > s_j, L_i <= s_j e^{-b}, with lambda_j and Mhat_j computed from the stored lower
    ends as in the theorem.  Returns the boolean membership vector and the vector Mhat."""
    passes = np.array([K * 2 ** m for m in range(m_max + 1)])
    cum = np.cumsum(L[None, :] > s[:, None], axis=1)
    NL = cum[:, passes - 1]                                                  # N_L(i', M): levels x passes
    dens = np.where(NL >= K, s[:, None] * NL / passes[None, :], 0.0).max(axis=1)
    best_prev = np.concatenate([[0.0], np.maximum.accumulate(dens)[:-1]])    # max over i' < j
    lam_j = np.maximum(ell0, c_eta / (1 + eta) * math.exp(-b) * best_prev)
    Mhat = np.maximum(K, 2 * nu * s / (lam_j * math.exp(b)))
    pos = np.arange(1, len(L) + 1)
    member = np.zeros(len(L), dtype=bool)
    for j in range(len(s)):
        member |= (pos <= Mhat[j]) & (U > s[j]) & (L <= s[j] * math.exp(-b))
    return member, Mhat


@conjecture("XX.5 Theorem 11.84, Claim B and the stopping rule (after the Scientific Discovery Division's finding M1, SCI-REV-0003): for arbitrary stored brackets [L_i, U_i] of ratio at most e^x — in adversarial orders and distributions, valid or not — the candidate set of the next stage has at most N = K + (J+1) max(K, 4(1+eta) c_eta^{-1} e^lambda nu e^x) members; with wider brackets the count fails (all stored brackets trivial: the candidate set is everything), and then the rule 'stop if |C| > N' fires before any evaluation, so that the stage never runs on more than N fibres")
def t_rounds_candidate_set(rng, trials):
    stats = dict(cases=0, worst_fill=0.0, wide_cases=0)
    for rep in range(max(40, trials // 8)):
        lam = float(rng.choice([0.25, 0.5, 1.0]))
        eta = float(rng.choice([0.25, 0.5]))
        c_eta = (1 - eta) / (1 + eta)
        J = int(rng.integers(12, 40))
        K = int(rng.integers(4, 12))
        m_max = int(rng.integers(11, 15))
        nu = K * float(rng.uniform(1.0, 3.0))
        x = float(rng.uniform(0.3, 2.0))
        b = float(rng.uniform(0.1, 1.0)) * x
        s = np.exp(lam * np.arange(J + 1))                                    # s_0 = ell_0 = 1
        Mmax = K * 2 ** m_max
        N = K + (J + 1) * max(K, 4 * (1 + eta) / c_eta * math.exp(lam) * nu * math.exp(x))
        kind = rep % 5
        if kind == 0:
            lnL = rng.uniform(0, lam * J, size=Mmax)
        elif kind == 1:                                                       # concentrated just above one level
            lnL = lam * int(rng.integers(1, J)) + rng.uniform(-x, x, size=Mmax)
        elif kind == 2:                                                       # heavy lower tail, a few large values
            lnL = lam * J * rng.random(Mmax) ** 6
        elif kind == 3:                                                       # sorted: large values first
            lnL = -np.sort(-rng.uniform(0, lam * J, size=Mmax))
        else:                                                                 # sorted: large values last
            lnL = np.sort(lam * J * rng.random(Mmax) ** 3)
        lnL = np.clip(lnL, 0.0, lam * J)
        L = np.exp(lnL)
        U = L * np.exp(x * rng.random(Mmax) ** float(rng.choice([0.2, 1.0, 5.0])))
        member, _ = rd_candidate_set(L, U, s, K, m_max, nu, c_eta, eta, b, 1.0)
        if member.sum() > N:
            return False, dict(reason="Claim B violated: brackets of ratio at most e^x, but more than N candidates", candidates=int(member.sum()), N=N, kind=kind)
        stats["cases"] += 1
        stats["worst_fill"] = max(stats["worst_fill"], float(member.sum()) / N)
        # the same positions with trivial brackets: everything is a candidate; the rule fires whenever N < M_max
        Lw, Uw = np.ones(Mmax), np.full(Mmax, float(s[-1]) * math.exp(lam))
        wide, Mhat = rd_candidate_set(Lw, Uw, s, K, m_max, nu, c_eta, eta, b, 1.0)
        expect = min(Mmax, int(Mhat.max()))
        if int(wide.sum()) != expect:
            return False, dict(reason="with trivial brackets the candidate set is not the first max_j Mhat_j positions", got=int(wide.sum()), expected=expect)
        if N < Mmax and expect == Mmax:
            stats["wide_cases"] += 1                                          # here 'in every run' fails and the rule fires
    if stats["wide_cases"] == 0:
        return False, dict(reason="no case in which trivial brackets exceed N: the stopping rule was not exercised")
    # the case in which the empirical lower bounds lambda_j are what keeps the set small: all stored brackets equal,
    # of ratio e^x, straddling one high level (the flat instance with an honest inner procedure)
    lam, eta, J, K, m_max, x, b, nu = 0.5, 0.5, 30, 6, 14, 1.0, 0.5, 6.0
    c_eta = (1 - eta) / (1 + eta)
    s = np.exp(lam * np.arange(J + 1))
    Mmax = K * 2 ** m_max
    N = K + (J + 1) * max(K, 4 * (1 + eta) / c_eta * math.exp(lam) * nu * math.exp(x))
    for jstar in (8, 15, 22, 29):
        for alpha in (0.05, 0.5, 0.95):
            Lb = float(s[jstar]) * math.exp(-b - alpha * (x - b))
            same, Mhat = rd_candidate_set(np.full(Mmax, Lb), np.full(Mmax, Lb * math.exp(x)), s, K, m_max, nu, c_eta, eta, b, 1.0)
            if same.sum() > N:
                return False, dict(reason="equal honest brackets: more than N candidates", candidates=int(same.sum()), N=round(N), level=jstar)
            stats["flat_max"] = max(stats.get("flat_max", 0), int(same.sum()))
    if not 0 < stats["flat_max"] < Mmax:
        return False, dict(reason="flat case: the candidate set is empty or everything", flat_max=stats["flat_max"])
    return True, stats


# -----------------------------------------------------------------------------------------------------------------
# XXI. Slices: for fixed samples and with a hint, no function-of-type known part is harder than the uniform cube (11.25)
# -----------------------------------------------------------------------------------------------------------------
def sl_kl(a, b):
    """KL(Bernoulli(a) || Bernoulli(b)), vectorised in a, with 0 ln 0 = 0."""
    a = np.clip(np.asarray(a, float), 0.0, 1.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(a > 0, a * np.log(a / b), 0.0) + np.where(a < 1, (1 - a) * np.log((1 - a) / (1 - b)), 0.0)


def sl_hi(m, k):
    """End of the ray of two-block profiles of type k around a centre of type m (towards the centre)."""
    return min(2 * m * (1 - k), 2 * (1 - m) * k)


def sl_F(m, k, l):
    """MI of the two-block profile (k + l/2m, k - l/(2(1-m))) inside the slice of density k (distance l from the mixed profile)."""
    return float(m * sl_kl(k + l / (2 * m), k) + (1 - m) * sl_kl(k - l / (2 * (1 - m)), k))


def sl_Psi(m, k, s):
    """Legendre transform of F on l >= 0."""
    if s <= 0:
        return 0.0
    return -mf_golden(lambda l: -(s * l - sl_F(m, k, l)), 0.0, sl_hi(m, k) * (1 - 1e-13), tol=1e-13)[0]


def sl_V(m, k, u, e):
    """Hinted value of a centre of type m on the slice k: the supremum over its shells, in closed form."""
    P = sl_Psi(m, k, u)
    return sl_F(m, k, (P - e) / u) if P > e else 0.0


def sl_N(m, k, u, X):
    """Non-adaptive value of a centre of type m on the slice k: F(l_X), u l_X - F(l_X) = Psi(u) - X on the rising branch."""
    P = sl_Psi(m, k, u)
    if X >= P:
        return 0.0
    lstar = mf_golden(lambda l: -(u * l - sl_F(m, k, l)), 0.0, sl_hi(m, k) * (1 - 1e-13), tol=1e-13)[1]
    a, b = 0.0, lstar
    for _ in range(60):
        mid = 0.5 * (a + b)
        if u * mid - sl_F(m, k, mid) <= P - X:
            a = mid
        else:
            b = mid
    return sl_F(m, k, 0.5 * (a + b))


def sl_clip(lam, mu, k, c_lo):
    """The clipping nu_j = min(max(mu_j, c_lo), c_hi) of type k (c_lo <= k <= c_hi); returns (nu, dist(nu, mu))."""
    lo = np.maximum(mu, c_lo)
    a, b = k, 1.0
    if float(np.dot(lam, np.minimum(lo, k))) >= k:
        b = k
    else:
        for _ in range(60):
            mid = 0.5 * (a + b)
            if float(np.dot(lam, np.minimum(lo, mid))) <= k:
                a = mid
            else:
                b = mid
    nu = np.minimum(lo, b)
    return nu, float(np.dot(lam, np.abs(nu - mu)))


def sl_r(lam, mu, k, u, e):
    """min{ MI(nu) : type of nu = k, u dist(nu, mu) <= e + MI(mu) } for a profile with any number of blocks (clipping,
    Lemma 11.77(a); along the path c_lo: 0 -> k the distance increases and MI decreases)."""
    lam, mu = np.asarray(lam, float), np.asarray(mu, float)
    Bd = (e + float(np.dot(lam, sl_kl(mu, k)))) / u
    if sl_clip(lam, mu, k, k)[1] <= Bd:
        return 0.0
    a, b = 0.0, k
    for _ in range(60):
        mid = 0.5 * (a + b)
        if sl_clip(lam, mu, k, mid)[1] <= Bd:
            a = mid
        else:
            b = mid
    return float(np.dot(lam, sl_kl(sl_clip(lam, mu, k, a)[0], k)))


def sl_best(k, u, e, ms=None):
    """sup over centre types of sl_V (scan, then golden section)."""
    ms = np.linspace(0.03, 0.97, 48) if ms is None else ms
    vals = [sl_V(m, k, u, e) for m in ms]
    i = int(np.argmax(vals))
    v, m = mf_golden(lambda mm: -sl_V(mm, k, u, e), ms[max(i - 1, 0)], ms[min(i + 1, len(ms) - 1)], tol=1e-9)
    return -v, m


def sl_cube_game(u, t):
    """Game function of the uniform cube: t ln cosh(u/2) - ln cosh(tu/2)."""
    return t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2))


@conjecture("XXI.1 Lemma 11.89 (odds ratio): among pairs of binary variables with log odds ratio 2s the mutual information is largest when both marginals are uniform, I(B;X) <= ln 2 - h(sigma(s)) (= among binary channels with a given odds ratio the symmetric one has the largest capacity); and the steps of the proof for P ~ exp(J b x + h1 b + h2 x): dI/dh1 = (1/2)(1 - mu^2)[T(h2) - delta(h1) Delta(h2)] with delta(h) = (1/2) ln[cosh(h+J)/cosh(h-J)], T(h) = J[tanh(h+J) + tanh(h-J)] - 2 delta(h), Delta(h) = tanh(h+J) - tanh(h-J); T(h) < 0 and -T(h) < delta(h) Delta(h) for h > 0, the latter in the form X ln(Y/X) < (1-Y) ln((1-X)/(1-Y)) for X = 1/(1+e^{2(h+J)}), Y = 1/(1+e^{2(h-J)}); the capacity is decreasing in the field of the channel")
def t_slice_odds_ratio(rng, trials):
    N = max(4000, 100 * trials)
    m, p, q = rng.uniform(0.001, 0.999, N), rng.uniform(0.0005, 0.9995, N), rng.uniform(0.0005, 0.9995, N)
    p, q = np.maximum(p, q), np.minimum(p, q)
    mi = mf_hb(m * p + (1 - m) * q) - m * mf_hb(p) - (1 - m) * mf_hb(q)
    s = 0.5 * (np.log(p / (1 - p)) - np.log(q / (1 - q)))
    sym = math.log(2) - mf_hb(1 / (1 + np.exp(-s)))
    if np.any(mi > sym + 1e-12):
        i = int(np.argmax(mi - sym))
        return False, dict(reason="a table with more mutual information than the symmetric one with the same odds ratio", m=float(m[i]), p=float(p[i]), q=float(q[i]), mi=float(mi[i]), symmetric=float(sym[i]))
    ps = 1 / (1 + np.exp(-s))
    eq = float(np.abs(mf_hb(0.5) - mf_hb(ps) - sym).max())           # the symmetric table itself: m = 1/2, (p, q) = (sigma(s), 1 - sigma(s))
    if eq > 1e-12:
        return False, dict(reason="no equality at the symmetric table", err=eq)
    J, h = rng.uniform(1e-3, 3.5, N), rng.uniform(1e-3, 3.5, N)
    delta = lambda J, h: 0.5 * (np.log(np.cosh(h + J)) - np.log(np.cosh(h - J)))
    T = lambda J, h: J * (np.tanh(h + J) + np.tanh(h - J)) - 2 * delta(J, h)
    Delta = lambda J, h: np.tanh(h + J) - np.tanh(h - J)
    if np.any(T(J, h) >= 0):
        return False, dict(reason="T(h) >= 0 for some h > 0")
    star = -T(J, h) - delta(J, h) * Delta(J, h)
    X, Y = 1 / (1 + np.exp(2 * (h + J))), 1 / (1 + np.exp(2 * (h - J)))
    kern = X * np.log(Y / X) - (1 - Y) * (np.log1p(-X) - np.log1p(-Y))
    if np.any(kern >= 0) or np.any(star >= 1e-13):
        return False, dict(reason="the kernel inequality fails", kernel=float(kern.max()), star=float(star.max()))
    al, be = np.exp(2 * (h + J)), np.exp(2 * (h - J))
    ident = ((al * be + 2 * be + 1) * np.log((al + 1) / (be + 1)) - be * (al + 1) * np.log(al / be)) / ((al + 1) * (be + 1))
    if float(np.abs(star - ident).max()) > 1e-10:
        return False, dict(reason="the reduction of (*) to the kernel inequality is not an identity", err=float(np.abs(star - ident).max()))

    def MI(J, h1, h2):
        P = np.array([[math.exp(J * b * x + h1 * b + h2 * x) for x in (1, -1)] for b in (1, -1)])
        P = P / P.sum()
        return float((P * np.log(P / (P.sum(1, keepdims=True) * P.sum(0, keepdims=True)))).sum()), float(P[0].sum() - P[1].sum())
    worst = 0.0
    for _ in range(max(6, trials // 20)):
        J0, h1, h2 = float(rng.uniform(0.05, 2.5)), float(rng.uniform(-3, 3)), float(rng.uniform(-3, 3))
        mu = MI(J0, h1, h2)[1]
        formula = 0.5 * (1 - mu ** 2) * (float(T(J0, h2)) - float(delta(J0, h1)) * float(Delta(J0, h2)))
        fd = (MI(J0, h1 + 1e-5, h2)[0] - MI(J0, h1 - 1e-5, h2)[0]) / 2e-5
        worst = max(worst, abs(fd - formula))
    if worst > 1e-8:
        return False, dict(reason="derivative of the mutual information against the formula", err=worst)
    for J0 in (0.4, 1.2):
        prev = None
        for h2 in np.linspace(0, 3, 13):
            C, h1s = mf_golden(lambda h1: -MI(J0, h1, float(h2))[0], -12.0, 12.0, tol=1e-9)
            if h2 > 0 and not (-h2 - 1e-6 < h1s < 0):
                return False, dict(reason="the optimal input field is not between -h2 and 0", J=J0, h2=float(h2), h1=h1s)
            if prev is not None and -C > prev + 1e-12:
                return False, dict(reason="the capacity increases with the field of the channel", J=J0, h2=float(h2))
            prev = -C
    return True, dict(tables=N, smallest_gap=float((sym - mi).min()), derivative_err=worst)


@conjecture("XXI.2 Theorem 11.90(a),(b) (a slice of density kappa; binary centres suffice; closed forms): for a centre of type m, F(l) = m KL(kappa + l/2m || kappa) + (1-m) KL(kappa - l/(2(1-m)) || kappa), Psi = F^* = min over tilts with th1 - th2 = 2s of m Lam(th1) + (1-m) Lam(th2); the supremum over shells of min{MI(nu) : u dist <= e + MI(mu)} is F((Psi(u) - e)_+/u) = max_{t <= 1}[t Psi(u) - Psi(tu) - te]; the non-adaptive value is F(l_X) with u l_X - F(l_X) = Psi(u) - X, = max_{tau < 1}(F*(tau) - tau X)/(1 - tau); and profiles with 3 to 5 blocks never beat the best binary centre (inner problem by clipping, no duality used); the best centre type of a slice of density != 1/2 is not the slice's own")
def t_slice_binary(rng, trials):
    stats = dict(legendre=0.0, closed=0.0, game=0.0, na_game=0.0, multi=-1.0)
    Lam = lambda k, th: np.logaddexp(math.log1p(-k), math.log(k) + th) - k * th
    for _ in range(max(6, trials // 30)):
        k, m, u = float(rng.uniform(0.12, 0.88)), float(rng.uniform(0.12, 0.88)), float(rng.uniform(0.3, 3))
        P = sl_Psi(m, k, u)
        dual = mf_golden(lambda t1: float(m * Lam(k, t1) + (1 - m) * Lam(k, t1 - 2 * u)), -40.0, 40.0 + 2 * u, tol=1e-12)[0]
        stats["legendre"] = max(stats["legendre"], abs(P - dual))
        e = float(rng.uniform(0, 0.8)) * P
        ls = np.linspace(0, sl_hi(m, k) * (1 - 1e-9), 3001)
        Fl = np.array([sl_F(m, k, l) for l in ls])
        x = ls - (e + Fl) / u
        direct = max([sl_F(m, k, xx) for xx in x[x > 0]], default=0.0)
        stats["closed"] = max(stats["closed"], abs(direct - sl_V(m, k, u, e)))
        game = -mf_golden(lambda t: -(t * P - sl_Psi(m, k, t * u) - t * e), 0.0, 1.0, tol=1e-11)[0]
        stats["game"] = max(stats["game"], abs(max(game, 0.0) - sl_V(m, k, u, e)))
        X = float(rng.uniform(0.05, 0.9)) * P
        ts = np.linspace(0, 0.999, 200)
        nav = [(t * P - sl_Psi(m, k, t * u) - t * X) / (1 - t) for t in ts]
        i = int(np.argmax(nav))
        na = -mf_golden(lambda t: -(t * P - sl_Psi(m, k, t * u) - t * X) / (1 - t), ts[max(i - 1, 0)], ts[min(i + 1, 199)], tol=1e-10)[0]
        stats["na_game"] = max(stats["na_game"], abs(na - sl_N(m, k, u, X)))
        if abs(P - dual) > 1e-8 or abs(direct - sl_V(m, k, u, e)) > 1e-6 or abs(max(game, 0.0) - sl_V(m, k, u, e)) > 1e-7 \
                or abs(na - sl_N(m, k, u, X)) > 1e-7:
            return False, dict(reason="closed forms on a slice", k=k, m=m, u=u, e=e, X=X, Psi=P, dual=dual, direct=direct,
                               closed=sl_V(m, k, u, e), game=game, na_game=na, na_closed=sl_N(m, k, u, X))
    for (k, u) in ((0.5, 1.0), (0.3, 1.0), (0.7, 2.0)):
        sb0, mb0 = sl_best(k, u, 0.0)
        for ef in (0.0, 0.3):
            e = ef * sb0
            sb, mb = sl_best(k, u, e)
            # the best binary profile itself, through the multi-block solver (it must not exceed the claimed supremum)
            P = sl_Psi(mb, k, u)
            lstar = mf_golden(lambda l: -(u * l - sl_F(mb, k, l)), 0.0, sl_hi(mb, k) * (1 - 1e-13), tol=1e-13)[1]
            own = sl_r([mb, 1 - mb], [k + lstar / (2 * mb), k - lstar / (2 * (1 - mb))], k, u, e)
            if abs(own - sb) > 1e-6:
                return False, dict(reason="the best binary profile through the multi-block solver", k=k, u=u, e=e, multi=own, closed=sb)
            for _ in range(max(8, trials // 25)):
                kb = int(rng.integers(3, 6))
                lam = rng.dirichlet(np.ones(kb) * float(rng.choice([0.5, 1, 3])))
                if rng.random() < 0.5:                                  # a perturbation of the best binary profile
                    base = np.where(np.arange(kb) < kb // 2, k + lstar / (2 * mb), k - lstar / (2 * (1 - mb)))
                    mu = np.clip(base + rng.normal(0, 0.05, kb), 0.001, 0.999)
                else:
                    mu = rng.uniform(0, 1, kb)
                t = float(np.dot(lam, mu))
                mu = mu * k / t if t > k else 1 - (1 - mu) * (1 - k) / (1 - t)
                val = sl_r(lam, mu, k, u, e)
                stats["multi"] = max(stats["multi"], val - sb)
                if val > sb + 1e-7:
                    return False, dict(reason="a profile with more than two blocks beats every binary centre on the slice", k=k, u=u, e=e, lam=lam.tolist(), mu=mu.tolist(), value=val, binary=sb)
        if k != 0.5 and abs(mb0 - k) < 0.02:
            return False, dict(reason="the best centre of an off-centre slice lies in the slice", k=k, m=mb0)
    return True, stats


@conjecture("XXI.6 Theorem 11.90(a) at negative accuracies (the case that the first proof did not cover; repair of the Scientific Discovery Division, SCI-REV-0001, M2): on the slice of density kappa a profile is feasible at e < 0 iff MI(mu) >= -e, and MI <= h(kappa) for every profile, with equality for the pure profile (blocks of density 1 and 0); the supremum over two-block profiles is at least -e (the shell with F = -e of the centre m = kappa); every feasible profile with three to five blocks — random ones, ones on the boundary MI = -e (zero budget, value -e) and mixtures of a wide and a narrow two-point law, whose narrow component is infeasible although the mixture is feasible — has a value at most the two-block supremum")
def t_slice_negative_accuracy(rng, trials):
    stats = dict(cases=0, worst=-1.0, boundary=0, mixtures=0)
    hbin = lambda k: -k * math.log(k) - (1 - k) * math.log(1 - k)
    for (k, u, ef) in ((0.5, 1.0, 0.25), (0.3, 1.0, 0.3), (0.3, 1.0, 0.9), (0.2, 0.5, 0.05), (0.7, 2.0, 0.5), (0.1, 1.0, 0.15)):
        e = -ef * hbin(k)
        # two-block supremum: all centre types and all feasible shells l >= 0, value F((l - (e + F(l))/u)_+)
        R2, at = -1.0, None
        for m in np.linspace(0.02, 0.98, 97):
            ls = np.linspace(0.0, sl_hi(m, k) * (1 - 1e-9), 1201)
            Fl = m * sl_kl(k + ls / (2 * m), k) + (1 - m) * sl_kl(k - ls / (2 * (1 - m)), k)
            ok = Fl >= -e
            if not ok.any():
                continue
            x = np.maximum(ls[ok] - (e + Fl[ok]) / u, 0.0)
            vals = m * sl_kl(k + x / (2 * m), k) + (1 - m) * sl_kl(k - x / (2 * (1 - m)), k)
            if float(vals.max()) > R2:
                R2, at = float(vals.max()), float(m)
        # the shell with F = -e of the centre m = kappa has the value -e exactly (so the two-block supremum is at least -e;
        # the grid value R2 can miss it by the grid error, because the value falls steeply beyond that shell)
        lo, hi = 0.0, sl_hi(k, k) * (1 - 1e-12)
        if sl_F(k, k, hi) < -e:
            return False, dict(reason="the ray of the centre m = kappa does not reach F = -e", k=k, e=e)
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if sl_F(k, k, mid) < -e else (lo, mid)
        own = sl_r([k, 1 - k], [k + hi / (2 * k), k - hi / (2 * (1 - k))], k, u, e)
        if abs(own - (-e)) > 1e-6:
            return False, dict(reason="the shell with F = -e of the centre m = kappa does not have the value -e", k=k, e=e, value=own)
        bound = max(R2, -e)
        # the bound MI <= h(kappa) is attained by the pure profile (blocks of density 1 and 0 with weights kappa and
        # 1 - kappa), so the constant cannot be lowered; the pure profile and two neighbours go through the same check
        pure = [(np.array([k, 1 - k]), np.array([1 - s * (1 - k), s * k])) for s in (0.0, 1e-3, 0.05)]
        if abs(float(np.dot(pure[0][0], sl_kl(pure[0][1], k))) - hbin(k)) > 1e-12:
            return False, dict(reason="the pure profile does not have MI = h(kappa)", k=k)
        for rep in range(-len(pure), max(30, trials // 8)):
            if rep < 0:
                lam, mu = pure[rep]
            else:
                kb = int(rng.integers(3, 6))
                lam = rng.dirichlet(np.ones(kb) * float(rng.choice([0.5, 1, 3])))
                mu = rng.beta(0.3, 0.3, size=kb)                             # spread-out block densities
                t = float(np.dot(lam, mu))
                mu = mu * k / t if t > k else 1 - (1 - mu) * (1 - k) / (1 - t)
            MI = float(np.dot(lam, sl_kl(mu, k)))
            if MI > hbin(k) + 1e-9:
                return False, dict(reason="a profile with MI above h(kappa)", MI=MI, h=hbin(k))
            if rep < 0:
                continue
            if MI < -e:
                continue                                                      # infeasible at this accuracy
            mode = rep % 3
            if mode == 1:                                                     # contract towards kappa until MI = -e: zero budget
                a, b = 0.0, 1.0
                for _ in range(80):
                    mid = 0.5 * (a + b)
                    a, b = (mid, b) if float(np.dot(lam, sl_kl(k + mid * (mu - k), k))) < -e else (a, mid)
                mu = k + b * (mu - k)
                val = sl_r(lam, mu, k, u, e)
                if abs(val - (-e)) > 1e-6:
                    return False, dict(reason="a profile with zero budget does not have the value -e", value=val, e=e)
                stats["boundary"] += 1
            elif mode == 2:                                                   # half a wide two-point law, half a narrow one
                wide = np.array([k + 0.98 * (1 - k), k - 0.98 * k])
                wlam = np.array([k, 1 - k])
                narrow = np.array([k + 0.02 * (1 - k), k - 0.02 * k])
                lam, mu = np.concatenate([0.5 * wlam, 0.5 * wlam]), np.concatenate([wide, narrow])
                MIw, MIn = float(np.dot(wlam, sl_kl(wide, k))), float(np.dot(wlam, sl_kl(narrow, k)))
                if not (0.5 * (MIw + MIn) >= -e):
                    continue
                if not MIn < -e:
                    return False, dict(reason="test construction: the narrow component is feasible")
                stats["mixtures"] += 1
            val = sl_r(lam, mu, k, u, e)
            stats["worst"] = max(stats["worst"], val - bound)
            if val > bound + 2e-3:
                return False, dict(reason="a feasible profile with more than two blocks beats the two-block supremum at a negative accuracy",
                                   k=k, u=u, e=e, value=val, two_block=R2, lam=lam.tolist(), mu=mu.tolist())
            stats["cases"] += 1
    if stats["boundary"] < 6 or stats["mixtures"] < 6 or stats["cases"] < 30:      # quick mode: about 17, 21, 56
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


@conjecture("XXI.3 Theorem 11.90(c), Corollary 11.91 (domination by the uniform cube): for every slice density kappa, centre type m and 0 <= t <= 1: t Psi_{m,kappa}(u) - Psi_{m,kappa}(tu) <= t ln cosh(u/2) - ln cosh(tu/2), with equality at m = kappa = 1/2 (where the slice's functions are the cube's: sup of the hinted values = KL((Lambda_1 + e)/u || 1/2)); hence sup_m V <= R_unif and the non-adaptive values are below the cube's; the slices at u = 1 have 0.028005, 0.024588, 0.018842 at kappa = 0.4, 0.3, 0.2; and for Curie-Weiss known parts (ferromagnet with two phases, antiferromagnet, a field) and random block profiles mu: r_mu(e) <= [the same minimum with exits restricted to the slice of mu, at accuracy e + (I - v)(type)] <= R_unif(e); for the antiferromagnet without a field the cube's optimal profile attains R_unif")
def t_slice_dominated(rng, trials):
    worst = dict(game=-1.0, na=-1.0, model=-1.0, chain=-1.0)
    for _ in range(max(40, trials)):
        k, m, u, t = float(rng.uniform(0.03, 0.97)), float(rng.uniform(0.03, 0.97)), float(rng.uniform(0.2, 4)), float(rng.uniform(0, 1))
        d = t * sl_Psi(m, k, u) - sl_Psi(m, k, t * u) - sl_cube_game(u, t)
        worst["game"] = max(worst["game"], d)
        if d > 1e-10:
            return False, dict(reason="a slice's game function exceeds the cube's", k=k, m=m, u=u, t=t, excess=d)
    for u in (0.5, 1.0, 2.0):
        for e in (0.0, 0.3 * mf_R_unif(0.0, u)):
            if abs(sl_V(0.5, 0.5, u, e) - mf_R_unif(e, u)) > 1e-9:
                return False, dict(reason="the centre of type 1/2 on the slice 1/2 is not the uniform cube", u=u, e=e, slice=sl_V(0.5, 0.5, u, e), cube=mf_R_unif(e, u))
        pu = 1 / (1 + math.exp(u))
        for X in (0.01, 0.05):
            rho = pu
            a, b = pu, 0.5
            for _ in range(60):
                rho = 0.5 * (a + b)
                if mf_kl(rho, pu) <= X:
                    a = rho
                else:
                    b = rho
            cube_na = mf_kl(a, 0.5) if mf_kl(0.5, pu) > X else 0.0
            if abs(sl_N(0.5, 0.5, u, X) - cube_na) > 1e-8:
                return False, dict(reason="non-adaptive value of the slice 1/2 against the cube", u=u, X=X, slice=sl_N(0.5, 0.5, u, X), cube=cube_na)
            for _ in range(6):
                k, m = float(rng.uniform(0.05, 0.95)), float(rng.uniform(0.05, 0.95))
                worst["na"] = max(worst["na"], sl_N(m, k, u, X) - cube_na)
                if sl_N(m, k, u, X) > cube_na + 1e-9:
                    return False, dict(reason="a slice's non-adaptive value exceeds the cube's", k=k, m=m, u=u, X=X)
    for k, want in ((0.4, 0.028005), (0.3, 0.024588), (0.2, 0.018842)):
        sb, mb = sl_best(k, 1.0, 0.0)
        if abs(sb - want) > 2e-6 or sb >= mf_R_unif(0.0, 1.0):
            return False, dict(reason="value of a slice at u = 1", k=k, value=sb, expected=want)
    for (bJ, bB, u) in ((1.5, 0.0, 1.0), (-2.0, 0.0, 1.0), (0.0, 0.6, 0.5), (0.8, 0.3, 1.0)):
        M = mf_model(bJ, bB, u, K=20001)
        for _ in range(max(3, trials // 60)):
            kb = int(rng.integers(2, 4))
            lam = rng.dirichlet(np.ones(kb) * 2)
            mu = rng.uniform(0.03, 0.97, kb)
            k = float(np.dot(lam, mu))
            gam = float(M["I"](k) - M["v"](k))
            e = float(rng.choice([0.0, 0.01, 0.03]))
            full = mf_r(M, lam, mu, e, G=500)
            inside = sl_r(lam, mu, k, u, e + gam)
            worst["model"] = max(worst["model"], full - inside)
            worst["chain"] = max(worst["chain"], inside - mf_R_unif(e, u))
            if full > inside + 2e-6 or inside > mf_R_unif(e, u) + 1e-9:
                return False, dict(reason="r_mu(e) <= slice value <= uniform cube fails", bJ=bJ, bB=bB, u=u, lam=lam.tolist(), mu=mu.tolist(), e=e,
                                   full=full, slice=inside, cube=mf_R_unif(e, u))
    M = mf_model(-2.0, 0.0, 1.0, K=20001)
    pu = 1 / (1 + math.e)
    for e in (0.0, 0.01):
        rho = (math.log(2 / (1 + math.exp(-1.0))) + e) / 1.0                 # the cube's optimal shell: distance p_u from the centre
        val = mf_r(M, np.array([0.5, 0.5]), np.array([1 - pu, pu]), e, G=1500)
        if abs(val - mf_R_unif(e, 1.0)) > 2e-6:
            return False, dict(reason="antiferromagnet without a field: the cube's optimal profile does not attain R_unif", e=e, value=val, cube=mf_R_unif(e, 1.0))
    return True, worst


@conjecture("XXI.4 Theorem 11.92, Lemma 11.93 (algorithms: reduction to slices; every n, exact enumeration on small cubes): for an exchangeable pi and a u-Lipschitz psi, t -> ln A_t (the mean of e^{-psi} over the type class T_t) is u-Lipschitz; the deficits d_t = ln[max_j p_j A_j / (p_t A_t)] are at least J_t - V_n(t), with equality for the flat-histogram instance; optimistic refinement (always refine the slice with the largest p_t U_t; stop when its bracket has the final width) returns a valid bracket of width at most x_last + ln(n+1) whatever the positions of the brackets, and refines a slice from the width x_{l-1} only if d_t <= x_{l-1}; for a uniform slice and a uniformly random set O of outer coordinates: A_k = sum_j H(j) A_{k;j}(O) for every O (H hypergeometric, A_{k;j}(O) the mean over the product of the outer slice of type j and the inner slice of type k - j) and E_O A_{k;j}(O) = A_k for every j; the inner-slice means are u-Lipschitz on the outer slice")
def t_slice_reduction(rng, trials):
    from itertools import combinations
    stats = dict(lip=-1.0, deficit=1e9, refinements=0, partition=0.0)
    for n in (8, 9):
        pts = np.array([[(x >> i) & 1 for i in range(n)] for x in range(1 << n)])
        wt = pts.sum(1)
        u = float(rng.uniform(0.3, 1.5))
        cs = pts[rng.integers(0, 1 << n, 6)]
        off = rng.uniform(-2, 2, 6) * u
        dist = (pts[:, None, :] != cs[None, :, :]).sum(2)
        psi = np.minimum((off[None, :3] + u * dist[:, :3]).min(1), np.maximum(off[3] - u * dist[:, 3], (off[None, 4:] + u * dist[:, 4:]).min(1)))
        for i in range(n):                                                # psi is u-Lipschitz
            nb = np.arange(1 << n) ^ (1 << i)
            if np.any(np.abs(psi - psi[nb]) > u + 1e-12):
                return False, dict(reason="the test function is not u-Lipschitz")
        A = np.array([np.exp(-psi[wt == t]).mean() for t in range(n + 1)])
        for lnA_ in (np.log(A), np.log(np.array([np.exp(u * wt[wt == t]).mean() for t in range(n + 1)]))):   # psi, and -u|x|
            lip = float(np.abs(np.diff(lnA_)).max())
            stats["lip"] = max(stats["lip"], lip - u)
            if lip > u + 1e-12:
                return False, dict(reason="ln A_t is not u-Lipschitz in t", n=n, slope=lip, u=u)
        J = rng.uniform(0, 0.5 * n, n + 1)
        J = J - np.log(np.exp(-J).sum())
        Vn = rd_lip_minorant(J.copy(), u)                                # the claim: d_t >= J_t - V_n(t)
        lnAH = rd_lip_minorant(J.copy(), 1.0 * u)                        # the flat-histogram instance: ln A_t = V_n(t)
        d = (np.log(A) - J).max() - (np.log(A) - J)
        for lnA_ in (np.log(A), lnAH, u * np.arange(n + 1.0)):
            d_ = (lnA_ - J).max() - (lnA_ - J)
            stats["deficit"] = min(stats["deficit"], float((d_ - (J - Vn)).min()))
            if np.any(d_ < J - Vn - 1e-10):
                return False, dict(reason="a deficit below J_t - V_n(t)", n=n)
        dH = (lnAH - J).max() - (lnAH - J)
        if float(np.abs(dH - (J - Vn)).max()) > 1e-10:
            return False, dict(reason="no equality at the flat-histogram instance", n=n)
        # optimistic refinement with brackets in arbitrary position
        ladder = np.linspace(2 * u * n, 0.25, 9)
        for rep in range(max(3, trials // 80)):
            lev = np.zeros(n + 1, int)
            th = rng.uniform(0, 1, n + 1)
            lo = np.log(A) - th * ladder[0]
            hi = lo + ladder[0]
            log = []
            while True:
                k = int(np.argmax(hi - J))
                if lev[k] == len(ladder) - 1:
                    break
                log.append((k, ladder[lev[k]]))
                lev[k] += 1
                th = float(rng.uniform(0, 1))
                nlo = np.log(A[k]) - th * ladder[lev[k]]
                lo[k], hi[k] = max(lo[k], nlo), min(hi[k], nlo + ladder[lev[k]])
            out_lo, out_hi = float((lo - J).max()), float((hi - J).max()) + math.log(n + 1)
            truth = float(np.log(np.exp(np.log(A) - J).sum()))
            if not (out_lo - 1e-12 <= truth <= out_hi + 1e-12) or out_hi - out_lo > ladder[-1] + math.log(n + 1) + 1e-12:
                return False, dict(reason="the bracket of the optimistic refinement is not valid or too wide", n=n, lo=out_lo, hi=out_hi, truth=truth)
            for k, width in log:
                if d[k] > width + 1e-12:
                    return False, dict(reason="a slice was refined although its deficit exceeds its bracket", n=n, slice=k, deficit=float(d[k]), width=float(width))
            stats["refinements"] = max(stats["refinements"], len(log))
            if len(log) > (n + 1) * (len(ladder) - 1):
                return False, dict(reason="more refinements than slices times rungs")
        # random partitions of a slice
        k, no = n // 2, n // 2 - 1
        w = np.exp(-psi)
        Ak = w[wt == k].mean()
        tot = np.zeros(no + 1)
        cnt = 0
        for O in combinations(range(n), no):
            mask = sum(1 << i for i in O)
            oj = np.array([bin(x & mask).count("1") for x in range(1 << n)])
            acc = 0.0
            for j in range(no + 1):
                sel = (wt == k) & (oj == j)
                if sel.any():
                    Hj = math.comb(no, j) * math.comb(n - no, k - j) / math.comb(n, k)
                    acc += Hj * w[sel].mean()
                    tot[j] += w[sel].mean()
            cnt += 1
            stats["partition"] = max(stats["partition"], abs(acc - Ak) / Ak)
            if abs(acc - Ak) > 1e-10 * Ak:
                return False, dict(reason="the decomposition of a slice by the type of the outer block fails", n=n, O=O)
        js = [j for j in range(no + 1) if 0 <= k - j <= n - no]
        err = max(abs(tot[j] / cnt - Ak) / Ak for j in js)
        stats["partition"] = max(stats["partition"], err)
        if err > 1e-10:
            return False, dict(reason="the mean over partitions of a product-slice mean is not the slice mean", n=n, err=err)
        # inner-slice means on the outer slice (O = the first no coordinates, j = 1)
        mask = (1 << no) - 1
        j = 1
        Wj = {}
        for x in range(1 << n):
            if wt[x] == k and bin(x & mask).count("1") == j:
                Wj.setdefault(x & mask, []).append(w[x])
        keys = list(Wj)
        for a in keys:
            for b in keys:
                dd = bin(a ^ b).count("1")
                if abs(math.log(np.mean(Wj[a])) - math.log(np.mean(Wj[b]))) > u * dd + 1e-12:
                    return False, dict(reason="inner-slice means are not u-Lipschitz on the outer slice", n=n)
    return True, stats


# -----------------------------------------------------------------------------------------------------------------
# XXII. Product landscapes with several site types, any alphabets, asymmetric envelopes (theory report 11.26)
# -----------------------------------------------------------------------------------------------------------------
def st_vertices(d):
    """Vertices of the Lipschitz polytope {g : g[a] - g[b] <= d[a][b]} of a site, normalised by g[0] = 0."""
    q = len(d)
    cons = [(a, b) for a in range(q) for b in range(q) if a != b]
    out = []
    for S in itertools.combinations(cons, q - 1):
        A = np.zeros((q - 1, q - 1))
        rhs = np.zeros(q - 1)
        for i, (a, b) in enumerate(S):
            if a > 0:
                A[i, a - 1] += 1
            if b > 0:
                A[i, b - 1] -= 1
            rhs[i] = d[a][b]
        if abs(np.linalg.det(A)) < 1e-12:
            continue
        g = np.concatenate([[0.0], np.linalg.solve(A, rhs)])
        if all(g[a] - g[b] <= d[a][b] + 1e-9 for a, b in cons) and not any(np.allclose(g, h, atol=1e-8) for h in out):
            out.append(g)
    return out


def st_gibbs(pi, g):
    w = np.asarray(pi, float) * np.exp(-np.asarray(g, float))
    return w / w.sum()


def st_site(pi, d):
    V = st_vertices(d)
    return dict(pi=np.asarray(pi, float), d=np.asarray(d, float), V=V, P=np.array([st_gibbs(pi, phi) for phi in V]))


def st_game(site, gamma, t):
    """F(gamma, t) = -ln of the value of the game K[a, phi] = (pi_phi(a)/pi_gamma(a))^t (the adversary mixes vertices)."""
    from scipy.optimize import linprog
    K = (site["P"] / st_gibbs(site["pi"], gamma)[None, :]).T ** t
    nr, nc = K.shape
    c = np.zeros(nc + 1)
    c[-1] = 1.0
    A_eq = np.zeros((1, nc + 1))
    A_eq[0, :nc] = 1.0
    res = linprog(c, A_ub=np.hstack([K, -np.ones((nr, 1))]), b_ub=np.zeros(nr), A_eq=A_eq, b_eq=[1.0],
                  bounds=[(0, None)] * nc + [(None, None)], method="highs")
    return -math.log(res.x[-1])


def st_renyi(site, t):
    """Theorem 11.99: F*(t) = max_M -t ln sum_a (sum_phi M(phi) pi_phi(a)^t)^(1/t); returns (value, upper bound from
    the dual (1-t) max_phi D_t(pi_phi || Q), M, the Renyi centre Q)."""
    from scipy.optimize import minimize
    Pt = site["P"] ** t
    nv = len(Pt)

    def N(M):
        return float(((M @ Pt) ** (1 / t)).sum())

    def dN(M):
        return (Pt * ((M @ Pt) ** (1 / t - 1))[None, :]).sum(axis=1) / t
    best = None
    for start in range(4):
        M0 = np.ones(nv) / nv if start == 0 else np.random.default_rng(start).dirichlet(np.ones(nv))
        res = minimize(N, M0, jac=dN, method="SLSQP", bounds=[(0, 1)] * nv, constraints=[{"type": "eq", "fun": lambda M: M.sum() - 1, "jac": lambda M: np.ones(nv)}],
                       options={"ftol": 1e-15, "maxiter": 400})
        M = np.clip(res.x, 0, None)
        M /= M.sum()
        m = (M @ Pt) ** (1 / t)
        Q = m / m.sum()
        val = -t * math.log(N(M))
        upper = max(-math.log(float((Pt[i] * Q ** (1 - t)).sum())) for i in range(nv))
        if best is None or val > best[0]:
            best = (val, upper, M, Q)
        if upper - val < 1e-9:
            break
    return best


def st_F(chain, t):
    """F*(t) = sum_j lam_j F*_j(t) of a chain [(lam_j, site_j)] (one common slope)."""
    if t <= 1e-12 or t >= 1 - 1e-12:
        return 0.0
    return sum(l * st_renyi(s, t)[0] for l, s in chain)


def st_R(chain, e, grid=60):
    ts = np.linspace(0, 1, grid + 1)
    vals = [st_F(chain, t) - t * e for t in ts]
    i = int(np.argmax(vals))
    v, t = mf_golden(lambda t: -(st_F(chain, t) - t * e), ts[max(i - 1, 0)], ts[min(i + 1, grid)], tol=1e-9)
    return max(-v, 0.0), t


def st_theta_na(chain, x, grid=60):
    ts = np.linspace(0, 0.995, grid + 1)
    vals = [(st_F(chain, t) - t * x) / (1 - t) for t in ts]
    i = int(np.argmax(vals))
    v, t = mf_golden(lambda t: -(st_F(chain, t) - t * x) / (1 - t), ts[max(i - 1, 0)], ts[min(i + 1, grid)], tol=1e-9)
    return max(-v, 0.0)


def st_E(site):
    """Threshold of a site: max_M -ln sum_a prod_phi pi_phi(a)^M(phi) (a concave programme)."""
    from scipy.optimize import minimize
    lP = np.log(site["P"])
    nv = len(lP)
    res = minimize(lambda M: math.log(float(np.exp(M @ lP).sum())), np.ones(nv) / nv, method="SLSQP", bounds=[(0, 1)] * nv,
                   constraints=[{"type": "eq", "fun": lambda M: M.sum() - 1}], options={"ftol": 1e-15, "maxiter": 400})
    return -float(res.fun)


def st_a(site):
    """Shannon capacity of the vertex channel (Blahut-Arimoto)."""
    P = site["P"]
    M = np.ones(len(P)) / len(P)
    for _ in range(4000):
        Q = M @ P
        D = (P * np.log(P / Q[None, :])).sum(axis=1)
        M2 = M * np.exp(D)
        M2 /= M2.sum()
        if np.abs(M2 - M).max() < 1e-13:
            M = M2
            break
        M = M2
    Q = M @ P
    return float((M[:, None] * P * np.log(P / Q[None, :])).sum())


def st_hamming(q, u):
    return [[0.0 if a == b else u for b in range(q)] for a in range(q)]


def st_groups(k, u, t=None):
    """Single dips on k equally weighted groups of letters with the Hamming envelope: Psi_k, the game function, h, a, E."""
    Psi = lambda s: math.log((math.exp(s) + k - 1) / k) - s / k
    if t is not None:
        return t * Psi(u) - Psi(t * u)
    h = -mf_golden(lambda tt: -(tt * Psi(u) - Psi(tt * u)), 0.0, 1.0, tol=1e-12)[0]
    p = math.exp(u) / (math.exp(u) + k - 1)
    a = math.log(k) + p * math.log(p) + (1 - p) * math.log((1 - p) / (k - 1))
    return h, a, Psi(u)


ST_SITES = dict(
    bin=([0.7, 0.3], st_hamming(2, 1.0)),
    path=([0.5, 0.3, 0.2], [[0, 0.8, 2.4], [0.8, 0, 1.6], [2.4, 1.6, 0]]),
    tri=([0.2, 0.5, 0.3], [[0, 1.0, 2.0], [1.0, 0, 1.5], [2.0, 1.5, 0]]),
    asym=([0.5, 0.3, 0.2], [[0, 1, 2], [0.5, 0, 1.5], [1, 0.5, 0]]),
)


@conjecture("XXII.1 Theorem 11.99 (the site function is a Renyi capacity): for a site with law pi and envelope d (zero diagonal, triangle inequality, not necessarily symmetric), Lipschitz polytope L = {g : g(a) - g(b) <= d(a,b)} with vertices V and Gibbs laws pi_phi ~ pi e^{-phi}: max over gamma in L of -ln val((pi_phi(a)/pi_gamma(a))^t) equals max_M -t ln sum_a (sum_phi M(phi) pi_phi(a)^t)^{1/t} = min_Q max_phi (1-t) D_t(pi_phi || Q); the maximising gamma has the Renyi centre as its Gibbs law and lies in L (closure under soft minima); no member of L does better; the example sites have 2, 4, 6, 5 vertices and h = max_t F*(t) = 0.025034, 0.089589, 0.066729, 0.045407")
def t_sites_renyi(rng, trials):
    stats = dict(gap=0.0, centre=0.0, random=-1.0)
    sites = {k: st_site(*v) for k, v in ST_SITES.items()}
    if [len(sites[k]["V"]) for k in ("bin", "path", "tri", "asym")] != [2, 4, 6, 5]:
        return False, dict(reason="number of vertices of the example sites", got=[len(s["V"]) for s in sites.values()])
    extra = []
    for _ in range(max(2, trials // 100)):
        q = int(rng.integers(2, 4))
        d = rng.uniform(0.3, 2.0, (q, q))
        np.fill_diagonal(d, 0.0)
        for k in range(q):                                              # shortest-path closure: the triangle inequality
            d = np.minimum(d, d[:, [k]] + d[[k], :])
        extra.append(st_site(rng.dirichlet(np.ones(q) * 3), d))
    for site in list(sites.values()) + extra:
        q = len(site["pi"])
        for t in (0.2, float(rng.uniform(0.3, 0.7)), 0.85):
            val, upper, M, Q = st_renyi(site, t)
            stats["gap"] = max(stats["gap"], upper - val)
            if not (-1e-9 <= upper - val <= 1e-7):
                return False, dict(reason="primal and dual form of the Renyi capacity differ", t=t, primal=val, dual=upper)
            gstar = -np.log(Q / site["pi"])
            if any(gstar[a] - gstar[b] > site["d"][a][b] + 1e-7 for a in range(q) for b in range(q)):
                return False, dict(reason="the instance whose Gibbs law is the Renyi centre is not in the class", t=t)
            at = st_game(site, gstar, t)
            stats["centre"] = max(stats["centre"], abs(at - val))
            if abs(at - val) > 2e-7:
                return False, dict(reason="the game at the Renyi centre does not have the Renyi value", t=t, game=at, renyi=val)
            for _ in range(max(3, trials // 80)):
                w = rng.dirichlet(np.ones(len(site["V"])) * float(rng.choice([0.3, 1.0])))
                g = sum(wi * v for wi, v in zip(w, site["V"]))            # a random member of L
                fg = st_game(site, g, t)
                stats["random"] = max(stats["random"], fg - val)
                if fg > val + 2e-7:
                    return False, dict(reason="an additive instance beats the Renyi value", t=t, game=fg, renyi=val)
    for name, want in (("bin", 0.025034), ("path", 0.089589), ("tri", 0.066729), ("asym", 0.045407)):
        h = st_R([(1.0, sites[name])], 0.0)[0]
        if abs(h - want) > 2e-6:
            return False, dict(reason="h of an example site", site=name, value=h, expected=want)
    return True, stats


@conjecture("XXII.2 Theorems 11.98, 11.99, Propositions 11.100, 11.102 (chains of several site types): F* = sum_j lam_j F*_j at one common slope; for the chain of half binary sites (pi = (0.7, 0.3), u = 1) and half three-state path sites (steps 0.8, 1.6; pi = (0.5, 0.3, 0.2)): E = 0.251877, a = 0.195046, h = 0.057275, R^max(0.3E) = 0.027759 < 0.030121 = the average of the two types at the common accuracy (the exponents do not add); the pair identity theta_na(e + R(e)) = R(e); on the uniform cube the dictionary: (1-t) C_t of the binary symmetric channel with crossover 1/(1+e^u) is t ln cosh(u/2) - ln cosh(tu/2), its capacity is KL(p_u || 1/2) and theta_na is the inverse sphere-packing exponent; a two-letter site with the asymmetric envelope (u1, u2) is the symmetric one with u = (u1+u2)/2 and the site law tilted by (u2-u1)/2")
def t_sites_chain(rng, trials):
    sb, sp = st_site(*ST_SITES["bin"]), st_site(*ST_SITES["path"])
    mix = [(0.5, sb), (0.5, sp)]
    E = 0.5 * st_E(sb) + 0.5 * st_E(sp)
    a = 0.5 * st_a(sb) + 0.5 * st_a(sp)
    h = st_R(mix, 0.0)[0]
    r3 = st_R(mix, 0.3 * E)[0]
    avg = 0.5 * st_R([(1.0, sb)], 0.3 * E)[0] + 0.5 * st_R([(1.0, sp)], 0.3 * E)[0]
    got = dict(E=E, a=a, h=h, R03=r3, average=avg)
    want = dict(E=0.251877, a=0.195046, h=0.057275, R03=0.027759, average=0.030121)
    for k in want:
        if abs(got[k] - want[k]) > 3e-6:
            return False, dict(reason="numbers of the mixed chain", quantity=k, value=got[k], expected=want[k])
    if not r3 < avg - 1e-3:
        return False, dict(reason="the exponents of the site types add", chain=r3, average=avg)
    worst = 0.0
    for e in (0.0, 0.3 * st_E(sp)):
        R = st_R([(1.0, sp)], e)[0]
        worst = max(worst, abs(st_theta_na([(1.0, sp)], e + R) - R))
    if worst > 1e-6:
        return False, dict(reason="pair identity theta_na(e + R(e)) = R(e)", err=worst)
    dic = 0.0
    for _ in range(max(4, trials // 60)):
        u, t = float(rng.uniform(0.3, 3)), float(rng.uniform(0.1, 0.9))
        cube = st_site([0.5, 0.5], st_hamming(2, u))
        closed = t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2))
        pu = 1 / (1 + math.exp(u))
        bsc = (1 - t) * math.log(2) - math.log(pu ** t + (1 - pu) ** t)          # (1-t) C_t of the binary symmetric channel
        dic = max(dic, abs(st_renyi(cube, t)[0] - closed), abs(bsc - closed), abs(st_a(cube) - mf_kl(pu, 0.5)), abs(st_E(cube) - math.log(math.cosh(u / 2))))
        x = float(rng.uniform(0.05, 0.9)) * math.log(math.cosh(u / 2))
        lo, hi = pu, 0.5                                                           # sphere-packing: KL(rho || p_u) = x, exponent KL(rho || 1/2)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if mf_kl(mid, pu) <= x:
                lo = mid
            else:
                hi = mid
        dic = max(dic, abs(st_theta_na([(1.0, cube)], x) - mf_kl(lo, 0.5)))
        u1, u2, p = float(rng.uniform(0.2, 2)), float(rng.uniform(0.2, 2)), float(rng.uniform(0.2, 0.8))
        asym = st_site([1 - p, p], [[0.0, u1], [u2, 0.0]])
        kap = (u2 - u1) / 2                                                        # psi = psi' + kap |x| with psi' symmetric-Lipschitz
        ww = np.array([1 - p, p * math.exp(-kap)])
        sym = st_site(ww / ww.sum(), st_hamming(2, (u1 + u2) / 2))
        dic = max(dic, abs(st_renyi(asym, t)[0] - st_renyi(sym, t)[0]))
    if dic > 2e-6:
        return False, dict(reason="dictionary on the cube / normal form of an asymmetric two-letter site", err=dic)
    return True, dict(got, pair=worst, dictionary=dic)


@conjecture("XXII.3 Proposition 11.103(d),(e) (which site law is hardest; uniform sites group their letters): with Psi_k(s) = ln((e^s + k - 1)/k) - s/k and h_k = max_t[t Psi_k(u) - Psi_k(tu)] (single dips on k equally weighted groups): h_k = h_{k+1} exactly at e^u = k(k-1), k = 2..5, with h_k > h_{k+1} below; the uniform three-letter Hamming site has (h, a, E) = (h_3, a_3, E_3) and the uniform four-letter site has each of h, a, E equal to the larger of its values for k = 2 and k = 4, and F*(t) = max(F*_2(t), F*_4(t)) pointwise (u = 1: h = h_2, a = a_4); at u = 0.5 the three-letter law (0.02, 0.49, 0.49) has a larger h than the uniform law (two letters: 0.007673 against 0.007425), at u = 0.3 a larger a, and at u = 1 the law (0.05, 0.5, 0.45) has a larger threshold E (0.120196 against 0.119499)")
def t_sites_hardest_law(rng, trials):
    stats = {}
    for k in (2, 3, 4, 5):
        u = math.log(k * (k - 1))
        hk, hk1 = st_groups(k, u)[0], st_groups(k + 1, u)[0]
        below = st_groups(k, 0.9 * u)[0] - st_groups(k + 1, 0.9 * u)[0]
        above = st_groups(k, 1.1 * u)[0] - st_groups(k + 1, 1.1 * u)[0]
        if abs(hk - hk1) > 1e-10 or not (below > 0 > above):
            return False, dict(reason="crossing of the groupings k and k+1 is not at e^u = k(k-1)", k=k, hk=hk, hk1=hk1, below=below, above=above)
    for u in (0.5, 1.0, 2.0):
        s3 = st_site([1 / 3] * 3, st_hamming(3, u))
        got = (st_R([(1.0, s3)], 0.0)[0], st_a(s3), st_E(s3))
        if max(abs(g - w) for g, w in zip(got, st_groups(3, u))) > 2e-6:
            return False, dict(reason="uniform three-letter site against single dips", u=u, got=got, closed=st_groups(3, u))
        s4 = st_site([0.25] * 4, st_hamming(4, u))
        got = (st_R([(1.0, s4)], 0.0)[0], st_a(s4), st_E(s4))
        want = tuple(max(x, y) for x, y in zip(st_groups(2, u), st_groups(4, u)))
        if max(abs(g - w) for g, w in zip(got, want)) > 2e-6:
            return False, dict(reason="uniform four-letter site against the best grouping", u=u, got=got, want=want)
        stats[f"u{u}"] = got[0]
    s4 = st_site([0.25] * 4, st_hamming(4, 1.0))
    for t in (0.3, 0.6, 0.65, 0.7, 0.9):
        f = st_renyi(s4, t)[0]
        if abs(f - max(st_groups(2, 1.0, t), st_groups(4, 1.0, t))) > 1e-7:
            return False, dict(reason="F* of the uniform four-letter site is not the upper envelope of the two groupings", t=t, value=f)
    if not (st_groups(2, 1.0)[0] > st_groups(4, 1.0)[0] and st_groups(4, 1.0)[1] > st_groups(2, 1.0)[1]):
        return False, dict(reason="at u = 1 the two groupings are not ordered differently for h and for a")
    near2 = st_site([0.02, 0.49, 0.49], st_hamming(3, 0.5))
    unif = st_site([1 / 3] * 3, st_hamming(3, 0.5))
    h_near, h_unif = st_R([(1.0, near2)], 0.0)[0], st_R([(1.0, unif)], 0.0)[0]
    if not (h_near > h_unif + 2e-4 and abs(st_groups(2, 0.5)[0] - 0.007673) < 1e-6 and abs(h_unif - 0.007425) < 1e-6):
        return False, dict(reason="small slope: a law near two letters is not harder than the uniform one", near=h_near, uniform=h_unif)
    a_near, a_unif = st_a(st_site([0.02, 0.49, 0.49], st_hamming(3, 0.3))), st_a(st_site([1 / 3] * 3, st_hamming(3, 0.3)))
    if not a_near > a_unif + 3e-4:
        return False, dict(reason="small slope: capacity", near=a_near, uniform=a_unif)
    E_field, E_unif = st_E(st_site([0.05, 0.5, 0.45], st_hamming(3, 1.0))), st_E(st_site([1 / 3] * 3, st_hamming(3, 1.0)))
    if abs(E_field - 0.120196) > 2e-6 or abs(E_unif - 0.119499) > 2e-6:
        return False, dict(reason="thresholds of the three-letter site at u = 1", field=E_field, uniform=E_unif)
    return True, dict(stats, h_near=h_near, h_unif=h_unif, a_near=a_near, a_unif=a_unif, E_field=E_field, E_unif=E_unif)


@conjecture("XXII.5 Proposition 11.103(d),(f), Proposition 11.100 and Theorem 11.101 after the reviews SCI-REV-0005 and SCI-REV-0001 section 5 of the Scientific Discovery Division: (f) the ceiling F*(t) <= t(1-t)u^2/8, u the largest entry of the envelope, for every site, approached by the two-letter cube at small slopes; (d) for the Hamming envelope a site law that gives some set of letters the weight 1/2 has F*(t) >= F*_cube(t); at u = 0.5 the three-letter law (0.05, 0.5, 0.45) is above the two-letter cube in h and in E, the law (0.02, 0.49, 0.49) below it in both — so neither 'close to two letters means the two-letter values' nor 'the cube is the supremum' holds; the convex kink of F* for the triangle site at t_c = 0.37799 is a slope jump of +0.0056 (not +0.0052); and theta_na is Lipschitz in the composition with constant max_j a_j")
def t_sites_corrections(rng, trials):
    stats = dict(ceiling=0.0, half=0.0, lip=0.0)
    cube = lambda u, t: t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2))
    # (f) the ceiling, on random sites with any envelope
    for rep in range(max(12, trials // 30)):
        q = int(rng.integers(2, 5))
        D = rng.uniform(0.2, 3.0, size=(q, q))
        if rep % 2 == 0:
            D = (D + D.T) / 2
        D = mr_closure(D)
        site = st_site(rng.dirichlet(np.ones(q) * 2.0), D)
        u = float(D.max())
        for t in (0.15, 0.5, 0.85):
            val = st_renyi(site, t)[0]
            if val > t * (1 - t) * u * u / 8 + 1e-9:
                return False, dict(reason="F* exceeds the ceiling t(1-t)u^2/8", t=t, value=val, ceiling=t * (1 - t) * u * u / 8)
            stats["ceiling"] = max(stats["ceiling"], val / (t * (1 - t) * u * u / 8))
    small = cube(0.05, 0.5) / (0.25 * 0.05 ** 2 / 8)
    if not 0.999 < small <= 1.0:
        return False, dict(reason="the ceiling is not approached by the cube at small slopes", ratio=small)
    # (d) weight one half on a set of letters: at least the cube (Hamming envelope)
    for rep in range(max(10, trials // 40)):
        q = int(rng.integers(3, 5))
        u = float(rng.uniform(0.3, 2.5))
        w = rng.dirichlet(np.ones(q))
        k = int(rng.integers(1, q))                                           # letters 0..k-1 form the set A
        pi = np.concatenate([0.5 * w[:k] / w[:k].sum(), 0.5 * w[k:] / w[k:].sum()])
        site = st_site(pi, st_hamming(q, u))
        for t in (0.2, 0.5, 0.8):
            excess = st_renyi(site, t)[0] - cube(u, t)
            if excess < -1e-9:
                return False, dict(reason="a site law with weight 1/2 on a set of letters is below the cube", pi=pi.tolist(), u=u, t=t, excess=excess)
            stats["half"] = min(stats["half"], excess) if stats["half"] else excess
    # the data points at u = 0.5
    hc, ac, Ec = st_groups(2, 0.5)
    vals = {}
    for name, pi in (("rare", [0.05, 0.5, 0.45]), ("near", [0.02, 0.49, 0.49])):
        site = st_site(pi, st_hamming(3, 0.5))
        vals[name] = (st_R([(1.0, site)], 0.0)[0], st_E(site))
    stats["h_cube"], stats["h_rare"], stats["h_near"] = round(hc, 8), round(vals["rare"][0], 8), round(vals["near"][0], 8)
    if not (abs(hc - 0.0076729) < 2e-7 and abs(Ec - 0.0309298) < 2e-7):
        return False, dict(reason="reference values of the two-letter cube at u = 0.5", h=hc, E=Ec)
    if not (vals["rare"][0] > hc + 1e-6 and vals["rare"][1] > Ec + 1e-6 and abs(vals["rare"][0] - 0.0076752) < 2e-7):
        return False, dict(reason="the law (0.05, 0.5, 0.45) is not above the cube in h and E", values=vals["rare"], cube=(hc, Ec))
    if not (vals["near"][0] < hc - 3e-7 and vals["near"][1] < Ec - 3e-6):
        return False, dict(reason="the law (0.02, 0.49, 0.49) is not below the cube in h and E", values=vals["near"], cube=(hc, Ec))
    # the kink of the triangle site: one-sided slopes at t_c
    tri = st_site(*ST_SITES["tri"])
    tc, dl = 0.377987, 5e-5
    f0, fm, fp = st_renyi(tri, tc)[0], st_renyi(tri, tc - dl)[0], st_renyi(tri, tc + dl)[0]
    jump = (fp - f0) / dl - (f0 - fm) / dl
    stats["jump"] = round(jump, 5)
    if not abs(jump - 0.00558) < 1.2e-4:
        return False, dict(reason="slope jump of F* at the kink of the triangle site", jump=jump, left=(f0 - fm) / dl, right=(fp - f0) / dl)
    # theta_na is Lipschitz in the composition
    sites = {k: st_site(*v) for k, v in ST_SITES.items()}
    amax = {k: st_a(s) for k, s in sites.items()}
    for (s1, s2) in (("bin", "path"), ("tri", "asym"), ("bin", "tri")):
        for _ in range(3):
            l1, l2 = float(rng.uniform(0.1, 0.9)), float(rng.uniform(0.1, 0.9))
            x = float(rng.uniform(0.005, 0.05))
            th1 = st_theta_na([(l1, sites[s1]), (1 - l1, sites[s2])], x, grid=30)
            th2 = st_theta_na([(l2, sites[s1]), (1 - l2, sites[s2])], x, grid=30)
            bound = 2 * abs(l1 - l2) * max(amax[s1], amax[s2])
            if abs(th1 - th2) > bound + 1e-7:
                return False, dict(reason="theta_na is not Lipschitz in the composition with constant max a_j", diff=abs(th1 - th2), bound=bound)
            if bound > 0:
                stats["lip"] = max(stats["lip"], abs(th1 - th2) / bound)
    return True, stats


@conjecture("XXII.4 Proposition 11.104 (local ensemble-averaged data do not change the non-adaptive exponent; with Lemma A of the Scientific Discovery Division): for a linear code C whose dual has minimum distance at least k + 1 (here the [7,3] simplex code, k = 2), a centre a and the C-symmetrised cone psi_C = u d(., a + C): the Gibbs measures of psi_C and of its truncation max(psi_C, u r) have exactly uniform marginals on every set of at most k coordinates (so a k-body marginal oracle answers identically on both), while the single cone does not; A(psi_C)/A(psi_C^tr) - 1 >= (A(cone)/A(cone^tr) - 1)/|C| and the two functions differ on at most |C| |B(r-1)| points; hence a non-adaptive algorithm with that oracle needs (1 - 2 delta)/(|C| q) evaluations at the accuracy of the single cone minus ln |C|")
def t_sites_marginal_oracle(rng, trials):
    n = 7
    gens = [0b1010101, 0b0110011, 0b0001111]
    C = sorted({(a * gens[0]) ^ (b * gens[1]) ^ (c * gens[2]) for a in (0, 1) for b in (0, 1) for c in (0, 1)})
    pts = np.arange(1 << n)
    bits = (pts[:, None] >> np.arange(n)[None, :]) & 1
    popc = np.array([bin(x).count("1") for x in range(1 << n)])
    stats = dict(marg=0.0, single=0.0, slack=1e9)
    for _ in range(max(3, trials // 60)):
        u, a = float(rng.uniform(0.3, 1.5)), int(rng.integers(0, 1 << n))
        dC = np.min(np.stack([popc[pts ^ a ^ c] for c in C]), axis=0)          # distance to the coset a + C
        d1 = popc[pts ^ a]
        for r in (1, 2):
            wC, w1 = np.exp(-u * dC), np.exp(-u * d1)
            wCt, w1t = np.minimum(wC, math.exp(-u * r)), np.minimum(w1, math.exp(-u * r))
            for w in (wC, wCt):
                mu = w / w.sum()
                for i in range(n):
                    for j in range(i, n):
                        for vi in (0, 1):
                            for vj in (0, 1):
                                sel = (bits[:, i] == vi) & (bits[:, j] == vj)
                                want = 0.5 if i == j and vi == vj else (0.0 if i == j else 0.25)
                                stats["marg"] = max(stats["marg"], abs(float(mu[sel].sum()) - want))
            m1 = w1 / w1.sum()
            stats["single"] = max(stats["single"], abs(float(m1[bits[:, 0] == 1].sum()) - 0.5))
            lhs = wC.sum() / wCt.sum() - 1
            rhs = (w1.sum() / w1t.sum() - 1) / len(C)
            stats["slack"] = min(stats["slack"], lhs - rhs)
            ball = sum(math.comb(n, j) for j in range(r))
            if stats["marg"] > 1e-12:
                return False, dict(reason="the symmetrised cone or its truncation has a non-uniform marginal of order at most two", err=stats["marg"])
            if lhs < rhs - 1e-12:
                return False, dict(reason="the effect of truncating the symmetrised cone is below that of the single cone divided by |C|", lhs=lhs, rhs=rhs)
            if int((wC != wCt).sum()) > len(C) * ball:
                return False, dict(reason="the symmetrised cone and its truncation differ on more than |C| balls", count=int((wC != wCt).sum()), bound=len(C) * ball)
    if stats["single"] < 1e-3:
        return False, dict(reason="the single cone has uniform one-body marginals (the control has no power)")
    return True, stats


@conjecture("XXI.5 Theorem 11.90(c), integral form, and the remark on more than two letters: on a binary type class the game function of a centre is an integral of the mutual information along the tilting path, t Psi(u) - Psi(tu) = t u int_{tu}^{u} I(s) s^-2 ds with I(s) = F(l(s)) the mutual information at slope s (also for single dips on k equally weighted groups, I_k(s) = ln k - H of the conditional law); for a Potts pair P(b, x) ~ a_b c_x exp(s 1[b = x]) on three letters the mutual information never exceeds the larger of its values for the uniform laws on two and on three letters, which cross at s = 0.519366 (two letters win below)")
def t_slice_integral_potts(rng, trials):
    xs, ws = np.polynomial.legendre.leggauss(24)
    stats = dict(integral=0.0, potts=-1.0)
    for _ in range(max(4, trials // 50)):
        m, k, u, t = float(rng.uniform(0.15, 0.85)), float(rng.uniform(0.15, 0.85)), float(rng.uniform(0.4, 3)), float(rng.uniform(0.15, 0.85))
        s_nodes = 0.5 * (u - t * u) * xs + 0.5 * (u + t * u)

        def I_s(s):
            l = mf_golden(lambda l: -(s * l - sl_F(m, k, l)), 0.0, sl_hi(m, k) * (1 - 1e-13), tol=1e-13)[1]
            return sl_F(m, k, l)
        val = t * u * 0.5 * (u - t * u) * sum(w * I_s(s) / s ** 2 for s, w in zip(s_nodes, ws))
        stats["integral"] = max(stats["integral"], abs(val - (t * sl_Psi(m, k, u) - sl_Psi(m, k, t * u))))
        kk = int(rng.integers(2, 6))
        Ik = lambda s: math.log(kk) + (lambda p: p * math.log(p) + (1 - p) * math.log((1 - p) / (kk - 1)))(math.exp(s) / (math.exp(s) + kk - 1))
        val = t * u * 0.5 * (u - t * u) * sum(w * Ik(s) / s ** 2 for s, w in zip(s_nodes, ws))
        stats["integral"] = max(stats["integral"], abs(val - st_groups(kk, u, t)))
    if stats["integral"] > 1e-7:
        return False, dict(reason="the game function is not the integral of the mutual information along the tilting path", err=stats["integral"])
    I_unif = lambda kk, s: math.log(kk) + (lambda p: p * math.log(p) + (1 - p) * math.log((1 - p) / (kk - 1)))(math.exp(s) / (math.exp(s) + kk - 1))
    if abs(I_unif(2, 0.519366) - I_unif(3, 0.519366)) > 1e-7 or not (I_unif(2, 0.4) > I_unif(3, 0.4) and I_unif(2, 0.7) < I_unif(3, 0.7)):
        return False, dict(reason="crossing of the uniform laws on two and three letters")
    N = max(3000, 60 * trials)
    for s in (0.3, 0.52, 1.0, 2.0):
        fa, fc = rng.normal(0, 1.5, (N, 3)), rng.normal(0, 1.5, (N, 3))
        fa[: N // 4, 2] -= 8.0                                           # tables that nearly live on two letters
        fc[: N // 4, 2] -= 8.0
        fa[: N // 8, :2] = 0.0
        fc[: N // 8, :2] = 0.0
        P = np.exp(fa[:, :, None] + fc[:, None, :] + s * np.eye(3)[None, :, :])
        P /= P.sum(axis=(1, 2), keepdims=True)
        pb, px = P.sum(axis=2, keepdims=True), P.sum(axis=1, keepdims=True)
        mi = (P * np.log(P / (pb * px))).sum(axis=(1, 2))
        bound = max(I_unif(2, s), I_unif(3, s))
        stats["potts"] = max(stats["potts"], float(mi.max() - bound))
        if mi.max() > bound + 1e-9:
            return False, dict(reason="a Potts pair with more mutual information than the uniform laws on two or three letters", s=s, mi=float(mi.max()), bound=bound)
        if s < 0.5 and not mi.max() > I_unif(3, s) + 1e-5:
            return False, dict(reason="below the crossing no table near two letters beats the uniform law on three", s=s)
    return True, stats


# ----------------------------------------------------------------------------------------------
# XXIII. Robust ratios of macrostate weights: the observable free energies (theory report 11.28; SCI-REQ-0001, Q1)
# ----------------------------------------------------------------------------------------------

def mr_closure(D):
    """Shortest-path closure of a matrix of nonnegative costs: a quasi-metric (triangle inequality, zero diagonal)."""
    D = D.copy()
    for k in range(len(D)):
        D = np.minimum(D, D[:, [k]] + D[[k], :])
    np.fill_diagonal(D, 0.0)
    return D


def mr_lp_full(w, D, A, B):
    """R+(A, B) = max sum_A w t subject to sum_B w t = 1 and t(y) <= e^{d(x,y)} t(x) for ALL ordered pairs x != y."""
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    n = len(w)
    rows, cols, vals = [], [], []
    r = 0
    for x in range(n):
        for y in range(n):
            if x != y:
                rows += [r, r]; cols += [y, x]; vals += [1.0, -math.exp(D[x, y])]; r += 1
    Aub = coo_matrix((vals, (rows, cols)), shape=(r, n)).tocsr()
    c = np.zeros(n); c[A] = -w[A]
    Aeq = np.zeros((1, n)); Aeq[0, B] = w[B]
    res = linprog(c, A_ub=Aub, b_ub=np.zeros(r), A_eq=Aeq, b_eq=[1.0], bounds=[(0, None)] * n, method="highs")
    return -res.fun, res.x


def mr_lp_bip(w, D, A, B):
    """The same with the constraints from B to A only (variables on A u B); returns the value and t (nan elsewhere)."""
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    idx = list(B) + list(A)
    pos = {v: i for i, v in enumerate(idx)}
    rows, cols, vals = [], [], []
    r = 0
    for z in B:
        for y in A:
            rows += [r, r]; cols += [pos[y], pos[z]]; vals += [1.0, -math.exp(D[z, y])]; r += 1
    Aub = coo_matrix((vals, (rows, cols)), shape=(r, len(idx))).tocsr()
    c = np.zeros(len(idx)); Aeq = np.zeros((1, len(idx)))
    for y in A:
        c[pos[y]] = -w[y]
    for z in B:
        Aeq[0, pos[z]] = w[z]
    res = linprog(c, A_ub=Aub, b_ub=np.zeros(r), A_eq=Aeq, b_eq=[1.0], bounds=[(0, None)] * len(idx), method="highs")
    t = np.full(len(w), np.nan); t[idx] = res.x
    return -res.fun, t


def mr_lp_dual(w, D, A, B):
    """Transport with gains: min lam s.t. sum_{y in A} e^{d(z,y)} psi(z,y) <= lam w(z), sum_{z in B} psi(z,y) >= w(y), psi >= 0."""
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    nb, na = len(B), len(A)
    nv = nb * na + 1
    c = np.zeros(nv); c[-1] = 1.0
    rows, cols, vals, rhs = [], [], [], []
    r = 0
    for i, z in enumerate(B):
        for j, y in enumerate(A):
            rows.append(r); cols.append(i * na + j); vals.append(math.exp(D[z, y]))
        rows.append(r); cols.append(nv - 1); vals.append(-w[z]); rhs.append(0.0); r += 1
    for j, y in enumerate(A):
        for i in range(nb):
            rows.append(r); cols.append(i * na + j); vals.append(-1.0)
        rhs.append(-w[y]); r += 1
    Aub = coo_matrix((vals, (rows, cols)), shape=(r, nv)).tocsr()
    res = linprog(c, A_ub=Aub, b_ub=np.array(rhs), bounds=[(0, None)] * nv, method="highs")
    return res.fun, res.x[:-1].reshape(nb, na)


def mr_ratio(w, g, A, B):
    return float((w[A] * np.exp(-g[A])).sum() / (w[B] * np.exp(-g[B])).sum())


@conjecture("XXIII.1 Theorem 11.105 (the robust ratio of two macrostate weights R+(A,B) = sup_g Z_g(A)/Z_g(B) over admissible residuals, on random finite spaces with asymmetric envelopes): (a) only the constraints from B to A matter -- the programme with all constraints of the space has the value of the bipartite one; (b) the lowest extension to A followed by the highest extension to B of an optimal residual is optimal, is a fixed point of the two extensions, and is admissible in all four directions; (c) strong duality with transport plans with gains, and weak duality against random admissible residuals; (d) one state against a macrostate in closed form (Theorem 11.12 for B = the rest); (e) the max-min sandwich M/|B| <= R+ <= |A| M with M = max_{y in A} min_{z in B} e^{d(z,y)} w(y)/w(z)")
def t_ratio_duality(rng, trials):
    stats = dict(cases=0, worst_gap=0.0, worst_adm=0.0, tight_lower=math.inf, tight_upper=math.inf)
    for rep in range(max(40, trials // 3)):
        n = int(rng.integers(5, 10))
        D = rng.uniform(0.1, 3.0, size=(n, n))
        if rep % 3 == 0:
            D = (D + D.T) / 2
        D = mr_closure(D)
        w = np.exp(rng.normal(0, 1.5, size=n))
        perm = rng.permutation(n)
        na = int(rng.integers(1, n - 1)); nb = int(rng.integers(1, n - na + 1))
        A = sorted(perm[:na].tolist()); B = sorted(perm[na:na + nb].tolist())
        vf, _ = mr_lp_full(w, D, A, B)
        vb, tb = mr_lp_bip(w, D, A, B)
        vd, psi = mr_lp_dual(w, D, A, B)
        if abs(vf - vb) > 1e-9 * vb:
            return False, dict(reason="the constraints inside A, inside B, from A to B or through other states change the value", full=vf, bipartite=vb)
        if abs(vd - vb) > 1e-9 * vb:
            return False, dict(reason="strong duality with transport plans with gains", primal=vb, dual=vd)
        if (psi < -1e-12).any() or any(sum(math.exp(D[z, y]) * psi[i, j] for j, y in enumerate(A)) > vd * w[z] * (1 + 1e-9) for i, z in enumerate(B)) \
                or any(psi[:, j].sum() < w[y] * (1 - 1e-9) for j, y in enumerate(A)):
            return False, dict(reason="the dual solution is not a feasible plan")
        idx = A + B
        g = np.zeros(n)
        g[idx] = -np.log(np.maximum(tb[idx], 1e-300))
        g1 = g.copy()
        for y in A:
            g1[y] = max(g[z] - D[z, y] for z in B)                  # the lowest admissible values on A
        g2 = g1.copy()
        for z in B:
            g2[z] = min(g1[y] + D[z, y] for y in A)                 # the highest admissible values on B
        back = max(abs(max(g2[z] - D[z, y] for z in B) - g2[y]) for y in A)
        adm = max(g2[x] - g2[y] - D[x, y] for x in idx for y in idx)
        if abs(mr_ratio(w, g2, A, B) - vb) > 1e-9 * vb or back > 1e-9 or adm > 1e-9:
            return False, dict(reason="the closed pair is optimal, a fixed point and admissible in all directions", ratio=mr_ratio(w, g2, A, B), value=vb, fixed_point=back, admissibility=adm)
        stats["worst_adm"] = max(stats["worst_adm"], adm)
        for _ in range(4):
            c = rng.normal(0, 2, size=n)
            gg = np.array([min(c[y] + D[x, y] for y in range(n)) for x in range(n)])       # an admissible residual
            if mr_ratio(w, gg, A, B) > vd * (1 + 1e-9):
                return False, dict(reason="weak duality: an admissible residual exceeds the value of a plan")
        if na == 1:
            closed = w[A[0]] / sum(w[z] * math.exp(-D[z, A[0]]) for z in B)
            if abs(closed - vb) > 1e-9 * vb:
                return False, dict(reason="one state against a macrostate: w(y)/sum_B w(z) e^{-d(z,y)}", closed=closed, value=vb)
        M = max(min(math.exp(D[z, y]) * w[y] / w[z] for z in B) for y in A)
        if not (M / len(B) <= vb * (1 + 1e-9) and vb <= len(A) * M * (1 + 1e-9)):
            return False, dict(reason="max-min sandwich", M=M, value=vb, A=len(A), B=len(B))
        stats["tight_lower"] = min(stats["tight_lower"], vb / (M / len(B)))
        stats["tight_upper"] = min(stats["tight_upper"], len(A) * M / vb)
        stats["worst_gap"] = max(stats["worst_gap"], abs(vf - vb) / vb, abs(vd - vb) / vb)
        stats["cases"] += 1
    return True, stats


def mr_cw_logweights(n, bJ, bB):
    """ln pi(T_j) for the Curie-Weiss known part on Q_n."""
    j = np.arange(n + 1)
    m = (2 * j - n) / n
    lw = np.array([math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) for k in j]) + n * (bJ / 2 * m ** 2 + bB * m)
    return lw - lw.max()


@conjecture("XXIII.2 Theorem 11.106 (symmetric reduction on the cube, any exchangeable known part, envelope u * Hamming, macrostates that are unions of type classes): the programme on all of Q_n has the value of the programme on types with the distances u|j - k|; for separated macrostates (every type of B below every type of A) the extremal residual is the maximal field, R+ = sum_A W_j e^{uj} / sum_B W_k e^{uk}, and it is the only closed symmetric pair; for a band between two parts of B the value exceeds both fields and equals that of the best cone around a type class of the band (in the examples)")
def t_ratio_types(rng, trials):
    stats = dict(cases=0, worst=0.0, band_gain_over_fields=math.inf)
    for n in ((5, 6) if trials < 100 else (5, 6, 7)):
        pts = np.array(list(itertools.product((0, 1), repeat=n)))
        wt = pts.sum(axis=1)
        H = (pts[:, None, :] != pts[None, :, :]).sum(axis=2).astype(float)
        for (bJ, bB, u) in ((0.0, 0.0, 1.0), (1.5, 0.0, 0.7), (0.8, 0.3, 1.3), (-1.0, 0.2, 0.5)):
            lw = mr_cw_logweights(n, bJ, bB)
            W = np.exp(lw)
            wfull = W[wt] / np.array([math.comb(n, int(k)) for k in wt])
            Dt = u * np.abs(np.subtract.outer(np.arange(n + 1), np.arange(n + 1))).astype(float)
            for (At, Bt) in (([k for k in range(n + 1) if k > n // 2], [k for k in range(n + 1) if k <= n // 2]), ([n - 1, n], [0, 1]),
                             ([n // 2, n // 2 + 1], [0, n]), ([2, 3], [0, 1, n - 1, n])):
                A = [i for i in range(len(pts)) if wt[i] in At]; B = [i for i in range(len(pts)) if wt[i] in Bt]
                vfull, _ = mr_lp_bip(wfull, u * H, A, B)
                vtype, _ = mr_lp_bip(W, Dt, At, Bt)
                if abs(vfull - vtype) > 1e-9 * vtype:
                    return False, dict(reason="the programme on Q_n differs from the programme on types", n=n, full=vfull, types=vtype)
                fields = [sum(W[j] * math.exp(s * u * j) for j in At) / sum(W[k] * math.exp(s * u * k) for k in Bt) for s in (1, -1)]
                cones = max(sum(W[j] * math.exp(-u * abs(j - c)) for j in At) / sum(W[k] * math.exp(-u * abs(k - c)) for k in Bt) for c in At)
                if max(Bt) < min(At):
                    if abs(fields[0] - vtype) > 1e-9 * vtype:
                        return False, dict(reason="separated macrostates: the maximal field is extremal", n=n, field=fields[0], value=vtype)
                else:
                    if vtype < max(fields) * (1 + 1e-6) or abs(cones - vtype) > 1e-8 * vtype:
                        return False, dict(reason="a band: the value exceeds both fields and is attained by a cone around a type class", n=n, fields=fields, cone=cones, value=vtype)
                    stats["band_gain_over_fields"] = min(stats["band_gain_over_fields"], vtype / max(fields))
                stats["worst"] = max(stats["worst"], abs(vfull - vtype) / vtype)
                stats["cases"] += 1
    return True, stats


@conjecture("XXIII.3 Theorem 11.107 (one-coordinate macrostates on product spaces with a site-additive envelope): for an additive known part R+ is the value of the single-site programme of that site; for a pairwise known part the single-site value with the marginal weights is a lower bound and the largest single-site value with the weights conditional on the other coordinates is an upper bound (a plan that moves the one coordinate only), and both inequalities are strict in general")
def t_ratio_one_coordinate(rng, trials):
    stats = dict(cases=0, worst_additive=0.0, strict_lower=0, strict_upper=0, largest_upper_gap=0.0)
    for rep in range(max(20, trials // 8)):
        qs = [int(rng.integers(2, 4)) for _ in range(3)]
        Ds = [mr_closure(rng.uniform(0.2, 2.0, size=(q, q))) for q in qs]
        pts = list(itertools.product(*[range(q) for q in qs]))
        D = np.array([[sum(Ds[i][x[i], y[i]] for i in range(3)) for y in pts] for x in pts])
        site = int(rng.integers(3))
        q = qs[site]
        perm = rng.permutation(q)
        na = int(rng.integers(1, q))
        Ai, Bi = sorted(perm[:na].tolist()), sorted(perm[na:].tolist())
        A = [k for k, x in enumerate(pts) if x[site] in Ai]; B = [k for k, x in enumerate(pts) if x[site] in Bi]
        f1 = [rng.normal(0, 1, size=qq) for qq in qs]
        pair = {(i, j): rng.normal(0, 1.0, size=(qs[i], qs[j])) for i in range(3) for j in range(i + 1, 3)}
        rest = sorted({tuple(x[j] for j in range(3) if j != site) for x in pts})
        for kind in ("additive", "pairwise"):
            lw = np.array([sum(f1[i][x[i]] for i in range(3)) + (sum(pair[ij][x[ij[0]], x[ij[1]]] for ij in pair) if kind == "pairwise" else 0.0) for x in pts])
            w = np.exp(lw)
            v, _ = mr_lp_bip(w, D, A, B)
            marg = np.array([sum(w[k] for k, x in enumerate(pts) if x[site] == a) for a in range(q)])
            lo = mr_lp_bip(marg, Ds[site], Ai, Bi)[0]
            hi = 0.0
            for r in rest:
                ws = np.zeros(q)
                for k, x in enumerate(pts):
                    if tuple(x[j] for j in range(3) if j != site) == r:
                        ws[x[site]] = w[k]
                hi = max(hi, mr_lp_bip(ws, Ds[site], Ai, Bi)[0])
            if kind == "additive":
                if abs(lo - v) > 1e-9 * v or abs(hi - v) > 1e-9 * v:
                    return False, dict(reason="additive known part: the single-site programme is exact", value=v, single_site=lo, conditional=hi)
                stats["worst_additive"] = max(stats["worst_additive"], abs(lo - v) / v)
            else:
                if lo > v * (1 + 1e-9) or v > hi * (1 + 1e-9):
                    return False, dict(reason="pairwise known part: marginal <= R+ <= largest conditional", marginal=lo, value=v, conditional=hi)
                stats["strict_lower"] += v > lo * (1 + 1e-6); stats["strict_upper"] += hi > v * (1 + 1e-6)
                stats["largest_upper_gap"] = max(stats["largest_upper_gap"], hi / v)
        stats["cases"] += 1
    if stats["strict_lower"] < stats["cases"] // 2 or stats["strict_upper"] < stats["cases"] // 2:
        return False, dict(reason="the test has no power: the two bounds were expected to be strict in most cases", **stats)
    return True, stats


def mr_lip_vertices(Dq):
    """Vertices of {phi : phi(b) - phi(a) <= Dq[a, b], phi(0) = 0}: the transport cost is W(P -> Q) = max_phi phi . (Q - P)."""
    q = len(Dq)
    cons = [(a, b) for a in range(q) for b in range(q) if a != b]
    V = []
    for S in itertools.combinations(cons, q - 1):
        M = np.zeros((q, q)); rhs = np.zeros(q)
        for r, (a, b) in enumerate(S):
            M[r, b] += 1; M[r, a] -= 1; rhs[r] = Dq[a, b]
        M[q - 1, 0] = 1
        if abs(np.linalg.det(M)) < 1e-12:
            continue
        phi = np.linalg.solve(M, rhs)
        if all(phi[b] - phi[a] <= Dq[a, b] + 1e-9 for a, b in cons) and not any(np.allclose(phi, v) for v in V):
            V.append(phi)
    return np.array(V)


@conjecture("XXIII.4 Theorem 11.108 (the exponential scale; three letters with the law (0.5, 0.3, 0.2), an asymmetric site envelope, macrostates {mean of h >= 1.25} and {mean of h <= 0.5} for h = (0, 1, 2)): the distance between two type classes is the transport cost between their types; for every n, M_n - ln|B-classes| <= ln R+ <= M_n + ln|A-classes| with M_n = max_{P in A} min_{Q in B} [n W(Q,P) + ln W_P - ln W_Q]; the best cone around a type class and the plan 'every class of A is served by its best class of B' bracket ln R+ (the exact value lies between them at n = 12); M_n/n is within 0.6/n of the continuum value max_P min_Q [W(Q,P) + KL(Q||pi) - KL(P||pi)] = 0.4142, and both ends of the bracket are within ln(n)/n above it")
def t_ratio_exponential_scale(rng, trials):
    from scipy.optimize import linprog
    from scipy.special import logsumexp
    Dq = mr_closure(np.array([[0, 1.0, 1.6], [0.7, 0, 1.2], [1.5, 0.9, 0]]))
    V = mr_lip_vertices(Dq)
    pi = np.array([0.5, 0.3, 0.2]); hfun = np.array([0.0, 1.0, 2.0])
    # the transport cost by the vertices against the transport programme
    for _ in range(20):
        P, Q = rng.dirichlet(np.ones(3)), rng.dirichlet(np.ones(3))
        Aeq = np.zeros((6, 9))
        for a in range(3):
            for b in range(3):
                Aeq[a, a * 3 + b] = 1; Aeq[3 + b, a * 3 + b] = 1
        res = linprog(Dq.reshape(-1), A_eq=Aeq, b_eq=np.concatenate([P, Q]), bounds=[(0, None)] * 9, method="highs")
        if abs(res.fun - float((V @ (Q - P)).max())) > 1e-9:
            return False, dict(reason="transport cost by the vertices of the Lipschitz polytope")
    # the continuum value on a grid of the simplex
    m = 120
    grid = np.array([(i / m, j / m, 1 - (i + j) / m) for i in range(m + 1) for j in range(m + 1 - i)])
    I = np.where(grid > 0, grid * np.log(np.maximum(grid, 1e-300) / pi), 0.0).sum(axis=1)
    hv = grid @ hfun
    PA, IA, QB, IB = grid[hv >= 1.25 - 1e-12], I[hv >= 1.25 - 1e-12], grid[hv <= 0.5 + 1e-12], I[hv <= 0.5 + 1e-12]
    cont = max(float(((V[None, :, :] * (P[None, None, :] - QB[:, None, :])).sum(axis=2).max(axis=1) + IB).min() - iP) for P, iP in zip(PA, IA))
    if abs(cont - 0.41441) > 3e-4:
        return False, dict(reason="continuum value (grid of mesh 1/120)", value=cont)
    out = {}
    for n in ((12, 24, 48) if trials < 100 else (12, 24, 48, 96)):
        T = np.array([c for c in itertools.product(range(n + 1), repeat=3) if sum(c) == n])
        lw = np.array([math.lgamma(n + 1) - sum(math.lgamma(k + 1) for k in c) for c in T]) + (T * np.log(pi)).sum(axis=1)
        hv = T @ hfun / n
        At, Bt = np.nonzero(hv >= 1.25 - 1e-12)[0], np.nonzero(hv <= 0.5 + 1e-12)[0]
        TA, TB = T[At].astype(float), T[Bt].astype(float)
        Wm = lambda Xs, Ys: np.concatenate([np.max(np.einsum("vk,xyk->xyv", V, Ys[None, :, :] - Xs[i:i + 200, None, :]), axis=2) for i in range(0, len(Xs), 200)])
        DBA, DAA = Wm(TB, TA), Wm(TA, TA)
        lower = float((logsumexp(lw[At][:, None] - DAA, axis=0) - logsumexp(lw[Bt][:, None] - DBA, axis=0)).max())
        score = DBA - lw[Bt][:, None]
        src = score.argmin(axis=0)
        load = np.full(len(Bt), -np.inf)
        for z, c in zip(src, DBA[src, np.arange(len(At))] + lw[At] - lw[Bt][src]):
            load[z] = np.logaddexp(load[z], c)
        upper = float(load.max())
        Mn = float((score.min(axis=0) + lw[At]).max())
        if not (lower <= upper + 1e-9 and Mn - math.log(len(Bt)) <= lower + 1e-9 and upper <= Mn + math.log(len(At)) + 1e-9):
            return False, dict(reason="cone <= plan, and both within ln(number of classes) of the max-min", n=n, lower=lower, upper=upper, M_n=Mn)
        if n == 12:
            full = np.zeros((len(T), len(T)))
            full[np.ix_(Bt, At)] = DBA
            v, _ = mr_lp_bip(np.exp(lw - lw.max()), full, At.tolist(), Bt.tolist())
            if not (lower - 1e-7 <= math.log(v) <= upper + 1e-7):
                return False, dict(reason="the exact value is not between the cone and the plan", n=n, lower=lower, exact=math.log(v), upper=upper)
            out["exact_12"] = math.log(v) / n
        if abs(Mn / n - cont) > 0.6 / n + 5e-4:
            return False, dict(reason="the max-min on types is not within 0.6/n of the continuum value", n=n, M_n_over_n=Mn / n, continuum=cont)
        if not (cont - 5e-4 <= lower / n and upper / n <= cont + math.log(n) / n):
            return False, dict(reason="the bracket is not within ln(n)/n above the continuum value", n=n, lower=lower / n, upper=upper / n, continuum=cont)
        out[n] = (round(lower / n, 5), round(upper / n, 5), round(Mn / n, 5))
    return True, dict(continuum=cont, brackets=out)


@conjecture("XXIII.5 Proposition 11.109 (a one-body marginal oracle with a field; brute force on Q_10 and Q_8): (a) every one-body marginal of the Gibbs measure of a u-Lipschitz residual lies in the window [p-, p+], logit p+- = logit p +- u; (b) an instance that is invariant under the cyclic shift has all one-body marginals equal to its mean type; (c) for a symmetric null and its deepest dip on a cyclically invariant set, mean type(dip) - mean type(null) = Phi/(1 + Phi) (type of the excess measure - mean type(null)), so the oracle cannot tell them apart iff the excess measure has the null's mean type; along the additive instances gamma|x| the mismatch of the family 'balls of radius 2 around centres of type 3/10' changes sign near gamma = 0, and at the root all marginals of null and alternative agree to 1e-10 while ln A differs by more than 1.1; the family 'radius 1 around centres of type 5/10' has its excess type above every null type and no root")
def t_oracle_field(rng, trials):
    # (a) the window, on random Lipschitz residuals
    n8 = 8
    D8 = na_cube(n8)
    pts8 = np.array(list(itertools.product((0, 1), repeat=n8)))
    worst = 0.0
    for rep in range(max(6, trials // 20)):
        u = float(rng.choice([0.5, 1.0, 2.0])); p = float(rng.uniform(0.1, 0.9))
        psi = na_rand_lipschitz(rng, n8, u, D8, rep % 5)
        lw = pts8.sum(axis=1) * math.log(p) + (n8 - pts8.sum(axis=1)) * math.log(1 - p) - psi
        w = np.exp(lw - lw.max())
        marg = (w[:, None] * pts8).sum(axis=0) / w.sum()
        lo, hi = p * math.exp(-u) / (p * math.exp(-u) + 1 - p), p * math.exp(u) / (p * math.exp(u) + 1 - p)
        if marg.min() < lo - 1e-12 or marg.max() > hi + 1e-12:
            return False, dict(reason="a one-body marginal outside the window", marginals=marg.tolist(), window=(lo, hi))
        worst = max(worst, float(max((marg.max() - lo) / (hi - lo), 0)))
    # (b), (c) on Q_10
    n, p, u = 10, 0.25, 1.0
    pts = np.array(list(itertools.product((0, 1), repeat=n)), dtype=np.int8)
    wt = pts.sum(axis=1)
    H = (pts[:, None, :] != pts[None, :, :]).sum(axis=2).astype(float)
    logpi = wt * math.log(p) + (n - wt) * math.log(1 - p)

    def family(m, rho, symmetrise=True):
        centre = np.array([1] * m + [0] * (n - m), dtype=np.int8)
        Dset = np.zeros(len(pts), dtype=bool)
        for c in (range(n) if symmetrise else range(1)):
            Dset |= (pts != np.roll(centre, c)).sum(axis=1) <= rho
        return Dset

    def pair(Dset, gamma):
        psi = gamma * wt.astype(float)
        alt = psi.copy()
        alt[Dset] = (psi[~Dset][None, :] - u * H[np.ix_(Dset, ~Dset)]).max(axis=1)          # the deepest dip on the set
        out = []
        for f in (psi, alt):
            lw = logpi - f
            w = np.exp(lw - lw.max())
            out.append((lw.max() + math.log(w.sum()), (w[:, None] * pts).sum(axis=0) / w.sum()))
        exc = np.exp(logpi - alt) - np.exp(logpi - psi)
        texc = float((exc * wt).sum() / exc.sum() / n) if exc.sum() > 0 else float("nan")
        return out, texc

    D2 = family(3, 2)
    for gamma in (-0.6, -0.2, 0.3):
        (null, alt), texc = pair(D2, gamma)
        if np.ptp(null[1]) > 1e-12 or np.ptp(alt[1]) > 1e-10:
            return False, dict(reason="a cyclically invariant instance has unequal one-body marginals", spread=float(np.ptp(alt[1])))
        Phi = math.exp(alt[0] - null[0]) - 1
        lhs = float(alt[1].mean() - null[1].mean())
        rhs = Phi / (1 + Phi) * (texc - float(null[1].mean()))
        if abs(lhs - rhs) > 1e-12:
            return False, dict(reason="mean type(dip) - mean type(null) = Phi/(1+Phi) (excess type - null type)", lhs=lhs, rhs=rhs)
    F = lambda g, Dset: (lambda r: float(r[0][1][1].mean() - r[0][0][1].mean()))(pair(Dset, g))
    lo_g, hi_g = -0.1, 0.0
    if not (F(lo_g, D2) < 0 < F(hi_g, D2)):
        return False, dict(reason="the mismatch of the family (3/10, radius 2) does not change sign between gamma = -0.1 and 0", values=(F(lo_g, D2), F(hi_g, D2)))
    for _ in range(50):
        mid = 0.5 * (lo_g + hi_g)
        if F(mid, D2) > 0:
            hi_g = mid
        else:
            lo_g = mid
    (null, alt), _ = pair(D2, 0.5 * (lo_g + hi_g))
    gap, sens = float(np.abs(alt[1] - null[1]).max()), alt[0] - null[0]
    if gap > 1e-10 or sens < 1.1:
        return False, dict(reason="at the root the oracle's answers coincide and the dip is still sensitive", marginal_gap=gap, sensitivity=sens)
    dens = max(float(D2[wt == k].mean()) for k in range(n + 1))
    # the dip is in the class
    psi = 0.5 * (lo_g + hi_g) * wt.astype(float)
    altv = psi.copy(); altv[D2] = (psi[~D2][None, :] - u * H[np.ix_(D2, ~D2)]).max(axis=1)
    if np.abs(altv[:, None] - altv[None, :])[H == 1].max() > u + 1e-12:
        return False, dict(reason="the deepest dip is not u-Lipschitz")
    # a family whose excess type is matched by no additive null
    D1 = family(5, 1)
    vals = [F(g, D1) for g in np.linspace(-0.95, 0.95, 20)]
    if min(vals) <= 0:
        return False, dict(reason="the family (5/10, radius 1) was expected to have its excess type above every null type", values=vals)
    return True, dict(root_gamma=0.5 * (lo_g + hi_g), marginal_gap_at_root=gap, sensitivity_at_root=sens, maxdens_of_the_symmetrised_set=dens, unmatched_family_min_mismatch=min(vals), window_use=worst)


@conjecture("XXIII.6 Robust ratios for monotone macrostates (theory report Theorem 11.106a; the sandwich theorem of the science division, SCI-MSG-0009, by Holley's inequality): on the cube with a submodular known part (additive plus pair terms J_ij x_i x_j, J_ij <= 0) and the envelope with constants c_i^up for raising and c_i^dn for lowering a site, for every up-set B and A its complement the robust ratio R+(A, B) is attained at the uniform field g = sum_i c_i^up x_i and R+(B, A) at g = -sum_i c_i^dn x_i — exact linear programmes; both hypotheses are needed: with a frustrated known part, or with a macrostate that is not monotone, the field is strictly suboptimal in some instances")
def t_ratio_monotone(rng, trials):
    stats = dict(cases=0, worst=0.0, frustrated_fail=0, nonmonotone_fail=0, controls=0)
    for rep in range(max(60, trials // 5)):
        n = int(rng.integers(3, 6))
        X = np.array(list(itertools.product((0, 1), repeat=n)))
        cu, cd = rng.uniform(0.2, 1.5, size=n), rng.uniform(0.2, 1.5, size=n)
        up = (X[:, None, :] > X[None, :, :])                                   # x above y at site i
        D = (up * cu).sum(axis=2) + ((X[:, None, :] < X[None, :, :]) * cd).sum(axis=2)   # d(x, y): g(x) - g(y) <= d(x, y)
        hfield = rng.normal(0, 1, size=n)
        J = -np.abs(rng.normal(0, 0.8, size=(n, n)))
        J = np.triu(J, 1)
        mode = rep % 3                                                         # 0: hypotheses hold; 1: frustrated; 2: non-monotone macrostate
        if mode == 1:
            J = np.triu(rng.normal(0, 1.2, size=(n, n)), 1)
            J[0, 1] = abs(J[0, 1]) + 0.5
        f = X @ hfield + np.einsum("xi,ij,xj->x", X, J, X)
        w = np.exp(-(f - f.min()))
        # a random up-set: the up-closure of a few points
        gens = X[rng.choice(len(X), size=int(rng.integers(1, 4)), replace=False)]
        inB = np.zeros(len(X), dtype=bool)
        for gpt in gens:
            inB |= np.all(X >= gpt, axis=1)
        if mode == 2:
            flip = rng.choice(len(X), size=2, replace=False)
            inB[flip] = ~inB[flip]
        if inB.all() or not inB.any():
            continue
        B, A = list(np.flatnonzero(inB)), list(np.flatnonzero(~inB))
        val_up, _ = mr_lp_bip(w, D, A, B)
        val_dn, _ = mr_lp_bip(w, D, B, A)
        field_up = mr_ratio(w, X @ cu, A, B)
        field_dn = mr_ratio(w, -(X @ cd), B, A)
        gap = max(math.log(val_up / field_up), math.log(val_dn / field_dn))
        if gap < -1e-7:
            return False, dict(reason="a field beats the linear programme: the field is not admissible?", gap=gap)
        if mode == 0:
            if gap > 1e-7:
                return False, dict(reason="the uniform field is not optimal although the known part is submodular and the macrostate monotone", gap=gap, n=n)
            stats["cases"] += 1
            stats["worst"] = max(stats["worst"], gap)
        else:
            stats["controls"] += 1
            if gap > 1e-6:
                stats["frustrated_fail" if mode == 1 else "nonmonotone_fail"] += 1
    if stats["cases"] < 10 or stats["frustrated_fail"] == 0 or stats["nonmonotone_fail"] == 0:
        return False, dict(reason="hypotheses not exercised, or the controls never fail", **stats)
    return True, stats


# ---------------------------------------------------------------------------------------------------------------------
# XXIII.7  A one-body oracle with a field: the compensation lemma of the Scientific Discovery Division (SCI-RES-0006),
#          Theorem 11.109a, and the corrected numbers of Proposition 11.109b.   Helpers cp_*.
# ---------------------------------------------------------------------------------------------------------------------
def cp_window(p, u):
    q = 1 - p
    return p * math.exp(-u) / (q + p * math.exp(-u)), p * math.exp(u) / (q + p * math.exp(u))


def cp_lip(w, n):
    """Largest |ln w(x) - ln w(x^i)| over the edges of the cube (w indexed by itertools.product order)."""
    lw = np.log(w).reshape((2,) * n)
    return max(float(np.abs(np.take(lw, 0, axis=i) - np.take(lw, 1, axis=i)).max()) for i in range(n))


def cp_lnH(n, k, p, u, g, r):
    """ln of H_{k,r} = max_x P_{s uniform in T_k}[x in the support of the dip of depth r at s on the base gamma], by sums over
    joint types: x is in the support iff Phi_s(x) = sum_i ln(pi_gamma(x_i)/pi_{s_i}(x_i)) < r."""
    q = 1 - p
    pg = p * math.exp(-g) / (q + p * math.exp(-g))
    pm, pp = cp_window(p, u)
    l = {(a, b): math.log(((1 - pg, pg)[a]) / (((1 - pm, pm), (1 - pp, pp))[b][a])) for a in (0, 1) for b in (0, 1)}
    lf = np.cumsum(np.concatenate([[0.0], np.log(np.arange(1, n + 1))]))              # ln j!
    lb = lambda N, K: lf[N] - lf[K] - lf[N - K]
    best = -math.inf
    for j in range(n + 1):
        i = np.arange(max(0, k - (n - j)), min(j, k) + 1)                              # ones of x inside the ones of s
        Phi = i * l[(1, 1)] + (j - i) * l[(1, 0)] + (k - i) * l[(0, 1)] + (n - j - k + i) * l[(0, 0)]
        sel = i[Phi < r]
        if len(sel) == 0:
            continue
        lw = lb(j, sel) + lb(n - j, k - sel) - lb(n, k)
        best = max(best, float(lw.max() + math.log(np.exp(lw - lw.max()).sum())))
    return best


def cp_rho(p, u, g, t, m):
    """rho_t(m; gamma) = max over the letter a of (1 - m)(pi_0(a)/pi_gamma(a))^t + m (pi_1(a)/pi_gamma(a))^t."""
    q = 1 - p
    pg = p * math.exp(-g) / (q + p * math.exp(-g))
    pm, pp = cp_window(p, u)
    return max((1 - m) * ((1 - pm, pm)[a] / (1 - pg, pg)[a]) ** t + m * ((1 - pp, pp)[a] / (1 - pg, pg)[a]) ** t for a in (0, 1))


def cp_R0(e, p, u):
    """Hinted exponent of the zero residual, max_m [h(m) - h((Lambda_m + e)/u)]_+ (Theorem 11.59(c)), by golden section on
    three brackets."""
    q, L0, L1 = fd_consts(p, u)
    hb = lambda x: 0.0 if x <= 0 or x >= 1 else -x * math.log(x) - (1 - x) * math.log(1 - x)

    def val(m):
        x = ((1 - m) * L0 + m * L1 + e) / u
        return 0.0 if x >= 0.5 else hb(m) - hb(max(x, 0.0))
    ms = np.linspace(1e-6, 1 - 1e-6, 401)
    i = int(np.argmax([val(m) for m in ms]))
    a, b = ms[max(i - 1, 0)], ms[min(i + 1, len(ms) - 1)]
    for _ in range(80):
        c1, c2 = a + 0.382 * (b - a), a + 0.618 * (b - a)
        a, b = (a, c2) if val(c1) > val(c2) else (c1, b)
    return max(0.0, val(0.5 * (a + b)))


def cp_profile(m, v0, v1, e, p, u):
    """Hitting exponent of the dips around the shell of profile (v0, v1) of centres of type m at the zero residual:
    min{ I(M, V') : u sum_phi M(phi)|v'_phi - v_phi| <= e + D(V || pi | M) }  (the two block laws move towards each other)."""
    kl = lambda a, b: (a * math.log(a / b) if a > 0 else 0.0) + ((1 - a) * math.log((1 - a) / (1 - b)) if a < 1 else 0.0)
    budget = (e + (1 - m) * kl(v0, p) + m * kl(v1, p)) / u
    (lo, wlo), (hi, whi) = sorted([(v0, 1 - m), (v1, m)])
    if budget >= min(wlo, whi) * (hi - lo):
        return 0.0

    def obj(a):
        b = (budget - wlo * a) / whi
        A, B = lo + a, hi - b
        if b < 0 or A >= B:
            return 0.0 if A >= B else math.inf
        bar = wlo * A + whi * B
        return wlo * kl(A, bar) + whi * kl(B, bar)
    a, b = 0.0, budget / wlo
    for _ in range(90):
        c1, c2 = a + 0.382 * (b - a), a + 0.618 * (b - a)
        a, b = (a, c2) if obj(c1) < obj(c2) else (c1, b)
    return min(obj(0.5 * (a + b)), obj(0.0), obj(budget / wlo))


@conjecture("XXIII.7 A one-body marginal oracle with a field — the compensation lemma and Theorems A, B of the Scientific Discovery Division (SCI-RES-0006; theory report Theorem 11.109a, Proposition 11.109b), re-derived and replicated with own code: on Q_n with the reference Bernoulli(p)^n, for the cyclic average of the cone dips of depth r around the shifts of a centre of type k/n on an additive base gamma, the excess has mass in [e^r - 1, e^r] and mean type within 1/(e^r - 1) of the cone law's; if that type is in the open window, the base plus b times an extreme additive instance, b = (c_Delta - p_gamma)/(p_2 - c_Delta), and the same plus the excess are class members whose one-body marginals all equal c_Delta, with ln A differing by ln(1 + E/(1 + b)), while without the compensator the marginals differ by Phi/(1 + Phi)(c_Delta - p_gamma); the fraction H of centres whose dip contains a given point satisfies H <= (n + 1) e^{tr} rho_t(k/n; gamma)^n for every t, and at the saddle of R^max the bound 1/(nH) has an exponent that approaches R^max from below (exact sums over joint types, n = 400, 1600); at p = 1/4, u = 1, e = 0.02 the hinted exponent of the zero residual is 0.013669, the tilt bound min_lambda R_0(e - c(lambda); theta - lambda) is 0.012941 and equals the supremum over two-block profiles of mean type p, whose maximiser has a block law outside the window; with block laws in the window the supremum is 0.012635")
def t_compensation(rng, trials):
    stats = dict(cases=0, outside=0, worst_marginal=0.0, least_unmatched=math.inf)
    for _ in range(max(8, trials // 40)):
        n = int(rng.integers(6, 9)); p = float(rng.uniform(0.1, 0.9)); u = float(rng.uniform(0.5, 2.0))
        gam = float(rng.uniform(-u, u)); k = int(rng.integers(1, n)); r = float(rng.uniform(0.7, 4.0))
        X = np.array(list(itertools.product((0, 1), repeat=n)), dtype=float)
        wt = X.sum(axis=1)
        q = 1 - p
        pi = p ** wt * q ** (n - wt)
        pg = lambda g: p * math.exp(-g) / (q + p * math.exp(-g))
        wtil = lambda g: np.exp(-g * wt) / (q + p * math.exp(-g)) ** n
        pm, pp = cp_window(p, u)
        Z0, Z1 = q + p * math.exp(-u), p + q * math.exp(-u)
        base = wtil(gam)
        s = np.array([1.0] * k + [0.0] * (n - k))
        dips = []
        for j in range(n):
            sj = np.roll(s, j)
            cone = np.exp(-u * np.abs(X - sj[None, :]).sum(axis=1)) / (Z0 ** (n - k) * Z1 ** k)
            dips.append(np.maximum(math.exp(r) * cone - base, 0.0))
        Dbar = sum(dips) / n
        E = float((pi * Dbar).sum())
        c = float((pi * Dbar * wt).sum() / (n * E))
        c0 = (1 - k / n) * pm + (k / n) * pp
        if not (math.exp(r) - 1 - 1e-10 <= E <= math.exp(r) + 1e-10):
            return False, dict(reason="mass of the excess outside [e^r - 1, e^r]", E=E, r=r)
        if abs(c - c0) > 1 / (math.exp(r) - 1) + 1e-10:
            return False, dict(reason="mean type of the excess further than 1/(e^r - 1) from the cone law", c=c, c0=c0, r=r)
        marg = lambda w: ((pi * w)[:, None] * X).sum(axis=0) / float((pi * w).sum())
        Phi = E / float((pi * base).sum())
        un = marg(base + Dbar)
        if np.abs(un - (pg(gam) + Phi / (1 + Phi) * (c - pg(gam)))).max() > 1e-11:
            return False, dict(reason="criterion: marginals of the uncompensated alternative", n=n, k=k)
        if not (pm < c < pp):
            stats["outside"] += 1
            continue
        p2, g2 = (pp, -u) if c > pg(gam) else (pm, u)
        b = (c - pg(gam)) / (p2 - c)
        if b < 0:
            return False, dict(reason="negative weight of the compensator", b=b)
        w0 = base + b * wtil(g2)
        w1 = w0 + Dbar
        if cp_lip(w0, n) > u + 1e-10 or cp_lip(w1, n) > u + 1e-10:
            return False, dict(reason="a compensated instance is not in the class", n=n, k=k, lip=(cp_lip(w0, n), cp_lip(w1, n)))
        err = float(max(np.abs(marg(w0) - c).max(), np.abs(marg(w1) - c).max()))
        stats["worst_marginal"] = max(stats["worst_marginal"], err)
        if err > 1e-11:
            return False, dict(reason="one-body marginals of null and alternative are not all equal to the excess type", err=err, n=n, k=k, b=b)
        gap = math.log(float((pi * w1).sum()) / float((pi * w0).sum()))
        if abs(gap - math.log(1 + E / (1 + b))) > 1e-10:
            return False, dict(reason="ln A(w1) - ln A(w0) != ln(1 + E/(1 + b))", gap=gap, E=E, b=b)
        if ((w1 != w0) != (Dbar > 0)).any():
            return False, dict(reason="null and alternative do not differ exactly on the support of the excess")
        stats["least_unmatched"] = min(stats["least_unmatched"], abs(Phi / (1 + Phi) * (c - pg(gam))))
        stats["cases"] += 1
    if stats["cases"] < 4:
        return False, dict(reason="compensation not exercised", **stats)
    # Theorem A at the saddle of R^max, (p, u) = (0.3, 1), e = 0.3 E: exact sums over joint types
    p, u = 0.3, 1.0
    T = np.linspace(1e-4, 1, 2001)
    Fs, F0, gs = fd_fstar(p, u, T, ngam=801)
    E_thr = float((Fs / T).max())
    e = 0.3 * E_thr
    it = int((Fs - T * e).argmax())
    Rmax, ts, gam = float((Fs - T * e)[it]), float(T[it]), float(gs[it])
    ms = np.linspace(0.01, 0.99, 981)
    mstar = float(ms[int(np.argmin([cp_rho(p, u, gam, ts, m) for m in ms]))])
    if abs(Rmax - 0.012210) > 3e-5 or abs(-math.log(cp_rho(p, u, gam, ts, mstar)) - float(Fs[it])) > 1e-5:
        return False, dict(reason="saddle of R^max at (0.3, 1), e = 0.3E", Rmax=Rmax, t=ts, gamma=gam, m=mstar)
    pm, pp = cp_window(p, u)
    om = pp - pm
    expo = []
    for n in (400, 1600):
        k = round(mstar * n)
        m = k / n
        omm = om * min(m, 1 - m)
        eps = e * n
        lo, hi = 1e-9, eps + 50.0                                           # least r with ln(1 + (e^r - 1)/(1 + beta(r))) > eps
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            kap = omm - 1 / math.expm1(mid)
            lo, hi = (lo, mid) if kap > 0 and math.log1p(math.expm1(mid) / (1 + om / kap)) > eps else (mid, hi)
        r = hi
        kap = omm - 1 / math.expm1(r)                                       # the gain of every alternative exceeds the accuracy:
        if not (kap > 0 and math.log1p(math.expm1(r) / (1 + om / kap)) > eps):   # E >= e^r - 1 and b <= omega/kappa
            return False, dict(reason="the certified gain ln(1 + (e^r - 1)/(1 + beta)) does not exceed the accuracy", n=n, r=r, eps=eps)
        lH = cp_lnH(n, k, p, u, gam, r)
        for t in np.linspace(0.0, 1.5, 61):
            if lH > math.log(n + 1) + t * r + n * math.log(cp_rho(p, u, gam, t, m)) + 1e-9:
                return False, dict(reason="H > (n + 1) e^{tr} rho_t^n", n=n, t=float(t), lnH=lH)
        expo.append((-lH - math.log(n)) / n)
    stats.update(Rmax=round(Rmax, 6), bound_400=round(expo[0], 6), bound_1600=round(expo[1], 6))
    if not (expo[0] < expo[1] < Rmax and expo[1] > 0.7 * Rmax):
        return False, dict(reason="the lower bound with the oracle does not approach R^max from below", **stats)
    # the numbers at the test point of Proposition 11.109b
    p, u, e = 0.25, 1.0, 0.02
    pm, pp = cp_window(p, u)
    r0 = cp_R0(e, p, u)
    cl = lambda lam: math.log(1 - p + p * math.exp(lam)) - lam * p
    tl = lambda lam: cp_R0(e - cl(lam), 1 / (1 + math.exp(-(math.log(p / (1 - p)) + lam))), u) if cl(lam) < e else math.inf
    lams = np.linspace(-0.4, 0.2, 61)
    i = int(np.argmin([tl(lam) for lam in lams]))
    a, b = lams[max(i - 1, 0)], lams[min(i + 1, len(lams) - 1)]
    for _ in range(50):
        c1, c2 = a + 0.382 * (b - a), a + 0.618 * (b - a)
        a, b = (a, c2) if tl(c1) < tl(c2) else (c1, b)
    tilt = tl(0.5 * (a + b))
    free, arg, win = 0.0, None, 0.0
    for m in np.linspace(0.30, 0.70, 41):                                    # two-block profiles of mean type p
        for v1 in np.linspace(0.05, 0.60, 111):
            v0 = (p - m * v1) / (1 - m)
            if not 1e-6 < v0 < 1 - 1e-6:
                continue
            val = cp_profile(m, v0, v1, e, p, u)
            if val > free:
                free, arg = val, (float(m), float(v0), float(v1))
            if pm <= v0 <= pp and pm <= v1 <= pp:
                win = max(win, val)
    for m in np.linspace(arg[0] - 0.01, arg[0] + 0.01, 21):                  # refinement around the maximiser
        for v1 in np.linspace(arg[2] - 0.005, arg[2] + 0.005, 21):
            val = cp_profile(m, (p - m * v1) / (1 - m), v1, e, p, u)
            if val > free:
                free, arg = val, (float(m), float((p - m * v1) / (1 - m)), float(v1))
    for wa in np.linspace(0.45, 0.65, 401):                                  # one block at the lower end of the window
        vb = (p - wa * pm) / (1 - wa)
        if vb <= pp:
            win = max(win, cp_profile(1 - wa, pm, vb, e, p, u))
    stats.update(R0=round(r0, 6), tilt=round(tilt, 6), free=round(free, 6), window=round(win, 6))
    if abs(r0 - 0.013669) > 2e-6 or abs(tilt - 0.012941) > 3e-6 or abs(win - 0.012635) > 4e-6:
        return False, dict(reason="numbers at p = 1/4, u = 1, e = 0.02", **stats)
    if abs(free - tilt) > 2e-5 or not (win < tilt < r0):
        return False, dict(reason="the supremum over profiles of type p is not the tilt bound, or the order window < tilt < R_0 fails", **stats)
    if pm <= min(arg[1], arg[2]) and max(arg[1], arg[2]) <= pp:
        return False, dict(reason="the maximising profile of type p has both block laws in the window", arg=arg, window=(pm, pp))
    return True, stats


# ---------------------------------------------------------------------------------------------------------------
# XXIV. Sup-norm (box) classes around a known function whose Gibbs measure can be sampled (theory report 11.30)
# ---------------------------------------------------------------------------------------------------------------

def bx_jensen_gap(w):
    """Largest Jensen gap ln E e^Y - E Y of a random variable with range w."""
    return math.log(math.expm1(w) / w) - 1 + w / math.expm1(w)


def bx_range(w, r, lo, hi, Q):
    """Exact range of ln Z = ln sum_x w e^{-r} over the box, given the values of r on Q."""
    mask = np.ones(len(w), dtype=bool)
    mask[list(Q)] = False
    S = float((w[~mask] * np.exp(-r[~mask])).sum())
    return math.log(S + float((w[mask] * np.exp(-hi[mask])).sum())), math.log(S + float((w[mask] * np.exp(-lo[mask])).sum()))


def bx_weights(w, r, lo, hi):
    return w * (np.exp(-lo) - np.exp(-r)), w * (np.exp(-r) - np.exp(-hi))


@conjecture("XXIV.1 Box classes lo <= r <= hi around a known function with Gibbs weights w (theory report Theorem 11.110(a),(b)): ln Z - ln Z0 = ln E_pi e^{-r} lies in [-E_pi r, -E_pi r + L(w)], L(w) = ln((e^w - 1)/w) - 1 + w/(e^w - 1) <= w^2/8 the largest Jensen gap of a variable of range w (attained by a two-point law); after evaluations on Q the possible values of ln Z fill exactly the interval between 'hi off Q' and 'lo off Q'; at the centre of a constant box the smallest deterministic certificate consists of the heaviest points up to mass 1 - q*, q* = (e^eps - 1)/(e^rho_minus - e^(eps - rho_plus) + e^eps - 1)")
def t_box_deterministic(rng, trials):
    stats = dict(gaps=0, certs=0)
    for wd in (0.2, 0.7, 1.5, 3.0, 6.0, 12.0):
        ts = np.linspace(0, 1, 100001)
        two = np.log1p(ts * math.expm1(wd)) - ts * wd
        if abs(float(two.max()) - bx_jensen_gap(wd)) > 1e-6 or bx_jensen_gap(wd) > wd * wd / 8 + 1e-12:
            return False, dict(reason="closed form of the largest Jensen gap", width=wd, formula=bx_jensen_gap(wd), two_point=float(two.max()))
        for _ in range(200):
            k = int(rng.integers(2, 7))
            y, p = rng.uniform(0, wd, size=k), rng.dirichlet(np.ones(k))
            if math.log(float(p @ np.exp(y))) - float(p @ y) > bx_jensen_gap(wd) + 1e-9:
                return False, dict(reason="a law with a larger Jensen gap than the two-point law", width=wd)
            stats["gaps"] += 1
    for _ in range(max(60, trials // 4)):
        n = int(rng.integers(4, 11))
        w = rng.dirichlet(np.ones(n) * float(rng.uniform(0.3, 2.0)))
        lo, hi = -rng.uniform(0.2, 3.0, size=n), rng.uniform(0.2, 3.0, size=n)
        r = rng.uniform(lo, hi)
        Q = [i for i in range(n) if rng.random() < 0.5]
        a, b = bx_range(w, r, lo, hi, Q)
        # random members agreeing with r on Q stay inside, and the two ends are members
        for _ in range(20):
            rp = rng.uniform(lo, hi)
            rp[Q] = r[Q]
            v = math.log(float(w @ np.exp(-rp)))
            if v < a - 1e-12 or v > b + 1e-12:
                return False, dict(reason="a member outside the claimed range of ln Z")
        # Jensen bracket at the instance
        lnratio = math.log(float(w @ np.exp(-r)))
        mean_r = float(w @ r)
        width = float(hi.max() - lo.min())
        if not (-mean_r - 1e-12 <= lnratio <= -mean_r + bx_jensen_gap(width) + 1e-12):
            return False, dict(reason="Jensen bracket violated", lnratio=lnratio, mean=mean_r)
    for n, rho_m, rho_p in ((10, 2.0, 1.0), (11, 1.0, 3.0), (12, 3.5, 0.5)):
        w = rng.dirichlet(np.ones(n) * 0.7)
        lo, hi, r0 = -rho_m * np.ones(n), rho_p * np.ones(n), np.zeros(n)
        order = np.argsort(-w)
        for eps in (0.05, 0.2, 0.6):
            best = next(k for k in range(n + 1)
                        if any((lambda ab: ab[1] - ab[0])(bx_range(w, r0, lo, hi, Q)) <= eps + 1e-12 for Q in itertools.combinations(range(n), k)))
            qstar = math.expm1(eps) / (math.exp(rho_m) - math.exp(eps - rho_p) + math.expm1(eps))
            formula = next(k for k in range(n + 1) if 1 - float(w[order[:k]].sum()) <= qstar + 1e-12)
            if best != formula:
                return False, dict(reason="smallest deterministic certificate differs from 'heaviest points up to mass 1 - q*'", n=n, eps=eps, brute=best, formula=formula)
            stats["certs"] += 1
    return True, stats


@conjecture("XXIV.2 Sampling certificates in a box class (theory report Theorem 11.110(c); BoxClass.lean: Zw_sub_le_dip, Zw_sub_le_bump, detect_ge, box_spotCheck_correct): a member that differs from r only on D raises Z by at most the dip weight sum_D w(e^{-lo} - e^{-r}) and lowers it by at most the bump weight sum_D w(e^{-r} - e^{-hi}), with equality at the ends of the box; hence every member with |ln Z' - ln Z| > eta differs from r on a set of probability at least p = (1/2) min((e^eta - 1) Z/U, (1 - e^{-eta}) Z/V) under the sampler (1/2) dip/U + (1/2) bump/V; the least detection probability of a far member in the linear relaxation (a fractional knapsack) lies between p and 2p, is exactly 2p at the centre of a constant box and close to p in generic instances; and the spot check with ceil(ln(1/delta)/p) samples misses the hardest far member with frequency at most delta")
def t_box_sampling(rng, trials):
    from scipy.optimize import linprog
    stats = dict(pairs=0, instances=0, worst_over_p=float("inf"), miss=0.0)
    for _ in range(max(2000, 5 * trials)):
        n = int(rng.integers(3, 10))
        w = rng.dirichlet(np.ones(n))
        lo, hi = -rng.uniform(0.2, 3.0, size=n), rng.uniform(0.2, 3.0, size=n)
        r = rng.uniform(lo, hi)
        rp = r.copy()
        D = rng.random(n) < 0.5
        mode = int(rng.integers(3))
        rp[D] = lo[D] if mode == 0 else (hi[D] if mode == 1 else rng.uniform(lo[D], hi[D]))
        D = rp != r
        Z, Zp = float(w @ np.exp(-r)), float(w @ np.exp(-rp))
        dip, bump = bx_weights(w, r, lo, hi)
        if Zp - Z > float(dip[D].sum()) + 1e-12 or Z - Zp > float(bump[D].sum()) + 1e-12:
            return False, dict(reason="change of the partition sum exceeds the dip or bump weight of the difference set")
        if mode == 0 and abs(Zp - Z - float(dip[D].sum())) > 1e-12:
            return False, dict(reason="dip weight not attained at the floor")
        if mode == 1 and abs(Z - Zp - float(bump[D].sum())) > 1e-12:
            return False, dict(reason="bump weight not attained at the ceiling")
        stats["pairs"] += 1
    most = 0.0
    for it in range(max(100, trials // 4)):
        n = int(rng.integers(6, 40))
        w = rng.dirichlet(np.ones(n))
        lo, hi = -rng.uniform(0.5, 4.0, size=n), rng.uniform(0.2, 3.0, size=n)
        r = rng.uniform(lo, hi)
        if it % 5 == 0:                                                        # the centre of a constant box: the sampler is pi
            lo, hi, r = np.full(n, lo[0]), np.full(n, hi[0]), np.zeros(n)     # itself and the relaxation's optimum is exactly 2p
        eta = float(rng.uniform(0.02, 0.5))
        Z = float(w @ np.exp(-r))
        dip, bump = bx_weights(w, r, lo, hi)
        U, V = float(dip.sum()), float(bump.sum())
        q = 0.5 * dip / U + 0.5 * bump / V
        p = 0.5 * min(math.expm1(eta) * Z / U, -math.expm1(-eta) * Z / V)
        vals = []
        for wt, need in ((dip, math.expm1(eta) * Z), (bump, -math.expm1(-eta) * Z)):
            if wt.sum() > need * (1 + 1e-9):                                   # a far member of this kind exists
                res = linprog(q, A_ub=[-wt], b_ub=[-need], bounds=[(0, 1)] * n, method="highs")
                vals.append(float(res.fun))
        if not vals:
            continue
        worst = min(vals)
        if worst < p - 1e-9:
            return False, dict(reason="a far member is detected with probability below p", p=p, worst=worst)
        if worst > 2 * p + 1e-9:
            return False, dict(reason="the least detection probability exceeds 2p: the bound p would be loose by more than its factor 1/2", p=p, worst=worst)
        stats["worst_over_p"] = min(stats["worst_over_p"], worst / p)
        most = max(most, worst / p)
        if it % 5 == 0 and abs(worst - 2 * p) > 1e-7 * p:
            return False, dict(reason="at the centre of a constant box the least detection probability of the relaxation is not exactly 2p", p=p, worst=worst)
        stats["instances"] += 1
    stats["most_over_p"] = most
    if not (stats["worst_over_p"] < 1.5 and most > 2 - 1e-6):
        return False, dict(reason="the two ends of the interval [p, 2p] are not both approached", **stats)
    # simulation at the centre of a constant box: the hardest far member is a dip of mass just above p0 at the floor
    n, rho_m, eps, delta = 4000, 3.0, 0.3, 0.1
    w = rng.dirichlet(np.ones(n) * 3.0)
    eta = eps / 2
    p0 = math.expm1(eta) / math.expm1(rho_m)                                   # pi-mass that a sensitive dip set must exceed
    order = rng.permutation(n)
    k = int(np.searchsorted(np.cumsum(w[order]), p0)) + 1
    Dset = order[:k]
    massD = float(w[Dset].sum())
    if not math.log(1 + massD * math.expm1(rho_m)) > eta:
        return False, dict(reason="test construction: the dip is not far")
    # sampler at the centre: 1/2 dip/U + 1/2 bump/V = pi; detection probability of this member is massD >= p0 >= p
    N = math.ceil(math.log(1 / delta) / p0)
    reps = 4000
    hits = rng.random((reps, 1)) < 1 - (1 - massD) ** N                        # exact miss probability, sampled as Bernoulli
    exact_miss = (1 - massD) ** N
    stats["miss"] = float(exact_miss)
    if exact_miss > delta + 1e-12 or abs(float(hits.mean()) - (1 - exact_miss)) > 0.03:
        return False, dict(reason="the spot check misses the hardest dip too often", miss=exact_miss, delta=delta)
    return True, stats


@conjecture("XXIV.3 Lower bound in a box class and the size-free bracket (theory report Theorem 11.110(d); BoxClass.lean: logZ_dipAlt_gt, box_expected_queries_ge): at the centre of the constant box [-rho_minus, rho_plus], a set of pi-mass above p0 = (e^eps - 1)/(e^rho_minus - 1) lowered to the floor changes ln Z by more than eps; if no atom of pi exceeds p0 there are at least floor(1/(2 p0)) disjoint such sets, so every randomised algorithm makes at least (1 - 2 delta) floor(1/(2 p0)) evaluations, against ceil(ln(1/delta)/p) for the spot check, p = min(1, (1/2) min((e^{eps/2} - 1)/(e^rho_minus - 1), (1 - e^{-eps/2})/(1 - e^{-rho_plus}))): the two differ by a factor that depends on eps and delta only, not on the number of states")
def t_box_lower_bound(rng, trials):
    stats = {}
    delta = 0.05
    for n, rho_m, rho_p, eps in ((4096, 3.0, 1.0, 0.2), (65536, 4.0, 2.0, 0.1), (400000, 5.0, 0.5, 0.1), (400000, 5.0, 5.0, 0.05)):
        w = rng.dirichlet(np.ones(n) * 5.0)
        p0 = math.expm1(eps) / math.expm1(rho_m)
        if float(w.max()) > p0:
            return False, dict(reason="test construction: an atom heavier than p0", n=n)
        k, acc = 0, 0.0
        for x in w:                                                            # greedy packing in a fixed order
            acc += float(x)
            if acc > p0:
                if not math.log(1 + acc * math.expm1(rho_m)) > eps:
                    return False, dict(reason="a set of mass above p0 lowered to the floor is not sensitive")
                k, acc = k + 1, 0.0
        if k < math.floor(1 / (2 * p0)):
            return False, dict(reason="fewer disjoint sensitive dips than floor(1/(2 p0))", found=k, bound=math.floor(1 / (2 * p0)))
        p = min(1.0, 0.5 * min(math.expm1(eps / 2) / math.expm1(rho_m), -math.expm1(-eps / 2) / -math.expm1(-rho_p)))
        upper = math.ceil(math.log(1 / delta) / p)
        lower = (1 - 2 * delta) * math.floor(1 / (2 * p0))
        ratio_bound = 4 * math.log(1 / delta) / (1 - 2 * delta) * math.expm1(eps) / math.expm1(eps / 2) * 1.05 + 1
        if upper / lower > ratio_bound:
            return False, dict(reason="upper and lower bound differ by more than the size-free factor", upper=upper, lower=lower, bound=ratio_bound)
        stats[f"n{n}_rho{rho_m}_eps{eps}"] = (round(lower, 1), upper)
    # the cost does not depend on the number of states: same box, growing n
    costs = []
    for n in (10 ** 4, 10 ** 5, 10 ** 6):
        p = 0.5 * min(math.expm1(0.1) / math.expm1(3.0), -math.expm1(-0.1) / -math.expm1(-1.0))
        costs.append(math.ceil(math.log(1 / delta) / p))
    if len(set(costs)) != 1:
        return False, dict(reason="spot-check cost depends on the number of states")
    return True, stats


@conjecture("XXIV.4 A sup-norm bound caps the cost of a first-order class (theory report Corollary 11.111): on the cube with per-site slope u, the members of the class that also satisfy -rho <= g <= rho form a subclass of the box, so at the zero residual the spot check with the uniform sampler needs at most ceil(2 ln(1/delta) max((e^rho - 1)/(e^{eps/2} - 1), (1 - e^{-rho})/(1 - e^{-eps/2}))) evaluations whatever n, while without the sup-norm bound the cost grows like e^{n theta_hint(eps/n)}; exact check: among all truncated cones -u min(kappa, (r - d(x, a))_+) with u kappa <= rho the largest change of ln Z per unit of uniform probability of the support is at most e^rho - 1")
def t_box_caps_first_order(rng, trials):
    stats = {}
    u, delta = 1.0, 0.05
    for n in (40, 200, 1000):
        logbin = np.array([math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) for k in range(n + 1)]) - n * math.log(2)
        for rho in (1.0, 3.0):
            kappa = int(rho / u)
            worst = 0.0
            for rad in range(1, n // 2):
                # truncated cone of radius rad and depth cap kappa: value -u*min(kappa, rad - d) on d < rad
                d = np.arange(0, rad)
                depth = u * np.minimum(kappa, rad - d)
                gain = float(np.exp(logbin[:rad] + np.log(np.expm1(depth))).sum())       # Z'/Z - 1
                support = float(np.exp(logbin[:rad]).sum())
                worst = max(worst, gain / support)
            if worst > math.expm1(rho) + 1e-9:
                return False, dict(reason="a truncated cone gains more than (e^rho - 1) per unit of support", n=n, rho=rho, worst=worst)
            stats[f"n{n}_rho{rho}"] = round(worst / math.expm1(u * kappa), 4)
    eps = 0.2
    cap = math.ceil(2 * math.log(1 / delta) * max(math.expm1(3.0) / math.expm1(eps / 2), -math.expm1(-3.0) / -math.expm1(-eps / 2)))
    # the hinted exponent of the cube class at a fixed accuracy: n * (ln 2 - h(Lambda1/u)) (theory report 11.25): exceeds the cap from n = 2000 on
    lam1 = math.log(2 / (1 + math.exp(-u)))
    theta = math.log(2) + (lam1 / u) * math.log(lam1 / u) + (1 - lam1 / u) * math.log(1 - lam1 / u)
    n_cross = next(n for n in range(10, 10 ** 6, 10) if n * theta > math.log(cap))
    stats["cap"], stats["theta_hint_fixed_accuracy"], stats["n_cross"] = cap, round(theta, 5), n_cross
    if not (0.02 < theta < 0.03 and n_cross < 2000):
        return False, dict(reason="comparison with the cube exponent", theta=theta, n_cross=n_cross)
    return True, stats


def bx_upper_bounds(samples, delta):
    """(empirical Bernstein upper bound of Maurer-Pontil form, naive 'mean + two standard errors') for the mean of a [0,1]-valued variable."""
    m = samples.shape[-1]
    mean = samples.mean(axis=-1)
    var = samples.var(axis=-1, ddof=1)
    eb = mean + np.sqrt(2 * var * math.log(2 / delta) / m) + 7 * math.log(2 / delta) / (3 * (m - 1))
    return eb, mean + 2 * np.sqrt(var / m)


@conjecture("XXIV.5 The bracket of the hint-free estimate (theory report 11.30, 'Without a hint'; a simulation, not a proof): for independent copies of a [0,1]-valued variable the empirical Bernstein bound mean + sqrt(2 V ln(2/delta)/m) + 7 ln(2/delta)/(3(m-1)) (V the sample variance) is an upper confidence bound for the mean at level 1 - delta — coverage on rare-dip, Bernoulli, uniform and beta laws; and for a law with zero sample variance it is 7 ln(2/delta)/(3(m-1)): the range of the variable enters only through the term of order 1/m")
def t_box_empirical_bernstein(rng, trials):
    delta, reps = 0.1, 4000
    stats = {}
    for m in (50, 400):
        laws = [("dip_half", lambda s: (rng.random(s) < 0.5 / m).astype(float), 0.5 / m),
                ("dip_one", lambda s: (rng.random(s) < 1.0 / m).astype(float), 1.0 / m),
                ("dip_three", lambda s: (rng.random(s) < 3.0 / m).astype(float), 3.0 / m),
                ("bern_0.1", lambda s: (rng.random(s) < 0.1).astype(float), 0.1),
                ("bern_0.5", lambda s: (rng.random(s) < 0.5).astype(float), 0.5),
                ("uniform", lambda s: rng.random(s), 0.5),
                ("beta_0.3_3", lambda s: rng.beta(0.3, 3.0, size=s), 0.3 / 3.3)]
        for name, draw, mean in laws:
            eb, _ = bx_upper_bounds(draw((reps, m)), delta)
            viol = float((eb < mean).mean())
            stats[f"{name}_m{m}"] = round(viol, 4)
            if viol > delta + 3 * math.sqrt(delta * (1 - delta) / reps):
                return False, dict(reason="empirical Bernstein bound violated more often than delta", law=name, m=m, frequency=viol)
        eb0, _ = bx_upper_bounds(np.zeros((1, m)), delta)
        if abs(float(eb0[0]) - 7 * math.log(2 / delta) / (3 * (m - 1))) > 1e-12:
            return False, dict(reason="value at zero sample variance")
    return True, stats


@conjecture("XXIV.6 A one-sided floor and an a-priori variance bracket the free energy without an exponential bill (theory report Theorem 11.110(f); Bennett's inequality in its two-point form — proposed for this place by the Scientific Discovery Division, SCI-MSG-0018): if the remainder r has mean r_bar, lies above r_bar - b and has variance at most sigma^2 under the known measure, then 0 <= K = ln E exp(-(r - r_bar)) <= W(b, sigma^2) = ln[(b^2 e^{-sigma^2/b} + sigma^2 e^b)/(b^2 + sigma^2)] <= (sigma^2/b^2)(e^b - 1 - b); the first bound is attained by the law with a state at the floor of probability sigma^2/(b^2 + sigma^2); it is monotone in b and in sigma^2, so that bounds on both suffice; and it is far below the two-point Jensen gap L(w) of the two-sided width when the variance is small.  With a ceiling a above the mean as well (Hoeffding 1963, as read by the Scientific Discovery Division, SCI-RES-0009): K <= -w p + ln(1 - p + p e^w) <= L(w) for w = a + b, p = a/w, with equality for two-point laws; and ln(1 + Var (e^-a - 1 + a)/a^2) <= K <= W <= ln(1 + (sigma^2/b^2)(e^b - 1 - b)), so that a floor and a ceiling bracket the error of first-order perturbation theory on both sides")
def t_bennett_bracket(rng, trials):
    W = lambda b, s2: math.log((b * b * math.exp(-s2 / b) + s2 * math.exp(b)) / (b * b + s2))
    stats = dict(laws=0, worst=-math.inf, attained=0, closest=math.inf, gain=0.0, hoeffding_closest=math.inf, lower_closest=math.inf, sharp_attained=math.inf)
    for _ in range(max(400, 4 * trials)):
        k = int(rng.integers(2, 9))
        pr = rng.dirichlet(np.ones(k) * float(rng.choice([0.3, 1.0, 3.0])))
        x = rng.normal(size=k) * float(rng.choice([0.2, 1.0, 3.0]))
        if rng.random() < 0.3:                                               # a rare deep dip
            pr = np.append(pr * (1 - 1e-3), 1e-3); x = np.append(x, -float(rng.uniform(2, 8)))
        x = x - float(pr @ x)
        b, s2 = -float(x.min()), float(pr @ (x * x))
        if b < 1e-6 or s2 < 1e-12:
            continue
        K = math.log(float(pr @ np.exp(-x)))
        w = W(b, s2)
        stats["worst"] = max(stats["worst"], K - w)
        stats["closest"] = min(stats["closest"], w - K)
        if K < -1e-12 or K > w + 1e-10:
            return False, dict(reason="the centred cumulant is outside [0, W(b, sigma^2)]", K=K, W=w, b=b, s2=s2)
        if w > s2 / (b * b) * (math.exp(b) - 1 - b) + 1e-10:
            return False, dict(reason="W exceeds Bennett's exponential bound", W=w, b=b, s2=s2)
        b2, s22 = b * float(rng.uniform(1, 2)), s2 * float(rng.uniform(1, 2))    # weaker bounds remain bounds
        if K > W(b2, s2) + 1e-10 or K > W(b, s22) + 1e-10 or W(b, s2) > W(b2, s22) + 1e-10:
            return False, dict(reason="W is not monotone in the floor or in the variance", b=b, s2=s2)
        # the two-point law attains W
        p0 = s2 / (b * b + s2)
        xs, ps = np.array([-b, s2 / b]), np.array([p0, 1 - p0])
        if abs(float(ps @ xs)) > 1e-10 or abs(float(ps @ (xs * xs)) - s2) > 1e-9 * (1 + s2) \
                or abs(math.log(float(ps @ np.exp(-xs))) - w) > 1e-9 * (1 + abs(w)):
            return False, dict(reason="the two-point law does not attain W", b=b, s2=s2)
        stats["attained"] += 1
        width = float(x.max() - x.min())
        Lw = math.log(math.expm1(width) / width) - 1 + width / math.expm1(width)
        if K > Lw + 1e-10:
            return False, dict(reason="the centred cumulant exceeds the two-point Jensen gap of the width", K=K, L=Lw)
        stats["gain"] = max(stats["gain"], Lw - w)
        # with the ceiling a = max x as well: Hoeffding's bound with the mean known, and second-order bounds on both sides
        a = float(x.max())
        ph = a / (a + b)
        hoeff = -(a + b) * ph + math.log(1 - ph + ph * math.exp(a + b))
        if K > hoeff + 1e-10 or hoeff > Lw + 1e-10:
            return False, dict(reason="the centred cumulant exceeds Hoeffding's bound with the mean known, or that bound exceeds L(w)",
                               K=K, hoeffding=hoeff, L=Lw)
        phi2 = lambda v: (math.exp(v) - 1 - v) / (v * v) if abs(v) > 1e-3 else 0.5 + v / 6 + v * v / 24 + v ** 3 / 120
        lower2 = math.log1p(s2 * phi2(-a))
        middle = math.log1p(s2 * phi2(b))
        if K < lower2 - 1e-10 or w > middle + 1e-10:
            return False, dict(reason="the second-order bounds ln(1 + Var phi(-a)) <= K <= W <= ln(1 + Var phi(b)) fail",
                               K=K, lower=lower2, W=w, middle=middle)
        stats["hoeffding_closest"] = min(stats["hoeffding_closest"], hoeff - K)
        if K > 1e-6:
            stats["lower_closest"] = min(stats["lower_closest"], (K - lower2) / K)
        stats["laws"] += 1
    # the certificate with a sample mean: the floor width may be r_bar - eta - lo (Scientific Discovery Division,
    # SCI-MSG-0023, machine-checked there and in BennettTwoPoint.lean: W(b, v) - b is nonincreasing in b); attained
    # when the sample mean is too high by eta and the law is the extremal two-point law
    for _ in range(200):
        b0, s2 = float(rng.uniform(1.2, 6.0)), float(rng.uniform(0.01, 2.0))
        p0 = s2 / (b0 * b0 + s2)
        mu, eta = float(rng.normal()), float(rng.uniform(0.01, 0.3))
        r = mu + np.array([-b0, s2 / b0])
        ps = np.array([p0, 1 - p0])
        lo = mu - b0
        lnE = math.log(float(ps @ np.exp(-r)))
        for e in (eta, -eta, float(rng.uniform(-eta, eta))):
            rbar = mu + e
            if not lo < rbar - eta:
                continue
            sharp = -rbar + eta + W(rbar - eta - lo, s2)
            old = -rbar + eta + W(rbar + eta - lo, s2)
            if lnE > sharp + 1e-9 or sharp > old + 1e-12:
                return False, dict(reason="the upper end with the floor width r_bar - eta - lo fails, or exceeds the one with r_bar + eta - lo",
                                   lnE=lnE, sharp=sharp, old=old)
            if e == eta:
                stats["sharp_attained"] = min(stats["sharp_attained"], sharp - lnE)
    # the regime of the measured instances: a floor of a few units and a small variance
    if not (W(3.7, 0.036 ** 2) < 3.5e-3 and W(0.08, 0.19 ** 2) < 0.0165):
        return False, dict(reason="values of W at the two quoted parameter pairs", a=W(3.7, 0.036 ** 2), b=W(0.08, 0.19 ** 2))
    if stats["laws"] < 100 or stats["gain"] <= 0 or stats["hoeffding_closest"] > 1e-9 or stats["lower_closest"] > 0.05 or stats["sharp_attained"] > 1e-9:
        return False, dict(reason="cases not exercised, or a bound never close to attained", **stats)
    return True, stats


@conjecture("XXIV.7 The floor is the end p = infinity of a family (theory report Proposition 11.112; the statements are the Scientific Discovery Division's, addendum A17 of its inference-limits notes and SCI-RES-0007, re-derived here).  With Y = exp(-r), mu = E Y under the known measure and the Renyi ball {||Y||_p <= B}: (a) two members that differ exactly on D satisfy pi(D) >= (|mu - mu'|/B)^(p/(p-1)), with equality in the limit of a flat alternative on an empty background; (b) hence every member whose ln mu differs from the hint's by more than eps differs from it on a set of mass at least q* = ((1 - e^-eps) mu/B)^(p/(p-1)), and the constant 1 - e^-eps cannot be replaced by e^eps - 1; (c) the alternative hint + (B - B0) q^(-1/p) on a set of mass q stays in the ball and raises mu by exactly (B - B0) q^(1-1/p), so that disjoint sets of mass above q_low = ((e^eps - 1) mu/(B - B0))^(p/(p-1)) give at least floor(1/(2 q_low)) alternatives, and the sample size of (b) is within the factor 2 ln(1/delta)/(1-2 delta) * (e^eps B/(B - B0))^(p/(p-1)) of the lower bound; (d) for p >= 2, ||Y||_2^2 <= mu^((p-2)/(p-1)) B^(p/(p-1)), with equality at two-level members; (e) Kullback-Leibler balls at the centre: every alternative with |ln mu'| > eps differs on a set of mass at least exp(-(kappa + ln 2)/(1 - e^-eps)), attained up to 1 per cent at eps = ln 2, and the two-level alternatives reach down to q_kappa with (1 - e^-eps) ln(eta/q_kappa) = kappa + eps up to a correction of order q_kappa; (f) on a product measure, one-site oscillations c_i give D_p <= sum_i [(p-1) c_i^2/8 + L(c_i)] <= p sum c_i^2/8 <= p^2 sum c_i^2/(8(p-1)) (the first, sharp form is the Scientific Discovery Division's, SCI-RES-0009: a variance bound for the tilted law of one site plus the largest divergence of a pair of laws with bounded log-ratio), attained to within a per cent by the additive instance on the uniform cube at small slope, where D_p = n[ln cosh(pu/2) - p ln cosh(u/2)]/(p-1); (g) a root-mean-square bound alone allows a change of ln mu by 86 at sigma = 0.1")
def t_renyi_family(rng, trials):
    orders = [1.5, 2.0, 3.0, 6.0, math.inf]
    expo = lambda p: 1.0 if math.isinf(p) else p / (p - 1)
    inv = lambda p: 0.0 if math.isinf(p) else 1.0 / p
    norm = lambda pr, Y, p: float(Y.max()) if math.isinf(p) else float(pr @ Y ** p) ** (1 / p)
    stats = dict(alternatives=0, closest=math.inf, two_level=0, closest_spot=math.inf, packings=0,
                 norm_closest=math.inf, kl=0, kl_closest=math.inf, cube=0, cube_largest=0.0, cube_sharp=0.0)
    for it in range(max(60, trials)):
        p = orders[it % len(orders)]
        e = expo(p)
        N = int(rng.integers(8, 60))
        pr = rng.dirichlet(np.ones(N))
        flat = it % 4 == 0                                    # an (almost) empty background: Hoelder is tight
        Y = np.full(N, 1e-9) if flat else np.exp(-rng.normal(0, float(rng.uniform(0.2, 2.0)), N))
        mu, B0 = float(pr @ Y), norm(pr, Y, p)
        B = (1.0 if flat else B0) * float(rng.uniform(1.2, 3.0))
        D = rng.random(N) < float(rng.uniform(0.05, 0.5))
        if not D.any() or D.all():
            D[:] = False; D[int(rng.integers(N))] = True
        q = float(pr[D].sum())
        # (a) alternatives on the boundary of the ball that differ from Y exactly on D
        alts = []
        for shape in (np.ones(N), rng.random(N) + 0.05):
            if math.isinf(p):
                t = B / float(shape[D].max())
            else:
                t = ((B ** p - float(pr[~D] @ Y[~D] ** p)) / float(pr[D] @ shape[D] ** p)) ** (1 / p)
            Y1 = np.where(D, t * shape, Y)
            if norm(pr, Y1, p) > B * (1 + 1e-9):
                return False, dict(reason="the alternative of the test left the ball", p=p)
            alts.append(Y1)
        alts.append(np.where(D, Y * 1e-12, Y))                 # lowered to (almost) nothing on D
        for Y1 in alts:
            dmu = abs(float(pr @ Y1) - mu)
            ratio = q / (dmu / B) ** e if dmu > 0 else math.inf
            stats["closest"] = min(stats["closest"], ratio)
            stats["alternatives"] += 1
            if ratio < 1 - 1e-9:
                return False, dict(reason="two members of a Renyi ball differ on a set smaller than the detection lemma allows",
                                   p=p, q=q, dmu=dmu, B=B, ratio=ratio)
        # (d) the second moment between the first and the p-th
        if p >= 2 and not flat:
            for Yt in (Y, np.where(D, Y, 1e-9 * Y)):
                m1, m2, mp = float(pr @ Yt), float(pr @ Yt ** 2), norm(pr, Yt, p)
                bound = m1 * mp if math.isinf(p) else m1 ** ((p - 2) / (p - 1)) * mp ** (p / (p - 1))
                stats["norm_closest"] = min(stats["norm_closest"], bound / m2)
                if m2 > bound * (1 + 1e-9):
                    return False, dict(reason="the second moment exceeds its interpolation bound", p=p, m2=m2, bound=bound)
        # (b) the spot check: a two-level hint whose upper level, lowered, changes ln mu by just more than eps
        eps = float(rng.uniform(0.05, 1.0))
        s, eta = 1 - math.exp(-eps), math.expm1(eps)
        qq = float(10 ** rng.uniform(-6, -1))
        prt = np.array([qq, 1 - qq])
        l = 1.0
        h = eta * 1.0001 * l * (1 - qq) / qq
        Yh = np.array([h, l]); Yalt = np.array([h * 1e-12, l])
        muh, Bh = float(prt @ Yh), norm(prt, Yh, p)
        if abs(math.log(float(prt @ Yalt)) - math.log(muh)) <= eps:
            return False, dict(reason="the alternative of the test does not change ln mu by more than eps")
        qstar = (s * muh / Bh) ** e
        stats["two_level"] += 1
        stats["closest_spot"] = min(stats["closest_spot"], qq / qstar)
        if qq < qstar * (1 - 1e-9):
            return False, dict(reason="an alternative that changes ln mu by more than eps differs from the hint on a set of mass below q*",
                               p=p, eps=eps, q=qq, qstar=qstar)
        # (c) the alternatives of the lower bound
        if not flat:
            a = (B - B0) * q ** (-inv(p))
            Y1 = Y + a * D
            if norm(pr, Y1, p) > B * (1 + 1e-9):
                return False, dict(reason="the alternative of the lower bound leaves the ball", p=p, q=q, norm=norm(pr, Y1, p), B=B)
            gain = float(pr @ Y1) - mu
            if abs(gain - (B - B0) * q ** (1 - inv(p))) > 1e-9 * (B - B0):
                return False, dict(reason="the alternative of the lower bound does not raise mu by (B - B0) q^(1-1/p)", p=p)
            qlow = (eta * mu / (B - B0)) ** e
            if q > qlow * (1 + 1e-9) and math.log(float(pr @ Y1)) - math.log(mu) <= eps:
                return False, dict(reason="a set of mass above q_low does not change ln mu by more than eps", p=p, q=q, qlow=qlow)
    # (c) continued: the packing at the centre of a ball on a fine-grained measure, and the size of the bracket
    for p in orders:
        e = expo(p)
        for eps, delta, ratioB in ((0.2, 0.05, 6.0), (1.0, 0.1, 3.0), (0.5, 0.05, 20.0)):
            N = 20000
            pr = rng.dirichlet(np.ones(N) * 5.0)
            mu = B0 = 1.0; B = ratioB
            s, eta = 1 - math.exp(-eps), math.expm1(eps)
            qlow = (eta * mu / (B - B0)) ** e
            if pr.max() > qlow:
                continue
            groups, acc = 0, 0.0
            for w in pr:
                acc += float(w)
                if acc > qlow:
                    if acc > 2 * qlow * (1 + 1e-12):
                        return False, dict(reason="a group of the greedy packing is heavier than 2 q_low")
                    aq = (B - B0) * acc ** (1 - inv(p))        # gain of the alternative on this group
                    if math.log(mu + aq) - math.log(mu) <= eps:
                        return False, dict(reason="a group of the packing does not change ln mu by more than eps", p=p)
                    groups += 1; acc = 0.0
            if groups < math.floor(1 / (2 * qlow)):
                return False, dict(reason="fewer disjoint alternatives than floor(1/(2 q_low))", p=p, groups=groups, qlow=qlow)
            upper = math.ceil(math.log(1 / delta) / (s * mu / B) ** e)
            lower = (1 - 2 * delta) * groups
            if groups >= 5 and upper > 2 * math.log(1 / delta) / (1 - 2 * delta) * (math.exp(eps) * B / (B - B0)) ** e * lower * 1.25 + 1:
                return False, dict(reason="the sample size of the spot check is not within the stated factor of the lower bound",
                                   p=p, upper=upper, lower=lower)
            stats["packings"] += 1
    # (e) Kullback-Leibler balls at the centre
    def kl_two_level(lq, eps):                                 # D_1 of the alternative 1 + a 1_D, a q = e^eps - 1, q = e^lq
        eta = math.expm1(eps)
        qm = math.exp(lq)
        return -eps + (qm + eta) * math.exp(-eps) * (math.log(eta) - lq + math.log1p(qm / eta))
    for it in range(max(60, trials)):
        eps = math.log(2) if it % 3 == 0 else float(rng.uniform(0.05, 1.0))
        s, eta = 1 - math.exp(-eps), math.expm1(eps)
        kappa = float(rng.uniform(3.0, 40.0))
        # the formula against a direct evaluation
        qm = float(10 ** rng.uniform(-8, -1))
        a = eta / qm
        prt, Yt = np.array([qm, 1 - qm]), np.array([1 + a, 1.0])
        dens = Yt / float(prt @ Yt)
        direct = float(prt @ (dens * np.log(dens)))
        if abs(direct - kl_two_level(math.log(qm), eps)) > 1e-9 * (1 + abs(direct)) or abs(math.log(float(prt @ Yt)) - eps) > 1e-12:
            return False, dict(reason="the divergence of the two-level alternative is not given by the formula", q=qm, eps=eps)
        lo_l, hi_l = -5000.0, math.log(eta)                    # D_1 decreases in q: the smallest admissible mass, in logarithms
        if kl_two_level(hi_l, eps) > kappa:
            continue
        for _ in range(200):
            mid = (lo_l + hi_l) / 2
            if kl_two_level(mid, eps) > kappa:
                lo_l = mid
            else:
                hi_l = mid
        lqk = hi_l
        floor_l = -(kappa + math.log(2)) / s
        if lqk < floor_l - 1e-9:
            return False, dict(reason="a two-level alternative of a Kullback-Leibler ball sits on a set smaller than the detection bound",
                               eps=eps, kappa=kappa, ln_q=lqk, ln_bound=floor_l)
        if it % 3 == 0 and kappa > 10:
            stats["kl_closest"] = min(stats["kl_closest"], math.exp(lqk - floor_l))
        corr = kappa + eps - s * (math.log(eta) - lqk)
        qk = math.exp(lqk)
        if corr < -1e-9 or corr > qk * math.exp(-eps) * (math.log(eta) - lqk + 1 + qk / eta) + 1e-9:
            return False, dict(reason="the threshold of the two-level alternatives is not exp(-(kappa + eps)/s) up to the stated correction",
                               eps=eps, kappa=kappa, ln_q=lqk, corr=corr)
        # random alternatives at the centre, upward and downward
        N = int(rng.integers(6, 40))
        pr = rng.dirichlet(np.ones(N))
        D = rng.random(N) < float(rng.uniform(0.05, 0.5))
        if not D.any() or D.all():
            D[:] = False; D[int(rng.integers(N))] = True
        for sign in (1.0, -1.0):
            Y1 = np.where(D, np.exp(sign * rng.uniform(0.0, 12.0, N)), 1.0)
            m1 = float(pr @ Y1)
            dens = Y1 / m1
            d1 = float(pr @ (dens * np.log(dens)))
            e1 = abs(math.log(m1)) * 0.999
            if e1 < 1e-6:
                continue
            s1 = 1 - math.exp(-e1)
            if float(pr[D].sum()) < math.exp(-(d1 + math.log(2)) / s1) * (1 - 1e-9):
                return False, dict(reason="an alternative of a Kullback-Leibler ball differs from the centre on a set smaller than the detection bound",
                                   d1=d1, eps=e1, q=float(pr[D].sum()))
        stats["kl"] += 1
    # (f) first-order constants on a product measure (enumeration)
    for it in range(max(12, trials // 5)):
        n = int(rng.integers(5, 10))
        X = np.array([[(v >> i) & 1 for i in range(n)] for v in range(2 ** n)], dtype=float)
        additive = it % 3 == 0
        if additive:
            u = [0.05, 0.5, 2.0][(it // 3) % 3]; pp = 0.5
            r = u * X.sum(axis=1)
        else:
            pp = float(rng.uniform(0.2, 0.8))
            J = np.triu(rng.normal(0, 0.4, (n, n)), 1)
            r = X @ rng.normal(0, 0.6, n) + np.einsum("vi,ij,vj->v", X, J, X) + rng.normal(0, 0.2, 2 ** n)
        pr = np.prod(np.where(X == 1, pp, 1 - pp), axis=1)
        idx = np.arange(2 ** n)
        cs = [float(np.abs(r - r[idx ^ (1 << i)]).max()) for i in range(n)]
        K = sum(c * c for c in cs)
        Lfun = lambda c: math.log(math.expm1(c) / c) - 1 + c / math.expm1(c) if c > 1e-9 else c * c / 8
        Y = np.exp(-(r - r.min()))
        mu = float(pr @ Y)
        for p in (1.5, 2.0, 4.0):
            dp = math.log(float(pr @ (Y / mu) ** p)) / (p - 1)
            bound = p * p * K / (8 * (p - 1))
            stats["cube_largest"] = max(stats["cube_largest"], dp / bound)
            if dp > bound + 1e-9:
                return False, dict(reason="a Renyi divergence exceeds the bound from one-site oscillations", p=p, dp=dp, bound=bound)
            sharp = sum((p - 1) * c * c / 8 + Lfun(c) for c in cs)
            if dp > sharp + 1e-9 or sharp > p * K / 8 + 1e-12 or p * K / 8 > bound + 1e-12:
                return False, dict(reason="the chain D_p <= sum[(p-1)c^2/8 + L(c)] <= pK/8 <= p^2 K/(8(p-1)) fails",
                                   p=p, dp=dp, sharp=sharp, K=K)
            stats["cube_sharp"] = max(stats["cube_sharp"], dp / sharp)
            if additive:
                exact = n * (math.log(math.cosh(p * u / 2)) - p * math.log(math.cosh(u / 2))) / (p - 1)
                if abs(dp - exact) > 1e-9 * (1 + exact):
                    return False, dict(reason="the divergence of the additive instance is not the closed form", p=p, dp=dp, exact=exact)
                if p == 2.0 and abs(dp - n * math.log1p(math.tanh(u / 2) ** 2)) > 1e-9 * (1 + dp):
                    return False, dict(reason="the chi-square form of the additive instance", dp=dp)
        stats["cube"] += 1
    # (g) a root-mean-square bound alone certifies nothing
    sigma, qd = 0.1, 1e-6
    d = sigma / math.sqrt(qd)
    change = math.log1p(qd * math.expm1(d))
    if not (abs(d - 100) < 1e-9 and 86.0 < change < 86.4):
        return False, dict(reason="the size of the dip that a root-mean-square budget allows", d=d, change=change)
    if not (stats["closest"] < 1.001 and stats["closest_spot"] < 1.05 and stats["norm_closest"] < 1.001
            and stats["kl_closest"] < 1.01 and stats["packings"] >= 8 and stats["cube"] >= 12
            and stats["cube_largest"] > 0.7 and stats["cube_sharp"] > 0.99 and stats["kl"] >= 30):
        return False, dict(reason="cases not exercised, or a bound never close to attained", **stats)
    return True, stats


@conjecture("XXIV.8 A ratio of two macrostate weights in a box class (theory report Corollary 11.114; BoxRatio.lean).  With W_M = sum over the macrostate M of pi e^{-r} and the dip and bump weights restricted to M: (a) a member that differs from r on D raises ln(W_A/W_B) by at most ln(1 + dip_A(D)/W_A) - ln(1 - bump_B(D)/W_B) and lowers it by at most ln(1 + dip_B(D)/W_B) - ln(1 - bump_A(D)/W_A), with equality for the floor on one macrostate and the ceiling on the other; (b) if the change exceeds eta, D has probability at least (1/2) min(p_A(eta), p_B(eta)) under the mixture of the two macrostates' samplers, p_M(eta) = (1/2) min((e^eta - 1) W_M/U_M, (1 - e^-eta) W_M/V_M) — the same level eta as for one partition sum, attained when one macrostate alone changes; (c) a set inside one macrostate with dip weight above (e^eps - 1) W_M changes the ratio by more than eps, the greedy packings give at least floor((W_M(lo)/W_M - 1)/(2(e^eps - 1))) such sets in each macrostate, and the sample size of the spot check is within the factor 8 ln(1/delta)(e^(eps/2) + 1)/(1 - 2 delta) of the lower bound; (d) the cost number max_M (W_M(lo)/W_M - 1) does not depend on the weights of the macrostates and can be far above Z(lo)/Z - 1 of the whole system")
def t_box_ratio(rng, trials):
    stats = dict(alternatives=0, extremal=0, closest=math.inf, packings=0, widest_factor=0.0)

    def setup(pr, lo, hi, r, M):
        w = pr * M
        W = float(w @ np.exp(-r))
        dip = w * (np.exp(-lo) - np.exp(-r))
        bump = w * (np.exp(-r) - np.exp(-hi))
        return W, dip, bump

    def pM(W, U, V, eta):
        return 0.5 * min(math.expm1(eta) * W / U, -math.expm1(-eta) * W / V)

    for it in range(max(60, trials)):
        N = int(rng.integers(12, 60))
        pr = rng.dirichlet(np.ones(N))
        lo = -rng.uniform(0.2, 4.0, N)
        hi = rng.uniform(0.2, 4.0, N)
        r = lo + (hi - lo) * rng.random(N)
        lab = rng.integers(0, 3, N)                              # 0: in A, 1: in B, 2: in neither
        lab[:2] = 0; lab[2:4] = 1
        A, B = (lab == 0).astype(float), (lab == 1).astype(float)
        tight = it % 4 == 0
        if tight:                                               # a deep floor in A, a shallow box in B
            lo = np.where(A == 1, lo - 6.0, -1e-3)
            hi = np.where(A == 1, hi, 1e-3)
            r = np.where(A == 1, r, 0.0)
        D = rng.random(N) < float(rng.uniform(0.05, 0.5))
        if tight:                                               # one macrostate alone, the hint at its ceiling there
            D = D & (A == 1)
            if not D.any():
                D[0] = True
            r = np.where(D, hi, r)
        elif not D.any():
            D[int(rng.integers(N))] = True
        WA, dipA, bumpA = setup(pr, lo, hi, r, A)
        WB, dipB, bumpB = setup(pr, lo, hi, r, B)
        UA, VA, UB, VB = float(dipA.sum()), float(bumpA.sum()), float(dipB.sum()), float(bumpB.sum())
        if min(UA, VA, UB, VB) <= 1e-12:
            continue
        q = 0.5 * (0.5 * dipA / UA + 0.5 * bumpA / VA) + 0.5 * (0.5 * dipB / UB + 0.5 * bumpB / VB)
        if abs(float(q.sum()) - 1) > 1e-9:
            return False, dict(reason="the mixed sampler is not a probability vector")
        rho = math.log(WA / WB)
        up = math.log1p(float(dipA[D].sum()) / WA) - math.log1p(-float(bumpB[D].sum()) / WB)
        down = math.log1p(float(dipB[D].sum()) / WB) - math.log1p(-float(bumpA[D].sum()) / WA)
        alts = [np.where(D, np.where(A == 1, lo, np.where(B == 1, hi, r)), r),      # extremal upwards
                np.where(D, np.where(A == 1, hi, np.where(B == 1, lo, r)), r),      # extremal downwards
                np.where(D, lo, r), np.where(D, hi, r),
                np.where(D, lo + (hi - lo) * rng.random(N), r)]
        for k, r1 in enumerate(alts):
            change = math.log(float((pr * A) @ np.exp(-r1)) / float((pr * B) @ np.exp(-r1))) - rho
            if change > up + 1e-9 or change < -down - 1e-9:
                return False, dict(reason="a member of the box changes the log-ratio by more than the dip and bump weights allow",
                                   change=change, up=up, down=down)
            if (k == 0 and abs(change - up) > 1e-9) or (k == 1 and abs(change + down) > 1e-9):
                return False, dict(reason="the extremal alternative does not attain the bound on the change of the log-ratio",
                                   k=k, change=change, up=up, down=down)
            stats["extremal"] += k < 2
            if abs(change) < 1e-9:
                continue
            eta = abs(change) * 0.999
            bound = 0.5 * min(pM(WA, UA, VA, eta), pM(WB, UB, VB, eta))
            differs = r1 != r
            qD = float(q[differs].sum())
            stats["alternatives"] += 1
            stats["closest"] = min(stats["closest"], qD / bound)
            if qD < bound * (1 - 1e-9):
                return False, dict(reason="a member whose log-ratio differs by more than eta differs from the hint on a set of smaller probability than the detection bound",
                                   eta=eta, qD=qD, bound=bound)
    # (c) packings in both macrostates on a fine-grained measure, and the size of the bracket
    for rhoA, rhoB, eps, delta in ((3.0, 1.0, 0.2, 0.05), (2.0, 2.0, 0.5, 0.1), (1.0, 5.0, 0.1, 0.05), (4.0, 0.5, 1.0, 0.05)):
        N = 40000
        pr = rng.dirichlet(np.ones(N) * 5.0)
        A = (np.arange(N) % 2 == 0).astype(float); B = 1 - A
        lo = np.where(A == 1, -rhoA, -rhoB); hi = np.full(N, 1.0); r = np.zeros(N)
        counts, numbers = [], []
        for M, sign in ((A, 1.0), (B, -1.0)):
            W, dip, bump = setup(pr, lo, hi, r, M)
            other = float((pr * (1 - M)) @ np.exp(-r))           # the other macrostate here: the complement
            thr = math.expm1(eps) * W
            number = float((pr * M) @ np.exp(-lo)) / W - 1
            numbers.append(number)
            if float(dip.max()) > thr:
                counts.append(None); continue
            groups, acc = 0, 0.0
            for d in dip[M == 1]:
                acc += float(d)
                if acc > thr:
                    change = sign * (math.log((W + acc) / other) - math.log(W / other))   # the other weight is untouched
                    if abs(change) <= eps:
                        return False, dict(reason="a group of the packing does not change the log-ratio by more than eps", eps=eps)
                    groups += 1; acc = 0.0
            if groups < math.floor(number / (2 * math.expm1(eps))):
                return False, dict(reason="fewer disjoint dips in a macrostate than floor((W_M(lo)/W_M - 1)/(2(e^eps - 1)))",
                                   groups=groups, number=number)
            counts.append(groups)
        if None in counts:
            continue
        WA, dipA, bumpA = setup(pr, lo, hi, r, A)
        WB, dipB, bumpB = setup(pr, lo, hi, r, B)
        p = min(1.0, 0.5 * min(pM(WA, float(dipA.sum()), float(bumpA.sum()), eps / 2),
                               pM(WB, float(dipB.sum()), float(bumpB.sum()), eps / 2)))
        upper = math.ceil(math.log(1 / delta) / p)
        closed = math.ceil(4 * math.log(1 / delta) * max(max(numbers) / math.expm1(eps / 2), 1 / -math.expm1(-eps / 2)))
        if upper > closed:
            return False, dict(reason="the sample size of the spot check exceeds its closed form", upper=upper, closed=closed)
        lower = (1 - 2 * delta) * sum(counts)
        factor = 8 * math.log(1 / delta) * (math.exp(eps / 2) + 1) / (1 - 2 * delta)
        if max(counts) >= 5:
            stats["widest_factor"] = max(stats["widest_factor"], upper / lower / factor)
            if upper > factor * lower * 1.3 + 1:
                return False, dict(reason="the sample size of the spot check is not within the stated factor of the lower bound",
                                   upper=upper, lower=lower, factor=factor)
        stats["packings"] += 1
    # (d) a rare macrostate with a deep floor: cheap for the whole system, expensive for the ratio
    N = 2000
    pr = np.full(N, 1.0 / N)
    A = (np.arange(N) < 20).astype(float)
    numbers = []
    for scale in (1.0, 1e-6):
        w = pr * np.where(A == 1, scale, 1.0); w = w / w.sum()
        lo = np.where(A == 1, -8.0, -0.1); r = np.zeros(N)
        numbers.append((float((w * A) @ np.exp(-lo)) / float((w * A) @ np.exp(-r)) - 1,
                        float(w @ np.exp(-lo)) / float(w @ np.exp(-r)) - 1))
    if abs(numbers[0][0] - numbers[1][0]) > 1e-9 * numbers[0][0] or abs(numbers[0][0] - math.expm1(8.0)) > 1e-6 * math.expm1(8.0):
        return False, dict(reason="the cost number of a macrostate depends on the weight of the macrostate", numbers=numbers)
    if not (numbers[1][1] < 0.12 and numbers[1][0] > 2000):
        return False, dict(reason="the rare macrostate with a deep floor is not cheap for the whole system and expensive for the ratio",
                           numbers=numbers)
    if not (stats["closest"] < 1.01 and stats["alternatives"] >= 100 and stats["packings"] >= 3):
        return False, dict(reason="cases not exercised, or the detection bound never close to attained", **stats)
    return True, stats


@conjecture("XXIV.9 Box classes, floor and ceiling, with and without a hint (theory report Theorem 11.110(d), (e) as corrected and the remark 'what the hint buys'; BoxClass.lean: logZ_bumpAlt_gt, box_expected_queries_ge_mixed, detect_ge_of_proportional; the corrections are due to the Scientific Discovery Division's prior-art review, SCI-RES-0009).  (a) A set whose bump weight exceeds (1 - e^-eps) Z changes ln Z by more than eps when raised to the ceiling; (b) with k the larger of the greedy packing numbers of dips and of bumps, (1 - 2 delta) k <= cost <= 4 ln(1/delta)(e^(eps/2) + 1)(k + 1) + 1 at every instance of a fine-grained box — near the floor the dips give k = 0 and the bumps carry the bound, which the statement with dips alone missed; (c) where bump and dip weights are proportional (the centre of a constant box) the detection probability is min((e^eta - 1) Z/U, (1 - e^-eta) Z/V), twice the general bound, so that the spot check needs 544 samples at rho = 3, eps = 0.2, delta = 0.05 where the general count is 1088; (d) without a hint: draw from the known measure, let v be the first value of the remainder and stop if the first N(v) = ceil(ln(1/delta)/q(v)) + 1 values all equal v, q(v) = min((e^eta - 1)/(e^(rho + v) - 1), 1 - e^-eta); the output -v is off by more than eta with probability at most delta on every member of the box, and N(0) = 545 at the same parameters: at a flat instance the hint is worth nothing")
def t_box_floor_ceiling(rng, trials):
    stats = dict(bump_sets=0, near_floor=0, widest_factor=0.0, centre_closest=math.inf, members=0, worst_failure=0.0)
    # (a), (b): fine-grained boxes at instances between the floor and the ceiling
    for case in range(12):
        N = 30000
        pr = rng.dirichlet(np.ones(N) * 5.0)
        rho_m, rho_p = float(rng.uniform(0.5, 4.0)), float(rng.uniform(0.5, 4.0))
        lo, hi = np.full(N, -rho_m), np.full(N, rho_p)
        mode = case % 3
        if mode == 0:                                              # near the floor: no heavy dips
            r = lo + 1e-4 * rng.random(N)
        elif mode == 1:                                            # anywhere in the box
            r = lo + (hi - lo) * rng.random(N)
        else:                                                      # near the ceiling
            r = hi - 1e-4 * rng.random(N)
        eps, delta = float(rng.choice([0.1, 0.3, 1.0])), float(rng.choice([0.05, 0.1]))
        Z = float(pr @ np.exp(-r))
        dip = pr * (np.exp(-lo) - np.exp(-r)); bump = pr * (np.exp(-r) - np.exp(-hi))
        U, V = float(dip.sum()), float(bump.sum())
        thr_d, thr_b = math.expm1(eps) * Z, -math.expm1(-eps) * Z
        if float(dip.max()) > thr_d or float(bump.max()) > thr_b:
            continue
        kd = kb = 0
        acc = 0.0
        for d in dip:
            acc += float(d)
            if acc > thr_d:
                if math.log((Z + acc) / Z) <= eps:
                    return False, dict(reason="a dip set above the threshold does not change ln Z by more than eps")
                kd += 1; acc = 0.0
        acc = 0.0
        for b in bump:
            acc += float(b)
            if acc > thr_b:
                if math.log(Z / (Z - acc)) <= eps:
                    return False, dict(reason="a bump set above the threshold does not change ln Z by more than eps",
                                       acc=acc, Z=Z, eps=eps)
                kb += 1; acc = 0.0
                stats["bump_sets"] += 1
        if kd < math.floor(U / (2 * thr_d)) or kb < math.floor(V / (2 * thr_b)):
            return False, dict(reason="fewer disjoint sets than the greedy bound", kd=kd, kb=kb)
        k = max(kd, kb)
        p = min(1.0, 0.5 * min(math.expm1(eps / 2) * Z / U, -math.expm1(-eps / 2) * Z / V))
        upper = math.ceil(math.log(1 / delta) / p)
        factor = 4 * math.log(1 / delta) * (math.exp(eps / 2) + 1)
        if upper > factor * (k + 1) + 1:
            return False, dict(reason="the sample size of the spot check exceeds 4 ln(1/delta)(e^(eps/2) + 1)(k + 1) + 1",
                               upper=upper, k=k, kd=kd, kb=kb)
        stats["widest_factor"] = max(stats["widest_factor"], upper / (factor * (k + 1) + 1))
        if mode == 0:
            # with dips alone the lower bound would be zero while the spot check still needs many samples
            if not (kd == 0 and kb >= 1 and upper > 5):
                return False, dict(reason="near the floor the dips should give no lower bound and the bumps one", kd=kd, kb=kb, upper=upper)
            stats["near_floor"] += 1
    # (c) the centre of a constant box: detection without the factor one half
    for _ in range(max(40, trials // 2)):
        N = int(rng.integers(10, 80))
        pr = rng.dirichlet(np.ones(N))
        rho_m, rho_p = float(rng.uniform(0.3, 4.0)), float(rng.uniform(0.3, 4.0))
        U, V = math.expm1(rho_m), -math.expm1(-rho_p)             # Z = 1 at the centre
        D = rng.random(N) < float(rng.uniform(0.02, 0.6))
        if not D.any():
            D[int(rng.integers(N))] = True
        q = float(pr[D].sum())
        for r1 in (np.where(D, -rho_m, 0.0), np.where(D, rho_p, 0.0), np.where(D, rng.uniform(-rho_m, rho_p, N), 0.0)):
            change = abs(math.log(float(pr @ np.exp(-r1))))
            if change < 1e-9:
                continue
            eta = change * 0.999
            bound = min(math.expm1(eta) / U, -math.expm1(-eta) / V)
            stats["centre_closest"] = min(stats["centre_closest"], q / bound)
            if q < bound * (1 - 1e-9):
                return False, dict(reason="at the centre of a constant box a member that changes ln Z by more than eta differs on a set of mass below the bound without the factor one half",
                                   q=q, bound=bound, eta=eta)
    eta, delta = 0.1, 0.05
    n_centre = math.ceil(math.log(1 / delta) / min(math.expm1(eta) / math.expm1(3.0), -math.expm1(-eta) / -math.expm1(-3.0)))
    n_general = math.ceil(math.log(1 / delta) / (0.5 * min(math.expm1(eta) / math.expm1(3.0), -math.expm1(-eta) / -math.expm1(-3.0))))
    if (n_centre, n_general) != (544, 1088):
        return False, dict(reason="the sample sizes at rho = 3, eps = 0.2, delta = 0.05", centre=n_centre, general=n_general)

    # (d) the rule without a hint: exact failure probability on members with two and three levels
    def N_rule(v, rho_m, eta, delta):
        qv = min(math.expm1(eta) / math.expm1(rho_m + v), -math.expm1(-eta)) if rho_m + v > 0 else -math.expm1(-eta)
        return math.ceil(math.log(1 / delta) / qv) + 1
    if N_rule(0.0, 3.0, 0.1, 0.05) != 545:
        return False, dict(reason="the length of the unhinted rule at the centre", N=N_rule(0.0, 3.0, 0.1, 0.05))
    for it in range(max(200, 3 * trials)):
        rho_m, rho_p = float(rng.uniform(0.5, 4.0)), float(rng.uniform(0.5, 4.0))
        eta, delta = float(rng.choice([0.05, 0.1, 0.5])), float(rng.choice([0.05, 0.1]))
        L = int(rng.integers(2, 4))
        if it % 2 == 0:
            # adversarial: a main level whose mass is just small enough for a deep dip to change ln Z by more than eta
            v = float(rng.uniform(-rho_m + 0.3, rho_p))
            qv = min(math.expm1(eta) / math.expm1(rho_m + v), -math.expm1(-eta))
            s_main = 1 - qv * float(rng.uniform(1.0005, 1.3))
            masses = np.array([s_main] + list((1 - s_main) * rng.dirichlet(np.ones(L - 1))))
            values = np.array([v] + [-rho_m] * (L - 1)) if it % 4 == 0 else np.array([v] + [rho_p] * (L - 1))
        else:
            masses = rng.dirichlet(np.ones(L) * float(rng.choice([0.3, 1.0])))
            values = rng.uniform(-rho_m, rho_p, L)
        lnmu = math.log(float(masses @ np.exp(-values)))
        failure = 0.0
        for s_l, v_l in zip(masses, values):
            if abs(lnmu + v_l) > eta:                              # the output -v_l would be wrong
                failure += float(s_l) ** N_rule(float(v_l), rho_m, eta, delta)
        stats["members"] += 1
        stats["worst_failure"] = max(stats["worst_failure"], failure / delta)
        if failure > delta * (1 + 1e-9):
            return False, dict(reason="the rule without a hint returns a wrong value with probability above delta",
                               failure=failure, delta=delta, masses=masses.tolist(), values=values.tolist())
    if not (stats["near_floor"] >= 2 and stats["bump_sets"] > 0 and stats["centre_closest"] < 1.01
            and stats["worst_failure"] > 0.5 and stats["members"] >= 200):
        return False, dict(reason="cases not exercised, or a bound never close to attained", **stats)
    return True, stats


@conjecture("XXIV.10 A sandwich of two sampleable models: sample where the bracket is wide (theory report Proposition 11.113; an answer to the Scientific Discovery Division's question P3-T3, SCI-MSG-0020).  If m_- <= E <= m_+ pointwise and both models have known partition functions, then with q proportional to e^{-m_-} - e^{-m_+} and W = (e^{-E} - e^{-m_+})/(e^{-m_-} - e^{-m_+}) in [0, 1]: (a) Z(E) = Z(m_+) + (Z(m_-) - Z(m_+)) E_q W exactly; (b) q is the law of an accepted draw when x from the Gibbs measure of m_- is accepted with probability 1 - e^{-(m_+(x) - m_-(x))}, and the acceptance rate is 1 - Z(m_+)/Z(m_-); (c) hence N samples of q bracket Z(E) within (Z(m_-) - Z(m_+)) sqrt(ln(2/delta)/(2N)) with probability 1 - delta (Hoeffding for a variable in [0, 1]; coverage simulated), the bracket never leaves the deterministic one, and its half-width is that of plain sampling from the lower model times E d/max d <= 1, d = 1 - e^{-(m_+ - m_-)}; (d) for a deterministic width of 0.0605 nats, 50 000 samples at delta = 0.05 give a width of at most 7.6e-4 nats, and 1 200 samples one of at most 5e-3")
def t_envelope_sampler(rng, trials):
    stats = dict(sandwiches=0, runs=0, misses=0, gain=math.inf, best_gain=0.0)
    for it in range(max(40, trials // 2)):
        N = int(rng.integers(6, 60))
        mlo = rng.normal(0, 1.5, N)
        gap = rng.exponential(float(rng.choice([0.05, 0.5, 2.0])), N) * (rng.random(N) < 0.8)   # some states with no gap
        if it % 5 == 0:
            gap = np.full(N, float(rng.uniform(0.1, 1.0)))         # a constant gap: no gain over plain sampling
        mhi = mlo + gap
        E = mlo + gap * rng.random(N)
        Zlo, Zhi, ZE = float(np.exp(-mlo).sum()), float(np.exp(-mhi).sum()), float(np.exp(-E).sum())
        dZ = Zlo - Zhi
        if dZ <= 1e-12 * Zlo:
            continue
        wq = np.exp(-mlo) - np.exp(-mhi)
        q = wq / dZ
        with np.errstate(divide="ignore", invalid="ignore"):
            W = np.where(wq > 0, (np.exp(-E) - np.exp(-mhi)) / np.where(wq > 0, wq, 1.0), 0.0)
        if W.min() < -1e-12 or W.max() > 1 + 1e-12:
            return False, dict(reason="the sampled variable leaves [0, 1]", lo=float(W.min()), hi=float(W.max()))
        theta = float(q @ W)
        if abs(Zhi + dZ * theta - ZE) > 1e-10 * ZE:
            return False, dict(reason="the partition sum is not Z(m+) + (Z(m-) - Z(m+)) E_q W", lhs=Zhi + dZ * theta, rhs=ZE)
        # (b) rejection from the Gibbs measure of the lower model
        pi_lo = np.exp(-mlo) / Zlo
        acc = -np.expm1(-(mhi - mlo))
        rate = float(pi_lo @ acc)
        if abs(rate - (1 - Zhi / Zlo)) > 1e-10 or np.abs(pi_lo * acc / rate - q).max() > 1e-10:
            return False, dict(reason="the accepted draws of the rejection sampler do not have the law q", rate=rate)
        # (c) coverage of the Hoeffding bracket, and the comparison with plain sampling
        delta, n = 0.1, 60
        t = math.sqrt(math.log(2 / delta) / (2 * n))
        draws = rng.choice(N, size=(40, n), p=q)
        est = W[draws].mean(axis=1)
        lo_b = Zhi + dZ * np.clip(est - t, 0.0, 1.0)
        hi_b = Zhi + dZ * np.clip(est + t, 0.0, 1.0)
        if (lo_b < Zhi * (1 - 1e-12)).any() or (hi_b > Zlo * (1 + 1e-12)).any():
            return False, dict(reason="the sampled bracket leaves the deterministic bracket")
        stats["runs"] += 40
        stats["misses"] += int(((ZE < lo_b * (1 - 1e-12)) | (ZE > hi_b * (1 + 1e-12))).sum())
        ratio = float(pi_lo @ acc) / float(acc.max())               # E d / max d
        plain = Zlo * float(acc.max()) * t                           # plain sampling of e^{-(E - m-)} in [e^{-u_max}, 1]
        if dZ * t > plain * (1 + 1e-12) or abs(dZ * t / plain - ratio) > 1e-9:
            return False, dict(reason="the half-width is not that of plain sampling times E d/max d", ratio=ratio)
        if it % 5 == 0 and abs(ratio - 1) > 1e-9:
            return False, dict(reason="with a constant gap the two samplers should coincide", ratio=ratio)
        stats["gain"] = min(stats["gain"], ratio)
        stats["best_gain"] = max(stats["best_gain"], ratio)
        stats["sandwiches"] += 1
    if stats["misses"] > 0.1 * stats["runs"]:
        return False, dict(reason="the bracket misses more often than delta", **stats)
    # (d) the two numbers
    width = lambda Delta, n, delta: 2 * math.sqrt(math.log(2 / delta) / (2 * n)) * math.expm1(Delta)
    if not (width(0.0605, 50000, 0.05) < 7.6e-4 and width(0.0605, 1200, 0.05) < 5e-3 and width(0.0605, 1100, 0.05) > 5e-3):
        return False, dict(reason="the quoted widths", a=width(0.0605, 50000, 0.05), b=width(0.0605, 1200, 0.05))
    if not (stats["sandwiches"] >= 30 and stats["gain"] < 0.5 and stats["best_gain"] > 1 - 1e-9 and stats["runs"] >= 1000):
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


def bx_binom_logpmf(N, p):
    """log pmf of Bin(N, p) on 0..N (no scipy)"""
    k = np.arange(N + 1)
    lc = np.concatenate([[0.0], np.cumsum(np.log((N - k[:-1]) / (k[:-1] + 1.0)))])
    with np.errstate(divide="ignore"):
        return lc + k * math.log(p) + (N - k) * math.log1p(-p)


def bx_kl(a, b):
    """Kullback-Leibler divergence of Bernoulli(a) from Bernoulli(b), infinite outside [0, 1]"""
    if a < 0 or a > 1:
        return math.inf
    out = 0.0
    if a > 0:
        out += a * math.log(a / b)
    if a < 1:
        out += (1 - a) * math.log((1 - a) / (1 - b))
    return out


def bx_nkl(Delta, eps, delta, ws):
    """the least N with ln(2/delta) <= N min(KL(w + t+ || w), KL(w - t- || w)) for every mean w of the grid, where
    t+ = (e^eps - 1)(c + w), t- = (1 - e^-eps)(c + w), c = 1/(e^Delta - 1): Hoeffding's Theorem 1 in its
    Kullback-Leibler form then gives the plug-in estimate of ln Z within eps on every member of the sandwich"""
    c = 1.0 / math.expm1(Delta)
    worst = 0.0
    for w in ws:
        tp, tm = math.expm1(eps) * (c + w), -math.expm1(-eps) * (c + w)
        worst = max(worst, math.log(2 / delta) / min(bx_kl(w + tp, w), bx_kl(w - tm, w)))
    return math.ceil(worst)


def bx_tv_binom(N, w1, w2):
    """total variation distance between Bin(N, w1) and Bin(N, w2)"""
    return 0.5 * float(np.abs(np.exp(bx_binom_logpmf(N, w1)) - np.exp(bx_binom_logpmf(N, w2))).sum())


def bx_plugin_failure(Delta, eps, N, w):
    """exact probability that the plug-in estimate ln(1 + a K/N) of a two-level member (W Bernoulli(w)) is off by
    more than eps"""
    c = 1.0 / math.expm1(Delta)
    k = np.arange(N + 1)
    pm = np.exp(bx_binom_logpmf(N, w))
    dev = k / N - w
    return float(pm[(dev > math.expm1(eps) * (c + w) + 1e-15) | (dev < math.expm1(-eps) * (c + w) - 1e-15)].sum())


@conjecture("XXIV.11 The sandwich sampler after the Scientific Discovery Division's review (theory report Proposition 11.113(c), (c'), (d) as corrected; SCI-REV-0013, findings M2 and m7; SCI-MSG-0025, section 4).  (d) Without a hint ln Z of a sandwich of width Delta is estimated within eps on every member from N_KL = max_w ln(2/delta)/min(KL(w + t+ || w), KL(w - t- || w)) evaluations, which is 2 ln(2/delta) sinh^2(Delta/2)/eps^2 up to a few per cent - smaller than the count (e^Delta - 1)^2 ln(2/delta)/(2 eps^2) of the first version by the factor e^-Delta; the exact failure probability of the plug-in estimate on two-level members is at most delta with N_KL evaluations and above delta with a quarter of them; the order is necessary - two-level members with independent inclusion probabilities w and w' = w + (e^(2 eps) - 1)(c + w) must be told apart, which needs total variation 1 - 2 delta between the laws of the observed bits, so no algorithm with fewer than 2(1 - 2 delta)^2/KL(w || w') evaluations exists (Pinsker), about (1 - 2 delta)^2 sinh^2(Delta/2)/eps^2 at the worst w, and the exact number N_TV at which Bin(N, w) and Bin(N, w') are that far apart lies between this bound and N_KL, within a factor 3.5 of each; (c) the sampled bracket leaves the deterministic one unless it is intersected with it; (c') the empirical Bernstein bound mean + sqrt(2 V ln(2/delta)/n) + 7 ln(2/delta)/(3(n - 1)) (Maurer and Pontil 2009, Theorem 4) covers a Bernoulli mean with exact probability at least 1 - delta, and not without its last term; with the standard deviation 0.022 measured by the division, 50 000 evaluations give a half-width more than ten times below Hoeffding's; in units of ln Z the width is ln(1 + a(W + t)) - ln(1 + a(W - t)) < 2 a t (0.026 against 0.057 at Delta = 1.74, W = 0.25, t = 0.006); an error of at most e in every evaluated energy shifts the estimated ln Z by at most e, although a single value of W moves by up to (e^e - 1)/(1 - e^-U(x)), whose mean under the sampler is (e^e - 1) Z(m-)/(Z(m-) - Z(m+))")
def t_sandwich_refinements(rng, trials):
    stats = dict(cases=0, worst_fail=0.0, quarter_fail=math.inf, ratio_lo=math.inf, ratio_hi=0.0, eb_worst=0.0, eb_bad=0.0,
                 leaves=0, shift=0.0, amplified=0.0, tv_over_bound=0.0, nkl_over_tv=0.0)
    delta = 0.05
    Lg = math.log(2 / delta)
    ws = [i / 400 for i in range(1, 400)]
    for Delta, eps in ((0.0605, 0.01), (0.5, 0.03), (1.0, 0.05), (2.0, 0.08), (3.0, 0.1)):
        N = bx_nkl(Delta, eps, delta, ws)
        closed = 2 * Lg * math.sinh(Delta / 2) ** 2 / eps ** 2
        first = Lg * math.expm1(Delta) ** 2 / (2 * eps ** 2)
        if not 0.95 <= N / closed <= 1.12:
            return False, dict(reason="the sufficient count is not 2 ln(2/delta) sinh^2(Delta/2)/eps^2 up to a few per cent",
                               Delta=Delta, eps=eps, N=N, closed=closed)
        if not 0.9 * math.exp(-Delta) <= N / first <= 1.2 * math.exp(-Delta):
            return False, dict(reason="the ratio to the count of the first version is not e^-Delta", Delta=Delta, N=N, first=first)
        stats["ratio_lo"] = min(stats["ratio_lo"], N / first * math.exp(Delta))
        stats["ratio_hi"] = max(stats["ratio_hi"], N / first * math.exp(Delta))
        grid = [i / 60 for i in range(1, 60)]
        worst = max(bx_plugin_failure(Delta, eps, N, w) for w in grid)
        if worst > delta:
            return False, dict(reason="with N_KL evaluations the plug-in estimate fails with probability above delta on a two-level member",
                               Delta=Delta, eps=eps, N=N, worst=worst)
        stats["worst_fail"] = max(stats["worst_fail"], worst)
        stats["quarter_fail"] = min(stats["quarter_fail"], max(bx_plugin_failure(Delta, eps, max(N // 4, 1), w) for w in grid))
        # the two-point lower bound for every algorithm, and the exact number of bits needed to tell the two members apart
        cc = 1.0 / math.expm1(Delta)
        w1 = cc / (1 + 2 * cc)
        w2 = w1 + math.expm1(2 * eps) * (cc + w1)
        lb = 2 * (1 - 2 * delta) ** 2 / bx_kl(w1, w2)
        if bx_tv_binom(N, w1, w2) < 1 - 2 * delta:
            return False, dict(reason="with N_KL evaluations the two members at distance 2 eps are not distinguishable, although the plug-in estimate separates them",
                               Delta=Delta, eps=eps, N=N)
        lo_n, hi_n = 1, N
        while lo_n < hi_n:
            mid_n = (lo_n + hi_n) // 2
            if bx_tv_binom(mid_n, w1, w2) >= 1 - 2 * delta:
                hi_n = mid_n
            else:
                lo_n = mid_n + 1
        if lb > lo_n or not 0.7 <= lb / ((1 - 2 * delta) ** 2 * math.sinh(Delta / 2) ** 2 / eps ** 2) <= 1.1:
            return False, dict(reason="the two-point lower bound exceeds the exact number of evaluations at which the two members can be told apart, or is not (1 - 2 delta)^2 sinh^2(Delta/2)/eps^2",
                               Delta=Delta, eps=eps, bound=lb, exact=lo_n)
        stats["tv_over_bound"] = max(stats["tv_over_bound"], lo_n / lb)
        stats["nkl_over_tv"] = max(stats["nkl_over_tv"], N / lo_n)
        stats["cases"] += 1
    if stats["quarter_fail"] <= delta:
        return False, dict(reason="a quarter of N_KL evaluations already suffices for the plug-in estimate at some width", **stats)
    # (c) the bracket around the estimate leaves the deterministic one unless it is clipped: E = m+ everywhere
    t = math.sqrt(math.log(2 / 0.1) / (2 * 60))
    Zhi, dZ, est = 1.0, 0.7, 0.0
    if Zhi + dZ * (est - t) < Zhi and Zhi + dZ * max(est - t, 0.0) >= Zhi:
        stats["leaves"] += 1
    # (c') Maurer-Pontil, Theorem 4, exactly for Bernoulli(p): the bound depends on the number of ones only
    for n in (20, 100, 1000):
        k = np.arange(n + 1)
        V = k * (n - k) / (n * (n - 1.0))
        bound = k / n + np.sqrt(2 * V * Lg / n) + 7 * Lg / (3 * (n - 1))
        bare = k / n + np.sqrt(2 * V * Lg / n)
        for p in [0.5 / n, 1.0 / n, 2.0 / n, 5.0 / n] + [i / 25 for i in range(1, 25)]:
            pm = np.exp(bx_binom_logpmf(n, p))
            viol = float(pm[bound < p - 1e-15].sum())
            if viol > delta:
                return False, dict(reason="the empirical Bernstein bound of Maurer and Pontil misses a Bernoulli mean with probability above delta",
                                   n=n, p=p, viol=viol)
            stats["eb_worst"] = max(stats["eb_worst"], viol)
            stats["eb_bad"] = max(stats["eb_bad"], float(pm[bare < p - 1e-15].sum()))
    L4 = math.log(4 / delta)
    hw_eb = math.sqrt(2 * 0.022 ** 2 * L4 / 50000) + 7 * L4 / (3 * 49999)
    hw_h = math.sqrt(Lg / (2 * 50000))
    if not (4.9e-4 < hw_eb < 5.0e-4 and hw_h / hw_eb > 10):
        return False, dict(reason="the two half-widths at the measured standard deviation", eb=hw_eb, hoeffding=hw_h)
    # the width in units of ln Z
    a, W0, t0 = math.expm1(1.74), 0.25, 0.006
    wid = math.log1p(a * (W0 + t0)) - math.log1p(a * (W0 - t0))
    if not (abs(wid - 0.026) < 6e-4 and abs(2 * a * t0 - 0.057) < 7e-4):
        return False, dict(reason="the width in units of ln Z at the division's numbers", wid=wid, linear=2 * a * t0)
    for _ in range(200):
        a, W0 = float(rng.uniform(0.01, 30)), float(rng.uniform(0.02, 0.98))
        t0 = float(rng.uniform(0.0, min(W0, 1 - W0)))
        wid = math.log1p(a * (W0 + t0)) - math.log1p(a * (W0 - t0))
        if wid > 2 * a * t0 / (1 + a * (W0 - t0)) + 1e-12 or wid > 2 * a * t0 + 1e-12:
            return False, dict(reason="the width in units of ln Z exceeds 2 a t/(1 + a(W - t))", a=a, W=W0, t=t0)
    # an error in the evaluated energies
    for it in range(max(30, trials // 4)):
        N = int(rng.integers(6, 40))
        mlo = rng.normal(0, 1.5, N)
        gap = rng.exponential(0.5, N) + 1e-3
        if it == 0:
            gap[0] = 0.01                                           # a state where the sandwich is narrow
        mhi = mlo + gap
        E = mlo + gap * rng.random(N)
        if it == 0:
            E[0] = mlo[0]
        e_err = float(rng.uniform(0.001, 0.05))
        Et = E + rng.uniform(-e_err, e_err, N)
        if it == 0:
            Et[0] = E[0] - e_err
        Zlo, Zhi = float(np.exp(-mlo).sum()), float(np.exp(-mhi).sum())
        wq = np.exp(-mlo) - np.exp(-mhi)
        q = wq / (Zlo - Zhi)
        W, Wt = (np.exp(-E) - np.exp(-mhi)) / wq, (np.exp(-Et) - np.exp(-mhi)) / wq
        est = Zhi + (Zlo - Zhi) * float(q @ Wt)
        ZE, ZEt = float(np.exp(-E).sum()), float(np.exp(-Et).sum())
        if abs(est - ZEt) > 1e-10 * ZEt or abs(math.log(ZEt) - math.log(ZE)) > e_err + 1e-12:
            return False, dict(reason="with perturbed energies the sampler does not estimate Z of the perturbed energy, or that is off by more than the error")
        amp = np.abs(Wt - W) * (-np.expm1(-gap)) / math.expm1(e_err)
        if amp.max() > 1 + 1e-9:
            return False, dict(reason="a value of W moves by more than (e^e - 1)/(1 - e^-U)")
        if abs(float(q @ (1 / -np.expm1(-gap))) - Zlo / (Zlo - Zhi)) > 1e-9 * Zlo / (Zlo - Zhi):
            return False, dict(reason="the mean of 1/(1 - e^-U) under the sampler is not Z(m-)/(Z(m-) - Z(m+))")
        stats["shift"] = max(stats["shift"], abs(math.log(ZEt) - math.log(ZE)) / e_err)
        stats["amplified"] = max(stats["amplified"], float(np.abs(Wt - W).max()) / e_err)
    if not (stats["cases"] == 5 and stats["leaves"] == 1 and stats["eb_bad"] > 0.3 and stats["amplified"] > 20 and stats["shift"] <= 1 + 1e-9
            and stats["tv_over_bound"] < 3.6 and stats["nkl_over_tv"] < 3.6):
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


@conjecture("XXIV.12 Nested sandwiches: the inner bracket at the price of free rejections (theory report Proposition 11.113a; an answer to the Scientific Discovery Division's question P6-T3, SCI-MSG-0025).  Let m- <= e- <= E <= e+ <= m+ pointwise, with Z(m-), Z(m+) known, the Gibbs measure of m- sampleable and e-, e+ computable pointwise without an evaluation of E.  With q proportional to e^{-m-} - e^{-m+}, beta = (e^{-e+} - e^{-m+})/(e^{-m-} - e^{-m+}), rho = (e^{-e-} - e^{-e+})/(e^{-m-} - e^{-m+}) and W_in = (e^{-E} - e^{-e+})/(e^{-e-} - e^{-e+}): (a) beta, rho, beta + rho lie in [0, 1] and the variable of the outer sampler is W = beta + rho W_in; (b) Z(e+) = Z(m+) + (Z(m-) - Z(m+)) E_q beta, Z(e-) - Z(e+) = (Z(m-) - Z(m+)) E_q rho, and a draw of q accepted with probability rho has the law of the inner sandwich's own sampler - so E is evaluated at a fraction E_q rho of the proposals only; (c) with N_f free draws and N evaluated draws, |Z(E) - Z(m+) - A(beta_bar + rho_bar W_bar)| <= A(t_f + rho_bar t) with probability 1 - delta, A = Z(m-) - Z(m+), t_f = sqrt(ln(6/delta)/(2 N_f)), t = sqrt(ln(6/delta)/(2 N)) (coverage simulated; the two-end form of the Scientific Discovery Division's review SCI-REV-0015, m8, which replaced our 2 t_f: in every run the error is at most the larger of the errors of the means of beta and of beta + rho, plus rho_bar times the error of the inner mean), and a free term cannot be dropped; the variant with one known mean, E_q W = E_q(beta + rho/2) + E_q rho (E_in W_in - 1/2) (that division's, SCI-RES-0017); against the plain sampler at equal evaluations the bound is narrower iff sqrt(N/N_f) + rho_bar < kappa(delta) = sqrt(ln(2/delta)/ln(6/delta)), which is 0.855, 0.878, 0.910 at delta = 0.1, 0.05, 0.01, and with every accepted draw evaluated only for rho_bar < 0.316 at delta = 0.05; (d) at equal numbers of evaluations the half-width is that of the outer sampler times E_q rho = (Z(e-) - Z(e+))/(Z(m-) - Z(m+)) in the limit of many free draws - 0.1 in a constructed instance where the outer model is loose on states at which the inner bracket has no width")
def t_nested_sandwich(rng, trials):
    stats = dict(cases=0, runs=0, misses=0, misses_without_free_term=0, runs_few_free=0, least_rho=math.inf, gain=None,
                 two_end_tight=0.0)
    delta = 0.1
    # against the plain sampler (review SCI-REV-0015, m10, for the two-end bound)
    kap = {d_: math.sqrt(math.log(2 / d_) / math.log(6 / d_)) for d_ in (0.1, 0.05, 0.01)}
    if any(abs(kap[d_] - v_) > 5e-4 for d_, v_ in ((0.1, 0.855), (0.05, 0.878), (0.01, 0.910))) \
            or abs(((math.sqrt(1 + 4 * kap[0.05]) - 1) / 2) ** 2 - 0.316) > 5e-4:
        return False, dict(reason="the constants of the comparison with the plain sampler")
    for _ in range(200):
        d_ = float(rng.choice([0.1, 0.05, 0.01]))
        Ne_, Nf_, rb_ = int(rng.integers(10, 5000)), int(rng.integers(10, 500000)), float(rng.uniform(0, 1))
        nested = math.sqrt(math.log(6 / d_) / (2 * Nf_)) + rb_ * math.sqrt(math.log(6 / d_) / (2 * Ne_))
        plain = math.sqrt(math.log(2 / d_) / (2 * Ne_))
        if (nested < plain) != (math.sqrt(Ne_ / Nf_) + rb_ < kap[d_]):
            return False, dict(reason="the criterion sqrt(N/N_f) + rho_bar < kappa(delta) for the nested bound to be the narrower one")
    for it in range(max(40, trials // 3)):
        N = int(rng.integers(8, 50))
        E = rng.normal(0, 1.5, N)
        env = rng.exponential(float(rng.choice([0.05, 0.3, 1.0])), N) * (rng.random(N) < 0.6)     # the inner half-width; zero on many states
        slack_lo, slack_hi = rng.exponential(0.5, N), rng.exponential(0.5, N)
        c = E + env * rng.uniform(-1, 1, N)                         # the centre of the inner bracket
        elo, ehi = c - env, c + env
        mlo, mhi = elo - slack_lo, ehi + slack_hi
        if it == 0:
            # the constructed instance: outer half-width 1 everywhere, inner half-width 1 on four states of forty
            N = 40
            E = np.zeros(N)
            env = np.where(np.arange(N) < 4, 1.0, 0.0)
            c = E.copy()
            elo, ehi = c - env, c + env
            mlo, mhi = c - 1.0, c + 1.0
        wq = np.exp(-mlo) - np.exp(-mhi)
        Zlo, Zhi = float(np.exp(-mlo).sum()), float(np.exp(-mhi).sum())
        A = Zlo - Zhi
        q = wq / A
        beta = (np.exp(-ehi) - np.exp(-mhi)) / wq
        rho = (np.exp(-elo) - np.exp(-ehi)) / wq
        inner = np.exp(-elo) - np.exp(-ehi)
        with np.errstate(divide="ignore", invalid="ignore"):
            Win = np.where(inner > 0, (np.exp(-E) - np.exp(-ehi)) / np.where(inner > 0, inner, 1.0), 0.0)
        W = (np.exp(-E) - np.exp(-mhi)) / wq
        if min(beta.min(), rho.min()) < -1e-12 or (beta + rho).max() > 1 + 1e-12 or Win.min() < -1e-12 or Win.max() > 1 + 1e-12:
            return False, dict(reason="beta, rho, beta + rho or the inner variable leave [0, 1]")
        if np.abs(W - (beta + rho * Win)).max() > 1e-10:
            return False, dict(reason="the outer variable is not beta + rho times the inner variable")
        Zelo, Zehi, ZE = float(np.exp(-elo).sum()), float(np.exp(-ehi).sum()), float(np.exp(-E).sum())
        if abs(Zhi + A * float(q @ beta) - Zehi) > 1e-10 * Zehi or abs(A * float(q @ rho) - (Zelo - Zehi)) > 1e-10 * Zelo:
            return False, dict(reason="the partition sums of the inner models are not Z(m+) + A E_q beta and A E_q rho apart")
        rate = float(q @ rho)
        if rate > 1e-12:
            q_in = q * rho / rate
            if np.abs(q_in - inner / (Zelo - Zehi)).max() > 1e-10:
                return False, dict(reason="accepted draws do not have the law of the inner sandwich's sampler")
            # one known mean: c = beta + rho/2 needs no evaluation, and E_q W = E_q c + E_q rho (E_in W_in - 1/2)
            if abs(float(q @ W) - (float(q @ (beta + rho / 2)) + rate * (float(q_in @ Win) - 0.5))) > 1e-10:
                return False, dict(reason="the identity of the variant with one known mean")
            if abs(Zehi + (Zelo - Zehi) * float(q_in @ Win) - ZE) > 1e-10 * ZE:
                return False, dict(reason="Z(E) is not Z(e+) + (Z(e-) - Z(e+)) E W_in")
        else:
            q_in = None
        stats["least_rho"] = min(stats["least_rho"], rate)
        if it == 0:
            stats["gain"] = rate                                     # half-width ratio at equal numbers of evaluations
            if abs(rate - 4 * math.sinh(1.0) / (40 * math.sinh(1.0))) > 1e-12:
                return False, dict(reason="the constructed instance: E_q rho should be 0.1", rate=rate)
        # (c) coverage with many free draws, and with few (where the free-sampling term decides)
        if q_in is None:
            continue
        for Nf, Ne, key in ((4000, 60, "many"), (40, 4000, "few")):
            tf, te = math.sqrt(math.log(6 / delta) / (2 * Nf)), math.sqrt(math.log(6 / delta) / (2 * Ne))
            reps = 12
            free = rng.choice(N, size=(reps, Nf), p=q)
            ev = rng.choice(N, size=(reps, Ne), p=q_in)
            bbar, rbar, wbar = beta[free].mean(axis=1), rho[free].mean(axis=1), Win[ev].mean(axis=1)
            estz = Zhi + A * (bbar + rbar * wbar)
            # the two-end inequality, run by run: the error of the free part is affine in the inner mean
            mu_in = float(q_in @ Win)
            two_end = np.maximum(np.abs(bbar - float(q @ beta)), np.abs(bbar + rbar - float(q @ (beta + rho)))) \
                + rbar * np.abs(wbar - mu_in)
            if (np.abs(estz - ZE) > A * two_end * (1 + 1e-9) + 1e-12 * ZE).any():
                return False, dict(reason="the error exceeds the larger of the two end errors plus rho_bar times the inner error")
            stats["two_end_tight"] = max(stats["two_end_tight"], float((np.abs(estz - ZE) / (A * two_end + 1e-300)).max()))
            miss = np.abs(estz - ZE) > A * (tf + rbar * te) * (1 + 1e-12)
            stats["runs"] += reps
            stats["misses"] += int(miss.sum())
            if key == "few":
                stats["runs_few_free"] += reps
                stats["misses_without_free_term"] += int((np.abs(estz - ZE) > A * rbar * te * (1 + 1e-12)).sum())
        stats["cases"] += 1
    if stats["misses"] > delta * stats["runs"]:
        return False, dict(reason="the bracket of the nested sampler misses more often than delta", **stats)
    if not (stats["cases"] >= 30 and stats["gain"] is not None and abs(stats["gain"] - 0.1) < 1e-12
            and stats["misses_without_free_term"] > 0.3 * stats["runs_few_free"] and stats["two_end_tight"] > 0.9):
        return False, dict(reason="cases not exercised, or the free-sampling term was never needed", **stats)
    return True, stats


# -----------------------------------------------------------------------------------------------------------------
# XXV. Known parts with interactions along the chain: nearest-neighbour (Markov) reference measures (theory report
#      11.32; workstream Y, referee R11, review SCI-REV-0010 of the Scientific Discovery Division)
# -----------------------------------------------------------------------------------------------------------------
def mk_chain(fields, couplings):
    """binary nearest-neighbour chain: pi(x) proportional to exp(-sum_i f_i[x_i] - sum_i J_i[x_i][x_{i+1}]); (confs, pi)"""
    n = len(fields)
    confs = list(itertools.product((0, 1), repeat=n))
    w = np.array([math.exp(-sum(fields[i][x[i]] for i in range(n)) - sum(couplings[i][x[i]][x[i + 1]] for i in range(n - 1)))
                  for x in confs])
    return confs, w / w.sum()


def mk_dist(confs, d):
    """d(x, y) = sum_i d[i][x_i][y_i] as a matrix"""
    X = np.array(confs)
    D = np.zeros((len(confs), len(confs)))
    for i in range(X.shape[1]):
        di = np.array(d[i])
        D += di[X[:, i][:, None], X[:, i][None, :]]
    return D


def mk_member(rng, D, scale=2.0):
    """a random member of {psi : psi(x) - psi(y) <= d(x, y)}: an inf-convolution of a random function"""
    r = rng.normal(0, scale, D.shape[0])
    return (r[None, :] + D).min(axis=1)


def mk_in_class(psi, D, tol=1e-9):
    return bool(((psi[:, None] - psi[None, :]) <= D + tol).all())


def mk_sym_block_law(L, p, prev=None):
    """law of L consecutive sites of the symmetric binary chain with flip probability p (stationary, or given the
    letter before the block); configurations as integers, site i = bit i"""
    P = np.zeros(2 ** L)
    for x in range(2 ** L):
        b = [(x >> i) & 1 for i in range(L)]
        w = 0.5 if prev is None else (p if b[0] != prev else 1 - p)
        for i in range(L - 1):
            w *= p if b[i] != b[i + 1] else 1 - p
        P[x] = w
    return P


def mk_cube_vertices(w, tol=1e-9):
    """all vertices of {f : |f(x) - f(x^i)| <= w_i} on the cube Q_L, f(0) = 0: a vertex has a connected graph of tight
    edges, hence a spanning tree of tight edges with signs (L <= 3: 384 trees of Q_3)"""
    L = len(w)
    nv = 2 ** L
    edges = [(x, x | (1 << i), i) for x in range(nv) for i in range(L) if not (x >> i) & 1]
    ea = np.array([e[0] for e in edges]); eb = np.array([e[1] for e in edges]); ew = np.array([w[e[2]] for e in edges])
    signs = np.array(list(itertools.product((1.0, -1.0), repeat=nv - 1)))
    seen = {}
    for S in itertools.combinations(range(len(edges)), nv - 1):
        adj = {v: [] for v in range(nv)}
        for k in S:
            a, b, i = edges[k]
            adj[a].append((b, k)); adj[b].append((a, k))
        col = {k: t for t, k in enumerate(S)}
        B = np.zeros((nv, nv - 1)); seen_v = {0}; stack = [0]
        while stack:
            v = stack.pop()
            for (u2, k) in adj[v]:
                if u2 not in seen_v:
                    seen_v.add(u2); B[u2] = B[v]; B[u2, col[k]] = 1.0; stack.append(u2)
        if len(seen_v) < nv:
            continue                                               # not a spanning tree
        F = (signs * np.array([w[edges[k][2]] for k in S])[None, :]) @ B.T
        ok = (np.abs(F[:, ea] - F[:, eb]) <= ew[None, :] + tol).all(axis=1)
        for f in F[ok]:
            seen[tuple(np.round(f, 9))] = f
    return np.array([seen[k] for k in sorted(seen)])


def mk_heights(L):
    """integer height functions on Q_L (f(0) = 0, |f(x) - f(x^i)| = 1 on every edge): the vertices for a uniform slope"""
    nv = 2 ** L
    order = sorted(range(nv), key=lambda x: (bin(x).count("1"), x))
    out, f = [], [None] * nv

    def rec(k):
        if k == nv:
            out.append(list(f)); return
        x = order[k]
        vals = None
        for i in range(L):
            y = x ^ (1 << i)
            if f[y] is not None:
                c = {f[y] - 1, f[y] + 1}
                vals = c if vals is None else vals & c
        for v in sorted(vals):
            f[x] = v
            rec(k + 1)
        f[x] = None

    f[0] = 0
    rec(1)
    return np.array(out, float)


def mk_rows(pi, V):
    lp = np.log(np.asarray(pi, float))[None, :] - np.asarray(V, float)
    lp -= lp.max(axis=1, keepdims=True)
    P = np.exp(lp)
    return P / P.sum(axis=1, keepdims=True)


def mk_renyi(P, t, iters=400):
    """Arimoto iteration for F*(t) = max_M -t ln sum_a (sum_phi M pi_phi^t)^(1/t); returns (G_t(M), dual value at the
    centre of M, M): by weak duality the first is a lower and the second an upper bound for F*(t), for every M"""
    Pt = P ** t
    M = np.full(P.shape[0], 1.0 / P.shape[0])
    for _ in range(iters):
        s = M @ Pt
        N = float((s ** (1.0 / t)).sum())
        r = Pt @ (s ** ((1.0 - t) / t))
        M = M * (r / N) ** (-t / (1.0 - t))
        M /= M.sum()
    s = M @ Pt
    N = float((s ** (1.0 / t)).sum())
    r = Pt @ (s ** ((1.0 - t) / t))
    return -t * math.log(N), -math.log(float(r.min())) + (1.0 - t) * math.log(N), M


def mk_capacity(P, iters=3000):
    """Blahut-Arimoto: (I(M; P), max_phi KL(pi_phi || Q_M)), a lower and an upper bound for the capacity"""
    M = np.full(P.shape[0], 1.0 / P.shape[0])
    lP = np.log(P)
    for _ in range(iters):
        Q = M @ P
        kl = (P * (lP - np.log(Q)[None, :])).sum(axis=1)
        M = M * np.exp(kl - kl.max())
        M /= M.sum()
    Q = M @ P
    kl = (P * (lP - np.log(Q)[None, :])).sum(axis=1)
    return float(M @ kl), float(kl.max())


def mk_ustar(u, p):
    """the fixed point of x = u + ln[((1-p)e^x + p)/(p e^x + 1 - p)] (p < 1/2): the one-sided slack of the Markov recursion"""
    x = u
    for _ in range(400):
        x = u + math.log(((1 - p) * math.exp(x) + p) / (p * math.exp(x) + 1 - p))
    return x


def mk_cube(u):
    """the uniform binary cube at slope u: (h, a, E) per site"""
    Psi = lambda s: math.log(math.cosh(s / 2))
    v, t = mf_golden(lambda t: -(t * Psi(u) - Psi(t * u)), 1e-6, 1 - 1e-6, tol=1e-12)
    pu = 1 / (1 + math.exp(u))
    return -v, math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu), Psi(u)


@conjecture("XXIV.13 One side at a time: what a floor alone and a ceiling alone certify (theory report Proposition 11.113b; an answer to the Scientific Discovery Division's question A16-T2; part (a) is its Lemma A17.16, machine-checked by it and adopted as SandwichCost.lean).  For m_lo <= E <= m_up on a finite set, means under the true ensemble: (a) the ceiling's defect ln Z(E) - ln Z(m_up) lies between <b> - <b^2>/2 and <b>, b = m_up - E; the floor's excess ln Z(m_lo) - ln Z(E) = ln <e^a> lies between <a> and <a> + (e^A/2) <a^2>, a = E - m_lo <= A, and is not bounded by any multiple of its mean band - a state of true probability 1/D with band D has mean band 1 and excess at least D - ln D - while the ceiling's defect never exceeds its mean band; (b) under the floor's Gibbs measure W = e^{-(E - m_lo)} lies in (0, 1] and has mean Z(E)/Z(m_lo), so N samples give a two-sided Hoeffding bracket with radius sqrt(ln(2/delta)/(2N)) - exact binomial coverage at least 1 - delta, and with half the radius not - at a relative accuracy eps for N = ln(2/delta) e^{2x}/(2 eps^2), x the excess; (c) under the ceiling's Gibbs measure W = e^{m_up - E} >= 1 has mean Z(E)/Z(m_up) and every truncation min(W, c) has a smaller mean, so the lower side is certified from samples, but lowering the energy at one unevaluated state by D stays below the ceiling, leaves every evaluated value unchanged and raises ln Z by at least D + ln of the true probability of that state: no finite upper bound without evaluating every state")
def t_one_side(rng, trials):
    stats = dict(lemma=0, floor_slack=0.0, ceil_slack=0.0, big_band=0, families=0, coverage=1.0, half_fails=0, trunc=0, needles=0)
    lnz = lambda f: float(np.log(np.exp(-(f - f.min())).sum()) - f.min())
    # (a) the two free bounds on random instances; some with a large band, where the factor e^A / 2 matters
    for it in range(max(60, trials // 2)):
        n = int(rng.integers(2, 9))
        E = rng.normal(0, 1.5, n)
        scale = float(rng.choice([0.2, 1.0, 4.0]))
        a = rng.uniform(0, scale, n)
        b = rng.uniform(0, scale, n)
        if it % 5 == 0:
            a[int(rng.integers(n))] = float(rng.uniform(6.0, 9.0))               # one state with a large band below
            stats["big_band"] += 1
        lo, up = E - a, E + b
        w = np.exp(-(E - E.min()))
        w /= w.sum()
        A = float(a.max())
        excess = lnz(lo) - lnz(E)
        defect = lnz(E) - lnz(up)
        ma, ma2, mb, mb2 = float(w @ a), float(w @ a ** 2), float(w @ b), float(w @ b ** 2)
        if abs(excess - math.log(float(w @ np.exp(a)))) > 1e-9 or abs(defect + math.log(float(w @ np.exp(-b)))) > 1e-9:
            return False, dict(reason="the excess of the floor is not ln <e^a>, or the defect of the ceiling not -ln <e^-b>")
        if not (ma - 1e-10 <= excess <= ma + (math.exp(A) / 2) * ma2 + 1e-10):
            return False, dict(reason="floor: <a> <= excess <= <a> + (e^A/2) <a^2> fails", excess=excess, ma=ma, ma2=ma2, A=A)
        if not (mb - mb2 / 2 - 1e-10 <= defect <= mb + 1e-10):
            return False, dict(reason="ceiling: <b> - <b^2>/2 <= defect <= <b> fails", defect=defect, mb=mb, mb2=mb2)
        stats["floor_slack"] = max(stats["floor_slack"], excess - ma)
        stats["ceil_slack"] = max(stats["ceil_slack"], mb - defect)
        stats["lemma"] += 1
    # a state of true probability 1/D with band D: mean band 1; the floor loses D - ln D, the ceiling at most 1
    for D in (5.0, 10.0, 20.0, 40.0):
        w = np.array([1 - 1 / D, 1 / D])
        band = np.array([0.0, D])
        mean_band = float(w @ band)
        excess = math.log(float(w @ np.exp(band)))
        defect = -math.log(float(w @ np.exp(-band)))
        if not (abs(mean_band - 1) < 1e-12 and excess >= D - math.log(D) and defect <= mean_band and defect < 2 / D + 1e-12):
            return False, dict(reason="the two-state family: mean band, excess of the floor, defect of the ceiling", D=D,
                               excess=excess, defect=defect)
        if D >= 20 and not excess > 5 * mean_band:
            return False, dict(reason="the floor's excess should not be bounded by a multiple of its mean band", D=D)
        stats["families"] += 1
    # (b) the floor's sampler: identity, exact binomial coverage of the Hoeffding bracket, and the sample size
    delta = 0.05
    for it in range(12):
        n = int(rng.integers(2, 7))
        E = rng.normal(0, 1.0, n)
        a = rng.uniform(0, 3.0, n)
        lo = E - a
        qlo = np.exp(-(lo - lo.min()))
        qlo /= qlo.sum()
        W = np.exp(-a)
        if abs(float(qlo @ W) - math.exp(lnz(E) - lnz(lo))) > 1e-10 or W.max() > 1 + 1e-12 or W.min() <= 0:
            return False, dict(reason="E_{q_lo} e^{-(E - m_lo)} is not Z(E)/Z(m_lo), or W is not in (0, 1]")
    for N, p1 in ((200, 0.5), (400, 0.3), (120, 0.5)):
        # W takes the values 1 (probability p1 under the floor's measure) and e^{-30} (essentially 0): the mean is K/N
        mu = p1 + (1 - p1) * math.exp(-30.0)
        t = math.sqrt(math.log(2 / delta) / (2 * N))
        pmf = np.exp(bx_binom_logpmf(N, p1))
        means = (np.arange(N + 1) + (N - np.arange(N + 1)) * math.exp(-30.0)) / N
        cover = float(pmf[np.abs(means - mu) <= t + 1e-15].sum())
        cover_half = float(pmf[np.abs(means - mu) <= t / 2 + 1e-15].sum())
        if cover < 1 - delta:
            return False, dict(reason="the two-sided Hoeffding bracket of the floor's sampler covers with probability below 1 - delta",
                               N=N, p1=p1, cover=cover)
        stats["coverage"] = min(stats["coverage"], cover)
        stats["half_fails"] += int(cover_half < 1 - delta)
    for x, eps in ((0.5, 0.1), (3.0, 0.1), (6.0, 0.05)):
        N = math.ceil(math.log(2 / delta) * math.exp(2 * x) / (2 * eps * eps))
        t = math.sqrt(math.log(2 / delta) / (2 * N))
        if not (t / math.exp(-x) <= eps + 1e-12 and math.log(1 + eps) <= eps and -math.log(1 - eps) <= eps / (1 - eps)):
            return False, dict(reason="the sample size of the floor's sampler at relative accuracy eps", x=x, eps=eps)
    # (c) the ceiling's sampler: the truncated mean is a lower bound; a needle below the ceiling is invisible
    for it in range(max(40, trials // 4)):
        n = int(rng.integers(3, 9))
        E = rng.normal(0, 1.5, n)
        b = rng.uniform(0, float(rng.choice([0.5, 3.0])), n)
        up = E + b
        qup = np.exp(-(up - up.min()))
        qup /= qup.sum()
        W = np.exp(b)
        ratio = math.exp(lnz(E) - lnz(up))
        if abs(float(qup @ W) - ratio) > 1e-9 * ratio or W.min() < 1 - 1e-12:
            return False, dict(reason="E_{q_up} e^{m_up - E} is not Z(E)/Z(m_up), or W is below 1")
        for c in (1.0, 1.5, 4.0, 50.0):
            tm = float(qup @ np.minimum(W, c))
            if not (1 - 1e-12 <= tm <= ratio + 1e-12):
                return False, dict(reason="the truncated mean of the ceiling's weights is not between 1 and Z(E)/Z(m_up)", c=c, tm=tm, ratio=ratio)
            stats["trunc"] += 1
        # the needle: one state, not evaluated, lowered by D
        a0 = int(rng.integers(n))
        w = np.exp(-(E - E.min()))
        w /= w.sum()
        for D in (5.0, 30.0):
            E2 = E.copy()
            E2[a0] -= D
            if not ((E2 <= up + 1e-12).all() and (np.delete(E2, a0) == np.delete(E, a0)).all()):
                return False, dict(reason="the needle leaves the class below the ceiling or changes an evaluated value")
            if not lnz(E2) - lnz(E) >= D + math.log(float(w[a0])) - 1e-9:
                return False, dict(reason="a needle of depth D raises ln Z by less than D + ln of the true probability of its state",
                                   D=D, rise=lnz(E2) - lnz(E), bound=D + math.log(float(w[a0])))
        stats["needles"] += 1
    if not (stats["lemma"] >= 60 and stats["big_band"] >= 10 and stats["floor_slack"] > 1.0 and stats["ceil_slack"] > 0.05
            and stats["families"] == 4 and stats["coverage"] < 0.999 and stats["half_fails"] >= 2 and stats["trunc"] >= 160
            and stats["needles"] >= 40):
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


@conjecture("XXV.1 Nearest-neighbour chains as known parts: the two exact reductions to products of blocks, and the lower bound for every algorithm (theory report Theorem 11.116(a)-(c); workstream Y, Theorems Y1, Y3 and Lemma A; re-derived by referee R11 and by the Scientific Discovery Division, SCI-REV-0010).  (U) With cuts between blocks, pi = rho e^{-g}/E_rho e^{-g} for the product rho of the free-boundary block laws and g the cut interactions, ln A_pi(psi) = ln A_rho(psi + g) - ln A_rho(g), and psi + g lies in the class of the envelope with the slacks delta^-(a, a') = max_b [J(a, b) - J(a', b)] at the site left of a cut and delta^+(b, b') = max_a [J(a, b) - J(a, b')] at the site right of it - and not in the class without them; (L') for blocks with gaps, the marginal on the blocks is the product of the block marginals times prod rho_j, and for every psi' in the class of the envelope reduced by eps^-/+ at the block ends, psi' + sum ln rho_j is a member of the chain's class with A_pi = A_product(psi') exactly; (A) for any label law M and 0 < t < 1 the soft minimum gamma* of the normalised labels is a member, sum_phi M(phi) (pi_phi/pi_gamma*)^t is the constant e^{-G_t(M)}, and gamma* - (r - Phi_phi)_+ is a member that raises ln A by at least r")
def t_markov_reductions(rng, trials):
    stats = dict(chains=0, U=0, U_needs_slack=0, Lp=0, Lp_needs_reduction=0, A=0, worst=0.0)
    for it in range(max(8, trials // 20)):
        n = int(rng.integers(5, 8))
        fields = [rng.normal(0, 0.7, 2) for _ in range(n)]
        strong = it % 2 == 0
        coup = [rng.normal(0, 1.2 if strong else 0.25, (2, 2)) for _ in range(n - 1)]
        d = [np.array([[0.0, rng.uniform(0.3, 1.5)], [rng.uniform(0.3, 1.5), 0.0]]) for _ in range(n)]
        if not strong:
            d = [x * 2.5 for x in d]                                 # room for the reduced envelope of (L')
        confs, pi = mk_chain(fields, coup)
        D = mk_dist(confs, d)
        stats["chains"] += 1
        # ---- (U)
        cuts = sorted(c for c in range(n - 1) if rng.random() < 0.4) or [int(rng.integers(n - 1))]
        coup0 = [np.zeros((2, 2)) if c in cuts else coup[c] for c in range(n - 1)]
        bounds = [0] + [c + 1 for c in cuts] + [n]
        rho = np.ones(len(confs))
        for a, b in zip(bounds[:-1], bounds[1:]):                    # product of the free-boundary block laws
            cb, pb = mk_chain(fields[a:b], coup[a:b - 1])
            lookup = {x: v for x, v in zip(cb, pb)}
            rho *= np.array([lookup[x[a:b]] for x in confs])
        g = np.array([sum(coup[c][x[c]][x[c + 1]] for c in cuts) for x in confs])
        if abs(rho.sum() - 1) > 1e-12 or np.abs(pi - rho * np.exp(-g) / float(rho @ np.exp(-g))).max() > 1e-12:
            return False, dict(reason="pi is not rho e^{-g} normalised")
        dplus = [x.copy() for x in d]
        dminus_only = [x.copy() for x in d]
        for c in cuts:
            J = coup[c]
            for a in range(2):
                for a2 in range(2):
                    if a != a2:
                        dm = max(J[a][b] - J[a2][b] for b in range(2))
                        dp = max(J[b][a] - J[b][a2] for b in range(2))
                        dplus[c][a][a2] += dm; dminus_only[c][a][a2] += dm
                        dplus[c + 1][a][a2] += dp
        Dplus, Dhalf = mk_dist(confs, dplus), mk_dist(confs, dminus_only)
        for _ in range(4):
            psi = mk_member(rng, D)
            lhs = math.log(float(pi @ np.exp(-psi)))
            rhs = math.log(float(rho @ np.exp(-psi - g))) - math.log(float(rho @ np.exp(-g)))
            stats["worst"] = max(stats["worst"], abs(lhs - rhs))
            if abs(lhs - rhs) > 1e-10:
                return False, dict(reason="ln A_pi(psi) is not ln A_rho(psi + g) - ln A_rho(g)", err=abs(lhs - rhs))
            if not mk_in_class(psi + g, Dplus):
                return False, dict(reason="psi + g is not in the class of the envelope with the two slacks", cuts=cuts)
            stats["U"] += 1
            stats["U_needs_slack"] += int(not mk_in_class(psi + g, D))
        # ---- (L'): blocks with gaps (only on the chains with weak couplings, where the reduced envelope is nonnegative)
        if not strong:
            L1 = int(rng.integers(1, 3)); m = int(rng.integers(0, 2)); L2 = n - L1 - m
            B1, B2 = list(range(L1)), list(range(L1 + m, n))
            e1, s2 = L1 - 1, L1 + m
            X = np.array(confs)
            def marg(sites):
                out = {}
                for x, v in zip(confs, pi):
                    k = tuple(x[i] for i in sites)
                    out[k] = out.get(k, 0.0) + v
                return out
            mB, m1, m2 = marg(B1 + B2), marg(B1), marg(B2)
            me, ms, mes = marg([e1]), marg([s2]), marg([e1, s2])
            rho0 = np.array([[mes[(a, b)] / (me[(a,)] * ms[(b,)]) for b in range(2)] for a in range(2)])
            for k, v in mB.items():
                if abs(v - m1[k[:L1]] * m2[k[L1:]] * rho0[k[L1 - 1]][k[L1]]) > 1e-12:
                    return False, dict(reason="the marginal on the blocks is not the product of the block marginals times rho")
            lr = np.log(rho0)
            dred = [x.copy() for x in d]
            for a in range(2):
                for a2 in range(2):
                    if a != a2:
                        dred[e1][a][a2] -= max(lr[a][b] - lr[a2][b] for b in range(2))
                        dred[s2][a][a2] -= max(lr[b][a] - lr[b][a2] for b in range(2))
            if min(dred[e1].min(), dred[s2].min()) >= 0:
                bc = sorted(mB)
                pos = {k: t for t, k in enumerate(bc)}
                prodlaw = np.array([m1[k[:L1]] * m2[k[L1:]] for k in bc])
                proj = np.array([pos[tuple(x[i] for i in B1 + B2)] for x in confs])
                corr = np.array([lr[x[e1]][x[s2]] for x in confs])
                for reduced in (True, False):
                    Db = mk_dist(bc, [(dred if reduced else d)[i] for i in B1 + B2])
                    for _ in range(3):
                        psib = mk_member(rng, Db)
                        psi = psib[proj] + corr
                        inside = mk_in_class(psi, D)
                        if reduced:
                            if not inside:
                                return False, dict(reason="psi' + ln rho is not a member of the chain's class")
                            err = abs(math.log(float(pi @ np.exp(-psi))) - math.log(float(prodlaw @ np.exp(-psib))))
                            stats["worst"] = max(stats["worst"], err)
                            if err > 1e-10:
                                return False, dict(reason="A_pi(psi' + ln rho) is not A_product(psi')", err=err)
                            stats["Lp"] += 1
                        else:
                            stats["Lp_needs_reduction"] += int(not inside)
        # ---- Lemma A
        labels = [mk_member(rng, D) for _ in range(6)]
        M = rng.dirichlet(np.ones(6)); t = float(rng.uniform(0.2, 0.8))
        tilde = [phi + math.log(float(pi @ np.exp(-phi))) for phi in labels]          # normalised: E_pi e^{-phi~} = 1
        gibbs = [pi * np.exp(-ph) for ph in tilde]
        mix = sum(Mk * gk ** t for Mk, gk in zip(M, gibbs))
        G = -t * math.log(float((mix ** (1 / t)).sum()))
        gamma = -(1 / t) * np.log(sum(Mk * np.exp(-t * ph) for Mk, ph in zip(M, tilde)))
        if not mk_in_class(gamma, D):
            return False, dict(reason="the soft minimum of the labels is not a member of the class")
        pg = pi * np.exp(-gamma); Ag = float(pg.sum()); pg /= Ag
        const = sum(Mk * (gk / pg) ** t for Mk, gk in zip(M, gibbs))
        if np.abs(const - math.exp(-G)).max() > 1e-9 * math.exp(-G):
            return False, dict(reason="sum_phi M (pi_phi/pi_gamma*)^t is not the constant e^{-G_t(M)}",
                               spread=float(const.max() - const.min()))
        r = float(rng.uniform(0.1, 1.5))
        for ph in tilde:
            Phi = ph - (gamma + math.log(Ag))
            if abs(float(pg @ np.exp(-Phi)) - 1) > 1e-9:
                return False, dict(reason="E_{pi_gamma*} e^{-Phi} is not 1")
            alt = gamma - np.maximum(r - Phi, 0.0)
            if not mk_in_class(alt, D):
                return False, dict(reason="an alternative gamma* - (r - Phi)_+ is not a member of the class")
            if math.log(float(pi @ np.exp(-alt))) - math.log(Ag) < r - 1e-9:
                return False, dict(reason="an alternative does not raise ln A by r")
        stats["A"] += 1
    if not (stats["U_needs_slack"] > 0 and stats["Lp"] > 5 and stats["Lp_needs_reduction"] > 0 and stats["A"] >= 8):
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


@conjecture("XXV.2 The symmetric binary chain with flip probability p at slope u: what the interaction does to the exponents (theory report Theorem 11.116(d)-(f), Proposition 11.117; workstream Y, Propositions F, J; referee R11, section 4.4; Scientific Discovery Division, SCI-REV-0010, finding M1).  (a) The Markov recursion: for every member phi, every Markov chain Q and 0 < t < 1, sum_x pi_phi^t Q^{1-t} >= prod_i c_i with c_i the least one-site value over the class of the envelope with the one-sided slack d*_i = d_i + G_i (random inhomogeneous chains); (b) the threshold: max over all vertices of KL(pi || pi_phi) is attained by the uniform field and equals ln Z_n(u/2)/Z_n(0) for n <= 4, whose growth rate is E_F = ln[(1-p)cosh(u/2) + sqrt((1-p)^2 sinh^2(u/2) + p^2)] > ln cosh(u/2); (c) at u = 1 the exponent of every algorithm is above the uniform cube's: with block labels of reduced end slopes the product of block Gibbs laws is the Gibbs law of a member of the chain's class (checked end to end on 8 sites), so G_t of one block of 10 sites divided by 10 is a lower bound for every algorithm, and it exceeds 0.029139 at p = 0.3; (d) the direction depends on the slope: at (p, u) = (0.2, 3) the capacity of the block channel of three sites with slopes (u, u, u*), divided by 3 - an upper bound for the non-adaptive exponent at vanishing accuracy - is below the cube's ln 2 - H(1/(1+e^u)), while the threshold is above the cube's at every slope")
def t_markov_symmetric(rng, trials):
    stats = dict(F_cases=0, F_smallest=math.inf, F_needs_slack=0, thr=0, block_bound=0.0, reversal=0.0)
    # ---- (a) the product inequality of the Markov recursion
    for it in range(max(30, trials // 4)):
        n = int(rng.integers(3, 7))
        fields = [rng.normal(0, 0.6, 2) for _ in range(n)]
        coup = [rng.normal(0, 1.0, (2, 2)) for _ in range(n - 1)]
        d = [np.array([[0.0, rng.uniform(0.2, 1.5)], [rng.uniform(0.2, 1.5), 0.0]]) for _ in range(n)]
        confs, pi = mk_chain(fields, coup)
        D = mk_dist(confs, d)
        phi = mk_member(rng, D)
        t = float(rng.uniform(0.15, 0.85))
        # kernels of pi: P_1 = law of x_1, P_i(b, a) = P(x_i = a | x_{i-1} = b)
        X = np.array(confs)
        P1 = np.array([pi[X[:, 0] == a].sum() for a in range(2)])
        Pk = []
        for i in range(1, n):
            K = np.array([[pi[(X[:, i - 1] == b) & (X[:, i] == a)].sum() for a in range(2)] for b in range(2)])
            Pk.append(K / K.sum(axis=1, keepdims=True))
        q1 = rng.dirichlet(np.ones(2)); qk = [rng.dirichlet(np.ones(2), size=2) for _ in range(n - 1)]
        Q = np.array([q1[x[0]] * math.prod(qk[i - 1][x[i - 1]][x[i]] for i in range(1, n)) for x in confs])
        pphi = pi * np.exp(-phi); pphi /= pphi.sum()
        lhs = float((pphi ** t * Q ** (1 - t)).sum())

        def bound(with_slack):
            dstar = [None] * n
            dstar[n - 1] = d[n - 1].copy()
            for i in range(n - 2, -1, -1):
                Gi = np.zeros((2, 2))
                if with_slack:
                    K = Pk[i]                                      # kernel from site i to site i + 1
                    for a in range(2):
                        for a2 in range(2):
                            if a != a2:
                                ends = (math.exp(-dstar[i + 1][1][0]), math.exp(dstar[i + 1][0][1]))
                                Gi[a][a2] = max(math.log((K[a2][0] + K[a2][1] * r) / (K[a][0] + K[a][1] * r)) for r in ends)
                dstar[i] = d[i] + Gi
            prod = 1.0
            for i in range(n):
                rows = [P1] if i == 0 else [Pk[i - 1][b] for b in range(2)]
                qs = [q1] if i == 0 else [qk[i - 1][b] for b in range(2)]
                ci = math.inf
                for Pr, qr in zip(rows, qs):
                    for lam in np.linspace(-dstar[i][0][1], dstar[i][1][0], 201):   # gamma(1) - gamma(0)
                        gl = Pr * np.exp(-np.array([0.0, lam])); gl /= gl.sum()
                        ci = min(ci, float((qr ** (1 - t) * gl ** t).sum()))
                prod *= ci
            return prod

        b_slack, b_plain = bound(True), bound(False)
        if lhs < b_slack * (1 - 1e-9):
            return False, dict(reason="the product bound of the Markov recursion is violated", n=n, t=t, ratio=lhs / b_slack)
        stats["F_cases"] += 1
        stats["F_smallest"] = min(stats["F_smallest"], lhs / b_slack)
        stats["F_needs_slack"] += int(lhs < b_plain * (1 - 1e-9))
    # a case in which the slack decides: the uniform field on a strongly coupled chain, with the chain itself as Q
    p, u, n, t = 0.1, 1.0, 8, 0.5
    pi = mk_sym_block_law(n, p)
    mag = np.array([sum(1 if (x >> i) & 1 else -1 for i in range(n)) for x in range(2 ** n)], float)
    pphi = pi * np.exp(u / 2 * mag); pphi /= pphi.sum()
    lhs = float((pphi ** t * pi ** (1 - t)).sum())
    us = mk_ustar(u, p)

    def one_site(slope, row):
        best = math.inf
        for lam in (-slope, slope):
            gl = row * np.exp(-np.array([0.0, lam])); gl /= gl.sum()
            best = min(best, float((row ** (1 - t) * gl ** t).sum()))
        return best
    with_slack = one_site(us, np.array([0.5, 0.5])) * one_site(us, np.array([1 - p, p])) ** (n - 2) * one_site(u, np.array([1 - p, p]))
    without = one_site(u, np.array([0.5, 0.5])) * one_site(u, np.array([1 - p, p])) ** (n - 1)
    if lhs < with_slack * (1 - 1e-9):
        return False, dict(reason="the product bound of the Markov recursion is violated by the uniform field", ratio=lhs / with_slack)
    stats["F_needs_slack"] += int(lhs < without * (1 - 1e-9))
    # ---- (b) the threshold
    for p in (0.4, 0.3):
        u = 1.0
        lam = 1 - 2 * p
        EF = math.log((1 - p) * math.cosh(u / 2) + math.sqrt((1 - p) ** 2 * math.sinh(u / 2) ** 2 + p ** 2))
        if not EF > math.log(math.cosh(u / 2)) + 1e-3:
            return False, dict(reason="E_F does not exceed the cube's threshold", p=p)
        for n in (2, 3, 4):
            pi = mk_sym_block_law(n, p)
            V = u * mk_heights(n)
            P = mk_rows(pi, V)
            kl = (pi[None, :] * (np.log(pi)[None, :] - np.log(P))).sum(axis=1)
            s = np.array([[1 if (x >> i) & 1 else -1 for i in range(n)] for x in range(2 ** n)], float)
            m = s.sum(axis=1)
            target = math.log(float(pi @ np.exp(u / 2 * m)))             # ln Z_n(u/2)/Z_n(0)
            if abs(float(kl.max()) - target) > 1e-10:
                return False, dict(reason="the uniform field does not maximise KL(pi || pi_phi) over the vertices, or the value is not ln Z_n(h)/Z_n(0)",
                                   n=n, p=p, got=float(kl.max()), want=target)
            stats["thr"] += 1
        T = lambda hh: np.array([[(1 - p) * math.exp(hh), p * math.exp(-hh)], [p * math.exp(hh), (1 - p) * math.exp(-hh)]])
        v = np.array([0.5 * math.exp(u / 2), 0.5 * math.exp(-u / 2)]); growth = 0.0
        for _ in range(400):
            v2 = v @ T(u / 2); growth = math.log(v2.sum() / v.sum()); v = v2 / v2.sum()
        if abs(growth - EF) > 1e-9:
            return False, dict(reason="the growth rate of ln Z_n(u/2)/Z_n(0) is not E_F", growth=growth, EF=EF)
    # ---- (c) the direction at u = 1: a block certificate
    p, u, t = 0.3, 1.0, 0.45
    K = math.log((1 - p) / p)
    hc, ac, Ec = mk_cube(u)
    if abs(hc - 0.0291391) > 1e-6:
        return False, dict(reason="the cube's exponent at u = 1", h=hc)

    def block_labels(L, end):
        """site-wise labels -sum_i h_i sigma_i s_i with at most two walls; h_i = u/2 inside and `end` at the two ends"""
        hs = np.array([end] + [u / 2] * (L - 2) + [end])
        s = np.array([[1 if (x >> i) & 1 else -1 for i in range(L)] for x in range(2 ** L)], float)
        sig = []
        for walls in range(3):
            for W in itertools.combinations(range(1, L), walls):
                base = np.ones(L)
                for wpos in W:
                    base[wpos:] *= -1
                sig += [base, -base]
        return np.array([-(s * (hs * sg)[None, :]).sum(axis=1) for sg in sig])

    def end_to_end(L, end):
        """two blocks of L sites, no gap: is phi_a + phi_b + ln rho_0 in the chain's class, with product Gibbs law?"""
        lab = block_labels(L, end)
        n = 2 * L
        pi = mk_sym_block_law(n, p)
        piL = mk_sym_block_law(L, p)
        xs = np.arange(2 ** n)
        lo, hi = xs & (2 ** L - 1), xs >> L
        same = ((lo >> (L - 1)) & 1) == (hi & 1)
        lnrho = np.where(same, math.log(2 * (1 - p)), math.log(2 * p))
        ok, prodok = True, True
        for a, b in ((0, 1), (3, 2), (len(lab) - 1, 5), (7, len(lab) - 2)):
            psi = lab[a][lo] + lab[b][hi] + lnrho
            for i in range(n):
                ok &= bool((np.abs(psi - psi[xs ^ (1 << i)]) <= u + 1e-9).all())
            gl = pi * np.exp(-psi); gl /= gl.sum()
            ga = piL * np.exp(-lab[a]); ga /= ga.sum(); gb = piL * np.exp(-lab[b]); gb /= gb.sum()
            prodok &= bool(np.abs(gl - ga[lo] * gb[hi]).max() < 1e-12)
        return ok, prodok

    ok, prodok = end_to_end(4, (u - K) / 2)
    if not (ok and prodok):
        return False, dict(reason="block labels with reduced end slopes: the sum plus ln rho is not a member with product Gibbs law",
                           member=ok, product=prodok)
    L = 10
    G, _, _ = mk_renyi(mk_rows(mk_sym_block_law(L, p), block_labels(L, (u - K) / 2)), t, iters=400)
    stats["block_bound"] = G / L
    if not G / L > hc * 1.10:
        return False, dict(reason="the block certificate does not exceed the cube's exponent", bound=G / L, cube=hc)
    # ---- (d) the reversal at large slope
    p, u = 0.2, 3.0
    us = mk_ustar(u, p)
    if abs(us - (u + math.log(((1 - p) * math.exp(us) + p) / (p * math.exp(us) + 1 - p)))) > 1e-12 or not u < us < u + math.log((1 - p) / p):
        return False, dict(reason="the one-sided slack u*", us=us)
    V = mk_cube_vertices([u, u, us])
    if len(V) != 96 or len(mk_cube_vertices([1.0, 1.0, 1.0])) != 38 or len(mk_heights(3)) != 38 or len(mk_heights(4)) != 990:
        return False, dict(reason="vertex counts of the Lipschitz polytopes of small cubes", n=len(V))
    lowc, upc = mk_capacity(mk_rows(mk_sym_block_law(3, p, prev=0), V))
    hc, ac, Ec = mk_cube(u)
    stats["reversal"] = upc / 3 / ac
    if not (upc / 3 < 0.95 * ac and upc - lowc < 1e-6):
        return False, dict(reason="at (p, u) = (0.2, 3) the block bound for the capacity exponent is not below the cube's",
                           bound=upc / 3, cube=ac, bracket=upc - lowc)
    for uu in (0.5, 1.0, 3.0, 6.0):
        EF = math.log((1 - p) * math.cosh(uu / 2) + math.sqrt((1 - p) ** 2 * math.sinh(uu / 2) ** 2 + p ** 2))
        if not EF > mk_cube(uu)[2]:
            return False, dict(reason="the threshold is not above the cube's at some slope", u=uu)
    if not (stats["F_cases"] >= 30 and stats["F_needs_slack"] > 0 and stats["thr"] == 6):
        return False, dict(reason="cases not exercised", **stats)
    return True, stats


@conjecture("XXV.3 The small-slope law (theory report Proposition 11.117(b): Propositions R10.1, R10.2 of the Scientific Discovery Division, SCI-REV-0010).  For a finite space with law pi and a SYMMETRIC envelope u d_0, F*(t) = (t(1-t)/2) u^2 V + O(u^3) with V the largest variance of a function that is 1-Lipschitz for d_0 (without symmetry the law fails: on two points with d_0(0,1) = 1, d_0(1,0) = 0 the class is a segment and the coefficient is V/4 - the division's counter-example, SCI-REV-0014, M1; the first version of this test and of the proposition had dropped the word); for binary sites with the Hamming envelope and an associated law (a ferromagnetic chain with any fields) V = Var(sum_i s_i)/4, attained by the uniform field; for an antiferromagnetic chain it is the staggered field and Var(sum s_i)/4 is strictly smaller, so the factor is the structure factor at zero wave vector for ferromagnetic chains only; for the symmetric chain Var(sum s_i)/n tends to (1-p)/p")
def t_markov_small_slope(rng, trials):
    stats = dict(chains=0, random_f=0, closest=0.0, expansion=[], asym=[])
    s_of = lambda n: np.array([[1 if (x >> i) & 1 else -1 for i in range(n)] for x in range(2 ** n)], float)
    for n in (2, 3, 4):
        H = mk_heights(n)
        s = s_of(n)
        m, stag = s.sum(axis=1), (s * np.array([(-1) ** i for i in range(n)])[None, :]).sum(axis=1)
        var = lambda pi, f: float(pi @ (f - pi @ f) ** 2)
        for p in (0.2, 0.3, 0.45, 0.7, 0.85):
            pi = mk_sym_block_law(n, p)
            V = max(var(pi, f) for f in H)
            want = var(pi, m if p < 0.5 else stag) / 4
            if abs(V - want) > 1e-12:
                return False, dict(reason="the largest variance of a Lipschitz function is not that of the uniform (ferromagnet) or staggered (antiferromagnet) field",
                                   n=n, p=p, V=V, want=want)
            if p > 0.5 and not var(pi, m) / 4 < V - 1e-3:
                return False, dict(reason="for an antiferromagnetic chain Var(sum s)/4 should be strictly below V", n=n, p=p)
            stats["chains"] += 1
    # associated laws with fields: every 1-Lipschitz function has variance at most Var(sum s)/4
    for it in range(max(20, trials // 10)):
        n = int(rng.integers(3, 7))
        fields = [np.array([0.0, rng.normal(0, 1.0)]) for _ in range(n)]
        coup = [np.array([[0.0, k], [k, 0.0]]) for k in rng.uniform(0.0, 1.5, n - 1)]   # a penalty on unequal neighbours
        confs, pi = mk_chain(fields, coup)
        D = mk_dist(confs, [np.array([[0.0, 1.0], [1.0, 0.0]])] * n)
        m = np.array([sum(2 * b - 1 for b in x) for x in confs], float)
        vm = float(pi @ (m - pi @ m) ** 2) / 4
        for _ in range(5):
            f = mk_member(rng, D, scale=float(rng.choice([0.5, 2.0, 6.0])))
            vf = float(pi @ (f - pi @ f) ** 2)
            if vf > vm + 1e-10:
                return False, dict(reason="a 1-Lipschitz function has a larger variance than half the magnetisation under an associated law",
                                   n=n, vf=vf, vm=vm)
            stats["closest"] = max(stats["closest"], vf / vm)
            stats["random_f"] += 1
    # the expansion of the game function at second order
    n, p = 3, 0.3
    pi = mk_sym_block_law(n, p)
    H = mk_heights(n)
    V = max(float(pi @ (f - pi @ f) ** 2) for f in H)
    fstar = max(H, key=lambda f: float(pi @ (f - pi @ f) ** 2))
    for u in (0.1, 0.05):
        for t in (0.3, 0.5):
            # lower bound: the two labels +-u f* with equal weights; upper bound: the centre Q = pi (weak duality)
            P2 = mk_rows(pi, np.array([u * fstar, -u * fstar]))
            lo = -t * math.log(float(((0.5 * P2[0] ** t + 0.5 * P2[1] ** t) ** (1 / t)).sum()))
            P = mk_rows(pi, u * H)
            up = max(-math.log(float((row ** t * pi ** (1 - t)).sum())) for row in P)
            coef = t * (1 - t) * u * u / 2
            stats["expansion"].append((round(lo / coef / V, 4), round(up / coef / V, 4)))
            if not ((1 - 2.5 * u) * V * coef < lo <= up + 1e-15 and up < (1 + 2.5 * u) * V * coef):
                return False, dict(reason="F*(t) is not (t(1-t)/2) u^2 V to second order", u=u, t=t, lower=lo / coef, upper=up / coef, V=V)
    # without symmetry the law fails (Scientific Discovery Division, SCI-REV-0014, M1): two points, d_0(0, 1) = 1,
    # d_0(1, 0) = 0; the class is the segment {c 1[x = 0] : 0 <= c <= u}, V = q (1 - q), and the coefficient is V/4;
    # with the symmetric envelope on the same two points it is V.  On two points every law is a tilt of pi, so the
    # minimum over centres is a one-dimensional minimisation.
    for q, t in ((0.5, 0.3), (0.3, 0.5)):
        for u in (0.1, 0.05):
            coef = t * (1 - t) * u * u / 2 * q * (1 - q)
            pi2 = np.array([q, 1 - q])
            tilt = lambda c: mk_rows(pi2, np.array([[c, 0.0]]))[0]
            cost = lambda P, Q: -math.log(float((P ** t * Q ** (1 - t)).sum()))

            def radius(cs):
                # min over centres pi_psi of the largest cost: a grid to bracket the minimum, golden section inside
                Ps = [tilt(c) for c in cs]
                worst = lambda psi: max(cost(P, tilt(psi)) for P in Ps)
                grid = np.linspace(-1.5 * u, 2.5 * u, 201)
                i = int(np.argmin([worst(x) for x in grid]))
                a_, b_ = float(grid[max(i - 1, 0)]), float(grid[min(i + 1, 200)])
                for _ in range(45):
                    m1, m2 = a_ + 0.382 * (b_ - a_), a_ + 0.618 * (b_ - a_)
                    if worst(m1) <= worst(m2):
                        b_ = m2
                    else:
                        a_ = m1
                return worst(0.5 * (a_ + b_))

            seg = radius(np.linspace(0.0, u, 11))              # the envelope that is not symmetric: labels c in [0, u]
            sym = radius(np.linspace(-u, u, 21))               # the symmetric envelope: labels c in [-u, u]
            stats["asym"].append((round(seg / coef, 4), round(sym / coef, 4)))
            if not (0.25 - 0.3 * u < seg / coef < 0.25 + 0.05 * u and 1 - 1.2 * u < sym / coef < 1 + 0.3 * u):
                return False, dict(reason="two points: the coefficient is not V/4 for the one-sided envelope and V for the symmetric one",
                                   q=q, t=t, u=u, one_sided=seg / coef, symmetric=sym / coef)
    # the structure factor of the symmetric chain
    for p in (0.1, 0.3, 0.45):
        lam, n = 1 - 2 * p, 4000
        varm = n + 2 * sum((n - k) * lam ** k for k in range(1, n))
        if abs(varm / n - (1 - p) / p) > 0.01 * (1 - p) / p:
            return False, dict(reason="Var(sum s)/n does not tend to (1-p)/p", p=p, got=varm / n)
    if not (stats["chains"] == 15 and stats["random_f"] >= 100 and stats["closest"] > 0.3 and len(stats["asym"]) == 4):
        return False, dict(reason="cases not exercised", **stats)
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


@conjecture("DEAD.23 The site function F* is concave in the slope (hence R^max is smooth and the best split of the accuracy between site types is exact)", expect_fail=True)
def t_dead_site_function_concave(rng, trials):
    tri = st_site(*ST_SITES["tri"])
    f = [st_renyi(tri, t)[0] for t in (0.376, 0.378, 0.380)]
    d2 = (f[0] - 2 * f[1] + f[2]) / 0.002 ** 2
    ctrl = []
    for t0 in (0.2, 0.6):
        g = [st_renyi(tri, t)[0] for t in (t0 - 0.002, t0, t0 + 0.002)]
        ctrl.append((g[0] - 2 * g[1] + g[2]) / 0.002 ** 2)
    s4 = st_site([0.25] * 4, st_hamming(4, 1.0))
    g = [st_renyi(s4, t)[0] for t in (0.64, 0.65, 0.66)]
    d4 = (g[0] - 2 * g[1] + g[2]) / 0.01 ** 2
    if d2 > 0.5 and d4 > 0.01 and max(ctrl) < -0.3:
        return False, dict(reason="the triangle site (1, 1.5, 2) has a convex kink of F* at the label switch t = 0.378, the uniform four-letter Hamming site at t = 0.65 where the best grouping of its letters changes; away from the switches F* is strictly concave",
                           second_difference_triangle=d2, second_difference_four_letters=d4, controls=ctrl)
    return True, dict(second_difference_triangle=d2, second_difference_four_letters=d4, controls=ctrl)


@conjecture("DEAD.24 Beyond two letters the uniform site law is still the hardest (a field always helps, Proposition 11.65(b); no known part is harder than none, Corollary 11.91)", expect_fail=True)
def t_dead_uniform_law_hardest(rng, trials):
    out = {}
    E_field, E_unif = st_E(st_site([0.05, 0.5, 0.45], st_hamming(3, 1.0))), st_E(st_site([1 / 3] * 3, st_hamming(3, 1.0)))
    h_near = st_R([(1.0, st_site([0.02, 0.49, 0.49], st_hamming(3, 0.5)))], 0.0)[0]
    h_unif = st_R([(1.0, st_site([1 / 3] * 3, st_hamming(3, 0.5)))], 0.0)[0]
    # control: two letters, where the statement is a theorem
    two = True
    for u in (0.5, 1.0, 2.0):
        for t in (0.2, 0.5, 0.8):
            f0 = st_renyi(st_site([0.5, 0.5], st_hamming(2, u)), t)[0]
            for p in (0.3, 0.1):
                two &= st_renyi(st_site([1 - p, p], st_hamming(2, u)), t)[0] <= f0 + 1e-9
    if E_field > E_unif + 5e-4 and h_near > h_unif + 2e-4 and two:
        return False, dict(reason="three letters, Hamming envelope: at u = 1 the law (0.05, 0.5, 0.45) has a larger threshold than the uniform law, at u = 0.5 the law (0.02, 0.49, 0.49) has a larger exponent at vanishing accuracy; for two letters the uniform law is the hardest in all 18 cases tried",
                           E_field=E_field, E_uniform=E_unif, h_near_two_letters=h_near, h_uniform=h_unif)
    return True, dict(E_field=E_field, E_uniform=E_unif, h_near=h_near, h_uniform=h_unif, two_letters_ok=two)


@conjecture("DEAD.25 For B = 0 the uniform cube's optimal shell (1/2; p_u, p_u) keeps the uniform cube's value at every coupling 1 < beta J < beta J*(e, u), for every slope and accuracy, so that R_H(e) = R_unif(e) up to beta J* (Proposition 11.81(b) as first stated: 'the local minimum is then the global one'; true at u = 1 and u = 2)", expect_fail=True)
def t_dead_junction_large_slope(rng, trials):
    u, e = 8.0, 0.0
    frac = 0.99                                   # the coupling is 1 + frac (beta J* - 1) < beta J*
    half = np.array([0.5, 0.5])

    def cell(u_, frac_):
        rho = (math.log(2 / (1 + math.exp(-u_))) + e) / u_
        c2 = 1 / (2 * rho * (1 - rho)) - 2
        bstar = 1 + u_ * c2 / (2 * math.log((1 - rho) / rho))
        bJ = 1 + frac_ * (bstar - 1)
        pu = 1 / (1 + math.exp(u_))
        M = mf_model(bJ, 0.0, u_, K=400001)
        return bstar, bJ, pu, M

    bstar, bJ, pu, M = cell(u, frac)
    Ru = mf_R_unif(e, u)
    mu = np.array([1 - pu, pu])
    val = mf_r(M, half, mu, e, G=3000)
    # the far exit in closed form: the constant profile at a well (MI = 0); it is feasible iff u dist + I <= e + alpha
    m = 1.0
    for _ in range(400):
        m = math.tanh(bJ * m)
    kw = (1 - m) / 2
    far = u * (0.5 - min(pu, kw)) + float(M["I"](kw))
    budget = e + mf_alpha(M, half, mu)
    barrier, E_unif = float(M["I"](0.5)), math.log(math.cosh(u / 2))
    # the best symmetric shell (1/2; x, x) on a scan: positive only beyond the cliff where every constant exit is infeasible
    best = max(mf_r(M, half, np.array([1 - x, x]), e, G=1200) for x in np.linspace(0.02, 0.06, 21))
    # controls: the same fraction of the way to beta J* at u = 1 and u = 2, where the statement holds
    ctrl = True
    for uc in (1.0, 2.0):
        _, _, puc, Mc = cell(uc, frac)
        ctrl &= abs(mf_r(Mc, half, np.array([1 - puc, puc]), e, G=3000) - mf_R_unif(e, uc)) < 2e-7
    if (abs(bstar - 8.3366) < 2e-4 and far < budget - 0.1 and barrier > E_unif - e + u * max(pu - kw, 0.0) and val < 1e-9
            and best < Ru - 0.02 and ctrl):
        return False, dict(reason="at u = 8, e = 0 and beta J = 8.263 < beta J* = 8.337 the barrier I(1/2) = 3.438 exceeds the uniform cube's threshold E_unif = 3.307, the constant exit at a well is feasible for the uniform cube's shell, its value is 0, and the best symmetric shell has 0.367 against R_unif = 0.3985; at u = 1, 2 the value is the uniform cube's",
                           bstar=bstar, coupling=bJ, far_exit=far, budget=budget, barrier=barrier, E_unif=E_unif, value_at_uniform_shell=val, best_symmetric_shell=best, R_unif=Ru)
    return True, dict(bstar=bstar, coupling=bJ, far_exit=far, budget=budget, value_at_uniform_shell=val, best_symmetric_shell=best, R_unif=Ru, controls=ctrl)


@conjecture("DEAD.26 The extremal residual of a ratio of two macrostate weights is constant on each macrostate (the two states are shifted against each other by their distance), so R+(A,B) = e^{d(B,A)} w(A)/w(B) with d(B,A) the least distance from B to A -- the first guess for 'the uncertainty of a free-energy difference'", expect_fail=True)
def t_dead_ratio_constant_shift(rng, trials):
    # the three-point example of the Scientific Discovery Division: A = {x1, x2}, B = {y}, d(x1,y) = 1, d(x2,y) = d(x1,x2) = 10
    D = np.array([[0, 10.0, 1.0], [10.0, 0, 10.0], [1.0, 10.0, 0]])
    w = np.ones(3)
    v, t = mr_lp_bip(w, D, [0, 1], [2])
    shift = math.exp(1.0) * 2 / 1
    g = -np.log(t)
    # the two halves of the cube Q_6, uniform measure, u = 1: the extremal residual is the maximal field
    n, u = 6, 1.0
    W = np.array([math.comb(n, j) for j in range(n + 1)], dtype=float)
    At, Bt = [4, 5, 6], [0, 1, 2, 3]
    Dt = u * np.abs(np.subtract.outer(np.arange(n + 1), np.arange(n + 1))).astype(float)
    vt, _ = mr_lp_bip(W, Dt, At, Bt)
    shift_t = math.exp(u) * W[At].sum() / W[Bt].sum()
    # control: for single states the shift is exact
    vc, _ = mr_lp_bip(w, D, [0], [2])
    if abs(vc - math.e) < 1e-9 and v > 100 * shift and abs((g[1] - g[0]) + 9.0) < 1e-6 and vt > 1.5 * shift_t:
        return False, dict(reason="three states: R+ = e + e^10 against the constant shift 2e, and the extremal residual differs by 9 between the two states of A; the two halves of Q_6: the maximal field gives 2.8 times the constant shift; for single states the shift is exact",
                           three_points=v, constant_shift=shift, g_difference=float(g[1] - g[0]), cube_halves=vt, cube_constant_shift=shift_t)
    return True, dict(three_points=v, constant_shift=shift, cube_halves=vt, cube_constant_shift=shift_t, single_states=vc)


@conjecture("DEAD.27 (documented refutation, D55) 'In every run the candidate sets of the batched schedule have at most N_l members' (the first version of Theorem 11.84(ii)) — false without the stopping rule: if the calls of the previous rung return their trivial brackets, which a bracket procedure may do with probability delta', every outer point is a candidate (finding M1 of SCI-REV-0003); true on the good event, and in every run once the schedule stops when the set is larger", expect_fail=True)
def t_dead_candidates_every_run(rng, trials):
    lam, eta, J, K, m_max, x = 0.5, 0.5, 30, 6, 14, 1.0
    c_eta, nu, b = (1 - eta) / (1 + eta), 6.0, 0.5
    s = np.exp(lam * np.arange(J + 1))
    Mmax = K * 2 ** m_max
    N = K + (J + 1) * max(K, 4 * (1 + eta) / c_eta * math.exp(lam) * nu * math.exp(x))
    wide, _ = rd_candidate_set(np.ones(Mmax), np.full(Mmax, float(s[-1]) * math.exp(lam)), s, K, m_max, nu, c_eta, eta, b, 1.0)
    if wide.sum() > N:
        return False, dict(reason="more than N candidates in a run in which the previous rung returned trivial brackets", candidates=int(wide.sum()), N=round(N), M_max=Mmax)
    return True, {}


@conjecture("DEAD.28 (documented refutation, D56) 'A typical-norm estimate is a certificate: the interval mean + two standard errors of the sampled Boltzmann factors is an upper confidence bound at level 0.9' — false in a box class: at a member with a rare deep dip (probability 1/m per sample) the sample contains no dip, and the sample variance vanishes, with probability about 1/e, and the interval then excludes the true mean", expect_fail=True)
def t_dead_naive_interval(rng, trials):
    delta, reps, m = 0.1, 4000, 200
    samples = (rng.random((reps, m)) < 1.0 / m).astype(float)
    _, naive = bx_upper_bounds(samples, delta)
    viol = float((naive < 1.0 / m).mean())
    if viol > delta + 3 * math.sqrt(delta * (1 - delta) / reps):
        return False, dict(reason="the naive interval misses the mean far more often than delta", frequency=round(viol, 4), expected_about=round(math.exp(-1), 4))
    return True, {}


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
