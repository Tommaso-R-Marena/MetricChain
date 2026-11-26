"""r10_07a: quick checks of r10_tilt.py: (a) the control p=1/2 (the cube); (c) single points
of the headline (p=0.3, t=0.43, q~=0.255) in safe and restricted mode for several grids."""
import time
import numpy as np
from r10lib import cube_F, cube_exponents, E_F
from r10_tilt import Tilt

t0 = time.time()
u = 1.0
print("(a) control p = 1/2, q~ = 1/2: cube F(t) = t ln cosh(u/2) - ln cosh(t u/2)")
for G in (101, 401, 1601):
    for mode in ("safe", "restricted"):
        T = Tilt(0.5, u, G, mode)
        row = []
        for t in (0.25, 0.49, 0.75):
            a, b, _ = T.renyi_rate(t, 0.5, sweeps=300)
            row.append("t=%.2f: [%.7f, %.7f] (cube %.7f)" % (t, b, a, cube_F(t, u)))
        e1, e2, _ = T.thr_rate(0.5, sweeps=300)
        c1, c2, _ = T.cap_rate(0.5, sweeps=300)
        print("  G=%4d %-10s %s | E: [%.7f, %.7f] | a: [%.7f, %.7f]   feasible triples %d  (%.1fs)"
              % (G, mode, "  ".join(row), e2, e1, c2, c1, T.n_feasible(), time.time() - t0))
hc, tc, ac, Ec = cube_exponents(u)
print("   cube: h=%.7f a=%.7f E=%.7f" % (hc, ac, Ec))

print("(c) p=0.3, t=0.43, q~=0.255  (Y 6.3: safe G=1601 0.04468, restricted 0.04435)")
for G in (201, 401, 801, 1601):
    for mode in ("safe", "restricted"):
        T = Tilt(0.3, u, G, mode)
        a, b, _ = T.renyi_rate(0.43, 0.255, sweeps=600, tol=1e-9)
        print("  G=%4d %-10s  [%.6f, %.6f]   (%.1fs)" % (G, mode, b, a, time.time() - t0))
print("(c') p=0.3 threshold with Q = pi: E_F = %.6f  (Y: safe G=3201: 0.232538; restricted = E_F)" % E_F(0.3, u))
for G in (201, 401, 801, 1601):
    for mode in ("safe", "restricted"):
        T = Tilt(0.3, u, G, mode)
        a, b, _ = T.thr_rate(sweeps=1500, tol=1e-9)
        print("  G=%4d %-10s  [%.6f, %.6f]   (%.1fs)" % (G, mode, b, a, time.time() - t0))
