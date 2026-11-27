#!/usr/bin/env python3
"""Where does the increment of the site-wise block capacity cross the cube's exponent, as the coupling goes to zero?

The engineering division's X-013 (section 6) finds numerically that the increment sw_7 - sw_6 of the site-wise optimum
crosses a_cube(u) at u = 1.51, 1.51, 1.50 for p = 0.45, 0.4, 0.3 and reads it as an indication of the crossover of a_inf.
Here, with the coordinator's own code (x013_sitewise_check.py: Blahut-Arimoto on the 2^L site-wise labels): the root in
u of  sw_{L+1}(p, u) - sw_L(p, u) = a_cube(u)  for p -> 1/2 (p = 0.495, 0.49, 0.48, 0.45) and L = 3 ... 7, by bisection -- to see whether the weak-coupling
limit is a number that an expansion to second order in the coupling K = ln((1-p)/p) should reproduce.
Then the coordinator's closed form for the second-order coefficient (a formal expansion to order K^2 of the mutual
information of the channel "site-wise label -> configuration" with an Ising-chain input whose coupling is optimised):
    site-wise capacity per site = a_cube(u) + (K^2 / 4) Fstar(u) + O(K^4),
    Fstar(u) = t^4 (1 - t^4) / 2 - u t^3 (1 - t^2) + (1 - t^2)^2 (u - t (1 + t^2))^2 / (2 t^2),   t = tanh(u / 2),
against the numbers at eleven slopes, with the predicted correlation of the optimal input, and its root u_0; the number of
sign changes of Fstar; whether the remainder scales like K^4; and a point (small u, finite K) where the expansion must fail,
because it is at fixed u > 0 and not uniform as u -> 0.
The numbers are [N]; the formula is a derivation without an error bound.  The site-wise optimum equals the block capacity
only where X-013 certifies it (p >= 0.3, L <= 4), and that the increment converges to a_inf is unproved.  Control: at p = 1/2 the increment must equal a_cube at
every slope (no root: the difference is zero identically).
Run: python3 -B x013_weak_coupling_crossover.py > x013_weak_coupling_crossover.log
"""
import math, time, itertools, functools
import numpy as np
from x013_sitewise_check import sitewise_capacity, a_cube, ustar, block_law

t0 = time.time()


@functools.lru_cache(maxsize=None)
def cap(p, u, L):
    """the site-wise capacity (upper end) by the same iteration as x013_sitewise_check.sitewise_capacity, with the divergences
    computed as  D = sum W ln W - W ln Q  (one matrix-vector product per step); validated against that function below"""
    us = ustar(p, u); w = np.array([u] * (L - 1) + [us]); X, pi = block_law(p, L); XA = np.array(X)
    mism = (XA[:, None, :] != XA[None, :, :]).astype(float) @ w                      # [sigma, x] = sum_i w_i [x_i != sigma_i]
    W = pi[None, :] * np.exp(-mism); W /= W.sum(axis=1, keepdims=True); h = (W * np.log(W)).sum(axis=1); M = np.full(len(X), 1.0 / len(X))
    for _ in range(200000):
        D = h - W @ np.log(M @ W); lo, hi = float(M @ D), float(D.max())
        if hi - lo < 1e-12: break
        M = M * np.exp(D); M /= M.sum()
    assert hi - lo < 1e-10, (p, u, L, hi - lo)
    cap.inputs[(p, u, L)] = (XA, M)
    return hi


cap.inputs = {}


def Fstar(u):
    """the coordinator's second-order coefficient (derivation in SCI-RES-0033 section 4 and addendum item 91):
    site-wise capacity per site = a_cube(u) + (K^2 / 4) Fstar(u) + O(K^4),   t = tanh(u/2)"""
    t = math.tanh(u / 2)
    return t ** 4 * (1 - t ** 4) / 2 - u * t ** 3 * (1 - t * t) + (1 - t * t) ** 2 * (u - t * (1 + t * t)) ** 2 / (2 * t * t)


def F_uniform(u):                       # the same with independent inputs (lambda = 0): the control
    t = math.tanh(u / 2); return t ** 4 * (1 - t ** 4) / 2 - u * t ** 3 * (1 - t * t)


