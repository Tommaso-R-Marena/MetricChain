#!/usr/bin/env python3
"""Two-round lower bound, exponent level (Theorem U3 of the report).

Family: two blocks of sizes phi1*n, phi2*n; block 1 carries the "flat-histogram" profile
g(d1) = -ln( P(shell d1 typical) / P(shell d1) ) wherever that is u-Lipschitz; the instance is the lower McShane
envelope of g from the set V1 = {rate <= theta} that a blind batch of e^{n theta} points sees, its twin the upper
McShane envelope from V2 = {block-2 rate <= theta}.

Hidden gain (exponent of A(deep)/A(visible)), with c = block-1 cost of the anchor shell:
    E_theta(c) = phi1 * x_na(c/phi1) + phi2 * D((theta - c)/phi2),   0 <= c <= min(theta, phi1*a),
    Xi(theta, phi1) = min_c E_theta(c).
Two rounds with batches below e^{n theta} fail whenever  Xi > 0  and  theta < phi2 * a.
theta2*(phi1) = min( phi2*a, sup{theta : Xi(theta, phi1) > 0} ),  theta2* = max over phi1.

Small-slope limit (units a = 1, h = 1/4): x_na(t) = (1 - sqrt t)^2, D(t) = 1 - 2 sqrt t.
usage: lb2_exponent.py
"""
import math, sys
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from ulib import Cube, f, finv


def Xi_cube(cube, theta, phi1, ngrid=4000):
    phi2 = 1 - phi1
    cmax = min(theta, phi1 * cube.a)
    cs = np.linspace(0.0, cmax, ngrid)
    best = 1e9
    for c in cs:
        b = (theta - c) / phi2
        if b >= math.log(2):
            continue
        val = phi1 * cube.x_na(c / phi1) + phi2 * cube.D(b)
        best = min(best, val)
    # refine by bounded minimisation
    def E(c):
        return phi1 * cube.x_na(c / phi1) + phi2 * cube.D((theta - c) / phi2)
    res = minimize_scalar(E, bounds=(0.0, cmax), method="bounded", options=dict(xatol=1e-12))
    return min(best, res.fun)


def theta_star_cube(cube, phi1):
    phi2 = 1 - phi1
    lo, hi = cube.h * 0.5, min(cube.a, 0.999 * math.log(2) * phi2)
    if Xi_cube(cube, hi, phi1, 400) > 0:
        thE = hi
    else:
        thE = brentq(lambda t: Xi_cube(cube, t, phi1, 400), lo, hi, xtol=1e-10)
    return min(thE, phi2 * cube.a), thE


def Xi_gauss(theta, phi1):
    phi2 = 1 - phi1
    cmax = min(theta, phi1)
    def E(c):
        return phi1 * (1 - math.sqrt(c / phi1)) ** 2 + phi2 * (1 - 2 * math.sqrt(max(theta - c, 0.0) / phi2))
    res = minimize_scalar(E, bounds=(0.0, cmax), method="bounded", options=dict(xatol=1e-13))
    cs = np.linspace(0, cmax, 2001)
    return min(res.fun, min(E(c) for c in cs))


def theta_star_gauss(phi1):
    phi2 = 1 - phi1
    hi = min(1.0, phi2 * 0.999999)
    if Xi_gauss(hi, phi1) > 0:
        thE = hi
    else:
        thE = brentq(lambda t: Xi_gauss(t, phi1), 0.2, hi, xtol=1e-12)
    return min(thE, phi2), thE


if __name__ == "__main__":
    print("== small-slope limit (a = 1, h = 0.25) ==")
    best = (0, None)
    for phi1 in np.linspace(0.05, 0.9, 171):
        t, tE = theta_star_gauss(phi1)
        if t > best[0]:
            best = (t, phi1, tE)
    print(f"theta2* = {best[0]:.6f}  at phi1 = {best[1]:.4f}  (root of Xi: {best[2]:.6f});  h = 0.25")
    for phi1 in (0.1, 0.3, 0.5, 0.6, 0.65, 0.7, 0.8):
        t, tE = theta_star_gauss(phi1)
        print(f"   phi1={phi1:.2f}: Xi(h)={Xi_gauss(0.25, phi1):+.5f}  root of Xi={tE:.5f}  phi2*a={1-phi1:.3f}  theta2*(phi1)={t:.5f}")
    print()
    for u in (0.25, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0):
        cube = Cube(u)
        best = (0, None, None)
        for phi1 in np.linspace(0.05, 0.9, 86):
            t, tE = theta_star_cube(cube, phi1)
            if t > best[0]:
                best = (t, phi1, tE)
        # refine around the best phi1
        p0 = best[1]
        for phi1 in np.linspace(max(0.02, p0 - 0.01), min(0.95, p0 + 0.01), 41):
            t, tE = theta_star_cube(cube, phi1)
            if t > best[0]:
                best = (t, phi1, tE)
        print(f"u={u}: a={cube.a:.6f} h={cube.h:.6f} h/a={cube.h/cube.a:.4f}  theta2*={best[0]:.6f}  theta2*/a={best[0]/cube.a:.4f}  theta2*/h={best[0]/cube.h:.4f}  at phi1={best[1]:.4f}")
        for phi1 in (0.3, 0.5, 0.65):
            t, tE = theta_star_cube(cube, phi1)
            print(f"   phi1={phi1:.2f}: Xi(h)={Xi_cube(cube, cube.h, phi1):+.6f}  root={tE/cube.a:.4f}a  phi2*a={(1-phi1):.3f}a  theta2*(phi1)={t/cube.a:.4f}a")
