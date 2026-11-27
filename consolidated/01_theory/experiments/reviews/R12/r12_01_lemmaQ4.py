#!/usr/bin/env python3
"""Referee R12, check 1: Lemma Q4 of Q_REPORT (closing radius at an extensive threshold), in exact arithmetic.

Everything is computed from the definitions of K_REPORT 2.1 (Gamma~, kappa, Gamma'', [N], [P], r_dagger, pi_dagger)
with big integers for the binomial sums and mpmath (60 digits) for the two exponential sums.

Part 0   my float tables (r12lib.Tab) against the exact ones, and against the earlier referee's r8_flat.TablesF.
Part A   Lemma Q4(a):  Gamma~_m(r) <= (m+1) e^{2u+e^u} e^{m e}  for every integer 0 <= r <= min(m, rho_e m + 1).
Part B   Lemma Q4(b):  with theta = c_eta^{-1} (m+1) e^{2u+e^u+m e}  EXACTLY at the threshold and (1-eta) nu_0 = 1
         (the least values the lemma allows):  r_dagger >= min{m-1, floor(rho_e m)+1}  and
         ln(1/pi_dagger) <= m theta_na(e) + ln(m+1).
Part C   how sharp: the same with theta a factor e^{-t} BELOW the threshold (not covered by the lemma), and the
         radius floor(rho_e m)+2 in part (a) (not claimed) -- to see where the statement stops being true.
Part D   Lemma K.4(a),(b) (= Lemma 11.55), on which Lemma Q4(a) and Lemma Q3 rest, in the same arithmetic.

usage: python3 r12_01_lemmaQ4.py > out_01_lemmaQ4.txt        (about 3 minutes)
"""
import sys, os, math, time
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r12lib import Cube, ExactTab, Tab, kl

t0 = time.time()
mp.mp.dps = 60


def mp_consts(u):
    u = mp.mpf(u)
    p = 1 / (1 + mp.exp(u))
    eps_star = mp.log(mp.cosh(u / 2))
    return u, p, eps_star


def mp_kl(r, p):
    s = mp.mpf(0)
    if r > 0:
        s += r * mp.log(r / p)
    if r < 1:
        s += (1 - r) * mp.log((1 - r) / (1 - p))
    return s


def mp_rho_e(e, p, eps_star):
    """rho in [p, 1/2] with KL(rho||p) = min(e, eps*) to 50 digits"""
    if e >= eps_star:
        return mp.mpf(1) / 2
    if e <= 0:
        return p
    lo, hi = p, mp.mpf(1) / 2
    for _ in range(180):
        mid = (lo + hi) / 2
        if mp_kl(mid, p) <= e:
            lo = mid
        else:
            hi = mid
    return lo


def mp_klhalf(r):
    return mp.log(2) + (r * mp.log(r) if r > 0 else 0) + ((1 - r) * mp.log(1 - r) if r < 1 else 0)


print("# Referee R12, check 1: Lemma Q4 in exact arithmetic (big integers, mpmath %d digits)" % mp.mp.dps)

# ---------------------------------------------------------------- Part 0
print("\n# Part 0: float tables r12lib.Tab against exact tables, and against r8_flat.TablesF")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'R8'))
import r8_flat
worst = 0.0
worst_k = 0
worst_r8 = 0.0
for u in (0.1, 0.5, 1.0, 2.0, 4.0):
    for m in (1, 2, 3, 7, 20, 64, 150, 400):
        ex = ExactTab(m, u)
        ft = Tab(m, u)
        d = max(max(abs(float(ex.lnB[r]) - ft.lB[r]) for r in range(m + 1)),
                max(abs(float(ex.lnE[r]) - ft.lE[r]) for r in range(m + 1)),
                max(abs(float(ex.lnT[r]) - ft.lT[r]) for r in range(m + 1)),
                max(abs(float(ex.lnGt[r]) - ft.lGt[r]) for r in range(m + 1)))
        worst = max(worst, d)
        for eta in (Fr(1, 2), Fr(1, 20), Fr(1, 3)):
            _, kap = ex.lnGpp(eta)
            kf = ft.kappa(math.log((1 - float(eta)) / (1 + float(eta))))
            worst_k = max(worst_k, int(np.max(np.abs(np.array(kap) - kf))))
        r8 = r8_flat.TablesF(m, u)
        worst_r8 = max(worst_r8, float(np.max(np.abs(r8.lB - ft.lB))), float(np.max(np.abs(r8.lE - ft.lE))),
                       float(np.max(np.abs(r8.lT - ft.lT))))
print("  40 cubes (u in {0.1,0.5,1,2,4}, m <= 400): largest |ln(float) - ln(exact)| over B, E, T, Gamma~ = %.2e;"
      " kappa differs by at most %d; largest difference to r8_flat.TablesF = %.2e" % (worst, worst_k, worst_r8))

