"""Referee A, test 5: sections 6 and 8 (Lemma T, Proposition C, Lemma RC, the chain) for pairs other than the two of
the report, with own code (theta given directly; slope map through the tangency condition, cross-checked against
direct maximisation).

For s_t = L + dst and b_0 = h + eps1:
  (C1), (C2) of Lemma RC;
  for every level j <= J: case A/B, B_t(j) (bisection), m_j = p_j'(B_t(j)) (chain rule), E_j, b_{j+1} = min(b_j, E_j),
  the range condition W_{j+1}(b_{j+1}) <= 1, the ratio m_{j+1}/m_j against the bound 1/(e_1 m_j) + theta(e_1)/e_1;
  on a B-grid of [0, b_0], for the levels in a list:
     Lemma T(b):  W_{j+1}(B) <= Sigma(B, W_j(B))        (reported: max of W_{j+1} - H_j over the grid, where H_j is finite)
     convexity of p_j (second differences on a uniform grid of the range where p_j <= s_t) and of W_j;
  j^2 (b_j - h)/const.
Usage: python3 a5_chain.py pair dst eps1 [J]
   pair: gauss | expo:a:c:d | recip:a:c:r | power:a:c:q:r
"""
import math, sys, time
import numpy as np
from smooth import make

name = sys.argv[1] if len(sys.argv) > 1 else "expo:1:0.3:0"
dst = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
eps1 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02
J = int(sys.argv[4]) if len(sys.argv) > 4 else 200
P = make(name)
h, L, a = P.h, P.L, P.a
s_t, b0 = L + dst, h + eps1
print("# %s : a = %.6f h = %.8f L = %.6f vartheta = %.6f const = 2 pi^2 h^2 vartheta = %.8f ; 1 - h/a = %.6f" % (P.name, a, h, L, P.vartheta, P.const, 1 - h / a))
print("# s_t = L + %g = %.6f ; b_0 = h + %g = %.6f ; (1 - s_t) a = %.6f" % (dst, s_t, eps1, b0, (1 - s_t) * a))
assert L < s_t < 1 - h / a and h < b0 < (1 - s_t) * a

# (C1), (C2)
Sh = P.sig3f(h, s_t)[0]
lo, hi = L, s_t
for _ in range(100):
    mid = 0.5 * (lo + hi)
    if P.sig3f(h, mid)[0] < s_t:
        lo = mid
    else:
        hi = mid
sig_star = 0.5 * (lo + hi)
r_ = P.sig3f(h, sig_star)
lam = r_[2]
c2 = (Sh - s_t) + lam * (1 - s_t - h / a)
print("# (C1) Sigma(h, s_t) = %.6f < 1: %s ; (C2) D(h, s_t) + lambda (1 - s_t - h/a) = %.6f < 1 - s_t = %.6f: %s  (sigma_* = %.6f, lambda = %.5f, e = %.5f)"
      % (Sh, Sh < 1, c2, 1 - s_t, c2 < 1 - s_t, sig_star, lam, r_[3]))

# ---- the chain ------------------------------------------------------------------------------------------------
t0 = time.time()
Bt = [None] * (J + 2); m = [None] * (J + 2)
prev_hi = b0
for j in range(0, J + 2):
    pj, _ = P.orbitf(b0, j)
    if pj <= s_t:
        continue                                        # case A
    lo, hi = h, prev_hi
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        if P.orbitf(mid, j)[0] <= s_t:
            lo = mid
        else:
            hi = mid
    Bt[j] = lo
    m[j] = P.orbitf(lo, j)[1]
    prev_hi = hi
print("# B_t(j), m_j for j <= %d: %.0f s ; first level in case B: %d" % (J + 1, time.time() - t0, min(j for j in range(J + 2) if Bt[j] is not None)))


def W(j, B):
    """W_j(B) for scalar B in [0, b0] (or beyond b0 on the linear part)."""
    if Bt[j] is None or B <= Bt[j]:
        return P.orbitf(B, j)[0]
    return s_t + m[j] * (B - Bt[j])


