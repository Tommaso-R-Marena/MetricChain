#!/usr/bin/env python3
"""Corollary 4(ii) of STRANDS_NN_HARDNESS.md, numerically: N* = floor(e^{beta E_0} Z_j) for j >= kT ln(2U)/eps,
U = n! 3^N.  Exact rationals with e^{1/kT} := 2 (kT = 1/ln 2), sigma = -1, several models."""
import pickle, math
from fractions import Fraction as F
from hard_test import INSTANCES, E_T1, E_T1c
cache = pickle.load(open('hard_cache.pkl', 'rb'))
ok = True; n = 0
for inst in INSTANCES:
    a, m, B = inst
    nn = len(a); N = 2 * m * B + m - 1; M = m * B - nn
    U = math.factorial(nn) * 3 ** N
    Nstar = sum(c for s, c in cache[inst].items() if s[0])
    for name, efun, E0, eps in [
        ('T1 bulge 0', lambda s: E_T1(s, F(-1), lambda uC, uT: F(0)), F(-M), F(1)),
        ("T1 H2' delta 1/4", lambda s: E_T1(s, F(-1), lambda uC, uT: -(uC + 1) + F(1, 4)), F(-M), F(1, 4)),
        ('T1c x=-3/2 gamma=1', lambda s: E_T1c(s, F(-1), F(-3, 2), lambda uC, uT: F(1)), F(-M) + F(-3, 2) * (nn - m), F(1, 2)),
    ]:
        if 'T1c' in name and B < 2:
            continue
        # beta = j ln 2 ; need j ln 2 >= ln(2U)/eps  ->  j >= log2(2U)/eps
        j = math.ceil(F(math.ceil(math.log2(2 * U)) + 1) / eps)
        j = j * eps.denominator       # make j*E integral for exact powers of two
        Z = sum(c * F(2) ** int(-j * efun(s)) for s, c in cache[inst].items())
        val = F(2) ** int(j * E0) * Z
        n += 1
        if math.floor(val) != Nstar or not (0 <= val - Nstar < F(1, 2)):
            ok = False; print('FAIL', inst, name, j, float(val), Nstar)
        # and with a magnification that is too small the floor is wrong on some instance (sanity)
print('Corollary 4(ii): floor(e^{beta E0} Z_j) = N* with rho < 1/2 in', n, 'instance/model pairs:', 'OK' if ok else 'FAIL')
