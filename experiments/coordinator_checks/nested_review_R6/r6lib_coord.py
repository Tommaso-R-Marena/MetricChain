"""Coordinator's check of SCI-REV-0007 -- shared exact tables and the constants of Theorem 11.56.

Written from the statements of the theory report (Theorem 11.56, Proposition 11.57(a), Theorem 11.45(b),
Theorem 11.25(a)) and from K_REPORT.md section 2.2 (constants) and section 3.2 (the base family); nothing is
imported from experiments/workstreams/K or from the science division's scripts.

Arithmetic: binomial coefficients and ball sizes are exact python integers; E_r, T_m(k) and everything that
contains e^u are mpmath numbers with 60 significant digits (all sums have positive terms only, so there is no
cancellation); radii are found by exact or 60-digit comparisons.

Notation on a cube Q_m with slope u:
    ball[r]  = |B(m, r)|,  r = 0..m               (|B(m,-1)| = 0)
    E[r]     = E_r(m) = sum_{j<=r} C(m,j) (e^{u(r+1-j)} - 1)
    T[k]     = T_m(k) = sum_j C(m,j) e^{-u (j-k)_+}
    Gt(r)    = E_r/|B(m,r-1)|  (r >= 1),  Gt(0) = e^u - 1                       one-sided ratio
    kappa(r) = largest k >= 0 with |B(m,k)| <= max{1, c_eta |B(m,r-1)|}
    G2(r)    = E_r / T_m(kappa(r))                                              two-sided ratio
"""
import math
import os
from fractions import Fraction
import bisect
import mpmath as mp

mp.mp.dps = 60

HERE = os.path.dirname(os.path.abspath(__file__))


def outfile(name):
    """Where an output goes: ../out/<name> in the scratch layout (scripts in code/, outputs in out/), and
    out_<name> next to the script in the repository (experiments/coordinator_checks/nested_review_R6/)."""
    d = os.path.join(HERE, os.pardir, "out")
    if os.path.basename(HERE) == "code" and os.path.isdir(d):
        return os.path.join(d, name)
    return os.path.join(HERE, "out_" + name)


class Tab:
    def __init__(self, m, u):
        self.m = m
        self.u = mp.mpf(u)
        binom = [1] * (m + 1)
        for j in range(1, m + 1):
            binom[j] = binom[j - 1] * (m - j + 1) // j
        self.binom = binom
        ball, s = [], 0
        for j in range(m + 1):
            s += binom[j]
            ball.append(s)
        self.ball = ball                                   # ball[r] = |B(m,r)|, exact
        assert ball[m] == 2 ** m
        eu = mp.exp(self.u)
        E = [eu - 1]
        for r in range(1, m + 1):                          # E_r = e^u E_{r-1} + (e^u - 1)|B(m,r)|
            E.append(eu * E[-1] + (eu - 1) * ball[r])
        self.E = E
        emu = mp.exp(-self.u)
        S = [mp.mpf(0)] * (m + 1)                          # S_k = sum_{j>k} C(m,j) e^{-u(j-k)}
        for k in range(m, 0, -1):
            S[k - 1] = emu * (binom[k] + S[k])
        self.T = [ball[k] + S[k] for k in range(m + 1)]
        self._kappa_cache = {}

    def ballm1(self, r):
        """|B(m, r)| with |B(m,-1)| = 0."""
        return self.ball[r] if r >= 0 else 0

    def Gt(self, r):
        return mp.exp(self.u) - 1 if r == 0 else self.E[r] / self.ball[r - 1]

    def kball(self, target):
        """largest k >= 0 with |B(m,k)| <= max(1, target); target an exact Fraction or int."""
        t = max(Fraction(1), Fraction(target))
        # ball is increasing; find the last index with ball[k] <= t
        k = bisect.bisect_right(self.ball, t) - 1          # comparison int <-> Fraction is exact
        return max(k, 0)

    def kappa(self, r, c_eta):
        key = (r, c_eta)
        if key not in self._kappa_cache:
            self._kappa_cache[key] = self.kball(c_eta * self.ballm1(r - 1))
        return self._kappa_cache[key]

    def G2(self, r, c_eta):
        return self.E[r] / self.T[self.kappa(r, c_eta)]

    def radius(self, q):
        """least r in 0..m with |B(m,r)| >= 2^m q, q an exact Fraction in (0,1]."""
        return bisect.bisect_left(self.ball, Fraction(q) * 2 ** self.m)


