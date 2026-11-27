#!/usr/bin/env python3
"""z6_certified_tops.py [u] [J] [K]  --  CERTIFIED upper bounds for the exponent of j nested levels (cube pair).

What is certified, and from what.  `docs/workstreams/Z_ADDENDUM.md` (A1, A6): if a sequence of families (V_j, c_j) is
admissible --
    (S1)  c_j >= c_{j+1} >= sup{B <= c_j : Sigma(B, V_j(B)) < infinity},
    (S2)  V_{j+1}(B) <= Sigma(B, V_j(B))  on [0, c_{j+1}],
    V_j : [0, c_j] -> [0, 1] convex, nondecreasing, continuous, V_j(0) = 0,
and starts with V_0 = 0 on [0, c_0], c_0 >= a, then T_j <= M_{V_j, c_j} for the level recursion, in particular
    tau_j <= c_j        and        T_j(g) <= max_B (B - V_j(B) g)        for every j >= 1 and every rate g >= 0.
This script constructs such a sequence in a form whose admissibility is checked by exact rational arithmetic and
interval arithmetic, so that the printed numbers are rigorous upper bounds GIVEN THAT STATEMENT (a paper proof).

The construction ("multi-rate sequence").  Sigma(B, s) = sup_e [B - (1 - s) theta(e)]/e  >=  [B - (1 - s) thbar]/e'
for every pair (e', thbar) with thbar >= theta(e') -- a lower bound, which is all (S2) asks for.  For the cube,
theta(e) = KL(rho || 1/2) with KL(rho || p_u) = e; for a floating-point number rho the pair
    e' := an upper bound of KL(rho || p_u),     thbar := an upper bound of KL(rho || 1/2)
(interval arithmetic, mpmath `iv`, 30 digits, rounded outwards to doubles) is valid because theta is nonincreasing.
V_j is kept as a maximum of finitely many lines alpha*B - beta (doubles) and the zero line.  If l <= V_j is one
of its lines, then  [B - thbar (1 - l(B))]/e'  is a line below Sigma(B, V_j(B)) on [0, c_j]  (the bracket is
decreasing in theta because l <= V_j <= 1 there); its coefficients are rounded so that the stored line is below it
(slope down, intercept down).  Which lines and rates are used is chosen in floating point (one line per sample
point, the rate by a golden-section search) -- that choice affects the quality of the bound, not its validity.
Cap at one: the stored lines form a convex function H; if H(c) > 1 the lines with value above one at c are dropped
and the tangent line from the point (c, 1) to H is added -- computed on the exact upper hull (Fractions), its slope
rounded up (a steeper line through (c, 1) is lower on [0, c]).
Top: c_{j+1} = min(c_j, c) for a double c that is verified EXACTLY to satisfy c + abar V_j(c) >= abar, abar >= a;
then every B <= c_j with Sigma(B, V_j(B)) < infinity (which forces B <= (1 - V_j(B)) a) is at most c_{j+1}.

Not certified: the theory quoted above; the constants h, c_*^2 and the floating-point envelope tops printed for
comparison; that the bounds are close to the truth (they are upper bounds, however coarse the sampling).
"""
import math
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np
from mpmath import iv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

u_str = sys.argv[1] if len(sys.argv) > 1 else "1"
JMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 40
K = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
COMPARE = (len(sys.argv) <= 4) or (sys.argv[4] != "nocompare")

iv.dps = 30
U = iv.mpf(u_str)
PU = 1 / (1 + iv.exp(U))
HALF = iv.mpf(1) / 2
INF = float("inf")


def up(x):
    """a double >= the interval x"""
    return math.nextafter(float(x.b), INF)


def dn(x):
    """a double <= the interval x"""
    return math.nextafter(float(x.a), -INF)


def kl_iv(r, p):
    return r * iv.log(r / p) + (1 - r) * iv.log((1 - r) / (1 - p))


A_IV = kl_iv(PU, HALF)
ABAR, ALOW = up(A_IV), dn(A_IV)                 # a = theta(0) = KL(p_u || 1/2)
pu = float(PU.mid)
u = float(u_str)


