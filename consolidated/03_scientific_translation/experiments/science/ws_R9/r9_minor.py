#!/usr/bin/env python3
"""R9, item 1: numbers attached to minor findings that I sampled (own code; mpmath/scipy).
 (i)   SCI-REV-0001 m3:  (m, kappa, u) = (0.83, 0.166, 4), e = 0: closed form over the shells l >= 0 against the whole ray.
 (ii)  SCI-REV-0001 m11 and the table of Theorem 11.90: R^kappa(0), N^kappa(0+) and their centre types at u = 1; the cusp.
 (iii) SCI-REV-0003 m9:  the witness for T^(3)(0) <= 0.5403 a at u = 1.
 (iv)  SCI-REV-0005 m8:  the slope jump at the kink of the triangle site;  m1: E_sp(theta) - theta at theta = 0.3a.
"""
import math, sys
import numpy as np
from scipy.optimize import brentq, minimize_scalar
sys.dont_write_bytecode = True

def KL(x, k):
    s = 0.0
    if x > 0: s += x * math.log(x / k)
    if x < 1: s += (1 - x) * math.log((1 - x) / (1 - k))
    return s

def F(l, m, k):
    return m * KL(k + l / (2 * m), k) + (1 - m) * KL(k - l / (2 * (1 - m)), k)

def lrange(m, k):
    return max(-2 * m * k, -2 * (1 - m) * (1 - k)), min(2 * m * (1 - k), 2 * (1 - m) * k)

def shell_value(l, m, k, u, e=0.0):
    """min F over exits l' on the same ray with u|l'-l| <= e + F(l)"""
    b = (e + F(l, m, k)) / u
    lo, hi = lrange(m, k)
    a, c = max(l - b, lo), min(l + b, hi)
    if a <= 0 <= c: return 0.0
    return F(a, m, k) if a > 0 else F(c, m, k)

P = lambda *a: (print(*a), sys.stdout.flush())

# ---------------------------------------------------------------- (i)
m, k, u = 0.83, 0.166, 4.0
lo, hi = lrange(m, k)
grid_pos = np.linspace(0, hi, 400001)[:-1]
grid_neg = np.linspace(lo, 0, 400001)[1:]
vpos = max(shell_value(l, m, k, u) for l in grid_pos[::4])
vneg = max(shell_value(l, m, k, u) for l in grid_neg[::4])
# refine
def refine(f, a, b):
    r = minimize_scalar(lambda x: -f(x), bounds=(a, b), method="bounded", options={"xatol": 1e-14})
    return -r.fun, r.x
bp = max(grid_pos[::4], key=lambda l: shell_value(l, m, k, u)); bn = max(grid_neg[::4], key=lambda l: shell_value(l, m, k, u))
vp, lp = refine(lambda l: shell_value(l, m, k, u), max(bp - 1e-4, 0), min(bp + 1e-4, hi * (1 - 1e-12)))
vn, ln_ = refine(lambda l: shell_value(l, m, k, u), max(bn - 1e-4, lo * (1 - 1e-12)), min(bn + 1e-4, 0))
# closed form: F((Psi(u))/u), Psi(u) = max_{l>=0} [u l - F(l)]
ps = refine(lambda l: u * l - F(l, m, k), 0, hi * (1 - 1e-12))
closed = F(ps[0] / u, m, k)
P(f"(i) (m, kappa, u) = ({m}, {k}, {u}), e = 0: ray l in [{lo:.4f}, {hi:.4f}];  sup over shells l >= 0: {vp:.6f} (at l = {lp:.5f});"
  f" closed form F(Psi(u)/u) = {closed:.6f};  sup over shells l < 0 (antipodal centre, type {1-m:.2f}): {vn:.6f} (at l = {ln_:.5f})")
P("    theory report (658b77f): '0.0202 against 0.1441';  SCI-REV-0001 m3: '0.1439 against 0.0201'")
# the antipodal centre directly: type 1-m, its own closed form
m2 = 1 - m
lo2, hi2 = lrange(m2, k)
ps2 = refine(lambda l: u * l - F(l, m2, k), 0, hi2 * (1 - 1e-12))
P(f"    closed form of the antipodal centre (m = {m2:.2f}): {F(ps2[0] / u, m2, k):.6f}")

# ---------------------------------------------------------------- (ii)
u = 1.0
def V_m(m, k, u):
    lo, hi = lrange(m, k)
    ps = refine(lambda l: u * l - F(l, m, k), 0, hi * (1 - 1e-13))
    return F(ps[0] / u, m, k)
def N0_m(m, k, u):
    lo, hi = lrange(m, k)
    ps = refine(lambda l: u * l - F(l, m, k), 0, hi * (1 - 1e-13))
    return F(ps[1], m, k), ps[1], ps[0]
P("\n(ii) u = 1: kappa, R^kappa(0) [centre type], N^kappa(0+) [centre type]   (report: 0.5: 0.029139 (0.500), 0.110944; 0.45: 0.028856 (0.477), 0.109898 [0.471];")
P("      0.4: 0.028005 (0.454), 0.106755 [0.442]; 0.3: 0.024588 (0.408), 0.094080 [0.383]; 0.2: 0.018842 (0.362), 0.072574 [0.325]; 0.1: 0.010688 (0.316), 0.041588 [0.266])")
for k in (0.5, 0.45, 0.4, 0.3, 0.2, 0.1):
    ms = np.linspace(0.02, 0.98, 961)
    bR = max(ms, key=lambda m: V_m(m, k, u)); bN = max(ms, key=lambda m: N0_m(m, k, u)[0])
    R, mR = refine(lambda m: V_m(m, k, u), bR - 0.002, bR + 0.002)
    Nv, mN = refine(lambda m: N0_m(m, k, u)[0], bN - 0.002, bN + 0.002)
    P(f"      {k:4.2f}: {R:.6f} [{mR:.3f}]   {Nv:.6f} [{mN:.3f}]")
