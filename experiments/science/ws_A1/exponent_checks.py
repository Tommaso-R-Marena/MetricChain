#!/usr/bin/env python3
"""Workstream A1 -- independent re-computation of the exponent functions of the cube class and of their
relation to the published "discrete random energy model" formulas for the Jarzynski estimator
(Suarez, Silbey, Oppenheim, Phys. Rev. E 85, 051108 (2012), arXiv:1108.5783, eqs. (39)-(46), (C4)-(C10)).

Own code; nothing imported from the theory division's scripts.

  E1  the numbers quoted in the theory report for theta_hint(0+), theta_na(0+) at several slopes;
  E2  S-S-O's bias formula  B/N = gamma ln2 + eps/(1+e^{eps_c}) - ln(2/(1+e^{-eps}))  (eps > eps_c), eps_c = logit(1-rho),
      rho = h2^{-1}(1-gamma), equals KL(rho || p_u) with u = eps, KL(rho || 1/2) = gamma ln 2;  hence the graph
      {(theta, accuracy rate)} of S-S-O is the graph of theta_na;  B_max = ln cosh(u/2);  gamma_c = 1 - h2(p_u) <-> a = KL(p_u||1/2);
  E3  the shear law at the cone:  x_na(theta) = e_hint(theta) + theta, i.e.  accuracy(nonadaptive) = accuracy(hinted) + ln(N)/n;
  E4  exact finite-n evaluation of the two lower-bound constructions (theory report Thm 11.25(a): dips at the zero
      function; Thm 11.45(b): cone against flattened cone), with exact binomial sums in log-space:
      exponents converge to theta_hint and theta_na;  replication of "0.0293 at n = 6400, u = 1, eps1 = (1/4) ln cosh(1/2), delta = 0.05";
  E5  simulation of plain Monte Carlo at the cone instance with M = e^{n theta} uniform samples (shell counts drawn
      exactly as Poisson/normal variables): the deficit  ln(A/A_hat)/n  against KL(rho_theta || p_u);
  E6  the exact one-sample bias (M = 1) equals n ln cosh(u/2) -- the threshold of Thm 11.25 is S-S-O's B_max;
  E7  mutation: a wrong identity (KL(rho||p_u) = KL(rho||1/2) + u rho - Lambda_1 with Lambda_1 replaced by u/2) must fail.
Run:  python3 exponent_checks.py     (about 1 min)
"""
import math
import sys

import numpy as np
from scipy.optimize import brentq
from scipy.special import gammaln, logsumexp

LN2 = math.log(2.0)
fails = 0


def check(name, ok, info=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + ("   " + info if info else ""))
    if not ok:
        fails += 1


def h(p):
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log(p) - (1 - p) * math.log1p(-p)


def kl(a, b):
    """binary relative entropy KL(a||b), nats"""
    out = 0.0
    if a > 0:
        out += a * math.log(a / b)
    if a < 1:
        out += (1 - a) * math.log((1 - a) / (1 - b))
    return out


def Lam1(u):
    return math.log(2.0 / (1.0 + math.exp(-u)))


def p_u(u):
    return 1.0 / (1.0 + math.exp(u))


def eps_star(u):
    return math.log(math.cosh(u / 2.0))


def theta_hint(e1, u):
    rho = (Lam1(u) + e1) / u
    return kl(rho, 0.5) if rho < 0.5 else 0.0


def rho_of_accuracy(e1, u):
    """largest rho in [p_u, 1/2] with KL(rho||p_u) <= e1"""
    pu = p_u(u)
    if kl(0.5, pu) <= e1:
        return 0.5
    if e1 <= 0:
        return pu
    return brentq(lambda r: kl(r, pu) - e1, pu, 0.5, xtol=1e-15)


def theta_na(e1, u):
    return kl(rho_of_accuracy(e1, u), 0.5)


def rho_of_budget(theta):
    """rho in (0, 1/2] with KL(rho||1/2) = theta"""
    if theta <= 0:
        return 0.5
    if theta >= LN2:
        return 0.0
    return brentq(lambda r: kl(r, 0.5) - theta, 1e-300, 0.5, xtol=1e-16)


