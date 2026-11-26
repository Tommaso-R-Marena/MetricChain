#!/usr/bin/env python3
"""RA03 -- Corollary A4 (comparison), Proposition A6 (the fixed-rate sequence), Proposition A7 (the cut chain).

 (a) the fixed-rate sequence of A6 in closed form: V_j(B) = v_j (B/h - 1)_+ (a hinge: the positive part always acts at
     B = h), v_{j+1} = (v_j + 1)/G_j, c_{j+1} = min(c_j, (1 + v_j)/(v_j/h + 1/a)), G_j = max(1, c_{j+1}(1/h - 1/a)).
     Checks: admissibility ((S1), (S2), values in [0, 1]) on grids; c_j reaches c* = ah/(a-h) after finitely many
     steps; the bound c_{j0+i+1} - h <= h(1 - h/a)/(i + h/a); comparison with the envelope sequence: b_j <= c_j, W_j >= V_j.
 (b) the cut orbit curves of R_REPORT section 6 from b_0 = h + eps1 (the referee's own implementation): the range
     condition, admissibility, and the comparison of A7: b_{k1+i} <= bcut_i, W_{k1+i} >= Wcut_i on [0, b_{k1+i}].
 (c) random admissible sequences (a random factor < 1 and a random horizontal stretch of the envelope of the image,
     tops between b+ and the previous top) against the envelope sequence, on grids.
Usage: python3 -B ra03_comparison.py [pair]       pair in {cube1, cube2, gauss}; default cube1
"""
import math
import random
import sys

import numpy as np

import ra_lib as R

which = sys.argv[1] if len(sys.argv) > 1 else "cube1"
P = (R.Gauss() if which == "gauss" else R.Cube(float(which[4:]))).setup()
a, h, L, c2 = P.a, P.h, P.L, P.cstar2
random.seed(2026)
print("# %s: a = %.8f, h = %.8f, L = %.6f, c_*^2 = %.8f" % (P.name, a, h, L, c2))
JE = 140
S = R.EnvSeq(P, JE)

# ---------------------------------------------------------------------------------------------------------------
print("\n== (a) the fixed-rate sequence ==")
cstar = a * h / (a - h)
v, c, G = [0.0], [a], []
for j in range(JE):
    root = (1.0 + v[j]) / (v[j] / h + 1.0 / a)
    cn = min(c[j], root)
    Gj = max(1.0, cn * (1.0 / h - 1.0 / a))
    G.append(Gj)
    c.append(cn)
    v.append((v[j] + 1.0) / Gj)
j0 = next(j for j in range(JE + 1) if c[j] <= cstar)
print("c* = ah/(a-h) = %.6f = %.4f a;  first j0 with c_j <= c*: %d   (c_j/a for j = 0..8: %s)"
      % (cstar, cstar / a, j0, " ".join("%.4f" % (x / a) for x in c[:9])))
print("G_j for j = 0..6: %s" % " ".join("%.4f" % x for x in G[:7]))
worstS2, worstTop, worstBound, worst_cmp_b, worst_cmp_W = -math.inf, -math.inf, -math.inf, -math.inf, -math.inf
for j in range(JE):
    xs = np.linspace(0.0, c[j + 1], 1501)
    Vj = v[j] * np.maximum(xs / h - 1.0, 0.0)
    Vn = v[j + 1] * np.maximum(xs / h - 1.0, 0.0)
    img = P.sigma_vec(xs, Vj)                      # +inf where not regular
    worstS2 = max(worstS2, float(np.max(Vn - img)))
    worstTop = max(worstTop, float(Vn[-1]) - 1.0)
    # (S1): Sigma(B, V_j(B)) = infinity beyond c_{j+1}
    if c[j + 1] < c[j]:
        Bx = c[j + 1] + 1e-9 * a
        assert not P.regular(Bx, v[j] * max(Bx / h - 1.0, 0.0))
    if j + 1 > j0:
        i = j - j0
        worstBound = max(worstBound, (c[j + 1] - h) - h * (1 - h / a) / (i + h / a))
    worst_cmp_b = max(worst_cmp_b, S.b[j + 1] - c[j + 1])
    if j + 1 <= 60:
        xb = np.linspace(0.0, S.b[j + 1], 801)
        worst_cmp_W = max(worst_cmp_W, float(np.max(v[j + 1] * np.maximum(xb / h - 1.0, 0.0) - S.Wvec(j + 1, xb))))
