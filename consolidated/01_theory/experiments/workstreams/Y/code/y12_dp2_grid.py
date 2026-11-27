"""Grid-convergence study of the tilt-state recursion at fixed (p, t, qt): the control grid errs on the unsafe side, so the
value must be seen to converge before it is used as an upper bound.
usage: python3 y12_dp2_grid.py p t qt"""
import sys, time, math
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ydp2 import DP2
p, t, qt = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]); t0 = time.time()
print("p=%.2f t=%.3f qt=%.4f" % (p, t, qt), flush=True)
for (G, C) in ((101, 11), (201, 11), (101, 21), (201, 21), (401, 21), (201, 41), (401, 41), (801, 41), (401, 81)):
    lo, hi = DP2(p, 1.0, G, C).renyi_rate(t, qt, iters=4000, tol=1e-9)
    print("  G=%4d C=%3d: rate in [%.7f, %.7f]   [%.0f s]" % (G, C, lo, hi, time.time() - t0), flush=True)
