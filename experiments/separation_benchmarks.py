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
    }
    if args.json:
        os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
        with open(args.json, "w") as fh:
            json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
