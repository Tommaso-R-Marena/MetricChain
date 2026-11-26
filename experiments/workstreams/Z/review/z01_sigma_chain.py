#!/usr/bin/env python3
"""z01: (i) of the brief -- the slope map by direct maximisation and the chain (W_j, b_j) of the cube from the definitions.

A. Sigma(B, s): direct maximisation over e (scan + golden section) against (1) the first-order solution used in the
   production code of this review (zrev.Cube.sigma), (2) a brute-force grid over e, (3) the coordinator's rlib (J-based),
   at random points; convexity/monotonicity of theta_na checked on a grid.
B. The chain for u = 1, s_t = L + 0.05, b_0 = h + 0.003 against the numbers of experiments/workstreams/R/out_r2_chain_cube1.txt
   and of the header of experiments/workstreams/Z/out_z1_onelevel_u1.txt; range condition; Lemma T(b) on a grid.
"""
import math
import os
import random
import sys

import numpy as np

sys.dont_write_bytecode = True
import zrev

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(1)
print("== A. the slope map ==")
worst_fo = worst_bf = worst_rl = 0.0
sys.path.insert(0, os.path.join(HERE, '..', '..', 'R'))
import rlib as coord_rlib        # the coordinator's library: comparison only
for u in (0.5, 1.0, 2.0):
    cu = zrev.Cube(u)
    P = coord_rlib.Cube(u).setup()
    # theta_na: convex, nonincreasing, theta(0+) = a, theta(h) = h, theta = 0 beyond eps*
    es = np.linspace(1e-9, 1.5 * cu.eps_star, 20001)
    th = cu.theta_v(es)
    d1 = np.diff(th)
    d2 = np.diff(th, 2)
    print("u = %g: theta_na nonincreasing: %s (max increment %.1e); convex: %s (min 2nd difference %.1e); theta(h) - h = %.1e; "
          "theta(0+) - a = %.1e; |h - coord| = %.1e, |L - coord| = %.1e, |c*^2 - coord| = %.1e"
          % (u, bool(d1.max() <= 1e-15), d1.max(), bool(d2.min() >= -1e-14), d2.min(), cu.theta(cu.h) - cu.h,
             cu.theta(1e-14) - cu.a, abs(cu.h - P.h), abs(cu.L - P.L), abs(cu.cstar2 - P.const)))
    n = 0
    eg = np.exp(np.linspace(math.log(1e-12), math.log(50.0), 200001))      # brute force over e on a log grid
    thg = cu.theta_v(eg)
    for _ in range(300):
        s = random.choice([0.0, random.random() * 0.95, random.random() * 0.6])
        B = random.random() * (1 - s) * cu.a * random.choice([0.999, 0.9, 0.5, 0.1, 0.01])
        sd = cu.sigma_direct(B, s)
        sf = float(cu.sigma(np.array([B]), np.array([s]))[0])
        s1 = cu.sig1(B, s)[0]
        assert abs(s1 - sf) <= 1e-9 * max(sf, 1e-9)
        bf = float(np.max((B - (1 - s) * thg) / eg))
        sr = P.sigma(B, s)
        worst_fo = max(worst_fo, abs(sd - sf) / max(sd, 1e-12))
        worst_bf = max(worst_bf, (bf - sd) / max(sd, 1e-12))       # brute force can only be below the true sup
        worst_rl = max(worst_rl, abs(sd - sr) / max(sd, 1e-12))
        n += 1
    print("   %d random (B, s): direct vs first-order (vector and scalar solvers): rel. diff <= %.2e; brute-force grid exceeds direct by <= %.2e (rel.); "
          "direct vs coordinator's rlib: <= %.2e" % (n, worst_fo, worst_bf, worst_rl))
    # derivative check of sigma_grad
    B0, s0 = 0.4 * cu.a, 0.3
    sg, gB, gs = cu.sigma_grad(np.array([B0]), np.array([s0]))
    eps = 1e-6
    nB = (cu.sigma_direct(B0 + eps, s0) - cu.sigma_direct(B0 - eps, s0)) / (2 * eps)
    ns = (cu.sigma_direct(B0, s0 + eps) - cu.sigma_direct(B0, s0 - eps)) / (2 * eps)
    print("   gradient at (0.4a, 0.3): analytic (%.6f, %.6f), numerical from the direct maximisation (%.6f, %.6f)" % (gB[0], gs[0], nB, ns))
    # fixed point: Sigma(h, L) = L, multiplier theta(h)/h = 1
    print("   Sigma(h, L) - L = %.2e (direct);  boundary: Sigma((1-s)a, s) = inf: %s" % (cu.sigma_direct(cu.h, cu.L) - cu.L, cu.sigma_direct(0.5 * cu.a, 0.5) == zrev.INF))

