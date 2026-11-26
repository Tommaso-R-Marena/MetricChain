"""Referee B -- own definitions (independent of rlib.py).

A pair is given by theta itself (convex, nonincreasing on (0, inf), a = theta(0+) finite) and its right derivative.
Everything is computed from the DEFINITIONS of R_REPORT.md:
    Sigma(B, s) = sup_{e > 0} [B - (1 - s) theta(e)]/e          (sigma_direct: grid scan + golden section on the ratio;
                                                                 sigma: bisection on the tangent intercept
                                                                 theta(e) - e theta'(e) = B/(1 - s), then the ratio)
    J(t)        = inf_{e > 0} [(1 - t) theta(e) + t e]          (J_direct: grid scan + golden section)
No use is made of J in the computation of Sigma (the report's (Sigma5) is checked against these, not assumed).
"""
import math
import numpy as np

GR = (math.sqrt(5.0) - 1.0) / 2.0


def golden_max(f, lo, hi, it=90):
    x1, x2 = hi - GR * (hi - lo), lo + GR * (hi - lo)
    f1, f2 = f(x1), f(x2)
    for _ in range(it):
        if f1 >= f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - GR * (hi - lo)
            f1 = f(x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + GR * (hi - lo)
            f2 = f(x2)
    return (x1, f1) if f1 >= f2 else (x2, f2)


class TPair:
    def __init__(self, name, theta, dtheta, a, e_lo=1e-14, e_hi=1e3, finite_slope0=None):
        """theta, dtheta: scalar functions on (0, inf) (dtheta = right derivative).  finite_slope0 = |theta'(0+)| if it
        is finite (then the boundary B = (1 - s) a is regular), else None."""
        self.name, self.theta, self.dtheta, self.a = name, theta, dtheta, a
        self.e_lo, self.e_hi = e_lo, e_hi
        self.finite_slope0 = finite_slope0
        self._zgrid = np.linspace(math.log(e_lo), math.log(e_hi), 2401)
        self._egrid = np.exp(self._zgrid)
        self._thgrid = np.array([theta(float(e)) for e in self._egrid])

    # ---------- the slope map, straight from the definition
    def sigma_direct(self, B, s):
        """sup_e [B - (1 - s) theta(e)]/e by a scan of 2401 log-spaced points and golden section in log e around the
        best one (the ratio is quasi-concave).  Returns inf if B > (1 - s) a (or = with infinite slope at 0)."""
        if B > (1.0 - s) * self.a or (B == (1.0 - s) * self.a and self.finite_slope0 is None and B > 0):
            return math.inf
        vals = (B - (1.0 - s) * self._thgrid) / self._egrid
        i = int(np.argmax(vals))
        lo, hi = self._zgrid[max(i - 1, 0)], self._zgrid[min(i + 1, len(vals) - 1)]
        f = lambda z: (B - (1.0 - s) * self.theta(math.exp(z))) / math.exp(z)
        z, v = golden_max(f, lo, hi)
        v = max(v, float(vals[i]), 0.0)
        if self.finite_slope0 is not None:          # limit e -> 0 of the ratio when B = (1 - s) a
            if B == (1.0 - s) * self.a:
                v = max(v, (1.0 - s) * self.finite_slope0)
        return v

    def argmax_direct(self, B, s):
        vals = (B - (1.0 - s) * self._thgrid) / self._egrid
        i = int(np.argmax(vals))
        lo, hi = self._zgrid[max(i - 1, 0)], self._zgrid[min(i + 1, len(vals) - 1)]
        f = lambda z: (B - (1.0 - s) * self.theta(math.exp(z))) / math.exp(z)
        z, v = golden_max(f, lo, hi)
        return math.exp(z), v

    def sigma(self, B, s):
        """the same supremum through the tangent point: the intercept theta(e) - e theta'(e) of the tangent at e is
        nonincreasing in e; bisection for intercept = B/(1 - s); then the RATIO at that point (second-order
        insensitive to the error of the point)."""
        if s >= 1.0:
            return math.inf if B > 0 else 0.0
        if B > (1.0 - s) * self.a:
            return math.inf
        if B == (1.0 - s) * self.a:
            if self.finite_slope0 is None:
                return math.inf if B > 0 else 0.0
            return max((1.0 - s) * self.finite_slope0, self._sigma_tan(B, s))
        return self._sigma_tan(B, s)

    def _sigma_tan(self, B, s):
        y = B / (1.0 - s)
        lo, hi = self.e_lo, self.e_hi
        th, dth = self.theta, self.dtheta
        if th(hi) - hi * dth(hi) >= y:              # the tangent intercept never comes down to y: sup at infinity
            return max(0.0, (B - (1.0 - s) * th(hi)) / hi)
        for _ in range(200):
            mid = math.sqrt(lo * hi)
            if th(mid) - mid * dth(mid) > y:
                lo = mid
            else:
                hi = mid
            if hi / lo < 1.0 + 4e-16:
                break
        e = hi
        return max(0.0, (B - (1.0 - s) * th(e)) / e, (B - (1.0 - s) * th(lo)) / lo)

    # ---------- the dual function, straight from the definition
    def J_direct(self, t):
        vals = (1.0 - t) * self._thgrid + t * self._egrid
        i = int(np.argmin(vals))
        lo, hi = self._zgrid[max(i - 1, 0)], self._zgrid[min(i + 1, len(vals) - 1)]
        f = lambda z: -((1.0 - t) * self.theta(math.exp(z)) + t * math.exp(z))
        z, v = golden_max(f, lo, hi)
        return min(-v, float(vals[i]))

    # ---------- constants
    def fixed_point(self):
        lo, hi = self.e_lo, self.e_hi
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if self.theta(mid) > mid:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def setup(self, d2theta_h=None):
        """h, r = -theta'(h), L, vartheta = theta''(h)/(1 + r)^3 (theta'' by central difference of dtheta unless given)."""
        self.h = self.fixed_point()
        self.r = -self.dtheta(self.h)
        self.L = self.r / (1.0 + self.r)
        if d2theta_h is None:
            d = 1e-6 * self.h
            d2theta_h = (self.dtheta(self.h + d) - self.dtheta(self.h - d)) / (2 * d)
        self.th2 = d2theta_h
        self.vartheta = d2theta_h / (1.0 + self.r) ** 3
        self.cstar = math.pi * self.h * math.sqrt(2.0 * self.vartheta) if self.vartheta > 0 else float("nan")
        self.c2 = self.cstar ** 2
        return self

    # ---------- orbits
    def orbit(self, B, n):
        out = [0.0]
        for _ in range(n):
            s = out[-1]
            out.append(self.sigma(B, s) if math.isfinite(s) else math.inf)
        return out

    def p(self, B, n):
        s = 0.0
        for _ in range(n):
            s = self.sigma(B, s)
            if not math.isfinite(s):
                return math.inf
        return s

    def passage(self, B, level, nmax=10 ** 8):
        s, n = 0.0, 0
        while s <= level:
            s = self.sigma(B, s)
            n += 1
            if n > nmax:
                return None
        return n

    def B_inf(self, k, tol=1e-15):
        """sup{B : p_k(B) < inf} by bisection on [h, a]."""
        lo, hi = self.h, self.a
        while hi - lo > tol * max(1.0, hi):
            mid = 0.5 * (lo + hi)
            if mid <= lo or mid >= hi:          # no representable point in between
                break
            if math.isfinite(self.p(mid, k)):
                lo = mid
            else:
                hi = mid
        return lo


# ---------------------------------------------------------------------------------------------------- the pairs
def gauss():
    th = lambda e: (1.0 - math.sqrt(e)) ** 2 if e < 1.0 else 0.0
    dth = lambda e: -(1.0 - math.sqrt(e)) / math.sqrt(e) if e < 1.0 else 0.0
    return TPair("Gaussian (1 - sqrt e)^2", th, dth, 1.0)


def quad():
    """theta = (1 - e)_+^2 : finite slope 2 at zero.  Closed form: Sigma = 2 (1 - s)(1 - sqrt(1 - B/(1 - s)))."""
    th = lambda e: (1.0 - e) ** 2 if e < 1.0 else 0.0
    dth = lambda e: -2.0 * (1.0 - e) if e < 1.0 else 0.0
    return TPair("quadratic (1 - e)_+^2", th, dth, 1.0, finite_slope0=2.0)


def cubroot():
    """theta = (1 - sqrt e)_+^3 : infinite slope at zero, like the Gaussian pair and the cube; not one of the author's."""
    th = lambda e: (1.0 - math.sqrt(e)) ** 3 if e < 1.0 else 0.0
    dth = lambda e: -1.5 * (1.0 - math.sqrt(e)) ** 2 / math.sqrt(e) if e < 1.0 else 0.0
    return TPair("(1 - sqrt e)_+^3", th, dth, 1.0)


def expo(c=2.0):
    """theta = exp(-c e): never zero, finite slope c at zero."""
    th = lambda e: math.exp(-c * e)
    dth = lambda e: -c * math.exp(-c * e)
    return TPair("exp(-%g e)" % c, th, dth, 1.0, e_hi=1e3, finite_slope0=c)


def shifted():
    """theta = 0.1 + 0.9 exp(-3 e): theta(inf) = 0.1 > 0, so J(0) = 0.1 > 0."""
    th = lambda e: 0.1 + 0.9 * math.exp(-3.0 * e)
    dth = lambda e: -2.7 * math.exp(-3.0 * e)
    return TPair("0.1 + 0.9 exp(-3 e)", th, dth, 1.0, finite_slope0=2.7)


def cube(u):
    """the cube from the definitions: theta_na(e) = KL(rho_e || 1/2), KL(rho_e || p_u) = e, rho_e in [p_u, 1/2]."""
    pu = 1.0 / (1.0 + math.exp(u))
    kl = lambda x, y: x * math.log(x / y) + (1 - x) * math.log((1 - x) / (1 - y))
    estar = kl(0.5, pu)

    def rho(e):
        lo, hi = pu, 0.5
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if kl(mid, pu) <= e:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def th(e):
        return kl(rho(e), 0.5) if e < estar else 0.0

    def dth(e):
        if e >= estar:
            return 0.0
        x = rho(e)
        lg = math.log(x / (1 - x))
        return lg / (lg + u)            # (d/drho KL(rho||1/2)) / (d/drho KL(rho||p_u))

    return TPair("cube u = %g (from KL definitions)" % u, th, dth, kl(pu, 0.5), e_lo=1e-13)


def kink_author():
    th = lambda e: max(1.0 - 3.0 * e, 0.5 - e, 0.0)
    dth = lambda e: -3.0 if e < 0.25 else (-1.0 if e < 0.5 else 0.0)
    return TPair("kinked max(1-3e, 1/2-e, 0)", th, dth, 1.0, finite_slope0=3.0)


def kink_smooth(m=0.4):
    """theta = max((1 - sqrt e)^2, 1/4 + m (1/4 - e)) (and 0 beyond 1): strictly convex pieces, kink at h = 1/4 with
    subdifferential [-1, -m]."""
    def th(e):
        g = (1.0 - math.sqrt(e)) ** 2 if e < 1.0 else 0.0
        return max(g, 0.25 + m * (0.25 - e), 0.0)

    def dth(e):
        g = (1.0 - math.sqrt(e)) ** 2 if e < 1.0 else 0.0
        l = 0.25 + m * (0.25 - e)
        if g > l or (g == l and e > 0.26):
            return -(1.0 - math.sqrt(e)) / math.sqrt(e) if e < 1.0 else 0.0
        return -m if l > 0 else 0.0
    return TPair("kink: max((1-sqrt e)^2, 1/4 + %g (1/4 - e))" % m, th, dth, 1.0)


def chord(e1=0.16, e2=0.36):
    """Gaussian theta with the arc over [e1, e2] replaced by its chord: theta is AFFINE near its fixed point
    (J has a corner at its maximum: the case p = 1 of the heuristic classification)."""
    t1, t2 = (1 - math.sqrt(e1)) ** 2, (1 - math.sqrt(e2)) ** 2
    sl = (t2 - t1) / (e2 - e1)

    def th(e):
        if e1 <= e <= e2:
            return t1 + sl * (e - e1)
        return (1.0 - math.sqrt(e)) ** 2 if e < 1.0 else 0.0

    def dth(e):
        if e1 <= e < e2:
            return sl
        return -(1.0 - math.sqrt(e)) / math.sqrt(e) if e < 1.0 else 0.0
    P = TPair("Gaussian with chord on [%g, %g]" % (e1, e2), th, dth, 1.0)
    P.e1, P.e2, P.sl = e1, e2, sl
    return P
