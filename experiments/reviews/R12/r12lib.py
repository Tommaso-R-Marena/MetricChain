#!/usr/bin/env python3
"""Referee R12 -- own library for the review of workstream Q (docs/workstreams/Q_REPORT.md).

Written from the definitions of docs/workstreams/K_REPORT.md sections 2.1-2.2 (tables, r_dagger, pi_dagger,
all constants of Theorem K1 = Theorem 11.56) and from the *text* of Q_REPORT.md (the design of its sections 3-5
and the error terms of its (5.2)).  Nothing of experiments/workstreams/Q is imported or was copied.

Contents
  Cube            constants of the cube class at slope u (p_u, a, h, eps*, rho_e, theta_na, epoch sequences)
  ExactTab        tables of Q_m in exact arithmetic (big integers; mpmath for the two exponential sums)
  Tab             the same tables as float64 logarithms (for large m); validated against ExactTab in r12_01
  level_consts / level_cmax
                  every constant of Theorem K1 for given parameters, and ln C_max
  Base, Slope, Drop
                  the certified families G_0, S[.], D[.] of Q_REPORT sections 3, 4.1, 4.2 with their exact
                  certified costs, the checks of the two propositions at every level built, and the check of
                  the induction inequality H(B, sigma, R; E) at every node
  Formula         the error terms of Q_REPORT (c_S, q_S, c_D, q_D, cbar_pi, E_base) and its (5.2)
"""
import math
import bisect
from fractions import Fraction
import numpy as np

LN2 = math.log(2.0)
INF = float('inf')
E1 = math.e


# ----------------------------------------------------------------------------------------------------------
#  constants of the cube
# ----------------------------------------------------------------------------------------------------------

def Hbin(r):
    if r <= 0.0 or r >= 1.0:
        return 0.0
    return -r * math.log(r) - (1 - r) * math.log(1 - r)


def kl_half(r):
    """KL(r || 1/2)"""
    return LN2 - Hbin(r)


def kl(r, p):
    """KL(r || p), 0 <= r <= 1, 0 < p < 1"""
    s = 0.0
    if r > 0:
        s += r * math.log(r / p)
    if r < 1:
        s += (1 - r) * math.log((1 - r) / (1 - p))
    return s


class Cube:
    def __init__(self, u):
        self.u = float(u)
        u = self.u
        self.p = 1.0 / (1.0 + math.exp(u))
        self.Lam1 = math.log(2.0 / (1.0 + math.exp(-u)))
        self.eps_star = math.log(math.cosh(u / 2))
        self.a = kl_half(self.p)
        self.rho_h = self.Lam1 / u
        self.h = kl_half(self.rho_h)
        self.Hp = Hbin(self.p)
        a, h = self.a, self.h
        self.kappa = h * h * a / ((a - h) * (a + h) * (2 * a - h))
        self.c1 = h * (1 + self.kappa) / self.kappa
        self.c2 = (a + h) * (2 * a - h) / (h * a) - 2
        self.rbar = (2 * a - h) / (a - h)
        self.Cstar = 2 * math.sqrt((1 + self.rbar) * self.c1 * (a / h + 4))

    def rho_e(self, e):
        """rho in [p_u, 1/2] with KL(rho || p_u) = min(e, eps*)"""
        t = min(e, self.eps_star)
        if t >= self.eps_star:
            return 0.5
        if t <= 0:
            return self.p
        lo, hi = self.p, 0.5
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if kl(mid, self.p) <= t:
                lo = mid
            else:
                hi = mid
        return lo

    def theta_na(self, e):
        return kl_half(self.rho_e(e))

    def epochs(self, M):
        """d_m, J_m, k_m, B_m, R_m, phi_m for m = 0..M (J, R, phi for m < M are the ones used)"""
        a, h = self.a, self.h
        d = [h / (a - h)]
        J = []
        k = [1]
        for m in range(M + 1):
            Jm = math.ceil(d[m])
            J.append(Jm)
            d.append(d[m] * (Jm * a + h) / (Jm * a - h * d[m]))
            k.append(k[m] + Jm + 1)
        B = [h * (1 + 1 / dm) for dm in d]
        R = [h / Jm for Jm in J]
        phi = [h / (Jm * a + h) for Jm in J]
        return dict(d=d[:M + 1], J=J, k=k[:M + 1], B=B[:M + 1], R=R, phi=phi)


# ----------------------------------------------------------------------------------------------------------
#  exact tables (big integers + mpmath)
# ----------------------------------------------------------------------------------------------------------

