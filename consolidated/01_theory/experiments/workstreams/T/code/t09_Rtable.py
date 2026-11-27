#!/usr/bin/env python3
"""t09 -- table of the dip exponent of the flat-histogram instance, R_H(e) = sup over binary centres of V(mu, e+alpha(mu); v),
on a grid of accuracies of both signs (warm starts along the grid, re-evaluated with the fine inner solver), with the
non-adaptive partner n_mu*(e + R_H(e)) (pair identity).  Written to out/Rtable_<tag>.txt for the tests on sets.
usage: python3 t09_Rtable.py bJ bB u emin emax ne tag
"""
import sys, time, math
import numpy as np
import tlib as T

bJ, bB, u, emin, emax = [float(x) for x in sys.argv[1:6]]
ne = int(sys.argv[6])
tag = sys.argv[7]
t0 = time.time()
K = T.Known(T.phi_cw(bJ, bB), u) if bJ > -90 else T.Known(T.phi_field(bB), u)
es = np.linspace(emax, emin, ne)        # from the largest accuracy downwards
rows = []
prev = None
# start in the middle (e closest to 0) and go both ways with warm starts
i0 = int(np.argmin(np.abs(es)))
order = list(range(i0, ne)) + list(range(i0 - 1, -1, -1))
warm = {}
for idx in order:
    e = float(es[idx])
    starts = []
    for nb in (idx - 1, idx + 1):
        if nb in warm:
            starts.append(warm[nb])
    R, arg = T.R_bin(K, e, K.v, starts=starts, nrand=0 if starts else 4, ms=np.array([0.5]) if starts else None)
    lams, mus = T.bin_blocks(*arg)
    Rf = T.obj_blocks(K, e, K.v, lams, mus, ng=2001, zoom=6)
    warm[idx] = arg
    X = e + Rf
    nmu = T.n_mu(K, lams, mus, X, K.v) if X > 1e-9 else float("nan")
    rows.append((e, Rf, arg[0], arg[1], arg[2], nmu))
    print(f"e={e:+.5f} R={Rf:.8f} S={X:.8f} n_mu*={nmu:.8f} arg=({arg[0]:.5f},{arg[1]:.5f},{arg[2]:.5f}) [{time.time()-t0:.0f}s]", flush=True)
rows.sort()
with open(f"../out/Rtable_{tag}.txt", "w") as f:    # (tables of several runs are merged by t09b_merge.py)
    f.write(f"# bJ={bJ} bB={bB} u={u}: e, R_H(e), m, a, b, n_mu*(e+R_H(e))\n")
    for r in rows:
        f.write(" ".join(f"{v:.10f}" for v in r) + "\n")
print(f"time {time.time()-t0:.0f}s")
