"""N9 — direction 3: funnels with INTERACTING known parts.  Integer funnel slope vs LP funnel slope.

Known part: binary pairwise  f(x) = sum_i h_i s_i + sum_{(i,j) in E} J_ij s_i s_j,  s = 1 - 2x in {+-1}
(written as a pairwise model with tables theta_i, theta_ij).  Envelope d = sum_i c_i [x_i != y_i].
x* = argmin f.

  tau    = min_{y != x*} (f(y) - f(x*)) / d(x*, y)        (integer funnel slope; brute force)
  tau_LP = max { t : exists messages phi with
                   theta~_ij(s,u) >= theta~_ij(x*_i, x*_j)               for all edges, labels
                   theta~_i(s) - theta~_i(x*_i) >= t c_i                 for all i, s != x*_i }
           (one linear programme; = sup{t : local-polytope LP of f - t d(x*,.) is tight at x*})

Theory (report Theorem E): tau_LP <= tau always; equality on trees and for ferromagnetic
(submodular) couplings; a single evaluation of the residual at x* certifies min(f+g) for every
admissible g iff c-scaled slope 1 <= tau, and then the messages are a polynomial-size proof
whenever 1 <= tau_LP.

Experiments: (1) random instances on a 4x4 grid, a 12-site chain with 6 extra long-range contacts,
a tree, with a fraction p of antiferromagnetic bonds and random fields; (2) heterogeneous c_i;
(3) the smallest frustrated example with tau_LP < tau, exact rationals printed.
Run: OMP_NUM_THREADS=1 python3 n9_lp_funnel.py
"""
import itertools
import json
import math

import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(909)


def energies(n, h, edges, J):
    idx = np.arange(1 << n)
    s = 1 - 2 * ((idx[:, None] >> np.arange(n)[None, :]) & 1)       # (2^n, n) spins
    E = s @ h
    for (i, j), Jij in zip(edges, J):
        E = E + Jij * s[:, i] * s[:, j]
    return E, s


def tau_integer(n, E, c):
    xs = int(np.argmin(E))
    idx = np.arange(1 << n)
    diff = idx ^ xs
    bits = ((diff[:, None] >> np.arange(n)[None, :]) & 1).astype(float)
    d = bits @ c
    mask = diff != 0
    ratio = (E[mask] - E[xs]) / d[mask]
    k = int(np.argmin(ratio))
    return xs, float(ratio[k]), int(np.count_nonzero(bits[mask][k]))


def tau_lp(n, h, edges, J, c, xs):
    """Maximise t subject to dual feasibility.  Variables: t, then phi[e, side, label]
    (side 0: message to node i of edge e=(i,j); side 1: to node j).  Spins: label 0 -> +1, 1 -> -1."""
    spin = lambda lab: 1 - 2 * lab
    xlab = [(xs >> i) & 1 for i in range(n)]
    nE = len(edges)
    nv = 1 + nE * 2 * 2
    var = lambda e, side, lab: 1 + (e * 2 + side) * 2 + lab
    A_ub, b_ub = [], []
    inc = [[] for _ in range(n)]
    for e, (i, j) in enumerate(edges):
        inc[i].append((e, 0))
        inc[j].append((e, 1))
    # unary:  theta_i(s) + sum phi(s) - theta_i(x*) - sum phi(x*) >= t c_i     for s != x*_i
    for i in range(n):
        s_lab = 1 - xlab[i]
        row = np.zeros(nv)
        row[0] = c[i]
        for (e, side) in inc[i]:
            row[var(e, side, s_lab)] -= 1.0
            row[var(e, side, xlab[i])] += 1.0
        A_ub.append(row)
        b_ub.append(h[i] * spin(s_lab) - h[i] * spin(xlab[i]))
    # pairwise: theta_ij(s,u) - phi_i(s) - phi_j(u) >= theta_ij(x*) - phi_i(x*_i) - phi_j(x*_j)
    for e, (i, j) in enumerate(edges):
        for s_lab, u_lab in itertools.product((0, 1), repeat=2):
            if (s_lab, u_lab) == (xlab[i], xlab[j]):
                continue
            row = np.zeros(nv)
            row[var(e, 0, s_lab)] += 1.0
            row[var(e, 1, u_lab)] += 1.0
            row[var(e, 0, xlab[i])] -= 1.0
            row[var(e, 1, xlab[j])] -= 1.0
            A_ub.append(row)
            b_ub.append(J[e] * spin(s_lab) * spin(u_lab) - J[e] * spin(xlab[i]) * spin(xlab[j]))
    cost = np.zeros(nv)
    cost[0] = -1.0
    bounds = [(None, None)] * nv
    res = linprog(cost, A_ub=np.array(A_ub), b_ub=np.array(b_ub), bounds=bounds, method="highs")
    if res.status != 0:
        return float("nan"), res.status
    return float(res.x[0]), 0


