#!/usr/bin/env python3
"""R17, item 4: the lower bound of Theorem 11.58a(c) (theory report at dd067f1, l.5521-5542), own code.

Theorem 11.25(a) (machine-checked by the theory division, `cube_exact_dip_randomized`): if eps < Delta_k then
E|Q(0)| >= (1 - 2 delta) 2^n / |B(n,k)|, with Delta_k = ln(1 + 2^{-n} E_k(n)),
E_k(n) = sum_{j<=k} C(n,j)(e^{u(k+1-j)} - 1).  k*(eps) = the least k with Delta_k > eps.
Claim (c): for delta < 1/2 and every n with k*(eps) <= n/2:
    ln N >= n h - max{1, c0} ln((1-rho_h)/rho_h) - ln(1/(1-2 delta)),   c0 = (eps + ln 2)/u,
and with c0 in place of the maximum whenever (rho_h - p_u) n >= 1 - c0  ("without the maximum the bound is
confirmed numerically wherever it was tested").

Part A (exact integers for the binomial sums; E_k in 50-digit mpmath): every n = 2..300 and a grid of
(u, eps): the inequality with the maximum (what the three lines prove) and without it; the cases where the
proviso fails are counted separately.  Also: is k*(eps) <= the radius k_1 = max{ceil(p_u n), ceil(rho_h n + c0 - 1)}
of the three lines, and does the median step hold at k_1 (2^{-n}E_k > e^{u(k+1) - n Lambda_1}/2 - 1 for k >= p_u n).
Part B (floats, lgamma): n up to 1e6: the bound, and the excess of the hinted lower bound over n h.

The delta-dependent term ln(1 - 2 delta) is the same on both sides and is left out.
"""
import math
import resource
import sys
import time

import mpmath as mp

mp.mp.dps = 50
LN2 = math.log(2.0)


def consts(u):
    p = 1 / (1 + math.exp(u))
    lam1 = math.log(2 / (1 + math.exp(-u)))
    rho = lam1 / u
    H = lambda x: -x * math.log(x) - (1 - x) * math.log(1 - x)
    h = LN2 - H(rho)
    return p, lam1, rho, h


def partA():
    print("== Part A: exact; every n = 2..300 ==")
    tot = dict(cases=0, kstar_le_half=0, viol_max=0, viol_nomax=0, proviso_fails=0, viol_nomax_in_proviso_fail=0,
               kstar_gt_k1=0, median_fail=0)
    least = dict(max=(1e300, None), nomax=(1e300, None), nomax_pf=(1e300, None))
    for u in (0.1, 0.3, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0):
        p, lam1, rho, h = consts(u)
        um = mp.mpf(u)
        eu = mp.e ** um
        slope = math.log((1 - rho) / rho)
        for n in range(2, 301):
            # exact |B(n,k)| and E_k(n) = e^u E_{k-1} + (e^u - 1)|B(n,k)|
            c = 1
            ball = []
            s = 0
            for j in range(n + 1):
                s += c
                ball.append(s)
                c = c * (n - j) // (j + 1)
            E = []
            prev = mp.mpf(0)
            for k in range(n + 1):
                prev = eu * prev + (eu - 1) * ball[k]
                E.append(prev)
            two_n = mp.mpf(2) ** n
            # median step at every k >= p_u n, k <= n:  2^{-n} E_k > e^{u(k+1) - n Lambda_1}/2 - 1
            for k in range(math.ceil(p * n), n + 1):
                if not (E[k] / two_n > mp.e ** (um * (k + 1) - n * mp.log(2 / (1 + mp.e ** (-um)))) / 2 - 1):
                    tot['median_fail'] += 1
            for eps in (1e-3, 1e-2, 0.1, 0.5, 1.0, 2.0, 5.0, 20.0):
                thr = mp.expm1(mp.mpf(eps))
                kstar = None
                for k in range(n + 1):
                    if E[k] / two_n > thr:
                        kstar = k
                        break
                tot['cases'] += 1
                if kstar is None:
                    continue                      # no dip changes ln Z by more than eps: no bound claimed
                c0 = (eps + LN2) / u
                k1 = max(math.ceil(p * n), math.ceil(rho * n + c0 - 1))
                if kstar > k1:
                    tot['kstar_gt_k1'] += 1
                if 2 * kstar > n:
                    continue
                tot['kstar_le_half'] += 1
                lb = n * LN2 - float(mp.log(ball[kstar]))           # ln(2^n/|B(n,k*)|)
                s_max = lb - (n * h - max(1.0, c0) * slope)
                s_nomax = lb - (n * h - c0 * slope)
                proviso = (rho - p) * n >= 1 - c0
                if s_max < least['max'][0]:
                    least['max'] = (s_max, (u, n, eps))
                if s_max < -1e-12:
                    tot['viol_max'] += 1
                if s_nomax < -1e-12:
                    tot['viol_nomax'] += 1
                if proviso:
                    if s_nomax < least['nomax'][0]:
                        least['nomax'] = (s_nomax, (u, n, eps))
                else:
                    tot['proviso_fails'] += 1
                    if s_nomax < least['nomax_pf'][0]:
                        least['nomax_pf'] = (s_nomax, (u, n, eps))
                    if s_nomax < -1e-12:
                        tot['viol_nomax_in_proviso_fail'] += 1
    print("cases (u, n, eps): %d; with k* <= n/2: %d" % (tot['cases'], tot['kstar_le_half']))
    print("median step 2^-n E_k > e^{u(k+1)-n Lambda_1}/2 - 1 for p_u n <= k <= n: failures %d" % tot['median_fail'])
    print("k*(eps) > k_1 = max{ceil(p_u n), ceil(rho_h n + c0 - 1)}: %d cases" % tot['kstar_gt_k1'])
    print("bound WITH max{1, c0} (proved): violations %d; least slack %.4f at (u, n, eps) = %s"
          % (tot['viol_max'], least['max'][0], least['max'][1]))
    print("bound WITHOUT the max: violations %d in all; where the proviso holds: least slack %.4f at %s;"
          % (tot['viol_nomax'], least['nomax'][0], least['nomax'][1]))
    print("   cases where the proviso (rho_h - p_u) n >= 1 - c0 FAILS: %d; violations among them %d; least slack %.4f at %s"
          % (tot['proviso_fails'], tot['viol_nomax_in_proviso_fail'], least['nomax_pf'][0], least['nomax_pf'][1]))


