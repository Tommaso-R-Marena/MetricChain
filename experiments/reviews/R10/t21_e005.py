"""bJ = 1.5, B = 0, u = 1, accuracy e (default 0.05): symmetric profile laws with a central atom,
   {x_1 < ... < x_p < 1/2} with weights w_i (each twice) and an atom at 1/2 with weight w_0,
for p = 2 (the report's S5: 0.0063867 at e = 0.05), p = 3, p = 4; Nelder-Mead with the clipping solver S1,
then re-evaluation of each optimum with S1(fine), S2 (dual per exit type, I) and S3 (primal SLSQP, I).
usage: python3 t21_e005.py [e]"""
import time, sys
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *
t0 = time.time()
e = float(sys.argv[1]) if len(sys.argv) > 1 else 0.05
M = Model(1.5, 0.0, 1.0)
fine = dict(G=400, zooms=5, ncand=6, nz=41, rounds=8)

def build(z, p):
    """z = (x_1..x_p, a_0, a_2..a_p): weights from softmax-like positive numbers; w_1 normalises"""
    x = np.clip(np.array(z[:p]), 1e-4, 0.4999)
    raw = np.abs(np.array(z[p:]))                     # w_0, w_2, ..., w_p   (half weights for i >= 2)
    w0 = raw[0]
    wi = raw[1:]
    w1 = (1.0 - w0 - 2 * wi.sum()) / 2.0
    if w1 <= 0:
        return None
    w = np.concatenate(([w1], wi))
    lam = np.concatenate((w, [w0], w[::-1]))
    mu = np.concatenate((x, [0.5], 1 - x[::-1]))
    return lam, mu

def obj(z, p):
    pr = build(z, p)
    if pr is None:
        return 1.0
    v = r_mu(M, pr[0], pr[1], e)
    return -v if np.isfinite(v) else 1.0

starts = {2: [0.270, 0.388, 0.085, 0.085],
          3: [0.2695, 0.3863, 0.4537, 0.081, 0.078, 0.0078],
          4: [0.2695, 0.37, 0.41, 0.4537, 0.081, 0.04, 0.04, 0.0078]}
results = {}
prev = None
for p in (2, 3, 4):
    best = None
    cands = [starts[p]]
    if prev is not None:                                   # also start from the previous optimum with a split atom
        zp = list(prev)
        xs, ws = zp[:p - 1], zp[p - 1:]
        cands.append(xs + [min(xs[-1] + 0.04, 0.48)] + ws + [0.004])
    for z0 in cands:
        z0 = np.array(z0, float)
        sim = np.vstack([z0] + [z0 + (0.01 if i < p else 0.004) * np.eye(len(z0))[i] for i in range(len(z0))])
        res = optimize.minimize(obj, z0, args=(p,), method='Nelder-Mead',
                                options={'xatol': 1e-8, 'fatol': 1e-13, 'maxiter': 2500 * p, 'maxfev': 2500 * p, 'initial_simplex': sim})
        if best is None or res.fun < best.fun:
            best = res
    prev = list(best.x)
    lam, mu = build(best.x, p)
    B = e + alpha(M, lam, mu)
    s1 = inner_clip(M, lam, mu, B, **fine)[0]
    s2, k2, loc = inner_dual(M, lam, mu, B, nk=801, refine=4)
    s3 = inner_primal(M, lam, mu, B, nstart=24)[0]
    results[p] = (s1, s2, s3)
    print(f"e={e}: {2*p+1} atoms: search {-best.fun:.9f};  S1fine {s1:.9f}  S2(dual, I) {s2:.9f}  S3(primal, I) {s3:.9f}", flush=True)
    print("     atoms  " + "  ".join(f"{m:.6f}" for m in mu))
    print("     weights " + "  ".join(f"{l:.6f}" for l in lam))
    print(f"     exits (type, value): {[(round(a,4), round(b,8)) for a,b in loc[:6]]}   t={time.time()-t0:.0f}", flush=True)
print(f"R_unif(e) = {R_unif(e, 1.0):.9f}")
print("time", time.time() - t0)
