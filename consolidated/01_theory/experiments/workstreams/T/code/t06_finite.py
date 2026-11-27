#!/usr/bin/env python3
"""t06 -- exact finite-n lower bounds (hypergeometric sums; every number is a certified bound on a cost).
(a) dips of a symmetric instance on density-capped unions of profile classes around a centre of type k:
    the smallest cap q such that ln(1 + Phi(D_q)) > eps; then EVERY algorithm that is (eps/2, delta)-correct on L_u makes
    at least (1 - 2 delta)/maxdens(D_q) evaluations at the instance.  Reported: theta = ln(1/maxdens)/n.
(b) the shell-cone u*d(x, class (i0,j0)) truncated at type-wise q-quantiles: the smallest q with
    ln[A(psi)/A(psi^{tr,q})] > eps; then every NON-ADAPTIVE (eps/2, delta)-correct algorithm makes at least
    (1 - 2 delta)/q evaluations.  Reported: theta = ln(1/q)/n.
usage: python3 t06_finite.py bJ bB u eps1 eps0 a0 b0 n1,n2,...   [mfrac]
   accuracy eps = eps1*n + eps0;  shell class (i0,j0) = (round(a0*k), round(b0*(n-k)));  centre type k = round(mfrac*n).
"""
import sys, time, math
import numpy as np
import tlib as T
import tfin as F

bJ, bB, u, eps1, eps0, a0, b0 = [float(x) for x in sys.argv[1:8]]
ns = [int(x) for x in sys.argv[8].split(",")]
mfrac = float(sys.argv[9]) if len(sys.argv) > 9 else 0.5
phi = T.phi_cw(bJ, bB) if bJ > -90 else T.phi_field(bB)
t0 = time.time()
print(f"bJ={bJ} bB={bB} u={u} eps = {eps1}*n + {eps0}; shell (a0,b0)=({a0},{b0}); centre type {mfrac}")
print("     n     k | dips of H: theta   eff/n       | dips of 0: theta   | shell-cone trunc.: theta   ratio/n | cone (centre) trunc.: theta | time")
for n in ns:
    k = int(round(mfrac * n))
    f = F.Fin(n, k, phi, u)
    eps = eps1 * n + eps0
    rH = f.best_dip_exponent(eps, f.Vn)
    r0 = f.best_dip_exponent(eps, np.zeros(n + 1))
    i0, j0 = int(round(a0 * k)), int(round(b0 * (n - k)))
    rS = f.best_na_exponent(eps, i0, j0)
    rC = f.best_na_exponent(eps, 0, 0)
    fmt = lambda r, w=2: "   none        " if r is None else "  ".join(f"{v:.6f}" for v in r[:w])
    print(f"{n:6d} {k:5d} | {fmt(rH)}  | {fmt(r0,1)} | {fmt(rS)} | {fmt(rC,1)} | {time.time()-t0:.0f}s", flush=True)
