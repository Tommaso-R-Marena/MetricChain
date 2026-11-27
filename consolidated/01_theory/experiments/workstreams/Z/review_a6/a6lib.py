"""a6lib.py -- the referee's own floating-point tools for the review of Z_ADDENDUM A6a/A6b/A9a.

Written from the definitions; imports nothing from the coordinator's code (zetalib, rlib, z6, ...) and nothing
from the earlier referees' code.  FLOATING POINT throughout (double precision): nothing in this file is certified.

The cube pair, slope u:
    p_u = 1/(1 + e^u),  theta(e) = KL(rho || 1/2) with KL(rho || p_u) = e, rho in [p_u, 1/2];  theta = 0 for e >= eps*.
    a = theta(0) = KL(p_u || 1/2),  eps* = KL(1/2 || p_u) = ln cosh(u/2).
    J(t) = inf_e [(1 - t) theta(e) + t e] = (1 - t) ln 2 - ln(1 + e^{tu}) + t ln(1 + e^u)        (own derivation:
        (1-t) KL(rho||1/2) + t KL(rho||p_u) = KL(rho || q_t) - ln Z_t, q_t ~ (1/2)^{1-t} p_u^t, minimised at rho = q_t,
        and rho(t) = q_t(1) = 1/(1 + e^{tu}) runs from 1/2 (t = 0) to p_u (t = 1)).
    Parametrisation of theta by t in [0, 1]:  e(t) = J + (1 - t) J',  theta = J - t J',  theta'(e) = -t/(1 - t).
    The slope map:  Sigma(B, s) = t (1 - s)/(1 - t)  with  J(t)/(1 - t) = B/(1 - s)   (for 0 <= B < (1 - s) a);
        the maximising rate is e(t).  (Own derivation: Sigma is the least sigma with inf_e[(1-s)theta + sigma e] >= B,
        and inf_e[(1-s) theta(e) + sigma e] = (1 - s + sigma) J(sigma/(1 - s + sigma)).)
"""
import math

import numpy as np

LN2 = math.log(2.0)


