"""t11: the worst-case pair (theta_na, R^max) from the closed game formula:
 (i) closed form F(gamma,t) against the 2x2 game solver; (ii) R^max from F* against R_max();
 (iii) theta_na = R^max o S^{-1} against the max-min formula max_m min{I : Icone_m <= x}, also for x < h (negative e);
 (iv) HintPair properties: slopes in [-1,0], convexity, S increasing, theta_na continuous, theta_na(h) = h, a, E."""
import math, numpy as np, time
from flib import *
rng = np.random.default_rng(11)
t0 = time.time()
worst = 0.0
for _ in range(2000):
    p = rng.uniform(0.02, 0.98); u = rng.uniform(0.1, 5); g = rng.uniform(-u, u); t = rng.uniform(1e-3, 1.0)
    worst = max(worst, abs(float(F_game(p, u, g, t)) - minus_log_val(p, u, g, t)))
    worst = max(worst, abs(float(F_game(p, u, g, 1.0))))
print("(i) closed form vs game solver, and F(gamma,1) = 0: max abs error", worst)
for p, u in ((0.5, 1.0), (0.3, 1.0), (0.1, 2.0), (0.05, 2.0), (0.2, 4.0)):
    st = Site(p, u)
    wp = WorstPair(p, u)
    ms = np.linspace(1e-6, 1 - 1e-6, 200001)
    a_mm = float(st.I(ms, st.eta1, st.eta0).max())
    Egrid = max(thr_additive(p, u, g) for g in np.linspace(-u, u, 801))
    print(f"p={p} u={u}: E={wp.E:.6f} (grid of thresholds {Egrid:.6f})  h={wp.h:.6f}  a={wp.a:.6f} (max_m I_cone = {a_mm:.6f})  e_c={wp.ec:.6f}")
    # (ii)
    w2 = 0.0
    for frac in (0.0, 0.2, 0.5, 0.8):
        e = frac * wp.E
        w2 = max(w2, abs(wp.R(e) - R_max(p, u, e, ngam=41, nt=401)[0]))
    # (iii)
    w3 = 0.0; rows = []
    for x in (0.02 * wp.h, 0.2 * wp.h, 0.6 * wp.h, wp.h, wp.h + 0.3 * (wp.E - wp.h), wp.h + 0.8 * (wp.E - wp.h)):
        e = wp.Sinv(x)
        mm = maxmin_precise(st, "na", x)
        w3 = max(w3, abs(mm[0] - wp.theta_na(x)))
        rows.append(f"x={x:.5f} (e={e:+.5f}): pair {wp.theta_na(x):.7f} maxmin {mm[0]:.7f}")
    # (iv)
    es = np.linspace(wp.ec - 0.05, wp.E * 1.05, 4001)
    Rs = wp.R(es)
    slopes = np.diff(Rs) / np.diff(es)
    conv = np.diff(slopes).min()
    Ss = es + Rs
    print(f"   (ii) max |R^max - R_max()| = {w2:.2e};  (iii) max |pair - maxmin| = {w3:.2e};  (iv) slope range [{slopes.min():.6f}, {slopes.max():.6f}], "
          f"min second difference {conv:.2e}, S nondecreasing: {bool((np.diff(Ss) >= -1e-12).all())}, theta_na(h) - h = {wp.theta_na(wp.h) - wp.h:.2e}")
    for r in rows: print("      ", r)
print("time", time.time() - t0)
