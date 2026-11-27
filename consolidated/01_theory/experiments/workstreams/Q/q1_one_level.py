#!/usr/bin/env python3
"""Workstream Q, check 1 -- the finite-n form of ONE level (Q_REPORT section 2) against exact evaluations.

Exact side: the referee's evaluator experiments/reviews/R8/r8_flat.flat_run (ln C_max, ln Mbar, K, J, r_dag, the
ladder and the costs of the inner base brackets) for the two-level design of K_REPORT 6.4 / theory report 11.19(1b):
b = 0.5, lam = 0.2, eta = eta' = theta = 0.05, delta = 0.05, geometric ladder of 40 rungs, n_o = floor(n/2), u = 1.

Part A  Proposition Q1 (decomposition) and the polynomial factors P_M, P_cnt (Lemma Q2), the delta' handed down.
Part B  Lemma Q3 (outer sample at a bounded theta): ln(1/pi_dag) - n_o a, measured, against the proved bounds
        (this report's refinement  u(1+s) + (4/(3p))(ell + 2/m) + ln(m+1)  and Lemma K.4(d)  (u + ln 4)(1+s) + ln(m+1)).
Part B' Lemma Q3 on exact tables for u = 1/2, 1, 2, m = 1 ... 64000 and eta = theta = c = 1/3 ... 0.001.
Part C  the one-level inequality in the form of the brief:
        ln C_max <= max{n_o a, max_l [min(n_o a, x_{l-1}) + ln C_l]} + Err,   Err = ln(L+2) + max{P_M + c_pi, P_cnt}.
Part D  Lemma Q4 (outer sample at an extensive theta): on exact tables for many (u, m, e), and through flat_run for the
        slope-step design (lam = 1, eta = 1/2, eta' = 1, nu_1 = 1, tolerance 1, accuracy exactly x = g n).
Part D'' Lemma Q4(a) by direct summation in 40-digit arithmetic (mpmath) for m <= 120, and the float tables against it.
Part E  Proposition Q5 (base family): exact cost of the two-sample bracket against d a + E_base(d, x; ln(1/delta)), and at
        extensive accuracies against d theta_na((x - c'_d)/d) + ln(8K(d+1))  (Q5(b)).

usage: python3 q1_one_level.py > out_q1_one_level.txt          (about 20 seconds)
"""
import math
import sys
import time

import numpy as np

import qlib as Q

F = Q.F
LN2 = Q.LN2
NS = (1000, 1400, 2000, 4000, 8000, 16000, 32000, 64000)
viol = 0


def chk(cond, what):
    global viol
    if not cond:
        viol += 1
        print("   *** VIOLATION:", what)