def consts(u):
    """(p_u, Lambda_1, eps*, a, h) as floats."""
    pu = 1 / (1 + math.exp(u))
    lam1 = math.log(2 / (1 + math.exp(-u)))
    kl = lambda x, y: x * math.log(x / y) + (1 - x) * math.log((1 - x) / (1 - y))
    return pu, lam1, math.log(math.cosh(u / 2)), kl(pu, 0.5), kl(lam1 / u, 0.5)


def frac(x):
    """Exact Fraction of a decimal parameter such as 0.05 (through its repr, so that 0.05 = 1/20)."""
    return Fraction(repr(x)) if not isinstance(x, Fraction) else x


def rdagger(tab, eta, theta, nu0):
    """r_dagger: the largest r in 0..m-1 such that for all r' <= r
         [N] Gt(r') <= theta (1-eta) nu0   and   [P] min{Gt(r')/c_eta, G2(r')} <= theta;   -1 if it fails at r' = 0."""
    eta_f = frac(eta)
    c_eta = (1 - eta_f) / (1 + eta_f)
    th = mp.mpf(theta)
    limN = th * (1 - mp.mpf(eta)) * nu0
    r = -1
    for rr in range(tab.m):
        g1 = tab.Gt(rr)
        if g1 <= limN and min(g1 / mp.mpf(c_eta.numerator) * c_eta.denominator, tab.G2(rr, c_eta)) <= th:
            r = rr
        else:
            break
    return r


def constants_2Lplus(n, n_o, u, lam, eta, etap, theta, nu1, b, delta, xs, tab_o):
    """The constants of Algorithm 2L+ (K_REPORT 2.2 / Theorem 11.56).  xs = [x_0, x_1, ..., x_L] (x_0 = 2 u n_i)."""
    L = len(xs) - 1
    uf, lamf, etaf, etapf, thf, bf = (mp.mpf(v) for v in (u, lam, eta, etap, theta, b))
    J = int(mp.ceil((2 * uf * n + bf + n_o * mp.log(2)) / lamf))
    nu0 = max((J + 1) * mp.expm1(lamf) / etapf, mp.mpf(nu1)) / (1 - etaf)
    rdag = rdagger(tab_o, eta, theta, nu0)
    two_no = mp.mpf(2) ** n_o
    pidag = mp.mpf(tab_o.ball[rdag]) / two_no if rdag >= 0 else 1 / (2 * two_no)
    m_max = int(mp.ceil(mp.log(2 * (1 + etaf) * mp.exp(lamf) * nu0 / ((1 - etaf) * pidag), 2)))
    K = int(mp.ceil(3 * (1 + etaf) / etaf ** 2 * mp.log(2 * (J + 1) * (m_max + 1) * (L + 2) / mp.mpf(delta))))
    nu = K * nu0
    Mdag = K / ((1 - etaf) * pidag)
    Mbar = 2 * (1 + etaf) * mp.exp(lamf) * nu0 * Mdag
    deltap = mp.mpf(delta) / (4 * L * Mbar)
    cnt = lambda x: max(mp.mpf(K), 2 * (1 + etaf) ** 2 / (1 - etaf) * mp.exp(lamf) * nu * mp.exp(mp.mpf(x)))
    pu = 1 / (1 + mp.exp(uf))
    x_out = mp.log((2 * pu) ** n + mp.exp(bf) * (mp.exp(lamf) * (1 + etaf) / (1 - etaf) + etapf + thf))
    return dict(L=L, J=J, nu0=nu0, rdag=rdag, pidag=pidag, m_max=m_max, K=K, nu=nu, Mdag=Mdag, Mbar=Mbar,
                deltap=deltap, cnt=cnt, x_out=x_out)


