#!/usr/bin/env python3
"""Workstream N, check 1: tail functions on small cubes, exactly.

  A. Q_m, m = 2, 3, 4, uniform measure, envelope u * Hamming: the exact tail functions (maximum / minimum over ALL
     subsets) against Harper's formulas E_r, T_k of Lemma 11.43(b),(c) (theory report) as functions of the measure q:
       A1  Harper's step function Xi(q) >= exact Xi(q) for every q = k/2^m, with equality at q = |B(r)|/2^m, r <= m-1;
       A2  Harper's Theta(p) <= exact Theta(p), with equality at p = |B(k)|/2^m;
       A3  the exact functions are attained by segments of the simplicial order at EVERY cardinality
           (so "integrality of radii" loses nothing if the segment values are used).
  B. the two tail inequalities (TU), (TL) of N_REPORT 2.1 with Harper's functions on members of the class, m <= 12
     (random u-Lipschitz functions of five kinds, all levels).
  C. weighted Hamming envelopes sum_i u_i [x_i != y_i] on Q_3, Q_4 (uniform measure): the "sorted-slope" Harper bound of
     N_REPORT 4(d) against the exact tail function: valid, equal when all slopes are equal, lossy otherwise.
  D. a biased product measure on Q_4 with the Hamming envelope: the exact tail function relative to the measure itself
     (reference 0) -- valid by construction; printed for the record (no closed form is claimed).

  E. the ball-volume and the transport tail functions of N_REPORT 4(e) on the cube: valid, far from Harper's values.

Run:  python3 n1_tail_bruteforce.py > out_n1_tail_bruteforce.txt      (about half a minute)
"""
import itertools
import math
import sys
import time

import numpy as np

from nlib import CubeTables, envelope_tails, INF

t0 = time.time()
fails = 0


def hamming_matrix(m):
    n = 1 << m
    x = np.arange(n)
    return np.array([[bin(a ^ b).count("1") for b in range(n)] for a in range(n)], dtype=float)


def weighted_matrix(m, us):
    n = 1 << m
    M = np.zeros((n, n))
    for a in range(n):
        for b in range(n):
            d = a ^ b
            M[a, b] = sum(us[i] for i in range(m) if (d >> i) & 1)
    return M


def simplicial_order(m):
    """points of Q_m sorted by weight, then so that x precedes y when the least element of the symmetric difference is in x"""
    pts = list(range(1 << m))

    def key(x):
        # weight first; then lexicographic on the indicator read from coordinate 0 with 1 before 0
        return (bin(x).count("1"), tuple(0 if (x >> i) & 1 else 1 for i in range(m)))
    return sorted(pts, key=key)


print("=" * 100)
print("A. exact tail functions of (Q_m, uniform, u*Hamming) against Harper's formulas")
print("=" * 100)
for m in (2, 3, 4):
    Hd = hamming_matrix(m)
    n = 1 << m
    mu = np.full(n, 1.0 / n)
    order = simplicial_order(m)
    for u in (0.5, 1.0, 2.0):
        Xi_ex, Th_ex, raw = envelope_tails(mu, u * Hd, return_sets=True)
        tab = CubeTables(m, u)
        worst_up, worst_lo = 0.0, INF
        eq_up = eq_lo = True
        seg_up = seg_lo = True
        for k in range(1, n):
            q = k / n
            ex = Xi_ex(q)
            ha = tab.Xi(q)
            if ha < INF:
                worst_up = max(worst_up, ex / ha if ha > 0 else 0.0)
                if ex > ha * (1 + 1e-12):
                    fails += 1
            if k in tab.ball[:m]:                      # ball sizes, r <= m-1
                eq_up &= abs(ex - ha) <= 1e-12 * ha
            # A3: D = the last k points of the simplicial order (complement of an initial segment)
            mask = sum(1 << x for x in order[n - k:])
            seg_up &= abs(raw['F'][mask] - ex) <= 1e-12 * max(ex, 1e-300)
        for k in range(1, n + 1):
            p = k / n
            ex = Th_ex(p)
            ha = tab.Theta(p)
            worst_lo = min(worst_lo, ex / ha)
            if ex < ha * (1 - 1e-12):
                fails += 1
            if k in tab.ball:
                eq_lo &= abs(ex - ha) <= 1e-12 * ha
            mask = sum(1 << x for x in order[:k])
            seg_lo &= abs(raw['G'][mask] - ex) <= 1e-12 * ex
        fails += (not eq_up) + (not eq_lo) + (not seg_up) + (not seg_lo)
        print("m=%d u=%.1f  subsets %6d   max exact/Harper (upper) %.6f [<=1]  equality at ball sizes: %s   "
              "min exact/Harper (lower) %.6f [>=1]  equality at ball sizes: %s   attained by simplicial segments at every size: %s / %s"
              % (m, u, (1 << n) - 2, worst_up, eq_up, worst_lo, eq_lo, seg_up, seg_lo))

print()
print("=" * 100)
print("B. (TU), (TL) with Harper's functions on random members of L_u(Q_m)")
print("=" * 100)
rng = np.random.default_rng(20261126)