# the cusp at kappa = 0.3: N^kappa(X) for small X, at the best centre (the supremum over m is re-optimised)
k = 0.3
def N_m_X(m, k, u, X):
    lo, hi = lrange(m, k)
    Nv, lstar, Psi = N0_m(m, k, u)
    g = lambda l: u * l - F(l, m, k) - (Psi - X)
    if g(0) >= 0: return 0.0
    lX = brentq(g, 0, lstar, xtol=1e-16, rtol=1e-15)
    return F(lX, m, k)
ms = np.linspace(0.30, 0.46, 321)
N0 = max(N0_m(m, k, u)[0] for m in ms)
for X in (1e-12, 1e-10, 1e-8, 1e-6):
    NX = max(N_m_X(m, k, u, X) for m in ms)
    P(f"      kappa = 0.3: N(X = {X:g}) = N(0+) - {N0 - NX:.3e}   (sqrt law: ratio to sqrt(X) = {(N0-NX)/math.sqrt(X):.4f})")
P("      report: N^kappa(1e-12) = N^kappa(0+) - 5.8e-7 at kappa = 0.3")

# ---------------------------------------------------------------- (iii)
u = 1.0
pu = 1 / (1 + math.exp(u))
a = KL(pu, 0.5)
def theta_na(X):
    """min{KL(rho||1/2) : KL(rho||p_u) <= X}, rho in [p_u, 1/2]"""
    if X <= 0: return a
    if KL(0.5, pu) <= X: return 0.0
    rho = brentq(lambda r: KL(r, pu) - X, pu, 0.5, xtol=1e-15)
    return KL(rho, 0.5)
phi, xi1, xi2 = 0.512, 0.631 * a, 0.107 * a
mu = phi * a
t1 = mu + (1 - phi) * theta_na(xi1)
t2 = min(mu, (1 - phi) * xi1) + (1 - phi) * theta_na(xi2)
t3 = min(mu, (1 - phi) * xi2) + (1 - phi) * theta_na(0.0)
P(f"\n(iii) u = 1, a = {a:.6f}: ladder (1,1,1), phi = {phi}, xi1 = 0.631a, xi2 = 0.107a: the three terms /a = {t1/a:.5f}, {t2/a:.5f}, {t3/a:.5f};"
  f" max = {max(t1,t2,t3)/a:.5f} a   (report: 0.54026a; '<= 0.5403a')")
# two rounds for comparison: T2(0)/a at u = 1
best = min(((max(p * a + (1 - p) * theta_na(x), min(p * a, (1 - p) * x) + (1 - p) * a)) / a, p, x)
           for p in np.linspace(0.3, 0.9, 601) for x in np.linspace(0.0, 0.12, 601))
P(f"      two rounds: min over (phi, xi) on a grid = {best[0]:.5f} a at phi = {best[1]:.3f}, xi = {best[2]/a:.3f} a   (report 0.624a)")
h = None
# h/a: h = KL(Lambda1/u || 1/2)
L1 = math.log(2 / (1 + math.exp(-u)))
P(f"      h/a = {KL(L1/u, 0.5)/a:.5f}  (report 0.263)")

# ---------------------------------------------------------------- (iv)
th = 0.3 * a
rho = brentq(lambda r: KL(r, 0.5) - th, 1e-9, 0.5, xtol=1e-15)
P(f"\n(iv) cube, u = 1: E_sp(0.3a) - 0.3a = {KL(rho, pu) - th:.5f}   (report: -0.008)")
import r9_sites as S
for name, d in (("d01=1, d02=1.5, d12=2", [[0, 1, 1.5], [1, 0, 2], [1.5, 2, 0]]), ("d01=1, d12=1.5, d02=2", [[0, 1, 2], [1, 0, 1.5], [2, 1.5, 0]]),
                ("d01=1.5, d12=1, d02=2", [[0, 1.5, 2], [1.5, 0, 1], [2, 1, 0]]), ("d01=2, d02=1, d12=1.5", [[0, 2, 1], [2, 0, 1.5], [1, 1.5, 0]]),
                ("d01=1.5, d02=1, d12=2", [[0, 1.5, 1], [1.5, 0, 2], [1, 2, 0]]), ("d01=2, d02=1.5, d12=1", [[0, 2, 1.5], [2, 0, 1], [1.5, 1, 0]])):
    s = S.Site([0.2, 0.5, 0.3], d)
    Ep, Ed = s.E(); ap, ad = s.a()
    match = abs(Ep - 0.284907) < 2e-6 and abs(ap - 0.247541) < 2e-6
    P(f"     triangle site, pi = (0.2, 0.5, 0.3), {name}: E = {Ep:.6f}, a = {ap:.6f}   {'<-- the report’s tri (E = 0.284907, a = 0.247541)' if match else ''}")
    if match:
        t, hp, hd = s.h()
        P(f"       h = [{hp:.6f}, {hd:.6f}] (report 0.066729)")
        tc = 0.377987
        for dt in (1e-3, 1e-4, 1e-5):
            fl = (s.Fstar(tc - 1e-7)[0] - s.Fstar(tc - 1e-7 - dt)[0]) / dt
            fr = (s.Fstar(tc + 1e-7 + dt)[0] - s.Fstar(tc + 1e-7)[0]) / dt
            P(f"       one-sided slopes of F* at t_c = {tc} (step {dt:g}): left {fl:.6f}, right {fr:.6f}, jump {fr - fl:+.6f}   (report: 0.054049 -> 0.059631, +0.0056)")
