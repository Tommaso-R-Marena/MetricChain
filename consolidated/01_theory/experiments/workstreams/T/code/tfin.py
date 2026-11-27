"""Workstream T -- exact finite-n sums on the profile grid around a centre s of type k (hypergeometric counts in logs).

A point x has the profile (i, j): i = #{l : s_l = 1, x_l = 0}, j = #{l : s_l = 0, x_l = 1};  the class has
C(k,i) C(n-k,j) points, type t = k - i + j, distance i + j from s, and the Hamming distance between a point of class
(i,j) and the nearest point of class (i',j') is |i-i'| + |j-j'|.
Known part: pi(x) = p_t / C(n,t), p_t = C(n,t) exp(-n phi(t/n)) / Z_n  (uniform on type classes).   J_t = -ln p_t.
Symmetric instance = a lattice function Lam(t) (exit landscape, u-Lipschitz minorant of J up to a constant):
   flat-histogram instance H:  Lam = V_n := largest u-Lipschitz minorant of J  (psi_H(x) = -V_n(|x|) is in L_u);
   zero residual: Lam = 0;   additive instance gamma|x|:  Lam(t) = -gamma t.
Then mu_chi(class) = exp(ldens - J_t + Lam(t)) / Z_chi,  Z_chi = sum_t exp(-J_t + Lam(t)),  and for a union D of classes
   Phi+_chi(D) = sum_{classes in D} exp(ldens - J_t + T(i,j)) / Z_chi,   T = min over classes outside D of [u*l1-distance + Lam(t')].
Everything is checked against brute force on full cubes (t05_bruteforce.py).
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp


def lbinom(n, k):
    return gammaln(n + 1.0) - gammaln(k + 1.0) - gammaln(n - k + 1.0)


def _cumsum_groups(d, starts, exclusive=False):
    """cumulative sums restarted at every group start (a global cumsum minus offsets would lose the small partial
    sums: absolute error 1e-16 * (number of groups), fatal for caps q = e^{-n theta})"""
    out = np.empty_like(d)
    ends = np.r_[starts[1:], len(d)]
    for a, b in zip(starts, ends):
        c = np.cumsum(d[a:b])
        if exclusive:
            out[a] = 0.0
            out[a + 1:b] = c[:-1]
        else:
            out[a:b] = c
    return out


class Fin:
    def __init__(self, n, k, phi, u):
        """n sites, centre of type k (k ones); phi: function of kappa (vectorised); u: Lipschitz constant per flip"""
        self.n, self.k, self.u = n, k, float(u)
        i = np.arange(k + 1)[:, None]
        j = np.arange(n - k + 1)[None, :]
        self.i, self.j = i, j
        self.t = (k - i + j)                                       # type of the class, shape (k+1, n-k+1)
        tt = np.arange(n + 1)
        self.lCn = lbinom(n, tt)
        logw = self.lCn - n * phi(tt / n)
        self.lZn = float(logsumexp(logw))
        self.J = -(logw - self.lZn)                                # J_t = -ln pi(T_t)
        self.lcnt = lbinom(k, i) + lbinom(n - k, j)
        self.ldens = self.lcnt - self.lCn[self.t]                  # ln (density of the class in its type class)
        self.Vn = self.lip_minorant(self.J)
        self.component = (i * (n - k) + j * k) < k * (n - k)       # a + b < 1 : the side of the centre s

    def lip_minorant(self, J):
        v = J.copy()
        for t in range(1, len(v)):
            v[t] = min(v[t], v[t - 1] + self.u)
        for t in range(len(v) - 2, -1, -1):
            v[t] = min(v[t], v[t + 1] + self.u)
        return v

    # ---- dips of a symmetric instance ---------------------------------------------------------------------------
    def transform(self, mask, Lam):
        """T(i,j) = min over classes (i',j') outside `mask` of [u(|i-i'|+|j-j'|) + Lam(t(i',j'))]   (l1 distance transform)"""
        u = self.u
        T = np.where(mask, np.inf, Lam[self.t])
        for a in range(1, T.shape[0]):
            np.minimum(T[a], T[a - 1] + u, out=T[a])
        for a in range(T.shape[0] - 2, -1, -1):
            np.minimum(T[a], T[a + 1] + u, out=T[a])
        for b in range(1, T.shape[1]):
            np.minimum(T[:, b], T[:, b - 1] + u, out=T[:, b])
        for b in range(T.shape[1] - 2, -1, -1):
            np.minimum(T[:, b], T[:, b + 1] + u, out=T[:, b])
        return T

    def dip(self, mask, Lam):
        """returns (ln Phi+(D), ln mu(D), ln Phi(D), maxdens(D)) for the union D of the classes in `mask`"""
        lZ = float(logsumexp(-self.J + Lam))
        T = self.transform(mask, Lam)
        base = (self.ldens - self.J[self.t])[mask]
        lPhiP = float(logsumexp(base + T[mask])) - lZ
        lmu = float(logsumexp(base + Lam[self.t][mask])) - lZ
        # Phi = Phi+ - mu(D) = sum mu (e^s - 1), computed term by term to avoid cancellation
        s = T[mask] - Lam[self.t][mask]                                           # slack to the complement, >= 0
        with np.errstate(divide="ignore"):
            lexpm1 = np.where(s > 1e-300, s + np.log(-np.expm1(-np.maximum(s, 1e-300))), -np.inf)   # ln(e^s - 1)
        lPhi = float(logsumexp(base + Lam[self.t][mask] + lexpm1)) - lZ
        dens = np.bincount(self.t[mask], weights=np.exp(self.ldens[mask]), minlength=self.n + 1)
        return lPhiP, lmu, lPhi, float(dens.max())

    def capped_family(self, region=None):
        """prepare the density-capped sets D_q: in every type class the rarest classes (inside `region`) are taken as
        long as their cumulative density stays <= q.  Returns a function q -> mask."""
        if region is None:
            region = self.component
        idx = np.nonzero(region.ravel())[0]
        t = self.t.ravel()[idx]
        ld = self.ldens.ravel()[idx]
        order = np.lexsort((ld, t))                               # by type, then by density ascending
        idx, t, ld = idx[order], t[order], ld[order]
        d = np.exp(ld)
        starts = np.nonzero(np.r_[True, t[1:] != t[:-1]])[0]
        cumt = _cumsum_groups(d, starts)                           # cumulative density within the type class (inclusive)
        shape = self.t.shape

        def mask_of(q):
            m = np.zeros(shape[0] * shape[1], dtype=bool)
            m[idx[cumt <= q]] = True
            return m.reshape(shape)
        return mask_of

    def best_dip_exponent(self, eps, Lam, region=None, iters=40):
        """smallest cap q such that the deepest dip on D_q changes ln A by more than eps (ln(1+Phi) > eps);
        returns (theta = -ln(maxdens)/n, ln(1+Phi)/n, q) -- a certified lower bound (1-2 delta)/maxdens on the cost."""
        mask_of = self.capped_family(region)
        lo, hi = -self.n * math.log(2.0) - 5.0, 0.0                # ln q: lo insensitive, hi sensitive
        def sens(lq):
            m = mask_of(math.exp(lq))
            if not m.any():
                return False, None
            lPhiP, lmu, lPhi, md = self.dip(m, Lam)
            eff = np.logaddexp(0.0, lPhi)                           # ln(1 + Phi)
            return eff > eps, (md, eff)
        ok, info = sens(hi - 1e-9)
        if not ok:
            return None
        best = info
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            ok, info = sens(mid)
            if ok:
                hi, best = mid, info
            else:
                lo = mid
        md, eff = best
        return -math.log(md) / self.n, eff / self.n, math.exp(hi)

    # ---- non-adaptive: a shell-cone truncated at type-wise quantiles ------------------------------------------------
    def shell_cone(self, i0, j0):
        """prepare psi = u * d(x, class (i0,j0)) = u(|i-i0| + |j-j0|);  returns q -> ln[A(psi)/A(psi^{tr,q})]"""
        n, u = self.n, self.u
        L = (np.abs(self.i - i0) + np.abs(self.j - j0)).ravel()
        t = self.t.ravel()
        ld = self.ldens.ravel()
        order = np.lexsort((L, t))
        Ls, ts, lds = L[order], t[order], ld[order]
        d = np.exp(lds)
        starts = np.nonzero(np.r_[True, ts[1:] != ts[:-1]])[0]
        cb = _cumsum_groups(d, starts, exclusive=True)             # density of the classes before this one in its type
        # classes with the same (t, L) form one level of psi in the type class: all get the value of the first of the group
        gstart = np.nonzero(np.r_[True, (ts[1:] != ts[:-1]) | (Ls[1:] != Ls[:-1])])[0]
        cb = np.repeat(cb[gstart], np.diff(np.r_[gstart, len(ts)]))
        cb = np.maximum(cb, 0.0)
        base = lds - self.J[ts]
        lA = float(logsumexp(base - u * Ls))

        def ratio(q):
            Lq = np.where(cb <= q * (1.0 + 1e-10), Ls, -1)        # (tolerance: cumulative densities are floating sums)
            Lstar = np.maximum.reduceat(Lq, starts)                # per type: largest level with dens{psi < level} <= q
            Lst = np.repeat(Lstar, np.diff(np.r_[starts, len(ts)]))
            lAtr = float(logsumexp(base - u * np.maximum(Ls, Lst)))
            return lA - lAtr
        return ratio

    def best_na_exponent(self, eps, i0, j0, iters=40):
        """smallest q with ln[A(psi)/A(psi^{tr,q})] > eps for the shell-cone around the class (i0,j0);
        returns (theta = ln(1/q)/n, ratio/n): every non-adaptive algorithm needs (1-2 delta)/q evaluations."""
        ratio = self.shell_cone(i0, j0)
        lo, hi = -self.n * math.log(2.0) - 5.0, 0.0                # ln q
        if not ratio(1.0 - 1e-12) > eps:
            return None
        r_hi = ratio(1.0 - 1e-12)
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            r = ratio(math.exp(mid))
            if r > eps:
                hi, r_hi = mid, r
            else:
                lo = mid
        return -hi / self.n, r_hi / self.n