def popcount_array(m):
    x = np.arange(1 << m)
    c = np.zeros(1 << m, dtype=np.int64)
    for i in range(m):
        c += (x >> i) & 1
    return c


def dist_to(m, z):
    x = np.arange(1 << m)
    d = x ^ z
    c = np.zeros(1 << m, dtype=np.int64)
    for i in range(m):
        c += (d >> i) & 1
    return c


def random_member(m, u, kind):
    n = 1 << m
    if kind == 0:        # lower McShane envelope of random values at random centres
        k = int(rng.integers(1, 9))
        psi = np.full(n, INF)
        for _ in range(k):
            psi = np.minimum(psi, rng.uniform(0, u * m) + u * dist_to(m, int(rng.integers(n))))
        return psi
    if kind == 1:        # upper envelope
        k = int(rng.integers(1, 9))
        psi = np.full(n, -INF)
        for _ in range(k):
            psi = np.maximum(psi, rng.uniform(0, u * m) - u * dist_to(m, int(rng.integers(n))))
        return psi
    if kind == 2:        # additive
        g = rng.uniform(-u, u, size=m)
        x = np.arange(n)
        return sum(g[i] * ((x >> i) & 1) for i in range(m))
    if kind == 3:        # cone with a flattened bottom
        z = int(rng.integers(n))
        R = int(rng.integers(0, m + 1))
        return u * np.maximum(dist_to(m, z), R).astype(float)
    # kind 4: dip of random depth on a random ball of a random member of kind 0
    psi = random_member(m, u, 0)
    z = int(rng.integers(n))
    c = rng.uniform(0, u * m / 2)
    return np.minimum(psi, psi[z] - c + u * dist_to(m, z))


names = ["min-envelope", "max-envelope", "additive", "flattened cone", "dip"]
for m in (6, 9, 12):
    for u in (0.5, 1.0, 2.0):
        tab = CubeTables(m, u)
        n = 1 << m
        worst = [0.0] * 5
        worstl = [INF] * 5
        cases = 0
        for kind in range(5):
            for rep in range(40 if m < 12 else 12):
                psi = random_member(m, u, kind)
                # Lipschitz check on all edges
                x = np.arange(n)
                for i in range(m):
                    assert np.max(np.abs(psi - psi[x ^ (1 << i)])) <= u + 1e-9
                W = np.exp(-(psi - psi.min()))
                vals = np.unique(W)
                Ws = np.sort(W)
                csum = np.concatenate(([0.0], np.cumsum(Ws)))
                levels = np.concatenate((vals, vals * math.exp(-0.37), vals * math.exp(0.41)))
                for s in levels:
                    cases += 1
                    k_gt = n - int(np.searchsorted(Ws, s, side='right'))      # |{W > s}|
                    k_ge = n - int(np.searchsorted(Ws, s, side='left'))       # |{W >= s}|
                    tail = (csum[n] - csum[n - k_gt] - s * k_gt) / n
                    if k_gt > 0:
                        xi = tab.Xi(k_gt / n)
                        if xi < INF:
                            ratio = tail / (s * xi)
                            worst[kind] = max(worst[kind], ratio)
                            if ratio > 1 + 1e-9:
                                fails += 1
                    if k_ge > 0:
                        trunc = (csum[n - k_ge] + s * k_ge) / n
                        ratio = trunc / (s * tab.Theta(k_ge / n))
                        worstl[kind] = min(worstl[kind], ratio)
                        if ratio < 1 - 1e-9:
                            fails += 1
        print("m=%2d u=%.1f  %6d levels   max E(W-s)_+/(s Xi(q)) by kind: %s   min E min(W,s)/(s Theta(p)): %s"
              % (m, u, cases, " ".join("%s %.4f" % (names[i], worst[i]) for i in range(5)),
                 " ".join("%.4f" % worstl[i] for i in range(5))))

print()
print("=" * 100)
print("C. weighted Hamming envelopes: the sorted-slope Harper bound against the exact tail function (uniform measure)")
print("   bound(q) = 2^-m sum_{j=1}^{r+1} (e^{U_j} - e^{U_{j-1}}) |B(m, r+1-j)|,  U_j = sum of the j largest slopes, r = r(q)")
print("=" * 100)


def sorted_slope_bound(m, us, q):
    tab = CubeTables(m, 1.0)
    if q * (1 << m) < 1 - 1e-12:
        return 0.0
    r = tab.radius(q)
    if r >= m:
        return INF
    U = np.concatenate(([0.0], np.cumsum(sorted(us, reverse=True))))
    tot = 0.0
    for j in range(1, r + 2):
        tot += (math.exp(U[j]) - math.exp(U[j - 1])) * tab.ball[r + 1 - j]
    return tot / (1 << m)


