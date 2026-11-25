#!/usr/bin/env python3
"""R8 / script 08 -- a proof-level link between the exact twin and G(R), checked numerically.

Claim (report, section 2, R8.3).  Let g' = min(g0, T_k*) be the exact plateau twin of radius r2 and
g'' = T_k* alone on the flat background (a plateau on the ball B(a', r2-1) at the level u k*), with
mean energy U''.  Then
   (1) Z'' = Zpl(r2-1, U'')                      (g'' is the plateau of its own energy)
   (2) Z'  >= Z''                                (g' <= g'' pointwise; no hypothesis on the overlap)
   (3) -1 <= d ln Zpl(R,U)/dU < 0                (d ln Z/dc = mu(P), dU/dc = -mu(P)(1+c+U))
hence     G(r2-1) - (U'' - U0)_+  <=  gap(r2)  <=  G(r2)        (right end: Lemma A16.5).
Also the heuristic size  gap(r2) - G(r2-1) ~ e^{-gap} (1 - |U0| 2^n/W).

Run: python3 r8_08_matching.py      (about 1 minute)
"""
import math, io, contextlib
import numpy as np
from scipy.special import logsumexp
from r8_lib import *
import r8_02_twin as TW
from r8_04_theorem166 import plateau_ball, CASES

print("    n    u   r2    gap(twin)    G(r2-1)      U''-U0      gap-G(r2-1)   e^-gap(1-|U0|2^n/W)   lower bound holds   dlnZpl/dU in [-1,0]")
ok = True
for c in CASES + [(800, 1.0, rho0(1.0) + 0.02, 0.004, 0.5), (800, 1.0, rho0(1.0) + 0.02, 0.008, 0.5)]:
    with contextlib.redirect_stdout(io.StringIO()):
        r = TW.find_case(*c)
    n, u, r1, r2, kap = r["n"], r["u"], r["r1"], r["r2"], r["kappa"]
    lc = lnC(n); d = np.arange(n + 1)
    g2 = -u * np.minimum(kap, np.maximum(r2 - d, 0.0))
    lnZ2, U2, S2 = radial_stats(n, g2)
    G1 = plateau_ball(n, u, r2 - 1, r["U0"], lc)[0] - r["lnZ0"]
    # (1): plateau of its own energy
    chk1 = abs(plateau_ball(n, u, r2 - 1, U2, lc)[0] - lnZ2) < 1e-8
    # (3): finite-difference derivative of ln Zpl in U
    dU = 1e-3 * max(1.0, abs(r["U0"]))
    der = (plateau_ball(n, u, r2 - 1, r["U0"] + dU, lc)[0] - plateau_ball(n, u, r2 - 1, r["U0"] - dU, lc)[0]) / (2 * dU)
    lnW = float(logsumexp(lc[:r1] + u * (r1 - d[:r1])))
    pred = math.exp(-r["gap"]) * (1 - abs(r["U0"]) * math.exp(n * LN2 - lnW))
    lb = r["gap"] >= G1 - max(U2 - r["U0"], 0.0) - 1e-9
    print(f"  {n:5d} {u:4.1f} {r2:4d}  {r['gap']:10.5f}  {G1:10.5f}   {U2-r['U0']:+.3e}    {r['gap']-G1:+.3e}       {pred:+.3e}             {lb and chk1}               {-1-1e-6 <= der <= 1e-9} ({der:+.4f})")
    ok &= lb and chk1 and (-1 - 1e-6 <= der <= 1e-9)
print("SUMMARY  G(r2-1) - (U''-U0)_+ <= gap(r2) in all cases:", ok)
