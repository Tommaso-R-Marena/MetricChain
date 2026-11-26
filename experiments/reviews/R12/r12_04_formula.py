#!/usr/bin/env python3
"""Referee R12, check 4: the formula (5.2) of Q_REPORT, the constants of Theorem Q / Q9, and the series C_1,
evaluated with own code (r12lib.Formula, typed from the text of the report) and compared with the numbers
printed in the report (typed in below from Q_REPORT.md sections 0, 5.1, 5.3, 6.1, 7.4 -- not read from the
author's output files, and none of the author's code is used).

Part A  constants p_u, a, h, kappa, c_1, c_2, rbar and C_* = 2 sqrt((1+rbar) c_1 (a/h + 4)).
Part B  the epoch table of section 5.1 at u = 1.
Part C  the series C_1 (base + drops): partial sums, the limit, the crude geometric majorant of Proposition Q9a.
Part D  the bound  n B_M + E_M(n, eps, delta)  of Theorem Q8 at the best M: the table of section 7.4 and the
        other numbers quoted there; the size from which the bound is below n a.
Part E  Proposition Q9a: its hypothesis and its conclusion on a grid; Theorem Q9(b): the closed form.
Part F  what the ratio (bound - n h)/sqrt(n ln n) does beyond n = 10^12 (closed form of Q9a with the best M).
Part G  monotonicity of the error functions used by the induction (nondecreasing in d and Lambda, nonincreasing in x).
Part H  Theorem Q9(d): accuracies eps_n = n^{-A}.

usage: python3 r12_04_formula.py > out_04_formula.txt       (about 2 minutes)
"""
import sys, os, math, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r12lib import Cube, Formula, LN2, INF

t0 = time.time()
print("# Referee R12, check 4: the formula (5.2), C_*, C_1 and the table of section 7.4, recomputed")

# ----------------------------------------------------------------------------------------- Part A
print("\n# Part A: constants")
print("#   u      p_u       a          h         h/a     kappa     c_1      c_1/a    c_2     rbar    a/h+4    C_*     (report: C_* = 4.65, 8.64, 13.5 at u = 1/2, 1, 2)")
for u in (0.1, 0.5, 1.0, 2.0, 4.0):
    c = Cube(u)
    print("  %4.1f  %.5f  %.6f  %.6f  %.4f  %.5f  %.5f  %.3f  %.4f  %.4f  %.4f  %.3f"
          % (u, c.p, c.a, c.h, c.h / c.a, c.kappa, c.c1, c.c1 / c.a, c.c2, c.rbar, c.a / c.h + 4, c.Cstar))

# ----------------------------------------------------------------------------------------- Part B
print("\n# Part B: epochs at u = 1 (report, section 5.1)")
rep = {0: (0.356, 1, 1, 1, 0.208), 1: (0.496, 1, 3, 0.792, 0.208), 2: (0.720, 1, 5, 0.627, 0.208), 3: (1.122, 2, 7, 0.497, 0.116),
       4: (1.489, 2, 10, 0.439, 0.116), 5: (2.093, 3, 13, 0.388, 0.081), 6: (2.787, 3, 17, 0.357, 0.081), 8: (5.35, 6, 27, 0.312, 0.042),
       10: (9.89, 10, 43, 0.289, 0.026), 12: (18.8, 19, 69, 0.277, 0.014), 16: (64.8, 65, 202, 0.2667, 0.0040),
       20: (220, 220, 642, 0.2638, 0.0012), 24: (745, 746, 2121, 0.2630, 0.00035), 32: (8533, 8533, 23995, 0.26268, 0.00003)}