def alpha_star(u):                      # predicted coupling of the optimal input chain, in units of J = K / 2
    t = math.tanh(u / 2); return (1 - t * t) * (u - t * (1 + t * t)) / t ** 3


def diff(p, u, L): return cap(p, u, L + 1) - cap(p, u, L) - a_cube(u)


def root(p, L, lo=1.2, hi=1.9):
    flo, fhi = diff(p, lo, L), diff(p, hi, L); assert flo > 0 > fhi, (p, L, flo, fhi)
    for _ in range(24):
        mid = 0.5 * (lo + hi); fm = diff(p, mid, L)
        lo, hi = (mid, hi) if fm > 0 else (lo, mid)
    return 0.5 * (lo + hi)


chk = max(abs(cap(p_, u_, L_) - sitewise_capacity(p_, u_, L_)[1]) for p_, u_, L_ in ((0.3, 1.5, 4), (0.45, 2.0, 3), (0.4, 1.0, 5)))
print(f"the fast iteration against x013_sitewise_check.sitewise_capacity at three points: largest difference {chk:.1e} (must be below 1e-10)")
assert chk < 1e-10


print("control, p = 1/2 (no coupling): increment minus a_cube at u = 1, 1.5, 2 for L = 3: " + ", ".join(f"{diff(0.5, u, 3):+.1e}" for u in (1.0, 1.5, 2.0)) + " (must vanish)")
assert all(abs(diff(0.5, u, 3)) < 1e-10 for u in (1.0, 1.5, 2.0))
print("| p | K | root in u of the increment (L -> L+1) minus a_cube, for L = 3, 4, 5, 6, 7 | second-order coefficient near the root: [increment - a_cube] / K^2 at u = 1.2, 1.5, 1.8 (L = 6) |")
print("|---|---|---|---|")
res = {}; c2s = {}
for p in (0.495, 0.49, 0.48, 0.45):               # weak coupling first: the iteration converges slowly at strong coupling (p = 0.3, 0.4 are in X-013: 1.50, 1.51)
    K = math.log((1 - p) / p); rs = [root(p, L) for L in (3, 4, 5, 6, 7)]; res[p] = rs
    c2 = [diff(p, u, 6) / K ** 2 for u in (1.2, 1.5, 1.8)]; c2s[p] = c2
    print(f"| {p} | {K:.4f} | {', '.join(f'{r:.5f}' for r in rs)} | {', '.join(f'{c:+.5f}' for c in c2)} | [{time.time() - t0:.0f}s]", flush=True)
# ---- the closed form against the numbers
pp = 0.499; K = math.log((1 - pp) / pp); J = K / 2; dev = 0.0; devu = 0.0
print(f"second-order coefficient: [increment (L = 5 -> 6) - a_cube] / K^2 at p = {pp} against Fstar(u) / 4, and against the same formula with independent inputs (control):")
print("| u | numerical | Fstar(u) / 4 | independent inputs (control) | nearest-neighbour correlation of the optimal input (interior bond, L = 6) | predicted alpha*(u) K / 2 |")
print("|---|---|---|---|---|---|")
for u in (0.5, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0, 4.0, 6.0):
    num = diff(pp, u, 5) / K ** 2; XA, M = cap.inputs[(pp, u, 6)]; sg = 1 - 2 * XA; corr = float((M * sg[:, 2] * sg[:, 3]).sum())
    dev = max(dev, abs(num - Fstar(u) / 4)); devu = max(devu, abs(num - F_uniform(u) / 4))
    print(f"| {u} | {num:+.6f} | {Fstar(u) / 4:+.6f} | {F_uniform(u) / 4:+.6f} | {corr:+.6f} | {alpha_star(u) * J:+.6f} |")
print(f"largest |numerical - Fstar / 4| = {dev:.1e} (must be below 1e-4: the next order is K^2 = {K * K:.1e} times a coefficient of order one); control, independent inputs: {devu:.2f} (must be far from zero)")
assert dev < 1e-4 and devu > 0.02
lo_, hi_ = 1.2, 1.9
for _ in range(60):
    mid = 0.5 * (lo_ + hi_); lo_, hi_ = (mid, hi_) if Fstar(mid) > 0 else (lo_, mid)
