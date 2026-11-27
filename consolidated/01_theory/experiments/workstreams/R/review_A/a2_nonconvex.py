"""Referee A, test 2: non-convex W.  T = M_{W,b} for a nondecreasing NON-convex W : [0, b] -> [0, 1].

  U_W    = sup_B (B - Sigma(B, W(B)) g)        the "line-by-line" value (what Proposition U would give if convexity
                                                were not needed)
  U_hull = the same with the lower convex envelope W** of W          (M_{W,b} = M_{W**,b}; Proposition U applies)
  Llow   = sup_B (B - max(W**(B), Sigma(B, W**(B))) g)               (Lemma L: a rigorous LOWER bound of R[T](g))
  R_bf   = brute force on R (min over a (phi, beta) grid of the brute-force sup over gamma): an UPPER estimate.
Expected: U_W < Llow <= R[T] <= U_hull (so the line-by-line value is NOT an upper bound), R_bf ~ U_hull.
"""
import math, sys
import numpy as np
import a1_propU_lib as L
from ralib import Gauss, Cube, Expo, Envelope, R_bruteforce


def lower_hull(x, y):
    """lower convex envelope of the points (x_i, y_i), x increasing; returns the hull vertices."""
    hx, hy = [], []
    for xi, yi in zip(x, y):
        while len(hx) >= 2 and (hy[-1] - hy[-2]) * (xi - hx[-2]) >= (yi - hy[-2]) * (hx[-1] - hx[-2]):
            hx.pop(); hy.pop()
        hx.append(xi); hy.append(yi)
    return np.array(hx), np.array(hy)


def run(th, name, b, Wfun, gs):
    xs = np.linspace(0, b, 801)
    W = np.clip(Wfun(xs), 0, 1)
    hx, hy = lower_hull(xs, W)
    T = Envelope(xs, W)
    # check M_W = M_{W**}
    xx = 10 ** np.linspace(-6, 2, 500)
    dM = float(np.max(np.abs(T(xx) - Envelope(hx, hy)(xx))))
    print("%s ; W = %s on [0, %.4f]  (max |M_W - M_W**| = %.1e; hull has %d vertices)" % (th.name, name, b, dM, len(hx)))
    for g in gs:
        UW = L.U_and_Llow(th, xs, W, g, nB=1200)[0]
        Uh, Ll = L.U_and_Llow(th, hx, hy, g, nB=1200)[:2]
        Rb = R_bruteforce(th, T, g, nphi=140, nbeta=20, ngam=160)
        print("   g = %.5f : U_W = %.6f   Llow = %.6f   R_bf = %.6f   U_hull = %.6f    (Llow - U_W)/a = %+.4f   (R_bf - U_hull)/a = %+.1e"
              % (g, UW, Ll, Rb, Uh, (Ll - UW) / th.a, (Rb - Uh) / th.a))
        sys.stdout.flush()


G = Gauss()
run(G, "0.8 sqrt(B/b)  (concave)", 0.45, lambda B: 0.8 * np.sqrt(B / 0.45), [0.002, 0.01, 0.05, 0.15])
# the instance behind harness XVI.7: T_2 <= M_W with W = min(1, Sigma(B, B)) = min(1, B(1-B)/(1-2B)) on [0, 1/2]
run(G, "min(1, B(1-B)/(1-2B))  (XVI.7)", 0.5, lambda B: np.minimum(1.0, B * (1 - B) / np.maximum(1 - 2 * B, 1e-300)), [0.0005, 0.002, 0.01, 0.05])
run(G, "smooth step 0.9/(1+exp(-(B-0.2)/0.02))", 0.4, lambda B: 0.9 / (1 + np.exp(-(B - 0.2) / 0.02)) - 0.9 / (1 + np.exp(10.0)), [0.002, 0.01, 0.05])
C = Cube(1.0)
run(C, "0.7 sqrt(B/b)  (concave)", 0.06, lambda B: 0.7 * np.sqrt(B / 0.06), [0.0005, 0.003, 0.01])
E = Expo(1.0, 0.25, 0.08)
run(E, "0.9 (B/b)^(1/3)", 0.5, lambda B: 0.9 * (B / 0.5) ** (1 / 3), [0.003, 0.02, 0.1])