def certified_pair(rho):
    """(e', thbar) doubles with thbar >= theta_na(e'), for a double rho in (p_u, 1/2]"""
    if rho >= 0.5:
        return up(kl_iv(HALF, PU)), 0.0
    r = iv.mpf(rho)
    e = kl_iv(r, PU)
    assert e.a > 0, "rho must be above p_u"
    return up(e), max(0.0, up(kl_iv(r, HALF)))


def e_of(rho):
    return rho * np.log(rho / pu) + (1 - rho) * np.log((1 - rho) / (1 - pu))


def th_of(rho):
    return np.maximum(0.0, rho * np.log(2 * rho) + (1 - rho) * np.log(2 * (1 - rho)))


def down(x, n=4):
    for _ in range(n):
        x = np.nextafter(x, -INF)
    return x


def upw(x, n=4):
    for _ in range(n):
        x = np.nextafter(x, INF)
    return x


class Curve:
    """V(B) = max(0, max_i (al[i]*B - be[i])) on [0, c]; al > 0, be >= 0 doubles; lines sorted by slope, all on the hull"""

    def __init__(self, al, be, c):
        self.c = c
        self.al, self.be = self._hull(list(al), list(be), c)

    @staticmethod
    def _hull(al, be, c):
        """exact upper hull of the lines and the zero line on [0, c]; returns the nonzero hull lines, by slope"""
        lines = sorted(set(zip(al, be)))                       # by slope, then by intercept
        best = {}
        for a_, b_ in lines:                                   # equal slopes: keep the higher line (smaller beta)
            if a_ not in best or b_ < best[a_]:
                best[a_] = b_
        L = [(Fr(0), Fr(0), 0.0, 0.0)] + [(Fr(a_), Fr(best[a_]), a_, best[a_]) for a_ in sorted(best) if a_ > 0]
        st = []
        for ln in L:
            while len(st) >= 2:
                a1, b1 = st[-2][0], st[-2][1]
                a2, b2 = st[-1][0], st[-1][1]
                a3, b3 = ln[0], ln[1]
                # line 2 is not needed if the crossing of 1 and 3 is left of the crossing of 1 and 2
                if (b3 - b1) * (a2 - a1) <= (b2 - b1) * (a3 - a1):
                    st.pop()
                else:
                    break
            st.append(ln)
        # drop the lines that become active only beyond c
        C = Fr(c)
        out = [st[0]]
        for i in range(1, len(st)):
            a1, b1 = st[i - 1][0], st[i - 1][1]
            a2, b2 = st[i][0], st[i][1]
            if (b2 - b1) < C * (a2 - a1):                     # crossing (b2 - b1)/(a2 - a1) < c
                out.append(st[i])
            else:
                break
        return np.array([o[2] for o in out[1:]], dtype=float), np.array([o[3] for o in out[1:]], dtype=float)

    def val(self, B):
        B = np.asarray(B, dtype=float)
        if len(self.al) == 0:
            return np.zeros(B.shape), np.full(B.shape, -1, dtype=int)
        M = self.al[None, :] * B[:, None] - self.be[None, :]
        i = np.argmax(M, axis=1)
        v = M[np.arange(len(B)), i]
        return np.where(v > 0, v, 0.0), np.where(v > 0, i, -1)

    def val_exact(self, B):
        B = Fr(B)
        v = Fr(0)
        for a_, b_ in zip(self.al, self.be):
            w = Fr(float(a_)) * B - Fr(float(b_))
            if w > v:
                v = w
        return v

    def vertices(self):
        """exact vertices (X, V(X)) of the hull on [0, c]: 0, the crossings, c"""
        C = Fr(self.c)
        A = [Fr(0)] + [Fr(float(x)) for x in self.al]
        Bt = [Fr(0)] + [Fr(float(x)) for x in self.be]
        vs = [(Fr(0), Fr(0))]
        for i in range(1, len(A)):
            X = (Bt[i] - Bt[i - 1]) / (A[i] - A[i - 1])
            if X < C:
                vs.append((X, A[i] * X - Bt[i]))
        vs.append((C, A[-1] * C - Bt[-1]))
        return vs

    def M_upper(self, g):
        """a double >= max_{0 <= B <= c} (B - V(B) g), g a double >= 0 (exact maximum over the vertices, rounded up)"""
        G = Fr(g)
        m = max(X - G * V for X, V in self.vertices())
        f = float(m)
        while Fr(f) < m:
            f = math.nextafter(f, INF)
        return f


