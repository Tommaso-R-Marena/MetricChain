#!/usr/bin/env python3
"""Workstream Q2, check 1: Proposition D' (the drop at a logarithmic accuracy) and one level of the chain T,
each with SATURATING inner families (certified cost exactly the majorant that the type allows), evaluated with the
exact constants of Theorem 11.56 by two independent evaluators (qlib of workstream Q, r12lib of referee R12).

Part A0 what a drop costs at the parameters of the schedule (a table for the report).
Part A  Proposition D' / Lemma U at e = 0.  Inner family: max(0, max_i[d B_i - sigma_i min(x, R d)]) + E.
        (i) the epoch schedule (B_m, 1, R_m), phi_m, m <= 12;  (ii) one line with any slope 0 <= sigma <= 1, several
        ranges R and outer fractions phi <= R/(a+R);  (iii) maxima of several lines.
        Sizes: from the first n at which the level exists to 10^6; delta from 0.5 to e^{-n}; horizon N = n and 3n.
        Checked at every level: accuracy = X exactly; Lemma Q4(b) at e = 0 (radius and ball); the constants of
        Lemma U; (2.1); Lemma U(d); the bound of Proposition D'.  Below the first size: the pass-through inequality.
Part B  One level of the chain T (Proposition T).  The inner family G' is saturating (cost d B' + E) and the
        procedure of the fine rung is given EXACTLY the bound that Proposition T claims for the chain below.
        Checked: accuracy <= a_d; ln(1/pi_dagger) <= varpi(m; c); the constants; (2.1); the induction step.
        Blocks: the block of the design and blocks half / twice as long (a shorter block makes Delta_T > 0).

usage: python3 q2_01_levels.py > out_q2_01_levels.txt          (about 2 minutes)
"""
import math
import sys
import time

import numpy as np

import q2lib as L

Q = L.Q
LN2 = L.LN2
INF = L.INF
t0 = time.time()

EFUNS = {
    'E=0': None,
    'E=3sqrt(d)': lambda d, x, Lam: 3 * math.sqrt(d),
    'E=Lam/7': lambda d, x, Lam: Lam / 7,
    'E=5/x+ln(Lam)': lambda d, x, Lam: 5 / x + math.log(Lam),
}


def first_n_D(cu, phi):
    n = 2
    while not L.Dprime_built(cu, n, phi):
        n += 1
    return n


print("# Workstream Q2, check 1: Proposition D' and one level of the chain T, saturating inner families, exact constants")
print("# (every level evaluated by qlib and by r12lib; the largest disagreement is printed at the end of each block)")

# ------------------------------------------------------------------------------------------------ Part A0
print("\n# Part A0: what a drop D' costs, at the parameters of the schedule (inner family saturating of slope one, E = 0; delta = 0.05, N = n)")
print("#  u   m   B_{m+1}/a   phi_m   n   X_D   n_o   r_dagger (Lemma Q4(b) needs >=)   ln(1/pi_dagger) - n_o a   ln C_max - n B_{m+1}   c_D' (bound)   slack")
for u in (0.5, 1.0, 2.0):
    ev = L.Ev(u)
    cu = ev.cu
    seq = Q.epoch_seq(cu, 13)
    for m in (0, 6):
        B, Rr, phi = seq['B'][m], seq['R'][m], seq['phi'][m]
        for n in (1000, 10000, 100000, 1000000):
            ld = math.log(0.05)
            calX = L.X_D(cu, n, phi)
            r = L.Dprime_level(ev, n, phi, Rr, calX, ld, L.SatLines([(B, 1.0)], Rr))
            c = r['c']
            Bp = L.Dprime_Bp(cu, [(B, 1.0)], phi)
            cd = L.cDp(cu, n, -ld + n * LN2, L.Dprime_Bt(cu, [(B, 1.0)], phi))
            print("  %.1f  %2d  %.4f  %.4f  %7d  %.2f  %6d  %6d (%6d)  %9.1f  %7.2f  %6.2f  %6.2f"
                  % (u, m, Bp / cu.a, phi, n, calX, r['n_o'], c['rdag'], min(r['n_o'] - 1, math.floor(cu.p * r['n_o']) + 1), c['l_inv_pi'] - r['n_o'] * cu.a,
                     r['lC'] - n * Bp, cd, n * Bp + cd - r['lC']))

