"""t08: as t07 but faster (five centre types around the predicted optimum, bracketed bisection), for larger n.
usage: python3 t08_finite_large.py p u frac n1,n2,n3"""
import math, sys, time, numpy as np
from flib import *
from finite import *

def extrap(ns, vals):
    M = np.array([[1.0, math.log(n) / n, 1.0 / n] for n in ns])
    return float(np.linalg.solve(M, np.array(vals))[0])

def best5(n, p, u, eps, kind, mstar, guess, logw0_t=None):
    if kind == "dip":
        fn = lambda C, ins: dip_effect(C, logw0_t, ins, u)
    else:
        fn = lambda C, ins: flatten_drop(C, ins, u)
    best = (-1.0, None)
    for dm in (-0.06, -0.03, 0.0, 0.03, 0.06):
        k = int(round(min(max(mstar + dm, 0.02), 0.98) * n))
        C = Centre(n, k, p)
        lo, hi = -n * (guess + 0.04), -n * max(guess - 0.004, 0.0)
        ins, mx = C.density_ball(hi)
        if not (ins.any() and (~ins).any() and fn(C, ins) > eps):
            hi = -1e-9
        ins, mx = C.density_ball(lo)
        if ins.any() and (~ins).any() and fn(C, ins) > eps:
            lo = -n * math.log(2) - 5
        while hi - lo > 0.01:
            mid = (lo + hi) / 2
            ins, mx = C.density_ball(mid)
            if ins.any() and (~ins).any() and fn(C, ins) > eps:
                hi = mid
            else:
                lo = mid
        ins, mx = C.density_ball(hi)
        if -mx / n > best[0]:
            best = (-mx / n, k)
    return best

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
    a, ka = best5(n, p, u, e1 * n, "dip", m0, r0, logw0_t=np.zeros(n + 1))
    b, kb = best5(n, p, u, e1 * n, "dip", aH[1], rmax, logw0_t=-gstar * tt)
    c, kc = best5(n, p, u, e1 * n, "dip", aH[1], rmax, logw0_t=logw_H(n, p, u, tt))
    d, kd = best5(n, p, u, e1 * n, "flatten", ana[1], ana[0])
    for key, v in zip(("g0", "add", "H", "na"), (a, b, c, d)):
        res[key].append(v)
    print(f"  n={n}: g=0: {a:.6f} (m={ka/n:.3f})  additive gamma*: {b:.6f} (m={kb/n:.3f})  H: {c:.6f} (m={kc/n:.3f})  cone flattened: {d:.6f} (m={kd/n:.3f})   [{time.time()-t0:.0f}s]", flush=True)
if len(ns) >= 3:
    print("  extrapolated a of a + b ln(n)/n + c/n (last three sizes): g=0: %.6f   additive: %.6f   H: %.6f   non-adaptive: %.6f" % tuple(extrap(ns[-3:], res[k][-3:]) for k in ("g0", "add", "H", "na")))
    print("  formulas:                                                 g=0: %.6f   additive: %.6f   H: %.6f   non-adaptive: %.6f" % (r0, rmax, rmax, ana[0]))
