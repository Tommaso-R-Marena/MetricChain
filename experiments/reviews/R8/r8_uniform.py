#!/usr/bin/env python3
"""Referee R8 -- the uniform statements (E0') numerically (accuracies that tend to zero; Corollary K3'(ii)).  Own code.

(a) Proposition K0: cost 2M of the two-sample bracket in dimension d at the accuracies x = 1, 0.01, d^-2,
    exp(-sqrt d), exp(-d^0.8) with delta' = e^{-d}: ln(2M)/(d a) must tend to 1 whenever ln(1/x_d) = o(d).
(b) Theorem K2 with a small target accuracy x: Algorithm 2L+ with b = x/2, lam = eta = eta' = theta = x/12,
    nu_1 = 2e^u n_o/theta, 40 rungs, Proposition-K0 brackets inside, at psi = 0 (exact number of evaluations,
    as in r8_flat.py): bracket valid, width <= x, cost >= hinted lower bound for eps = x, cost <= C_max,
    and ln(cost)/(n a) against the value at x_out = 0.87.

usage: python3 r8_uniform.py
"""
import math, sys, time
import numpy as np
import r8_flat as F

t0 = time.time()
u = 1.0
pu = 1 / (1 + math.exp(u))
a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
print("(a) Proposition K0, u = 1, delta' = e^{-d}: ln(cost)/(d a)   [cost = min(2M, 2^d)]")
print("      d      x=1      x=0.01    x=d^-2   x=exp(-sqrt d)  x=exp(-d^0.8)")
for d in (1000, 10000, 100000, 1000000):
    row = []
    for lx in (0.0, math.log(0.01), -2 * math.log(d), -math.sqrt(d), -d ** 0.8):
        x = math.exp(lx) if lx > -700 else None
        if x is None or x < 1e-300:
            row.append(float('nan'))
            continue
        c, lL, lU, kind = F.k0_plan_flat(d, u, x, -float(d))
        row.append(c / (d * a))
    print("%8d  %7.4f  %7.4f  %7.4f   %7.4f        %7.4f" % (d, *row))
print("    (exp(-d^0.8) underflows for d >= 10^4: nan; there ln(1/x)/d is still 0.16 at d = 10^5)")
print("(b) Theorem K2 with a small target accuracy x, at psi = 0, u = 1:")
print("      n     x      phi   ln(cost)/(na)  hinted LB/(na)  ln(C_max)/(na)  width<=x  valid  cost>=LB  cost<=C_max  levels J   K")
for (n, x, phis) in ((4000, 0.87, (0.65,)), (4000, 0.2, (0.65, 0.8)), (4000, 0.05, (0.65, 0.8)), (16000, 0.87, (0.55,)),
                     (16000, 0.2, (0.55, 0.65)), (16000, 0.05, (0.55, 0.65))):
    for phi in phis:
        if x == 0.87:
            r = F.flat_run(u, n, phi)
        else:
            c0 = x / 12
            r = F.flat_run(u, n, phi, lam=c0, eta=c0, etap=c0, theta=c0, b=x / 2, delta=0.05, Lr=40, bounded=True)
        lb, kstar = F.hinted_lower_bound(u, n, r['xout'], 0.05)
        print("%7d  %5.2f  %5.2f    %8.4f       %8.4f        %8.4f       %s     %s    %s      %s     %9d  %d   [%.0f s]"
              % (n, x, phi, r['lcost'] / (n * a), lb / (n * a), r['lCmax'] / (n * a), r['width'] <= x + 1e-9 if x != 0.87 else r['width'] <= r['xout'] + 1e-9,
                 r['lL'] <= 1e-12 and r['lU'] >= -1e-12, r['lcost'] >= lb, r['lcost'] <= r['lCmax'] + 1e-9, r['J'], r['K'], time.time() - t0))
        sys.stdout.flush()
