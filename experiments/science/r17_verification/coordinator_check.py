#!/usr/bin/env python3
"""Coordinator's checks of workstream R17 (the referee report on the theory division's Theorem 11.58a), with lines
that are neither R17's nor the theory division's.

(1) The constants of the cube class at slope u: p_u, Lambda_1, a = KL(p_u || 1/2), rho_h = Lambda_1 / u, h = KL(rho_h || 1/2).
(2) The lower bound (c) of Theorem 11.58a:
        ln N  >=  n h - max{1, (eps + ln 2)/u} ln((1 - rho_h)/rho_h) - ln(1/(1 - 2 delta))
    as a consequence of the hinted bound  N >= (1 - 2 delta) 2^n / |B(n, k*)|,  k* = the least k with
    Delta_k = ln(1 + 2^-n E_k) > eps,  E_k = sum_{j <= k} C(n, j) (e^{u (k + 1 - j)} - 1)  (exact integers for the
    binomials, 60-digit decimals for the exponentials).  Checked on a grid; the excess over n h at the sizes R17 quotes;
    a control that must fail: the same inequality without its O(1) term.
(3) The epoch schedule of the upper bound (theory report, Theorem 11.58a; our RateFull.lean): d_0 = h/(a - h),
    J_m = ceil(d_m), B_m = h (1 + 1/d_m), B_{m+1} = B_m J_m a / (J_m a + h); k_M = 1 + sum_{m < M} (J_m + 1) levels with
    the bracket counted; compared with the numbers of R17's table (best M, k_M) and with the leading term B_M / a of
    "bound / (n a)".
Run: python3 -B coordinator_check.py > coordinator_check.log
"""
import math, sys, time
from decimal import Decimal, getcontext
from math import comb
getcontext().prec = 60
t0 = time.time()


def consts(u):
    p = 1.0 / (1.0 + math.exp(u)); L1 = math.log(2.0 / (1.0 + math.exp(-u)))
    kl = lambda x: math.log(2.0) + x * math.log(x) + (1 - x) * math.log(1 - x)
    rho = L1 / u
    return p, L1, kl(p), rho, kl(rho)


def kstar(n, u, eps):
    """least k with ln(1 + 2^-n E_k) > eps; E_k computed incrementally: E_k = e^u E_{k-1} + (e^u - 1) |B(n, k)|."""
    eu = Decimal(u).exp(); thr = (Decimal(eps).exp() - 1) * (Decimal(2) ** n)
    ball = 1; E = (eu - 1) * 1                                              # k = 0: C(n,0) (e^u - 1)
    k = 0
    while E <= thr:
        if k == n: return None, None                                       # no single dip moves ln A by more than eps: the bound is empty
        k += 1; ball += comb(n, k); E = eu * E + (eu - 1) * ball
    return k, ball


print("(1) constants")
for u in (0.5, 1.0, 2.0):
    p, L1, a, rho, h = consts(u)
    print(f"    u = {u}: p_u = {p:.6f}, Lambda_1 = {L1:.6f}, a = {a:.6f}, rho_h = {rho:.6f}, h = {h:.6f}, h/a = {h / a:.6f}, ln((1-rho_h)/rho_h) = {math.log((1 - rho) / rho):.6f}")

print("(2) the lower bound (c): exact hinted bound against the closed form")
viol = ctrl = cases = skipped = 0; least = float("inf")
for u in (0.1, 0.5, 1.0, 2.0, 4.0, 8.0):
    p, L1, a, rho, h = consts(u); slope = math.log((1 - rho) / rho)
    for n in list(range(2, 61)) + [80, 100, 150, 200, 300]:
        for eps in (0.001, 0.1, 1.0, 5.0, 20.0):
            k, ball = kstar(n, u, eps)
            if k is None or 2 * k > n: skipped += 1; continue
            for delta in (0.05, 0.4):
                exact = math.log(1 - 2 * delta) + n * math.log(2.0) - math.log(ball)   # ln of the hinted bound
                closed = n * h - max(1.0, (eps + math.log(2.0)) / u) * slope - math.log(1.0 / (1 - 2 * delta))
                cases += 1; viol += int(exact < closed - 1e-9); least = min(least, exact - closed)
                ctrl += int(exact < n * h - 1e-9)                                     # control: "ln N >= n h" with no O(1) term
print(f"    {cases} cases with k* <= n/2 ({skipped} skipped: k* > n/2 or no k*): violations of (c): {viol}; least slack {least:.3f} nats; "
      f"control that must fail (the bound without its O(1) term, 'ln N >= n h'): {ctrl} violations")
assert viol == 0 and ctrl > 0
u, eps, delta = 1.0, 1.0, 0.05; p, L1, a, rho, h = consts(u)
cells = []
for n in (10, 1000, 16000):
    k, ball = kstar(n, u, eps); cells.append(f"n = {n}: k* = {k}, excess {math.log(1 - 2 * delta) + n * math.log(2.0) - math.log(ball) - n * h:.3f}")
print("    excess of the hinted bound over n h at u = 1, eps = 1, delta = 0.05 (R17: 0.579, 2.552, 4.066): " + "; ".join(cells))

print("(3) the epoch schedule at u = 1")
d = h / (a - h); B = h * (1 + 1 / d); k = 1; Js = []; rows = {}
assert abs(B - a) < 1e-12
for m in range(0, 26):
    rows[m] = (k, B / a)
    J = math.ceil(d - 1e-12); Js.append(J)
    B = B * J * a / (J * a + h); d = 1.0 / (B / h - 1.0); k += J + 1
for M, kM_r17, ratio_r17, n in ((5, 13, 0.7072, 6.4e4), (10, 43, 0.3713, 1e6), (17, 268, 0.2731, 1e8), (25, 2868, 0.2637, 1e10)):
    kM, BMa = rows[M]
    print(f"    M = {M}: k_M = {kM} (R17's table: {kM_r17}; agree: {kM == kM_r17}); slope steps J_0..J_(M-1) sum to {sum(Js[:M])}; leading term B_M/a = {BMa:.4f}; "
          f"R17's bound/(n a) at n = {n:.1e}: {ratio_r17} -> error term / (n a) = {ratio_r17 - BMa:.4f}")
    assert kM == kM_r17 and BMa < ratio_r17
print(f"    h/a = {h / a:.4f}: the limit of bound/(n a)")
print(f"ALL DONE {time.time() - t0:.0f} s")