def part_ABC(u=1.0):
    cu = Q.Cube(u)
    a, h, p = cu.a, cu.h, cu.p
    lam = 0.2; eta = 0.05; etap = 0.05; theta = 0.05; b = 0.5; delta = 0.05; Lr = 40
    m0 = math.ceil(math.log((1 + eta) / (1 - eta)) / u)
    ell = math.log(2 * math.exp(u * (m0 + 2)) / theta)
    tau2 = 0.5004 * a
    print("# Parts A-C.  u = %.1f: a = %.6f, h = %.6f, p_u = %.5f; design b=0.5, lam=0.2, eta=eta'=theta=0.05, delta=0.05, 40 rungs, phi=0.5"
          % (u, a, h, p))
    print("# m_0 = %d, ell = ln(2 e^{u(m_0+2)}/theta) = %.4f; proved sqrt-constants: u sqrt(ell/2) = %.4f (Lemma Q3), (u+ln4) sqrt(ell/2) = %.4f (K.4(d))"
          % (m0, ell, u * math.sqrt(ell / 2), (u + math.log(4)) * math.sqrt(ell / 2)))
    rows = []
    for n in NS:
        r = F.flat_run(u, n, 0.5)
        n_o, n_i = r['n_o'], r['n_i']
        c = Q.level_consts(u, n, n_o, lam, eta, etap, math.log(theta), 2 * math.exp(u) * n_o / theta, b, math.log(delta), Lr)
        lC, terms = Q.level_cmax(c, r['xs'], r['lcosts'])
        chk(abs(lC - r['lCmax']) < 1e-9 and c['K'] == r['K'] and c['J'] == r['J'] and c['rdag'] == r['rdag'], "qlib differs from flat_run")
        Lam = LN2 + c['lMbar']                        # ln 2Mbar
        lpi = -c['lpidag']                            # ln(1/pi_dag)
        chk(abs(Lam - (c['P_M'] + lpi)) < 1e-9, "Lambda = P_M + ln(1/pi_dag)")
        mx = float(np.max(terms))
        am = int(np.argmax(terms))
        # Proposition Q1
        chk(mx <= lC + 1e-12 and lC <= mx + math.log(Lr + 2) + 1e-12, "Proposition Q1")
        # Lemma Q2: the polynomial factors, formula against the exact constants
        J = c['J']; K = c['K']
        chk(J <= (2 * u * n + b + n_o * LN2) / lam + 1, "J")
        nu0 = c['nu0']
        mmax_bound = math.log2(2 * (1 + eta) * math.exp(lam) * nu0 / (1 - eta)) + n_o + 2
        chk(c['m_max'] <= mmax_bound, "m_max")
        Kb = 3 * (1 + eta) / eta ** 2 * (math.log(1 / delta) + math.log(2 * (J + 1) * (mmax_bound + 1) * (Lr + 2))) + 1
        chk(K <= Kb, "K")
        ldp = -c['ldeltap']                           # ln(1/delta')
        chk(abs(ldp - (math.log(1 / delta) + math.log(2 * Lr) + Lam)) < 1e-9, "delta'")
        chk(ldp <= math.log(1 / delta) + math.log(2 * Lr) + c['P_M'] + (n_o + 1) * LN2, "delta' bound")
        # Lemma Q3
        s = math.sqrt(n_o * ell / 2)
        regime = s <= p * n_o / 2 - 1
        q3 = u * (1 + s) + 4 / (3 * p) * (ell + 2 / n_o) + math.log(n_o + 1)
        k4d = (u + math.log(4)) * (1 + s) + math.log(n_o + 1)
        over = lpi - n_o * a
        if regime:
            chk(over <= q3 + 1e-9, "Lemma Q3")
            chk(over <= k4d + 1e-9, "K.4(d)")
        chk(over <= Q.cpi_bar_ell(cu, n_o, ell) + 1e-9, "Lemma Q3, uniform form")
        rplus = math.floor(p * n_o - s)
        chk((not regime) or c['rdag'] >= rplus, "K.4(c)")
        # Part C: the form of the brief
        lc = np.array(r['lcosts'][1:])
        xs = np.array(r['xs'])
        ideal = max(n_o * a, float(np.max(np.minimum(n_o * a, xs[:-1]) + lc)))
        err = lC - ideal
        cpi = q3 if regime else Q.cpi_bar_ell(cu, n_o, ell)
        err_bound = math.log(Lr + 2) + max(c['P_M'] + cpi, c['P_cnt'])
        chk(err <= err_bound + 1e-9, "one-level inequality (brief's form)")
        err_exactconst = math.log(Lr + 2) + max(c['P_M'] + over, c['P_cnt'])      # the same with the measured overhead
        chk(err <= err_exactconst + 1e-9, "one-level inequality with the measured overhead")
        # the base bracket at the finest rung (bounded accuracy b) and at the rung that carries the maximum
        base_fin = r['lcosts'][Lr] - n_i * a
        eb_fin = Q.E_base(cu, n_i, b, ldp)
        chk(base_fin <= eb_fin + 1e-9, "Proposition Q5 at the finest rung")
        rows.append(dict(n=n, n_o=n_o, lC=lC, mx=mx, am=am, Lam=Lam, lpi=lpi, over=over, q3=q3, k4d=k4d, regime=regime, PM=c['P_M'],
                         Pcnt=c['P_cnt'], J=J, K=K, nu0=nu0, ldp=ldp, err=err, err_bound=err_bound, ideal=ideal, base_fin=base_fin,
                         eb_fin=eb_fin, rdag=c['rdag'], rplus=rplus, xs=xs, lc=lc, n_i=n_i))
    print()
    print("# Part A (Proposition Q1, Lemma Q2).  Lam = ln 2Mbar; t_l = min(Lam, x_{l-1} + P_cnt) + ln C_l; M* = max(Lam, max_l t_l)")
    print("#     n   lnCmax/(na)   lnCmax      M*      lnCmax-M* (<= ln 42 = %.3f)   argmax rung l (x_{l-1} -> x_l)      Lam     P_M    P_cnt   ln(J+1)  ln nu0   ln K   ln(1/delta')"
          % math.log(42))
    for w in rows:
        am = w['am']
        if am == 0:
            where = "outer sample 2Mbar"
        else:
            where = "l=%d (%.1f -> %.1f)" % (am, w['xs'][am - 1], w['xs'][am])
        print("%7d   %.4f     %9.2f %9.2f   %6.3f                         %-28s %9.2f %7.2f %7.2f %7.2f %7.2f %7.2f %9.2f"
              % (w['n'], w['lC'] / (w['n'] * a), w['lC'], w['mx'], w['lC'] - w['mx'], where, w['Lam'], w['PM'], w['Pcnt'],
                 math.log(w['J'] + 1), math.log(w['nu0']), math.log(w['K']), w['ldp']))
    print()
    print("# Part B (Lemma Q3): the outer sample at a bounded theta.  over = ln(1/pi_dag) - n_o a")
    print("#     n    n_o   r_dag   r_+ = floor(p n_o - s)   over     over/sqrt(n_o)   Lemma Q3 bound   /sqrt(n_o)   K.4(d) bound   /sqrt(n_o)   regime s<=p n_o/2-1")
    for w in rows:
        sq = math.sqrt(w['n_o'])
        print("%7d %6d %6d %8d               %8.2f   %7.3f        %9.2f      %6.3f      %9.2f     %6.3f        %s"
              % (w['n'], w['n_o'], w['rdag'], w['rplus'], w['over'], w['over'] / sq, w['q3'], w['q3'] / sq, w['k4d'], w['k4d'] / sq, w['regime']))
    print()
    print("# Part C: ln C_max - max{n_o a, max_l[min(n_o a, x_{l-1}) + ln C_l]}  against  Err = ln(L+2) + max{P_M + c_pi, P_cnt};")
    print("#         and the excess over the limit n tau_2 (tau_2 = 0.5004 a), with the base bracket of the finest rung (accuracy 0.5, failure delta')")
    print("#     n   lnCmax    ideal max    difference   Err (proved)    lnCmax - n tau_2   /sqrt(n)    base(n_i, 0.5, delta') - n_i a   E_base (proved)   /sqrt(n_i): measured, proved")
    for w in rows:
        n = w['n']
        print("%7d %9.2f  %9.2f    %8.2f     %8.2f        %9.2f       %6.3f         %9.2f                 %9.2f          %6.3f  %6.3f"
              % (n, w['lC'], w['ideal'], w['err'], w['err_bound'], w['lC'] - n * tau2, (w['lC'] - n * tau2) / math.sqrt(n),
                 w['base_fin'], w['eb_fin'], w['base_fin'] / math.sqrt(w['n_i']), w['eb_fin'] / math.sqrt(w['n_i'])))
    print()


