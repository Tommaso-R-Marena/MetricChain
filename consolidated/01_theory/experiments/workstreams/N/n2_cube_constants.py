#!/usr/bin/env python3
"""Workstream N, check 2: the abstract level theorem (Theorem N1 of N_REPORT) specialised to the cube, against the
constants of Theorem 11.56 = Theorem K1 as evaluated by workstream Q's library (experiments/workstreams/Q/qlib.py:
level_consts, level_cmax -- formulas of K_REPORT 2.2, themselves checked there against the referee's r8_flat).

The dictionary (N_REPORT 2.5):  X_o = Q_{n_o}, mu_o uniform;  ell_0 = e^{-psi_0}((1+e^-u)/2)^n;  V_max = e^{-psi_0 + un};
kappa_0 = (2 p_u)^n (so s_0 = e^{-psi_0 - un});  Xi(q) = 2^{-n_o} E_{r(q)}(n_o) (0 below the atom, +inf at r = n_o);
Theta(p) = 2^{-n_o} T_{n_o}(k(p));  x_0 = 2 u n_i;  C_0 = c_ref = 1.

  A. with the cube's conventions (J = ceil((2un + b + n_o ln 2)/lam); pi_* = 2^{-n_o-1} when r_dagger = -1) every
     constant of Theorem N1 must EQUAL the one of Theorem 11.56:  J, nu_0, pi_dagger, m_max, K, Mbar, delta', x_out, C_max.
     The closing level is computed from the abstract definition (conditions [N], [P] in terms of Xi, Theta as functions
     of q) and must coincide with |B(n_o, r_dagger)|/2^{n_o}.
  B. with the abstract conventions (J = ceil(2un/lam): rule (c0); pi_* = sup) the constants are reported next to
     the cube's: where they differ and by how much.

Run:  python3 n2_cube_constants.py > out_n2_cube_constants.txt       (a few seconds)
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "Q"))
import qlib  # noqa: E402   (read only)

from nlib import CubeTables, Consts, closing_level_steps  # noqa: E402

LN2 = math.log(2.0)
fails = 0
rows = []
cases = [
    # u, n, n_o, lam, eta, etap, theta, nu1 ('b' = 2 e^u n_o/theta, the bounded-accuracy choice), b, delta, ladder rungs
    (1.0, 60, 30, 0.2, 0.05, 0.05, 0.05, 'b', 0.5, 0.05, 12),
    (1.0, 200, 100, 0.2, 0.05, 0.05, 0.05, 'b', 0.5, 0.05, 40),
    (1.0, 400, 180, 0.3, 0.25, 0.5, 0.2, 'b', 1.0, 0.01, 17),
    (2.0, 300, 150, 0.2, 0.05, 0.05, 0.05, 'b', 0.5, 0.05, 30),
    (0.5, 600, 300, 0.2, 0.05, 0.05, 0.05, 'b', 0.5, 0.05, 40),
    (1.0, 300, 120, 1.0, 0.5, 1.0, math.exp(25.0), 1.0, 2.0, 1e-6, 20),     # extensive threshold (Theorem 11.52 regime)
    (1.0, 500, 250, 1.0, 0.5, 1.0, math.exp(8.0), 1.0, 3.0, 1e-3, 25),
    (2.0, 120, 30, 0.5, 0.5, 1.0, 0.01, 1.0, 0.5, 0.05, 10),               # nu1 = 1, small theta: r_dagger = -1
    (1.0, 40, 10, 1.0, 0.5, 1.0, 0.5, 1.0, 1.0, 0.05, 6),
    (0.5, 80, 20, 0.1, 0.1, 0.1, 3.0, 'b', 0.3, 0.05, 15),
]
print("A. cube conventions: Theorem N1's constants against Theorem 11.56's (qlib.level_consts / level_cmax)")
print("%4s %5s %5s | %6s %6s | %5s %5s | %9s %9s | %5s %5s | %7s %7s | %11s %11s | %10s %10s | %s"
      % ("u", "n", "n_o", "J", "J_K1", "rdag", "r_K1", "ln pi*", "ln pi_K1", "m_max", "K1", "K", "K_K1",
         "ln Mbar", "K1", "ln Cmax", "K1", "all equal"))
for (u, n, n_o, lam, eta, etap, theta, nu1, b, delta, Lr) in cases:
    n_i = n - n_o
    if nu1 == 'b':
        nu1 = 2 * math.exp(u) * n_o / theta
    ceta = (1 - eta) / (1 + eta)
    tab = CubeTables(n_o, u)
    bp, val = tab.steps()
    # a ladder x_0 = 2 u n_i > ... > x_L = b (geometric) and inner log-costs (any nonincreasing numbers: here a made-up family)
    x0 = 2 * u * n_i
    xs = [x0 * (b / x0) ** (l / Lr) for l in range(Lr + 1)]
    xs[-1] = b
    lcost = [0.0] + [0.11 * n_i * max(0.0, 1 - xs[l] / (0.12 * n_i)) + 3.0 for l in range(1, Lr + 1)]
    # --- Theorem 11.56 (qlib) ---
    c = qlib.level_consts(u, n, n_o, lam, eta, etap, math.log(theta), nu1, b, math.log(delta), Lr)
    lC_K1, _ = qlib.level_cmax(c, xs, lcost)
    # --- Theorem N1 with the cube's conventions ---
    J_cube = math.ceil((2 * u * n + b + n_o * LN2) / lam)
    kappa0 = (2.0 / (1.0 + math.exp(u))) ** n
    lnD = n * (u + math.log(2.0 / (1.0 + math.exp(-u))))            # ln(V_max/ell_0)

    def closing(thrN, th, ce, bp=bp, val=val, tab=tab):
        pis, i = closing_level_steps(bp, val, tab.ThetaBar, thrN, th, ce)
        return pis, i

    nu0 = max((J_cube + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
    pis, istep = closing(theta * (1 - eta) * nu0, theta, ceta)
    rdag_abs = istep - 1                                             # first failing step i = r_dagger + 1
    pi_use = pis if rdag_abs >= 0 else 0.5 / tab.N                   # the cube's convention at r_dagger = -1
    C = Consts(lam, eta, etap, theta, nu1, b, xs, delta, kappa0, None, lnD=lnD, J=J_cube, pi_star=pi_use,
               C=np.exp(np.array(lcost)))
    lC_N1 = math.log(C.Cmax())
    eq = (C.J == c['J'] and abs(C.nu0 - c['nu0']) <= 1e-9 * c['nu0'] and rdag_abs == c['rdag']
          and abs(math.log(C.pi_star) - c['lpidag']) < 1e-9 and C.m_max == c['m_max'] and C.K == c['K']
          and abs(math.log(C.Mbar) - c['lMbar']) < 1e-9 and abs(math.log(C.deltap) - c['ldeltap']) < 1e-9
          and abs(C.xout - c['xout']) < 1e-9 and abs(lC_N1 - lC_K1) < 1e-8)
    fails += (not eq)
    print("%4.1f %5d %5d | %6d %6d | %5d %5d | %9.4f %9.4f | %5d %5d | %7d %7d | %11.6f %11.6f | %10.5f %10.5f | %s"
          % (u, n, n_o, C.J, c['J'], rdag_abs, c['rdag'], math.log(C.pi_star), c['lpidag'], C.m_max, c['m_max'], C.K, c['K'],
             math.log(C.Mbar), c['lMbar'], lC_N1, lC_K1, "YES" if eq else "NO"))
    # --- Theorem N1 with its own conventions ---
    Cab = Consts(lam, eta, etap, theta, nu1, b, xs, delta, kappa0, lambda thrN, th, ce: closing(thrN, th, ce)[0],
                 lnD=lnD, C=np.exp(np.array(lcost)))
    rows.append((u, n, n_o, Cab.J, c['J'], math.log(Cab.pi_star), c['lpidag'], Cab.K, c['K'], math.log(Cab.Mbar), c['lMbar'],
                 math.log(Cab.Cmax()), lC_K1, Cab.xout, c['xout']))

print()
print("B. abstract conventions (rule (c0): J = ceil(2un/lam); pi_* = sup): constants next to Theorem 11.56's")
print("%4s %5s %5s | %6s %6s | %9s %9s | %6s %6s | %10s %10s | %10s %10s | %9s"
      % ("u", "n", "n_o", "J", "J_K1", "ln pi*", "ln pi_K1", "K", "K_K1", "ln Mbar", "K1", "ln Cmax", "K1", "x_out same"))
for r in rows:
    print("%4.1f %5d %5d | %6d %6d | %9.4f %9.4f | %6d %6d | %10.5f %10.5f | %10.5f %10.5f | %9s"
          % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12],
             "YES" if abs(r[13] - r[14]) < 1e-9 else "NO"))
print()
print("differences in A:", fails)
sys.exit(1 if fails else 0)
