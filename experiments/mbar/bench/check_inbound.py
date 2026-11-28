"""Division 9 -- numerical checks of statements received from the other Phase II divisions after our
first message (THY-MSG-0024, THY-MSG-0025, HIE-MSG-0003, ENG-MSG-0011), and of the statements with which
we answer them (MBAR-MSG-0003).  Exact computations on finite supports, or one-dimensional quadrature.
Nothing here verifies a proof of another division; each item says what is computed.

  I1  THY-MSG-0024 section 2.4: the three-state instance with lazy chains; variance of MBAR on the raw
      samples at s, (s+t)/2, t (not quasi-convex) and of the weighted estimator V_c(s/C).
  I2  THY-MSG-0024 section 2.5: s_i s_j BC_ij^2 / sum(s) <= -L_ij(s) <= int min(s_i p_i, s_j p_j), and the
      resulting bound on effective resistances (Rayleigh).
  I3  THY-MSG-0025 section 2: V_c(s) >= (f_L - f_0)^2 / max_k f_k (1 - f_k) for indicator test functions
      (a corollary of our dual formula A2).
  I4  ENG-MSG-0011, Proposition M2: a shared energy error d(x) in [-eps, eps] moves f_j - f_i by at most
      ln(1 + (e^{2 eps} - 1) TV(p_i, p_j)).
  I5  HIE-MSG-0003 sections 2.3, 2.4: the half-space identity of the Gaussian cap, and ln(Z_B/Z_A).
  I6  our answer to ENG question (a): the region of Theorem B2 lies between two sets described by the
      Hessian H at the minimiser, with a certified remainder:
      omega_-(osc d) d.H.d <= Phi(fhat + d) - Phi(fhat) <= omega_+(osc d) d.H.d,
      omega_-(r) = (exp(-r) + r - 1)/r^2,  omega_+(r) = (exp(r) - r - 1)/r^2.
  I7  our answer to ENG question (d): the effective resistance R_c(s) = c.L(s)^+.c is convex in s.
"""
import json
import os
import sys

import numpy as np
from scipy import integrate
from scipy.special import logsumexp, ndtr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
from d9mbar import population as pop          # noqa: E402
from d9mbar.estimators import mbar            # noqa: E402

rng = np.random.default_rng(20261128)
report = {}


def random_model(K, J, zero=0.0):
    while True:
        P = rng.dirichlet(np.ones(J) * rng.uniform(0.3, 2.0), size=K)
        if zero:
            P = np.where(rng.random((K, J)) < zero, 0.0, P)
        if np.all(P.sum(axis=1) > 0):
            P = P / P.sum(axis=1, keepdims=True)
            if np.all((P > 0).any(axis=0)):
                return P


def potentials(P, s, c):
    """v = L(s)^+ c and z = sum_k pi_k v_k on the support (s > 0)."""
    m = s @ P
    pi = (s[:, None] * P) / m
    L = np.diag(s) - (pi * m) @ pi.T
    v = np.linalg.pinv(L) @ c
    return v, pi.T @ v, L


def state_var(P, z):
    mu = P @ z
    return P @ (z ** 2) - mu ** 2


# ---------------------------------------------------------------- I1
P = np.array([[0.0344, 0.8010, 0.1182, 0.0463],
              [0.4817, 0.3260, 0.1709, 0.0215],
              [0.2941, 0.0319, 0.2172, 0.4568]])
P = P / P.sum(axis=1, keepdims=True)
C = np.array([1.706, 135.105, 1.053])
c = np.array([-1.0, 1.0, 0.0])
s = np.array([0.2047, 0.0295, 0.7658])
t = np.array([0.2387, 0.6463, 0.1149])


def F_raw(sv):
    v, z, _ = potentials(P, sv, c)
    return float(np.sum(C * sv * state_var(P, z)))


def V_weighted(sv):
    return float(pop.variance(P, sv / C, pop.contrast_measure(P, c)))