class Cube:
    def __init__(self, u):
        u = float(u)
        self.u = u
        self.lse = math.log1p(math.exp(u))                 # ln(1 + e^u)
        self.pu = 1.0 / (1.0 + math.exp(u))
        self.a = LN2 - self.lse + u * (1.0 - self.pu)      # KL(p_u || 1/2)
        self.eps = self.lse - LN2 - 0.5 * u                # KL(1/2 || p_u) = ln cosh(u/2)
        c = (self.lse - LN2) / u                           # J'(L) = 0  <=>  logistic(L u) = c
        self.L = math.log(c / (1.0 - c)) / u
        self.h = float(self.J(self.L))
        self.vth = -1.0 / float(self.J2(self.L))           # theta_hint''(0) = -1/J''(L)
        self.cs2 = 2.0 * math.pi ** 2 * self.h ** 2 * self.vth

    # ---- the dual function
    def J(self, t):
        t = np.asarray(t, dtype=float)
        return (1.0 - t) * LN2 - np.logaddexp(0.0, t * self.u) + t * self.lse

    def J1(self, t):
        t = np.asarray(t, dtype=float)
        return -LN2 - self.u / (1.0 + np.exp(-t * self.u)) + self.lse

    def J2(self, t):
        t = np.asarray(t, dtype=float)
        x = np.exp(-np.abs(t * self.u))
        return -self.u ** 2 * x / (1.0 + x) ** 2

    # ---- theta through the parameter t
    def e_of_t(self, t):
        return self.J(t) + (1.0 - np.asarray(t, dtype=float)) * self.J1(t)

    def th_of_t(self, t):
        return self.J(t) - np.asarray(t, dtype=float) * self.J1(t)

    def rho_of_t(self, t):
        return 1.0 / (1.0 + np.exp(np.asarray(t, dtype=float) * self.u))

    def t_of_e(self, e):
        """t in [0, 1] with e(t) = e (e(t) decreases from eps* at t = 0 to 0 at t = 1); e clipped to [0, eps*]"""
        e = np.clip(np.asarray(e, dtype=float), 0.0, self.eps)
        lo = np.zeros(e.shape)
        hi = np.ones(e.shape)
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            big = self.e_of_t(mid) > e
            lo = np.where(big, mid, lo)
            hi = np.where(big, hi, mid)
        return 0.5 * (lo + hi)

    def theta(self, e):
        e = np.asarray(e, dtype=float)
        t = self.t_of_e(e)
        return np.where(e >= self.eps, 0.0, np.maximum(0.0, self.th_of_t(t)))

    def theta_direct(self, e):
        """theta from the definition (bisection on rho for KL(rho||p_u) = e): an independent route, for cross-checks"""
        e = np.asarray(e, dtype=float)
        lo = np.full(e.shape, self.pu)
        hi = np.full(e.shape, 0.5)
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            small = kl(mid, self.pu) < e
            lo = np.where(small, mid, lo)
            hi = np.where(small, hi, mid)
        r = 0.5 * (lo + hi)
        return np.where(e >= self.eps, 0.0, kl(r, 0.5))

    # ---- the hinted exponent
    def theta_hint(self, g):
        g = np.asarray(g, dtype=float)
        gg = np.clip(g, 0.0, self.eps * (1 - 1e-15))
        c = (self.eps + 0.5 * self.u - gg) / self.u            # logistic(t u) = c
        t = np.log(c / (1.0 - c)) / self.u
        t = np.clip(t, 0.0, 1.0)
        return np.where(g >= self.eps, 0.0, self.J(t) - t * gg)

    def t_hint(self, g):
        g = np.asarray(g, dtype=float)
        gg = np.clip(g, 0.0, self.eps)
        c = (self.eps + 0.5 * self.u - gg) / self.u
        return np.clip(np.log(c / (1.0 - c)) / self.u, 0.0, 1.0)

    def t1(self, B):
        """the smaller solution of J(t) = B, for 0 <= B <= h (t in [0, L])"""
        B = np.asarray(B, dtype=float)
        lo = np.zeros(B.shape)
        hi = np.full(B.shape, self.L)
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            small = self.J(mid) < B
            lo = np.where(small, mid, lo)
            hi = np.where(small, hi, mid)
        return 0.5 * (lo + hi)

    # ---- the slope map
    def G(self, t):
        """J(t)/(1 - t), increasing from 0 (t = 0) to a (t -> 1)"""
        t = np.asarray(t, dtype=float)
        return self.J(t) / (1.0 - t)

    def sigma_t(self, B, s):
        """the parameter t of the maximising rate of Sigma(B, s): J(t)/(1 - t) = B/(1 - s); nan where irregular"""
        B = np.asarray(B, dtype=float)
        s = np.asarray(s, dtype=float)
        with np.errstate(divide="ignore", invalid="ignore"):
            r = np.where(s < 1.0, B / (1.0 - s), np.inf)
        ok = r < self.a
        rr = np.where(ok, r, 0.0)
        lo = np.zeros(rr.shape)
        hi = np.full(rr.shape, 1.0 - 1e-15)
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            small = self.G(mid) < rr
            lo = np.where(small, mid, lo)
            hi = np.where(small, hi, mid)
        t = 0.5 * (lo + hi)
        return np.where(ok, t, np.nan)

    def sigma(self, B, s):
        """Sigma(B, s); +inf where B >= (1 - s) a and B > 0 (infinite slope at zero)"""
        B = np.asarray(B, dtype=float)
        s = np.asarray(s, dtype=float)
        t = self.sigma_t(B, s)
        with np.errstate(invalid="ignore"):
            val = t * (1.0 - s) / (1.0 - t)
        val = np.where(np.isnan(t), np.inf, val)
        return np.where(B <= 0.0, 0.0, val)

    def sigma_direct(self, B, s, n=20001):
        """Sigma(B, s) from the definition: maximum of [B - (1 - s) theta]/e over a fine grid of rho (scalar B, s)"""
        w = np.linspace(2e-3, 1.0, n)                      # below that the float KL(rho || p_u) cancels too much
        rho = self.pu + (0.5 - self.pu) * w * w
        e = kl(rho, self.pu)
        th = kl(rho, 0.5)
        f = (B - (1.0 - s) * th) / e
        i = int(np.argmax(f))
        # local parabolic refinement (uniform spacing in w)
        if 0 < i < n - 1:
            y0, y1, y2 = f[i - 1], f[i], f[i + 1]
            d = y0 - 2 * y1 + y2
            if d < -1e-300 and abs(y2 - y0) < 0.5 * abs(d) * 4:
                return float(max(y1 - 0.125 * (y2 - y0) ** 2 / d, 0.0))
        return float(max(f[i], 0.0))


