#!/usr/bin/env python3
"""The odds-ratio lemma (theory report, Lemma 11.89): every step of the proof, numerically.

Spins b, x = +-1, P(b, x) ~ exp(J b x + h1 b + h2 x), J > 0.  I(h1, h2) = mutual information.
(1) information density  iota = J b x - delta(h2) b - delta(h1) x + const,  delta(h) = (1/2) ln[cosh(h+J)/cosh(h-J)]
(2) dI/dh1 = Cov(iota, B) = (1/2)(1 - mu^2) [T(h2) - delta(h1) Delta(h2)],
    T(h) = J[tanh(h+J) + tanh(h-J)] - 2 delta(h),  Delta(h) = tanh(h+J) - tanh(h-J)
(3) T(h) < 0 for h > 0
(4) -T(h) < delta(h) Delta(h) for h > 0   <=>   X ln(Y/X) < (1-Y) ln((1-X)/(1-Y)),  X = 1/(1+e^{2(h+J)}), Y = 1/(1+e^{2(h-J)})
(5) capacity C(h2) = max_h1 I is decreasing in h2 > 0; the optimal h1 = -k with 0 < k < h2
(6) conclusion: I(h1, h2) <= I(0, 0) = ln 2 - h(sigma(2J))"""
import numpy as np
from scipy.optimize import minimize_scalar, brentq
rng = np.random.default_rng(11)
def table(J, h1, h2):
    P = np.array([[np.exp(J*b*x + h1*b + h2*x) for x in (1, -1)] for b in (1, -1)]); return P/P.sum()
def MI(J, h1, h2):
    P = table(J, h1, h2); pb = P.sum(1, keepdims=True); px = P.sum(0, keepdims=True)
    return float((P*np.log(P/(pb*px))).sum())
delta = lambda J, h: 0.5*(np.log(np.cosh(h + J)) - np.log(np.cosh(h - J)))
T = lambda J, h: J*(np.tanh(h + J) + np.tanh(h - J)) - 2*delta(J, h)
Delta = lambda J, h: np.tanh(h + J) - np.tanh(h - J)
# (1), (2)
w1 = w2 = 0
for _ in range(300):
    J, h1, h2 = rng.uniform(0.05, 2.5), rng.uniform(-3, 3), rng.uniform(-3, 3)
    P = table(J, h1, h2); pb = P.sum(1); px = P.sum(0)
    iota = np.log(P/np.outer(pb, px))
    bs = np.array([1, -1]); model = J*np.outer(bs, bs) - delta(J, h2)*bs[:, None] - delta(J, h1)*bs[None, :]
    d = iota - model; w1 = max(w1, d.max() - d.min())
    mu = pb[0] - pb[1]
    formula = 0.5*(1 - mu**2)*(T(J, h2) - delta(J, h1)*Delta(J, h2))
    eps = 1e-5; fd = (MI(J, h1 + eps, h2) - MI(J, h1 - eps, h2))/(2*eps)
    w2 = max(w2, abs(fd - formula))
print(f"(1) iota - [J b x - delta(h2) b - delta(h1) x] is constant: largest oscillation {w1:.1e}")
print(f"(2) dI/dh1 against the formula: largest difference {w2:.1e} (central differences, step 1e-5)")
# (3), (4)
J = rng.uniform(1e-3, 6, 200000); h = rng.uniform(1e-3, 6, 200000)
print(f"(3) largest T(h) over 2e5 pairs (h, J > 0): {T(J, h).max():.2e}  (< 0)")
X = 1/(1 + np.exp(2*(h + J))); Y = 1/(1 + np.exp(2*(h - J)))
lhs = X*np.log(Y/X); rhs = (1 - Y)*(np.log1p(-X) - np.log1p(-Y))
star = -T(J, h) - delta(J, h)*Delta(J, h)
# the reduction: star has the sign of lhs - rhs; exact identity  star = (alpha+1)(beta+1)... check by ratio
alpha, beta = np.exp(2*(h + J)), np.exp(2*(h - J))
ident = (alpha*beta + 2*beta + 1)*np.log((alpha + 1)/(beta + 1)) - beta*(alpha + 1)*np.log(alpha/beta)     # < 0 claimed
pref = (alpha + 1)*(beta + 1)
sel = (h + J) < 8          # beyond this the left side is below rounding
print(f"(4) largest (lhs - rhs)/rhs of the kernel inequality: {((lhs - rhs)/rhs).max():.2e}  (< 0);   (*) = identity/prefactor: largest relative mismatch "
      f"{np.abs(star[sel] - ident[sel]/pref[sel]).max()/np.abs(star[sel]).max():.1e}")
t = rng.uniform(1e-6, 1, 100000); W = rng.uniform(1e-6, 1, 100000)
gp = np.log(t/(t + W)) + W/(t + W)
print(f"    g_W'(t) = ln(t/(t+W)) + W/(t+W): largest value {gp.max():.2e}  (< 0)")
# (5)
ok = True; wk = 0
for J0 in (0.2, 0.7, 1.5, 3.0):
    prev = None
    for h2 in np.linspace(0.0, 5.0, 26):
        r = minimize_scalar(lambda h1: -MI(J0, h1, h2), bounds=(-12, 12), method="bounded", options={"xatol": 1e-11})
        C, h1s = -r.fun, r.x
        if h2 > 0:
            k = -h1s
            ok &= (0 < k < h2 + 1e-6)
            # stationarity: delta(h1*) = T(h2)/Delta(h2)
            wk = max(wk, abs(delta(J0, h1s) - T(J0, h2)/Delta(J0, h2)))
        if prev is not None: ok &= (C < prev + 1e-13)
        prev = C
print(f"(5) capacity decreasing in the field and 0 < k < h2 at the optimal input (4 couplings, 25 fields): {ok};  stationarity residual {wk:.1e}")
# (6)
w = -1
h2f = lambda p: -p*np.log(p) - (1 - p)*np.log(1 - p)
for _ in range(200000 // 200):
    J0 = rng.uniform(0.01, 3); hh = rng.uniform(-4, 4, (200, 2))
    sym = np.log(2) - h2f(1/(1 + np.exp(-2*J0)))
    w = max(w, max(MI(J0, a, b) for a, b in hh) - sym)
print(f"(6) largest I(h1, h2) - I(0, 0) over 2e5 tables: {w:.2e}  (<= 0)")
