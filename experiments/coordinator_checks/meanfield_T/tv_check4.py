#!/usr/bin/env python3
"""Check 4: the late statements of workstream T.
(a) u_top: the largest slope of a chord from the top of the barrier (bJ = 1.5, B = 0);
(b) u = 0.30: the binary barrier shell, and the failure of the pair identity for cones around it;
(c) the free block at e = 0.02 as a function of the coupling: none at bJ = 1.12, present at 1.2."""
import numpy as np, time
from scipy.optimize import minimize_scalar, minimize
from tv_lib import *
t0 = time.time()
M = Model(curie_weiss(1.5, 0.0), 1.0)
k = M.kap; I = M.Ik; top = float(M.Iex(0.5))
sl = (top - I[k < 0.499]) / (0.5 - k[k < 0.499])
j = int(np.argmax(sl))
kw = k[np.argmin(I[: len(k)//2])]
print(f"(a) largest slope of a chord from the top of the barrier: {sl[j]:.5f} (to kappa = {k[j]:.4f});  mean slope to the well ({kw:.4f}): {top/(0.5-kw):.5f};  largest slope of I on the barrier: {np.max(np.abs(np.gradient(I, k))[(k > kw) & (k < 1-kw)]):.5f}")
u = 0.30
M3 = Model(curie_weiss(1.5, 0.0), u)
cs = M3.kap[np.isclose(M3.Ik, M3.vk, atol=1e-11)]
gaps = np.flatnonzero(np.diff(cs) > 1e-4)
pieces = [(cs[0] if i == 0 else cs[gaps[i-1]+1], cs[g]) for i, g in enumerate(gaps)] + [(cs[gaps[-1]+1] if len(gaps) else cs[0], cs[-1])]
print(f"(b) u = 0.30: contact set pieces {[(round(a,4), round(b,4)) for a, b in pieces]}")
half = np.array([0.5, 0.5]); shell = lambda x: np.array([1 - x, x])
r = minimize_scalar(lambda x: -r_of_e(M3, half, shell(x), 0.0), bounds=(0.40, 0.49), method="bounded", options={"xatol": 1e-7})
x0, R0 = r.x, -r.fun
print(f"    best symmetric barrier shell at e = 0: x = {x0:.4f}, r = {R0:.7f}   (report: 0.4409, 0.0022646)   [{time.time()-t0:.0f}s]", flush=True)
def n_mu(x, X):
    """n_mu(X) = min{ r_mu(e) : e + r_mu(e) <= X } = r_mu at the largest feasible e (r_mu is nonincreasing; e <= X)."""
    lam, mu = half, shell(x)
    al = alpha(M3, lam, mu)
    lo_e = float(M3.v(0.5)) - al
    rr = lambda e: r_fast(M3, lam, mu, e + al, G=1500)
    if rr(X) <= 1e-12:
        return 0.0                                   # the largest feasible accuracy is X itself
    es = np.linspace(max(lo_e, X - 0.004), X, 33)
    g = np.array([e + rr(e) - X for e in es])
    ok = np.flatnonzero(g <= 0)
    if len(ok) == 0:
        return np.inf
    a, b = es[ok[-1]], es[min(ok[-1] + 1, len(es) - 1)]
    for _ in range(18):
        m_ = 0.5 * (a + b)
        if m_ + rr(m_) - X <= 0: a = m_
        else: b = m_
    return float(rr(a))
v0 = n_mu(x0, R0)
print(f"    n_mu(S(0)) at the optimal dip shell x = {x0:.4f}: {v0:.7f}   (report: 0, the pair identity fails there)   [{time.time()-t0:.0f}s]", flush=True)
best = (0, None)
for x in (0.4435, 0.447, 0.4495, 0.4514, 0.4535, 0.456, 0.46):
    v = n_mu(float(x), R0)
    print(f"       shell x = {x}: n_mu(S(0)) = {v:.7f}   [{time.time()-t0:.0f}s]", flush=True)
    if np.isfinite(v) and v > best[0]: best = (v, float(x))
print(f"    sup over these symmetric shells of n_mu(S(0)): {best[0]:.7f} at x = {best[1]:.4f}   (report: 0.0018400 at 0.4514; ratio to R: {best[0]/R0:.3f})", flush=True)
print("(c) free block at e = 0.02, u = 1", flush=True)
def S3(x, lf): return np.array([(1 - lf) / 2, lf, (1 - lf) / 2]), np.array([1 - x, 0.5, x])
for bJ, claim2, claim3, par in ((1.12, 0.0201047, None, None), (1.2, 0.0189503, 0.0192108, (0.2694, 0.034)), (1.3, 0.0175999, 0.0181202, (0.272, 0.072))):
    Mj = Model(curie_weiss(bJ, 0.0), 1.0)
    b2 = -minimize_scalar(lambda x: -r_of_e(Mj, half, shell(x), 0.02), bounds=(0.25, 0.33), method="bounded", options={"xatol": 1e-7}).fun
    if par is None:
        vals = [r_of_e(Mj, *S3(x, lf), 0.02) for x in (0.2689, 0.2700) for lf in (0.002, 0.005, 0.01, 0.03)]
        print(f"    bJ = {bJ}: binary {b2:.7f} (report {claim2});  best of eight profiles with a free block {max(vals):.7f}  (report: no gain)   [{time.time()-t0:.0f}s]", flush=True)
    else:
        f = lambda p: -r_of_e(Mj, *S3(p[0], p[1]), 0.02) if (0.2 < p[0] < 0.4 and 1e-4 < p[1] < 0.5) else 1.0
        rr = minimize(f, list(par), method="Nelder-Mead", options={"xatol": 1e-5, "fatol": 1e-11, "maxfev": 120})
        print(f"    bJ = {bJ}: binary {b2:.7f} (report {claim2});  with a free block {-rr.fun:.7f} at (x, lam_f) = {np.round(rr.x, 4)}  (report {claim3} at {par})   [{time.time()-t0:.0f}s]", flush=True)