def kl(r, p):
    r = np.asarray(r, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        x = np.where(r > 0, r * np.log(r / p), 0.0)
        y = np.where(r < 1, (1.0 - r) * np.log((1.0 - r) / (1.0 - p)), 0.0)
    return x + y


# ------------------------------------------------------------------------------------------------------------
# convex piecewise-linear curves as maxima of lines  (V(B) = max(0, max_i (al_i B - be_i)) on [0, c])
# ------------------------------------------------------------------------------------------------------------

def upper_hull(al, be, c):
    """float upper hull of the zero line and the lines al*B - be on [0, c].  Returns (al, be, X): hull lines by slope
    (without the zero line) and X[i] = the point where hull line i becomes active (X increasing, X[i] < c)."""
    order = np.lexsort((be, al))                         # by slope, then by beta (smaller beta = higher line first)
    A = [0.0]
    Bt = [0.0]
    for i in order:
        a_, b_ = float(al[i]), float(be[i])
        if a_ <= 0.0:
            continue
        if a_ == A[-1]:
            continue                                     # same slope: the higher line (smaller beta) came first
        while len(A) >= 2:
            a1, b1, a2, b2 = A[-2], Bt[-2], A[-1], Bt[-1]
            if (b_ - b1) * (a2 - a1) <= (b2 - b1) * (a_ - a1):
                A.pop()
                Bt.pop()
            else:
                break
        A.append(a_)
        Bt.append(b_)
    Xs = [(Bt[i] - Bt[i - 1]) / (A[i] - A[i - 1]) for i in range(1, len(A))]
    n = 0
    while n < len(Xs) and Xs[n] < c:
        n += 1
    return np.array(A[1:n + 1]), np.array(Bt[1:n + 1]), np.array(Xs[:n])


class LCurve:
    """V = max(0, lines) on [0, c], lines on the hull, sorted"""

    def __init__(self, al, be, c):
        self.c = float(c)
        self.al, self.be, self.X = upper_hull(np.asarray(al, dtype=float), np.asarray(be, dtype=float), self.c)

    def val(self, B):
        """(V(B), index of the active line or -1 for the zero line)"""
        B = np.asarray(B, dtype=float)
        if len(self.al) == 0:
            return np.zeros(B.shape), np.full(B.shape, -1, dtype=int)
        i = np.searchsorted(self.X, B, side="right") - 1          # active hull line (-1: zero line)
        ii = np.maximum(i, 0)
        v = np.where(i >= 0, self.al[ii] * B - self.be[ii], 0.0)
        return np.maximum(v, 0.0), i

    def vertices(self):
        if len(self.al) == 0:
            return np.array([0.0, self.c]), np.array([0.0, 0.0])
        Xv = np.concatenate([[0.0], self.X, [self.c]])
        Vv = np.concatenate([[0.0], self.al * self.X - self.be, [self.al[-1] * self.c - self.be[-1]]])
        return Xv, np.maximum(Vv, 0.0)

    def M(self, g):
        """max_{0 <= B <= c} (B - V(B) g) for an array of rates g (maximum over the vertices)"""
        Xv, Vv = self.vertices()
        g = np.atleast_1d(np.asarray(g, dtype=float))
        out = np.empty(g.shape)
        for k in range(0, len(g), 256):
            gg = g[k:k + 256]
            out[k:k + 256] = np.max(Xv[None, :] - gg[:, None] * Vv[None, :], axis=1)
        return out


def top_of(P, V):
    """the next top: c' = c if c + a V(c) < a, else the root of B + a V(B) = a on [0, c] (float)"""
    a = P.a
    vc = float(V.val(np.array([V.c]))[0][0])
    if V.c + a * vc < a:
        return V.c
    lo, hi = 0.0, V.c
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid + a * float(V.val(np.array([mid]))[0][0]) >= a:
            hi = mid
        else:
            lo = mid
    return hi


def sample_points(c, K):
    """the referee's sample points on (0, c): uniform, plus a geometric refinement towards the top"""
    uni = (np.arange(1, K + 1) - 0.5) * (c / K)
    geo = c * (1.0 - np.geomspace(1e-10, 0.3, max(8, K // 3)))
    return np.unique(np.concatenate([uni, geo]))


def _tangent_lines(P, V, Bs):
    """float tangent lines of Sigma(., V(.)) at the points Bs: arrays (al, be)"""
    s, idx = V.val(Bs)
    ok = (s < 1.0) & (Bs < (1.0 - s) * P.a * (1 - 1e-13)) & (Bs > 0)
    Bs, s, idx = Bs[ok], s[ok], idx[ok]
    t = P.sigma_t(Bs, s)
    e = P.e_of_t(t)
    th = np.maximum(P.th_of_t(t), 0.0)
    if len(V.al):
        a0 = np.where(idx >= 0, V.al[np.maximum(idx, 0)], 0.0)
        b0 = np.where(idx >= 0, V.be[np.maximum(idx, 0)], 0.0)
    else:
        a0 = np.zeros(Bs.shape)
        b0 = np.zeros(Bs.shape)
    good = e > 1e-300
    return (1.0 + th[good] * a0[good]) / e[good], th[good] * (1.0 + b0[good]) / e[good]


def lines_step(P, V, K, refine=0):
    """one step of the multi-rate sequence in FLOATING POINT (tangent lines of Sigma(., V(.)) at the sample points,
    capped at one by the tangent from the top).  Returns the new LCurve.  Its top errs upwards up to rounding.
    refine > 0: a second pass with extra sample points around the point where the cap line leaves the curve."""
    c = top_of(P, V)
    al, be = _tangent_lines(P, V, sample_points(c, K))
    H = cap(LCurve(al, be, c))
    if refine and len(H.al) and H.al[-1] * c - H.be[-1] > 1.0 - 1e-9:
        xt = float(H.X[-1])
        w = 4.0 * c / K
        for _ in range(2):
            extra = np.linspace(max(xt - w, 0.0), min(xt + w, c), refine + 2)[1:-1]
            al2, be2 = _tangent_lines(P, V, extra)
            al, be = np.concatenate([al, al2]), np.concatenate([be, be2])
            H = cap(LCurve(al, be, c))
            xt = float(H.X[-1])
            w = 4.0 * w / refine
    return H


def cap(H):
    c = H.c
    if len(H.al) and H.al[-1] * c - H.be[-1] > 1.0:
        Xv, Vv = H.vertices()
        m = float(np.max((1.0 - Vv[:-1]) / (c - Xv[:-1])))
        keep = H.al * c - H.be <= 1.0
        H = LCurve(np.concatenate([H.al[keep], [m]]), np.concatenate([H.be[keep], [m * c - 1.0]]), c)
    return H


def lines_sequence(P, J, K, keep=None, verbose=False, refine=0):
    """the float multi-rate ('lines') sequence from V_0 = 0 on [0, a]; returns the list of tops c_0..c_J and the
    curves with index in `keep` (all if keep is None)"""
    V = LCurve([], [], P.a)
    tops = [P.a]
    curves = {0: V}
    for j in range(1, J + 1):
        V = lines_step(P, V, K, refine=refine)
        tops.append(V.c)
        if keep is None or j in keep:
            curves[j] = V
        if verbose:
            print(j, V.c, len(V.al), flush=True)
    return tops, curves


# ------------------------------------------------------------------------------------------------------------
# the envelope sequence on grids (values at grid points; the piecewise-linear interpolant is ABOVE the curve, so the
# tops err DOWNWARDS) -- the other side of the sandwich
# ------------------------------------------------------------------------------------------------------------

def lower_hull_points(x, y):
    """indices of the lower convex hull of the points (x_i, y_i), x increasing"""
    st = []
    for i in range(len(x)):
        while len(st) >= 2:
            i1, i2 = st[-2], st[-1]
            if (y[i2] - y[i1]) * (x[i] - x[i1]) >= (y[i] - y[i1]) * (x[i2] - x[i1]):
                st.pop()
            else:
                break
        st.append(i)
    return np.array(st, dtype=int)


def grid_points(c, K):
    uni = np.linspace(0.0, c, K + 1)
    geo = c * (1.0 - np.geomspace(1e-12, 0.3, max(8, K // 2)))
    return np.unique(np.concatenate([uni, geo]))


def grid_sequence(P, J, K, keep=None, refine=0):
    """envelope sequence on grids: W_j is the piecewise-linear function through (x, w).  Returns tops and curves.
    The interpolant of exact values of a convex function is above it, and the lower hull of grid values is above
    the envelope: the curves err upwards and the tops DOWNWARDS (up to rounding).
    refine > 0: extra grid points around the vertex where the final segment to the top starts."""
    a = P.a
    x = np.array([0.0, a])
    w = np.array([0.0, 0.0])
    tops = [a]
    curves = {0: (x, w)}
    for j in range(1, J + 1):
        c = x[-1]
        if c + a * w[-1] >= a:                              # top: root of B + a W(B) = a
            lo, hi = 0.0, c
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if mid + a * float(np.interp(mid, x, w)) >= a:
                    hi = mid
                else:
                    lo = mid
            cn = lo                                         # just inside the regular region
            top_irregular = True
        else:
            cn = c
            top_irregular = False

        def values(g):
            f = np.minimum(1.0, P.sigma(g, np.interp(g, x, w)))
            f[g <= 0.0] = 0.0
            if top_irregular:
                f[g >= cn] = 1.0
            return f

        g = grid_points(cn, K)
        f = values(g)
        hull = lower_hull_points(g, f)
        if refine and len(hull) >= 3:
            wd = 4.0 * cn / K
            for _ in range(2):
                xt = g[hull[-2]]                            # the vertex where the last segment starts
                extra = np.linspace(max(xt - wd, 0.0), min(xt + wd, cn), refine + 2)[1:-1]
                g = np.unique(np.concatenate([g, extra]))
                f = values(g)
                hull = lower_hull_points(g, f)
                wd = 4.0 * wd / refine
        x, w = g[hull], f[hull]
        tops.append(cn)
        if keep is None or j in keep:
            curves[j] = (x, w)
    return tops, curves


def grid_M(x, w, g):
    g = np.atleast_1d(np.asarray(g, dtype=float))
    out = np.empty(g.shape)
    for k in range(0, len(g), 256):
        gg = g[k:k + 256]
        out[k:k + 256] = np.max(x[None, :] - gg[:, None] * w[None, :], axis=1)
    return out
