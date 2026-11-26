#!/usr/bin/env python3
"""Compare the author's multiset_dp.magnified_pf (verbatim copy in author_copy/) with the referee's
brute force (bf.py) on systems chosen to stress symmetric cases.  Letter-independent models only,
because the author's implementation has no letter dependence."""
import sys, time, itertools
from fractions import Fraction
sys.dont_write_bytecode = True
sys.path.insert(0, 'author_copy')
import multiset_dp as A
import bf

def mk_models():
    ms = []
    # 1 unit
    ms.append(('unit', lambda u: Fraction(1), lambda a, b: Fraction(1), 1, 1, 1))
    # 2 sizes
    def hp(u): return Fraction(u + 2, 7)
    def il(l1, l2):
        if l1 == 0 and l2 == 0: return Fraction(5, 2)
        return Fraction(3, 2 + 3 * (l1 + l2) + 5 * abs(l1 - l2))
    ms.append(('sizes', hp, il, Fraction(2, 3), Fraction(3, 5), Fraction(7, 11)))
    # 3 primes: every loop type gets its own prime-ish weight so that cancellations are unlikely
    P = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    def hp3(u): return Fraction(P[u % 30], P[(u + 7) % 30])
    def il3(l1, l2):
        a, b = min(l1, l2), max(l1, l2)
        return Fraction(P[(3 * a + 5 * b + 1) % 30], P[(a * b + a + 11) % 30])
    ms.append(('primes', hp3, il3, Fraction(127, 131), Fraction(137, 139), Fraction(149, 151)))
    # 4 hp>=3 (zero weights for small hairpins), strong stacks
    def hp4(u): return Fraction(0) if u < 3 else Fraction(1, u)
    def il4(l1, l2):
        if l1 == 0 and l2 == 0: return Fraction(4)
        return Fraction(1, 1 + l1 + l2)
    ms.append(('hp3', hp4, il4, Fraction(1, 2), Fraction(2, 3), Fraction(5, 4)))
    return ms

def run(strands, alphas=(0, 1, 2, 3, -1, -2), orbits=True, models=None, quiet=False):
    species = sorted(set(strands))
    counts = [strands.count(s) for s in species]
    res_ok = True
    for name, hp, il, ma, mb, mc in (models or mk_models()):
        am = A.Model(hp, il, ma, mb, mc)
        bm = bf.Model(lambda u, a, b: hp(u), lambda l1, a1, b1, l2, a2, b2: il(l1, l2), ma, mb, mc, name)
        als = [a for a in alphas if not (name == 'hp3' and a < 0)]
        t0 = time.time()
        st2 = {}
        ref_w = bf.physical_sum_by_words(strands, bm, als, stats=st2)
        st = {}
        if orbits:
            ref_o = bf.physical_sum_by_orbits(strands, bm, als, stats=st)
            assert ref_o == ref_w, ('orbit reference != word reference', strands, name)
        t1 = time.time()
        bad = []
        for a in als:
            dp = A.magnified_pf(species, counts, am, a)
            if dp != ref_w[a]:
                bad.append((a, dp, ref_w[a]))
        t2 = time.time()
        if bad:
            res_ok = False
        if not quiet or bad:
            print(f"{list(zip(species, counts))} model {name}: pairs {st2.get('pairs')} Rhist(Y,S) {st2.get('Rhist_pairs')} orbits {st.get('orbits')} Rhist {st.get('Rhist')}: "
                  f"{'OK' if not bad else 'MISMATCH ' + repr(bad)} [bf {t1-t0:.1f}s dp {t2-t1:.1f}s]", flush=True)
    return res_ok

if __name__ == '__main__':
    cases = [
        ['GC'], ['G'], ['GGACC'], ['GCGC'], ['GGGAAACCC'],
        ['GC'] * 2, ['GC'] * 3, ['GC'] * 4, ['GC'] * 5, ['GC'] * 6,
        ['CG'] * 2, ['CG'] * 3, ['CG'] * 4,
        ['GGCC'] * 2, ['GGCC'] * 3, ['GCGC'] * 2, ['GCGC'] * 3, ['ACGT'] * 2, ['ACGT'] * 3, ['GATC'] * 2, ['GATC'] * 3,
        ['GGATCC'] * 2, ['GCATGC'] * 2,
        ['G', 'C'], ['G', 'C'] * 2, ['GG', 'CC'], ['GG', 'CC'] * 2, ['GG', 'CC'] * 3,
        ['GA', 'TC'] * 2, ['GA', 'TC'] * 3, ['GAC', 'GTC'] * 2, ['GCA', 'TGC'] * 2,
        ['GC', 'GGCC'] * 2, ['GC', 'G', 'C'] * 2, ['GC'] * 4 + ['GGC'] * 2, ['GC'] * 2 + ['G'] * 2, ['GC'] * 2 + ['C'] * 4,
        ['GGC', 'GCC', 'GC'], ['GGC', 'GCC'] * 2,
        ['GA', 'TC', 'GC'] * 2,
    ]
    ok = True
    for st in cases:
        ok &= run(st)
    print('ALL OK' if ok else 'SOME MISMATCH')
