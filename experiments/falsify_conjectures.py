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
    """Instance for II.4: configurations, weights c, Lipschitz factor kappa, white-box part f,
    kappa-Lipschitz residual g (as arrays over the configurations) and the tolerance eps."""
    if it == 0:
        # Planted tight instance (two binary sites, c = (1, 1), kappa = 1/2, eps = 1/10, tent residual
        # g = -kappa d(00, .)).  A = {00} is a valid eps-certificate and y = 01 has gap 0.45: above the
        # true threshold (1 - kappa) * 1 - eps = 0.4, below the two mutated thresholds 0.6 and 0.9.
        configs = all_configs(2, 2)
        c = np.array([1.0, 1.0])
        kappa, eps = 0.5, 0.1
        g = np.array([-kappa * weighted_hamming(c, configs[0], y) for y in configs])
        f = np.array([0.0, 0.95, 0.95, 2.5])
        return configs, c, kappa, f, g, eps
    n, k = 2, int(rng.integers(2, 4))
    if rng.random() < 0.4:
        n, k = 3, 2
    configs = all_configs(n, k)
    N = len(configs)
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
                low = max(g[a] - weighted_hamming(c, configs[a], configs[y]) for a in A0)
                f[y] = U0 - eps - low + float(rng.uniform(0.0, 0.3)) * float(rng.random() < 0.7)
    return configs, c, kappa, f, g, eps


@conjecture("II.4 Witness-size lower bound: every state with gap < (1-kappa) sigma - eps must be an anchor of every eps-certificate")
def t_witness_lower_bound(rng, trials):
    """Exhaustive form of `anchor_necessary` / `anchor_card_lower_bound` (EnvelopeDuality.lean).

    For E = f + g with g kappa-Lipschitz for the weighted Hamming envelope d (kappa <= 1), a non-empty
    anchor set A is an eps-certificate iff  min_A E - eps <= f(y) + max_{a in A} (g(a) - d(a, y))  for
    ALL y.  The theorem: for every eps-certificate A, every y with
        E(y) - Estar < (1 - kappa) * sigma - eps,    sigma <= d(a, y) for all a in A, a != y,
    belongs to A (Estar any lower bound on E over A).  The test enumerates ALL non-empty subsets A of the
    configuration space, keeps the valid certificates and checks the conclusion for each of them with
      * the sharpest admissible separation sigma_y(A) = min_{a in A, a != y} d(a, y) (per-y form),
      * the uniform separation sigma = min_i c_i (the cardinality bound |A| >= #forced),
      * Estar = global minimum of E and Estar = min_A E (the largest admissible value),
      * the nominal kappa and the exact Lipschitz constant of g (the smallest admissible value).
    Power: the same enumeration must refute two mutated thresholds, (1 - kappa) sigma + eps (sign of
    eps flipped) and sigma - eps (kappa replaced by 0 although the true kappa is positive)."""
    st = dict(instances=0, valid_certificates=0, forced_nonempty=0, forced_nonempty_uniform=0,
              wrong_eps_sign_caught=0, kappa_zero_caught=0)
    tight = tight_u = math.inf
    largest_tight = 0
    masks = {}
    for it in range(max(40, trials)):
        configs, c, kappa, f, g, eps = _witness_instance(rng, it)
        N = len(configs)
        D = np.array([[weighted_hamming(c, x, y) for y in configs] for x in configs])
        E = f + g
        if (g[:, None] - g[None, :] - kappa * D).max() > 1e-9:
            return False, dict(reason="generator produced a residual that is not kappa-Lipschitz")
        off = ~np.eye(N, dtype=bool)
        kappa_eff = max(0.0, float(((g[:, None] - g[None, :])[off] / D[off]).max()))
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
        gap_global = np.broadcast_to(E - E.min(), sigma.shape)           # Estar = global minimum
        gap_anchor = E[None, :] - U[:, None]                             # Estar = min_A E
        cmin = float(c.min())

        def forced_sets(kap, gap, sig, eps_sign=-1.0):
            """forced[A, y]: the hypothesis `gap < (1 - kap) sig - eps` holds (with a safety margin)."""
            if 1.0 - kap > 0.0:
                thr = (1.0 - kap) * sig + eps_sign * eps                 # sig = inf (A = {y}): any sigma works
            else:
                thr = np.full(np.shape(sig), eps_sign * eps)
            return gap < thr - 1e-9

        for kap in (kappa, kappa_eff):
            for gap in (gap_global, gap_anchor):
                for sig, label in ((sigma, "per-y separation"), (cmin, "uniform separation")):
                    bad = valid[:, None] & forced_sets(kap, gap, sig) & ~Mk
                    if bad.any():
                        A, y = (int(v) for v in np.argwhere(bad)[0])
                        sg = float(sigma[A, y]) if label.startswith("per") else cmin
                        return False, dict(reason="forced configuration missing from a valid certificate (" + label + ")",
                                           n_configs=N, c=c.tolist(), kappa=kap, eps=eps, f=f.tolist(), g=g.tolist(),
                                           anchors=[configs[a] for a in range(N) if Mk[A, a]], y=configs[y],
                                           gap=float(gap[A, y]), threshold=(1 - kap) * sg - eps)
        st["instances"] += 1
        nv = int(valid.sum())
        st["valid_certificates"] += nv
        forced = forced_sets(kappa_eff, gap_global, sigma)               # per-y forced sets (subsets of A)
        nf = forced.sum(axis=1)
        sel = valid & (nf > 0)
        st["forced_nonempty"] += int(sel.sum())
        if sel.any():
            tight = min(tight, float((sizes[sel] / nf[sel]).min()))
        nfu = int(forced_sets(kappa_eff, E - E.min(), cmin).sum())       # uniform forced set (same for all A)
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


