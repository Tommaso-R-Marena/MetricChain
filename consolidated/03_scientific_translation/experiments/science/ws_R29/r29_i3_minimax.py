#!/usr/bin/env python3
"""r29_i3_minimax.py [u]  --  the minimax step of Theorem 11.58e(a) / Lemma A1 at the exponent level: an attempt to break it.

For a family (W, b) (W convex, nondecreasing, continuous, W(0) = 0, values in [0, 1]) and a rate g > 0:
    LHS(g)  = inf_{0<phi<1} max_{B <= b, W(B) <= s <= 1} [ (1 - phi) B + (1 - s) phi theta(g/phi) ]
            = inf_phi max_B [ (1 - phi) B + (1 - W(B)) phi theta(g/phi) ]           (theta >= 0: s = W(B) is the worst)
    RHS1(g) = sup{ B - Sigma(B, W(B)) g : 0 <= B <= b, Sigma(B, W(B)) < inf }       (the line-by-line value)
    RHS2(g) = M_{W', b'}(g) for the envelope step (W', b') = E(W, b)                 (the best admissible next family)
Claims tested:  LHS <= RHS1 (the minimax step; my re-derivation gives LHS = RHS1 exactly)  and  RHS1 <= RHS2.
W is piecewise linear, given by vertices; the maximum over B in LHS is exact (a vertex).  phi by golden section (the
function is convex in phi); B in RHS1 by golden section (concave) plus all vertices; the slope map in doubles.
Families: the envelope curves W_1..W_6 of the cube (as fine piecewise-linear interpolants; convex up to 1e-12), the
flat family, the chord W = B/b (slope at the cap at the top), one line with a kink, two lines that cross at the top,
random convex families with 2-6 pieces, with tops between h and a.  Rates: 1e-6 eps* ... 1.5 eps*.
CONTROL (must fail): the same comparison for families that are NOT convex (concave kinks): the line-by-line value
must fall below the true minimax value in a substantial fraction of cases (the value is that of the convex hull).
Second control: RHS1 against the envelope step of the *next* level (two levels' gain for one) must fail.
"""
import math
import random
import sys

import numpy as np

import r29lib as R
import r29env as E

R.cap_memory()
u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
P = E.CubeF(u)
a, h, es = P.a, P.h, P.estar
GR = (math.sqrt(5.0) - 1) / 2


