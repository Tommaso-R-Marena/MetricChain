#!/usr/bin/env python3
"""Workstream Q2, check 3: the bound of Theorem A in numbers (formula evaluation only), against the bound of
Theorem Q8 of Q_REPORT (its formula (5.2), qlib.E_total -- the table of its section 7.4).

Columns "old": (5.2) of Q_REPORT.  "new/Q": Theorem A with the slope-step error c_S of Q_REPORT.
"new": Theorem A with the slope-step error of Lemma U (sigma'(1 + c_log + h) + ell_0).  "no-chain": the variant
of section 5.4 (drops D' without chains; tolerances b_m).  Every bound is minimised over the number of epochs M
(and never taken above n ln 2, the cost of enumeration).

Part A  the table: u = 1, eps = 1, delta = 0.05, n = 10^3 ... 10^12
Part B  where the new bound is below the old one (scan, 10 sizes per decade)
Part C  other parameters (eps, delta, u)
Part D  the accuracy enters additively: bound(eps) - bound(1) against ln(1/eps)
Part E  the closed form of Proposition A' against (A.1); the constants C_* and C_*'
Part F  the terms of the closed form: the level term, the second term (chains, drops, base) against (ln n)^2

usage: python3 q2_03_formula.py > out_q2_03_formula.txt          (about 4 minutes)
"""
import math
import sys
import time

import q2lib as L

Q = L.Q
LN2 = L.LN2
t0 = time.time()
MMAX = 46


def best(f, cu, n, seq, kcap=None):
    """min over M of n B_M + f(M); stops when k_M exceeds kcap, or when five consecutive M have not improved the
    minimum (n B_M decreases and the error term increases with M)"""
    bv = None
    for M in range(0, MMAX):
        if kcap is not None and seq['k'][M] > kcap:
            break
        v = n * seq['B'][M] + f(M)
        if bv is None or v < bv[0]:
            bv = (v, M)
        elif M - bv[1] >= 5:
            break
    return bv


def all_best(cu, n, eps, dl, seq, trap=True):
    kcap = 6 * math.sqrt(n) + 20
    o = best(lambda M: L.E_old(cu, n, eps, dl, M, seq), cu, n, seq, kcap)
    nq = best(lambda M: L.E_new(cu, n, eps, dl, M, seq, sharp=False), cu, n, seq, kcap)
    nw = best(lambda M: L.E_new(cu, n, eps, dl, M, seq, sharp=True), cu, n, seq, kcap)
    tr = best(lambda M: L.E_trap(cu, n, eps, dl, M, seq), cu, n, seq, kcap) if trap else None
    return o, nq, nw, tr


print("# Workstream Q2, check 3: the bound of Theorem A against the bound of Theorem Q8 (formula evaluation)")
for u in (1.0,):
    cu = Q.Cube(u)
    seq = Q.epoch_seq(cu, MMAX + 1)
    print("\n# constants at u = %g: a = %.6f, h = %.6f, h/a = %.5f, c1 = %.4f, rbar = %.4f, kappa = %.5f" % (u, cu.a, cu.h, cu.h / cu.a, cu.c1, cu.rbar, cu.kappa))

# ------------------------------------------------------------------------------------------------ Part A
print("\n# Part A: u = 1, eps = 1, delta = 0.05; bounds in units of n a; (b - nh)/sqrt(n ln n) in brackets")
print("#   n      | old: M  bound      | new/Q: M  bound      | new: M  k_M  bound      [ratio]  | no-chain: M  bound   | old - new [nats]  (old - new)/(old - nh)"
      " | new: E = base + slope steps (number x mean) + drops D' (number x mean) + chains (number x mean); Lam_end/Lam_0")
