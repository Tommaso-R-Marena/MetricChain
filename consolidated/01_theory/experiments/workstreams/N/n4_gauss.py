#!/usr/bin/env python3
"""Workstream N, check 4: Gauss space (N_REPORT sections 4(e'), 5.1, 5.3).

  G1  the closed forms of the two tail functions of the L-Lipschitz class on (R^n, gamma_n),
        Xi_L(q) = e^{L^2/2 - Lt} Phi(L - t) - Phi(-t),  t = Phi^-1(1-q);     Theta_L(p) = p + e^{Lc + L^2/2} Phi(-c-L),  c = Phi^-1(p),
      against numerical integration of  int_0^inf L e^{Lr} Phi(-t-r) dr  and  int_0^inf L e^{-Lr} Phi(c+r) dr.
  G2  (TU), (TL) on L-Lipschitz functions, by quadrature (no Monte Carlo):
        n = 1  (random piecewise functions on a grid of 4*10^5 points);
        n = 2  (grid 2001^2: cones, envelopes, half-planes in random directions);
        any n  (radial functions g(|x|): one-dimensional integrals against the chi law);
        any n  (functions of (x_1, |x_perp|): the ball dips of Proposition N11 -- bounded sets that nearly attain the tail function).
  G3  the sum metric: c-Lipschitz functions for l_1 on (R^m, gamma_m) against Xi_{c sqrt m}  (m = 2 on the grid; the diagonal
      half-space attains it; a coordinate function stays far below).
  G4  Proposition N11 (the hinted lower bound from ball dips): the exact effect of the dip on B(r_0 e_1, rho), r_0 = n/t,
      rho^2 = n^2/t^2 - n, against the proved bound 0.112 e^{L^2/2 - Lt} - Phi(-t)/2 and against the half-space value Xi_L(Phi(-t)).
  G5  Algorithm A in its unbounded variant (Theorem N1', N_REPORT 2.5) on a Gaussian outer space: V(a) = e^{-g(a)} with g
      L-Lipschitz (Euclid) or c-Lipschitz for l_1, A known exactly; validity, width, termination within J levels.
  G6  two levels with and without extensivity for the Gaussian pair.
  G7  the abstract base family (Proposition N2) on Gauss space: coverage and width.

Run:  python3 n4_gauss.py > out_n4_gauss.txt        (about 2 minutes)
"""
import math
import sys
import time

import numpy as np
from scipy import integrate
from scipy.special import ndtr, ndtri, log_ndtr
from scipy.stats import chi as chi_dist

from nlib import gauss_Xi, gauss_Theta, Consts, closing_level_grid, run_level, check_run, INF

t0 = time.time()
rng = np.random.default_rng(271126)
fails = 0

print("=" * 110)
print("G1. closed forms against numerical integration")
print("=" * 110)
worst = 0.0
for L in (0.3, 1.0, 2.5, 4.0):
    for q in (1e-8, 1e-4, 0.01, 0.2, 0.5, 0.9, 0.999):
        t = -ndtri(q)
        num, _ = integrate.quad(lambda r: L * math.exp(L * r + log_ndtr(-t - r)), 0, np.inf, epsabs=0, epsrel=1e-11, limit=400)
        cf = gauss_Xi(L, q)
        c = ndtri(q)
        num2, _ = integrate.quad(lambda r: L * math.exp(-L * r) * ndtr(c + r), 0, np.inf, epsabs=0, epsrel=1e-11, limit=400)
        cf2 = gauss_Theta(L, q)
        worst = max(worst, abs(num / cf - 1), abs(num2 / cf2 - 1))
