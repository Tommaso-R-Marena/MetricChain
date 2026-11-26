#!/usr/bin/env python3
"""Workstream N -- shared routines (numpy/scipy only; nothing of the repository is imported here).

Contents
  CubeTables(m, u)            exact tables of the cube Q_m: |B(r)|, E_r, T_k; Harper's two tail functions as functions of q
  StepTail                    a nondecreasing step function on (0,1] (the form of every exact tail function of a finite space)
  envelope_tails(mu, rho)     the exact tail functions of an envelope class on a finite space by enumeration of all subsets
                              (N_REPORT section 2.1, Lemma N.0):   Xi(q) = max{ sum_{x in D} mu(x)(e^{rho(x -> D^c)} - 1) : mu(D) <= q }
                                                                   Theta(p) = min{ sum_x mu(x) e^{-rho(S -> x)} : mu(S) >= p }
  closing_level_steps(...)    the closing level pi_* of N_REPORT section 2.2 for step tail functions (exact)
  closing_level_grid(...)     the same on a grid of q (for tail functions given by formulas)
  Consts                      all constants of Algorithm A (N_REPORT section 2.2) from the parameters
  run_level(...)              Algorithm A (the abstract form of Algorithm 2L+ of K_REPORT 2.2) with a simulated bracket oracle
                              around the exact outer integrand, and the certificates of every pass recorded
  check_run(...)              the inequalities of the proof of Theorem N1, checked on a run of a finite outer space
  gauss_Xi, gauss_Theta       the exact tail functions of L-Lipschitz functions on Gauss space (N_REPORT section 5.1)
"""
import math

import numpy as np
from scipy.special import log_ndtr, ndtr, ndtri

INF = float("inf")


# ----------------------------------------------------------------------------------------------------------------
# the cube
# ----------------------------------------------------------------------------------------------------------------
class CubeTables:
    """exact tables of Q_m for the slope u (python floats; m up to a few hundred)"""

    def __init__(self, m, u):
        self.m, self.u = m, u
        self.N = 2.0 ** m
        self.binom = [math.comb(m, j) for j in range(m + 1)]
        self.ball = [0] * (m + 1)
        acc = 0
        for j in range(m + 1):
            acc += self.binom[j]
            self.ball[j] = acc
        # E_r = sum_{j<=r} C(m,j)(e^{u(r+1-j)} - 1):  E_r = e^u E_{r-1} + (e^u - 1)|B(r)|
        self.E = [0.0] * (m + 1)
        self.E[0] = math.expm1(u)
        for r in range(1, m + 1):
            self.E[r] = math.exp(u) * self.E[r - 1] + math.expm1(u) * self.ball[r]
        # T_k = sum_j C(m,j) e^{-u (j-k)_+}
        S = [0.0] * (m + 1)                        # S_k = sum_{j>k} C(m,j) e^{-u(j-k)}
        for k in range(m, 0, -1):
            S[k - 1] = math.exp(-u) * (self.binom[k] + S[k])
        self.T = [self.ball[k] + S[k] for k in range(m + 1)]

    # --- Harper's functions as functions of the measure -----------------------------------------------------
    def radius(self, q):
        """least r with |B(m,r)| >= 2^m q"""
        target = q * self.N * (1 - 1e-13)
        for r in range(self.m + 1):
            if self.ball[r] >= target:
                return r
        return self.m

    def Xi(self, q):
        """upper tail function (Lemma 11.43(b)):  0 below the atom, 2^-m E_r for the least r with |B(r)| >= 2^m q, r <= m-1,
        +infinity if r = m"""
        if q * self.N < 1 - 1e-12:
            return 0.0
        r = self.radius(q)
        return INF if r >= self.m else self.E[r] / self.N

    def kball(self, count):
        """largest k >= 0 with |B(m,k)| <= max(1, count)"""
        t = max(1.0, count) * (1 + 1e-13)
        k = 0
        while k + 1 <= self.m and self.ball[k + 1] <= t:
            k += 1
        return k

    def Theta(self, p):
        """lower tail function (Lemma 11.43(c)): 2^-m T_k, k the largest radius with |B(k)| <= max(1, 2^m p)"""
        return self.T[self.kball(p * self.N)] / self.N

    def ThetaBar(self, p):
        return max(p, self.Theta(p))

    # --- the quantities of K_REPORT 2.1 ----------------------------------------------------------------------
    def Gt(self, r):
        return math.expm1(self.u) if r == 0 else self.E[r] / self.ball[r - 1]

    def kappa(self, r, ceta):
        return 0 if r == 0 else self.kball(ceta * self.ball[r - 1])

    def G2(self, r, ceta):
        return self.E[r] / self.T[self.kappa(r, ceta)]

    def rdagger(self, theta, nu0, eta):
        """r_dagger of K_REPORT 2.1 (largest r <= m-1 with [N], [P] for all r' <= r; -1 if they fail at 0)"""
        ceta = (1 - eta) / (1 + eta)
        r = -1
        for rr in range(self.m):
            okN = self.Gt(rr) <= theta * (1 - eta) * nu0
            okP = min(self.Gt(rr) / ceta, self.G2(rr, ceta)) <= theta
            if okN and okP:
                r = rr
            else:
                break
        return r

    def pidagger(self, theta, nu0, eta):
        r = self.rdagger(theta, nu0, eta)
        return (self.ball[r] / self.N if r >= 0 else 0.5 / self.N), r

    def steps(self):
        """the upper tail function as a step function: breakpoints b_i = |B(i)|/2^m (i = 0..m), Xi = E_i/2^m on
        (b_{i-1}, b_i], = 0 below b_0, +inf on the last step"""
        bp = [self.ball[r] / self.N for r in range(self.m + 1)]
        val = [self.E[r] / self.N for r in range(self.m)] + [INF]
        return bp, val


