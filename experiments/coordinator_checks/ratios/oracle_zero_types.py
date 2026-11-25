"""Zero residual with a field: the dip exponent restricted to profiles whose type is kappa,
rho_e(kappa) = sup{ r_mu(e) : type(mu) = kappa } (two blocks), against the unrestricted R_0(e) = max_kappa rho_e(kappa)."""
import sys, math, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location("fc", __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "..", "..", "falsify_conjectures.py"))
fc = importlib.util.module_from_spec(spec); sys.argv = ["x"]; spec.loader.exec_module(fc)
from scipy.optimize import minimize

def model(p, u):
    bB = 0.5 * math.log(p / (1 - p))
    M = fc.mf_model(0.0, bB, u, K=40001)
    M0 = dict(M); M0["v"] = lambda x: np.zeros_like(np.asarray(x, float))
    return M0

def r_profile(M0, m, x1, x0, e, G=300):
    lam = np.array([m, 1 - m]); mu = np.array([x1, x0])
    al = fc.mf_alpha(M0, lam, mu)
    if e + al < 0:           # not admissible at the zero landscape
        return 0.0
    v = fc.mf_inner(M0, lam, mu, e + al, G)
    return v if math.isfinite(v) else 0.0

def rho(M0, kappa, e):
    best = (0.0, None)
    for m in np.linspace(0.1, 0.9, 9):
        for x1 in np.linspace(max(kappa, 0.02), 0.98, 13):
            x0 = (kappa - m * x1) / (1 - m)
            if not (0.005 < x0 < x1):
                continue
            v = r_profile(M0, m, x1, x0, e)
            if v > best[0]:
                best = (v, (m, x1, x0))
    if best[1] is None:
        return best
    def neg(z):
        m, x1 = z
        if not (0.02 < m < 0.98 and 0.01 < x1 < 0.99):
            return 1.0
        x0 = (kappa - m * x1) / (1 - m)
        if not (0.002 < x0 < 0.998):
            return 1.0
        return -r_profile(M0, m, x1, x0, e, G=500)
    res = minimize(neg, best[1][:2], method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-9, maxiter=120))
    if -res.fun > best[0]:
        m, x1 = res.x
        best = (-res.fun, (m, x1, (kappa - m * x1) / (1 - m)))
    return best

for (p, u) in ((0.25, 1.0),):
    M0 = model(p, u)
    plo, phi = p * math.exp(-u) / (p * math.exp(-u) + 1 - p), p * math.exp(u) / (p * math.exp(u) + 1 - p)
    print(f"p={p} u={u}: window of one-body marginals [{plo:.4f}, {phi:.4f}]")
    for e in (0.02,):
        row = []
        for kappa in np.linspace(plo + 0.02, phi - 0.02, 7).tolist() + [p]:
            v, arg = rho(M0, kappa, e)
            row.append((kappa, v, arg))
        row.sort()
        kbest = max(row, key=lambda r: r[1])
        sys.stdout.flush(); print(f"   e={e}:  " + "  ".join(f"{k:.3f}:{v:.5f}" for k, v, _ in row))
        vp = [v for k, v, _ in row if abs(k - p) < 1e-12][0]
        print(f"        max over the grid of types: {kbest[1]:.5f} at type {kbest[0]:.3f} (m, x1, x0) = {tuple(round(float(t), 3) for t in kbest[2])};   at type p: {vp:.5f}   ratio {vp / kbest[1]:.3f}")
