"""
r16lib.py -- workstream R16 (science division): the certified cost bound of nested levels of
Algorithm 2L+ (Theorem 11.56 of the theory report at 9befefd = Theorem K1 of K_REPORT.md), written
from the STATEMENTS:

  * constants of one level:   K_REPORT.md section 2.2 "Constants" / theory report lines 5023-5033
        J, nu_0, r-dagger, pi-dagger, m_max, K, nu, M-dagger, M-bar, delta', cnt(x), C_max, x_out
  * base bracket:             Proposition K0 (K_REPORT.md section 3.2), the family
        eta = min(1/2, tanh(x/4)), K = ceil(3(1+eta)/eta^2 ln(4/delta')), r*, M, cost 2M, or enumeration
  * the rule of THY-RES-0013 section 4 / remark (1b):  a rung is served by the admissible candidate with
        the smallest certified cost.

Not imported, not copied: the theory division's r8_flat.py / cert3.py.  They were READ to resolve the
ambiguities of the DESIGN that the texts leave open; every such place is marked  [RESOLVED-BY-READING]
below and listed in R16_REPORT.md section 4.

Everything is evaluated in logarithms (float64).  Binomial coefficients and ball sizes are exact Python
integers, converted to logarithms with math.log (no lgamma, no accumulated rounding in |B(m,r)|).
E_r and T_m(k) are sums of positive terms, evaluated by prefix/suffix log-sum-exp with my own formulas:

    E_r(m) = sum_{j<=r} C(m,j)(e^{u(r+1-j)} - 1)  =  (e^u - 1) sum_{i<=r} e^{u(r-i)} |B(m,i)|
             (from E_r = e^u E_{r-1} + (e^u - 1)|B(m,r)|, E_{-1} = 0; no subtraction),
    T_m(k) = sum_j C(m,j) e^{-u (j-k)_+}          =  |B(m,k)| + e^{uk} sum_{j>k} C(m,j) e^{-uj}.

The file is cross-checked against the science division's exact-arithmetic implementation of workstream R6
(experiments/science/ws_R6/r6lib.py, everyn.py: exact integers and 40-digit mpmath) in r16_validate.py.
"""
import math
import numpy as np

LN2 = math.log(2.0)
NEG_INF = float("-inf")


# ---------------------------------------------------------------------------------------------------
# tables on a cube Q_m
# ---------------------------------------------------------------------------------------------------
class Tab:
    def __init__(self, m, u):
        self.m, self.u = m, u
        # exact integers, streamed (no list of big integers is kept: at m = 51 200 such a list would take 0.3 GB)
        c = 1                                                    # C(m, j)
        s = 1                                                    # |B(m, j)|
        lC = [0.0]
        lB = [0.0]
        for j in range(m):
            c = c * (m - j) // (j + 1)
            s += c
            lC.append(math.log(c))
            lB.append(math.log(s))
        assert s == 1 << m
        self.lC = np.array(lC)
        self.lB = np.array(lB)                                   # lB[r] = ln |B(m,r)|, r = 0..m
        j = np.arange(m + 1, dtype=float)
        self.lE = math.log(math.expm1(u)) + u * j + np.logaddexp.accumulate(self.lB - u * j)
        suf = np.logaddexp.accumulate((self.lC - u * j)[::-1])[::-1]      # ln sum_{j>=k} C(m,j) e^{-uj}
        lR = np.full(m + 1, NEG_INF)
        lR[:m] = u * j[:m] + suf[1:]
        self.lT = np.logaddexp(self.lB, lR)                      # lT[k] = ln T_m(k)
        self.mln2 = m * LN2
        # ln Gamma~(r):  Gamma~(0) = e^u - 1,  Gamma~(r) = E_r / |B(m,r-1)|
        self.lGt = np.empty(m + 1)
        self.lGt[0] = math.log(math.expm1(u))
        self.lGt[1:] = self.lE[1:] - self.lB[:-1]
        self._kap = {}

    def kappa(self, lceta):
        """kappa(r) = the largest k >= 0 with |B(m,k)| <= max{1, c_eta |B(m,r-1)|}, for r = 0..m  (|B(m,-1)| = 0)"""
        key = lceta
        if key not in self._kap:
            prev = np.concatenate(([NEG_INF], self.lB[:-1]))
            v = np.maximum(0.0, lceta + prev)
            self._kap[key] = np.maximum(0, np.searchsorted(self.lB, v, side="right") - 1)
        return self._kap[key]

    def lGpp(self, lceta):
        """ln Gamma''(r) = ln( E_r / T_m(kappa(r)) ), r = 0..m"""
        return self.lE - self.lT[self.kappa(lceta)]