c = Cube(1.0)
ep = c.epochs(45)
print("#   m     d_m         J_m     k_m     B_m/a     phi_m      | report: d_m, J_m, k_m, B_m/a, phi_m   | agree (to the digits printed)")
nbad = 0
for m in sorted(rep):
    r = rep[m]
    mine = (ep['d'][m], ep['J'][m], ep['k'][m], ep['B'][m] / c.a, ep['phi'][m])

    def agree(x, y):
        s = ('%g' % y)
        dec = len(s.split('.')[1]) if '.' in s else 0
        return abs(x - y) <= 10 ** (-dec) * 1.0001 + 1e-12          # one unit of the last digit printed in the report
    ok = all(agree(x, y) for x, y in zip(mine, r))
    nbad += (not ok)
    print("  %3d  %10.4f  %6d  %6d  %8.5f  %9.6f   | %s | %s" % (m, mine[0], mine[1], mine[2], mine[3], mine[4], r, 'yes' if ok else 'NO'))
print("# rows that differ from the report: %d" % nbad)
print("# (B_m - h) k_m/a at m = 25: %.4f (report: 0.745);  k_{m+1}/k_m at m = 30: %.4f (report: -> a/(a-h) = %.3f);  d_{m+1}/d_m at m = 30: %.4f"
      % ((ep['B'][25] - c.h) * ep['k'][25] / c.a, ep['k'][31] / ep['k'][30], c.a / (c.a - c.h), ep['d'][31] / ep['d'][30]))

# ----------------------------------------------------------------------------------------- Part C
print("\n# Part C: the series C_1 = u [ sqrt(ell0_{alpha_0}/2) + sum_m sqrt(phi_m ell_{c_m}/2) B_{m+1}/a ]")
print("#  u    eps    alpha_0(M=44)   base      drops: M=5     M=13     M=44     M=120    M=400     crude geometric majorant of Q9a (drops part)")
for u in (0.5, 1.0, 2.0):
    c = Cube(u)
    fm = Formula(c)
    for eps in (1.0, 0.1):
        ep = c.epochs(401)
        eh = min(eps, 1.0)
        out = []
        for M in (5, 13, 44, 120, 400):
            _, cm, alpha = fm.schedule(eps, M)
            s = sum(math.sqrt(ep['phi'][m] * fm.ell_c(cm[m]) / 2) * ep['B'][m + 1] / c.a for m in range(M))
            out.append(u * s)
        _, cm, alpha = fm.schedule(eps, 44)
        base = u * math.sqrt(fm.ell0(alpha[0]) / 2)
        ellbar = LN2 + 3 * u + 0.1 + math.log(13 / eh)
        crude = u * c.rbar ** -0.5 * sum((1 + c.kappa) ** (-m / 2) * math.sqrt((ellbar + 2 * math.log(m + 2)) / 2) for m in range(20000))
        print("  %.1f  %.2f   %.4f        %.3f      %.3f   %.3f   %.3f   %.3f   %.3f      %.1f"
              % (u, eps, alpha[0], base, out[0], out[1], out[2], out[3], out[4], crude))
print("#   (report: u = 1, eps = 1: C_1 = 1.6 + 3.9 = 5.5 'first 44 epochs'; eps = 0.1: C_1 = 6.3)")
# is every term of the series below its geometric majorant?
bad = 0
for u in (0.1, 0.5, 1.0, 2.0, 4.0):
    c = Cube(u)
    ep = c.epochs(300)
    for m in range(300):
        if ep['phi'][m] > (1 + c.kappa) ** (-m) / c.rbar * (1 + 1e-12):
            bad += 1
        if ep['d'][m] + 1 < (1 + c.kappa) ** m * c.a / (c.a - c.h) * (1 - 1e-12):
            bad += 1
print("#   phi_m <= rbar^{-1} (1+kappa)^{-m} and d_m + 1 >= (1+kappa)^m a/(a-h), 300 epochs, u in {0.1,0.5,1,2,4}: %d failures" % bad)

# ----------------------------------------------------------------------------------------- Part D
print("\n# Part D: bound = n B_M + E_M at the best M (Theorem Q8), u = 1, eps = 1, delta = 0.05")


