#!/usr/bin/env python3
"""
MetricChain separation benchmarks: synthetic tightness / scaling comparisons between the bounds
proved in proofs/ and the strongest classical baselines they are compared against in
docs/THEORY_REPORT.md.  Everything here is synthetic (random pairwise chain models, random point
clouds, idealised torsion chains); no biological sequences or experimental data are involved.

Usage:  python3 experiments/separation_benchmarks.py [--quick] [--json PATH]
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import falsify_conjectures as fc  # noqa: E402


def section(title):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


# ----------------------------------------------------------------------------------------------
# B1. Pruning under a non-decomposable residual: global-oscillation DEE vs differential DEE vs
#     the exact contact-set criterion (envelope duality).
# ----------------------------------------------------------------------------------------------

def chain_model(rng, n, k, contact_p=0.3):
    h = rng.normal(0, 1.0, size=(n, k))
    J = np.zeros((n, n, k, k))
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or rng.random() < contact_p:
                J[i, j] = rng.normal(0, 1.0, size=(k, k))
    return h, J


def bench_pruning(rng, quick):
    section("B1. Fraction of (site,state) pairs eliminated when E = E0 + residual, residual in BD(c)")
    n, k = (5, 3) if quick else (6, 3)
    reps = 10 if quick else 40
    configs = fc.all_configs(n, k)
    rows = []
    print("   single-site rules (polynomial time)      |  exact information-theoretic limits (brute force)")
    print(f"{'c':>6} | {'global-osc DEE':>15} | {'differential DEE':>17} | {'energy window (global osc)':>27} | {'contact set (envelope)':>23} | (n={n}, k={k}, {reps} instances)")
    for c_val in (0.05, 0.1, 0.2, 0.4, 0.8):
        tot = np.zeros(4)
        for _ in range(reps):
            h, J = chain_model(rng, n, k)
            c = np.full(n, c_val)
            E0 = {x: fc.energy(h, J, x) for x in configs}
            Emin = min(E0.values())
            domains = [list(range(k)) for _ in range(n)]
            osc = c.sum()  # best global oscillation bound implied by the bounded differences
            pruned = np.zeros(4)
            # exact criterion: state (i,r) is removable iff no configuration with x_i = r is on the contact set
            contact = {x for x in configs if all(E0[x] <= E0[y] + fc.weighted_hamming(c, x, y) + 1e-12 for y in configs)}
            for i in range(n):
                for r in range(k):
                    best = max(fc.goldstein(h, J, i, r, t, domains) for t in range(k) if t != r)
                    pruned[0] += best > osc
                    pruned[1] += best > c[i]
                    # exact limit when only the global oscillation is known: the energy window
                    pruned[2] += min(E0[x] for x in configs if x[i] == r) > Emin + osc
                    pruned[3] += not any(x[i] == r for x in contact)
            tot += pruned / (n * k)
        tot /= reps
        rows.append(dict(c=c_val, global_dee=tot[0], differential_dee=tot[1], window_exact=tot[2], contact_exact=tot[3]))
        print(f"{c_val:6.2f} | {tot[0]:15.3f} | {tot[1]:17.3f} | {tot[2]:27.3f} | {tot[3]:23.3f}")
    return rows


# ----------------------------------------------------------------------------------------------
# B2. Witness-size lower bound vs the smallest anchor certificate (brute force).
# ----------------------------------------------------------------------------------------------

def bench_witness(rng, quick):
    section("B2. Residual evaluations needed for an eps-certificate: lower bound vs brute-force optimum")
    rows = []
    n, k = 3, 2
    configs = fc.all_configs(n, k)
    print(f"{'kappa':>6} {'eps':>6} | {'forced (theorem)':>17} | {'min certificate':>16} | {'all states':>10}")
    for kappa in (0.0, 0.5, 0.9):
        for eps in (0.0, 0.2):
            forced_tot = best_tot = 0.0
            reps = 6 if quick else 20
            for _ in range(reps):
                c = rng.uniform(0.5, 1.0, size=n)
                f = {x: float(rng.normal(0, 0.3)) for x in configs}
                g = fc.random_lipschitz(rng, configs, c, kappa=kappa)
                E = {x: f[x] + g[x] for x in configs}
                Estar = min(E.values())
                forced = sum(E[y] - Estar < (1 - kappa) * c.min() - eps - 1e-12 for y in configs)
                best = None
                for size in range(1, len(configs) + 1):
                    for A in itertools.combinations(configs, size):
                        U = min(E[a] for a in A)
                        LB = min(f[y] + max(g[a] - fc.weighted_hamming(c, a, y) for a in A) for y in configs)
                        if U - LB <= eps + 1e-12:
                            best = size
                            break
                    if best:
                        break
                forced_tot += forced
                best_tot += best
            rows.append(dict(kappa=kappa, eps=eps, forced=forced_tot / reps, optimum=best_tot / reps))
            print(f"{kappa:6.2f} {eps:6.2f} | {forced_tot / reps:17.2f} | {best_tot / reps:16.2f} | {len(configs):10d}")
    return rows


# ----------------------------------------------------------------------------------------------
# B3. Spectral realizability obstruction: classical strain bound vs trace-enhanced bound vs optimum.
# ----------------------------------------------------------------------------------------------

def bench_spectral(rng, quick):
    section("B3. Lower bounds on min_X ||Dhat - Delta(X)||_F (3-D realization error of predicted squared distances)")
    rows = []
    print(f"{'L':>4} {'model':>14} | {'strain bound':>12} | {'trace bound':>12} | {'best found':>11} | {'trace/strain':>12} | {'opt/trace':>9}")
    Ls = (8, 16, 32) if quick else (8, 16, 32, 64)
    for L in Ls:
        for model in ("uniform bias", "gaussian noise", "scale error"):
            X0 = rng.normal(size=(L, 3)) * 2.0
            D0 = fc.sqdist(X0)
            if model == "uniform bias":
                Dhat = D0 + 1.0 * (np.ones((L, L)) - np.eye(L))
            elif model == "gaussian noise":
                N = rng.normal(0, 0.5, size=(L, L))
                Dhat = D0 + (N + N.T) / 2
            else:
                Y = np.c_[X0, rng.normal(size=(L, 1)) * 0.7]  # a hidden 4th dimension
                Dhat = fc.sqdist(Y)
            np.fill_diagonal(Dhat, 0.0)
            lb, strain = fc.trace_bound_sq(Dhat, 3)
            best = fc.sstress_min(Dhat, 3, rng, restarts=2 if quick else 4)
            rows.append(dict(L=L, model=model, strain=math.sqrt(strain), trace=math.sqrt(lb), best=math.sqrt(best)))
            print(f"{L:4d} {model:>14} | {math.sqrt(strain):12.3f} | {math.sqrt(lb):12.3f} | {math.sqrt(best):11.3f} | "
                  f"{math.sqrt(lb / strain):12.2f} | {math.sqrt(best / lb):9.3f}")
    return rows


# ----------------------------------------------------------------------------------------------
# B4. Free-energy sandwich widths.
# ----------------------------------------------------------------------------------------------

def rio_l(t):
    """Rio's exact extremal function l(t) = sup_r [log(1 + r(e^t - 1)) - t r]  (<= t^2/8)."""
    if t < 1e-8:
        return t * t / 8
    return (t - math.log(t) - 1) + t / math.expm1(t) + math.log(-math.expm1(-t))


def bench_sandwich(rng, quick):
    section("B4. Certified width of ln(Z/Z0) + beta<Delta>_0 for a residual with bounded differences c (product reference)")
    rows = []
    n, k = 6, 2
    ps, configs, w = fc.product_space(rng, n, k)
    print(f"{'beta*c':>7} | {'trivial b*osc':>13} | {'Hoeffding':>10} | {'McDiarmid':>10} | {'Rio (exact sup)':>15} | {'worst additive':>14} | {'random BD':>10}")
    for bc in (0.1, 0.3, 1.0, 3.0, 10.0):
        c = np.full(n, bc)
        osc = c.sum()
        trivial = osc
        hoeff = osc ** 2 / 8
        mcd = float(np.sum(c ** 2)) / 8
        rio = sum(rio_l(ci) for ci in c)
        worst_add = sum(fc.best_subset_phi(ps[i], c[i]) for i in range(n))
        vals = []
        for _ in range(5 if quick else 20):
            g = fc.random_lipschitz(rng, configs, c)
            mean = sum(w[x] * g[x] for x in configs)
            vals.append(math.log(sum(w[x] * math.exp(-(g[x] - mean)) for x in configs)))
        rows.append(dict(beta_c=bc, trivial=trivial, hoeffding=hoeff, mcdiarmid=mcd, rio=rio, additive=worst_add, random=max(vals)))
        print(f"{bc:7.2f} | {trivial:13.3f} | {hoeff:10.3f} | {mcd:10.3f} | {rio:15.3f} | {worst_add:14.3f} | {max(vals):10.3f}")
    return rows


# ----------------------------------------------------------------------------------------------
# B5. Certificate sizes on disjoint frustrated triangles: tree-like vs additive.
# ----------------------------------------------------------------------------------------------

