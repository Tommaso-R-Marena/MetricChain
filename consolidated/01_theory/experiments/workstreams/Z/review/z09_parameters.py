#!/usr/bin/env python3
"""z09: a remark, not a check of the report -- the illustration of section 7 (u = 1) with other chain parameters (cut level s_t,
restart height b_0 = h + eps1): the range condition for the levels used, M_1, and the formula of section 6 minimised over k.
The proof (Lemma RC) guarantees the range condition for SOME eps1 > 0 only; for a given k it is a finite check (j <= k).
Usage: python3 z09_parameters.py"""
import math
import sys

sys.dont_write_bytecode = True
import zrev
import zlev

RL = zlev.RL
LN2 = math.log(2.0)
u = 1.0
cu = zrev.Cube(u)
rc = RL.Cube(u)
h, a = cu.h, cu.a
dm = zlev.dmin(u)
ep = RL.epochs(rc, 60)
dln = math.log(1 / 0.05)
JEX = 70


def chain_step(n, Bp, calX, alpha, Lam):
    m = RL.Chain.design_m(rc, n, Bp, calX, alpha, Lam)
    ch = RL.Chain(rc, n, Bp, calX, alpha, m)
    Lam2 = Lam + ch.j(n) * ch.qT(n, Lam + n * Bp)
    return ch.A_T(n, Lam2), Lam2


def base_A1(n, Lam, M):
    E = 0.0
    cl = 1 + RL.c_log(rc, n) + h
    for e in range(M, -1, -1):
        Bp = ep['B'][e] if e >= 1 else a
        calX = RL.X_D(rc, n, ep['phi'][e - 1]) if e >= 1 else RL.X_B(rc, n)
        A, Lam = chain_step(n, Bp, calX, 1.0, Lam)
        E += A
        if e >= 1:
            B, R, d_ = ep['B'][e - 1], ep['R'][e - 1], ep['d'][e - 1]
            E += max(1.0, R / (2 * u * a)) * B + zlev.ell0(u, n, Lam)
            Lam += zlev.q(u, n, Lam)
            for j in range(ep['J'][e - 1], 0, -1):
                E += (j / d_) * cl + zlev.ell0(u, n, Lam)
                Lam += zlev.q(u, n, Lam)
    return E + RL.E_frakB(rc, n, Lam)


def total(n, k, C, M1):
    Lam = dln + n * LN2
    X0n = zlev.X0(u, n)
    E = 0.0
    for j in range(k, 0, -1):
        A, Lam = chain_step(n, C.b[j], X0n + 1, 1.0, Lam)
        E += A + X0n + 2 + zlev.ell0(u, n, Lam) + X0n + dm * LN2 + 2
        Lam += zlev.q(u, n, Lam)
    return n * (C.b[k] - h) + E + base_A1(n, Lam, M1)


print("# u = 1, delta = 0.05, eps = 1; entries: ln(evaluations) - n h, minimised over 1 <= k <= %d" % JEX)
print("#  s_t - L   b_0 - h   range condition (j <= %d), largest W_j(b_j)   M_1  k_{M_1} |  n = 10^6: total (k)    n = 10^7: total (k)    n = 10^8: total (k)    n = 10^9: total (k)" % JEX)
for dst, eps1 in ((0.05, 0.003), (0.15, 0.003), (0.05, 0.012), (0.15, 0.012), (0.10, 0.012), (0.15, 0.006), (0.10, 0.02)):
    try:
        C = zrev.Chain(cu, dst, eps1, JEX)
    except AssertionError:
        print("   %.2f     %.3f    not admissible (b_0 >= (1 - s_t) a or s_t >= 1 - h/a)" % (dst, eps1))
        continue
    M1 = next(m for m in range(60) if ep['B'][m] <= C.b0)
    row = "   %.2f     %.3f    %-5s  %.4f                                  %3d   %3d   |" % (dst, eps1, C.range_ok, max(C.Wtop), M1, ep['k'][M1])
    if C.range_ok:
        for ex in (6, 7, 8, 9):
            n = 10 ** ex
            best = min((total(n, k, C, M1), k) for k in list(range(1, 20)) + list(range(20, JEX + 1, 3)))
            row += "   %10.4g (%2d)    " % best
    print(row)
    sys.stdout.flush()
print("# for comparison (report, section 7): Theorem A of Q2: 1.059e4, 2.613e4, 7.02e4, 2.06e5;  non-adaptive n(a - h): 8.18e4, 8.18e5, ...")
