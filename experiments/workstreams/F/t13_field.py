"""t13: dependence on the field theta (p = 1/(1+e^theta)):  the worst-case exponent R^max, the hinted exponent
R_0 of the instance g = 0, the non-adaptive exponent, and what plain Monte Carlo from pi_f would need."""
import math, numpy as np, time
from flib import *
t0 = time.time()
for u in (1.0, 2.0):
    print(f"u = {u}")
    print("  theta    p      | thresholds: g=0     class E  gamma*(E) | eps1 -> 0: R_0      R^max   gamma*   theta_na=a   plain MC a_pi | eps1 = E/4: R_0      R^max    theta_na   plainMC")
    for theta in (0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0):
        p = 1 / (1 + math.exp(theta))
        st = Site(p, u)
        wp = WorstPair(p, u)
        w0 = WorstPair(p, u, gam_fixed=0.0)
        gs = np.linspace(-u, u, 2001)
        thr = np.array([thr_additive(p, u, g) for g in gs])
        gE = gs[int(np.argmax(thr))]
        g0 = wp.gstar_t[int(np.argmax(wp.Fstar))]                    # gamma* at eps1 = 0 (maximiser of F*)
        ms = np.linspace(1e-6, 1 - 1e-6, 20001)
        a_pi = float((st.J(ms, st.eta1, st.eta0)).max())              # max_m KL(pi_s || pi)/n
        e = wp.E / 4
        na_pi = maxmin_J(st, "na", e)[0]
        print(f"  {theta:5.2f}  {p:.4f} |            {w0.E:.5f}  {wp.E:.5f}  {gE:+.4f}  |          {w0.h:.6f} {wp.h:.6f} {g0:+.4f}  {wp.a:.6f}   {a_pi:.6f}    |"
              f"            {float(w0.R(e)):.6f} {float(wp.R(e)):.6f} {wp.theta_na(e):.6f}  {na_pi:.6f}")
print("time", time.time() - t0)