def best(fm, n, eps, ld):
    """minimum over M of n B_M + E_M; M runs over all epochs with k_M <= max(100, sqrt(n)/2) (the minimum is interior:
    asserted below)"""
    kcap = max(100.0, 0.5 * math.sqrt(n))
    ks = fm.c.epochs(200)['k']
    b = None
    last = 0
    for M in range(200):
        if ks[M] > kcap:
            break
        d = fm.E_total(n, eps, ld, M, detail=True)
        val = n * d['B'] + d['E']
        last = M
        if b is None or val < b[0]:
            b = (val, M, d)
    assert b[1] < last, "minimum at the end of the range of M"
    return b


rep_tab = {1e3: (0, 1, 1.916), 1e4: (0, 1, 1.190), 1.6e4: (2, 5, 1.098), 3.2e4: (3, 7, 0.858), 6.4e4: (5, 13, 0.707), 1e5: (5, 13, 0.618),
           1e6: (10, 43, 0.371), 1e7: (14, 116, 0.296), 1e8: (17, 268, 0.2731), 1e9: (21, 863, 0.2660), 1e10: (25, 2868, 0.2637),
           1e12: (32, 23995, 0.2628)}
rep_E = {1e3: 102, 1e4: 210, 1.6e4: 836, 3.2e4: 1283, 6.4e4: 2266, 1e5: 2544, 1e6: 9112, 1e7: 28413, 1e8: 83105, 1e9: 276187, 1e10: 927200}
c = Cube(1.0)
fm = Formula(c)
print("#        n     M    k_M   bound/(na)   B_M/a    (bound-nh)/sqrt(n ln n)   (bound-nh)/n^{3/4}     E_M  = base + S (number x mean) + D(cbar_pi part) + D(rest)"
      "    Lam_T/Lam_0 | report: M, k_M, bound/(na), E_M | agree")
nbad = 0
for n in (1e3, 1e4, 1.6e4, 3.2e4, 6.4e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10, 1e12):
    val, M, d = best(fm, n, 1.0, math.log(0.05))
    r = rep_tab[n]
    dec = len(('%g' % r[2]).split('.')[1])
    ok = (M == r[0] and d['k'] == r[1] and abs(val / (n * c.a) - r[2]) <= 10 ** (-dec) * 1.001)       # one unit of the last digit
    if n in rep_E:
        ok = ok and abs(d['E'] - rep_E[n]) <= 1.0
    nbad += (not ok)
    print("  %9.3g  %3d  %6d   %.4f      %.4f        %.3f                  %.4f          %10.1f = %8.1f + %5d x %6.1f + %9.1f + %8.1f   %.4f | %s %s | %s"
          % (n, M, d['k'], val / (n * c.a), d['B'] / c.a, (val - n * c.h) / math.sqrt(n * math.log(n)), (val - n * c.h) / n ** 0.75,
             d['E'], d['base'], d['nS'], (d['S'] / d['nS'] if d['nS'] else 0.0), d['Dsq'], d['Drest'], d['LamT'] / d['Lam0'],
             r, rep_E.get(n, ''), 'yes' if ok else 'NO'))
print("# rows that differ from the table of the report: %d" % nbad)

print("#\n# other numbers quoted in section 7.4 (iv), (v) and in section 0:")
quoted = [
    ("u=1, eps=0.1, delta=0.05", 1.0, 0.1, lambda n: math.log(0.05), {6.4e4: 0.741, 1e6: 0.379, 1e8: 0.2738}),
    ("u=1, eps=1, delta=e^-n", 1.0, 1.0, lambda n: -n, {6.4e4: 0.7088, 1e6: 0.3717, 1e8: 0.2731}),
    ("u=0.5, eps=1, delta=0.05", 0.5, 1.0, lambda n: math.log(0.05), {6.4e4: 1.029, 1e6: 0.444, 1e8: 0.2717}),
    ("u=2, eps=1, delta=0.05", 2.0, 1.0, lambda n: math.log(0.05), {6.4e4: 0.561, 1e6: 0.363, 1e8: 0.3036}),
]
for name, u, eps, ldf, vals in quoted:
    cc = Cube(u)
    ff = Formula(cc)
    row = []
    for n, rv in vals.items():
        val, M, d = best(ff, n, eps, ldf(n))
        dec = len(('%g' % rv).split('.')[1])
        ok = abs(val / (n * cc.a) - rv) <= 10 ** (-dec) * 1.001
        row.append("n=%g: %.4f (M=%d, k=%d; report %g) %s" % (n, val / (n * cc.a), M, d['k'], rv, 'ok' if ok else 'DIFFERS'))
    print("#   %-26s %s" % (name, ';  '.join(row)))