# ----------------------------------------------------------------------------------------------------------------
# step tail functions and the closing level
# ----------------------------------------------------------------------------------------------------------------
class StepTail:
    """nondecreasing step function f on (0,1]:  f(q) = val[i] for b[i-1] < q <= b[i]  (b[-1] := 0), and, if
    `zero_below`, f(q) = 0 for q < b[0] (an atom of mass b[0]).  For a lower tail function use `left=True`:
    f(p) = val[i] for b[i] <= p < b[i+1], f = val0 below b[0]."""

    def __init__(self, bp, val, zero_below=True, left=False, val0=0.0):
        self.bp = np.asarray(bp, dtype=float)
        self.val = np.asarray(val, dtype=float)
        self.zero_below, self.left, self.val0 = zero_below, left, val0

    def __call__(self, q):
        if self.left:
            i = int(np.searchsorted(self.bp, q * (1 + 1e-13), side='right')) - 1
            return self.val0 if i < 0 else float(self.val[i])
        if self.zero_below and q < self.bp[0] * (1 - 1e-13):
            return 0.0
        i = int(np.searchsorted(self.bp, q * (1 - 1e-13), side='left'))
        i = min(i, len(self.val) - 1)
        return float(self.val[i])


def closing_level_steps(bp, val, ThetaBar, thrN, theta, ceta):
    """pi_* = sup{pi : [N] Xi(q) <= thrN q and [P] Xi(q) <= theta ThetaBar(ceta q) for all 0 < q < pi}, for the step
    function Xi = val[i] on (bp[i-1], bp[i]], Xi = 0 below bp[0] (so the first step is the single point bp[0]).
    ThetaBar must be nondecreasing.  On a step Xi is constant and both right-hand sides are nondecreasing, so the
    conditions hold on the whole step iff they hold in the limit at its left end.  Returns (pi_*, index of the first
    step that fails or len(bp))."""
    for i in range(len(bp)):
        left = bp[0] if i == 0 else bp[i - 1]
        qq = left if i == 0 else left * (1 + 1e-12)          # the right limit at the left end
        okN = val[i] <= thrN * left * (1 + 1e-12)
        okP = val[i] <= theta * ThetaBar(ceta * qq) * (1 + 1e-12)
        if not (okN and okP):
            return left, i
    return 1.0, len(bp)


