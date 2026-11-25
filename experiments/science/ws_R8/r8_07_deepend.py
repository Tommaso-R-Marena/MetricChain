#!/usr/bin/env python3
"""R8 / script 07 -- the deep end of Proposition A16.3 written out, and two repairs of A16.6.

Part 1.  A16.3, step (3): "m(r2) < U0 by the algebra of R6.2 at s = +1" for every r2 >= r1 + 1.
  Notation (k = r2 - r1 >= 1, twin = the full cone of radius r2 about a'):
     W  = sum_{d<r1} C(n,d) e^{u(r1-d)},  V = |B(n,r1-1)|,  Z0 = 2^n + W - V,  A' = -sum g0 e^{-g0},
     X  = sum_{d=r1}^{r2-1} C(n,d) e^{-u(d-r1)}        (the cone's mass beyond r1, divided by e^{uk})
     Y  = sum_{d=r1}^{r2-1} C(n,d) u (r2-d) e^{-u(d-r1)},
     free sums (as if g0 = 0 on the twin's support):  E^f = e^{uk}(W+X) - |B(n,r2-1)|,
                                                     D^f = -e^{uk}(A' + u k W + Y),
     omega = sum over the overlap {g0<0, T<0} of e^{-T}.
  Chain (each step is checked numerically below, with exact sums):
     (i)   E^f - omega <= E <= E^f
     (ii)  D^f <= D <= D^f + u r2 omega
     (iii) W + X <= Z0                                   [because X <= 2^n - V; no hypothesis]
     (iv)  D^f + (A'/Z0) E^f <= -e^{uk}(u k W + Y)       [from (iii)]
     (v)   D + (A'/Z0) E <= -e^{uk}(u k W + Y) + u r2 omega
  Hence  m(r2) < U0  as soon as   r2 omega < e^{uk}(k W + Y/u);  since omega <= p e^{uk}(W+X) with p the
  overlap fraction and Y >= u X, k >= 1, it suffices that  p < 1/r2.   No dominance hypothesis is
  needed at the deep end (it is needed at the shallow end only through |U0| > 1).
  With Hoeffding's bound  p <= exp(-(n/2 - r1 - 2 Delta)^2/(2 r2)),  Delta = sqrt(n ln n):  the least n
  from which the sufficient condition holds is tabulated.

Part 2.  A16.6 (ii)/(iii), expectation against high probability.
  (a) quantile form of the lower bound:  P(#evaluations > m) >= (1-2 delta)(1-2/n^2) - m |B(n,r2-1)|/2^n.
  (b) a tolerant test: accept "all but at most k0 of M' samples show one value v"; then E[cost at g0]
      <= M' + 1 with an exhaustive fallback as soon as (M'|V|/2^n)^{k0+1} 2^n <= 1.  Table of k0.

Run:  python3 r8_07_deepend.py        (about 1 minute)
"""
import math, sys
import numpy as np
from scipy.special import logsumexp
from r8_lib import *
import r8_02_twin as TW


