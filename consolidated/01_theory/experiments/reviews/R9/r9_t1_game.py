# R9 test 1: the game function F(gamma,t): LP solver vs closed form vs cosh form; F(g,1)=0; F<=0 for t>=1;
# sign of dF/dgamma(0,t); v closed form vs max over gamma; E; a.
import numpy as np, time, sys
from math import log, exp
from r9lib import Par, h, kl
rng = np.random.default_rng(20261125)
t0 = time.time()
d1 = d2 = d3 = 0.0
nb = 0
for trial in range(4000):
    p = rng.uniform(0.02, 0.98); u = rng.uniform(0.1, 6.0)
    P = Par(p, u)
    g = rng.uniform(-u, u); t = rng.uniform(0.01, 3.0)
    if trial % 10 == 0: g = rng.choice([-u, u])          # endpoints of the gamma-interval
    f_closed = float(P.F(g, t)); f_cosh = float(P.F_cosh(g, t)); f_lp = P.F_game(g, t)
    d1 = max(d1, abs(f_closed - f_lp)); d2 = max(d2, abs(f_closed - f_cosh))
    d3 = max(d3, abs(float(P.F(g, 1.0))))
    if t >= 1 and f_lp > 1e-9: nb += 1
print(f"4000 random (p,u,gamma,t): max|closed - LP game| = {d1:.2e}; max|closed - cosh| = {d2:.2e}; max|F(g,1)| = {d3:.2e}; cases t>=1 with F>1e-9: {nb}")
# F(g,t) <= 0 for t >= 1 on a grid
worst = -1e9
for (p, u) in [(0.1, 2.0), (0.3, 1.0), (0.5, 1.0), (0.05, 4.0), (0.8, 3.0)]:
    P = Par(p, u)
    gs = np.linspace(-u, u, 401)[None, :]; ts = np.linspace(1.0, 12.0, 1101)[:, None]
    worst = max(worst, float(np.max(P.F(gs, ts))))
print(f"max F(g,t) over t in [1,12], 5 parameter pairs: {worst:.3e}  (claim: <= 0)")
# sign of dF/dgamma(0,t) and the formula t g(t)/[(1-e^{-tu})(A0^t+A1^t)]
bad = 0; dmax = 0.0
for trial in range(3000):
    p = rng.uniform(0.02, 0.98); u = rng.uniform(0.1, 6.0); t = rng.uniform(0.02, 0.98)
    P = Par(p, u); eps = 1e-5
    fd = (float(P.F(eps, t)) - float(P.F(-eps, t))) / (2 * eps)
    A0 = P.q + P.p * exp(-u); A1 = P.p + P.q * exp(-u)
    gt = A0 ** t * (P.p + P.q * exp(-t * u)) - A1 ** t * (P.q + P.p * exp(-t * u))
    form = t * gt / ((1 - exp(-t * u)) * (A0 ** t + A1 ** t))
    dmax = max(dmax, abs(fd - form))
    if abs(p - 0.5) > 1e-3 and np.sign(form) != np.sign(p - 0.5): bad += 1
print(f"dF/dgamma(0,t): max|finite difference - formula| = {dmax:.2e}; sign != sign(p-1/2) in {bad} of 3000")
# v closed form against max over gamma
dv = 0.0
for trial in range(300):
    p = rng.uniform(0.02, 0.98); u = rng.uniform(0.1, 6.0); P = Par(p, u); k = rng.uniform(0, 1)
    dv = max(dv, abs(float(P.v(k)) - P.v_bymax(k)))
print(f"v(kappa): max|closed form - max over gamma grid| = {dv:.2e}")
# thresholds and a
for (p, u) in [(0.1, 2.0), (0.3, 1.0), (0.5, 1.0), (0.05, 2.0), (0.2, 4.0), (0.5, 2.0)]:
    P = Par(p, u)
    E, gE, E0 = P.E()
    ts, Fs, Gs = P.table()
    supFt = np.max(Fs[1:] / ts[1:])
    a1 = -P.ec(); a2, m2 = P.a_cone()
    F0 = P.F(0.0, ts)
    gap = np.min((Fs - F0)[5:-5])
    print(f"p={p} u={u}: E={E:.6f} (gamma={gE:+.4f}), E0={E0:.6f}, sup_t F*(t)/t on grid={supFt:.6f}; a=-e_c={a1:.6f}, max_m I(z_c(m))={a2:.6f} (m={m2:.4f}); min_t [F*-F(0,.)] on (0,1) = {gap:.2e}; h=R^max(0)={P.Rmax(0.0):.6f}, R0(0)={P.R0(0.0):.6f}")
print(f"[{time.time()-t0:.1f}s]")