def gold_min(f, lo, hi, it=80):
    x1, x2 = hi - GR * (hi - lo), lo + GR * (hi - lo)
    f1, f2 = f(x1), f(x2)
    for _ in range(it):
        if f1 < f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - GR * (hi - lo)
            f1 = f(x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + GR * (hi - lo)
            f2 = f(x2)
    xm = 0.5 * (lo + hi)
    return xm, f(xm)


class Fam:
    """a function W on [0, b] given by vertices (xs, ws) (linear in between); convex or not"""

    def __init__(self, xs, ws, name=""):
        self.xs = np.asarray(xs, float)
        self.ws = np.asarray(ws, float)
        self.b = float(self.xs[-1])
        self.name = name

    def W(self, B):
        return float(np.interp(B, self.xs, self.ws))

    def is_convex(self, tol=1e-12):
        sl = np.diff(self.ws) / np.diff(self.xs)
        return bool(np.all(np.diff(sl) >= -tol)) and bool(np.all(sl >= -tol))

    def lhs(self, g, dense=None):
        """inf_phi max_B [(1 - phi) B + (1 - W(B)) phi theta(g/phi)]; the max over B at the vertices (W piecewise linear)"""
        xs, ws = self.xs, self.ws

        def f(phi):
            th = P.theta(g / phi)
            return float(np.max((1 - phi) * xs + (1 - ws) * phi * th))
        # convex in phi: scan to bracket, then golden section
        # the infimum over the open interval (0, 1) is the minimum over [0, 1] (continuity); it is often approached only
        # as phi -> 1 (outer rate e -> g), which is why the statement has "+ eta".  phi = 1 is evaluated as a candidate.
        srt = np.unique(np.concatenate([np.geomspace(1e-9, 0.5, 80), 1 - np.geomspace(1e-14, 0.5, 120)]))   # unique: a duplicate 0.5 made the bracket one-sided
        vals = [f(p) for p in srt]
        k = int(np.argmin(vals))
        lo, hi = srt[max(k - 2, 0)], srt[min(k + 2, len(srt) - 1)]
        return min(gold_min(f, lo, hi)[1], f(1.0), vals[k])

    def bplus(self):
        """sup{B <= b : B < (1 - W(B)) a}"""
        if self.b < (1 - self.W(self.b)) * a:
            return self.b
        lo, hi = 0.0, self.b
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if mid < (1 - self.W(mid)) * a:
                lo = mid
            else:
                hi = mid
        return lo

    def H(self, B):
        return P.Sigma(B, self.W(B))

    def rhs1(self, g):
        """sup{B - Sigma(B, W(B)) g : Sigma finite}: all vertices, and a golden-section search on every piece"""
        bp = self.bplus()

        def f(B):
            s = self.H(B)
            return -math.inf if s == math.inf else B - s * g
        best = 0.0                                      # B = 0: Sigma(0, 0) = 0
        pts = [x for x in self.xs if x < bp] + [bp * (1 - 1e-13)]
        vals = [f(float(x)) for x in pts]
        k = int(np.argmax(vals))
        best = max(best, vals[k])
        # B -> B - Sigma(B, W(B)) g is concave (Sigma(., W(.)) is convex for a convex W): the maximum is on a piece
        # next to the best vertex
        for i in (k - 1, k):
            if 0 <= i < len(pts) - 1 and pts[i + 1] > pts[i]:
                best = max(best, -gold_min(lambda B: -f(B), float(pts[i]), float(pts[i + 1]), it=70)[1])
        return best

    def envelope_step(self, n=4000):
        """(W', b') = E(W, b) as a fine piecewise-linear function: H up to the tangent point, then the line to (b', 1)"""
        bp = self.bplus()

        def r(B):
            Hv = self.H(B)
            return -math.inf if Hv == math.inf else (1 - Hv) / (bp - B)
        Hend = self.H(bp * (1 - 1e-13))
        if Hend <= 1.0:                                  # no cap needed
            Bt, m = bp, None
        else:
            # r is quasi-concave (H convex): scan + golden section; candidates include the kinks of W
            cand = sorted(set([0.0] + [float(x) for x in self.xs if x < bp] + list(np.linspace(0, bp * (1 - 1e-9), 400))))
            vals = [r(c) for c in cand]
            k = int(np.argmax(vals))
            lo, hi = cand[max(k - 1, 0)], cand[min(k + 1, len(cand) - 1)]
            Bt, mneg = gold_min(lambda B: -r(B), lo, hi)
            m = -mneg
            if vals[k] > m:
                Bt, m = cand[k], vals[k]
        xs = np.unique(np.concatenate([np.linspace(0.0, Bt, n), [x for x in self.xs if x < Bt]]))
        ws = np.array([self.H(float(x)) for x in xs])
        if m is not None:
            ws[-1] = 1 - m * (bp - Bt)
            xs = np.append(xs, bp)
            ws = np.append(ws, 1.0)
        ws = np.clip(ws, 0.0, 1.0)
        return Fam(xs, ws, name=self.name + "'")

    def M(self, g):
        return float(np.max(self.xs - self.ws * g))


def lhs_dense(F, g, nB=4001):
    """LHS for a NON-convex W: the max over B on a dense grid plus the vertices (the set {s >= W(B)} is not convex)"""
    Bs = np.unique(np.concatenate([np.linspace(0.0, F.b, nB), F.xs]))
    Ws = np.interp(Bs, F.xs, F.ws)

    def f(phi):
        return float(np.max((1 - phi) * Bs + (1 - Ws) * phi * P.theta(g / phi)))
    grid = np.unique(np.concatenate([np.geomspace(1e-9, 0.5, 80), 1 - np.geomspace(1e-14, 0.5, 120)]))
    vals = [f(p) for p in grid]
    k = int(np.argmin(vals))
    return min(gold_min(f, grid[max(k - 2, 0)], grid[min(k + 2, len(grid) - 1)])[1], f(1.0), vals[k])


def rhs1_dense(F, g, nB=4001):
    bp = F.bplus()
    best = 0.0
    for B in np.unique(np.concatenate([np.linspace(0.0, bp * (1 - 1e-12), nB), [x for x in F.xs if x < bp]])):
        s = F.H(float(B))
        if s < math.inf:
            best = max(best, float(B) - s * g)
    return best


# ---------------------------------------------------------------------------------------------------------- families
rng = random.Random(2029)
fams = []
env = E.EnvSA(P, 8)
for j in range(0, 7):
    bj = env.b[j]
    if j == 0:
        fams.append(Fam([0.0, bj], [0.0, 0.0], "envelope W_0 (flat, b = a)"))
    else:
        xs = np.unique(np.concatenate([np.linspace(0, env.Bt[j], 1500), [bj]]))
        ws = np.array([float(env.W(j, float(x))) for x in xs])
        fams.append(Fam(xs, np.clip(ws, 0, 1), "envelope W_%d" % j))
for b in (a, 0.9 * a, 0.5 * a, h * 1.5, h * 1.05, h * 1.0001):
    fams.append(Fam([0.0, b], [0.0, 0.0], "flat, b = %.4f a" % (b / a)))
    fams.append(Fam([0.0, b], [0.0, 1.0], "chord W = B/b (slope at the cap at the top), b = %.4f a" % (b / a)))
    fams.append(Fam([0.0, 0.6 * b, b], [0.0, 0.0, 1.0], "zero then one line to the cap, b = %.4f a" % (b / a)))
    fams.append(Fam([0.0, 0.5 * b, b], [0.0, 0.1, 0.7], "two lines, b = %.4f a" % (b / a)))
    # two lines that cross exactly at the top: W = max(l1, l2) with l1(b) = l2(b): the second is never active before b
    fams.append(Fam([0.0, 0.999999 * b, b], [0.0, 0.3 * 0.999999, 0.3], "two lines crossing at the top, b = %.4f a" % (b / a)))
for _ in range(60):
    k = rng.randrange(2, 7)
    b = h + (a - h) * rng.random() ** 2
    cuts = sorted(rng.random() for _ in range(k - 1))
    xs = [0.0] + [c * b for c in cuts] + [b]
    slopes = sorted(rng.random() * 3 for _ in range(k))
    ws = [0.0]
    for i in range(k):
        ws.append(ws[-1] + slopes[i] * (xs[i + 1] - xs[i]))
    scale = (rng.random() ** 0.5) / max(ws[-1], 1e-9) if rng.random() < 0.8 else 1.0 / max(ws[-1], 1e-9)   # 20 %: W(b) = 1 exactly
    fams.append(Fam(xs, [w * min(scale, 1.0 / max(ws[-1], 1e-9)) for w in ws], "random convex, %d pieces" % k))

rates = [1e-6 * es, 1e-4 * es, 0.003 * es, 0.03 * es, 0.1 * es, 0.3 * es, 0.6 * es, 0.9 * es, 0.999 * es, es, 1.5 * es]
print("# minimax step at the exponent level, cube u = %g: %d convex families x %d rates" % (u, len(fams), len(rates)))
n = v1 = v2 = 0
worst_gap = 0.0          # LHS - RHS1 (must be <= tolerance; my derivation: = 0)
worst_eq = 0.0           # |LHS - RHS1|
worst2 = -math.inf       # RHS1 - RHS2 (must be <= tolerance)
tol = 2e-9 * a
ctrl2 = 0
rows = []
for F in fams:
    assert F.is_convex(1e-9), F.name
    Fn = F.envelope_step()
    Fnn = Fn.envelope_step(n=1500)
    for g in rates:
        L = F.lhs(g)
        R1 = F.rhs1(g)
        R2 = Fn.M(g)
        R3 = Fnn.M(g)
        n += 1
        worst_gap = max(worst_gap, L - R1)
        worst_eq = max(worst_eq, abs(L - R1))
        worst2 = max(worst2, R1 - R2)
        if L - R1 > tol:
            v1 += 1
            rows.append((F.name, g / es, L, R1, R2))
        if R1 - R2 > 1e-7 * a:                          # the envelope curve is a fine interpolant: allow its 1e-7 a
            v2 += 1
            rows.append((F.name, g / es, L, R1, R2))
        if L > R3 + 1e-6 * a:
            ctrl2 += 1
print("    cases %d;  violations of LHS <= RHS1 (tolerance 2e-9 a): %d;  violations of RHS1 <= M_{W',b'}(g) (tolerance 1e-7 a): %d" % (n, v1, v2))
print("    largest LHS - RHS1 = %.2e a;  largest |LHS - RHS1| = %.2e a  (the minimax identity is an equality);  largest RHS1 - M_{W',b'} = %.2e a" % (worst_gap / a, worst_eq / a, worst2 / a))
for r in rows[:8]:
    print("    VIOLATION: %s  g = %.4g eps*  LHS %.12f  RHS1 %.12f  M' %.12f" % r)
print("    control 2 (two levels' gain claimed for one: LHS <= M_{W'',b''}(g)): fails in %d of %d cases  [must be > 0]" % (ctrl2, n))

# ---------------------------------------------------------------------------------------------------------- control: non-convex
nc = fail = 0
big = 0.0
for _ in range(40):
    b = h + (a - h) * rng.random()
    # a concave kink: steep first, flat later (not convex), values in [0, 1]
    x1 = b * (0.2 + 0.5 * rng.random())
    w1 = 0.3 + 0.6 * rng.random()
    w2 = w1 + (1 - w1) * 0.3 * rng.random()
    F = Fam([0.0, x1, b], [0.0, w1, w2], "non-convex")
    if F.is_convex():
        continue
    for g in (0.003 * es, 0.03 * es, 0.1 * es, 0.3 * es):
        L = lhs_dense(F, g)
        R1 = rhs1_dense(F, g)
        nc += 1
        big = max(big, L - R1)
        if L - R1 > 1e-6 * a:
            fail += 1
print("CONTROL (families that are not convex): the line-by-line value is below the minimax value in %d of %d cases, by up to %.3f a  [must be > 0]" % (fail, nc, big / a))
ok = (v1 == 0 and v2 == 0 and fail > 0 and ctrl2 > 0)
print("MINIMAX: %s" % ("no violation; both controls fail as they must" if ok else "CHECK FAILED"))
R.finish("r29_i3_minimax u=%g" % u)