vals = [F_raw(s), F_raw((s + t) / 2), F_raw(t)]
wvals = [V_weighted(s), V_weighted((s + t) / 2), V_weighted(t)]
report["I1"] = dict(F_raw=vals, reported_raw=[69.00, 183.78, 163.95], V_weighted=wvals,
                    reported_weighted=[6.15, 7.90, 13.04],
                    midpoint_exceeds_both_ends=bool(vals[1] > max(vals[0], vals[2])))
print("I1 raw MBAR under lazy chains at s, mid, t:", [round(x, 2) for x in vals], "(reported 69.00, 183.78, 163.95)")
print("   weighted estimator V_c(s/C):", [round(x, 2) for x in wvals], "(reported 6.15, 7.90, 13.04)")
assert vals[1] > max(vals[0], vals[2])
assert max(abs(a - b) / b for a, b in zip(vals, [69.00, 183.78, 163.95])) < 5e-3
assert max(abs(a - b) / b for a, b in zip(wvals, [6.15, 7.90, 13.04])) < 5e-3
# convexity of the weighted variance along the same segment
g = np.linspace(0, 1, 41)
w = np.array([V_weighted((1 - a) * s + a * t) for a in g])
chord = (1 - g) * w[0] + g * w[-1]
assert np.all(w <= chord * (1 + 1e-10))

# ---------------------------------------------------------------- I2
worst_lo, worst_hi, worst_res = np.inf, np.inf, 0.0
for _ in range(300):
    K, J = int(rng.integers(2, 6)), int(rng.integers(3, 14))
    Pm = random_model(K, J, zero=rng.choice([0.0, 0.3]))
    sv = rng.dirichlet(np.ones(K)) * rng.uniform(0.5, 3.0)
    m = sv @ Pm
    pi = (sv[:, None] * Pm) / m
    L = np.diag(sv) - (pi * m) @ pi.T
    cond = np.zeros((K, K))
    for i in range(K):
        for j in range(i + 1, K):
            bc = np.sum(np.sqrt(Pm[i] * Pm[j]))
            lo = sv[i] * sv[j] * bc ** 2 / sv.sum()
            hi = np.sum(np.minimum(sv[i] * Pm[i], sv[j] * Pm[j]))
            worst_lo = min(worst_lo, -L[i, j] - lo)
            worst_hi = min(worst_hi, hi + L[i, j])
            cond[i, j] = cond[j, i] = lo
    Lbc = np.diag(cond.sum(axis=1)) - cond
    # connected pairs only
    if np.linalg.matrix_rank(Lbc, tol=1e-12) == K - 1:
        Lp, Lbp = np.linalg.pinv(L), np.linalg.pinv(Lbc)
        for i in range(K):
            for j in range(i + 1, K):
                e = np.zeros(K); e[i], e[j] = 1.0, -1.0
                worst_res = max(worst_res, (e @ Lp @ e) / (e @ Lbp @ e))
report["I2"] = dict(min_slack_lower=float(worst_lo), min_slack_upper=float(worst_hi),
                    max_resistance_over_bc_network=float(worst_res))
print("I2 min slack of the two inequalities:", worst_lo, worst_hi, "| max R(L)/R(BC network):", round(worst_res, 4))
assert worst_lo > -1e-12 and worst_hi > -1e-12 and worst_res <= 1 + 1e-9

# ---------------------------------------------------------------- I3
worst = np.inf
for _ in range(400):
    K, J = int(rng.integers(2, 7)), int(rng.integers(3, 14))
    Pm = random_model(K, J)
    sv = rng.dirichlet(np.ones(K))
    i, j = rng.choice(K, size=2, replace=False)
    cc = np.zeros(K); cc[i], cc[j] = -1.0, 1.0
    V = pop.variance(Pm, sv, pop.contrast_measure(Pm, cc))
    a = (rng.random(J) < 0.5).astype(float)
    f = Pm @ a
    den = np.max(f * (1 - f))
    if den > 1e-12:
        worst = min(worst, V / ((f[j] - f[i]) ** 2 / den) if abs(f[j] - f[i]) > 1e-9 else np.inf)
