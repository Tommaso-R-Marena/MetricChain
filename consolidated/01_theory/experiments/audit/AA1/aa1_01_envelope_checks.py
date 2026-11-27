#!/usr/bin/env python3
"""AA1 audit, script 1: small exact checks behind classifications in THEORY_REPORT sections 2-3.

Each block states the assumption that is dropped and what is observed.  Everything is exact
(fractions or tiny linear programmes); no randomness.

Run:  python3 experiments/audit/AA1/aa1_01_envelope_checks.py > experiments/audit/AA1/out_01_envelope_checks.txt
"""
from fractions import Fraction as Fr
from itertools import product
import math

import numpy as np
from scipy.optimize import linprog

OK = True


def check(name, cond):
    global OK
    print(("PASS  " if cond else "FAIL  ") + name)
    OK = OK and bool(cond)


# ---------------------------------------------------------------------------------------------
# (a) Theorem 2.3 / 2.4 with a raw difference table that violates the triangle inequality.
#     Assumption dropped: "d is an envelope (triangle inequality)".
# ---------------------------------------------------------------------------------------------
print("(a) contact-set and sharp-minimum criteria applied to a table that is not transitively closed")
X = ["x", "y", "z"]
BIG = 10.0
d = {(a, b): (0.0 if a == b else BIG) for a in X for b in X}
d[("y", "z")] = 1.0
d[("z", "x")] = 1.0          # so the closure has d*(y,x) = 2 < 10 = d(y,x)
f = {"x": 5.0, "y": 0.0, "z": 100.0}


def admissible_lp(extra_A, extra_b):
    """Feasibility of {g : g(a)-g(b) <= d(a,b)} plus extra rows (A g <= b)."""
    idx = {a: i for i, a in enumerate(X)}
    A, b = [], []
    for a in X:
        for c in X:
            if a != c:
                row = [0.0] * 3
                row[idx[a]] += 1.0
                row[idx[c]] -= 1.0
                A.append(row)
                b.append(d[(a, c)])
    A += extra_A
    b += extra_b
    res = linprog(c=[0, 0, 0], A_ub=A, b_ub=b, bounds=[(-1e3, 1e3)] * 3, method="highs")
    return res.status == 0


def closure(dd):
    dc = dict(dd)
    for k in X:
        for a in X:
            for b in X:
                dc[(a, b)] = min(dc[(a, b)], dc[(a, k)] + dc[(k, b)])
    return dc


raw_contact = all(f["x"] <= f[y] + d[(y, "x")] for y in X)
# is there an admissible g with x in argmin(f+g)?   f(x)+g(x) <= f(w)+g(w)  for all w
rows, rhs = [], []
idx = {a: i for i, a in enumerate(X)}
for w in X:
    if w != "x":
        row = [0.0] * 3
        row[idx["x"]] += 1.0
        row[idx[w]] -= 1.0
        rows.append(row)
        rhs.append(f[w] - f["x"])
exists_g = admissible_lp(rows, rhs)
dc = closure(d)
closed_contact = all(f["x"] <= f[y] + dc[(y, "x")] for y in X)
print(f"    raw table: contact condition holds = {raw_contact}; an admissible g making x optimal exists = {exists_g}")
print(f"    closed table d*(y,x) = {dc[('y','x')]}: contact condition holds = {closed_contact}")
check("(a1) raw contact condition holds but no admissible residual makes x optimal (Thm 2.3 '<=' fails without the triangle inequality)",
      raw_contact and not exists_g)
check("(a2) with the shortest-path closure the criterion agrees with the LP", closed_contact == exists_g)

# sharp minimum: x optimal for EVERY admissible g, although the raw condition d(x,y) <= f(y)-f(x) fails
f2 = {"x": 0.0, "y": 3.0, "z": 3.0}
d2 = {(a, b): (0.0 if a == b else BIG) for a in X for b in X}
d2[("x", "z")] = 1.0
d2[("z", "y")] = 1.0         # closure: d*(x,y) = 2 <= 3, raw d(x,y) = 10 > 3
d_save = d
d = d2
raw_sharp = all(d2[("x", y)] <= f2[y] - f2["x"] for y in X)
# x fails to be optimal for some admissible g  <=>  exists g admissible and w with f(w)+g(w) < f(x)+g(x)
some_violation = False
for w in X:
    if w == "x":
        continue
    # maximise g(x) - g(w) over the class; violation iff max > f(w) - f(x)
    idxs = {a: i for i, a in enumerate(X)}
    A, b = [], []
    for a in X:
        for c in X:
            if a != c:
                row = [0.0] * 3
                row[idxs[a]] += 1.0
                row[idxs[c]] -= 1.0
                A.append(row)
                b.append(d2[(a, c)])
    cvec = [0.0] * 3
    cvec[idxs["x"]] = -1.0
    cvec[idxs[w]] = 1.0
    res = linprog(c=cvec, A_ub=A, b_ub=b, bounds=[(-1e3, 1e3)] * 3, method="highs")
    if -res.fun > f2[w] - f2["x"] + 1e-9:
        some_violation = True
d2c = closure(d2)
closed_sharp = all(d2c[("x", y)] <= f2[y] - f2["x"] for y in X)
print(f"    sharp minimum: raw condition = {raw_sharp}, closed condition = {closed_sharp}, x optimal for every admissible g = {not some_violation}")
check("(a3) x is optimal for every admissible g although the raw sharp-minimum condition fails (Thm 2.4 '=>' fails without the triangle inequality)",
      (not raw_sharp) and (not some_violation) and closed_sharp)
d = d_save

