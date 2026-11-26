"""R11 / 03 -- Proposition H (site-wise labels with a tilted Markov law).

(1) the closed formula against a direct computation from the definitions (enumeration of all
    2^n labels and 2^n configurations; n = 6, 8, 10), including the instance gamma*;
(2) the limit n -> infinity (moment Lyapunov exponents by my own operator), maximised over
    (t, c); the i.i.d.-label values (c = 0);
(3) p -> 1/2 reproduces the cube; finite-n values against the limit.

Run:  python3 r11_03_propH.py     (about 1-2 minutes)
"""
import time
import numpy as np
from scipy.optimize import minimize
from r11lib import *

T0 = time.time()
u = 1.0
h = u / 2


def G_formula_finite(n, p, t, c):
    """Proposition H, finite n, by exact enumeration of the 2^(n-1) bond patterns."""
    Kp = 0.5 * np.log((1 - p) / p)
    pc = 1.0 / (1.0 + np.exp(2 * c))
    lnZ0 = lambda x: np.log(2.0) + (n - 1) * np.log(2 * np.cosh(x))
    A = np.log(Xi_exact_moment(pc, Kp, h, t, n))
    B = np.log(Xi_exact_moment(p, c, t * h, 1.0 / t, n))
    return A - t * B - t * lnZ0(Kp) + lnZ0(c)


def G_bruteforce(n, p, t, c, return_all=False):
    """straight from the definitions: labels phi_sigma(s) = -h sigma.s, Gibbs laws pi_sigma,
    M_c(sigma) ~ M_0(sigma) Z(sigma)^t, G_t(M_c) = -t ln sum_s (sum_sigma M_c pi_sigma^t)^(1/t)."""
    s, pi = chain_law(n, p)
    sig = configs(n).astype(float)
    phis = -h * sig @ s.T.astype(float)                 # labels x configs
    logpi = np.log(pi)
    lw = logpi[None, :] - phis
    lnZ = logsumexp(lw, axis=1)                         # ln E_pi e^{-phi_sigma}   (normalised by Z_0(K'))
    logP = lw - lnZ[:, None]
    nfl = ((sig[:, :-1] * sig[:, 1:]) == -1).sum(axis=1)
    lM0 = c * (n - 1 - 2 * nfl)                         # c * sum sigma_i sigma_{i+1}
    lM = lM0 + t * lnZ
    lM -= logsumexp(lM)
    M = np.exp(lM)
    G = G_of_M(logP, M, t)
    if return_all:
        return G, s, pi, sig, phis, logP, M, lnZ
    return G


def G_inf(p, t, c, N=64):
    Kp = 0.5 * np.log((1 - p) / p)
    pc = 1.0 / (1.0 + np.exp(2 * c))
    return (L_moment(pc, Kp, h, t, N=N) - t * L_moment(p, c, t * h, 1.0 / t, N=N)
            - t * np.log(2 * np.cosh(Kp)) + np.log(2 * np.cosh(c)))


print("== (1) formula of Proposition H against the brute-force Renyi form ==")
worst = 0.0
ncase = 0
for n in (6, 8, 10):
    for p in (0.4, 0.3, 0.1):
        for t in (0.3, 0.45, 0.7):
            for c in ((0.0, 0.5, 1.0) if n < 10 else (0.86,)):
                gb = G_bruteforce(n, p, t, c)
                gf = G_formula_finite(n, p, t, c)
                worst = max(worst, abs(gb - gf))
                ncase += 1
print(f"{ncase} cases (n = 6, 8, 10; p = 0.4, 0.3, 0.1; t = 0.3, 0.45, 0.7; several c): max |brute force - formula| = {worst:.2e}")

