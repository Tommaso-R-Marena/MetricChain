"""Tilt-state recursion with a CONSERVATIVE discretisation (children's tilts on the grid; feasible region enlarged or shrunk).

State: (previous letter b, tilt lam of the conditional law of the next letter), lam in [-u*, u*].
Children (mu_+, mu_-) of a state lam are feasible iff
    theta_- := lam + A(mu_-) - B(mu_+)  in [-u, u],      theta_+ := theta_- + mu_+ - mu_-  in [-u, u],
    A(m) = ln(p e^m + 1 - p),  B(m) = ln((1-p) e^m + p)        (binary symmetric chain, flip probability p).
Grid mu_k with spacing D.  mode = +1 ("safe"): the feasible region is enlarged by eps = 1.5 D and the stage factors are the
extremes over the cell of lam, so that the grid value bounds the true value of the relaxed problem on the safe side for every lam
of the cell (induction over the levels).  mode = -1: exact region restricted to grid tilts, stage factors at the cell centre (the adversary is restricted: unsafe side).
Renyi (min problem):  W(b,k) = min_{(i,j) feasible} c_+(b,k) W(+,i) + c_-(b,k) W(-,j),  c_a = tau_lam(b,a)^t q(b,a)^(1-t);
    for ANY positive W:  rate <= -ln min_k (TW/W)(k)   (T monotone, positively homogeneous).
KL (max problem, Q = pi):  W(b,k) = k_b(lam) + max sum_a P(b,a) W(a, .);  growth <= max_k (TW - W)(k)."""
import math
import numpy as np

def gfun(x, p): return math.log(((1 - p) * math.exp(x) + p) / (p * math.exp(x) + 1 - p))

