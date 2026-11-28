"""Additional Lemma B cases: small slopes (large N_u), odd block sizes, blocks exactly at N_u, five blocks,
and budgets at the minimum allowed by the lemma.  Compact output: only the extreme values per group."""
import itertools
import math
import time
import numpy as np
from r2_lemmaB import extremal
from rv_common import consts

t0 = time.time()
tot = 0
gmax = (-1e300, None)
gmaxh = (-1e300, None)
gworst = (-1e300, None)
groups = []
# (u, list of block-size tuples, role patterns, multipliers of n h added to the minimal budget)
import sys
ALL = ((0.25, [(81, 81), (83, 162), (81, 81, 82)]),
       (0.5, [(41, 41), (43, 82), (123, 41, 42), (41, 41, 41), (61, 83, 41)]),
       (3.0, [(9, 9, 9, 9, 9), (9, 10, 11, 12, 13), (27, 9, 18, 9)]),
       (12.0, [(6, 6, 6, 6, 6), (6, 7, 8, 9, 10), (30, 6, 12)]))
want = [float(x) for x in sys.argv[1:]]
for u, sizes in [g for g in ALL if (not want or g[0] in want)]:
    c = consts(u)
    assert all(min(s) >= c['Nu'] for s in sizes)
    lmax = -1e300
    for ns in sizes:
        m = len(ns)
        n = sum(ns)
        L = math.log(n + 1.0)
        pats = [''.join(p) for p in itertools.product('PQT', repeat=m)]
        if len(pats) > 40:
            rng = np.random.default_rng(5)
            pats = list(rng.choice(pats, size=40, replace=False))
        for roles in pats:
            for mult in (0.0, 0.5, 2.0):
                Theta = n * c['h'] + 2 * m * L + mult * n * c['h']
                o = extremal(list(ns), roles, u, Theta, parity=True)
                tot += 1
                assert o['hyp_Theta'] and o['hyp_N'] and o['lip'] <= u + 1e-9
                lmax = max(lmax, o['X'])
                if o['X'] > gmax[0]:
                    gmax = (o['X'], (u, ns, roles, mult, o['allow']))
                if o['Xhidden'] == o['Xhidden'] and o['Xhidden'] > gmaxh[0]:
                    gmaxh = (o['Xhidden'], (u, ns, roles, mult, o['allow']))
                if o['X'] - o['allow'] > gworst[0]:
                    gworst = (o['X'] - o['allow'], (u, ns, roles, mult, o['allow']))
    print('u=%g (N_u=%d): sizes %s: largest X = %+.3f   [%.0f s]' % (u, c['Nu'], sizes, lmax, time.time() - t0), flush=True)
print('%d cases, all inside the hypotheses of Lemma B (parity version)' % tot)
print('largest X          : %+.3f at (u, ns, roles, mult, allowance) = %s' % gmax)
print('largest X_hidden   : %+.3f at %s' % gmaxh)
print('largest X-allowance: %+.3f at %s  (the lemma requires <= 0)' % gworst)
