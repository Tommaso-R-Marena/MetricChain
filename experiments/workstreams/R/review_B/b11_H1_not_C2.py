"""Referee B, check 11: (H1) without theta in C^2.   theta(e) = (1 - sqrt e)^2 + c P(e - 1/4),
P(x) = x^4 sin^2(1/x) psi(x),  psi(x) = (1 - (x/0.2)^2)^3 on |x| < 0.2 (0 outside),  c = 0.3.
theta is convex and decreasing (checked on a grid below), theta(1/4) = 1/4, theta'(1/4) = -1, and the perturbation is
O(x^4), so J(t) = t - t^2 + O((t - 1/2)^4): (H1) holds with vartheta = 1/2 (as for the Gaussian pair), although
theta''(1/4 + x) = 4 + 0.6 cos(2/x) + O(x) has no limit as x -> 0.  Prediction of (Sigma6)/Lemma PT: the same
c_* = pi/4 as for the Gaussian pair."""
import math
import blib

c = 0.3


def P(x):
    if x == 0.0 or abs(x) >= 0.2:
        return 0.0
    return x ** 4 * math.sin(1 / x) ** 2 * (1 - 25 * x * x) ** 3


def dP(x):
    if x == 0.0 or abs(x) >= 0.2:
        return 0.0
    psi = (1 - 25 * x * x) ** 3
    dpsi = -150 * x * (1 - 25 * x * x) ** 2
    return (4 * x ** 3 * math.sin(1 / x) ** 2 - x * x * math.sin(2 / x)) * psi + x ** 4 * math.sin(1 / x) ** 2 * dpsi


th = lambda e: ((1 - math.sqrt(e)) ** 2 if e < 1 else 0.0) + c * P(e - 0.25)
dth = lambda e: (-(1 - math.sqrt(e)) / math.sqrt(e) if e < 1 else 0.0) + c * dP(e - 0.25)
# convexity and monotonicity on a fine grid (the oscillation has wavelength ~ pi x^2: use a grid refined at 1/4)
worst_conv, worst_mono = 0.0, -1e9
prev = None
pts = sorted(set([0.05 + 0.4 * i / 400000 for i in range(400001)] + [0.25 + s * 10 ** (-j / 2000.0) for j in range(1400, 24001) for s in (-1, 1)]))
for e in pts:
    d = dth(e)
    worst_mono = max(worst_mono, d)
    if prev is not None:
        worst_conv = max(worst_conv, prev - d)
    prev = d
print("theta' nondecreasing on %d points of [0.05, 0.45]: largest decrease %.2e;  largest theta' = %.3e (must be <= 0)" % (len(pts), worst_conv, worst_mono))
d = 1e-7
print("second derivative (difference quotient of theta') at 1/4 + x:  " + "  ".join("x=%.0e: %.3f" % (x, (dth(0.25 + x + d * x) - dth(0.25 + x - d * x)) / (2 * d * x)) for x in [1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3.3e-5]))
Pr = blib.TPair("Gaussian + 0.3 x^4 sin^2(1/x)", th, dth, 1.0)
Pr.h, Pr.L, Pr.vartheta = 0.25, 0.5, 0.5
Pr.cstar = math.pi / 4
print("h (fixed point) = %.12f;  Sigma(h, L) - L = %.2e" % (Pr.fixed_point(), Pr.sigma(0.25, 0.5) - 0.5))
print("(Sigma6) ratio D h/(delta + v^2/(2 vartheta)):")
vs = [-0.03, -0.01, -0.003, -0.001, -0.0003, 0.0, 0.0003, 0.001, 0.003, 0.01, 0.03]
print("   v =          " + " ".join("%+8.4f" % v for v in vs))
for dl in [1e-4, 1e-6, 1e-8, 1e-10]:
    print("   delta=%.0e " % dl + " ".join("%8.5f" % ((Pr.sigma(0.25 + dl, 0.5 + v) - 0.5 - v) * 0.25 / (dl + v * v)) for v in vs))
print("Lemma PT: sqrt(delta) N_t / (pi/4), s_t = 0.6:  " + "  ".join("%.0e: %.5f" % (dl, math.sqrt(dl) * Pr.passage(0.25 + dl, 0.6) / (math.pi / 4)) for dl in [1e-4, 1e-6, 1e-8, 1e-10]))
G = blib.gauss()
print("   (Gaussian pair, same deltas:                  " + "  ".join("%.0e: %.5f" % (dl, math.sqrt(dl) * G.passage(0.25 + dl, 0.6) / (math.pi / 4)) for dl in [1e-4, 1e-6, 1e-8, 1e-10]) + ")")
