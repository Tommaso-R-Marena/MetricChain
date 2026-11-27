#!/usr/bin/env python3
"""AA1 audit, script 2: the product-reference hypothesis of Theorem 3.1(c) and Theorem 11.21.

Question: the report shows that the width beta^2 sum c_i^2 / 8 fails for a PERFECTLY correlated
reference (D14).  Is there a threshold of weak dependence below which it survives, and what is the
quantitative replacement?

Part A (exact, two binary sites, symmetric Markov reference with P(x1 = x2) = (1+rho)/2, c = (1,1)):
    sup over the whole bounded-difference class of the Jensen gap  ln E exp(-beta(D - E D)),
    by enumeration of the vertices of the class (the functional is convex), against
      product width        beta^2 * 2 / 8,
      Kontorovich-Ramanan  beta^2 * ((1+rho)^2 + 1) / 8     (martingale ranges c1 + rho c2, c2),
      Hoeffding (any ref)  beta^2 * 4 / 8.
Part B (exact, n-site homogeneous binary Markov chain, additive residual D = sum x_i, c_i = 1):
    the gap per site against beta^2/8, and the structure factor (1+rho)/(1-rho).
Part C (exact): the concentration inequality of Theorem 11.21 with C = sum c_i^2 for a dependent
    reference, N = 1 sample.
Part D (seeded, exact enumeration): a reference that is a mixture of K product measures (a
    multimodal ensemble): the width beta^2 sum c_i^2 / 8 survives if the K component averages are
    used in place of the single average, and fails with the single average.

Run:  python3 experiments/audit/AA1/aa1_02_sandwich_dependence.py > experiments/audit/AA1/out_02_sandwich_dependence.txt
"""
from itertools import combinations, product
import math

import numpy as np

OK = True


def check(name, cond):
    global OK
    print(("PASS  " if cond else "FAIL  ") + name)
    OK = OK and bool(cond)


def gap(w, vals, beta):
    """ln E exp(-beta (D - E D)) for weights w and values vals."""
    w = np.asarray(w, float)
    vals = np.asarray(vals, float)
    m = float(np.dot(w, vals))
    return math.log(float(np.dot(w, np.exp(-beta * (vals - m)))))


# --------------------------------------------------------------------------- Part A
print("Part A: two binary sites, Markov reference with correlation rho, c = (1,1)")
# unknowns (a, b, t) = (D(10), D(01), D(11)), D(00) = 0; constraints |a|<=1, |b|<=1, |t-a|<=1, |t-b|<=1
rowsA = [((1, 0, 0), 1), ((-1, 0, 0), 1), ((0, 1, 0), 1), ((0, -1, 0), 1),
         ((-1, 0, 1), 1), ((1, 0, -1), 1), ((0, -1, 1), 1), ((0, 1, -1), 1)]
verts = set()
for trip in combinations(range(8), 3):
    M = np.array([rowsA[i][0] for i in trip], float)
    r = np.array([rowsA[i][1] for i in trip], float)
    if abs(np.linalg.det(M)) < 1e-12:
        continue
    v = np.linalg.solve(M, r)
    if all(np.dot(row, v) <= rhs + 1e-9 for row, rhs in rowsA):
        verts.add(tuple(np.round(v, 9)))
verts = sorted(verts)
print(f"    vertices of the class (D(10), D(01), D(11)), D(00) = 0: {len(verts)}")


def sup_gap(rho, beta):
    # weights of 00, 10, 01, 11
    w = np.array([(1 + rho) / 4, (1 - rho) / 4, (1 - rho) / 4, (1 + rho) / 4])
    best, arg = -1.0, None
    for (a, b, t) in verts:
        gval = gap(w, [0.0, a, b, t], beta)
        if gval > best:
            best, arg = gval, (a, b, t)
    return best, arg