def grid_edges(a, b):
    e = []
    for r in range(a):
        for q in range(b):
            i = r * b + q
            if q + 1 < b:
                e.append((i, i + 1))
            if r + 1 < a:
                e.append((i, i + b))
    return e


def chain_with_contacts(n, k):
    e = [(i, i + 1) for i in range(n - 1)]
    cand = [(i, j) for i in range(n) for j in range(i + 3, n)]
    pick = rng.choice(len(cand), k, replace=False)
    return e + [cand[p] for p in pick]


def random_tree(n):
    return [(int(rng.integers(0, i)), i) for i in range(1, n)]


def run_family(name, make_edges, n, p_af, hscale, ntrial, hetero=False):
    eq = 0
    ratios, taus, taulps = [], [], []
    viol = 0
    for _ in range(ntrial):
        edges = make_edges()
        J = -np.abs(rng.standard_normal(len(edges)))               # ferromagnetic: J < 0 favours equal spins
        flip = rng.random(len(edges)) < p_af
        J = np.where(flip, -J, J)
        h = hscale * rng.standard_normal(n)
        c = rng.uniform(0.5, 2.0, n) if hetero else np.ones(n)
        E, _ = energies(n, h, edges, J)
        xs, tau, droplet = tau_integer(n, E, c)
        tlp, status = tau_lp(n, h, edges, J, c, xs)
        if status != 0:
            viol += 1
            continue
        if tlp > tau + 1e-7:
            viol += 1
        taus.append(tau)
        taulps.append(tlp)
        if abs(tlp - tau) <= 1e-7 * max(1.0, abs(tau)):
            eq += 1
        ratios.append(tlp / tau if tau > 1e-12 else float("nan"))
    r = np.array(ratios)
    rec = {"family": name, "n": n, "p_antiferro": p_af, "field_scale": hscale, "hetero_c": hetero,
           "trials": ntrial, "violations(tau_LP>tau or LP failure)": viol,
           "frac_equal": eq / max(1, len(taus)),
           "frac_LP_tight_at_xstar(tau_LP>=0)": float(np.mean(np.array(taulps) >= -1e-9)),
           "median_tau": float(np.median(taus)), "median_tau_LP": float(np.median(taulps)),
           "median_ratio": float(np.nanmedian(r)), "q10_ratio": float(np.nanquantile(r, 0.1))}
    print(rec, flush=True)
    return rec


out = []
for p_af in (0.0, 0.1, 0.3, 0.5):
    for hs in (0.5, 2.0):
        out.append(run_family("grid4x4", lambda: grid_edges(4, 4), 16, p_af, hs, 60))
for p_af in (0.0, 0.3, 0.5):
    out.append(run_family("chain12+6contacts", lambda: chain_with_contacts(12, 6), 12, p_af, 1.0, 100))
    out.append(run_family("chain12+6contacts", lambda: chain_with_contacts(12, 6), 12, p_af, 1.0, 100,
                          hetero=True))
out.append(run_family("tree14", lambda: random_tree(14), 14, 0.5, 1.0, 100))
out.append(run_family("tree14", lambda: random_tree(14), 14, 0.5, 1.0, 100, hetero=True))

# ---- a minimal explicit example: exhaustive search over triangles with half-integer fields
best = None
edges = [(0, 1), (1, 2), (0, 2)]
c = np.ones(3)
vals = [x / 2 for x in range(-8, 9)]
for Js in itertools.product((-1.0, 1.0), repeat=3):
    for hs in itertools.product(vals, repeat=3):
        h, J = np.array(hs), np.array(Js)
        E, _ = energies(3, h, edges, J)
        srt = np.sort(E)
        if srt[1] - srt[0] < 1e-9:
            continue                                       # unique ground state only
        xs, tau, droplet = tau_integer(3, E, c)
        tlp, st = tau_lp(3, h, edges, J, c, xs)
        if st == 0 and tau - tlp > 1e-6:
            gap = (tau - tlp) / tau
            if best is None or gap > best[0] + 1e-9:
                best = (gap, hs, Js, tau, tlp, xs, droplet, E.tolist())
if best is None:
    ex = {"example": "no triangle with half-integer fields in [-4,4] and J=+-1 has tau_LP < tau"}
else:
    ex = {"example": "triangle, largest relative gap among half-integer fields in [-4,4], J=+-1",
          "h": best[1], "J(01,12,02)": best[2], "tau": best[3], "tau_LP": best[4],
          "xstar": best[5], "worst_droplet_size": best[6], "E": best[7]}
print(ex)
out.append(ex)
with open("n9_lp_funnel.json", "w") as fh:
    json.dump(out, fh, indent=1)
print("N9 done")
