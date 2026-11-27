#!/usr/bin/env python3
"""r05_chain_stress.py -- referee: Proposition T away from the design (200 s of random cases): random blocks (from one site), exponents
B' in (0, ln 2], coarse accuracies X > 1, alpha down to 1e-9, u in {0.2, 0.5, 1, 2, 4}, horizons 30..4000.
Every level of every chain: (i), (ii) and the claim t(d, delta) <= d B' + E_T(d; Lam) at its own (d, delta)."""
import math, sys, time, random
sys.dont_write_bytecode = True
import rlib
from rlib import LN2, INF
import r02_chain as R2

random.seed(20261126)
t0 = time.time()
Efs = [None, lambda d, x, Lam: 3 * math.sqrt(d), lambda d, x, Lam: Lam / 7, lambda d, x, Lam: 5 / x + math.log(Lam)]
tot = viol = chains = nclaim = 0
gmin = (INF, None)
minbottom = INF
nontrivial_varpi = 0
for it in range(100000):
    if time.time() - t0 > 200:
        break
    u = random.choice([0.2, 0.5, 1.0, 2.0, 4.0])
    cu = rlib.Cube(u)
    N = random.choice([30, 60, 150, 400, 1000, 2500, 4000])
    Bp = random.choice([cu.h, 0.5 * (cu.h + cu.a), cu.a, 0.5 * (cu.a + LN2), LN2, 0.3 * cu.h])
    alpha = random.choice([1.0, 0.3, 1e-3, 1e-9])
    calX = random.choice([1.01, 3.0, rlib.X_B(cu, N), 40.0])
    m = random.choice([1, 2, 3, 5, 9, 17, 40, 100, 250, 600])
    if m >= N:
        continue
    ld = random.choice([math.log(0.5), math.log(0.05), -30.0, -float(N), -50.0 * N])
    Ef = random.choice(Efs)
    ch = rlib.Chain(cu, N, Bp, calX, alpha, m)
    if ch.d0 > N:
        d = N        # no level: the base family only; check the bottom bound for a few d
        for dd in (1, 2, N // 2, N):
            t, _ = rlib.base_lcost(cu, dd, ch.alow, ld)
            sl = dd * Bp + ch.e0(-ld + dd * LN2) - t
            minbottom = min(minbottom, sl)
            if sl < -1e-9:
                viol += 1
        continue
    r = R2.run_chain(cu, N, Bp, calX, alpha, m, ld, Ef, "", check_every=max(1, ch.j(N) // 40), verbose=False)
    chains += 1
    tot += r['levels']
    nclaim += r['stat']['n']
    viol += r['stat']['viol']
    minbottom = min(minbottom, r['stat'].get('bottom_slack', INF))
    if r['stat']['minslack'] < gmin[0]:
        gmin = (r['stat']['minslack'], (u, N, round(Bp / cu.a, 3), alpha, round(calX, 2), m, round(ld, 1), r['levels'],
                                        round(r['exact'], 2), round(r['bound'], 2)))
    if r['varpi'] < (m + 1) * LN2 - 1e-9:
        nontrivial_varpi += 1
print("chains %d, levels %d (parts (i), (ii) at every level; the claim (iii) at %d levels: >= 40 evenly spaced levels per chain and the last three), violations %d" % (chains, tot, nclaim, viol))
print("least slack of the claim %.3f nats at (u, N, B'/a, alpha, X, m, ln delta, levels, exact - N B', E_T) = %s" % gmin)
print("least slack of the bottom (base family against d B' + e_0): %.3f nats" % minbottom)
print("chains in which varpi is the bound of Lemma Q3 (not the trivial one): %d" % nontrivial_varpi)
print("time %.0f s" % (time.time() - t0))
