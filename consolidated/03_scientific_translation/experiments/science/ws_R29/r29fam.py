#!/usr/bin/env python3
"""r29fam.py -- own routines of workstream R29: a family (W, b) with W piecewise linear, its line-by-line value, its
minimax value and its envelope step (the class Fam of r29_i3_minimax.py, as a module).  setup(P) must be called first
with a r29env.CubeF."""
import math

import numpy as np

GR = (math.sqrt(5.0) - 1) / 2
P = None
a = h = es = None


def setup(cube):
    global P, a, h, es
    P = cube
    a, h, es = cube.a, cube.h, cube.estar


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