class ExactTab:
    """Q_m, slope u (an mpmath number or a float converted exactly), in exact / high-precision arithmetic.

    C[j] = C(m,j), Bv[r] = |B(m,r)| (integers);
    E[r] = sum_{j<=r} C(m,j)(e^{u(r+1-j)} - 1),  T[k] = sum_j C(m,j) e^{-u (j-k)_+}   (mpmath numbers).
    """

    def __init__(self, m, u, dps=60):
        import mpmath as mp
        self.mp = mp
        mp.mp.dps = dps
        self.m = m
        self.u = mp.mpf(u)
        C = [1]
        for j in range(1, m + 1):
            C.append(C[-1] * (m - j + 1) // j)
        Bv = []
        s = 0
        for j in range(m + 1):
            s += C[j]
            Bv.append(s)
        assert Bv[m] == 1 << m
        self.C, self.Bv = C, Bv
        eu = mp.exp(self.u)
        emu = 1 / eu
        F = mp.mpf(0)
        E = []
        for r in range(m + 1):
            F = eu * (F + C[r])                 # F_r = sum_{j<=r} C(m,j) e^{u(r+1-j)}
            E.append(F - Bv[r])
        G = [mp.mpf(0)] * (m + 1)                # G_k = sum_{j>k} C(m,j) e^{-u(j-k)}
        for kk in range(m - 1, -1, -1):
            G[kk] = emu * (C[kk + 1] + G[kk + 1])
        T = [Bv[kk] + G[kk] for kk in range(m + 1)]
        self.E, self.T = E, T
        self.lnE = [mp.log(x) for x in E]
        self.lnT = [mp.log(x) for x in T]
        self.lnB = [mp.log(x) for x in Bv]
        # one-sided ratio
        self.lnGt = [mp.log(mp.expm1(self.u))] + [self.lnE[r] - self.lnB[r - 1] for r in range(1, m + 1)]

    def kappa(self, r, ceta):
        """largest k >= 0 with |B(m,k)| <= max(1, c_eta |B(m,r-1)|); ceta a Fraction"""
        if r == 0:
            t = 1
        else:
            num = ceta.numerator * self.Bv[r - 1]
            t = max(1, num // ceta.denominator)       # |B(m,k)| integer:  B_k <= x  iff  B_k <= floor(x)
        return max(0, bisect.bisect_right(self.Bv, t) - 1)

    def lnGpp(self, eta):
        """ln Gamma''(r), r = 0..m, for eta a Fraction"""
        ceta = (1 - eta) / (1 + eta)
        kap = [self.kappa(r, ceta) for r in range(self.m + 1)]
        return [self.lnE[r] - self.lnT[kap[r]] for r in range(self.m + 1)], kap

    def rdag(self, eta, ln_theta, ln_onemeta_nu0, lnGpp=None):
        """r_dagger from the definition (K_REPORT 2.1): the largest r in {0..m-1} such that for every r' <= r
        [N] Gt(r') <= theta (1-eta) nu0  and  [P] min(Gt(r')/c_eta, G''(r')) <= theta;  -1 if it fails at 0.
        Also returns the smallest margin (in the logarithm) of a satisfied / of the first violated condition."""
        mp = self.mp
        ceta = (1 - eta) / (1 + eta)
        lnceta = mp.log(mp.mpf(ceta.numerator) / ceta.denominator)
        if lnGpp is None:
            lnGpp, _ = self.lnGpp(eta)
        r = -1
        for rp in range(self.m):
            okN = self.lnGt[rp] <= ln_theta + ln_onemeta_nu0
            okP = min(self.lnGt[rp] - lnceta, lnGpp[rp]) <= ln_theta
            if okN and okP:
                r = rp
            else:
                break
        return r

    def ln_inv_pidag(self, r):
        mp = self.mp
        if r < 0:
            return (self.m + 1) * mp.log(2)
        return self.m * mp.log(2) - self.lnB[r]


# ----------------------------------------------------------------------------------------------------------
#  float tables (logarithms), for large m
# ----------------------------------------------------------------------------------------------------------

_LG = np.zeros(2)


def _lg(nmax):
    """table of ln k! for k = 0..nmax (math.lgamma, not a cumulative sum)"""
    global _LG
    if _LG.shape[0] < nmax + 1:
        _LG = np.array([math.lgamma(k + 1.0) for k in range(max(nmax + 1, 2 * _LG.shape[0]))])
    return _LG


TOL = 1e-12        # tolerance of comparisons of logarithms of table entries (ties in exact arithmetic)


class Tab:
    """float64 logarithms of the tables of Q_m"""
    __slots__ = ('m', 'u', 'lC', 'lB', 'lE', 'lT', 'lGt', 'mln2', '_kap', '_gpp')

    def __init__(self, m, u):
        self.m, self.u = m, u
        lg = _lg(m)
        j = np.arange(m + 1)
        self.lC = lg[m] - lg[j] - lg[m - j]
        self.lB = np.logaddexp.accumulate(self.lC)
        w = self.lC - u * j
        lF = u * (j + 1.0) + np.logaddexp.accumulate(w)             # ln sum_{j<=r} C e^{u(r+1-j)}
        self.lE = lF + np.log1p(-np.exp(self.lB - lF))
        suf = np.logaddexp.accumulate(w[::-1])[::-1]                # ln sum_{j>=k} C e^{-uj}
        lG = np.full(m + 1, -INF)
        lG[:m] = u * j[:m] + suf[1:]
        self.lT = np.logaddexp(self.lB, lG)
        self.lGt = np.empty(m + 1)
        self.lGt[0] = math.log(math.expm1(u))
        self.lGt[1:] = self.lE[1:] - self.lB[:-1]
        self.mln2 = m * LN2
        self._kap = {}
        self._gpp = {}

    def kappa(self, lceta):
        key = round(lceta, 14)
        if key not in self._kap:
            prev = np.concatenate(([-INF], self.lB[:-1]))
            v = np.maximum(0.0, lceta + prev)
            self._kap[key] = np.maximum(0, np.searchsorted(self.lB, v + TOL, side='right') - 1)
        return self._kap[key]

    def lGpp(self, lceta):
        key = round(lceta, 14)
        if key not in self._gpp:
            self._gpp[key] = self.lE - self.lT[self.kappa(lceta)]
        return self._gpp[key]


class TabCache:
    def __init__(self, u, maxitems=40):
        self.u = u
        self.maxitems = maxitems
        self.d = {}
        self.order = []

    def get(self, m):
        t = self.d.get(m)
        if t is None:
            t = Tab(m, self.u)
            self.d[m] = t
            self.order.append(m)
            if len(self.order) > self.maxitems:
                old = self.order.pop(0)
                del self.d[old]
        return t


# ----------------------------------------------------------------------------------------------------------
#  one level of Algorithm 2L+: the constants of K_REPORT 2.2 and ln C_max
# ----------------------------------------------------------------------------------------------------------

def level_consts(cube, tab, n, n_o, lam, eta, etap, ltheta, nu1, b, ldelta, L):
    """All constants of Theorem K1 that do not depend on the inner costs.  tab = Tab(n_o, u).
    ltheta = ln theta, ldelta = ln delta.  Returns a dict (logarithms where the numbers are large)."""
    u = cube.u
    assert n >= 2 and 1 <= n_o <= n - 1 and 0 < lam <= 1 and 0 < eta <= 0.5 and 0 < etap <= 1 and nu1 >= 1 and b > 0 and L >= 1
    n_i = n - n_o
    J = math.ceil((2 * u * n + b + n_o * LN2) / lam)
    nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
    lceta = math.log((1 - eta) / (1 + eta))
    lGt = tab.lGt
    lGpp = tab.lGpp(lceta)
    okN = lGt[:n_o] <= ltheta + math.log((1 - eta) * nu0) + TOL
    okP = np.minimum(lGt[:n_o] - lceta, lGpp[:n_o]) <= ltheta + TOL
    bad = np.nonzero(~(okN & okP))[0]
    rdag = (int(bad[0]) - 1) if bad.size else n_o - 1
    l_inv_pi = (tab.mln2 - tab.lB[rdag]) if rdag >= 0 else (n_o + 1) * LN2       # ln(1/pi_dagger)
    m_max = math.ceil((math.log(2 * (1 + eta) / (1 - eta)) + lam + math.log(nu0) + l_inv_pi) / LN2)
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(2.0 * (J + 1) * (m_max + 1) * (L + 2)) - ldelta))
    lK = math.log(K)
    lMdag = lK - math.log(1 - eta) + l_inv_pi
    lMbar = math.log(2 * (1 + eta)) + lam + math.log(nu0) + lMdag
    ldeltap = ldelta - math.log(4.0 * L) - lMbar
    xout = float(np.logaddexp(n * math.log(2 * cube.p),
                              b + np.logaddexp(math.log(math.exp(lam) * (1 + eta) / (1 - eta) + etap), ltheta)))
    P_M = math.log(4 * (1 + eta) * math.exp(lam) / (1 - eta)) + math.log(nu0) + lK
    P_cnt = math.log(J + 1) + math.log(2 * (1 + eta) ** 2 * math.exp(lam) / (1 - eta)) + math.log(nu0) + lK
    return dict(n=n, n_o=n_o, n_i=n_i, J=J, nu0=nu0, rdag=rdag, l_inv_pi=float(l_inv_pi), m_max=m_max, K=K, lK=lK,
                lMbar=float(lMbar), ldeltap=float(ldeltap), xout=xout, P_M=P_M, P_cnt=P_cnt, L=L, lam=lam, eta=eta,
                Lam=float(LN2 + lMbar))