u0 = 0.5 * (lo_ + hi_)
print(f"the root of Fstar: u_0 = {u0:.6f}  (Fstar > 0 below it: the coupling raises the site-wise capacity; < 0 above it)")
def Fsign(u):
    """Fstar(u) / (1 - t^2), with 1 - t^2 = 1 / cosh^2(u/2) taken out (in double precision tanh(u/2) = 1 exactly from u = 38 on, and
    Fstar itself evaluates to 0 there -- a first version counted that as a second sign change); its limit at large u is 1 - u"""
    t = math.tanh(u / 2); s2 = 1.0 / math.cosh(u / 2) ** 2
    return t ** 4 * (1 + t * t) / 2 - u * t ** 3 + s2 * (u - t * (1 + t * t)) ** 2 / (2 * t * t)


grid = np.arange(0.02, 40.0, 0.001); sg_ = np.sign([Fsign(float(v)) for v in grid]); nch = int((sg_[1:] != sg_[:-1]).sum())
chkF = max(abs(Fsign(v) / math.cosh(v / 2) ** 2 - Fstar(v)) for v in (0.3, 1.0, 1.5, 2.5, 6.0))
print(f"sign changes of Fstar on the grid u = 0.02 ... 40 (step 0.001), from Fstar / (1 - t^2): {nch} (must be 1; this form against Fstar at five slopes: {chkF:.1e}); "
      f"Fstar(0.02) = {Fstar(0.02):.4f} (its limit at u -> 0 is 1/2); Fstar / (1 - t^2) at u = 40: {Fsign(40.0):.3f} (its limit at large u is 1 - u)")
assert nch == 1 and chkF < 1e-12
# ---- the next order: does the remainder scale like K^4 (as the symmetry K -> -K of the bulk suggests) or like K^3 ?
print("the remainder [increment - a_cube] / K^2 - Fstar / 4, divided by K^2 (constant in K if the next term is of order K^4), at u = 1.2, 1.5, 1.8, and the shift of the root, (root - u_0) / K^2:")
print("| p | K | remainder / K^4 at u = 1.2, 1.5, 1.8 | (root - u_0) / K^2 (L = 7) |")
print("|---|---|---|---|")
sh = {}
for p_ in (0.49, 0.48, 0.45):
    K_ = math.log((1 - p_) / p_); rem = [(c - Fstar(u_) / 4) / K_ ** 2 for c, u_ in zip(c2s[p_], (1.2, 1.5, 1.8))]; sh[p_] = (res[p_][-1] - u0) / K_ ** 2
    print(f"| {p_} | {K_:.4f} | {', '.join(f'{v:+.4f}' for v in rem)} | {sh[p_]:+.4f} |")
assert abs(sh[0.48] - sh[0.45]) < 0.2 * abs(sh[0.45])                 # a K^3 term would make these differ by the factor K(0.45)/K(0.48) = 2.5
# ---- the expansion is at fixed u > 0: it is not uniform as u -> 0 (the optimal input coupling alpha* J ~ J / t^2 must be small)
p_, u_ = 0.45, 0.1; K_ = math.log((1 - p_) / p_); num_ = diff(p_, u_, 5) / K_ ** 2
print(f"not uniform as u -> 0: at p = {p_} (K / 2 = {K_ / 2:.3f}), u = {u_} (t^2 = {math.tanh(u_ / 2) ** 2:.4f}, predicted alpha* K / 2 = {alpha_star(u_) * K_ / 2:.1f}, not small): "
      f"numerical [increment - a_cube] / K^2 = {num_:+.5f} against Fstar / 4 = {Fstar(u_) / 4:+.5f} (must differ: by {abs(num_ - Fstar(u_) / 4):.3f})")
assert abs(num_ - Fstar(u_) / 4) > 0.01
r = res[0.495][-1]
assert abs(u0 - r) < 2e-4
print(f"weak-coupling limit (p = 0.495, L = 7 -> 8): u_0 = {r:.5f}; change from p = 0.49: {r - res[0.49][-1]:+.1e}; change from L = 6: {r - res[0.495][-2]:+.1e}")
print(f"for comparison: the root of u tanh(u/2) = 1 (the inflection point of a_cube) is 1.54340; u_0 / 1.54340 = {r / 1.5434046:.5f}")
print(f"ALL DONE {time.time() - t0:.0f} s")
