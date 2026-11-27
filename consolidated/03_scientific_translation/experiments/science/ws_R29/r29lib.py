#!/usr/bin/env python3
"""r29lib.py -- own routines of workstream R29 (science division).  Nothing here imports the theory division's code.

Contents
  cap_memory, finish            the resource rules of the brief (3 GB address space; peak memory in the last line)
  DI                            interval arithmetic of my own on dyadic rationals (Python integers scaled by 2^-P),
                                outward rounding by floor/ceil; +, -, *, / (positive divisor), log, exp of a rational
  CubeDI                        rigorous enclosures for the cube pair: p_u, a, eps*, KL(r || p_u), KL(r || 1/2)
  CubeMP                        the cube pair in mpmath (plain multiprecision, NOT intervals): theta_na, J, Sigma, h, L, ...
  upper_hull                    exact upper envelope of the zero line and lines alpha*B - beta on [0, c]  (Fractions)
  PL                            a convex piecewise-linear curve V = max(0, max_i(alpha_i B - beta_i)) on [0, c], exact
  build_step / check_step       one step of a multi-rate sequence (Z_ADDENDUM Proposition A13) with explicit
                                certificates, and an independent exact checker of such a step

Conventions.  A line is a pair (alpha, beta) of Fractions and stands for B -> alpha*B - beta.  The pair of exponent
functions is that of the uniform cube with slope u:  p_u = 1/(1 + e^u),
    theta_na(e) = min{ KL(rho || 1/2) : KL(rho || p_u) <= e },      a = KL(p_u || 1/2),
so for ANY rho in (0, 1):   e' >= KL(rho || p_u)  and  th >= KL(rho || 1/2)   imply   th >= theta_na(e').
"""
import math
import resource
import sys
import time
from fractions import Fraction as Fr

_T0 = time.time()


def cap_memory(gb=3.0):
    lim = int(gb * 1024 ** 3)
    resource.setrlimit(resource.RLIMIT_AS, (lim, lim))


def finish(tag=""):
    """the last line of every script: wall time and peak resident memory"""
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    print("R29-END %s wall %.1f s; address-space cap 3 GB; peak RSS %.1f MB" % (tag, time.time() - _T0, peak), flush=True)


