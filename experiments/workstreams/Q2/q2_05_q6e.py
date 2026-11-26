#!/usr/bin/env python3
"""Workstream Q2, check 5 (Part B): Proposition Q6(e) -- the slope step at a general outer rate e -- and its corollary
for types that are a maximum of finitely many lines, one level at a time, with SATURATING inner families
(certified cost exactly max(0, max_i[d B_i - sigma_i min(x, R d)]) + E), exact constants of Theorem 11.56,
two independent evaluators.

Rates e on both sides of h:  e/h in {0.2, 0.5, 0.8, 1, 1.25, 2, 3} and e = 0.97 eps*.
Types: (i) the epoch schedule (B_m, j/d_m, h/j);  (ii) one line, any 0 <= sigma <= 1, several ranges (R = inf for
sigma = 0);  (iii) maxima of three or four lines.  Sizes from the first n at which a level exists to 10^6, accuracies
at both ends of [X_0^e(n), R'n], delta from 0.5 to e^{-n}.
Checked at every level: accuracy = x-hat exactly; Lemma Q4(b) at the rate e (radius and ball); the constants of
Lemma U and (2.1); the range condition n_o theta_na(e) <= R n_i; Lemma U(d); the bound of Proposition Q6(e).
Below X_0^e(n): the pass-through inequality.
Part C: the level of Proposition Q6 of Q_REPORT itself (e = h, ladder capped at ceil(x-hat)) against the sharper
error term of Lemma U:  sigma'(1 + c_log(n) + h) + ell_0  instead of  (B/h)(1 + c_log(n) + h) + ell_0.

usage: python3 q2_05_q6e.py > out_q2_05_q6e.txt          (about 20 minutes)
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


def first_n(cu, Rp, e):
    n = 2
    while Rp * n < L.X0e(cu, n, e):
        n = max(n + 1, int(n * 1.05))
    while n > 2 and Rp * (n - 1) >= L.X0e(cu, n - 1, e):
        n -= 1
    return n


def types_for(cu, seq):
    a, h = cu.a, cu.h
    g = {'schedule': [], 'one line': [], 'max of lines': []}
    for m in range(9):
        for j in range(seq['J'][m]):
            if j <= 2 or j == seq['J'][m] - 1:
                g['schedule'].append(([(seq['B'][m], j / seq['d'][m])], INF if j == 0 else h / j))
    for B in (h, 1.5 * h, a, 3 * a):
        for (s, Rr) in ((0.0, INF), (0.0, h), (0.3, h), (0.7, h / 3), (1.0, h), (1.0, h / 3), (0.5, 2 * h), (1.0, 2 * h), (0.2, h / 20)):
            if Rr < INF and B < s * Rr:
                continue            # a line that is negative on its range is the type of no family
            g['one line'].append(([(B, s)], Rr))
    for Rr in (h, h / 4, 2 * h):
        g['max of lines'].append(([(a, 1.0), (0.8 * a, 0.5), (0.6 * a, 0.0)], Rr))
        g['max of lines'].append(([(1.6 * h, 1.0), (1.3 * h, 0.4), (1.1 * h, 0.1), (h, 0.0)], Rr))
        g['max of lines'].append(([(h, 1.0), (2 * a, 0.0)], Rr))
        g['max of lines'].append(([(1.2 * h, 0.9), (1.15 * h, 0.6), (1.05 * h, 0.2)], Rr))
    return g


print("# Workstream Q2, check 5 (Part B): Proposition Q6(e), saturating inner families, exact constants, two evaluators")
print("#  u   e/h   theta_na(e)/a   types   levels   viol   least slack of Q6(e) [nats] at (kind, lines (B/h, sigma), R/h, n, x-hat, ln delta, E)"
      "   least slack of Lemma U(d)   range of the error term   Q4(b): least radius margin, least ball slack   max|x_out - x-hat|   pass-through cases   [time]")
grand = grand_viol = 0
for u in (0.5, 1.0, 2.0):
    ev = L.Ev(u)
    cu = ev.cu
    a, h, es = cu.a, cu.h, cu.eps_star
    seq = Q.epoch_seq(cu, 9)
    groups = types_for(cu, seq)
    rates = [f * h for f in (0.2, 0.5, 0.8, 1.0, 1.25, 2.0, 3.0)] + [0.97 * es]
    for e in rates:
        th = cu.theta_na(e)
        rho_e = cu.rho_of(e)
        viol = []
        nlev = npass = ntyp = 0
        minS = (INF, None)
        minU = INF
        crng = [INF, -INF]
        minrad = INF
        minball = INF
        maxacc = 0.0
        for kind, cases in groups.items():
            for ci, (lines, Rr) in enumerate(cases):
                ntyp += 1
                Rp = L.slope_e_Rp(cu, Rr, e)
                sigp = [L.slope_e_sigp(cu, B, s, e) for (B, s) in lines]
                sbar = max(sigp)
                n1 = first_n(cu, Rp, e)
                if n1 > 1000000:
                    continue
                ns = sorted(set([n1, n1 + 1, n1 + 7, 2 * n1, 5 * n1] + [n for n in (1000, 10000, 100000, 1000000) if n >= n1]))
                ns = [n for n in ns if n <= 1000000]
                # pass-through: accuracies with x-hat < X_0^e(n)
                for n in sorted(set([1, 2, 3, 10, max(1, n1 // 2), max(1, n1 - 1), n1, 10 * n1])):
                    X0 = L.X0e(cu, n, e)
                    for x in (1.0, 0.5 * X0, X0 - 1e-9, 3 * X0, 1e9):
                        xh = min(x, Rp * n)
                        if xh >= X0:
                            continue
                        for ld in (math.log(0.5), -float(n)):
                            for ename, ef in EFUNS.items():
                                inner = L.SatLines(lines, Rr, ef)
                                Lam = -ld + n * LN2
                                v = float(inner.costs(n, np.array([x]), ld)[0])
                                bound = max(n * B - sp * xh for (B, s), sp in zip(lines, sigp)) + L.cSe(cu, n, Lam, sbar, e) \
                                    + inner.E(n, min(x, 1.0), Lam + Q.qS(cu, n, Lam))
                                npass += 1
                                if v > bound + 1e-9:
                                    viol.append("pass-through n=%d x=%g %s R=%g" % (n, x, lines, Rr))
                for n in ns:
                    big = n >= 100000
                    if big and kind != 'schedule' and ci % 3 != 0:
                        continue
                    if n == 1000000 and ci % 2 != 0:
                        continue
                    X0 = L.X0e(cu, n, e)
                    top = Rp * n
                    if big:
                        xset = [X0, 0.5 * (X0 + top), top]
                        lds = (math.log(0.05), -float(n))
                    else:
                        xset = [X0, X0 + 1e-9, X0 + 0.5, float(math.ceil(X0)), 0.5 * (X0 + top), top - 1e-9, top]
                        lds = (math.log(0.5), math.log(0.05), math.log(1e-12), -float(n))
                    xset = sorted(set(x for x in xset if X0 <= x <= top))
                    for xh in xset:
                        for ld in lds:
                            for ename, ef in EFUNS.items():
                                if ename != 'E=0' and (ld != lds[-1] or xh != xset[-1]):
                                    continue
                                inner = L.SatLines(lines, Rr, ef)
                                r = L.slope_e_level(ev, n, xh, e, ld, inner)
                                c = r['c']
                                n_o, n_i = r['n_o'], r['n_i']
                                nlev += 1
                                Lam = -ld + n * LN2
                                E1_ = inner.E(n, 1.0, Lam + Q.qS(cu, n, Lam))
                                maxacc = max(maxacc, abs(c['xout'] - xh))
                                if abs(c['xout'] - xh) > 1e-7:
                                    viol.append("accuracy n=%d xh=%g" % (n, xh))
                                r1 = min(n_o - 1, math.floor(rho_e * n_o) + 1)
                                minrad = min(minrad, c['rdag'] - r1)
                                sb = n_o * th + math.log(n_o + 1) - c['l_inv_pi']
                                minball = min(minball, sb)
                                if c['rdag'] < r1 or sb < -1e-9:
                                    viol.append("Q4(b) n_o=%d e=%g" % (n_o, e))
                                lth = L.ltheta_exact(cu, n, xh)
                                if lth < math.log(3 * (n_o + 1)) + 2 * u + math.exp(u) + n_o * e - 1e-9 or (Rr < INF and Rr * n_i < n_o * th - 1e-9) \
                                        or lth < xh - 1 - LN2 - 1e-12:
                                    viol.append("hypothesis of Lemma U n=%d xh=%g" % (n, xh))
                                L.check_U_consts(cu, n, n_o, c, Lam, viol, (kind, n, xh, ld))
                                bU = max(n_i * B + (1 - s) * n_o * th for (B, s) in lines) + L.ell0(cu, n, Lam) + E1_
                                minU = min(minU, bU - r['lC'])
                                if r['lC'] > bU + 1e-9:
                                    viol.append("Lemma U(d) n=%d xh=%g" % (n, xh))
                                ce = L.cSe(cu, n, Lam, sbar, e)
                                crng = [min(crng[0], ce), max(crng[1], ce)]
                                bS = max(n * B - sp * xh for (B, s), sp in zip(lines, sigp)) + ce + E1_
                                sl = bS - r['lC']
                                if sl < minS[0]:
                                    minS = (sl, (kind, [(round(B / h, 3), round(s, 3)) for (B, s) in lines], (round(Rr / h, 4) if Rr < INF else INF), n,
                                                 round(xh, 4), round(ld, 2), ename))
                                if sl < -1e-9:
                                    viol.append("Q6(e) n=%d xh=%g ld=%.3g %s R=%g: lC=%.4f bound=%.4f" % (n, xh, ld, lines, Rr, r['lC'], bS))
        print("  %.1f  %.2f  %.4f  %3d  %6d  %3d   %8.3f at %s   %8.3f   [%.1f, %.1f]   %d, %.4f   %.1e   %d   [%.0f s]"
              % (u, e / h, th / a, ntyp, nlev, len(viol), minS[0], minS[1], minU, crng[0], crng[1], minrad, minball, maxacc, npass, time.time() - t0))
        for v in viol[:8]:
            print("     VIOLATION: " + v)
        sys.stdout.flush()
        grand += nlev
        grand_viol += len(viol)
    print("  %.1f  the two evaluators on %d levels: largest difference %.2e in ln C_max / ln delta' / x_out; r_dagger, J or K differ on %d levels"
          % (u, ev.nlev, ev.maxdiff, ev.rdag_diff))
print("# Parts A/B total: %d levels built, %d violations" % (grand, grand_viol))

# ------------------------------------------------------------------------------------------------ Part C
print("\n# Part C: the level of Proposition Q6 of Q_REPORT (e = h, ladder capped at ceil(x-hat)) against the sharper error term of Lemma U")
print("#  u   types   levels   viol   least slack of [n B - sigma' x-hat + sigma'(1 + c_log + h) + ell_0 + E_1] - exact   at   |   the same with Q's c_S"
      "   | largest (c_S - sharper term)")
for u in (0.5, 1.0, 2.0):
    ev = L.Ev(u)
    cu = ev.cu
    a, h = cu.a, cu.h
    seq = Q.epoch_seq(cu, 13)
    cases = []
    for m in range(13):
        for j in range(seq['J'][m]):
            if j <= 2 or j == seq['J'][m] - 1:
                cases.append((seq['B'][m], j / seq['d'][m], INF if j == 0 else h / j))
    for B in (h, 1.01 * h, 2 * h, 11 * h):
        cases.append((B, 0.0, INF))
        for s in (0.0, 0.3, 1.0):
            for Rf in (1.0, 1 / 3, 1 / 50):
                cases.append((B, s, h * Rf))
    viol = []
    nlev = 0
    minS = (INF, None)
    minQ = INF
    maxd = 0.0
    for (B, s, Rr) in cases:
        Rp = h if Rr == INF else Rr * h / (h + Rr)
        sp = s + B / h - 1
        n1 = first_n(cu, Rp, h)
        if n1 > 1000000:
            continue
        ns = sorted(set([n1, n1 + 1, 2 * n1] + [n for n in (1000, 10000, 100000, 1000000) if n >= n1]))
        ns = [n for n in ns if n <= 1000000]
        for n in ns:
            X0 = Q.X0(cu, n)
            top = Rp * n
            for xh in sorted(set(x for x in (X0, X0 + 0.5, 0.5 * (X0 + top), top) if X0 <= x <= top)):
                for ld in (math.log(0.05), -float(n), -50.0 * n):
                    inner = L.SatLines([(B, s)], Rr)
                    n_o = int(math.floor((xh - 1 - Q.c_log(cu, n)) / h + 1e-12))
                    r = L.level_U(ev, n, n_o, L.ltheta_exact(cu, n, xh), xh, ld, inner)        # cap Xi = x-hat: the ladder of Q6
                    nlev += 1
                    Lam = -ld + n * LN2
                    sharp = L.cSe(cu, n, Lam, sp, h)
                    sl = n * B - sp * xh + sharp - r['lC']
                    slQ = n * B - sp * xh + Q.cS(cu, n, Lam, B) - r['lC']
                    maxd = max(maxd, Q.cS(cu, n, Lam, B) - sharp)
                    minQ = min(minQ, slQ)
                    if sl < minS[0]:
                        minS = (sl, (round(B / h, 3), round(s, 3), (round(Rr / h, 4) if Rr < INF else INF), n, round(xh, 3), round(ld, 2)))
                    if sl < -1e-9:
                        viol.append("n=%d xh=%g B/h=%g s=%g" % (n, xh, B / h, s))
    print("  %.1f  %3d  %6d  %3d   %8.3f at %s   |   %8.3f   |   %.2f   [%.0f s]" % (u, len(cases), nlev, len(viol), minS[0], minS[1], minQ, maxd, time.time() - t0))
    for v in viol[:8]:
        print("     VIOLATION: " + v)
    sys.stdout.flush()
print("\n# done in %.0f s" % (time.time() - t0))
