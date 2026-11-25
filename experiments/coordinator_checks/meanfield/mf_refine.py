#!/usr/bin/env python3
"""Convergence check of the two-phase numbers (Curie-Weiss, bJ = 1.5, B = 0, u = 1): the dip exponent of the
flat-histogram instance at centre type 1/2 on grids G = 401, 801, 1601, and the shell-cone non-adaptive exponent
with the shell radius refined.  Exploration, not a result."""
import numpy as np, sys, time
from mf_lib import Model, hb

bJ, bB, u = 1.5, 0.0, 1.0
phi = lambda k: -(bJ / 2) * (2 * k - 1) ** 2 - bB * (2 * k - 1)


def R_dip_m(M, chi_k, e, m, iters=26):
    lo, hi = 0.0, float(hb(np.array(m))) * 0.999
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if M.dip_exponent(chi_k, m, mid) >= e:
            lo = mid
        else:
            hi = mid
    return lo


def shell_m(M, x, m, a0s, b0s):
    f = M.fields(m)
    base = f["MI"] + f["I"]
    best = (-1, None)
    for a0 in a0s:
        for b0 in b0s:
            val = base + M.u * (m * np.abs(M.A - a0) + (1 - m) * np.abs(M.B - b0))
            ok = val - val.min() <= x
            th = float(f["MI"][ok].min())
            if th > best[0]:
                best = (th, (float(a0), float(b0)))
    return best


t0 = time.time()
print(f"Curie-Weiss bJ={bJ}, B={bB}, u={u}; centre type 1/2; uniform-cube value KL(Lambda_1/u || 1/2) at e=0: 0.029139")
for G in (401, 801, 1601):
    M = Model(phi, u, G=G)
    row = []
    for e in (-0.01, 0.0, 0.01):
        row.append(R_dip_m(M, -M.vk, e, 0.5))
    print(f"  G={G:5d}: R_H(dip; m=1/2) at e = -0.01, 0, 0.01: {row[0]:.5f}  {row[1]:.5f}  {row[2]:.5f}   [{time.time()-t0:.0f}s]", flush=True)
RH0 = row[1]
M = Model(phi, u, G=801)
for e, RH in ((-0.01, row[0]), (0.0, row[1]), (0.01, row[2])):
    x = e + RH
    grid = np.linspace(0.20, 0.36, 17)
    best = (-1, None)
    for r0 in grid:                                   # symmetric shells (r0, r0) and slightly asymmetric ones
        for d in (-0.02, -0.01, 0.0, 0.01, 0.02):
            th, z0 = shell_m(M, x, 0.5, [r0 + d], [r0 - d])
            if th > best[0]:
                best = (th, z0)
    cone, _ = shell_m(M, x, 0.5, [0.0], [0.0])
    print(f"  e={e:+.2f}: R_H = {RH:.5f};  theta_na at x = e + R_H: shell {best[0]:.5f} (z0 = ({best[1][0]:.2f}, {best[1][1]:.2f})), cone {cone:.5f}"
          f"   [{time.time()-t0:.0f}s]", flush=True)
