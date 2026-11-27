#!/usr/bin/env python3
"""Workstream Q -- shared routines (numpy only).

Everything that evaluates Theorem 11.56 uses the referee's tables experiments/reviews/R8/r8_flat.TablesF and the
same formulas for the constants as r8_flat.flat_run (K_REPORT.md section 2.2); `selftest()` checks that
`level_consts` + `level_cmax` reproduce flat_run's lCmax, lMbar, K, J, rdag, ldeltap, xout to rounding.

Contents
  Cube(u)                constants p_u, a, h, rho_h, eps*, kappa, c1, c2, rbar and theta_na
  epoch_seq(cube, M)     the epoch sequences d_m, J_m, k_m, B_m, R_m, phi_m of the rate proof (RateFull.lean, closed_form)
  level_consts(...)      exact constants of one level of Algorithm 2L+ (J, nu0, r_dag, pi_dag, m_max, K, Mbar, delta')
  level_cmax(...)        exact ln C_max for a ladder and inner log-costs
  base_cost(...)         the base family G_0 (Proposition K0 or enumeration): exact log cost, vectorised in the accuracy
  the error terms of Q_REPORT.md: c_log, X0, A_n, cS, qS, cD, qD, n_D, cpi_bar, E_base, accuracy schedule, E_total
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "reviews", "R8"))
import r8_flat as F  # noqa: E402

LN2 = math.log(2.0)
NEG_INF = float("-inf")
E1 = math.e


def kl(x, y):
    """binary relative entropy KL(x || y)"""
    s = 0.0
    if x > 0:
        s += x * math.log(x / y)
    if x < 1:
        s += (1 - x) * math.log((1 - x) / (1 - y))
    return s


def Hb(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log(x) - (1 - x) * math.log(1 - x)


class Cube:
    """constants of the class L_u(Q_n)"""

    def __init__(self, u):
        self.u = u
        self.p = 1.0 / (1.0 + math.exp(u))
        self.a = kl(self.p, 0.5)
        self.Lam1 = math.log(2.0 / (1.0 + math.exp(-u)))
        self.rho_h = self.Lam1 / u
        self.h = kl(self.rho_h, 0.5)
        self.eps_star = math.log(math.cosh(u / 2))
        a, h = self.a, self.h
        self.kappa = h * h * a / ((a - h) * (a + h) * (2 * a - h))
        self.c1 = h * (1 + self.kappa) / self.kappa
        self.c2 = (a + h) * (2 * a - h) / (h * a) - 2
        self.rbar = (2 * a - h) / (a - h)
        self.Hp = Hb(self.p)

    def rho_of(self, e):
        """the rho in [p_u, 1/2] with KL(rho || p_u) = e (1/2 from eps* on)"""
        if e >= self.eps_star:
            return 0.5
        if e <= 0:
            return self.p
        lo, hi = self.p, 0.5
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if kl(mid, self.p) <= e:
                lo = mid
            else:
                hi = mid
        return lo

    def theta_na(self, e):
        return kl(self.rho_of(e), 0.5)


def epoch_seq(cube, M):
    """d_m, J_m, k_m, B_m, R_m, phi_m for m = 0..M (epochSeq of RateFull.lean; B_m = h(1 + 1/d_m))"""
    a, h = cube.a, cube.h
    d = [h / (a - h)]
    J = []
    k = [1]
    for m in range(M + 1):
        Jm = int(math.ceil(d[m] - 1e-15))
        if Jm < d[m]:
            Jm += 1
        J.append(Jm)
        d.append(d[m] * (Jm * a + h) / (Jm * a - h * d[m]))
        k.append(k[m] + Jm + 1)
    B = [h * (1 + 1 / dm) for dm in d]
    R = [h / Jm for Jm in J]
    phi = [h / (Jm * a + h) for Jm in J]
    return dict(d=d, J=J, k=k, B=B, R=R, phi=phi)


# ----------------------------------------------------------------------------------------------------------------
# tables with a small cache (the referee's class; its own cache r8_flat._tf is never filled from here)
# ----------------------------------------------------------------------------------------------------------------
_tabs = {}
_tab_order = []
TAB_CACHE = 6


def tab(m, u):
    key = (m, u)
    if key in _tabs:
        return _tabs[key]
    t = F.TablesF(m, u)
    _tabs[key] = t
    _tab_order.append(key)
    if len(_tab_order) > TAB_CACHE:
        old = _tab_order.pop(0)
        _tabs.pop(old, None)
    return t


def rdag_of(t, u, n_o, eta, ltheta, nu0):
    """r_dagger and ln pi_dagger exactly as in r8_flat.flat_run (section 2.1 of K_REPORT)"""
    lceta = math.log((1 - eta) / (1 + eta))
    kap = t.kappa_all(lceta)
    lGt = np.concatenate(([math.log(math.expm1(u))], t.lE[1:] - t.lB[:-1]))
    lGpp = t.lE - t.lT[kap]
    okN = lGt <= ltheta + math.log((1 - eta) * nu0)
    okP = np.minimum(lGt - lceta, lGpp) <= ltheta
    okb = (okN & okP)[:n_o]
    badi = np.nonzero(~okb)[0]
    rdag = (int(badi[0]) - 1) if badi.size else n_o - 1
    lpidag = (float(t.lB[rdag]) - n_o * LN2) if rdag >= 0 else -(n_o + 1) * LN2
    return rdag, lpidag


def level_consts(u, n, n_o, lam, eta, etap, ltheta, nu1, b, ldelta, L, t=None):
    """the constants of Algorithm 2L+ (K_REPORT 2.2) for a ladder of L rungs; formulas as in r8_flat.flat_run"""
    if t is None:
        t = tab(n_o, u)
    J = math.ceil((2 * u * n + b + n_o * LN2) / lam)
    nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
    rdag, lpidag = rdag_of(t, u, n_o, eta, ltheta, nu0)
    m_max = math.ceil((math.log(2 * (1 + eta) / (1 - eta)) + lam + math.log(nu0) - lpidag) / LN2)
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(2 * (J + 1) * (m_max + 1) * (L + 2)) - ldelta))
    lK = math.log(K)
    lnu = lK + math.log(nu0)
    lMdag = lK - math.log(1 - eta) - lpidag
    lMbar = math.log(2 * (1 + eta)) + lam + math.log(nu0) + lMdag
    ldeltap = ldelta - math.log(4 * L) - lMbar
    xout = float(np.logaddexp(n * math.log(2 / (1 + math.exp(u))),
                              b + np.logaddexp(math.log(math.exp(lam) * (1 + eta) / (1 - eta) + etap), ltheta)))
    P_cnt = math.log(J + 1) + math.log(2 * (1 + eta) ** 2 / (1 - eta)) + lam + lnu      # ln((J+1) cnt(x)) = x + P_cnt
    P_M = math.log(4 * (1 + eta) / (1 - eta)) + lam + math.log(nu0) + lK                # ln(2 Mbar) = P_M + ln(1/pi_dag)
    return dict(J=J, nu0=nu0, rdag=rdag, lpidag=lpidag, m_max=m_max, K=K, lK=lK, lnu=lnu, lMbar=lMbar,
                ldeltap=ldeltap, xout=xout, P_cnt=P_cnt, P_M=P_M, L=L, lam=lam, eta=eta, n=n, n_o=n_o)


def level_cmax(c, xs, lcost):
    """ln C_max = ln(1 + 2 Mbar + sum_{l=1}^{L} min{2 Mbar, (J+1) cnt(x_{l-1})} C_l); xs[0..L], lcost[1..L] (lcost[0] unused).
    Returns (lCmax, terms) with terms[l] = min(ln 2Mbar, ln((J+1)cnt(x_{l-1}))) + lcost[l], terms[0] = ln 2Mbar."""
    L = c['L']
    assert len(xs) == L + 1 and len(lcost) == L + 1
    lam2M = LN2 + c['lMbar']
    xs = np.asarray(xs, dtype=float)
    lc = np.asarray(lcost[1:], dtype=float)
    lcnt = np.maximum(c['lK'], math.log(2 * (1 + c['eta']) ** 2 / (1 - c['eta'])) + c['lam'] + c['lnu'] + xs[:-1])
    terms = np.minimum(lam2M, math.log(c['J'] + 1) + lcnt) + lc
    allt = np.concatenate(([0.0, lam2M], terms))
    lCmax = float(np.logaddexp.reduce(allt))
    return lCmax, np.concatenate(([lam2M], terms))


# ----------------------------------------------------------------------------------------------------------------
# the base family G_0: Proposition K0 (two-sample bracket) or enumeration -- exact log cost
# ----------------------------------------------------------------------------------------------------------------
X_ETA_HALF = 2 * math.log(3.0)          # from here on eta = min(1/2, tanh(x/4)) = 1/2


def base_cost_one(u, d, x, ldelta, t=None):
    """log cost of the base procedure for (d, x, delta): min(2M, 2^d) with the K0 design; formulas of
    r8_flat.k0_plan_flat, plus ln(1 + 1/M) for rounding M up (the referee's routine omits the rounding)."""
    if t is None:
        t = tab(d, u)
    eta = min(0.5, math.tanh(x / 4))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) - ldelta))
    budget = x - math.log((1 + eta) / (1 - eta))
    kap = t.kappa_all(math.log((1 - eta) / (1 + eta)))
    lGpp = t.lE - t.lT[kap]
    ok = np.logaddexp(0.0, lGpp[:d]) <= budget
    if not ok[0]:
        return d * LN2
    bad = np.nonzero(~ok)[0]
    rstar = (int(bad[0]) - 1) if bad.size else d - 1
    lM = math.log(K) + t.mln2 - math.log(1 - eta) - float(t.lB[rstar])
    lM = max(lM, math.log(K / (1 - eta)))
    lcost = LN2 + lM + math.log1p(math.exp(-lM))
    return min(lcost, d * LN2)