def part_Bprime():
    print("# Part B' (Lemma Q3 on exact tables): eta = theta = c, nu_0 = 2 e^u m/(theta (1 - eta)) (the least value allowed), ell_c = ln 2 + 3u + 2.25c + ln(1/c)")
    print("#   proved: ln(1/pi_dag) <= m a + cbar_pi(m; ell_c);  if s = sqrt((m/2) ln(2e^{u(m_0+2)}/theta)) <= p m/2 - 1:  <= m a + u(1+s) + (4/(3p))(ell_1 + 2/m) + ln(m+1)")
    print("#   u      c        m     regime   r_dag   floor(p m - s)   ln(1/pi_dag) - m a   refined bound   cbar_pi    (measured)/sqrt(m)   u sqrt(ell_1/2)")
    worst = float('inf')
    cnt = 0
    for u in (0.5, 1.0, 2.0):
        cu = Q.Cube(u)
        for m in (1, 2, 3, 5, 8, 13, 30, 100, 300, 1000, 3000, 10000, 30000, 64000):
            t = F.TablesF(m, u)
            for c in (1 / 3, 0.1, 0.05, 0.01, 0.001):
                eta = theta = c
                nu0 = 2 * math.exp(u) * m / (theta * (1 - eta))
                rdag, lpid = Q.rdag_of(t, u, m, eta, math.log(theta), nu0)
                over = -lpid - m * cu.a
                m0 = math.ceil(math.log((1 + eta) / (1 - eta)) / u)
                ell1 = math.log(2 * math.exp(u * (m0 + 2)) / theta)
                ellc = Q.ell_c(cu, c)
                chk(ell1 <= ellc + 1e-12, "ell_1 <= ell_c")
                s = math.sqrt(m * ell1 / 2)
                regime = s <= cu.p * m / 2 - 1
                cb = Q.cpi_bar(cu, m, c)
                chk(over <= cb + 1e-9, "Lemma Q3 (uniform) at u=%g m=%d c=%g" % (u, m, c))
                worst = min(worst, cb - over)
                ref = float('nan')
                if regime:
                    ref = u * (1 + s) + 4 / (3 * cu.p) * (ell1 + 2 / m) + math.log(m + 1)
                    chk(over <= ref + 1e-9, "Lemma Q3 (refined) at u=%g m=%d c=%g" % (u, m, c))
                    chk(rdag >= math.floor(cu.p * m - s), "K.4(c) at u=%g m=%d c=%g" % (u, m, c))
                cnt += 1
                if u == 1.0 and m in (100, 3000, 64000) and c in (1 / 3, 0.05, 0.001):
                    print("  %.1f  %6.4f %6d    %-5s  %6d   %8d          %9.2f          %9.2f    %9.2f       %6.3f             %6.3f"
                          % (u, c, m, regime, rdag, math.floor(cu.p * m - s), over, ref, cb, over / math.sqrt(m), u * math.sqrt(ell1 / 2)))
    print("#   %d cases (u = 0.5, 1, 2; 14 sizes m = 1 ... 64000; c = 1/3, 0.1, 0.05, 0.01, 0.001): least slack of the uniform bound %.3f" % (cnt, worst))
    print()