cu = Q.Cube(1.0)
seq = Q.epoch_seq(cu, MMAX + 1)
dl = math.log(1 / 0.05)
rows = {}
for n in (10 ** 3, 10 ** 4, 16000, 32000, 64000, 10 ** 5, 10 ** 6, 10 ** 7, 10 ** 8, 10 ** 9, 10 ** 10, 10 ** 11, 10 ** 12):
    o, nq, nw, tr = all_best(cu, n, 1.0, dl, seq)
    na = n * cu.a
    nh = n * cu.h
    rt = math.sqrt(n * math.log(n))
    cap = n * LN2
    pr = L.E_new(cu, n, 1.0, dl, nw[1], seq, detail=True)
    rows[n] = (o, nq, nw, tr, pr)
    print("  %.1e | %2d  %.4f [%.3f] | %2d  %.4f [%.3f] | %2d  %5d  %.4f [%.3f] | %2d  %.4f [%.3f] | %10.0f   %6.3f | %.0f = %.0f + %d x %.1f + %d x %.1f + %d x %.1f;  %.2f"
          % (n, o[1], min(o[0], cap) / na, (o[0] - nh) / rt, nq[1], min(nq[0], cap) / na, (nq[0] - nh) / rt, nw[1], seq['k'][nw[1]], min(nw[0], cap) / na,
             (nw[0] - nh) / rt, tr[1], min(tr[0], cap) / na, (tr[0] - nh) / rt, o[0] - nw[0], (o[0] - nw[0]) / (o[0] - nh),
             pr['E'], pr['Ebase'], pr['nS'], pr['S'] / max(pr['nS'], 1), pr['nD'], pr['D'] / max(pr['nD'], 1), pr['nT'], pr['T'] / pr['nT'],
             pr['Lam'] / (dl + n * LN2)))
    sys.stdout.flush()
print("# the chains of the best design at n = 10^6 and n = 10^10 (from the top; e = index of the exponent B_e that the chain stands on):")
for n in (10 ** 6, 10 ** 10):
    pr = rows[n][4]
    print("#  n = %.0e:  e  B'/a  X  block m  c  levels j(n)  d_0  A_T (a_T, e_0)  Delta_T  growth of Lam / n" % n)
    for c in pr['chains']:
        if n == 10 ** 6 or c['e'] in (0, 1, 2, 5, 10, 15, 20, 25):
            print("     %2d  %.4f  %.2f  %6d  %.2e  %8d  %6d  %8.1f (%.1f, %.1f)  %.2f  %.4f"
                  % (c['e'], c['Bp'] / cu.a, c['X'], c['m'], c['c'], c['j'], c['d0'], c['A'], c['a'], c['e0'], c['Delta'], c['dLam'] / n))
print("# [%.0f s]" % (time.time() - t0))

# ------------------------------------------------------------------------------------------------ Part B
print("\n# Part B: scan (10 sizes per decade, 10^3 ... 10^12; u = 1, eps = 1, delta = 0.05; every bound capped at n ln 2)")
last_not = {'new': None, 'new/Q': None, 'no-chain': None}
nc_worse_than_old = None
first_below_na = {'old': None, 'new': None}
sup_ratio = {'old': (0, None), 'new': (0, None)}
for i in range(0, 91):
    n = int(round(10 ** (3 + i / 10.0)))
    o, nq, nw, tr = all_best(cu, n, 1.0, dl, seq)
    cap = n * LN2
    vo, vq, vn, vt = min(o[0], cap), min(nq[0], cap), min(nw[0], cap), min(tr[0], cap)
    if vn > vo + 1e-9:
        last_not['new'] = n
    if vq > vo + 1e-9:
        last_not['new/Q'] = n
    if vt <= vn + 1e-9:
        last_not['no-chain'] = n          # the last size at which the variant without chains is at least as good
    if vt > vo + 1e-9 and nc_worse_than_old is None and n >= 10 ** 6:
        nc_worse_than_old = n
    for nm, v in (('old', vo), ('new', vn)):
        if v < n * cu.a and first_below_na[nm] is None:
            first_below_na[nm] = n
        if v >= n * cu.a:
            first_below_na[nm] = None
        r = (v - n * cu.h) / math.sqrt(n * math.log(n))
        if r > sup_ratio[nm][0]:
            sup_ratio[nm] = (r, n)
