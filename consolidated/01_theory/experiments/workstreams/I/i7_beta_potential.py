#!/usr/bin/env python3
"""Workstream I, experiment 7: is the real-radius binomial profile an exact sub-solution of the growth
recursion?  For a site law (q0, q1) = (1 - p, p), balls around the all-ones vertex of real radius rho,

    beta_n(rho) := P( Bin(n, q0) <= rho ) interpolated by the regularised incomplete beta function
                 = I_{q1}(n - rho, rho + 1)          (rho in (-1, n)),

Pascal's rule beta_{n+1}(rho) = q1 beta_n(rho) + q0 beta_n(rho - 1) holds for real rho.  Candidate bound
G_n(m, t) = beta_n(beta_n^{-1}(m) + t).  Recursion (fibres of real radii a at letter 0, b at letter 1):

    q0 max(beta_n(a + t), beta_n(b + t - 1)) + q1 max(beta_n(b + t), beta_n(a + t - 1))  >=  beta_{n+1}(R + t),
    beta_{n+1}(R) = q0 beta_n(a) + q1 beta_n(b).

Prints the largest violation  ln(RHS/LHS)  over a grid of (a, b, t).  Floating point exploration."""
import sys, math
import numpy as np
from scipy.special import betainc
from scipy.optimize import brentq

def beta(n, q1, rho):
    rho = np.asarray(rho, dtype=float)
    out = np.where(rho >= n, 1.0, 0.0)
    mid = (rho > -1) & (rho < n)
    r = np.where(mid, rho, 0.0)
    return np.where(mid, betainc(np.maximum(n - r, 1e-300), r + 1, q1), out)

def inv_beta(n, q1, m):
    if m <= 0: return -1.0
    if m >= 1: return float(n)
    f = lambda r: float(beta(n, q1, r)) - m
    return brentq(f, -1 + 1e-12, n - 1e-12, xtol=1e-13)

def scan(n, q1, ts, na=140):
    q0 = 1 - q1
    worst = (-1e9, None)
    radii = np.linspace(-0.999, n - 0.001, na)
    for t in ts:
        for a in radii:
            for b in radii:
                m = q0 * float(beta(n, q1, a)) + q1 * float(beta(n, q1, b))
                if m <= 1e-300 or m >= 1 - 1e-15: continue
                R = inv_beta(n + 1, q1, m)
                rhs = float(beta(n + 1, q1, R + t))
                lhs = q0 * max(float(beta(n, q1, a + t)), float(beta(n, q1, b + t - 1))) \
                    + q1 * max(float(beta(n, q1, b + t)), float(beta(n, q1, a + t - 1)))
                if lhs <= 0: continue
                v = math.log(rhs / lhs)
                if v > worst[0]:
                    worst = (v, (t, a, b, m, lhs, rhs))
    return worst

if __name__ == "__main__":
    for (n, q1) in ((6, 0.5), (12, 0.5), (24, 0.5), (12, 0.2), (24, 0.2), (12, 0.8)):
        w, info = scan(n, q1, ts=[1, 2, max(1, n // 4)], na=90 if n <= 12 else 70)
        t, a, b, m, lhs, rhs = info
        print(f"n={n:3d} q1={q1}: largest ln(RHS/LHS) = {w:+.6f}  at t={t}, a={a:.3f}, b={b:.3f}, m={m:.3e}, lhs={lhs:.6e}, rhs={rhs:.6e}")
