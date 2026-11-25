"""t07: exact finite-n exponents on a biased cube against the single-letter formulas.
For each n: the smallest density ball (largest type density q) whose dip changes ln A by more than eps = eps1 n
 - at the zero residual g = 0                         -> R_0(eps1)
 - at the hardest additive instance gamma*            -> max_gamma R_gamma(eps1)
 - at the flat-histogram instance H                   -> the same value
and the smallest density ball on which flattening a cone lowers ln A by more than eps -> theta_na(eps1).
Reported: n^{-1} ln(1/q), and the extrapolation a of the fit a + b ln(n)/n + c/n through three sizes."""
import math, sys, time, numpy as np
from flib import *
from finite import *

def extrap(ns, vals):
    M = np.array([[1.0, math.log(n) / n, 1.0 / n] for n in ns])
    return float(np.linalg.solve(M, np.array(vals))[0])

p, u, frac = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
ns = [int(x) for x in sys.argv[4].split(",")]
st = Site(p, u)
E = max(thr_additive(p, u, g) for g in np.linspace(-u, u, 401))
e1 = frac * E
r0, _ = R_additive(p, u, 0.0, e1)
rmax, gstar = R_max(p, u, e1, ngam=41, nt=401)
m0 = hint0_rd(st, e1, nm=200001)[1]
aH = maxmin_precise(st, "H", e1)
ana = maxmin_precise(st, "na", e1)
print(f"p={p} u={u} eps1={e1:.6f} (= {frac} x class threshold {E:.6f})")
print(f"  formulas: R_0={r0:.6f} (m*={m0:.3f})  max_gamma R_gamma={rmax:.6f} (gamma*={gstar:+.4f}, m*={aH[1]:.3f})  theta_na={ana[0]:.6f} (m*={ana[1]:.3f})")
res = {key: [] for key in ("g0", "add", "H", "na")}
t0 = time.time()
for n in ns:
    tt = np.arange(n + 1)
    def kg(mstar):
        return sorted(set(int(round(x * n)) for x in np.clip(np.linspace(mstar - 0.12, mstar + 0.12, 7), 0.02, 0.98)))
    a, ka = best_over_centres(n, p, u, e1 * n, "dip", logw0_t=np.zeros(n + 1), kgrid=kg(m0))
    b, kb = best_over_centres(n, p, u, e1 * n, "dip", logw0_t=-gstar * tt, kgrid=kg(aH[1]))
    c, kc = best_over_centres(n, p, u, e1 * n, "dip", logw0_t=logw_H(n, p, u, tt), kgrid=kg(aH[1]))
    d, kd = best_over_centres(n, p, u, e1 * n, "flatten", kgrid=kg(ana[1]))
    for key, v in zip(("g0", "add", "H", "na"), (a, b, c, d)):
        res[key].append(v)
    print(f"  n={n}: g=0: {a:.6f} (m={ka/n:.3f})  additive gamma*: {b:.6f} (m={kb/n:.3f})  H: {c:.6f} (m={kc/n:.3f})  cone flattened: {d:.6f} (m={kd/n:.3f})   [{time.time()-t0:.0f}s]", flush=True)
if len(ns) >= 3:
    print("  extrapolated (last three sizes): g=0: %.6f   additive: %.6f   H: %.6f   non-adaptive: %.6f" % tuple(extrap(ns[-3:], res[k][-3:]) for k in ("g0", "add", "H", "na")))
    print("  formulas:                        g=0: %.6f   additive: %.6f   H: %.6f   non-adaptive: %.6f" % (r0, rmax, rmax, ana[0]))