class BaseTable:
    """base costs in one dimension d for many accuracies x >= 2 ln 3 (eta = 1/2) at once"""

    def __init__(self, u, d, t=None):
        self.u, self.d = u, d
        self.t = t if t is not None else tab(d, u)
        eta = 0.5
        kap = self.t.kappa_all(math.log((1 - eta) / (1 + eta)))
        lGpp = self.t.lE - self.t.lT[kap]
        g = np.logaddexp(0.0, lGpp[:d])
        self.gmax = np.maximum.accumulate(g)

    def costs(self, xs, ldelta):
        xs = np.asarray(xs, dtype=float)
        out = np.empty(xs.shape)
        big = xs >= X_ETA_HALF
        if np.any(big):
            eta = 0.5
            K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) - ldelta))
            budget = xs[big] - math.log(3.0)
            rstar = np.searchsorted(self.gmax, budget, side='right') - 1
            lM = math.log(K) + self.t.mln2 - math.log(1 - eta) - self.t.lB[np.maximum(rstar, 0)]
            lM = np.maximum(lM, math.log(K / (1 - eta)))
            lc = LN2 + lM + np.log1p(np.exp(-lM))
            lc = np.where(rstar < 0, self.d * LN2, np.minimum(lc, self.d * LN2))
            out[big] = lc
        for i in np.nonzero(~big)[0]:
            out[i] = base_cost_one(self.u, self.d, float(xs[i]), ldelta, self.t)
        return out