for m in (3, 4):
    n = 1 << m
    mu = np.full(n, 1.0 / n)
    sets = [("equal", [1.0] * m), ("two kinds", [2.0] * (m // 2) + [0.5] * (m - m // 2)),
            ("random", list(rng.uniform(0.2, 2.5, size=m))), ("one steep", [3.0] + [0.3] * (m - 1))]
    for name, us in sets:
        Xi_ex, Th_ex = envelope_tails(mu, weighted_matrix(m, us))
        worst = 0.0
        best = INF
        for k in range(1, n):
            q = k / n
            ex = Xi_ex(q)
            bd = sorted_slope_bound(m, us, q)
            if bd < INF:
                worst = max(worst, ex / bd)
                best = min(best, ex / bd)
                if ex > bd * (1 + 1e-12):
                    fails += 1
        print("m=%d slopes %-10s %s   exact/bound over all q: max %.4f [<=1], min %.4f"
              % (m, name, "[" + ", ".join("%.2f" % v for v in us) + "]", worst, best))

print()
print("=" * 100)
print("D. biased product measure Bernoulli(p)^4 with the Hamming envelope, slope u: the exact tail function of the")
print("   class under the measure itself, at the measures of the Hamming balls around 1111 and 0000 (for the record)")
print("=" * 100)
m = 4
n = 1 << m
Hd = hamming_matrix(m)
for (p, u) in [(0.3, 1.0), (0.2, 2.0)]:
    w = np.array([p ** bin(x).count("1") * (1 - p) ** (m - bin(x).count("1")) for x in range(n)])
    Xi_ex, Th_ex = envelope_tails(w, u * Hd)
    row = []
    for q in (0.001, 0.01, 0.05, 0.2, 0.5, 0.9):
        row.append("Xi(%.3f)=%.4g" % (q, Xi_ex(q)))
    print("p=%.1f u=%.1f   %s" % (p, u, "  ".join(row)))
    # validity on random members (sanity of the enumeration)
    for rep in range(200):
        psi = random_member(m, u, int(rng.integers(5)))
        W = np.exp(-psi)
        for s in np.unique(W):
            q = float(w[W > s].sum())
            if 0 < q < 1:
                tail = float((w * np.maximum(W - s, 0)).sum())
                if tail > s * Xi_ex(q) * (1 + 1e-9):
                    fails += 1
            pge = float(w[W >= s].sum())
            trunc = float((w * np.minimum(W, s)).sum())
            if trunc < s * Th_ex(pge) * (1 - 1e-9):
                fails += 1
print("   (TU), (TL) with the enumerated functions on 400 random members: checked")

print()
print("=" * 100)
print("E. two valid tail functions that use no isoperimetry (N_REPORT 4(e)), on the cube, against Harper's exact values")
print("   ball-volume:  Xi_in(q) = q (e^{u(r'+1)} - 1),  r' the largest radius with |B(r')| <= 2^m q")
print("   transport:    Xi_T(q)  = int_0^{um} e^r min{q, exp(-2 (r - r_0)_+^2/(m u^2))} dr,  r_0 = u sqrt(m ln(1/(1-q))/2)")
print("=" * 100)
from scipy import integrate


def xi_transport(m, u, q, lcomp):
    """lcomp = ln(1/(1-q)), computed from the exact counts"""
    sig2 = m * u * u
    r0 = math.sqrt(sig2 * lcomp / 2)
    lq = math.log(q)
    # min{q, e^{-2 (r - r0)^2/sig2}} = q for r <= rc := r0 + sqrt(sig2 ln(1/q)/2)
    rc = min(u * m, r0 + math.sqrt(sig2 * (-lq) / 2))
    part1 = q * math.expm1(rc)
    part2 = 0.0
    if rc < u * m:
        part2, _ = integrate.quad(lambda r: math.exp(r - 2 * (r - r0) ** 2 / sig2), rc, u * m, epsrel=1e-10)
    return part1 + part2


for m in (4, 12, 64, 256):
    for u in (0.5, 1.0, 2.0):
        if m * (u + 0.7) > 600:
            continue
        tab = CubeTables(m, u)
        worst_in, worst_T = 0.0, 0.0
        best_in, best_T = INF, INF
        for r in range(m):                                   # q = |B(r)|/2^m, where Harper's value is exact
            q = tab.ball[r] / tab.N
            ha = tab.E[r] / tab.N
            xin = q * math.expm1(u * (r + 1))
            lcomp = m * math.log(2.0) - math.log((1 << m) - tab.ball[r])
            xT = xi_transport(m, u, q, lcomp)
            worst_in, worst_T = max(worst_in, ha / xin), max(worst_T, ha / xT)
            best_in, best_T = min(best_in, ha / xin), min(best_T, ha / xT)
        if worst_in > 1 + 1e-9 or worst_T > 1 + 1e-9:
            fails += 1
        print("m=%3d u=%.1f  Harper/ball-volume over all ball sizes: max %.4f [<=1], min %.3g;   Harper/transport: max %.4f [<=1], min %.3g"
              % (m, u, worst_in, best_in, worst_T, best_T))

print()
print("violations:", fails, "   time %.1f s" % (time.time() - t0))
sys.exit(1 if fails else 0)