def level_cmax(cs, xs, lC):
    """ln C_max = ln( 1 + 2 Mbar + sum_l min{2 Mbar, (J+1) cnt(x_{l-1})} C_l ),  xs = [x_0, ..., x_L], lC[l-1] = ln C_l.
    Also returns the index l of the largest term (0: the outer sample)."""
    L = cs['L']
    assert len(xs) == L + 1 and len(lC) == L
    xs = np.asarray(xs, dtype=float)
    lC = np.asarray(lC, dtype=float)
    assert np.all(np.diff(xs) < 0), "ladder not decreasing"
    eta, lam = cs['eta'], cs['lam']
    lcnt = np.maximum(cs['lK'], math.log(2 * (1 + eta) ** 2 / (1 - eta)) + lam + cs['lK'] + math.log(cs['nu0']) + xs[:-1])
    mult = np.minimum(LN2 + cs['lMbar'], math.log(cs['J'] + 1) + lcnt)
    terms = np.concatenate(([0.0, LN2 + cs['lMbar']], mult + lC))
    lCmax = float(np.logaddexp.reduce(terms))
    arg = int(np.argmax(terms))
    return lCmax, (0 if arg <= 1 else arg - 1)


# ----------------------------------------------------------------------------------------------------------
#  error terms of Q_REPORT (formulas typed from its text)
# ----------------------------------------------------------------------------------------------------------