# ----------------------------------------------------------------------------------------------------------------
# the error terms of Q_REPORT.md (sections 2-5); every function is the formula of the report, nothing else
# ----------------------------------------------------------------------------------------------------------------
def A_n(cube, n):
    return (2 * cube.u + LN2) * n + 3


def c_log(cube, n):
    return math.log(n + 1) + math.log(6) + 2 * cube.u + math.exp(cube.u)


def X0(cube, n):
    return 1 + c_log(cube, n) + cube.h


C18 = math.log(18 * E1 * (E1 - 1))
C24 = math.log(24 * E1 * (E1 - 1))


def KbarS(cube, n, Lam):
    An = A_n(cube, n)
    mbar = n + 2 + math.log2(12 * E1 * (E1 - 1) * An)
    return 18 * (Lam + math.log(2 * An * mbar * (n + 3))) + 1


def cS(cube, n, Lam, B):
    """error of one slope step (Proposition Q6)"""
    An = A_n(cube, n)
    return (1 + c_log(cube, n) + cube.h) * B / cube.h + 1 + 2 * math.log(An) + C18 + math.log(KbarS(cube, n, Lam)) \
        + math.log(n + 3)


def qS(cube, n, Lam):
    """what a slope step adds to ln(1/delta) + d ln 2"""
    return math.log(4 * (n + 1)) + math.log(A_n(cube, n)) + C24 + math.log(KbarS(cube, n, Lam))


def nubarD(cube, n, c):
    return (1.8 * A_n(cube, n) + 3 * math.exp(cube.u) * n) / c


