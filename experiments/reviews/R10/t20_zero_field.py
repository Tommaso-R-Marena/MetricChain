"""bJ = 1.5, bB = 0.05, u = 1, e = 0: the zero residual (landscape 0) -- report 0.0075630; the dips sit in the
stable well, so the starts are profiles in the wells.  Also e = 0.01, 0.02 for the binary optimum of H
(report 0.0198677, 0.0152121) and the zero residual (0.0036644, 0.0012178)."""
import time
import numpy as np
from r10lib import *
from r10search import *
from r10tab import *
t0 = time.time()
M = Model(1.5, 0.05, 1.0)
zero = lambda k: 0.0 * np.asarray(k, float)
print("wells: stable minimum of I at", round(M.kmin, 4), "; contact", [(round(a, 4), round(b, 4)) for a, b in M.contact()])
wells = [(0.6, 0.03, 0.80), (0.4, 0.2, 0.97), (0.5, 0.05, 0.85), (0.59, 0.03, 0.80), (0.41, 0.80, 0.03), (0.5, 0.9, 0.06), (0.5, 0.3, 0.3)]
for e, rH, r0 in ((0.0, 0.0250232, 0.0075630), (0.01, 0.0198677, 0.0036644), (0.02, 0.0152121, 0.0012178)):
    RH, lH, mH = R_binary(M, e, starts=[(0.4761, 0.3260, 0.2707), (0.5, 0.3, 0.3), (0.45, 0.31, 0.28)])
    R0, l0, m0 = R_binary(M, e, land=zero, starts=wells)
    s2 = inner_dual(M, l0, m0, e + alpha(M, l0, m0), nk=1201, refine=5, use_v=False)[0] if False else float('nan')
    print(f"e={e}: H binary {RH:.7f} (m; a, b) = ({lH[0]:.4f}; {1-mH[0]:.4f}, {mH[1]:.4f}) (report {rH});  zero residual {R0:.7f} [{fmt(l0, m0)}] (report {r0})   t={time.time()-t0:.0f}", flush=True)
print("time", time.time() - t0)