class Formula:
    def __init__(self, cube):
        self.c = cube

    # --- functions of the dimension (section 4)
    def A(self, n):
        return (2 * self.c.u + LN2) * n + 3

    def clog(self, n):
        return math.log(n + 1) + math.log(6) + 2 * self.c.u + math.exp(self.c.u)

    def X0(self, n):
        return 1 + self.clog(n) + self.c.h

    # --- slope step (Proposition Q6)
    def mbarS(self, n):
        return n + 2 + math.log2(12 * E1 * (E1 - 1) * self.A(n))

    def KbarS(self, n, Lam):
        return 18 * (Lam + math.log(2) + math.log(self.A(n)) + math.log(self.mbarS(n)) + math.log(n + 3)) + 1

    def cS(self, n, Lam, B):
        return ((1 + self.clog(n) + self.c.h) * B / self.c.h + 1 + 2 * math.log(self.A(n)) + math.log(18 * E1 * (E1 - 1))
                + math.log(self.KbarS(n, Lam)) + math.log(n + 3))

    def qS(self, n, Lam):
        return math.log(4 * (n + 1)) + math.log(self.A(n)) + math.log(24 * E1 * (E1 - 1)) + math.log(self.KbarS(n, Lam))

    # --- bounded theta (Lemma Q3)
    def mstar(self, ell):
        p = self.c.p
        return ((math.sqrt(ell / 2) + math.sqrt(ell / 2 + 2 * p)) / p) ** 2

    def cbar_pi(self, m, ell):
        c = self.c
        return max(LN2 + self.mstar(ell) * c.Hp,
                   c.u * (1 + math.sqrt(m * ell / 2)) + (4 / (3 * c.p)) * (ell + 2) + math.log(m + 1))

    # --- drop (Proposition Q7)
    @staticmethod
    def w(cc):
        return math.log(math.exp(cc) * (1 + cc) / (1 - cc) + 2 * cc) + cc

    def ell_c(self, cc):
        return LN2 + 3 * self.c.u + 2.25 * cc + math.log(1 / cc)

    def nDp(self, cc):
        u = self.c.u
        return max(2 / u + 2, math.log(6 / (5 * cc)) / math.log((1 + math.exp(u)) / 2))

    def varsigma(self, n, cc, R):
        phi = R / (self.c.a + R)
        return self.cbar_pi(math.floor(phi * n), self.ell_c(cc)) / (self.c.a + R)

    def nubarD(self, n, cc):
        return (1.8 * self.A(n) + 3 * math.exp(self.c.u) * n) / cc

    def mbarD(self, n, cc):
        return n + 2 + math.log2(5.6 * self.nubarD(n, cc))

    def KbarD(self, n, Lam, cc):
        return 4 / cc ** 2 * (Lam + math.log(2) + math.log(self.A(n) / cc) + math.log(self.mbarD(n, cc)) + math.log(n + 4)) + 1

    def PbarCnt(self, n, Lam, cc):
        return math.log(self.A(n) / cc) + math.log(7.45) + math.log(self.nubarD(n, cc)) + math.log(self.KbarD(n, Lam, cc))

    def PbarM(self, n, Lam, cc):
        return math.log(11.17) + math.log(self.nubarD(n, cc)) + math.log(self.KbarD(n, Lam, cc))

    def cD(self, n, Lam, B, R, cc, shift=True, parts=False):
        c = self.c
        phi = R / (c.a + R)
        cpi = self.cbar_pi(math.floor(phi * n), self.ell_c(cc))
        Bp = B * c.a / (c.a + R)
        first = B * (1 + phi * self.nDp(cc))
        sq = cpi * Bp / c.a if shift else cpi           # B*varsigma(n) = cbar_pi * B'/a ; without shift: cbar_pi
        rest = math.log(n + 4) + 1 + self.PbarCnt(n, Lam, cc)
        if parts:
            return first, sq, rest
        return first + sq + rest

    def qD(self, n, Lam, cc):
        return math.log(4 * (n + 2)) + self.PbarM(n, Lam, cc)

    # --- base family (Proposition Q5(a))
    @staticmethod
    def eta_x(x):
        return min(0.5, math.tanh(x / 4))

    def Kbar0(self, x, Lam):
        e = self.eta_x(x)
        return 3 * (1 + e) / e ** 2 * (math.log(4) + Lam) + 1

    def ell0(self, x):
        lden = math.log(math.expm1(x / 2)) if x < 1000 else x / 2          # ln(e^{x/2} - 1)
        v = math.log(2) + 3 * self.c.u + min(x / 2, math.log(3)) - lden
        return max(0.0, v)

    def Ebase(self, d, x, Lam):
        c = self.c
        l0 = self.ell0(x)
        return math.log(8 * self.Kbar0(x, Lam)) + max(self.mstar(l0) * c.Hp,
                                                      c.u * (1 + math.sqrt(d * l0 / 2)) + (4 / (3 * c.p)) * (l0 + 2) + math.log(d + 1))

    # --- the schedule of section 5 and the error term (5.2)
    def schedule(self, eps, M):
        eh = min(eps, 1.0)
        cm = [eh / (13.0 * (m + 1) * (m + 2)) for m in range(M)]
        alpha = [0.0] * (M + 1)
        alpha[M] = eh
        for m in range(M - 1, -1, -1):
            alpha[m] = alpha[m + 1] - self.w(cm[m])
        return eh, cm, alpha

    def E_total(self, n, eps, ldelta, M, detail=False):
        """the error term (5.2); returns (E_M, B_M, k_M) or a detailed dict"""
        c = self.c
        ep = c.epochs(M)
        eh, cm, alpha = self.schedule(eps, M)
        Lam0 = -ldelta + n * LN2
        Lam = Lam0
        tot_S = tot_Dsq = tot_Drest = 0.0
        nS = 0
        for m in range(M - 1, -1, -1):
            B, R = ep['B'][m], ep['R'][m]
            f, sq, rest = self.cD(n, Lam, B, R, cm[m], parts=True)
            tot_Dsq += sq
            tot_Drest += f + rest
            Lam += self.qD(n, Lam, cm[m])
            for _ in range(ep['J'][m]):
                tot_S += self.cS(n, Lam, B)
                nS += 1
                Lam += self.qS(n, Lam)
        eb = self.Ebase(n, alpha[0], Lam)
        E = eb + tot_S + tot_Dsq + tot_Drest
        if detail:
            return dict(E=E, B=ep['B'][M], k=ep['k'][M], base=eb, S=tot_S, nS=nS, Dsq=tot_Dsq, Drest=tot_Drest,
                        LamT=Lam, Lam0=Lam0, alpha0=alpha[0])
        return E, ep['B'][M], ep['k'][M]