def closing_level_grid(Xi, ThetaBar, thrN, theta, ceta, qgrid):
    """the same on an increasing grid of q (approximate: for tail functions given by formulas)"""
    pi = None
    for q in qgrid:
        x = Xi(q)
        if x <= thrN * q and x <= theta * ThetaBar(ceta * q):
            pi = q
        else:
            return (pi if pi is not None else qgrid[0] * 0.5)
    return pi


# ----------------------------------------------------------------------------------------------------------------
# exact tail functions of an envelope class on a finite space (all subsets)
# ----------------------------------------------------------------------------------------------------------------
def envelope_tails(mu, rho, return_sets=False):
    """mu: probabilities of the n points (n <= 20); rho[x, z] >= 0 the envelope: the class is
    {V > 0 : V(x) <= V(z) e^{rho[x,z]} for all x, z}.  Returns (Xi, Theta) as StepTail objects:
       Xi(q)    = max{ F(D) : D proper nonempty, mu(D) <= q },   F(D) = sum_{x in D} mu(x)(exp(min_{z not in D} rho[x,z]) - 1)
       Theta(p) = min{ G(S) : S nonempty, mu(S) >= p },          G(S) = sum_x mu(x) exp(-min_{y in S} rho[y,x])
    (Lemma N.0 of N_REPORT: both are valid, and attained by dips whenever rho is a quasi-metric.)"""
    mu = np.asarray(mu, dtype=float)
    n = len(mu)
    nm = 1 << n
    masks = np.arange(nm, dtype=np.int64)
    inD = ((masks[:, None] >> np.arange(n)[None, :]) & 1).astype(bool)          # (nm, n)
    meas = inD.astype(float) @ mu
    BIG = 1e300
    F = np.zeros(nm)
    G = np.zeros(nm)
    for x in range(n):
        # min over z not in D of rho[x, z]
        dmin = np.min(np.where(inD, BIG, rho[x][None, :]), axis=1)
        F += np.where(inD[:, x], mu[x] * np.expm1(np.minimum(dmin, 700.0)), 0.0)
        # min over y in S of rho[y, x]
        smin = np.min(np.where(inD, rho[:, x][None, :], BIG), axis=1)
        G += mu[x] * np.exp(-np.minimum(smin, 700.0))
    proper = np.ones(nm, dtype=bool)
    proper[0] = False
    proper[nm - 1] = False
    # Xi: sort by measure, prefix maximum
    idx = np.nonzero(proper)[0]
    order = idx[np.argsort(meas[idx], kind='stable')]
    m_sorted = meas[order]
    f_sorted = np.maximum.accumulate(F[order])
    # collapse equal measures (keep the last = the largest prefix maximum)
    keep = np.ones(len(m_sorted), dtype=bool)
    keep[:-1] = m_sorted[1:] > m_sorted[:-1] * (1 + 1e-12) + 1e-300
    bp = np.concatenate((m_sorted[keep], [1.0]))
    val = np.concatenate((f_sorted[keep], [INF]))
    Xi = StepTail(bp, val, zero_below=True)
    # Theta: nonempty S, sorted by measure, suffix minimum;  Theta(p) = min over mu(S) >= p
    idx2 = np.arange(1, nm)
    order2 = idx2[np.argsort(meas[idx2], kind='stable')]
    m2 = meas[order2]
    g2 = np.minimum.accumulate(G[order2][::-1])[::-1]
    # Theta(p) = g2[first index with m2 >= p]
    def Theta(p, m2=m2, g2=g2):
        i = int(np.searchsorted(m2, p * (1 - 1e-12), side='left'))
        return float(g2[min(i, len(g2) - 1)])
    if return_sets:
        return Xi, Theta, dict(meas=meas, F=F, G=G)
    return Xi, Theta