# range of the ratio
for u, lo_hi in ((1.0, (2.4, 3.8)), (0.5, (1.0, 1.8)), (2.0, (4.6, 8.7))):
    cc = Cube(u)
    ff = Formula(cc)
    rs = []
    for n in (1.6e4, 3.2e4, 6.4e4, 1e5, 3e5, 1e6, 1e7, 1e8, 1e9, 1e10, 1e11, 1e12):
        val, M, d = best(ff, n, 1.0, math.log(0.05))
        rs.append((val - n * cc.h) / math.sqrt(n * math.log(n)))
    print("#   u = %.1f: (bound - nh)/sqrt(n ln n) over n = 1.6e4 ... 1e12: min %.3f, max %.3f   (report: between %.1f and %.1f)"
          % (u, min(rs), max(rs), lo_hi[0], lo_hi[1]))
# from which n is the bound below n a ?
c = Cube(1.0)
fm = Formula(c)
lo, hi = 1e4, 1e5
grid = [int(round(10 ** x)) for x in np.linspace(4, 5, 201)]
first = None
last_above = None
for n in grid:
    val, M, d = best(fm, n, 1.0, math.log(0.05))
    if val < n * c.a:
        if first is None:
            first = n
    else:
        last_above = n
print("#   u = 1: the bound is below n a for the first time at n = %s on a grid of 200 sizes per decade, and for the last time not below at n = %s"
      "   (report: 'from n ~ 3 10^4 on')" % (first, last_above))

# ----------------------------------------------------------------------------------------- Part E
print("\n# Part E: Proposition Q9a (closed form) and Theorem Q9(b)")
print("#  u      n       M    T=k_M-1   q*       T q*/Lam_0   Lam_T/Lam_0   E_M (5.2)    closed form C_1 sqrt(n) + (T-M) l_S + M l_D + l_B   l_S     (a/h+4) ln n    l_D      l_B     holds")
nbad = 0
for u in (0.5, 1.0, 2.0):
    cc = Cube(u)
    ff = Formula(cc)
    for n in (1e3, 6.4e4, 1e6, 1e8, 1e10):
        for M in (1, 3, 6, 10, 17, 25):
            ep = cc.epochs(M)
            T = ep['k'][M] - 1
            if T > 3e6:
                continue
            ld = math.log(0.05)
            eh, cm, alpha = ff.schedule(1.0, M)
            Lam0 = -ld + n * LN2
            qstar = max([ff.qS(n, 2 * Lam0)] + [ff.qD(n, 2 * Lam0, cm[m]) for m in range(M)])
            d = ff.E_total(n, 1.0, ld, M, detail=True)
            C1 = u * (math.sqrt(ff.ell0(alpha[0]) / 2) + sum(math.sqrt(ep['phi'][m] * ff.ell_c(cm[m]) / 2) * ep['B'][m + 1] / cc.a for m in range(M)))
            lS = ff.cS(n, 2 * Lam0, cc.a)
            lD = max(ff.cD(n, 2 * Lam0, ep['B'][m], ep['R'][m], cm[m]) - u * math.sqrt(ep['phi'][m] * n * ff.ell_c(cm[m]) / 2) * ep['B'][m + 1] / cc.a
                     for m in range(M))
            lB = ff.Ebase(n, alpha[0], 2 * Lam0) - u * math.sqrt(n * ff.ell0(alpha[0]) / 2)
            closed = C1 * math.sqrt(n) + (T - M) * lS + M * lD + lB
            hyp = T * qstar <= Lam0
            ok = (not hyp) or (d['LamT'] <= 2 * Lam0 * (1 + 1e-12) and d['E'] <= closed + 1e-9)
            nbad += (not ok)
            print("  %.1f  %7.1e  %3d  %8d  %7.2f   %8.4f     %.4f       %11.1f   %11.1f      %7.2f   %7.2f    %7.2f  %7.2f   %s"
                  % (u, n, M, T, qstar, T * qstar / Lam0, d['LamT'] / Lam0, d['E'], closed, lS, (cc.a / cc.h + 4) * math.log(n), lD, lB,
                     ('yes' if ok else 'NO') + ('' if hyp else ' (hypothesis T q* <= Lam_0 not satisfied)')))