print("  last size of the scan at which the new bound is NOT below the old one: %s (new with Q's c_S: %s)" % (last_not['new'], last_not['new/Q']))
print("  last size of the scan at which the variant without chains is at least as good as the new bound: %s;"
      " first size >= 10^6 at which it is worse than the old bound: %s" % (last_not['no-chain'], nc_worse_than_old))
print("  first size from which the bound stays below n a:  old %s,  new %s" % (first_below_na['old'], first_below_na['new']))
print("  sup over the scan of (bound - nh)/sqrt(n ln n):  old %.3f at n = %d,  new %.3f at n = %d" % (sup_ratio['old'] + sup_ratio['new']))
print("# [%.0f s]" % (time.time() - t0))

# ------------------------------------------------------------------------------------------------ Part C
print("\n# Part C: other parameters; bound/(n a) old | new, and (new - nh)/sqrt(n ln n)")
print("#   u    eps      delta      n = 6.4e4            1e6               1e8               1e10              1e12")
for (u, eps, dname) in ((1.0, 1.0, '0.05'), (1.0, 0.1, '0.05'), (1.0, 0.01, '0.05'), (1.0, 1e-6, '0.05'), (1.0, 1.0, 'e^-n'),
                        (0.5, 1.0, '0.05'), (2.0, 1.0, '0.05'), (2.0, 0.01, '0.05'), (0.5, 0.01, '0.05')):
    cu_ = Q.Cube(u)
    seq_ = Q.epoch_seq(cu_, MMAX + 1)
    out = []
    for n in (64000, 10 ** 6, 10 ** 8, 10 ** 10, 10 ** 12):
        dl_ = math.log(20.0) if dname == '0.05' else float(n)
        o, nq, nw, tr = all_best(cu_, n, eps, dl_, seq_, trap=False)
        cap = n * LN2
        out.append("%.4f | %.4f (M=%d) [%.2f]" % (min(o[0], cap) / (n * cu_.a), min(nw[0], cap) / (n * cu_.a), nw[1], (nw[0] - n * cu_.h) / math.sqrt(n * math.log(n))))
    print("  %.1f  %-7g  %-5s   " % (u, eps, dname) + "   ".join(out) + "   (h/a = %.5f)" % (cu_.h / cu_.a))
    sys.stdout.flush()
print("# [%.0f s]" % (time.time() - t0))

# ------------------------------------------------------------------------------------------------ Part D
print("\n# Part D: the accuracy enters additively (u = 1, delta = 0.05): [bound(eps) - bound(1)] in nats, and divided by ln(1/eps);")
print("#         old bound of Q_REPORT in the same way")
print("#   n       eps:    1e-1            1e-2            1e-4            1e-8            1e-16           1e-32")
for n in (10 ** 6, 10 ** 8, 10 ** 10):
    b1 = all_best(cu, n, 1.0, dl, seq, trap=False)
    outn, outo = [], []
    for eps in (1e-1, 1e-2, 1e-4, 1e-8, 1e-16, 1e-32):
        b = all_best(cu, n, eps, dl, seq, trap=False)
        outn.append("%8.0f (%5.1f)" % (b[2][0] - b1[2][0], (b[2][0] - b1[2][0]) / math.log(1 / eps)))
        outo.append("%8.0f (%5.1f)" % (b[0][0] - b1[0][0], (b[0][0] - b1[0][0]) / math.log(1 / eps)))
    print("  %.0e  new:  " % n + "  ".join(outn))
    print("  %.0e  old:  " % n + "  ".join(outo))
print("# [%.0f s]" % (time.time() - t0))

