#!/usr/bin/env python3
"""RA06 -- the numbers of A8: the bound of Theorem Z' as a formula.

The unrolling below is written by the referee from section 6 of Z_REPORT.md with M_1 = 0 (Theorem Z'):
    Lam := ln(1/delta) + n ln 2;   for j = k, ..., 1:
        chain (B' = b_j, accuracy X = X_0(n) + 1, alpha = min(eps, 1) for j = k, 1 otherwise):  block m by (4.1) of Q2 at Lam;
              Lam <- Lam + j(n) q_T(n, Lam + n b_j);   E += A_T(n, Lam) + j(n) Delta_T(n, Lam) + X + 1
        level:  E += ell_0(n, Lam) + X_0(n) + d_min ln 2 + 2;   Lam <- Lam + q(n, Lam)
    base (Theorem A of Q2 with no epoch, entered with Lam, accuracy 1):  E += E'_0(n; Lam)
    bound:  ln N - n h <= n (b_k - h) + E.
The tops b_k are the referee's (structural envelope sequence, no grid, k <= 600; h + c_*^2/k^2 beyond, as in A8).
The formulas of Q2 (A_T, q_T, Delta_T, the block, ell_0, q, E'_M, and the bounds of Theorem 11.58a / Theorem A that the
table compares with) are taken from the workstream's library q2lib (read-only import) -- they are not re-derived here.
Usage: python3 -B ra06_formula.py
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(HERE, '..', '..', 'Q2'))
import q2lib as Q2      # noqa: E402

import ra_lib as R      # noqa: E402

Q = Q2.Q
LN2 = math.log(2.0)
u = 1.0
P = R.Cube(u).setup()
a, h, c2 = P.a, P.h, P.cstar2
cu = Q.Cube(u)
assert abs(cu.h - h) < 1e-9 and abs(cu.a - a) < 1e-12
KEX = 600
S = R.EnvSeq(P, KEX)
dmin = int(math.floor(1.0 / (2 * u))) + 2


def X0(d):
    return 2.0 + math.log(3.0 * (d + 1)) + 2 * u + math.exp(u)


def b_of(k):
    return S.b[k] if k <= KEX else h + c2 / k ** 2


seq = Q.epoch_seq(cu, 70)
MMAX = len(seq['B']) - 1


def E_env(n, eps, dln, k):
    eh = min(eps, 1.0)
    Lam = dln + n * LN2
    X0n = X0(n)
    calX = X0n + 1.0
    chains = levels = 0.0
    for j in range(k, 0, -1):
        alpha = eh if j == k else 1.0
        Bp = b_of(j)
        m = Q2.Chain.design_m(cu, n, Bp, calX, alpha, Lam)
        ch = Q2.Chain(cu, n, Bp, calX, alpha, m)
        Lam = Lam + ch.j(n) * Q2.qT(cu, n, Lam + n * Bp, ch.c)
        chains += ch.A_T(n, Lam) + ch.j(n) * ch.Delta_T(n, Lam) + calX + 1.0
        levels += Q2.ell0(cu, n, Lam) + X0n + dmin * LN2 + 2.0
        Lam += Q2.qSb(cu, n, Lam)
    base = Q2.E_new(cu, n, 1.0 if k >= 1 else eps, Lam - n * LN2, 0, seq)
    return chains, levels, base


def best_k(n, eps, dln, kmax):
    cand, k = [], 1.0
    while k <= kmax:
        cand.append(int(round(k)))
        k = max(k * 1.05, k + 1)
    best = (math.inf, None)
    for k in sorted(set(cand)):
        c, l, b = E_env(n, eps, dln, k)
        v = n * (b_of(k) - h) + c + l + b
        if v < best[0]:
            best = (v, k, n * (b_of(k) - h), c, l, b)
    return best


def best_M(f, M0):
    bestv, bestM, up = math.inf, None, 0
    for M in range(M0, MMAX):
        v = f(M)
        if v < bestv:
            bestv, bestM, up = v, M, 0
        else:
            up += 1
            if up >= 3:
                break
    return bestv, bestM


dln, eps = math.log(1 / 0.05), 1.0
print("# cube u = 1, delta = 0.05, eps = 1; entries: ln(evaluations) - n h in nats.  Tops: referee's structural sequence (k <= %d)." % KEX)
print("#       n     n(a-h)    Thm 11.58a   Theorem A(Q2)  | envelope schedule: total    k    n(b_k-h)   chains    levels    base   (chains+levels)/(k ln n) | addendum: total (k)")
add = {4: (1025, 2), 4.5: (1627, 3), 5: (2476, 4), 6: (5648, 6), 7: (1.38e4, 12), 8: (3.33e4, 24), 9: (7.87e4, 52), 10: (1.84e5, 104)}
cut = {5: 7466, 6: 1.15e4, 7: 2.52e4, 8: 4.91e4, 9: 9.97e4, 10: 2.10e5, 12: 1.04e6, 15: 1.19e7}
rows = {}
for ex in (4, 4.5, 5, 6, 7, 8, 9, 10):
    n = int(round(10 ** ex))
    vo, Mo = best_M(lambda M: n * (seq['B'][M] - h) + Q2.E_old(cu, n, eps, dln, M, seq), 1)
    vn, Mn = best_M(lambda M: n * (seq['B'][M] - h) + Q2.E_new(cu, n, eps, dln, M, seq), 0)
    v, k, nb, c, l, b = best_k(n, eps, dln, int(min(n ** 0.5, 400)))
    rows[ex] = (n * (a - h), vo, vn, v)
    print("  10^%-4g %10.4g  %10.4g   %10.4g     | %10.4g  %6d  %9.4g  %8.4g  %8.4g  %7.4g      %6.2f               |  %g (%d)"
          % (ex, n * (a - h), vo, vn, v, k, nb, c, l, b, (c + l) / k / math.log(n), add[ex][0], add[ex][1]))

print("\n# the excess over n h: best earlier bound in the table of A8 (non-adaptive, 11.58a, Theorem A, and the cut curves of Z_REPORT as quoted there) / envelope schedule")
for ex in (5, 6, 7, 8, 9, 10):
    na, vo, vn, v = rows[ex]
    others = {"non-adaptive": na, "11.58a": vo, "Theorem A": vn, "cut curves (Z_REPORT, as quoted)": cut[ex]}
    kbest = min(others, key=others.get)
    print("  n = 10^%g:  best earlier = %-34s %10.4g;  factor %.2f   (against Theorem A alone: %.2f;  against the cut curves: %.2f)"
          % (ex, kbest, others[kbest], others[kbest] / v, vn / v, cut[ex] / v))
print("# n = 10^12, 10^15 (from the table of A8 itself): 6.76e6/9.68e5 = %.2f and 2.35e8/1.13e7 = %.2f against Theorem A;  1.04e6/9.68e5 = %.2f and 1.19e7/1.13e7 = %.2f against the cut curves"
      % (6.76e6 / 9.68e5, 2.35e8 / 1.13e7, 1.04e6 / 9.68e5, 1.19e7 / 1.13e7))

print("\n# where does the envelope schedule fall below the non-adaptive cost and below the earlier bounds?")
print("#        n     n(a-h)    Thm 11.58a   Theorem A   envelope (k)     below non-adaptive   below 11.58a   below Theorem A")
for n in (10000, 12000, 14000, 16000, 18000, 20000, 22000, 25000, 28000, 31623, 40000, 50000, 70000, 100000):
    vo, Mo = best_M(lambda M: n * (seq['B'][M] - h) + Q2.E_old(cu, n, eps, dln, M, seq), 1)
    vn, Mn = best_M(lambda M: n * (seq['B'][M] - h) + Q2.E_new(cu, n, eps, dln, M, seq), 0)
    v, k, nb, c, l, b = best_k(n, eps, dln, int(min(n ** 0.5, 60)))
    na = n * (a - h)
    print("  %7d  %9.1f   %9.1f   %9.1f   %9.1f (%d)        %-5s                %-5s          %-5s" % (n, na, vo, vn, v, k, v < na, v < vo, v < vn))