def part1():
    print("== 1: the deep-end chain, exact sums ==")
    ok = True
    for (n, u, drho, k, Dfrac) in ((400, 1.0, 0.03, 1, 0.5), (400, 1.0, 0.03, 12, 0.5), (800, 1.0, 0.02, 30, 0.42),
                                   (800, 2.0, 0.01, 60, 0.5), (600, 4.0, 0.01, 80, 0.55), (800, 1.0, 0.02, 30, 0.25),
                                   (800, 1.0, 0.02, 30, 0.1), (300, 0.5, 0.02, 5, 0.5)):
        r1 = math.ceil((rho0(u) + drho) * n); r2 = r1 + k; D = int(Dfrac * n)
        tw = TW.Twin(n, u, r1, r2, D)
        lc = lnC(n); d = np.arange(n + 1)
        # all quantities divided by 2^n e^{uk}-free scale: work in logs relative to s = ln Z0
        s = tw.lnZ0
        lnW = float(logsumexp(lc[:r1] + u * (r1 - d[:r1])))
        lnV = ln_ball(n, r1 - 1, lc)
        lnA = float(logsumexp(lc[:r1] + u * (r1 - d[:r1]) + np.log(u * (r1 - d[:r1]))))
        lnX = float(logsumexp(lc[r1:r2] - u * (d[r1:r2] - r1)))
        lnY = float(logsumexp(lc[r1:r2] - u * (d[r1:r2] - r1) + np.log(u * (r2 - d[r1:r2]))))
        uk = u * k
        # true sums at kappa = r2 (full cone)
        T = tw.T(float(r2))
        mask = T < tw.g0
        lcm = tw.lc[mask]; Tm = T[mask]; gm = tw.g0[mask]
        lnE = float(logsumexp(lcm - Tm + np.log1p(-np.exp(Tm - gm))))
        # D = sum (T e^{-T} - g0 e^{-g0}) <= 0 ;  -D = sum (|T| e^{|T|} - |g0| e^{|g0|})
        negD = np.exp(lcm - Tm - s) * (-Tm) - np.exp(lcm - gm - s) * (-gm)
        Dsc = -float(negD.sum())                                   # D / Z0
        Esc = math.exp(lnE - s)                                    # E / Z0
        sup = T < 0
        ov = sup & (tw.g0 < 0)
        lnom = float(logsumexp((tw.lc - T)[ov])) if ov.any() else -np.inf
        lnW2 = float(logsumexp((tw.lc - T)[sup]))
        Efsc = math.exp(uk + np.logaddexp(lnW, lnX) - s) - math.exp(ln_ball(n, r2 - 1, lc) - s)
        Dfsc = -math.exp(uk - s) * (math.exp(lnA) + uk * math.exp(lnW) + math.exp(lnY)) if lnA < 700 else None
        # use logs for the big ones
        lnDf = uk - s + float(logsumexp([lnA, math.log(uk) + lnW, lnY]))      # ln(-D^f/Z0)
        Dfsc = -math.exp(lnDf)
        omsc = math.exp(lnom - s)
        AoverZ = math.exp(lnA - s)                                  # A'/Z0 = |U0|
        c1 = (Efsc - omsc) * (1 - 1e-9) <= Esc <= Efsc * (1 + 1e-9)
        c2 = Dfsc * (1 + 1e-9) <= Dsc <= (Dfsc + u * r2 * omsc) * (1 - 1e-9) + 1e-300 if Dfsc + u * r2 * omsc < 0 else Dfsc * (1 + 1e-9) <= Dsc
        c3 = np.logaddexp(lnW, lnX) <= s + 1e-12
        lhs4 = Dfsc + AoverZ * Efsc
        rhs4 = -math.exp(uk - s) * (uk * math.exp(lnW) + math.exp(lnY))
        c4 = lhs4 <= rhs4 * (1 - 1e-9)
        lhs5 = Dsc + AoverZ * Esc
        rhs5 = rhs4 + u * r2 * omsc
        c5 = lhs5 <= rhs5 + abs(rhs5) * 1e-9
        suff = lnom - lnW2 < -math.log(r2)
        sign = lhs5 < 0
        print(f"  n={n} u={u} r1={r1} r2=r1+{k} D={D}: (i) {c1} (ii) {c2} (iii) {c3} (iv) {c4} (v) {c5};  "
              f"ln(omega/W2)={lnom-lnW2:7.1f} vs ln(1/r2)={-math.log(r2):.1f}: sufficient condition {suff};  m(r2) < U0: {sign}")
        ok &= c1 and c2 and c3 and c4 and c5 and (sign or not suff)
    print("  least n from which Hoeffding's bound gives the sufficient condition p < 1/r2  (rho_bar = r2/n):")
    for (u, drho, rbar) in ((1.0, 0.01, 0.45), (1.0, 0.01, 0.49), (2.0, 0.01, 0.40), (4.0, 0.01, 0.30), (0.5, 0.01, 0.47)):
        rho1 = rho0(u) + drho
        n0 = None
        for n in range(50, 2000001, 50):
            Delta = math.sqrt(n * math.log(n))
            t = n / 2 - rho1 * n - 2 * Delta
            if t > 0 and t * t / (2 * rbar * n) > math.log(rbar * n):
                n0 = n
                break
        print(f"     u={u} rho1=rho0+{drho} rho_bar={rbar}: n >= {n0}")
    return ok


def part2():
    print("== 2: expectation against high probability in A16.6 ==")
    print("  (a) quantile lower bound: every class-correct algorithm with the datum uses more than m evaluations at g0 with")
    print("      probability >= (1-2 delta)(1-2/n^2) - m|B(n,r2-1)|/2^n;  e.g. delta=0.05, m = 0.45*2^n/|B|: >= 0.45 - o(1).")
    print("  (b) tolerant test: least k0 with (M'|V|/2^n)^(k0+1) * 2^n <= 1, M' = 3(ln(1/delta)+k0) 2^n/|B(n,R)|, delta = 0.05")
    for (n, u, drho, e1) in ((800, 1.0, 0.02, 0.03), (1500, 1.0, 0.01, 0.05), (1000, 2.0, 0.01, 0.10), (700, 4.0, 0.01, 0.30),
                             (400, 1.0, 0.03, 0.02), (2400, 1.0, 0.005, 0.02)):
        lbt = ln_ball_table(n)
        r1 = math.ceil((rho0(u) + drho) * n)
        R = int((r1 / n - sig(u) + sigma2(u, e1)) * n) - 2
        k0 = None
        for k in range(0, 2000):
            lnMp = math.log(3 * (math.log(20) + k)) + n * LN2 - lbt[R]
            lnp = lnMp + lbt[r1 - 1] - n * LN2
            if lnp < 0 and (k + 1) * lnp + n * LN2 <= 0:
                k0 = k
                break
        print(f"     n={n} u={u} r1={r1} R={R}: ln(M|V|/2^n) = {math.log(math.log(20)) + lbt[r1-1] - lbt[R]:8.2f};  k0 = {k0}"
              f"  (asymptotically k0 ~ ln2/(h(R/n)-h(r1/n)) = {LN2/(hb(R/n)-hb(r1/n)):.1f})")
    return True


if __name__ == "__main__":
    ok = part1()
    part2()
    print("SUMMARY deep-end chain holds in all cases:", ok)
