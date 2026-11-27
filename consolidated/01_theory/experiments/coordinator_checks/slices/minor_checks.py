#!/usr/bin/env python3
"""Assistant A, SCI-REV-0001: numerics for section 4 of the review (four-line proof, curvature form) and for the
minor findings m1-m6, m11, m12.  Own code (numpy/scipy), fixed seed; imports only m2_check.py (also mine)."""
import math, sys, time
import numpy as np
from scipy.optimize import linprog, minimize
import m2_check as M

rng = np.random.default_rng(20261125)
kl, F, Fp, lmax, lstar, golden, logit, sig, hb = M.kl, M.F, M.Fp, M.lmax, M.lstar, M.golden, M.logit, M.sig, M.hb
K = lambda x: x * math.tanh(x) - math.log(math.cosh(x))
lc = lambda x: math.log(math.cosh(x))


def table(p, q, c):
    """T_c(b, x) = p_b q_x + c b x, b, x = +1, -1 (p, q = probabilities of +1)."""
    return np.array([[p * q + c, p * (1 - q) - c], [(1 - p) * q - c, (1 - p) * (1 - q) + c]])


def omega(T):
    return math.log(T[0, 0] * T[1, 1] / (T[0, 1] * T[1, 0]))


def mi(T):
    return float((T * np.log(T / (T.sum(1, keepdims=True) * T.sum(0, keepdims=True)))).sum())


def ell_of_s(m, k, s):
    a, b = 0.0, lmax(m, k) * (1 - 1e-15)
    for _ in range(200):
        mid = 0.5 * (a + b)
        if Fp(m, k, mid) < s:
            a = mid
        else:
            b = mid
    return 0.5 * (a + b)


def Psi(m, k, s):
    if s <= 0:
        return 0.0
    l = ell_of_s(m, k, s)
    return s * l - F(m, k, l)


def Fstar(m, k, u, t):
    return t * Psi(m, k, u) - Psi(m, k, t * u)


def V_closed(m, k, u, e):
    P = Psi(m, k, u)
    return F(m, k, (P - e) / u) if P > e else 0.0


def N_centre(m, k, u, X):
    P = Psi(m, k, u)
    if X >= P:
        return 0.0
    ls = ell_of_s(m, k, u)
    a, b = 0.0, ls
    for _ in range(200):
        mid = 0.5 * (a + b)
        if u * mid - F(m, k, mid) <= P - X:
            a = mid
        else:
            b = mid
    return F(m, k, 0.5 * (a + b))


def sup_m(f, lo=0.002, hi=0.998, n=499):
    ms = np.linspace(lo, hi, n)
    vals = np.array([f(m) for m in ms])
    i = int(np.argmax(vals))
    v, m = golden(f, ms[max(i - 1, 0)], ms[min(i + 1, n - 1)])
    return (v, m) if v >= vals[i] else (float(vals[i]), float(ms[i]))


print("=== Section 4 of the review: thermodynamic integration on the fibre, AM-GM, curvature form ===")
worst = dict(dw=0.0, dI=0.0, ratio=math.inf, lemma=-math.inf, curv=-math.inf, psi2=0.0, gap=math.inf)
for _ in range(20000):
    p, q = rng.uniform(0.01, 0.99, 2)
    cmin, cmax = -min(p * q, (1 - p) * (1 - q)), min(p * (1 - q), (1 - p) * q)
    c = rng.uniform(cmin, cmax) * 0.999
    T = table(p, q, c)
    S, w = float((1 / T).sum()), omega(T)
    worst["ratio"] = min(worst["ratio"], S / (16 * math.cosh(w / 4) ** 2))
    worst["lemma"] = max(worst["lemma"], mi(T) - K(abs(w) / 4))
for _ in range(400):
    p, q = rng.uniform(0.05, 0.95, 2)
    cmin, cmax = -min(p * q, (1 - p) * (1 - q)), min(p * (1 - q), (1 - p) * q)
    c = rng.uniform(cmin, cmax) * 0.9
    d = 1e-6 * (cmax - cmin)
    T = table(p, q, c)
    S, w = float((1 / T).sum()), omega(T)
    worst["dw"] = max(worst["dw"], abs((omega(table(p, q, c + d)) - omega(table(p, q, c - d))) / (2 * d) - S) / S)
    worst["dI"] = max(worst["dI"], abs((mi(table(p, q, c + d)) - mi(table(p, q, c - d))) / (2 * d) - w))
