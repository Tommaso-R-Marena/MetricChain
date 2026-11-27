#!/usr/bin/env python3
"""Validate the C++ brute force against the pure-Python definition-level brute force (bf.py)."""
import sys, time
from fractions import Fraction
import bf, drv
alphas = [0, 1, 2, 3, -1]
systems = [['GC'], ['GGACC'], ['GC'] * 2, ['GC'] * 3, ['GC'] * 4, ['GGCC'] * 2, ['GCGC'] * 2, ['ACGT'] * 3, ['GAC', 'GTC'] * 2,
           ['GG', 'CC'] * 2, ['GG', 'CC'] * 3, ['GC', 'GGCC'] * 2, ['GGC', 'GCC', 'GC'], ['GA', 'TC', 'GC'] * 2, ['G', 'C'], ['GCGAAAGC', 'GC'],
           ['GGGAAACCC'], ['GCAGC', 'GCTGC'], ['AGCT'] * 4]
ok = True
for mk in (bf.model_unit, bf.model_sizes, bf.model_letters, lambda: bf.model_letters(7)):
    m = mk()
    for st in systems:
        species = sorted(set(st)); counts = [st.count(s) for s in species]; c = len(st)
        ref = bf.physical_sum_by_orbits(st, m, alphas) if c <= 6 else bf.physical_sum_by_words(st, m, alphas)
        for mode in (0, 1):
            res, nw, ns = drv.brute_mod(species, counts, m, alphas, mode=mode)
            q = drv.Q_from_T(res, c, alphas)
            good = all(q[a] == drv.fmod(ref[a]) for a in alphas)
            ok &= good
            if not good:
                print('MISMATCH', m.name, st, mode, {R: v[0] for R, v in res.items()})
    print(m.name, 'done', 'ok' if ok else 'FAIL', flush=True)
print('C++ brute force agrees with Python definition-level brute force' if ok else 'FAILURES')