def bench_certificate_size(rng, quick):
    section("B5. Leaves needed to certify the optimum of m disjoint frustrated triangles")
    rows = []
    print(f"{'m':>3} | {'sum-free (brute force minimum)':>31} | {'theorem 2^m':>11} | {'with sum rule (2m)':>18}")
    for m in (1, 2):
        n, edges = fc.triangles_instance(m)
        memo = {}

        def min_leaves(dom):
            if dom in memo:
                return memo[dom]
            domains = [((0, 1) if d == 2 else (d,)) for d in dom]
            if fc.lp_bound(n, edges, domains) >= m - 1e-7:
                memo[dom] = 1
                return 1
            best = math.inf
            for i in range(n):
                if dom[i] == 2:
                    best = min(best, min_leaves(dom[:i] + (0,) + dom[i + 1:]) + min_leaves(dom[:i] + (1,) + dom[i + 1:]))
            memo[dom] = best
            return best

        leaves = min_leaves(tuple([2] * n))
        rows.append(dict(m=m, sum_free=leaves, bound=2 ** m, with_sum=2 * m))
        print(f"{m:3d} | {leaves:31d} | {2 ** m:11d} | {2 * m:18d}")
    for m in (4, 8, 16, 32):
        print(f"{m:3d} | {'(>= 2^m by theorem)':>31} | {2 ** m:11d} | {2 * m:18d}")
        rows.append(dict(m=m, sum_free=None, bound=2 ** m, with_sum=2 * m))
    return rows


# ----------------------------------------------------------------------------------------------
# B6. Thermal dead-end elimination: certified vs actual change of ln Z.
# ----------------------------------------------------------------------------------------------

def bench_thermal(rng, quick):
    section("B6. Thermal DEE: actual vs certified change of ln Z after pruning every state with Goldstein margin > gamma_min")
    rows = []
    n, k = (5, 3) if quick else (6, 3)
    print(f"{'beta':>5} {'gamma_min':>9} | {'pruned frac':>11} | {'actual dlnZ':>12} | {'certified dlnZ':>14} | {'energy-window count bound':>26}")
    for beta in (0.5, 1.0, 2.0, 4.0):
        for gmin in (0.5, 1.5):
            acc = np.zeros(4)
            reps = 5 if quick else 15
            for _ in range(reps):
                h, J = chain_model(rng, n, k)
                configs = fc.all_configs(n, k)
                E = {x: fc.energy(h, J, x) for x in configs}
                domains = [list(range(k)) for _ in range(n)]
                cert = 0.0
                npruned = 0
                changed = True
                while changed:
                    changed = False
                    for i in range(n):
                        for r in list(domains[i]):
                            cands = [(fc.goldstein(h, J, i, r, t, domains), t) for t in domains[i] if t != r]
                            if not cands:
                                continue
                            g, t = max(cands)
                            if g > gmin:
                                domains[i].remove(r)
                                cert += math.log1p(math.exp(-beta * g))
                                npruned += 1
                                changed = True
                Zfull = sum(math.exp(-beta * e) for e in E.values())
                Zpr = sum(math.exp(-beta * E[x]) for x in configs if all(x[i] in domains[i] for i in range(n)))
                Emin = min(E.values())
                # classical additive energy-window bound: every pruned conformation is >= gmin above the optimum
                n_removed = len(configs) - int(np.prod([len(d) for d in domains]))
                window = math.log1p(n_removed * math.exp(-beta * (Emin + gmin)) / Zpr)
                acc += np.array([npruned / (n * k), math.log(Zfull / Zpr), cert, window])
            acc /= reps
            rows.append(dict(beta=beta, gamma_min=gmin, pruned=acc[0], actual=acc[1], certified=acc[2], window=acc[3]))
            print(f"{beta:5.1f} {gmin:9.1f} | {acc[0]:11.3f} | {acc[1]:12.2e} | {acc[2]:14.2e} | {acc[3]:26.2e}")
    return rows


# ----------------------------------------------------------------------------------------------
# B7. Torsion-error to RMSD propagation.
# ----------------------------------------------------------------------------------------------

def bench_torsion(rng, quick):
    section("B7. Kabsch RMSD after i.i.d. torsion errors of size eps: actual vs reduced-inertia chain bound vs naive lever bound")
    rows = []
    print(f"{'torsions':>8} {'eps(rad)':>8} | {'actual RMSD':>11} | {'reduced-inertia bound':>21} | {'naive lever-arm bound':>21}")
    for m in ((8, 32) if quick else (8, 32, 96)):
        for eps in (0.02, 0.1):
            a = b = c = 0.0
            reps = 4 if quick else 10
            for _ in range(reps):
                theta = rng.uniform(-math.pi, math.pi, size=m)
                delta = rng.normal(0, eps, size=m)
                X = fc.build_chain(theta)
                N = X.shape[0]
                cur = theta.copy()
                total = 0.0
                naive = 0.0
                for kk in range(m):
                    Xc = fc.build_chain(cur)
                    p, q = Xc[kk + 1], Xc[kk + 2]
                    axis = (q - p) / np.linalg.norm(q - p)

                    def inertia(P):
                        v = P - p
                        perp = v - np.outer(v @ axis, axis)
                        return float(np.sum(perp ** 2))

                    IA, IB = inertia(Xc[: kk + 3]), inertia(Xc[kk + 3:])
                    total += math.sqrt(fc.coaxial_cost(IA, IB, delta[kk]))
                    naive += 2 * abs(math.sin(delta[kk] / 2)) * math.sqrt(IB)  # rotate the distal part, no superposition
                    cur[kk] += delta[kk]
                true = math.sqrt(fc.kabsch(X, fc.build_chain(theta + delta)) / N)
                a += true
                b += total / math.sqrt(N)
                c += naive / math.sqrt(N)
            rows.append(dict(torsions=m, eps=eps, actual=a / reps, reduced=b / reps, naive=c / reps))
            print(f"{m:8d} {eps:8.2f} | {a / reps:11.4f} | {b / reps:21.4f} | {c / reps:21.4f}")
    return rows


# ----------------------------------------------------------------------------------------------
# B8. Certificate complexity on product landscapes: exact layer counts against the predicted exponent
#     R* = max_x [ln(1+x) - ln(1+x^(1/rho))]  (two-state sites, excitation e, envelope c, rho = e/c, zero residual);
#     and the finite-temperature exponent R_beta against the Gibbs entropy.
# ----------------------------------------------------------------------------------------------
def binary_rstar(rho):
    return max(math.log1p(x) - math.log1p(x ** (1.0 / rho)) for x in np.linspace(1e-6, 1.0, 200001))


def layer_exponent(n, rho):
    """(1/n) ln max_mu L_mu with L_mu = min_nu C(n,mu) / |S_nu cap layer mu| (exact integers).
    max_mu L_mu <= N_frac <= (n+1) max_mu L_mu, and N_cov <= (1 + n ln 2) N_frac."""
    from fractions import Fraction
    from math import comb
    best_log = -1.0
    for mu in range(n + 1):
        r = math.floor(rho * mu + 1e-12)
        frac = Fraction(0)
        for nu in range(max(0, mu - r), min(n, mu + r) + 1):
            cnt = 0
            for j in range(0, min(mu, r) + 1):
                l = nu - mu + j
                if 0 <= l <= n - mu and j + l <= r:
                    cnt += comb(mu, j) * comb(n - mu, l)
            frac = max(frac, Fraction(cnt, comb(n, nu)))
        best_log = max(best_log, math.log(frac.denominator) - math.log(frac.numerator))
    return best_log / n


def thermal_rate(e, c, beta, rng):
    """R_beta = max_{t, v} ((beta+t)/beta) ln sum_s pi^{t/(beta+t)} v^{beta/(beta+t)} - ln max_a sum_s v e^{-t s(a,s)}."""
    from scipy.optimize import minimize
    pi = np.exp(-beta * np.array([0.0, e]))
    pi /= pi.sum()
    slack = np.array([[0.0, c], [c, 0.0]])

    def neg(params):
        t = params[0] ** 2
        v = np.array([1.0, math.exp(params[1])])
        p = beta / (beta + t)
        return -(math.log(float(np.sum(pi ** (1 - p) * v ** p))) / p - math.log(float(np.max(np.exp(-t * slack) @ v))))

    best = 0.0
    for _ in range(40):
        res = minimize(neg, [rng.uniform(0, 4), rng.normal(0, 2)], method="Nelder-Mead",
                       options=dict(xatol=1e-10, fatol=1e-13, maxiter=20000))
        best = max(best, -res.fun)
    return best, float(-np.sum(pi * np.log(pi)))