# ----------------------------------------------------------------------------------------------------------------
# constants of Algorithm A
# ----------------------------------------------------------------------------------------------------------------
class Consts:
    """The constants of Algorithm A (N_REPORT 2.2).
       xs = [x_0, ..., x_L] (x_L <= b);  kappa0 = s_0/ell_0;  lnD = ln(V_max/ell_0)  ('cap' termination), or
       lnDA = ln(u_0/ell_0) with A <= u_0 ('unb' termination; then closing is called with thrN = theta nu1);
       closing(thrN, theta, ceta) -> pi_*;  J may be forced (e.g. to the cube's value)."""

    def __init__(self, lam, eta, etap, theta, nu1, b, xs, delta, kappa0, closing, lnD=None, lnDA=None, mode='cap',
                 J=None, pi_star=None, K=None, C=None, C0=1.0, cref=1.0):
        self.lam, self.eta, self.etap, self.theta, self.nu1, self.b, self.delta = lam, eta, etap, theta, nu1, b, delta
        self.xs = np.asarray(xs, dtype=float)
        self.L = len(xs) - 1
        assert self.L >= 1 and np.all(self.xs[:-1] > self.xs[1:]) and self.xs[-1] <= b * (1 + 1e-12)
        self.kappa0, self.mode = kappa0, mode
        assert 0 < kappa0 <= 1 and nu1 >= 1
        self.ceta = (1 - eta) / (1 + eta)
        if mode == 'cap':
            self.J = math.ceil((lnD - math.log(kappa0)) / lam - 1e-12) if J is None else J
            self.nu0 = max((self.J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
            self.pi_star = closing(theta * (1 - eta) * self.nu0, theta, self.ceta) if pi_star is None else pi_star
        else:                                                  # 'unb': no cap on V; termination through the closing level
            self.pi_star = closing(theta * nu1, theta, self.ceta) if pi_star is None else pi_star
            self.J = math.floor((lnDA - math.log(kappa0) + b + lam
                                 + math.log((1 + eta) / ((1 - eta) * self.pi_star))) / lam) if J is None else J
            self.nu0 = max((self.J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
        self.m_max = math.ceil(math.log2(2 * (1 + eta) * math.exp(lam) * self.nu0 / ((1 - eta) * self.pi_star)) - 1e-12)
        self.Nev = (self.J + 1) * (self.m_max + 1) * (self.L + 2)
        self.K = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(2 * self.Nev / delta)) if K is None else K
        self.nu = self.K * self.nu0
        self.Mdag = self.K / ((1 - eta) * self.pi_star)
        self.Mbar = 2 * (1 + eta) * math.exp(lam) * self.nu0 * self.Mdag
        self.deltap = delta / (4 * self.L * self.Mbar)
        self.ratio_bound = kappa0 + math.exp(b) * (math.exp(lam) * (1 + eta) / (1 - eta) + etap + theta)
        self.xout = math.log(self.ratio_bound)
        self.C0, self.cref = C0, cref
        self.C = np.ones(self.L + 1) if C is None else np.asarray(C, dtype=float)      # C[l] for l = 1..L (C[0] unused)

    def cnt(self, x):
        return max(self.K, 2 * (1 + self.eta) ** 2 / (1 - self.eta) * math.exp(self.lam) * self.nu * math.exp(x))

    def Cmax(self):
        tot = self.cref + 2 * self.Mbar * self.C0
        for l in range(1, self.L + 1):
            tot += min(2 * self.Mbar, (self.J + 1) * self.cnt(self.xs[l - 1])) * self.C[l]
        return tot


# ----------------------------------------------------------------------------------------------------------------
# Algorithm A with a simulated bracket oracle
# ----------------------------------------------------------------------------------------------------------------
def _oracle(rng, W, x, s, eb, mode):
    """a valid bracket [lo, lo e^x] around the true values W.  mode 0: random position; 1: value at the top;
    2: value at the bottom; 3: adversarial -- keep the point undecided at the level s if a valid bracket allows it
    (hi > s and lo <= s e^-b), otherwise random."""
    if mode == 1:
        lo = W * math.exp(-x)
    elif mode == 2:
        lo = W.copy()
    else:
        lo = W * np.exp(-x * rng.uniform(size=W.shape))
        if mode == 3:
            # lo in [W e^-x, W] with lo > s e^-x and lo <= s e^-b
            cand = np.minimum(W, s * eb)
            ok = (cand >= W * math.exp(-x)) & (cand > s * math.exp(-x))
            lo = np.where(ok, cand, lo)
    return lo, lo * math.exp(x)


def run_level(rng, draw, C, Xi, ThetaBar, ell0, Vmax=None, oracle_mode=0, max_points=6_000_000, mut=()):
    """Algorithm A.  draw(k) returns the true values V(a) of k fresh independent outer points (law mu_o).
    Vmax: the cap (rule (c0)); None in the 'unb' variant.  mut: mutations for the power of the checks --
       'q_plain'  q = max(N,K)/M (no factor 1/(1-eta));   'no_cap'  rule (c0) switched off.
    Returns a dict (stop reason, bracket, the certificates of every level, counts of calls)."""
    lam, eta, b, K = C.lam, C.eta, C.b, C.K
    xs, Lx = C.xs, C.L
    eb = math.exp(-b)
    s0 = C.kappa0 * ell0
    W = np.zeros(0)
    Lb = np.zeros(0)
    Ub = np.zeros(0)
    rung = np.zeros(0, dtype=np.int16)
    ell = ell0
    Sigma = 0.0
    sumU = 0.0
    levels = []
    calls_tot = np.zeros(Lx + 1, dtype=np.int64)
    res = dict(levels=levels, calls=calls_tot, s0=s0)
    j = 0
    while True:
        s = s0 * math.exp(j * lam)
        if Vmax is not None and 'no_cap' not in mut and s >= Vmax * (1 - 1e-13):
            res.update(stop='cap', level=j, L=max(ell, Sigma), U=s0 + sumU, tail=0.0, npoints=len(W), ell=ell)
            return res
        if j > C.J:
            res.update(stop='abort_levels', level=j, npoints=len(W), ell=ell)
            return res
        ell_in = ell
        Mneg = C.nu * s / (ell_in * math.exp(b))
        M = K
        lev = dict(j=j, s=s, ell_in=ell_in, Mneg=Mneg, calls=np.zeros(Lx + 1, dtype=np.int64), passes=[])
        levels.append(lev)
        while True:
            if M > max_points:
                res.update(stop='too_large', level=j, npoints=len(W), M=M, ell=ell)
                return res
            if len(W) < M:
                extra = M - len(W)
                Wn = np.asarray(draw(extra), dtype=float)
                lo, hi = _oracle(rng, Wn, xs[0], s, eb, 0 if oracle_mode == 3 else oracle_mode)
                W = np.concatenate((W, Wn))
                Lb = np.concatenate((Lb, lo))
                Ub = np.concatenate((Ub, hi))
                rung = np.concatenate((rung, np.zeros(extra, dtype=np.int16)))
            # classify a_1..a_M at level j
            while True:
                idx = np.nonzero((Ub[:M] > s) & (Lb[:M] <= s * eb * (1 - 1e-13)))[0]
                if idx.size == 0:
                    break
                r = rung[idx] + 1
                if np.any(r > Lx):
                    res.update(stop='abort_unclassified', level=j, npoints=len(W), ell=ell)
                    return res
                # all points of idx at the same next rung are refined together
                for rr in np.unique(r):
                    sub = idx[r == rr]
                    lo, hi = _oracle(rng, W[sub], xs[rr], s, eb, oracle_mode)
                    Lb[sub] = np.maximum(Lb[sub], lo)
                    Ub[sub] = np.minimum(Ub[sub], hi)
                    rung[sub] = rr
                    lev['calls'][rr] += sub.size
                    calls_tot[rr] += sub.size
            N = int(np.count_nonzero(Ub[:M] > s))
            if 'q_plain' in mut:
                q = min(1.0, max(N, K) / M)
            else:
                q = min(1.0, max(N, K) / ((1 - eta) * M))
            pop = N >= K
            pbar = N / ((1 + eta) * M) if pop else 0.0
            if pop:
                ell = max(ell, s * eb * ThetaBar(pbar))
            xi = Xi(q)
            tail = s * xi if xi < INF else INF
            pa = dict(M=M, N=N, q=q, pop=pop, pbar=pbar, tail=tail, ell=ell)
            lev['passes'].append(pa)
            if tail <= C.theta * math.exp(b) * ell:
                Lout = max(ell, Sigma + ((1 - math.exp(-lam)) * eb * s * pbar if pop else 0.0))
                res.update(stop='closed', level=j, L=Lout, U=s0 + sumU + tail, tail=tail, npoints=len(W), ell=ell,
                           Sigma=Sigma, W=W, rung=rung)
                lev.update(kind='stop', M=M, q=q, pbar=pbar)
                return res
            if pop:
                lev.update(kind='pop', M=M, q=q, pbar=pbar)
                Sigma += (1 - math.exp(-lam)) * eb * s * pbar
                sumU += (math.exp(lam) - 1) * s * q
                break
            if M >= Mneg:
                lev.update(kind='neg', M=M, q=q, pbar=0.0)
                sumU += (math.exp(lam) - 1) * s * q
                break
            M *= 2
        j += 1


def check_run(res, C, A, pfun, W=None, pbar_fun=None):
    """the inequalities of the proof of Theorem N1 on a run that stopped ('closed' or 'cap').
    A: the true mean; pfun(t) = mu_o(V > t) exactly.  Returns a dict of booleans:
       good     the Chernoff events (V2), (V3) at the passes that occurred ((V1) holds by construction of the oracle)
       valid    L <= A <= U
       width    U <= ratio_bound * L                                  [every run]
       certs    p(s_i) <= q_i at every level, pbar_i <= p(s_i e^-b) at populated ones, ell <= A
       closing  q_j >= pi_* at every level that was left              [every run]
       sizes    M <= max(K, 2 M_j^neg), M_j^neg <= (1+eta) e^lam nu0 M_dagger, M <= Mbar     [every run]
       count    M_j^neg p(s_j e^-x) <= c_eta^-1 e^lam nu e^x for the x of the ladder and x = b
       calls    calls of rung l during level j <= #{i <= M_j : V_i > s_j e^-x_{l-1}} <= cnt(x_{l-1}) (the second on the good event)
       term     stopped at a level <= J
    """
    out = {}
    eta, lam, b, K = C.eta, C.lam, C.b, C.K
    Wv = res.get('W') if W is None else W
    good = True
    certs = True
    closing = True
    sizes = True
    count = True
    calls = True
    tol = 1 + 1e-9
    for lev in res['levels']:
        s = lev['s']
        for pa in lev['passes']:
            M, N, q = pa['M'], pa['N'], pa['q']
            # thresholds are compared with a relative tolerance of 1e-9 in the favourable direction: a flat fibre
            # puts the reference weight exactly on the level grid (the structural tie of K_REPORT, errata (m10), (e2))
            ps = pfun(s * (1 + 1e-9))
            pb = pfun(s * math.exp(-b) * (1 - 1e-9))
            if Wv is not None:
                X_s = int(np.count_nonzero(Wv[:M] > s))
                X_b = int(np.count_nonzero(Wv[:M] > s * math.exp(-b)))
                if not (M * ps <= K / (1 - eta) * tol or X_s >= (1 - eta) * M * ps / tol):
                    good = False
                if not (X_b < K or X_b <= (1 + eta) * M * pb * tol):
                    good = False
            if not ps <= q * tol:
                certs = False
            if pa['pop'] and not pa['pbar'] <= pb * tol:
                certs = False
            if not pa['ell'] <= A * tol:
                certs = False
        kind = lev.get('kind')
        if kind in ('pop', 'neg') and not lev['q'] >= C.pi_star / tol:
            closing = False
        if 'M' in lev:
            Mj = lev['M']
            if not (Mj <= max(K, 2 * lev['Mneg']) * tol and Mj <= C.Mbar * tol):
                sizes = False
            if not lev['Mneg'] <= (1 + eta) * math.exp(lam) * C.nu0 * C.Mdag * tol:
                sizes = False
            for l in range(0, C.L):
                x = C.xs[l]
                t = s * math.exp(-x)
                if not lev['Mneg'] * pfun(t * (1 + 1e-9)) <= math.exp(lam) * C.nu * math.exp(x) / C.ceta * tol:
                    count = False
                if Wv is not None:
                    Xt = int(np.count_nonzero(Wv[:Mj] > t))
                    Xt_tol = int(np.count_nonzero(Wv[:Mj] > t * (1 - 1e-9)))
                    if not (Xt < K or Xt <= (1 + eta) * Mj * pfun(t * (1 - 1e-9)) * tol):
                        good = False
                    if not lev['calls'][l + 1] <= Xt_tol:
                        calls = False
                    if good and not Xt <= C.cnt(x) * tol:
                        calls = False
    out['good'] = good
    out['valid'] = (res['L'] <= A * tol) and (A <= res['U'] * tol)
    out['width'] = res['U'] <= C.ratio_bound * res['L'] * tol
    out['certs'] = certs
    out['closing'] = closing
    out['sizes'] = sizes
    out['count'] = count
    out['calls'] = calls
    out['term'] = res['level'] <= C.J
    return out


# ----------------------------------------------------------------------------------------------------------------
# Gauss space
# ----------------------------------------------------------------------------------------------------------------
def gauss_Xi(L, q):
    """exact upper tail function of the L-Lipschitz class on (R^n, gamma_n), any n:  with t = Phi^-1(1-q),
       Xi_L(q) = int_0^inf L e^{Lr} Phi(-t-r) dr = e^{L^2/2 - L t} Phi(L - t) - Phi(-t)        (+inf at q = 1)"""
    if q >= 1.0:
        return INF
    t = -ndtri(q)
    return math.exp(L * L / 2 - L * t + log_ndtr(L - t)) - q


def gauss_Theta(L, p):
    """exact lower tail function:  with c = Phi^-1(p),  Theta_L(p) = int_0^inf L e^{-Lr} Phi(c+r) dr = p + e^{L c + L^2/2} Phi(-c-L)"""
    if p >= 1.0:
        return 1.0
    if p <= 0.0:
        return 0.0
    c = ndtri(p)
    return p + math.exp(L * c + L * L / 2 + log_ndtr(-c - L))


if __name__ == '__main__':
    # a small self-test: the cube tables against direct sums; the step closing level against the cube's r_dagger
    ok = True
    for (m, u) in [(6, 1.0), (10, 0.5), (12, 2.0)]:
        t = CubeTables(m, u)
        for r in range(m + 1):
            E = sum(math.comb(m, j) * math.expm1(u * (r + 1 - j)) for j in range(r + 1))
            T = sum(math.comb(m, j) * math.exp(-u * max(j - r, 0)) for j in range(m + 1))
            ok &= abs(E - t.E[r]) <= 1e-9 * E and abs(T - t.T[r]) <= 1e-9 * T
        for (theta, nu0, eta) in [(0.3, 50.0, 0.5), (2.0, 400.0, 0.25), (50.0, 3.0, 0.5), (0.05, 5000.0, 0.1), (0.5, 1.2, 0.5)]:
            ceta = (1 - eta) / (1 + eta)
            pid, r = t.pidagger(theta, nu0, eta)
            bp, val = t.steps()
            pis, i = closing_level_steps(bp, val, t.ThetaBar, theta * (1 - eta) * nu0, theta, ceta)
            ref = t.ball[r] / t.N if r >= 0 else 1.0 / t.N
            ok &= abs(pis - ref) <= 1e-12
    print("nlib self-test:", "OK" if ok else "FAILED")