# ------------------------------------------------------------------ E1
quoted_hint = {0.5: 0.0077, 1.0: 0.0291, 2.0: 0.0973, math.log(16): 0.156}
quoted_na = {0.5: 0.0303, 1.0: 0.1109, 2.0: 0.3278}
ok = True
rows = []
for u, q in quoted_hint.items():
    v = theta_hint(0.0, u)
    rows.append("u=%.4g: h=%.5f (report %.4g)" % (u, v, q))
    ok &= abs(v - q) < 6e-4
for u, q in quoted_na.items():
    v = kl(p_u(u), 0.5)
    rows.append("u=%.4g: a=%.5f (report %.4g)" % (u, v, q))
    ok &= abs(v - q) < 6e-5
check("E1  theta_hint(0+) and theta_na(0+) agree with the numbers in the theory report", ok, "; ".join(rows))
ok = all(abs(Lam1(u) + eps_star(u) - u / 2) < 1e-14 and abs(kl(0.5, p_u(u)) - eps_star(u)) < 1e-14
         for u in (0.1, 0.5, 1, 2, 5))
check("E1b Lambda_1 + ln cosh(u/2) = u/2  and  KL(1/2 || p_u) = ln cosh(u/2)", ok)
ratio = [theta_na(0.0, u) / theta_hint(0.0, u) for u in (0.01, 0.1, 1.0)]
check("E1c a/h -> 4 as u -> 0", abs(ratio[0] - 4) < 0.02, "a/h at u=0.01, 0.1, 1: %.4f, %.4f, %.4f" % tuple(ratio))


# ------------------------------------------------------------------ E2
def sso_bias_per_N(gamma, eps):
    """Suarez-Silbey-Oppenheim eq. (43): bias of the Jarzynski estimator, binomial work, M = 2^{gamma N}."""
    if gamma >= 1:
        return 0.0
    # rho = h2^{-1}(1-gamma) in [0, 1/2]  (entropy in bits)
    rho = brentq(lambda r: h(r) / LN2 - (1 - gamma), 1e-300, 0.5, xtol=1e-16)
    eps_c = math.log((1 - rho) / rho)
    if eps <= eps_c:
        return 0.0
    return gamma * LN2 + eps / (1.0 + math.exp(eps_c)) - math.log(2.0 / (1.0 + math.exp(-eps)))


maxdiff = 0.0
for u in (0.3, 1.0, 2.0, 4.0):
    for gamma in np.linspace(0.0005, 0.9995, 400):
        theta = gamma * LN2
        rho = rho_of_budget(theta)
        mine = kl(rho, p_u(u)) if rho > p_u(u) else 0.0
        maxdiff = max(maxdiff, abs(mine - sso_bias_per_N(gamma, u)))
check("E2  S-S-O bias curve (their eq. 43)  ==  KL(rho_theta || p_u),  KL(rho_theta || 1/2) = theta = gamma ln 2",
      maxdiff < 1e-10, "max difference over 1600 (u, gamma) = %.2e" % maxdiff)
# inverse reading: theta_na(e1) is the budget at which the S-S-O bias equals e1
maxdiff = 0.0
for u in (0.5, 1.0, 2.0):
    for frac in (0.02, 0.1, 0.25, 0.5, 0.9):
        e1 = frac * eps_star(u)
        th = theta_na(e1, u)
        maxdiff = max(maxdiff, abs(sso_bias_per_N(th / LN2, u) - e1))
check("E2b theta_na(e1) is the inverse of the S-S-O bias curve", maxdiff < 1e-9, "max |B(theta_na(e1)) - e1| = %.1e" % maxdiff)
ok = all(abs(sso_bias_per_N(1e-13, u) - eps_star(u)) < 1e-6 for u in (0.5, 1, 2, 4))
check("E2c S-S-O B_max (M = 1) = ln cosh(u/2) = threshold of Theorem 11.25", ok)
ok = all(abs((1 - h(p_u(u)) / LN2) * LN2 - kl(p_u(u), 0.5)) < 1e-14 for u in (0.5, 1, 2, 4))
check("E2d S-S-O gamma_c(eps) ln 2 = KL(p_u || 1/2) = a  (also Chatterjee-Diaconis Thm 3.4: q = p(0)-p(u)+u p'(u))", ok)
# Chatterjee-Diaconis q(beta) with p(beta) = ln(1+e^{-beta}) (per site, H = Hamming distance to the centre), beta0 = 0
okcd = True
for u in (0.5, 1, 2, 4):
    p = lambda b: math.log(1 + math.exp(-b))
    dp = -1.0 / (1.0 + math.exp(u))
    q = p(0.0) - p(u) - (0.0 - u) * dp
    okcd &= abs(q - kl(p_u(u), 0.5)) < 1e-14