# ---------------------------------------------------------------- Parts A, B, C
US = (0.1, 0.3, 0.5, 1.0, 2.0, 4.0)
MS = list(range(1, 41)) + [45, 50, 60, 64, 75, 100, 128, 150, 200, 256, 300, 400, 500, 640, 750, 1000, 1500, 2000, 3000, 4000, 5000]
ETAS = (Fr(1, 2), Fr(1, 4), Fr(1, 20), Fr(1, 100))
EFRAC = (0.0, 1e-6, 0.01, 0.1, 0.25, 'h', 0.5, 0.75, 0.9, 0.99, 0.999999, 1.0, 1.000001, 1.5, 3.0, 50.0)

print("\n# Parts A, B, C: u in %s; m in {1..40} + %s (%d sizes); eta in %s;" % (US, MS[40:], len(MS), [str(e) for e in ETAS]))
print("#   e/eps* in %s  ('h': e = h, the rate of the slope steps)" % (EFRAC,))
print("#  u    cases(a): radii checked, least slack of (a) [ln], at (m, e/eps*, r) | cases(b), violations of the radius, "
      "cases with r_dag = r_1 exactly, violations of ln(1/pi), least slack of ln(1/pi) at (m, e/eps*, eta)"
      " | below threshold by e^-1: radius fails / pi fails; by e^-5: radius fails / pi fails | (a) at floor(rho_e m)+2 fails")
tot_a = tot_b = 0
viol_a = viol_r = viol_pi = 0
glob_min_b = (mp.inf, None)
for u in US:
    um, p, eps_star = mp_consts(u)
    cu = Cube(u)
    h = mp_klhalf(mp.log(2 / (1 + mp.exp(-um))) / um)
    na = nb = 0
    va = vr = vpi = 0
    tight = 0
    min_a = (mp.inf, None)
    min_b = (mp.inf, None)
    below1 = [0, 0]
    below5 = [0, 0]
    a2fail = 0
    a2tot = 0
    for m in MS:
        ex = ExactTab(m, um)
        gpp = {eta: ex.lnGpp(eta)[0] for eta in ETAS}
        # running maxima for r_dagger
        runN = []
        cur = -mp.inf
        for r in range(m):
            cur = max(cur, ex.lnGt[r])
            runN.append(cur)
        runP = {}
        for eta in ETAS:
            ceta = (1 - eta) / (1 + eta)
            lnceta = mp.log(mp.mpf(ceta.numerator) / ceta.denominator)
            cur = -mp.inf
            arr = []
            for r in range(m):
                cur = max(cur, min(ex.lnGt[r] - lnceta, gpp[eta][r]))
                arr.append(cur)
            runP[eta] = (arr, lnceta)

        def rdag(eta, ln_theta, ln_nu):
            arr, lnceta = runP[eta]
            r = -1
            # largest r with runN[r] <= ln_theta + ln_nu and runP[r] <= ln_theta (both nondecreasing in r)
            lo, hi = -1, m - 1
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if runN[mid] <= ln_theta + ln_nu and arr[mid] <= ln_theta:
                    lo = mid
                else:
                    hi = mid - 1
            return lo

        for ef in EFRAC:
            e = h if ef == 'h' else ef * eps_star
            rho = mp_rho_e(e, p, eps_star)
            thna = mp_klhalf(rho)
            lnbound_a = mp.log(m + 1) + 2 * um + mp.exp(um) + m * e
            # (a)
            rmax = min(m, int(mp.floor(rho * m + 1)))
            for r in range(0, rmax + 1):
                na += 1
                sl = lnbound_a - ex.lnGt[r]
                if sl < min_a[0]:
                    min_a = (sl, (m, ef, r))
                if sl < 0:
                    va += 1
            # (a) one radius further (not claimed)
            r2 = int(mp.floor(rho * m)) + 2
            if r2 <= m:
                a2tot += 1
                if ex.lnGt[r2] > lnbound_a:
                    a2fail += 1
            # (b)
            r1 = min(m - 1, int(mp.floor(rho * m)) + 1)
            for eta in ETAS:
                arr, lnceta = runP[eta]
                ln_theta = -lnceta + lnbound_a
                rd = rdag(eta, ln_theta, mp.mpf(0))
                nb += 1
                if rd < r1:
                    vr += 1
                if rd == r1:
                    tight += 1
                lip = ex.ln_inv_pidag(rd)
                sl = m * thna + mp.log(m + 1) - lip
                if sl < min_b[0]:
                    min_b = (sl, (m, ef, str(eta)))
                if sl < 0:
                    vpi += 1
                for t, cnt in ((1, below1), (5, below5)):
                    rd2 = rdag(eta, ln_theta - t, mp.mpf(0))
                    if rd2 < r1:
                        cnt[0] += 1
                    if m * thna + mp.log(m + 1) - ex.ln_inv_pidag(rd2) < 0:
                        cnt[1] += 1
        del ex
    print("  %.1f   %7d  %8.4f at %s | %6d  %3d  %5d  %3d  %10.6f at %s | %d / %d ; %d / %d | %d of %d"
          % (u, na, float(min_a[0]), min_a[1], nb, vr, tight, vpi, float(min_b[0]), min_b[1],
             below1[0], below1[1], below5[0], below5[1], a2fail, a2tot))
    sys.stdout.flush()
    tot_a += na
    tot_b += nb
    viol_a += va
    viol_r += vr
    viol_pi += vpi
    if min_b[0] < glob_min_b[0]:
        glob_min_b = min_b
