#!/usr/bin/env python3
"""Workstream Q2 -- shared routines (numpy only).

Nothing here re-implements Theorem 11.56: every level is evaluated with the two existing, independent exact
evaluators of the certified cost of one level of Algorithm 2L+,
    experiments/workstreams/Q/qlib.py        (author of Q_REPORT; tables of experiments/reviews/R8/r8_flat.TablesF)
    experiments/reviews/R12/r12lib.py        (referee R12; own tables),
which are imported, not modified; `Ev.consts` runs both and records the largest disagreement.

Contents (the names are those of docs/workstreams/Q2_REPORT.md)
  Ev                      both evaluators for one slope u
  SatLines                a "saturating" inner family: certified cost EQUAL to max_i[d B_i - sigma_i min(x, R d)] + E
  level_U                 the level of Lemma U (lam = 1, eta = 1/2, eta' = 1, nu_1 = 1, tolerance b >= 1, unit ladder below a cap)
  Dprime_*                the drop D' (Proposition D'): design, level, bound
  slope_e_*               the slope step at outer rate e (Proposition Q6(e)): design, level, bound
  Chain                   the chain T (Proposition T): design, exact recursion, bound
  E_new, E_old, E_trap    the error terms of the new schedule (Theorem A), of Q_REPORT's (5.2) and of the variant without chains
  E_new_closed            the closed form of Proposition A'
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True          # no __pycache__ in the directories of the imported libraries (nothing outside Q2/ is written)
sys.path.insert(0, os.path.join(HERE, '..', 'Q'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'reviews', 'R12'))
import qlib as Q        # noqa: E402
import r12lib as R      # noqa: E402

LN2 = Q.LN2
E1 = math.e
INF = float('inf')
C18 = math.log(18 * E1 * (E1 - 1))
C24 = math.log(24 * E1 * (E1 - 1))
FL = 1e-12                       # added before a floor so that an exact integer is not lost to rounding


# ---------------------------------------------------------------------------------------------------------------
#  the two evaluators
# ---------------------------------------------------------------------------------------------------------------
class Ev:
    """constants and ln C_max of one level of Algorithm 2L+, by qlib (always) and by r12lib (if both=True)"""

    def __init__(self, u, both=True, maxtabs=4):
        self.u = float(u)
        self.cu = Q.Cube(self.u)
        self.cuR = R.Cube(self.u)
        self.tabsR = R.TabCache(self.u, maxtabs)
        self.both = both
        self.maxdiff = 0.0           # largest disagreement between the two evaluators (ln C_max, ln delta', x_out)
        self.rdag_diff = 0           # number of levels on which r_dagger differs (ties in the tables)
        self.nlev = 0

    def consts(self, n, n_o, lam, eta, etap, ltheta, nu1, b, ld, L):
        c = Q.level_consts(self.u, n, n_o, lam, eta, etap, ltheta, nu1, b, ld, L)
        c['b'] = b
        c['l_inv_pi'] = -c['lpidag']
        c['Lam'] = LN2 + c['lMbar']
        if self.both:
            c['R'] = R.level_consts(self.cuR, self.tabsR.get(n_o), n, n_o, lam, eta, etap, ltheta, nu1, b, ld, L)
        return c

    def cmax(self, c, xs, lc):
        """xs = [x_0, ..., x_L], lc = [ln C_1, ..., ln C_L]; returns ln C_max and the index of the largest term (0: outer sample)"""
        xs = np.asarray(xs, dtype=float)
        lc = np.asarray(lc, dtype=float)
        lC, terms = Q.level_cmax(c, xs, np.concatenate(([0.0], lc)))
        self.nlev += 1
        if self.both:
            cs = c['R']
            lC2, _ = R.level_cmax(cs, xs, lc)
            d = max(abs(lC2 - lC), abs(cs['ldeltap'] - c['ldeltap']), abs(cs['xout'] - c['xout']))
            if cs['rdag'] != c['rdag'] or cs['K'] != c['K'] or cs['J'] != c['J']:
                self.rdag_diff += 1
            self.maxdiff = max(self.maxdiff, d)
        return lC, int(np.argmax(terms))


# ---------------------------------------------------------------------------------------------------------------
#  saturating inner families
# ---------------------------------------------------------------------------------------------------------------
class SatLines:
    """A family whose certified cost EQUALS  max(0, max_i [d B_i - sigma_i min(x, R d)]) + Efun(d, x, ln(1/delta) + d ln 2):
    the largest cost that the type H(max of lines, R; E) allows (a certified bound is >= 0: one evaluation)."""

    def __init__(self, lines, Rr=INF, Efun=None):
        self.lines = [(float(B), float(s)) for (B, s) in lines]
        self.R = Rr
        self.Efun = Efun

    def E(self, d, x, Lam):
        return 0.0 if self.Efun is None else self.Efun(d, x, Lam)

    def major(self, d, x):
        xm = min(x, self.R * d) if self.R < INF else x
        return max(d * B - s * xm for (B, s) in self.lines)

    def costs(self, d, xs, ld):
        xs = np.asarray(xs, dtype=float)
        xm = np.minimum(xs, self.R * d) if self.R < INF else xs
        v = np.full(xs.shape, -INF)
        for (B, s) in self.lines:
            v = np.maximum(v, d * B - s * xm)
        v = np.maximum(v, 0.0)
        if self.Efun is not None:
            Lam = -ld + d * LN2
            v = v + np.array([self.Efun(d, float(x), Lam) for x in xs])
        return v


# ---------------------------------------------------------------------------------------------------------------
#  the common constants of the levels with lam = 1, eta = 1/2, eta' = 1, nu_1 = 1, tolerance 1 (Lemma U)
# ---------------------------------------------------------------------------------------------------------------
def A_nb(cu, n, b=1.0):
    """A_n^b = (2u + ln 2) n + 2 + b  (A_n of Q_REPORT at the tolerance b = 1)"""
    return Q.A_n(cu, n) + (b - 1.0)


def KbarSb(cu, n, Lam, b=1.0):
    An = A_nb(cu, n, b)
    mbar = n + 2 + math.log2(12 * E1 * (E1 - 1) * An)
    return 18 * (Lam + math.log(2 * An * mbar * (n + 3))) + 1


def qSb(cu, n, Lam, b=1.0):
    """what a level of Lemma U adds to ln(1/delta) + d ln 2  (= q_S of Q_REPORT at b = 1)"""
    return math.log(4 * (n + 1)) + math.log(A_nb(cu, n, b)) + C24 + math.log(KbarSb(cu, n, Lam, b))


def ell0(cu, n, Lam, b=1.0):
    """ell_0^b(n, Lam) = 1 + 2 ln A_n^b + ln(18e(e-1)) + ln Kbar_S^b(n, Lam) + ln(n+3)
    (at b = 1: c_S of Q_REPORT without its first term)"""
    return 1 + 2 * math.log(A_nb(cu, n, b)) + C18 + math.log(KbarSb(cu, n, Lam, b)) + math.log(n + 3)


def ltheta_exact(cu, n, acc, b=1.0):
    """ln theta for theta = e^{acc-b} - (3e+1) - (2p_u)^n e^{-b}: the threshold at which a level of Lemma U with
    tolerance b has accuracy exactly acc"""
    return (acc - b) + math.log1p(-((3 * E1 + 1) + math.exp(n * math.log(2 * cu.p) - b)) * math.exp(-(acc - b)))


def level_U(ev, n, n_o, ltheta, Xi, ld, inner, b=1.0):
    """The level of Lemma U in dimension n with outer block n_o, threshold theta, cap Xi of the ladder, tolerance b >= 1:
    lam = 1, eta = 1/2, eta' = 1, nu_1 = 1, ladder 2u n_i > b + k_1 > b + k_1 - 1 > ... > b + 1 > b,
    k_1 = min(max(ceil(Xi - b), 0), ceil(2u n_i - b) - 1)   (for b = 1: x_1 = min(max(ceil(Xi), 1), ceil(2u n_i) - 1)),
    inner procedures inner(n_i, x_l, delta').  Returns a dict with ln C_max and everything the checks need."""
    u = ev.u
    n_i = n - n_o
    assert 1 <= n_o <= n - 1 and 2 * u * n_i > b >= 1
    k1 = min(max(int(math.ceil(Xi - b)), 0), int(math.ceil(2 * u * n_i - b)) - 1)
    assert k1 >= 0 and b + k1 < 2 * u * n_i
    xs = np.concatenate(([2 * u * n_i], b + np.arange(k1, -1, -1, dtype=float)))
    L = k1 + 1
    c = ev.consts(n, n_o, 1.0, 0.5, 1.0, ltheta, 1.0, b, ld, L)
    lc = inner.costs(n_i, xs[1:], c['ldeltap'])
    lC, arg = ev.cmax(c, xs, lc)
    return dict(lC=lC, c=c, xs=xs, lc=lc, arg=arg, n_i=n_i, L=L)


def check_U_consts(cu, n, n_o, c, Lam, viol, tag, b=1.0):
    """the constants of Lemma U, one by one (step (2) of its proof)"""
    An = A_nb(cu, n, b)
    KS = KbarSb(cu, n, Lam, b)
    mbar = n + 2 + math.log2(12 * E1 * (E1 - 1) * An)
    ok = (c['J'] + 1 <= An + 1e-9 and abs(c['nu0'] - 2 * (E1 - 1) * (c['J'] + 1)) <= 1e-9 * c['nu0']
          and c['m_max'] + 1 <= mbar + 1e-9 and c['L'] + 2 <= n + 3 and c['K'] <= KS + 1e-6
          and c['P_cnt'] <= 2 * math.log(An) + C18 + math.log(KS) + 1e-9
          and c['P_M'] <= math.log(An) + C24 + math.log(KS) + 1e-9
          and c['P_M'] + math.log(n_o + 1) <= 1 + c['P_cnt'] + 1e-9
          and -c['ldeltap'] + (n - n_o) * LN2 <= Lam + qSb(cu, n, Lam, b) + 1e-9)
    if not ok:
        viol.append("constants of Lemma U at %s" % (tag,))
    return ok


# ---------------------------------------------------------------------------------------------------------------
#  Proposition D'  (the drop at a logarithmic accuracy)
# ---------------------------------------------------------------------------------------------------------------
def X_D(cu, N, phi, b=1.0):
    """the least accuracy X_D^b(N; phi) = b + ln(3e + 2 + 3(phi N + 1) e^{2u + e^u}) of the drop D' with horizon N
    and tolerance b"""
    return b + math.log(3 * E1 + 2 + 3 * (phi * N + 1) * math.exp(2 * cu.u + math.exp(cu.u)))


def Dprime_no(n, phi):
    return int(math.floor(phi * n + FL))


def Dprime_built(cu, n, phi, b=1.0):
    n_o = Dprime_no(n, phi)
    return n_o >= 1 and 2 * cu.u * (n - n_o) > b


def Dprime_level(ev, n, phi, Rr, calX, ld, inner, b=1.0):
    """the level as built of D'[F; phi, X] at (n, delta): outer block floor(phi n), accuracy exactly X, cap R n_i"""
    cu = ev.cu
    n_o = Dprime_no(n, phi)
    n_i = n - n_o
    r = level_U(ev, n, n_o, ltheta_exact(cu, n, calX, b), Rr * n_i, ld, inner, b)
    r['n_o'] = n_o
    return r


def Dprime_Bp(cu, lines, phi):
    """the exponent after the drop: max_i [(1 - phi) B_i + (1 - sigma_i) phi a]"""
    return max((1 - phi) * B + (1 - s) * phi * cu.a for (B, s) in lines)


def Dprime_Bt(cu, lines, phi, b=1.0):
    """B~ = max{1, b phi/(2u(1 - phi))} max_i (B_i - (1 - sigma_i) a)_+ : rounding of the outer block and pass-through"""
    return max(1.0, b * phi / (2 * cu.u * (1 - phi))) * max(max(B - (1 - s) * cu.a, 0.0) for (B, s) in lines)


def cDp(cu, n, Lam, Bt, b=1.0):
    """the error term c_D'(n, Lam) of Proposition D'"""
    return Bt + ell0(cu, n, Lam, b)


# ---------------------------------------------------------------------------------------------------------------
#  Proposition Q6(e)  (the slope step at a general outer rate e)
# ---------------------------------------------------------------------------------------------------------------
def X0e(cu, n, e, b=1.0):
    return b + Q.c_log(cu, n) + e


def slope_e_no(cu, n, xh, e, b=1.0):
    return int(math.floor((xh - b - Q.c_log(cu, n)) / e + FL))


def slope_e_Rp(cu, Rr, e):
    th = cu.theta_na(e)
    return e if Rr == INF else Rr * e / (th + Rr)


def slope_e_level(ev, n, xh, e, ld, inner, b=1.0):
    """the level as built of S_e[F] at accuracy xh = x-hat >= X_0^e(n): outer block floor((xh - b - c_log(n))/e),
    accuracy exactly xh, cap n_o theta_na(e)"""
    cu = ev.cu
    n_o = slope_e_no(cu, n, xh, e, b)
    r = level_U(ev, n, n_o, ltheta_exact(cu, n, xh, b), n_o * cu.theta_na(e), ld, inner, b)
    r['n_o'] = n_o
    return r


def slope_e_sigp(cu, B, s, e):
    """the new slope sigma' = [B - (1 - sigma) theta_na(e)]/e"""
    return (B - (1 - s) * cu.theta_na(e)) / e


def cSe(cu, n, Lam, sigp_bar, e, b=1.0):
    """the error term of Proposition Q6(e): sigma'_+ (b + c_log(n) + e) + ell_0^b(n, Lam)"""
    return max(sigp_bar, 0.0) * (b + Q.c_log(cu, n) + e) + ell0(cu, n, Lam, b)


# ---------------------------------------------------------------------------------------------------------------
#  Proposition T  (the chain that brings a logarithmic accuracy back to a bounded one)
# ---------------------------------------------------------------------------------------------------------------
def varpi(cu, m, c):
    """a bound for ln(1/pi_dagger) on an outer block of m sites at theta = eta = c, nu_1 = 2e^u m/c:
    the trivial one, (m+1) ln 2 (Lemma Q2(b)), or -- if m >= m*(ell_c), i.e. sqrt(m ell_c/2) <= p_u m/2 - 1 -- the refined
    bound of Lemma Q3 (= Lemma 11.55(c)),  m a + u(1 + sqrt(m ell_c/2)) + (4/(3p_u))(ell_c + 2) + ln(m+1); the smaller"""
    v = (m + 1) * LN2
    ell = Q.ell_c(cu, c)
    if m >= Q.mstar(cu, ell):
        v = min(v, m * cu.a + Q.sqrt_term(cu, m, ell))
    return v


def qT(cu, d, Lam, c):
    """what one level of the chain adds to ln(1/delta) + d ln 2: ln(4L) + P_M with L = 2"""
    return math.log(8.0) + Q.PMD(cu, d, Lam, c)


class Chain:
    """The chain T[G'; alpha, m] with horizon N on top of a family G' of flat type H_N(B', 0, inf; E) with least
    accuracy X (Proposition T).  All levels have the outer block m, lam = eta = eta' = theta = c = alpha/(13 ceil(N/m)),
    nu_1 = 2e^u m/c and the ladder 2u(d - m) > X > b_d; below d_0 the base family at accuracy alpha_low."""

    def __init__(self, cu, N, Bp, calX, alpha, m):
        self.cu, self.N, self.Bp, self.calX, self.alpha, self.m = cu, N, Bp, calX, alpha, int(m)
        u = cu.u
        self.NT = int(math.ceil(N / self.m))
        self.c = alpha / (13.0 * self.NT)
        self.w = Q.w_acc(self.c)
        self.alow = alpha - self.NT * self.w
        self.d0 = max(self.m + int(math.floor(calX / (2 * u))) + 1,
                      int(math.ceil(math.log(6 / (5 * self.c)) / math.log((1 + math.exp(u)) / 2))))
        assert self.alow > 0 and self.d0 >= self.m + 1 and calX > 1 and Bp <= LN2

    # --- design
    def j(self, d):
        """number of levels of the chain that starts in dimension d"""
        return 0 if d < self.d0 else (d - self.d0) // self.m + 1

    def acc(self, d):
        """the accuracy a_d that the chain delivers in dimension d (alpha_low below d_0)"""
        return self.alow + self.j(d) * self.w

    def tol(self, d):
        return self.alow + (self.j(d) - 1) * self.w

    @staticmethod
    def design_m(cu, N, Bp, calX, alpha, Lam_entry):
        """the block of the design: the least m >= 1 with  m B' >= X + Pbar_cnt(N, Lam_entry + N B'; c(m)) + ln 4"""
        Lhat = Lam_entry + N * Bp

        def ok(m):
            c = alpha / (13.0 * math.ceil(N / m))
            return m * Bp >= calX + Q.PcntD(cu, N, Lhat, c) + math.log(4.0)

        hi = 1
        while not ok(hi):
            hi *= 2
            if hi > 10 ** 15:
                raise RuntimeError("no block")
        lo = hi // 2                    # ok(lo) is False (or lo = 0)
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if ok(mid):
                hi = mid
            else:
                lo = mid
        return hi

    # --- the bound of Proposition T
    def a_T(self, d, Lam):
        return varpi(self.cu, self.m, self.c) - self.m * self.Bp + Q.PMD(self.cu, d, Lam, self.c) + math.log(4.0)

    def e0(self, Lam):
        d1 = self.d0 - 1
        return min(d1 * (LN2 - self.Bp), d1 * max(self.cu.a - self.Bp, 0.0) + Q.E_base(self.cu, d1, self.alow, Lam))

    def A_T(self, d, Lam):
        return max(self.a_T(d, Lam), self.e0(Lam))

    def Delta_T(self, d, Lam):
        return max(0.0, self.calX + Q.PcntD(self.cu, d, Lam, self.c) + math.log(4.0) - self.m * self.Bp)

    def Lam_star(self, d, Lam):
        """the j(d)-fold iterate of Lam -> Lam + q_T(d, Lam)"""
        for _ in range(self.j(d)):
            Lam = Lam + qT(self.cu, d, Lam, self.c)
        return Lam

    def Lam_sharp(self, d, Lam):
        """the closed upper bound Lam + j(d) q_T(d, Lam + d B') of Lam_star (valid when Delta_T(d, Lam + d B') = 0)"""
        return Lam + self.j(d) * qT(self.cu, d, Lam + d * self.Bp, self.c)

    def E_T(self, d, Lam, Efun=None, closed=False):
        """the error function of Proposition T:  E(d, X; Lam*) + A_T(d, Lam*) + j(d) Delta_T(d, Lam*)"""
        Ls = self.Lam_sharp(d, Lam) if closed else self.Lam_star(d, Lam)
        E = 0.0 if Efun is None else Efun(d, self.calX, Ls)
        return E + self.A_T(d, Ls) + self.j(d) * self.Delta_T(d, Ls)

    # --- exact certified cost by the recursion over the chain
    def exact(self, ev, d, ld, Gp, keep=False):
        """ln of the certified cost of the chain started at (d, delta = e^ld) on top of the family Gp
        (Gp.costs(d', [X], ld')); returns (ln cost, list of per-level records from the top)."""
        cu, u, m, c = self.cu, self.cu.u, self.m, self.c
        recs = []
        dd, l = d, ld
        while dd >= self.d0:
            b = self.tol(dd)
            cs = ev.consts(dd, m, c, c, c, math.log(c), 2 * math.exp(u) * m / c, b, l, 2)
            recs.append(dict(d=dd, ld=l, c=cs, b=b))
            dd, l = dd - m, cs['ldeltap']
        # the bottom: the base family at accuracy alpha_low (two-sample bracket or enumeration, the cheaper)
        t = Q.base_cost_one(u, dd, self.alow, l) if dd >= 1 else 0.0
        bottom = dict(d=dd, ld=l, t=t)
        for r in reversed(recs):
            cs = r['c']
            xs = [2 * u * (r['d'] - m), self.calX, r['b']]
            lc1 = float(Gp.costs(r['d'] - m, np.array([self.calX]), cs['ldeltap'])[0])
            lC, arg = ev.cmax(cs, xs, [lc1, t])
            r['lc1'], r['lc2'], r['t'], r['arg'] = lc1, t, lC, arg
            t = lC
        return t, recs, bottom


# ---------------------------------------------------------------------------------------------------------------
#  the base family at a logarithmic accuracy (Proposition Q5(b) of Q_REPORT at e = 0)
# ---------------------------------------------------------------------------------------------------------------
def X_B(cu, N):
    """c'_N = ln 12 + 2 ln(N+1) + 2u + e^u: from this accuracy on the two-sample bracket costs e^{d a} up to 8K(d+1)"""
    return math.log(12.0) + 2 * math.log(N + 1) + 2 * cu.u + math.exp(cu.u)


def E_frakB(cu, d, Lam):
    """ln(8 K) + ln(d+1) with K <= 18(ln 4 + Lam) + 1"""
    return math.log(8 * (18 * (math.log(4.0) + Lam) + 1)) + math.log(d + 1)


# ---------------------------------------------------------------------------------------------------------------
#  the error terms of the schedules (formula evaluation)
# ---------------------------------------------------------------------------------------------------------------
def E_new(cu, n, eps, delta_ln, M, seq=None, detail=False, sharp=True):
    """Theorem A, formula (A.1):  ln cost(G_M(n, eps^, delta)) <= n B_M + E_new.   delta_ln = ln(1/delta).
    Unrolled from the top: chain_M, then for m = M-1 .. 0: D'_m, the J_m slope steps of epoch m (the last one first),
    chain_m; then the base family at the accuracy X_B(n).  Chains use the closed update Lam <- Lam + j(n) q_T(n, Lam + n B').
    sharp=True: slope steps with the error term of Lemma U, sigma'(1 + c_log(n) + h) + ell_0 (sigma' = j/d_m);
    sharp=False: with c_S(n, Lam; B_m) of Q_REPORT."""
    if seq is None:
        seq = Q.epoch_seq(cu, max(M, 1))
    eh = min(eps, 1.0)
    Lam = delta_ln + n * LN2
    parts = dict(S=0.0, D=0.0, T=0.0, nS=0, nD=0, nT=0, chains=[])
    tot = 0.0
    for e in range(M, -1, -1):
        alpha = eh if e == M else 1.0
        Bp = seq['B'][e] if e >= 1 else cu.a
        calX = X_D(cu, n, seq['phi'][e - 1]) if e >= 1 else X_B(cu, n)
        m = Chain.design_m(cu, n, Bp, calX, alpha, Lam)
        ch = Chain(cu, n, Bp, calX, alpha, m)
        Ls = ch.Lam_sharp(n, Lam)
        t = ch.A_T(n, Ls) + ch.j(n) * ch.Delta_T(n, Ls)
        parts['chains'].append(dict(e=e, m=m, c=ch.c, j=ch.j(n), d0=ch.d0, A=t, a=ch.a_T(n, Ls), e0=ch.e0(Ls), X=calX, Bp=Bp,
                                    Delta=ch.Delta_T(n, Ls), dLam=Ls - Lam))
        tot += t
        parts['T'] += t
        parts['nT'] += 1
        Lam = Ls
        if e >= 1:
            B, phi, dm = seq['B'][e - 1], seq['phi'][e - 1], seq['d'][e - 1]
            cd = cDp(cu, n, Lam, Dprime_Bt(cu, [(B, 1.0)], phi))
            tot += cd
            parts['D'] += cd
            parts['nD'] += 1
            Lam += Q.qS(cu, n, Lam)
            for j in range(seq['J'][e - 1], 0, -1):
                cs = cSe(cu, n, Lam, j / dm, cu.h) if sharp else Q.cS(cu, n, Lam, B)
                tot += cs
                parts['S'] += cs
                parts['nS'] += 1
                Lam += Q.qS(cu, n, Lam)
    eb = E_frakB(cu, n, Lam)
    E = tot + eb
    if detail:
        parts.update(E=E, Ebase=eb, Lam=Lam)
        return parts
    return E


def E_old(cu, n, eps, delta_ln, M, seq=None, sharp=False):
    """(5.2) of Q_REPORT (= qlib.E_total for sharp=False); sharp=True: its slope steps with the error term of Lemma U"""
    if seq is None:
        seq = Q.epoch_seq(cu, max(M, 1))
    if not sharp:
        return Q.E_total(cu, n, eps, delta_ln, M, seq)
    c, alpha = Q.acc_schedule(eps, M)
    Lam = delta_ln + n * LN2
    tot = 0.0
    for m in range(M - 1, -1, -1):
        tot += Q.cD(cu, n, Lam, c[m], seq['phi'][m], seq['R'][m], seq['B'][m])
        Lam += Q.qD(cu, n, Lam, c[m])
        for j in range(seq['J'][m], 0, -1):
            tot += cSe(cu, n, Lam, j / seq['d'][m], cu.h)
            Lam += Q.qS(cu, n, Lam)
    return tot + Q.E_base(cu, n, alpha[0], Lam)


def trap_tolerances(cu, n, M, seq):
    """the least accuracies of the variant without chains: b_0 = X_B(n), b_{m+1} = X_D^{b_m}(n; phi_m)"""
    bs = [X_B(cu, n)]
    for m in range(M):
        bs.append(X_D(cu, n, seq['phi'][m], bs[m]))
    return bs


def E_trap(cu, n, eps, delta_ln, M, seq=None, detail=False):
    """the variant in which the drops D' are NOT followed by a chain (section 5.4 of the report): epoch m is built with
    the tolerance b_m (its inner family's least accuracy), and one chain at the top brings b_M back to eps^."""
    if seq is None:
        seq = Q.epoch_seq(cu, max(M, 1))
    eh = min(eps, 1.0)
    Lam = delta_ln + n * LN2
    bs = trap_tolerances(cu, n, M, seq)
    Bp = seq['B'][M] if M >= 1 else cu.a
    m = Chain.design_m(cu, n, Bp, bs[M], eh, Lam)
    ch = Chain(cu, n, Bp, bs[M], eh, m)
    Ls = ch.Lam_sharp(n, Lam)
    T = ch.A_T(n, Ls) + ch.j(n) * ch.Delta_T(n, Ls)
    Lam = Ls
    S = D = 0.0
    for mm in range(M - 1, -1, -1):
        b = bs[mm]
        B, phi, dm = seq['B'][mm], seq['phi'][mm], seq['d'][mm]
        D += cDp(cu, n, Lam, Dprime_Bt(cu, [(B, 1.0)], phi, b), b)
        Lam += qSb(cu, n, Lam, b)
        for j in range(seq['J'][mm], 0, -1):
            S += cSe(cu, n, Lam, j / dm, cu.h, b)
            Lam += qSb(cu, n, Lam, b)
    eb = E_frakB(cu, n, Lam)
    if detail:
        return dict(E=T + S + D + eb, T=T, S=S, D=D, Ebase=eb, bs=bs, m=m, Lam=Lam)
    return T + S + D + eb


def ellT_closed(cu, n, Lhat, Bp, calX, alpha):
    """the closed bound ell_T of Proposition A' for the error of one chain:
    (ln 2 - B') max{mbar + X/(2u), n''(c_)} + Pbar_M(n, Lhat; c_) + ln 8,  c_ = alpha/(13 n),
    mbar = 1 + (X + Pbar_cnt(n, Lhat; c_) + ln 4)/B'"""
    cl = alpha / (13.0 * n)
    mbar = 1 + (calX + Q.PcntD(cu, n, Lhat, cl) + math.log(4.0)) / Bp
    npp = math.log(6 / (5 * cl)) / math.log((1 + math.exp(cu.u)) / 2)
    return (LN2 - Bp) * max(mbar + calX / (2 * cu.u), npp) + Q.PMD(cu, n, Lhat, cl) + math.log(8.0)


def E_new_closed(cu, n, eps, delta_ln, M, seq=None):
    """Proposition A': with Lhat = (M + 3) Lam_0 and (k_M - 1) q_S(n, Lhat) <= Lam_0,
    E_new <= sum over slope steps of [sigma'_t (1 + c_log + h) + ell_0(n, Lhat)] + M ell_D' + sum of ell_T + ell_B.
    Returns (bound, condition holds?)."""
    if seq is None:
        seq = Q.epoch_seq(cu, max(M, 1))
    eh = min(eps, 1.0)
    Lam0 = delta_ln + n * LN2
    Lhat = (M + 3) * Lam0
    cond = (seq['k'][M] - 1) * Q.qS(cu, n, Lhat) <= Lam0
    l0 = ell0(cu, n, Lhat)
    cl = 1 + Q.c_log(cu, n) + cu.h
    tot = E_frakB(cu, n, Lhat)
    for e in range(M, -1, -1):
        alpha = eh if e == M else 1.0
        Bp = seq['B'][e] if e >= 1 else cu.a
        calX = X_D(cu, n, seq['phi'][e - 1]) if e >= 1 else X_B(cu, n)
        tot += ellT_closed(cu, n, Lhat, Bp, calX, alpha)
        if e >= 1:
            B, phi, dm, J = seq['B'][e - 1], seq['phi'][e - 1], seq['d'][e - 1], seq['J'][e - 1]
            tot += Dprime_Bt(cu, [(B, 1.0)], phi) + l0
            tot += J * l0 + cl * J * (J + 1) / (2 * dm)
    return tot, cond


# ---------------------------------------------------------------------------------------------------------------
#  families with exact certified costs (interface of experiments/workstreams/Q/qscheme.py:
#  costs(d, xs, ld) -> ln of the certified bound; B, sigma, R; Ebound(d, x, Lam))
# ---------------------------------------------------------------------------------------------------------------
class Stat:
    """least slacks and violations of the inequalities checked on the way"""

    def __init__(self):
        self.n = {}
        self.minslack = {}
        self.viol = []

    def add(self, name, exact, bound, tag=None):
        self.n[name] = self.n.get(name, 0) + 1
        sl = bound - exact
        if sl < self.minslack.get(name, (INF, None))[0]:
            self.minslack[name] = (sl, tag)
        if sl < -1e-9:
            self.viol.append((name, tag, exact, bound))

    def total(self):
        return sum(self.n.values())


class FamBase:
    sigma = 0.0
    R = INF

    def majorant(self, d, x):
        if self.sigma == 0.0:
            return d * self.B
        return d * self.B - self.sigma * min(x, self.R * d)

    def node(self, d, x, ld, v):
        Lam = -ld + d * LN2
        self.st.add('induction ' + self.name, float(v), self.majorant(d, x) + self.Ebound(d, x, Lam), (d, x, ld))


class HiBase(FamBase):
    """the base family (two-sample bracket of Proposition K0 or enumeration) used at accuracies >= X_B(N) only:
    type H_N(a, 0, inf; E_frakB) by Proposition Q5(b) of Q_REPORT at e = 0"""
    name = 'base at log accuracy'

    def __init__(self, cu, N, st, fast=True):
        self.cu, self.N, self.st = cu, N, st
        self.B = cu.a
        self.xmin = X_B(cu, N)
        # fast: the referee's implementation of the base family (r12lib.Base, pure numpy tables); otherwise qlib's
        # (the two agree to rounding: q2_02_chain.py, part B, compares them)
        self.fast = fast
        if fast:
            cR = R.Cube(cu.u)
            self.rbase = R.Base(cR, R.TabCache(cu.u, 2), R.Stats(), R.Formula(cR))

    def Ebound(self, d, x, Lam):
        return E_frakB(self.cu, d, Lam)

    def costs(self, d, xs, ld):
        xs = np.asarray(xs, dtype=float)
        assert d <= self.N and np.all(xs >= self.xmin - 1e-12)
        if self.fast:
            if len(self.rbase._rm) > 2:
                self.rbase._rm.clear()          # r12lib.Base keeps up to 60 arrays of length d: 1 GB at d = 10^6
            out = np.array([self.rbase.raw(d, float(x), ld)[0] for x in xs])
        else:
            out = Q.BaseTable(self.cu.u, d).costs(xs, ld)
        self.node(d, float(xs[-1]), ld, out[-1])
        return out


class DprimeFam(FamBase):
    """D'[inner; phi, X] with horizon N (Proposition D'), inner of type H_N(B, sigma, R; E) with one line.
    mode 'proof': the level as built where it is defined, the pass-through elsewhere; 'min': the cheaper of the two."""
    name = "D'"

    def __init__(self, ev, inner, phi, N, st, mode='min', calX=None):
        self.ev, self.cu, self.inner, self.phi, self.N, self.st, self.mode = ev, ev.cu, inner, phi, N, st, mode
        self.lines = [(inner.B, inner.sigma)]
        self.Rin = inner.R
        assert 0 <= inner.sigma <= 1 and 0 < inner.R <= 1 and phi <= inner.R / (self.cu.a + inner.R) * (1 + 1e-12)
        self.calX = X_D(self.cu, N, phi) if calX is None else calX
        assert self.calX >= X_D(self.cu, N, phi) - 1e-12
        self.xmin = self.calX
        self.B = Dprime_Bp(self.cu, self.lines, phi)
        self.Bt = Dprime_Bt(self.cu, self.lines, phi)
        self.memo = {}
        self.wins = dict(level=0, passthrough=0)

    def Ebound(self, d, x, Lam):
        return self.inner.Ebound(d, 1.0, Lam + Q.qS(self.cu, d, Lam)) + cDp(self.cu, d, Lam, self.Bt)

    def costs(self, d, xs, ld):
        xs = np.asarray(xs, dtype=float)
        assert d <= self.N and np.all(xs >= self.calX - 1e-12)
        key = (d, round(ld, 9))
        if key not in self.memo:
            cu = self.cu
            cands = {}
            if Dprime_built(cu, d, self.phi):
                r = Dprime_level(self.ev, d, self.phi, self.Rin, self.calX, ld, self.inner)
                c = r['c']
                Lam = -ld + d * LN2
                n_o = r['n_o']
                self.st.add("D' as built", r['lC'], d * self.B + self.Ebound(d, self.calX, Lam), (d, ld))
                self.st.add("D': Lemma Q4(b) at e = 0", c['l_inv_pi'], n_o * cu.a + math.log(n_o + 1), (d,))
                self.st.add("D': accuracy", abs(c['xout'] - self.calX), 1e-8, (d,))
                check_U_consts(cu, d, n_o, c, Lam, self.st.viol, ("D'", d, ld))
                cands['level'] = r['lC']
            if self.mode == 'min' or not cands:
                cands['passthrough'] = float(self.inner.costs(d, np.array([self.calX]), ld)[0])
            win = min(cands, key=cands.get)
            self.wins[win] += 1
            self.memo[key] = cands[win]
            self.node(d, self.calX, ld, cands[win])
        return np.full(xs.shape, self.memo[key])


class ChainFam(FamBase):
    """T[inner; alpha, m] with horizon N (Proposition T) on top of a flat family `inner` of least accuracy X = inner.xmin.
    Accuracy-blind: delivers a_d <= alpha.  m = None: the block of the design for the entry value Lam_entry."""
    name = 'T'

    def __init__(self, ev, inner, alpha, N, st, Lam_entry, m=None):
        self.ev, self.cu, self.inner, self.N, self.st = ev, ev.cu, inner, N, st
        assert inner.sigma == 0.0
        self.B = inner.B
        self.calX = inner.xmin
        if m is None:
            m = Chain.design_m(self.cu, N, self.B, self.calX, alpha, Lam_entry)
        self.ch = Chain(self.cu, N, self.B, self.calX, alpha, m)
        self.xmin = alpha
        self.memo = {}
        self.nlev = 0

    def Ebound(self, d, x, Lam):
        return self.ch.E_T(d, Lam, Efun=lambda dd, xx, LL: self.inner.Ebound(dd, xx, LL))

    def costs(self, d, xs, ld):
        xs = np.asarray(xs, dtype=float)
        assert d <= self.N and np.all(xs >= self.xmin - 1e-12)
        key = (d, round(ld, 9))
        if key not in self.memo:
            t, recs, bottom = self.ch.exact(self.ev, d, ld, self.inner)
            self.nlev += len(recs)
            cu, ch = self.cu, self.ch
            # the bottom and every level of this chain against the bound of Proposition T, and the ball of every level
            self.node(bottom['d'], ch.alpha, bottom['ld'], bottom['t'])
            for r in recs:
                self.node(r['d'], ch.alpha, r['ld'], r['t'])
                self.st.add('T: ln(1/pi_dagger) <= varpi', r['c']['l_inv_pi'], varpi(cu, ch.m, ch.c), (r['d'],))
                self.st.add('T: accuracy', r['c']['xout'], ch.acc(r['d']) + 1e-12, (r['d'],))
            self.memo[key] = t
        return np.full(xs.shape, self.memo[key])