def partB():
    print("\n== Part B: floats (lgamma); delta-term omitted; excess = ln(2^n/|B(n,k*)|) - n h ==")
    print("   (referee R12, m1: 0.58, 2.55, 4.07, 5.22 at n = 10, 1e3, 1.6e4, 2.56e5 for u = 1, eps = 1, delta = 0.05,")
    print("    i.e. with ln(1 - 2 delta) = %.4f included; mine below are printed without and with it)" % math.log(0.9))
    for u in (0.5, 1.0, 2.0):
        p, lam1, rho, h = consts(u)
        slope = math.log((1 - rho) / rho)
        for eps in (0.01, 1.0, 10.0):
            c0 = (eps + LN2) / u
            row = []
            worst = 1e300
            for n in (10, 100, 1000, 16000, 256000, 1000000):
                # ln C(n,j), ln|B(n,k)|, ln E_k by recurrences in logarithms, only up to k ~ rho n + c0 + 5
                kmax = min(n, int(rho * n + max(1.0, c0) + 10))
                lB = -math.inf
                lE = -math.inf
                lthr = math.log(math.expm1(eps)) + n * LN2
                leu1 = math.log(math.expm1(u))
                kstar = None
                lBk = None
                for k in range(kmax + 1):
                    lC = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
                    lB = lC if lB == -math.inf else lB + math.log1p(math.exp(lC - lB))
                    t1 = u + lE
                    t2 = leu1 + lB
                    lE = max(t1, t2) + math.log1p(math.exp(-abs(t1 - t2))) if t1 > -math.inf else t2
                    if lE > lthr:
                        kstar = k
                        lBk = lB
                        break
                if kstar is None or 2 * kstar > n:
                    row.append("n=%d: -" % n)
                    continue
                exc = n * LN2 - lBk - n * h
                worst = min(worst, exc + max(1.0, c0) * slope)
                row.append("n=%d: k*=%d (rho_h n=%.1f) excess %.3f [%.3f]" % (n, kstar, rho * n, exc, exc + math.log(0.9)))
            print("u=%g eps=%g: max{1,c0} ln((1-rho)/rho) = %.3f; least slack of (c) %.3f;  %s"
                  % (u, eps, max(1.0, c0) * slope, worst, "; ".join(row)))


if __name__ == "__main__":
    t0 = time.time()
    partA()
    partB()
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    print("LAST LINE r17_lower.py: completed; wall %.1f s; peak RSS %.1f MB" % (time.time() - t0, rss))