report["I3"] = dict(min_V_over_indicator_bound=float(worst))
print("I3 min V_c(s) / [(f_j - f_i)^2 / max_k f_k(1-f_k)]:", round(worst, 4), "(must be >= 1)")
assert worst >= 1 - 1e-9

# ---------------------------------------------------------------- I4
worst, tight = 0.0, 0.0
for _ in range(400):
    J = int(rng.integers(3, 14))
    Pm = random_model(2, J)
    eps = rng.uniform(0.05, 1.5)
    tv = 0.5 * np.abs(Pm[0] - Pm[1]).sum()
    bound = np.log1p((np.exp(2 * eps) - 1) * tv)
    # true densities q e^{-d}: the change of f_1 - f_0 is -ln( E_1 e^{-d} / E_0 e^{-d} )
    for trial in range(6):
        if trial == 0:      # extremal: d = -eps where p_1 > p_0, +eps elsewhere
            d = np.where(Pm[1] > Pm[0], -eps, eps)
        else:
            d = rng.uniform(-eps, eps, size=J)
        change = abs(np.log((Pm[1] @ np.exp(-d)) / (Pm[0] @ np.exp(-d))))
        worst = max(worst, change / bound)
        if trial == 0:
            tight = max(tight, change / bound)
report["I4"] = dict(max_change_over_bound=float(worst), max_ratio_at_two_level_error=float(tight))
print("I4 shared error: max |change| / ln(1 + (e^{2eps}-1) TV):", round(worst, 4), "(two-level errors reach", round(tight, 4), ")")
assert worst <= 1 + 1e-9

# ---------------------------------------------------------------- I5
# (exponents are combined before exponentiation and upper tails are taken as ndtr(-x): no overflow, no
# cancellation)
errs = []
for Lc, tt in ((1.0, 0.5), (2.0, 1.0), (3.0, 4.0), (0.5, 2.0)):
    lhs = integrate.quad(lambda x: np.exp(Lc * (x - tt) - 0.5 * x * x) / np.sqrt(2 * np.pi), tt, tt + Lc + 40,
                         epsabs=0, epsrel=1e-12)[0]
    rhs = np.exp(Lc * Lc / 2 - Lc * tt) * ndtr(Lc - tt)
    errs.append(abs(lhs - rhs) / rhs)
gaps, gaps_closed = {}, {}
for Lc in (3.0, 4.0, 6.0, 8.0):
    # Z_B = E exp(L x_+),  Z_A = E exp(L min(x_+, L)); both divided by exp(L^2/2) to stay in range
    f = lambda x: np.exp(-0.5 * (x - Lc) ** 2) / np.sqrt(2 * np.pi)   # noqa: E731  exp(Lx) phi(x) exp(-L^2/2)
    zb = 0.5 * np.exp(-Lc * Lc / 2) + integrate.quad(f, 0, Lc + 40, points=[Lc], epsabs=0, epsrel=1e-12)[0]
    za = 0.5 * np.exp(-Lc * Lc / 2) + integrate.quad(f, 0, Lc, epsabs=0, epsrel=1e-12)[0] + np.exp(Lc * Lc / 2) * ndtr(-Lc)
    gaps[str(Lc)] = float(np.log(zb / za))
    zb_c = 0.5 * np.exp(-Lc * Lc / 2) + ndtr(Lc)
    za_c = 0.5 * np.exp(-Lc * Lc / 2) + (0.5 - ndtr(-Lc)) + np.exp(Lc * Lc / 2) * ndtr(-Lc)
    gaps_closed[str(Lc)] = float(np.log(zb_c / za_c))
report["I5"] = dict(half_space_identity_max_rel_error=float(max(errs)), ln_ZB_over_ZA=gaps, ln_ZB_over_ZA_closed_form=gaps_closed,
                    reported=dict(zip(("3.0", "4.0", "6.0", "8.0"), (0.473, 0.520, 0.571, 0.599))))
print("I5 Gaussian cap, half-space identity rel. error:", max(errs), "| ln(Z_B/Z_A):", {k: round(v, 3) for k, v in gaps.items()},
      "(reported 0.473, 0.520, 0.571, 0.599)")