# ------------------------------------------------------------------------------------------------ Part E
print("\n# Part E: constants.  C_* = 2 sqrt((1 + rbar) c1 (a/h + 4)) of Q_REPORT;  C_*' = 2 sqrt((1 + rbar) c1 9/2) (Theorem B);")
print("#         2 sqrt((a - h) 9/2): what the same formula gives with the numerical asymptotics of the epochs (heuristic)")
for u in (0.5, 1.0, 2.0, 4.0):
    c_ = Q.Cube(u)
    Cs = 2 * math.sqrt((1 + c_.rbar) * c_.c1 * (c_.a / c_.h + 4))
    Cp = 2 * math.sqrt((1 + c_.rbar) * c_.c1 * 4.5)
    print("  u = %.1f:  C_* = %.3f   C_*' = %.3f   (ratio %.3f)   2 sqrt(4.5 (a - h)) = %.3f" % (u, Cs, Cp, Cp / Cs, 2 * math.sqrt(4.5 * (c_.a - c_.h))))
print("# the closed form of Proposition A' against (A.1): cases, cases in which its hypothesis holds, least (closed - formula) there, largest ratio closed/formula")
ncase = nhyp = 0
mind = float('inf')
maxr = 0.0
nviol = 0
for u in (0.5, 1.0, 2.0):
    c_ = Q.Cube(u)
    s_ = Q.epoch_seq(c_, 30)
    for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 8, 10 ** 10):
        for M in (0, 1, 2, 3, 5, 8, 12, 16, 20, 25):
            if s_['k'][M] > 6 * math.sqrt(n) + 20:
                continue
            for (eps, dl_) in ((1.0, math.log(20.0)), (0.01, math.log(20.0)), (1.0, float(n))):
                ex = L.E_new(c_, n, eps, dl_, M, s_)
                cl, cond = L.E_new_closed(c_, n, eps, dl_, M, s_)
                ncase += 1
                if cond:
                    nhyp += 1
                    mind = min(mind, cl - ex)
                    maxr = max(maxr, cl / ex)
                    if cl < ex - 1e-9:
                        nviol += 1
print("  %d cases, hypothesis holds in %d, least difference %.1f nats, largest ratio %.2f, violations %d" % (ncase, nhyp, mind, maxr, nviol))
print("# [%.0f s]" % (time.time() - t0))

# ------------------------------------------------------------------------------------------------ Part F
print("\n# Part F: the parts of the new bound at its best M (u = 1, eps = 1, delta = 0.05):")
print("#   n     M   k_M   n(B_M - h)   slope steps   [both]/sqrt(n ln n)   chains + drops + base ('second term')   second/(ln n)^2   second/[(M+1) ln n]"
      "   | old: C_1 sqrt(n)-part (base + drops) of (5.2)")
for n in (10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7, 10 ** 8, 10 ** 9, 10 ** 10, 10 ** 11, 10 ** 12):
    nw = best(lambda M: L.E_new(cu, n, 1.0, dl, M, seq), cu, n, seq, 6 * math.sqrt(n) + 20)
    M = nw[1]
    pr = L.E_new(cu, n, 1.0, dl, M, seq, detail=True)
    second = pr['T'] + pr['D'] + pr['Ebase']
    lev = n * (seq['B'][M] - cu.h) + pr['S']
    oM = best(lambda MM: L.E_old(cu, n, 1.0, dl, MM, seq), cu, n, seq, 6 * math.sqrt(n) + 20)[1]
    po = Q.E_total(cu, n, 1.0, dl, oM, seq, detail=True)
    print("  %.0e  %2d  %5d  %10.0f  %10.0f   %.3f   %9.0f   %.2f   %.2f   | %10.0f (M = %d)"
          % (n, M, seq['k'][M], n * (seq['B'][M] - cu.h), pr['S'], lev / math.sqrt(n * math.log(n)), second, second / math.log(n) ** 2,
             second / ((M + 1) * math.log(n)), po['Ebase'] + po['Dsqrt'] + po['Dlog'], oM))
print("\n# done in %.0f s" % (time.time() - t0))