print("# TOTAL: (a) %d radii, %d violations;  (b) %d cases, %d violations of r_dag >= min{m-1, floor(rho_e m)+1}, "
      "%d violations of ln(1/pi_dag) <= m theta_na(e) + ln(m+1)   [%.0f s]" % (tot_a, viol_a, tot_b, viol_r, viol_pi, time.time() - t0))

# ---------------------------------------------------------------- the slack of (b) along m at e = h
print("\n# the slack  m h + ln(m+1) - ln(1/pi_dag)  at e = h, eta = 1/2, theta at the threshold, (1-eta) nu_0 = 1:")
print("#  u     m: slack  (r_dag, floor(rho_h m)+1)")
for u in (0.5, 1.0, 2.0):
    um, p, eps_star = mp_consts(u)
    rho_h = mp.log(2 / (1 + mp.exp(-um))) / um
    h = mp_klhalf(rho_h)
    row = []
    for m in (1, 2, 5, 10, 100, 1000, 5000):
        ex = ExactTab(m, um)
        eta = Fr(1, 2)
        ln_theta = mp.log(3) + mp.log(m + 1) + 2 * um + mp.exp(um) + m * h
        rd = ex.rdag(eta, ln_theta, mp.mpf(0))
        sl = m * h + mp.log(m + 1) - ex.ln_inv_pidag(rd)
        row.append("%d: %.4f (%d, %d)" % (m, float(sl), rd, min(m - 1, int(mp.floor(rho_h * m)) + 1)))
    print("  %.1f   %s" % (u, ';  '.join(row)))

# ---------------------------------------------------------------- Part D: Lemma K.4(a),(b)
print("\n# Part D: Lemma K.4 (= Lemma 11.55) in exact arithmetic")
print("#  (a) Gamma~(r) <= 2 e^u m for 0 <= r <= p_u(m+1);  (b) Gamma''(r) <= 2 e^{u(m0+2)} P(Bin(m,p_u) <= r) for 0 <= r <= p_u m,")
print("#      and kappa(r) >= r - 1 - m0 for 1 <= r <= p_u(m+1)+1")
na = nb = nk = 0
va = vb = vk = 0
min_a = mp.inf
min_b = mp.inf
for u in US:
    um, p, eps_star = mp_consts(u)
    for m in list(range(1, 31)) + [50, 100, 200, 400, 800, 1600, 3000]:
        ex = ExactTab(m, um)
        # binomial cdf, exact: P(Bin <= r) = sum_{j<=r} C(m,j) e^{-uj} / (1+e^{-u})^m
        emu = mp.exp(-um)
        cdf = []
        s = mp.mpf(0)
        pw = mp.mpf(1)
        for j in range(m + 1):
            s += ex.C[j] * pw
            pw *= emu
            cdf.append(s)
        tot = cdf[-1]
        for r in range(0, m + 1):
            if r <= p * (m + 1):
                na += 1
                sl = mp.log(2 * m) + um - ex.lnGt[r]
                min_a = min(min_a, sl)
                if sl < 0:
                    va += 1
        for eta in ETAS:
            ceta = (1 - eta) / (1 + eta)
            m0 = int(mp.ceil(mp.log(mp.mpf(ceta.denominator) / ceta.numerator) / um))
            g, kap = ex.lnGpp(eta)
            for r in range(0, m + 1):
                if 1 <= r <= p * (m + 1) + 1:
                    nk += 1
                    if kap[r] < r - 1 - m0:
                        vk += 1
                if r <= p * m:
                    nb += 1
                    sl = mp.log(2) + um * (m0 + 2) + mp.log(cdf[r] / tot) - g[r]
                    min_b = min(min_b, sl)
                    if sl < 0:
                        vb += 1
        del ex
print("  (a): %d radii, %d violations, least slack %.4f [ln];  kappa: %d cases, %d violations;  (b): %d cases, %d violations, least slack %.4f [ln]"
      % (na, va, float(min_a), nk, vk, nb, vb, float(min_b)))
print("\n# done in %.0f s" % (time.time() - t0))
