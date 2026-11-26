"""R3: exact lower bounds for the Gaussian pair at finite k, in rational arithmetic (no rounding anywhere).

Proposition A of R_REPORT.md (machine-checked iteration: LineDynamics.lines_le_exactRec, gauss_slope_map): tau_k >= B
whenever the orbit p_0 = 0, p_{j+1} = B (1 - p_j)/(1 - p_j - B) satisfies p_j + B < 1 for j = 0, ..., k - 1.
For each k the largest B = N/10^9 with this property is found by bisection on the integer N (the condition is
monotone in B); the orbit is computed with Python fractions.  Printed: B_k, and the exact rational lower bound of
k^2 (tau_k - 1/4) compared with pi^2/16 = 0.6168502750680849 (decimal comparison only in the last column).
Usage: python3 r3_gauss_exact_lb.py
"""
from fractions import Fraction
import math

D = 10 ** 9


def regular(B, k):
    p = Fraction(0)
    for _ in range(k):
        if not p + B < 1:
            return False
        p = B * (1 - p) / (1 - p - B)
    return True


print("#    k   B_k = N/10^9 (tau_k >= B_k, exact)    k^2 (B_k - 1/4)    ratio to pi^2/16   (k + 1/2)^2 (B_k - 1/4)/(pi^2/16)")
for k in [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 60, 80, 120, 160]:
    lo, hi = D // 4, D            # B = 1/4 is always regular (the orbit converges to 1/2 < 3/4)
    assert regular(Fraction(lo, D), k)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if regular(Fraction(mid, D), k):
            lo = mid
        else:
            hi = mid
    B = Fraction(lo, D)
    c = math.pi ** 2 / 16
    print("  %4d   %d/10^9 = %.9f              %.8f          %.6f           %.6f" % (
        k, lo, float(B), float(k * k * (B - Fraction(1, 4))), float(k * k * (B - Fraction(1, 4))) / c,
        float((2 * k + 1) ** 2 * (B - Fraction(1, 4)) / 4) / c))
