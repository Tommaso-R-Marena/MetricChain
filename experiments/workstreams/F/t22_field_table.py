"""t22: precise thresholds and exponents for the table of REPORT.md section 3.7 (thresholds via t = 1e-6)."""
import math, numpy as np
from scipy.optimize import minimize_scalar
from flib import *
for u in (1.0, 2.0):
    print("u =", u)
    for theta in (0.0, 0.5, 1.0, 2.0, 3.0):
        p = 1 / (1 + math.exp(theta))
        st = Site(p, u)
        E0 = thr_additive(p, u, 0.0)
        res = minimize_scalar(lambda g: -thr_additive(p, u, g), bounds=(-u, u), method="bounded", options=dict(xatol=1e-9))
        E, gE = -res.fun, res.x
        wp = WorstPair(p, u); w0 = WorstPair(p, u, gam_fixed=0.0)
        g0 = wp.gstar_t[int(np.argmax(wp.Fstar))]
        ms = np.linspace(1e-6, 1 - 1e-6, 200001)
        a = float(st.I(ms, st.eta1, st.eta0).max())
        api = float(st.J(ms, st.eta1, st.eta0).max())
        print(f"  theta={theta:.1f} p={p:.4f}: E_0={E0:.5f} E={E:.5f} (gamma*={gE:+.3f})  R_0(0)={w0.h:.6f} R^max(0)={wp.h:.6f} (gamma*={g0:+.3f})  a={a:.4f}  a_pi={api:.4f}"
              f"  | at E/4: R_0={float(w0.R(E/4)):.6f} R^max={float(wp.R(E/4)):.6f} theta_na={wp.theta_na(E/4):.6f}")
