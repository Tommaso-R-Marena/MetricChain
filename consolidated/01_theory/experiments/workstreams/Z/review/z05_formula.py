#!/usr/bin/env python3
"""z05: (v) of the brief -- rows of the table of section 7 of Z_REPORT.md from the formulas of its section 6, own code.

  ln N <= n b_k + E_k,   E_k unrolled from the top (section 6):  Lam := ln(1/delta) + n ln 2;  for j = k .. 1:
      chain (B' = b_j, accuracy X = X_0(n) + 1, alpha = eps^ for j = k, 1 otherwise): block m_j by (4.1) of Q2 at Lam_in = Lam;
          Lam += j(n) q_T(n, Lam + n b_j);   E += A_T(n, Lam) + X + 1;
      level:  E += ell_0(n, Lam) + X_0(n) + d_min ln 2 + 2;   Lam += q(n, Lam);
  then the base: (A.1) of Q2_REPORT section 5.2 with M_1 epochs and top accuracy 1, started at this Lam.

b_j: own chain (zrev.Chain, s_t = L + 0.05, b_0 = h + 0.003).  Chain functions (P_cnt-bar, P_M-bar, varpi, A_T, design block):
those of the referee of Q2 (Q2/review/rlib.py), which were written from the text of Q2_REPORT section 4 and which I compared
with that text line by line; ell_0, q, X_0, the unrolling and (A.1) are written here from the text.
Nothing is imported from the coordinator's zetalib/q2lib/qlib.
Usage: python3 z05_formula.py
"""
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
JEX = 130
C = zrev.Chain(cu, 0.05, 0.003, JEX)
assert C.range_ok
dm = zlev.dmin(u)
ep = RL.epochs(rc, 60)
M1 = next(m for m in range(60) if ep['B'][m] <= C.b0)
print("# u = 1: h = %.6f a = %.6f c_*^2 = %.6f; chain to level %d (range condition holds: %s, largest W_j(b_j) = %.4f)" % (h, a, cu.cstar2, JEX, C.range_ok, max(C.Wtop)))
print("# base: M_1 = %d epochs, B_{M_1}/h - 1 = %.4f <= b_0/h - 1 = %.4f, k_{M_1} = %d" % (M1, ep['B'][M1] / h - 1, C.b0 / h - 1, ep['k'][M1]))


def chain_step(n, Bp, calX, alpha, Lam):
    m = RL.Chain.design_m(rc, n, Bp, calX, alpha, Lam)
    ch = RL.Chain(rc, n, Bp, calX, alpha, m)
    Lam2 = Lam + ch.j(n) * ch.qT(n, Lam + n * Bp)
    assert ch.Delta_T(n, Lam + n * Bp) == 0.0            # Proposition T(iv): the block of the design
    return ch.A_T(n, Lam2), Lam2, m


def base_A1(n, Lam, M, eps_top=1.0):
    """(A.1) of Q2_REPORT: the unrolled error of Theorem A with M epochs, entered with Lam; returns (E, Lam_final)."""
    E = 0.0
    cl = 1 + RL.c_log(rc, n) + h
    for e in range(M, -1, -1):
        alpha = min(eps_top, 1.0) if e == M else 1.0
        Bp = ep['B'][e] if e >= 1 else a
        calX = RL.X_D(rc, n, ep['phi'][e - 1]) if e >= 1 else RL.X_B(rc, n)
        A, Lam, m = chain_step(n, Bp, calX, alpha, Lam)
        E += A
        if e >= 1:
            B, R, d_ = ep['B'][e - 1], ep['R'][e - 1], ep['d'][e - 1]
            E += max(1.0, R / (2 * u * a)) * B + zlev.ell0(u, n, Lam)          # the drop D'
            Lam += zlev.q(u, n, Lam)
            for j in range(ep['J'][e - 1], 0, -1):                              # slope steps, sigma' = j/d
                E += (j / d_) * cl + zlev.ell0(u, n, Lam)
                Lam += zlev.q(u, n, Lam)
    return E + RL.E_frakB(rc, n, Lam), Lam


def E_Z(n, eps, dln, k, bfun):
    Lam = dln + n * LN2
    X0n = zlev.X0(u, n)
    calX = X0n + 1
    chains = levels = 0.0
    for j in range(k, 0, -1):
        alpha = min(eps, 1.0) if j == k else 1.0
        A, Lam, m = chain_step(n, bfun(j), calX, alpha, Lam)
        chains += A + calX + 1
        levels += zlev.ell0(u, n, Lam) + X0n + dm * LN2 + 2
        Lam += zlev.q(u, n, Lam)
    base, LamF = base_A1(n, Lam, M1)
    return chains, levels, base, LamF


