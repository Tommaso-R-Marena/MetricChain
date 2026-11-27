#!/usr/bin/env python3
"""R12 — small arithmetic quoted in R12_REPORT (review of the theory report at 9408e33); no simulation.
One command:  python3 r12_10_arithmetic.py
"""
import math


def L(w):
    return math.log((math.exp(w) - 1) / w) - 1 + w / (math.exp(w) - 1)


def W(b, s2):
    return math.log((b * b * math.exp(-s2 / b) + s2 * math.exp(b)) / (b * b + s2))


print("1. Theorem 11.110(a), (f): L(3.7) = %.4f (report: 1.46);  W(3.7, 0.036^2) = %.3e (report: 3.4e-3);  "
      "(sigma^2/b^2)(e^b - 1 - b) = %.3e" % (L(3.7), W(3.7, 0.036 ** 2),
                                           0.036 ** 2 / 3.7 ** 2 * (math.exp(3.7) - 1 - 3.7)))
print("   L(w) <= w^2/8 at w = 0.5, 1, 2, 3.7: %s" % [(round(L(w), 5), round(w * w / 8, 5)) for w in (0.5, 1, 2, 3.7)])

print("2. Theorem 11.110(c): ln(20) (e^3 - 1)/(e^0.1 - 1) = %.2f -> %d;  twice: %d;  rule without a hint N(0) = %d" % (
    math.log(20) * (math.exp(3) - 1) / (math.exp(0.1) - 1),
    math.ceil(math.log(20) * (math.exp(3) - 1) / (math.exp(0.1) - 1)),
    math.ceil(2 * math.log(20) * (math.exp(3) - 1) / (math.exp(0.1) - 1)),
    math.ceil(math.log(20) / min((math.exp(0.1) - 1) / (math.exp(3) - 1), 1 - math.exp(-0.1))) + 1))

print("3. Corollary 11.111: e^{0.0291 n} = 1088 at n = %.1f; = 544 at n = %.1f (report: 'from n ~ 240')" % (
    math.log(1088) / 0.0291, math.log(544) / 0.0291))

print("4. XXIV.7, 'attained to 0.3 % at u = 0.05': D_p/n = [ln cosh(pu/2) - p ln cosh(u/2)]/(p - 1) against (p-1)u^2/8 + L(u)")
u = 0.05
for p in (1.5, 2.0, 4.0):
    dp = (math.log(math.cosh(p * u / 2)) - p * math.log(math.cosh(u / 2))) / (p - 1)
    sharp = (p - 1) * u * u / 8 + L(u)
    print("   p = %-4g ratio %.6f, deficit %.3f %%" % (p, dp / sharp, 100 * (1 - dp / sharp)))

print("5. Our twenty-residue sandwich (SCI-MSG-0020: Delta = 0.0605 nats), arithmetic only, delta = 0.05:")
D = 0.0605
a_max, b_max = math.exp(D) - 1, 1 - math.exp(-D)
eps = 0.005            # (eps/2, delta)-correct with eps/2 = 0.0025: a bracket of width 5e-3
print("   cost numbers: Z(m-)/Z(E) - 1 <= %.5f, 1 - Z(m+)/Z(E) <= %.5f" % (a_max, b_max))
print("   hinted spot check at E = m+ (worst for dips), bracket width 5e-3: N = ceil(ln 20 * 2 a/(e^{eps/2} - 1)) = %d;"
      " with the one-sided sampler (bumps vanish there): %d" % (
          math.ceil(math.log(20) * 2 * a_max / (math.exp(eps / 2) - 1)),
          math.ceil(math.log(20) * a_max / (math.exp(eps / 2) - 1))))
print("   lower bound there: (1 - 2 delta) floor(a/(2(e^eps - 1))) = 0.9 * %d = %.1f" % (
    math.floor(a_max / (2 * (math.exp(eps) - 1))), 0.9 * math.floor(a_max / (2 * (math.exp(eps) - 1)))))
print("   Proposition 11.113(c): width <= (e^Delta - 1) sqrt(2 ln 40 / N): N = 50000: %.3e;  N = 1200: %.3e" % (
    a_max * math.sqrt(2 * math.log(40) / 50000), a_max * math.sqrt(2 * math.log(40) / 1200)))
print("   ball of radius 4 on 20 sites with 3 states: sum_{j<5} C(20,j) 2^j = %d (SCI-MSG-0020: 87 441)" % sum(
    math.comb(20, j) * 2 ** j for j in range(5)))

print("6. Corollary 11.114, example of (3): e^8 - 1 = %.2f;  1e-6 (e^8 - 1) + (1 - 1e-6)(e^0.1 - 1) = %.5f" % (
    math.exp(8) - 1, 1e-6 * (math.exp(8) - 1) + (1 - 1e-6) * (math.exp(0.1) - 1)))
print("R12_10_DONE")
