#!/usr/bin/env python3
"""Theorem 1e in its SECOND form (commit 89114ea, made while this review was running; outside the brief):
hypothesis D_C + max(D_G, |x|/B) < |sigma| and |sigma| - |x| + gamma + |e_A| > 0, sigma <= x <= 0, B >= 2;
gap min(|sigma| - D_C - max(D_G,|x|/B), |sigma| - |x| + gamma + |e_A|)."""
import pickle
from fractions import Fraction as F
from hard_test import INSTANCES
cache = pickle.load(open('hard_cache.pkl', 'rb'))
sigma = F(-1)
def E(sig, x, gamma, DG, DC, eA, eA1):
    til, nst, bul, nfl, dG, dC, dA2, dA1 = sig
    return sigma * nst + x * nfl + gamma * len(bul) - DG * dG - DC * dC + eA * dA2 + eA1 * dA1
viol = 0; ninside = 0; out_fail = {}
params = []
for x in (F(0), F(-1, 2), F(-1)):
    for gamma in (F(0), F(1, 10), F(1)):
        for DG, DC in ((F(0), F(0)), (F(2, 5), F(2, 5)), (F(1, 2), F(2, 5)), (F(0), F(2, 3)), (F(0), F(5, 6)), (F(9, 10), F(0)), (F(1, 3), F(3, 5)), (F(1, 2), F(1, 2))):
            for eA in (F(0), F(-1, 4), F(-2)):
                for eA1 in sorted({eA, F(0)}):
                    params.append((x, gamma, DG, DC, eA, eA1))
for inst in INSTANCES:
    a, m, B = inst
    if B < 2:
        continue
    sigs = list(cache[inst].items())
    for (x, gamma, DG, DC, eA, eA1) in params:
        h1 = DC + max(DG, abs(x) / B) < abs(sigma)
        h2 = abs(sigma) - abs(x) + gamma + abs(eA) > 0
        Estar = sigma * (m * B - len(a)) + x * (len(a) - m) + (m - 1) * eA
        til_e = set(); omin = None
        for sig, cnt in sigs:
            e = E(sig, x, gamma, DG, DC, eA, eA1)
            if sig[0]: til_e.add(e)
            else: omin = e if omin is None else min(omin, e)
        if h1 and h2:
            ninside += 1
            eps = min(abs(sigma) - DC - max(DG, abs(x) / B), abs(sigma) - abs(x) + gamma + abs(eA))
            if not (all(e == Estar for e in til_e) and (omin is None or omin >= Estar + eps)):
                viol += 1
                print('VIOLATION of Theorem 1e (v2)', inst, x, gamma, DG, DC, eA, eA1, omin, Estar, eps, flush=True)
        else:
            okc = all(e == Estar for e in til_e) and (omin is None or omin > Estar)
            key = (x, gamma, DG, DC, eA, eA1, B)
            d = out_fail.setdefault(key, [0, 0]); d[0] += 1; d[1] += (not okc)
print('Theorem 1e (second form): (instance, model) pairs inside the hypotheses:', ninside, '; violations:', viol)
# the author's sharpness claim: x = sigma, D_G = 0, D_C = 2/3 or 5/6 fails on instances with B = 2
for DC in (F(2, 3), F(5, 6)):
    for B in (2, 3, 4, 5):
        tot = [0, 0]
        for key, d in out_fail.items():
            if key[0] == F(-1) and key[2] == 0 and key[3] == DC and key[6] == B:
                tot[0] += d[0]; tot[1] += d[1]
        print('  x = sigma, D_G = 0, D_C = %s, B = %d: (instance, model) pairs outside the hypotheses %d, conclusion fails in %d' % (DC, B, tot[0], tot[1]))