def next_top(V):
    """a double c' with c' = c_j, or c' + abar V(c') >= abar exactly; then c' >= sup{B <= c_j : B <= (1 - V(B)) a}"""
    A = Fr(ABAR)
    C = Fr(V.c)
    if C + A * V.val_exact(V.c) < A:
        return V.c
    lo, hi = 0.0, V.c
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid + ABAR * float(V.val(np.array([mid]))[0][0]) >= ABAR:
            hi = mid
        else:
            lo = mid
    c = hi
    for _ in range(200):
        if Fr(c) + A * V.val_exact(c) >= A:
            return min(c, V.c)
        c = math.nextafter(c, INF)
    raise RuntimeError("top not verified")


GOLD = (math.sqrt(5.0) - 1) / 2


def best_rho(B, s):
    """floating-point maximiser of [B - (1 - s) theta(rho)]/e(rho) over rho in (p_u, 1/2]  (rho = p_u + (1/2 - p_u) w^2)"""
    def F(w):
        rho = pu + (0.5 - pu) * w * w
        return (B - (1 - s) * th_of(rho)) / e_of(rho)
    lo = np.full(B.shape, 1e-6)
    hi = np.ones(B.shape)
    x1 = hi - GOLD * (hi - lo)
    x2 = lo + GOLD * (hi - lo)
    f1, f2 = F(x1), F(x2)
    for _ in range(90):
        left = f1 > f2
        hi = np.where(left, x2, hi)
        lo = np.where(left, lo, x1)
        nx1 = hi - GOLD * (hi - lo)
        nx2 = lo + GOLD * (hi - lo)
        x1, x2 = nx1, nx2
        f1, f2 = F(x1), F(x2)
    w = 0.5 * (lo + hi)
    w = np.where(F(np.ones(B.shape)) >= F(w), 1.0, w)          # the end point rho = 1/2 (theta = 0)
    return np.minimum(0.5, pu + (0.5 - pu) * w * w), F(w)


