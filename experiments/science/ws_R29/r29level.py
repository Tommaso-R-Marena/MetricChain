#!/usr/bin/env python3
"""r29level.py -- my own exact evaluator of the certified cost C_max of one level of Algorithm 2L+ (theory report,
Theorem 11.56, as quoted there), written from the statement; nothing of the theory division's evaluators is imported.

From the statement (THEORY_REPORT.md lines 5544-5553 and 5605-5646):
    E_r(m) = sum_{j<=r} C(m,j)(e^{u(r+1-j)} - 1),     T_m(k) = sum_j C(m,j) e^{-u(j-k)_+},     c_eta = (1-eta)/(1+eta),
    Gamma~(r) = E_r(m)/|B(m, r-1)|  (Gamma~(0) = e^u - 1),   Gamma''(r) = E_r(m)/T_m(kappa(r)),
    kappa(r) = the largest k >= 0 with |B(m,k)| <= max{1, c_eta |B(m, r-1)|};
    J = ceil((2un + b + n_o ln 2)/lambda),   nu_0 = (1-eta)^{-1} max{(J+1)(e^lambda - 1)/eta', nu_1},   nu = K nu_0,
    r_dagger = the largest radius <= n_o - 1 with Gamma~(r') <= theta (1-eta) nu_0 and min{Gamma~(r')/c_eta, Gamma''(r')} <= theta
               for all r' <= r_dagger,     pi_dagger = 2^{-n_o} |B(n_o, r_dagger)|,
    Mbar = 2(1+eta) e^lambda nu_0 K/((1-eta) pi_dagger),     delta' = delta/(4 L Mbar),
    cnt(x) = max{K, 2(1+eta)^2 (1-eta)^{-1} e^lambda nu e^x},
    accuracy = ln[(2p_u)^n + e^b (e^lambda (1+eta)/(1-eta) + eta' + theta)],
    C_max = 1 + 2 Mbar + sum_{l=1}^{L} min{2 Mbar, (J+1) cnt(x_{l-1})} C_l.
NOT in the statement as quoted ("K = O(eta^-2 ln(nL/delta))"; "complete text and all constants: K_REPORT.md 2.2", which
is not in my export):  the exact K and m_max.  They are taken from the theory division's evaluator qlib.level_consts
(read, not imported):   m_max = ceil((ln(2(1+eta)/(1-eta)) + lambda + ln nu_0 - ln pi_dagger)/ln 2),
                        K = ceil(3(1+eta) eta^-2 (ln(2(J+1)(m_max+1)(L+2)) + ln(1/delta))).
Arithmetic: ball sizes are exact integers; E_r and T_m(k) are computed by exact recurrences in 40-digit mpmath
(their evaluators use log-domain doubles); kappa(r) by exact integer comparison for rational eta.
"""
import math
from fractions import Fraction as Fr

import mpmath
import numpy as np

LN2 = math.log(2.0)


class Tables:
    """log Gamma~(r) and log Gamma''(r), r = 0..m-1, and log |B(m, r)|, on the outer cube Q_m"""

    def __init__(self, m, u, eta=Fr(1, 2)):
        mpmath.mp.dps = 40
        self.m = m
        C = [1] * (m + 1)
        for j in range(1, m + 1):
            C[j] = C[j - 1] * (m - j + 1) // j
        B = [0] * (m + 1)
        acc = 0
        for j in range(m + 1):
            acc += C[j]
            B[j] = acc
        eu = mpmath.exp(mpmath.mpf(u))
        emu = 1 / eu
        # A_r = sum_{j<=r} C(m,j) e^{u(r+1-j)} = e^u (A_{r-1} + C(m,r));   E_r = A_r - |B(m,r)|
        A = [None] * (m + 1)
        prev = mpmath.mpf(0)
        for r in range(m + 1):
            prev = eu * (prev + C[r])
            A[r] = prev
        # D_k = sum_{j>k} C(m,j) e^{-u(j-k)}:  D_m = 0,  D_{k-1} = e^{-u}(C(m,k) + D_k);   T_m(k) = |B(m,k)| + D_k
        D = [None] * (m + 1)
        D[m] = mpmath.mpf(0)
        for k in range(m, 0, -1):
            D[k - 1] = emu * (C[k] + D[k])
        ceta = (1 - Fr(eta)) / (1 + Fr(eta))
        num, den = ceta.numerator, ceta.denominator
        lGt = np.empty(m)
        lGpp = np.empty(m)
        kap = 0
        for r in range(m):                                  # radii 0 .. m-1
            Er = A[r] - B[r]
            if r == 0:
                lGt[r] = float(mpmath.log(eu - 1))
                bound_num, bound_den = 1, 1                  # max{1, c_eta * 0} = 1
            else:
                lGt[r] = float(mpmath.log(Er / B[r - 1]))
                # max{1, c_eta |B(m, r-1)|} as a rational
                if num * B[r - 1] > den:
                    bound_num, bound_den = num * B[r - 1], den
                else:
                    bound_num, bound_den = 1, 1
            while kap + 1 <= m and B[kap + 1] * bound_den <= bound_num:   # kappa(r) is nondecreasing in r
                kap += 1
            Tk = B[kap] + D[kap]
            lGpp[r] = float(mpmath.log(Er / Tk))
        self.lGt, self.lGpp = lGt, lGpp
        self.lB = np.array([float(mpmath.log(b)) for b in B])
        self.lceta = math.log(float(ceta))


