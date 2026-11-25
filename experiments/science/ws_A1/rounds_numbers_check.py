#!/usr/bin/env python3
"""Workstream A1 -- independent re-computation of two headline NUMBERS of the round hierarchy (theory report
sect. 11.24) from the formulas as printed there.  This replicates the evaluation of the formulas, not their proofs.

  U  two-round upper value   T2(0) = min_{phi, xi} max{ phi a + (1-phi) theta_na(xi) ,  min(phi a, (1-phi) xi) + (1-phi) a }
     (Theorem 11.84(b));  report:  T2(0)/a = 0.620, 0.624, 0.641, 0.665 at u = 0.5, 1, 2, 3; golden ratio 0.618 as u -> 0.
  L  two-round lower value   theta2* = sup{ theta : Xi(theta, phi1) > 0 and theta < phi2 a for some phi1 },
     Xi(theta, phi1) = min_{0 <= c <= min(theta, phi1 a)} [ phi1 x_na(c/phi1) + phi2 D((theta - c)/phi2) ],
     D(t) = u f^{-1}(t) - Lambda_1,  x_na(t) = D(t) + t,  f(rho) = KL(rho || 1/2)   (Theorem 11.86);
     report: theta2*/a = 0.349, 0.359, 0.394, 0.440 at u = 0.5, 1, 2, 3  and  theta2*/h = 1.38, 1.37, 1.33, 1.28.
Run: python3 rounds_numbers_check.py  (about 1 min)
"""
import math, sys
import numpy as np
from scipy.optimize import brentq, minimize_scalar

LN2 = math.log(2)
def kl(a, b):
    o = 0.0
    if a > 0: o += a * math.log(a / b)
    if a < 1: o += (1 - a) * math.log((1 - a) / (1 - b))
    return o
def finv(t):                       # rho in [0, 1/2] with KL(rho||1/2) = t
    if t <= 0: return 0.5
    if t >= LN2: return 0.0
    return brentq(lambda r: kl(r, 0.5) - t, 1e-300, 0.5, xtol=1e-15)

fails = 0
def check(name, ok, info=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + ("   " + info if info else "")); fails += (not ok)

rep_U = {0.5: 0.620, 1.0: 0.624, 2.0: 0.641, 3.0: 0.665}
rep_L = {0.5: 0.349, 1.0: 0.359, 2.0: 0.394, 3.0: 0.440}
rep_Lh = {0.5: 1.38, 1.0: 1.37, 2.0: 1.33, 3.0: 1.28}
rowsU, rowsL, okU, okL = [], [], True, True
for u in (0.5, 1.0, 2.0, 3.0):
    pu = 1 / (1 + math.exp(u)); Lam = math.log(2 / (1 + math.exp(-u)))
    a = kl(pu, 0.5); h = kl(Lam / u, 0.5); estar = math.log(math.cosh(u / 2))
    def theta_na(e):
        if e >= estar: return 0.0
        if e <= 0: return a
        return kl(brentq(lambda r: kl(r, pu) - e, pu, 0.5, xtol=1e-15), 0.5)
    # ---- U: for fixed phi the first term decreases in xi, the second increases: minimise max over xi by scalar search
    def inner(phi):
        f = lambda xi: max(phi * a + (1 - phi) * theta_na(xi), min(phi * a, (1 - phi) * xi) + (1 - phi) * a)
        grid = np.linspace(1e-6, estar, 400)
        k = int(np.argmin([f(x) for x in grid]))
        lo, hi = grid[max(k - 1, 0)], grid[min(k + 1, 399)]
        return minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-12}).fun
    gridp = np.linspace(0.02, 0.98, 97)
    vals = [inner(p) for p in gridp]
    k = int(np.argmin(vals))
    T2 = minimize_scalar(inner, bounds=(gridp[max(k - 1, 0)], gridp[min(k + 1, 96)]), method="bounded", options={"xatol": 1e-10}).fun
    rowsU.append("u=%.1f: T2(0)/a = %.4f (report %.3f)" % (u, T2 / a, rep_U[u]))
    okU &= abs(T2 / a - rep_U[u]) < 1.5e-3
    # ---- L
    D = lambda t: u * finv(t) - Lam
    xna = lambda t: D(t) + t
    def Xi(theta, phi1):
        phi2 = 1 - phi1
        cmax = min(theta, phi1 * a)
        g = lambda c: phi1 * xna(c / phi1) + phi2 * D((theta - c) / phi2)
        cs = np.linspace(0.0, cmax, 600)
        v = [g(c) for c in cs]
        k = int(np.argmin(v))
        lo, hi = cs[max(k - 1, 0)], cs[min(k + 1, 599)]
        return min(v[k], minimize_scalar(g, bounds=(lo, hi), method="bounded", options={"xatol": 1e-13}).fun)
    best = 0.0
    for phi1 in np.linspace(0.30, 0.85, 56):
        phi2 = 1 - phi1
        top = phi2 * a * (1 - 1e-9)
        if Xi(h, phi1) <= 0 or top <= h:
            continue
        if Xi(top, phi1) > 0:
            th = top
        else:
            th = brentq(lambda t: Xi(t, phi1), h, top, xtol=1e-9)
        best = max(best, th)
    rowsL.append("u=%.1f: theta2*/a = %.4f (report %.3f), theta2*/h = %.3f (report %.2f)" % (u, best / a, rep_L[u], best / h, rep_Lh[u]))
    okL &= abs(best / a - rep_L[u]) < 2.5e-3 and abs(best / h - rep_Lh[u]) < 1.2e-2
check("U  two-round upper value T2(0)/a re-computed from the printed formula", okU, "; ".join(rowsU))
check("L  two-round lower value theta2*/a, theta2*/h re-computed from the printed formula", okL, "; ".join(rowsL))
# small-slope limit of U: golden ratio
u = 0.02
pu = 1 / (1 + math.exp(u)); Lam = math.log(2 / (1 + math.exp(-u))); a = kl(pu, 0.5); estar = math.log(math.cosh(u / 2))
def theta_na(e):
    if e >= estar: return 0.0
    if e <= 0: return a
    return kl(brentq(lambda r: kl(r, pu) - e, pu, 0.5, xtol=1e-16), 0.5)
def inner(phi):
    f = lambda xi: max(phi * a + (1 - phi) * theta_na(xi), min(phi * a, (1 - phi) * xi) + (1 - phi) * a)
    grid = np.linspace(estar * 1e-6, estar, 2000)
    return min(f(x) for x in grid)
T2 = min(inner(p) for p in np.linspace(0.2, 0.8, 301))
check("U' small-slope limit: T2(0)/a -> (sqrt(5)-1)/2 = 0.618", abs(T2 / a - 0.6180) < 2e-3, "at u = 0.02: %.4f" % (T2 / a))
print("\nfailures: %d" % fails); sys.exit(1 if fails else 0)
