"""Referee B, check 12 (outside Theorem R; shows what (H1) excludes): different curvatures of theta on the two sides of h.
theta = (1 - sqrt e)^2 for e <= 1/4 (theta''(h-) = 4);  theta = 1/4 - x + 4 x^2, x = e - 1/4, for 0 <= x <= 1/8 (theta''(h+) = 8),
constant 3/16 beyond.  Then J(L + q) ~ h - q^2/(2 vartheta_side) with vartheta = 1/2 for q > 0 (e < h) and 1 for q < 0, and the
argument of Lemma PT gives  sqrt(delta) N_t -> (pi h/2)(sqrt(2 * 1/2) + sqrt(2 * 1)) = (pi/8)(1 + sqrt 2)."""
import math
import blib


def th(e):
    if e <= 0.25:
        return (1 - math.sqrt(e)) ** 2
    x = min(e - 0.25, 0.125)
    return 0.25 - x + 4 * x * x


def dth(e):
    if e < 0.25:
        return -(1 - math.sqrt(e)) / math.sqrt(e)
    x = e - 0.25
    return -1 + 8 * x if x < 0.125 else 0.0


P = blib.TPair("two-sided curvature 4 | 8", th, dth, 1.0)
pred = math.pi / 8 * (1 + math.sqrt(2))
print("h = %.12f; one-sided vartheta = q^2/(2 (h - J(L + q))) at q = +1e-3: %.4f, at q = -1e-3: %.4f" % (
    P.fixed_point(), 1e-6 / (2 * (0.25 - P.J_direct(0.5 + 1e-3))), 1e-6 / (2 * (0.25 - P.J_direct(0.5 - 1e-3)))))
print("sqrt(delta) N_t(delta), s_t = 0.6:  " + "  ".join("%.0e: %.5f" % (d, math.sqrt(d) * P.passage(0.25 + d, 0.6)) for d in [1e-4, 1e-6, 1e-8, 1e-10]))
print("prediction (pi/8)(1 + sqrt 2) = %.5f;   pi h sqrt(2 vartheta) with vartheta = 1/2: %.5f, with vartheta = 1: %.5f" % (pred, math.pi / 4, math.pi / 4 * math.sqrt(2)))
