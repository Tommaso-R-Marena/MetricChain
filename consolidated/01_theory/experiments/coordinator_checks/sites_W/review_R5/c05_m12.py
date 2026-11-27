"""m12: a blind maximisation over gamma of game values computed with default solver tolerances is biased upwards.
Reproduce with the harness helper st_game (HiGHS, default tolerances), then re-evaluate with certified bounds."""
import sys, time, math
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import minimize, linprog
import dlib
H = dlib.load_harness()
t0 = time.time()


def certified_upper(site, gamma, t):
    """F(gamma,t) = -ln val, val = max_Q min_phi sum_a Q(a) K(a,phi).  Any Q gives val >= min_phi (Q^T K), i.e. an UPPER bound of F.
    Q from the sampler's LP with tight tolerances, cleaned (clipped, renormalised) and then evaluated exactly."""
    K = (site.P / dlib.gibbs(site.pi, gamma)[None, :]).T ** t          # K[a, phi]
    nr, nc = K.shape
    c = np.zeros(nr + 1); c[-1] = -1.0                                   # maximise s subject to s <= sum_a Q(a) K(a,phi)
    A_ub = np.hstack([-K.T, np.ones((nc, 1))]); A_eq = np.zeros((1, nr + 1)); A_eq[0, :nr] = 1
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(nc), A_eq=A_eq, b_eq=[1.0], bounds=[(0, None)] * nr + [(None, None)], method="highs",
                  options={"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10})
    Q = np.clip(res.x[:nr], 0, None); Q /= Q.sum()
    return -math.log(float((Q @ K).min()))


worst_default = worst_cert = -1.0
for name, t in (("path", 0.2), ("path", 0.46), ("asym", 0.2), ("asym", 0.46), ("asym", 0.8), ("tri", 0.46)):
    so = dlib.Site(*dlib.SITES[name]); hs = H.st_site(*H.ST_SITES[name])
    val, upper, M, Q = dlib.renyi(so, t)
    gstar = -np.log(Q / so.pi)
    q = so.q

    def neg(z):
        g = np.concatenate([[0.0], z])
        if any(g[a] - g[b] > so.d[a, b] + 1e-12 for a in range(q) for b in range(q)): return 1.0
        return -H.st_game(hs, g, t)
    blind = -1.0; garg = None
    rng = np.random.default_rng(3)
    for s in range(6):
        z0 = (gstar - gstar[0])[1:] * (0.0 if s == 0 else 1.0) + (0 if s < 2 else rng.normal(0, 0.05, q - 1))
        res = minimize(neg, z0, method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-14, "maxiter": 3000})
        if -res.fun > blind: blind, garg = -res.fun, np.concatenate([[0.0], res.x])
    cert = certified_upper(so, garg, t)
    worst_default = max(worst_default, blind - upper); worst_cert = max(worst_cert, cert - upper)
    print("%-5s t = %.2f: Renyi value %.12f, dual bound %.12f | blind search with default tolerances %.12f (excess over the dual bound %+.2e)"
          " | certified upper bound of F at the point found %.12f (excess %+.2e)" % (name, t, val, upper, blind, blind - upper, cert, cert - upper))
print("largest excess of the blind search over the certified dual bound: default tolerances %+.2e; re-evaluated with a certified bound %+.2e" % (worst_default, worst_cert))
print("time %.1f s" % (time.time() - t0))
