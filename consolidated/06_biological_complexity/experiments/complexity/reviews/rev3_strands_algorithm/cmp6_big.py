#!/usr/bin/env python3
"""A few larger systems with gcd of the copy numbers 4 and 6 and several species (C++ brute force, up to 20 min each)."""
import sys, time
sys.dont_write_bytecode = True
import cmp2
cmp2.TLIM = 1100
from cmp1 import mk_models
cases = [(['GCC', 'GG'], [6, 6]), (['GGC', 'CC'], [6, 6]), (['GCG', 'C'], [6, 6]), (['GA', 'TC', 'GC'], [6, 6, 6]), (['GC', 'GGCC'], [6, 6]), (['GAC', 'GTC'], [6, 6]), (['G', 'C', 'GCGC'], [4, 4, 4]), (['GA', 'TC', 'GC', 'AT'], [4, 4, 4, 4])]
lo, hi = int(sys.argv[1]), int(sys.argv[2])
ok = True
with open('cmp6_%d_%d.log' % (lo, hi), 'w') as log:
    for sp, ct in cases[lo:hi]:
        ok &= cmp2.run(sp, ct, alphas=(0, 1, 2, 3, -1), log=log, models=mk_models()[1:3])
print('ALL OK' if ok else 'SOME MISMATCH')
