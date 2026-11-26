#!/usr/bin/env python3
"""Coordinator's checks of workstream R13 before publication as SCI-REV-0014 -- written from the statements; none of
the workstream's code is imported.

(1) Finding M1 (the theory division's Proposition 11.117(b) without "symmetric").  Two points, pi = (q, 1 - q),
    envelope u d0 with d0(0, 1) = 1, d0(1, 0) = 0: the class is {c 1[x = 0] : 0 <= c <= u}.  The site function of the
    theory report's Setting,  F*(t) = min_Q max_phi  -ln sum_x pi_phi(x)^t Q(x)^(1-t),  computed by a one-dimensional
    minimisation in 40-digit arithmetic, against the claimed (t(1-t)/2) u^2 V with V = q(1 - q); the same with the
    symmetric envelope d0 = 1 both ways (same V).
(2) Finding m1: E_F := ln[(1-p) cosh(u/2) + sqrt((1-p)^2 sinh^2(u/2) + p^2)] against ln cosh(u/2) for p > 1/2.
(3) The constants of the rate at u = 1 from a = KL(p_u || 1/2), h = KL(Lambda_1/u || 1/2) as quoted in the report
    (the two numbers are taken from R13's table; kappa, c1, c2 are recomputed from the remark's formulas), and the
    epoch recursion  d' = d (J a + h)/(J a - h d),  J = ceil(d),  against the closed form  h/d_m <= c1/(k + c2)  at
    every level, in exact rational arithmetic.
Run:  python3 -B r13_adoption_check.py > r13_adoption_check.log      (seconds)
"""
import math
from fractions import Fraction
import mpmath as mp
mp.mp.dps = 40


def Fstar(q, t, u, sym):
    cs = [-u, u] if sym else [0, u]
    def pi(c):
        a = q * mp.e ** (-c); b = 1 - q; return a / (a + b), b / (a + b)
    Ps = [pi(c) for c in cs]
    def val(r, PP):
        return max(-mp.log(P[0] ** t * r ** (1 - t) + P[1] ** t * (1 - r) ** (1 - t)) for P in PP)
    lo, hi = mp.mpf("1e-12"), 1 - mp.mpf("1e-12"); g = (mp.sqrt(5) - 1) / 2
    for _ in range(200):
        a = hi - g * (hi - lo); b = lo + g * (hi - lo)
        if val(a, Ps) < val(b, Ps): hi = b
        else: lo = a
    r = (lo + hi) / 2
    inner = [pi(cs[0] + (cs[1] - cs[0]) * mp.mpf(k) / 50) for k in range(51)]     # members between the vertices
    assert abs(val(r, Ps) - val(r, inner)) < mp.mpf("1e-20")
    return val(r, Ps)


print("(1) F*(t) / ((t(1-t)/2) u^2 V), V = q(1-q), at u = 0.4, 0.2, 0.1, 0.05, 0.025")
for q, t in ((mp.mpf("0.5"), mp.mpf("0.3")), (mp.mpf("0.3"), mp.mpf("0.5"))):
    for sym in (False, True):
        row = [mp.nstr(Fstar(q, t, mp.mpf(u), sym) / (t * (1 - t) / 2 * mp.mpf(u) ** 2 * q * (1 - q)), 5) for u in ("0.4", "0.2", "0.1", "0.05", "0.025")]
        print(f"    q = {mp.nstr(q, 2)}, t = {mp.nstr(t, 2)}, {'symmetric envelope    ' if sym else 'NON-symmetric envelope'}: " + ", ".join(row))
print("    -> without symmetry the ratio tends to 1/4, with it to 1: Proposition 11.117(b) needs the word.")
EF = lambda p, u: math.log((1 - p) * math.cosh(u / 2) + math.sqrt((1 - p) ** 2 * math.sinh(u / 2) ** 2 + p * p))
print(f"(2) E_F(p = 0.7, u = 1) = {EF(0.7, 1.0):.6f}, E_F(p = 0.3, u = 1) = {EF(0.3, 1.0):.6f}, ln cosh(1/2) = {math.log(math.cosh(0.5)):.6f}"
      f"  -> 'E_F > ln cosh(u/2) for p != 1/2' fails for p > 1/2")
a, h = Fraction("0.110944071672"), Fraction("0.0291391385016")
kappa = h * h * a / ((a - h) * (a + h) * (2 * a - h)); c1 = h * (1 + kappa) / kappa; c2 = (a + h) * (2 * a - h) / (h * a) - 2
print(f"(3) u = 1: kappa = {float(kappa):.6f}, c1 = {float(c1):.6f} = {float(c1 / a):.3f} a, c2 = {float(c2):.6f}")
d = h / (a - h); k = 1; worst = Fraction(0); nep = 0
while k < 200000:
    J = math.ceil(d)                                     # an epoch of J + 1 levels starts at level k with B_k = h (1 + 1/d)
    for kk in range(k, k + J + 1):                       # every level of the epoch is bounded by the epoch's starting value
        ratio = (h / d) / (c1 / (kk + c2)); worst = max(worst, ratio)
        assert ratio <= 1, (kk, float(ratio))
    dn = d * (J * a + h) / (J * a - h * d)
    assert dn - d > (J + 1) * kappa
    # keep the rationals small: round d DOWN to 40 digits when its denominator has grown (a smaller d is a weaker, safe bound)
    d = Fraction(math.floor(dn * 10 ** 40), 10 ** 40) if dn.denominator > 10 ** 60 else dn
    k += J + 1; nep += 1
print(f"    epoch recursion against the closed form to level {k} ({nep} epochs; exact rationals, d rounded down to 40 digits when its denominator grows): "
      f"largest (h/d_m)/(c1/(k + c2)) = {float(worst):.4f} (must be <= 1); gain per level above kappa in every epoch")
print("ALL DONE")
