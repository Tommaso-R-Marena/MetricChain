#!/usr/bin/env python3
"""Author's multiset_dp (verbatim copy) vs the referee's C++ brute force, modulo 2^61-1, on larger systems
that stress the symmetric cases.  Compares G1, every Gd, and magnified_pf.  Letter-independent models."""
import sys, time, json
from fractions import Fraction
from math import gcd
sys.dont_write_bytecode = True
sys.path.insert(0, 'author_copy')
import multiset_dp as A
import bf, drv
from cmp1 import mk_models

TLIM = 240

def fm(x):
    return drv.fmod(x)

def run(species, counts, alphas=(0, 1, 2, 3, -1, -2, 5), log=None, models=None):
    c = sum(counts)
    g = 0
    for n in counts:
        g = gcd(g, n)
    allok = True
    for name, hp, il, ma, mb, mc in (models or mk_models()):
        am = A.Model(hp, il, ma, mb, mc)
        bm = bf.Model(lambda u, a, b: hp(u), lambda l1, a1, b1, l2, a2, b2: il(l1, l2), ma, mb, mc, name)
        als = [a for a in alphas if not (name == 'hp3' and a < 0)]
        t0 = time.time()
        try:
            res, nw, ns = drv.brute_mod(species, counts, bm, als, mode=1, timeout=TLIM)
        except Exception as ex:
            msg = f"{list(zip(species, counts))} {name}: SKIPPED (brute force exceeded {TLIM}s)"
            print(msg, flush=True)
            if log:
                log.write(msg + '\n'); log.flush()
            break
        t1 = time.time()
        q = drv.Q_from_T(res, c, als)
        bad = []
        for t, a in enumerate(als):
            if fm(A.G1(species, counts, am, a)) != drv.F_from_T(res, 1, t):
                bad.append(('G1', a))
            for d in A.divisors(g):
                if d >= 2 and fm(A.Gd(species, counts, am, a, d)) != drv.F_from_T(res, d, t):
                    bad.append(('G%d' % d, a))
            if fm(A.magnified_pf(species, counts, am, a)) != q[a]:
                bad.append(('Q', a))
        t2 = time.time()
        msg = f"{list(zip(species, counts))} {name}: words {nw} structs {ns} pairs-by-R {dict((R, v[0]) for R, v in sorted(res.items()))}: {'OK' if not bad else 'MISMATCH ' + repr(bad)} [bf {t1-t0:.1f}s dp {t2-t1:.1f}s]"
        print(msg, flush=True)
        if log:
            log.write(msg + '\n'); log.flush()
        allok &= not bad
    return allok

if __name__ == '__main__':
    cases = []
    for w in ['GC', 'CG']:
        for n in range(2, 11):
            cases.append(([w], [n]))
    for w, top in [('GGCC', 6), ('GCGC', 5), ('ACGT', 7), ('GATC', 7), ('GGATCC', 4), ('GCATGC', 4), ('GGGCCC', 4), ('GCGCGC', 4),
                   ('GGC', 7), ('GCC', 7), ('GAGCTC', 4), ('GCAAAGC', 3), ('GGAAACC', 3), ('GCTTTTGC', 3), ('GAC', 6), ('GTAC', 6), ('CATG', 6), ('GCG', 8), ('GGCGCC', 3)]:
        for n in range(2, top + 1):
            cases.append(([w], [n]))
    two = [('GA', 'TC'), ('GG', 'CC'), ('GAC', 'GTC'), ('GGC', 'GCC'), ('GC', 'GGCC'), ('GCA', 'TGC'), ('G', 'GCC'), ('C', 'GGC'), ('G', 'CC'), ('GC', 'G'), ('GCGC', 'GC'), ('AGC', 'GCT'), ('GAAC', 'GTTC')]
    cnts2 = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (3, 3), (2, 4), (4, 2), (4, 4), (6, 2), (2, 6), (6, 3), (3, 6), (6, 4), (4, 6), (5, 5), (6, 6), (8, 4), (4, 8), (8, 8), (9, 3), (9, 6), (10, 5), (12, 6), (12, 12)]
    for sp in two:
        for ct in cnts2:
            N = sum(len(s) * n for s, n in zip(sp, ct))
            if N <= 26:
                cases.append((list(sp), list(ct)))
    three = [('GA', 'TC', 'GC'), ('G', 'C', 'GC'), ('GG', 'CC', 'GC'), ('GAC', 'GTC', 'GC'), ('GA', 'TC', 'GATC')]
    cnts3 = [(1, 1, 1), (2, 2, 2), (2, 2, 4), (4, 2, 2), (4, 4, 2), (3, 3, 3), (6, 3, 3), (3, 3, 6), (4, 4, 4), (6, 6, 6), (2, 4, 6), (1, 2, 3), (2, 1, 2)]
    for sp in three:
        for ct in cnts3:
            N = sum(len(s) * n for s, n in zip(sp, ct))
            if N <= 24:
                cases.append((list(sp), list(ct)))
    four = [('GA', 'TC', 'GC', 'AT'), ('G', 'C', 'GC', 'GGCC'), ('GA', 'TC', 'CA', 'TG')]
    for sp in four:
        for ct in [(1, 1, 1, 1), (2, 2, 2, 2), (2, 2, 4, 4), (3, 3, 3, 3), (2, 4, 2, 4)]:
            N = sum(len(s) * n for s, n in zip(sp, ct))
            if N <= 24:
                cases.append((list(sp), list(ct)))
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else len(cases)
    print(len(cases), 'cases; running', lo, hi, flush=True)
    ok = True
    with open('cmp2_%d_%d.log' % (lo, hi), 'w') as log:
        for sp, ct in cases[lo:hi]:
            ok &= run(sp, ct, log=log)
        log.write('ALL OK\n' if ok else 'SOME MISMATCH\n')
    print('ALL OK' if ok else 'SOME MISMATCH')
