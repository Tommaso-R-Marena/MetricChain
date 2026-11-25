"""Workstream T -- exact finite-n sums on k-block profile grids (k >= 2).

The coordinates are partitioned into k blocks of sizes n_1..n_k; a point x has the block profile (i_1..i_k),
i_j = number of ones in block j; the class has prod C(n_j, i_j) points, type t = sum i_j, and the Hamming distance
between a point of class i and the nearest point of class i' is sum |i_j - i'_j|.
(A binary centre s of type k is the case of two blocks: the ones of s and the zeros of s.)
Checked against brute force in t08_families.py (n <= 12).
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp


def lbinom(n, k):
    return gammaln(n + 1.0) - gammaln(k + 1.0) - gammaln(n - k + 1.0)


class KFin:
    def __init__(self, sizes, phi, u):
        self.sizes = tuple(int(s) for s in sizes)
        self.k = len(self.sizes)
        self.n = n = sum(self.sizes)
        self.u = float(u)
        grids = np.meshgrid(*[np.arange(s + 1) for s in self.sizes], indexing="ij")
        self.idx = grids
        self.t = sum(grids)
        tt = np.arange(n + 1)
        self.lCn = lbinom(n, tt)
        logw = self.lCn - n * phi(tt / n)
        self.J = -(logw - float(logsumexp(logw)))
        self.lcnt = sum(lbinom(s, g) for s, g in zip(self.sizes, grids))
        self.ldens = self.lcnt - self.lCn[self.t]
        v = self.J.copy()
        for t in range(1, n + 1):
            v[t] = min(v[t], v[t - 1] + self.u)
        for t in range(n - 1, -1, -1):
            v[t] = min(v[t], v[t + 1] + self.u)
        self.Vn = v

    def transform(self, mask, Lam):
        """T = min over classes outside `mask` of [u * l1-distance + Lam(type)]"""
        u = self.u
        T = np.where(mask, np.inf, Lam[self.t])
        for ax in range(self.k):
            T = np.moveaxis(T, ax, 0)
            for a in range(1, T.shape[0]):
                np.minimum(T[a], T[a - 1] + u, out=T[a])
            for a in range(T.shape[0] - 2, -1, -1):
                np.minimum(T[a], T[a + 1] + u, out=T[a])
            T = np.moveaxis(T, 0, ax)
        return T

    def dist_to(self, mask):
        """l1 distance (in flips) from every class to the union of the classes in `mask`"""
        T = np.where(mask, 0.0, np.inf)
        for ax in range(self.k):
            T = np.moveaxis(T, ax, 0)
            for a in range(1, T.shape[0]):
                np.minimum(T[a], T[a - 1] + 1.0, out=T[a])
            for a in range(T.shape[0] - 2, -1, -1):
                np.minimum(T[a], T[a + 1] + 1.0, out=T[a])
            T = np.moveaxis(T, 0, ax)
        return T

    def dip(self, mask, Lam):
        """(ln Phi+(D), ln mu(D), ln Phi(D), maxdens(D)) for the union D of the classes in `mask` (instance landscape Lam)"""
        lZ = float(logsumexp(-self.J + Lam))
        T = self.transform(mask, Lam)
        base = (self.ldens - self.J[self.t])[mask]
        LamD = Lam[self.t][mask]
        lPhiP = float(logsumexp(base + T[mask])) - lZ
        lmu = float(logsumexp(base + LamD)) - lZ
        s = T[mask] - LamD
        with np.errstate(divide="ignore"):
            lexpm1 = np.where(s > 1e-300, s + np.log(-np.expm1(-np.maximum(s, 1e-300))), -np.inf)
        lPhi = float(logsumexp(base + LamD + lexpm1)) - lZ
        dens = np.bincount(self.t[mask].ravel(), weights=np.exp(self.ldens[mask]).ravel(), minlength=self.n + 1)
        return lPhiP, lmu, lPhi, float(dens.max())
