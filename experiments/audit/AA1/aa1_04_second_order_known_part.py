#!/usr/bin/env python3
"""AA1 audit, script 4: Theorem 11.33(a) ("second-order classes below the Curie-Weiss coupling
w = beta c2 n <= 4 cost polynomially many evaluations, at every accuracy") needs a hypothesis on
the known part that the theory report's statement omits (its source, D_REPORT.md Theorem 13, has
"f additive").

Counterexample family (new): f = M * [x not in C], C a binary code of minimum distance dmin,
class G2(c2) = {g : |mixed second differences| <= c2}, instance g = 0.
For y in C the droplet  g_y(x) = -c2 * T(r - d_H(x, y)),  T(m) = m(m+1)/2 for m >= 0, else 0,
  * belongs to G2(c2)                                   (Theorem 11.31(a); re-checked below),
  * differs from 0 exactly on the ball d_H(x, y) <= r - 1,
  * multiplies the weight of the codeword y by exp(beta c2 T(r)).
If 2 (r - 1) < dmin the supports are disjoint and each contains one codeword, so by Theorem
11.22(c) every (eps/2, delta)-correct algorithm has  E|Q(0)| >= (1 - 2 delta) |C|  as soon as
eps < ln(1 + (exp(beta c2 T(r)) - 1) / Z(f)).

Part A: droplet membership (exhaustive, n = 10) and the second differences of the profile.
Part B: an explicit instance: the extended binary Golay code, n = 24, |C| = 4096, dmin = 8, w = 4.
Part C: asymptotics with Gilbert-Varshamov codes: the exponent
        R_code(w) = max_delta min( ln 2 - h(delta), w delta^2 / 8 ) > 0 for every w > 0.
Part D: the same mechanism with a PAIRWISE known part (ferromagnetic blocks): at w = 4 the number
        of disjoint sensitive droplets is 2^(n/b) with b ~ n^(2/3), i.e. exp(Theta(n^(1/3))).

Run:  python3 experiments/audit/AA1/aa1_04_second_order_known_part.py > experiments/audit/AA1/out_04_second_order_known_part.txt
"""
import math
from itertools import combinations

import numpy as np
from scipy.optimize import brentq

OK = True


def check(name, cond):
    global OK
    print(("PASS  " if cond else "FAIL  ") + name)
    OK = OK and bool(cond)


def T(m):
    return m * (m + 1) // 2 if m >= 0 else 0


# --------------------------------------------------------------------------- Part A
print("Part A: the droplet -c2 T(r - d_H(x,y)) is in the class (all mixed second differences in [-c2, 0])")
n = 10
N = 1 << n
pop = np.array([bin(i).count("1") for i in range(N)], dtype=np.int64)
worst_lo, worst_hi = 0, 0
for r in range(1, n + 2):
    g = -np.array([T(r - int(k)) for k in pop], dtype=np.int64)        # centre y = 0, c2 = 1
    idx = np.arange(N)
    for i, j in combinations(range(n), 2):
        bi, bj = 1 << i, 1 << j
        base = idx[(idx & bi == 0) & (idx & bj == 0)]
        md = g[base | bi | bj] - g[base | bi] - g[base | bj] + g[base]
        worst_lo = min(worst_lo, int(md.min()))
        worst_hi = max(worst_hi, int(md.max()))
print(f"    n = {n}, all radii r = 1..{n+1}, all pairs and base points: mixed differences lie in [{worst_lo}, {worst_hi}] * c2")
check("(A) droplets belong to G2(c2)", worst_lo >= -1 and worst_hi <= 0)

# --------------------------------------------------------------------------- Part B
print("Part B: extended binary Golay code, n = 24, w = beta c2 n = 4")
# generator of the (23,12) Golay code from the generator polynomial x^11+x^10+x^6+x^5+x^4+x^2+1, plus parity
gpoly = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]            # coefficients of x^0..x^11
rows = []
for s in range(12):
    v = [0] * 23
    for k, cbit in enumerate(gpoly):
        if cbit:
            v[s + k] = 1
    v.append(sum(v) % 2)
    rows.append(int("".join(map(str, v)), 2))