print("  28 pairs (L, q), L in {0.3, 1, 2.5, 4}, q from 1e-8 to 0.999: largest relative difference %.2e" % worst)
fails += worst > 1e-8
# three elementary facts used in N_REPORT 5.1 (checked on grids; the first two are quoted there from memory)
from scipy.stats import chi2
ks = np.unique(np.round(np.exp(np.linspace(0, math.log(1e6), 400)))).astype(int)
med_ok = bool(np.all(chi2.cdf(ks, ks) > 0.5))
tt = np.linspace(0, 38, 38001)
mills_ok = bool(np.all(log_ndtr(-tt) >= -0.5 * tt * tt - np.log(3 * (1 + tt))))
worst_U = -INF
for L in (1.0, 3.0, 6.0, 10.0):
    for t in np.linspace(-3.0, L + 12.0, 3001):
        q = float(ndtr(-t))
        if q <= 0 or q >= 1:
            continue
        lhs = L * L / 2 - L * t + float(log_ndtr(L - t)) - float(log_ndtr(-t))        # ln(Xi_L(q)/q + 1)
        rhs = max(L - t, 0.0) ** 2 / 2 + math.log(3 * (1 + abs(t)))
        worst_U = max(worst_U, lhs - rhs)
print("  P(chi^2_k <= k) > 1/2 for k up to 10^6: %s;   Phi(-t) >= e^{-t^2/2}/(3(1+t)) on [0, 38]: %s;   "
      "ln(1 + Xi_L(q)/q) - [(L-t)_+^2/2 + ln(3(1+|t|))] <= %.3f [<= 0] for L in {1, 3, 6, 10}" % (med_ok, mills_ok, worst_U))
fails += (not med_ok) + (not mills_ok) + (worst_U > 1e-9)


def check_levels(V, w, L, levels, tol):
    """max over the levels of E(V-s)_+ / (s Xi_L(q)) and min of E min(V,s) / (s Theta_L(p)); V, w flat arrays (w sums to ~1)"""
    order = np.argsort(V)
    Vs = V[order]
    ws = w[order]
    cvw = np.concatenate(([0.0], np.cumsum(ws * Vs)))                     # sums over {V < s}
    sw = np.concatenate((np.cumsum(ws[::-1])[::-1], [0.0]))               # sums over the super-level sets, computed
    svw = np.concatenate((np.cumsum((ws * Vs)[::-1])[::-1], [0.0]))       # from the top (no cancellation against the bulk)
    mx, mn = 0.0, INF
    for s in levels:
        i_gt = int(np.searchsorted(Vs, s, side='right'))
        i_ge = int(np.searchsorted(Vs, s, side='left'))
        q = sw[i_gt]
        tail = svw[i_gt] - s * q
        if 1e-12 < q < 1 - 1e-9:
            mx = max(mx, tail / (s * gauss_Xi(L, min(q, 1 - 1e-15))))
        p = sw[i_ge]
        if p > 1e-12:
            trunc = cvw[i_ge] + s * p
            mn = min(mn, trunc / (s * gauss_Theta(L, min(p, 1.0))))
    return mx, mn


print()
print("=" * 110)
print("G2. (TU), (TL) for L-Lipschitz functions on Gauss space, by quadrature")
print("=" * 110)
# ---- n = 1 ----
x = np.linspace(-13.0, 13.0, 400001)
w = np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi) * (x[1] - x[0])
w[0] *= 0.5
w[-1] *= 0.5


def rand_lip_1d(L):
    kind = int(rng.integers(5))
    if kind == 0:
        f = np.full_like(x, INF)
        for _ in range(int(rng.integers(1, 6))):
            f = np.minimum(f, rng.uniform(-2, 2) + rng.uniform(0.2, 1) * L * np.abs(x - rng.uniform(-3, 3)))
        return f
    if kind == 1:
        f = np.full_like(x, -INF)
        for _ in range(int(rng.integers(1, 6))):
            f = np.maximum(f, rng.uniform(-2, 2) - rng.uniform(0.2, 1) * L * np.abs(x - rng.uniform(-3, 3)))
        return f
    if kind == 2:
        return rng.uniform(-L, L) * x
    if kind == 3:
        om = rng.uniform(0.3, 3)
        return 0.7 * L * np.sin(x * om) / om + rng.uniform(-L, L) * 0.3 * x
    f1, f2 = rand_lip_1d(L), rand_lip_1d(L)
    return np.minimum(f1, f2) if rng.uniform() < 0.5 else np.maximum(f1, f2)