# ---------------------------------------------------------------------------------------------
# (b) Theorem 2.7 with the separation read in the transposed direction (asymmetric envelope).
# ---------------------------------------------------------------------------------------------
print("(b) Theorem 2.7: 'y is sigma-separated' must be read as d(anchor, y) >= sigma")
# X = {a, y}; d(a,y) = 0, d(y,a) = 1; g = 0 (kappa = 0); f(a) = 0, f(y) = 1/10; A = {a}; eps = 0
dab = {("a", "a"): Fr(0), ("y", "y"): Fr(0), ("a", "y"): Fr(0), ("y", "a"): Fr(1)}
ff = {"a": Fr(0), "y": Fr(1, 10)}
gg = {"a": Fr(0), "y": Fr(0)}
tri = all(dab[(p, r)] <= dab[(p, q)] + dab[(q, r)] for p in "ay" for q in "ay" for r in "ay")
adm = all(gg[p] - gg[q] <= dab[(p, q)] for p in "ay" for q in "ay")
L = {w: gg["a"] - dab[("a", w)] for w in "ay"}           # lower McShane envelope from the anchor a
UB = ff["a"] + gg["a"]
is_cert = all(UB - 0 <= ff[w] + L[w] for w in "ay")
gap_y = ff["y"] + gg["y"] - UB
sigma_correct = dab[("a", "y")]          # distance FROM the anchor TO y
sigma_transposed = dab[("y", "a")]
print(f"    envelope ok = {tri}, g admissible = {adm}, A = {{a}} is an exact certificate = {is_cert}, gap(y) = {gap_y}")
print(f"    correct reading: sigma <= d(a,y) = {sigma_correct}: forces y iff gap(y) < sigma, i.e. {gap_y < sigma_correct}")
print(f"    transposed reading: sigma <= d(y,a) = {sigma_transposed}: would force y iff {gap_y < sigma_transposed}")
check("(b) transposed reading would force y into A although A = {a} certifies without it",
      tri and adm and is_cert and (gap_y < sigma_transposed) and not (gap_y < sigma_correct))

# ---------------------------------------------------------------------------------------------
# (c) Theorem 2.1: injectivity of T, and beta >= 0.
# ---------------------------------------------------------------------------------------------
print("(c) Theorem 2.1: transport map two-to-one; negative beta")
beta, gamma = 1.0, 1.0
E = {"s": 0.0, "a1": 1.0, "a2": 1.0}        # T(a1) = T(a2) = s, E(T x) + gamma <= E(x)
ZA = sum(math.exp(-beta * E[a]) for a in ("a1", "a2"))
ZS = math.exp(-beta * E["s"])
print(f"    Z(A) = {ZA:.6f},  e^(-beta gamma) Z(S) = {math.exp(-beta*gamma)*ZS:.6f},  with fibre size m = 2: {2*math.exp(-beta*gamma)*ZS:.6f}")
check("(c1) a two-to-one map violates Z(A) <= e^{-beta gamma} Z(S) and attains the fibre bound m e^{-beta gamma} Z(S)",
      ZA > math.exp(-beta * gamma) * ZS + 1e-12 and abs(ZA - 2 * math.exp(-beta * gamma) * ZS) < 1e-12)
beta = -1.0
E = {"s": 0.0, "a": 2.0}                    # E(T a) + gamma <= E(a) with gamma = 1
ZA, ZS = math.exp(-beta * E["a"]), math.exp(-beta * E["s"])
check("(c2) for beta < 0 the inequality fails for an injective map", ZA > math.exp(-beta * gamma) * ZS + 1e-12)

# ---------------------------------------------------------------------------------------------
# (d) Theorem 2.2: the referee's ferromagnetic chain (multi-site improving map without any
#     single-site or pair dominance), and a 3-body example where the nested sum-of-minima rule
#     is strictly weaker than exact dominance.
# ---------------------------------------------------------------------------------------------
print("(d) Theorem 2.2: scope of 'the gauge does not help'")
n = 6


def Echain(x):
    return sum(x) + 3 * sum(1 for i in range(n - 1) if x[i] != x[i + 1])


confs = list(product((0, 1), repeat=n))
single = []
for i in range(n):
    for r, t in ((0, 1), (1, 0)):
        margin = min(Echain(x[:i] + (r,) + x[i + 1:]) - Echain(x[:i] + (t,) + x[i + 1:]) for x in confs)
        single.append(margin)
pair11 = []
for i in range(n - 1):
    for tt in ((0, 0), (0, 1), (1, 0)):
        margin = min(Echain(x[:i] + (1, 1) + x[i + 2:]) - Echain(x[:i] + tt + x[i + 2:]) for x in confs)
        pair11.append(margin)
improving = all(Echain((0,) * n) <= Echain(x) for x in confs)
print(f"    largest single-site Goldstein margin = {max(single)} (a state is dominated iff some margin >= 0)")
print(f"    largest pair margin for eliminating (1,1) on adjacent sites = {max(pair11)}")
check("(d1) no single-site dominance, the pair (1,1) is never dominated, yet x -> 0...0 is improving",
      max(single) < 0 and max(pair11) < 0 and improving)
# 3-body: difference energy at site i as a function of two neighbours (j,k):
#   D(xj,xk) = a(xj) + b(xk) + q(xj,xk)   with a = b = (0,1), q = [[1,0],[0,-1]]
a_, b_ = (0, 1), (0, 1)
q_ = ((1, 0), (0, -1))
exact = min(a_[s] + b_[u] + q_[s][u] for s in (0, 1) for u in (0, 1))
nested = min(a_) + min(b_) + min(min(row) for row in q_)
print(f"    3-body difference energy: exact margin = {exact}, nested sum-of-minima = {nested}")
check("(d2) with a 3-body term the term-wise (nested) rule is strictly below the exact margin (exact > 0 >= nested)",
      exact > 0 >= nested)

print()
print("ALL CHECKS PASSED" if OK else "SOME CHECK FAILED")
