# Referee R9 -- exact finite-n sums on "profile sets" (own code).
# The coordinates are split into G groups of sizes n_1..n_G; a cell is the vector w = (w_1..w_G) of the numbers of
# ones of x in the groups.  A set D that is a union of cells is invariant under the Young subgroup.  For x in a cell w
# and a cell w', the least Hamming distance from x to a point of w' is the l1 distance |w - w'|_1, so for a reference
# psi that depends on the type t = sum w only,
#     min_{y not in D} [u d(x,y) - psi(y)]  =  min_{w' not in D} [u |w - w'|_1 - psi(t')]
# is a separable l1 min-plus transform on the grid of cells (exact, two passes per axis).
import numpy as np
from math import log
from scipy.special import gammaln
from r9lib import Par


def logbinom(n, k):
    return gammaln(n + 1.0) - gammaln(k + 1.0) - gammaln(n - k + 1.0)


def lse(a):
    a = np.asarray(a, dtype=float)
    if a.size == 0:
        return -np.inf
    m = np.max(a)
    if not np.isfinite(m):
        return float(m)
    return float(m + np.log(np.sum(np.exp(a - m))))


def l1_transform(f, u):
    """in place: f(w) <- min_{w'} [f(w') + u |w - w'|_1]"""
    for ax in range(f.ndim):
        g = np.moveaxis(f, ax, 0)        # a view
        L = g.shape[0]
        for i in range(1, L):
            np.minimum(g[i], g[i - 1] + u, out=g[i])
        for i in range(L - 2, -1, -1):
            np.minimum(g[i], g[i + 1] + u, out=g[i])
    return f


class Grid:
    def __init__(self, P, sizes):
        self.P = P
        self.sizes = tuple(int(s) for s in sizes)
        self.n = n = sum(self.sizes)
        G = len(self.sizes)
        self.G = G
        self.shape = tuple(s + 1 for s in self.sizes)
        self.w = []
        logc = 0.0
        t = 0
        for g, s in enumerate(self.sizes):
            sh = [1] * G
            sh[g] = s + 1
            wg = np.arange(s + 1, dtype=float).reshape(sh)
            self.w.append(wg)
            logc = logc + logbinom(s, wg)
            t = t + wg
        self.logc = np.broadcast_to(logc, self.shape).copy()
        self.t = np.broadcast_to(t, self.shape).copy()            # type (number of ones)
        self.ti = self.t.astype(np.int64)
        self.logpi = self.t * log(P.p) + (n - self.t) * log(P.q)  # ln pi(x) for x in the cell
        self.logT = logbinom(n, np.arange(n + 1.0))               # ln |T_t|
        self.logdens = self.logc - self.logT[self.ti]             # ln density of the cell in its type class
        # the reference H
        self.psiH_t = -n * P.v(np.arange(n + 1.0) / n)            # psi_H as a function of the type
        tt = np.arange(n + 1.0)
        self.lnZH = lse(self.logT + tt * log(P.p) + (n - tt) * log(P.q) - self.psiH_t)

    def psi_of(self, kind, g=0.0):
        n = self.n
        if kind == 'H':
            return self.psiH_t
        if kind == 'add':
            return g * np.arange(n + 1.0)
        raise ValueError(kind)

    def lnA(self, psi_t):
        n = self.n
        tt = np.arange(n + 1.0)
        return lse(self.logT + tt * log(self.P.p) + (n - tt) * log(self.P.q) - psi_t)

    def dist_to(self, pattern):
        """Hamming distance of a cell to the centre whose letters are pattern[g] on group g"""
        d = 0.0
        for g, s in enumerate(self.sizes):
            d = d + ((s - self.w[g]) if pattern[g] else self.w[g])
        return np.broadcast_to(d, self.shape).copy()

    def stats(self, D, psi_t=None, want_T=False):
        """for the reference psi (default H) and a union D of cells (boolean array, D != everything, D nonempty):
        returns ln mu(D), ln Phi^+(D), ln Phi(D), ln maxdens(D)."""
        P = self.P
        if psi_t is None:
            psi_t = self.psiH_t
            lnA = self.lnZH
        else:
            lnA = self.lnA(psi_t)
        negpsi = -psi_t[self.ti]
        f = np.where(D, np.inf, negpsi)
        l1_transform(f, P.u)                       # T(w) = min_{w' notin D} [u|w-w'| - psi(t')]
        base = self.logc + self.logpi
        ln_mu = lse((base + negpsi)[D]) - lnA
        slack = (f - negpsi)[D]                    # s(x -> D^c) >= 0
        b = base[D] + negpsi[D]
        ln_phip = lse(b + slack) - lnA
        sl = np.maximum(slack, 0.0)
        with np.errstate(divide='ignore'):
            lg = np.where(sl > 30.0, sl, np.log(np.expm1(np.minimum(sl, 30.0))))   # ln(e^s - 1), stable
        ln_phi = lse(b + lg) - lnA
        # density of D in every type class
        dens = np.zeros(self.n + 1)
        np.add.at(dens, self.ti[D], np.exp(self.logdens[D]))
        with np.errstate(divide='ignore'):
            ln_md = float(np.log(np.max(dens)))      # (-inf if all densities underflow; not used for the exponents)
        if want_T:
            return ln_mu, ln_phip, ln_phi, ln_md, f
        return ln_mu, ln_phip, ln_phi, ln_md

    def density_ball_order(self, pattern):
        """for the centre 'pattern': for every cell the cumulative density (in its type class) of the Hamming ball
        {d(.,s) <= d(cell)} intersected with the type class (shells (t,d) are units).  Returns ln cum (computed in
        log space: no underflow for densities below 1e-308)."""
        d = self.dist_to(pattern).astype(np.int64)
        n = self.n
        key = self.ti * (n + 1) + d
        shell = np.full((n + 1) * (n + 1), -np.inf)
        np.logaddexp.at(shell, key.ravel(), self.logdens.ravel())
        shell = shell.reshape(n + 1, n + 1)
        cum = np.logaddexp.accumulate(shell, axis=1)
        return cum[self.ti, d], d
