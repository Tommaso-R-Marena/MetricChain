"""R4: the scaled defect profile of the level recursion at positive accuracy (R_REPORT.md, section 8a).

Claim [P-sketch; N]:  k^2 (T_k(zeta h/k) - theta_hint(zeta h/k)) -> h^2 theta_hint''(0) f(zeta),
    f(zeta) = sup{ 2 z^2 + 2 zeta z cot z : z in (0, pi)  or  z = i y, y > 0 } - zeta^2/2
(for imaginary z: -2 y^2 + 2 zeta y coth y).  Printed: f on a list of zeta; the residual of the similarity equation
zeta f'^2/2 + zeta f' + (zeta - 2) f = 0 (finite differences); and, for the Gaussian pair and the cube, the envelope
of the minorant lines of Proposition A,  k^2 [sup_B (B - p_k(B) x) - theta_hint(x)]/(h^2 theta_hint''(0))  at
x = zeta h/k, computed from the exact orbit curves (a lower bound of the profile at every k).
Usage: python3 r4_profile.py
"""
import math
from rlib import Gauss, Cube


def f(zeta, n=20000):
    best = 2 * zeta                                   # z -> 0
    for i in range(1, n):
        z = math.pi * i / n
        best = max(best, 2 * (z * z + zeta * z / math.tan(z)))
        y = 30.0 * i / n
        best = max(best, 2 * (-y * y + zeta * y / math.tanh(y)))
    return best - zeta * zeta / 2


zetas = [0.0, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]
print("# closed form: f(0) = 2 pi^2 = %.6f;  f(3) = 3/2;  f'(2) = -2" % (2 * math.pi ** 2))
print("  zeta   f(zeta)     residual of  zeta f'^2/2 + zeta f' + (zeta - 2) f")
for z in zetas:
    if z > 0:
        d = 1e-3
        fp = (f(z + d, 60000) - f(z - d, 60000)) / (2 * d)
        res = z * fp * fp / 2 + z * fp + (z - 2) * f(z, 60000)
        print("  %5.2f  %.6f   %+.1e" % (z, f(z, 60000), res))
    else:
        print("  %5.2f  %.6f" % (z, f(z, 60000)))

for P in [Gauss().setup(), Cube(1.0).setup()]:
    h, L, vt = P.h, P.L, P.vartheta

    def theta_hint(x):
        # theta_hint(x) = max_t [J(t) - t x]  (concave dual), by a fine search around L
        lo, hi = 0.0, 1.0
        for _ in range(200):
            m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            if P.J(m1) - m1 * x < P.J(m2) - m2 * x:
                lo = m1
            else:
                hi = m2
        t = 0.5 * (lo + hi)
        return P.J(t) - t * x
    print("# %s: lower envelope of the lines of Proposition A, scaled; the last column is f" % P.name)
    print("  zeta " + "".join("  k = %-6d" % k for k in (20, 40, 80, 160)) + "   f(zeta)")
    for z in [0.25, 0.5, 1.0, 2.0, 3.0, 5.0]:
        row = []
        for k in (20, 40, 80, 160):
            x = z * h / k
            best = -1e9
            # intercepts B = h + delta, delta = c h^2 (2 vt)/k^2 with c = z'^2 in (-(8)^2, pi^2)
            for i in range(-600, 400):
                c = i / 400.0 * math.pi ** 2 if i >= 0 else -(i / 600.0 * 8.0) ** 2
                B = h + c * h * h * 2 * vt / (k * k)
                p = P.orbit(B, k)[-1]
                if math.isfinite(p):
                    best = max(best, B - p * x)
            row.append(k * k * (best - theta_hint(x)) / (h * h * vt))
        print("  %4.2f " % z + "".join("  %9.4f " % r for r in row) + "   %.4f" % f(z))
