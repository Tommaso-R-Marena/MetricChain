#!/usr/bin/env python3
"""Two-phase Curie-Weiss known part (bJ = 1.5, B = 0), u = 1: is the hardest instance additive?
Dip exponents by the variational definition for the flat-histogram instance H and for additive instances gamma*kappa."""
import numpy as np, sys, time
from mf_lib import Model

bJ, bB, u = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
G = int(sys.argv[4]) if len(sys.argv) > 4 else 241
phi = lambda k: -(bJ / 2) * (2 * k - 1) ** 2 - bB * (2 * k - 1)
M = Model(phi, u, G=G)
ms = np.linspace(0.06, 0.94, 23)
t0 = time.time()
for e in (0.0,):
    RHf, mf = M.R_formula(e, ms, "v")
    RHd, md = M.R_dip(-M.vk, e, ms, iters=16)
    print(f"bJ={bJ} bB={bB} u={u} e={e}: R_H formula = {RHf:.5f} (m={mf:.2f}), R_H dip definition = {RHd:.5f} (m={md:.2f})   [{time.time()-t0:.0f}s]", flush=True)
    res = []
    for gam in np.linspace(-0.8, 0.8, 9):
        Rg, mg = M.R_dip(gam * M.kap, e, ms, iters=16)
        res.append((Rg, gam, mg))
        print(f"    additive gamma = {gam:+.2f}: R = {Rg:.5f} (m = {mg})   [{time.time()-t0:.0f}s]", flush=True)
    best = max(res)
    print(f"  max over additive instances: {best[0]:.5f} at gamma = {best[1]:+.2f}, centre type {best[2]}")