# the instance gamma* of Lemma A for this family, checked from the definitions (n = 8)
n, p, t, c = 8, 0.3, 0.431, 0.86
G, s, pi, sig, phis, logP, M, lnZ = G_bruteforce(n, p, t, c, return_all=True)
phit = phis + lnZ[:, None]                                 # phi~ = phi + ln E_pi e^-phi
gam = -logsumexp(np.log(M)[:, None] - t * phit, axis=0) / t
print(f"n=8, p=0.3, t=0.431, c=0.86: G_t(M_c) = {G:.9f} (per site {G/n:.6f}; cube n F(t) = {n*cube_F(t):.6f})")
print(f"   gamma* in the class: largest |gamma*(x)-gamma*(x^i)| - u = {is_lipschitz(gam, n, [u]*n):.3e} (<= 0 admissible)")
# Gibbs law of gamma* = Renyi centre ~ pi * E_{M0}[e^{t h sigma.s}]^{1/t}
lg = np.log(pi) - gam
lg -= logsumexp(lg)
nfl = ((sig[:, :-1] * sig[:, 1:]) == -1).sum(axis=1)
lM0 = c * (n - 1 - 2 * nfl)
lM0 -= logsumexp(lM0)
inner = logsumexp(lM0[:, None] + t * h * (sig @ s.T.astype(float)), axis=0)
lq = np.log(pi) + inner / t
lq -= logsumexp(lq)
print(f"   max |ln pi_gamma* - ln( pi E_M0[e^(th sigma.s)]^(1/t) / norm )| = {np.abs(lg-lq).max():.2e}")
# gamma* is a function of the bonds s_i s_{i+1} only?
bondkey = ((s[:, :-1] * s[:, 1:]) == -1) @ (1 << np.arange(n - 1))
dev = 0.0
for k in np.unique(bondkey):
    v = gam[bondkey == k]
    dev = max(dev, v.max() - v.min())
print(f"   gamma* depends on the bonds only: max spread within a bond pattern = {dev:.2e};  osc gamma* = {gam.max()-gam.min():.4f}")

print("\n== (2) n -> infinity: G_inf(t; c), maximised over (t, c) (report: 0.033503 (0.458, 0.774), 0.038695 (0.431, 0.859), 0.041770 (0.402, 0.861), 0.039608 (0.364, 0.833)) ==")
hc, tc, ac, Ec = cube_constants(u)
print(f"cube: h = {hc:.6f} at t* = {tc:.4f}")
rows = {}
for p in (0.5, 0.4, 0.3, 0.2, 0.1):
    best = None
    for t0, c0 in ((0.45, 0.8), (0.4, 0.5), (0.48, 0.1)):
        res = minimize(lambda z: -G_inf(p, min(max(z[0], 0.02), 0.98), abs(z[1])), [t0, c0], method='Nelder-Mead',
                       options=dict(xatol=1e-6, fatol=1e-12, maxiter=2000))
        if best is None or -res.fun > best[0]:
            best = (-res.fun, min(max(res.x[0], 0.02), 0.98), abs(res.x[1]))
    val, ts, cs = best
    chk = G_inf(p, ts, cs, N=128)
    t0, v0 = golden_max(lambda t: G_inf(p, t, 0.0), 0.05, 0.95, tol=1e-7)
    rows[p] = (val, ts, cs, v0, t0)
    print(f"p={p}: h >= {val:.6f} at t* = {ts:.3f}, c* = {cs:.3f} (N=64 vs 128: {abs(val-chk):.1e});  ratio to the cube {val/hc:.3f};  i.i.d. labels (c=0): {v0:.6f} at t = {t0:.3f}")

print("\n== (3a) p -> 1/2 ==")
for p in (0.45, 0.48, 0.49, 0.499, 0.4999):
    res = minimize(lambda z: -G_inf(p, min(max(z[0], 0.02), 0.98), abs(z[1])), [0.48, 0.3], method='Nelder-Mead',
                   options=dict(xatol=1e-7, fatol=1e-13, maxiter=2000))
    print(f"p={p}: max_(t,c) G_inf = {-res.fun:.7f} at t = {res.x[0]:.4f}, c = {abs(res.x[1]):.4f};   cube {hc:.7f};  c=0: {golden_max(lambda t: G_inf(p, t, 0.0), 0.05, 0.95, tol=1e-7)[1]:.7f}")
print("   p = 1/2 exactly, any c:  G_inf(t*, c) for c = 0, 0.3, 0.8:", " ".join(f"{G_inf(0.5, tc, c):.7f}" for c in (0.0, 0.3, 0.8)),
      " (c = 0 is the cube; c > 0 must be smaller)")

print("\n== (3b) finite n against the limit (p = 0.3, t = 0.431, c = 0.859) ==")
p, t, c = 0.3, 0.431, 0.859
gi = G_inf(p, t, c)
prev = None
for n in (6, 8, 10, 12, 14, 16, 18, 20):
    g = G_formula_finite(n, p, t, c)
    inc = "" if prev is None else f"  increment per site {(g-prev)/2:.6f}"
    print(f"n={n:2d}: G_t(M_c) = {g:.6f}  per site {g/n:.6f}{inc}   (cube: {cube_F(t):.6f} per site;  limit {gi:.6f})")
    prev = g
print(f"{time.time()-T0:.1f} s")
