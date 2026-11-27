"""a6exact.py -- the referee's own RIGOROUS tools: interval arithmetic on integers, enclosures of exp and log by
their series with explicit remainders, enclosures of the two divergences of the cube pair, exact rounding of
rationals to doubles, an exact upper hull of lines, and a certified multi-rate sequence built with them.

Nothing here uses mpmath's interval arithmetic (the coordinator's z6_certified_tops.py does), and nothing is
imported from the coordinator's code.  What is trusted: Python integers and fractions.Fraction (exact), the
conversion Fraction(float) (exact), math.nextafter, and the correct rounding of float(Fraction).

Intervals: a pair of Python integers (lo, hi) in units of 2^-PREC; every operation rounds lo down and hi up.
"""
import math
from fractions import Fraction as Fr

PREC = 200
ONE = 1 << PREC
INF = float("inf")


class IV:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi):
        if lo > hi:
            raise ValueError("empty interval")
        self.lo, self.hi = lo, hi

    @staticmethod
    def of(x):
        if isinstance(x, IV):
            return x
        fr = Fr(x)                                             # exact for int, Fraction and float
        n, d = fr.numerator << PREC, fr.denominator
        return IV(n // d, -((-n) // d))

    def __add__(self, o):
        o = IV.of(o)
        return IV(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return IV(-self.hi, -self.lo)

    def __sub__(self, o):
        o = IV.of(o)
        return IV(self.lo - o.hi, self.hi - o.lo)

    def __rsub__(self, o):
        return IV.of(o) - self

    def __mul__(self, o):
        o = IV.of(o)
        ps = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return IV(min(ps) >> PREC, -((-max(ps)) >> PREC))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = IV.of(o)
        if o.lo <= 0 <= o.hi:
            raise ZeroDivisionError("interval division by an interval containing zero")
        if o.hi < 0:
            return (-self) / (-o)
        lo = min((x << PREC) // y for x in (self.lo, self.hi) for y in (o.lo, o.hi))
        hi = max(-((-(x << PREC)) // y) for x in (self.lo, self.hi) for y in (o.lo, o.hi))
        return IV(lo, hi)

    def __rtruediv__(self, o):
        return IV.of(o) / self

    def lower(self):
        return Fr(self.lo, ONE)

    def upper(self):
        return Fr(self.hi, ONE)

    def width(self):
        return Fr(self.hi - self.lo, ONE)

    def __repr__(self):
        return "IV[%.20g, %.20g]" % (float(self.lower()), float(self.upper()))


def _two_atanh(z):
    """enclosure of 2 atanh(z) = 2 sum_{k>=0} z^(2k+1)/(2k+1) for an interval z with |z| <= 1/2"""
    zmax = max(abs(z.lo), abs(z.hi))
    if zmax * 2 > ONE:
        raise ValueError("argument of the atanh series too large")
    z2 = z * z
    z2 = IV(max(z2.lo, 0), z2.hi)                              # a square is nonnegative
    term = z
    s = IV(0, 0)
    k = 0
    while True:
        s = s + term / (2 * k + 1)
        term = term * z2
        k += 1
        tmax = max(abs(term.lo), abs(term.hi))
        if tmax <= 4:                                          # |z|^(2k+1) <= 4 units of 2^-PREC
            break
        if k > 400:
            raise RuntimeError("atanh series does not converge")
    # remainder: |sum_{j>=k} z^(2j+1)/(2j+1)| <= |z|^(2k+1)/((2k+1)(1 - z^2)) <= (4/3)|z|^(2k+1) <= 2 tmax   (|z| <= 1/2)
    r = 2 * tmax + 1
    s = IV(s.lo - r, s.hi + r)
    return IV(2 * s.lo, 2 * s.hi)


LN2 = _two_atanh(IV.of(Fr(1, 3)))                               # ln 2 = 2 atanh(1/3)


def _log_point(v):
    """enclosure of ln(v / 2^PREC) for an integer v > 0"""
    if v <= 0:
        raise ValueError("log of a nonpositive number")
    k = v.bit_length() - PREC - 1                              # 2^k <= v/2^PREC < 2^(k+1)
    # m = v / 2^(PREC + k) in [1, 2); if m > 1.41422 shift once more so that m is in [0.7071, 1.4143]
    if k >= 0:
        m_lo, m_hi = v >> k, -((-v) >> k)
    else:
        m_lo = m_hi = v << (-k)
    if m_lo * 100000 > 141422 * ONE:
        k += 1
        if k >= 0:
            m_lo, m_hi = v >> k, -((-v) >> k)
        else:
            m_lo = m_hi = v << (-k)
    m = IV(m_lo, m_hi)
    z = (m - 1) / (m + 1)
    return LN2 * k + _two_atanh(z)


def log(x):
    """enclosure of ln(x) for an interval x > 0 (log is increasing: lower end from x.lo, upper end from x.hi)"""
    x = IV.of(x)
    if x.lo <= 0:
        raise ValueError("log of an interval that is not positive")
    return IV(_log_point(x.lo).lo, _log_point(x.hi).hi)


def exp(x):
    """enclosure of exp(x) for a rational or interval x >= 0 (Taylor series with the remainder of a geometric tail)"""
    x = IV.of(x)
    if x.lo < 0:
        raise ValueError("exp is implemented for nonnegative arguments only")
    xmax = Fr(x.hi, ONE)
    term = IV.of(1)
    s = IV(0, 0)
    k = 0
    while True:
        s = s + term
        k += 1
        term = term * x / k
        if k > 2 * xmax + 2 and term.hi <= 4:
            break
        if k > 5000:
            raise RuntimeError("exp series does not converge")
    # remainder sum_{j>=k} x^j/j! <= term_k / (1 - x/(k+1)) <= 2 term_k   (k + 1 > 2 x)
    return IV(s.lo, s.hi + 2 * term.hi + 1)


def kl(r, p):
    """enclosure of KL(r || p) = r ln(r/p) + (1 - r) ln((1 - r)/(1 - p)),  0 < r, p < 1"""
    r, p = IV.of(r), IV.of(p)
    return r * log(r / p) + (1 - r) * log((1 - r) / (1 - p))


def fl_up(fr):
    """the least double >= the rational fr"""
    fr = Fr(fr)
    d = float(fr)                                              # correctly rounded
    while Fr(d) < fr:
        d = math.nextafter(d, INF)
    while True:
        e = math.nextafter(d, -INF)
        if Fr(e) >= fr:
            d = e
        else:
            break
    return d


def fl_dn(fr):
    """the greatest double <= the rational fr"""
    fr = Fr(fr)
    d = float(fr)
    while Fr(d) > fr:
        d = math.nextafter(d, -INF)
    while True:
        e = math.nextafter(d, INF)
        if Fr(e) <= fr:
            d = e
        else:
            break
    return d


class CubeX:
    """rigorous constants of the cube pair for a rational slope u (given as a string or Fraction)"""

    def __init__(self, u):
        self.u = Fr(u)
        self.pu = 1 / (1 + exp(self.u))                        # interval for p_u = 1/(1 + e^u)
        self.half = IV.of(Fr(1, 2))
        self.a = kl(self.pu, self.half)                        # a = KL(p_u || 1/2)
        self.eps = kl(self.half, self.pu)                      # eps* = KL(1/2 || p_u)
        self.a_hi, self.a_lo = self.a.upper(), self.a.lower()
        self.eps_hi = self.eps.upper()
        self._cache = {}

    def pair(self, rho):
        """(E, TH) rationals with E >= KL(rho || p_u), TH >= KL(rho || 1/2), for a rational 0 < rho <= 1/2.
        Then TH >= theta(e) for every e >= E:  if rho >= p_u, theta(e) <= theta(KL(rho||p_u)) = KL(rho||1/2);
        if rho < p_u, KL(rho||1/2) > a >= theta(e)."""
        rho = Fr(rho)
        if not (0 < rho <= Fr(1, 2)):
            raise ValueError("rho must be in (0, 1/2]")
        if rho in self._cache:
            return self._cache[rho]
        if rho == Fr(1, 2):
            out = (self.eps_hi, Fr(0))
        else:
            e = kl(rho, self.pu)
            th = kl(rho, self.half)
            out = (e.upper(), max(Fr(0), th.upper()))
        if len(self._cache) < 200000:
            self._cache[rho] = out
        return out

    def valid_pair(self, e0, th0, rho):
        """True if the rational pair (e0, th0) is PROVED valid (th0 >= theta(e0)) by the witness rho"""
        if e0 <= 0 or th0 < 0:
            return False
        if e0 >= self.eps_hi:
            return True                                         # theta(e0) = 0 <= th0
        if rho is None:
            return False
        E, TH = self.pair(rho)
        return E <= e0 and TH <= th0


# ------------------------------------------------------------------------------------------------------------
# exact curves:  V(B) = max(0, max_i (al_i B - be_i)) on [0, c];  al, be, c doubles; all comparisons in Fractions
# ------------------------------------------------------------------------------------------------------------

def exact_hull(lines, c):
    """lines: iterable of (al, be) doubles.  Returns the list of hull lines (al, be) by increasing slope -- the lines
    of the upper envelope of the zero line and the given lines that are active somewhere on [0, c) -- and the list of
    exact activation points X (Fractions).  Lines with al <= 0 are ignored (they are below the zero line where they
    matter only if be < 0, which is refused)."""
    best = {}
    for al, be in lines:
        if be < 0:
            raise ValueError("a line with a positive value at zero")
        if al <= 0:
            continue
        if al not in best or be < best[al]:
            best[al] = be
    C = Fr(c)
    A, Bt = [Fr(0)], [Fr(0)]
    keep = [None]
    for al in sorted(best):
        a3, b3 = Fr(al), Fr(best[al])
        while len(A) >= 2:
            a1, b1, a2, b2 = A[-2], Bt[-2], A[-1], Bt[-1]
            if (b3 - b1) * (a2 - a1) <= (b2 - b1) * (a3 - a1):  # crossing(1,3) <= crossing(1,2): line 2 is never the maximum alone
                A.pop()
                Bt.pop()
                keep.pop()
            else:
                break
        A.append(a3)
        Bt.append(b3)
        keep.append((al, best[al]))
    out, X = [], []
    for i in range(1, len(A)):
        x = (Bt[i] - Bt[i - 1]) / (A[i] - A[i - 1])
        if x < C:
            out.append(keep[i])
            X.append(x)
        else:
            break
    return out, X


class XCurve:
    def __init__(self, lines, c):
        self.c = float(c)
        self.lines, self.X = exact_hull(lines, self.c)
        self.al = [l[0] for l in self.lines]
        self.be = [l[1] for l in self.lines]
        self._Xf = [float(x) for x in self.X]

    def val_exact(self, B):
        B = Fr(B)
        v = Fr(0)
        for al, be in self.lines:
            w = Fr(al) * B - Fr(be)
            if w > v:
                v = w
        return v

    def active(self, B):
        """index of a line that attains V(B) up to rounding (-1: the zero line) -- float, used for choices only"""
        import bisect
        return bisect.bisect_right(self._Xf, B) - 1

    def val_float(self, B):
        i = self.active(B)
        return max(0.0, self.al[i] * B - self.be[i]) if i >= 0 else 0.0

    def vertices(self):
        """exact vertices (X, V(X)): 0, the activation points, c"""
        C = Fr(self.c)
        vs = [(Fr(0), Fr(0))]
        for (al, be), x in zip(self.lines, self.X):
            vs.append((x, Fr(al) * x - Fr(be)))
        if self.lines:
            vs.append((C, Fr(self.al[-1]) * C - Fr(self.be[-1])))
        else:
            vs.append((C, Fr(0)))
        return vs

    def M_exact(self, g):
        G = Fr(g)
        return max(x - G * v for x, v in self.vertices())


def exact_top(V, abar):
    """a double c' <= V.c with c' = V.c or c' + abar V(c') >= abar EXACTLY (abar a double >= a).  Float bisection,
    exact verification."""
    A = Fr(abar)
    C = Fr(V.c)
    if C + A * V.val_exact(V.c) < A:
        return V.c
    lo, hi = 0.0, V.c
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if mid + abar * V.val_float(mid) >= abar:
            hi = mid
        else:
            lo = mid
    c = hi
    for _ in range(64):                                         # walk down while the exact inequality holds
        d = math.nextafter(c, -INF)
        if d > 0 and Fr(d) + A * V.val_exact(d) >= A:
            c = d
        else:
            break
    for _ in range(4096):
        if Fr(c) + A * V.val_exact(c) >= A:
            return min(c, V.c)
        c = math.nextafter(c, INF)
    raise RuntimeError("top not verified")


def exact_cap(lines, c):
    """lines: the lines of a curve H on [0, c].  If H(c) > 1: the lines with value <= 1 at c, plus a line through
    (c, <= 1) that is below H on [0, c] (slope: the largest chord slope from a vertex of H to (c, 1), rounded up)."""
    H = XCurve(lines, c)
    C = Fr(c)
    if H.val_exact(c) <= 1:
        return H
    vs = H.vertices()
    mstar = max((1 - v) / (C - x) for x, v in vs[:-1])
    m = fl_up(mstar)
    bL = fl_up(Fr(m) * C - 1)
    kept = [(al, be) for al, be in H.lines if Fr(al) * C - Fr(be) <= 1]
    H2 = XCurve(kept + [(m, bL)], c)
    if H2.val_exact(c) > 1:
        raise RuntimeError("cap failed")
    return H2


def own_lines_at(PX, Pf, V, Bs):
    """the referee's certified lines for the step from the curve V, at the sample points Bs (an array of doubles).
    PX: CubeX (rigorous), Pf: a6lib.Cube (float, for the choice of the line and of the rate only).
    Every returned line (al, be) is, on B >= 0, below  [B - TH (1 - l(B))]/E  for a line l of V (or the zero line)
    and a pair (E, TH) PROVED valid by PX.pair; slope rounded down, beta rounded up, exactly (Fractions)."""
    import bisect
    import numpy as np
    Bs = np.asarray(Bs, dtype=float)
    idx = np.array([bisect.bisect_right(V._Xf, float(B)) - 1 for B in Bs], dtype=int)
    al_ = np.array(V.al if V.al else [0.0])
    be_ = np.array(V.be if V.be else [0.0])
    a0 = np.where(idx >= 0, al_[np.maximum(idx, 0)], 0.0)
    b0 = np.where(idx >= 0, be_[np.maximum(idx, 0)], 0.0)
    s = np.maximum(0.0, a0 * Bs - b0)
    ok = (s < 1.0) & (Bs < (1.0 - s) * Pf.a * (1 - 1e-12)) & (Bs > 0)
    t = Pf.sigma_t(np.where(ok, Bs, 0.0), np.where(ok, s, 0.0))          # float choice of the rate
    rho = Pf.rho_of_t(t)
    out = []
    for k in range(len(Bs)):
        if not ok[k]:
            continue
        r = float(rho[k])
        if not (0.0 < r <= 0.5):
            continue
        E, TH = PX.pair(r)
        A0, B0 = Fr(float(a0[k])), Fr(float(b0[k]))
        al = fl_dn((1 + TH * A0) / E)
        be = fl_up(TH * (1 + B0) / E)
        if al > 0:
            out.append((al, be))
    return out


def own_step(PX, Pf, V, abar, K, sampler, refine=0):
    """one step of the referee's certified multi-rate sequence: exact top, certified lines at the sample points,
    exact hull, exact cap.  refine > 0: a second pass with that many extra sample points around the point where the
    cap line leaves the curve (a matter of quality only: any set of sample points gives valid lines)."""
    import numpy as np
    c = exact_top(V, abar)
    lines = own_lines_at(PX, Pf, V, sampler(c, K))
    H = exact_cap(lines, c)
    if refine and H.lines and Fr(H.al[-1]) * Fr(c) - Fr(H.be[-1]) > Fr(999999, 1000000):
        xt = float(H.X[-1])                                              # the cap line is the last hull line
        w = 4.0 * c / K
        extra = np.linspace(max(xt - w, 0.0), min(xt + w, c), refine + 2)[1:-1]
        lines = lines + own_lines_at(PX, Pf, V, extra)
        H = exact_cap(lines, c)
    assert H.val_exact(c) <= 1 and all(be >= 0 for be in H.be) and all(al > 0 for al in H.al)
    return H
