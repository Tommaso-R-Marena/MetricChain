#!/usr/bin/env python3
"""Non-adaptive exponent from cones around shells, against the dip exponent of the flat-histogram instance.

theta_na^shell(x) = max over centre types m and shell profiles z0 of
        min{ MI(z) : MI(z) + I(kappa_z) + u dist(z, z0) - V(z0) <= x },   V(z0) = min_z [MI + I + u dist(z, z0)]
(the function u * d(x, {points with profile z0 around s}) truncated where a type-uniform sample of e^{n theta}
points per type does not see it); z0 = (0,0) is the cone around the centre.
R_H(e) = dip exponent of the flat-histogram instance (variational definition, mf_lib.Model.R_dip)."""
import numpy as np, sys, time
from mf_lib import Model, hb


def theta_na_shell(M, x, ms, nz0=21, only_centre=False):
    best = (-1.0, None, None)
    z0s = [(0.0, 0.0)] if only_centre else [(a0, b0) for a0 in np.linspace(0, 1, nz0) for b0 in np.linspace(0, 1, nz0)]
    for m in ms:
        f = M.fields(m)
        base = f["MI"] + f["I"]
        for (a0, b0) in z0s:
            dist = m * np.abs(M.A - a0) + (1 - m) * np.abs(M.B - b0)
            val = base + M.u * dist
            V = val.min()
            ok = val - V <= x
            th = f["MI"][ok].min()
            if th > best[0]:
                best = (float(th), float(m), (float(a0), float(b0)))
    return best


def main():
    bJ, bB, u = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
    G = int(sys.argv[4]) if len(sys.argv) > 4 else 161
    if bJ < 0:                       # field control: phi = theta*kappa with p = bB
        import math
        p = bB
        phi = lambda k: math.log((1 - p) / p) * k
    else:
        phi = lambda k: -(bJ / 2) * (2 * k - 1) ** 2 - bB * (2 * k - 1)
    M = Model(phi, u, G=G)
    ms = np.linspace(0.1, 0.9, 9) if bB == 0 and bJ >= 0 else np.linspace(0.1, 0.9, 17)
    t0 = time.time()
    print(f"bJ={bJ} bB={bB} u={u} G={G}")
    for e in [float(v) for v in sys.argv[5:]] or [0.0]:
        RHd, md = M.R_dip(-M.vk, e, ms, iters=14)
        RHf, mf = M.R_formula(e, ms, "v")
        x = e + RHd
        cone = theta_na_shell(M, x, ms, only_centre=True)
        shell = theta_na_shell(M, x, ms)
        cone_f = theta_na_shell(M, e + RHf, ms, only_centre=True)
        print(f" e = {e:+.4f}: R_H(dip) = {RHd:.5f} (m={md:.2f})  R_H(formula) = {RHf:.5f} | at x = e + R_H(dip) = {x:.5f}: "
              f"theta_na cone = {cone[0]:.5f}, shell = {shell[0]:.5f} (m={shell[1]:.2f}, z0=({shell[2][0]:.2f},{shell[2][1]:.2f}))"
              f" | cone at e + R_H(formula): {cone_f[0]:.5f}   [{time.time()-t0:.0f}s]", flush=True)


main()
