#!/usr/bin/env python3
"""rlib.py -- the referee's own evaluator for the review of Q2_REPORT.md.

Written from the formulas of the theory report (Theorem 11.56, Lemma 11.55, Proposition 11.57(a))
and of K_REPORT.md section 2.1-2.2 (tables on the outer cube, the constants J, nu0, m_max, K, Mbar,
delta', cnt, C_max).  Nothing is imported from the workstream's libraries.

Everything is in natural logarithms.  Tables of the outer cube Q_m are numpy float64 arrays of
length m+1 (log-space), so memory is O(m).
"""
import math
import numpy as np

LN2 = math.log(2.0)
TOL = 1e-12          # tolerance of table comparisons
INF = float('inf')


# ----------------------------------------------------------------------------- the cube constants
def kl(x, y):
    """KL(x || y) for Bernoulli parameters."""
    s = 0.0
    if x > 0:
        s += x * math.log(x / y)
    if x < 1:
        s += (1 - x) * math.log((1 - x) / (1 - y))
    return s


class Cube:
    def __init__(self, u):
        self.u = u
        self.p = 1.0 / (1.0 + math.exp(u))
        self.a = kl(self.p, 0.5)
        self.Lam1 = math.log(2.0 / (1.0 + math.exp(-u)))
        self.rho_h = self.Lam1 / u
        self.h = kl(self.rho_h, 0.5)
        self.eps_star = math.log(math.cosh(u / 2.0))
        # sanity: KL(rho_h || p_u) = h
        assert abs(kl(self.rho_h, self.p) - self.h) < 1e-12

    def rho_of(self, e):
        """rho_e in [p_u, 1/2] with KL(rho || p_u) = min(e, eps*)."""
        if e <= 0:
            return self.p
        if e >= self.eps_star:
            return 0.5
        lo, hi = self.p, 0.5
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if kl(mid, self.p) < e:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def theta_na(self, e):
        return kl(self.rho_of(e), 0.5)


# ----------------------------------------------------------------------------- tables on Q_m
class Tables:
    """log-tables on the outer cube Q_m for a given Chernoff parameter eta (c_eta = (1-eta)/(1+eta)).

    lB[r]  = ln |B(m, r)|,                      r = 0..m
    lE[r]  = ln E_r(m),   E_r(m) = sum_{j<=r} C(m,j) (e^{u(r+1-j)} - 1)
    lT[k]  = ln T_m(k),   T_m(k) = sum_j C(m,j) e^{-u (j-k)_+}
    lGt[r] = ln Gamma~(r),  Gamma~(0) = e^u - 1,  Gamma~(r) = E_r(m)/|B(m, r-1)|
    lG2[r] = ln Gamma''(r) = ln E_r(m) - ln T_m(kappa(r)),
             kappa(r) = largest k >= 0 with |B(m,k)| <= max{1, c_eta |B(m, r-1)|}
    """

    def __init__(self, u, m, eta):
        self.u, self.m, self.eta = u, m, eta
        j = np.arange(m + 1, dtype=np.float64)
        lgam = np.vectorize(math.lgamma)
        lC = math.lgamma(m + 1.0) - lgam(j + 1.0) - lgam(m - j + 1.0)
        lC[0] = 0.0
        lC[m] = 0.0
        self.lB = np.logaddexp.accumulate(lC)
        self.lB[0] = 0.0
        # E_r = e^{u(r+1)} sum_{j<=r} C(m,j) e^{-uj}  -  |B(m,r)|
        w = lC - u * j
        lA = u * (j + 1.0) + np.logaddexp.accumulate(w)
        self.lE = lA + np.log1p(-np.exp(self.lB - lA))
        # T_m(k) = |B(m,k)| + e^{uk} sum_{j>k} C(m,j) e^{-uj}
        suf = np.full(m + 1, -INF)
        if m >= 1:
            rev = np.logaddexp.accumulate(w[::-1])[::-1]      # rev[k] = ln sum_{j>=k} C e^{-uj}
            suf[:-1] = rev[1:]
        with np.errstate(divide='ignore'):
            self.lT = np.logaddexp(self.lB, u * j + suf)
        # Gamma~
        self.lGt = np.empty(m + 1)
        self.lGt[0] = math.log(math.expm1(u))
        if m >= 1:
            self.lGt[1:] = self.lE[1:] - self.lB[:-1]
        # kappa(r) and Gamma''
        lce = math.log((1.0 - eta) / (1.0 + eta))
        thr = np.empty(m + 1)
        thr[0] = 0.0
        if m >= 1:
            thr[1:] = np.maximum(0.0, lce + self.lB[:-1])
        kap = np.searchsorted(self.lB, thr + TOL, side='right') - 1
        kap = np.maximum(kap, 0)
        self.kappa = kap
        self.lG2 = self.lE - self.lT[kap]
        self.lce = lce
        # for r_dagger: the [P] test value  min{Gamma~/c_eta, Gamma''}  and prefix maxima
        self.lP = np.minimum(self.lGt - lce, self.lG2)
        self.pmaxP = np.maximum.accumulate(self.lP)
        self.pmaxN = np.maximum.accumulate(self.lGt)

    def rdag(self, ltheta, lnu0):
        """largest r in {0..m-1} with [N] Gamma~(r') <= theta (1-eta) nu0 and
        [P] min{Gamma~(r')/c_eta, Gamma''(r')} <= theta for all r' <= r;  -1 if none."""
        m = self.m
        rP = int(np.searchsorted(self.pmaxP, ltheta + TOL, side='right')) - 1
        rN = int(np.searchsorted(self.pmaxN, ltheta + math.log(1.0 - self.eta) + lnu0 + TOL,
                                 side='right')) - 1
        return min(rP, rN, m - 1)

    def lpi(self, r):
        """ln pi_dagger for the radius r (r = -1: 2^{-m-1})."""
        if r < 0:
            return -(self.m + 1) * LN2
        return float(self.lB[r]) - self.m * LN2