print("    rho    beta   sup gap     product    KR bound   Hoeffding  sup/product  extremal (a,b,t)")
viol_small_rho = True
for rho in (0.0, 0.01, 0.05, 0.2, 0.5, 0.8, 1.0):
    for beta in (0.1, 1.0, 3.0):
        sg, arg = sup_gap(rho, beta)
        prod = beta ** 2 * 2 / 8
        kr = beta ** 2 * ((1 + rho) ** 2 + 1) / 8
        hoef = beta ** 2 * 4 / 8
        print(f"    {rho:4.2f}   {beta:4.1f}   {sg:9.6f}   {prod:8.6f}   {kr:8.6f}   {hoef:8.6f}   {sg/prod:8.5f}    {tuple(float(z) for z in arg)}")
        if not (sg <= min(kr, hoef) + 1e-12):
            check(f"bound order violated at rho={rho}, beta={beta}", False)
        if rho > 0 and beta == 0.1 and not sg > prod:
            viol_small_rho = False
check("(A1) at beta = 0.1 the product width is violated for EVERY rho > 0 tested (down to rho = 0.01)", viol_small_rho)
r0, _ = sup_gap(0.0, 1.0)
check("(A2) at rho = 0 the product width holds", r0 <= 1.0 ** 2 * 2 / 8 + 1e-12)
# small-beta law: sup gap / (beta^2/4) -> 1 + rho
lim_ok = True
for rho in (0.01, 0.2, 0.5, 1.0):
    sg, _ = sup_gap(rho, 1e-3)
    ratio = sg / (1e-6 / 4)
    print(f"    small-beta ratio sup gap / (beta^2/4) at rho = {rho}: {ratio:.5f}   (1 + rho = {1+rho:.5f})")
    lim_ok = lim_ok and abs(ratio - (1 + rho)) < 2e-3
check("(A3) as beta -> 0 the worst gap is (1 + rho) times the product width: no threshold of weak dependence", lim_ok)
# the perfectly correlated case reproduces the report's counterexample ln cosh 1
sg, _ = sup_gap(1.0, 1.0)
check("(A4) rho = 1, beta = 1 gives ln cosh 1 = 0.4338 (theory report, D14)", abs(sg - math.log(math.cosh(1.0))) < 1e-9)

# --------------------------------------------------------------------------- Part B
print("Part B: homogeneous binary Markov chain of n sites, D = number of ones, c_i = 1")


def chain_weights(n, rho):
    confs = list(product((0, 1), repeat=n))
    w = []
    for x in confs:
        p = 0.5
        for i in range(n - 1):
            p *= (1 + rho) / 2 if x[i] == x[i + 1] else (1 - rho) / 2
        w.append(p)
    return confs, np.array(w)


beta = 0.2
print(f"    beta = {beta}; columns: gap / (n beta^2 / 8)")
print("    n     rho=0     rho=0.3    rho=0.6    rho=0.9      [(1+rho)/(1-rho) = 1, 1.857, 4, 19]")
grow = True
for n in (2, 4, 8, 12, 16):
    line = f"    {n:2d}"
    for rho in (0.0, 0.3, 0.6, 0.9):
        confs, w = chain_weights(n, rho)
        vals = [sum(x) for x in confs]
        gval = gap(w, vals, beta)
        line += f"   {gval / (n * beta**2 / 8):8.4f}"
        if rho == 0.0 and gval > n * beta ** 2 / 8 + 1e-12:
            grow = False
    print(line)
check("(B1) at rho = 0 the additive residual stays within the product width", grow)
confs, w = chain_weights(16, 0.6)
g16 = gap(w, [sum(x) for x in confs], beta) / (16 * beta ** 2 / 8)
check("(B2) at rho = 0.6, n = 16 the product width is exceeded by a factor > 3 (approaching the structure factor 4)", g16 > 3.0)

# --------------------------------------------------------------------------- Part C
print("Part C: Theorem 11.21's concentration bound 2 exp(-2 N eta^2 / sum c_i^2) with one sample")
for (n, rho) in ((4, 1.0), (12, 0.6), (12, 0.3)):
    confs, w = chain_weights(n, rho)
    vals = np.array([sum(x) for x in confs], float)
    mean = float(np.dot(w, vals))
    worst = 0.0
    arg = None
    for eta in sorted(set(abs(v - mean) for v in vals)):
        if eta <= 0:
            continue
        p = float(w[np.abs(vals - mean) >= eta - 1e-12].sum())
        bound = 2 * math.exp(-2 * eta ** 2 / n)
        if p / bound > worst:
            worst, arg = p / bound, (eta, p, bound)
    print(f"    n = {n:2d}, rho = {rho}: largest P(|D - mean| >= eta) / bound = {worst:.3f} at eta = {arg[0]:.2f} (P = {arg[1]:.4g}, bound = {arg[2]:.4g})")
    if rho >= 0.6:
        check(f"(C) the bound with C = sum c_i^2 is violated for the dependent reference n = {n}, rho = {rho}", worst > 1.0)

