# R9 test 13: spot-check of the table of Section 3.7 (thresholds and exponents against the field), own code.
import numpy as np, time
from math import log, exp
from scipy.optimize import minimize, minimize_scalar
from r9lib import Par, kl
t0 = time.time()
print("table of Section 3.7 (u; theta; E_0; E; R_0(0+); R^max(0+); gamma* at eps->0; a; a_pi)")
rep = {(1.0, 0.0): (.12011, .12011, .029139, .029139, 0, .1109, .1109), (1.0, 0.5): (.11367, .11383, .027531, .027621, -.055, .1052, .1225),
       (1.0, 1.0): (.09678, .09728, .023340, .023618, -.105, .0899, .1201), (1.0, 2.0): (.05400, .05479, .012884, .013322, -.177, .0507, .0826),
       (1.0, 3.0): (.02395, .02446, .005672, .005954, -.214, .0227, .0409), (2.0, 0.0): (.43378, .43378, .097281, .097281, 0, .3278, .3278),
       (2.0, 0.5): (.41607, .41774, .092895, .093758, -.170, .3162, .4078), (2.0, 1.0): (.36766, .37315, .081093, .083936, -.330, .2836, .4621),
       (2.0, 2.0): (.22872, .23925, .048716, .054171, -.583, .1841, .4338), (2.0, 3.0): (.11140, .11942, .023040, .027194, -.734, .0928, .2732)}
worst = 0.0
for (u, th), r in rep.items():
    P = Par(1 / (1 + exp(th)), u)
    E, gE, E0 = P.E(); R0 = P.R0(0.0); Rm, tst, gst = P.Rmax(0.0, True); a = -P.ec()
    api = max(float(kl(P.eta1, P.q)), float(kl(P.eta0, P.p)))
    mine = (E0, E, R0, Rm, gst, a, api)
    dev = max(abs(x - y) for x, y in zip(mine, r))
    worst = max(worst, dev)
    print(f"  u={u} theta={th}: " + " ".join(f"{x:.6f}" for x in mine) + f"   | max deviation from the printed row: {dev:.1e}")
print(f"  largest deviation from the report's table: {worst:.1e} (printed digits: 4-6)")
# (Proposition F11(a) is checked in r9_t13b_F11.py: for product samplers the maximum over m is at m = 0 or 1.)