b = b0
bs = [b0]
worst_rc, worst_j, ok = 0.0, None, True
worst_ratio_excess = -1e9
supRC = (-1e9, None)
rows = []
for j in range(0, J + 1):
    if Bt[j] is None:
        E = math.inf
    else:
        E = Bt[j] + (1 - s_t - Bt[j] / a) / (m[j] + 1 / a)
    b_next = min(b, E)
    Wn = W(j + 1, b_next)
    ratio = bound = float("nan")
    if Bt[j] is not None and Bt[j + 1] is not None:
        sig1 = P.orbitf(Bt[j + 1], j)[0]
        r1 = P.sig3f(Bt[j + 1], sig1)
        ratio, bound = m[j + 1] / m[j], r1[1] / m[j] + r1[2]
        worst_ratio_excess = max(worst_ratio_excess, ratio - bound)
        # the quantity bounded in Lemma RC, case (beta):  m_{j+1} (E_j - B_t(j+1))  vs  1 - s_t
        q = m[j + 1] * (E - Bt[j + 1])
        if q > supRC[0]:
            supRC = (q, j)
    if Wn > worst_rc:
        worst_rc, worst_j = Wn, j
    if Wn > 1 + 1e-12:
        ok = False
    rows.append((j, "A" if Bt[j] is None else "B", (Bt[j] - h) if Bt[j] else float("nan"), m[j] if m[j] else float("nan"), E - h, b - h, Wn,
                 j * j * (b - h) / P.const, ratio, bound))
    b = b_next
    bs.append(b)
show = set([0, 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 75, 100, 150, 200, 300, 400, 600, 800, 1000])
print("#    j case  B_t(j)-h      m_j          E_j-h        b_j-h        W_{j+1}(b_{j+1})  j^2(b_j-h)/const  m_{j+1}/m_j  bound")
for r in rows:
    if r[0] in show or r[6] > 1 + 1e-12:
        print("  %5d  %s   %.6e  %.5e  %.6e  %.6e   %.6f         %.5f          %.4f      %.4f" % r)
print("# RANGE CONDITION W_{j+1}(b_{j+1}) <= 1 for all j <= %d: %s  (largest value %.6f at j = %s)" % (J, ok, worst_rc, worst_j))
Db0 = P.sig3f(b0, s_t)[0] - s_t
print("# Lemma RC, case (beta): sup_j m_{j+1}(E_j - B_t(j+1)) = %.6f (at j = %s)  <=  limit bound D(h,s_t) + lambda (1 - s_t - h/a) = %.6f ?  %s ;  needed: < 1 - s_t = %.6f ;  [D(b_0, s_t) = %.6f, D(h, s_t) = %.6f]"
      % (supRC[0], supRC[1], c2, supRC[0] <= c2, 1 - s_t, Db0, Sh - s_t))
print("# Lemma RC, case (alpha): Sigma(b_0, s_t) = %.6f  (must be <= 1)" % P.sig3f(b0, s_t)[0])
print("# slope ratio: max over j of [m_{j+1}/m_j - (1/(e_1 m_j) + theta(e_1)/e_1)] = %+.3e  (must be <= 0)" % worst_ratio_excess)

