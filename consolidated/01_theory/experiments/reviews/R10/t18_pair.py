"""bJ = 1.5, B = 0, u = 1: the pair identity with shells and its failure with cones (own code).
 (a) n_mu*(e + R2(e)) for the optimal binary shell, two ways (through r_mu, Theorem T8(b); and by a
     two-parameter search over clippings);
 (b) the truncated shell-cone directly: theta_shell(S; mu*) on a full grid of exit profiles;
 (c) the truncated cone around a point at the same accuracy: theta_shell(S; centre);
 (d) the same identity at the free-block optimum at e = 0.02."""
import time
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *
from r10tab import *
t0 = time.time()
M = Model(1.5, 0.0, 1.0)
u = 1.0
sh = lambda x: binary(0.5, x, x)
g = np.linspace(0.0, 1.0, 2001)
N1, N0 = np.meshgrid(g, g, indexing='ij')

def theta_shell_grid(lam, mu0, X):
    """min{ MI(nu) : G_mu0(nu) - min G_mu0 <= X } for two blocks, full grid + zoom (I in G)"""
    def fields(A, B):
        nb = lam[0] * A + lam[1] * B
        mi = h(nb) - lam[0] * h(A) - lam[1] * h(B)
        G = mi + M.I(nb) + u * (lam[0] * np.abs(A - mu0[0]) + lam[1] * np.abs(B - mu0[1]))
        return mi, G
    mi, G = fields(N1, N0)
    # minimum of G: polish
    i, j = np.unravel_index(int(np.argmin(G)), G.shape)
    f = lambda z: fields(np.clip(z[0], 1e-12, 1 - 1e-12), np.clip(z[1], 1e-12, 1 - 1e-12))[1]
    res = optimize.minimize(lambda z: float(f(z)), [g[i], g[j]], method='Nelder-Mead', options={'xatol': 1e-13, 'fatol': 1e-16})
    Vmin = min(float(res.fun), float(G.min()))
    best = np.inf
    lo1, hi1, lo0, hi0 = 0.0, 1.0, 0.0, 1.0
    A, B = N1, N0
    for it in range(5):
        mi, G = fields(A, B)
        mf = np.where(G - Vmin <= X, mi, np.inf)
        i, j = np.unravel_index(int(np.argmin(mf)), mf.shape)
        best = min(best, float(mf[i, j]))
        a_, b_ = A[i, j], B[i, j]
        w1, w0 = (hi1 - lo1) / 60, (hi0 - lo0) / 60
        lo1, hi1, lo0, hi0 = max(a_ - w1, 0), min(a_ + w1, 1), max(b_ - w0, 0), min(b_ + w0, 1)
        A, B = np.meshgrid(np.linspace(lo1, hi1, 1201), np.linspace(lo0, hi0, 1201), indexing='ij')
    return best, Vmin, res.x

for e, x in ((0.0, 0.29803), (0.02, 0.30552), (-0.05, 0.28212)):
    lam, mu = sh(x)
    R = r_mu(M, lam, mu, e, G=400, zooms=5, ncand=6, nz=41, rounds=8)
    S = e + R
    n1, emax = n_mu(M, lam, mu, S, ne=400)
    n2 = n_mu_grid(M, lam, mu, S)
    ts, Vmin, arg = theta_shell_grid(lam, mu, S)
    tc, Vc, argc = theta_shell_grid(lam, np.array([1.0, 0.0]), S)
    print(f"e={e:+.3f} shell x={x}: R2 = {R:.8f}, S = {S:.8f};  n_mu(S) = {n1:.8f} (through r_mu; e_max = {emax:+.6f}) = {n2:.8f} (clippings);  truncated shell-cone, direct grid: {ts:.8f} (self-consistent: min G - alpha = {Vmin - alpha(M, lam, mu):+.1e});  truncated cone around the centre: {tc:.8f} (its Gibbs shell nu = ({argc[0]:.4f}, {argc[1]:.4f}), type {0.5*argc[0]+0.5*argc[1]:.4f})   t={time.time()-t0:.0f}", flush=True)
# (d) free-block optimum at e = 0.02
lf, x = 0.14083, 0.27739
lam = np.array([(1 - lf) / 2, lf, (1 - lf) / 2]); mu = np.array([1 - x, 0.5, x])
e = 0.02
R = r_mu(M, lam, mu, e, G=400, zooms=5, ncand=6, nz=41, rounds=8)
n1, emax = n_mu(M, lam, mu, e + R, ne=400)
n2 = n_mu_grid(M, lam, mu, e + R)
print(f"free-block profile lf={lf} x={x} at e={e}: R = {R:.8f}; n_mu(e + R) = {n1:.8f} (through r_mu) = {n2:.8f} (clippings); difference {n1 - R:+.1e}")
print("time", time.time() - t0)
