"""t03: precise evaluation: hint0 (max-min) against the closed form; H (max-min) against max_gamma R_gamma;
is the exit type inside the window (H = Hraw)?"""
import math, numpy as np, time
from flib import *
t0 = time.time()
worst0 = worstH = 0.0
for p, u in ((0.5, 1.0), (0.3, 1.0), (0.1, 1.0), (0.1, 2.0), (0.05, 2.0), (0.2, 4.0), (0.02, 3.0), (0.4, 0.5)):
    st = Site(p, u)
    gs = np.linspace(-u, u, 401)
    E = max(thr_additive(p, u, g) for g in gs)
    for frac in (0.0, 0.1, 0.3, 0.6, 0.9):
        e = frac * E
        r0, _ = R_additive(p, u, 0.0, e)
        rmax, gstar = R_max(p, u, e, ngam=41, nt=401)
        a0 = maxmin_precise(st, "hint0", e)
        aH = maxmin_precise(st, "H", e)
        aHr = maxmin_precise(st, "Hraw", e)
        worst0 = max(worst0, abs(a0[0] - r0)); worstH = max(worstH, abs(aH[0] - rmax))
        inwin = st.kmin - 1e-9 <= aH[4] <= st.kmax + 1e-9
        print(f"p={p} u={u} eps1={e:.5f}: R_0={r0:.8f} maxmin0={a0[0]:.8f} | max_g R_g={rmax:.8f} (g*={gstar:+.4f}) maxminH={aH[0]:.8f} "
              f"(m*={aH[1]:.4f}, x*={aH[2]:.4f}, y*={aH[3]:.4f}, kappa*={aH[4]:.4f}, in window: {inwin}) Hraw={aHr[0]:.8f}")
print("max |maxmin0 - R_0| =", worst0, "  max |maxminH - max_gamma R_gamma| =", worstH, " time", time.time() - t0)