def bench_exponent(rng, quick):
    section("B8. Certificate complexity exponent on product landscapes (exact layer counts) and at finite temperature")
    ns = (25, 50, 100) if quick else (25, 50, 100, 200, 400)
    rows = []
    print(f"{'rho=e/c':>8} | {'R* (predicted)':>14} | " + " | ".join(f"n={n:<4d}" for n in ns) + "   [(1/n) ln max_mu L_mu]")
    for rho in (0.25, 0.5, 0.75):
        R = binary_rstar(rho)
        vals = [layer_exponent(n, rho) for n in ns]
        rows.append(dict(rho=rho, Rstar=R, ns=list(ns), layer=vals))
        print(f"{rho:8.2f} | {R:14.4f} | " + " | ".join(f"{v:6.4f}" for v in vals))
    print("\nfinite temperature, e/c = 1/2 (zero-temperature exponent R* = %.4f):" % binary_rstar(0.5))
    print(f"{'beta*c':>8} | {'entropy H(pi)':>13} | {'R_beta':>8}")
    for beta in (0.5, 1.0, 4.0, 40.0):
        Rb, H = thermal_rate(0.5, 1.0, beta, rng)
        rows.append(dict(beta=beta, entropy=H, R_beta=Rb))
        print(f"{beta:8.1f} | {H:13.4f} | {Rb:8.4f}")
    print("sharp site (e/c = 2: one evaluation certifies the ground state), beta*c = ln 2:")
    Rb, H = thermal_rate(2.0, 1.0, math.log(2.0), rng)
    rows.append(dict(beta=math.log(2.0), entropy=H, R_beta=Rb, sharp=True))
    print(f"{math.log(2.0):8.3f} | {H:13.4f} | {Rb:8.4f}   (verified one-shot bound: ln(6/5) = {math.log(1.2):.4f})")
    return rows


# ----------------------------------------------------------------------------------------------
# B9. Best-first search against the smallest certificate and against covers at shrunk radii.
# ----------------------------------------------------------------------------------------------
def bench_best_first(rng, quick):
    section("B9. Best-first search: evaluations vs minimal cover N_cov(eps) vs shrunk cover (theta, eps/6)")
    reps = 60 if quick else 400
    rows = []
    print(f"{'kappa':>6} | {'mean evals':>10} | {'mean N_cov':>10} | {'mean shrunk+1':>13} | {'evals > N_cov+1':>15} | {'max evals/N_cov':>15}")
    for kappa in (0.0, 0.2, 0.5, 0.8):
        ev = nc = sh = 0.0
        exceed, worst = 0, 0.0
        for _ in range(reps):
            n = int(rng.integers(6, 12))
            d = fc.cg_metric(rng, n)
            g = fc.cg_lipschitz(rng, d, kappa)
            f = rng.normal(0, 1.0, size=n)
            E = f + g
            gap = E - E.min()
            s = fc.cg_slack(d, g)
            eps = 0.2
            m = len(fc.cg_best_first(d, f, g, eps, int(rng.integers(n))))
            ncov = fc.cg_min_cover(s <= gap[None, :] + eps + 1e-12)
            theta = (1 - kappa) / (4 * (1 + kappa))
            nshr = fc.cg_min_cover(s <= theta * (gap[None, :] + eps / 6) + 1e-12)
            assert m <= nshr + 1
            ev += m
            nc += ncov
            sh += nshr + 1
            exceed += m > ncov + 1
            worst = max(worst, m / ncov)
        rows.append(dict(kappa=kappa, evals=ev / reps, ncov=nc / reps, shrunk=sh / reps, exceed=exceed / reps, worst=worst))
        print(f"{kappa:6.1f} | {ev / reps:10.2f} | {nc / reps:10.2f} | {sh / reps:13.2f} | {exceed / reps:15.3f} | {worst:15.2f}")
    for leaves in (4, 8, 16):
        n = leaves + 2
        d = np.full((n, n), 2.0)
        d[0, :] = d[:, 0] = 10.0
        d[1, 2:] = d[2:, 1] = 1.0
        np.fill_diagonal(d, 0.0)
        f = np.full(n, 1.5)
        f[0], f[1] = 0.0, 100.0
        g = np.zeros(n)
        m = len(fc.cg_best_first(d, f, g, 0.1, 0))
        ncov = fc.cg_min_cover(fc.cg_slack(d, g) <= (f - f.min())[None, :] + 0.1 + 1e-12) if n <= 12 else 2
        rows.append(dict(hub_leaves=leaves, evals=m, ncov=ncov))
        print(f"hub instance with {leaves:2d} leaves: best-first evaluates {m:2d} points, the smallest certificate has {ncov}")
    return rows


# ----------------------------------------------------------------------------------------------
# B10. Query complexity of every algorithm.  Three single-letter exponents for one site — zero temperature (R*, all
#      algorithms), finite temperature deterministic (R_beta, certificates), finite temperature randomised (lower
#      bound R^rand_beta, distortion budget = soft gap) — and the accuracy threshold on the uniform cube.
# ----------------------------------------------------------------------------------------------
def lp_rate(rho, t):
    """max over weights v >= 0 of ln(sum v) subject to sum_s v(s) exp(-t rho(a, s)) <= 1 for every a."""
    from scipy.optimize import linprog
    A = np.exp(-t * np.asarray(rho, dtype=float))
    col = A.max(axis=0)
    res = linprog(-1.0 / col, A_ub=A / col, b_ub=np.ones(len(A)), bounds=(0, None), method="highs")
    if res.status != 0 or -res.fun <= 0:
        return float("-inf")
    return math.log(-res.fun)


def randomized_rate(e, c, beta, eps1=0.0, grid=801):
    """R^rand_beta(eps1) = max_t max_v [ln sum v - ln max_a sum_s v(s) exp(-t (s(a,s) - (lam(s) + eps1)/beta))],
    lam(s) = -ln sum_a pi(a) exp(-beta s(a, s)) the soft gap of the letter s; and the critical accuracy per site
    eps1_crit = max_P min_a E_P[beta s(a, .) - lam] (value of a zero-sum game)."""
    from scipy.optimize import linprog
    E = np.array([0.0, e])
    pi = np.exp(-beta * E)
    pi /= pi.sum()
    slack = np.array([[0.0, c], [c, 0.0]])
    lam = -np.log(np.exp(-beta * slack).T @ pi)
    rate = max(0.0, max(lp_rate(slack - ((lam + eps1) / beta)[None, :], t) for t in np.linspace(0.0, 40.0, grid)))
    M = beta * slack - lam[None, :]
    res = linprog([0, 0, -1], A_ub=np.hstack([-M, np.ones((2, 1))]), b_ub=np.zeros(2), A_eq=[[1, 1, 0]], b_eq=[1],
                  bounds=[(0, None), (0, None), (None, None)], method="highs")
    upper = math.log(float(np.sum(pi * np.exp(lam))))          # U_beta = ln E_pi e^{Lambda}: soft-gap sampling
    return rate, float(-res.fun), upper


def cube_hitting_exponent(n, u, eps):
    """(1/n) ln (2^n / |B(r*)|), r* the least radius whose Hamming ball supports a perturbation of ln Z by more
    than eps on the uniform cube (c-Lipschitz class, u = beta c): the randomised query complexity at g = 0 up to
    factors polynomial in n (Harper's isoperimetric theorem)."""
    logc = [math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) for k in range(n + 1)]

    def logsum(terms):
        m = max(terms)
        return m + math.log(sum(math.exp(x - m) for x in terms))

    def effect(r):
        return logsum([logc[k] + (u * (r + 1 - k) if k <= r else 0.0) for k in range(n + 1)]) - n * math.log(2)

    lo, hi = -1, n
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if effect(mid) > eps:
            hi = mid
        else:
            lo = mid
    return (n * math.log(2) - logsum(logc[: hi + 1])) / n


def cube_regime_exponent(n, u, log_excess):
    """(1/n) ln (2^n / |B(k*)|), k* the least radius such that the dip supported on the Hamming ball B(k) has excess
    E[e^{u (k+1-H)_+} - 1] > exp(log_excess) (uniform cube; H the distance to the centre).  Exact, in the log domain,
    so that exponentially small accuracies eps = e^{-lambda n} (log_excess = -lambda n) can be used."""
    logc = [math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) for k in range(n + 1)]

    def logsum(terms):
        m = max(terms)
        return m + math.log(sum(math.exp(x - m) for x in terms))

    def log_expm1(z):
        return z + math.log1p(-math.exp(-z)) if z > 30.0 else math.log(math.expm1(z))

    def log_excess_of(k):
        return logsum([logc[j] + log_expm1(u * (k + 1 - j)) for j in range(k + 1)]) - n * math.log(2)

    lo, hi = -1, n
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if log_excess_of(mid) > log_excess:
            hi = mid
        else:
            lo = mid
    return (n * math.log(2) - logsum(logc[: hi + 1])) / n


def cube_regime_prediction(u, lam):
    """Exponent of the randomised cost at the zero residual for accuracy eps = e^{-lam n} (lam = 0: eps of order one):
    ln 2 - h((Lambda1 - lam)/u) for lam <= lam_c = ln 2 - h(1/(1+e^u)), and min(lam, ln 2) beyond."""
    hb = lambda x: 0.0 if x <= 0 or x >= 1 else -x * math.log(x) - (1 - x) * math.log(1 - x)
    lam1 = math.log(2.0 / (1.0 + math.exp(-u)))
    lam_c = math.log(2) - hb(1.0 / (1.0 + math.exp(u)))
    return (math.log(2) - hb((lam1 - lam) / u)) if lam <= lam_c else min(lam, math.log(2))


