"""t02: hardest additive instance (max_gamma R_gamma) against the profile formula for the flat-histogram
instance H, and against the hinted exponent at g = 0."""
import math, numpy as np, time
from flib import *
t0 = time.time()
for p, u in ((0.5, 1.0), (0.3, 1.0), (0.1, 1.0), (0.1, 2.0), (0.05, 2.0), (0.2, 4.0)):
    st = Site(p, u)
    pg = ProfileGrid(st, nm=161, nx=401, ny=401)
    thr0 = thr_additive(p, u, 0.0)
    gs = np.linspace(-u, u, 401)
    thrs = [thr_additive(p, u, g) for g in gs]
    E = max(thrs); gE = gs[int(np.argmax(thrs))]
    print(f"p={p} u={u}: threshold at g=0: {thr0:.6f}; class threshold eps1* = {E:.6f} at gamma*={gE:.4f}")
    for frac in (0.0, 0.25, 0.5, 0.75, 0.95):
        e = frac * E
        r0, _ = R_additive(p, u, 0.0, e)
        rmax, gstar = R_max(p, u, e, ngam=41, nt=401)
        h0 = pg.maxmin("hint0", e)
        hH = pg.maxmin("H", e)
        hHraw = pg.maxmin("Hraw", e)
        print(f"   eps1={e:.5f}: R_0={r0:.6f} [grid hint0 {h0[0]:.6f}]   max_gamma R_gamma={rmax:.6f} (gamma*={gstar:+.4f})   "
              f"profile H={hH[0]:.6f} (m*={hH[1]:.3f}, kappa*={hH[4]:.3f}; window [{st.kmin:.3f},{st.kmax:.3f}])  Hraw={hHraw[0]:.6f}")
print("time", time.time() - t0)