for w in (0.3, 1.0, 2.5, 6.0):                                # equality at uniform marginals
    c = 0.25 * math.tanh(w / 4)
    T = table(0.5, 0.5, c)
    assert abs(omega(T) - w) < 1e-12 and abs((1 / T).sum() - 16 * math.cosh(w / 4) ** 2) < 1e-9 and abs(mi(T) - K(w / 4)) < 1e-12
print(f"  d omega/dc = S: largest relative error of a central difference {worst['dw']:.1e};  dI/dc = omega: largest error {worst['dI']:.1e}  (400 tables)")
print(f"  S / (16 cosh^2(omega/4)) over 20 000 random tables: smallest {worst['ratio']:.6f} (must be >= 1); equality checked at uniform marginals for omega = 0.3, 1, 2.5, 6")
print(f"  I - K(|omega|/4): largest {worst['lemma']:.2e} (must be <= 0)")
for _ in range(3000):
    m, k, s = rng.uniform(0.03, 0.97), rng.uniform(0.03, 0.97), rng.uniform(0.02, 5.0)
    l = ell_of_s(m, k, s)
    T = table(m, k, l / 2)
    S = float((1 / T).sum())
    assert abs(omega(T) - 2 * s) < 1e-7
    worst["curv"] = max(worst["curv"], 4 / S - 0.25 / math.cosh(s / 2) ** 2)
for _ in range(300):
    m, k, s = rng.uniform(0.1, 0.9), rng.uniform(0.1, 0.9), rng.uniform(0.2, 3.0)
    d = 1e-3
    fd = (Psi(m, k, s + d) - 2 * Psi(m, k, s) + Psi(m, k, s - d)) / d ** 2
    l = ell_of_s(m, k, s)
    S = float((1 / table(m, k, l / 2)).sum())
    worst["psi2"] = max(worst["psi2"], abs(fd - 4 / S) / (4 / S))
D = lambda m, k, s: lc(s / 2) - Psi(m, k, s)
for _ in range(2000):
    m, k, t = rng.uniform(0.03, 0.97), rng.uniform(0.03, 0.97), rng.uniform(0.02, 0.98)
    u1 = rng.uniform(0.1, 4.0)
    u2 = u1 + rng.uniform(0.05, 1.5)
    g1 = t * D(m, k, u1) - D(m, k, t * u1)
    g2 = t * D(m, k, u2) - D(m, k, t * u2)
    worst["gap"] = min(worst["gap"], min(g1, g2 - g1))
print(f"  curvature: max of Psi''_(m,kappa)(s) - Psi_c''(s) = 4/S - sech^2(s/2)/4 over 3000 random (m, kappa, s): {worst['curv']:.2e} (must be <= 0)")
print(f"  Psi'' = 4/S against a second difference of the Legendre transform (300 cases): largest relative error {worst['psi2']:.1e}")
print(f"  gap F*_c(t) - F*_(m,kappa)(t) = t D(u) - D(tu): smallest value of (gap, increment of the gap from u1 to u2 > u1) over 2000 cases: {worst['gap']:.2e} (must be >= 0)")

print("\n=== m1, m2: the optimal input of an asymmetric channel P(b, x) ~ exp(J b x + h1 b + h2 x) ===")
def ising(J, h1, h2):
    P = np.array([[math.exp(J * b * x + h1 * b + h2 * x) for x in (1, -1)] for b in (1, -1)])
    P /= P.sum()
    return P
delta = lambda J, h: 0.5 * (lc(h + J) - lc(h - J))
Tf = lambda J, h: J * (math.tanh(h + J) + math.tanh(h - J)) - 2 * delta(J, h)
Dl = lambda J, h: math.tanh(h + J) - math.tanh(h - J)
cnt = dict(n=0, tilt=0, mean=0, root=0)
w2 = wk = 0.0
for _ in range(60):
    J, h2 = rng.uniform(0.1, 2.5), rng.uniform(0.05, 3.0)
    v, h1 = golden(lambda h: mi(ising(J, h, h2)), -15.0, 15.0, tol=1e-11)
    P = ising(J, h1, h2)
    EB = float(P[0].sum() - P[1].sum())
    g = -Tf(J, h2) / Dl(J, h2)
    cnt["n"] += 1
    cnt["tilt"] += (-h2 < h1 < 0)
    cnt["mean"] += (EB > 0)
    cnt["root"] += (0 < g < delta(J, h2) < J)
    wk = max(wk, abs(delta(J, -h1) - g))                       # the maximiser solves delta(k) = g(h2), k = -h1
    d = 1e-4
    fd = (mi(ising(J, h1 + d, h2)) - 2 * mi(ising(J, h1, h2)) + mi(ising(J, h1 - d, h2))) / d ** 2
    formula = -0.5 * (1 - EB ** 2) * 0.5 * Dl(J, h1) * Dl(J, h2)   # -1/2 (1 - mu^2) delta'(h1) Delta(h2), delta' = Delta/2
    w2 = max(w2, abs(fd - formula) / abs(formula))