def cube_dip_tables(n, u):
    """(logex, logball) for the uniform n-cube at the zero residual: logex[k] = ln(e^{Delta_k} - 1), Delta_k the effect
    on ln Z of the dip of depth c(k+1) (supported on the Hamming ball B(k)); logball[k] = ln |B(k)|."""
    logc = [math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) for k in range(n + 1)]

    def logsum(terms):
        m = max(terms)
        return m + math.log(sum(math.exp(x - m) for x in terms))

    def log_expm1(z):
        return z + math.log1p(-math.exp(-z)) if z > 30.0 else math.log(math.expm1(z))

    logex, logball, acc = [], [], None
    for k in range(n + 1):
        logex.append(logsum([logc[j] + log_expm1(u * (k + 1 - j)) for j in range(k + 1)]) - n * math.log(2))
        acc = logc[k] if acc is None else logsum([acc, logc[k]])
        logball.append(acc)
    return logex, logball


def cube_bracket(n, tables, eps, eta, log_eps=None):
    """(ln LB, ln UB) of Theorem 11.25(c) without the factors (1 - 2 delta) and ln(1/delta): LB = 2^n / |B(k*(eps))|,
    UB = min(2^n, max(2^n / |B(k*(eps - eta) - 1)|, 1 / (1 - e^{-eta}))); eta = eps/2 is the unhedged spot-check.
    For accuracies too small for floating point pass log_eps = ln(eps) (then eta = eps/2 is used)."""
    logex, logball = tables
    lt = lambda z: math.log(z) if z < 1e-8 else math.log(math.expm1(z))
    if log_eps is not None:
        target_lb, target_ub, log_inv_p = log_eps, log_eps - math.log(2), -(log_eps - math.log(2))
    else:
        target_lb, target_ub, log_inv_p = lt(eps), lt(eps - eta), -math.log(-math.expm1(-eta))

    def kstar(target):
        lo, hi = -1, n + 1                                 # logex is increasing; k* in 0..n+1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if mid <= n and logex[mid] > target:
                hi = mid
            else:
                lo = mid
        return hi

    k2, k1 = kstar(target_lb), kstar(target_ub) - 1
    log_lb = n * math.log(2) - logball[min(k2, n)]
    log_ub = min(n * math.log(2), max(n * math.log(2) - (logball[min(k1, n)] if k1 >= 0 else 0.0), log_inv_p))
    return log_lb, log_ub


def site_threshold(e, c, beta, gamma, grid=20001):
    """(eps1_crit, W1) for a two-state site with known part (0, e), envelope constant c and additive residual (0, gamma):
    eps1_crit = max_P min_a E_P[beta s(a, .) - Lambda_1] (vanishing point of the randomised lower bound) and
    W1 = largest Jensen gap ln E_pi exp(-beta (h - E_pi h)) over admissible changes h of the residual."""
    w1 = math.exp(-beta * (e + gamma))
    pi0, pi1 = 1.0 / (1.0 + w1), w1 / (1.0 + w1)
    s01, s10 = c + gamma, c - gamma                        # s(0,1), s(1,0)
    lam0 = -math.log(pi0 + pi1 * math.exp(-beta * s10))
    lam1 = -math.log(pi1 + pi0 * math.exp(-beta * s01))
    q = np.linspace(0.0, 1.0, grid)
    crit = float(np.max(np.minimum(beta * q * s01, beta * (1 - q) * s10) - (1 - q) * lam0 - q * lam1))
    jensen = lambda t: math.log(pi0 * math.exp(beta * pi1 * t) + pi1 * math.exp(-beta * pi0 * t))   # h(1) - h(0) = t
    return crit, max(jensen(c - gamma), jensen(-c - gamma))


def bench_query_complexity(rng, quick):
    section("B10. Query complexity of every algorithm: three exponents for one site, and the threshold on the cube")
    rows = []
    grid = 401 if quick else 801
    for e in (0.5, 2.0):
        print(f"two-state site, excitation e = {e}, envelope constant c = 1, zero residual; "
              f"zero-temperature exponent R* = {binary_rstar(e) if e < 1 else 0.0:.4f}")
        print(f"{'beta':>6} | {'H(pi)':>7} | {'R_beta (deterministic)':>22} | {'R^rand_beta (randomised, >=)':>28} | "
              f"{'U_beta (randomised, <=)':>23} | {'eps1_crit':>9}")
        for beta in ((0.5, 1.0, 4.0, 40.0) if quick else (0.25, 0.5, 1.0, 2.0, 4.0, 10.0, 40.0)):
            Rb, H = thermal_rate(e, 1.0, beta, rng)
            Rr, crit, U = randomized_rate(e, 1.0, beta, grid=grid)
            rows.append(dict(e=e, beta=beta, entropy=H, R_beta=Rb, R_rand=Rr, U_beta=U, eps1_crit=crit))
            print(f"{beta:6.2f} | {H:7.4f} | {Rb:22.4f} | {Rr:28.4f} | {U:23.4f} | {crit:9.4f}")
            if Rr > min(Rb, U) + 1e-3:
                raise RuntimeError("randomised lower bound exceeds an upper bound")
            pex = math.exp(-beta * e) / (1.0 + math.exp(-beta * e))
            closed = 0.5 * math.log(1.0 + 2.0 * pex * (1.0 - pex) * (math.cosh(beta) - 1.0))
            if abs(crit - closed) > 1e-6 * max(1.0, closed):
                raise RuntimeError("critical accuracy differs from 0.5 ln(1 + 2p(1-p)(cosh(beta c) - 1))")
    print("\nuniform cube (e = 0; the deterministic exponent is ln 2 = 0.6931 for every beta):")
    print(f"{'u=beta*c':>8} | {'ln2 - h(rho0)':>13} | {'LP value':>9} | {'U = ln(2/(1+e^-u))':>18} | {'threshold ln cosh(u/2)':>22} | {'game value':>10} | "
          + " | ".join(f"n={n}" for n in ((100, 400) if quick else (100, 400, 1600))) + "   [(1/n) ln(2^n/|B(r*)|), eps = 0.5]")
    hb = lambda x: -x * math.log(x) - (1 - x) * math.log(1 - x)
    for u in (0.5, 1.0, 2.0, math.log(16.0)):
        rho0 = math.log(2.0 / (1.0 + math.exp(-u))) / u
        Rr, crit, U = randomized_rate(0.0, 1.0, u, grid=grid)
        vals = [cube_hitting_exponent(n, u, 0.5) for n in ((100, 400) if quick else (100, 400, 1600))]
        rows.append(dict(u=u, closed_form=math.log(2) - hb(rho0), lp=Rr, upper=U, threshold=math.log(math.cosh(u / 2)),
                         game=crit, finite_n=vals))
        print(f"{u:8.3f} | {math.log(2) - hb(rho0):13.5f} | {Rr:9.5f} | {U:18.5f} | {math.log(math.cosh(u / 2)):22.5f} | {crit:10.5f} | "
              + " | ".join(f"{v:.5f}" for v in vals))
    print("\naccuracy regimes on the cube at the zero residual, u = 1 (exact ball counts against the predicted exponent;")
    print("eps = e^{-lambda n}; for exponentially small accuracies the soft-gap exponent ln2 - h(rho0) = 0.0291 is NOT attained):")
    nn = 800 if quick else 3200
    print(f"{'lambda':>7} | {'predicted':>9} | n={nn}")
    for lam in (0.0, 0.02, 0.05, 0.1, 0.3, 0.6, 0.8):
        log_excess = math.log(math.expm1(0.5)) if lam == 0.0 else -lam * nn
        val = cube_regime_exponent(nn, 1.0, log_excess)
        pred = cube_regime_prediction(1.0, lam)
        rows.append(dict(lam=lam, predicted=pred, n=nn, exact=val))
        print(f"{lam:7.2f} | {pred:9.4f} | {val:.4f}")
        if abs(val - pred) > (0.03 if quick else 0.012):
            raise RuntimeError("cube accuracy-regime exponent differs from the prediction")
    hb0 = lambda x: 0.0 if x <= 0 or x >= 1 else -x * math.log(x) - (1 - x) * math.log(1 - x)
    lam1 = math.log(2.0 / (1.0 + math.exp(-1.0)))
    tables = {n: cube_dip_tables(n, 1.0) for n in ((200, 800) if quick else (200, 800, 3200))}
    print(f"\nextensive accuracies eps = n eps1, u = 1 (threshold ln cosh(1/2) = {math.log(math.cosh(0.5)):.4f}); "
          f"exponent of the lower bound against ln2 - h((Lambda1 + eps1)/u):")
    print(f"{'eps1':>6} | {'predicted':>9} | n={nn}")
    tb = cube_dip_tables(nn, 1.0)
    for eps1 in (0.02, 0.048, 0.08, 0.11):
        lb, _ = cube_bracket(nn, tb, nn * eps1, 1.0)
        pred = math.log(2) - hb0(lam1 + eps1)
        rows.append(dict(eps1=eps1, predicted=pred, n=nn, exact=lb / nn))
        print(f"{eps1:6.3f} | {pred:9.4f} | {lb / nn:.4f}")
        if abs(lb / nn - pred) > (0.03 if quick else 0.012):
            raise RuntimeError("extensive-accuracy exponent differs from the prediction")
    print("\nupper bound / lower bound at the zero residual, u = 1: ln UB - ln LB (without ln(1/delta) and 1 - 2 delta)")
    print("  unhedged spot-check (must detect at level eps/2)  |  hedged spot-check (output ln Z(0) + eps/2 - 1)")
    cols = [("eps=2", lambda n: 2.0), ("ln n", lambda n: math.log(n)), ("sqrt n", lambda n: math.sqrt(n)),
            ("0.02n", lambda n: 0.02 * n), ("0.06n", lambda n: 0.06 * n), ("0.10n", lambda n: 0.10 * n)]
    print(f"{'n':>6} | " + " ".join(f"{name:>7}" for name, _ in cols) + "  |  " + " ".join(f"{name:>7}" for name, _ in cols))
    for n, tb in tables.items():
        un, he = [], []
        for name, fn in cols:
            eps = fn(n)
            lb, ub = cube_bracket(n, tb, eps, eps / 2)
            lb2, ub2 = cube_bracket(n, tb, eps, 1.0)
            un.append(ub - lb)
            he.append(ub2 - lb2)
        rows.append(dict(n=n, unhedged=un, hedged=he))
        print(f"{n:6d} | " + " ".join(f"{v:7.1f}" for v in un) + "  |  " + " ".join(f"{v:7.1f}" for v in he))
        if max(he) > 2.5 or min(un + he) < -1e-9:
            raise RuntimeError("hedged bracket on the cube does not close within the expected constant")
    print("\nwhole accuracy range, eta = min(1, eps/2): largest ln UB - ln LB over eps from e^{-0.69 n} to the threshold")
    for n, tb in tables.items():
        top = n * math.log(math.cosh(0.5))
        gaps = []
        for lam in np.linspace(0.69, 0.02, 60):            # eps = e^{-lam n}, in the log domain
            lb, ub = cube_bracket(n, tb, None, None, log_eps=-float(lam) * n)
            gaps.append(ub - lb)
        for eps in np.linspace(0.05, 0.999 * top, 60):
            lb, ub = cube_bracket(n, tb, float(eps), min(1.0, float(eps) / 2))
            gaps.append(ub - lb)
        rows.append(dict(n=n, max_log_gap=max(gaps)))
        print(f"   n = {n:5d}:  max = {max(gaps):.2f}   (ln(n+1) = {math.log(n + 1):.2f})")
        if max(gaps) > 2 * math.log(n + 1) + 2.5 or min(gaps) < -1e-9:
            raise RuntimeError("bracket of Theorem 11.25(c) does not close up to a polynomial factor")
    print("\nthreshold of the randomised lower bound at additive instances (site e/c = 1/2, beta = 1; residual difference gamma):")
    print(f"{'gamma':>7} | {'eps1_crit(gamma)':>16} | {'Jensen width W1(gamma)':>22}")
    best = (-1.0, 0.0)
    for gamma in np.linspace(-0.99, 0.99, 199 if quick else 1981):
        crit, w1 = site_threshold(0.5, 1.0, 1.0, float(gamma))
        if crit > w1 + 1e-6:
            raise RuntimeError("eps1_crit exceeds the Jensen width of the sandwich")
        best = max(best, (crit, float(gamma)))
    for gamma in (-0.9, -0.5, best[1], 0.0, 0.5, 0.9):
        crit, w1 = site_threshold(0.5, 1.0, 1.0, gamma)
        rows.append(dict(gamma=gamma, eps1_crit=crit, W1=w1))
        print(f"{gamma:7.3f} | {crit:16.5f} | {w1:22.5f}" + ("   <- largest eps1_crit" if gamma == best[1] else ""))
    crit0, _ = site_threshold(0.5, 1.0, 1.0, 0.0)
    if not (abs(crit0 - 0.11367) < 2e-4 and crit0 < best[0] < crit0 + 1e-3):
        raise RuntimeError("instance dependence of eps1_crit is not as documented")
    return rows