check("E2e Chatterjee-Diaconis q(u) = KL(p_u || 1/2)", okcd)

# ------------------------------------------------------------------ E3
maxdiff = 0.0
for u in (0.5, 1.0, 2.0):
    for theta in np.linspace(1e-4, kl(p_u(u), 0.5) * 0.999, 200):
        rho = rho_of_budget(theta)
        x_na = kl(rho, p_u(u))          # accuracy rate certified by e^{n theta} non-adaptive points
        e_hint = u * rho - Lam1(u)      # accuracy rate certified with a hint / adaptively by e^{n theta} points
        maxdiff = max(maxdiff, abs(x_na - (e_hint + theta)))
        # consistency with theta_hint: theta_hint(e_hint) = theta when e_hint >= 0
        if e_hint > 0:
            maxdiff = max(maxdiff, abs(theta_hint(e_hint, u) - theta))
check("E3  shear law: x_na(theta) = e_hint(theta) + theta  (accuracy_nonadaptive = accuracy_adaptive + ln N / n)",
      maxdiff < 1e-10, "max deviation %.1e" % maxdiff)


# ------------------------------------------------------------------ E4  (exact finite n, log-space)
def log_binom_row(n):
    j = np.arange(n + 1)
    return gammaln(n + 1) - gammaln(j + 1) - gammaln(n - j + 1)


def finite_n(n, u, e1, delta=0.05):
    lb = log_binom_row(n)
    j = np.arange(n + 1)
    logcum = np.logaddexp.accumulate(lb)          # log |B(k)|
    eps = e1 * n
    # (i) hinted lower bound: least k with Delta_k > eps;  e^{Delta_k} - 1 = 2^{-n} sum_{j<=k} C(n,j)(e^{u(k+1-j)} - 1)
    kstar = None
    for k in range(0, n):
        jj = j[: k + 1]
        xx = u * (k + 1 - jj)                      # > 0
        terms = lb[: k + 1] + xx + np.log1p(-np.exp(-xx))   # log(C(n,j)) + log(e^x - 1), overflow-free
        log_excess = logsumexp(terms) - n * LN2
        Delta = np.logaddexp(0.0, log_excess)
        if Delta > eps:
            kstar = k
            break
    hint_exp = (math.log(1 - 2 * delta) + n * LN2 - logcum[kstar]) / n
    # (ii) non-adaptive lower bound: least R with D_R > eps;  D_R = n ln(1+e^{-u}) - ln sum_j C(n,j) e^{-u max(j,R)}
    base = n * math.log1p(math.exp(-u))
    # D_R is nondecreasing in R; the strongest bound 2^n/|B(R-1)| comes from the LEAST R with D_R > eps
    Rbest = None
    for R in range(1, n + 1):
        D = base - logsumexp(lb - u * np.maximum(j, R))
        if D > eps:
            Rbest = R
            break
    na_exp = (math.log(1 - 2 * delta) + n * LN2 - logcum[Rbest - 1]) / n
    return hint_exp, na_exp, kstar, Rbest


u, e1 = 1.0, 0.25 * eps_star(1.0)
lim_h, lim_na = theta_hint(e1, u), theta_na(e1, u)
rows = []
prev = None
for n in (200, 800, 3200, 6400):
    he, ne, ks, Rb = finite_n(n, u, e1)
    rows.append("n=%d: hinted %.4f, non-adaptive %.4f" % (n, he, ne))
    last = (he, ne)
