#!/usr/bin/env python3
"""R12 item 3 — Proposition 11.113 (a sandwich of two sampleable models), written from the statement
in the theory report (export at 9408e33), before the theory division's harness block XXIV.10 was
opened.

  m_- <= E <= m_+ pointwise;  q(x) ∝ e^{-m_-} - e^{-m_+};  W = (e^{-E} - e^{-m_+})/(e^{-m_-} - e^{-m_+}).
  (a) Z(E) = Z(m_+) + (Z(m_-) - Z(m_+)) E_q W
  (b) q = law of an accepted draw of pi_{m_-} accepted with probability 1 - e^{-(m_+ - m_-)};
      acceptance rate 1 - Z(m_+)/Z(m_-)
  (c) |Z(E) - Z(m_+) - (Z(m_-) - Z(m_+)) W_hat| <= (Z(m_-) - Z(m_+)) sqrt(ln(2/delta)/(2N)) w.p. >= 1 - delta;
      plain sampling of e^{-(E - m_-)} under pi_{m_-}: half-width larger by max d / E d, d = 1 - e^{-(m_+ - m_-)}
  (d) without a hint about ln(2/delta)(e^Delta - 1)^2/(2 eps^2) evaluations, "and this order is
      necessary in the worst case over the box"; with a hint (e^Delta - 1)/eps; "the hint is worth
      the factor (e^Delta - 1)/eps".

Parts:
  1. exact enumeration on random small sandwiches: identity (a), rate (b), law of accepted draws,
     ratio of half-widths E d / max d;
  2. coverage of the bracket (c) and bias of the estimator over repetitions (simulation), and the
     EXACT coverage for two-level W (binomial) minimised over the mean;
  3. the arithmetic of the illustration (0.0605 nats; 50 000 and 1 200 evaluations);
  4. claim (d): the sample size that the plug-in estimate needs on EVERY member of the box by
     Hoeffding's Theorem 1 in its Kullback-Leibler form (valid for every [0,1]-valued W with the
     given mean; Hoeffding 1963, Theorem 1 - from memory, standard), against the count of (d);
     the exact failure probability of that sample size on two-level members (binomial); and a
     two-point lower bound (Bretagnolle-Huber, from memory) for comparison.

One command:  python3 r12_04_sandwich.py
"""
import math
import time

import numpy as np
from scipy.stats import binom

T0 = time.time()
rng = np.random.default_rng(2026112604)

print("=" * 110)
print("PART 1 — exact enumeration on random sandwiches")
print("=" * 110)
max_err_a = 0.0
max_err_rate = 0.0
rows = []
insts = []
for inst in range(200):
    n = int(rng.integers(20, 400))
    m_lo = rng.normal(0, 1.5, n)
    kind = inst % 4
    if kind == 0:      # uniform width
        width = rng.exponential(1.0, n)
    elif kind == 1:    # wide only on states that the lower model rarely visits
        width = np.where(m_lo > np.quantile(m_lo, 0.9), rng.exponential(3.0, n), rng.exponential(0.01, n))
    elif kind == 2:    # some zero-width states
        width = np.where(rng.random(n) < 0.5, 0.0, rng.exponential(0.5, n))
    else:              # narrow
        width = rng.exponential(0.05, n)
    m_hi = m_lo + width
    E = m_lo + rng.random(n) * width
    Zlo, Zhi, ZE = np.exp(-m_lo).sum(), np.exp(-m_hi).sum(), np.exp(-E).sum()
    num = np.exp(-m_lo) - np.exp(-m_hi)
    q = num / num.sum()
    with np.errstate(invalid="ignore", divide="ignore"):
        W = np.where(num > 0, (np.exp(-E) - np.exp(-m_hi)) / np.where(num > 0, num, 1.0), 0.0)
    assert np.all(W >= -1e-12) and np.all(W <= 1 + 1e-12)
    lhs = ZE
    rhs = Zhi + (Zlo - Zhi) * float(np.sum(q * W))
    max_err_a = max(max_err_a, abs(lhs - rhs) / lhs)
    pi_lo = np.exp(-m_lo) / Zlo
    d = 1 - np.exp(-(m_hi - m_lo))
    acc = float(np.sum(pi_lo * d))
    max_err_rate = max(max_err_rate, abs(acc - (1 - Zhi / Zlo)))
    law = pi_lo * d / acc
    assert np.max(np.abs(law - q)) < 1e-12
    ratio = acc / d.max()
    rows.append((kind, ratio, math.log(Zlo / Zhi)))
    insts.append((m_lo, m_hi, E, q, W, Zlo, Zhi, ZE, pi_lo, d))
