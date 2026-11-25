"""two small checks (own code):
 (1) equality case of T9(e): bJ = 0.5, B = 0, u = 1 -- the value of mu* = (1/2; p_u, p_u) with fine solvers against R_unif;
 (2) Section 6.6, last column: global self-consistency of the shell (1/2; p_u, p_u) at bJ = 1.2, 1.75, 2.0 (u = 1)."""
import numpy as np
from scipy import optimize
from r10lib import *
u = 1.0
pu = p_u(u)
lam, mu = binary(0.5, pu, pu)
fine = dict(G=400, zooms=5, ncand=6, nz=41, rounds=8)
for bJ in (0.5, 1.0, -2.0):
    M = Model(bJ, 0.0, u)
    for e in (0.0, 0.03, -0.04):
        B = e + alpha(M, lam, mu)
        s1 = inner_clip(M, lam, mu, B, **fine)[0]
        s2 = inner_dual(M, lam, mu, B, nk=1201, refine=5)[0]
        print(f"(1) bJ={bJ} e={e:+.2f}: r_mu* S1 {s1:.10f}  S2 {s2:.10f}  R_unif {R_unif(e,u):.10f}  S1 - R_unif = {s1 - R_unif(e,u):+.1e}")
g = np.linspace(0.0005, 0.9995, 2000)
N1, N0 = np.meshgrid(g, g, indexing='ij')
nb = 0.5 * N1 + 0.5 * N0
for bJ in (1.2, 1.75, 2.0):
    M = Model(bJ, 0.0, u)
    G = h(nb) - 0.5 * h(N1) - 0.5 * h(N0) + M.I(nb) + u * (0.5 * np.abs(N1 - mu[0]) + 0.5 * np.abs(N0 - mu[1]))
    al = alpha(M, lam, mu)
    far = (np.abs(N1 - mu[0]) + np.abs(N0 - mu[1])) > 0.05
    i1, i0 = np.unravel_index(int(np.argmin(G)), G.shape)
    print(f"(2) bJ={bJ}: alpha(mu*) = {al:.9f}; min of G_mu* on the 2000^2 grid = {float(G.min()):.9f} at nu = ({g[i1]:.4f}, {g[i0]:.4f}); min of G - alpha at distance > 0.05: {float(np.min(G[far])) - al:+.5f}  => self-consistent: {float(G.min()) >= al - 1e-6};  contact set {[(round(a,3), round(b,3)) for a,b in M.contact()]}")