for L in (0.5, 1.5, 3.0):
    mx_all, mn_all = 0.0, INF
    for rep in range(60):
        f = rand_lip_1d(L)
        assert np.max(np.abs(np.diff(f))) <= L * (x[1] - x[0]) * (1 + 1e-6)
        V = np.exp(-(f - f.min()))
        levels = np.quantile(V, np.linspace(0.001, 0.9995, 50))
        mx, mn = check_levels(V, w, L, levels, 1e-3)
        mx_all, mn_all = max(mx_all, mx), min(mn_all, mn)
    # the extremal function: V = e^{L (x - t)_+}
    ext = []
    for tt in (-1.0, 0.5, 2.0):
        V = np.exp(L * np.maximum(x - tt, 0))
        mx, mn = check_levels(V, w, L, [1.0 + 1e-9], 1e-3)
        V2 = np.exp(-L * np.maximum(x - tt, 0))
        mx2, mn2 = check_levels(V2, w, L, [1.0], 1e-3)
        ext.append((mx, mn2))
    print("  n=1  L=%.1f  60 random functions x 50 levels: max E(V-s)_+/(s Xi) = %.5f [<=1], min E min(V,s)/(s Theta) = %.5f [>=1];"
          "  half-lines: upper %s, lower %s" % (L, mx_all, mn_all, " ".join("%.5f" % e[0] for e in ext), " ".join("%.5f" % e[1] for e in ext)))
    fails += (mx_all > 1 + 2e-3) + (mn_all < 1 - 2e-3) + any(abs(e[0] - 1) > 2e-3 or abs(e[1] - 1) > 2e-3 for e in ext)

# ---- n = 2 ----
g1 = np.linspace(-8.5, 8.5, 2001)
X1, X2 = np.meshgrid(g1, g1, indexing='ij')
w2 = (np.exp(-0.5 * (X1 ** 2 + X2 ** 2)) / (2 * math.pi) * (g1[1] - g1[0]) ** 2).ravel()


def rand_lip_2d(L, metric=2):
    """L-Lipschitz for the Euclidean norm (metric=2) or for l_1 (metric=1)"""
    def dist(c):
        if metric == 2:
            return np.sqrt((X1 - c[0]) ** 2 + (X2 - c[1]) ** 2)
        return np.abs(X1 - c[0]) + np.abs(X2 - c[1])
    kind = int(rng.integers(4))
    if kind == 0:
        f = np.full(X1.shape, INF)
        for _ in range(int(rng.integers(1, 5))):
            f = np.minimum(f, rng.uniform(-2, 2) + rng.uniform(0.3, 1) * L * dist(rng.uniform(-2.5, 2.5, size=2)))
        return f
    if kind == 1:
        f = np.full(X1.shape, -INF)
        for _ in range(int(rng.integers(1, 5))):
            f = np.maximum(f, rng.uniform(-2, 2) - rng.uniform(0.3, 1) * L * dist(rng.uniform(-2.5, 2.5, size=2)))
        return f
    if kind == 2:
        if metric == 2:
            th = rng.uniform(0, 2 * math.pi)
            return -L * np.maximum(math.cos(th) * X1 + math.sin(th) * X2 - rng.uniform(-1, 2), 0)
        sg = rng.choice([-1.0, 1.0], size=2)
        return -L * np.maximum(sg[0] * X1 + sg[1] * X2 - rng.uniform(-1, 2), 0)
    f1, f2 = rand_lip_2d(L, metric), rand_lip_2d(L, metric)
    return np.minimum(f1, f2) if rng.uniform() < 0.5 else np.maximum(f1, f2)


for L in (0.7, 2.0):
    mx_all, mn_all = 0.0, INF
    for rep in range(14):
        f = rand_lip_2d(L)
        V = np.exp(-(f - f.min())).ravel()
        levels = np.quantile(V[::37], np.linspace(0.002, 0.999, 30))
        mx, mn = check_levels(V, w2, L, levels, 2e-2)
        mx_all, mn_all = max(mx_all, mx), min(mn_all, mn)
    th = 0.7
    V = np.exp(L * np.maximum(math.cos(th) * X1 + math.sin(th) * X2 - 0.8, 0)).ravel()
    mxe, _ = check_levels(V, w2, L, [1.0 + 1e-9], 2e-2)
    print("  n=2  L=%.1f  14 random functions x 30 levels: max ratio (upper) %.5f [<=1], min ratio (lower) %.5f [>=1];  a half-plane: %.5f"
          % (L, mx_all, mn_all, mxe))
    fails += (mx_all > 1.01) + (mn_all < 0.99) + (abs(mxe - 1) > 0.01)

