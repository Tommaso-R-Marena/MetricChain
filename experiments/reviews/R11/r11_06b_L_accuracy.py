"""R11 / 06b -- section 6.2, column "(L), L = 3": the accuracy version of the lower reduction,
h >= max_t [F_L(t) - t kappa_m] / (L + m)  with the plain block function F_L (all 38 vertices),
and the columns a >= , E >= of (L') for L = 3.
Report: (L): 0.01873 (m=2), 0.01629 (3), 0.01251 (5), 0.00153 (5) for p = 0.4, 0.3, 0.2, 0.1;
        (L') a >= 0.07987, 0.06978, 0.05681, 0.03518;  E >= 0.10199, 0.09375, 0.07830, 0.04459.

Run:  python3 r11_06b_L_accuracy.py     (about 1 minute)
"""
import numpy as np
from r11lib import *

u = 1.0
L = 3
V = lipschitz_vertices(L, [u] * L)


def kappa(p, m):
    lam = 1 - 2 * p
    return np.log((1 + lam ** (m + 1)) / (1 - lam ** (m + 1)))


for p, mrep, rep in ((0.4, 2, 0.01873), (0.3, 3, 0.01629), (0.2, 5, 0.01251), (0.1, 5, 0.00153)):
    s, pi = chain_law(L, p)
    logP = gibbs_logs(np.log(pi), V)
    best = (-1, None)
    for m in range(0, 6):
        km = kappa(p, m)
        tt, v = golden_max(lambda t: maximise_G_fast(logP, t)[0] - t * km, 0.02, 0.98, tol=1e-4)
        if v / (L + m) > best[0]:
            best = (v / (L + m), m)
    print(f"p={p}: (L) h >= {best[0]:.5f} at m = {best[1]}   (report {rep:.5f} at m = {mrep})")

for p, arep, erep in ((0.4, 0.07987, 0.10199), (0.3, 0.06978, 0.09375), (0.2, 0.05681, 0.07830), (0.1, 0.03518, 0.04459)):
    s, pi = chain_law(L, p)
    ba = be = (-1, None)
    for m in range(0, 6):
        red = u - kappa(p, m)
        if red < 0:
            continue
        Vm = lipschitz_vertices(L, [red, u, red])
        logP = gibbs_logs(np.log(pi), Vm)
        a = maximise_a_fast(logP)[0] / (L + m)
        e = maximise_E_fast(logP)[0] / (L + m)
        ba = max(ba, (a, m))
        be = max(be, (e, m))
    print(f"p={p}: (L') L=3: a >= {ba[0]:.5f} (m={ba[1]}; report {arep:.5f});  E >= {be[0]:.5f} (m={be[1]}; report {erep:.5f})")
