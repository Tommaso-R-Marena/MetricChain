#!/usr/bin/env python3
"""Workstream Q, table 4 -- what Theorem Q8 / Theorem Q9 of Q_REPORT.md give in numbers (formula evaluation only).

  (a) the constants of the rate and of the theorem for u = 1/2, 1, 2;
  (b) the epoch sequences d_m, J_m, k_m, B_m, phi_m (RateFull.lean, epochSeq) and the series of the sqrt(n)-term;
  (c) for n = 10^3 ... 10^12: the best number of epochs M, the bound  n B_M + E_M(n, eps, delta)  of Theorem Q8, its
      parts, and (bound - n h)/sqrt(n ln n);  the same for other accuracies and failure probabilities;
  (d) the closed form of Theorem Q9(b) against the minimum over M.

usage: python3 q4_bound_table.py > out_q4_bound_table.txt        (a few seconds)
"""
import math

import qlib as Q

LN2 = Q.LN2


def best_M(cu, seq, n, eps, dl, Mmax):
    best = None
    for M in range(0, Mmax + 1):
        if seq['k'][M] > n:
            break
        E = Q.E_total(cu, n, eps, dl, M, seq)
        val = n * seq['B'][M] + E
        if best is None or val < best[0]:
            best = (val, M, E)
        elif M >= best[1] + 3 and E > 2 * best[2] + n * (seq['B'][best[1]] - cu.h):
            break           # from here on the error term alone exceeds the best bound's excess over n h: no later M can win
    return best


def main():
    print("# Workstream Q, table 4: the bound of Theorem Q8 in numbers")
    MM = 44
    for u in (0.5, 1.0, 2.0):
        cu = Q.Cube(u)
        a, h = cu.a, cu.h
        seq = Q.epoch_seq(cu, MM + 1)
        Cstar = 2 * math.sqrt((1 + cu.rbar) * cu.c1 * (a / h + 4))
        print()
        print("# ===== u = %.1f =====" % u)
        print("# (a) p_u = %.5f, a = %.6f, h = %.6f, h/a = %.4f, rho_h = %.5f;  kappa = %.5f, c1 = %.5f = %.3f a, c2 = %.4f, rbar = %.4f"
              % (cu.p, a, h, h / a, cu.rho_h, cu.kappa, cu.c1, cu.c1 / a, cu.c2, cu.rbar))
        print("#     C_* = 2 sqrt((1 + rbar) c1 (a/h + 4)) = %.3f     [the constant of Theorem Q9(b)];   for comparison 2 sqrt(5 (a - h)) = %.3f"
              % (Cstar, 2 * math.sqrt(5 * (a - h))))
        print("# (b) epochs:  m   d_m        J_m     k_m      B_m/a     (B_m-h)/a   (B_m-h)(k_m+c2)/c1   phi_m      sum_{m'<=m} sqrt(phi_m')   k_{m+1}/k_m")
        acc = 0.0
        for m in range(0, MM):
            acc += math.sqrt(seq['phi'][m])
            if m <= 12 or m % 4 == 0:
                print("#           %3d  %10.4f %6d %8d   %.5f   %.6f     %.4f             %.6f   %.4f                    %.3f"
                      % (m, seq['d'][m], seq['J'][m], seq['k'][m], seq['B'][m] / a, (seq['B'][m] - h) / a,
                         (seq['B'][m] - h) * (seq['k'][m] + cu.c2) / cu.c1, seq['phi'][m], acc, seq['k'][m + 1] / seq['k'][m]))
        for eps in (1.0, 0.1):
            cs, alpha = Q.acc_schedule(eps, MM)
            ser = sum(math.sqrt(seq['phi'][m] * Q.ell_c(cu, cs[m]) / 2) * seq['B'][m + 1] / a for m in range(MM))
            ell0 = Q.ell0_x(cu, alpha[0])
            print("#     eps = %.2f: alpha_0 = %.4f (>= 0.519 eps);  coefficient of sqrt(n):  base u sqrt(ell0/2) = %.3f,  drops u sum_m sqrt(phi_m ell_m/2) B_{m+1}/a = %.3f  (first %d epochs)"
                  % (eps, alpha[0], u * math.sqrt(ell0 / 2), u * ser, MM))
        for (eps, dl_of, tag) in ((1.0, lambda n: math.log(1 / 0.05), "eps = 1, delta = 0.05"),
                                  (0.1, lambda n: math.log(1 / 0.05), "eps = 0.1, delta = 0.05"),
                                  (1.0, lambda n: float(n), "eps = 1, delta = e^{-n}")):
            if u != 1.0 and eps != 1.0:
                continue
            print("# (c) %s.   bound = n B_M + E_M;  E_M = base + slope steps + drops (sqrt part, log part)" % tag)
            print("#        n      M   k_M    bound/(n a)   B_M/a    (bound-nh)/sqrt(n ln n)   (bound-nh)/n^{3/4}    E_M      = base     + S: levels x per level           + D sqrt    + D log     Lam_T/Lam_0   closed form of Q9(b)/(n a)")
            for n in (10 ** 3, 10 ** 4, 16000, 32000, 64000, 10 ** 5, 10 ** 6, 10 ** 7, 10 ** 8, 10 ** 9, 10 ** 10, 10 ** 11, 10 ** 12):
                dl = dl_of(n)
                val, M, E = best_M(cu, seq, n, eps, dl, MM)
                p = Q.E_total(cu, n, eps, dl, M, seq, detail=True)
                Lam0 = dl + n * LN2
                # closed form: n h + 2 sqrt((1 + rbar) c1 n l_S) + (base + drops) evaluated at Lam = 2 Lam0
                lS = Q.cS(cu, n, 2 * Lam0, a)
                closed = n * h + 2 * math.sqrt((1 + cu.rbar) * cu.c1 * n * lS) + p['Ebase'] + p['Dsqrt'] + p['Dlog']
                per = (p['S'] / p['nS']) if p['nS'] else 0.0
                print("# %10.3g   %3d %6d    %.4f      %.4f        %7.3f                 %7.3f          %10.1f   %9.1f    %5d x %6.1f = %10.1f   %10.1f  %9.1f     %.4f        %.4f"
                      % (n, M, seq['k'][M], val / (n * a), seq['B'][M] / a, (val - n * h) / math.sqrt(n * math.log(n)),
                         (val - n * h) / n ** 0.75, E, p['Ebase'], p['nS'], per, p['S'], p['Dsqrt'], p['Dlog'], p['Lam'] / Lam0, closed / (n * a)))
    print()
    print("# reading: the bound is below the non-adaptive exponent a (bound/(n a) < 1) from n of order 10^4-10^5 on, and")
    print("# (bound - n h)/sqrt(n ln n) stays bounded while (bound - n h)/n^{3/4} tends to zero.")


if __name__ == '__main__':
    main()
