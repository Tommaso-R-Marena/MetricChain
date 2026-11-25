"""Addendum A15, size trend: the SAME instrument (the same absolute q grid and the same relative
tolerance) applied to chains of 11, 13 and 15 beads.  The grid is the Shannon grid of the longest
chain, q_j = j*pi/D_max(15 beads), j = 1..11 (q_max = 1.745 per lattice unit, i.e. q_max*b = 3.02 for
the bond length b = sqrt(3)); for the shorter chains it oversamples slightly.

Usage: python3 scattering_fixed_instrument.py            (about 2 minutes)
"""
from __future__ import annotations
import json, math, os, time
import numpy as np
from scattering_identified import setup, intensity, interval

def run(n, qs, tols=(0.0, 0.01, 0.05)):
    S = setup(n); N = S["N"]; M = len(S["g"])
    p = np.ones(M)/M
    thr = np.quantile(S["rg2"], 0.10)
    targets = {"Rg2 / <Rg2>": S["rg2"]/(p @ S["rg2"]), "end-to-end R2 / <R2>": S["ree2"]/(p @ S["ree2"]),
               "gauche fraction": S["g"]/n, "P(compact decile)": (S["rg2"] <= thr).astype(float)}
    F = np.stack([intensity(S, q) for q in qs], axis=1); m = p @ F
    Dmax = math.sqrt(S["ree2"].max()); rg0 = math.sqrt(p @ S["rg2"])
    rows = []
    print(f"# N = {N} beads, {M} conformations; D_max = {Dmax:.2f}, Rg = {rg0:.2f}; {len(qs)} points, q_max = {qs[-1]:.3f} "
          f"(q_max Rg = {qs[-1]*rg0:.2f}; Shannon channels in range: {qs[-1]*Dmax/math.pi:.1f})")
    for tol in tols:
        line = f"N={N} tol={tol:4.2f}:"
        for name, psi in targets.items():
            iv = interval(F, psi, m, tol)
            a0, a1 = float(psi.min()), float(psi.max())
            if iv is None:
                line += f"  {name}: LP failed"; continue
            lo, hi = iv; frac = (hi - lo)/(a1 - a0)
            rows.append(dict(n=n, N=N, npoints=len(qs), qmax=float(qs[-1]), tol=tol, target=name, lo=lo, hi=hi,
                             apriori_lo=a0, apriori_hi=a1, unidentified_fraction=frac))
            line += f"  {name.split(' ')[0]} [{lo:.3f},{hi:.3f}] ({frac:.3f})"
        print(line, flush=True)
    return rows

if __name__ == "__main__":
    Dmax15 = 14*math.sqrt(2.0)
    qs = np.array([j*math.pi/Dmax15 for j in range(1, 12)])
    out = []
    for n in (8, 10, 12):
        t0 = time.time(); out += run(n, qs); print(f"# n={n}: {time.time()-t0:.0f} s")
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scattering_fixed_instrument.json"), "w"), indent=1)