_tabs = {}


def tab(m, u):
    if (m, u) not in _tabs:
        _tabs[(m, u)] = Tab(m, u)
    return _tabs[(m, u)]


def clear_tabs(keep=()):
    for k in list(_tabs):
        if k not in keep:
            del _tabs[k]


def lsumexp(vals):
    vals = [v for v in vals if v > NEG_INF]
    if not vals:
        return NEG_INF
    mx = max(vals)
    return mx + math.log(sum(math.exp(v - mx) for v in vals))


# ---------------------------------------------------------------------------------------------------
# one level of Algorithm 2L+ : its constants (statement of Theorem 11.56 / K_REPORT section 2.2)
# ---------------------------------------------------------------------------------------------------
class Level:
    """constants of Algorithm 2L+ in dimension n with outer dimension n_o.

    parameters: lam, eta, etap (eta'), ltheta = ln(theta), nu1, b (tolerance), ldelta = ln(delta),
    xs = [x_0 = 2 u n_i, x_1, ..., x_L]  (strictly decreasing, x_L <= b).
    """

    def __init__(self, u, n, n_o, lam, eta, etap, ltheta, nu1, b, ldelta, xs):
        # hypotheses of the theorem (theory report line 5023; K_REPORT section 2.2 "Parameters")
        assert n >= 2 and 1 <= n_o <= n - 1
        assert 0 < lam <= 1 and 0 < eta <= 0.5 and 0 < etap <= 1 and nu1 >= 1 and b > 0
        self.u, self.n, self.n_o, self.n_i = u, n, n_o, n - n_o
        self.lam, self.eta, self.etap, self.ltheta, self.nu1, self.b, self.ldelta = lam, eta, etap, ltheta, nu1, b, ldelta
        self.xs = list(xs)
        L = self.L = len(xs) - 1
        assert L >= 1
        assert abs(xs[0] - 2 * u * self.n_i) <= 1e-9 * xs[0], "x_0 must be 2 u n_i"
        assert all(xs[i] > xs[i + 1] for i in range(L)), "the ladder must decrease strictly"
        assert xs[L] <= b, "x_L <= b"
        t = tab(n_o, u)
        m = n_o
        self.J = J = math.ceil((2 * u * n + b + n_o * LN2) / lam)
        self.nu0 = nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
        lceta = math.log((1 - eta) / (1 + eta))
        # r-dagger: the largest r in {0..m-1} such that for all r' <= r
        #   [N] Gamma~(r') <= theta (1-eta) nu_0   and   [P] min{Gamma~(r')/c_eta, Gamma''(r')} <= theta
        okN = t.lGt <= ltheta + math.log((1 - eta) * nu0)
        okP = np.minimum(t.lGt - lceta, t.lGpp(lceta)) <= ltheta
        ok = (okN & okP)[:m]
        bad = np.nonzero(~ok)[0]
        self.rdag = rdag = (int(bad[0]) - 1) if bad.size else m - 1
        # pi-dagger = |B(m, r-dagger)| / 2^m   (2^{-m-1} if r-dagger = -1)
        self.lpidag = lpidag = (t.lB[rdag] - m * LN2) if rdag >= 0 else -(m + 1) * LN2
        self.m_max = m_max = math.ceil((math.log(2 * (1 + eta) / (1 - eta)) + lam + math.log(nu0) - lpidag) / LN2)
        self.K = K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(2 * (J + 1) * (m_max + 1) * (L + 2)) - ldelta))
        self.lK = math.log(K)
        self.lnu = self.lK + math.log(nu0)
        self.lMdag = self.lK - math.log(1 - eta) - lpidag
        self.lMbar = math.log(2 * (1 + eta)) + lam + math.log(nu0) + self.lMdag
        self.ldeltap = ldelta - math.log(4 * L) - self.lMbar        # delta' = delta / (4 L Mbar)
        # certified accuracy  ln[(2 p_u)^n + e^b (e^lam (1+eta)/(1-eta) + eta' + theta)]
        la = math.log(math.exp(lam) * (1 + eta) / (1 - eta) + etap)
        mx = max(la, ltheta)
        ladd = mx + math.log(math.exp(la - mx) + math.exp(ltheta - mx))          # ln(e^lam(1+eta)/(1-eta) + eta' + theta)
        l1 = n * math.log(2 / (1 + math.exp(u)))
        l2 = b + ladd
        mx = max(l1, l2)
        self.xout = mx + math.log(math.exp(l1 - mx) + math.exp(l2 - mx))
        self.xout_minus_b = ladd

    def lcnt(self, x):
        """ln cnt(x),  cnt(x) = max{K, 2 (1+eta)^2 (1-eta)^{-1} e^lam nu e^x}"""
        eta = self.eta
        return max(self.lK, math.log(2 * (1 + eta) ** 2 / (1 - eta)) + self.lam + self.lnu + x)

    def lmult(self, l):
        """ln min{2 Mbar, (J+1) cnt(x_{l-1})}  and which of the two it is"""
        cap = LN2 + self.lMbar
        cnt = math.log(self.J + 1) + self.lcnt(self.xs[l - 1])
        return (cap, "cap") if cap <= cnt else (cnt, "count")

    def lCmax(self, lC):
        """ln C_max,  C_max = 1 + 2 Mbar + sum_{l=1}^L min{2 Mbar, (J+1) cnt(x_{l-1})} C_l ;  lC[l] = ln C_l, l = 1..L"""
        terms = [0.0, LN2 + self.lMbar]
        for l in range(1, self.L + 1):
            terms.append(self.lmult(l)[0] + lC[l])
        return lsumexp(terms)