def base_bracket_cost(tab_i, x, deltap):
    """Cost (number of evaluations, mpf) of the base bracket of Proposition 11.57(a) = K0 in dimension d = tab_i.m
    with accuracy x and failure probability deltap:  eta = min(1/2, tanh(x/4)),  K = ceil(3(1+eta)/eta^2 ln(4/deltap)),
    r* the largest radius <= d-1 with ln(1 + G2(r')) <= x - ln((1+eta)/(1-eta)) for all r' <= r*,
    M = ceil(K 2^d/((1-eta)|B(d,r*)|)),  cost min(2M, 2^d);  2^d if no radius qualifies.  Returns (cost, info)."""
    d = tab_i.m
    xf = mp.mpf(x)
    eta = min(mp.mpf(1) / 2, mp.tanh(xf / 4))
    # kappa needs c_eta exactly: eta is irrational in general, so use a 60-digit rational image of c_eta
    c_eta_mp = (1 - eta) / (1 + eta)
    c_eta = Fraction(int(mp.floor(c_eta_mp * mp.mpf(10) ** 55)), 10 ** 55)
    K = int(mp.ceil(3 * (1 + eta) / eta ** 2 * mp.log(4 / deltap)))
    budget = xf - mp.log((1 + eta) / (1 - eta))
    full = mp.mpf(2) ** d
    if budget <= 0:
        return full, dict(eta=eta, K=K, rstar=None, enumerated=True)
    lim = mp.expm1(budget)                                  # G2 <= e^budget - 1
    rstar = -1
    for r in range(d):
        if tab_i.G2(r, c_eta) <= lim:
            rstar = r
        else:
            break
    if rstar < 0:
        return full, dict(eta=eta, K=K, rstar=None, enumerated=True)
    M = mp.ceil(K * full / ((1 - eta) * tab_i.ball[rstar]))
    cost = min(2 * M, full)
    return cost, dict(eta=eta, K=K, rstar=rstar, M=M, enumerated=(2 * M >= full))


def nonadaptive_lb(tab_n, eps, delta):
    """Theorem 11.45(b): D_R = n ln(1+e^{-u}) - ln sum_j C(n,j) e^{-u max(j,R)};  if eps < D_R every randomised
    non-adaptive algorithm that is (eps/2, delta)-correct on the class evaluates at least (1-2 delta) 2^n/|B(n,R-1)|
    points in expectation.  Returns (ln of the bound for the least R with D_R > eps, R, D_R, D_{R-1})."""
    n, u = tab_n.m, tab_n.u
    binom = tab_n.binom
    # F(R) = sum_j C(n,j) e^{-u max(j,R)} = e^{-uR} |B(n,R)|-ish:  = e^{-uR} sum_{j<=R} C(n,j) + sum_{j>R} C(n,j) e^{-uj}
    emu = mp.exp(-u)
    up = [mp.mpf(0)] * (n + 2)                              # up[R] = sum_{j>=R} C(n,j) e^{-uj}
    for j in range(n, -1, -1):
        up[j] = up[j + 1] + binom[j] * emu ** j
    base = n * mp.log(1 + emu)
    prevD = None
    for R in range(0, n + 1):
        low = tab_n.ball[R - 1] if R >= 1 else 0           # sum_{j<R} C(n,j)
        F = mp.exp(-u * R) * low + up[R]
        D = base - mp.log(F)
        if D > eps:
            if R == 0:
                return None
            lb = mp.log(1 - 2 * mp.mpf(delta)) + n * mp.log(2) - mp.log(tab_n.ball[R - 1])
            return lb, R, D, prevD
        prevD = D
    return None


def hinted_lb(tab_n, eps, delta):
    """Theorem 11.25(a): if eps < Delta_k, e^{Delta_k} - 1 = 2^{-n} E_k(n), then E|Q(0)| >= (1-2 delta) 2^n/|B(n,k)|.
    Returns (ln of the bound for the least such k, k)."""
    n = tab_n.m
    target = mp.expm1(mp.mpf(eps)) * mp.mpf(2) ** n
    for k in range(n + 1):
        if tab_n.E[k] > target:
            return mp.log(1 - 2 * mp.mpf(delta)) + n * mp.log(2) - mp.log(tab_n.ball[k]), k
    return None