def _residual_data(rng, n, k, configs, plant=None):
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
        c, anchors, duplicated = _residual_data(rng, n, k, configs, plant=planted[it] if it < len(planted) else None)
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


def lp_bound(n, edges, domains, free_pairs=()):
    """Local-polytope LP lower bound for cost sum_{(i,j) in edges} [x_i == x_j] on restricted domains (binary).

    `free_pairs`: further pairs of sites that carry pairwise marginals at zero cost.  The dual leaf of the
    certificate kernel (`LeafOK`) has messages on EVERY pair of sites; by LP duality its best bound on a
    box is this LP with `free_pairs` = all non-edges (and that equals the LP on the edges alone)."""
    from scipy.optimize import linprog
    # variables: mu_i(a) for a in {0,1}; mu_ij(a,b)
    pairs = list(edges) + list(free_pairs)
    nv = 2 * n + 4 * len(pairs)
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
    for e, (i, j) in enumerate(pairs):
        base = 2 * n + 4 * e
        for a in range(2):
            for b in range(2):
                bounds.append((0, 1))
                if a == b and e < len(edges):
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
    """Per-triangle tables over the 27 domain states of ONE frustrated triangle:
    leaf[state]        best bound of a dual leaf (`LeafOK`) = local-polytope LP on the box;
    prune[state, i, r] dead-end elimination of state r at site i (dominator t = 1 - r) passes `PruneOK`
                       with margin 0 on the box and removes something (site i still has both states)."""
    n, edges, h, J = triangles_tables(1)
    leaf, prune = {}, {}
    for state in itertools.product(range(3), repeat=3):
        leaf[state] = lp_bound(n, edges, _box(state))
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
      leaf    closes the box at cost 1 iff the LP (dual) bound of the box is >= target;
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
    # (0) per-triangle decomposition of the leaf bound and of the dominance check, on random joint boxes
    n_boxes = max(12, trials // 4)
    for b in range(n_boxes):
        nt = 2 + b % 2
        n, edges, h, J = triangles_tables(nt)
        dom = tuple(int(v) for v in rng.choice(3, size=n, p=[0.2, 0.2, 0.6]))
        blocks = [dom[3 * q: 3 * q + 3] for q in range(nt)]
        non_edges = [(i, j) for i in range(n) for j in range(i + 1, n) if (i, j) not in edges]
        lp_edges = lp_bound(n, edges, _box(dom))
        lp_kernel = lp_bound(n, edges, _box(dom), free_pairs=non_edges)
        lp_blocks = sum(leaf[s] for s in blocks)
        if abs(lp_edges - lp_blocks) > 1e-7 or abs(lp_kernel - lp_blocks) > 1e-7:
            return False, dict(reason="leaf bound does not decompose over the triangles", box=dom, lp_edges=lp_edges,
                               lp_all_pairs=lp_kernel, sum_of_blocks=lp_blocks)
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
    # (2) power: with an UNSOUND elimination rule (dominance margin ignored) the search must find fewer leaves
    mutated = {nt: bnb_min_leaves_blocks(nt, nt, True, leaf, prune, unsound_prune=True) for nt in sorted(free)}
    if any(mutated[nt] >= 2 ** nt for nt in mutated):
        return False, dict(reason="powerless: an unsound elimination rule did not reduce the number of leaves", **mutated)
    # (3) with decomposition: one two-leaf certificate per triangle (bound 1 each), 2m leaves in total
    per_triangle = bnb_min_leaves_blocks(1, 1, True, leaf, prune)
    with_sum = {}
    for nt in sorted(free):
        n, edges, h, J = triangles_tables(nt)
        for q in range(nt):
            sub = edges[3 * q: 3 * q + 3]            # sub-instance: triangle q alone (the parts add up to the instance)
            if lp_bound(n, sub, _box((2,) * n)) >= 1 - 1e-7:
                return False, dict(reason="a single leaf certifies a frustrated triangle", m=nt, triangle=q)
            for a in range(2):
                dom = (2,) * (3 * q) + (a,) + (2,) * (n - 3 * q - 1)
                if lp_bound(n, sub, _box(dom)) < 1 - 1e-7:
                    return False, dict(reason="two-leaf certificate of one triangle is rejected", m=nt, triangle=q, state=a)
        with_sum[nt] = nt * per_triangle
        if with_sum[nt] != 2 * nt or (nt >= 3 and with_sum[nt] >= free[nt]):
            return False, dict(reason="decomposed certificate does not have 2m leaves", m=nt, leaves=with_sum[nt])

    def show(d):
        return " ".join(f"m={a}:{b}" for a, b in sorted(d.items()))

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


def _envelope_product(env, lo, hi, beta):
    """prod_i int_{lo_i}^{hi_i} exp(-beta env_i(t)) dt by adaptive 1-D quadrature (scipy quad).
    Returns (product, bound on its relative error from the quadrature error estimates)."""
    from scipy import integrate
    prod, rel = 1.0, 1e-12
    for i, fn in enumerate(env):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", integrate.IntegrationWarning)
            v, e = integrate.quad(lambda t: math.exp(-beta * fn(t)), float(lo[i]), float(hi[i]),
                                  epsabs=0.0, epsrel=1e-12, limit=200)
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
    one-dimensional envelope integrals by adaptive `quad`.  The reference value shares no grid with the
    envelope integrals, so the inequalities are compared up to the quadrature error estimates only (a few
    1e-11 relative) and can fail.  Envelopes: (A) phi_i, psi_i = a_i -+ kappa/d (the coupling is bounded by
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
            if upper > math.exp(beta * float(np.sum(w))) * lower * (1 + rel):
                return False, dict(reason="ratio bound exp(beta * sum w_i) violated", envelope=label, lower=lower,
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