# ----------------------------------------------------------------------------------------------------------
#  certified families
# ----------------------------------------------------------------------------------------------------------

class Stats:
    def __init__(self):
        self.nodes = 0
        self.viol = []                       # list of strings
        self.min_ind = INF                   # least slack of the induction inequality
        self.min_ind_at = None
        self.min_q3 = INF
        self.min_q4 = INF
        self.min_q6 = INF                    # least slack of the bound of Proposition Q6 for a level as built
        self.min_q7 = INF
        self.min_q7ns = INF
        self.built = dict(S=0, Dshift=0, Dnoshift=0, Dpass=0, Spass=0)    # S: slope levels built; D*: variant CHOSEN at a drop node
        self.lev = dict(Dshift=0, Dnoshift=0)                                # drop levels built and checked
        self.max_xout_err = 0.0

    def bad(self, s):
        if len(self.viol) < 200:
            self.viol.append(s)
        else:
            self.viol.append('')


class Family:
    """interface: cost(d, x, ld) -> ln of the certified cost bound;  B, sigma, R, xmin;  E(d, x, Lam)"""

    def check_node(self, d, x, ld, cost):
        st = self.st
        st.nodes += 1
        Lam = -ld + d * LN2
        bound = d * self.B - self.sigma * min(x, self.R * d if self.R < INF else INF) + self.E(d, x, Lam)
        sl = bound - cost
        if sl < st.min_ind:
            st.min_ind = sl
            st.min_ind_at = (type(self).__name__, self.tag, d, x, ld)
        if sl < -1e-9:
            st.bad("induction: %s%s d=%d x=%.6g ld=%.6g cost=%.4f bound=%.4f" % (type(self).__name__, self.tag, d, x, ld, cost, bound))


class Base(Family):
    """G_0: the two-sample bracket of Proposition K0, or enumeration if no radius qualifies or if 2M >= 2^d"""

    def __init__(self, cube, tabs, st, fm, tag=''):
        self.c, self.tabs, self.st, self.fm, self.tag = cube, tabs, st, fm, tag
        self.B, self.sigma, self.R, self.xmin = cube.a, 0.0, INF, 0.0
        self.memo = {}
        self._rm = {}

    def E(self, d, x, Lam):
        return self.fm.Ebase(d, x, Lam)

    def _runmax(self, d, eta):
        key = (d, round(eta, 14))
        r = self._rm.get(key)
        if r is None:
            if len(self._rm) > 60:
                self._rm.clear()
            t = self.tabs.get(d)
            g = np.logaddexp(0.0, t.lGpp(math.log((1 - eta) / (1 + eta)))[:d])       # ln(1 + Gamma''(r)), r <= d-1
            r = (np.maximum.accumulate(g), t.lB)
            self._rm[key] = r
        return r

    def raw(self, d, x, ld):
        """(ln cost, kind, r*)"""
        eta = min(0.5, math.tanh(x / 4))
        K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) - ld))
        budget = x - math.log((1 + eta) / (1 - eta))
        rm, lB = self._runmax(d, eta)
        rstar = int(np.searchsorted(rm, budget + TOL, side='right')) - 1
        if rstar < 0:
            return d * LN2, 'enum', -1
        lM = math.log(K) + d * LN2 - math.log(1 - eta) - lB[rstar]
        lM = lM + math.log1p(math.exp(-lM))                    # the ceiling: M <= X + 1
        if LN2 + lM >= d * LN2:
            return d * LN2, 'enum', rstar
        return LN2 + lM, 'K0', rstar

    def cost(self, d, x, ld):
        key = (d, x, ld)
        v = self.memo.get(key)
        if v is None:
            v = self.raw(d, x, ld)[0]
            self.memo[key] = v
            self.check_node(d, x, ld, v)
        return v

    def cost_many(self, d, xs, ld):
        """the same as cost() for a list of accuracies; the rungs with eta = 1/2 (x >= 2 ln 3) are done in one
        numpy pass (no memo), the others one by one.  Checked against the scalar path in r12_05 (self-test)."""
        xs = list(xs)
        out = [None] * len(xs)
        big = [i for i, x in enumerate(xs) if x >= 2 * math.log(3)]
        for i, x in enumerate(xs):
            if x < 2 * math.log(3):
                out[i] = self.cost(d, x, ld)
        if big:
            c, st = self.c, self.st
            xb = np.array([xs[i] for i in big])
            K = math.ceil(18.0 * (math.log(4) - ld))
            rm, lB = self._runmax(d, 0.5)
            rstar = np.searchsorted(rm, xb - math.log(3) + TOL, side='right') - 1
            ok = rstar >= 0
            lM = math.log(K) + d * LN2 + LN2 - lB[np.maximum(rstar, 0)]
            lM = lM + np.log1p(np.exp(-lM))
            cost = np.where(ok, np.minimum(LN2 + lM, d * LN2), d * LN2)
            # node check:  cost <= d a + E_base(d, x; Lam),  Lam = ln(1/delta) + d ln 2   (eta_x = 1/2 here)
            Lam = -ld + d * LN2
            l0 = np.maximum(0.0, math.log(2) + 3 * c.u + math.log(3) - np.where(xb < 1000, np.log(np.expm1(np.minimum(xb, 1000) / 2)), xb / 2))
            p = c.p
            mst = ((np.sqrt(l0 / 2) + np.sqrt(l0 / 2 + 2 * p)) / p) ** 2
            Eb = math.log(8 * (18 * (math.log(4) + Lam) + 1)) + np.maximum(mst * c.Hp, c.u * (1 + np.sqrt(d * l0 / 2)) + (4 / (3 * p)) * (l0 + 2)
                                                                             + math.log(d + 1))
            sl = d * c.a + Eb - cost
            st.nodes += len(big)
            k = int(np.argmin(sl))
            if sl[k] < st.min_ind:
                st.min_ind = float(sl[k])
                st.min_ind_at = ('Base', self.tag, d, float(xb[k]), ld)
            if sl[k] < -1e-9:
                st.bad("induction: Base d=%d x=%.6g ld=%.6g slack=%.4f" % (d, float(xb[k]), ld, float(sl[k])))
            for i, v in zip(big, cost):
                out[i] = float(v)
        return out