def KbarD(cube, n, Lam, c):
    An = A_n(cube, n)
    mbar = n + 2 + math.log2(5.6 * nubarD(cube, n, c))
    return 4 / c ** 2 * (Lam + math.log(2 * (An / c) * mbar * (n + 4))) + 1


def PcntD(cube, n, Lam, c):
    return math.log(A_n(cube, n) / c) + math.log(7.45) + math.log(nubarD(cube, n, c)) + math.log(KbarD(cube, n, Lam, c))


def PMD(cube, n, Lam, c):
    return math.log(11.17) + math.log(nubarD(cube, n, c)) + math.log(KbarD(cube, n, Lam, c))


def ell_c(cube, c):
    return LN2 + 3 * cube.u + 2.25 * c + math.log(1 / c)


def mstar(cube, ell):
    """least m (real) from which sqrt(m ell/2) <= p_u m/2 - 1"""
    return ((math.sqrt(ell / 2) + math.sqrt(ell / 2 + 2 * cube.p)) / cube.p) ** 2


def sqrt_term(cube, m, ell):
    """Lemma Q3: for sqrt(m ell/2) <= p_u m/2 - 1 a ball of radius floor(p_u m - sqrt(m ell/2)) in Q_m has
    2^m/|B| <= exp(m a + sqrt_term)"""
    return cube.u * (1 + math.sqrt(m * ell / 2)) + 4 / (3 * cube.p) * (ell + 2) + math.log(m + 1)


def cpi_bar_ell(cube, m, ell):
    return max(LN2 + mstar(cube, ell) * cube.Hp, sqrt_term(cube, m, ell))


def cpi_bar(cube, m, c):
    """bound of ln(1/pi_dagger) - m a for a bounded level with theta = eta = c on an outer cube Q_m (Lemma Q3)"""
    return cpi_bar_ell(cube, m, ell_c(cube, c))


def n_Dp(cube, c):
    """a drop is built only for n >= n_Dp (ladder top above the first rung; (2 p_u)^n <= 5c/6)"""
    return max(2 / cube.u + 2, math.log(6 / (5 * c)) / math.log((1 + math.exp(cube.u)) / 2))


def shift_D(cube, n, c, phi, R):
    """the shift of the outer block of a drop: n_o = floor(phi n - shift)"""
    return cpi_bar(cube, int(math.floor(phi * n)), c) / (cube.a + R)


def cD(cube, n, Lam, c, phi, R, B):
    """error of one drop (Proposition Q7); B/(a + R) = B'/a"""
    return B * (1 + phi * n_Dp(cube, c)) + shift_D(cube, n, c, phi, R) * B + math.log(n + 4) + 1 + PcntD(cube, n, Lam, c)


def qD(cube, n, Lam, c):
    return math.log(4 * (n + 2)) + PMD(cube, n, Lam, c)


def w_acc(c):
    """what a drop with lam = eta = eta' = theta = c takes from the accuracy: ln(e^c (1+c)/(1-c) + 2c) + c"""
    return math.log(math.exp(c) * (1 + c) / (1 - c) + 2 * c) + c


def acc_schedule(eps, M):
    """c_m (m = 0..M-1) and alpha_m (m = 0..M)"""
    eh = min(eps, 1.0)
    c = [eh / (13.0 * (m + 1) * (m + 2)) for m in range(M)]
    alpha = [0.0] * (M + 1)
    alpha[M] = eh
    for m in range(M - 1, -1, -1):
        alpha[m] = alpha[m + 1] - w_acc(c[m])
    return c, alpha


def ell0_x(cube, x):
    """ln_+( 2 e^{3u + min(x/2, ln 3)} / (e^{x/2} - 1) )"""
    y = x / 2
    lden = math.log(math.expm1(y)) if y < 30 else y + math.log1p(-math.exp(-y))
    lv = LN2 + 3 * cube.u + min(y, math.log(3.0)) - lden
    return lv if lv > 0 else 0.0


def Kbar0(x, Lam):
    eta = min(0.5, math.tanh(x / 4))
    return 3 * (1 + eta) / eta ** 2 * (math.log(4) + Lam) + 1


def E_base(cube, d, x, Lam):
    """the base family: ln cost <= d a + E_base(d, x; Lam) whenever ln(1/delta) <= Lam (Proposition Q5)"""
    ell = ell0_x(cube, x)
    return math.log(8 * Kbar0(x, Lam)) + max(mstar(cube, ell) * cube.Hp, sqrt_term(cube, d, ell))


