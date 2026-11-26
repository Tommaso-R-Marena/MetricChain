#!/usr/bin/env python3
"""R24, item 1 (iii): explicit small models in which the least ratio lambda_gs = min_x c(x)/b(x) and the transition lambda_c
(half of the weight displaced, or mean number of displaced sites = n/2) differ by a large factor -- or in which one exists
without the other.  Everything by enumeration (brute force), no code of the division.
 M1  one reference state a (cost 0, penalty 0) and q displaced states of cost c1 and penalty b1 each (a degenerate level);
 M2  n independent sites, each with one reference state and q displaced states (cost c1, penalty b1 per displaced site):
     no single state takes over, the crossover is smooth, lambda_gs / lambda_c does not depend on n;
 M3  M1 with q = 1 and a penalty that is b0 > 0 on EVERY state plus b1 on the displaced one: lambda_gs is finite and small,
     lambda_c is where it was (a constant penalty changes nothing in the ensemble): lambda_gs is not an upper bound either.
Control: M1 with q = 1 (no entropy): the two agree to e^{-c1}.
Run: python3 -B r24_item1_toy.py > r24_item1_toy.log
"""
import math, itertools, resource
import numpy as np


def analyse(cost, pen, disp, n_half):
    """cost, pen: arrays over states (kT); disp: number of displaced sites per state.  Returns (lambda_gs, lambda_c)."""
    L0 = math.log(np.exp(-cost).sum()); c = L0 + cost; pos = pen > 0; lam_gs = float((c[pos] / pen[pos]).min())
    def occ(lam):
        a = lam * pen - c; a -= a.max(); p = np.exp(a); p /= p.sum(); return float((p * disp).sum())
    lo, hi = 0.0, 1.0
    while occ(hi) < n_half and hi < 1e6: hi *= 2
    if hi >= 1e6: return lam_gs, float("inf")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if occ(mid) < n_half: lo = mid
        else: hi = mid
    return lam_gs, 0.5 * (lo + hi)


print("M1  one reference state, q displaced states of cost c1 = 10 kT and penalty b1 = 1 kT:  q | lambda_gs | lambda_c (half the weight displaced) | ratio | closed forms (c1 + ln(1 + q e^-c1))/b1, (c1 - ln q)/b1")
for q in (1, 10, 100, 1000, 8103, 20000):
    cost = np.array([0.0] + [10.0] * q); pen = np.array([0.0] + [1.0] * q); disp = np.array([0.0] + [1.0] * q)
    g, cst = analyse(cost, pen, disp, 0.5)
    print(f"      {q} | {g:.5f} | {cst:.5f} | {g / cst:.3f} | {10 + math.log(1 + q * math.exp(-10)):.5f}, {10 - math.log(q):.5f}")
print("M2  n independent sites, each with q = 6 displaced states of cost c1 = 3 kT and penalty b1 = 1 kT (a rotamer-like alphabet):  n | lambda_gs | lambda_c (mean displaced = n/2) | ratio | closed forms")
for n in (1, 2, 4, 6):
    q = 6; st = np.array(list(itertools.product(range(q + 1), repeat=n))); disp = (st > 0).sum(axis=1).astype(float)
    g, cst = analyse(3.0 * disp, 1.0 * disp, disp, n / 2)
    print(f"      {n} | {g:.5f} | {cst:.5f} | {g / cst:.3f} | {3 + math.log(1 + q * math.exp(-3)):.5f}, {3 - math.log(q):.5f}")
print("M3  two states, cost (0, 10), penalty (b0, b0 + 1): a penalty with a constant part.  b0 | lambda_gs | lambda_c | ratio")
for b0 in (0.0, 0.01, 0.1, 1.0):
    g, cst = analyse(np.array([0.0, 10.0]), np.array([b0, b0 + 1.0]), np.array([0.0, 1.0]), 0.5)
    print(f"      {b0:g} | {g:.6f} | {cst:.5f} | {g / cst:.2e}")
print(f"ALL DONE; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
