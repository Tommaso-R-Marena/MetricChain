# R9 test 2b: the max-min forms once more with a second, independent inner minimiser
# (SLSQP started from the grid optimum, constraint c(z) <= level) -- to see that the 1e-4 deviations of test 2 are
# artefacts of the grid/zoom search (they must shrink; a true discrepancy would stay).
import numpy as np, time, sys
from scipy.optimize import minimize, minimize_scalar
from r9lib import Par
t0 = time.time()
def minI_polish(P, kind, m, level, g=0.0):
    v0, z0 = P.minI(kind, m, level, g, N=201, zooms=4)
    if z0 is None: return np.inf
    best = v0
    fI = lambda z: float(P.cons(kind, m, z[0], z[1], g)[0])
    fc = lambda z: level - float(P.cons(kind, m, z[0], z[1], g)[1])
    for start in (z0, (min(z0[0] + 0.01, 1 - 1e-9), max(z0[1] - 0.01, 1e-9)), (max(z0[0] - 0.01, 1e-9), min(z0[1] + 0.01, 1 - 1e-9))):
        r = minimize(fI, start, method='SLSQP', bounds=[(1e-12, 1 - 1e-12)] * 2, constraints=[{'type': 'ineq', 'fun': fc}], options={'ftol': 1e-15, 'maxiter': 500})
        if r.success and fc(r.x) >= -1e-10: best = min(best, r.fun)
    return best
def maxmin_polish(P, kind, level, g=0.0):
    ms = np.linspace(0.02, 0.98, 49)
    vals = np.array([minI_polish(P, kind, m, level, g) for m in ms]); i = int(np.argmax(vals))
    r = minimize_scalar(lambda m: -minI_polish(P, kind, m, level, g), bounds=(ms[max(i-1,0)], ms[min(i+1,48)]), method='bounded', options={'xatol': 1e-8})
    return max(-r.fun, vals[i])
dev = 0.0
for (p, u, frac, kind, g) in [(0.5, 1.0, 0.3, 'R0', 0.0), (0.5, 1.0, 0.1, 'Rg', 0.4), (0.5, 1.0, 0.6, 'Rg', 0.4), (0.1, 2.0, 0.0, 'R0', 0.0),
                              (0.05, 2.0, 0.0, 'Rg', -1.0), (0.05, 2.0, 0.1, 'R0', 0.0), (0.2, 4.0, 0.9, 'R0', 0.0), (0.1, 2.0, 0.3, 'Rmax', 0.0),
                              (0.2, 4.0, 0.3, 'Rmax', 0.0), (0.3, 1.0, 0.1, 'Rmax', 0.0), (0.1, 2.0, 0.3, 'na', 0.0), (0.2, 4.0, 0.1, 'na', 0.0), (0.7, 1.5, 0.6, 'na', 0.0)]:
    P = Par(p, u); E = P.E()[0]; e = frac * E
    if kind == 'R0': form = P.R0(e); lev = e
    elif kind == 'Rg': form = P.Rg(g, e); lev = e
    elif kind == 'Rmax': form = P.Rmax(e); lev = e
    else: lev = e + P.Rmax(e); form = P.theta_na(lev)
    mm = maxmin_polish(P, kind, lev, g)
    dev = max(dev, abs(mm - form))
    print(f"p={p} u={u} e={frac}E {kind:5s} g={g:+.1f}: formula {form:.9f}  direct max-min (SLSQP-polished) {mm:.9f}  diff {mm-form:+.2e}")
print(f"largest |difference| = {dev:.2e}   [{time.time()-t0:.1f}s]")
