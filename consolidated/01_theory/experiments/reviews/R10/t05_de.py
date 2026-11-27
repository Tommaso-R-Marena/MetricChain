"""differential evolution over k-block profiles (no symmetry imposed), then Nelder-Mead polish,
then re-evaluation of the optimum with S1(fine), S2 (dual, I) and S3 (primal, I).
usage: python3 t05_de.py bJ bB u e k seed popmult maxiter"""
import time, sys
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *
bJ, bB, u, e = (float(x) for x in sys.argv[1:5])
k, seed, popmult, maxiter = (int(x) for x in sys.argv[5:9])
t0 = time.time()
M = Model(bJ=bJ, bB=bB, u=u)
neval = [0]

def P(z):
    w = np.concatenate(([0.0], z[:k - 1])); w = w - w.max(); lam = np.exp(w); lam /= lam.sum()
    return lam, np.asarray(z[k - 1:])

def f(z):
    neval[0] += 1
    lam, mu = P(z)
    val = r_mu(M, lam, mu, e)
    return -val if np.isfinite(val) else 0.0

bounds = [(-4.0, 4.0)] * (k - 1) + [(0.002, 0.998)] * k
best_hist = []
def cb(xk, convergence):
    best_hist.append(-f(xk))
    if len(best_hist) % 10 == 0:
        print(f"  gen {len(best_hist)} best {best_hist[-1]:.9f} evals {neval[0]} t={time.time()-t0:.0f}", flush=True)
    return (time.time() - t0) > 440

res = optimize.differential_evolution(f, bounds, seed=seed, popsize=popmult, maxiter=maxiter, tol=1e-12, atol=1e-13,
                                      mutation=(0.5, 1.0), recombination=0.7, polish=False, callback=cb, init='sobol')
lam, mu = P(res.x)
print(f"# bJ={bJ} bB={bB} u={u} e={e} k={k} seed={seed}: DE {-res.fun:.9f} [{fmt(lam, mu)}] evals {neval[0]} t={time.time()-t0:.0f}", flush=True)
v, l2, m2 = nm(M, e, lam, mu, maxiter=3000)
print(f"# polished {v:.9f} [{fmt(l2, m2)}] mean {float(l2@m2):.5f} t={time.time()-t0:.0f}", flush=True)
fine = dict(G=400, zooms=5, ncand=6, nz=41, rounds=8)
B = e + alpha(M, l2, m2)
s1 = inner_clip(M, l2, m2, B, **fine)[0]
s2, k2, loc = inner_dual(M, l2, m2, B, nk=1201, refine=5)
s3 = inner_primal(M, l2, m2, B, nstart=40)[0]
print(f"# re-evaluation: S1fine {s1:.9f}  S2(dual, I) {s2:.9f}  S3(primal, I) {s3:.9f}  exits {[(round(a,4), round(b,8)) for a,b in loc[:4]]}  time {time.time()-t0:.0f}", flush=True)