code = {0}
for rrow in rows:
    code |= {c ^ rrow for c in code}
code = sorted(code)
wts = [bin(c).count("1") for c in code]
from collections import Counter

enum = Counter(wts)
dmin = min(w_ for w_ in wts if w_ > 0)
print(f"    |C| = {len(code)}, weight enumerator = {dict(sorted(enum.items()))}, dmin = {dmin}")
check("(B1) the code has 4096 words and minimum distance 8", len(code) == 4096 and dmin == 8)
n = 24
beta = 1.0
c2 = 4.0 / n                       # w = beta c2 n = 4  (the boundary case of Theorem 11.33(a))
r = 4                              # support radius r - 1 = 3, 2 * 3 < 8
betaM = 60.0
# Z(f) and Z(f + g_y) by distance classes from a codeword y (the code is linear: distance distribution = weight enumerator)
Zf = len(code) + (2 ** n - len(code)) * math.exp(-betaM)
Zfg = 0.0
for d_ in range(n + 1):
    A_d = enum.get(d_, 0)
    boost = math.exp(beta * c2 * T(r - d_))
    Zfg += A_d * boost + (math.comb(n, d_) - A_d) * math.exp(-betaM) * boost
effect = math.log(Zfg / Zf)
print(f"    r = {r}: beta c2 T(r) = {beta*c2*T(r):.4f};  ln Z(f + g_y) - ln Z(f) = {effect:.6e}")
print(f"    supports B(y, {r-1}) are pairwise disjoint (2*{r-1} < dmin = {dmin}); each query point detects at most one droplet")
print(f"    => every (eps/2, delta)-correct algorithm with eps < {effect:.4e} has E|Q(0)| >= (1 - 2 delta) * {len(code)}   (2^n = {2**n})")
check("(B2) every one of the 4096 droplets is sensitive at eps = 1e-3 and no point lies in two supports",
      effect > 1.0e-3 and 2 * (r - 1) < dmin)

# --------------------------------------------------------------------------- Part C
print("Part C: Gilbert-Varshamov asymptotics; exponent of E|Q(0)| at any bounded accuracy")


def h(x):
    return 0.0 if x <= 0 or x >= 1 else -x * math.log(x) - (1 - x) * math.log(1 - x)


print("      w     delta*    R_code(w) = ln2 - h(delta*) = w delta*^2/8     [f additive: exponent 0 for w <= 4 by Theorem 11.33(a)]")
allpos = True
for w in (0.25, 1.0, 2.0, 4.0, 8.0):
    fn = lambda dlt: (math.log(2) - h(dlt)) - w * dlt * dlt / 8
    dstar = brentq(fn, 1e-6, 0.5 - 1e-9)
    R = w * dstar * dstar / 8
    print(f"    {w:5.2f}   {dstar:.4f}    {R:.5f}")
    allpos = allpos and R > 0
check("(C) R_code(w) > 0 for every w tested, in particular for w <= 4", allpos)
print("    (for a rate R < R_code(w) take a sub-code of a Gilbert-Varshamov code with relative distance delta*, r = floor((dmin+1)/2):")
print("     |C| = e^{Rn}, effect of one droplet >= ln(1 + e^{(w delta*^2/8 - R) n}(1 - o(1))) -> infinity, supports disjoint.)")

# --------------------------------------------------------------------------- Part D
print("Part D: a PAIRWISE known part: ferromagnetic blocks of size b (m = n/b blocks, no coupling between blocks)")
print("    f(x) = 2 J sum_blocks k_I (b - k_I), k_I = number of ones in block I  (a complete-graph ferromagnet in each block);")
print("    for beta J large the Gibbs measure of f is uniform on the 2^m block-constant configurations, pairwise distance >= b.")