def part_D():
    print("# Part D (Lemma Q4): theta >= ((1+eta)/(1-eta)) (m+1) e^{2u + e^u + m e}  ==>  ln(1/pi_dag) <= m theta_na(e) + ln(m+1)")
    print("#   exact tables; eta = 1/2 and eta = 0.05; nu_0 = 1/(1-eta) (the least value allowed); slack = bound - ln(1/pi_dag)")
    print("#   u      m      e/h     r_dag   rho_e m    ln(1/pi_dag)   m theta_na(e)   ln(m+1)    slack (eta=1/2)   slack (eta=0.05)")
    worst = float('inf')
    cnt = 0
    for u in (0.5, 1.0, 2.0):
        cu = Q.Cube(u)
        for m in (1, 2, 3, 5, 8, 13, 30, 100, 300, 1000, 3000, 10000, 30000, 64000):
            t = F.TablesF(m, u)
            for ef in (0.0, 0.25, 0.5, 1.0, 2.0, cu.eps_star / cu.h * 0.5, cu.eps_star / cu.h * 0.999, cu.eps_star / cu.h * 1.5):
                e = ef * cu.h
                out = []
                for eta in (0.5, 0.05):
                    lth = math.log((1 + eta) / (1 - eta)) + math.log(m + 1) + 2 * u + math.exp(u) + m * e
                    rdag, lpid = Q.rdag_of(t, u, m, eta, lth, 1 / (1 - eta))
                    bound = m * cu.theta_na(e) + math.log(m + 1)
                    slack = bound + lpid
                    out.append((rdag, -lpid, slack))
                    worst = min(worst, slack)
                    cnt += 1
                    chk(slack >= -1e-9, "Lemma Q4 at u=%g m=%d e=%g eta=%g" % (u, m, e, eta))
                    chk(rdag >= min(m - 1, math.floor(cu.rho_of(e) * m) + 1), "Lemma Q4, radius, at u=%g m=%d e=%g eta=%g" % (u, m, e, eta))
                if m in (1, 13, 1000, 64000) and ef in (0.0, 1.0, 2.0):
                    print("  %.1f %6d   %6.3f  %6d  %9.2f   %10.3f     %10.3f     %7.3f    %8.3f         %8.3f"
                          % (u, m, ef, out[0][0], cu.rho_of(e) * m, out[0][1], m * cu.theta_na(e), math.log(m + 1), out[0][2], out[1][2]))
    print("#   %d cases (u = 0.5, 1, 2; 14 sizes; 8 rates; 2 values of eta): least slack %.4f" % (cnt, worst))
    print()
    print("# Part D': the slope-step design through flat_run (lam=1, eta=1/2, eta'=1, nu_1=1, tolerance 1, theta = e^{x-1}-(3e+1)-(2p)^n/e, u = 1)")
    print("#     n     x = g n   g/h    n_o    r_dag   rho_h n_o   x_out - x    ln(1/pi_dag)   n_o h    ln(1/pi_dag) - n_o h   (<= ln(n_o+1))   ln 2Mbar - (x-1)   (<= P_cnt)   lnCmax/(na) [two levels, base inside, 30 rungs]")
    u = 1.0
    cu = Q.Cube(u)
    for n in NS:
        for gf in (0.1, 0.25, 0.5, 0.9):
            x = gf * cu.h * n
            if x < Q.X0(cu, n):
                continue
            n_o = int(math.floor((x - 1 - Q.c_log(cu, n)) / cu.h))
            lth = (x - 1) + math.log1p(-(3 * math.e + 1 + (2 * cu.p) ** n / math.e) * math.exp(-(x - 1)))
            r = F.flat_run(u, n, (n_o + 0.5) / n, lam=1.0, eta=0.5, etap=1.0, b=1.0, Lr=30, bounded=False, ltheta=lth, delta=0.05)
            assert r['n_o'] == n_o
            c = Q.level_consts(u, n, n_o, 1.0, 0.5, 1.0, lth, 1.0, 1.0, math.log(0.05), 30)
            chk(abs(c['lMbar'] - r['lMbar']) < 1e-9 and c['rdag'] == r['rdag'], "qlib differs from flat_run (slope step)")
            lpi = -c['lpidag']
            chk(abs(r['xout'] - x) < 1e-9, "accuracy exactly x")
            chk(lpi <= n_o * cu.h + math.log(n_o + 1) + 1e-9, "Lemma Q4 in the slope step")
            Lam = LN2 + c['lMbar']
            chk(Lam <= x - 1 + c['P_cnt'] + 1e-9, "Lambda <= x - 1 + P_cnt")
            if gf in (0.25, 0.5):
                print("%7d  %8.1f  %.2f %6d  %6d  %9.1f    %8.1e    %9.2f   %9.2f      %7.2f           %6.2f          %7.2f         %6.2f       %.4f"
                      % (n, x, gf, n_o, r['rdag'], cu.rho_h * n_o, r['xout'] - x, lpi, n_o * cu.h, lpi - n_o * cu.h, math.log(n_o + 1),
                         Lam - (x - 1), c['P_cnt'], r['lCmax'] / (n * cu.a)))
    print()