def E_total(cube, n, eps, delta_ln, M, seq=None, detail=False):
    """the error term of Theorem Q8:  ln cost(G_M(n, eps, delta)) <= n B_M + E_total.   delta_ln = ln(1/delta)."""
    if seq is None:
        seq = epoch_seq(cube, M)
    c, alpha = acc_schedule(eps, M)
    Lam = delta_ln + n * LN2
    tot = 0.0
    parts = dict(S=0.0, Dlog=0.0, Dsqrt=0.0, nS=0, nD=0)
    for m in range(M - 1, -1, -1):
        # the drop that ends epoch m, then the J_m slope steps of epoch m
        cd = cD(cube, n, Lam, c[m], seq['phi'][m], seq['R'][m], seq['B'][m])
        sq = shift_D(cube, n, c[m], seq['phi'][m], seq['R'][m]) * seq['B'][m]
        tot += cd
        parts['Dsqrt'] += sq
        parts['Dlog'] += cd - sq
        parts['nD'] += 1
        Lam += qD(cube, n, Lam, c[m])
        for _ in range(seq['J'][m]):
            cs = cS(cube, n, Lam, seq['B'][m])
            tot += cs
            parts['S'] += cs
            parts['nS'] += 1
            Lam += qS(cube, n, Lam)
    eb = E_base(cube, n, alpha[0], Lam)
    E = eb + tot
    if detail:
        parts.update(E=E, Ebase=eb, Lam=Lam)
        return parts
    return E


