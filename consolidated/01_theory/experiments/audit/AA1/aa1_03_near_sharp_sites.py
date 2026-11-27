#!/usr/bin/env python3
"""AA1 audit, script 3: "one evaluation or exponentially many" (Theorems 11.7-11.9) outside the
hypothesis "finitely many site types".

Family: n two-state sites, known part f(x) = e * |x| (e = 1), envelope c * Hamming with
c = e (1 + delta), zero residual, eps = 0.  Every site is NON-sharp (c > e) for every delta > 0.

A centre a covers y iff  c * d_H(a, y) <= gap(y) = e * |y|.

Part A (exact): N_cov for delta < 1/n.  Claim: N_cov = n + 1 (the ground state and the n single
    excitations are each covered only by themselves, and together they cover everything).
    So the number of evaluations is neither one nor exponential: it is linear in n, although all
    n sites are non-sharp.  Exact for n <= 12 by exhaustive coverage tables.
Part B: the exponent R*(delta) = max_x [ln(1+x) - ln(1+x^(1+delta))] of Theorem 11.9 for small
    margins: R*/delta -> max_x (-x ln x)/(1+x) = 0.2785.  Super-polynomial growth needs
    n * delta >> ln n.
Part C (exact, small n): for fixed n the exact fractional covering number as delta decreases
    (linear programme), to show the crossover between the two regimes.
Part D: the report's own example at kappa = 1 (phi = (0,0), gamma = (0,c)): N_cov = 1 although
    the site is not sharp (needs kappa < 1).

Run:  python3 experiments/audit/AA1/aa1_03_near_sharp_sites.py > experiments/audit/AA1/out_03_near_sharp_sites.txt
"""
import math
from fractions import Fraction as Fr

import numpy as np
from scipy.optimize import linprog, minimize_scalar

OK = True


def check(name, cond):
    global OK
    print(("PASS  " if cond else "FAIL  ") + name)
    OK = OK and bool(cond)


def cover_matrix(n, delta, eps=Fr(0)):
    """C[a, y] = True iff a covers y, exact rational arithmetic on integers d_H, |y|."""
    N = 1 << n
    idx = np.arange(N, dtype=np.int64)
    pop = np.array([bin(i).count("1") for i in range(N)], dtype=np.int64)
    C = np.zeros((N, N), dtype=bool)
    # c d_H <= e |y| + eps  with e = 1, c = 1 + delta = (p+q)/q for delta = p/q
    p, q = delta.numerator, delta.denominator
    ep, eq = eps.numerator, eps.denominator
    for a in range(N):
        dh = pop[np.bitwise_xor(idx, a)]
        # (p+q)/q * dh <= |y| + ep/eq   <=>   (p+q) * dh * eq <= q * (|y| * eq + ep)
        C[a] = (p + q) * dh * eq <= q * (pop * eq + ep)
    return C, pop


# --------------------------------------------------------------------------- Part A
print("Part A: exact N_cov for margins delta < 1/n (all n sites non-sharp)")
allA = True
for n in range(2, 13):
    delta = Fr(1, 2 * n)                       # < 1/n
    C, pop = cover_matrix(n, delta)
    N = 1 << n
    forced = [y for y in range(N) if C[:, y].sum() == 1]          # covered only by itself
    centres = [0] + [1 << i for i in range(n)]
    covers_all = bool(C[centres].any(axis=0).all())
    forced_set = set(forced)
    ok = covers_all and all(c in forced_set for c in centres)
    print(f"    n = {n:2d}, delta = 1/{2*n}: forced points = {len(forced)}, "
          f"{{ground state}} + singletons cover everything = {covers_all}  =>  N_cov = {n+1 if ok else '?'}"
          f"   (2^n = {N})")
    allA = allA and ok and len(forced) == n + 1
check("(A) for delta < 1/n: N_cov = n + 1 exactly (n = 2..12): linear, with every site non-sharp", allA)

# --------------------------------------------------------------------------- Part B
print("Part B: the exponent of Theorem 11.9 for a two-state site with margin delta = c/e - 1")


def Rstar(delta):
    f = lambda x: -(math.log1p(x) - math.log1p(x ** (1 + delta)))
    res = minimize_scalar(f, bounds=(1e-9, 1 - 1e-9), method="bounded", options={"xatol": 1e-12})
    return -res.fun


lim = -minimize_scalar(lambda x: x * math.log(x) / (1 + x), bounds=(1e-9, 1 - 1e-9), method="bounded",
                       options={"xatol": 1e-12}).fun
print(f"    max_x (-x ln x)/(1+x) = {lim:.6f}")
print("    delta      R*(delta)     R*/delta    n needed for exp(n R*) = 1000")
ratio_ok = True
for delta in (1.0, 0.5, 0.1, 0.01, 0.001):
    r = Rstar(delta)
    print(f"    {delta:6.3f}    {r:.6f}     {r/delta:.5f}     {math.log(1000)/r:10.0f}")
    if delta <= 0.01:
        ratio_ok = ratio_ok and abs(r / delta - lim) < 0.01
check("(B1) R*(delta = 1) = 0.1882 (the report's value at e/c = 1/2)", abs(Rstar(1.0) - 0.1882) < 5e-5)
check("(B2) R*(delta)/delta -> 0.2785 as delta -> 0: the exponent vanishes linearly in the margin", ratio_ok)

# --------------------------------------------------------------------------- Part C
print("Part C: exact fractional covering numbers, n = 8, as the margin shrinks")
n = 8
N = 1 << n
prev = None
mono = True
for delta in (Fr(1), Fr(1, 2), Fr(1, 4), Fr(1, 7), Fr(1, 9), Fr(1, 100)):
    C, pop = cover_matrix(n, delta)
    # min sum w_a  s.t.  sum_{a covers y} w_a >= 1 for all y
    res = linprog(c=np.ones(N), A_ub=-C.T.astype(float), b_ub=-np.ones(N), bounds=[(0, None)] * N, method="highs")
    nf = res.fun
    forced = int((C.sum(axis=0) == 1).sum())
    print(f"    delta = {str(delta):6s}: N_frac = {nf:9.3f},  forced points = {forced:3d},  exp(n R*) = {math.exp(n * Rstar(float(delta))):7.3f},  2^n = {N}")
    if prev is not None and nf > prev + 1e-6:
        mono = False
    prev = nf
check("(C) N_frac decreases to n + 1 = 9 as delta -> 0 (it is 9 for delta < 1/8)", mono and abs(prev - 9) < 1e-6)

# --------------------------------------------------------------------------- Part D
print("Part D: kappa = 1 (theory report, proof of Theorem 11.9): phi = (0,0), gamma = (0,c)")
c = Fr(1)
phi = (Fr(0), Fr(0))
gam = (Fr(0), c)
E = [phi[s] + gam[s] for s in (0, 1)]
Estar = min(E)
slack = lambda a, y: (c if a != y else Fr(0)) - gam[a] + gam[y]
covers = {(a, y): slack(a, y) <= E[y] - Estar for a in (0, 1) for y in (0, 1)}
sharp = all(c <= phi[s] - phi[0] for s in (1,))
print(f"    site sharp = {sharp}; letter 1 covers both letters = {covers[(1,0)] and covers[(1,1)]}; "
      f"letter 0 covers letter 1 = {covers[(0,1)]}")
check("(D) at kappa = 1 a non-sharp site has N_cov = 1 (the dichotomy needs kappa < 1)",
      (not sharp) and covers[(1, 0)] and covers[(1, 1)])

print()
print("ALL CHECKS PASSED" if OK else "SOME CHECK FAILED")