_TAB = {}


def tables(u, m, eta, keep=6):
    key = (u, m, eta)
    t = _TAB.get(key)
    if t is None:
        if len(_TAB) >= keep:
            _TAB.pop(next(iter(_TAB)))
        t = Tables(u, m, eta)
        _TAB[key] = t
    return t


# ----------------------------------------------------------------------------- one level of Algorithm 2L+
class Level:
    """Constants of Theorem 11.56 (K_REPORT 2.2) for one level.

    Arguments: u, n, n_o, lam, eta, etap, ltheta (= ln theta), nu1, b (tolerance), ld (= ln delta), L.
    """

    def __init__(self, u, n, n_o, lam, eta, etap, ltheta, nu1, b, ld, L, tab=None):
        assert n >= 2 and 1 <= n_o <= n - 1 and 0 < lam <= 1 and 0 < eta <= 0.5 and 0 < etap <= 1
        assert nu1 >= 1 and b > 0 and L >= 1 and ld < 0
        self.u, self.n, self.n_o, self.n_i = u, n, n_o, n - n_o
        self.lam, self.eta, self.etap, self.ltheta, self.nu1, self.b, self.ld, self.L = \
            lam, eta, etap, ltheta, nu1, b, ld, L
        self.J = math.ceil((2 * u * n + b + n_o * LN2) / lam - 1e-12)
        self.nu0 = max((self.J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
        self.lnu0 = math.log(self.nu0)
        t = tab if tab is not None else tables(u, n_o, eta)
        self.rd = t.rdag(ltheta, self.lnu0)
        self.lpi = t.lpi(self.rd)                       # ln pi_dagger  (<= 0)
        self.m_max = math.ceil((math.log(2 * (1 + eta) / (1 - eta)) + lam + self.lnu0 - self.lpi) / LN2 - 1e-12)
        self.K = math.ceil(3 * (1 + eta) / eta ** 2 *
                           (math.log(2.0 * (self.J + 1) * (self.m_max + 1) * (L + 2)) - ld) - 1e-12)
        self.lK = math.log(self.K)
        # Mbar = 2(1+eta) e^lam nu0 * K / ((1-eta) pi_dagger)
        self.lMbar = math.log(2 * (1 + eta)) + lam + self.lnu0 + self.lK - math.log(1 - eta) - self.lpi
        self.Lam_lev = LN2 + self.lMbar                 # ln 2 Mbar
        self.ldp = ld - math.log(4.0 * L) - self.lMbar  # ln delta'
        self.P_M = math.log(4 * (1 + eta) / (1 - eta)) + lam + self.lnu0 + self.lK
        self.P_cnt = math.log(self.J + 1) + math.log(2 * (1 + eta) ** 2 / (1 - eta)) + lam + self.lnu0 + self.lK
        p = 1.0 / (1.0 + math.exp(u))
        # accuracy  ln[(2p)^n + e^b ( e^lam (1+eta)/(1-eta) + eta' + theta )]
        c0 = math.exp(lam) * (1 + eta) / (1 - eta) + etap
        self.x_out = np.logaddexp(n * math.log(2 * p), b + np.logaddexp(math.log(c0), ltheta))

    def lcnt(self, x):
        """ln[(J+1) cnt(x)],  cnt(x) = max{K, 2(1+eta)^2 (1-eta)^{-1} e^lam nu e^x},  nu = K nu0."""
        eta = self.eta
        second = math.log(2 * (1 + eta) ** 2 / (1 - eta)) + self.lam + self.lK + self.lnu0 + x
        return math.log(self.J + 1) + max(self.lK, second)

    def lcmax(self, xs, lcost):
        """ln C_max for the ladder xs = [x_1, ..., x_L] (x_0 = 2 u n_i) and inner ln-costs lcost."""
        assert len(xs) == self.L == len(lcost)
        x0 = 2 * self.u * self.n_i
        assert x0 > xs[0] and all(xs[i] > xs[i + 1] for i in range(len(xs) - 1)) and xs[-1] <= self.b + 1e-12
        xprev = np.concatenate(([x0], np.asarray(xs[:-1], dtype=np.float64)))
        eta = self.eta
        second = math.log(2 * (1 + eta) ** 2 / (1 - eta)) + self.lam + self.lK + self.lnu0 + xprev
        mult = np.minimum(self.Lam_lev, math.log(self.J + 1) + np.maximum(self.lK, second))
        terms = np.concatenate(([0.0, self.Lam_lev], mult + np.asarray(lcost, dtype=np.float64)))
        mx = terms.max()
        self.terms = terms
        return float(mx + math.log(np.exp(terms - mx).sum()))


# ----------------------------------------------------------------------------- the functions of Lemma U
E1 = math.e
C3 = 3 * E1 + 1
C12 = 12 * E1 * (E1 - 1)
C18 = math.log(18 * E1 * (E1 - 1))
C24 = math.log(24 * E1 * (E1 - 1))


def A_nb(cu, n, b=1.0):
    return (2 * cu.u + LN2) * n + 2 + b


def mbar_b(cu, n, b=1.0):
    return n + 2 + math.log2(C12 * A_nb(cu, n, b))


def Kbar_b(cu, n, Lam, b=1.0):
    return 18 * (Lam + math.log(2 * A_nb(cu, n, b) * mbar_b(cu, n, b) * (n + 3))) + 1


def q_b(cu, n, Lam, b=1.0):
    return math.log(4.0 * (n + 1)) + math.log(A_nb(cu, n, b)) + C24 + math.log(Kbar_b(cu, n, Lam, b))


def ell0_b(cu, n, Lam, b=1.0):
    return 1 + 2 * math.log(A_nb(cu, n, b)) + C18 + math.log(Kbar_b(cu, n, Lam, b)) + math.log(n + 3)


def c_log(cu, n):
    return math.log(n + 1.0) + math.log(6.0) + 2 * cu.u + math.exp(cu.u)


def ladder_U(cu, n_i, b, Xi):
    """the ladder of Lemma U: x_1 = b + k_1 > ... > b,  k_1 = min{max(ceil(Xi-b),0), ceil(2u n_i - b) - 1}."""
    k1 = min(max(math.ceil(Xi - b - 1e-12), 0), math.ceil(2 * cu.u * n_i - b - 1e-12) - 1)
    assert k1 >= 0
    return [b + (k1 - i) for i in range(k1 + 1)]


def ltheta_for_accuracy(cu, n, acc, b):
    """ln theta with  ln[(2p)^n + e^b (c3 + theta)] = acc,  i.e. theta = e^{acc-b} - c3 - (2p)^n e^{-b}."""
    z = acc - b
    sub = C3 + math.exp(n * math.log(2 * cu.p) - b)
    if z > 700:
        return z + math.log1p(-sub * math.exp(-z))
    v = math.exp(z) - sub
    assert v > 0
    return math.log(v)


class SatFamily:
    """A saturating family: certified ln-cost = max(floor, max_i [d B_i - sigma_i min(x, R d)]) + E(d, x; ln(1/delta) + d ln 2).

    lines: list of (B_i, sigma_i);  R in (0, inf];  Efun(d, x, Lam) >= 0 (None: zero);
    floor0: if True the majorant is cut at 0 (the family then has the type only where the majorant is >= 0).
    """

    def __init__(self, lines, R=INF, Efun=None, floor0=True):
        self.lines, self.R, self.Efun, self.floor0 = list(lines), R, Efun, floor0

    def E(self, d, x, Lam):
        return 0.0 if self.Efun is None else self.Efun(d, x, Lam)

    def major(self, d, x):
        xx = min(x, self.R * d) if self.R < INF else x
        return max(d * B - s * xx for (B, s) in self.lines)

    def cost(self, d, x, ld):
        mj = self.major(d, x)
        if self.floor0:
            mj = max(mj, 0.0)
        return mj + self.E(d, x, -ld + d * LN2)


# ----------------------------------------------------------------------------- the base family (Proposition 11.57(a) / Q (B))
def base_lcost(cu, d, x, ld):
    """ln of the certified cost of the base family G_0(d, x, delta): the two-sample bracket
    (eta = min(1/2, tanh(x/4)), K = ceil(3(1+eta) eta^-2 ln(4/delta)), r* the largest radius <= d-1 with
    ln(1 + Gamma''_d(r')) <= x - ln((1+eta)/(1-eta)) for all r' <= r*, M = ceil(K 2^d / ((1-eta)|B(d, r*)|)), cost 2M)
    or enumeration (2^d) if no radius qualifies or 2M >= 2^d."""
    eta = min(0.5, math.tanh(x / 4.0))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4.0) - ld) - 1e-12)
    t = tables(cu.u, d, eta)
    y = x - math.log((1 + eta) / (1 - eta))
    # ln(1 + Gamma'') <= y   <=>  Gamma'' <= e^y - 1
    if y <= 0:
        return d * LN2, -1
    lth = math.log(math.expm1(y)) if y < 30 else y + math.log1p(-math.exp(-y))
    pm = np.maximum.accumulate(t.lG2)
    r = min(int(np.searchsorted(pm, lth + TOL, side='right')) - 1, d - 1)
    if r < 0:
        return d * LN2, -1
    lM = math.log(K) + d * LN2 - math.log(1 - eta) - float(t.lB[r])
    if lM < 40:
        lM = math.log(math.ceil(math.exp(lM) - 1e-9))
    return min(LN2 + lM, d * LN2), r