def part_Dexact():
    """Lemma Q4(a) and the tables themselves by direct summation in 40-digit arithmetic (mpmath), no tables"""
    import mpmath as mp
    mp.mp.dps = 40
    print("# Part D'' (Lemma Q4(a) by direct summation, mpmath, 40 digits; and the referee's float tables against it)")
    worst = mp.inf
    maxdev = 0.0
    cnt = 0
    for u in (0.3, 1.0, 2.0, 4.0):
        cu = Q.Cube(u)
        U = mp.mpf(u)
        for m in (1, 2, 3, 4, 7, 12, 25, 60, 120):
            C = [mp.binomial(m, j) for j in range(m + 1)]
            Bc = [mp.fsum(C[:r + 1]) for r in range(m + 1)]
            E = [mp.fsum(C[j] * (mp.e ** (U * (r + 1 - j)) - 1) for j in range(r + 1)) for r in range(m + 1)]
            gt = [mp.e ** U - 1] + [E[r] / Bc[r - 1] for r in range(1, m + 1)]
            t = F.TablesF(m, u)
            lGt = np.concatenate(([math.log(math.expm1(u))], t.lE[1:] - t.lB[:-1]))
            maxdev = max(maxdev, max(abs(float(mp.log(gt[r])) - float(lGt[r])) for r in range(m + 1)))
            for ef in (0.0, 0.3, 1.0, 2.0, cu.eps_star / cu.h, 2 * cu.eps_star / cu.h):
                e = ef * cu.h
                rho = cu.rho_of(e)
                bound = mp.log(m + 1) + 2 * U + mp.e ** U + m * mp.mpf(e)
                for r in range(0, m + 1):
                    if r <= rho * m + 1:
                        slack = bound - mp.log(gt[r])
                        worst = min(worst, slack)
                        cnt += 1
                        chk(slack >= 0, "Lemma Q4(a), exact, u=%g m=%d e=%g r=%d" % (u, m, e, r))
    print("#   %d triples (u = 0.3, 1, 2, 4; m = 1 ... 120; six rates; all r <= rho_e m + 1): least slack of ln[(m+1) e^{2u+e^u+me}/Gamma~(r)] = %.4f;"
          % (cnt, float(worst)))
    print("#   largest deviation of the float tables' ln Gamma~(r) from the exact value: %.2e" % maxdev)
    print()


