"""Steps 2/4 -- exact site functions of short chains (the whole chain of n sites as ONE super-site, all vertices of its
Lipschitz polytope = all integer height functions times u), binary symmetric chain, u = 1.
 (i)   F*_n(t), E_n, a_n with all vertices against site-wise labels only; weight of the non-additive vertices in the optimal M
 (ii)  the Markov-recursion (DP) upper bound  F*_n(t) <= F*[(1/2,1/2); d*_1](t) + sum_{i>=2} F*[(1-p,p); d*_i](t),  d*_n = u, d*_i = u + g(d*_{i+1})
 (iii) almost-additivity |F*_{n1+n2} - F*_{n1} - F*_{n2}| <= t K
 (iv)  E_n against ln Z_n(h)/Z_n(0) (the two uniform-field labels)
usage: python3 y04_exact_small_n.py [nmax]   (default 4; 5 needs 395094 vertices, about 1 GB and several minutes)"""
import sys, time, math
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import *

t0 = time.time(); u = 1.0
nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
ts = (0.25, 0.45, 0.65)
def gfun(x, p): return math.log(((1 - p) * math.exp(x) + p) / (p * math.exp(x) + 1 - p))
def site_F(law, slope, t):
    P = gibbs_rows(law, [[0.0, slope], [0.0, -slope]]); return renyi_F(P, t, tol=1e-12)[1]
def site_E(law, slope):
    P = gibbs_rows(law, [[0.0, slope], [0.0, -slope]]); return E_threshold(P, tol=1e-12)[1]
def site_a(law, slope):
    P = gibbs_rows(law, [[0.0, slope], [0.0, -slope]]); return capacity(P, tol=1e-12)[1]
def lnZ_field(n, p, h):
    Kp = 0.5 * math.log((1 - p) / p)
    T = np.array([[math.exp(Kp), math.exp(-Kp)], [math.exp(-Kp), math.exp(Kp)]]); D = np.diag([math.exp(h), math.exp(-h)])
    v = np.array([math.exp(h), math.exp(-h)]); x = v.copy()
    for _ in range(n - 1): x = D @ (T @ x)
    return math.log(x.sum())

H = {n: height_functions(n) * u for n in range(1, nmax + 1)}
print("vertices:", {n: len(H[n]) for n in H}, " (%.1f s)" % (time.time() - t0))
addmask = {}
for n in H:
    add = sitewise_labels([u] * n); add = add - add[:, :1]
    keys = {tuple(np.round(f, 6)) for f in add}
    addmask[n] = np.array([tuple(np.round(f, 6)) in keys for f in H[n]])
    assert addmask[n].sum() == 2 ** n

store = {}
for p in (0.4, 0.3, 0.1):
    K = math.log((1 - p) / p)
    print("\n=== p = %.1f, K = %.4f" % (p, K))
    for n in range(1, nmax + 1):
        pi = bsc_block_law(n, p); P = gibbs_rows(pi, H[n]); Pa = P[addmask[n]]
        tol = 1e-10 if n <= 4 else 2e-8; itmax = 100000 if n <= 4 else 2500
        dst = [u]
        for i in range(n - 1): dst.append(u + gfun(dst[-1], p))
        dst = dst[::-1]                                              # d*_1 .. d*_n
        line = "n=%d:" % n
        for t in ts:
            lo, up, M, Q = renyi_F(P, t, tol=tol, itmax=itmax)
            loa, upa, Ma, Qa = renyi_F(Pa, t, tol=tol, itmax=itmax)
            dp = site_F([0.5, 0.5], dst[0], t) + sum(site_F([1 - p, p], dst[i], t) for i in range(1, n))
            store[(p, n, t)] = (lo, up)
            line += "  t=%.2f: F*_n=[%.7f,%.7f] site-wise only=[%.7f,%.7f] w(non-add)=%.1e  DP bound=%.7f (%s)" % (
                t, lo, up, loa, upa, M[~addmask[n]].sum(), dp, "ok" if dp >= lo - 1e-9 else "VIOLATED")
        print(line)
        Elo, Eup, ME, QE = E_threshold(P, tol=tol, itmax=20 * itmax); Ealo, Eaup, _, _ = E_threshold(Pa, tol=tol, itmax=20 * itmax)
        alo, aup, Ma_, _ = capacity(P, tol=tol, itmax=20 * itmax); aalo, aaup, _, _ = capacity(Pa, tol=tol, itmax=20 * itmax)
        EF = lnZ_field(n, p, u / 2) - lnZ_field(n, p, 0.0)
        dpE = site_E([0.5, 0.5], dst[0]) + sum(site_E([1 - p, p], dst[i]) for i in range(1, n))
        dpa = site_a([0.5, 0.5], dst[0]) + sum(site_a([1 - p, p], dst[i]) for i in range(1, n))
        store[(p, n, "E")] = (Elo, Eup); store[(p, n, "a")] = (alo, aup)
        print("      E_n=[%.7f,%.7f] site-wise only=[%.7f,%.7f] w(non-add)=%.1e | ln Z_n(h)/Z_n(0)=%.7f (E_n - that = %.2e) | DP bound=%.7f" % (
            Elo, Eup, Ealo, Eaup, ME[~addmask[n]].sum(), EF, Elo - EF, dpE))
        print("      a_n=[%.7f,%.7f] site-wise only=[%.7f,%.7f] w(non-add)=%.1e | DP bound=%.7f" % (alo, aup, aalo, aaup, Ma_[~addmask[n]].sum(), dpa))
        print("      per site: F*_n(0.45)/n = %.6f, E_n/n = %.6f, a_n/n = %.6f" % (store[(p, n, 0.45)][0] / n, Elo / n, alo / n))
    # almost-additivity
    worst = 0.0
    for n1 in range(1, nmax):
        for n2 in range(n1, nmax - n1 + 1):
            for t in ts:
                dlt = store[(p, n1 + n2, t)][0] - store[(p, n1, t)][0] - store[(p, n2, t)][0]
                worst = max(worst, abs(dlt) / (t * K))
    print("  almost-additivity: max |F*_{n1+n2} - F*_{n1} - F*_{n2}| / (t K) = %.4f  (must be <= 1)" % worst)
print("%.1f s" % (time.time() - t0))
