#!/usr/bin/env python3
"""Referee R8 -- the binomial-median fact (Me) used in Lemma K.4(b):
     P(Bin(m,p) >= k) >= 1/2  for every integer k <= m p.
It is enough to check k = floor(m p).  Exact integer arithmetic, p = i/D rational.
Also reports the infimum found (how close to 1/2 the probability gets) and the companion
P(Bin(m,p) <= ceil(mp)) >= 1/2 (the other half of the Kaas-Buhrman statement
"every median lies in [floor(mp), ceil(mp)]")."""
import sys, time, random
from math import comb
from fractions import Fraction as Fr
t0 = time.time()
viol = 0; ncase = 0; worst = (Fr(1), None)
def check(m, num, den):
    global viol, ncase, worst
    # P(X=j) = C(m,j) num^j (den-num)^(m-j) / den^m
    k = (m * num) // den
    tot = den ** m
    lo = 0   # sum_{j<k}
    q = den - num
    for j in range(0, k):
        lo += comb(m, j) * num ** j * q ** (m - j)
    upper = tot - lo           # P(X >= k) * tot
    ncase += 1
    if 2 * upper < tot:
        viol += 1; print("VIOLATION P(X>=floor(mp))<1/2:", m, num, den)
    f = Fr(upper, tot)
    if f < worst[0]:
        worst = (f, (m, num, den))
    kc = -((-m * num) // den)   # ceil
    le = lo
    for j in range(k, kc + 1):
        le += comb(m, j) * num ** j * q ** (m - j)
    if 2 * le < tot:
        viol += 1; print("VIOLATION P(X<=ceil(mp))<1/2:", m, num, den)
for D in (64, 97, 30):
    for m in range(1, 241):
        for i in range(1, D):
            check(m, i, D)
random.seed(8)
for _ in range(3000):
    m = random.randint(1, 1500); D = random.randint(2, 10**6); i = random.randint(1, D - 1)
    check(m, i, D)
print("cases:", ncase, " violations:", viol, " smallest P(X>=floor(mp)) = %.6f at (m,p)=%s" % (float(worst[0]), worst[1]),
      " [%.0fs]" % (time.time() - t0))