def part_E():
    print("# Part E (Proposition Q5): the base family.  cost = min(2M, 2^d);  over = ln cost - d a;  E_base(d, x; ln(1/delta)) proved")
    print("#   u      d       x      ln(1/delta)     ln cost      over     over/sqrt(d)    E_base    E_base/sqrt(d)")
    worst = float('inf')
    cnt = 0
    for u in (0.5, 1.0, 2.0):
        cu = Q.Cube(u)
        for d in (1, 2, 5, 10, 30, 100, 300, 1000, 2000, 4000, 8000, 16000, 32000, 64000):
            t = F.TablesF(d, u)
            for x in (0.05, 0.26, 0.5, 1.0, 2.0, 2.5, 5.0, 20.0, 100.0, 0.02 * d, 0.2 * d, 3 * u * d):
                for ld in (math.log(1 / 0.05), 30.0, d * cu.a + 20, d * 1.0 + 5):
                    lc = Q.base_cost_one(u, d, x, -ld, t)
                    eb = Q.E_base(cu, d, x, ld)
                    over = lc - d * cu.a
                    worst = min(worst, eb - over)
                    cnt += 1
                    chk(over <= eb + 1e-9, "Proposition Q5 at u=%g d=%d x=%g ld=%g" % (u, d, x, ld))
                    if u == 1.0 and d in (1000, 8000, 64000) and x in (0.26, 0.5, 5.0) and ld in (math.log(1 / 0.05), d * cu.a + 20):
                        print("  %.1f %6d  %6.2f   %10.2f    %10.2f  %9.2f    %7.3f     %9.2f    %7.3f"
                              % (u, d, x, ld, lc, over, over / math.sqrt(d), eb, eb / math.sqrt(d)))
    print("#   %d cases (u = 0.5, 1, 2; 14 dimensions 1..64000; 12 accuracies; 4 failure probabilities): least slack %.3f" % (cnt, worst))
    print()
    print("# Part E' (Proposition Q5(b)): the base family at extensive accuracies x = f eps* d;  c'_d = ln 12 + 2 ln(d+1) + 2u + e^u;")
    print("#   proved:  ln cost <= d theta_na((x - c'_d)/d) + ln(8K) + ln(d+1)   and   <= d theta_na(x/d) + u sqrt(d c'_d/2) + ln(8K(d+1)),  K = ceil(18 ln(4/delta))")
    worst1 = worst2 = float('inf')
    cnt = 0
    rows = {}
    for u in (0.5, 1.0, 2.0):
        cu = Q.Cube(u)
        for d in (1000, 4000, 16000, 64000):
            t = F.TablesF(d, u)
            cpd = math.log(12) + 2 * math.log(d + 1) + 2 * u + math.exp(u)
            for f in (0.1, 0.25, 0.5, 0.75):
                x = f * cu.eps_star * d
                for ld in (math.log(1 / 0.05), d * cu.a):
                    if x < max(cpd, Q.X_ETA_HALF):
                        if u == 1.0 and ld > 10:
                            rows.setdefault(d, []).append(None)             # the proposition needs x >= c'_d
                        continue
                    lc = Q.base_cost_one(u, d, x, -ld, t)
                    K = math.ceil(18 * (math.log(4) + ld))
                    b1 = d * cu.theta_na((x - cpd) / d) + math.log(8 * K) + math.log(d + 1)
                    b2 = d * cu.theta_na(x / d) + u * math.sqrt(d * cpd / 2) + math.log(8 * K * (d + 1))
                    chk(lc <= b1 + 1e-9, "Proposition Q5(b) at u=%g d=%d x=%g" % (u, d, x))
                    chk(b1 <= b2 + 1e-9, "Proposition Q5(b), consequence, at u=%g d=%d x=%g" % (u, d, x))
                    worst1 = min(worst1, b1 - lc)
                    worst2 = min(worst2, b2 - lc)
                    cnt += 1
                    if u == 1.0 and ld > 10:
                        rows.setdefault(d, []).append((lc - d * cu.theta_na(x / d), b1 - d * cu.theta_na(x / d), b2 - d * cu.theta_na(x / d)))
    print("#   %d cases (u = 0.5, 1, 2; d = 1000 ... 64000; f = 0.1, 0.25, 0.5, 0.75; delta = 0.05 and e^{-d a}): least slack %.2f (first bound), %.2f (second bound)"
          % (cnt, worst1, worst2))
    cu = Q.Cube(1.0)
    print("#   u = 1, delta = e^{-d a}:  ln cost - d theta_na(x/d)  [first bound - d theta_na(x/d); second bound - d theta_na(x/d)]   (theta_na(x/d)/a = %s)"
          % ", ".join("%.3f" % (cu.theta_na(f * cu.eps_star) / cu.a) for f in (0.1, 0.25, 0.5, 0.75)))
    print("#     d        f = 0.1                     f = 0.25                    f = 0.5                     f = 0.75")
    for d in sorted(rows):
        print("%7d   %s      [ln d = %.2f, ln(18 d a) = %.2f]"
              % (d, "   ".join(("%6.2f [%6.2f; %7.2f]" % v) if v is not None else "   (x < c'_d)           " for v in rows[d]),
                 math.log(d), math.log(18 * d * cu.a)))
    print()


if __name__ == '__main__':
    t0 = time.time()
    print("# Workstream Q, check 1: one level at finite n.  Exact side: experiments/reviews/R8/r8_flat.flat_run and its tables.")
    bad = Q.selftest()
    print()
    part_ABC()
    part_Bprime()
    part_D()
    part_Dexact()
    part_E()
    print("violations of proved inequalities: %d   (selftest failures: %d)   [%.0f s]" % (viol, bad, time.time() - t0))