def game_value(K):
    """min over mixed columns of max over rows of sum_j M_j K[a, j] (matrix game, LP)."""
    from scipy.optimize import linprog
    na, nj = K.shape
    res = linprog(np.r_[np.zeros(nj), 1.0], A_ub=np.c_[K, -np.ones(na)], b_ub=np.zeros(na),
                  A_eq=[np.r_[np.ones(nj), 0.0]], b_eq=[1.0], bounds=[(0, None)] * nj + [(None, None)], method="highs")
    if res.status != 0:
        raise RuntimeError("game LP failed")
    return float(res.fun)


def site_exponent(pi, cols, beta, eps1=0.0, grid=401):
    """Single-letter lower bound max_{0 <= t <= 1.5 beta} [-ln val(K_t) - t eps1/beta], K_t[a, phi] = exp(-t (phi[a] - Lambda(phi)/beta)),
    for the family `cols` of slack-Lipschitz site functions (theory report Theorem 11.27)."""
    lam = [-math.log(float(np.sum(pi * np.exp(-beta * phi)))) for phi in cols]
    sig = np.array([phi - l / beta for phi, l in zip(cols, lam)]).T
    best = 0.0
    for t in np.linspace(0.0, 1.5 * beta, grid)[1:]:
        best = max(best, -math.log(game_value(np.exp(-t * sig))) - t * eps1 / beta)
    return best


def site_game_threshold(pi, cols, beta):
    """min_Q max_phi [beta E_Q phi - Lambda(phi)] over the site functions `cols` (theory report Theorem 11.28)."""
    M = np.array([[beta * phi[a] + math.log(float(np.sum(pi * np.exp(-beta * phi)))) for a in range(len(pi))] for phi in cols])
    return game_value(M)                                  # rows: site functions (maximiser); columns: letters (mixed by Q)


def hamming_vertices(k, c=1.0):
    """Vertices of the Lipschitz polytope of c * (uniform metric) on k points: c * 1[a not in B], B a proper nonempty subset."""
    return [c * np.array([0.0 if a in B else 1.0 for a in range(k)]) for r in range(1, k) for B in itertools.combinations(range(k), r)]


def class_threshold(f1, beta, c=1.0):
    """(eps*, Q*): the hint-free worst-case threshold min_Q [max F_Q - min F_Q] of a class of identical sites with known part
    f1 and envelope c * (uniform metric); F_Q(psi) = ln sum exp(-beta (f1 + psi)) + beta E_Q psi (theory report 11.28(d))."""
    from scipy.optimize import minimize
    k = len(f1)
    V = hamming_vertices(k, c)
    FQ = lambda Q, psi: math.log(float(np.sum(np.exp(-beta * (f1 + psi))))) + beta * float(Q @ psi)
    cons = [{"type": "ineq", "fun": (lambda z, a=a, b=b: c - (np.r_[0.0, z][a] - np.r_[0.0, z][b]))}
            for a in range(k) for b in range(k) if a != b]

    def m_of(Q):
        free = -np.log(np.maximum(Q, 1e-12)) / beta - f1
        best = float("inf")
        for start in (np.zeros(k - 1), np.clip(free[1:] - free[0], -5.0, 5.0)):
            res = minimize(lambda z: FQ(Q, np.r_[0.0, z]), start, constraints=cons, method="SLSQP", options=dict(ftol=1e-13, maxiter=500))
            if np.all([cc["fun"](res.x) >= -1e-9 for cc in cons]):
                best = min(best, float(res.fun))
        return best

    def obj(z):
        Q = np.exp(z - z.max())
        Q /= Q.sum()
        return max(FQ(Q, v) for v in V) - m_of(Q)

    best = min((minimize(obj, z0, method="Nelder-Mead", options=dict(xatol=1e-9, fatol=1e-12, maxiter=4000)) for z0 in (np.zeros(k), -beta * f1)),
               key=lambda r: r.fun)
    Q = np.exp(best.x - best.x.max())
    return float(best.fun), Q / Q.sum()


