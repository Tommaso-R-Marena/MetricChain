"""t20: which sampling distribution?  Non-adaptive exponent when the sample is drawn from ONE product measure
Bernoulli(r)^n (r = p: plain Monte Carlo from pi_f; other r: a tilted product measure), with importance weights:
    theta_na^{(r)}(x) = max_m min { I(S;X) + KL(P_X || r) : D(P_{X|S} || pi_s | P_S) <= x }
(the cone with centre of type m, truncated on the largest set of Bernoulli(r)^n-measure e^{-n theta}, is not seen),
against the exponent theta_na(x) of the type-uniform (NML) sampler.  The best single product measure is found by a
scan over r."""
import math, numpy as np, time
from scipy.optimize import minimize, minimize_scalar
from flib import *

def inner(site, r, m, x):
    """min { m KL(xh || 1-r) + (1-m) KL(yh || r) : Icone_m(xh, yh) <= x }"""
    obj = lambda z: m * kls(z[0], 1 - r) + (1 - m) * kls(z[1], r)
    con = lambda z: x - (m * kls(z[0], site.eta1) + (1 - m) * kls(z[1], site.eta0))
    if con([1 - r, r]) >= 0:
        return 0.0
    # start: boundary point on the segment from the cone point to the typical point of the sampler
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        z = [site.eta1 + mid * (1 - r - site.eta1), site.eta0 + mid * (r - site.eta0)]
        if con(z) >= 0: lo = mid
        else: hi = mid
    z0 = [site.eta1 + lo * (1 - r - site.eta1), site.eta0 + lo * (r - site.eta0)]
    res = minimize(obj, z0, method="SLSQP", constraints=[{"type": "ineq", "fun": con}], bounds=[(1e-12, 1 - 1e-12)] * 2,
                   options=dict(ftol=1e-15, maxiter=500))
    best = obj(z0)
    if con(res.x) >= -1e-10:
        best = min(best, obj(res.x))
    return best

def theta_prod(site, r, x):
    ms = np.linspace(0.005, 0.995, 100)
    vals = [inner(site, r, m, x) for m in ms]
    i = int(np.argmax(vals))
    res = minimize_scalar(lambda m: -inner(site, r, m, x), bounds=(ms[max(i - 1, 0)], ms[min(i + 1, 99)]), method="bounded", options=dict(xatol=1e-9))
    return max(vals[i], -res.fun)

t0 = time.time()
for p, u in ((0.1, 2.0), (0.3, 1.0)):
    st = Site(p, u)
    wp = WorstPair(p, u)
    for frac in (0.05, 0.25):
        x = frac * wp.E
        tna = wp.theta_na(x)
        tp = theta_prod(st, p, x)
        rs = np.linspace(max(st.kmin * 0.5, 0.005), min(st.kmax * 1.3, 0.995), 41)
        vals = [theta_prod(st, r, x) for r in rs]
        i = int(np.argmin(vals))
        res = minimize_scalar(lambda r: theta_prod(st, r, x), bounds=(rs[max(i - 1, 0)], rs[min(i + 1, 40)]), method="bounded", options=dict(xatol=1e-6))
        print(f"p={p} u={u} x={x:.5f}: type-uniform sampler theta_na = {tna:.6f};  plain Monte Carlo from pi_f: {tp:.6f};"
              f"  best single product measure Bernoulli(r)^n: {min(vals[i], res.fun):.6f} at r = {res.x:.4f}   [{time.time()-t0:.0f}s]", flush=True)