# ---- any n: radial functions ----
for n in (3, 20, 200):
    r = np.linspace(0.0, math.sqrt(n) + 14.0, 300001)
    wr = chi_dist.pdf(r, n) * (r[1] - r[0])
    for L in (0.5, 2.0):
        mx_all, mn_all = 0.0, INF
        for rep in range(20):
            kind = rep % 5
            c0 = math.sqrt(n) + rng.uniform(-2, 2)
            if kind == 0:
                g = L * r
            elif kind == 1:
                g = -L * r
            elif kind == 2:
                g = L * np.abs(r - c0)
            elif kind == 3:
                g = -L * np.abs(r - c0)
            else:
                g = L * np.minimum(np.abs(r - c0), rng.uniform(0.5, 3))
            V = np.exp(-(g - g.min()))
            levels = np.quantile(V[wr > 1e-14 * wr.max()], np.linspace(0.002, 0.999, 40))
            mx, mn = check_levels(V, wr, L, levels, 1e-3)
            mx_all, mn_all = max(mx_all, mx), min(mn_all, mn)
        print("  n=%3d radial, L=%.1f: 20 profiles x 40 levels: max ratio (upper) %.5f [<=1], min ratio (lower) %.5f [>=1]" % (n, L, mx_all, mn_all))
        fails += (mx_all > 1 + 2e-3) + (mn_all < 1 - 2e-3)

print()
print("=" * 110)
print("G3. the sum metric on Gauss space: c-Lipschitz for l_1 on R^m against Xi_{c sqrt m}  (m = 2, grid)")
print("=" * 110)
# a grid with incommensurable spacings in the two coordinates: the boundaries of the extremal sets are the lines
# x1 +- x2 = const, which on a square lattice are lattice lines (a systematic error of order of the spacing)
g2b = np.linspace(-8.5, 8.5, 1873)
X1, X2 = np.meshgrid(g1, g2b, indexing='ij')
w2 = (np.exp(-0.5 * (X1 ** 2 + X2 ** 2)) / (2 * math.pi) * (g1[1] - g1[0]) * (g2b[1] - g2b[0])).ravel()
for c in (0.5, 1.5):
    Lm = c * math.sqrt(2.0)
    mx_all, mn_all = 0.0, INF
    for rep in range(12):
        f = rand_lip_2d(c, metric=1)
        V = np.exp(-(f - f.min())).ravel()
        levels = np.quantile(V[::37], np.linspace(0.002, 0.999, 30))
        mx, mn = check_levels(V, w2, Lm, levels, 2e-2)
        mx_all, mn_all = max(mx_all, mx), min(mn_all, mn)
    V = np.exp(c * np.maximum(X1 + X2 - 0.8 * math.sqrt(2.0), 0)).ravel()        # the diagonal half-plane {(x1+x2)/sqrt 2 > 0.8}
    mxd, _ = check_levels(V, w2, Lm, [1.0 + 1e-9], 2e-2)
    V = np.exp(c * np.maximum(X1 - 0.8, 0)).ravel()                               # a coordinate half-plane
    mxc, _ = check_levels(V, w2, Lm, [1.0 + 1e-9], 2e-2)
    print("  c=%.1f (L = c sqrt 2 = %.3f): 12 random l_1-Lipschitz functions x 30 levels: max ratio %.5f [<=1], min ratio (lower) %.5f [>=1];"
          "  diagonal half-plane %.5f (attains), coordinate half-plane %.5f" % (c, Lm, mx_all, mn_all, mxd, mxc))
    fails += (mx_all > 1.01) + (mn_all < 0.99) + (abs(mxd - 1) > 0.01)