print("== B. the chain for u = 1, s_t = L + 0.05, b_0 = h + 0.003 ==")
cu = zrev.Cube(1.0)
C = zrev.Chain(cu, 0.05, 0.003, 62)
print("range condition W_j(b_j) <= 1 for j <= 62: %s (largest %.6f at j = %d)" % (C.range_ok, max(C.Wtop), int(np.argmax(C.Wtop))))
ref = {3: (2.277101e-03, 7.40326e+01, 4.405963e-03, 3.000000e-03), 6: (7.819829e-04, 1.81876e+02, 1.778737e-03, 2.286144e-03),
       10: (3.522094e-04, 3.98543e+02, 8.285700e-04, 9.779032e-04), 20: (1.147689e-04, 1.46877e+03, 2.475919e-04, 2.726405e-04),
       50: (2.325359e-05, 1.29101e+04, 3.851078e-05, 4.020023e-05)}
print("#  j   B_t(j)-h      m_j          E_j-h        b_j-h      | coordinator (out_r2_chain_cube1.txt): the same four")
for j in sorted(ref):
    Bt, m = C.cut[j]
    print("  %2d  %.6e  %.5e  %.6e  %.6e | %.6e  %.5e  %.6e  %.6e" % ((j, Bt - cu.h, m, C.E[j + 1] - cu.h, C.b[j] - cu.h) + ref[j]))
print("(b_j - h)/h, j = 0..12: " + " ".join("%.4f" % ((b - cu.h) / cu.h) for b in C.b[:13]))
print("   coordinator:         0.1030 0.1030 0.1030 0.1030 0.1030 0.1030 0.0785 0.0610 0.0490 0.0402 0.0336 0.0284 0.0244")
print("j^2 (b_j - h)/c_*^2 at j = 10, 20, 40, 60: " + " ".join("%.4f" % (j * j * (C.b[j] - cu.h) / cu.cstar2) for j in (10, 20, 40, 60))
      + "   (coordinator: 1.3745 1.5328 1.4629 at 10, 20, 40)")
# Lemma T(b):  W_{j+1}(B) <= Sigma(B, W_j(B)) on [0, b_0];  W_j convex nondecreasing with W_j(0) = 0
worstT = -1e9
conv_ok = mono_ok = True
for j in range(0, 40):
    Bs = np.linspace(0.0, C.b0, 3001)
    Wj = C.W(j, Bs)
    Wn = C.W(j + 1, Bs)
    img = cu.sigma(Bs, np.minimum(Wj, 1.0))
    img = np.where(Wj >= 1.0, zrev.INF, img)
    worstT = max(worstT, float(np.max(np.where(np.isfinite(img), Wn - img, -1.0))))
    d2 = np.diff(Wj, 2)
    conv_ok &= bool(d2.min() >= -1e-9)
    mono_ok &= bool(np.diff(Wj).min() >= -1e-12) and abs(Wj[0]) < 1e-15
print("Lemma T(b): max of W_{j+1} - Sigma(., W_j(.)) over [0, b_0], j < 40: %.2e (must be <= 0 up to rounding);  W_j convex: %s, nondecreasing with W_j(0) = 0: %s"
      % (worstT, conv_ok, mono_ok))