print("200 random sandwiches (20-400 states, four kinds of width profile):")
print("  identity (a): largest relative error %.2e" % max_err_a)
print("  acceptance rate = 1 - Z(m+)/Z(m-): largest absolute error %.2e; law of an accepted draw = q: exact (asserted)" % max_err_rate)
for kind, name in enumerate(["uniform width", "wide where the lower model is rare", "half of the states of zero width",
                             "narrow"]):
    rr = [r[1] for r in rows if r[0] == kind]
    dd = [r[2] for r in rows if r[0] == kind]
    print("  %-36s E d / max d: min %.4f median %.4f max %.4f   (Delta = ln Z(m-)/Z(m+): median %.4f)" % (
        name, min(rr), float(np.median(rr)), max(rr), float(np.median(dd))))
print("  E d / max d <= 1 in every instance: %s" % all(r[1] <= 1 + 1e-12 for r in rows))

print()
print("=" * 110)
print("PART 2 — coverage of the bracket (c) and bias, over repetitions")
print("=" * 110)
delta = 0.05
reps = 20000
worst_cov = 1.0
worst_cov_plain = 1.0
max_bias_z = 0.0
out_of_det = 0
tot = 0
for idx in (0, 1, 2, 3, 5, 6, 9, 13, 17, 21):
    m_lo, m_hi, E, q, W, Zlo, Zhi, ZE, pi_lo, d = insts[idx]
    for N in (20, 200):
        draws = rng.choice(len(q), size=(reps, N), p=q)
        What = W[draws].mean(axis=1)
        est = Zhi + (Zlo - Zhi) * What
        half = (Zlo - Zhi) * math.sqrt(math.log(2 / delta) / (2 * N))
        cov = float(np.mean(np.abs(est - ZE) <= half))
        worst_cov = min(worst_cov, cov)
        se = float(est.std() / math.sqrt(reps))
        bias_z = abs(float(est.mean()) - ZE) / max(se, 1e-300)
        max_bias_z = max(max_bias_z, bias_z)
        out_of_det += int(np.sum((est < Zhi - 1e-12) | (est > Zlo + 1e-12)))
        tot += reps
        # plain sampling of Y = e^{-(E - m_-)} under pi_{m_-}, Hoeffding with the range max d
        draws2 = rng.choice(len(q), size=(reps, N), p=pi_lo)
        Y = np.exp(-(E - m_lo))
        est2 = Zlo * Y[draws2].mean(axis=1)
        half2 = Zlo * d.max() * math.sqrt(math.log(2 / delta) / (2 * N))
        worst_cov_plain = min(worst_cov_plain, float(np.mean(np.abs(est2 - ZE) <= half2)))
