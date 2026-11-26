"""r10_07c: does the safe value of the tilt-state recursion converge to the restricted value at
small p?  One point (p=0.01, u=1, t=0.15, q~=0.03), G = 401 .. 3201, both modes."""
import time, numpy as np
from r10_tilt import Tilt
t0 = time.time()
p, u, t, qt = 0.01, 1.0, 0.15, 0.03
for G in (401, 801, 1601):
    Ts = Tilt(p, u, G, "safe")
    a, b, w = Ts.renyi_rate(t, qt, sweeps=6000, tol=1e-7)
    Tr = Tilt(p, u, G, "restricted")
    ar, br, wr = Tr.renyi_rate(t, qt, sweeps=6000, tol=1e-7)
    print("G=%d (cell %.5f): safe in [%.6f, %.6f]   restricted in [%.6f, %.6f]   (%.0fs)" % (G, 2 * Ts.us / G, b, a, br, ar, time.time() - t0), flush=True)
print("time %.0fs" % (time.time() - t0))
