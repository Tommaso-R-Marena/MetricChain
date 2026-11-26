#!/usr/bin/env python3
"""Fractional / real alpha: the author's code run with a float or Fraction alpha against a floating-point
evaluation of the definition (sum over (Y,S) of w^alpha R^(1-alpha) / c) by the referee's Python brute force."""
import sys, itertools, math
from fractions import Fraction
sys.dont_write_bytecode = True
sys.path.insert(0, 'author_copy')
import multiset_dp as A
import bf
from cmp1 import mk_models

def ref_float(strands, bm, alpha):
    c = len(strands)
    tot = 0.0
    for Y in bf.distinct_words(strands):
        structs, _ = bf.all_connected(list(Y), bm)
        for partner, w, R in structs:
            tot += float(w) ** alpha * float(R) ** (1 - alpha)
    return tot / c

worst = 0.0
for strands in (['GC'] * 2, ['GC'] * 3, ['GC'] * 6, ['GGCC'] * 2, ['GGCC'] * 3, ['ACGT'] * 4, ['GAC', 'GTC'] * 2, ['GG', 'CC'] * 3, ['GGC', 'GCC', 'GC'], ['GA', 'TC', 'GC'] * 2, ['GGACC']):
    species = sorted(set(strands)); counts = [strands.count(s) for s in species]
    for name, hp, il, ma, mb, mc in mk_models()[:3]:
        am = A.Model(hp, il, ma, mb, mc)
        bm = bf.Model(lambda u, a, b: hp(u), lambda l1, a1, b1, l2, a2, b2: il(l1, l2), ma, mb, mc, name)
        for alpha in (0.5, 1.5, 2.5, -0.5, 0.25, math.pi, Fraction(1, 2), Fraction(7, 3)):
            try:
                dp = A.magnified_pf(species, counts, am, alpha)
            except Exception as ex:
                print('author code raised', type(ex).__name__, ex, 'for alpha', repr(alpha), strands, name)
                continue
            r = ref_float(strands, bm, float(alpha))
            rel = abs(float(dp) - r) / max(abs(r), 1e-300)
            worst = max(worst, rel)
            if rel > 1e-9:
                print('MISMATCH', strands, name, repr(alpha), dp, r)
print('largest relative deviation for non-integer alpha: %.3g' % worst)