class Slope(Family):
    """S[F] of Q_REPORT 4.1.  F has H(B, sigma, R; E); S[F] has H(B, sigma + B/h - 1, R'; E')."""

    def __init__(self, cube, tabs, st, fm, inner, tag='', only_built=False):
        self.c, self.tabs, self.st, self.fm, self.inner, self.tag = cube, tabs, st, fm, inner, tag
        h = cube.h
        assert inner.B >= h - 1e-15 and 0 <= inner.sigma <= 1 + 1e-12 and inner.xmin <= 1
        assert inner.R == INF or 0 < inner.R <= h * (1 + 1e-12)
        if inner.R == INF:
            assert inner.sigma == 0
        self.Rp = h if inner.R == INF else inner.R * h / (h + inner.R)
        self.B = inner.B
        self.sigma = inner.sigma + inner.B / h - 1
        self.R = self.Rp
        self.xmin = inner.xmin
        self.memo = {}
        self.only_built = only_built          # 'proof' variant: the level as built and nothing else

    def E(self, d, x, Lam):
        return self.inner.E(d, min(x, 1.0), Lam + self.fm.qS(d, Lam)) + self.fm.cS(d, Lam, self.B)

    def cost(self, d, x, ld):
        key = (d, x, ld)
        v = self.memo.get(key)
        if v is not None:
            return v
        c, fm, st = self.c, self.fm, self.st
        xh = min(x, self.Rp * d)
        if xh < fm.X0(d):
            st.built['Spass'] += 1
            v = self.inner.cost(d, x, ld)
        else:
            lev = self.level(d, xh, ld)
            if self.only_built:
                v = lev
            else:
                v = min(lev, self.inner.cost(d, x, ld))
        self.memo[key] = v
        self.check_node(d, x, ld, v)
        return v

    def cost_many(self, d, xs, ld):
        return [self.cost(d, x, ld) for x in xs]

    def level(self, n, xh, ld):
        """the level as built at accuracy xh = x-hat >= X_0(n); returns ln C_max and checks Proposition Q6"""
        c, fm, st = self.c, self.fm, self.st
        u, h = c.u, c.h
        n_o = math.floor((xh - 1 - fm.clog(n)) / h + 1e-12)      # 1e-12: xh = X_0(n) exactly must give n_o = 1 in floating point
        n_i = n - n_o
        assert 1 <= n_o <= n - 1
        ltheta = (xh - 1) + math.log1p(-((3 * E1 + 1) + math.exp(n * math.log(2 * c.p) - 1)) * math.exp(-(xh - 1)))
        x1 = min(math.ceil(xh), math.ceil(2 * u * n_i) - 1)
        assert 1 <= x1 < 2 * u * n_i
        xs = [2 * u * n_i] + [float(v) for v in range(x1, 0, -1)]
        L = x1
        tab = self.tabs.get(n_o)
        cs = level_consts(c, tab, n, n_o, 1.0, 0.5, 1.0, ltheta, 1.0, 1.0, ld, L)
        st.built['S'] += 1
        st.max_xout_err = max(st.max_xout_err, abs(cs['xout'] - xh))
        if abs(cs['xout'] - xh) > 1e-7:
            st.bad("slope: accuracy %.9g instead of %.9g at n=%d" % (cs['xout'], xh, n))
        # Lemma Q4 at m = n_o, e = h
        r1 = min(n_o - 1, math.floor(c.rho_h * n_o) + 1)
        if cs['rdag'] < r1:
            st.bad("Q4 radius: n_o=%d rdag=%d < %d" % (n_o, cs['rdag'], r1))
        s4 = n_o * h + math.log(n_o + 1) - cs['l_inv_pi']
        st.min_q4 = min(st.min_q4, s4)
        if s4 < -1e-9:
            st.bad("Q4 pi: n_o=%d slack %.4g" % (n_o, s4))
        # (4.1)
        if cs['Lam'] > xh - 1 + cs['P_M'] + 1e-9:
            st.bad("(4.1): n=%d xh=%.6g" % (n, xh))
        # step (3) of the proof of Proposition Q6, constant by constant
        An = fm.A(n)
        KS = fm.KbarS(n, -ld)
        if not (cs['J'] + 1 <= An + 1e-9 and abs(cs['nu0'] - 2 * (E1 - 1) * (cs['J'] + 1)) < 1e-6 * cs['nu0']
                and cs['m_max'] + 1 <= fm.mbarS(n) + 1e-9 and L <= h * n + 1 + 1e-9 and cs['K'] <= KS + 1e-6
                and cs['P_cnt'] <= 2 * math.log(An) + math.log(18 * E1 * (E1 - 1)) + math.log(KS) + 1e-9
                and cs['P_M'] <= math.log(An) + math.log(24 * E1 * (E1 - 1)) + math.log(KS) + 1e-9
                and ltheta >= xh - 1 - LN2 - 1e-12 and 2 * u * n_i > 1):
            st.bad("Q6 step (3): a constant at n=%d xh=%.6g ld=%.6g" % (n, xh, ld))
        st.nconst = getattr(st, 'nconst', 0) + 1
        lC = self.inner.cost_many(n_i, xs[1:], cs['ldeltap'])
        lCmax, arg = level_cmax(cs, xs, lC)
        # the bound of Proposition Q6 for the level as built, with the actual inner family
        Lam = -ld + n * LN2
        bound = n * self.B - self.sigma * xh + fm.cS(n, Lam, self.B) + self.inner.E(n, 1.0, Lam + fm.qS(n, Lam))
        st.min_q6 = min(st.min_q6, bound - lCmax)
        if lCmax > bound + 1e-9:
            st.bad("Q6 level: n=%d xh=%.6g ld=%.6g lCmax=%.4f bound=%.4f" % (n, xh, ld, lCmax, bound))
        # the handed-down invariant (2.1)
        if -cs['ldeltap'] + n_i * LN2 > Lam + fm.qS(n, Lam) + 1e-9:
            st.bad("(2.1) slope: n=%d" % n)
        return lCmax