def bench_generalised_dips(rng, quick):
    section("B11. Beyond the cube: generalised dips, instance thresholds, and the hint-free threshold of two-state sites")
    rows = []
    print("single-letter lower bounds on the randomised exponent of ln Z (eps = o(n)) and thresholds; Hamming envelope c = 1, zero residual")
    print(f"{'site (energies), beta':>28} | {'R^rand (single dips)':>20} | {'R^gen (all vertices)':>20} | {'eps1_crit (dips)':>16} | {'eps1_thr (all)':>14}")
    sites = [("two-state (0, 0.5), 1", [0.0, 0.5], 1.0), ("flat 3-state, 1", [0.0] * 3, 1.0), ("flat 4-state, 1", [0.0] * 4, 1.0),
             ("flat 4-state, 0.5", [0.0] * 4, 0.5), ("three-state (0,0,2), 1", [0.0, 0.0, 2.0], 1.0),
             ("three-state (0,2,2), 1", [0.0, 2.0, 2.0], 1.0)]
    if not quick:
        sites += [("flat 8-state, 1", [0.0] * 8, 1.0), ("flat 8-state, 2", [0.0] * 8, 2.0)]
    grid = 201 if quick else 401
    for name, energies, beta in sites:
        E = np.array(energies)
        k = len(E)
        pi = np.exp(-beta * E)
        pi /= pi.sum()
        V = hamming_vertices(k)
        dips = [v for v in V if v.sum() == k - 1]         # B a singleton
        rr, rg = site_exponent(pi, dips, beta, grid=grid), site_exponent(pi, V, beta, grid=grid)
        crit, thr = site_game_threshold(pi, dips, beta), site_game_threshold(pi, V, beta)
        rows.append(dict(site=name, R_rand=rr, R_gen=rg, eps1_crit=crit, eps1_thr=thr))
        print(f"{name:>28} | {rr:20.5f} | {rg:20.5f} | {crit:16.5f} | {thr:14.5f}")
        if rg < rr - 1e-7 or thr < crit - 1e-9 or (k == 2 and (abs(rg - rr) > 1e-7 or abs(thr - crit) > 1e-9)):
            raise RuntimeError("generalised-dip exponent or threshold below the dip value, or different for a two-state site")
    by = {r["site"]: r for r in rows}
    if not (abs(by["flat 4-state, 1"]["R_gen"] - 0.02914) < 3e-5 and abs(by["flat 4-state, 1"]["R_rand"] - 0.02841) < 3e-5
            and abs(by["three-state (0,0,2), 1"]["eps1_thr"] - 0.1197) < 2e-4 and abs(by["three-state (0,0,2), 1"]["eps1_crit"] - 0.0947) < 2e-4):
        raise RuntimeError("documented values of the generalised-dip bounds are not reproduced")
    print("\nexact finite-n hitting numbers on flat k-state sites, u = 1, eps = 1 (uniform sampler, binomial tails): ln N for dips centred")
    print("at boxes of m-subsets; m = 1 are the single dips")
    for k, ms, n in ((4, (1, 2), 2000 if quick else 20000), (8, (1, 2, 3, 4), 1000)):
        vals = []
        for m in ms:
            pth = 1 - m / k
            logpmf = [math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) + j * math.log(pth) + (n - j) * math.log(1 - pth)
                      for j in range(n + 1)]
            lse = lambda a, b: max(a, b) + math.log1p(math.exp(-abs(a - b)))
            log_s, log_cdf, out = float("-inf"), float("-inf"), 0.0
            for R in range(1, n + 2):
                log_s = 1.0 + lse(log_s, logpmf[R - 1])
                log_cdf = lse(log_cdf, logpmf[R - 1])
                tail = -math.expm1(log_cdf) if log_cdf < 0 else 0.0
                if (lse(log_s, math.log(tail)) if tail > 0 else log_s) > 1.0:
                    out = -log_cdf
                    break
            vals.append(out)
        rows.append(dict(k=k, n=n, log_hitting=vals))
        print(f"   k = {k}, n = {n}: " + ", ".join(f"m={m}: {v:.1f}" for m, v in zip(ms, vals)))
        if max(vals[1:]) <= vals[0]:
            raise RuntimeError("boxes should be harder to hit than single dips on flat sites at u = 1")
    print("\nhint-free threshold of identical two-state sites (c = 1): largest chord gap of P(theta) = ln(1 + e^{-beta(e+theta)}) over [-c, c]")
    print(f"{'e':>5} {'beta':>5} | {'theta*':>8} | {'eps* = G(theta*)':>16} | {'G(0) (zero residual)':>20} | {'untilted width':>14} | {'ln cosh(beta c/2)':>17}")
    for e, beta in ((0.0, 1.0), (0.5, 1.0), (1.0, 1.0), (2.0, 1.0), (0.5, 4.0), (-1.0, 2.0)):
        P = lambda th: math.log1p(math.exp(-beta * (e + th)))
        p1 = lambda th: 1.0 / (1.0 + math.exp(beta * (e + th)))
        G = lambda th: ((1 + th) * P(1.0) + (1 - th) * P(-1.0)) / 2 - P(th)
        Dv = lambda tp, th: P(tp) - P(th) + (tp - th) * beta * p1(th)
        q = (P(-1.0) - P(1.0)) / (2 * beta)
        th_star = -e - math.log(q / (1 - q)) / beta
        eps_star, untilted = G(th_star), max(Dv(1.0, 0.0), Dv(-1.0, 0.0))
        rows.append(dict(e=e, beta=beta, theta_star=th_star, eps_star=eps_star, G0=G(0.0), untilted=untilted))
        print(f"{e:5.2f} {beta:5.2f} | {th_star:8.4f} | {eps_star:16.5f} | {G(0.0):20.5f} | {untilted:14.5f} | {math.log(math.cosh(beta / 2)):17.5f}")
        if not (G(0.0) <= eps_star + 1e-12 <= untilted + 1e-9 and abs(Dv(1.0, th_star) - eps_star) < 1e-10):
            raise RuntimeError("ordering G(0) <= eps* <= untilted width violated")
        if e in (0.5, 2.0) and beta == 1.0 and abs(class_threshold(np.array([0.0, e]), beta)[0] - eps_star) > 1e-6:
            raise RuntimeError("two-state site: min_Q [M(Q) - m(Q)] differs from the chord gap")
    print("\nhint-free threshold of a class of identical sites, any alphabet: eps* = min_Q [max F_Q - min F_Q] (c = 1, beta = 1)")
    print(f"{'site (energies)':>22} | {'eps1_thr at the zero residual':>29} | {'eps* (class, no hint)':>21} | {'passive width at zero':>21} | Q*")
    for name, energies in (("(0, 0.5)", [0.0, 0.5]), ("(0, 0, 2)", [0.0, 0.0, 2.0]), ("(0, 2, 2)", [0.0, 2.0, 2.0]), ("(0, 1, 3)", [0.0, 1.0, 3.0]),
                           ("flat 3-state", [0.0] * 3), ("flat 4-state", [0.0] * 4)):
        f1 = np.array(energies)
        k = len(f1)
        pi = np.exp(-f1)
        pi /= pi.sum()
        V = hamming_vertices(k)
        thr0 = site_game_threshold(pi, V, 1.0)
        passive = max(float(pi @ v) + math.log(float(np.sum(pi * np.exp(-v)))) for v in V)
        es, Qs = class_threshold(f1, 1.0)
        rows.append(dict(site=name, thr_zero=thr0, eps_star=es, passive_zero=passive, Q_star=Qs.tolist()))
        print(f"{name:>22} | {thr0:29.5f} | {es:21.5f} | {passive:21.5f} | {np.round(Qs, 4)}")
        if not (thr0 <= es + 1e-6 <= passive + 2e-6):
            raise RuntimeError("ordering eps1_thr(0) <= eps* <= passive width violated")
    return rows


def kl2(a, b):
    r = 0.0
    if a > 0:
        r += a * math.log(a / b)
    if a < 1:
        r += (1 - a) * math.log((1 - a) / (1 - b))
    return r


def theta_nonadaptive(u, e1):
    """min{KL(rho || 1/2) : KL(rho || p_u) <= e1}: exponent of non-adaptive algorithms (Theorems 11.44-11.45)."""
    pu = 1 / (1 + math.exp(u))
    if e1 >= kl2(0.5, pu):
        return 0.0
    lo, hi = pu, 0.5
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if kl2(mid, pu) <= e1 else (lo, mid)
    return kl2(lo, 0.5)


def theta_hinted(u, e1):
    rho = (math.log(2 / (1 + math.exp(-u))) + e1) / u
    return kl2(rho, 0.5) if rho < 0.5 else 0.0


def nonadaptive_bounds(n, u, eps, delta=0.05):
    """(R*, ln lower bound, r0, ln upper bound): the non-adaptive lower bound (1 - 2 delta) 2^n / |B(R* - 1)|, R* the least
    floor radius whose flattening lowers ln Z by more than eps (Theorem 11.45), and the Monte Carlo sample size
    8 ln(1/delta) 2^n / |B(r0)|, r0 the largest radius with ln(2 (1 + Gamma_n(r))) + ln(1/delta) <= eps for all r <= r0
    (Theorem 11.44)."""
    logc = [math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) for j in range(n + 1)]
    logex, logball = cube_dip_tables(n, u)
    lz_cone = n * math.log1p(math.exp(-u))

    def lz_flat(R):
        terms = [logc[j] - u * max(j, R) for j in range(n + 1)]
        mx = max(terms)
        return mx + math.log(sum(math.exp(t - mx) for t in terms))

    Rstar = next((R for R in range(1, n + 1) if lz_cone - lz_flat(R) > eps), None)
    lower = math.log(1 - 2 * delta) + n * math.log(2) - logball[Rstar - 1] if Rstar else 0.0
    budget, r0, worst = eps - math.log(2 / delta), None, -math.inf
    for r in range(1, n + 1):
        g = logex[r] + n * math.log(2) - logball[r - 1]
        worst = max(worst, g + math.log1p(math.exp(-g)) if g > 0 else math.log1p(math.exp(g)))
        if worst > budget:
            break
        r0 = r
    upper = math.log(8 * math.log(1 / delta)) + n * math.log(2) - (logball[r0] if r0 is not None else 0.0)
    return Rstar, lower, r0, upper


