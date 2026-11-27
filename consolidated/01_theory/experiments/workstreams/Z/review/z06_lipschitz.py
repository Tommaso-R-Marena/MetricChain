#!/usr/bin/env python3
"""z06: Lemma Z1a of Z_REPORT.md -- phi -> Psi_g(phi; B, s) = (1 - phi) B + (1 - s) phi theta_na(g/phi) is convex on (0, 1] and
a-Lipschitz for 0 <= B <= a, 0 <= s <= 1 -- on random arguments, including rates g/phi beyond eps* (theta_na = 0) and phi near
0 and 1; and the rounding step of Proposition Z3: for every phi* in (0, 1) and d > d_min there is an admissible fraction
n_o/d (1 <= n_o <= d - d_min + 1) within max(1, d_min - 1)/d <= d_min/d of phi*."""
import math
import sys

import numpy as np

sys.dont_write_bytecode = True
import zrev

rng = np.random.default_rng(5)
for u in (0.25, 0.5, 1.0, 2.0, 4.0):
    cu = zrev.Cube(u)
    n = 400000
    g = 10.0 ** rng.uniform(-7, math.log10(3 * u), n)
    kind = rng.integers(0, 4, n)
    phi1 = np.where(kind == 0, 10.0 ** rng.uniform(-9, 0, n), np.where(kind == 1, 1 - 10.0 ** rng.uniform(-9, 0, n), rng.uniform(0, 1, n)))
    phi2 = np.where(rng.random(n) < 0.5, np.clip(phi1 * (1 + rng.normal(0, 1e-3, n)), 1e-12, 1.0), rng.uniform(1e-9, 1, n))
    phi1 = np.clip(phi1, 1e-12, 1.0)
    B = np.where(rng.random(n) < 0.3, cu.a, rng.uniform(0, cu.a, n))
    B = np.where(rng.random(n) < 0.15, 0.0, B)
    s = np.where(rng.random(n) < 0.3, 0.0, rng.uniform(0, 1, n))

    def Psi(ph):
        return (1 - ph) * B + (1 - s) * ph * cu.theta_v(g / ph)
    p1, p2 = Psi(phi1), Psi(phi2)
    ok = np.abs(phi1 - phi2) > 1e-7          # below that the difference quotient is dominated by rounding (|Psi| ~ a, eps ~ 1e-17)
    ratio = np.abs(p1 - p2)[ok] / np.abs(phi1 - phi2)[ok]
    # convexity: midpoint
    pm = Psi(0.5 * (phi1 + phi2))
    conv = float(np.max(pm - 0.5 * (p1 + p2)))
    print("u = %g: %d random (g, phi, phi', B, s): max |Psi - Psi'|/|phi - phi'| = %.6f a  (a = %.6f; Lipschitz constant a: %s);  max midpoint excess %.1e (convex: %s)"
          % (u, int(ok.sum()), float(ratio.max()) / cu.a, cu.a, bool(ratio.max() <= cu.a * (1 + 1e-8)), conv, conv <= 1e-12))
# the rounding step
worst = 0.0
for u in (0.05, 0.25, 0.5, 1.0, 2.0):
    dm = int(math.floor(1 / (2 * u))) + 2
    for d in list(range(dm + 1, dm + 60)) + [1000, 12345]:
        adm = np.arange(1, d - dm + 2) / d
        ps = np.concatenate([np.linspace(1e-12, 1 - 1e-12, 20001), 10.0 ** np.linspace(-12, -1, 200), 1 - 10.0 ** np.linspace(-12, -1, 200)])
        i = np.clip(np.searchsorted(adm, ps), 1, len(adm) - 1) if len(adm) > 1 else np.zeros(len(ps), dtype=int)
        dist = np.minimum(np.abs(ps - adm[i]), np.abs(ps - adm[np.maximum(i - 1, 0)]))       # nearest admissible fraction (adm is sorted)
        worst = max(worst, float(np.max(dist * d / max(1, dm - 1))))
print("rounding: max over (u, d, phi*) of [distance to the nearest admissible fraction] / [max(1, d_min - 1)/d] = %.6f  (must be <= 1)" % worst)
