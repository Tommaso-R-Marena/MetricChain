"""r10_08: Proposition D of Y_REPORT 4.2 (exact sub-/super-additivity and the sandwich) and
the block tables 6.1 (U) and 6.2 (L') of Y, with own code (all vertices of the weighted
block polytopes by spanning-tree enumeration, L <= 3).

Binary symmetric chain: free-boundary block law = stationary L-marginal;
  F+_L   = F*[pi_L; slopes (u+K, u, ..., u, u+K)]            (L=1: u+2K)
  F-_L,m = F*[pi_L; slopes (u-kappa_m, u, ..., u, u-kappa_m)]  (L=1: u-2 kappa_m),  kappa_m = ln[(1+lam^(m+1))/(1-lam^(m+1))]
  F_L    = F*[pi_L; slopes (u,...,u)]   (plain)
"""
import time
import numpy as np
from r10lib import *

u = 1.0
t0 = time.time()


def block_W(p, L, ends_extra):
    slopes = [u] * L
    slopes[0] += ends_extra
    slopes[-1] += ends_extra
    if min(slopes) <= 0:
        return None
    V = cube_vertices_weighted(slopes)
    W, _ = gibbs(binary_chain_law(L, p), V)
    return W


def Fstar(W, t):
    br = renyi_bracket(W, t, tol=1e-12)
    return 0.5 * (br["lower"] + br["upper"]), br["upper"] - br["lower"]


def exps(W, per):
    low = lambda t: renyi_bracket(W, t, tol=1e-11)["lower"]
    tb, _ = golden_max(low, 0.03, 0.97, tol=1e-6)
    br = renyi_bracket(W, tb, tol=1e-12)
    return br["upper"] / per, capacity_bracket(W, tol=1e-12)["upper"] / per, threshold_bracket(W, tol=1e-12)["upper"] / per, tb


print("=== Prop. D: F+ sub-additive, F- super-additive, F- <= F <= F+, (F+ - F-) <= t C, C = 2(u+K) ===")
for p in (0.4, 0.3):
    K = np.log((1 - p) / p)
    C = 2 * (u + K)
    Wp = {L: block_W(p, L, K) for L in (1, 2, 3)}
    Wm = {L: block_W(p, L, -K) for L in (1, 2, 3)}
    W0 = {L: block_W(p, L, 0.0) for L in (1, 2, 3)}
    for t in (0.3, 0.45, 0.7):
        Fp = {L: Fstar(Wp[L], t)[0] for L in (1, 2, 3)}
        F0 = {L: Fstar(W0[L], t)[0] for L in (1, 2, 3)}
        Fm = {L: (Fstar(Wm[L], t)[0] if Wm[L] is not None else None) for L in (1, 2, 3)}
        s = "p=%.1f t=%.2f: F+_2-2F+_1=%+.4f  F+_3-F+_1-F+_2=%+.4f |" % (p, t, Fp[2] - 2 * Fp[1], Fp[3] - Fp[1] - Fp[2])
        if Fm[1] is not None:
            s += " F-_2-2F-_1=%+.4f  F-_3-F-_1-F-_2=%+.4f |" % (Fm[2] - 2 * Fm[1], Fm[3] - Fm[1] - Fm[2])
        else:
            s += " (u <= 2K: F-_1 undefined at m=0) F-_2=%.4f F-_3=%.4f |" % (Fm[2], Fm[3])
        s += " order F-<=F<=F+: %s | (F+_3-F-_3)/(tC)=%.3f | per site: F-_3/3=%.5f F_3/3=%.5f F+_3/3=%.5f" % (
            all((Fm[L] is None or Fm[L] <= F0[L] + 1e-10) and F0[L] <= Fp[L] + 1e-10 for L in (1, 2, 3)),
            (Fp[3] - Fm[3]) / (t * C), Fm[3] / 3, F0[3] / 3, Fp[3] / 3)
        print(s)
print("   Y 4.2: F+_2-2F+_1 = -0.041...-0.114, F+_3-F+_1-F+_2 = -0.039...-0.115 (p=0.4,0.3); F-_2-2F-_1 = +0.019...+0.023, F-_3-F-_1-F-_2 = +0.027...+0.035, (F+_3-F-_3)/(tC) <= 0.096 (p=0.4)")

print("\n=== Y table 6.1: upper bounds from (U), L = 1,2,3 ===")
theirs = {0.4: ((0.08302, 0.05804, 0.04948), (0.28723, 0.19792, 0.17181), (0.36375, 0.26437, 0.23243)),
          0.3: ((0.15031, 0.09387, 0.07428), (0.45721, 0.28620, 0.23680), (0.71954, 0.47295, 0.39226)),
          0.2: ((0.22525, 0.13205, 0.10025), (0.58562, 0.35982, 0.29177), (1.21588, 0.76151, 0.61087)),
          0.1: ((0.31125, 0.17250, 0.12692), (0.66423, 0.41025, 0.32951), (2.00861, 1.20471, 0.93694))}
maxdev = 0.0
for p in (0.4, 0.3, 0.2, 0.1):
    K = np.log((1 - p) / p)
    row = []
    for L in (1, 2, 3):
        W = block_W(p, L, K)
        h_, a_, e_, tb = exps(W, L)
        row.append((h_, a_, e_, W.shape[0]))
        maxdev = max(maxdev, abs(h_ - theirs[p][0][L - 1]), abs(a_ - theirs[p][1][L - 1]), abs(e_ - theirs[p][2][L - 1]))
    print("p=%.1f  h<= %s   a<= %s   E<= %s   |V| = %s" % (p, " ".join("%.5f" % r[0] for r in row), " ".join("%.5f" % r[1] for r in row),
                                                       " ".join("%.5f" % r[2] for r in row), [r[3] for r in row]))
print("   largest deviation from Y's 36 entries: %.1e" % maxdev)

print("\n=== Y table 6.2: lower bounds from (L'), best gap m <= 5 ===")
theirs_L = {0.4: ((0.01049, 1), (0.01891, 1), (0.02307, 1), 0.07987, 0.10199),
            0.3: ((0.00595, 3), (0.01465, 2), (0.02088, 2), 0.06978, 0.09375),
            0.2: ((0.00329, 5), (0.01031, 4), (0.01742, 3), 0.05681, 0.07830),
            0.1: ((None, None), (0.00327, 5), (0.01020, 5), 0.03518, 0.04459)}
for p in (0.4, 0.3, 0.2, 0.1):
    lam = 1 - 2 * p
    out = []
    for L in (1, 2, 3):
        best = (0.0, None, 0.0, 0.0)
        for m in range(0, 6):
            kap = np.log((1 + lam ** (m + 1)) / (1 - lam ** (m + 1)))
            W = block_W(p, L, -kap)
            if W is None:
                continue
            h_, a_, e_, tb = exps(W, L + m)
            if h_ > best[0]:
                best = (h_, m, best[2], best[3])
            best = (best[0], best[1], max(best[2], a_), max(best[3], e_))
        out.append(best)
    print("p=%.1f  h>= %s   a>= (L=3) %.5f   E>= (L=3) %.5f     Y: %s  a>= %.5f  E>= %.5f" % (
        p, "  ".join(("%.5f (m=%s)" % (b[0], b[1])) if b[1] is not None else "-" for b in out), out[2][2], out[2][3],
        "  ".join(("%.5f (%d)" % x) if x[0] is not None else "-" for x in theirs_L[p][:3]), theirs_L[p][3], theirs_L[p][4]))
print("time %.1fs" % (time.time() - t0))
