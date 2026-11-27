"""r10_07g: safe tilt-state bound for the capacity exponent a at other slopes, reference Markov(q~)
scanned over a wide range.  Is a_inf below the cube's capacity?"""
import sys, time
import numpy as np
from r10lib import cube_exponents
from r10_tilt import Tilt
t0 = time.time()
ps = [float(x) for x in sys.argv[1:]] or [0.3]
for p in ps:
    for u in (1.0, 1.25, 1.5, 2.0, 2.5, 3.0):
        ac = cube_exponents(u)[2]
        T = Tilt(p, u, 801, "safe")
        best = (9.0, None)
        for qt in np.linspace(0.7 * p, 0.5, 25):
            a = T.cap_rate(float(qt), sweeps=3000, tol=1e-9)[0]
            if a < best[0]:
                best = (a, float(qt))
        print("p=%.2f u=%.2f: a <= %.6f (safe tilt, G=801, q~=%.4f)   cube %.6f   ratio %.4f   (%.0fs)" % (p, u, best[0], best[1], ac, best[0] / ac, time.time() - t0), flush=True)