# --------------------------------------------------------------------------- Part D
print("Part D: a multimodal reference = mixture of K product measures (not in the report)")
print("    claim:  ln sum_k w_k e^{-beta m_k}  <=  ln(Z/Z0)  <=  ln sum_k w_k e^{-beta m_k} + beta^2 sum c_i^2 / 8,")
print("            m_k = <D> under the k-th product component  (Theorem 3.1(a),(c) applied per component)")
rng = np.random.default_rng(20261126)
nD, K = 6, 3
confsD = np.array(list(product((0, 1), repeat=nD)))
worst_low, worst_up, viol_single = float('inf'), float('-inf'), 0
trials = 400
for _ in range(trials):
    ps = rng.uniform(0.02, 0.98, size=(K, nD))
    wk = rng.dirichlet(np.ones(K))
    comp = np.array([np.prod(np.where(confsD == 1, ps[k], 1 - ps[k]), axis=1) for k in range(K)])   # K x 2^n
    mix = wk @ comp
    # random residual: additive part plus a non-additive part; its bounded-difference constants are computed exactly
    gD = confsD @ rng.normal(0, 1, nD) + 0.5 * rng.normal(0, 1, len(confsD))
    cD = np.zeros(nD)
    idxD = {tuple(x): i for i, x in enumerate(confsD)}
    for i in range(nD):
        for x in confsD:
            if x[i] == 0:
                y = x.copy()
                y[i] = 1
                cD[i] = max(cD[i], abs(gD[idxD[tuple(x)]] - gD[idxD[tuple(y)]]))
    betaD = rng.uniform(0.2, 2.0)
    lnratio = math.log(float(mix @ np.exp(-betaD * gD)))
    mk = comp @ gD
    core = math.log(float(wk @ np.exp(-betaD * mk)))
    width = betaD ** 2 * float(cD @ cD) / 8
    worst_low = min(worst_low, lnratio - core)
    worst_up = max(worst_up, lnratio - core - width)
    single = -betaD * float(mix @ gD)                 # the one-average sandwich of Theorem 3.1(c)
    if lnratio > single + width + 1e-12:
        viol_single += 1
print(f"    {trials} random instances (n = {nD}, K = {K}): min(lnratio - lower) = {worst_low:.3e} (>= 0), "
      f"max(lnratio - upper) = {worst_up:.3e} (<= 0)")
print(f"    the single-average sandwich with width beta^2 sum c_i^2/8 is violated in {viol_single} of {trials} instances")
check("(D1) the per-component sandwich holds with the product width in every instance", worst_low >= -1e-12 and worst_up <= 1e-12)
# a bimodal instance: two product components with p = 0.02 and p = 0.98 at every site, D = number of ones
psB = np.array([[0.02] * nD, [0.98] * nD])
wB = np.array([0.5, 0.5])
compB = np.array([np.prod(np.where(confsD == 1, psB[k], 1 - psB[k]), axis=1) for k in range(2)])
mixB = wB @ compB
gB = confsD.sum(axis=1).astype(float)
betaB = 1.0
lnratioB = math.log(float(mixB @ np.exp(-betaB * gB)))
coreB = math.log(float(wB @ np.exp(-betaB * (compB @ gB))))
widthB = betaB ** 2 * nD / 8
singleB = -betaB * float(mixB @ gB)
print(f"    bimodal instance (n = {nD}, p = 0.02 / 0.98, D = |x|, beta = 1): ln(Z/Z0) = {lnratioB:.4f}; "
      f"single-average bracket [{singleB:.4f}, {singleB + widthB:.4f}]; per-component bracket [{coreB:.4f}, {coreB + widthB:.4f}]")
check("(D2) on the bimodal instance the single-average sandwich fails and the per-component one holds",
      lnratioB > singleB + widthB and coreB - 1e-12 <= lnratioB <= coreB + widthB + 1e-12)

print()
print("ALL CHECKS PASSED" if OK else "SOME CHECK FAILED")
