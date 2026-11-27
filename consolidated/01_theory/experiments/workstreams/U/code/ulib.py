#!/usr/bin/env python3
"""Shared formulas for workstream U (own code; numpy/scipy only).

Notation of the theory report: p_u = 1/(1+e^u), Lambda1 = ln(2/(1+e^{-u})),
f(rho) = KL(rho || 1/2), a = f(p_u), h = f(Lambda1/u), eps* = ln cosh(u/2),
theta_hint(e) = f((Lambda1+e)/u) (0 from eps* on),
theta_na(e)   = min{ f(rho) : KL(rho||p_u) <= e } (0 from eps* on),
D(theta)      = u f^{-1}(theta) - Lambda1  (the accuracy rate that a budget e^{n theta} certifies with a hint;
                the inverse of theta_hint; D(h) = 0, D(a) = -a ... = u p_u - Lambda1),
x_na(theta)   = D(theta) + theta (shear law: what a non-adaptive sample of e^{n theta} points certifies).
"""
import math
import numpy as np
from scipy.optimize import brentq

LN2 = math.log(2.0)


def f(rho):
    """KL(rho || 1/2), for 0 <= rho <= 1 (scalar or array)."""
    r = np.clip(np.asarray(rho, dtype=float), 1e-300, 1 - 1e-16)
    return LN2 + r * np.log(r) + (1 - r) * np.log1p(-r)


def finv(theta):
    """the radius rho in [0, 1/2] with f(rho) = theta (0 <= theta <= ln 2)."""
    theta = float(theta)
    if theta <= 0:
        return 0.5
    if theta >= LN2:
        return 0.0
    return brentq(lambda r: float(f(r)) - theta, 1e-15, 0.5, xtol=1e-15, rtol=1e-14)


class Cube:
    def __init__(self, u):
        self.u = float(u)
        self.pu = 1.0 / (1.0 + math.exp(u))
        self.Lam1 = math.log(2.0 / (1.0 + math.exp(-u)))
        self.rho_h = self.Lam1 / u
        self.a = float(f(self.pu))
        self.h = float(f(self.rho_h))
        self.eps_star = math.log(math.cosh(u / 2.0))

    def kl_pu(self, rho):
        """KL(rho || p_u) = f(rho) + u rho - Lambda1."""
        return f(rho) + self.u * np.asarray(rho, dtype=float) - self.Lam1

    def theta_hint(self, e):
        if e >= self.eps_star:
            return 0.0
        return float(f((self.Lam1 + e) / self.u))

    def theta_na(self, e):
        """min{ f(rho) : KL(rho||p_u) <= e }, for e > 0; theta_na(0) := a."""
        if e >= self.eps_star:
            return 0.0
        if e <= 0:
            return self.a
        r = brentq(lambda r: float(self.kl_pu(r)) - e, self.pu, 0.5, xtol=1e-15, rtol=1e-14)
        return float(f(r))

    def D(self, theta):
        """hinted accuracy rate at budget theta: u f^{-1}(theta) - Lambda1."""
        return self.u * finv(theta) - self.Lam1

    def x_na(self, theta):
        """non-adaptive accuracy rate at budget theta (0 <= theta <= a): KL(f^{-1}(theta) || p_u)."""
        return self.D(theta) + theta


def log_binom_pmf(n):
    """log of the Bin(n, 1/2) probability mass function, array of length n+1."""
    from scipy.special import gammaln
    k = np.arange(n + 1)
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1) - n * LN2


def logsumexp(a):
    a = np.asarray(a, dtype=float)
    m = np.max(a)
    return m + math.log(np.sum(np.exp(a - m)))
