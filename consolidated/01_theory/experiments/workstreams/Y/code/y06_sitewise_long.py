"""Step 3(b) -- site-wise labels on chains of n = 6, 8, 10, 12 sites (the whole chain as one super-site, 2^n labels x 2^n
configurations, exact): the optimal label law (Arimoto, duality bracket WITHIN the site-wise family) against the best Z^t-tilted
Markov law, at t = t*(p) of the Lyapunov scan; increments (F_n - F_{n-2})/2 as estimates of the limit.
usage: python3 y06_sitewise_long.py p t [nmax]"""
import sys, time, math, itertools
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import *
from ylyap import *

t0 = time.time(); u = 1.0
p = float(sys.argv[1]); t = float(sys.argv[2]); nmax = int(sys.argv[3]) if len(sys.argv) > 3 else 12
Kp = 0.5 * math.log((1 - p) / p); h = u / 2
cube = t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2))
print("p = %.2f, t = %.3f; cube value per site %.6f; Lyapunov limit of the tilted Markov family: max_c G_inf = %.6f" % (
    p, t, cube, max(G_inf(t, c, p, u) for c in np.linspace(0, 2, 81))))
prev = None
for n in range(6, nmax + 1, 2):
    S = np.array(list(itertools.product((1.0, -1.0), repeat=n)))
    e_pi = Kp * (S[:, :-1] * S[:, 1:]).sum(axis=1)
    W = e_pi[None, :] + h * (S @ S.T)                                # log weights: rows labels sigma, columns s
    W -= W.max(axis=1, keepdims=True); P = np.exp(W); P /= P.sum(axis=1, keepdims=True)
    lo, up, M, Q = renyi_F(P, t, tol=1e-8, itmax=6000 if n >= 12 else 20000)
    gm = max((G_finite(t, c, p, u, n), c) for c in np.linspace(0, 2, 41))
    # label statistics under the optimal law: P(sigma_i sigma_{i+1} = -1) in the middle of the chain; number of labels with weight
    mid = n // 2 - 1
    flip = float(M[(S[:, mid] * S[:, mid + 1]) < 0].sum())
    # is the centre Markov?  I(x_{mid-1}; x_{mid+1} | x_mid)
    def cmi(Qv, i):
        tot = 0.0
        for b in (1, -1):
            idx = S[:, i] == b; pb = Qv[idx].sum(); J = np.zeros((2, 2))
            for a in (0, 1):
                for c in (0, 1):
                    J[a, c] = Qv[idx & (S[:, i - 1] == 1 - 2 * a) & (S[:, i + 1] == 1 - 2 * c)].sum() / pb
            tot += pb * float((J * np.log(J / np.outer(J.sum(axis=1), J.sum(axis=0)))).sum())
        return tot
    inc = "" if prev is None else "  increment (F_n - F_{n-2})/2 = %.6f" % ((lo - prev) / 2)
    print("n=%2d: optimal site-wise law F = [%.7f, %.7f] (per site %.6f)%s | best tilted Markov %.7f at c=%.2f (per site %.6f) | support(>1e-6) %d labels, P(label flip at the middle bond) = %.4f | centre: I(x_{m-1};x_{m+1}|x_m) = %.2e | %.0f s" % (
        n, lo, up, lo / n, inc, gm[0], gm[1], gm[0] / n, int((M > 1e-6).sum()), flip, cmi(Q, mid), time.time() - t0))
    prev = lo
    del P, W
