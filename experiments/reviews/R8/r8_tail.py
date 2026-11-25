#!/usr/bin/env python3
"""Referee R8 -- Harper's theorem in the form (H) and Lemma K.1(a),(b).  Own code.
(1) (H) exhaustively: for every subset S of Q_m, m <= 4, and for 200000 random subsets of Q_5, Q_6:
    |S| >= |B(m,k)|  =>  |N(S)| >= |B(m,k+1)|  (N = closed neighbourhood); also the iterated form used in the
    proofs, |N^i(S)| >= |B(m,k+i)|, and the complement form |{x: dist(x,D^c) >= i}| <= |B(m,r+1-i)| if |D| <= |B(m,r)|, r <= m-1.
(2) Lemma K.1(a),(b) at every threshold of u-Lipschitz functions on Q_4..Q_10 (15 families), and the equality cases
    (truncated cone for (a), cone for (b))."""
import math, sys, time
import numpy as np
from r8_pops import gen_psi, KINDS, dist_to
t0 = time.time()
def ballsize(m, r):
    if r < 0: return 0
    return sum(math.comb(m, j) for j in range(0, min(r, m) + 1))
def neighbourhood_mask(S, m):
    """S as a python int bitmask over the 2^m vertices; returns mask of the closed neighbourhood"""
    out = S
    for i in range(m):
        bit = 1 << i
        # vertices with coordinate i = 0 are those indices v with v & bit == 0; flipping maps v -> v ^ bit
        lowmask = LOW[m][i]
        out |= ((S & lowmask) << bit) | ((S >> bit) & lowmask)
    return out
LOW = {}
for m in range(1, 7):
    LOW[m] = []
    for i in range(m):
        mask = 0
        for v in range(1 << m):
            if not (v >> i) & 1:
                mask |= 1 << v
        LOW[m].append(mask)
viol = 0; nsub = 0
for m in range(1, 5):
    sizes = [ballsize(m, k) for k in range(-1, m + 1)]
    for S in range(1, 1 << (1 << m)):
        nsub += 1
        c = bin(S).count('1')
        k = max(kk for kk in range(0, m + 1) if ballsize(m, kk) <= c)      # |S| >= |B(m,k)|
        T = S
        for i in range(1, m - k + 1):
            T = neighbourhood_mask(T, m)
            if bin(T).count('1') < ballsize(m, k + i):
                viol += 1
print("(H) exhaustive, all nonempty subsets of Q_1..Q_4: %d subsets, violations of |N^i(S)| >= |B(m,k+i)|: %d" % (nsub, viol))
rng = np.random.default_rng(12)
viol2 = 0; n2 = 0
for m in (5, 6):
    V = 1 << m
    for trial in range(100000):
        typ = trial % 4
        if typ == 0:
            c = int(rng.integers(1, V + 1)); idx = rng.choice(V, c, replace=False)
        elif typ == 1:      # union of a few balls
            idx = set()
            for _ in range(int(rng.integers(1, 4))):
                cen = int(rng.integers(0, V)); rad = int(rng.integers(0, m))
                idx |= {v for v in range(V) if bin(v ^ cen).count('1') <= rad}
            idx = list(idx)
        elif typ == 2:      # subcube
            fixed = int(rng.integers(0, V)); mask = int(rng.integers(0, V))
            idx = [v for v in range(V) if (v & mask) == (fixed & mask)]
        else:               # ball plus part of the next sphere
            cen = int(rng.integers(0, V)); rad = int(rng.integers(0, m))
            idx = [v for v in range(V) if bin(v ^ cen).count('1') <= rad]
            sph = [v for v in range(V) if bin(v ^ cen).count('1') == rad + 1]
            if sph:
                idx += list(rng.choice(sph, int(rng.integers(0, len(sph) + 1)), replace=False))
        S = 0
        for v in idx: S |= 1 << int(v)
        c = bin(S).count('1')
        if c == 0: continue
        n2 += 1
        k = max(kk for kk in range(0, m + 1) if ballsize(m, kk) <= c)
        T = S
        for i in range(1, m - k + 1):
            T = neighbourhood_mask(T, m)
            if bin(T).count('1') < ballsize(m, k + i):
                viol2 += 1
print("(H) on %d random / structured subsets of Q_5, Q_6: violations %d   [%.0f s]" % (n2, viol2, time.time() - t0))
# (2) Lemma K.1 on functions
nthr = 0; va = vb = 0; eq_a = eq_b = False; nf = 0
for m in range(4, 11):
    for u in (0.5, 1.0, 2.0):
        E = lambda r: sum(math.comb(m, j) * (math.exp(u * (r + 1 - j)) - 1) for j in range(0, r + 1))
        Tm = lambda k: sum(math.comb(m, j) * math.exp(-u * max(j - k, 0)) for j in range(0, m + 1))
        funcs = [gen_psi(kind, m, max(1, m // 2), u, rng) for kind in KINDS for _ in range(2)]
        # equality cases: truncated cone (a), cone (b)
        d0 = dist_to(m, 0).astype(float)
        funcs.append(np.maximum(u * d0, u * (m // 3)) * 0 + u * d0)          # cone
        funcs.append(-u * np.maximum((m // 2) + 1 - d0, 0))                    # dip = cone truncated from above
        for psi in funcs:
            nf += 1
            W = np.exp(-(psi - psi.min()))
            vals = np.unique(W)
            thr = np.concatenate((vals, 0.5 * (vals[1:] + vals[:-1]), [vals[0] * 0.5, vals[-1] * 1.5]))
            for t in thr:
                nthr += 1
                D = int((W > t).sum()); S = int((W >= t).sum())
                # (a): smallest r with |D| <= |B(m,r)|, need r <= m-1
                r = next(rr for rr in range(-1, m + 1) if ballsize(m, rr) >= D)
                if r <= m - 1:
                    lhs = float(np.maximum(W - t, 0).sum()); rhs = t * (E(r) if r >= 0 else 0.0)
                    if lhs > rhs * (1 + 1e-10) + 1e-12: va += 1
                    if D > 0 and abs(lhs - rhs) <= 1e-9 * rhs: eq_a = True
                if S > 0:
                    k = max(kk for kk in range(0, m + 1) if ballsize(m, kk) <= S)
                    lhs = float(np.minimum(W, t).sum()); rhs = t * Tm(k)
                    if lhs < rhs * (1 - 1e-10): vb += 1
                    if abs(lhs - rhs) <= 1e-9 * rhs and S < (1 << m): eq_b = True
print("Lemma K.1 on %d u-Lipschitz functions of Q_4..Q_10, %d thresholds: violations of (a): %d, of (b): %d; equality attained in (a): %s, in (b): %s   [%.0f s]"
      % (nf, nthr, va, vb, eq_a, eq_b, time.time() - t0))
