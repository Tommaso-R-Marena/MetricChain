# R9 test 3b: Lemma SL, adversarial search over laws P_UX with |U| = 2 by Nelder-Mead (objective V - R^max(B - alpha),
# V by a 2-D grid + zoom + SLSQP polish; e = B - alpha fixed, both signs).  The lemma says the objective is <= 0;
# by test 3(c) the value 0 is attained at the generalised dip.  Also: F(g,t)/t -> chord gap of ln C as t -> 0.
import numpy as np, sys, time
from math import log, exp
from scipy.optimize import minimize
from r9lib import Par, h, kl
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 41); t0 = time.time()
def V2(P, Pu, mu, B):
    best = float(h(np.dot(Pu, mu)) - np.dot(Pu, h(mu)))
    lo = np.zeros(2); hi = np.ones(2); N = 241; c0 = np.array(mu, dtype=float)
    for z in range(6):
        a = np.linspace(lo[0], hi[0], N)[:, None]; b = np.linspace(lo[1], hi[1], N)[None, :]
        nb = Pu[0] * a + Pu[1] * b
        I = h(nb) - Pu[0] * h(a) - Pu[1] * h(b)
        g = P.u * (Pu[0] * np.abs(a - mu[0]) + Pu[1] * np.abs(b - mu[1])) + P.v(nb) - B
        I = np.where(g <= 0, I, np.inf); k = int(np.argmin(I)); i, j = divmod(k, N)
        if not np.isfinite(I[i, j]): break
        best = min(best, float(I[i, j])); w = (hi - lo) / (N - 1) * 4; c0 = np.array([a[i, 0], b[0, j]])
        lo = np.clip(c0 - w, 0, 1); hi = np.clip(c0 + w, 0, 1)
    # polish in split variables
    fI = lambda x: float(h(np.dot(Pu, np.clip(mu + x[:2] - x[2:], 1e-13, 1 - 1e-13))) - np.dot(Pu, h(np.clip(mu + x[:2] - x[2:], 1e-13, 1 - 1e-13))))
    fc = lambda x: B - (P.u * float(np.dot(Pu, x[:2] + x[2:])) + float(P.v(np.dot(Pu, np.clip(mu + x[:2] - x[2:], 1e-13, 1 - 1e-13)))))
    x0 = np.concatenate([np.maximum(c0 - mu, 0), np.maximum(mu - c0, 0)])
    try:
        r = minimize(fI, x0, method='SLSQP', bounds=[(0, 1 - m) for m in mu] + [(0, m) for m in mu], constraints=[{'type': 'ineq', 'fun': fc}], options={'ftol': 1e-15, 'maxiter': 300})
        if fc(r.x) >= -1e-11 and np.isfinite(r.fun): best = min(best, float(r.fun))
    except Exception: pass
    return best
for (p, u) in [(0.1, 2.0), (0.3, 1.0), (0.2, 4.0)]:
    P = Par(p, u); E = P.E()[0]; a = -P.ec()
    for e in (-0.5 * a, -0.15 * a, 0.0, 0.3 * E, 0.7 * E):
        Re = P.Rmax(e)
        def obj(x):
            w = 1 / (1 + exp(-x[0])); mu = 1 / (1 + np.exp(-np.array(x[1:3])))
            Pu = np.array([1 - w, w]); al = float(np.dot(Pu, kl(mu, P.p))); B = al + e
            if B < float(P.v(np.dot(Pu, mu))) - 1e-12: return 1.0 + (float(P.v(np.dot(Pu, mu))) - B)     # infeasible for the lemma: penalty
            return -(V2(P, Pu, mu, B) - Re)
        best = -np.inf; arg = None
        starts = [np.array([0.0, log(P.eta0 / (1 - P.eta0)), log((1 - P.eta1) / P.eta1)])] + [rng.normal(0, 1.5, 3) for _ in range(5)]
        for x0 in starts:
            r = minimize(obj, x0, method='Nelder-Mead', options={'xatol': 1e-6, 'fatol': 1e-12, 'maxiter': 500})
            if -r.fun > best and r.fun < 0.99: best = -r.fun; arg = r.x
        w = 1 / (1 + exp(-arg[0])); mu = 1 / (1 + np.exp(-arg[1:3]))
        print(f"p={p} u={u} e={e:+.5f}: sup over |U|=2 laws of V - R^max(e) found = {best:+.3e}  (R^max(e)={Re:.6f}; at P(u2)={w:.4f}, mu=({mu[0]:.4f},{mu[1]:.4f}); cone law: ({P.eta0:.4f},{1-P.eta1:.4f}))   [{time.time()-t0:.0f}s]")
        sys.stdout.flush()
# chord gap limit
dd = 0.0
for _ in range(2000):
    p = rng.uniform(0.02, 0.98); u = rng.uniform(0.1, 6); P = Par(p, u); g = rng.uniform(-u, u); t = 1e-6
    th = P.theta; lnC = lambda x: np.log(2 * np.cosh(x / 2))
    G = ((u - g) * lnC(th - u) + (u + g) * lnC(th + u)) / (2 * u) - lnC(th + g)
    dd = max(dd, abs(float(P.F(g, t)) / t - G))
print(f"max |F(g,t)/t - chord gap of ln C| at t = 1e-6 over 2000 random (p,u,g): {dd:.1e}")
