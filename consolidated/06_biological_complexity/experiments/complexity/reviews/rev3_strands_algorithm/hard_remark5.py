#!/usr/bin/env python3
"""Remark 5 of STRANDS_NN_HARDNESS.md (several complexes): template + a subset J of the items in one complex,
the other items free; energy = sum of loop energies + |J| * dG_assoc."""
import itertools, sys
from fractions import Fraction as F
from hard_test import cache_structures, E_T1, Til_bruteforce

insts = [((2, 2, 2), 2, 3), ((2, 2), 2, 2), ((1, 3), 2, 2), ((3, 3), 2, 3), ((1, 2, 3), 2, 3), ((2, 4), 2, 3), ((2, 2, 2), 3, 2), ((4, 2), 3, 2),
         ((2, 2, 4), 2, 4), ((2, 3, 3), 2, 4), ((3, 5), 2, 4), ((2, 2, 2, 2), 2, 4), ((3, 3, 2), 4, 2), ((2, 2, 5), 3, 3), ((3, 3, 3), 3, 3)]
sigma = F(-1)
models = [('H2: bulge 0', lambda uC, uT: F(0)), ("H2': (uC+1)sigma + 1/10", lambda uC, uT: (uC + 1) * sigma + F(1, 10))]
subcache = {}
def minE(aJ, m, B, bulge):
    key = (tuple(sorted(aJ)), m, B)
    if key not in subcache:
        subcache[key] = cache_structures(list(key[0]), m, B) if aJ else None
    c = subcache[key]
    if c is None:
        return F(0)          # template alone, no pairs possible
    if not c:
        return None          # no connected structure
    return min(E_T1(sig, sigma, bulge) for sig in c)

bad = 0
for a, m, B in insts:
    n = len(a)
    solvable = Til_bruteforce(a, m, B) > 0
    for name, bulge in models:
        # accounting inequality for sub-systems
        table = {}
        for r in range(0, n + 1):
            for J in sorted(set(tuple(sorted(a[i] for i in idx)) for idx in itertools.combinations(range(n), r))):
                e = minE(J, m, B, bulge)
                table[J] = e
                if e is not None and e < sigma * sum(x - 1 for x in J):
                    bad += 1
                    print('ACCOUNTING VIOLATED', a, m, B, J, e)
        for assoc in (F(-1, 2), F(0), F(1, 2), F(9, 10), F(1), F(3, 2), F(5, 2)):
            cond = all(abs(sigma) * (x - 1) > assoc for x in a)
            Estar = sigma * (m * B - n) + n * assoc
            best = min((e + len(J) * assoc, len(J) == n) for J, e in table.items() if e is not None)
            full = table[tuple(sorted(a))]
            full_tot = None if full is None else full + n * assoc
            # claim under cond: every (J,S) with J != all has energy > E*; so MFE == E* iff solvable
            minproper = min(e + len(J) * assoc for J, e in table.items() if e is not None and len(J) < n)
            ok = (minproper > Estar) if cond else True
            mfe = min(minproper, full_tot) if full_tot is not None else minproper
            equiv = ((mfe == Estar) == solvable) and mfe >= Estar
            if cond and not (ok and equiv):
                bad += 1
                print('REMARK 5 VIOLATED', a, m, B, name, assoc)
            if (a, m, B) == ((2, 2, 2), 2, 3) or (not cond and not equiv):
                print(f'{a} m={m} B={B} {name} assoc={assoc}: condition |sigma|(a_i-1)>assoc {cond}; E*={Estar}; min over proper J {minproper}; all items {full_tot}; solvable {solvable}; "MFE<=E* iff solvable" {equiv}')
print('violations:', bad)
