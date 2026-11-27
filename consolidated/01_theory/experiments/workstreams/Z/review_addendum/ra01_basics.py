#!/usr/bin/env python3
"""RA01 -- basics: the constants of the brief; the slope map computed in two independent ways (through J, and as the
supremum over e from theta_na itself); J against inf_e; theta_hint closed form against sup_t [J - t g]; the Gaussian
closed form; the convex-envelope routine against a brute-force definition; Sigma >= s + B/h - 1 (the bound used in A6).
Usage: python3 -B ra01_basics.py
"""
import math
import random

import numpy as np

import ra_lib as R

random.seed(12345)
np.random.seed(12345)

print("== constants ==")
for P in (R.Cube(1.0).setup(), R.Cube(2.0).setup(), R.Cube(0.5).setup(), R.Gauss().setup()):
    print("%-14s a = %.8f  h = %.8f  L = %.6f  theta_hint''(0) = %.6f  c_*^2 = %.8f  h/a = %.5f  eps* = %.6f  1 - h/a = %.5f"
          % (P.name, P.a, P.h, P.L, P.vartheta, P.cstar2, P.h / P.a, P.epsstar, 1 - P.h / P.a))
P = R.Cube(1.0).setup()
print("brief (cube u = 1): a = 0.110944, h = 0.029139, L = 0.4900, theta_hint''(0) = 4.245, c_*^2 = 0.071147")
rho_h = P.Lam_u / P.u
print("cube u = 1: theta_hint''(0) = 1/(u^2 rho_h (1 - rho_h)) = %.6f;  theta(h) - h = %.2e;  theta'(0+) check: theta(1e-10)/a = %.6f"
      % (1 / (P.u ** 2 * rho_h * (1 - rho_h)), P.theta(P.h) - P.h, P.theta(1e-10) / P.a))

print("\n== J (closed form) against inf_e [(1-t) theta(e) + t e] from theta itself ==")
for P in (R.Cube(1.0).setup(), R.Cube(2.0).setup(), R.Gauss().setup()):
    worst = 0.0
    for t in np.linspace(0.02, 0.98, 49):
        worst = max(worst, abs(P.J(t) - P.J_direct(t)))
    print("%-14s max |J - J_direct| over 49 values of t: %.2e" % (P.name, worst))

print("\n== Sigma through J against the supremum over e from theta itself (random regular points) ==")
for P in (R.Cube(1.0).setup(), R.Cube(2.0).setup(), R.Cube(0.5).setup(), R.Gauss().setup()):
    worst_rel, n = 0.0, 0
    worst_vec = 0.0
    pts = []
    while n < 300:
        s = random.uniform(0.0, 0.98)
        B = random.uniform(0.0, 1.0) * (1.0 - s) * P.a * 0.995
        v1 = P.sigma(B, s)
        v2 = P.sigma_direct(B, s)
        worst_rel = max(worst_rel, abs(v1 - v2) / max(1e-12, abs(v1)))
        pts.append((B, s, v1))
        n += 1
    Bs = np.array([p[0] for p in pts])
    ss = np.array([p[1] for p in pts])
    vv = P.sigma_vec(Bs, ss)
    worst_vec = float(np.max(np.abs(vv - np.array([p[2] for p in pts])) / np.maximum(1e-12, np.abs(vv))))
    extra = ""
    if isinstance(P, R.Gauss):
        cf = Bs * (1 - ss) / (1 - ss - Bs)
        extra = ";  against B(1-s)/(1-s-B): %.2e" % float(np.max(np.abs(cf - np.array([p[2] for p in pts])) / cf))
    print("%-14s 300 points: max rel. difference J-route vs direct sup = %.2e;  scalar vs vectorised = %.2e%s"
          % (P.name, worst_rel, worst_vec, extra))

