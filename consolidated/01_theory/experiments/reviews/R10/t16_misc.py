"""miscellaneous checks at bJ = 1.5, B = 0 (own code): the numbers of the example, u_top,
self-consistency of the barrier shells and uniqueness of the Gibbs shell (for a = a_unif),
theta_shell at small accuracies, a from cones."""
import time
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *
from r10tab import *
t0 = time.time()
M = Model(1.5, 0.0, 1.0)
kk = np.linspace(0.02, 0.98, 960001)
dI = np.gradient(M.I(kk), kk)
print(f"wells at {M.kmin:.5f} and {1-M.kmin:.5f}; barrier I(1/2) = {float(M.I(0.5)):.6f}; largest slope of I on the barrier flank: {np.max(np.abs(dI[(kk > M.kmin) & (kk < 0.5)])):.5f}; contact set (u=1): {[(round(a,4), round(b,4)) for a,b in M.contact()]}")
# u_top: largest slope of a chord from the top of the barrier
ks = np.linspace(0.001, 0.4999, 500000)
ch = (float(M.I(0.5)) - M.I(ks)) / (0.5 - ks)
j = int(np.argmax(ch))
print(f"u_top = max chord slope from the top = {ch[j]:.5f} at kappa = {ks[j]:.4f} (report 0.28153 at 0.1183); mean slope to the bottom of the well: {float(M.I(0.5)) / (0.5 - M.kmin):.5f} (report 0.26834)")
for u in (0.2815, 0.2816, 0.30):
    Mu = Model(1.5, 0.0, u, N=200001)
    print(f"   u={u}: (I - v)(1/2) = {float(M.I(0.5)) - float(Mu.v(0.5)):.3e}; contact pieces {[(round(a,4), round(b,4)) for a,b in Mu.contact()]}")
# self-consistency of the shells (1/2; x, x): min over nu of G_mu(nu) = MI + I + u dist against alpha(mu)
u = 1.0
pu = p_u(u)
g = np.linspace(0.0005, 0.9995, 2000)
N1, N0 = np.meshgrid(g, g, indexing='ij')
nb = 0.5 * N1 + 0.5 * N0
base = h(nb) - 0.5 * h(N1) - 0.5 * h(N0) + M.I(nb)
print("shell x | alpha(mu) | min_nu G_mu(nu) on a 2000^2 grid (polished) | self-consistent? | second-best local minimum of G - alpha away from mu")
for x in (0.24, 0.26, pu, 0.28, 0.298, 0.35):
    lam, mu = binary(0.5, x, x)
    G = base + u * (0.5 * np.abs(N1 - mu[0]) + 0.5 * np.abs(N0 - mu[1]))
    al = alpha(M, lam, mu)
    i1, i0 = np.unravel_index(int(np.argmin(G)), G.shape)
    f = lambda nu: MI(lam, np.clip(nu, 1e-12, 1 - 1e-12)) + float(M.I(np.clip(lam @ nu, 0, 1))) + u * float(lam @ np.abs(nu - mu))
    res = optimize.minimize(f, [g[i1], g[i0]], method='Nelder-Mead', options={'xatol': 1e-12, 'fatol': 1e-16})
    far = (np.abs(N1 - mu[0]) + np.abs(N0 - mu[1])) > 0.05
    print(f"   x={x:.5f}  alpha={al:.9f}  min G={min(res.fun, al):.9f} at nu=({res.x[0]:.4f},{res.x[1]:.4f})  {abs(min(res.fun, al) - al) < 1e-10}   min of G - alpha at distance > 0.05 from mu: {float(np.min(G[far])) - al:+.5f}")
# theta_shell(X; mu) for the shell x = p_u as X -> 0  (the vanishing-accuracy exponent of the shell-cone)
lam, mu = binary(0.5, pu, pu)
al = alpha(M, lam, mu)
G = base + u * (0.5 * np.abs(N1 - mu[0]) + 0.5 * np.abs(N0 - mu[1]))
mi = h(nb) - 0.5 * h(N1) - 0.5 * h(N0)
for X in (1e-2, 1e-3, 1e-4, 3e-5):
    feas = (G - al) <= X
    print(f"   theta_shell(X={X:g}; x = p_u) = {float(np.min(mi[feas])):.6f}  (grid; tends to MI(mu) = KL(p_u||1/2) = {float(kl(pu, 0.5)):.6f})")
a, ma = a_cone(M)
print(f"a from cones around points: {a:.6f} at centre type m = {ma:.4f} (report 0.0446);  Gibbs shell of the cone m=1/2: nu = {cone_shell(M, 0.5)[1]}")
Rc, mc = R_cone(M, 0.0)
zero = lambda k: 0.0 * np.asarray(k, float)
R0, l0, m0 = R_binary(M, 0.0, land=zero, starts=[(0.5, 0.3, 0.3), (0.3, 0.2, 0.2), (0.2, 0.1, 0.1), (0.15, 0.6, 0.03), (0.8, 0.05, 0.5), (0.1, 0.5, 0.05)])
print(f"cone formula R_cone(0) = {Rc:.7f} at m = {mc:.4f} (report 0.0107007);  zero residual R_0(0) = {R0:.7f} [{fmt(l0, m0)}] (report 0.0087471)")
print("time", time.time() - t0)
