#!/usr/bin/env python3
"""Referee R12, check 2: Lemma Q3 of Q_REPORT (the outer sample at a bounded theta), in exact arithmetic.

Lemma Q3:  m >= 1, 0 < eta <= 1/2, 0 < theta <= 2 e^{u(m0+2)}, nu_0 >= 2 e^u m/(theta(1-eta)),  ell >= ell_1 := ln(2e^{u(m0+2)}/theta).
           Then  ln(1/pi_dag) <= m a + cbar_pi(m; ell),
           cbar_pi(m; ell) = max{ ln 2 + m*(ell) H(p_u) ,  u(1 + sqrt(m ell/2)) + (4/(3 p_u))(ell + 2) + ln(m+1) },
           m*(ell) = ((sqrt(ell/2) + sqrt(ell/2 + 2 p_u))/p_u)^2;
           and if s := sqrt(m ell_1/2) <= p_u m/2 - 1:  ln(1/pi_dag) <= m a + u(1+s) + (4/(3p_u))(ell_1 + 2/m) + ln(m+1).
Tested with ell = ell_1 (the least value allowed) and nu_0 at its least value, i.e. [N] reads Gamma~(r') <= 2 e^u m.
Also Lemma K.4(c) (r_dag >= r_+ := floor(p_u m - s) whenever r_+ >= 0), which Lemma Q3 quotes, and Lemma K.4(d)
with its constant u + ln 4 for comparison.

Part A  exact arithmetic (big integers, mpmath 60 digits), m <= 5000.
Part B  float tables (r12lib.Tab), m up to 64000: the size of (ln(1/pi_dag) - m a)/sqrt(m) against u sqrt(ell_1/2).

usage: python3 r12_02_lemmaQ3.py > out_02_lemmaQ3.txt        (about 2 minutes)
"""
import sys, os, math, time
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r12lib import Cube, ExactTab, Tab, Formula, LN2

t0 = time.time()
mp.mp.dps = 60

print("# Referee R12, check 2: Lemma Q3 (and Lemma K.4(c),(d)) on exact tables")
US = (0.1, 0.5, 1.0, 2.0, 4.0)
MS = list(range(1, 41)) + [50, 64, 100, 150, 200, 300, 400, 600, 800, 1200, 1600, 2400, 3200, 5000]
ETAS = (Fr(1, 2), Fr(1, 3), Fr(1, 10), Fr(1, 20), Fr(1, 100), Fr(1, 1000))
THETAS = ('max', 1.0, 'eta', 0.05, 1e-3, 1e-6, 1e-12, 1e-30)
print("# Part A: u in %s; m in {1..40} + %s; eta in %s; theta in %s ('max' = 2e^{u(m0+2)}, 'eta': theta = eta as in the drop)"
      % (US, MS[40:], [str(e) for e in ETAS], THETAS))
print("#  u   cases | K.4(c): cases with r_+ >= 0, violations | Lemma Q3 uniform: violations, least slack at (m, eta, theta)"
      " | refined (s <= p m/2 - 1): cases, violations, least slack at (m, eta, theta) | K.4(d) (r_+ >= p m/2): cases, violations, least slack")