# ----------------------------------------------------------------------------- the functions of Q7 / Proposition T
def A_n(cu, n):
    return (2 * cu.u + LN2) * n + 3


def nubar_D(cu, n, c):
    return (1.8 * A_n(cu, n) + 3 * math.exp(cu.u) * n) / c


def mbar_D(cu, n, c):
    return n + 2 + math.log2(5.6 * nubar_D(cu, n, c))


def Kbar_D(cu, n, Lam, c):
    return 4 / c ** 2 * (Lam + math.log(2 * (A_n(cu, n) / c) * mbar_D(cu, n, c) * (n + 4))) + 1


def Pbar_cnt(cu, n, Lam, c):
    return math.log(A_n(cu, n) / c) + math.log(7.45) + math.log(nubar_D(cu, n, c)) + math.log(Kbar_D(cu, n, Lam, c))


def Pbar_M(cu, n, Lam, c):
    return math.log(11.17) + math.log(nubar_D(cu, n, c)) + math.log(Kbar_D(cu, n, Lam, c))


def ell_c(cu, c):
    return LN2 + 3 * cu.u + 2.25 * c + math.log(1 / c)


def mstar(cu, ell):
    return ((math.sqrt(ell / 2) + math.sqrt(ell / 2 + 2 * cu.p)) / cu.p) ** 2