# ------------------------------------------------------------------------------------------------ Part A
print("\n# Part A: Proposition D' (Lemma U at e = 0)")
print("#  u   kind   cases   levels   viol   least slack of D' [nats] at (lines, R/h, phi, n, N, ln delta, E)   least slack of Lemma U(d)"
      "   range of c_D'   least slack of Q4(b): radius, ball   max|x_out - X|   pass-through cases   [time]")
grandA = 0
grand_viol = 0
for u in (0.5, 1.0, 2.0):
    ev = L.Ev(u)
    cu = ev.cu
    a, h = cu.a, cu.h
    seq = Q.epoch_seq(cu, 13)
    groups = {'schedule': [], 'one line': [], 'max of lines': []}
    for m in range(13):
        groups['schedule'].append(([(seq['B'][m], 1.0)], seq['R'][m], seq['phi'][m]))
    for B in (h, a, 3 * a):
        for s in (0.0, 0.3, 0.7, 1.0):
            for Rr in (h, h / 3, h / 50, min(1.0, 6 * h)):
                if B < s * Rr:
                    continue        # a line that is negative on its range is the type of no family (certified bounds are >= 0)
                for pf in (1.0, 0.5):
                    groups['one line'].append(([(B, s)], Rr, pf * Rr / (a + Rr)))
    for Rr in (h, h / 4, min(1.0, 3 * h)):
        for pf in (1.0, 0.6):
            phi = pf * Rr / (a + Rr)
            groups['max of lines'].append(([(a, 1.0), (0.8 * a, 0.5), (0.6 * a, 0.0)], Rr, phi))
            groups['max of lines'].append(([(1.6 * h, 1.0), (1.3 * h, 0.4), (1.1 * h, 0.1), (h, 0.0)], Rr, phi))
            groups['max of lines'].append(([(h, 1.0), (2 * a, 0.0)], Rr, phi))
    for kind, cases in groups.items():
        viol = []
        nlev = npass = 0
        minD = (INF, None)
        minU = INF
        crng = [INF, -INF]
        minrad = INF
        minball = INF
        maxacc = 0.0
        for ci, (lines, Rr, phi) in enumerate(cases):
            n1 = first_n_D(cu, phi)
            ns = sorted(set([n1, n1 + 1, n1 + 7, 2 * n1 + 3, 5 * n1] + [n for n in (1000, 10000, 100000, 1000000) if n >= n1]))
            ns = [n for n in ns if n <= 1000000]
            Bp = L.Dprime_Bp(cu, lines, phi)
            Bt = L.Dprime_Bt(cu, lines, phi)
            # pass-through below the first size (and wherever the level is not built)
            for n in range(1, min(n1 + 40, 400)):
                if L.Dprime_built(cu, n, phi):
                    continue
                for ld in (math.log(0.5), -float(n)):
                    for ename, ef in EFUNS.items():
                        inner = L.SatLines(lines, Rr, ef)
                        N = max(n, 2)
                        calX = L.X_D(cu, N, phi)
                        Lam = -ld + n * LN2
                        v = float(inner.costs(n, np.array([calX]), ld)[0])
                        bound = n * Bp + L.cDp(cu, n, Lam, Bt) + inner.E(n, 1.0, Lam + Q.qS(cu, n, Lam))
                        npass += 1
                        if v > bound + 1e-9:
                            viol.append("pass-through n=%d %s" % (n, lines))
            for n in ns:
                big = n >= 100000
                if big and kind != 'schedule' and ci % 3 != 0:
                    continue
                lds = (math.log(0.05), -float(n)) if big else (math.log(0.5), math.log(0.05), math.log(1e-12), -float(n))
                for N in ((n,) if big else (n, 3 * n)):
                    calX = L.X_D(cu, N, phi)
                    for ld in lds:
                        for ename, ef in EFUNS.items():
                            if ename != 'E=0' and (ld != lds[-1] or N != n):
                                continue
                            inner = L.SatLines(lines, Rr, ef)
                            r = L.Dprime_level(ev, n, phi, Rr, calX, ld, inner)
                            c = r['c']
                            n_o, n_i = r['n_o'], r['n_i']
                            nlev += 1
                            Lam = -ld + n * LN2
                            E1_ = inner.E(n, 1.0, Lam + Q.qS(cu, n, Lam))
                            # accuracy
                            maxacc = max(maxacc, abs(c['xout'] - calX))
                            if abs(c['xout'] - calX) > 1e-8:
                                viol.append("accuracy n=%d" % n)
                            # Lemma Q4(b) at e = 0
                            r1 = min(n_o - 1, math.floor(cu.p * n_o) + 1)
                            minrad = min(minrad, c['rdag'] - r1)
                            sb = n_o * a + math.log(n_o + 1) - c['l_inv_pi']
                            minball = min(minball, sb)
                            if c['rdag'] < r1 or sb < -1e-9:
                                viol.append("Q4(b) n_o=%d" % n_o)
                            # the hypothesis theta >= 3(n_o+1)e^{2u+e^u} and the cap
                            lth = L.ltheta_exact(cu, n, calX)
                            if lth < math.log(3 * (n_o + 1)) + 2 * u + math.exp(u) - 1e-12 or Rr * n_i < n_o * a - 1e-9:
                                viol.append("hypothesis of Lemma U n=%d" % n)
                            L.check_U_consts(cu, n, n_o, c, Lam, viol, (kind, n, ld))
                            # Lemma U(d)
                            bU = max(n_i * B + (1 - s) * n_o * a for (B, s) in lines) + L.ell0(cu, n, Lam) + E1_
                            minU = min(minU, bU - r['lC'])
                            if r['lC'] > bU + 1e-9:
                                viol.append("Lemma U(d) n=%d" % n)
                            # Proposition D'
                            cd = L.cDp(cu, n, Lam, Bt)
                            crng = [min(crng[0], cd), max(crng[1], cd)]
                            bD = n * Bp + cd + E1_
                            sl = bD - r['lC']
                            if sl < minD[0]:
                                minD = (sl, ([(round(B / h, 3), s) for (B, s) in lines], round(Rr / h, 4), round(phi, 5), n, N, round(ld, 2), ename))
                            if sl < -1e-9:
                                viol.append("D' n=%d ld=%.3g %s: lC=%.4f bound=%.4f" % (n, ld, lines, r['lC'], bD))
        print("  %.1f  %-13s %3d  %6d  %3d   %8.3f at %s   %8.3f   [%.1f, %.1f]   %d, %.4f   %.1e   %d   [%.0f s]"
              % (u, kind, len(cases), nlev, len(viol), minD[0], minD[1], minU, crng[0], crng[1], minrad, minball, maxacc, npass, time.time() - t0))
        for v in viol[:8]:
            print("     VIOLATION: " + v)
        sys.stdout.flush()
        grandA += nlev
        grand_viol += len(viol)
    print("  %.1f  the two evaluators on %d levels: largest difference %.2e in ln C_max / ln delta' / x_out; r_dagger, J or K differ on %d levels"
          % (u, ev.nlev, ev.maxdiff, ev.rdag_diff))
