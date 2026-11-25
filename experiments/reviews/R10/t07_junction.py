"""Section 6.6: the junction with the uniform cube.  For B = 0 and the uniform cube's optimal
profile mu* = (1/2; p_u, p_u):  bJ*(e,u) = 1 + u c2/(2L).  Check (ii) the second-order coefficient
by finite differences on the boundary curve, and (iii) whether r_{mu*}(e) = R_unif(e) for bJ < bJ*
(is the local minimum global?), for several (u, e) -- not only u = 1.
r_{mu*}(e) is evaluated with S1 (clippings, v) and S2 (dual per exit type, I)."""
import time, sys
import numpy as np
from r10lib import *
t0 = time.time()

def consts(u, e):
    rho = (Lam1(u) + e) / u
    c2 = 1.0 / (2 * rho * (1 - rho)) - 2.0
    L = np.log((1 - rho) / rho)
    return rho, c2, L, 1.0 + u * c2 / (2 * L)

print("# (ii) second-order coefficient of MI along the tilted exits (a',b') = (rhobar - t, rhobar + t), finite differences")
for (u, e, bJ) in ((1.0, 0.0, 1.10), (1.0, 0.0, 1.20), (1.0, 0.02, 1.05), (2.0, 0.1, 1.3), (0.5, 0.0, 1.03)):
    M = Model(bJ=bJ, bB=0.0, u=u)
    rho, c2, L, bJs = consts(u, e)
    pu = p_u(u)
    lam, mu = binary(0.5, pu, pu)
    B = e + alpha(M, lam, mu)
    def mi_t(t):
        # exit (a', b') = (rb - t, rb + t): nu = (1 - a', b'), type 1/2 + t; rb from the constraint
        f = lambda rb: u * (rb - pu) + float(M.I(0.5 + t)) - B
        from scipy.optimize import brentq
        rb = brentq(f, pu, 0.6)
        return MI(lam, np.array([1 - (rb - t), rb + t]))
    t = 1e-3
    coef = (mi_t(t) - 2 * mi_t(0.0) + mi_t(-t)) / (2 * t * t)
    print(f"  u={u} e={e} bJ={bJ}: finite difference {coef:.6f}   formula c2 + 2(1-bJ)L/u = {c2 + 2*(1-bJ)*L/u:.6f}   bJ* = {bJs:.5f}")

print("# (iii) r_{mu*}(e) against R_unif(e):  columns  u  e  bJ*  f=(bJ-1)/(bJ*-1)  bJ  barrier  R_unif  S1  S2  deficit  cheapest exit type")
fine = dict(G=400, zooms=5, ncand=6, nz=41, rounds=8)
for u in (0.3, 1.0, 2.0, 4.0):
    Eu = np.log(np.cosh(u / 2))
    ec = -float(kl(p_u(u), 0.5))
    for e in (0.6 * ec, 0.0, 0.3 * Eu, 0.6 * Eu, 0.9 * Eu):
        rho, c2, L, bJs = consts(u, e)
        for f in (0.5, 0.9, 0.99, 1.02, 1.2):
            bJ = 1.0 + f * (bJs - 1.0)
            M = Model(bJ=bJ, bB=0.0, u=u, N=200001)
            pu = p_u(u)
            lam, mu = binary(0.5, pu, pu)
            B = e + alpha(M, lam, mu)
            s1 = inner_clip(M, lam, mu, B, **fine)[0]
            s2, k2, loc = inner_dual(M, lam, mu, B, nk=801, refine=4)
            Ru = R_unif(e, u)
            barrier = float(M.I(0.5))
            flag = "" if (abs(s1 - Ru) < 2e-9) == (f < 1) else "   <-- differs from claim (iii)" if f < 1 else "   <-- no deficit beyond bJ*?"
            print(f"  {u:.1f} {e:+.5f} {bJs:.5f} {f:.2f} {bJ:.5f} {barrier:.5f}  {Ru:.9f} {s1:.9f} {s2:.9f}  {Ru - s1:+.2e}  {k2:.4f}{flag}", flush=True)
print("time", time.time() - t0)