class DP3:
    def __init__(self, p, u, G=401, mode=+1):
        self.p, self.u, self.G, self.mode = p, u, G, mode
        us = u
        for _ in range(600): us = u + gfun(us, p)
        self.us = us
        mu = np.linspace(-us, us, G); self.mu = mu; D = mu[1] - mu[0]; self.D = D
        eps = 1.5 * D if mode > 0 else 1e-12
        A = np.log(p * np.exp(mu) + 1 - p); B = np.log((1 - p) * np.exp(mu) + p); Cc = mu - B; Dd = A - mu
        lam = mu[:, None]
        # theta_- in [-u-eps, u+eps]  <=>  B(i) in [lam + A(j) - u - eps, lam + A(j) + u + eps]
        i1 = np.searchsorted(B, (lam + A[None, :] - u - eps).ravel(), "left").reshape(G, G)
        i2 = np.searchsorted(B, (lam + A[None, :] + u + eps).ravel(), "right").reshape(G, G) - 1
        # theta_+ = lam + Dd(j) + Cc(i) in [-u-eps, u+eps]
        i3 = np.searchsorted(Cc, (-u - eps - lam - Dd[None, :]).ravel(), "left").reshape(G, G)
        i4 = np.searchsorted(Cc, (u + eps - lam - Dd[None, :]).ravel(), "right").reshape(G, G) - 1
        lo = np.maximum(i1, i3); hi = np.minimum(i2, i4)
        self.bad = lo > hi
        lo = np.where(self.bad, 0, lo); hi = np.where(self.bad, 0, hi)
        ln = hi - lo + 1
        self.kk = np.floor(np.log2(ln)).astype(int)
        self.lo = lo; self.hi2 = hi - (1 << self.kk) + 1
        self.nlev = int(self.kk.max()) + 1
        self.P = {+1: (1 - p, p), -1: (p, 1 - p)}

    def _rmq(self, W, want_min=True):
        tbl = [W]; op = np.minimum if want_min else np.maximum
        for k in range(1, self.nlev):
            h = 1 << (k - 1); prev = tbl[-1]
            cur = prev.copy(); cur[:len(prev) - h] = op(prev[:len(prev) - h], prev[h:])
            tbl.append(cur)
        T = np.stack(tbl)                                               # levels x G
        return op(T[self.kk, self.lo], T[self.kk, self.hi2])

    def _tilt(self, b, lam):
        Pp, Pm = self.P[b]
        z = Pp * np.exp(lam / 2) + Pm * np.exp(-lam / 2)
        return Pp * np.exp(lam / 2) / z, Pm * np.exp(-lam / 2) / z

    def renyi_rate(self, t, qt, iters=4000, tol=1e-9):
        """returns (-ln max ratio, -ln min ratio); the SECOND number bounds the rate of the discretised problem from above"""
        G, mu, D = self.G, self.mu, self.D
        qq = {+1: (1 - qt, qt), -1: (qt, 1 - qt)}
        st = {}
        for b in (+1, -1):
            if self.mode > 0:      # smallest factors over the cell: tau(+) increases, tau(-) decreases with lam
                cp = self._tilt(b, mu - D / 2)[0] ** t * qq[b][0] ** (1 - t); cm = self._tilt(b, mu + D / 2)[1] ** t * qq[b][1] ** (1 - t)
            else:
                tp, tm = self._tilt(b, mu); cp = tp ** t * qq[b][0] ** (1 - t); cm = tm ** t * qq[b][1] ** (1 - t)
            st[b] = (cp, cm)
        W = {+1: np.ones(G), -1: np.ones(G)}; lo = hi = None
        for it in range(iters):
            inner = np.where(self.bad, np.inf, self._rmq(W[+1], True))          # [k, j]: best mu_+ for the child pair (., j)
            Wn = {}
            for b in (+1, -1):
                cp, cm = st[b]
                Wn[b] = (cp[:, None] * inner + cm[:, None] * W[-1][None, :]).min(axis=1)
            r = np.concatenate([Wn[+1] / W[+1], Wn[-1] / W[-1]])
            lo, hi = float(r.min()), float(r.max())
            s = max(Wn[+1].max(), Wn[-1].max()); W = {b: Wn[b] / s for b in Wn}
            if hi - lo < tol * hi: break
        return -math.log(hi), -math.log(lo)

    def kl_rate(self, iters=6000, tol=1e-10):
        """Q = pi, t -> 0: returns (min, max) of TW - W; the SECOND number bounds the growth of the discretised problem from above"""
        G, mu, D = self.G, self.mu, self.D
        k = {}
        for b in (+1, -1):
            Pp, Pm = self.P[b]
            def kl(lam):
                tp, tm = self._tilt(b, lam); return Pp * np.log(Pp / tp) + Pm * np.log(Pm / tm)
            k[b] = np.maximum(kl(mu - D / 2), kl(mu + D / 2)) if self.mode > 0 else kl(mu)   # convex in lam: max over the cell at its ends
        W = {+1: np.zeros(G), -1: np.zeros(G)}; lo = hi = None
        for it in range(iters):
            inner = np.where(self.bad, -np.inf, self._rmq(W[+1], False))
            Wn = {}
            for b in (+1, -1):
                Pp, Pm = self.P[b]
                Wn[b] = k[b] + (Pp * inner + Pm * W[-1][None, :]).max(axis=1)
            d = np.concatenate([Wn[+1] - W[+1], Wn[-1] - W[-1]])
            lo, hi = float(d.min()), float(d.max())
            m = max(Wn[+1].max(), Wn[-1].max()); W = {b: Wn[b] - m for b in Wn}
            if hi - lo < tol: break
        return lo, hi

    def shannon_rate(self, qt, iters=6000, tol=1e-9):
        """t -> 1: growth of the relaxed maximum of KL(pi_phi || Q_qt); returns (min, max) of TW - W.
        W is kept <= 0, so the smallest transition weights over the cell are on the safe side."""
        G, mu, D = self.G, self.mu, self.D
        qq = {+1: (1 - qt, qt), -1: (qt, 1 - qt)}
        k = {}; wp = {}; wm = {}
        for b in (+1, -1):
            def kl(lam):
                tp, tm = self._tilt(b, lam); return tp * np.log(tp / qq[b][0]) + tm * np.log(tm / qq[b][1])
            if self.mode > 0:
                k[b] = np.maximum(np.maximum(kl(mu - D / 2), kl(mu + D / 2)), kl(mu))      # KL(tilt||q) is convex along the tilt path? take the max of 3 points + slack below
                k[b] = k[b] + 2.0 * D * D                              # slack for the curvature inside the cell
                wp[b] = self._tilt(b, mu - D / 2)[0]; wm[b] = self._tilt(b, mu + D / 2)[1]
            else:
                k[b] = kl(mu); wp[b], wm[b] = self._tilt(b, mu)
        W = {+1: np.zeros(G), -1: np.zeros(G)}; lo = hi = None
        for it in range(iters):
            inner = np.where(self.bad, -np.inf, self._rmq(W[+1], False))
            Wn = {}
            for b in (+1, -1):
                Wn[b] = k[b] + (wp[b][:, None] * inner + wm[b][:, None] * W[-1][None, :]).max(axis=1)
            d = np.concatenate([Wn[+1] - W[+1], Wn[-1] - W[-1]])
            lo, hi = float(d.min()), float(d.max())
            m = max(Wn[+1].max(), Wn[-1].max()); W = {b: Wn[b] - m for b in Wn}
            if hi - lo < tol: break
        return lo, hi