assert max(errs) < 1e-9
assert all(abs(gaps[k] - gaps_closed[k]) < 1e-9 for k in gaps)
assert all(abs(gaps[k] - r) < 1e-3 for k, r in zip(("3.0", "4.0", "6.0", "8.0"), (0.473, 0.520, 0.571, 0.599)))

# ---------------------------------------------------------------- I6
omega = lambda r: (np.exp(-r) + r - 1) / r ** 2 if r > 1e-6 else 0.5 - r / 6   # noqa: E731
omega_up = lambda r: (np.exp(r) - r - 1) / r ** 2 if r > 1e-6 else 0.5 + r / 6   # noqa: E731
worst, worst_up, n_dir = np.inf, 0.0, 0
for _ in range(60):
    K, J = int(rng.integers(2, 6)), int(rng.integers(4, 12))
    Pm = random_model(K, J)
    n = rng.integers(8, 60, size=K)
    xs = np.concatenate([rng.choice(J, size=n[k], p=Pm[k]) for k in range(K)])
    y = np.repeat(np.arange(K), n)
    with np.errstate(divide="ignore"):
        U = -np.log(Pm[:, xs].T)
    try:
        fhat, info = mbar(U, y)
    except (RuntimeError, ValueError):
        continue
    N = len(y)
    A = np.log(n / N)[None, :] - U
    A = A - A[np.arange(N), y][:, None]

    def Phi(f):
        return float(np.sum(logsumexp(A + f, axis=1) - f[y]))

    Z = A + fhat
    p = np.exp(Z - logsumexp(Z, axis=1)[:, None])
    H = np.diag(p.sum(axis=0)) - p.T @ p
    base = Phi(fhat)
    for _ in range(40):
        d = rng.normal(size=K) * rng.choice([0.1, 1.0, 5.0, 20.0])
        d -= d.mean()
        r = d.max() - d.min()
        lhs = Phi(fhat + d) - base
        rhs = omega(r) * (d @ H @ d)
        if rhs > 1e-9:
            worst = min(worst, lhs / rhs)
            n_dir += 1
            if r < 50:      # the upper bound is astronomically large beyond; skip to stay in range
                worst_up = max(worst_up, lhs / (omega_up(r) * (d @ H @ d)))
report["I6"] = dict(directions=n_dir, min_ratio_of_increase_to_lower_curvature_bound=float(worst),
                    max_ratio_of_increase_to_upper_curvature_bound=float(worst_up))
print("I6 region between two sets with a certified remainder, over", n_dir, "directions: min increase / [omega_-(osc d) d.H.d] =",
      round(worst, 4), "(must be >= 1); max increase / [omega_+(osc d) d.H.d] =", round(worst_up, 4), "(must be <= 1)")
assert worst >= 1 - 1e-6 and worst_up <= 1 + 1e-6

# ---------------------------------------------------------------- I7
worst = -np.inf
for _ in range(400):
    K, J = int(rng.integers(2, 6)), int(rng.integers(3, 12))
    Pm = random_model(K, J)
    cc = rng.normal(size=K); cc -= cc.mean()
    s1, s2 = rng.dirichlet(np.ones(K)), rng.dirichlet(np.ones(K))
    a = rng.uniform(0.1, 0.9)

    def R(sv):
        _, _, L = potentials(Pm, sv, cc)
        return float(cc @ np.linalg.pinv(L) @ cc)

    mid, ch = R(a * s1 + (1 - a) * s2), a * R(s1) + (1 - a) * R(s2)
    worst = max(worst, (mid - ch) / ch)
report["I7"] = dict(max_relative_convexity_defect_of_resistance=float(worst))
print("I7 effective resistance R_c(s): largest (R(mix) - chord)/chord over 400 segments:", worst, "(must be <= 0)")
assert worst <= 1e-9

with open(os.path.join(HERE, "..", "results", "inbound_checks.json"), "w") as fh:
    json.dump(report, fh, indent=1)
print("ALL INBOUND CHECKS PASSED")
