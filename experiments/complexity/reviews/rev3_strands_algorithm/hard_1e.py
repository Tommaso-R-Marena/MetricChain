#!/usr/bin/env python3
"""Theorem 1e (added to the note while this review was running; outside the brief): flush coaxial stacking and
dangles together.  Test on the referee's cached enumerations."""
import pickle
from fractions import Fraction as F
from hard_test import INSTANCES
cache = pickle.load(open('hard_cache.pkl', 'rb'))
sigma = F(-1)
def E(sig, x, gamma, DG, DC, eA, eA1):
    til, nst, bul, nfl, dG, dC, dA2, dA1 = sig
    return sigma * nst + x * nfl + gamma * len(bul) - DG * dG - DC * dC + eA * dA2 + eA1 * dA1
viol = 0
rows = []
for x in (F(0), F(-1, 2), F(-9, 10), F(-1)):
    for gamma in (F(0), F(1, 10), F(1)):
        for DG, DC in ((F(0), F(0)), (F(1, 5), F(1, 5)), (F(2, 5), F(2, 5)), (F(1, 2), F(2, 5)), (F(1, 2), F(1, 2))):
            for eA in (F(0), F(-1, 4), F(-2)):
                for eA1 in sorted({eA, F(0)}):
                    nfail = 0; ntest = 0; nfail_out = 0; ntest_out = 0; mg = None
                    for inst in INSTANCES:
                        a, m, B = inst
                        if B < 2:
                            continue
                        h1 = DG + DC < abs(sigma) - abs(x) / B
                        h2 = abs(sigma) - abs(x) + gamma + abs(eA) > 0
                        eps = min(abs(sigma) - abs(x) / B - DG - DC, abs(sigma) - abs(x) + gamma + abs(eA))
                        Estar = sigma * (m * B - len(a)) + x * (len(a) - m) + (m - 1) * eA
                        til_e = set(); omin = None
                        for sig, cnt in cache[inst].items():
                            e = E(sig, x, gamma, DG, DC, eA, eA1)
                            if sig[0]: til_e.add(e)
                            else: omin = e if omin is None else min(omin, e)
                        if h1 and h2:
                            ntest += 1
                            ok = all(e == Estar for e in til_e) and (omin is None or omin >= Estar + eps)
                            if not ok:
                                nfail += 1; viol += 1
                                print('VIOLATION of Theorem 1e', inst, x, gamma, DG, DC, eA, eA1, sorted(til_e), omin, Estar, eps)
                        else:
                            ntest_out += 1
                            ok = all(e == Estar for e in til_e) and (omin is None or omin > Estar)
                            nfail_out += (not ok)
                    rows.append((x, gamma, DG, DC, eA, eA1, ntest, nfail, ntest_out, nfail_out))
print('parameter sets:', len(rows), '; violations inside the hypotheses:', viol)
print('outside the hypotheses (instance-wise): parameter sets with failing instances:', sum(1 for r in rows if r[9] > 0), 'of', sum(1 for r in rows if r[8] > 0))
for r in rows:
    if r[8] > 0 and r[0] == F(-1) and r[5] == r[4]:
        print('  x=%s gamma=%s DG=%s DC=%s eA=%s: inside-hyp instances %d (fail %d); outside-hyp instances %d (conclusion fails on %d)' % (r[0], r[1], r[2], r[3], r[4], r[6], r[7], r[8], r[9]))
