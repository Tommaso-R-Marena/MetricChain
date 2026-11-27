#!/usr/bin/env python3
"""Workstream Q, check 2 -- the two inductive steps (Propositions Q6 and Q7 of Q_REPORT.md) against exact evaluations,
with an inner family that SATURATES the hypothesis: its certified log-cost is exactly  d B - sigma min(x, R d)
(error function 0).  For such a family the exact ln C_max of the new level (all constants of Theorem 11.56 from the
referee's tables, via qlib.level_consts) must satisfy

   slope step:   ln C_max  <=  n B - (sigma + B/h - 1) min(x, R' n) + c_S(n, Lam; B),         R' = R h/(h + R)  (h if R = inf)
   drop:         ln C_max  <=  n B a/(a + R) + c_D(n, Lam; c, phi, R, B)                      (with the shift of the outer block)
                 ln C_max  <=  n B a/(a + R) + c_D^0                                          (without the shift)

with Lam = ln(1/delta) + n ln 2.  (B, sigma, R) run through the values that occur in the epoch schedule: epoch m,
step j: B = B_m, sigma = j/d_m, R = h/j (inf for j = 0); drops: sigma = 1, R = h/J_m.

usage: python3 q2_step_checks.py > out_q2_step_checks.txt          (about 6 minutes)
"""
import math
import sys
import time

import numpy as np

import qlib as Q
import qscheme as S

LN2 = Q.LN2
INF = float('inf')


def run(us=(0.5, 1.0, 2.0)):
    t0 = time.time()
    tot_viol = 0
    print("# Workstream Q, check 2: the inductive steps with a saturating inner family (exact constants of Theorem 11.56)")
    for u in us:
        cu = Q.Cube(u)
        seq = Q.epoch_seq(cu, 14)
        print()
        print("# u = %.1f: a = %.5f, h = %.5f;  epochs m: (J_m, B_m/a, R_m/h, phi_m) = %s"
              % (u, cu.a, cu.h, ", ".join("%d:(%d, %.3f, %.3f, %.3f)" % (m, seq['J'][m], seq['B'][m] / cu.a, seq['R'][m] / cu.h, seq['phi'][m])
                                           for m in (0, 1, 3, 5, 8, 12))))
        # ---------------- slope steps
        print("# slope step (Proposition Q6).  slack = bound - exact;  c_S = the error term of the proposition")
        print("#       n   ln(1/delta)   cases   violations   least slack   least slack/c_S   largest slack/c_S     c_S(n, Lam; a) .. c_S(n, Lam; h)   [nats]")
        for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
            for ldl in (math.log(1 / 0.05), float(n)):
                S.reset_check()
                Lam = ldl + n * LN2
                lo, hi = INF, -INF
                ncase = 0
                if n < 10 ** 6:
                    combos = [(m, j) for m in range(0, 9) for j in range(seq['J'][m])]
                else:
                    combos = [(0, 0), (3, 0), (3, seq['J'][3] - 1), (8, 0), (8, seq['J'][8] - 1)]
                for (m, j) in combos:
                    B = seq['B'][m]
                    sig = j / seq['d'][m]
                    R = INF if j == 0 else cu.h / j
                    inner = S.Synthetic(B, sig, R)
                    lev = S.SLevel(cu, inner, B, minrule=False)
                    X0 = Q.X0(cu, n)
                    Rp = lev.R
                    cand = [X0 + 0.01, X0 + 1.7, 3 * X0, 0.03 * Rp * n, 0.1 * Rp * n, 0.5 * Rp * n, 0.999 * Rp * n, Rp * n, 2 * Rp * n]
                    for x in cand:
                        if min(x, Rp * n) < X0:
                            continue
                        v = float(lev.costs(n, np.array([x]), -ldl)[0])
                        bound = lev.majorant(n, x) + Q.cS(cu, n, Lam, B)
                        cs = Q.cS(cu, n, Lam, B)
                        sl = (bound - v) / cs
                        lo, hi = min(lo, sl), max(hi, sl)
                        ncase += 1
                ck = S.CHECK
                st = ck.by.get('S as built', [0, INF, 0])
                q4 = ck.by.get('S: Lemma Q4', [0, INF, 0])
                tot_viol += st[2] + q4[2]
                print("%9d   %10.1f   %5d      %3d        %9.2f       %6.3f            %6.3f              %7.1f .. %7.1f      [%.0f s]"
                      % (n, ldl, ncase, st[2] + q4[2], st[1], lo, hi, Q.cS(cu, n, Lam, cu.a), Q.cS(cu, n, Lam, cu.h), time.time() - t0), flush=True)
        # ---------------- drops
        print("# drop (Proposition Q7); c = c_m of the accuracy schedule for eps = 1 and eps = 0.1; with the shift, without it, and the choice by certified cost")
        print("#       n   ln(1/delta)   cases   violations   least slack (shift)   least slack (no shift)   c_D for m = 0, 3, 8 (eps = 1): total [of which the shift term B c_pi/(a+R)]")
        for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
            for ldl in (math.log(1 / 0.05), float(n)):
                S.reset_check()
                Lam = ldl + n * LN2
                ncase = 0
                ms = range(0, 13) if n < 10 ** 6 else (0, 3, 8, 12)
                for eps in (1.0, 0.1):
                    cs, alpha = Q.acc_schedule(eps, 13)
                    for m in ms:
                        B = seq['B'][m]
                        R = seq['R'][m]
                        inner = S.Synthetic(B, 1.0, R)
                        lev = S.DLevel(cu, inner, cs[m], alpha[m + 1], alpha[m], R, seq['phi'][m], minrule=True)
                        v = float(lev.costs(n, np.array([alpha[m + 1]]), -ldl)[0])
                        ncase += 1
                ck = S.CHECK
                a1 = ck.by.get('D as built (shift)', [0, INF, 0])
                a2 = ck.by.get('D as built (no shift)', [0, INF, 0])
                a3 = ck.by.get('D', [0, INF, 0])
                a4 = ck.by.get('D: Lemma Q3', [0, INF, 0])
                nv = a1[2] + a2[2] + a3[2] + a4[2]
                tot_viol += nv
                cs1, _ = Q.acc_schedule(1.0, 13)
                cds = []
                for m in (0, 3, 8):
                    cd = Q.cD(cu, n, Lam, cs1[m], seq['phi'][m], seq['R'][m], seq['B'][m])
                    sh = Q.shift_D(cu, n, cs1[m], seq['phi'][m], seq['R'][m]) * seq['B'][m]
                    cds.append("%.1f [%.1f]" % (cd, sh))
                print("%9d   %10.1f   %5d      %3d        %9.2f (%d built)    %9.2f (%d built)        %s      [%.0f s]"
                      % (n, ldl, ncase, nv, a1[1], a1[0], a2[1], a2[0], ",  ".join(cds), time.time() - t0), flush=True)
    print()
    print("violations of proved inequalities: %d   [%.0f s]" % (tot_viol, time.time() - t0))


if __name__ == '__main__':
    run()
