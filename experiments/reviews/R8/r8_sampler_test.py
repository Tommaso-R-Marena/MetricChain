#!/usr/bin/env python3
"""Referee R8 -- self-test of the tail-safe multinomial sampler of r8_pops.py.
(1) small case against numpy's multinomial (chi-square of the marginal means);
(2) N = 2^59 points over the shells of Q_300: the counts of the far-tail shells (expected counts 1e-3 ... 1e6)
    are compared with the exact binomial means and variances; and the same cells with numpy's own samplers,
    to see the trap the report warns of."""
import math, sys, time
import numpy as np
from fractions import Fraction as Fr
from r8_pops import multinomial_shells, binom_safe
t0 = time.time()
rng = np.random.default_rng(20261125)
m = 300
C = [math.comb(m, j) for j in range(m + 1)]
ball = [0]
for c in C: ball.append(ball[-1] + c)
N = 1 << 59
reps = 400
acc = {}
tot_ok = True
TAIL = [d for d in range(m + 1) if 1e-3 <= N * C[d] / 2.0 ** m <= 1e7]
print('tail shells tested:', TAIL[0], '..', TAIL[len(TAIL)//2 - 1], 'and', TAIL[len(TAIL)//2], '..', TAIL[-1])
for rep in range(reps):
    out = {}
    multinomial_shells(rng, N, ball, 0, m, out)
    if sum(out.values()) != N: tot_ok = False
    for d in TAIL:
        acc.setdefault(d, []).append(out.get(d, 0))
print("total preserved in all draws:", tot_ok)
print(" shell   expected      mean(sim)   z(mean)    var/mean   [exact: var/mean = 1-p ~ 1]")
worstz = 0
for d in sorted(acc):
    mu = N * C[d] / 2.0 ** m
    if mu < 1e-3 or mu > 1e7: continue
    x = np.array(acc[d], dtype=float)
    z = (x.mean() - mu) / math.sqrt(mu / reps)
    worstz = max(worstz, abs(z))
    if d % 3 == 0 or abs(z) > 3:
        print("%5d  %11.4g  %11.4g  %7.2f   %8.3f" % (d, mu, x.mean(), z, x.var() / max(mu, 1e-300)))
print("largest |z| over the tail shells with expected count in [1e-3, 1e7]: %.2f" % worstz)
# numpy's own samplers on a far-tail cell
p = C[TAIL[3]] / 2.0 ** m
x = rng.binomial(N, p, size=2000)
print("numpy binomial(2^59, p=%.3g): expected %.4g, mean of 2000 draws %.4g" % (p, N * p, x.mean()))
y = np.array([binom_safe(rng, N, p) for _ in range(2000)])
print("own   binom_safe(2^59, p=%.3g): expected %.4g, mean of 2000 draws %.4g (z=%.2f)" % (p, N * p, y.mean(), (y.mean() - N * p) / math.sqrt(N * p / 2000)))
pv = np.array([c / 2.0 ** m for c in C])
z = rng.multinomial(N, pv, size=200)
for d in (TAIL[1], TAIL[3], TAIL[6], TAIL[10]):
    print("numpy multinomial: shell %d expected %.4g, mean of 200 draws %.4g" % (d, N * pv[d], z[:, d].mean()))
# (1) small case
m2 = 12; C2 = [math.comb(m2, j) for j in range(m2 + 1)]; ball2 = [0]
for c in C2: ball2.append(ball2[-1] + c)
acc2 = np.zeros(m2 + 1)
R = 20000; N2 = 1000
for _ in range(R):
    out = {}
    multinomial_shells(rng, N2, ball2, 0, m2, out)
    for d, v in out.items(): acc2[d] += v
exp2 = np.array(C2) / 2.0 ** m2 * N2 * R
chi = float(np.sum((acc2 - exp2) ** 2 / exp2))
print("small case (m=12, N=1000, 20000 draws): chi-square of shell totals = %.1f on 12 d.o.f." % chi)
print("[%.0fs]" % (time.time() - t0))