# ---------------------------------------------------------------------------------------------------
# the base bracket (Proposition K0)
# ---------------------------------------------------------------------------------------------------
def k0(u, d, x, ldeltap):
    """ln cost of the base family in dimension d at accuracy x, failure probability e^ldeltap; and its kind.
    eta = min(1/2, tanh(x/4)); K = ceil(3(1+eta)/eta^2 ln(4/delta')); r* the largest radius <= d-1 with
    ln(1 + Gamma''_d(r')) <= x - ln((1+eta)/(1-eta)) for all r' <= r*; M = ceil(K 2^d/((1-eta)|B(d,r*)|)); cost 2M;
    enumeration (2^d queries, exact) if no radius qualifies, or if it is cheaper."""
    t = tab(d, u)
    eta = min(0.5, math.tanh(x / 4))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) - ldeltap))
    budget = x - math.log((1 + eta) / (1 - eta))
    lg = t.lGpp(math.log((1 - eta) / (1 + eta)))[:d]
    ok = np.logaddexp(0.0, lg) <= budget
    if not ok[0]:
        return d * LN2, "enum"
    bad = np.nonzero(~ok)[0]
    rstar = (int(bad[0]) - 1) if bad.size else d - 1
    lM = math.log(K) + d * LN2 - math.log(1 - eta) - t.lB[rstar]
    if lM < 40:                                   # the ceiling of the proposition (invisible above e^40)
        lM = math.log(math.ceil(math.exp(lM) - 1e-9))
    lcost = LN2 + lM
    if lcost >= d * LN2:
        return d * LN2, "enum"
    return lcost, "K0"


# ---------------------------------------------------------------------------------------------------
# designs
# ---------------------------------------------------------------------------------------------------
def geometric_ladder(x0, b, L):
    """[RESOLVED-BY-READING: r8_flat.py line 106]  'a geometric ladder of L rungs': x_l = x_0 (b/x_0)^{l/L}, x_L = b"""
    xs = [x0 * (b / x0) ** (l / L) for l in range(L + 1)]
    xs[-1] = b
    return xs