print("\n== partial derivatives of Sigma (1/e*, theta(e*)/e*) against finite differences ==")
for P in (R.Cube(1.0).setup(), R.Gauss().setup()):
    worst = 0.0
    for _ in range(200):
        s = random.uniform(0.0, 0.9)
        B = random.uniform(0.05, 0.9) * (1.0 - s) * P.a
        S, SB, Ss = P.sigma_grad(B, s)
        d = 1e-6
        fB = (P.sigma(B + d * P.a, s) - P.sigma(B - d * P.a, s)) / (2 * d * P.a)
        fs = (P.sigma(B, s + d) - P.sigma(B, s - d)) / (2 * d)
        worst = max(worst, abs(fB - SB) / SB, abs(fs - Ss) / max(Ss, 1e-9))
    print("%-14s max rel. error of the analytic partials: %.2e" % (P.name, worst))

print("\n== Sigma(B, s) >= s + B/h - 1 (the rate e = h; used for the fixed-rate sequence of A6) and Sigma(h, L) = L ==")
for P in (R.Cube(1.0).setup(), R.Cube(2.0).setup(), R.Gauss().setup()):
    worst = math.inf
    for _ in range(2000):
        s = random.uniform(0.0, 0.99)
        B = random.uniform(0.0, 1.0) * (1.0 - s) * P.a * 0.999
        worst = min(worst, P.sigma(B, s) - (s + B / P.h - 1.0))
    print("%-14s min over 2000 points of Sigma - (s + B/h - 1) = %.3e;   Sigma(h, L) - L = %.2e;  L < 1 - h/a: %s"
          % (P.name, worst, P.sigma(P.h, P.L) - P.L, P.L < 1 - P.h / P.a))

print("\n== joint convexity and monotonicity of Sigma (random midpoints) ==")
for P in (R.Cube(1.0).setup(), R.Gauss().setup()):
    worst = -math.inf
    mono = -math.inf
    for _ in range(3000):
        s1, s2 = random.uniform(0.0, 0.95), random.uniform(0.0, 0.95)
        B1 = random.uniform(0.0, 1.0) * (1.0 - s1) * P.a * 0.99
        B2 = random.uniform(0.0, 1.0) * (1.0 - s2) * P.a * 0.99
        mid = P.sigma(0.5 * (B1 + B2), 0.5 * (s1 + s2))
        worst = max(worst, mid - 0.5 * (P.sigma(B1, s1) + P.sigma(B2, s2)))
        if B1 <= B2 and s1 <= s2:
            mono = max(mono, P.sigma(B1, s1) - P.sigma(B2, s2))
    print("%-14s max of Sigma(mid) - mean (must be <= 0): %.2e;   max violation of monotonicity: %.2e" % (P.name, worst, mono))

print("\n== theta_hint: closed form against sup_t [J(t) - t g] ==")
for P in (R.Cube(1.0).setup(), R.Cube(2.0).setup(), R.Gauss().setup()):
    worst = 0.0
    for g in list(np.linspace(0.0, 1.3 * P.epsstar, 27)):
        worst = max(worst, abs(P.theta_hint(g) - P.theta_hint_sup(g)))
    d = 1e-4
    print("%-14s max difference: %.2e;  theta_hint(0) - h = %.2e, -theta_hint'(0) - L = %.2e, theta_hint''(0) - vartheta = %.2e"
          % (P.name, worst, P.theta_hint(0.0) - P.h, -(P.theta_hint(d) - P.theta_hint(0)) / d - P.L + 0.5 * d * P.vartheta,
             (P.theta_hint(2 * d) - 2 * P.theta_hint(d) + P.theta_hint(0.0)) / d ** 2 - P.vartheta))

print("\n== the convex-envelope routine against the brute-force definition (random data, 200 cases of 40 points) ==")
worst = 0.0
for _ in range(200):
    x = np.sort(np.random.rand(40))
    x[0], x[-1] = 0.0, 1.0
    y = np.random.rand(40) if random.random() < 0.5 else np.minimum(1.0, 3 * x ** 2 + 0.3 * np.random.rand(40))
    e, _ = R.lower_env(x, y)
    worst = max(worst, float(np.max(np.abs(e - R.lower_env_bruteforce(x, y)))))
print("max difference: %.2e" % worst)