print("(S2)  max of V_{j+1} - Sigma(., V_j) on [0, c_{j+1}], all j < %d: %.3e   (must be <= 0)" % (JE, worstS2))
print("values in [0,1]: max of V_{j+1}(c_{j+1}) - 1: %.3e   (must be <= 0)" % worstTop)
print("the bound of A6: max over i >= 0 of (c_{j0+i+1} - h) - h(1 - h/a)/(i + h/a): %.3e   (must be <= 0)" % worstBound)
print("comparison (Corollary A4): max of b_j - c_j: %.3e (must be <= 0);  max of V_j - W_j on [0, b_j], j <= 60: %.3e (must be <= 0)"
      % (worst_cmp_b, worst_cmp_W))
print("   j     b_j/a      c_j/a     (c_j - h)·j/h    (b_j - h) j^2/c_*^2")
for j in (1, 2, 3, 4, 5, 6, 8, 10, 20, 40, 80, 140):
    print("  %3d   %.5f   %.5f    %8.4f        %8.4f" % (j, S.b[j] / a, c[j] / a, (c[j] - h) * j / h, (S.b[j] - h) * j * j / c2))

# ---------------------------------------------------------------------------------------------------------------
print("\n== (b) the cut orbit curves (R_REPORT section 6) and Proposition A7 ==")


def cut_chain(dst, eps1, JC):
    st, b0 = L + dst, h + eps1
    assert st < 1 - h / a and b0 < (1 - st) * a
    cuts, b, rng = [], [b0], 0.0
    for j in range(JC + 1):
        if P.orbit_with_slope(b0, j)[0] <= st:
            cuts.append(None)                       # case A
        else:
            lo, hi = h, b0
            for _ in range(100):
                mid = 0.5 * (lo + hi)
                if P.orbit_with_slope(mid, j)[0] <= st:
                    lo = mid
                else:
                    hi = mid
            cuts.append((lo, P.orbit_with_slope(lo, j)[1]))
    def W(j, B):
        cj = cuts[j]
        if cj is None or B <= cj[0]:
            return P.orbit_with_slope(B, j)[0]
        return st + cj[1] * (B - cj[0])
    for j in range(JC):
        cj = cuts[j]
        bn = b[j] if cj is None else min(b[j], cj[0] + (1 - st - cj[0] / a) / (cj[1] + 1 / a))
        b.append(bn)
        rng = max(rng, W(j + 1, bn))
    return st, b0, cuts, b, W, rng


