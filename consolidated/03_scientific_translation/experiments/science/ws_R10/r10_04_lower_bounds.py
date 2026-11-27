"""r10_04: lower ends of the brackets (Y_REPORT sections 5.3, 5.4, 6.4).  Own code.
 1. E_F closed form (Prop. J(a)) and the exact finite-n value ln Z_n(h)/Z_n(0).
 2. Prop. H: the every-n formula against the brute-force Renyi form (definition) at n=8;
    then max over (t,c) of G_inf(t;c);  c=0 (i.i.d. labels);  a-bound sup G_inf/(1-t).
"""
import time
import numpy as np
from scipy.optimize import minimize
from r10lib import *
from r10_lyap import *

u = 1.0
t0 = time.time()
hc, tc, ac, Ec = cube_exponents(u)
print("cube: h=%.7f a=%.7f E=%.7f" % (hc, ac, Ec))

print("\n1. threshold: E_F(p,u=1) and ln Z_n(h)/Z_n(0) / n")
theirs_EF = {0.4: 0.169127, 0.3: 0.232400, 0.2: 0.310766, 0.1: 0.401719}
for p in (0.4, 0.3, 0.2, 0.1):
    P = np.array([[1 - p, p], [p, 1 - p]])
    D = np.diag([np.exp(u / 2), np.exp(-u / 2)])
    # largest eigenvalue of D^(1/2) P D^(1/2) (independent of the closed form)
    Ds = np.diag([np.exp(u / 4), np.exp(-u / 4)])
    lam = np.max(np.linalg.eigvalsh(Ds @ P @ Ds))
    vals = []
    for n in (4, 16, 64, 256):
        v = np.array([0.5, 0.5]) @ D
        for _ in range(n - 1):
            v = v @ P @ D
        vals.append(np.log(v.sum()) / n)
    print("p=%.1f  E_F=%.6f (ln lam_max=%.6f; Y: %.6f)  ratio to cube %.4f   ln E e^{hm}/n at n=4,16,64,256: %s"
          % (p, E_F(p, u), np.log(lam), theirs_EF[p], E_F(p, u) / Ec, " ".join("%.6f" % x for x in vals)))

print("\n2a. Prop. H formula against the definition, n = 8 (256 labels x 256 configurations)")
n = 8
s = spins(n).astype(float)
worst = 0.0
for p in (0.4, 0.3, 0.1):
    pi = binary_chain_law(n, p)
    Kp = 0.5 * np.log((1 - p) / p)
    for t in (0.25, 0.45, 0.7):
        for c in (0.0, 0.5, 1.1):
            h = u / 2
            lab = -h * (s @ s.T)                     # rows sigma: phi_sigma(x) = -h sigma.s
            W, lnZ = gibbs(pi, lab)
            # M_c(sigma) prop. to M0(sigma) Z(sigma)^t,  Z(sigma) = sum_s exp(K' sum s s + h sigma.s)
            bonds = (s[:, 1:] * s[:, :-1]).sum(axis=1)
            lnM0 = c * bonds
            lnZsig = lnZ + np.log(2) + (n - 1) * np.log(2 * np.cosh(Kp))   # Z(sigma) = E_pi e^{h sigma.s} * Z0(K')
            lm = lnM0 + t * lnZsig
            M = np.exp(lm - lm.max()); M /= M.sum()
            G_def = -t * np.log((((M @ W ** t)) ** (1 / t)).sum())
            G_for = G_finite(t, c, p, u, n)
            worst = max(worst, abs(G_def - G_for))
print("   27 cases, largest |definition - formula| = %.2e" % worst)

print("\n2b. Prop. H: max over (t,c) of G_inf(t;c)   [operator N=48; checked with N=80 and exact increments]")
theirs_H = {0.4: (0.033503, 0.458, 0.774), 0.3: (0.038695, 0.431, 0.859), 0.2: (0.041770, 0.402, 0.861), 0.1: (0.039608, 0.364, 0.833)}
theirs_iid = {0.4: 0.028907, 0.3: 0.028151, 0.2: 0.026626, 0.1: 0.023418}
res = {}
for p in (0.4, 0.3, 0.2, 0.1):
    f = lambda v: -G_inf(min(max(v[0], 0.02), 0.98), max(v[1], 0.0), p, u)
    best = None
    for start in ((0.45, 0.8), (0.4, 0.5)):
        r = minimize(f, start, method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-12))
        if best is None or r.fun < best.fun:
            best = r
    tt, cc = best.x
    val = -best.fun
    val80 = G_inf(tt, cc, p, u, N=80)
    # exact finite-n increments (Aitken) as an independent evaluation at the optimum
    h = u / 2; Kp = 0.5 * np.log((1 - p) / p); pc = 1 / (1 + np.exp(2 * cc))
    ex = (lyap_exact(Kp, h, pc, tt, 22)[1] - tt * lyap_exact(cc, tt * h, p, 1 / tt, 22)[1]
          - tt * np.log(2 * np.cosh(Kp)) + np.log(2 * np.cosh(cc)))
    # their (t*, c*) evaluated with my code
    th = theirs_H[p]
    at_theirs = G_inf(th[1], th[2], p, u)
    # c = 0
    r0 = minimize(lambda v: -G_inf(min(max(v[0], 0.02), 0.98), 0.0, p, u), [0.45], method="Nelder-Mead",
                  options=dict(xatol=1e-7, fatol=1e-13))
    res[p] = (val, tt, cc)
    print("p=%.1f  h >= %.6f at (t*=%.3f, c*=%.3f)  [N=80: %.6f; exact increments: %.6f]   Y: %.6f (%.3f, %.3f); my code at Y's (t*,c*): %.6f   ratio to cube %.4f"
          % (p, val, tt, cc, val80, ex, th[0], th[1], th[2], at_theirs, val / hc))
    print("        c=0 (i.i.d. labels; instance = zero residual): max_t = %.6f at t=%.3f  (Y: %.6f)   ratio to cube %.4f"
          % (-r0.fun, r0.x[0], theirs_iid[p], -r0.fun / hc))

print("\n2c. a >= sup_{t,c} G_inf(t;c)/(1-t)   and   E >= sup G_inf(t;c)/t  (family of Prop. H only)")
for p in (0.4, 0.3, 0.2, 0.1):
    best_a = (0, 0, 0)
    for t in (0.9, 0.97, 0.99, 0.997, 0.999):
        r = minimize(lambda v: -G_inf(t, max(v[0], 0.0), p, u, N=64) / (1 - t), [0.6], method="Nelder-Mead",
                     options=dict(xatol=1e-5, fatol=1e-12))
        if -r.fun > best_a[0]:
            best_a = (-r.fun, t, r.x[0])
        print("   p=%.1f t=%.3f: sup_c G/(1-t) = %.6f at c=%.3f" % (p, t, -r.fun, r.x[0]))
    best_e = (0, 0, 0)
    for t in (0.1, 0.03, 0.01):
        for c in (1.0, 2.0, 4.0, 8.0):
            v = G_inf(t, c, p, u, N=64) / t
            if v > best_e[0]:
                best_e = (v, t, c)
    print("p=%.1f  a >= %.6f (t=%.3f,c=%.3f; ratio to cube %.4f)    E >= %.6f (t=%.2f, c=%.1f) vs E_F=%.6f"
          % (p, best_a[0], best_a[1], best_a[2], best_a[0] / ac, best_e[0], best_e[1], best_e[2], E_F(p, u)))
print("time %.1fs" % (time.time() - t0))