def block_instance_bruteforce(n, b, betaJ, betac2, r):
    """Exact ln Z(f + g_y) - ln Z(f) for y = 0...0 by enumeration, and the closed form of the text."""
    m = n // b
    N = 1 << n
    idx = np.arange(N, dtype=np.int64)
    popc = np.zeros(N, dtype=np.int64)
    fE = np.zeros(N)
    for I in range(m):
        kI = np.zeros(N, dtype=np.int64)
        for j in range(b):
            kI += (idx >> (I * b + j)) & 1
        fE += 2.0 * betaJ * kI * (b - kI)
        popc += kI
    Tvals = np.array([T(r - int(k)) for k in range(n + 1)], dtype=float)
    g = -betac2 * Tvals[popc]
    lnZf = np.log(np.exp(-fE).sum())
    lnZfg = np.log(np.exp(-(fE + g)).sum())
    closed = math.log(1 + (math.exp(betac2 * T(r)) - 1) / 2 ** m)
    # supports: block-constant configurations other than y inside B(y, r-1)?
    blockconst = np.ones(N, dtype=bool)
    for I in range(m):
        kI = np.zeros(N, dtype=np.int64)
        for j in range(b):
            kI += (idx >> (I * b + j)) & 1
        blockconst &= (kI == 0) | (kI == b)
    inside = int((blockconst & (popc <= r - 1)).sum())
    return lnZfg - lnZf, closed, inside


eff, closed, inside = block_instance_bruteforce(12, 4, betaJ=6.0, betac2=1.0, r=2)
print(f"    brute force, n = 12, b = 4, r = 2, beta c2 = 1, beta J = 6: effect {eff:.6f}; closed form ln(1 + (e^(beta c2 T(r)) - 1)/2^m) = {closed:.6f};")
print(f"    block-constant configurations inside the support B(y, r-1): {inside} (only y itself); 2(r-1) = 2 < b = 4")
check("(D1) the closed form of the droplet effect agrees with exact enumeration for the pairwise block known part",
      abs(eff - closed) < 1e-3 and inside == 1)

print("    w = beta c2 n = 4 (the boundary of Theorem 11.33(a)); r = floor((b+1)/2); closed form:")
print("         n        b     m = n/b    codewords 2^m    beta c2 T(r)    ln Z change of one droplet    E|Q(0)| >= (1-2delta) *")
grow = []
for (n, b) in ((64, 16), (512, 96), (4096, 384), (32256, 1536), (262144, 6144), (2097152, 24576)):
    m = n // b
    r = (b + 1) // 2
    expo = 4.0 / n * T(r)
    # ln(1 + (e^expo - 1)/2^m) computed stably
    x = expo - m * math.log(2)
    effect = math.log1p(math.exp(x)) if x < 30 else x
    grow.append((n, m, effect))
    print(f"    {n:9d}  {b:7d}   {m:6d}      2^{m:<4d}         {expo:10.2f}         {effect:10.3f}                 2^{m}")
check("(D2) with b ~ 1.5 n^(2/3) every droplet is sensitive at eps = 1 from n = 32256 on, and the number of disjoint droplets 2^(n/b) grows like exp(c n^(1/3))",
      all(e > 1.0 for (n, m, e) in grow if n >= 32256) and grow[-1][1] > grow[-3][1] > grow[-4][1])
print("    => with a pairwise (block-ferromagnetic) known part and w = 4 every algorithm needs exp(Theta(n^(1/3))) evaluations at bounded accuracy:")
print("       super-polynomial, where Theorem 11.33(a) as stated in the theory report promises polynomially many.")
print("       (In block variables the class has the effective coupling w * b: far above the Curie-Weiss value.)")

print()
print("ALL CHECKS PASSED" if OK else "SOME CHECK FAILED")
