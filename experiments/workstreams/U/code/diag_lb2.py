#!/usr/bin/env python3
"""Test of the asymptotic formula of Theorem U3 against exact finite-n values.

For fixed phi1 and several T/n: exact ln A(F_D)/n and ln A(F_S)/n (lb2_exact.build, with cap), against the prediction
    lim n^{-1} ln A(F_D) = min( Xi_theta(phi1), phi2 * KL(y1 || p_u) )_+ ,   phi2 f(y1) = theta,
    lim n^{-1} ln A(F_S) = 0,
with theta read at finite n as the effective exponent -ln(p1)/n.  The convergence is O(log n / n).
Also the first (uncapped) version, for the record of the failed attempt: there ln A(F_S)/n does not vanish.
usage: diag_lb2.py [phi1]
"""
import sys, math
import numpy as np
from ulib import Cube, f, finv
from lb2_exact import build, lnA
from lb2_exponent import Xi_cube

u = 1.0
cube = Cube(u)
phi1 = float(sys.argv[1]) if len(sys.argv) > 1 else 0.6
print(f"u={u} phi1={phi1} a={cube.a:.5f} h={cube.h:.5f}")
print("n | T/n | theta_eff=-ln(p1)/n | exact lnA(F_D)/n, lnA(F_S)/n | predicted min(Xi, phi2 k(y1)) [Xi, phi2 k(y1)] | uncapped: lnA(deep)/n, lnA(sh)/n")
for n in (1600, 6400, 12800):
    n1 = int(round(phi1 * n)); n2 = n - n1
    for th in (0.030, 0.034, 0.038, 0.042):
        B = build(u, n1, n2, th * n, balance=False, cap=True)
        aD, aS = lnA(B, "F") / n, lnA(B, "Fs") / n
        th1 = -B["lnp1"] / n
        xi = Xi_cube(cube, th1, phi1, 800)
        y1 = finv(th1 / (1 - phi1))
        kk = (1 - phi1) * float(cube.kl_pu(y1)) if y1 > cube.pu else 0.0
        pred = max(0.0, min(xi, kk))
        del B
        B0 = build(u, n1, n2, th * n, balance=False, cap=False)
        bD, bS = lnA(B0, "F") / n, lnA(B0, "Fs") / n
        del B0
        print(f"{n} | {th:.3f} | {th1:.5f} | {aD:+.5f} {aS:+.5f} | {pred:+.5f} [{xi:+.5f}, {kk:+.5f}] | {bD:+.5f} {bS:+.5f}", flush=True)
