"""Workstream K -- shared formulas (own code; nothing imported from the repository).

Notation (theory report 11.16 / 11.18):
  p_u = 1/(1+e^u), Lambda1 = ln(2/(1+e^-u)), eps* = ln cosh(u/2), a = KL(p_u||1/2), h = KL(Lambda1/u||1/2)
  B(n,r) Hamming ball, E_r(n) = sum_{j<=r} C(n,j)(e^{u(r+1-j)} - 1), T_n(k) = sum_j C(n,j) e^{-u (j-k)_+}
  Gt(r)  = E_r/|B(r-1)|  (r >= 1),  Gt(0) = e^u - 1            ("one-sided" ratio, Gamma-tilde of Theorem 11.52)
  kappa(r) = largest k >= 0 with |B(k)| <= max(1, c |B(r-1)|),  c = (1-eta)/(1+eta)
  G2(r)  = E_r / T(kappa(r))                                   ("two-sided" ratio used for populated levels)
All tables are in natural logarithms so that n up to 10^5 is harmless.
"""
import math
import numpy as np


def kl(a, b):
    r = 0.0
    if a > 0:
        r += a * math.log(a / b)
    if a < 1:
        r += (1 - a) * math.log((1 - a) / (1 - b))
    return r


def consts(u):
    """(p_u, Lambda1, eps*, a, h)"""
    pu = 1 / (1 + math.exp(u))
    lam = math.log(2 / (1 + math.exp(-u)))
    return pu, lam, math.log(math.cosh(u / 2)), kl(pu, 0.5), kl(lam / u, 0.5)


def theta_na(u, e1):
    """min{KL(rho||1/2) : KL(rho||p_u) <= e1}  (non-adaptive exponent); a at e1 = 0."""
    pu = 1 / (1 + math.exp(u))
    if e1 >= kl(0.5, pu):
        return 0.0
    if e1 <= 0:
        return kl(pu, 0.5)
    lo, hi = pu, 0.5
    for _ in range(200):
        mid = (lo + hi) / 2
        if kl(mid, pu) <= e1:
            lo = mid
        else:
            hi = mid
    return kl(lo, 0.5)


def theta_hint(u, e1):
    rho = (math.log(2 / (1 + math.exp(-u))) + e1) / u
    return kl(rho, 0.5) if rho < 0.5 else 0.0


class Cube:
    """Log-tables of the n-cube for slope u.

    lb[j]      = ln C(n,j)                     j = 0..n
    lball[r+1] = ln |B(n,r)|                   r = -1..n   (lball[0] = -inf)
    lE[r]      = ln E_r(n)                     r = 0..n
    lT[k]      = ln T_n(k)                     k = 0..n
    lGt[r]     = ln Gt(r)                      r = 0..n
    """

    def __init__(self, n, u):
        self.n, self.u = n, u
        j = np.arange(n + 1)
        self.lb = np.array([math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) for k in j])
        self.lball = np.concatenate([[-np.inf], np.logaddexp.accumulate(self.lb)])
        l1 = math.log(math.expm1(u))
        lE = np.empty(n + 1)
        lE[0] = l1
        for r in range(1, n + 1):                       # E_r = e^u E_{r-1} + (e^u - 1)|B(r)|
            lE[r] = np.logaddexp(u + lE[r - 1], l1 + self.lball[r + 1])
        self.lE = lE
        lS = np.empty(n + 1)                            # S_k = sum_{j>k} C(n,j) e^{-u(j-k)},  S_{k-1} = e^{-u}(C(n,k) + S_k)
        lS[n] = -np.inf
        for k in range(n, 0, -1):
            lS[k - 1] = -u + np.logaddexp(self.lb[k], lS[k])
        self.lT = np.logaddexp(self.lball[1:], lS)
        self.lGt = np.concatenate([[l1], lE[1:] - self.lball[1:-1]])

    def lball_r(self, r):
        return self.lball[r + 1]

    def radius(self, logq):
        """least r in 0..n with |B(n,r)| >= 2^n q   (logq = ln q <= 0).  For q = 1 the answer is n: in floating point
        ln|B(n,r)| is indistinguishable from n ln 2 long before r = n, and a tail lemma applied at such a radius
        would be the closure gap of DEAD_ENDS D45, item 4."""
        if logq >= 0:
            return self.n
        return int(np.searchsorted(self.lball[1:], self.n * math.log(2) + logq - 1e-12))

    def kball(self, logcount):
        """largest k >= 0 with |B(n,k)| <= max(1, count)   (logcount = ln count)"""
        t = max(0.0, logcount)
        k = int(np.searchsorted(self.lball[1:], t + 1e-12, side="right")) - 1
        return max(k, 0)

    def kappa(self, r, eta):
        """largest k >= 0 with |B(k)| <= max(1, (1-eta)/(1+eta) |B(r-1)|)"""
        if r == 0:
            return 0
        return self.kball(math.log((1 - eta) / (1 + eta)) + self.lball[r])

    def lG2(self, r, eta):
        return self.lE[r] - self.lT[self.kappa(r, eta)]

    def log_binom_cdf(self, p):
        """ln P(Bin(n,p) <= r) for r = 0..n and ln P(Bin(n,p) >= k) for k = 0..n"""
        j = np.arange(self.n + 1)
        lp = self.lb + j * math.log(p) + (self.n - j) * math.log(1 - p)
        lower = np.logaddexp.accumulate(lp)
        upper = np.logaddexp.accumulate(lp[::-1])[::-1]
        return lower, upper


def rdagger(cube, eta, theta, nu0):
    """largest r <= n-1 such that for all r' <= r:
         [N]  Gt(r') <= theta (1-eta) nu0     and     [P]  min((1+eta)/(1-eta) Gt(r'), G2(r')) <= theta ;
       -1 if the conditions fail at r' = 0."""
    n = cube.n
    lth = math.log(theta)
    lN = lth + math.log((1 - eta) * nu0)
    c = math.log((1 + eta) / (1 - eta))
    r = -1
    for rr in range(0, n):
        okN = cube.lGt[rr] <= lN + 1e-12
        okP = min(c + cube.lGt[rr], cube.lG2(rr, eta)) <= lth + 1e-12
        if okN and okP:
            r = rr
        else:
            break
    return r
