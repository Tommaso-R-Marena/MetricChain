"""Referee A, test 6: Proposition C end to end.  Gaussian pair.  The recursion itself on a fine grid (the code of
a4b_recursion_fine.py) for levels 1..K, a restart at the level k1 where tau_{k1} <= b_0 = h + eps1, and the chain
of section 6:  T_{k1 + j} <= M_{W_j, b_j}  pointwise in the accuracy g, with W_j the cut orbit curves (s_t = L + dst).
Usage: python3 a6_chain_vs_recursion.py [K] [dst] [eps1] [NU]
"""
import sys, math, time
import numpy as np

K = int(sys.argv[1]) if len(sys.argv) > 1 else 16
dst = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
eps1 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02
NU = sys.argv[4] if len(sys.argv) > 4 else "321"
argv_saved = sys.argv
sys.argv = ["a4b", str(K), "nocheck", NU]
src = open("a4b_recursion_fine.py").read()
ns = {}
exec(compile(src[:src.index("vals = G(gs)\nprint(")], "a4b_defs", "exec"), ns)
G, gs, PLT, R_fine, dd, majorant = ns["G"], ns["gs"], ns["PLT"], ns["R_fine"], ns["dd"], ns["majorant"]
h, L, a = 0.25, 0.5, 1.0
s_t, b0 = L + dst, h + eps1
GR = (math.sqrt(5) - 1) / 2


def orbit(B, n):
    """p_n(B), p_n'(B) for the Gaussian pair (Moebius map with its partial derivatives)."""
    p, dp = 0.0, 0.0
    for _ in range(n):
        d = 1 - p - B
        if d <= 0:
            return math.inf, math.inf
        y = 1 - p
        p, dp = B * y / d, y * y / (d * d) + B * B / (d * d) * dp
    return p, dp


# the recursion
t0 = time.time()
Tk = {1: G(gs)}
vals = G(gs)
for k in range(2, K + 1):
    T = PLT(vals)
    new = np.array([min(T.v[i], R_fine(T, float(g))) for i, g in enumerate(gs[:-1])] + [0.0])
    vals = np.minimum.accumulate(new)
    Tk[k] = vals.copy()
print("# recursion: %d levels on %d accuracies, %.0f s ; sup T_k (value at g = 1e-8): " % (K, len(gs), time.time() - t0)
      + " ".join("%d:%.5f" % (k, Tk[k][0]) for k in range(1, K + 1)))
# restart level: the first k with T_k(1e-8) + margin <= b0 (the grid value at 1e-8 is below sup T_k by O(sqrt(1e-8)); margin 3e-4)
k1 = min(k for k in range(1, K + 1) if Tk[k][0] + 3e-4 <= b0)
print("# s_t = %.4f, b_0 = %.4f ; restart level k1 = %d (T_{k1}(1e-8) = %.6f)" % (s_t, b0, k1, Tk[k1][0]))

# the chain
Bt, m = {}, {}
for j in range(0, K - k1 + 2):
    if orbit(b0, j)[0] <= s_t:
        continue
    lo, hi = h, b0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if orbit(mid, j)[0] <= s_t:
            lo = mid
        else:
            hi = mid
    Bt[j] = lo; m[j] = orbit(lo, j)[1]


def W(j, B):
    if j not in Bt or B <= Bt[j]:
        return orbit(B, j)[0]
    return s_t + m[j] * (B - Bt[j])


b = b0
print("#  j  level  case  b_j        W_j(b_j)   max_g (T_{k1+j} - M_{W_j,b_j})   at g      min_g (M - T)    [M at g=1e-8, T at g=1e-8]")
for j in range(0, K - k1 + 1):
    # majorant M_{W_j, b_j}(x) = max_{0<=B<=b_j} (B - W_j(B) x): grid + golden (concave in B)
    Bs = np.unique(np.concatenate([np.linspace(0, b, 1501), b - b * 10.0 ** np.linspace(-9, -1, 200)]))
    Wv = np.array([W(j, float(B)) for B in Bs])
    Mv = np.empty(len(gs))
    for q, xx in enumerate(gs):
        v = Bs - Wv * xx
        i = int(np.argmax(v))
        lo, hi = Bs[max(i - 1, 0)], Bs[min(i + 1, len(Bs) - 1)]
        f = lambda B: B - W(j, B) * xx
        x1, x2 = hi - GR * (hi - lo), lo + GR * (hi - lo)
        f1, f2 = f(x1), f(x2)
        for _ in range(40):
            if f1 >= f2:
                hi, x2, f2 = x2, x1, f1
                x1 = hi - GR * (hi - lo); f1 = f(x1)
            else:
                lo, x1, f1 = x1, x2, f2
                x2 = lo + GR * (hi - lo); f2 = f(x2)
        Mv[q] = max(float(v[i]), f1, f2)
    d = Tk[k1 + j] - Mv
    i = int(np.argmax(d))
    print("  %2d  %3d    %s    %.6f   %.6f   %+.3e                    %.3g    %+.3e   [%.6f, %.6f]"
          % (j, k1 + j, "B" if j in Bt else "A", b, W(j, b), d[i], gs[i], float(np.min(-d)), Mv[0], Tk[k1 + j][0]))
    # next b
    if j in Bt:
        E = Bt[j] + (1 - s_t - Bt[j] / a) / (m[j] + 1 / a)
        b = min(b, E)
