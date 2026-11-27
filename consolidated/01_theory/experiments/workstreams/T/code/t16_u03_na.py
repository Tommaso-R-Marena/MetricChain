#!/usr/bin/env python3
"""t16 -- u = 0.3 (narrow contact piece at the top of the barrier): the non-adaptive lower bound from shells,
N(X) = sup_mu n_mu(X), against the sheared dip exponent R(e) at X = e + R(e).
 (1) symmetric binary shells (1/2; x, x): scan + polish;  (2) general binary profiles (m, a, b): Nelder-Mead;
 (3) symmetric profiles with a free block: Nelder-Mead over (lf, x).
usage: python3 t16_u03_na.py bJ u e R"""
import sys, time
import numpy as np
from scipy.optimize import minimize, minimize_scalar
import tlib as T
bJ, u, e, R = [float(x) for x in sys.argv[1:5]]
K = T.Known(T.phi_cw(bJ, 0.0), u)
X = e + R
t0 = time.time()
lam2 = np.array([0.5, 0.5])
f1 = lambda x: T.n_mu(K, lam2, np.array([1 - x, x]), X, K.v)
xs = np.linspace(1 / (1 + np.exp(u)), 0.495, 40)
v1 = [f1(x) for x in xs]
i = int(np.argmax(v1))
r = minimize_scalar(lambda x: -f1(x), bounds=(xs[max(i - 1, 0)], xs[min(i + 1, 39)]), method="bounded", options={"xatol": 1e-7})
best1 = max(-r.fun, v1[i]); x1 = r.x
print(f"X = e + R = {X:.7f} (e = {e}, R = {R:.7f})")
print(f" (1) symmetric binary shells: sup n_mu(X) = {best1:.7f} at x = {x1:.5f}   [{time.time()-t0:.0f}s]", flush=True)
def f2(p):
    m, a, b = p
    if not (0.05 < m < 0.95 and 0 < a < 1 and 0 < b < 1 and a + b < 1):
        return 0.0
    return -T.n_mu(K, *T.bin_blocks(m, a, b), X, K.v)
best2 = (best1, (0.5, x1, x1))
for s in ((0.5, x1, x1), (0.47, x1 + 0.01, x1 - 0.01), (0.53, x1 - 0.01, x1 + 0.01)):
    rr = minimize(f2, np.array(s), method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-12, "maxiter": 250, "initial_simplex": T._simplex(s, 0.006)})
    if -rr.fun > best2[0]:
        best2 = (-rr.fun, tuple(rr.x))
print(f" (2) general binary profiles: {best2[0]:.7f} at (m,a,b) = ({best2[1][0]:.4f},{best2[1][1]:.4f},{best2[1][2]:.4f})   [{time.time()-t0:.0f}s]", flush=True)
def f3(p):
    lf, x = p
    if not (0.0 < lf < 0.9 and 0 < x < 0.5):
        return 0.0
    return -T.n_mu(K, *T.sym_profile("S3", (lf, x)), X, K.v)
best3 = (0.0, None)
for s in ((0.05, x1), (0.15, x1 - 0.005), (0.3, x1 - 0.01)):
    rr = minimize(f3, np.array(s), method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-12, "maxiter": 200, "initial_simplex": np.array([s, (s[0] + 0.03, s[1]), (s[0], s[1] + 0.004)])})
    if -rr.fun > best3[0]:
        best3 = (-rr.fun, tuple(rr.x))
print(f" (3) with a free block: {best3[0]:.7f} at (lf, x) = ({best3[1][0]:.4f},{best3[1][1]:.4f})   [{time.time()-t0:.0f}s]")
print(f" ratio of the best shell value to R: {max(best1, best2[0], best3[0])/R:.4f}   (time {time.time()-t0:.0f}s)")
