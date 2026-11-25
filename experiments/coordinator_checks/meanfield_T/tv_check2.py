#!/usr/bin/env python3
"""Check 2: headline numbers of workstream T at bJ = 1.5, B = 0, u = 1 with the coordinator's solvers."""
import numpy as np, time
from scipy.optimize import minimize, minimize_scalar
from tv_lib import *
t0 = time.time()
M = Model(curie_weiss(1.5, 0.0), 1.0)
def S2(x): return np.array([0.5, 0.5]), np.array([1 - x, x])
def S3(x, lf): return np.array([(1 - lf) / 2, lf, (1 - lf) / 2]), np.array([1 - x, 0.5, x])
print("== B. binary symmetric shells (1/2; x, x): maximum over x of r(e)")
claims2 = {-0.05: (0.0575961, 0.2821), 0.0: (0.0251012, 0.29803), 0.01: (0.0199399, 0.30170), 0.02: (0.0152765, 0.30553), 0.05: (0.0046265, 0.31795)}
for e, (val, x) in claims2.items():
    f = lambda x: -r_of_e(M, *S2(x), e)
    r = minimize_scalar(f, bounds=(0.22, 0.40), method="bounded", options={"xatol": 1e-7})
    at = r_of_e(M, *S2(x), e)
    print(f"   e={e:+.3f}: max_x = {-r.fun:.7f} at x = {r.x:.5f}   (report: {val:.7f} at {x});  at the report's x: {at:.7f}   [{time.time()-t0:.0f}s]", flush=True)
print("== C. is the symmetric shell optimal among all binary centres (m; a, b)?  Nelder-Mead from perturbed starts, e = 0")
def fbin(p, e):
    m, a, b = p
    if not (0.02 < m < 0.98 and 0.01 < a < 0.99 and 0.01 < b < 0.99): return 1.0
    lam = np.array([m, 1 - m]); mu = np.array([1 - a, b])
    Bv = e + alpha(M, lam, mu)
    if Bv < float(M.v((lam * mu).sum())): return 1.0
    return -r_fast(M, lam, mu, Bv)
best = 0
for st in ([0.5, 0.30, 0.30], [0.45, 0.27, 0.33], [0.6, 0.25, 0.30], [0.50035, 0.29868, 0.29785]):
    r = minimize(fbin, st, args=(0.0,), method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-10, "maxfev": 260})
    print(f"   start {st} -> {-r.fun:.7f} at (m, a, b) = {np.round(r.x, 5)}   [{time.time()-t0:.0f}s]", flush=True)
    best = max(best, -r.fun)
print(f"   best binary value at e = 0: {best:.7f}   (report: 0.0251012)")
print("== D. three blocks with a free block (S3): value at the report's parameters and own maximisation")
claims3 = {0.002: (0.02404192, 0.2715, 0.140), 0.01: (0.02038167, 0.2744, 0.140), 0.02: (0.01615476, 0.2774, 0.141), 0.05: (0.00616685, None, None)}
for e, (val, x, lf) in claims3.items():
    if x is not None:
        at = r_of_e(M, *S3(x, lf), e)
    else:
        at = float("nan")
    f = lambda p: -r_of_e(M, *S3(p[0], p[1]), e) if (0.2 < p[0] < 0.4 and 0.01 < p[1] < 0.6) else 1.0
    bestv = 0; arg = None
    for st in ([0.275, 0.14], [0.29, 0.08], [0.27, 0.25]):
        r = minimize(f, st, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-11, "maxfev": 400})
        if -r.fun > bestv: bestv = -r.fun; arg = r.x
    b2 = -minimize_scalar(lambda x: -r_of_e(M, *S2(x), e), bounds=(0.22, 0.40), method="bounded", options={"xatol": 1e-7}).fun
    print(f"   e={e:.3f}: S3 max = {bestv:.8f} at (x, lam_f) = {np.round(arg, 4)}  (report: {val:.8f});  at the report's parameters {at:.8f};  binary {b2:.8f};  gain {100*(bestv/b2-1):+.2f} %   [{time.time()-t0:.0f}s]", flush=True)
print("== E. the same S3 optima re-evaluated with the slow solver (no clipping lemma, I in the constraint)")
for e, x, lf in [(0.02, 0.2774, 0.141), (0.0, 0.29803, None)]:
    lam, mu = S3(x, lf) if lf is not None else S2(x)
    Bv = e + alpha(M, lam, mu)
    s, arg = r_slow(M, lam, mu, Bv, nk=500)
    kp = arg[0]
    s2, arg2 = r_slow(M, lam, mu, Bv, kgrid=np.linspace(kp - 0.003, kp + 0.003, 121))
    # all local minima over the exit type
    print(f"   e={e}: slow {min(s, s2):.8f} (exit type {arg2[0] if s2 < s else kp:.4f}, exit profile {np.round(arg2[1] if s2 < s else arg[1], 4)});  fast {r_fast(M, lam, mu, Bv):.8f}   [{time.time()-t0:.0f}s]", flush=True)
