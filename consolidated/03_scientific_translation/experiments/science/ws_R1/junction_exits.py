#!/usr/bin/env python3
"""R1: explicit evidence for junction_scan.py -- where are the exits?  For the cube's optimal profile (m=1/2, shell l*),
Curie-Weiss B=0, e=0: the smallest MI among feasible exits, by type of the exit (dense grid 2001^2, no polishing:
values are upper bounds of the true minima of each band, accurate to about 1e-4)."""
import math
import numpy as np
import corollary_1191_checks as C
from thm_1190 import R_unif
def scan(u, bJ, e=0.0, ng=2001):
    rt = C.Rate(C.cw(bJ), u)
    lstar = 0.5*math.tanh(u/2); m, a, b = 0.5, 0.5 + lstar, 0.5 - lstar
    budget = e + float(C.MI2(m, a, b)) + float(rt.I(0.5))
    g = np.linspace(0, 1, ng); A, B = np.meshgrid(g, g, indexing="ij")
    typ = m*A + (1-m)*B
    cons = u*(m*np.abs(A-a) + (1-m)*np.abs(B-b)) + rt.I(typ)
    obj = np.where(cons <= budget, C.MI2(m, A, B), np.inf)
    out = []
    for lo, hi in ((0.0, 0.3), (0.3, 0.45), (0.45, 0.49), (0.49, 0.51), (0.51, 0.55), (0.55, 0.7), (0.7, 1.0)):
        band = np.where((typ >= lo) & (typ <= hi), obj, np.inf)
        j = int(np.argmin(band))
        out.append((lo, hi, float(band.flat[j]), float(A.flat[j]), float(B.flat[j])))
    return out, R_unif(e, u), float(rt.I(0.5))
for (u, bJ, note) in ((3.0, 2.0, "below bJ* = 2.1158"), (3.0, 2.25, "above bJ*"), (6.0, 5.0, "below bJ* = 5.2783"), (2.5, 1.7, "below bJ*(u=2.5)")):
    out, ru, bar = scan(u, bJ)
    print(f"u = {u}, bJ = {bJ} ({note}); R_unif(0) = {ru:.6f}; barrier I(1/2) = {bar:.4f}")
    for lo, hi, v, aa, bb in out:
        print(f"    exits of type in [{lo:.2f}, {hi:.2f}]: min MI = {v:.6f}" + (f" at (a', b') = ({aa:.4f}, {bb:.4f})" if math.isfinite(v) else "  (none feasible)")
              + ("   <-- below R_unif" if v < ru - 2e-4 else ""))
