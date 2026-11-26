#!/usr/bin/env python3
"""(version 2.  In v1 the control M2 was taken over the same random instances as M1 and did not react (0 failures of the
one-average bound among random mixtures with random residuals: the residuals were not aligned with the modes) - a control
that could not fail is no control: own error E5; log logs/item2d_mixture_sandwich_20261126T181040Z.log, "TOTAL violations: 1".
v2 adds a designed family for M2: two components Bernoulli(a)^n and Bernoulli(1-a)^n, Delta = |x|.)

R23 Item 2, last part: the 'positive fact' of the synthesis §6 that looks most consequential - the K-component
sandwich for mixture references (AA1 entry E7, S2(D)); written before reading the audit's S2 code.

Claim: if the reference is mu0 = sum_k w_k mu_k with every mu_k a PRODUCT measure on X = prod_i S_i, and the residual
Delta has bounded differences c_i on X, then with m_k = E_{mu_k} Delta
        ln sum_k w_k e^{-beta m_k}  <=  ln E_{mu0} e^{-beta Delta}  <=  ln sum_k w_k e^{-beta m_k} + beta^2 sum_i c_i^2 / 8 .
Argument (two lines): Jensen and the product sandwich (Theorem 3.1(a),(c) [V]) applied to each component, then sum.

Checks (exact enumeration of X = {0,1}^n or {0,1,2}^n, random instances):
  M1  both inequalities for random mixtures, random residuals (c_i = the exact largest single-site change)
  M2  control: the ONE-average form  ln E e^{-beta Delta} <= -beta E_{mu0}Delta + beta^2 sum c_i^2/8  must FAIL for some
      mixtures (a two-component mixture is a dependent reference: D14 of the theory division) - shows that the K averages
      are needed, i.e. that the fact is not a triviality in disguise
  M3  degenerate end: K = |X| point masses -> the bracket collapses to the exact value (the statement is always true and
      says nothing unless K is small and the components are known)
  M4  the bracket's width is beta^2 sum c_i^2/8 whatever K: extensive, as for one product reference
Run: python3 -I -B item2d_mixture_sandwich_v2.py
"""
import itertools, math
import numpy as np
rng = np.random.default_rng(20261126)
viol = 0
def product_measure(n, q, rng, sharp=1.0):
    ps = [rng.dirichlet(np.ones(q) * sharp) for _ in range(n)]
    X = list(itertools.product(range(q), repeat=n))
    return np.array([math.prod(ps[i][x[i]] for i in range(n)) for x in X]), X
def bdiff(Delta, X, n, q):
    idx = {x: j for j, x in enumerate(X)}
    c = np.zeros(n)
    for x in X:
        for i in range(n):
            for s in range(q):
                if s != x[i]:
                    y = x[:i] + (s,) + x[i+1:]
                    c[i] = max(c[i], abs(Delta[idx[x]] - Delta[idx[y]]))
    return c
m1_lo = m1_hi = 0; m2_fail = 0; ncase = 0; worst_slack = 1e9; maxratio = 0
for (n, q) in ((6, 2), (4, 3), (8, 2)):
    for K in (1, 2, 3, 5):
        for rep in range(40):
            comps = []; X = None
            for k in range(K):
                mu, X = product_measure(n, q, rng, sharp=0.3)
                comps.append(mu)
            w = rng.dirichlet(np.ones(K))
            mu0 = sum(wk * mk for wk, mk in zip(w, comps))
            # residual: additive part + a non-additive part (random function scaled)
            kind = rep % 3
            if kind == 0: Delta = rng.normal(size=len(X))
            elif kind == 1: Delta = np.array([sum(x) ** 2 for x in X], dtype=float) * rng.uniform(0.1, 1)
            else: Delta = np.array([math.cos(1.7 * sum((i + 1) * xi for i, xi in enumerate(x))) for x in X]) * rng.uniform(0.2, 2)
            c = bdiff(Delta, X, n, q)
            for beta in (0.3, 1.0, 3.0):
                ncase += 1
                truth = math.log(float(np.sum(mu0 * np.exp(-beta * Delta))))
                mk = [float(np.sum(mu * Delta)) for mu in comps]
                lo = math.log(sum(wk * math.exp(-beta * m) for wk, m in zip(w, mk)))
                hi = lo + beta ** 2 * float(np.sum(c ** 2)) / 8
                m1_lo += truth < lo - 1e-10; m1_hi += truth > hi + 1e-10
                worst_slack = min(worst_slack, hi - truth)
                one = -beta * float(np.sum(mu0 * Delta)) + beta ** 2 * float(np.sum(c ** 2)) / 8
                if K >= 2 and truth > one + 1e-10:
                    m2_fail += 1; maxratio = max(maxratio, (truth + beta * float(np.sum(mu0 * Delta))) / (beta ** 2 * float(np.sum(c ** 2)) / 8))
