#!/usr/bin/env python3
"""t19 -- the onset of the free block in the coupling (Curie-Weiss, B = 0, u and e fixed).
Diluted uniform-cube profile S3(lf, p_u): blocks ((1-lf)/2, lf, (1-lf)/2) of types (1-p_u, 1/2, p_u).  Its symmetric exit has
radius rho' = (Lam1 + e/(1-lf))/u and the value (1-lf) KL(rho' || 1/2).  Along the exits (1-rb+t, 1/2, rb+t) of type
1/2 + (1-lf) t on the boundary of the feasible set,
     MI(t) = MI(0) + (1-lf) t^2 A(lf) + O(t^4),    A(lf) = c2 + 2 lf - 2 L (bJ-1)(1-lf)/u,
     c2 = 1/(2 rho'(1-rho')) - 2,   L = ln((1-rho')/rho'),
so the symmetric exit is a strict local minimum iff bJ < bJ_stab(lf) = 1 + u (c2 + 2 lf)/(2 L (1-lf));  bJ_stab(0) = bJ*.
 (1) finite-difference check of A(lf) on the explicit boundary curve (no solver);
 (2) solver check: value of S3(lf, p_u) against (1-lf) KL(rho' || 1/2) on both sides of bJ_stab(lf);
 (3) the marginal weight lf_stab(bJ) (bJ_stab(lf_stab) = bJ), the slope k = d bJ_stab/d lf at 0, the cost c = R - e R' of a
     free block, and the predicted onset bJ** = bJ* + c/(2 kappa k) from the quadratic deficit kappa (bJ - bJ*)^2 of the
     binary branch (kappa fitted to the values of t10 given on the command line).
usage: python3 t19_onset.py u e  [bJ:binary_value ...]
"""
import sys, time, math
import numpy as np
from scipy.optimize import brentq
import tlib as T

u, e = float(sys.argv[1]), float(sys.argv[2])
pairs = [tuple(float(x) for x in a.split(":")) for a in sys.argv[3:]]
t0 = time.time()
Lam1 = math.log(2 / (1 + math.exp(-u)))
pu = 1 / (1 + math.exp(u))
ln2 = math.log(2.0)


def h(x):
    return -x * math.log(x) - (1 - x) * math.log(1 - x)


def rho_of(lf):
    return (Lam1 + e / (1 - lf)) / u


def c2L(lf):
    r = rho_of(lf)
    return 1 / (2 * r * (1 - r)) - 2, math.log((1 - r) / r)


def bJ_stab(lf):
    c2, L = c2L(lf)
    return 1 + u * (c2 + 2 * lf) / (2 * L * (1 - lf))


def A_coef(lf, bJ):
    c2, L = c2L(lf)
    return c2 + 2 * lf - 2 * L * (bJ - 1) * (1 - lf) / u


def diluted_value(lf):
    r = rho_of(lf)
    return (1 - lf) * (ln2 - h(r)) if r < 0.5 else 0.0


def I_rel(bJ, T_):
    """I(1/2 + T) - I(1/2) for B = 0 (on the contact set)"""
    return -2 * bJ * T_ * T_ - h(0.5 + T_) + ln2


def MI_boundary(lf, bJ, t):
    """MI of the exit (1-rb+t, 1/2, rb+t) on the boundary  u(1-lf)(rb - p_u) + I(1/2+(1-lf)t) - I(1/2) = e + (1-lf)KL(p_u||1/2)"""
    rb = pu + (e + (1 - lf) * (ln2 - h(pu)) - I_rel(bJ, (1 - lf) * t)) / (u * (1 - lf))
    return h(0.5 + (1 - lf) * t) - (1 - lf) * 0.5 * (h(rb - t) + h(rb + t)) - lf * ln2


print(f"u={u} e={e}: Lam1={Lam1:.6f} p_u={pu:.6f} rho={rho_of(0):.6f}; bJ* = bJ_stab(0) = {bJ_stab(0):.5f};  R_unif(e) = {diluted_value(0):.7f}")
print("(1) finite differences on the boundary curve:  [MI(t) - MI(0)]/((1-lf) t^2)  against  A(lf)")
for lf in (0.0, 0.05, 0.15):
    for bJ in (bJ_stab(lf) - 0.05, bJ_stab(lf) + 0.05):
        fd = [(MI_boundary(lf, bJ, t) - MI_boundary(lf, bJ, 0.0)) / ((1 - lf) * t * t) for t in (1e-2, 3e-3, 1e-3)]
        print(f"   lf={lf:.2f} bJ={bJ:.4f} (bJ_stab={bJ_stab(lf):.4f}):  t=1e-2: {fd[0]:+.6f}  3e-3: {fd[1]:+.6f}  1e-3: {fd[2]:+.6f}   A = {A_coef(lf, bJ):+.6f}")
        assert abs(fd[2] - A_coef(lf, bJ)) < 2e-4

print("(2) solver: r_mu(e) of S3(lf, p_u) against the diluted uniform-cube value (1-lf) KL(rho'||1/2)")
for lf in (0.03, 0.08):
    lams, mus = T.sym_profile("S3", [lf, pu])
    for d in (-0.03, -0.005, +0.005, +0.03):
        bJ = bJ_stab(lf) + d
        K = T.Known(T.phi_cw(bJ, 0.0), u)
        val = T.obj_blocks(K, e, K.v, lams, mus, ng=2001, zoom=6)
        print(f"   lf={lf:.2f} bJ = bJ_stab{d:+.3f} = {bJ:.4f}:  r_mu(e) = {val:.8f}   diluted value = {diluted_value(lf):.8f}   difference {val - diluted_value(lf):+.2e}   [{time.time()-t0:.0f}s]", flush=True)

print("(3) marginal weight and predicted onset")
r = rho_of(0)
L0 = math.log((1 - r) / r)
c = diluted_value(0) + e * L0 / u          # R - e R',  R' = -L/u
k = (bJ_stab(1e-5) - bJ_stab(0)) / 1e-5
print(f"   cost of a free block  c = R_unif(e) - e R_unif'(e) = {c:.6f};   k = d bJ_stab/d lf (0) = {k:.4f}")
if pairs:
    bs = bJ_stab(0)
    ks = [(diluted_value(0) - val) / (bJ - bs) ** 2 for bJ, val in pairs]
    for (bJ, val), kk in zip(pairs, ks):
        print(f"   binary branch: bJ={bJ:.4f}  R = {val:.7f}  deficit {diluted_value(0)-val:.3e} = {kk:.4f} * (bJ - bJ*)^2")
    kap = float(np.median(ks))
    print(f"   kappa = {kap:.4f}:  predicted onset of the free block  bJ** = bJ* + c/(2 kappa k) = {bs + c/(2*kap*k):.4f}")
print("   bJ      marginal weight lf_stab(bJ)   [bJ_stab(lf_stab) = bJ]     diluted value at lf_stab")
for bJ in (1.13, 1.14, 1.15, 1.2, 1.3, 1.5, 1.75, 2.0):
    if bJ <= bJ_stab(0):
        continue
    lf = brentq(lambda x: bJ_stab(x) - bJ, 0.0, 0.6)
    print(f"   {bJ:.3f}   {lf:.4f}                                              {diluted_value(lf):.7f}")
print(f"time {time.time()-t0:.0f}s")