_TABS = {}


def tables(m, u):
    key = (m, u)
    if key not in _TABS:
        if len(_TABS) > 2500:
            _TABS.clear()
        _TABS[key] = Tables(m, u)
    return _TABS[key]


def level(u, n, n_o, ltheta, xs, lcosts_fn, ldelta, lam=1.0, eta=0.5, etap=1.0, nu1=1.0, b=1.0):
    """ln C_max and the constants of one level.  xs = [x_0 = 2u n_i, x_1 > ... > x_L] (x_L <= b);  lcosts_fn(n_i, xs[1:],
    ln delta') returns the log-costs ln C_l of the inner procedures."""
    t = tables(n_o, u)
    L = len(xs) - 1
    J = math.ceil((2 * u * n + b + n_o * LN2) / lam)
    nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
    okN = t.lGt <= ltheta + math.log((1 - eta) * nu0)
    okP = np.minimum(t.lGt - t.lceta, t.lGpp) <= ltheta
    ok = okN & okP                                          # radii 0 .. n_o - 1
    bad = np.nonzero(~ok)[0]
    rdag = (int(bad[0]) - 1) if bad.size else n_o - 1
    if rdag < 0:
        raise ValueError("r_dagger = -1: not covered by the statement as quoted")
    lpidag = float(t.lB[rdag]) - n_o * LN2
    m_max = math.ceil((math.log(2 * (1 + eta) / (1 - eta)) + lam + math.log(nu0) - lpidag) / LN2)
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(2 * (J + 1) * (m_max + 1) * (L + 2)) - ldelta))
    lK = math.log(K)
    lMbar = math.log(2 * (1 + eta)) + lam + math.log(nu0) + lK - math.log(1 - eta) - lpidag
    ldeltap = ldelta - math.log(4 * L) - lMbar
    pu = 1.0 / (1.0 + math.exp(u))
    xout = float(np.logaddexp(n * math.log(2 * pu), b + np.logaddexp(math.log(math.exp(lam) * (1 + eta) / (1 - eta) + etap), ltheta)))
    xs = np.asarray(xs, dtype=float)
    lc = np.asarray(lcosts_fn(n - n_o, xs[1:], ldeltap), dtype=float)
    lcnt = np.maximum(lK, math.log(2 * (1 + eta) ** 2 / (1 - eta)) + lam + lK + math.log(nu0) + xs[:-1])
    terms = np.minimum(LN2 + lMbar, math.log(J + 1) + lcnt) + lc
    lC = float(np.logaddexp.reduce(np.concatenate(([0.0, LN2 + lMbar], terms))))
    return dict(lC=lC, J=J, nu0=nu0, rdag=rdag, lpidag=lpidag, m_max=m_max, K=K, lMbar=lMbar, ldeltap=ldeltap, xout=xout, L=L)


def level_Z2(u, d, n_o, y, theta_na, lines, ldelta):
    """the level L(d; n_o, e = y/n_o) of Lemma Z2 over a family that SATURATES the type of the lines [(B, sigma)]:
    lambda = 1, eta = 1/2, eta' = 1, nu_1 = 1, tolerance 1, theta = 3(n_o + 1) exp(2u + e^u + n_o e),
    ladder x_0 = 2u n_i > x_1 = min{max(ceil(n_o theta_na(e)), 1), ceil(2u n_i) - 1} > x_1 - 1 > ... > 1."""
    n_i = d - n_o
    e = y / n_o
    th = theta_na(e)
    ltheta = math.log(3.0 * (n_o + 1)) + 2 * u + math.exp(u) + y
    x1 = min(max(int(math.ceil(n_o * th)), 1), int(math.ceil(2 * u * n_i)) - 1)
    xs = np.concatenate(([2 * u * n_i], np.arange(x1, 0, -1, dtype=float)))
    LB = np.array([B for (B, s) in lines])
    LS = np.array([s for (B, s) in lines])

    def costs(ni, xl, ldp):
        return np.maximum(0.0, np.max(ni * LB[None, :] - LS[None, :] * np.asarray(xl)[:, None], axis=1))
    r = level(u, d, n_o, ltheta, xs, costs, ldelta)
    r["th"] = th
    r["main"] = float(np.max(n_i * LB + (1 - LS) * n_o * th))     # max_i [n_i B_i + (1 - sigma_i) n_o theta_na(e)]
    return r


# the explicit error functions of Lemma U as given in Q2_REPORT section 2 / q2lib (taken as given; not re-derived)
def A_n(u, n):
    return (2 * u + LN2) * n + 3


def Kbar_S(u, n, Lam):
    An = A_n(u, n)
    mbar = n + 2 + math.log2(12 * math.e * (math.e - 1) * An)
    return 18 * (Lam + math.log(2 * An * mbar * (n + 3))) + 1


def ell0(u, n, Lam):
    return 1 + 2 * math.log(A_n(u, n)) + math.log(18 * math.e * (math.e - 1)) + math.log(Kbar_S(u, n, Lam)) + math.log(n + 3)


def X0(u, d):
    return 2.0 + math.log(3.0 * (d + 1)) + 2 * u + math.exp(u)


def dmin(u):
    return int(math.floor(1.0 / (2 * u))) + 2
