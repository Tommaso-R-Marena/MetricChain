#!/usr/bin/env python3
"""R8 / script 09 -- independent replication of the two examples quoted in A16 (b) and of the
'100.036 against 100.036' of A16.6 (iii), with my own code (r8_02_twin, r8_04_theorem166).

  A16(b): n = 2000, u = 1, rho1 = rho0 + 0.01, gap 0.050 n: r2 = 899, kappa* = 244.57, against the radius 860
          of the smallest dip that does the same without the datum;
          n = 600, u = 4, gap 0.30 n: r2 = 190 against 147.
  A16.6 (iii): 100.036 against 100.036 at n = 2000.
Run: python3 r8_09_replicate_examples.py   (about 2 minutes)
"""
import math, io, contextlib
import numpy as np
from scipy.special import logsumexp
from r8_lib import *
import r8_02_twin as TW
from r8_04_theorem166 import plateau_ball

def nodatum_radius(n, u, eps):
    """least r such that the cone dip -u (r - d)_+ on the flat instance raises ln Z by more than eps"""
    lc = lnC(n); d = np.arange(n + 1)
    for r in range(1, n // 2 + 1):
        lw = lc + u * np.maximum(r - d, 0)
        if float(logsumexp(lw)) - n * LN2 > eps:
            return r
    return None

for (n, u, drho, e1, quoted) in ((2000, 1.0, 0.01, 0.05, "r2 = 899, kappa* = 244.57, no datum 860"),
                                 (600, 4.0, 0.01, 0.30, "r2 = 190, no datum 147")):
    with contextlib.redirect_stdout(io.StringIO()):
        r = TW.find_case(n, u, rho0(u) + drho, e1, 0.5)
    G1 = plateau_ball(n, u, r["r2"] - 1, r["U0"])[0] - r["lnZ0"]
    print(f"n={n} u={u} rho1=rho0+{drho} gap>{e1}n: mine r1={r['r1']} r2={r['r2']} kappa*={r['kappa']:.2f} gap={r['gap']:.3f} "
          f"G(r2-1)={G1:.3f}; no datum: radius {nodatum_radius(n,u,e1*n)}   | addendum: {quoted}")