def step(V):
    c = next_top(V)
    Bs = np.unique(np.concatenate([np.linspace(0.0, c, K + 1)[1:], c * (1.0 - np.geomspace(1e-9, 0.25, K // 4))]))
    s, idx = V.val(Bs)
    keep = s < 1.0
    Bs, s, idx = Bs[keep], s[keep], idx[keep]
    rho, Fv = best_rho(Bs, s)
    good = (Fv > 0) & np.isfinite(Fv) & (Fv < 50.0)           # slopes far above one are dropped by the cap anyway
    al_new, be_new = [], []
    cache = {}
    for B_, r_, i_ in zip(Bs[good], rho[good], idx[good]):
        r_ = float(r_)
        if r_ not in cache:
            cache[r_] = certified_pair(r_)
        e_, th_ = cache[r_]
        a0 = float(V.al[i_]) if i_ >= 0 else 0.0
        b0 = float(V.be[i_]) if i_ >= 0 else 0.0
        # exact line: [B (1 + th a0) - th (1 + b0)]/e ; stored: slope rounded down, beta rounded up
        al_new.append(float(down(np.float64((1.0 + th_ * a0) / e_))))
        be_new.append(float(upw(np.float64(th_ * (1.0 + b0) / e_))))
    H = Curve(al_new, be_new, c)
    C = Fr(c)
    if len(H.al) and Fr(float(H.al[-1])) * C - Fr(float(H.be[-1])) > 1:
        # the cap: drop the lines above one at c; add the tangent from (c, 1), slope rounded up
        vs = H.vertices()
        mstar = max((1 - Vx) / (C - X) for X, Vx in vs[:-1])
        m = float(mstar)
        while Fr(m) < mstar:
            m = math.nextafter(m, INF)
        bL = float(Fr(m) * C - 1)
        while Fr(bL) < Fr(m) * C - 1:
            bL = math.nextafter(bL, INF)
        kal = [float(a_) for a_, b_ in zip(H.al, H.be) if Fr(float(a_)) * C - Fr(float(b_)) <= 1]
        kbe = [float(b_) for a_, b_ in zip(H.al, H.be) if Fr(float(a_)) * C - Fr(float(b_)) <= 1]
        H = Curve(kal + [m], kbe + [bL], c)
    assert H.val_exact(c) <= 1, "cap failed"
    assert all(b_ >= 0 for b_ in H.be) and all(a_ > 0 for a_ in H.al)
    return H


def main():
    t0 = time.time()
    print("# CERTIFIED upper bounds c_j >= tau_j for the exponent of j nested levels; cube pair, u = %s" % u_str)
    print("# a in [%.15g, %.15g] (interval arithmetic); sample points per level K = %d; levels up to %d" % (ALOW, ABAR, K, JMAX))
    ref = None
    hh = cs2 = None
    try:
        import zetalib
        P = zetalib.rlib.Cube(u).setup()
        hh, LL = P.h, P.L
        thpp = None
        for nm in ("thpp", "theta_hint_pp", "vartheta", "thhpp"):
            if hasattr(P, nm):
                thpp = getattr(P, nm)
        if thpp is None:                                         # theta_hint''(0) = -1/J''(L), by a difference quotient
            d = 1e-4
            Jf = lambda t: math.log(2 / (1 + math.exp(-t * u))) - t * math.log(2 / (1 + math.exp(-u)))
            thpp = -1.0 / ((Jf(LL + d) - 2 * Jf(LL) + Jf(LL - d)) / (d * d))
        cs2 = 2 * math.pi ** 2 * hh * hh * thpp
        if COMPARE and JMAX <= 80:
            ref = zetalib.EnvZ(u, JMAX, NG=8000).b
        print("# for comparison only (floating point, not certified): h = %.9f, c_*^2 = %.7f%s" % (hh, cs2, "; envelope tops b_j by zetalib.EnvZ (grid 8000)" if ref else ""))
    except Exception as ex:                                       # the comparison is optional
        print("# (comparison constants not available: %s)" % ex)
    gs = [0.0] + ([0.1 * hh, 0.5 * hh, hh] if hh else [])
    V = Curve([], [], ABAR)                                       # V_0 = 0 on [0, abar]
    print("# columns: j | c_j (certified: tau_j <= c_j) | c_j/a (upper bound) | lines | float envelope top b_j | (c_j - b_j)/(b_j - h) | j^2 (c_j - h)/c_*^2"
          + (" | certified M_j(g) >= T_j(g) at g = 0.1h, 0.5h, h" if hh else ""))
    rows = []
    for j in range(1, JMAX + 1):
        V = step(V)
        cj = V.c
        ratio = cj / ALOW
        ratio = math.nextafter(ratio, INF)
        cmp_ = ""
        if ref is not None:
            bj = ref[j]
            cmp_ = "%.9f | %9.2e" % (bj, (cj - bj) / (bj - hh))
        else:
            cmp_ = "- | -"
        extra = ""
        if hh:
            extra = " | %.6f | " % (j * j * (cj - hh) / cs2) + "  ".join("%.9f" % V.M_upper(g) for g in gs[1:])
        print("%4d | %.12f | %.9f | %5d | %s%s" % (j, cj, ratio, len(V.al), cmp_, extra), flush=True)
        rows.append((j, cj))
    mono = all(rows[i][1] >= rows[i + 1][1] for i in range(len(rows) - 1))
    above = all(cj > (hh if hh else 0.0) for _, cj in rows)
    print("# tops nonincreasing: %s;  all above h (as they must be: tau_j > h): %s;  time %.0f s" % (mono, above, time.time() - t0))
    print("ALL CHECKS PASS" if mono and above else "CHECK FAILED")


if __name__ == "__main__":
    main()