class Drop(Family):
    """D[F; c, alpha] of Q_REPORT 4.2.  F has H(B, 1, R; E) with 0 < R <= h <= B; D has H(B a/(a+R), 0, inf; E')."""

    def __init__(self, cube, tabs, st, fm, inner, cc, alpha, R=None, tag='', only_built=False, variants=('shift', 'noshift', 'pass')):
        self.c, self.tabs, self.st, self.fm, self.inner, self.tag = cube, tabs, st, fm, inner, tag
        a, h = cube.a, cube.h
        self.Rin = inner.R if R is None else R
        assert inner.sigma >= 1 - 1e-12 and 0 < self.Rin <= min(h, inner.R) * (1 + 1e-12) and inner.B >= h - 1e-15
        assert 0 < cc <= 1 / 3 and 0 < alpha <= 1
        self.cc, self.alpha = cc, alpha
        self.beta = alpha - fm.w(cc)
        assert self.beta >= inner.xmin - 1e-12 and self.beta > 0
        self.phi = self.Rin / (a + self.Rin)
        self.Bin = inner.B
        self.B = inner.B * a / (a + self.Rin)
        self.sigma, self.R, self.xmin = 0.0, INF, alpha
        self.memo = {}
        self.only_built = only_built
        self.variants = variants
        self.info = {}

    def E(self, d, x, Lam):
        return self.inner.E(d, self.beta, Lam + self.fm.qD(d, Lam, self.cc)) + self.fm.cD(d, Lam, self.Bin, self.Rin, self.cc)

    def cost(self, d, x, ld):
        key = (d, ld)
        v = self.memo.get(key)
        if v is not None:
            return v
        fm, st = self.fm, self.st
        cands = {}
        if d >= fm.nDp(self.cc):
            no_s = math.floor(self.phi * d - fm.varsigma(d, self.cc, self.Rin))
            no_n = math.floor(self.phi * d)
            if no_s >= 1 and 'shift' in self.variants:
                cands['shift'] = self.level(d, no_s, ld, True)
            if no_n >= 1 and 'noshift' in self.variants and not self.only_built:
                cands['noshift'] = self.level(d, no_n, ld, False)
        if self.only_built:
            # 'proof' variant: the level as built (with shift) where it is defined, the pass-through elsewhere
            if 'shift' not in cands:
                cands['pass'] = self.inner.cost(d, self.alpha, ld)
        elif 'pass' in self.variants:
            cands['pass'] = self.inner.cost(d, self.alpha, ld)
        which = min(cands, key=cands.get)
        v = cands[which]
        st.built['D' + which] += 1
        self.info[key] = (which, dict(cands))
        self.memo[key] = v
        self.check_node(d, self.alpha, ld, v)
        return v

    def cost_many(self, d, xs, ld):
        v = self.cost(d, self.alpha, ld)
        return [v] * len(xs)

    def level(self, n, n_o, ld, shift):
        c, fm, st = self.c, self.fm, self.st
        u, a = c.u, c.a
        cc, R = self.cc, self.Rin
        n_i = n - n_o
        x1 = math.ceil(R * n_i)
        assert 1 <= x1 < 2 * u * n_i and 1 <= n_o <= n - 1
        xs = [2 * u * n_i] + [float(v) for v in range(x1, 0, -1)] + [self.beta]
        L = x1 + 1
        tab = self.tabs.get(n_o)
        cs = level_consts(c, tab, n, n_o, cc, cc, cc, math.log(cc), 2 * math.exp(u) * n_o / cc, self.beta, ld, L)
        if cs['xout'] > self.alpha + 1e-12:
            st.bad("drop: accuracy %.9g > alpha %.9g at n=%d" % (cs['xout'], self.alpha, n))
        # Lemma Q3 at m = n_o with ell = ell_c
        s3 = n_o * a + fm.cbar_pi(n_o, fm.ell_c(cc)) - cs['l_inv_pi']
        st.min_q3 = min(st.min_q3, s3)
        if s3 < -1e-9:
            st.bad("Q3: n_o=%d slack %.4g" % (n_o, s3))
        if shift and cs['Lam'] > cs['P_M'] + R * n_i + 1e-9:
            st.bad("(4.2): n=%d" % n)
        # step (3) of the proof of Proposition Q7, constant by constant
        An = fm.A(n)
        KD = fm.KbarD(n, -ld, cc)
        if not (cs['J'] + 1 <= An / cc * (1 + 1e-12) and cs['nu0'] <= fm.nubarD(n, cc) * (1 + 1e-12)
                and cs['m_max'] + 1 <= fm.mbarD(n, cc) + 1e-9 and L <= c.h * n + 2 + 1e-9 and cs['K'] <= KD * (1 + 1e-12)
                and cs['P_cnt'] <= fm.PbarCnt(n, -ld, cc) + 1e-9 and cs['P_M'] <= fm.PbarM(n, -ld, cc) + 1e-9
                and n_o < n / 2 and R * n_i + 1 <= 2 * u * n_i):
            st.bad("Q7 step (3): a constant at n=%d n_o=%d c=%.3g ld=%.6g" % (n, n_o, cc, ld))
        st.nconst = getattr(st, 'nconst', 0) + 1
        lC = self.inner.cost_many(n_i, xs[1:], cs['ldeltap'])
        lCmax, arg = level_cmax(cs, xs, lC)
        st.lev['Dshift' if shift else 'Dnoshift'] += 1
        Lam = -ld + n * LN2
        E1_ = self.inner.E(n, self.beta, Lam + fm.qD(n, Lam, cc))
        bound = n * self.B + fm.cD(n, Lam, self.Bin, R, cc, shift=shift) + E1_
        if shift:
            st.min_q7 = min(st.min_q7, bound - lCmax)
        else:
            st.min_q7ns = min(st.min_q7ns, bound - lCmax)
        if lCmax > bound + 1e-9:
            st.bad("Q7 level (%s): n=%d ld=%.6g lCmax=%.4f bound=%.4f" % ('shift' if shift else 'noshift', n, ld, lCmax, bound))
        if -cs['ldeltap'] + n_i * LN2 > Lam + fm.qD(n, Lam, cc) + 1e-9:
            st.bad("(2.1) drop: n=%d" % n)
        self.last = dict(cs=cs, xs=xs, lC=lC, arg=arg)
        return lCmax