# ----------------------------------------------------------------------------------------------------------------
def selftest():
    """level_consts/level_cmax against r8_flat.flat_run; base_cost against r8_flat.k0_plan_flat"""
    bad = 0
    rng = np.random.default_rng(1)
    for (u, n, phi, kw) in [(1.0, 1000, 0.5, {}), (1.0, 4000, 0.45, {}), (2.0, 1500, 0.6, {}), (0.5, 3000, 0.5, {}),
                            (1.0, 6000, 0.3, dict(lam=0.3, eta=0.25, etap=0.5, theta=0.2, b=1.0, Lr=17)),
                            (1.0, 5000, 0.2, dict(lam=1.0, eta=0.5, etap=1.0, b=1.0, Lr=25, bounded=False, ltheta=150.0))]:
        r = F.flat_run(u, n, phi, **kw)
        lam = kw.get('lam', 0.2); eta = kw.get('eta', 0.05); etap = kw.get('etap', 0.05); b = kw.get('b', 0.5)
        Lr = kw.get('Lr', 40); bounded = kw.get('bounded', True)
        ltheta = kw.get('ltheta', None)
        if ltheta is None:
            ltheta = math.log(kw.get('theta', 0.05))
        n_o = r['n_o']
        nu1 = 2 * math.exp(u) * n_o / math.exp(ltheta) if bounded else 1.0
        c = level_consts(u, n, n_o, lam, eta, etap, ltheta, nu1, b, math.log(0.05), Lr)
        lC, terms = level_cmax(c, r['xs'], r['lcosts'])
        ok = (c['J'] == r['J'] and c['K'] == r['K'] and c['rdag'] == r['rdag'] and abs(c['lMbar'] - r['lMbar']) < 1e-9
              and abs(c['ldeltap'] - r['ldeltap']) < 1e-9 and abs(c['xout'] - r['xout']) < 1e-12 and abs(lC - r['lCmax']) < 1e-9)
        # the base costs of the rungs: the referee's routine against ours (ours adds the rounding of M)
        d = r['n_i']
        bt = BaseTable(u, d)
        mine = bt.costs(np.array(r['xs'][1:]), r['ldeltap'])
        ref = np.array(r['lcosts'][1:])
        ok2 = bool(np.all(mine >= ref - 1e-9) and np.all(mine <= ref + 1e-3))      # ours adds ln(1 + 1/M), M >= K
        print("selftest u=%.1f n=%d phi=%.2f %s: constants and lCmax %s (lCmax %.6f vs %.6f); base costs %s"
              % (u, n, phi, kw, "AGREE" if ok else "DIFFER", lC, r['lCmax'], "AGREE" if ok2 else "DIFFER"))
        bad += (not ok) + (not ok2)
    # epoch sequences: B_{m+1} = B_m J a/(J a + h), closed form h/d_m <= c1/(k_m + c2)
    for u in (0.5, 1.0, 2.0, 5.0):
        cu = Cube(u)
        s = epoch_seq(cu, 40)
        for m in range(40):
            assert abs(s['B'][m + 1] - s['B'][m] * s['J'][m] * cu.a / (s['J'][m] * cu.a + cu.h)) < 1e-13
            assert abs(s['B'][m + 1] - (1 - s['phi'][m]) * s['B'][m]) < 1e-13
            assert s['d'][m] <= s['J'][m] < s['d'][m] + 1
            for kk in (s['k'][m], s['k'][m + 1] - 1):          # the bound is decreasing in the level: the ends suffice
                assert cu.h / s['d'][m] <= cu.c1 / (kk + cu.c2) + 1e-15
            assert s['d'][m + 1] <= cu.rbar * s['d'][m] * (1 + 1e-12) and s['k'][m + 1] <= (1 + cu.rbar) * s['k'][m] + 1e-9
        assert abs(cu.theta_na(cu.h) - cu.h) < 1e-12 and abs(kl(cu.rho_h, cu.p) - cu.h) < 1e-13
        assert cu.h <= u * u / 16 + 1e-15 and cu.h < cu.a < LN2
        # facts used in Q_REPORT sections 1, 5, 6
        assert cu.h <= u and cu.c2 >= 0 and abs(cu.c2 - (2 * cu.a + cu.h) * (cu.a - cu.h) / (cu.h * cu.a)) < 1e-12
        for m in range(40):
            assert s['phi'][m] <= (1 + cu.kappa) ** (-m) / cu.rbar * (1 + 1e-12)                 # phi_m <= rbar^-1 (1+kappa)^-m
            assert s['d'][m + 1] + 1 >= (s['d'][m] + 1) * (1 + cu.kappa) * (1 - 1e-12)
        for M in range(1, 40):
            assert M <= 1 + math.log(s['k'][M]) / math.log(1 + cu.kappa) + 1e-9
        prev = None
        for i in range(1, 400):                                                                # (F4)
            t = cu.eps_star * 1.2 * i / 400
            th = cu.theta_na(t)
            assert cu.a - th <= u * math.sqrt(t / 2) + 1e-12
            if prev is not None and i >= 3:
                assert th - 2 * prev[0] + prev[1] >= -1e-12                                    # convex
            prev = (th, prev[0]) if prev is not None else (th, cu.a)
        for ell in (0.0, 0.5, 3.0, 8.0, 20.0, 60.0):
            assert mstar(cu, ell) <= (2 * ell + 8 * cu.p) / cu.p ** 2 * (1 + 1e-12)
            mm = mstar(cu, ell)
            assert abs(math.sqrt(mm * ell / 2) - (cu.p * mm / 2 - 1)) < 1e-9 * max(1.0, mm)
    # the numerical constants of Proposition Q7 and the accuracy schedule
    for i in range(1, 1001):
        c = i / 3000.0
        assert w_acc(c) <= 6.25 * c + 1e-15
        assert math.expm1(c) / c <= 1.2 and 1 / (1 - c) <= 1.5 + 1e-12
        assert 2 * (1 + c) * math.exp(c) / (1 - c) <= 5.6 and 2 * (1 + c) ** 2 * math.exp(c) / (1 - c) <= 7.45
        assert 4 * (1 + c) * math.exp(c) / (1 - c) <= 11.17 and 3 * (1 + c) <= 4 + 1e-12
        assert -math.expm1(-c) >= 5 * c / 6 and math.log((1 + c) / (1 - c)) <= 2.25 * c + 1e-15
    for eps in (5.0, 1.0, 0.3, 0.01):
        for M in (0, 1, 5, 50, 500):
            cs, al = acc_schedule(eps, M)
            assert al[0] >= 0.519 * min(eps, 1.0) and all(al[m] < al[m + 1] for m in range(M)) and all(c <= 1 / 26 + 1e-15 for c in cs)
    print("selftest: epoch sequences, closed form, theta_na(h) = h, h <= u^2/16, (F4), the constants of Q7 and the accuracy schedule: OK")
    print("selftest failures:", bad)
    return bad


if __name__ == '__main__':
    sys.exit(selftest())
