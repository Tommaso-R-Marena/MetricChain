# R9 test 3c: the small positive values (<= 1.6e-6) of "V - R^max" in test 3b are artefacts of the inner minimiser
# (V is computed from above).  Here V is recomputed with a multi-start SLSQP + a finer grid on a neighbourhood of the
# generalised dip for the case with the largest reported value (p = 0.3, u = 1, e = 0).
import numpy as np, sys, time
from math import log, exp
from scipy.optimize import minimize
from r9lib import Par, h, kl
rng = np.random.default_rng(1); t0 = time.time()
P = Par(0.3, 1.0); e = 0.0; Re = P.Rmax(e)
def V(Pu, mu, B, nstart=12):
    best = float(h(np.dot(Pu, mu)) - np.dot(Pu, h(mu)))
    cl = lambda x: np.clip(mu + x[:2] - x[2:], 1e-13, 1 - 1e-13)
    fI = lambda x: float(h(np.dot(Pu, cl(x))) - np.dot(Pu, h(cl(x))))
    fc = lambda x: B - (P.u * float(np.dot(Pu, x[:2] + x[2:])) + float(P.v(np.dot(Pu, cl(x)))))
    bnds = [(0, 1 - m) for m in mu] + [(0, m) for m in mu]
    mub = float(np.dot(Pu, mu))
    starts = [np.zeros(4)]
    for c in (mub, P.kminus, P.kplus, P.p, 0.5):
        for s in np.linspace(0.05, 0.95, 7):
            tgt = mu + s * (c - mu); starts.append(np.concatenate([np.maximum(tgt - mu, 0), np.maximum(mu - tgt, 0)]))
    for x0 in starts:
        r = minimize(fI, x0, method='SLSQP', bounds=bnds, constraints=[{'type': 'ineq', 'fun': fc}], options={'ftol': 1e-16, 'maxiter': 1000})
        if fc(r.x) >= -1e-12 and np.isfinite(r.fun): best = min(best, float(r.fun))
    return best
worst = -np.inf
mstar = 0.5006
for trial in range(400):
    w = mstar + rng.normal(0, 0.01); mu = np.array([P.eta0, 1 - P.eta1]) + rng.normal(0, 0.003, 2)
    if trial == 0: w = mstar; mu = np.array([P.eta0, 1 - P.eta1])
    Pu = np.array([1 - w, w]); al = float(np.dot(Pu, kl(mu, P.p))); B = al + e
    if B < float(P.v(np.dot(Pu, mu))): continue
    worst = max(worst, V(Pu, mu, B) - Re)
print(f"p=0.3 u=1 e=0: 400 laws in a neighbourhood of the generalised dip, V by 36-start SLSQP: max(V - R^max) = {worst:+.2e}   [{time.time()-t0:.0f}s]")
