#!/usr/bin/env python3
"""Workstream Q2, check 6: Lemma U, Proposition D' and Proposition Q6(e) with a TOLERANCE b > 1 (the levels of the
variant without chains, section 5.4 of the report: the inner family has the least accuracy b, the ladder ends at b).
Saturating inner families, exact constants of Theorem 11.56, two independent evaluators.

Part A  D' with tolerance b in {2.5, 17.3, 45} (and b = 1 for comparison): accuracy X_D^b(N; phi) exactly; Lemma Q4(b)
        at the rate 0; constants with A_n^b; Lemma U(d); the bound n B' + c_D'^b + E(n, b; Lam + q^b).
Part B  Q6(e) with tolerance b, rates e/h in {0.5, 1, 2}: accuracy x-hat exactly; Lemma Q4(b) at the rate e; the
        range condition; Lemma U(d); the bound  max_i[n B_i - sigma_i' x-hat] + sigma'_+ (b + c_log + e) + ell_0^b + E.
        Below b + c_log(n) + e: the pass-through inequality.

usage: python3 q2_06_tolerance.py > out_q2_06_tolerance.txt          (about 5 minutes)
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
BS = (1.0, 2.5, 17.3, 45.0)

EFUNS = {
    'E=0': None,
    'E=Lam/7': lambda d, x, Lam: Lam / 7,
    'E=5/x+ln(Lam)': lambda d, x, Lam: 5 / x + math.log(Lam),
}

print("# Workstream Q2, check 6: Lemma U with a tolerance b (Proposition D' and Proposition Q6(e) at b > 1)")

# ------------------------------------------------------------------------------------------------ Part A
print("\n# Part A: D' with tolerance b")
print("#  u    b    cases   levels   viol   least slack of D' [nats] at (lines (B/h, sigma), R/h, phi, n, ln delta, E)   least slack of Lemma U(d)"
      "   range of c_D'^b   Q4(b): least radius margin, least ball slack   max|x_out - X|   pass-through cases")
tot = totv = 0
for u in (0.5, 1.0, 2.0):
    ev = L.Ev(u)
    cu = ev.cu
    a, h = cu.a, cu.h
    seq = Q.epoch_seq(cu, 13)
    cases = []
    for m in (0, 1, 3, 6, 10):
        cases.append(([(seq['B'][m], 1.0)], seq['R'][m], seq['phi'][m]))
    for (B, s, Rr) in ((a, 0.0, h), (a, 0.4, h), (1.5 * h, 0.7, h / 3), (3 * a, 1.0, min(1.0, 4 * h)), (h, 1.0, h)):
        cases.append(([(B, s)], Rr, Rr / (a + Rr)))
        cases.append(([(B, s)], Rr, 0.5 * Rr / (a + Rr)))
    cases.append(([(a, 1.0), (0.8 * a, 0.5), (0.6 * a, 0.0)], h, h / (a + h)))
    cases.append(([(1.6 * h, 1.0), (1.3 * h, 0.4), (1.1 * h, 0.1), (h, 0.0)], h / 4, 0.6 * (h / 4) / (a + h / 4)))
    for b in BS:
        viol = []
        nlev = npass = 0
        minD = (INF, None)
        minU = INF
        crng = [INF, -INF]
        minrad = INF
        minball = INF
        maxacc = 0.0
        for (lines, Rr, phi) in cases:
            n1 = 2
            while not L.Dprime_built(cu, n1, phi, b):
                n1 += 1
            Bp = L.Dprime_Bp(cu, lines, phi)
            Bt = L.Dprime_Bt(cu, lines, phi, b)
            for n in range(1, min(n1 + 30, 300)):
                if L.Dprime_built(cu, n, phi, b):
                    continue
                for ld in (math.log(0.5), -float(n)):
                    for ename, ef in EFUNS.items():
                        inner = L.SatLines(lines, Rr, ef)
                        calX = L.X_D(cu, max(n, 2), phi, b)
                        Lam = -ld + n * LN2
                        v = float(inner.costs(n, np.array([calX]), ld)[0])
                        bound = n * Bp + L.cDp(cu, n, Lam, Bt, b) + inner.E(n, b, Lam + L.qSb(cu, n, Lam, b))
                        npass += 1
                        if v > bound + 1e-9:
                            viol.append("pass-through n=%d %s" % (n, lines))
            ns = sorted(set([n1, n1 + 1, n1 + 5, 3 * n1] + [n for n in (1000, 10000, 100000, 1000000) if n >= n1]))
            for n in ns:
                big = n >= 100000
                for N in ((n,) if big else (n, 4 * n)):
                    calX = L.X_D(cu, N, phi, b)
                    for ld in ((math.log(0.05), -float(n)) if big else (math.log(0.5), math.log(0.05), -float(n), -20.0 * n)):
                        for ename, ef in EFUNS.items():
                            if ename != 'E=0' and (ld != -float(n) or N != n):
                                continue
                            inner = L.SatLines(lines, Rr, ef)
                            r = L.Dprime_level(ev, n, phi, Rr, calX, ld, inner, b)
                            c = r['c']
                            n_o, n_i = r['n_o'], r['n_i']
                            nlev += 1
                            Lam = -ld + n * LN2
                            E1_ = inner.E(n, b, Lam + L.qSb(cu, n, Lam, b))
                            maxacc = max(maxacc, abs(c['xout'] - calX))
                            if abs(c['xout'] - calX) > 1e-8 or r['xs'][-1] != b or np.any(np.abs(np.diff(r['xs'][1:]) + 1.0) > 1e-9):
                                viol.append("accuracy / ladder n=%d" % n)
                            r1 = min(n_o - 1, math.floor(cu.p * n_o) + 1)
                            minrad = min(minrad, c['rdag'] - r1)
                            sb = n_o * a + math.log(n_o + 1) - c['l_inv_pi']
                            minball = min(minball, sb)
                            if c['rdag'] < r1 or sb < -1e-9:
                                viol.append("Q4(b) n_o=%d" % n_o)
                            L.check_U_consts(cu, n, n_o, c, Lam, viol, ('D', b, n, ld), b)
                            bU = max(n_i * B + (1 - s) * n_o * a for (B, s) in lines) + L.ell0(cu, n, Lam, b) + E1_
                            minU = min(minU, bU - r['lC'])
                            if r['lC'] > bU + 1e-9:
                                viol.append("Lemma U(d) n=%d" % n)
                            cd = L.cDp(cu, n, Lam, Bt, b)
                            crng = [min(crng[0], cd), max(crng[1], cd)]
                            sl = n * Bp + cd + E1_ - r['lC']
                            if sl < minD[0]:
                                minD = (sl, ([(round(B / h, 3), s) for (B, s) in lines], round(Rr / h, 3), round(phi, 5), n, round(ld, 2), ename))
                            if sl < -1e-9:
                                viol.append("D' b=%g n=%d ld=%.3g %s" % (b, n, ld, lines))
        print("  %.1f  %5.1f  %3d  %6d  %3d   %8.3f at %s   %8.3f   [%.1f, %.1f]   %d, %.4f   %.1e   %d   [%.0f s]"
              % (u, b, len(cases), nlev, len(viol), minD[0], minD[1], minU, crng[0], crng[1], minrad, minball, maxacc, npass, time.time() - t0))
        for v in viol[:6]:
            print("     VIOLATION: " + v)
        sys.stdout.flush()
        tot += nlev
        totv += len(viol)
    print("  %.1f  the two evaluators on %d levels: largest difference %.2e; r_dagger, J or K differ on %d" % (u, ev.nlev, ev.maxdiff, ev.rdag_diff))
print("# Part A total: %d levels, %d violations" % (tot, totv))

# ------------------------------------------------------------------------------------------------ Part B
print("\n# Part B: Q6(e) with tolerance b")
print("#  u    b    e/h   types   levels   viol   least slack of Q6(e) [nats] at (lines (B/h, sigma), R/h, n, x-hat, ln delta, E)   least slack of Lemma U(d)"
      "   range of the error term   Q4(b): least radius margin, least ball slack   max|x_out - x-hat|   pass-through cases")
tot = totv = 0
for u in (0.5, 1.0, 2.0):
    ev = L.Ev(u)
    cu = ev.cu
    a, h = cu.a, cu.h
    seq = Q.epoch_seq(cu, 9)
    types = []
    for m in (0, 2, 5, 8):
        for j in sorted(set([0, 1, seq['J'][m] - 1])):
            if j <= seq['J'][m] - 1:                  # the slope before the last step of an epoch is (J_m - 1)/d_m <= 1
                types.append(([(seq['B'][m], j / seq['d'][m])], INF if j == 0 else h / j))
    for (lines_, R_) in types:
        assert all(0 <= s_ <= 1 for (B_, s_) in lines_)
    for (B, s, Rr) in ((h, 0.0, INF), (a, 0.3, h), (1.5 * h, 0.7, h / 3), (3 * a, 1.0, 2 * h), (h, 1.0, h)):
        types.append(([(B, s)], Rr))
    types.append(([(a, 1.0), (0.8 * a, 0.5), (0.6 * a, 0.0)], h))
    types.append(([(1.6 * h, 1.0), (1.3 * h, 0.4), (1.1 * h, 0.1), (h, 0.0)], h / 4))
    for b in BS[1:]:
        for ef_ in (0.5, 1.0, 2.0):
            e = ef_ * h
            th = cu.theta_na(e)
            rho_e = cu.rho_of(e)
            viol = []
            nlev = npass = 0
            minS = (INF, None)
            minU = INF
            crng = [INF, -INF]
            minrad = INF
            minball = INF
            maxacc = 0.0
            for (lines, Rr) in types:
                Rp = L.slope_e_Rp(cu, Rr, e)
                sigp = [L.slope_e_sigp(cu, B, s, e) for (B, s) in lines]
                sbar = max(sigp)
                n1 = 2
                while Rp * n1 < L.X0e(cu, n1, e, b):
                    n1 = max(n1 + 1, int(n1 * 1.05))
                while n1 > 2 and Rp * (n1 - 1) >= L.X0e(cu, n1 - 1, e, b):
                    n1 -= 1
                if n1 > 1000000:
                    continue
                for n in sorted(set([2, 10, max(1, n1 // 2), max(1, n1 - 1), n1, 10 * n1])):
                    X0 = L.X0e(cu, n, e, b)
                    for x in (b, 0.5 * (b + X0), X0 - 1e-9, 3 * X0, 1e9):
                        xh = min(x, Rp * n)
                        if xh >= X0:
                            continue
                        for ld in (math.log(0.5), -float(n)):
                            for ename, ef in EFUNS.items():
                                inner = L.SatLines(lines, Rr, ef)
                                Lam = -ld + n * LN2
                                v = float(inner.costs(n, np.array([x]), ld)[0])
                                bound = max(n * B - sp * xh for (B, s), sp in zip(lines, sigp)) + L.cSe(cu, n, Lam, sbar, e, b) \
                                    + inner.E(n, min(x, b), Lam + L.qSb(cu, n, Lam, b))
                                npass += 1
                                if v > bound + 1e-9:
                                    viol.append("pass-through n=%d x=%g" % (n, x))
                ns = sorted(set([n1, n1 + 1, 2 * n1] + [n for n in (10000, 100000, 1000000) if n >= n1]))
                ns = [n for n in ns if n <= 1000000]
                for n in ns:
                    big = n >= 100000
                    X0 = L.X0e(cu, n, e, b)
                    top = Rp * n
                    xset = sorted(set(x for x in ((X0, top) if big else (X0, X0 + 0.5, 0.5 * (X0 + top), top)) if X0 <= x <= top))
                    for xh in xset:
                        for ld in ((math.log(0.05), -float(n)) if big else (math.log(0.5), math.log(0.05), -float(n))):
                            for ename, ef in EFUNS.items():
                                if ename != 'E=0' and ld != -float(n):
                                    continue
                                inner = L.SatLines(lines, Rr, ef)
                                r = L.slope_e_level(ev, n, xh, e, ld, inner, b)
                                c = r['c']
                                n_o, n_i = r['n_o'], r['n_i']
                                nlev += 1
                                Lam = -ld + n * LN2
                                E1_ = inner.E(n, b, Lam + L.qSb(cu, n, Lam, b))
                                maxacc = max(maxacc, abs(c['xout'] - xh))
                                if abs(c['xout'] - xh) > 1e-7 or r['xs'][-1] != b:
                                    viol.append("accuracy n=%d xh=%g" % (n, xh))
                                r1 = min(n_o - 1, math.floor(rho_e * n_o) + 1)
                                minrad = min(minrad, c['rdag'] - r1)
                                sb = n_o * th + math.log(n_o + 1) - c['l_inv_pi']
                                minball = min(minball, sb)
                                if c['rdag'] < r1 or sb < -1e-9 or (Rr < INF and Rr * n_i < n_o * th - 1e-9):
                                    viol.append("Q4(b) / range n_o=%d" % n_o)
                                L.check_U_consts(cu, n, n_o, c, Lam, viol, ('S', b, n, xh, ld), b)
                                bU = max(n_i * B + (1 - s) * n_o * th for (B, s) in lines) + L.ell0(cu, n, Lam, b) + E1_
                                minU = min(minU, bU - r['lC'])
                                if r['lC'] > bU + 1e-9:
                                    viol.append("Lemma U(d) n=%d xh=%g" % (n, xh))
                                ce = L.cSe(cu, n, Lam, sbar, e, b)
                                crng = [min(crng[0], ce), max(crng[1], ce)]
                                sl = max(n * B - sp * xh for (B, s), sp in zip(lines, sigp)) + ce + E1_ - r['lC']
                                if sl < minS[0]:
                                    minS = (sl, ([(round(B / h, 3), round(s, 3)) for (B, s) in lines], (round(Rr / h, 3) if Rr < INF else INF), n, round(xh, 3),
                                                 round(ld, 2), ename))
                                if sl < -1e-9:
                                    viol.append("Q6(e) b=%g n=%d xh=%g" % (b, n, xh))
            print("  %.1f  %5.1f  %.1f  %3d  %6d  %3d   %8.3f at %s   %8.3f   [%.1f, %.1f]   %d, %.4f   %.1e   %d   [%.0f s]"
                  % (u, b, ef_, len(types), nlev, len(viol), minS[0], minS[1], minU, crng[0], crng[1], minrad, minball, maxacc, npass, time.time() - t0))
            for v in viol[:6]:
                print("     VIOLATION: " + v)
            sys.stdout.flush()
            tot += nlev
            totv += len(viol)
    print("  %.1f  the two evaluators on %d levels: largest difference %.2e; r_dagger, J or K differ on %d" % (u, ev.nlev, ev.maxdiff, ev.rdag_diff))
print("# Part B total: %d levels, %d violations" % (tot, totv))
print("\n# done in %.0f s" % (time.time() - t0))