print(f"  {cnt['n']} channels (J in [0.1, 2.5], h2 in [0.05, 3]): optimal tilt h1* in (-h2, 0): {cnt['tilt']}/{cnt['n']};  E[B] > 0 at the optimum (the input DISTRIBUTION favours the more reliable symbol): {cnt['mean']}/{cnt['n']}")
print(f"  0 < g(h2) < delta(h2) < J (existence of the root of delta(k) = g(h2)): {cnt['root']}/{cnt['n']};  |delta(-h1*) - g(h2)| <= {wk:.1e}")
print(f"  d^2 I/dh1^2 at the maximiser against -1/2 (1 - mu^2) delta'(h1) Delta(h2): largest relative error {w2:.1e} (so the maximum is non-degenerate)")

print("\n=== m3: the closed form of Theorem 11.90(b) holds over the shells l >= 0 only ===")
m, k, u = 0.83, 0.166, 4.0
def V_ray(m, k, u, e, both, n=400001):
    lo = -min(2 * m * k, 2 * (1 - m) * (1 - k)) if both else 0.0
    l = np.linspace(lo, lmax(m, k), n)
    Fl = m * kl(k + l / (2 * m), k) + (1 - m) * kl(k - l / (2 * (1 - m)), k)
    best = 0.0
    lg = np.linspace(lo, lmax(m, k), 4001)
    Fg = m * kl(k + lg / (2 * m), k) + (1 - m) * kl(k - lg / (2 * (1 - m)), k)
    for li, Fi in zip(l[:: max(1, n // 20000)], Fl[:: max(1, n // 20000)]):
        B = (e + Fi) / u
        if B < 0:
            continue
        ok = np.abs(lg - li) <= B
        best = max(best, float(Fg[ok].min()) if ok.any() else Fi)
    return best
print(f"  (m, kappa, u) = ({m}, {k}, {u}), e = 0: closed form V_(m,kappa)(0) = {V_closed(m, k, u, 0.0):.4f};  brute force over shells l >= 0 (exits on a grid of 4001): {V_ray(m, k, u, 0.0, False):.4f};")
print(f"     brute force over the WHOLE ray: {V_ray(m, k, u, 0.0, True):.4f};  closed form of the antipodal centre V_(1-m,kappa)(0) = {V_closed(1 - m, k, u, 0.0):.4f}")

print("\n=== m4: the game form of V_(m,kappa) for negative accuracies ===")
for (m, k, u) in ((0.4, 0.3, 1.0), (0.7, 0.3, 2.0)):
    ls = ell_of_s(m, k, u)
    Fs, Fmax = F(m, k, ls), F(m, k, lmax(m, k))
    game = lambda e: max(golden(lambda t: Fstar(m, k, u, t) - t * e, 0.0, 1.0)[0], -e, 0.0)
    out = []
    for e in (-0.5 * Fs, -0.5 * (Fs + Fmax), -(Fmax + 0.05)):
        out.append(f"e = {e:+.4f}: sup over feasible shells {M.V_centre(m, k, u, e):.6f}, game form {game(e):.6f}")
    print(f"  (m, kappa, u) = ({m}, {k}, {u}): F(l*) = {Fs:.4f}, F(l_max) = {Fmax:.4f}, h(kappa) = {hb(k):.4f};  " + ";  ".join(out))

print("\n=== m5: R_unif(e) = KL((Lambda_1 + e)/u || 1/2) against the game form max_t [F*_c(t) - te] ===")
for u in (1.0, 2.0):
    L1 = math.log(2 / (1 + math.exp(-u)))
    ec, E = -K(u / 2), lc(u / 2)
    row = []
    for e in (-0.99 * L1, ec - 0.05, ec, ec + 0.05, 0.0, 0.5 * E, E, E + 0.05):
        rho = (L1 + e) / u
        klform = float(kl(rho, 0.5)) if 0 <= rho <= 1 else float("nan")
        row.append(f"e={e:+.4f}: KL {klform:.6f} / game {M.game_cube(u, e):.6f}")
    print(f"  u = {u}: -K(u/2) = {ec:.6f}, ln cosh(u/2) = {E:.6f}, -Lambda_1 = {-L1:.6f}\n     " + "\n     ".join(row))

print("\n=== m6: strict inequality R^kappa < cube for kappa != 1/2 fails for e <= -K(u/2) (game form) ===")
u = 1.0
for k in (0.3, 0.45):
    for e in (-0.3, -K(u / 2), -K(u / 2) + 0.01, -0.05, 0.0):
        r2 = M.R2(k, u, e)[0]
        print(f"  kappa = {k}, u = 1, e = {e:+.6f}: R^kappa = {r2:.9f}, cube (game form) = {M.game_cube(u, e):.9f}, difference {M.game_cube(u, e) - r2:.2e}")

print("\n=== table of Theorem 11.90 (u = 1) and m11: centre types for N^kappa(0+), the cusp at X = 0 ===")
u = 1.0
for k in (0.5, 0.45, 0.4, 0.3, 0.2, 0.1):
    R0, mR = sup_m(lambda m: V_closed(m, k, u, 0.0))
    a0, ma = sup_m(lambda m: F(m, k, ell_of_s(m, k, u)))
    print(f"  kappa = {k:4.2f}: R^kappa(0) = {R0:.6f} at m = {mR:.4f};  N^kappa(0+) = sup_m F(l*) = {a0:.6f} at m = {ma:.4f}")
for (k, X) in ((0.3, 1e-12), (0.5, 1e-9), (0.3, 1e-9)):
    a0, ma = sup_m(lambda m: F(m, k, ell_of_s(m, k, u)))
    nX = sup_m(lambda m: N_centre(m, k, u, X))[0]
    print(f"  cusp: kappa = {k}, N(0+) - N({X:g}) = {a0 - nX:.3e}  (N({X:g}) = {nX:.6f});  u sqrt(2X/F''(l*)) at the best centre = {u * math.sqrt(2 * X / (0.25 * float((1 / table(ma, k, ell_of_s(ma, k, u) / 2)).sum()))):.3e}")

print("\n=== m12: the non-adaptive function n for profiles with any number of blocks (LP over all grid laws) ===")
def gn(x, tau, xi, k, u):
    a = logit(k)
    y = np.clip(x, sig(a - (xi + tau * u) / (1 + tau)), sig(a - (xi - tau * u) / (1 + tau)))
    return (1 + tau) * kl(y, k) + tau * u * np.abs(y - x) + xi * (y - k) - tau * kl(x, k)
def lp_n(x, tau, xi, k, u, X):
    res = linprog(-gn(x, tau, xi, k, u), A_eq=[np.ones_like(x), x], b_eq=[1.0, k], bounds=(0, None), method="highs")
    return (-res.fun - tau * X, res.x) if res.status == 0 else (-math.inf, None)
x = np.linspace(0.0, 1.0, 1201)
for (k, u, X) in ((0.5, 1.0, 0.02), (0.3, 1.0, 0.01), (0.3, 2.0, 0.05), (0.7, 0.5, 0.004), (0.2, 3.0, 0.2)):
    t0 = time.time()
    n2, mb = sup_m(lambda m: N_centre(m, k, u, X))
    best = (-math.inf, 0, 0)
    for tau in np.concatenate([np.linspace(0, 3, 25), [4, 5, 7, 10, 15, 25]]):
        for xi in np.linspace(-6, 6, 37):
            v = lp_n(x, tau, xi, k, u, X)[0]
            if v > best[0]:
                best = (v, tau, xi)
    res = minimize(lambda z: -lp_n(x, abs(z[0]), z[1], k, u, X)[0], [best[1], best[2]], method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-13, "maxiter": 300})
    if -res.fun > best[0]:
        best = (-res.fun, abs(res.x[0]), res.x[1])
    rho = lp_n(x, best[1], best[2], k, u, X)[1]
    na = int((rho > 1e-9).sum())
    pu = 1 / (1 + math.exp(u))
    print(f"  kappa={k}, u={u}, X={X}: two-block sup N^kappa(X) = {n2:.9f} (m = {mb:.4f});  sup_(tau,xi)[LP - tau X] over all grid laws = {best[0]:.9f} (tau = {best[1]:.3f}, {na} atoms);  LP - two-block = {best[0] - n2:+.2e}  [{time.time() - t0:.0f} s]")
    sys.stdout.flush()