print("10 instances x N in {20, 200} x %d repetitions, delta = %g:" % (reps, delta))
print("  least coverage of the bracket (c): %.4f (required >= %.2f)" % (worst_cov, 1 - delta))
print("  largest |mean of the estimates - Z(E)| in units of its standard error: %.2f (unbiased: a few units at most)" % max_bias_z)
print("  point estimates outside the deterministic bracket [Z(m+), Z(m-)]: %d of %d" % (out_of_det, tot))
print("  least coverage of the plain-sampling Hoeffding bracket (range max d): %.4f" % worst_cov_plain)
# the bracket itself (not the point estimate) may leave the deterministic one unless clipped
m_lo, m_hi, E, q, W, Zlo, Zhi, ZE, pi_lo, d = insts[0]
N = 20
draws = rng.choice(len(q), size=(reps, N), p=q)
What = W[draws].mean(axis=1)
t = math.sqrt(math.log(2 / delta) / (2 * N))
frac_out = float(np.mean((What - t < 0) | (What + t > 1)))
print("  instance 0, N = 20: the UNCLIPPED bracket [est - half, est + half] sticks out of [Z(m+), Z(m-)] in %.1f %% of the "
      "repetitions (half-width/(Z(m-) - Z(m+)) = %.3f): 'never leaves the deterministic one' holds for the point "
      "estimate, and for the bracket only after intersection with [Z(m+), Z(m-)]" % (100 * frac_out, t))
# exact coverage for two-level W: K ~ Bin(N, w)
worst_exact = 1.0
arg = None
for N in (10, 20, 50, 200, 1000):
    t = math.sqrt(math.log(2 / delta) / (2 * N))
    ks = np.arange(N + 1)
    for w in np.linspace(0.0, 1.0, 2001):
        pm = binom.pmf(ks, N, w)
        cov = float(pm[np.abs(ks / N - w) <= t + 1e-15].sum())
        if cov < worst_exact:
            worst_exact, arg = cov, (N, float(w))
print("  exact coverage for two-level W (binomial), N in {10, 20, 50, 200, 1000}, mean on a grid of 2001: least %.5f at (N, w) = %s"
      % (worst_exact, arg))

print()
print("=" * 110)
print("PART 3 — the arithmetic of the illustration")
print("=" * 110)
Delta = 0.0605
for N in (50000, 1200):
    fac = math.sqrt(2 * math.log(2 / 0.05) / N)
    wz = (math.exp(Delta) - 1) * fac          # width of the bracket for Z in units of Z(m+)
    print("  N = %6d: sqrt(2 ln(2/delta)/N) = %.5f; width in Z / Z(m+) = %.3e; in nats <= %.3e (dividing by the lower end "
          "of the bracket, >= Z(m+)); Delta x factor = %.3e" % (N, fac, wz, wz, Delta * fac))
print("  report: 'at most 7.6e-4 nats from 50 000 samples at delta = 0.05, and 5e-3 from 1 200'")

print()
print("=" * 110)
print("PART 4 — claim (d): which sample size is necessary without a hint in the worst case over the box?")
print("=" * 110)


def kl(p, r):
    """KL(Bern(p) || Bern(r))."""
    if p <= 0:
        return -math.log(1 - r)
    if p >= 1:
        return -math.log(r)
    return p * math.log(p / r) + (1 - p) * math.log((1 - p) / (1 - r))


def n_kl(Delta, eps, delta, grid=20001):
    """Sample size N such that the plug-in estimate ln(Z(m+) + (Z(m-) - Z(m+)) W_hat) is within eps of ln Z(E)
    with probability >= 1 - delta for EVERY [0,1]-valued W, by Hoeffding's Theorem 1 (KL form) applied to both
    tails: N >= ln(2/delta)/KL(w + t_plus || w) and >= ln(2/delta)/KL(w - t_minus || w), for every mean w,
    t_plus = (e^eps - 1)(c + w), t_minus = (1 - e^-eps)(c + w), c = 1/(e^Delta - 1)."""
    c = 1 / (math.exp(Delta) - 1)
    worst = 0.0
    argw = None
    L = math.log(2 / delta)
    ws = np.concatenate([np.linspace(0, 1, grid), np.geomspace(1e-9, 1, 4000)])
    for w in ws:
        w = float(w)
        need = 0.0
        tp = (math.exp(eps) - 1) * (c + w)
        tm = (1 - math.exp(-eps)) * (c + w)
        if 0 < w < 1:
            if w + tp < 1:
                need = max(need, L / kl(w + tp, w))
            elif w + tp == 1:
                need = max(need, L / kl(1.0, w))
            if w - tm > 0:
                need = max(need, L / kl(w - tm, w))
            elif w - tm == 0:
                need = max(need, L / kl(0.0, w))
        if need > worst:
            worst, argw = need, w
    return math.ceil(worst), argw


