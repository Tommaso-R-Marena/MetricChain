"""Workstream R (the rate of the level recursion) -- common definitions.

A *pair* is given by its dual function J on [0, 1]:
    J(t) = inf_{e > 0} [ (1 - t) theta_na(e) + t e ],
concave, J(0) = J(1) = 0, h = max J = J(L), a = lim_{t -> 1} J(t)/(1 - t) = theta_na(0+).
The minimiser e*(t) and theta_na(e*(t)) are  e* = J + (1 - t) J',  theta_na(e*) = J - t J'.

The slope map   Sigma(B, s) = sup_{e > 0} [B - (1 - s) theta_na(e)]/e   (finite iff B < (1 - s) a)  is
    Sigma(B, s) = t' (1 - s)/(1 - t'),     Q(t') = B/(1 - s),    Q(t) = J(t)/(1 - t)   (increasing from 0 to a),
with partial derivatives  d/dB = 1/e*(t'),  d/ds = theta_na(e*(t'))/e*(t').
"""
import math


class Pair:
    name = "abstract"

    def J(self, t):
        raise NotImplementedError

    def dJ(self, t):
        raise NotImplementedError

    def Q(self, t):
        return self.J(t) / (1.0 - t)

    def Qinv(self, y):
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if self.Q(mid) < y:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def setup(self):
        # maximiser of J by bisection on J'
        lo, hi = 1e-12, 1 - 1e-12
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if self.dJ(mid) > 0:
                lo = mid
            else:
                hi = mid
        self.L = 0.5 * (lo + hi)
        self.h = self.J(self.L)
        d = 1e-4
        self.J2 = (self.J(self.L + d) - 2 * self.J(self.L) + self.J(self.L - d)) / d ** 2
        self.vartheta = -1.0 / self.J2           # = theta_hint''(0)
        self.const = 2 * math.pi ** 2 * self.h ** 2 * self.vartheta
        return self

    def regular(self, B, s):
        return s < 1.0 and B < (1.0 - s) * self.a

    def sigma(self, B, s):
        if not self.regular(B, s):
            return math.inf
        tp = self.Qinv(B / (1.0 - s))
        return tp * (1.0 - s) / (1.0 - tp)

    def sigma_grad(self, B, s):
        """(Sigma, dSigma/dB, dSigma/ds) at a regular point."""
        tp = self.Qinv(B / (1.0 - s))
        e = self.J(tp) + (1 - tp) * self.dJ(tp)
        th = self.J(tp) - tp * self.dJ(tp)
        return tp * (1.0 - s) / (1.0 - tp), 1.0 / e, th / e

    def orbit(self, B, n):
        """p_0 = 0, p_{j+1} = Sigma(B, p_j), j = 0..n  (inf once irregular)."""
        out = [0.0]
        for _ in range(n):
            s = out[-1]
            out.append(self.sigma(B, s) if math.isfinite(s) else math.inf)
        return out

    def orbit_with_slope(self, B, n):
        """(p_n(B), dp_n/dB) by the chain rule; (inf, inf) once irregular."""
        p, dp = 0.0, 0.0
        for _ in range(n):
            if not self.regular(B, p):
                return math.inf, math.inf
            p, gB, gs = self.sigma_grad(B, p)
            dp = gB + gs * dp
        return p, dp

    def passage(self, B, level, nmax=10 ** 7):
        """least n with p_n(B) > level."""
        s, n = 0.0, 0
        while s <= level:
            s = self.sigma(B, s)
            n += 1
            if n > nmax:
                return None
        return n


class Gauss(Pair):
    name = "Gaussian pair"
    a = 1.0

    def J(self, t):
        return t - t * t

    def dJ(self, t):
        return 1 - 2 * t

    def Qinv(self, y):
        return y

    def theta_na(self, e):
        return (1 - math.sqrt(e)) ** 2 if e < 1 else 0.0


class Cube(Pair):
    def __init__(self, u):
        self.u = u
        self.name = "cube u = %g" % u
        self.lam_u = math.log(2 / (1 + math.exp(-u)))
        self.a = -math.log(2 / (1 + math.exp(u))) - 0.0
        # a = KL(p_u || 1/2) = ln 2 - H(p_u); equivalently lim J/(1-t) = u Lambda'(u) ... computed below
        pu = 1 / (1 + math.exp(u))
        self.a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)

    def Lam(self, v):
        return math.log(2 / (1 + math.exp(-v)))

    def J(self, t):
        return self.Lam(t * self.u) - t * self.lam_u

    def dJ(self, t):
        return self.u / (1 + math.exp(t * self.u)) - self.lam_u

    def theta_na(self, e):
        """KL(rho || 1/2) at the rho in [p_u, 1/2] with KL(rho || p_u) = e  (0 beyond eps* = ln cosh(u/2))."""
        pu = 1 / (1 + math.exp(self.u))
        kl = lambda x, y: x * math.log(x / y) + (1 - x) * math.log((1 - x) / (1 - y))
        if e >= kl(0.5, pu):
            return 0.0
        lo, hi = pu, 0.5
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if kl(mid, pu) <= e:
                lo = mid
            else:
                hi = mid
        return kl(0.5 * (lo + hi), 0.5)


class Kinked(Pair):
    """theta_na = max(1 - 3e, (1 - e)/3 ... ) -- a convex piecewise-linear decreasing function with a KINK at its fixed
    point: theta_na(e) = max(1 - 3 e, 1/2 - e, 0) has theta_na(1/4) = 1/4, slopes -3 and -1 at h = 1/4.
    J(t) = min over the vertices e in {0+, 1/4, 1/2, infinity}: J(t) = min((1 - t), 1/4, t/2) -> flat maximum on
    [1/2, 3/4]."""
    name = "kinked pair"
    a = 1.0

    def J(self, t):
        return min(1.0 - t, 0.25, 0.5 * t)

    def dJ(self, t):
        return 0.5 if t < 0.5 else (0.0 if t < 0.75 else -1.0)

    def theta_na(self, e):
        return max(1 - 3 * e, 0.5 - e, 0.0)

    def regular(self, B, s):
        return s < 1.0 and B <= (1.0 - s) * self.a          # finite slope 3 at zero: the boundary is regular

    def sigma(self, B, s):
        if not self.regular(B, s):
            return math.inf
        # theta_na is piecewise linear: the supremum over e is attained at a vertex (1/4, 1/2), or is the limit e -> 0
        # (value 3(1 - s) when B = (1 - s) a), or 0 (e -> infinity)
        v = max(0.0, (B - (1 - s) * 0.25) / 0.25, B / 0.5)
        if B == (1.0 - s) * self.a:
            v = max(v, 3 * (1 - s))
        return v