print("# failures of Proposition Q9a where its hypothesis holds: %d" % nbad)
print("#\n# Theorem Q9(b), closed form 'n h + 2 sqrt((1+rbar) c_1 n l_S) + C_1 sqrt(n) + M l_D + l_B' with k_dagger = sqrt((1+rbar) c_1 n/l_S), in units of n a")
print("#   (report, section 7.4(v): 1.72, 0.655, 0.305, 0.2673 at n = 6.4e4, 1e6, 1e8, 1e10, u = 1)")
cc = Cube(1.0)
ff = Formula(cc)
for n in (6.4e4, 1e6, 1e8, 1e10):
    ld = math.log(0.05)
    Lam0 = -ld + n * LN2
    lS = ff.cS(n, 2 * Lam0, cc.a)
    kd = math.sqrt((1 + cc.rbar) * cc.c1 * n / lS)
    ep = cc.epochs(60)
    M = max(m for m in range(60) if ep['k'][m] <= kd)
    eh, cm, alpha = ff.schedule(1.0, M)
    T = ep['k'][M] - 1
    C1 = 1.0 * (math.sqrt(ff.ell0(alpha[0]) / 2) + sum(math.sqrt(ep['phi'][m] * ff.ell_c(cm[m]) / 2) * ep['B'][m + 1] / cc.a for m in range(M)))
    lD = max([ff.cD(n, 2 * Lam0, ep['B'][m], ep['R'][m], cm[m]) - math.sqrt(ep['phi'][m] * n * ff.ell_c(cm[m]) / 2) * ep['B'][m + 1] / cc.a
              for m in range(M)] + [0.0])
    lB = ff.Ebase(n, alpha[0], 2 * Lam0) - math.sqrt(n * ff.ell0(alpha[0]) / 2)
    qstar = max([ff.qS(n, 2 * Lam0)] + [ff.qD(n, 2 * Lam0, cm[m]) for m in range(M)])
    closed_b = n * cc.h + 2 * math.sqrt((1 + cc.rbar) * cc.c1 * n * lS) + C1 * math.sqrt(n) + M * lD + lB
    actual = n * ep['B'][M] + ff.E_total(n, 1.0, ld, M)[0]
    # a variant: C_1, l_D, l_B taken at the best M of Part D instead of the M of the proof
    Mb = best(ff, n, 1.0, ld)[1]
    ehb, cmb, alb = ff.schedule(1.0, Mb)
    C1b = 1.0 * (math.sqrt(ff.ell0(alb[0]) / 2) + sum(math.sqrt(ep['phi'][m] * ff.ell_c(cmb[m]) / 2) * ep['B'][m + 1] / cc.a for m in range(Mb)))
    lDb = max([ff.cD(n, 2 * Lam0, ep['B'][m], ep['R'][m], cmb[m]) - math.sqrt(ep['phi'][m] * n * ff.ell_c(cmb[m]) / 2) * ep['B'][m + 1] / cc.a
               for m in range(Mb)] + [0.0])
    lBb = ff.Ebase(n, alb[0], 2 * Lam0) - math.sqrt(n * ff.ell0(alb[0]) / 2)
    variant = n * cc.h + 2 * math.sqrt((1 + cc.rbar) * cc.c1 * n * lS) + C1b * math.sqrt(n) + Mb * lDb + lBb
    print("#   n = %7.1e: k_dagger = %8.1f, M = %2d, k_M = %5d (k_dagger/(1+rbar) = %.1f), T q*/Lam_0 = %.3f;  closed form/(na) = %.4f;  (5.2) at this M: %.4f;  %s;"
          "  variant with C_1, l_D, l_B at the best M = %d of Part D: %.4f"
          % (n, kd, M, ep['k'][M], kd / (1 + cc.rbar), T * qstar / Lam0, closed_b / (n * cc.a), actual / (n * cc.a),
             'closed form >= (5.2)' if closed_b >= actual else 'CLOSED FORM BELOW (5.2)', Mb, variant / (n * cc.a)))