check("E4  finite-n lower bounds converge to theta_hint = %.4f and theta_na = %.4f (u=1, eps1 = (1/4) ln cosh(1/2))" % (lim_h, lim_na),
      abs(last[0] - lim_h) < 2e-3 and abs(last[1] - lim_na) < 2e-3, "; ".join(rows))
check("E4b replication of the theory report's '0.0293 at n = 6400' (non-adaptive lower bound, delta = 0.05; limit 0.0283)",
      abs(last[1] - 0.0293) < 2e-4 and abs(lim_na - 0.0283) < 1e-4, "mine: %.5f, limit %.5f" % (last[1], lim_na))

# ------------------------------------------------------------------ E5  simulation of plain MC at the cone
rng = np.random.default_rng(7)


def simulate_deficit(n, u, theta, reps=40):
    lb = log_binom_row(n)
    j = np.arange(n + 1)
    logp = lb - n * LN2
    logM = n * theta
    logA = n * math.log((1 + math.exp(-u)) / 2.0)
    lam_log = logM + logp
    out = []
    for _ in range(reps):
        cnt_log = np.full(n + 1, -np.inf)
        small = lam_log < math.log(1e6)
        lam_small = np.exp(np.minimum(lam_log[small], math.log(1e6)))
        c = rng.poisson(lam_small).astype(float)
        with np.errstate(divide="ignore"):
            cnt_log[small] = np.log(c)
        big = ~small
        # normal approximation of a Poisson count, in log-space: N = lam (1 + z / sqrt(lam))
        z = rng.standard_normal(big.sum())
        cnt_log[big] = lam_log[big] + np.log1p(np.clip(z * np.exp(-0.5 * lam_log[big]), -0.999, None))
        logAhat = logsumexp(cnt_log - u * j) - logM
        out.append((logA - logAhat) / n)
    return float(np.mean(out)), float(np.std(out))


rows, ok = [], True
u = 1.0
a = kl(p_u(u), 0.5)
for frac in (0.25, 0.5, 0.75):
    theta = frac * a
    target = kl(rho_of_budget(theta), p_u(u))
    vals = []
    for n in (500, 2000, 8000, 32000):
        m, s = simulate_deficit(n, u, theta)
        vals.append(m)
    rows.append("theta=%.2fa: deficit/n = %s -> predicted %.5f" % (frac, ", ".join("%.5f" % v for v in vals), target))
    ok &= abs(vals[-1] - target) < 6e-4 and abs(vals[-1] - target) < abs(vals[0] - target)
check("E5  plain Monte Carlo at the cone with e^{n theta} samples: ln(A/A_hat)/n -> KL(rho_theta || p_u)  (n = 500..32000)",
      ok, " | ".join(rows))
m, s = simulate_deficit(8000, u, 1.3 * a)
check("E5b above the budget a the deficit vanishes", abs(m) < 2e-4, "deficit/n at theta = 1.3a, n = 8000: %.2e" % m)

# ------------------------------------------------------------------ E6
ok = True
for n, u in ((50, 1.0), (400, 0.7), (3000, 2.0)):
    # one uniform sample: E[-ln w] - (-ln A) = u n/2 + n ln((1+e^{-u})/2) = n ln cosh(u/2)
    bias = u * n / 2 + n * math.log((1 + math.exp(-u)) / 2)
    ok &= abs(bias - n * eps_star(u)) < 1e-9 * n
check("E6  exact bias of the one-sample estimate at the cone = n ln cosh(u/2)", ok)

# ------------------------------------------------------------------ E7  mutation
bad = max(abs(kl(r, p_u(1.0)) - (kl(r, 0.5) + 1.0 * r - 0.5)) for r in (0.2, 0.3, 0.4))
good = max(abs(kl(r, p_u(1.0)) - (kl(r, 0.5) + 1.0 * r - Lam1(1.0))) for r in (0.2, 0.3, 0.4))
check("E7  identity KL(rho||p_u) = KL(rho||1/2) + u rho - Lambda_1 holds; with Lambda_1 -> u/2 it fails (mutation detected)",
      good < 1e-14 and bad > 1e-2, "true identity residual %.1e, mutated residual %.3f" % (good, bad))

print("\nfailures: %d" % fails)
sys.exit(1 if fails else 0)
