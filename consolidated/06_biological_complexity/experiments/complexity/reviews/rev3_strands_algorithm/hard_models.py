#!/usr/bin/env python3
"""Referee's model sweep for Theorems 1, 1c, 1d of STRANDS_NN_HARDNESS.md on the cached enumerations
(hard_test.py).  Exact rational arithmetic."""
import pickle, sys, itertools
from fractions import Fraction as F
from hard_test import E_T1, E_T1c, E_T1d, INSTANCES

cache = pickle.load(open('hard_cache.pkl', 'rb'))
insts = [i for i in INSTANCES if i in cache]
print(len(insts), 'instances,', sum(sum(v.values()) for v in cache.values()), 'structures')

def check(inst, efun, Estar, eps):
    """returns (ok, tiling energies set, min non-tiling energy - Estar)"""
    til_e = set()
    omin = None
    for sig, cnt in cache[inst].items():
        e = efun(sig)
        if sig[0]:
            til_e.add(e)
        else:
            omin = e if omin is None else min(omin, e)
    ok = all(e == Estar for e in til_e) and (omin is None or omin >= Estar + eps)
    return ok, til_e, (None if omin is None else omin - Estar)

def M_of(inst):
    a, m, B = inst
    return m * B - len(a)

# ---------------------------------------------------------------- Theorem 1
print('\n=== Theorem 1: (H0),(H1),(H2\') ===')
for sigma in (F(-1), F(-3, 2)):
    for label, delta, bulge in [
        ('bulge = (uC+1)sigma + delta, delta=1/100', F(1, 100), lambda uC, uT, s=sigma: (uC + 1) * s + F(1, 100)),
        ('bulge = (uC+1)sigma + delta, delta=1/2', F(1, 2), lambda uC, uT, s=sigma: (uC + 1) * s + F(1, 2)),
        ('bulge = (uC+1)sigma + delta, delta=|sigma|', -sigma, lambda uC, uT, s=sigma: (uC + 1) * s - s),
        ('bulge = (uC+1)sigma + 5', F(5), lambda uC, uT, s=sigma: (uC + 1) * s + 5),
        ('bulge = 0 (H2), delta=|sigma|', -sigma, lambda uC, uT: F(0)),
        ('bulge = (uC+1)sigma + 1/7 + uT/3 (depends on template side)', F(1, 7), lambda uC, uT, s=sigma: (uC + 1) * s + F(1, 7) + F(uT, 3)),
        ('CONTROL bulge = (uC+1)sigma (delta = 0)', F(0), lambda uC, uT, s=sigma: (uC + 1) * s),
        ('CONTROL bulge = (uC+1)sigma - 1/10', F(-1, 10), lambda uC, uT, s=sigma: (uC + 1) * s - F(1, 10)),
        ('CONTROL bulge = sigma + 1/2 regardless of uC (violates H2\' when uC>=1 ... only if (uC+1)sigma+delta > sigma+1/2)', None, lambda uC, uT, s=sigma: s + F(1, 2)),
    ]:
        fails = []
        mingap = None
        for inst in insts:
            Estar = sigma * M_of(inst)
            eps = min(delta, -sigma) if delta is not None and delta > 0 else F(1, 10**9)
            ok, til_e, gap = check(inst, lambda sig: E_T1(sig, sigma, bulge), Estar, eps)
            if not ok:
                fails.append((inst, sorted(til_e), gap))
            if gap is not None:
                mingap = gap if mingap is None else min(mingap, gap)
        print(f'sigma={sigma} {label}: failures {len(fails)}; min over instances of (min non-tiling E - E*) = {mingap}' + (f'; first failures {fails[:3]}' if fails else ''))

# ---------------------------------------------------------------- Theorem 1c
print('\n=== Theorem 1c: flush coaxial stacking, sigma = -1, bulge/interior = gamma exactly ===')
sigma = F(-1)
xs = [F(0), F(-1, 2), F(-9, 10), F(-1), F(-11, 10), F(-3, 2), F(-19, 10), F(-2), F(-5, 2)]
gs = [F(0), F(1, 10), F(1, 2), F(1), F(3, 2), F(2), F(3)]
print('rows x, columns gamma =', [str(g) for g in gs])
print('entry: H = hypothesis holds; h = hypothesis fails; then ok/FAIL(n) = conclusion (tiling <=> E = E*_x, others >= E*_x + eps_x resp. > E*_x) on instances with B>=2')
disagree = 0
for x in xs:
    row = []
    for gamma in gs:
        hyp = abs(x) < abs(sigma) + min(abs(sigma), gamma)
        if abs(x) < abs(sigma):
            eps = abs(sigma) - abs(x)
        else:
            eps = min(abs(sigma), gamma) - (abs(x) - abs(sigma))
        nf = 0
        firstfail = None
        for inst in insts:
            a, m, B = inst
            if B < 2:
                continue
            Estar = sigma * M_of(inst) + x * (len(a) - m)
            ok, til_e, gap = check(inst, lambda sig: E_T1c(sig, sigma, x, lambda uC, uT: gamma), Estar, eps if hyp else F(1, 10**9))
            if not ok:
                nf += 1
                if firstfail is None:
                    firstfail = (inst, gap)
        row.append(('H' if hyp else 'h') + (' ok' if nf == 0 else ' FAIL(%d)' % nf))
        if hyp and nf:
            disagree += 1
            print('   !!! hypothesis holds but conclusion fails: x', x, 'gamma', gamma, firstfail)
        if (not hyp) and nf == 0:
            print('   note: hypothesis fails but no failing instance found: x', x, 'gamma', gamma)
    print(f'x={str(x):>6}: ' + ' | '.join(row))