def n_outer(phi, n):
    """[RESOLVED-BY-READING: r8_flat.py lines 100-101]  n_o = floor(phi n) evaluated in floating point, clipped to [1, n-1]"""
    return min(max(int(math.floor(phi * n)), 1), n - 1)


def outer_level(u, n, phi, ldelta=None):
    """the outer level of the README / remark (1b):  b = 0.5, lam = 0.2, eta = eta' = theta = 0.05, delta = 0.05,
    nu_1 = 2 e^u n_o / theta  (K_REPORT section 6.4; theory report line 5303), a geometric ladder of 40 rungs."""
    n_o = n_outer(phi, n)
    n_i = n - n_o
    b, lam, eta, etap, theta = 0.5, 0.2, 0.05, 0.05, 0.05
    ld = math.log(0.05) if ldelta is None else ldelta
    xs = geometric_ladder(2 * u * n_i, b, 40)
    return Level(u, n, n_o, lam, eta, etap, math.log(theta), 2 * math.exp(u) * n_o / theta, b, ld, xs)


def two_level_bound(u, lev):
    """ln C_max of the level `lev` with base brackets on every rung, and the list ln C_l"""
    lC = [None] + [k0(u, lev.n_i, lev.xs[l], lev.ldeltap)[0] for l in range(1, lev.L + 1)]
    return lev.lCmax(lC), lC


def middle_extensive(u, d, x, p2, ldelta):
    """'extensive' middle design (Corollary K1.b style; header of r8_flat3.py):  lam = 1, eta = 1/2, eta' = 1, nu_1 = 1,
    tolerance b = x/4, theta = e^{x-b} - (3e+1) - (2p_u)^d e^{-b}  (certified accuracy exactly x), 30 rungs."""
    bm = x / 4
    lth = (x - bm) + math.log1p(-(3 * math.e + 1 + (2 / (1 + math.exp(u))) ** d * math.exp(-bm)) * math.exp(-(x - bm)))
    n_o = n_outer(p2, d)
    xs = geometric_ladder(2 * u * (d - n_o), bm, 30)
    return Level(u, d, n_o, 1.0, 0.5, 1.0, lth, 1.0, bm, ldelta, xs)


def middle_bounded(u, d, x, p2, bm, ldelta):
    """'bounded-accuracy' middle design (Theorem K2 style):  lam = eta = eta' = theta = c = min(x/12, 1/3),
    nu_1 = 2 e^u n_o / theta, tolerance bm, 30 rungs."""
    c = min(x / 12, 1 / 3)
    n_o = n_outer(p2, d)
    xs = geometric_ladder(2 * u * (d - n_o), bm, 30)
    return Level(u, d, n_o, c, c, c, math.log(c), 2 * math.exp(u) * n_o / c, bm, ldelta, xs)


def theta_hint(u, g):
    lam1 = math.log(2 / (1 + math.exp(-u)))
    est = math.log(math.cosh(u / 2))
    if g >= est:
        return 0.0
    r = (lam1 + g) / u
    return math.log(2) + r * math.log(r) + (1 - r) * math.log(1 - r)


def acc_const(c):
    """ln(e^lam (1+eta)/(1-eta) + eta' + theta) at lam = eta = eta' = theta = c"""
    return math.log(math.exp(c) * (1 + c) / (1 - c) + 2 * c)


_mid = {}


def middle_bound(u, kind, d, x, p2, bm, ldelta):
    """(ln C_max, certified accuracy, description) of a two-level run in dimension d, base brackets inside; cached"""
    key = (u, kind, d, x, p2, bm, ldelta)
    if key not in _mid:
        if kind == "ext":
            lev = middle_extensive(u, d, x, p2, ldelta)
            name = "extensive (lam=1, eta=1/2, b=x/4), phi_2=%.3f" % p2
        else:
            lev = middle_bounded(u, d, x, p2, bm, ldelta)
            name = "bounded (c=%.3f, b=%s), phi_2=%.2f" % (min(x / 12, 1 / 3), "x/2" if bm == x / 2 else "max", p2)
        lcm, _ = two_level_bound(u, lev)
        _mid[key] = dict(lCmax=lcm, xout=lev.xout, name=name, kind=kind, p2=p2, bm=bm, lev=lev)
    return _mid[key]