def fixed_accuracy_bounds(n, u, eps, eta=0.3, delta3=0.05):
    """Monte Carlo at a fixed accuracy eps (output ln Ahat, no recentring), by the two-sided tail lemma:
    (1 - eta)/(1 + G') <= Ahat/A <= 1 + eta + G'/delta3 outside probability e^{-eta^2 K/2} + e^{-eta^2 K/3} + delta3,
    G' = Gamma'_n(r) = sum_{j<=r} C(n,j)(e^{u(r+1-j)} - 1) / sum_j C(n,j) e^{-u(j-r+1)_+}.  Returns
    (r, ln M) for the largest admissible radius, K = 3 ln(40)/eta^2, or (None, None) if eps is too small for eta."""
    target = min(math.exp(eps / 2) * (1 - eta) - 1, delta3 * (math.exp(eps / 2) - 1 - eta))
    if target <= 0:
        return None, None
    K = 3 * math.log(40) / eta ** 2
    logc = [math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) for j in range(n + 1)]
    logex, logball = cube_dip_tables(n, u)

    def log_T(k):
        terms = [logc[j] - u * max(j - k, 0) for j in range(n + 1)]
        mx = max(terms)
        return mx + math.log(sum(math.exp(t - mx) for t in terms))

    best = None
    for r in range(1, n + 1):
        if logex[r] + n * math.log(2) - log_T(r - 1) > math.log(target):
            break
        best = r
    if best is None:
        return None, None
    return best, math.log(K) + n * math.log(2) - logball[best]


def bench_without_hint(rng, quick):
    section("B12. Without a hint on the cube: Monte Carlo is optimal among non-adaptive algorithms")
    out = dict(exponents=[], finite=[], simulation=[])
    print("exponents at accuracy n*eps1 (eps1 as a fraction of the threshold ln cosh(u/2)):")
    print(f"{'u':>7} | {'eps1/thr':>8} | {'with a hint (zero residual)':>27} | {'non-adaptive = Monte Carlo':>26} | {'ratio':>6} | {'Chebyshev bound ln cosh u':>25}")
    for u in (0.5, 1.0, 2.0, math.log(16.0)):
        thr = math.log(math.cosh(u / 2))
        for frac in (0.0, 0.1, 0.25, 0.5, 0.75, 0.9):
            a, b = theta_hinted(u, frac * thr), theta_nonadaptive(u, frac * thr)
            out["exponents"].append(dict(u=u, frac=frac, hinted=a, nonadaptive=b))
            print(f"{u:7.4f} | {frac:8.2f} | {a:27.5f} | {b:26.5f} | {b / a:6.3f} | {math.log(math.cosh(u)):25.5f}")
            if not a < b:
                raise RuntimeError("hinted exponent is not below the non-adaptive exponent")
    ex = {(round(r["u"], 4), r["frac"]): r for r in out["exponents"]}
    if not (abs(ex[(1.0, 0.0)]["hinted"] - 0.02914) < 2e-5 and abs(ex[(1.0, 0.0)]["nonadaptive"] - 0.11094) < 2e-5
            and abs(ex[(0.5, 0.0)]["nonadaptive"] - 0.03030) < 2e-5 and abs(ex[(2.0, 0.0)]["nonadaptive"] - 0.32781) < 2e-5):
        raise RuntimeError("documented exponents are not reproduced")
    print("\nfinite n (delta = 0.05): ln(evaluations)/n for the non-adaptive lower bound and for the Monte Carlo sample size")
    print(f"{'u':>5} | {'eps1':>7} | {'n':>5} | {'R*':>5} | {'lower':>8} | {'r0':>5} | {'upper':>8} | {'limit':>8}")
    for u, frac in ((1.0, 0.25), (2.0, 0.5)):
        e1 = frac * math.log(math.cosh(u / 2))
        for n in (100, 400, 1600) if quick else (100, 400, 1600, 6400):
            Rs, lo, r0, up = nonadaptive_bounds(n, u, n * e1)
            th = theta_nonadaptive(u, e1)
            out["finite"].append(dict(u=u, eps1=e1, n=n, Rstar=Rs, lower=lo / n, r0=r0, upper=up / n, limit=th))
            print(f"{u:5.1f} | {e1:7.4f} | {n:5d} | {Rs:5d} | {lo / n:8.5f} | {str(r0):>5} | {up / n:8.5f} | {th:8.5f}")
            if lo > up + 1e-9:
                raise RuntimeError("lower bound above upper bound")
    print("\nfixed accuracy eps = 1 (n fixed): ln(evaluations)/n; the first bound (Gamma) is void there, the two-sided lemma (Gamma') is not")
    print(f"{'u':>5} | {'n':>5} | {'first bound':>11} | {'two-sided':>9} | {'non-adaptive lower bound':>24} | {'KL(p_u||1/2)':>12} | {'Chebyshev ln cosh u':>19}")
    out["fixed"] = []
    for u in (0.5, 1.0, 2.0):
        for n in (1000,) if quick else (1000, 4000):
            _, lo, r0, up = nonadaptive_bounds(n, u, 1.0)
            r2, up2 = fixed_accuracy_bounds(n, u, 1.0)
            pu = 1 / (1 + math.exp(u))
            first = "void" if r0 is None else f"{up / n:.4f}"
            out["fixed"].append(dict(u=u, n=n, first=None if r0 is None else up / n, two_sided=up2 / n, lower=lo / n, kl=kl2(pu, 0.5)))
            print(f"{u:5.1f} | {n:5d} | {first:>11} | {up2 / n:9.4f} | {lo / n:24.4f} | {kl2(pu, 0.5):12.4f} | {math.log(math.cosh(u)):19.4f}")
            if r0 is not None or not lo <= up2 + 1e-9 or up2 / n > math.log(math.cosh(u)):
                raise RuntimeError("fixed-accuracy bounds are not as documented")
    print("\nMonte Carlo at a cone (n = 60, u = 1; 400 repetitions; weights sampled exactly through the binomial law of the distance):")
    print(f"{'M':>8} | {'median ln(Ahat/A)':>18} | {'1% quantile':>12} | {'certified lower end -ln(2(1+Gamma))':>36} | {'fraction below':>14}")
    n, u, K = 60, 1.0, 8 * math.log(20.0)
    logex, logball = cube_dip_tables(n, u)
    lnA = n * math.log((1 + math.exp(-u)) / 2)
    for M in (10 ** 3, 10 ** 4) if quick else (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
        r = next(k for k in range(n + 1) if logball[k] >= n * math.log(2) + math.log(K / M) - 1e-12)
        lg = (logex[r] + n * math.log(2) - logball[r - 1]) if r > 0 else -math.inf
        cert = -(math.log(2) + (math.log1p(math.exp(lg)) if lg < 30 else lg))
        reps = 400 if M <= 10 ** 5 else 100
        vals = np.empty(reps)
        for i in range(reps):
            dist = rng.binomial(n, 0.5, size=M)
            vals[i] = math.log(float(np.exp(-u * dist).mean())) - lnA
        below = float((vals < cert).mean())
        out["simulation"].append(dict(M=M, median=float(np.median(vals)), q01=float(np.quantile(vals, 0.01)), certified=cert, below=below))
        print(f"{M:8d} | {np.median(vals):18.3f} | {np.quantile(vals, 0.01):12.3f} | {cert:36.3f} | {below:14.3f}")
        if below > math.exp(-K / 8):
            raise RuntimeError("Monte Carlo falls below the certified lower end too often")
    print("\nadaptive against non-adaptive on the pair (cone, cone with flattened bottom), delta = 0.05:")
    print(f"{'n':>5} | {'u':>4} | {'eps':>8} | {'adaptive evaluations':>20} | {'non-adaptive lower bound':>24}")
    for n in (60, 200, 1000):
        e1 = 0.25 * math.log(math.cosh(0.5))
        Rs, lo, _, _ = nonadaptive_bounds(n, 1.0, n * e1)
        print(f"{n:5d} | {1.0:4.1f} | {n * e1:8.2f} | {n + 2:20d} | {'e^%.1f' % lo:>24}")
        out["finite"].append(dict(n=n, adaptive=n + 2, nonadaptive_ln=lo))
    return out


class LevelCube:
    """Balls and tail sums of the n-cube in logarithms: ln|B(n,r)|, ln E_r(n), ln Gamma~(r) = ln(E_r/|B(r-1)|)."""
    def __init__(self, n, u):
        self.n, self.u = n, u
        j = np.arange(n + 1)
        lb = np.array([math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) for k in j])
        self.logball = np.logaddexp.accumulate(lb)
        logE = np.empty(n + 1)
        logE[0] = math.log(math.expm1(u))
        for r in range(1, n + 1):                                   # E_r = e^u E_{r-1} + (e^u - 1) |B(r)|
            logE[r] = np.logaddexp(u + logE[r - 1], math.log(math.expm1(u)) + self.logball[r])
        self.logE = logE
        self.maxgam = np.maximum.accumulate(np.concatenate([[math.log(math.expm1(u))], logE[1:] - self.logball[:-1]]))

    def radius(self, logq):
        """least r with |B(n, r)| >= 2^n q"""
        return int(np.searchsorted(self.logball, self.n * math.log(2) + logq - 1e-12))

    def bracket_cost(self, x, K):
        """ln(evaluations) of the two-sample bracket of Proposition 11.46 with certified log-width at most x"""
        ok = np.nonzero(np.logaddexp(math.log(3), math.log(12) + self.maxgam) <= x)[0]
        if len(ok) == 0:
            return math.inf
        logm = (self.n + 1) * math.log(2) + math.log(K) - self.logball[int(ok[-1])]
        return math.log(2) + max(logm, math.log(2 * K))


