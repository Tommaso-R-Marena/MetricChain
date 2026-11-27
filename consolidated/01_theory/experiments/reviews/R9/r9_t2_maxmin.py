# R9 test 2: R_0, R_gamma, R^max, theta_na by direct max-min optimisation over profiles (m; a, b)
# (grid + zoom, no duality) against the formulas built from F*; the identity theta_na(e + R^max(e)) = R^max(e)
# and its failure with R_0; the closed form max_m [h(m) - h((Lam_m+e)/u)]_+ ; the case p = 1/2.
import numpy as np, time, sys
from math import log, exp
from scipy.optimize import minimize_scalar, brentq
from r9lib import Par, h, kl
t0 = time.time()
pairs = [(0.1, 2.0), (0.3, 1.0), (0.05, 2.0), (0.2, 4.0), (0.7, 1.5), (0.5, 1.0)]
if len(sys.argv) > 1: pairs = pairs[:int(sys.argv[1])]
dmax = dict(R0=0.0, R0closed=0.0, Rg=0.0, Rmax=0.0, na=0.0, na2=0.0, natau=0.0, ident=0.0)
for (p, u) in pairs:
    P = Par(p, u); E, gE, E0 = P.E(); a = -P.ec()
    print(f"p={p} u={u}: E={E:.6f} E0={E0:.6f} a={a:.6f}")
    for frac in (0.0, 0.1, 0.3, 0.6, 0.9):
        e = frac * E
        # hint at g = 0
        r0_f = P.R0(e); r0_mm, m0 = P.maxmin('R0', e)
        # closed form max_m [h(m) - h((Lam_m+e)/u)]_+
        def cf(m):
            rho = ((1 - m) * P.Lam0 + m * P.Lam1 + e) / u
            return float(h(m) - h(rho)) if rho <= min(m, 1 - m) else 0.0
        ms = np.linspace(1e-4, 1 - 1e-4, 20001); vals = np.array([cf(m) for m in ms]); i = int(np.argmax(vals))
        rr = minimize_scalar(lambda m: -cf(m), bounds=(ms[max(i-1,0)], ms[min(i+1,len(ms)-1)]), method='bounded', options={'xatol':1e-12})
        r0_c = max(-rr.fun, vals[i])
        # hardest additive instance
        rm_f, tstar, gstar = P.Rmax(e, True); rm_mm, mm = P.maxmin('Rmax', e)
        # one additive instance gamma != 0
        g1 = -0.5 * u if p < 0.5 else 0.4 * u
        rg_f = P.Rg(g1, e); rg_mm, _ = P.maxmin('Rg', e, g=g1)
        # non-adaptive at x = S(e) = e + R^max(e)   (identity) and at the same x with R_0
        x = e + rm_f
        if x > 1e-9:
            na_f = P.theta_na(x); na_tau = P.theta_na_tau(x)
            na_mm, mna = P.maxmin('na', x); na2_mm, _ = P.maxmin('na2', x)
        else:
            na_f = na_tau = na_mm = na2_mm = float('nan'); mna = float('nan')
        x0 = e + r0_f
        na_at_x0 = P.theta_na(x0) if x0 > 1e-9 else float('nan')
        dmax['R0'] = max(dmax['R0'], abs(r0_f - r0_mm)); dmax['R0closed'] = max(dmax['R0closed'], abs(r0_f - r0_c))
        dmax['Rmax'] = max(dmax['Rmax'], abs(rm_f - rm_mm)); dmax['Rg'] = max(dmax['Rg'], abs(rg_f - rg_mm))
        if x > 1e-9:
            dmax['na'] = max(dmax['na'], abs(na_f - na_mm)); dmax['na2'] = max(dmax['na2'], abs(na_f - na2_mm))
            dmax['natau'] = max(dmax['natau'], abs(na_f - na_tau)); dmax['ident'] = max(dmax['ident'], abs(na_f - rm_f))
        print(f"  e={frac:.1f}E: R0: game {r0_f:.7f} maxmin {r0_mm:.7f} closed {r0_c:.7f} (m*={m0:.4f}) | Rmax: F* {rm_f:.7f} maxmin {rm_mm:.7f} (m*={mm:.4f}, gamma*={gstar:+.4f}, t*={tstar:.4f}) | R_g(g={g1:+.2f}): {rg_f:.7f} / {rg_mm:.7f}")
        print(f"          theta_na at x=e+Rmax(e)={x:.6f}: R^max o S^-1 {na_f:.7f}, tau-form {na_tau:.7f}, maxmin(I^cone) {na_mm:.7f} (m*={mna:.4f}), maxmin(I+c_H) {na2_mm:.7f}; identity: theta_na(e+Rmax(e)) - Rmax(e) = {na_f-rm_f:+.2e}; with R0: theta_na(e+R0(e)) - R0(e) = {na_at_x0 - r0_f:+.6f}; Rmax-R0 = {rm_f-r0_f:+.6f}")
    sys.stdout.flush()
print("largest deviations:", {k: f"{v:.2e}" for k, v in dmax.items()})
# p = 1/2: the three exponents against KL((Lam1+e)/u || 1/2) and min{KL(rho||1/2) : KL(rho||p_u) <= e}
for u in (0.5, 1.0, 2.0, 4.0):
    P = Par(0.5, u); Lam1 = log(2 / (1 + exp(-u))); pu = 1 / (1 + exp(u)); Es = log(np.cosh(u / 2))
    dd = 0.0
    for frac in (0.05, 0.3, 0.7):
        e = frac * Es
        hint = float(kl((Lam1 + e) / u, 0.5))
        rho = brentq(lambda r: float(kl(r, pu)) - e, pu, 0.5); na = float(kl(rho, 0.5))
        dd = max(dd, abs(P.R0(e) - hint), abs(P.Rmax(e) - hint), abs(P.theta_na(e) - na))
    print(f"p=1/2 u={u}: E - ln cosh(u/2) = {P.E()[0]-Es:+.2e}; max deviation of (R0, Rmax, theta_na) from the Section 11.16 formulas at 3 accuracies: {dd:.2e}")
print(f"[{time.time()-t0:.1f}s]")