# ---- Lemma T(b) and convexity on a grid --------------------------------------------------------------------------
levels = [j for j in list(range(0, min(J, 40))) + list(range(40, J, 10))]
Bg = np.unique(np.concatenate([np.linspace(0, h, 1501), h + (b0 - h) * 10.0 ** np.linspace(-8, 0, 4001)]))
# p_j on the grid for all j (vectorised), keeping only values <= s_t region accurate (beyond: may be inf)
p = np.zeros_like(Bg); dp = np.zeros_like(Bg)
Wprev = None
maxviol, maxviol_j = -1e9, None
minconv, minconv_j = 1e9, None
mingap, nlin, nmut, nmut_detected = 1e9, 0, 0, 0
t0 = time.time()
Wgrid = {}
for j in range(0, J + 1):
    if j > 0:
        fin = np.isfinite(p)
        S, dB, ds = P.sig3(Bg, np.where(fin, p, 2.0))
        p = np.where(fin, S, np.inf)
    # W_j on grid
    if Bt[j] is None:
        Wj = p.copy()
    else:
        Wj = np.where(Bg <= Bt[j], p, s_t + m[j] * (Bg - Bt[j]))
    if (j - 1) in levels and Wprev is not None:
        # H_{j-1} = Sigma(B, W_{j-1}(B)) on the grid; W_j <= H_{j-1}
        Hm = P.sig3(Bg, Wprev)[0]
        fin = np.isfinite(Hm)
        viol = np.max((Wj - Hm)[fin] / np.maximum(1.0, np.abs(Hm[fin])))
        if viol > maxviol:
            maxviol, maxviol_j = float(viol), j - 1
        if Bt[j] is not None:
            # the linear part of W_j only (B > B_t(j)): gap H_{j-1} - W_j relative to the squared distance (>= 0 expected)
            lin = fin & (Bg > Bt[j])
            if np.any(lin):
                nlin += int(np.sum(lin))
                gap = float(np.min((Hm - Wj)[lin] / np.maximum(1.0, np.abs(Hm[lin]))))
                mingap = min(mingap, gap)
                # mutation: slope 0.5 per cent larger -- must be detected
                Wmut = s_t + 1.005 * m[j] * (Bg - Bt[j])
                if float(np.max((Wmut - Hm)[lin])) > 0:
                    nmut_detected += 1
                nmut += 1
    if j in levels:
        # convexity of W_j: second differences on a UNIFORM grid of [0, b_0] (801 points; scalar evaluation)
        Bu = np.linspace(0, b0, 801)
        Wu = np.array([W(j, float(B)) for B in Bu])
        fin = np.isfinite(Wu)
        nf = int(np.sum(fin))
        if nf >= 3:
            d2 = Wu[2:nf] - 2 * Wu[1:nf - 1] + Wu[:nf - 2]
            c = float(np.min(d2 / np.maximum(1.0, np.abs(Wu[1:nf - 1]))))
            if c < minconv:
                minconv, minconv_j = c, j
    Wprev = Wj
# ---- sharper test of Lemma T(b): for each tested level, sample the linear part of W_{j+1} between B_t(j+1) and the
# end of the regular range of H_j directly (120 points, geometric in B - B_t(j+1)), scalar evaluation
t1 = time.time()
ad_min, ad_n, ad_mut, ad_levels = 1e9, 0, 0, 0
for j in [jj for jj in levels if jj <= 120 or jj % 50 == 0]:
    if Bt[j + 1] is None:
        continue
    Bend = b0 if Bt[j] is None else min(b0, Bt[j] + (1 - s_t - Bt[j] / a) / (m[j] + 1 / a))
    det = False
    for uu in 10.0 ** np.linspace(-7, -0.001, 120):
        B = Bt[j + 1] + (Bend - Bt[j + 1]) * uu
        wj = W(j, B)
        Hj = P.sig3f(B, wj)[0]
        if not math.isfinite(Hj):
            continue
        w1 = s_t + m[j + 1] * (B - Bt[j + 1])
        ad_min = min(ad_min, (Hj - w1) / max(1.0, abs(Hj)))
        ad_n += 1
        if s_t + 1.005 * m[j + 1] * (B - Bt[j + 1]) > Hj:
            det = True
    ad_levels += 1
    ad_mut += det
print("# Lemma T(b), adaptive sampling of the linear part of W_{j+1} (%d levels, %d points): min of (Sigma(B, W_j(B)) - W_{j+1}(B))/max(1, .) = %+.3e ; mutation (slope * 1.005) detected at %d of %d levels  [%.0f s]"
      % (ad_levels, ad_n, ad_min, ad_mut, ad_levels, time.time() - t1))
print("# Lemma T(b) on a grid of %d points of [0, b_0], levels j in %d..%d (%d levels): max of (W_{j+1} - Sigma(B, W_j(B)))/max(1, .) = %+.3e (at j = %s)  [%.0f s]"
      % (len(Bg), levels[0], levels[-1], len(levels), maxviol, maxviol_j, time.time() - t0))
print("#   on the linear parts only (%d grid points with Sigma finite): min of (Sigma(B, W_j(B)) - W_{j+1}(B))/max(1, .) = %+.3e ; mutation (tangent slope * 1.005) detected at %d of %d levels" % (nlin, mingap, nmut_detected, nmut))
print("# convexity of W_j (uniform grid of 801 points of [0, b_0]): most negative second difference / max(1, |W_j|) = %+.3e (at j = %s)" % (minconv, minconv_j))