def referee_candidates(u, d, x, ldelta):
    """the two middle designs of the referee's three-level construction (header of r8_flat3.py):
       x >= 8: extensive, phi_2 = g/(g + theta_hint(g)) clipped to [0.05, 0.7], and 1.5 times that
               [RESOLVED-BY-READING: r8_flat3.py lines 48-51: the second is clipped to 0.8; a candidate whose first
                inner accuracy 2u(d - n_o) is not above 1.5 b is skipped];
       x <  8: bounded, b = x/2, phi_2 = 0.55."""
    out = []
    g = x / d
    if x >= 8:
        bm = x / 4
        p0 = min(0.7, max(0.05, g / (g + theta_hint(u, g))))
        for p2 in (p0, min(0.8, 1.5 * p0)):
            if 2 * u * (d - int(p2 * d)) <= bm * 1.5:
                continue
            out.append(middle_bound(u, "ext", d, x, p2, bm, ldelta))
    else:
        out.append(middle_bound(u, "bnd", d, x, 0.55, x / 2, ldelta))
    return out


def added_candidates(u, d, x, ldelta):
    """'more middle designs' (README; THY-RES-0013 section 4): the bounded design at every accuracy, tolerance x/2 or the
    largest its accuracy allows, outer fraction by descent from 0.50 in steps of 0.05.
    [RESOLVED-BY-READING: cert3.py lines 89-109: 'the largest' is x - ln(e^c(1+c)/(1-c) + 2c) - 1e-6; the descent stops
     at 0.20, at the first fraction whose bound does not improve, whose certified accuracy exceeds x, or whose first
     inner accuracy is not above 1.5 b.]"""
    c = min(x / 12, 1 / 3)
    bmax = x - acc_const(c) - 1e-6
    out = []
    for bm in (x / 2, bmax):
        if bm <= 0 or bm > bmax:
            continue
        prev = None
        for p2 in (0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20):
            if 2 * u * (d - int(p2 * d)) <= bm * 1.5:
                break
            r = middle_bound(u, "bnd", d, x, p2, bm, ldelta)
            if r["xout"] > x + 1e-9:
                break
            if prev is not None and r["lCmax"] >= prev:
                break
            out.append(r)
            prev = r["lCmax"]
    return out


def serve(u, d, x, ldeltap, mode, a_const):
    """the server of a rung (dimension d, accuracy x, failure probability e^ldeltap) by certified cost.
    mode: 'two' (base bracket only), 'tuned' (referee's candidates), 'searched' (plus the added ones).
    Returns dict(lC, kind, c0, best) -- lC the certified cost charged, best the best two-level candidate (or None).
    [RESOLVED-BY-READING: cert3.py lines 127, 134: no two-level candidate is tried when x/d >= 0.9 eps* or d < 50; the
     added candidates are tried only where the base bracket costs more than e^{0.2 d a}.]"""
    c0, kind0 = k0(u, d, x, ldeltap)
    res = dict(lC=c0, kind=kind0, c0=c0, best=None, ncand=0)
    if mode == "two":
        return res
    est = math.log(math.cosh(u / 2))
    if x / d >= 0.9 * est or d < 50:
        return res
    cands = list(referee_candidates(u, d, x, ldeltap))
    if mode == "searched" and c0 > 0.2 * d * a_const:
        cands += added_candidates(u, d, x, ldeltap)
    res["ncand"] = len(cands)
    if not cands:
        return res
    best = min(cands, key=lambda r: r["lCmax"])
    res["best"] = best
    res["cands"] = cands
    if best["lCmax"] < c0:
        res["lC"], res["kind"] = best["lCmax"], "2L+"
    return res


def three_level_bound(u, n, phi, mode, a_const):
    lev = outer_level(u, n, phi)
    rows = [None]
    lC = [None]
    for l in range(1, lev.L + 1):
        r = serve(u, lev.n_i, lev.xs[l], lev.ldeltap, mode, a_const)
        rows.append(r)
        lC.append(r["lC"])
    return lev, lev.lCmax(lC), rows


def a_of(u):
    pu = 1 / (1 + math.exp(u))
    return math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)


def peak_rss_mb():
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
