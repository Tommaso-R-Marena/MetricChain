#!/usr/bin/env python3
"""Referee's own DP (mydp.py, written from the document, letter-dependent weights) against the referee's C++
brute force, for letter-dependent models; plus agreement with the author's DP on letter-independent models."""
import sys, time, random
from math import gcd
from fractions import Fraction
sys.dont_write_bytecode = True
sys.path.insert(0, 'author_copy')
import multiset_dp as A
import bf, drv, mydp
from cmp1 import mk_models

def run(species, counts, models, alphas=(0, 1, 2, 3, -1, 6), tlim=200, log=None):
    c = sum(counts)
    g = 0
    for n in counts:
        g = gcd(g, n)
    allok = True
    for m in models:
        try:
            res, nw, ns = drv.brute_mod(species, counts, m, list(alphas), mode=1, timeout=tlim)
        except Exception as ex:
            print('SKIPPED', species, counts, m.name, flush=True)
            continue
        q = drv.Q_from_T(res, c, alphas)
        bad = []
        for t, a in enumerate(alphas):
            if mydp.F1(species, counts, m, a) != drv.F_from_T(res, 1, t):
                bad.append(('F1', a))
            for d in range(2, g + 1):
                if g % d == 0 and mydp.Fd(species, counts, m, a, d) != drv.F_from_T(res, d, t):
                    bad.append(('F%d' % d, a))
            if mydp.magnified_pf(species, counts, m, a) != q[a]:
                bad.append(('Q', a))
        msg = f"{list(zip(species, counts))} {m.name}: structs {ns} pairs-by-R {dict((R, v[0]) for R, v in sorted(res.items()))}: {'OK' if not bad else 'MISMATCH ' + repr(bad)}"
        print(msg, flush=True)
        if log:
            log.write(msg + '\n'); log.flush()
        allok &= not bad
    return allok

if __name__ == '__main__':
    part = sys.argv[1] if len(sys.argv) > 1 else 'fixed'
    lm = [bf.model_letters(1), bf.model_letters(2), bf.model_letters(3)]
    ok = True
    if part == 'indep':
        # my DP against the author's DP, letter-independent models
        n = 0
        for sp, ct in [(['GC'], [2]), (['GC'], [6]), (['GGCC'], [4]), (['ACGT'], [6]), (['GAC', 'GTC'], [4, 4]), (['GGC', 'GCC'], [2, 4]), (['G', 'GCC'], [6, 6]), (['GA', 'TC', 'GC'], [2, 2, 2]),
                       (['GCGC', 'GC'], [2, 4]), (['GGGAAACCCAGGGAAACCC'], [1]), (['GCAAAGC'], [3]), (['G', 'C', 'GC', 'GGCC'], [2, 2, 2, 2]), (['GGAACC', 'GC'], [2, 2])]:
            for name, hp, il, ma, mb, mc in mk_models():
                am = A.Model(hp, il, ma, mb, mc)
                bm = bf.Model(lambda u, a, b: hp(u), lambda l1, a1, b1, l2, a2, b2: il(l1, l2), ma, mb, mc, name)
                for a in (0, 1, 2, 3, 7) + (() if name == 'hp3' else (-1, -2)):
                    x = drv.fmod(A.magnified_pf(sp, ct, am, a)); y = mydp.magnified_pf(sp, ct, bm, a)
                    n += 1
                    if x != y:
                        ok = False; print('DIFF author vs referee DP', sp, ct, name, a)
        print('referee DP vs author DP on letter-independent models:', n, 'comparisons,', 'ALL EQUAL' if ok else 'DIFFERENCES')
    elif part == 'fixed':
        cases = [(['GC'], [n]) for n in range(1, 9)] + [(['GGCC'], [n]) for n in range(1, 6)] + [(['GCGC'], [n]) for n in range(2, 5)] + \
                [(['ACGT'], [n]) for n in range(2, 7)] + [(['GATC'], [n]) for n in range(2, 7)] + [(['GGATCC'], [n]) for n in range(2, 4)] + \
                [(['GCATGC'], [n]) for n in range(2, 4)] + [(['AGCT'], [n]) for n in range(2, 7)] + [(['GTAC'], [n]) for n in range(2, 6)] + \
                [(['TGCA'], [n]) for n in range(2, 6)] + [(['CATG'], [n]) for n in range(2, 6)] + [(['GAGCTC'], [2]), (['GAGCTC'], [3]), (['AGGCCT'], [2]), (['CTGCAG'], [3]), (['GAATTC'], [2]), (['GAATTC'], [3])] + \
                [(['GGC'], [n]) for n in range(2, 7)] + [(['GCAAAGC'], [2]), (['GCAAAGC'], [3]), (['GCTTTTGC'], [2]), (['GGGAAACCCAGGGAAACCC'], [1]), (['GCGAAGCTTGC'], [1]), (['GCGAAGCTTGC'], [2])]
        for sp in [('GA', 'TC'), ('GAC', 'GTC'), ('GGC', 'GCC'), ('GC', 'GGCC'), ('GCA', 'TGC'), ('G', 'GCC'), ('C', 'GGC'), ('AGC', 'GCT'), ('GAAC', 'GTTC'), ('GCGC', 'GC'), ('AT', 'GATC'), ('ACGT', 'CG')]:
            for ct in [(1, 1), (2, 2), (3, 3), (2, 4), (4, 2), (4, 4), (6, 2), (2, 6), (6, 3), (3, 6), (5, 5), (6, 6), (1, 2), (3, 2)]:
                if sum(len(s) * n for s, n in zip(sp, ct)) <= 24:
                    cases.append((list(sp), list(ct)))
        for sp in [('GA', 'TC', 'GC'), ('GAC', 'GTC', 'GC'), ('GA', 'TC', 'GATC'), ('AG', 'CT', 'AGCT')]:
            for ct in [(1, 1, 1), (2, 2, 2), (2, 2, 4), (4, 2, 2), (3, 3, 3), (4, 4, 4), (2, 4, 6), (1, 2, 3)]:
                if sum(len(s) * n for s, n in zip(sp, ct)) <= 24:
                    cases.append((list(sp), list(ct)))
        for sp in [('GA', 'TC', 'CA', 'TG'), ('G', 'C', 'GC', 'GGCC'), ('GA', 'TC', 'GC', 'AT')]:
            for ct in [(1, 1, 1, 1), (2, 2, 2, 2), (3, 3, 3, 3)]:
                if sum(len(s) * n for s, n in zip(sp, ct)) <= 24:
                    cases.append((list(sp), list(ct)))
        print(len(cases), 'cases', flush=True)
        with open('cmp4_fixed.log', 'w') as log:
            for sp, ct in cases:
                ok &= run(sp, ct, lm, log=log)
            log.write('ALL OK\n' if ok else 'SOME MISMATCH\n')
    else:
        import cmp3_random
        seed = int(part)
        rng = random.Random(seed)
        with open('cmp4_seed%d.log' % seed, 'w') as log:
            for it in range(int(sys.argv[2])):
                sp, ct = cmp3_random.rand_case(rng)
                ok &= run(sp, ct, lm[:2], tlim=100, log=log)
            log.write('ALL OK\n' if ok else 'SOME MISMATCH\n')
    print('ALL OK' if ok else 'SOME MISMATCH')