print()
print("=" * 110)
print("G4. Proposition N11: ball dips g_z(x) = -L (rho - |x - z|)_+, z = r_0 e_1, r_0 = n/t, rho^2 = n^2/t^2 - n")
print("    effect = E[(e^{L(rho - |x-z|)} - 1)_+] by quadrature in (x_1, |x_perp|);  hit fraction of any point <= e^{-t^2/2}")
print("=" * 110)
print("  %4s %5s %8s | %12s %12s %8s | %12s %10s | %s" % ("L", "t", "n", "ball effect", "half-space", "ratio", "proved bound", "bound ok", "n >= max(4t^2, L T^2 t)"))
for (L, t, n) in [(3.0, 1.0, 100), (3.0, 1.0, 1000), (3.0, 1.0, 10000), (4.0, 2.0, 200), (4.0, 2.0, 2000), (4.0, 2.0, 100000),
                  (5.0, 1.0, 300), (5.0, 3.0, 2000), (5.0, 3.0, 50000), (6.0, 4.0, 3000), (2.0, 0.5, 30)]:
    T = L + 1.2816
    r0 = n / t
    rho = math.sqrt(n * n / (t * t) - n)
    # integrate over x1 in [t-ish, L + 9] under the tilted law N(L,1) and R = |x_perp| ~ chi_{n-1}
    x1 = np.linspace(-6.0, L + 10.0, 3201)
    R = np.linspace(max(0.0, math.sqrt(n - 1) - 9.0), math.sqrt(n - 1) + 9.0, 1601)
    w1 = np.exp(-0.5 * x1 * x1) / math.sqrt(2 * math.pi) * (x1[1] - x1[0])
    wR = chi_dist.pdf(R, n - 1) * (R[1] - R[0])
    XX, RR = np.meshgrid(x1, R, indexing='ij')
    dist = np.sqrt((XX - r0) ** 2 + RR ** 2)
    depth = np.maximum(rho - dist, 0.0)
    eff = float(np.einsum('i,j,ij->', w1, wR, np.expm1(L * depth)))
    half = gauss_Xi(L, float(ndtr(-t)))
    bound = 0.112 * math.exp(L * L / 2 - L * t) - 0.5 * float(ndtr(-t))
    cond = n >= max(4 * t * t, L * T * T * t) and t <= L
    okb = (eff >= bound) if cond else None
    if cond and not eff >= bound:
        fails += 1
    # (TU) for the ball-dip function itself (a function of (x_1, |x_perp|)): ratio at the level s = 1
    Vd = np.exp(L * depth).ravel()
    wd = np.outer(w1, wR).ravel()
    q = float(wd[Vd > 1.0 + 1e-12].sum())
    ratio_tu = eff / gauss_Xi(L, q)
    if ratio_tu > 1.005:
        fails += 1
    print("  %4.1f %5.1f %8d | %12.5g %12.5g %8.4f | %12.5g %10s | %s   [gamma(ball) = %.4g vs Phi(-t) = %.4g; (TU) ratio at its own measure %.4f]"
          % (L, t, n, eff, half, eff / half, bound, {True: "yes", False: "NO", None: "n/a"}[okb], "yes" if cond else "no",
             q, float(ndtr(-t)), ratio_tu))
# the cap bound P(omega_1 >= s) <= e^{-n s^2/2} on the sphere, exactly (the law of omega_1 has density prop. to (1-x^2)^{(n-3)/2})
worst = 0.0
for n in (5, 30, 300, 3000):
    xs_ = np.linspace(-1, 1, 400001)
    dens = np.exp(0.5 * (n - 3) * np.log(np.maximum(1 - xs_ * xs_, 1e-300)))
    dens /= dens.sum()
    cdf_up = np.cumsum(dens[::-1])[::-1]
    for s_ in (0.02, 0.05, 0.1, 0.3, 0.6):
        i = int(np.searchsorted(xs_, s_))
        worst = max(worst, cdf_up[i] / math.exp(-n * s_ * s_ / 2))
print("  cap bound P(omega_1 >= s) <= e^{-n s^2/2}: largest ratio over n in {5, 30, 300, 3000}, s in {.02 .. .6}: %.4f [<=1]" % worst)
fails += worst > 1.0