viol += m1_lo + m1_hi
print(f"M1 {ncase} cases (n,q) in (6,2),(4,3),(8,2), K in 1,2,3,5, three residual families, beta in 0.3,1,3:")
print(f"   lower inequality violated: {m1_lo};  upper inequality violated: {m1_hi};  smallest slack of the upper end: {worst_slack:.3e}")
print(f"M2 (information) among the random instances with K >= 2 the one-average product width fails in {m2_fail} cases")
# designed control family: two modes
fail2 = 0; ok2 = 0; tot2 = 0; mx = 0.0
for nn in (8, 12):
    XX = list(itertools.product(range(2), repeat=nn)); wt = np.array([sum(x) for x in XX], dtype=float)
    for a in (0.05, 0.1, 0.2, 0.3, 0.4):
        mu_a = a ** wt * (1 - a) ** (nn - wt); mu_b = (1 - a) ** wt * a ** (nn - wt)
        for beta in (0.3, 1.0, 3.0):
            tot2 += 1
            mu0 = 0.5 * mu_a + 0.5 * mu_b
            truth = math.log(float(np.sum(mu0 * np.exp(-beta * wt))))
            width = beta ** 2 * nn / 8
            one = -beta * float(np.sum(mu0 * wt)) + width
            lo = math.log(0.5 * math.exp(-beta * float(np.sum(mu_a * wt))) + 0.5 * math.exp(-beta * float(np.sum(mu_b * wt))))
            if truth > one + 1e-12: fail2 += 1; mx = max(mx, (truth + beta * float(np.sum(mu0 * wt))) / width)
            ok2 += (lo - 1e-12 <= truth <= lo + width + 1e-12)
print(f"M2 control (designed): two modes Bernoulli(a)^n, Bernoulli(1-a)^n, Delta = |x|, n in 8,12, a in .05..0.4, beta in .3,1,3: {tot2} cases;")
print(f"   the one-average product width is violated in {fail2} (largest gap/width = {mx:.2f}); the K = 2 bracket holds in {ok2} of {tot2}")
viol += int(fail2 == 0) + (tot2 - ok2)
# sharp control for M2: perfectly correlated two-point mixture, additive residual
n = 6; X = list(itertools.product(range(2), repeat=n))
mu_a = np.array([1.0 if sum(x) == 0 else 0.0 for x in X]); mu_b = np.array([1.0 if sum(x) == n else 0.0 for x in X])
Delta = np.array([float(sum(x)) for x in X]); beta = 1.0; c = np.ones(n)
mu0 = 0.5 * mu_a + 0.5 * mu_b
truth = math.log(float(np.sum(mu0 * np.exp(-beta * Delta)))); one = -beta * float(np.sum(mu0 * Delta)) + beta ** 2 * n / 8
lo = math.log(0.5 * math.exp(0) + 0.5 * math.exp(-beta * n)); hi = lo + beta ** 2 * n / 8
print(f"   perfectly correlated reference (two point masses 0^n, 1^n), Delta = |x|, n = 6, beta = 1: truth {truth:.4f}; one-average bound {one:.4f} (violated: {truth > one}); K = 2 bracket [{lo:.4f}, {hi:.4f}] (holds: {lo - 1e-12 <= truth <= hi + 1e-12})")
viol += int(not truth > one) + int(not (lo - 1e-12 <= truth <= hi + 1e-12))
# M3: K = |X| point masses
mu, X = product_measure(5, 2, rng); Delta = rng.normal(size=len(X)); beta = 1.0
lo = math.log(float(np.sum(mu * np.exp(-beta * Delta)))); truth = lo
print(f"M3 K = |X| point masses: lower end = truth = {truth:.6f} (the bracket is then the exact value plus a useless upper width)")
print("M4 the width beta^2 sum c_i^2/8 does not depend on K (by construction); it is extensive.")
print(f"TOTAL violations: {viol}")
print("END item2d_mixture_sandwich_v2")