tot = 0
tv = 0
for u in US:
    cu = Cube(u)
    fm = Formula(cu)
    um = mp.mpf(u)
    p = 1 / (1 + mp.exp(um))
    a = mp.log(2) + p * mp.log(p) + (1 - p) * mp.log(1 - p)
    ncase = nc = vc = vq = nr = vr = nd = vd = 0
    minq = (mp.inf, None)
    minr = (mp.inf, None)
    mind = mp.inf
    for m in MS:
        ex = ExactTab(m, um)
        runN = []
        cur = -mp.inf
        for r in range(m):
            cur = max(cur, ex.lnGt[r])
            runN.append(cur)
        for eta in ETAS:
            ceta = (1 - eta) / (1 + eta)
            lnceta = mp.log(mp.mpf(ceta.numerator) / ceta.denominator)
            m0 = int(mp.ceil(-lnceta / um))
            g, _ = ex.lnGpp(eta)
            arr = []
            cur = -mp.inf
            for r in range(m):
                cur = max(cur, min(ex.lnGt[r] - lnceta, g[r]))
                arr.append(cur)
            ln_theta_max = mp.log(2) + um * (m0 + 2)
            lnN = mp.log(2 * m) + um                       # theta (1-eta) nu_0 at the least nu_0
            for th in THETAS:
                if th == 'max':
                    ln_theta = ln_theta_max
                elif th == 'eta':
                    ln_theta = mp.log(mp.mpf(eta.numerator) / eta.denominator)
                else:
                    ln_theta = mp.log(mp.mpf(th))
                if ln_theta > ln_theta_max:
                    continue
                ncase += 1
                lo, hi = -1, m - 1
                while lo < hi:
                    mid = (lo + hi + 1) // 2
                    if runN[mid] <= lnN and arr[mid] <= ln_theta:
                        lo = mid
                    else:
                        hi = mid - 1
                rd = lo
                lip = ex.ln_inv_pidag(rd)
                ell1 = ln_theta_max - ln_theta
                s = mp.sqrt(m * ell1 / 2)
                rplus = int(mp.floor(p * m - s))
                if rplus >= 0:
                    nc += 1
                    if rd < rplus:
                        vc += 1
                # uniform bound
                ell1f = float(ell1)
                bound = m * a + fm.cbar_pi(m, ell1f)
                sl = bound - lip
                if sl < minq[0]:
                    minq = (sl, (m, str(eta), th))
                if sl < -mp.mpf(10) ** (-9):
                    vq += 1
                # refined bound
                if s <= p * m / 2 - 1:
                    nr += 1
                    b2 = m * a + um * (1 + s) + (4 / (3 * p)) * (ell1 + mp.mpf(2) / m) + mp.log(m + 1)
                    sl = b2 - lip
                    if sl < minr[0]:
                        minr = (sl, (m, str(eta), th))
                    if sl < 0:
                        vr += 1
                # Lemma K.4(d)
                if rplus >= p * m / 2:
                    nd += 1
                    b3 = m * a + (um + mp.log(4)) * (1 + s) + mp.log(m + 1)
                    mind = min(mind, b3 - lip)
                    if b3 < lip:
                        vd += 1
        del ex
    print("  %.1f  %5d | %5d  %d | %d  %9.4f at %s | %5d  %d  %9.4f at %s | %5d  %d  %9.4f"
          % (u, ncase, nc, vc, vq, float(minq[0]), minq[1], nr, vr, float(minr[0]), minr[1], nd, vd, float(mind)))
    sys.stdout.flush()
    tot += ncase
    tv += vc + vq + vr + vd
print("# TOTAL %d cases, %d violations   [%.0f s]" % (tot, tv, time.time() - t0))

# ------------------------------------------------------------------ Part B
print("\n# Part B (float tables): over := ln(1/pi_dag) - m a, with nu_0 at its least value; 'lead' = u sqrt(ell_1/2) (Lemma Q3),")
print("#   'K4d' = (u + ln 4) sqrt(ell_1/2) (Lemma K.4(d)); 'Q3/sqrt m' = cbar_pi(m; ell_1)/sqrt(m) (the whole bound)")
print("#  u    eta=theta     m      r_dag   r_+     over     over/sqrt(m)   lead    K4d     Q3/sqrt m    slack of Q3")
nviol = 0
for u in (0.5, 1.0, 2.0):
    cu = Cube(u)
    fm = Formula(cu)
    for c in (1 / 3, 0.05, 0.001):
        lceta = math.log((1 - c) / (1 + c))
        m0 = math.ceil(-lceta / u)
        ell1 = LN2 + u * (m0 + 2) - math.log(c)
        for m in (500, 2000, 8000, 32000, 64000):
            t = Tab(m, u)
            g = t.lGpp(lceta)
            okN = t.lGt[:m] <= math.log(2 * m) + u
            okP = np.minimum(t.lGt[:m] - lceta, g[:m]) <= math.log(c)
            bad = np.nonzero(~(okN & okP))[0]
            rd = int(bad[0]) - 1 if bad.size else m - 1
            lip = (m * LN2 - t.lB[rd]) if rd >= 0 else (m + 1) * LN2
            over = lip - m * cu.a
            s = math.sqrt(m * ell1 / 2)
            rp = math.floor(cu.p * m - s)
            q3 = fm.cbar_pi(m, ell1)
            if over > q3 + 1e-9 or (rp >= 0 and rd < rp):
                nviol += 1
            print("  %.1f   %8.4f   %6d   %6d  %6d  %8.2f   %7.3f       %6.3f  %6.3f   %7.3f     %8.2f"
                  % (u, c, m, rd, rp, over, over / math.sqrt(m), u * math.sqrt(ell1 / 2), (u + math.log(4)) * math.sqrt(ell1 / 2),
                     q3 / math.sqrt(m), q3 - over))
print("# violations in part B: %d" % nviol)
print("\n# done in %.0f s" % (time.time() - t0))