print()
print("=" * 110)
print("G5. Algorithm A, unbounded variant (Theorem N1'), on a Gaussian outer space R^{n_o}: V = e^{-g}, exact A")
print("=" * 110)


def chi_mgf(n, L):
    """E e^{L |x|} for x ~ N(0, I_n)"""
    r = np.linspace(0.0, math.sqrt(n) + abs(L) + 14.0, 400001)
    return float(np.sum(chi_dist.pdf(r, n) * np.exp(L * r)) * (r[1] - r[0]))


def l1_mgf(c):
    """E e^{c |x_1|}"""
    return 2.0 * math.exp(c * c / 2) * float(ndtr(c))


stats = {}
LIN = dict(runs=0, viol=0, min=INF)
for (label, n_o, L, metric) in (("Euclid L=1.5", 6, 1.5, 2), ("Euclid L=2.5", 4, 2.5, 2), ("Euclid L=3.5", 3, 3.5, 2),
                                ("l_1 c=0.6 (L = c sqrt n_o)", 6, 0.6, 1)):
    Leff = L if metric == 2 else L * math.sqrt(n_o)
    Xi = lambda q, Leff=Leff: gauss_Xi(Leff, min(q, 1.0))
    ThBar = lambda p, Leff=Leff: max(p, gauss_Theta(Leff, min(p, 1.0)))
    if metric == 2:
        up, lo = chi_mgf(n_o, L), chi_mgf(n_o, -L)
    else:
        up, lo = l1_mgf(L) ** n_o, l1_mgf(-L) ** n_o
    qgrid = np.exp(np.linspace(math.log(1e-15), math.log(0.999999), 6000))
    for pname, lam, eta, etap, theta, nu1, b in [("th=.5", 0.5, 0.5, 0.5, 0.5, 4.0, 0.5), ("th=5", 1.0, 0.5, 1.0, 5.0, 1.0, 1.0)]:
        if L == 3.5 and pname == "th=.5":
            continue                                          # closing level 2e-6: samples beyond the simulation
        xs = [8.0, 3.0, b]
        closing = lambda thrN, th, ce: closing_level_grid(Xi, ThBar, thrN, th, ce, qgrid)
        C = Consts(lam, eta, etap, theta, nu1, b, xs, 0.05, 0.2, closing, lnDA=math.log(up / lo), mode='unb')
        for inst in range(5):
            omega = rng.normal(size=n_o)
            omega /= np.linalg.norm(omega)
            sg = rng.choice([-1.0, 1.0], size=n_o)
            tq = float(rng.uniform(0.0, 2.0))
            if inst == 0:                                     # zero function
                gfun = lambda a: np.zeros(len(a))
                A = 1.0
                pfun = lambda s: 1.0 if s < 1 else 0.0
            elif inst == 1 and metric == 2:                   # extremal dip on a half-space
                gfun = lambda a, omega=omega, tq=tq: -L * np.maximum(a @ omega - tq, 0)
                A = 1.0 + gauss_Xi(L, float(ndtr(-tq)))
                pfun = lambda s, tq=tq: 1.0 if s < 1 else float(ndtr(-(tq + math.log(s) / L)))
            elif inst == 1:                                   # extremal dip on a diagonal half-space (l_1)
                gfun = lambda a, sg=sg, tq=tq: -L * np.maximum(a @ sg - tq * math.sqrt(n_o), 0)
                A = 1.0 + gauss_Xi(Leff, float(ndtr(-tq)))
                pfun = lambda s, tq=tq: 1.0 if s < 1 else float(ndtr(-(tq + math.log(s) / Leff)))
            elif inst == 2 and metric == 2:                   # linear
                gfun = lambda a, omega=omega: L * (a @ omega)
                A = math.exp(L * L / 2)
                pfun = lambda s: float(ndtr(-math.log(s) / L))
            elif inst == 2:
                gfun = lambda a, sg=sg: L * (a @ sg)
                A = math.exp(Leff * Leff / 2)
                pfun = lambda s: float(ndtr(-math.log(s) / Leff))
            elif inst == 3 and metric == 2:                   # radial cone (a peak at the origin)
                gfun = lambda a: L * np.linalg.norm(a, axis=1)
                A = lo
                pfun = lambda s: float(chi_dist.cdf(-math.log(s) / L, n_o)) if s < 1 else 0.0
            elif inst == 3:
                gfun = lambda a: L * np.abs(a).sum(axis=1)
                A = lo
                pfun = None
            elif metric == 2:                                 # radial anti-cone: the largest member with g(0) = 0
                gfun = lambda a: -L * np.linalg.norm(a, axis=1)
                A = up
                pfun = lambda s: float(chi_dist.sf(math.log(s) / L, n_o)) if s > 1 else 1.0
            else:
                gfun = lambda a: -L * np.abs(a).sum(axis=1)
                A = up
                pfun = None
            draw = lambda kk, gfun=gfun: np.exp(-gfun(rng.normal(size=(kk, n_o))))
            ell0, u0 = lo, up                                 # g(0) = 0 in every instance:  E e^{-d(x,0)} <= A <= E e^{d(0,x)}
            assert ell0 <= A * (1 + 1e-9) <= u0 * (1 + 2e-9)
            for rep in range(3):
                res = run_level(rng, draw, C, Xi, ThBar, ell0, Vmax=None, oracle_mode=rep % 4, max_points=4_000_000)
                key = "%s %s" % (label, pname)
                d = stats.setdefault(key, dict(runs=0, stopped=0, invalid=0, width=0, term=0, checks=0, maxM=0, maxlev=0, C=C,
                                               neg=0, pop=0))
                d['runs'] += 1
                if res['stop'] == 'closed':
                    d['stopped'] += 1
                    valid = res['L'] <= A * (1 + 1e-9) and A <= res['U'] * (1 + 1e-9)
                    d['invalid'] += (not valid)
                    d['width'] += not (res['U'] <= C.ratio_bound * res['L'] * (1 + 1e-9))
                    d['term'] += not (res['level'] <= C.J)
                    d['maxM'] = max(d['maxM'], res['npoints'])
                    d['maxlev'] = max(d['maxlev'], res['level'])
                    d['neg'] += sum(1 for l in res['levels'] if l.get('kind') == 'neg')
                    d['pop'] += sum(1 for l in res['levels'] if l.get('kind') == 'pop')
                    if pfun is not None:
                        chk = check_run(res, C, A, pfun)
                        if chk['good'] and not all(chk[k] for k in chk):
                            d['checks'] += 1
                        if inst == 2 and chk['good'] and C.xout < Leff * Leff / 2:
                            # Proposition N10(b): at the linear instance M_max >= (2K/(1+eta)) exp((L - sqrt(2 x_out))^2/2)
                            Mmax = max(pa['M'] for lev in res['levels'] for pa in lev['passes'])
                            bnd = 2 * C.K / (1 + C.eta) * math.exp((Leff - math.sqrt(2 * C.xout)) ** 2 / 2)
                            LIN['runs'] += 1
                            LIN['min'] = min(LIN['min'], Mmax / bnd)
                            LIN['viol'] += Mmax < bnd
