"""R11 / 04c -- lower ends of a from Proposition I at t close to 1:  a_inf >= F_inf(t)/(1-t) >= bound(t)/(1-t).
Report (section 6.4, y07): p = 0.3: 0.126444 (t = 0.99, <= 2 walls, L = 8);  p = 0.2: 0.129797 (L = 10);
p = 0.1: 0.116632 (L = 10);  p = 0.4: 0.116547 (L = 6; the table uses the Prop. H value 0.116817).
M_L = my optimum of G_L on the label set (any M_L is valid).

Run:  python3 r11_04c_a_lower.py      (about 1 minute)
"""
import time
import numpy as np
from r11lib import *

T0 = time.time()
u = 1.0
h = u / 2


def walls_labels(L, maxwalls):
    sig = configs(L)
    nw = ((sig[:, :-1] * sig[:, 1:]) == -1).sum(axis=1)
    return sig[nw <= maxwalls]


def end_matrix(s, w):
    B = np.zeros((2, 2))
    np.add.at(B, ((s[:, 0] == -1).astype(int), (s[:, -1] == -1).astype(int)), w)
    return B


def bound(p, L, t, maxwalls, N=96):
    labels = walls_labels(L, maxwalls)
    s, pi = chain_law(L, p)
    phis = -h * labels.astype(float) @ s.T.astype(float)
    logP = gibbs_logs(np.log(pi), phis)
    lo, up, M = maximise_G_fast(logP, t)
    keep = M > 1e-14
    Mk = M[keep] / M[keep].sum()
    G_L = G_of_M(logP[keep], Mk, t)
    rho0 = 2 * np.array([[1 - p, p], [p, 1 - p]])
    As = [end_matrix(s, np.exp(lp)) @ rho0 for lp in logP[keep]]
    Lam = moment_lyapunov(As, Mk, t, N=N)
    lamQ = float(np.max(np.linalg.eigvals(end_matrix(s, np.exp(centre_of_M(logP[keep], Mk, t))) @ rho0).real))
    return (G_L + Lam - t * np.log(lamQ)) / L, G_L, Lam


ac = cube_constants(u)[2]
for p, L, rep in ((0.4, 6, 0.116547), (0.3, 8, 0.126444), (0.2, 10, 0.129797), (0.1, 10, 0.116632)):
    t = 0.99
    b1, G_L, Lam = bound(p, L, t, 2, N=96)
    b2, _, Lam2 = bound(p, L, t, 2, N=160)
    print(f"p={p} L={L} t={t}: bound/(1-t) = {b1/(1-t):.6f}  (N=96 vs 160: {abs(b1-b2)/(1-t):.1e});  report {rep:.6f};  cube a = {ac:.6f};"
          f"  G_L = {G_L:.9f}, Lambda_blk = {Lam:.9f}   [{time.time()-T0:.0f} s]", flush=True)