print('violations of Theorem 1c:', disagree)

print('\n--- Theorem 1c on B = 1 instances (allowed only for |x| < |sigma|) ---')
for x in xs:
    for gamma in (F(0), F(1, 2), F(2)):
        hyp = abs(x) < abs(sigma) + min(abs(sigma), gamma)
        eps = abs(sigma) - abs(x) if abs(x) < abs(sigma) else min(abs(sigma), gamma) - (abs(x) - abs(sigma))
        res = []
        for inst in insts:
            a, m, B = inst
            if B != 1:
                continue
            Estar = sigma * M_of(inst) + x * (len(a) - m)
            ok, til_e, gap = check(inst, lambda sig: E_T1c(sig, sigma, x, lambda uC, uT: gamma), Estar, eps if eps > 0 else F(1, 10**9))
            if not ok:
                res.append((inst, gap))
        print(f'x={x} gamma={gamma} hyp(|x|<|s|+min)={hyp} |x|<|sigma|={abs(x) < abs(sigma)}: failing B=1 instances: {res[:4]}')

# gamma depending on sizes, still >= gamma
print('\n--- Theorem 1c with bulge = gamma + uT/5 + uC/3 ---')
for x, gamma in [(F(-1), F(1, 10)), (F(-3, 2), F(3, 4)), (F(-19, 10), F(1)), (F(-1, 2), F(0)), (F(-1), F(1, 1000))]:
    eps = abs(sigma) - abs(x) if abs(x) < abs(sigma) else min(abs(sigma), gamma) - (abs(x) - abs(sigma))
    nf = 0; mg = None
    for inst in insts:
        a, m, B = inst
        if B < 2 and abs(x) >= abs(sigma):
            continue
        Estar = sigma * M_of(inst) + x * (len(a) - m)
        ok, til_e, gap = check(inst, lambda sig: E_T1c(sig, sigma, x, lambda uC, uT: gamma + F(uT, 5) + F(uC, 3)), Estar, eps)
        nf += (not ok)
        if gap is not None:
            mg = gap if mg is None else min(mg, gap)
    print(f'x={x} gamma={gamma}: eps_x={eps} failures {nf}, min gap observed {mg}')

# ---------------------------------------------------------------- Theorem 1d
print('\n=== Theorem 1d: dangles, sigma = -1, (H2) bulge >= 0 ===')
for DG, DC in [(F(0), F(0)), (F(1, 4), F(1, 4)), (F(2, 5), F(1, 2)), (F(9, 10), F(0)), (F(0), F(9, 10)), (F(1, 2), F(1, 2)), (F(3, 5), F(1, 2)), (F(1), F(0)), (F(0), F(1)), (F(0), F(6, 5))]:
    for eA in (F(0), F(-1, 3), F(-2)):
        for eA1 in sorted({eA, eA / 2, F(0)}):
            for bl, bulge in (('0', lambda uC, uT: F(0)), ('1/3', lambda uC, uT: F(1, 3))):
                hyp = abs(sigma) > DG + DC
                eps = abs(sigma) - DG - DC
                nf = 0; mg = None; ff = None
                for inst in insts:
                    a, m, B = inst
                    Estar = sigma * M_of(inst) + (m - 1) * eA
                    ok, til_e, gap = check(inst, lambda sig: E_T1d(sig, sigma, DG, DC, eA, eA1, bulge), Estar, eps if hyp else F(1, 10**9))
                    if not ok:
                        nf += 1
                        if ff is None:
                            ff = (inst, sorted(til_e), gap)
                    if gap is not None:
                        mg = gap if mg is None else min(mg, gap)
                flag = ''
                if hyp and nf:
                    flag = '   !!! VIOLATION ' + repr(ff)
                if (not hyp) and nf == 0:
                    flag = '   (hypothesis fails, no failing instance)'
                if flag or (eA1 == eA and bl == '0'):
                    print(f'DG={DG} DC={DC} eA={eA} eA(one paired nb)={eA1} bulge={bl}: hyp={hyp} eps={eps} failures={nf} min gap={mg}{flag}')
