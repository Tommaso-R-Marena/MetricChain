#!/usr/bin/env python3
"""Coordinator's checks before adopting workstream R12 (review of the theory division's seventeenth checkpoint), 2026-11-26.
Written from the statements of the two major findings; none of the workstream's code is imported.

M1 (their Proposition 11.18e(b) is false as written).  On the cube {-1,1}^n with m = 2 the class is g = h + R, h affine
    (free), |R| <= C.  Claimed by the reviewer: with q = ceil(log2(1/delta)) uniformly random evaluations,
    B = (n + 1)(max_j |g(x^j)| + C) + C bounds sup|g| with probability >= 1 - delta, for EVERY g of the class.
    (a) the lemma: for every affine h at least half of the points have |h| >= ||h||_inf/(n + 1)  -- exact enumeration on
        random, sparse and adversarial h (the extremal case h = alpha(1 + s_1), which vanishes on exactly half the cube);
    (b) end to end: the exact failure probability of the algorithm on the extremal member (it fails iff all q points
        fall where h = 0: 2^-q), and a simulation on random members with a remainder.
M2 (their Proposition 11.113(d): "(e^D - 1)^2/eps^2 is necessary").  Z(E) = Z+ (1 + a w), a = e^D - 1, w = E_q W in [0,1].
    The plug-in estimate from N samples of a two-level W (Bernoulli(w)) is off by more than eps in ln Z with a
    probability computed exactly from the binomial law; maximised over w on a grid.  With N = N_d (the count of (d))
    and with N = N_KL = ln(2/delta) (e^D - 1)^2 / (2 e^D eps^2) = 2 ln(2/delta) sinh^2(D/2)/eps^2  (the coordinator's own
    derivation: Var W <= w(1-w), relative accuracy eps of 1 + a w, worst w = 1/(a + 2)).
Run:  python3 r12_adoption_check.py > r12_adoption_check.log      (about half a minute)
"""
import math, time, itertools
import numpy as np
from scipy.stats import binom
t0 = time.time(); rng = np.random.default_rng(20261126)
def log(s): print(s, flush=True)

log("=== M1 (a): at least half of the cube has |h| >= ||h||_inf / (n + 1) for affine h")
worst = 1.0; ncase = 0
for n in (4, 6, 8, 10, 12, 14):
    S = np.array(list(itertools.product((-1.0, 1.0), repeat=n)))
    fam = []
    for _ in range(300): fam.append((rng.normal(), rng.normal(size=n)))
    for _ in range(300):                                        # sparse, heavy-tailed
        b = np.zeros(n); idx = rng.choice(n, rng.integers(1, 4), replace=False); b[idx] = rng.standard_cauchy(len(idx)); fam.append((rng.standard_cauchy(), b))
    for i in range(n):                                          # the extremal family and near-ties
        b = np.zeros(n); b[i] = 1.0; fam.append((1.0, b)); fam.append((-1.0, b)); fam.append((1.0 + 1e-9, b)); fam.append((0.0, b))
    fam.append((1.0, np.ones(n))); fam.append((0.0, np.ones(n))); fam.append((float(n), np.ones(n)))
    w_n = 1.0
    for al, be in fam:
        h = al + S @ be; sup = abs(al) + np.abs(be).sum()
        if sup == 0: continue
        frac = float((np.abs(h) >= sup / (n + 1) * (1 - 1e-12)).mean()); w_n = min(w_n, frac); ncase += 1
    worst = min(worst, w_n)
    log(f"   n = {n:2d}: {len(fam)} functions, least fraction of good points {w_n:.6f}")
log(f"   {ncase} functions in all; least fraction {worst:.6f} (the lemma says >= 0.5; 0.5 is attained by alpha(1 + s_i))")
assert worst >= 0.5

log("=== M1 (b): the counter-algorithm end to end (delta = 0.05, q = 5 random evaluations, whatever n)")
delta = 0.05; q = math.ceil(math.log2(1 / delta))
for n in (8, 12, 16):
    S = np.array(list(itertools.product((-1.0, 1.0), repeat=n)))
    # extremal member: h = 1 + s_1, no remainder: the algorithm fails iff all q points have s_1 = -1
    h = 1.0 + S[:, 0]; fail_exact = float((h == 0).mean()) ** q
    # random members with a remainder |R| <= C: simulate
    C = 0.7; trials = 20000; bad = 0
    E0 = rng.normal(size=len(S))
    for t in range(40):
        al, be = rng.standard_cauchy(), rng.standard_cauchy(n) * (rng.random(n) < 0.3)
        R = C * (2 * rng.random(len(S)) - 1); g = al + S @ be + R; sup = float(np.abs(g).max())
        idx = rng.integers(0, len(S), size=(trials // 40, q)); M = np.abs(g[idx]).max(axis=1)
        B = (n + 1) * (M + C) + C
        # valid iff sup|g| <= B (then min E0 - B <= min(E0 + g) and |ln Z(E0 + g) - ln Z(E0)| <= B)
        bad += int((B < sup).sum())
    log(f"   n = {n:2d} (N_ball = {n + 1}; claimed lower bound (1 - delta) N_ball = {(1 - delta) * (n + 1):.2f} evaluations): q = {q}; "
        f"exact failure on the extremal member 2^-{q} = {fail_exact:.5f} <= delta; random members with |R| <= {C}: invalid bound in {bad} of {trials} runs")
    assert fail_exact <= delta

log("=== M2: exact failure probability of the plug-in estimate on two-level members, worst over the mean w")
def worst_failure(D, eps, N):
    a = math.expm1(D); ws = np.concatenate([np.linspace(1e-4, 0.9999, 400), [1.0 / (a + 2.0)]]); worst = 0.0; wstar = None
    k = np.arange(N + 1)
    for w in ws:
        est = np.log1p(a * k / N); tru = math.log1p(a * w)
        pf = float(binom.pmf(k, N, w)[np.abs(est - tru) > eps].sum())
        if pf > worst: worst, wstar = pf, w
    return worst, wstar
log("   | D | eps | N_d = ln(2/delta)(e^D-1)^2/(2 eps^2) | N_KL = N_d e^-D | worst failure with N_KL | with N_KL/4 | with N_KL/16 | (delta = 0.05)")
for D, eps in ((0.0605, 0.01), (0.5, 0.02), (1.0, 0.02), (2.0, 0.05), (3.0, 0.1), (5.0, 0.2)):
    Nd = math.log(2 / delta) * math.expm1(D) ** 2 / (2 * eps * eps); Nkl = 2 * math.log(2 / delta) * math.sinh(D / 2) ** 2 / (eps * eps)
    f1, w1 = worst_failure(D, eps, max(1, round(Nkl))); f4, _ = worst_failure(D, eps, max(1, round(Nkl / 4))); f16, _ = worst_failure(D, eps, max(1, round(Nkl / 16)))
    log(f"   | {D} | {eps} | {Nd:.0f} | {Nkl:.0f} (ratio {Nkl / Nd:.4f}, e^-D = {math.exp(-D):.4f}) | {f1:.4f} (at w = {w1:.3f}; 1/(a+2) = {1 / (math.expm1(D) + 2):.3f}) | {f4:.3f} | {f16:.3f} |")
    assert f1 <= delta
log(f"ALL DONE {time.time() - t0:.0f} s")
