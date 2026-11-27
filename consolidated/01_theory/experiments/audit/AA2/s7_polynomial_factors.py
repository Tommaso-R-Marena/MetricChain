#!/usr/bin/env python3
"""AA2 audit, script S7 -- "optimal up to a polynomial factor, for every n": how large the factor is.

Theorem 11.76(a): the type-stratified sample is optimal among non-adaptive algorithms up to the factor
    8 (n+1) ln(2(n+1)/delta) / (1 - 2 delta)   in the cost   and   ln(4/delta)   in the accuracy.
Theorem 11.95: the same with joint types, N_orb = prod_j C(n_j + q_j - 1, q_j - 1) for n + 1.
Remark after Theorem 11.76: "the statement is empty when the number of orbits is exponential".

The script tabulates the factor against (i) the cost it is a factor of, exp(n a) at vanishing accuracy, and
(ii) the number of configurations, for homogeneous and heterogeneous compositions.  Arithmetic only.

Run:  python3 experiments/audit/AA2/s7_polynomial_factors.py > experiments/audit/AA2/out_s7.txt
"""
import math

delta = 0.05


def factor(N_orb_ln):
    """ln of 8 N_orb ln(2 N_orb/delta)/(1 - 2 delta), given ln N_orb."""
    return math.log(8) + N_orb_ln + math.log(N_orb_ln + math.log(2 / delta)) - math.log(1 - 2 * delta)


def ln_comb(a, b):
    return math.lgamma(a + 1) - math.lgamma(b + 1) - math.lgamma(a - b + 1)


print("AA2 / S7: the polynomial factors of Theorems 11.76(a) and 11.95 (delta = 0.05)")
print(f"accuracy offset of both theorems: ln(4/delta) = {math.log(4 / delta):.3f} nats  -> nothing is claimed for accuracies below it")
print()
print("(a) uniform cube / any exchangeable known part, two letters (Theorem 11.76(a)); cost scale exp(n a), a = 0.110944 (u = 1)")
print("     n    ln(factor)   n*a     factor exceeds the cost it multiplies?")
for n in (20, 50, 100, 200, 500, 1000):
    lf = factor(math.log(n + 1))
    print(f"  {n:5d}   {lf:8.2f}   {n * 0.110944:7.2f}    {'YES (vacuous)' if lf > n * 0.110944 else 'no'}")
print()
print("(b) heteropolymer product landscapes (Theorem 11.95): m site types, q letters each, n/m sites per type")
print("    cost scale exp(n a) with a = 0.25 per site (the example sites of section 11.26 have a = 0.095 ... 0.295)")
print("     m    q      n    ln N_orb   ln(factor)    n*a    n ln q   verdict")
for m, q in ((1, 2), (2, 3), (5, 3), (20, 3), (20, 4)):
    for n in (100, 300, 1000, 10000):
        if n % m:
            continue
        nj = n // m
        lnN = m * ln_comb(nj + q - 1, q - 1)
        lf = factor(lnN)
        verdict = "vacuous: factor > exp(n a)" if lf > 0.25 * n else "informative"
        print(f"  {m:4d}  {q:3d}  {n:6d}  {lnN:9.2f}   {lf:9.2f}  {0.25 * n:8.1f}  {n * math.log(q):8.1f}   {verdict}")
print()
print("(c) every site its own type (m = n; site-dependent parameters without repetition): the symmetry group is trivial,")
print("    N_orb = number of configurations, and the factor is the cost of complete enumeration:")
for n, q in ((30, 3), (100, 3)):
    lnN = n * math.log(q)
    print(f"    n = {n}, q = {q}: ln N_orb = {lnN:.1f} = ln |X|, ln(factor) = {factor(lnN):.1f}  -> the every-n statement is empty")