# ----------------------------------------------------------------------------------------- Part F
print("\n# Part F: beyond 10^12 -- the closed form of Proposition Q9a (an upper bound of (5.2) when T q* <= Lam_0), minimised over M;")
print("#   B_M - h is computed as h/d_M (not as a difference), sums over the epochs are cumulative")
print("#  u     n       best M    k_M        (closed - n h)/sqrt(n ln n)  = C_1/sqrt(ln n) + level part [n(B_M-h) + (T-M) l_S]/sqrt(n ln n) + rest      "
      "2 sqrt((a-h)(a/h+4))    C_*     T q*/Lam_0")
for u in (0.5, 1.0, 2.0):
    cc = Cube(u)
    ff = Formula(cc)
    NE = 760
    ep = cc.epochs(NE)
    for n in (1e12, 1e16, 1e24, 1e40, 1e80, 1e150):
        ld = math.log(0.05)
        Lam0 = -ld + n * LN2
        lS = ff.cS(n, 2 * Lam0, cc.a)
        cm = [1.0 / (13.0 * (m + 1) * (m + 2)) for m in range(NE)]
        wsum = 0.0
        ssum = 0.0
        lDmax = -INF
        qmax = ff.qS(n, 2 * Lam0)
        bestv = None
        for M in range(1, NE):
            m = M - 1
            wsum += ff.w(cm[m])
            ssum += math.sqrt(ep['phi'][m] * ff.ell_c(cm[m]) / 2) * ep['B'][m + 1] / cc.a
            lDmax = max(lDmax, ff.cD(n, 2 * Lam0, ep['B'][m], ep['R'][m], cm[m])
                        - u * math.sqrt(ep['phi'][m] * n * ff.ell_c(cm[m]) / 2) * ep['B'][m + 1] / cc.a)
            qmax = max(qmax, ff.qD(n, 2 * Lam0, cm[m]))
            T = ep['k'][M] - 1
            if T * qmax > Lam0:
                break
            alpha0 = 1.0 - wsum
            C1 = u * (math.sqrt(ff.ell0(alpha0) / 2) + ssum)
            lB = ff.Ebase(n, alpha0, 2 * Lam0) - u * math.sqrt(n * ff.ell0(alpha0) / 2)
            lev = n * cc.h / ep['d'][M] + (T - M) * lS
            v = lev + C1 * math.sqrt(n) + M * lDmax + lB
            if bestv is None or v < bestv[0]:
                bestv = (v, M, T + 1, C1, lev, T * qmax / Lam0)
        v, M, k, C1, lev, hyp = bestv
        s_ = math.sqrt(n * math.log(n))
        print("  %.1f  %7.0e   %4d   %10.4g       %8.4f                  = %7.4f          + %8.4f   + %8.5f                %.4f             %.3f    %.2e"
              % (u, n, M, k, v / s_, C1 / math.sqrt(math.log(n)), lev / s_, (v - C1 * math.sqrt(n) - lev) / s_,
                 2 * math.sqrt((cc.a - cc.h) * (cc.a / cc.h + 4)), cc.Cstar, hyp))