class SlopeOne(Family):
    """a family with slope >= 1 on (0, R) read as slope one (Theorem Q8: 'a slope larger than one implies slope one')"""

    def __init__(self, inner):
        self.inner = inner
        self.c, self.tabs, self.st, self.fm, self.tag = inner.c, inner.tabs, inner.st, inner.fm, inner.tag
        assert inner.sigma >= 1 - 1e-12
        self.B, self.sigma, self.R, self.xmin = inner.B, 1.0, inner.R, inner.xmin

    def E(self, d, x, Lam):
        return self.inner.E(d, x, Lam)

    def cost(self, d, x, ld):
        return self.inner.cost(d, x, ld)

    def cost_many(self, d, xs, ld):
        return self.inner.cost_many(d, xs, ld)


def build_design(cube, eps, M, st=None, only_built=False, maxtabs=40, tabs=None):
    """the family G_M of Q_REPORT 5.1; returns (family, list of all families bottom-up, formula object, stats)"""
    st = st or Stats()
    fm = Formula(cube)
    tabs = tabs or TabCache(cube.u, maxtabs)
    ep = cube.epochs(M)
    eh, cm, alpha = fm.schedule(eps, M)
    fam = Base(cube, tabs, st, fm, tag='[G0]')
    fam.xmin = alpha[0]
    fams = [fam]
    for m in range(M):
        assert abs(fam.B - ep['B'][m]) < 1e-12
        for j in range(1, ep['J'][m] + 1):
            fam = Slope(cube, tabs, st, fm, fam, tag='[m=%d,j=%d]' % (m, j), only_built=only_built)
            fams.append(fam)
            assert abs(fam.sigma - j / ep['d'][m]) < 1e-9 and abs(fam.R - cube.h / j) < 1e-12
        fam = SlopeOne(fam)
        assert abs(fam.R - ep['R'][m]) < 1e-12
        fam = Drop(cube, tabs, st, fm, fam, cm[m], alpha[m + 1], tag='[m=%d]' % m, only_built=only_built)
        fams.append(fam)
        assert abs(fam.beta - alpha[m]) < 1e-12 and abs(fam.B - ep['B'][m + 1]) < 1e-12
    return fam, fams, fm, st