def b_of(j):
    return C.b[j]


dln = math.log(1 / 0.05)
ref = {5: (1, 7466, 300, 468.9, 78.73, 6618), 7: (13, 2.521e4, 6152, 8712, 1325, 9018), 8: (30, 4.913e4, 1.197e4, 2.352e4, 3407, 1.024e4),
       9: (61, 9.971e4, 2.61e4, 5.45e4, 7643, 1.147e4), 10: (121, 2.095e5, 5.91e4, 1.211e5, 1.659e4, 1.271e4)}
print("# delta = 0.05, eps = 1; entries: ln(evaluations) - n h")
print("#    n     k   total     n beta_k   chains    levels    base  per-level/ln n | report (out_z2_formula_u1.txt): total, n beta_k, chains, levels, base | Lam_final/Lam_0 vs (k+M_1+4)")
for ex in (5, 7, 8, 9, 10):
    n = 10 ** ex
    k = ref[ex][0]
    ch, lv, bs, LamF = E_Z(n, 1.0, dln, k, b_of)
    nb = n * (b_of(k) - h)
    tot = nb + ch + lv + bs
    Lam0 = dln + n * LN2
    print("  10^%-2d %4d  %9.4g  %9.4g  %8.4g  %8.4g  %7.4g   %6.2f   | %9.4g  %9.4g  %8.4g  %8.4g  %7.4g | %.2f vs %d"
          % (ex, k, tot, nb, ch, lv, bs, (ch + lv) / k / math.log(n), ref[ex][1], ref[ex][2], ref[ex][3], ref[ex][4], ref[ex][5], LamF / Lam0, k + M1 + 4))
# is k of the table the minimiser? (neighbours)
for ex, ks in ((7, (11, 12, 13, 14, 15)), (9, (56, 61, 66))):
    n = 10 ** ex
    vals = []
    for k in ks:
        ch, lv, bs, _ = E_Z(n, 1.0, dln, k, b_of)
        vals.append(n * (b_of(k) - h) + ch + lv + bs)
    print("# n = 10^%d: total at k = %s: %s" % (ex, ks, " ".join("%.5g" % v for v in vals)))
# the per-level loss at large n and for k up to sqrt(n): is c_Z = 50 a valid constant of the theorem?
print("# per-level loss (chain + level)/ln n at b_j = h (the limit; the loss increases as b_j decreases), eps = 1, delta = 0.05,")
print("# entered with the largest Lam of the unrolling, (k + M_1 + 3) Lam_0:")
print("#     n        k = (n/ln n)^(1/3)     k = sqrt(n)")
for ex in (7, 10, 15, 20, 30, 40, 50):
    n = 10.0 ** ex
    out = []
    for kk in ((n / math.log(n)) ** (1 / 3.0), math.sqrt(n)):
        Lam = (kk + M1 + 3) * (dln + n * LN2)
        X0n = zlev.X0(u, n)
        A, Lam2, m = chain_step(n, h, X0n + 1, 1.0, Lam)
        out.append((A + X0n + 1 + 1 + zlev.ell0(u, n, Lam2) + X0n + dm * LN2 + 2) / math.log(n))
    print("   10^%-4d      %7.2f              %7.2f" % (ex, out[0], out[1]))


def climit(gam):
    """the limit of (per-level loss)/ln n for Lam = n^{1+gam+o(1)}, B' -> h, from the formulas of Q2 section 4 (u = 1: (Q3) applies):
    m h = (8 + gam) ln n;  a_T = varpi_3 - m h + Pbar_M  with  varpi_3 = m a + u sqrt(m ln n / 2) + (4/(3 p_u)) ln n,  Pbar_M = (5 + gam) ln n;
    level: ell_0 = (4 + gam) ln n, X_0 = ln n; chain: + X = ln n."""
    mh = 8 + gam
    aT = mh * a / h + u * math.sqrt(mh / (2 * h)) + 4 / (3 * cu.p) - mh + (5 + gam)
    return aT + 1 + (4 + gam) + 1


for gam, name in ((1 / 3.0, "k ~ n^(1/3)"), (0.5, "k = sqrt(n)")):
    cz = climit(gam)
    print("# limit of the per-level loss / ln n for %s: %.2f  ->  (3/2)(2 c_*^2)^(1/3) c_Z^(2/3) = %.2f   (with c_Z = 49.97, the value of the table at n = 10^15: %.2f)"
          % (name, cz, 1.5 * (2 * cu.cstar2) ** (1 / 3.0) * cz ** (2 / 3.0), 1.5 * (2 * cu.cstar2) ** (1 / 3.0) * 49.97 ** (2 / 3.0)))