def exact_failure_two_level(Delta, eps, N, ws):
    """Exact failure probability of the plug-in estimate with N samples on two-level members (W in {0,1},
    mean w): P(|ln(c + K/N) - ln(c + w)| > eps), K ~ Bin(N, w); maximised over the given means."""
    c = 1 / (math.exp(Delta) - 1)
    ks = np.arange(N + 1)
    est = np.log(c + ks / N)
    worst = 0.0
    for w in ws:
        pm = binom.pmf(ks, N, w)
        f = float(pm[np.abs(est - math.log(c + w)) > eps].sum())
        worst = max(worst, f)
    return worst


def bh_lower(Delta, eps, delta, grid=4000):
    """Two-point lower bound (Bretagnolle-Huber): an algorithm that is (eps, delta)-correct on two members whose
    ln Z differ by more than 2 eps, and that sees N independent evaluations at points drawn from a fine-grained q
    (two-level members, W = 1 on a random set of q-mass w or w'), needs N >= ln(1/(4 delta))/KL(Bern(w)||Bern(w'))."""
    c = 1 / (math.exp(Delta) - 1)
    best = 0.0
    for w in np.geomspace(1e-6, 0.999, grid):
        w = float(w)
        w2 = (c + w) * math.exp(2 * eps) - c
        if 0 < w2 < 1:
            best = max(best, math.log(1 / (4 * delta)) / kl(w, w2))
    return best


print("delta = 0.05.  N_H = ln(2/delta)(e^Delta-1)^2/(2 eps^2) (the count of (d));  N_KL = sufficient for every member by the "
      "KL form;\n  pred = ln(2/delta)(e^Delta-1)^2/(2 e^Delta eps^2);  LB = two-point lower bound")
print("  %6s %6s %12s %12s %12s %10s %12s %10s %s" % ("Delta", "eps", "N_H", "N_KL", "pred", "N_KL/N_H", "LB", "e^-Delta",
                                                    "worst mean w"))
for Delta in (0.0605, 0.5, 1.0, 2.0, 3.0, 5.0):
    for eps in (0.1, 0.01):
        NH = math.log(2 / delta) * (math.exp(Delta) - 1) ** 2 / (2 * eps ** 2)
        NK, argw = n_kl(Delta, eps, delta)
        pred = math.log(2 / delta) * (math.exp(Delta) - 1) ** 2 / (2 * math.exp(Delta) * eps ** 2)
        LB = bh_lower(Delta, eps, delta)
        print("  %6g %6g %12.0f %12d %12.0f %10.4f %12.0f %10.4f %s" % (
            Delta, eps, NH, NK, pred, NK / NH, LB, math.exp(-Delta),
            ("%.4g" % argw) if argw is not None else "- (Delta < eps: the deterministic bracket suffices, N = 0)"))
print("exact check on two-level members (binomial), eps = 0.1:")
for Delta in (1.0, 3.0, 5.0):
    NK, argw = n_kl(Delta, 0.1, delta)
    ws = np.concatenate([np.linspace(0.0005, 0.9995, 400), np.geomspace(1e-5, 0.5, 200)])
    f = exact_failure_two_level(Delta, 0.1, NK, ws)
    NH = math.log(2 / delta) * (math.exp(Delta) - 1) ** 2 / (2 * 0.1 ** 2)
    print("  Delta = %g: plug-in with N_KL = %d samples (N_H = %.0f): largest exact failure probability over 600 means: %.4f "
          "(delta = %g)  %s" % (Delta, NK, NH, f, delta, "OK" if f <= delta else "FAIL"))
print()
print("total elapsed %.1f s" % (time.time() - T0))
print("R12_04_DONE")
