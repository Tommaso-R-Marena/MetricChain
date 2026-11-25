"""w07: exact finite-n sums for NON-ADAPTIVE algorithms: generalised cones truncated at the orbit-wise quantiles.

The generalised cone psi(x) = sum_i phi_i(x_i), phi_i a vertex of the Lipschitz polytope of the site type of i
(label blocks of sizes round(n M*(phi))), is an additive, non-invariant member of the class; its weight is
constant on the cells (joint type P, value c).  For 0 < q < 1 let t_P be the upper q-quantile of w = e^{-psi}
on the joint-type class T_P and psi^{tr,q} = max(psi, -ln t_P): a member of the class that differs from psi on
density at most q in every joint-type class (report, Theorem W1(a); GroupSampling.lean).  Then EVERY
non-adaptive (eps/2, delta)-correct algorithm makes at least (1 - 2 delta)/q evaluations whenever
eps < x_n(q) := ln[A(psi)/A(psi^{tr,q})]   (group_nonadaptive_queries_ge).  x_n(q) is computed exactly.

Reported: theta_n(eps) = -ln(q_min)/n with q_min the least q such that x_n(q) > eps = x n + eps0, against the
single-letter non-adaptive exponent theta_na(x) = R(S^{-1}(x)); here x = e + R(e), so theta_na(x) = R(e).

usage: python3 w07_nonadaptive_finite.py <chain (one site type)> <e_frac> <n1,n2,...> [eps0]
"""
import math
import sys
import time

import numpy as np

from wlib import *
from wfin import *
from wprimal import dip_profile
from wsites import chains

UNITS = {"path(0.8,1.6)": 0.8, "tri(1,1.5,2)": 0.5, "asym": 0.5, "bin(0.3,1)": 1.0}


def cone_table(s, n, P, phis):
    sz = round_counts(n, P)
    p = Part(s, sz, unit=UNITS[s.name])
    blks, shift = [], 0.0
    for u, nu in enumerate(sz):
        K, c = p.linear_costs(int(nu), phis[u])
        blks.append((K, c))
        shift += int(nu) * float(np.min(phis[u]))
    cmax = sum(int(c.max()) for (K, c) in blks)
    p.build(blks, cmax)
    return p, sz, shift


def xn_of_q(p, f, F, G, lastsup, w, lpiT, q):
    """ln[A/A^tr] for the truncation at the orbit-wise upper q-quantiles (exact)"""
    idx = p.Pidx
    # c0 = number of i in [0, cmax] with Fcum[P, i] <= q, minus 1;  c* = last support point <= c0
    c0 = np.sum(F[idx, :p.C1] <= q * (1 + 1e-12), axis=1) - 1
    cs = lastsup[idx, c0]
    assert np.all(cs >= 0)
    dens_above = F[idx, cs]                               # dens{w > t_P} <= q
    assert np.all(dens_above <= q * (1 + 1e-9))
    Etr = F[idx, cs + 1] * w[cs] + (G[idx, p.C1] - G[idx, cs + 1])
    Efull = G[idx, p.C1]
    lA = np.logaddexp.reduce(lpiT + np.log(Efull))
    lAtr = np.logaddexp.reduce(lpiT + np.log(Etr))
    return float(lA - lAtr), float(dens_above.max())


if __name__ == "__main__":
    name = sys.argv[1]
    e_frac = float(sys.argv[2])
    ns = [int(x) for x in sys.argv[3].split(",")]
    eps0 = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    t00 = time.time()
    ch = chains()[name]
    assert len(ch.sites) == 1
    s = ch.sites[0]
    E = ch.E()
    e1 = e_frac * E
    R, ts = ch.R(e1, return_t=True)
    x = e1 + R
    prof, phis, Ms, gam = dip_profile(ch, ts)
    print(f"=== w07 non-adaptive finite-n: chain {ch.name}; e = {e_frac} E = {e1:.6f}; R(e) = {R:.6f}; accuracy rate x = e + R(e) = {x:.6f};"
          f" theta_na(x) = R(e) = {R:.6f}; eps = x n + {eps0} ===")
    print(f"  cone labels (vertices) {np.round(phis[0], 3).tolist()} with weights {np.round(prof.P[0], 4)}")
    rows = []
    for n in ns:
        t0 = time.time()
        p, sz, shift = cone_table(s, n, prof.P[0], phis[0])
        f, F = p.dens_table()
        w = np.exp(-np.arange(p.C1) * p.unit)             # weights up to the common factor e^{-shift}
        G = np.zeros_like(F)
        np.cumsum(f * w[None, :], axis=1, out=G[:, 1:])
        sup = np.where(f > 0, np.arange(p.C1)[None, :], -1)
        lastsup = np.maximum.accumulate(sup, axis=1)
        lpiT = p.lTP[p.Pidx] + p.Ptypes @ np.log(s.pi)
        eps = x * n + eps0
        # x_n(q) is nondecreasing in q: bisection on ln q for the least q with x_n(q) > eps
        lo, hi = -n * math.log(s.q) - 5.0, 0.0
        xhi, _ = xn_of_q(p, f, F, G, lastsup, w, lpiT, math.exp(hi) * (1 - 1e-12))
        if xhi <= eps:
            print(f"  n = {n}: even q -> 1 does not reach eps = {eps:.3f} (x_n(1-) = {xhi:.3f}); no bound")
            continue
        for it in range(60):
            mid = 0.5 * (lo + hi)
            xm, _ = xn_of_q(p, f, F, G, lastsup, w, lpiT, math.exp(mid))
            if xm > eps:
                hi = mid
            else:
                lo = mid
        q = math.exp(hi)
        xq, dmax = xn_of_q(p, f, F, G, lastsup, w, lpiT, q)
        th = -hi / n
        rows.append((n, th))
        print(f"  n = {n:4d}: block sizes {sz.tolist()}; eps = {eps:8.3f}; least q with x_n(q) > eps: q = {q:.4e} (x_n = {xq:.3f}, largest orbit density of the"
              f" truncated set {dmax:.3e})  ->  theta_n = {th:.6f}   (theta_na = {R:.6f}; (theta_n - theta_na) n / ln n = {(th - R) * n / math.log(n):+.3f}); {time.time()-t0:.1f} s")
    if len(rows) >= 2:
        (n1, t1), (n2, t2) = rows[-2], rows[-1]
        b = (t1 - t2) / (math.log(n1) / n1 - math.log(n2) / n2)
        print(f"  two-point extrapolation a + b ln n/n from n = {n1}, {n2}: a = {t2 - b * math.log(n2) / n2:.6f}, b = {b:.3f}   (theta_na = {R:.6f})")
    print(f"time {time.time()-t00:.0f} s")
