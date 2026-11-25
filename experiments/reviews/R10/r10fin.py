"""
r10fin.py -- referee R10, exact finite-n sums (own code).

Blocks of sizes n_1..n_k (a Young subgroup).  A cell = vector of counts (i_1..i_k), i_j = number
of ones in block j; multiplicity prod C(n_j, i_j); type t = sum i_j; the Hamming distance from a
point of one cell to the nearest point of another cell is the l1 distance of the count vectors.

Exchangeable pi: p_t = C(n,t) exp(-n phi(t/n)) / Z_n,  J_t = -ln p_t,  V_n = largest u-Lipschitz
minorant of J on the lattice.  Symmetric instance with exit landscape Lam (u-Lipschitz, Lam <= J
with equality somewhere):  for a union D of cells

   Phi+(D) = Z^{-1} sum_{c in D} pi(c) exp( min_{c' not in D} [u*l1(c,c') + Lam(t')] ),   Z = sum_t exp(-J_t + Lam_t),
   mu(D)   = Z^{-1} sum_{c in D} pi(c) exp(Lam(t_c)),      Phi = Phi+ - mu.

Brute force on the full cube (n <= 12) is in `Brute`.
"""
import numpy as np
from scipy.special import gammaln, logsumexp


def lbinom(n, k):
    return gammaln(n + 1.0) - gammaln(k + 1.0) - gammaln(n - k + 1.0)


def lip_minorant(J, u):
    v = np.array(J, dtype=float)
    for t in range(1, len(v)):
        v[t] = min(v[t], v[t - 1] + u)
    for t in range(len(v) - 2, -1, -1):
        v[t] = min(v[t], v[t + 1] + u)
    return v


def exchangeable(n, phi):
    """returns J_t = -ln p_t for p_t prop. to C(n,t) exp(-n phi(t/n))"""
    t = np.arange(n + 1)
    lw = lbinom(n, t) - n * phi(t / n)
    return -(lw - logsumexp(lw))


class FinBlocks:
    def __init__(self, sizes, phi, u, J=None):
        self.sizes = tuple(int(s) for s in sizes)
        self.k = len(self.sizes)
        self.n = n = sum(self.sizes)
        self.u = float(u)
        self.J = exchangeable(n, phi) if J is None else np.asarray(J, float)
        self.Vn = lip_minorant(self.J, self.u)
        self.cnt = np.meshgrid(*[np.arange(s + 1) for s in self.sizes], indexing='ij')
        self.t = sum(self.cnt)
        self.lmult = sum(lbinom(s, c) for s, c in zip(self.sizes, self.cnt))
        self.lCn = lbinom(n, np.arange(n + 1))
        self.ldens = self.lmult - self.lCn[self.t]
        self.lpi = self.ldens - self.J[self.t]          # ln pi(cell)

    def transform(self, F):
        """min over cells c' of [F(c') + u * l1(c, c')]  (sequential 1-d passes, exact for l1)"""
        F = np.array(F, dtype=float)
        u = self.u
        for ax in range(self.k):
            F = np.moveaxis(F, ax, 0)
            for i in range(1, F.shape[0]):
                np.minimum(F[i], F[i - 1] + u, out=F[i])
            for i in range(F.shape[0] - 2, -1, -1):
                np.minimum(F[i], F[i + 1] + u, out=F[i])
            F = np.moveaxis(F, 0, ax)
        return F

    def dip(self, mask, Lam):
        """mask: boolean array over cells (the set D, a proper nonempty subset).
        returns dict with ln Phi+, ln mu, ln Phi, maxdens, ln(1+Phi)"""
        Lam = np.asarray(Lam, float)
        lZ = float(logsumexp(-self.J + Lam))
        out = np.where(mask, np.inf, Lam[self.t])
        T = self.transform(out)
        lPhiP = float(logsumexp((self.lpi + T)[mask])) - lZ
        lmu = float(logsumexp((self.lpi + Lam[self.t])[mask])) - lZ
        d = lmu - lPhiP
        lPhi = lPhiP + np.log1p(-np.exp(d)) if d < 0 else -np.inf
        dens = np.bincount(self.t[mask].ravel(), weights=np.exp(self.ldens[mask]).ravel(),
                           minlength=self.n + 1)
        # per-type log densities, robust against underflow
        if dens.max() <= 0:
            md = 0.0
        else:
            md = float(dens.max())
        return dict(lPhiP=lPhiP, lmu=lmu, lPhi=float(lPhi), maxdens=md,
                    eff=float(np.logaddexp(0.0, lPhi)), lZ=lZ)

    def lmaxdens(self, mask):
        """ln of the largest type-wise density of the union of cells (log-domain, no underflow)"""
        best = -np.inf
        tt = self.t[mask].ravel()
        ld = self.ldens[mask].ravel()
        order = np.argsort(tt, kind='stable')
        tt, ld = tt[order], ld[order]
        starts = np.nonzero(np.r_[True, tt[1:] != tt[:-1]])[0]
        ends = np.r_[starts[1:], len(tt)]
        for a, b in zip(starts, ends):
            best = max(best, float(logsumexp(ld[a:b])))
        return best


class Brute:
    """full cube, n <= 12"""

    def __init__(self, n, J, u):
        self.n, self.u = n, float(u)
        N = 1 << n
        self.pts = np.arange(N)
        self.wt = np.array([bin(x).count('1') for x in range(N)])
        self.J = np.asarray(J, float)
        self.lpi = -self.J[self.wt] - lbinom(n, self.wt)
        self.pi = np.exp(self.lpi)
        x = self.pts[:, None] ^ self.pts[None, :]
        pc = np.zeros_like(x)
        for b in range(n):
            pc += (x >> b) & 1
        self.d = pc

    def A(self, psi):
        return float(np.sum(self.pi * np.exp(-psi)))

    def is_lip(self, psi, tol=1e-12):
        return bool(np.all(np.abs(psi[:, None] - psi[None, :]) <= self.u * self.d + tol))

    def dip(self, psi, mask):
        """deepest dip of psi on the set D = mask: max_{y not in D}[psi(y) - u d(x,y)] on D"""
        out = np.where(mask, -np.inf, psi)
        low = np.max(out[None, :] - self.u * self.d, axis=1)
        return np.where(mask, low, psi)

    def phi(self, psi, mask):
        """Phi(D), Phi+(D), mu(D) for the instance psi (direct definition with slack)"""
        w = self.pi * np.exp(-psi)
        A = w.sum()
        mu = w / A
        s = self.u * self.d + psi[:, None] - psi[None, :]
        s_out = np.min(np.where(mask[None, :], np.inf, s), axis=1)
        PhiP = float(np.sum(mu[mask] * np.exp(s_out[mask])))
        return PhiP - float(mu[mask].sum()), PhiP, float(mu[mask].sum())

    def maxdens(self, mask):
        cnt = np.bincount(self.wt[mask], minlength=self.n + 1)
        tot = np.bincount(self.wt, minlength=self.n + 1)
        return float(np.max(cnt / tot))
