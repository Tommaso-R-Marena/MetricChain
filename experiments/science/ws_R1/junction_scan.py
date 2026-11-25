#!/usr/bin/env python3
"""R1: Corollary 11.91(iii) / Proposition 11.81(b): is R_H = R_unif up to beta J*(e,u) = 1 + u c2/(2L) for every slope?
(The new checkpoint 89ac710 reports from referee R10 that for larger slopes the junction comes earlier.)
r_mu(e) with exits of every type at the cube's optimal profile (m = 1/2, shell l* = tanh(u/2)/2), Curie-Weiss, B = 0.
R_H = R_unif iff this value equals R_unif(e) (Theorem 11.90(c): no other slice profile reaches R_unif)."""
import math, sys
import numpy as np
import corollary_1191_checks as C
from thm_1190 import R_unif, Psi_c
print(f"{'u':>4} {'e':>7} {'bJ*':>8} {'bJ':>8} {'frac':>5} {'r_mu(e)':>12} {'R_unif(e)':>12} {'diff':>10} contact  exit type")
first_fail = {}
for u in (1.0, 2.0, 3.0, 4.0, 6.0):
    for efrac in (0.0, 0.3):
        e = efrac * Psi_c(u)
        Lam1 = math.log(2 / (1 + math.exp(-u)))
        rho = (Lam1 + e) / u
        bJs = 1 + u * (1 / (2 * rho * (1 - rho)) - 2) / (2 * math.log((1 - rho) / rho))
        lstar = 0.5 * math.tanh(u / 2)
        for frac in (0.3, 0.6, 0.8, 0.9, 0.97):
            bJ = 1 + frac * (bJs - 1)
            rt = C.Rate(C.cw(bJ), u)
            contact = abs(float(rt.I(0.5)) - float(rt.v(0.5))) < 1e-9
            val = C.r_general(rt, "v", 0.5, 0.5 + lstar, 0.5 - lstar, e, u, ngrid=1001, polish=12)
            ru = R_unif(e, u)
            flag = val < ru - 1e-7
            if flag and (u, efrac) not in first_fail:
                first_fail[(u, efrac)] = (bJ, bJs, frac)
            print(f"{u:4.1f} {e:7.4f} {bJs:8.4f} {bJ:8.4f} {frac:5.2f} {val:12.8f} {ru:12.8f} {val - ru:10.2e} {str(contact):>7}  {'EARLY JUNCTION' if flag else ''}")
            sys.stdout.flush()
print()
if first_fail:
    for (u, ef), (bJ, bJs, frac) in sorted(first_fail.items()):
        print(f"u = {u}, e = {ef} Psi_c(u): R_H < R_unif already at bJ = {bJ:.4f} = 1 + {frac}(bJ* - 1), bJ* = {bJs:.4f}")
else:
    print("no early junction on this grid")