def two_level_flat_cost(n, u, phi, b, G, delta=0.05):
    """ln(evaluations) of the two-level algorithm of Theorem 11.52 at the flat instance, with the constants of the
    proof and expectations in place of counts (all fibre averages are equal; an estimate, not a bound)."""
    n_o = max(1, int(round(phi * n)))
    n_i = n - n_o
    logn = (n + 6) * math.log(2) + 3 * math.log(n) - math.log(delta)
    K, Kin = math.ceil(24 * logn), math.ceil(24 * (logn + 2 * math.log(2)))
    J = math.ceil(2 * u * n + b + n_o * math.log(2) + 10)
    outer, inner = LevelCube(n_o, u), LevelCube(n_i, u)
    logs = [math.log(K * max(b, 1.0)) + inner.bracket_cost(b, Kin)]   # the levels within b of the bulk
    x = 1
    while x <= 5 * u * n + 50:                                       # levels at height x above the last populated one
        logMneg = math.log(4 * K * J) + 2 + (x - 1)
        logM, closed = math.log(K), False
        while logM <= logMneg + math.log(2):
            logq = math.log(2 * K) - logM
            if n_o * math.log(2) + logq < 0:
                closed = True
                break
            r = outer.radius(logq)
            if r < n_o and x + outer.logE[r] - n_o * math.log(2) <= G - b - math.log(2):
                closed = True
                break
            logM += math.log(2)
        logs.append(logM + inner.bracket_cost(max(x, b), Kin))
        if closed:
            mx = max(logs)
            if not math.isfinite(mx):                               # some inner accuracy cannot be certified at this size
                return math.inf, None
            return mx + math.log(sum(math.exp(t - mx) for t in logs)), G + math.log(4 * math.e * J + 3)
        x += 1
    return math.inf, None


def bench_adaptive_levels(rng, quick):
    section("B13. Adaptive algorithms without a hint: the level recursion approaches the hinted exponent")
    out = dict(levels=[], fixed_point=[])
    depth = 7 if quick else 14
    marks = (0.0, 0.05, 0.25, 0.5, 0.75)
    print("T_k / theta_na at accuracy n*eps1 (eps1 as a fraction of the threshold; 0.00 stands for 1e-4);")
    print("T_1 = theta_na (non-adaptive), T_{k+1} = min(T_k, R[T_k]) (k nested levels, Theorem 11.52); last row: theta_hint / theta_na")
    for u in (0.5, 1.0, 2.0):
        r = fc.LvRecursion(u) if quick else fc.LvRecursion(u, G=240, P=80, B=24, C=64)
        idx = [int(np.argmin(np.abs(r.g - max(m, 1e-4) * r.estar))) for m in marks]
        na = np.array([fc.na_theta_na(u, float(x)) for x in r.g])
        print(f"\nu = {u}:  a = theta_na(0+) = {r.a:.5f},  h = theta_hint(0+) = {r.h:.5f},  h/a = {r.h / r.a:.4f}")
        print(f"{'levels':>10} | " + " | ".join(f"{m:6.2f}" for m in marks) + " | max (T_k - theta_hint)/a")
        for k in range(2, depth + 1):
            r.step()
            if np.any(r.T < r.hint - 2e-4 * r.a):
                raise RuntimeError("a level of the recursion is below the hinted exponent")
            exc = float(np.max(r.T - r.hint)) / r.a
            out["levels"].append(dict(u=u, k=k, ratios=[float(r.T[i] / na[i]) for i in idx], excess=exc))
            if k in (2, 3, 4, 5, 7, 10, 14):
                print(f"{k:10d} | " + " | ".join(f"{r.T[i] / na[i]:6.3f}" for i in idx) + f" | {exc:8.4f}")
        print(f"{'hint':>10} | " + " | ".join(f"{r.hint[i] / na[i]:6.3f}" for i in idx) + " |")
        if exc > (0.03 if quick else 0.012):
            raise RuntimeError("the recursion does not approach the hinted exponent")
    lv = {(d["u"], d["k"]): d for d in out["levels"]}
    if not (0.47 < lv[(1.0, 2)]["ratios"][0] < 0.53 and lv[(1.0, 3)]["ratios"][0] < 0.40 and lv[(1.0, 4)]["ratios"][0] < 0.34):
        raise RuntimeError("documented values of the second to fourth level are not reproduced")
    print("\nthe fixed point (Theorem 11.53(b)): outer fraction phi* = g/(g + theta_hint(g)); the outer sample has exponent phi* theta_hint(g),")
    print("each inner bracket (1 - phi*) theta_hint(g), at inner accuracy rate g;  identity theta_na(g + theta_hint(g)) = theta_hint(g):")
    print(f"{'u':>5} | {'g/eps*':>6} | {'phi*':>6} | {'theta_hint(g)':>13} | {'theta_na(g + theta_hint(g))':>27} | {'theta_na(g)':>11}")
    for u in (0.5, 1.0, 2.0):
        _, _, estar, a, h = fc.lv_consts(u)
        for frac in (0.05, 0.25, 0.5, 0.75):
            g = frac * estar
            th = fc.na_theta_hint(u, g)
            lhs = fc.na_theta_na(u, g + th)
            out["fixed_point"].append(dict(u=u, frac=frac, phi=g / (g + th), hint=th, shifted=lhs))
            print(f"{u:5.1f} | {frac:6.2f} | {g / (g + th):6.3f} | {th:13.6f} | {lhs:27.6f} | {fc.na_theta_na(u, g):11.6f}")
            if abs(lhs - th) > 1e-9:
                raise RuntimeError("identity theta_na(g + theta_hint(g)) = theta_hint(g) fails")
    print("\nwhen would it pay?  flat instance, u = 1, accuracy rate eps*/4, delta = 0.05; ln(evaluations) of the two-level")
    print("algorithm with the constants of the proof (expectations in place of counts; best of a few (phi, b)) against the")
    print("two-sample bracket at the same certified width:")
    print(f"{'n':>7} | {'two-level':>10} | {'two-sample bracket':>18} | {'phi':>4} | {'width/n':>8}")
    u = 1.0
    estar = math.log(math.cosh(u / 2))
    out["crossover"] = []
    for n in ((1000, 5000) if quick else (500, 1000, 2000, 5000, 10000, 20000)):
        G = 0.25 * estar * n
        best = (math.inf, 0.0, G + math.log(4 * math.e * math.ceil(2 * u * n + 10) + 3))
        for phi in ((0.7, 0.8) if quick else (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)):
            for bfrac in ((0.1, 0.2, 0.4) if quick else (0.02, 0.05, 0.1, 0.2, 0.4)):
                c, width = two_level_flat_cost(n, u, phi, bfrac * G, G)
                if c < best[0]:
                    best = (c, phi, width)
        c, phi, width = best
        mc = LevelCube(n, u).bracket_cost(width, 24 * math.log(4 / 0.05))
        out["crossover"].append(dict(n=n, two_level=c, bracket=mc, phi=phi, width=width))
        print(f"{n:7d} | {c:10.1f} | {mc:18.1f} | {phi:4.1f} | {width / n:8.4f}")
    cr = {d["n"]: d for d in out["crossover"]}
    if not (cr[1000]["two_level"] > cr[1000]["bracket"] and cr[5000]["two_level"] < cr[5000]["bracket"]):
        raise RuntimeError("documented crossover between n = 1000 and n = 5000 is not reproduced")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--json", type=str, default=None)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    out = {
        "B1_pruning": bench_pruning(rng, args.quick),
        "B2_witness": bench_witness(rng, args.quick),
        "B3_spectral": bench_spectral(rng, args.quick),
        "B4_sandwich": bench_sandwich(rng, args.quick),
        "B5_certificate_size": bench_certificate_size(rng, args.quick),
        "B6_thermal": bench_thermal(rng, args.quick),
        "B7_torsion": bench_torsion(rng, args.quick),
        "B8_exponent": bench_exponent(rng, args.quick),
        "B9_best_first": bench_best_first(rng, args.quick),
        "B10_query_complexity": bench_query_complexity(rng, args.quick),
        "B11_generalised_dips": bench_generalised_dips(rng, args.quick),
        "B12_without_hint": bench_without_hint(rng, args.quick),
        "B13_adaptive_levels": bench_adaptive_levels(rng, args.quick),
    }
    if args.json:
        os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
        with open(args.json, "w") as fh:
            json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
