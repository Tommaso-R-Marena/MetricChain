#!/usr/bin/env python3
"""Workstream I, experiment 4: is the single-letter (Chernoff) potential an approximate sub-solution of
the growth recursion?  Uniform cube, unit cost.  Potential:

    Gamma_n(d, t) = n * KL( max(pi(d/n) - t/n, 1/2) || 1/2 ),     KL(pi(delta) || 1/2) = delta,  pi in [1/2, 1],

the exponent of the ball {|x| >= pi n} grown by t.  The recursion needs, for all fibre exponents d0, d1
(d = -ln((e^{-d0} + e^{-d1})/2)):

    defect := -ln[ (1/2) max(G(d0,t), G(d1,t-1)) + (1/2) max(G(d1,t), G(d0,t-1)) ] - Gamma_{n+1}(d, t) <= eps_n,

G = exp(-Gamma_n).  If sup defect = O(1/n) the potential with a polynomial correction is inductive.
Floating point exploration."""
import math, sys
import numpy as np

LN2 = math.log(2.0)
def kl(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return LN2 + x * np.log(x) + (1 - x) * np.log1p(-x)

def pi_of(delta):
    """inverse of KL(.||1/2) on [1/2, 1], vectorised (bisection)."""
    delta = np.asarray(delta, dtype=float)
    lo = np.full(delta.shape, 0.5); hi = np.full(delta.shape, 1.0)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        big = kl(mid) < delta
        lo = np.where(big, mid, lo); hi = np.where(big, hi, mid)
    return 0.5 * (lo + hi)

def Gamma(n, d, t):
    d = np.minimum(np.maximum(d, 0.0), n * LN2)
    p = pi_of(d / n)
    return n * kl(np.maximum(p - t / n, 0.5))

def scan(n, nd=400):
    worst = (-1e9, None)
    dgrid = np.linspace(0.0, n * LN2, nd)
    for t in sorted(set([1, 2, 3, max(1, n // 20), max(1, n // 10), max(1, n // 5), max(1, n // 3)])):
        g_t = Gamma(n, dgrid, t); g_t1 = Gamma(n, dgrid, t - 1) if t >= 1 else None
        D0, D1 = np.meshgrid(dgrid, dgrid, indexing='ij')
        A0 = g_t[:, None] + 0 * D1; A1 = g_t[None, :] + 0 * D0
        B0 = g_t1[:, None] + 0 * D1; B1 = g_t1[None, :] + 0 * D0
        lhs = -np.log(0.5 * np.exp(-np.minimum(A0, B1)) + 0.5 * np.exp(-np.minimum(A1, B0)))
        d = -np.log(0.5 * np.exp(-D0) + 0.5 * np.exp(-D1))
        rhs = Gamma(n + 1, d, t)
        df = lhs - rhs
        i = np.unravel_index(np.argmax(df), df.shape)
        if df[i] > worst[0]:
            worst = (float(df[i]), (t, float(D0[i]), float(D1[i]), float(d[i]), float(lhs[i]), float(rhs[i])))
    return worst

for n in (20, 50, 100, 200, 400, 800):
    w, info = scan(n)
    t, d0, d1, d, lhs, rhs = info
    print(f"n={n:4d}: sup defect = {w:+.5f}  (n*defect = {n*w:+.3f})  at t={t}, d0={d0:.3f}, d1={d1:.3f}, d={d:.3f}, lhs={lhs:.4f}, rhs={rhs:.4f}")