# ----------------------------------------------------------------------------------------- Part G
print("\n# Part G: monotonicity of c_S, q_S, c_D, q_D, cbar_pi, E_base (nondecreasing in d and Lambda; E_base nonincreasing in x)")
bad = 0
rng = np.random.default_rng(12)
for u in (0.1, 1.0, 4.0):
    cc = Cube(u)
    ff = Formula(cc)
    ep = cc.epochs(6)
    for trial in range(4000):
        d1 = int(10 ** rng.uniform(0, 7))
        d2 = d1 + int(10 ** rng.uniform(0, 5))
        L1 = 10 ** rng.uniform(-1, 8)
        L2 = L1 * (1 + 10 ** rng.uniform(-3, 2))
        x1 = 10 ** rng.uniform(-6, 3)
        x2 = x1 * (1 + 10 ** rng.uniform(-3, 2))
        m = int(rng.integers(0, 6))
        B, R = ep['B'][m], ep['R'][m]
        cc_ = 10 ** rng.uniform(-9, math.log10(1 / 3))
        tests = [
            ff.cS(d1, L1, B) <= ff.cS(d2, L1, B) + 1e-9, ff.cS(d1, L1, B) <= ff.cS(d1, L2, B) + 1e-9,
            ff.qS(d1, L1) <= ff.qS(d2, L1) + 1e-9, ff.qS(d1, L1) <= ff.qS(d1, L2) + 1e-9,
            ff.cD(d1, L1, B, R, cc_) <= ff.cD(d2, L1, B, R, cc_) + 1e-9, ff.cD(d1, L1, B, R, cc_) <= ff.cD(d1, L2, B, R, cc_) + 1e-9,
            ff.qD(d1, L1, cc_) <= ff.qD(d2, L1, cc_) + 1e-9, ff.qD(d1, L1, cc_) <= ff.qD(d1, L2, cc_) + 1e-9,
            ff.cbar_pi(d1, x1) <= ff.cbar_pi(d2, x1) + 1e-9, ff.cbar_pi(d1, x1) <= ff.cbar_pi(d1, x2) + 1e-9,
            ff.Ebase(d1, x1, L1) <= ff.Ebase(d2, x1, L1) + 1e-9, ff.Ebase(d1, x1, L1) <= ff.Ebase(d1, x1, L2) + 1e-9,
            ff.Ebase(d1, x2, L1) <= ff.Ebase(d1, x1, L1) + 1e-9,
            min(ff.cS(d1, L1, B), ff.qS(d1, L1), ff.cD(d1, L1, B, R, cc_), ff.qD(d1, L1, cc_), ff.Ebase(d1, x1, L1)) >= 0,
        ]
        bad += sum(1 for t in tests if not t)
print("  12000 random triples of arguments x 14 inequalities: %d failures" % bad)
# ----------------------------------------------------------------------------------------- Part H
print("\n# Part H: Theorem Q9(d) -- accuracies eps_n = n^{-A}: the bound of Theorem Q8 at the best M, u = 1, delta = 0.05")
print("#   A      n       eps_n      best M   k_M    bound/(na)   (bound - nh)/sqrt(n ln n)   base part of E_M/sqrt(n ln n)   cbar_pi part of the drops/sqrt(n ln n)")
c = Cube(1.0)
fm = Formula(c)
for A in (0.5, 1.0, 3.0):
    for n in (1e4, 1e6, 1e8, 1e10, 1e12):
        val, M, d = best(fm, n, n ** (-A), math.log(0.05))
        s_ = math.sqrt(n * math.log(n))
        print("  %.1f  %7.0e  %9.2e   %3d  %6d   %.4f        %.3f                      %.3f                           %.3f"
              % (A, n, n ** (-A), M, d['k'], val / (n * c.a), (val - n * c.h) / s_, d['base'] / s_, d['Dsq'] / s_))

print("\n# done in %.0f s" % (time.time() - t0))
