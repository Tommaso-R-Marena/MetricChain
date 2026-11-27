#!/usr/bin/env python3
"""t14 -- exact finite-n lower bounds from neighbourhoods of block-profile classes with 2, 3 and 4 blocks (kfin.py).
For a symmetric profile (S2: {1-x, x}; S3: {1-x, 1/2, x} with a free block lf; S4: {1-x, 1/2+d, 1/2-d, x}) on the lattice of n,
C = the class, D_B = union of the classes c' with u*l1(c', c) + V_n(type(c')) < n B.  The smallest B with ln(1 + Phi_H(D_B)) > eps
gives the certified bound: every algorithm that is (eps/2, delta)-correct on L_u makes at least (1-2 delta)/maxdens(D_B)
evaluations at H.  Reported: theta = -ln maxdens(D_B)/n  (to be compared with the single-letter value V and with each other).
usage: python3 t14_finite3.py bJ u eps1 kind p1,p2,.. n1,n2,...
   kind in S2, S3, S4 with parameters (x) / (lf, x) / (lf, x, d);  accuracy eps = eps1 * n + 1
"""
import sys, time, math
import numpy as np
import tlib as T
import kfin as KF

bJ, u, eps1 = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
kind = sys.argv[4]
p = [float(x) for x in sys.argv[5].split(",")]
ns = [int(x) for x in sys.argv[6].split(",")]
phi = T.phi_cw(bJ, 0.0)
K = T.Known(phi, u)
lams, mus = T.sym_profile(kind, p)
Vsl = T.obj_blocks(K, eps1, K.v, lams, mus, ng=2001, zoom=6)
t0 = time.time()
print(f"bJ={bJ} u={u} eps = {eps1}*n + 1; profile {kind}: lams {np.round(lams,4)}, mus {np.round(mus,4)};  single-letter value V(mu, e + alpha) = {Vsl:.6f}")
print("      n   block sizes          theta = ln(1/maxdens)/n   ln(1+Phi)/n   B*        theta - V     (theta - V)/(ln n/n)   time")
for n in ns:
    sizes = np.round(lams * n).astype(int)
    sizes[-1] += n - sizes.sum()
    # keep the profile symmetric on the lattice
    sizes[0] = sizes[-1]
    if len(sizes) == 3:
        sizes[1] = n - 2 * sizes[0]
    elif len(sizes) == 4:
        sizes[1] = sizes[2] = (n - 2 * sizes[0]) // 2
        sizes[0] = sizes[-1] = (n - 2 * sizes[1]) // 2
        if sizes.sum() != n:
            continue
    f = KF.KFin(sizes, phi, u)
    cell = tuple(int(round(m_ * s)) for m_, s in zip(mus, sizes))
    mask0 = np.zeros(f.t.shape, dtype=bool)
    mask0[cell] = True
    score = f.u * f.dist_to(mask0) + f.Vn[f.t]          # class c' is in D_B iff score < n B
    eps = eps1 * n + 1.0
    lo, hi = float(f.Vn[f.t[cell]]) / n, float(f.Vn[f.t[cell]]) / n + 2.0
    best = None
    for _ in range(34):
        mid = 0.5 * (lo + hi)
        mask = score < n * mid
        if mask.all():
            hi = mid
            continue
        lPhiP, lmu, lPhi, md = f.dip(mask, f.Vn)
        if np.logaddexp(0.0, lPhi) > eps:
            hi, best = mid, (md, float(np.logaddexp(0.0, lPhi)))
        else:
            lo = mid
    if best is None:
        print(f"  {n:5d}   {tuple(int(s) for s in sizes)}   no sensitive set found")
        continue
    th = -math.log(best[0]) / n
    print(f"  {n:5d}   {str(tuple(int(s) for s in sizes)):20s} {th:.6f}                  {best[1]/n:.6f}      {hi:.5f}   {th-Vsl:+.6f}     {(th-Vsl)/(math.log(n)/n):+.3f}                 {time.time()-t0:.0f}s", flush=True)