# ----------------------------------------------------------------------------------------------------------------
#  DI: dyadic interval arithmetic with integers.  The interval is [lo, hi] * 2^-P, lo <= hi integers.
# ----------------------------------------------------------------------------------------------------------------
class DI:
    __slots__ = ("lo", "hi")
    P = 256

    def __init__(self, lo, hi):
        if lo > hi:
            raise ValueError("DI: empty interval")
        self.lo, self.hi = lo, hi

    # -- constructors
    @staticmethod
    def of(q):
        """enclosure of a rational number (int, Fraction, or a float taken exactly)"""
        if isinstance(q, DI):
            return q
        q = Fr(q)
        num, den = q.numerator << DI.P, q.denominator
        return DI(num // den, -((-num) // den))

    # -- exact endpoints
    def lo_fr(self):
        return Fr(self.lo, 1 << DI.P)

    def hi_fr(self):
        return Fr(self.hi, 1 << DI.P)

    def width_fr(self):
        return Fr(self.hi - self.lo, 1 << DI.P)

    def mid_float(self):
        return float(Fr(self.lo + self.hi, 1 << (DI.P + 1)))

    # -- arithmetic
    def __neg__(self):
        return DI(-self.hi, -self.lo)

    def __add__(self, o):
        o = DI.of(o)
        return DI(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __sub__(self, o):
        o = DI.of(o)
        return DI(self.lo - o.hi, self.hi - o.lo)

    def __rsub__(self, o):
        return DI.of(o) - self

    def __mul__(self, o):
        o = DI.of(o)
        ps = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return DI(min(ps) >> DI.P, -((-max(ps)) >> DI.P))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = DI.of(o)
        if o.lo <= 0:
            raise ZeroDivisionError("DI: divisor must be a positive interval")
        a, b = self.lo << DI.P, self.hi << DI.P
        lo = min(a // o.lo, a // o.hi)
        hi = max(-((-b) // o.lo), -((-b) // o.hi))
        return DI(lo, hi)

    def __rtruediv__(self, o):
        return DI.of(o) / self

    # -- elementary functions
    @staticmethod
    def _atanh_pos(z, nterms, upper):
        """for an integer 0 <= z <= 2/5 * 2^P (the number z 2^-P): a lower bound (upper=False) or an upper bound
        (upper=True) of atanh(z 2^-P) * 2^P, by the series sum z^(2i+1)/(2i+1) with every operation rounded down
        (resp. up) and, for the upper bound, the remainder  z^(2n+1)/((2n+1)(1 - z^2)) <= (25/21) z^(2n+1)/(2n+1)."""
        P = DI.P
        if z == 0:
            return 0
        if not upper:
            z2 = (z * z) >> P
            p, total = z, z
            for i in range(1, nterms):
                p = (p * z2) >> P
                total += p // (2 * i + 1)
            return total
        z2 = -((-(z * z)) >> P)
        p, total = z, z
        for i in range(1, nterms):
            p = -((-(p * z2)) >> P)
            total += -((-p) // (2 * i + 1))
        p = -((-(p * z2)) >> P)                                   # an upper bound of z^(2n+1)
        total += -((-p * 25) // (21 * (2 * nterms + 1))) + 1
        return total

    @staticmethod
    def _atanh(z, nterms):
        """enclosure of atanh(z) for an interval z with |z| <= 2/5 that does not straddle zero (or is zero)"""
        one = 1 << DI.P
        if 5 * max(abs(z.lo), abs(z.hi)) > 2 * one:
            raise ValueError("DI._atanh: |z| > 2/5")
        if z.lo >= 0:
            return DI(DI._atanh_pos(z.lo, nterms, False), DI._atanh_pos(z.hi, nterms, True))
        if z.hi <= 0:                                             # atanh is odd
            return DI(-DI._atanh_pos(-z.lo, nterms, True), -DI._atanh_pos(-z.hi, nterms, False))
        return DI(-DI._atanh_pos(-z.lo, nterms, True), DI._atanh_pos(z.hi, nterms, True))

    _LN2 = None
    _LN2_P = None

    @staticmethod
    def ln2():
        if DI._LN2 is None or DI._LN2_P != DI.P:
            n = int(DI.P / (2 * math.log2(3.0))) + 6
            DI._LN2 = DI._atanh(DI.of(Fr(1, 3)), n) * DI.of(2)
            DI._LN2_P = DI.P
        return DI._LN2

    @staticmethod
    def _log_point(n):
        """enclosure of ln(n * 2^-P) for an integer n > 0"""
        if n <= 0:
            raise ValueError("DI.log: argument not positive")
        k = n.bit_length() - DI.P - 1                      # n 2^-P = m 2^k with m in [1, 2), m = n / 2^(P + k)
        sh = DI.P + k
        big = (3 * n >= (4 << sh)) if sh >= 0 else (3 * (n << -sh) >= 4)
        if big:
            k += 1                                         # now m in [2/3, 4/3)
        sh = DI.P + k
        if sh >= 0:
            num, den = n - (1 << sh), n + (1 << sh)
        else:
            num, den = (n << -sh) - 1, (n << -sh) + 1
        z = DI.of(Fr(num, den))                            # |z| <= 1/5
        nterms = int(DI.P / (2 * math.log2(5.0))) + 6
        return DI.of(k) * DI.ln2() + DI._atanh(z, nterms) * DI.of(2)

    def log(self):
        if self.lo <= 0:
            raise ValueError("DI.log: interval not positive")
        return DI(DI._log_point(self.lo).lo, DI._log_point(self.hi).hi)

    @staticmethod
    def exp_rational(q):
        """enclosure of exp(q) for a rational 0 <= q <= 8 (Taylor series with the remainder bound of a geometric series)"""
        q = Fr(q)
        if not (0 <= q <= 8):
            raise ValueError("DI.exp_rational: argument out of range")
        Q = DI.of(q)
        N = 40 + int(DI.P / 2)
        term, total = DI.of(1), DI.of(1)
        for k in range(1, N + 1):
            term = term * Q / DI.of(k)
            total = total + term
        # remainder sum_{k > N} q^k/k!  <=  term_N * (q/(N+1)) / (1 - q/(N+2))
        rem = term * Q / DI.of(N + 1) / (DI.of(1) - Q / DI.of(N + 2))
        return DI(total.lo, total.hi + max(rem.hi, 0) + 1)

    def __repr__(self):
        return "DI[%.17g, %.17g; width %.2e]" % (float(self.lo_fr()), float(self.hi_fr()), float(self.width_fr()))


def ceil_dyadic(q, bits):
    """the least multiple of 2^-bits that is >= the Fraction q"""
    q = Fr(q)
    return Fr(-((-q.numerator << bits) // q.denominator), 1 << bits)


def floor_dyadic(q, bits):
    """the largest multiple of 2^-bits that is <= the Fraction q"""
    q = Fr(q)
    return Fr((q.numerator << bits) // q.denominator, 1 << bits)


# ----------------------------------------------------------------------------------------------------------------
#  the cube pair with rigorous enclosures
# ----------------------------------------------------------------------------------------------------------------
class CubeDI:
    """rigorous enclosures for the cube of slope u (a rational given as a string or a Fraction)"""

    def __init__(self, u):
        self.u = Fr(u)
        self.EU = DI.exp_rational(self.u)
        self.PU = DI.of(1) / (DI.of(1) + self.EU)
        self.HALF = DI.of(Fr(1, 2))
        self.A = self.kl(self.PU, self.HALF)                       # a = KL(p_u || 1/2)
        self.ESTAR = self.kl(self.HALF, self.PU)                   # eps* = KL(1/2 || p_u) = ln cosh(u/2)
        self._cache = {}

    @staticmethod
    def kl(r, p):
        r, p = DI.of(r), DI.of(p)
        one = DI.of(1)
        return r * (r / p).log() + (one - r) * ((one - r) / (one - p)).log()

    def pair_enclosures(self, rho):
        """(E, TH): enclosures of KL(rho || p_u) and KL(rho || 1/2) for an exact rational 0 < rho < 1"""
        rho = Fr(rho)
        if rho not in self._cache:
            if not (0 < rho < 1):
                raise ValueError("rho must be in (0, 1)")
            if rho == Fr(1, 2):
                self._cache[rho] = (self.ESTAR, DI(0, 0))
            else:
                r = DI.of(rho)
                self._cache[rho] = (self.kl(r, self.PU), self.kl(r, self.HALF))
        return self._cache[rho]

    def certified_pair(self, rho, bits=96):
        """(e', th) Fractions, multiples of 2^-bits, with e' >= KL(rho || p_u) > 0 and th >= KL(rho || 1/2) >= 0:
        then th >= theta_na(e') because rho is feasible in the minimum that defines theta_na(e')."""
        E, TH = self.pair_enclosures(rho)
        e = ceil_dyadic(E.hi_fr(), bits)
        th = max(Fr(0), ceil_dyadic(TH.hi_fr(), bits))
        if e <= 0:
            raise ValueError("certified_pair: e' not positive")
        return e, th

    def abar(self, bits=96):
        return ceil_dyadic(self.A.hi_fr(), bits)

    def alow(self, bits=96):
        return floor_dyadic(self.A.lo_fr(), bits)


# ----------------------------------------------------------------------------------------------------------------
#  the cube pair in plain multiprecision (mpmath mp): for estimates and ground truth, NOT rigorous
# ----------------------------------------------------------------------------------------------------------------
class CubeMP:
    def __init__(self, u, dps=40):
        import mpmath
        self.mp = mpmath.mp
        self.mpmath = mpmath
        self.mp.dps = dps
        mpf = mpmath.mpf
        self.u = mpf(str(u)) if not isinstance(u, Fr) else mpf(u.numerator) / mpf(u.denominator)
        self.pu = 1 / (1 + mpmath.exp(self.u))
        self.half = mpf(1) / 2
        self.a = self.kl(self.pu, self.half)
        self.lam1 = self.Lam(self.u)
        self.estar = mpmath.log(mpmath.cosh(self.u / 2))
        self.rho_h = self.lam1 / self.u
        self.h = self.kl(self.rho_h, self.half)
        self.L = mpmath.log((1 - self.rho_h) / self.rho_h) / self.u          # p_{Lu} = rho_h
        self.thpp = 1 / (self.u ** 2 * self.rho_h * (1 - self.rho_h))         # theta_hint''(0)
        self.cs2 = 2 * mpmath.pi ** 2 * self.h ** 2 * self.thpp

    def kl(self, r, p):
        mp = self.mpmath
        r = mp.mpf(r)
        out = mp.mpf(0)
        if r > 0:
            out += r * mp.log(r / p)
        if r < 1:
            out += (1 - r) * mp.log((1 - r) / (1 - p))
        return out

    def Lam(self, v):
        mp = self.mpmath
        return mp.log(2 / (1 + mp.exp(-v)))

    def e_of(self, rho):
        return self.kl(rho, self.pu)

    def th_of(self, rho):
        return self.kl(rho, self.half)

    def rho_of_e(self, e):
        """rho in [p_u, 1/2] with KL(rho || p_u) = e   (0 <= e <= eps*)"""
        mp = self.mpmath
        e = mp.mpf(e)
        if e <= 0:
            return self.pu
        if e >= self.estar:
            return self.half
        lo, hi = self.pu, self.half
        # bisection to 20 bits, then Newton (d/drho KL(rho||p_u) = ln(rho/(1-rho)) + u > 0 on (p_u, 1/2])
        for _ in range(30):
            mid = (lo + hi) / 2
            if self.e_of(mid) > e:
                hi = mid
            else:
                lo = mid
        r = (lo + hi) / 2
        for _ in range(60):
            f = self.e_of(r) - e
            d = mp.log(r / (1 - r)) + self.u
            rn = r - f / d
            if rn <= lo or rn >= hi:
                rn = (lo + hi) / 2
            if self.e_of(rn) > e:
                hi = min(hi, rn)
            else:
                lo = max(lo, rn)
            if abs(rn - r) < mp.mpf(10) ** (-(self.mp.dps - 3)):
                r = rn
                break
            r = rn
        return r

    def theta(self, e):
        mp = self.mpmath
        e = mp.mpf(e)
        if e >= self.estar:
            return mp.mpf(0)
        if e <= 0:
            return self.a
        return self.th_of(self.rho_of_e(e))

    def theta_prime(self, e):
        """theta_na'(e) = -l/(u - l), l = ln((1-rho)/rho), for 0 < e < eps*"""
        mp = self.mpmath
        r = self.rho_of_e(e)
        l = mp.log((1 - r) / r)
        return -l / (self.u - l)

    def J(self, t):
        return self.Lam(t * self.u) - t * self.lam1

    def Jp(self, t):
        mp = self.mpmath
        return self.u / (1 + mp.exp(t * self.u)) - self.lam1

    def theta_hint(self, x):
        mp = self.mpmath
        r = (self.lam1 + x) / self.u
        if r >= self.half:
            return mp.mpf(0)
        return self.kl(r, self.half)

    def Q(self, t):
        return self.J(t) / (1 - t)

    def Sigma(self, B, s):
        """the slope map Sigma(B, s) = sup_e [B - (1 - s) theta(e)]/e, through J:  = t'(1-s)/(1-t'),  J(t')/(1-t') = B/(1-s);
        +inf if B >= (1 - s) a (infinite slope at zero), 0 if B = 0."""
        mp = self.mpmath
        B, s = mp.mpf(B), mp.mpf(s)
        if B <= 0:
            return mp.mpf(0)
        if s >= 1 or B >= (1 - s) * self.a:
            return mp.inf
        tgt = B / (1 - s)
        lo, hi = mp.mpf(0), mp.mpf(1)
        nb = int(self.mp.prec) + 8
        for _ in range(nb):
            mid = (lo + hi) / 2
            if self.Q(mid) <= tgt:
                lo = mid
            else:
                hi = mid
        tp = (lo + hi) / 2
        return tp * (1 - s) / (1 - tp)

    def Sigma_direct(self, B, s, n=4000):
        """the same by a direct maximisation over rho of [B - (1 - s) KL(rho||1/2)]/KL(rho||p_u)  (for cross-checks)"""
        mp = self.mpmath
        B, s = mp.mpf(B), mp.mpf(s)
        if s >= 1 or B >= (1 - s) * self.a:
            return mp.inf

        def F(w):
            rho = self.pu + (self.half - self.pu) * w * w
            return (B - (1 - s) * self.th_of(rho)) / self.e_of(rho)
        # coarse grid then golden section in w
        best, wb = -mp.inf, None
        for i in range(1, 201):
            w = mp.mpf(i) / 200
            v = F(w)
            if v > best:
                best, wb = v, w
        lo, hi = max(wb - mp.mpf(1) / 200, mp.mpf(10) ** -12), min(wb + mp.mpf(1) / 200, mp.mpf(1))
        gr = (mp.sqrt(5) - 1) / 2
        x1, x2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
        f1, f2 = F(x1), F(x2)
        for _ in range(int(2.1 * self.mp.prec)):
            if f1 > f2:
                hi, x2, f2 = x2, x1, f1
                x1 = hi - gr * (hi - lo)
                f1 = F(x1)
            else:
                lo, x1, f1 = x1, x2, f2
                x2 = lo + gr * (hi - lo)
                f2 = F(x2)
        return max(F((lo + hi) / 2), F(mp.mpf(1)), best)


# ----------------------------------------------------------------------------------------------------------------
#  exact piecewise-linear convex curves
# ----------------------------------------------------------------------------------------------------------------
def upper_hull(lines, c):
    """Exact upper envelope on [0, c] of the zero line and the lines (alpha, beta) -> alpha*B - beta, beta >= 0.
    Returns a list of triples (alpha, beta, x_start), slopes strictly increasing, starting with (0, 0, 0): the line
    is the maximum exactly on [x_start, next x_start] (the last one up to c).  Lines never strictly above the others
    on (0, c) are dropped.  (My own routine: breakpoints kept on a stack; not the three-line test of z6.)"""
    c = Fr(c)
    best = {}
    for al, be in lines:
        al, be = Fr(al), Fr(be)
        if be < 0:
            raise ValueError("upper_hull: a line that is positive at 0")
        if al <= 0:
            continue                                       # never above the zero line on [0, c]
        if al not in best or be < best[al]:
            best[al] = be
    st = [(Fr(0), Fr(0), Fr(0))]
    for al in sorted(best):
        be = best[al]
        while True:
            a0, b0, x0 = st[-1]
            # value of the new line at the start of the top line, against the top line there
            if len(st) > 1 and al * x0 - be >= a0 * x0 - b0:
                st.pop()
            else:
                break
        a0, b0, x0 = st[-1]
        x = (be - b0) / (al - a0)                          # crossing of the new line with the top line (al > a0)
        if x < c:
            st.append((al, be, x))
    return st


class PL:
    """V(B) = max(0, max_i (alpha_i B - beta_i)) on [0, c], exact; kept as its upper hull"""

    def __init__(self, lines, c):
        self.c = Fr(c)
        self.hull = upper_hull(lines, self.c)
        self.starts = [h[2] for h in self.hull]

    def lines(self):
        """the nonzero hull lines (alpha, beta), by slope"""
        return [(h[0], h[1]) for h in self.hull[1:]]

    def active(self, B):
        """index into self.hull of a line that is the maximum at B (0 = the zero line), by exact comparison"""
        B = Fr(B)
        lo, hi = 0, len(self.hull) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.starts[mid] <= B:
                lo = mid
            else:
                hi = mid - 1
        return lo

    def val(self, B):
        B = Fr(B)
        a_, b_, _ = self.hull[self.active(B)]
        return a_ * B - b_

    def val_brute(self, B):
        B = Fr(B)
        return max([Fr(0)] + [h[0] * B - h[1] for h in self.hull[1:]])

    def vertices(self):
        """exact vertices (X, V(X)): 0, the breakpoints, c"""
        vs = [(h[2], h[0] * h[2] - h[1]) for h in self.hull]
        vs.append((self.c, self.hull[-1][0] * self.c - self.hull[-1][1]))
        return vs

    def M(self, g):
        """max_{0 <= B <= c} (B - V(B) g), exactly (attained at a vertex)"""
        g = Fr(g)
        return max(X - g * V for X, V in self.vertices())


# ----------------------------------------------------------------------------------------------------------------
#  one step of a multi-rate sequence (Proposition A13), with certificates; and its independent checker
# ----------------------------------------------------------------------------------------------------------------
def top_exact(V, abar):
    """the least c' in [0, V.c] with c' + abar V(c') >= abar, or V.c if there is none: exact (piecewise linear)"""
    abar = Fr(abar)
    if V.c + abar * V.val(V.c) < abar:
        return V.c
    for k, (al, be, x0) in enumerate(V.hull):
        x1 = V.hull[k + 1][2] if k + 1 < len(V.hull) else V.c
        # on [x0, x1]: B + abar (al B - be) = abar  <=>  B = abar (1 + be)/(1 + abar al)
        B = abar * (1 + be) / (1 + abar * al)
        if x0 <= B <= x1:
            return B
    raise RuntimeError("top_exact: no root found (should not happen)")


def image_line(parent, e, th):
    """the exact line [B - th (1 - l(B))]/e for l = parent = (alpha0, beta0):  ((1 + th alpha0)/e, th (1 + beta0)/e)"""
    a0, b0 = parent
    return (1 + th * a0) / e, th * (1 + b0) / e


def check_step(V, Vn, certs, cube, abar, verbose=False):
    """Independent exact check that (V, V.c) -> (Vn, Vn.c) is a step of an admissible sequence in the sense of
    Proposition A13.  `certs` maps every nonzero hull line (alpha, beta) of Vn to
        ('img', parent, rho, e, th)      parent a hull line of V or (0, 0);  claims  line <= [B - th(1 - parent(B))]/e
        ('cap', (l1, c1), (l2, c2))      two certified image lines (each with its own 'img' certificate c_i);
                                         claims  line <= max(l1, l2)  everywhere.
    Returns a list of violations (strings); empty means: every condition verified exactly.
    Conditions:  (i) V is a family on [0, V.c]: V(V.c) <= 1 (V(0) = 0 and convexity hold by the representation);
    (ii) 0 < Vn.c <= V.c and (Vn.c = V.c or Vn.c + abar V(Vn.c) >= abar), abar >= a rigorously;
    (iii) every line of Vn is certified;  (iv) Vn(Vn.c) <= 1, betas >= 0."""
    bad = []
    one = Fr(1)
    if V.val_brute(V.c) > one:
        bad.append("V(c) > 1")
    c2 = Vn.c
    if not (0 < c2 <= V.c):
        bad.append("top not in (0, c]")
    if abar < cube.A.hi_fr():
        bad.append("abar is not a rigorous upper bound of a")
    if c2 != V.c and c2 + abar * V.val_brute(c2) < abar:
        bad.append("(S1) fails: c' + abar V(c') < abar and c' != c")
    parents = set(V.lines()) | {(Fr(0), Fr(0))}

    def check_img(line, cert):
        _, parent, rho, e, th = cert
        if parent not in parents:
            return "parent is not a line of V"
        E, TH = cube.pair_enclosures(rho)
        if not (e > 0 and e >= E.hi_fr()):
            return "pair: e' < upper enclosure of KL(rho||p_u)"
        if not (th >= 0 and th >= TH.hi_fr()):
            return "pair: th < upper enclosure of KL(rho||1/2)"
        al, be = line
        ia, ib = image_line(parent, e, th)
        if al > ia:
            return "slope above the image line"
        if be < ib:
            return "beta below the image line (line higher at 0)"
        return None

    for line in Vn.lines():
        al, be = line
        if be < 0:
            bad.append("beta < 0")
        cert = certs.get(line)
        if cert is None:
            bad.append("uncertified line (%.6g, %.6g)" % (float(al), float(be)))
            continue
        if cert[0] == "img":
            msg = check_img(line, cert)
            if msg:
                bad.append("img line (%.6g, %.6g): %s" % (float(al), float(be), msg))
        elif cert[0] == "cap":
            (l1, c1), (l2, c2_) = cert[1], cert[2]
            ok = True
            for l_, c_ in ((l1, c1), (l2, c2_)):
                if l_ == (Fr(0), Fr(0)):
                    continue                                   # the zero line needs no certificate
                if c_ is None or c_[0] != "img":
                    bad.append("cap witness without an image certificate")
                    ok = False
                    continue
                msg = check_img(l_, c_)
                if msg:
                    bad.append("cap witness: %s" % msg)
                    ok = False
            if ok:
                (a1, b1), (a2, b2) = l1, l2
                if not (a1 <= al <= a2) or a1 == a2:
                    bad.append("cap: slopes of the witnesses do not straddle the cap slope")
                else:
                    X0 = (b2 - b1) / (a2 - a1)                 # crossing of the two witnesses
                    if al * X0 - be > a1 * X0 - b1:
                        bad.append("cap: the cap line is above the witnesses at their crossing")
        else:
            bad.append("unknown certificate")
    if Vn.val_brute(c2) > one:
        bad.append("V'(c') > 1")
    if verbose and bad:
        for b in bad[:10]:
            print("   check_step:", b)
    return bad


def float_rate(u, a, lam1, B, s):
    """floating-point choice of the rate for the point (B, s): the tangency rho = 1/(1 + exp(t' u)), Q(t') = B/(1 - s),
    Q(t) = J(t)/(1 - t), J(t) = Lambda(tu) - t Lambda(u).  None if the point is not regular.  Quality only."""
    if s >= 1.0 or B >= (1.0 - s) * a or B <= 0:
        return None
    tgt = B / (1.0 - s)
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        Jm = math.log(2.0 / (1.0 + math.exp(-mid * u))) - mid * lam1
        if Jm <= tgt * (1.0 - mid):
            lo = mid
        else:
            hi = mid
    tp = 0.5 * (lo + hi)
    return 1.0 / (1.0 + math.exp(tp * u))


def build_step(V, cube, abar, samples, rho_bits=40, pair_bits=96, line_bits=128, extra_rates=()):
    """One step (V, c) -> (V', c') of a multi-rate sequence, my construction:
      top      c' = the exact root of c' + abar V(c') = abar (or c), rounded UP to a multiple of 2^-line_bits (capped by c);
      lines    for every sample point B in (0, c') with s = V(B) < 1 and B < (1 - s) a: the active line l of V at B (exact),
               the rate rho = tangency point of the slope map at (B, s) (floating point, rounded to rho_bits bits),
               optionally also rho*(1 + d) for d in extra_rates;  certified pair (e', th) from my interval arithmetic;
               the image line [B - th (1 - l(B))]/e', slope rounded DOWN and beta rounded UP to 2^-line_bits;
      cap      if the hull H of these lines has H(c') > 1: the line through (c', 1) with the least slope m that keeps it
               below H at all vertices of H (m rounded UP), lines with value > 1 at c' dropped.
    Returns (V', certs) with certificates for check_step."""
    u = float(cube.u)
    a = cube.A.mid_float()
    lam1 = math.log(2.0 / (1.0 + math.exp(-u)))
    cex = top_exact(V, abar)
    c2 = min(V.c, ceil_dyadic(cex, line_bits))
    certs = {}
    new = []
    for B in samples(c2):
        B = Fr(B)
        if not (0 < B < c2):
            continue
        k = V.active(B)
        al0, be0, _ = V.hull[k]
        s = al0 * B - be0
        if s >= 1:
            continue
        r0 = float_rate(u, a, lam1, float(B), float(s))
        if r0 is None:
            continue
        for d in (0.0,) + tuple(extra_rates):
            r = r0 * (1.0 + d)
            if not (0.0 < r < 1.0):
                continue
            rho = min(Fr(1, 2), ceil_dyadic(Fr(r), rho_bits))
            e, th = cube.certified_pair(rho, pair_bits)
            ia, ib = image_line((al0, be0), e, th)
            line = (floor_dyadic(ia, line_bits), ceil_dyadic(ib, line_bits))
            if line[0] <= 0:
                continue
            if line not in certs:
                certs[line] = ("img", (al0, be0), rho, e, th)
                new.append(line)
    H = PL(new, c2)
    if H.val(c2) > 1:
        vs = H.vertices()
        mstar, kstar = None, None
        for k, (X, VX) in enumerate(vs[:-1]):
            m = (1 - VX) / (c2 - X)
            if mstar is None or m > mstar:
                mstar, kstar = m, k
        m = ceil_dyadic(mstar, line_bits)
        capline = (m, m * c2 - 1)
        # witnesses: the two hull lines of H that meet at the vertex kstar (hull index kstar - 1 and kstar; vertex 0 is
        # the origin, where the zero line starts: then the witnesses are the zero line and the first line)
        if kstar == 0:
            w1, w2 = H.hull[0], H.hull[1]
        else:
            w1, w2 = H.hull[kstar - 1], H.hull[kstar]
        # the slope m (rounded up) may exceed the slope of w2: move the witnesses right until they straddle m
        j = kstar if kstar > 0 else 1
        while j + 1 < len(H.hull) and H.hull[j][0] < m:
            j += 1
        w1, w2 = H.hull[j - 1], H.hull[j]
        l1, l2 = (w1[0], w1[1]), (w2[0], w2[1])
        keep = [ln for ln in H.lines() if ln[0] * c2 - ln[1] <= 1]
        certs[capline] = ("cap", (l1, certs.get(l1)), (l2, certs.get(l2)))
        Vn = PL(keep + [capline], c2)
    else:
        Vn = H
    certs = {ln: certs[ln] for ln in Vn.lines()}
    return Vn, certs