def varpi(cu, m, c):
    v = (m + 1) * LN2
    ell = ell_c(cu, c)
    if m >= mstar(cu, ell):
        v = min(v, m * cu.a + cu.u * (1 + math.sqrt(m * ell / 2)) + 4 / (3 * cu.p) * (ell + 2) + math.log(m + 1.0))
    return v


def w_acc(c):
    return math.log(math.exp(c) * (1 + c) / (1 - c) + 2 * c) + c


def Hb(x):
    return -x * math.log(x) - (1 - x) * math.log(1 - x)


def E_base(cu, d, x, Lam):
    """E_base of Proposition Q5(a)."""
    eta = min(0.5, math.tanh(x / 4.0))
    K0 = 3 * (1 + eta) / eta ** 2 * (math.log(4.0) + Lam) + 1
    v = 2 * math.exp(3 * cu.u + min(x / 2, math.log(3.0))) / math.expm1(x / 2)
    ell = max(math.log(v), 0.0)
    return math.log(8 * K0) + max(mstar(cu, ell) * Hb(cu.p),
                                  cu.u * (1 + math.sqrt(d * ell / 2)) + 4 / (3 * cu.p) * (ell + 2) + math.log(d + 1.0))


def X_B(cu, N):
    return math.log(12.0) + 2 * math.log(N + 1.0) + 2 * cu.u + math.exp(cu.u)


