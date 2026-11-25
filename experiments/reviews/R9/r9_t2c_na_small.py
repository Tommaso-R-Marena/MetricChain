# R9 test 2c: theta_na(x) for x BELOW h = R^max(0), i.e. where S^{-1}(x) < 0 (the regime of negative accuracies of the
# pair): direct max-min  max_m min{ I(z) : I^cone(z) <= x }  (grid + SLSQP polish, no duality) against R^max o S^{-1}
# and against the tau-form max_tau (F*(tau) - tau x)/(1 - tau).  Also the dual pair of F4(c):
# sup{theta : max_m F_m(theta) > x} with F_m(theta) = min{I^cone : I <= theta}.
import numpy as np, time
from scipy.optimize import minimize, minimize_scalar
from r9lib import Par
t0 = time.time()
def minI_polish(P, m, level):
    v0, z0 = P.minI('na', m, level, 0.0, N=201, zooms=5)
    if z0 is None: return np.inf
    best = v0
    fI = lambda z: float(P.cons('na', m, z[0], z[1])[0]); fc = lambda z: level - float(P.cons('na', m, z[0], z[1])[1])
    for start in (z0, (P.eta1, P.eta0)):
        r = minimize(fI, start, method='SLSQP', bounds=[(1e-12, 1 - 1e-12)] * 2, constraints=[{'type': 'ineq', 'fun': fc}], options={'ftol': 1e-15, 'maxiter': 500})
        if r.success and fc(r.x) >= -1e-10: best = min(best, r.fun)
    return best
def maxmin(P, level):
    ms = np.linspace(0.02, 0.98, 49); vals = np.array([minI_polish(P, m, level) for m in ms]); i = int(np.argmax(vals))
    r = minimize_scalar(lambda m: -minI_polish(P, m, level), bounds=(ms[max(i - 1, 0)], ms[min(i + 1, 48)]), method='bounded', options={'xatol': 1e-8})
    return max(-r.fun, vals[i]), (r.x if -r.fun >= vals[i] else ms[i])
dev = 0.0
for (p, u) in [(0.1, 2.0), (0.3, 1.0), (0.2, 4.0), (0.5, 1.0)]:
    P = Par(p, u); hh = P.Rmax(0.0); a = -P.ec()
    for f in (0.02, 0.2, 0.5, 0.8):
        x = f * hh
        e = P.Sinv(x); form = P.Rmax(e); tau = P.theta_na_tau(x); mm, mst = maxmin(P, x)
        dev = max(dev, abs(mm - form), abs(tau - form))
        print(f"p={p} u={u} x={f}h={x:.5f}: S^-1(x) = {e:+.5f} (< 0); R^max o S^-1 = {form:.8f}; tau-form {tau:.8f}; direct max-min {mm:.8f} (m*={mst:.4f}); a = {a:.5f}   [{time.time()-t0:.0f}s]")
print(f"largest deviation: {dev:.1e}")
