"""Check of the separation bound in Theorem 4' (INFERENCE_LIMITS_ADDENDA.md A1).

For a linear code C and a centre s:  A = sum_x exp(-u d(x, s+C)),  F = sum_x exp(-u max(d(x, s+C), R)),
A1 = (1+e^-u)^n, F1 = sum_j C(n,j) exp(-u max(j,R)), D_R = ln A1 - ln F1.
Claim:  ln A - ln F >= D_R - ln|C|   (and A - F >= A1 - F1,  F <= |C| F1).
Exact enumeration for the simplex code [15,4] and RM(1,4) [16,5].
"""
import math
import numpy as np
from code_cone_check import rm1, simplex, span, dist_to_code

def check(name, n, gens):
    code = span(gens, n)
    d = dist_to_code(n, code).astype(float)          # s = 0 w.l.o.g. (translation)
    worst = float("inf")
    for u in (0.3, 0.7, 1.0, 2.0, 3.0):
        A = np.exp(-u*d).sum(); A1 = (1+math.exp(-u))**n
        for R in range(1, n//2 + 2):
            F = np.exp(-u*np.maximum(d, R)).sum()
            F1 = sum(math.comb(n, j)*math.exp(-u*max(j, R)) for j in range(n+1))
            DR = math.log(A1) - math.log(F1)
            sep = math.log(A) - math.log(F)
            assert A - F >= A1 - F1 - 1e-9*A1, (u, R)
            assert F <= len(code)*F1*(1+1e-12), (u, R)
            assert sep >= DR - math.log(len(code)) - 1e-10, (u, R, sep, DR)
            if DR > 1e-3:
                worst = min(worst, sep - (DR - math.log(len(code))))
    print(f"{name}: n={n}, |C|={len(code)}: all inequalities hold; smallest slack of the separation bound = {worst:.4f}")

n, gens = simplex(4); check("simplex [15,4]", n, gens)
n, gens = rm1(4);     check("RM(1,4) [16,5]", n, gens)