def X_D(cu, N, phi, b=1.0):
    return b + math.log(C3 + 1 + 3 * (phi * N + 1) * math.exp(2 * cu.u + math.exp(cu.u)))


def E_frakB(cu, d, Lam):
    return math.log(8 * (18 * (math.log(4.0) + Lam) + 1)) + math.log(d + 1.0)


def epochs(cu, M):
    """the epoch sequences d_m, J_m, k_m, B_m, R_m, phi_m for m = 0..M."""
    a, h = cu.a, cu.h
    d = [h / (a - h)]
    J, k, B, R, phi = [], [1], [], [], []
    for m in range(M + 1):
        Jm = math.ceil(d[m] - 1e-13)
        J.append(Jm)
        B.append(h * (1 + 1 / d[m]))
        R.append(h / Jm)
        phi.append(R[m] / (a + R[m]))
        d.append(d[m] * (Jm * a + h) / (Jm * a - h * d[m]))
        k.append(k[m] + Jm + 1)
    return dict(d=d, J=J, k=k, B=B, R=R, phi=phi)


class Chain:
    """the chain T[G'; alpha, m] of Proposition T (horizon N, exponent Bp, coarse accuracy calX)."""

    def __init__(self, cu, N, Bp, calX, alpha, m):
        self.cu, self.N, self.Bp, self.calX, self.alpha, self.m = cu, N, Bp, calX, alpha, int(m)
        u = cu.u
        self.NT = math.ceil(N / self.m)
        self.c = alpha / (13.0 * self.NT)
        self.w = w_acc(self.c)
        self.alow = alpha - self.NT * self.w
        self.d0 = max(self.m + math.floor(calX / (2 * u)) + 1,
                      math.ceil(math.log(6 / (5 * self.c)) / math.log((1 + math.exp(u)) / 2)))

    def j(self, d):
        return 0 if d < self.d0 else (d - self.d0) // self.m + 1

    @staticmethod
    def design_m(cu, N, Bp, calX, alpha, Lam_in):
        """least m >= 1 with  m B' >= X + Pbar_cnt(N, Lam_in + N B'; alpha/(13 ceil(N/m))) + ln 4   (4.1)."""
        def ok(m):
            c = alpha / (13.0 * math.ceil(N / m))
            return m * Bp >= calX + Pbar_cnt(cu, N, Lam_in + N * Bp, c) + math.log(4.0)
        hi = 1
        while not ok(hi):
            hi *= 2
        lo = hi // 2
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if ok(mid):
                hi = mid
            else:
                lo = mid
        return hi

    def qT(self, d, Lam):
        return math.log(8.0) + Pbar_M(self.cu, d, Lam, self.c)

    def Lam_star(self, d, Lam):
        for _ in range(self.j(d)):
            Lam = Lam + self.qT(d, Lam)
        return Lam

    def a_T(self, d, Lam):
        return varpi(self.cu, self.m, self.c) - self.m * self.Bp + Pbar_M(self.cu, d, Lam, self.c) + math.log(4.0)

    def e0(self, Lam):
        d1 = self.d0 - 1
        return min(d1 * (LN2 - self.Bp), d1 * max(self.cu.a - self.Bp, 0.0) + E_base(self.cu, d1, self.alow, Lam))

    def A_T(self, d, Lam):
        return max(self.a_T(d, Lam), self.e0(Lam))

    def Delta_T(self, d, Lam):
        return max(0.0, self.calX + Pbar_cnt(self.cu, d, Lam, self.c) + math.log(4.0) - self.m * self.Bp)

    def E_T(self, d, Lam, Efun=None):
        Ls = self.Lam_star(d, Lam)
        E = 0.0 if Efun is None else Efun(d, self.calX, Ls)
        return E + self.A_T(d, Ls) + self.j(d) * self.Delta_T(d, Ls)