for key, d in stats.items():
    C = d['C']
    print("  %-34s runs %3d  closed %3d  invalid %d  width violated %d  stopped above level J %d  proof checks failed on the good event %d |"
          " levels left: %d populated, %d negligible | J = %d, highest stopping level %d; pi_* = %.3g, largest sample %d (Mbar = %.3g)"
          % (key, d['runs'], d['stopped'], d['invalid'], d['width'], d['term'], d['checks'], d['pop'], d['neg'], C.J, d['maxlev'],
             C.pi_star, d['maxM'], C.Mbar))
    fails += d['invalid'] + d['width'] + d['term'] + d['checks'] + (d['stopped'] < d['runs'])
print("  Proposition N10(b) at the linear instances with x_out < L^2/2: %d runs, smallest M_max / [(2K/(1+eta)) e^{(L - sqrt(2 x_out))^2/2}] = %.2f [>= 1], violations %d"
      % (LIN['runs'], LIN['min'], LIN['viol']))
fails += LIN['viol']

print()
print("=" * 110)
print("G6. two levels for the Gaussian pair theta_na(x) = (1 - sqrt x)^2 (units of a): with and without extensivity")
print("=" * 110)
tna = lambda xx: (1 - math.sqrt(min(max(xx, 0.0), 1.0))) ** 2
best = min(max(1 - phi, max(min(g, phi) + (1 - phi) * tna(g / (1 - phi)) for g in np.linspace(0, 1, 2001)))
           for phi in np.linspace(0.01, 0.99, 981))
