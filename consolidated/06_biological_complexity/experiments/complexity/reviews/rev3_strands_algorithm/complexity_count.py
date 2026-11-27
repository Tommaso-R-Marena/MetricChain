#!/usr/bin/env python3
"""Empirical operation counts of the author's implementation against the bound of Theorem 1.
Proxy for 'operations': number of calls of Tables.can (one per candidate pair examined in the innermost loops)
plus number of sub-multiset pairs generated.  Bound: L0^4 * sum_{d | gcd} prod_i C(n_i/d + 2, 2)."""
import sys, time, math
from fractions import Fraction
sys.dont_write_bytecode = True
sys.path.insert(0, 'author_copy')
import multiset_dp as A

class Counter:
    can = 0
    subs = 0
orig_can = A.Tables.can
orig_sub = A.Tables.submultisets
def can(self, s, i, t, j):
    Counter.can += 1
    return orig_can(self, s, i, t, j)
def subm(self, Am):
    for x in orig_sub(self, Am):
        Counter.subs += 1
        yield x
A.Tables.can = can
A.Tables.submultisets = subm
m = A.Model(lambda u: Fraction(1), lambda a, b: Fraction(1), 1, 1, 1)

def bound(species, counts):
    L0 = sum(len(s) for s in species)
    g = 0
    for n in counts: g = math.gcd(g, n)
    tot = 0
    for d in range(1, g + 1):
        if g % d == 0:
            p = 1
            for n in counts: p *= math.comb(n // d + 2, 2)
            tot += p
    return L0 ** 4 * tot, L0, tot

print('species counts | L0 | sum_d prod C(n_i/d+2,2) | can-calls | submultiset pairs | (can+subs)/(L0^4 * sum) | seconds')
for species, cl in [(['GGC', 'GCC'], [(1, 1), (2, 2), (3, 3), (4, 4), (6, 6), (8, 8), (12, 12), (16, 16)]),
                    (['GGC'], [(1,), (2,), (4,), (8,), (16,), (32,), (64,)]),
                    (['GA', 'TC', 'GC'], [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4), (6, 6, 6)]),
                    (['GGCGCC', 'GCGGCC'], [(1, 1), (2, 2), (4, 4)]),
                    (['GGCGCCAAGGCC', 'GCC'], [(1, 1), (1, 4), (2, 8)]),
                    ]:
    for ct in cl:
        Counter.can = Counter.subs = 0
        t0 = time.time()
        A.magnified_pf(species, list(ct), m, 1)
        b, L0, tot = bound(species, ct)
        print(species, ct, '|', L0, '|', tot, '|', Counter.can, '|', Counter.subs, '| %.4f' % ((Counter.can + Counter.subs) / b), '| %.1f' % (time.time() - t0), flush=True)
# distinct strands: 3^c
import itertools, random
rng = random.Random(5)
for c in (2, 3, 4, 5, 6, 7, 8):
    species = []
    while len(species) < c:
        w = ''.join(rng.choice('GC') for _ in range(3))
        if w not in species: species.append(w)
    Counter.can = Counter.subs = 0
    t0 = time.time()
    A.magnified_pf(species, [1] * c, m, 1)
    b, L0, tot = bound(species, [1] * c)
    print('distinct strands c=%d' % c, '|', L0, '|', tot, '(3^c = %d)' % 3 ** c, '|', Counter.can, '|', Counter.subs, '| %.4f' % ((Counter.can + Counter.subs) / b), '| %.1f' % (time.time() - t0), flush=True)