for dst, eps1 in ((0.05, 0.003 if which != "gauss" else 0.02), (0.05, 0.001 if which != "gauss" else 0.005)):
    JC = 60
    st, b0, cuts, bc, Wc, rng = cut_chain(dst, eps1, JC)
    k1 = next(k for k in range(JE + 1) if S.b[k] <= b0)
    firstB = next(j for j in range(JC + 1) if cuts[j] is not None)
    print("s_t = L + %.3g, b_0 = h + %.4g:  range condition: max W_{j+1}(b_{j+1}) = %.4f (<= 1: %s);  first level in case B: %d;  k_1 = %d (b_{k1} = h + %.5f)"
          % (dst, eps1, rng, rng <= 1.0, firstB, k1, S.b[k1] - h))
    worst_b, worst_W, worst_S2 = -math.inf, -math.inf, -math.inf
    for i in range(0, min(JC, JE - k1) + 1):
        worst_b = max(worst_b, S.b[k1 + i] - bc[i])
        xs = np.linspace(0.0, S.b[k1 + i], 201)
        We = S.Wvec(k1 + i, xs)
        Wcut = np.array([Wc(i, x) for x in xs])
        worst_W = max(worst_W, float(np.max(Wcut - We)))
        if i < JC:                                    # (S2) for the cut curves on [0, bcut_{i+1}]
            xs2 = np.linspace(0.0, bc[i + 1], 201)
            Wi = np.array([Wc(i, x) for x in xs2])
            Wn = np.array([Wc(i + 1, x) for x in xs2])
            worst_S2 = max(worst_S2, float(np.max(Wn - P.sigma_vec(xs2, Wi))))
    print("   (S2) for the cut curves: max of Wcut_{i+1} - Sigma(., Wcut_i): %.3e (must be <= 0 up to rounding)" % worst_S2)
    print("   comparison: max of b_{k1+i} - bcut_i: %.3e (must be <= 0);   max of Wcut_i - W_{k1+i} on [0, b_{k1+i}]: %.3e (must be <= 0)"
          % (worst_b, worst_W))
    print("     i    bcut_i - h      b_{k1+i} - h     ratio      i^2 (bcut_i - h)/c_*^2    (k1+i)^2 (b_{k1+i} - h)/c_*^2")
    for i in (0, 1, 2, 5, 10, 20, 40, 60):
        if k1 + i <= JE:
            print("   %3d   %.6e   %.6e   %.4f        %8.4f                  %8.4f"
                  % (i, bc[i] - h, S.b[k1 + i] - h, (S.b[k1 + i] - h) / (bc[i] - h), i * i * (bc[i] - h) / c2, (k1 + i) ** 2 * (S.b[k1 + i] - h) / c2))

# ---------------------------------------------------------------------------------------------------------------
print("\n== (c) random admissible sequences against the envelope sequence (grids of 3000 points, 12 levels, 40 sequences) ==")
NG = 3000


def grid_env_step(x, W, b):
    """(x', env, b+) for the family (W on the grid x of [0, b])"""
    g = W - (1.0 - x / a)
    if g[-1] < 0:
        bp = b
    else:
        k = int(np.argmax(g >= 0))
        bp = x[0] if k == 0 else x[k - 1] - g[k - 1] * (x[k] - x[k - 1]) / (g[k] - g[k - 1])
    xn = bp * (1.0 - (1.0 - np.linspace(0.0, 1.0, NG + 1)) ** 2)
    f = np.minimum(1.0, P.sigma_vec(xn, np.interp(xn, x, W)))
    f[0] = 0.0
    if g[-1] >= 0:
        f[-1] = 1.0
    e, _ = R.lower_env(xn, f)
    return xn, e, bp


G0 = R.GridEnv(P, 12, NG, "quad")
viol_b, viol_W, viol_S1 = -math.inf, -math.inf, -math.inf
for trial in range(40):
    b0 = a * random.uniform(0.35, 1.0)
    x = np.linspace(0.0, b0, NG + 1)
    V = np.zeros(NG + 1)
    cj = b0
    # the envelope sequence from the same start
    xe, We, be = x.copy(), V.copy(), b0
    for j in range(12):
        xn, e, bp = grid_env_step(x, V, cj)
        lam = random.uniform(0.3, 1.0)
        cn = bp + random.uniform(0.0, 1.0) * (cj - bp) * random.choice([0.0, 1.0])
        # V_{j+1}(B) = lam * env(B * bp/cn) on [0, cn]:  convex, nondecreasing, <= env <= image on [0, bp]; free beyond
        xv = np.linspace(0.0, cn, NG + 1)
        Vn = lam * np.interp(xv * bp / cn, xn, e)
        x, V, cj = xv, Vn, cn
        xe, We, be = grid_env_step(xe, We, be)
        viol_b = max(viol_b, (be - cj) / a)
        viol_W = max(viol_W, float(np.max(np.interp(xe, x, V) - We)))
print("max of (b_j - c_j)/a: %.3e (must be <= 0 up to the grid);   max of V_j - W_j on [0, b_j]: %.3e (must be <= 0 up to the grid)"
      % (viol_b, viol_W))