noext = min(max(max(min(g, tna(G - bb)) + tna(g) for g in np.linspace(bb, 1.5, 600)) for bb in np.linspace(1e-4, G - 1e-4, 60))
            for G in (0.02,))
print("  at accuracy -> 0:  sum metric (blocks phi, 1-phi):  tau_2/a = min_phi sup_gamma [min(gamma, phi) + (1-phi) theta_na(gamma/(1-phi))] = %.4f" % best)
print("  Euclidean class (no factors phi, 1-phi), accuracy G = 0.02 a:  inf_beta sup_gamma [min(gamma, theta_na(G-beta)) + theta_na(gamma)] = %.4f"
      "  >=  theta_na(G) = %.4f" % (noext, tna(0.02)))
fails += noext < tna(0.02) - 1e-9

print()
print("=" * 110)
print("G7. the abstract base family (Proposition N2: two samples, threshold at the K-th largest value, closed by the two tail")
print("    functions) on Gauss space R^6, L = 1.5:  L = A^/(1+eta) <= A <= U = A^/(1-eta) + t^ Xi(q_+),  U/L <= ((1+eta)/(1-eta)) (1 + Xi(q_+)/ThetaBar(q_-))")
print("=" * 110)
n_b, Lb_ = 6, 1.5
eta = 0.25
Kb = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(4 / 0.05))
fail_bound = 4 * math.exp(-eta * eta * Kb / (3 * (1 + eta)))
up, lo = chi_mgf(n_b, Lb_), chi_mgf(n_b, -Lb_)
omega = np.zeros(n_b)
omega[0] = 1.0
insts = [("zero", lambda a: np.zeros(len(a)), 1.0),
         ("half-space dip t=1", lambda a: -Lb_ * np.maximum(a @ omega - 1.0, 0), 1.0 + gauss_Xi(Lb_, float(ndtr(-1.0)))),
         ("linear", lambda a: Lb_ * (a @ omega), math.exp(Lb_ * Lb_ / 2)),
         ("cone L|x|", lambda a: Lb_ * np.linalg.norm(a, axis=1), lo),
         ("anti-cone -L|x|", lambda a: -Lb_ * np.linalg.norm(a, axis=1), up)]
for M in (4000, 40000):
    qp, qm = Kb / ((1 - eta) * M), Kb / ((1 + eta) * M)
    rb = (1 + eta) / (1 - eta) * (1 + gauss_Xi(Lb_, qp) / max(qm, gauss_Theta(Lb_, qm)))
    row = []
    for name, gfun, A in insts:
        cover = 0
        within = 0
        reps = 200
        for rep in range(reps):
            V1 = np.exp(-gfun(rng.normal(size=(M, n_b))))
            V2 = np.exp(-gfun(rng.normal(size=(M, n_b))))
            that = np.partition(V1, M - Kb)[M - Kb]                     # the K-th largest value of the first sample
            Ahat = float(np.mean(np.minimum(V2, that)))
            Lo, Up = Ahat / (1 + eta), Ahat / (1 - eta) + that * gauss_Xi(Lb_, qp)
            cover += (Lo <= A <= Up)
            within += (Up / Lo <= rb * (1 + 1e-9))
        row.append("%s: covered %d/%d, ratio within the bound %d/%d" % (name, cover, reps, within, reps))
        if cover < reps * (1 - fail_bound) - 3 * math.sqrt(reps * fail_bound):
            fails += 1
    print("  M=%5d (K=%d, q_+=%.4f, ratio bound %.3f; failure bound %.3f):  %s" % (M, Kb, qp, rb, fail_bound, ";  ".join(row)))

print()
print("violations:", fails, "   time %.1f s" % (time.time() - t0))
sys.exit(1 if fails else 0)