print("# Part A total: %d levels built, %d violations" % (grandA, grand_viol))

# ------------------------------------------------------------------------------------------------ Part B
print("\n# Part B: one level of the chain T (induction step of Proposition T), saturating G' and saturated chain below")
print("#  u   chains   levels   viol   least slack of the step [nats] at (e, alpha, N, m, d, ln delta, E)   least slack of varpi"
      "   largest x_out - a_d   levels with Delta_T > 0   [time]")
grandB = 0
grand_violB = 0
for u in (0.5, 1.0, 2.0):
    ev = L.Ev(u)
    cu = ev.cu
    seq = Q.epoch_seq(cu, 13)
    viol = []
    nlev = nch = ndelta = 0
    minS = (INF, None)
    minV = INF
    maxacc = -INF
    for e in (0, 1, 2, 4, 8, 12):
        Bp = seq['B'][e] if e >= 1 else cu.a
        for alpha in (1.0, 0.1, 0.001):
            for N in (1000, 10000, 100000, 1000000):
                calX = L.X_D(cu, N, seq['phi'][e - 1]) if e >= 1 else L.X_B(cu, N)
                for ldN in (math.log(0.05), -float(N)):
                    m0 = L.Chain.design_m(cu, N, Bp, calX, alpha, -ldN + N * LN2)
                    for m in sorted(set([m0, max(1, m0 // 2), 2 * m0, max(1, m0 // 7)])):
                        ch = L.Chain(cu, N, Bp, calX, alpha, m)
                        if ch.d0 > N:
                            continue
                        nch += 1
                        ds = sorted(set([ch.d0, ch.d0 + 1, ch.d0 + m - 1, ch.d0 + m, 2 * ch.d0, (N + ch.d0) // 2, N - 1, N]))
                        ds = [d for d in ds if ch.d0 <= d <= N]
                        for d in ds:
                            for ld in (math.log(0.5), math.log(0.05), -float(d), -30.0 * d):
                                for ename, ef in EFUNS.items():
                                    if ename != 'E=0' and (ld != -float(d) or d not in (ds[0], ds[-1])):
                                        continue

                                    def U(dd, Lam):
                                        Ls = ch.Lam_star(dd, Lam)
                                        E = 0.0 if ef is None else ef(dd, calX, Ls)
                                        return max(E + ch.a_T(dd, Ls), ch.e0(Ls)) + ch.j(dd) * ch.Delta_T(dd, Ls)

                                    b = ch.tol(d)
                                    c = ev.consts(d, m, ch.c, ch.c, ch.c, math.log(ch.c), 2 * math.exp(u) * m / ch.c, b, ld, 2)
                                    Lam = -ld + d * LN2
                                    Lam1 = -c['ldeltap'] + (d - m) * LN2
                                    lc1 = (d - m) * Bp + (0.0 if ef is None else ef(d - m, calX, Lam1))
                                    lc2 = (d - m) * Bp + U(d - m, Lam1)
                                    lC, arg = ev.cmax(c, [2 * u * (d - m), calX, b], [lc1, lc2])
                                    nlev += 1
                                    # accuracy, the ball, the constants, (2.1)
                                    maxacc = max(maxacc, c['xout'] - ch.acc(d))
                                    if c['xout'] > ch.acc(d) + 1e-12 or ch.acc(d) > alpha + 1e-12 or b <= 0:
                                        viol.append("accuracy d=%d" % d)
                                    sv = L.varpi(cu, m, ch.c) - c['l_inv_pi']
                                    minV = min(minV, sv)
                                    An = Q.A_n(cu, d)
                                    okc = (c['J'] + 1 <= An / ch.c * (1 + 1e-12) and c['nu0'] <= Q.nubarD(cu, d, ch.c) * (1 + 1e-12)
                                           and c['m_max'] + 1 <= d + 2 + math.log2(5.6 * Q.nubarD(cu, d, ch.c)) + 1e-9
                                           and c['K'] <= Q.KbarD(cu, d, -ld, ch.c) * (1 + 1e-12)
                                           and c['P_cnt'] <= Q.PcntD(cu, d, -ld, ch.c) + 1e-9 and c['P_M'] <= Q.PMD(cu, d, -ld, ch.c) + 1e-9
                                           and Lam1 <= Lam + L.qT(cu, d, Lam, ch.c) + 1e-9 and 2 * u * (d - m) > calX > b)
                                    if sv < -1e-9 or not okc:
                                        viol.append("constants d=%d m=%d" % (d, m))
                                    if ch.Delta_T(d, ch.Lam_star(d, Lam)) > 0:
                                        ndelta += 1
                                    bound = d * Bp + U(d, Lam)
                                    sl = bound - lC
                                    if sl < minS[0]:
                                        minS = (sl, (e, alpha, N, m, d, round(ld, 2), ename))
                                    if sl < -1e-9:
                                        viol.append("step e=%d alpha=%g N=%d m=%d d=%d ld=%.3g %s: lC=%.4f bound=%.4f" % (e, alpha, N, m, d, ld, ename, lC, bound))
    print("  %.1f  %5d  %7d  %3d   %8.3f at %s   %8.3f   %.2e   %d   [%.0f s]"
          % (u, nch, nlev, len(viol), minS[0], minS[1], minV, maxacc, ndelta, time.time() - t0))
    for v in viol[:8]:
        print("     VIOLATION: " + v)
    print("  %.1f  the two evaluators on %d levels: largest difference %.2e; r_dagger, J or K differ on %d levels" % (u, ev.nlev, ev.maxdiff, ev.rdag_diff))
    sys.stdout.flush()
    grandB += nlev
    grand_violB += len(viol)
print("# Part B total: %d levels, %d violations" % (grandB, grand_violB))
print("\n# done in %.0f s" % (time.time() - t0))
