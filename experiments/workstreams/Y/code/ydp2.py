"""Tilt-state recursion ("DP2"): a relaxation of  max_{phi in C} (1-t) D_t(pi_phi || Q)  for the binary symmetric chain and a
symmetric Markov reference Q (flip probability qt), which keeps the state "tilt of the conditional law".

For phi in C let V_i(x_<=i) = E_pi[e^{-phi} | x_<=i] and lam_i(x_<i) = ln V_i(x_<i,+)/V_i(x_<i,-).  Then
  pi_phi(x_i = . | x_<i) = tilt of P(x_{i-1}, .) by lam_i,     sum_x pi_phi^t Q^(1-t) = sum_x prod_i tau_{lam_i}(x_{i-1},x_i)^t q(x_{i-1},x_i)^(1-t),
and for every prefix there are theta_+, theta_- in [-u, u] with (mu_a := lam_{i+1}(x_<i, a))
  mu_+ = mu_- + theta_+ - theta_-,     lam_i = ln[(1-p) e^{theta_+ + mu_-} + p e^{theta_-}] - ln[p e^{mu_-} + 1 - p],     |lam_n| <= u.
Minimising over ALL tilt processes with these properties (a superset) is a dynamic programme in the state (previous letter, tilt):
  W_i(b, lam) = min_{theta_+-} sum_a tau_lam(b,a)^t q(b,a)^(1-t) W_{i+1}(a, mu_a),     F*_n(t) <= -ln min_lam W_1.
The t -> 0 analogue with Q = pi bounds the threshold: W_i(b,lam) = k_b(lam) + max sum_a P(b,a) W_{i+1}(a, mu_a), k_b = KL(P(b,.)||tilt).
Numerics: tilt grid of size G on [-u*_i, u*_i] (level-dependent for finite chains), control grid C x C including the end points,
linear interpolation in the tilt.  Discretising the controls errs on the unsafe side; convergence in (G, C) must be checked."""
import math
import numpy as np

def gfun(x, p): return math.log(((1 - p) * math.exp(x) + p) / (p * math.exp(x) + 1 - p))

class DP2:
    def __init__(self, p, u, G=301, C=21):
        self.p, self.u, self.G, self.C = p, u, G, C
        us = u
        for _ in range(400): us = u + gfun(us, p)
        self.us = us
        self.th = np.linspace(-u, u, C)
        self.P = {+1: (1 - p, p), -1: (p, 1 - p), 0: (0.5, 0.5)}       # P(b, a) for a = +, -
        self._st = self.maps(np.linspace(-us, us, G), us)

    def maps(self, lam, child_lim):
        """for a tilt grid lam and children restricted to |mu| <= child_lim: feasibility mask and children's tilts"""
        p = self.p
        L = lam[:, None, None]; Tp = self.th[None, :, None]; Tm = self.th[None, None, :]
        num = (1 - p) * np.exp(L) - p * np.exp(Tm); den = (1 - p) * np.exp(Tp) - p * np.exp(L)
        ok = (num > 0) & (den > 0)
        mum = np.where(ok, np.log(np.where(ok, num, 1.0)) - np.log(np.where(ok, den, 1.0)), 0.0) + 0 * Tp
        mup = mum + Tp - Tm
        ok = ok & (np.abs(mup) <= child_lim + 1e-10) & (np.abs(mum) <= child_lim + 1e-10)
        return ok, np.clip(mup, -child_lim, child_lim), np.clip(mum, -child_lim, child_lim)

    @staticmethod
    def interp(W, grid, mu):
        x = (mu - grid[0]) / (grid[-1] - grid[0]) * (len(grid) - 1)
        i = np.clip(np.floor(x).astype(int), 0, len(grid) - 2); f = x - i
        return W[i] * (1 - f) + W[i + 1] * f

    def tilt(self, b, lam):
        Pp, Pm = self.P[b]
        z = Pp * np.exp(lam / 2) + Pm * np.exp(-lam / 2)
        return Pp * np.exp(lam / 2) / z, Pm * np.exp(-lam / 2) / z

    def stage(self, b, lam, t, qt):
        tp, tm = self.tilt(b, lam)
        qq = {+1: (1 - qt, qt), -1: (qt, 1 - qt), 0: (0.5, 0.5)}[b]
        return tp ** t * qq[0] ** (1 - t), tm ** t * qq[1] ** (1 - t)

    def kl_stage(self, b, lam):
        Pp, Pm = self.P[b]; tp, tm = self.tilt(b, lam)
        return Pp * np.log(Pp / tp) + Pm * np.log(Pm / tm)

    def _levels(self, n):
        lims = [self.u]
        for _ in range(n - 1): lims.append(self.u + gfun(lims[-1], self.p))
        return lims[::-1]                                              # lims[i-1] = u*_i

    def renyi_finite(self, n, t, qt):
        """-ln min over the relaxed tilt processes, chain of n sites, stationary start: >= max_phi (1-t) D_t(pi_phi || Q)"""
        lims = self._levels(n)
        grid = np.linspace(-lims[n - 1], lims[n - 1], self.G)
        W = {b: sum(self.stage(b, grid, t, qt)) for b in (+1, -1, 0)}
        for i in range(n - 1, 0, -1):
            g2 = np.linspace(-lims[i - 1], lims[i - 1], self.G)
            ok, mup, mum = self.maps(g2, lims[i])
            Wp = self.interp(W[+1], grid, mup); Wm = self.interp(W[-1], grid, mum)
            Wn = {}
            for b in (+1, -1, 0):
                cp, cm = self.stage(b, g2, t, qt)
                Wn[b] = np.where(ok, cp[:, None, None] * Wp + cm[:, None, None] * Wm, np.inf).reshape(self.G, -1).min(axis=1)
            W, grid = Wn, g2
        return -math.log(float(W[0].min()))

    def _prep(self):
        """interpolation indices/weights and the feasibility penalty for the stationary recursion (computed once)"""
        if hasattr(self, "_pp"): return self._pp
        grid = np.linspace(-self.us, self.us, self.G); ok, mup, mum = self._st
        def idx(mu):
            x = (mu - grid[0]) / (grid[-1] - grid[0]) * (self.G - 1)
            i = np.clip(np.floor(x).astype(int), 0, self.G - 2); return i, x - i
        ip, fp = idx(mup); im, fm = idx(mum)
        self._pp = (grid, ip, fp, im, fm, np.where(ok, 0.0, np.inf))
        return self._pp

    def renyi_rate(self, t, qt, iters=3000, tol=1e-9):
        """per-site rate of the stationary recursion W -> T W (min over controls).  For ANY positive W,
        -ln min(TW/W) >= the rate >= -ln max(TW/W) (T is monotone and positively homogeneous), so the second number returned
        is a valid upper bound for F_inf(t) (up to the discretisation) even without convergence.  Plain power iteration from W = 1:
        min(TW/W) is nondecreasing and max(TW/W) nonincreasing along the iteration."""
        grid, ip, fp, im, fm, pen = self._prep()
        W = {+1: np.ones(self.G), -1: np.ones(self.G)}
        st = {b: self.stage(b, grid, t, qt) for b in (+1, -1)}
        best = None
        for it in range(iters):
            Wp = W[+1][ip] * (1 - fp) + W[+1][ip + 1] * fp; Wm = W[-1][im] * (1 - fm) + W[-1][im + 1] * fm
            Wn = {}
            for b in (+1, -1):
                cp, cm = st[b]
                Wn[b] = (cp[:, None, None] * Wp + cm[:, None, None] * Wm + pen).reshape(self.G, -1).min(axis=1)
            r = np.concatenate([Wn[+1] / W[+1], Wn[-1] / W[-1]])
            lo, hi = float(r.min()), float(r.max())
            if best is None or lo > best[0]: best = (lo, hi)
            if hi - lo < tol * hi: break
            s = max(Wn[+1].max(), Wn[-1].max()); W = {b: Wn[b] / s for b in Wn}   # plain power iteration: min(TW/W) is nondecreasing
        return -math.log(best[1]), -math.log(best[0])

    def shannon_rate(self, qt, iters=6000, tol=1e-9):
        """t -> 1: growth of the relaxed maximum of KL(pi_phi || Q):  W(b,lam) = max [ KL(tau_lam(b,.)||q(b,.)) + sum_a tau_lam(b,a) W(a,mu_a) ].
        For any W, max(TW - W) is an upper bound for the growth (T monotone, T(W+c) = TW + c), hence for a_inf.  Returns (min, max)."""
        grid, ip, fp, im, fm, pen = self._prep()
        W = {+1: np.zeros(self.G), -1: np.zeros(self.G)}; best = None
        tl = {b: self.tilt(b, grid) for b in (+1, -1)}
        qq = {+1: (1 - qt, qt), -1: (qt, 1 - qt)}
        k = {b: tl[b][0] * np.log(tl[b][0] / qq[b][0]) + tl[b][1] * np.log(tl[b][1] / qq[b][1]) for b in (+1, -1)}
        for it in range(iters):
            Wp = W[+1][ip] * (1 - fp) + W[+1][ip + 1] * fp; Wm = W[-1][im] * (1 - fm) + W[-1][im + 1] * fm
            Wn = {}
            for b in (+1, -1):
                Wn[b] = k[b] + (tl[b][0][:, None, None] * Wp + tl[b][1][:, None, None] * Wm - pen).reshape(self.G, -1).max(axis=1)
            d = np.concatenate([Wn[+1] - W[+1], Wn[-1] - W[-1]])
            lo, hi = float(d.min()), float(d.max())
            if best is None or hi < best[1]: best = (lo, hi)
            if hi - lo < tol: break
            m = max(Wn[+1].max(), Wn[-1].max()); W = {b: Wn[b] - m for b in Wn}     # plain iteration: max(TW - W) is nonincreasing
        return best

    def kl_finite(self, n):
        """max over the relaxed tilt processes of KL(pi || pi_phi), chain of n sites: >= max_phi KL(pi || pi_phi) >= E_n"""
        lims = self._levels(n)
        grid = np.linspace(-lims[n - 1], lims[n - 1], self.G)
        W = {b: self.kl_stage(b, grid) for b in (+1, -1, 0)}
        for i in range(n - 1, 0, -1):
            g2 = np.linspace(-lims[i - 1], lims[i - 1], self.G)
            ok, mup, mum = self.maps(g2, lims[i])
            Wp = self.interp(W[+1], grid, mup); Wm = self.interp(W[-1], grid, mum)
            Wn = {}
            for b in (+1, -1, 0):
                Pp, Pm = self.P[b]
                Wn[b] = self.kl_stage(b, g2) + np.where(ok, Pp * Wp + Pm * Wm, -np.inf).reshape(self.G, -1).max(axis=1)
            W, grid = Wn, g2
        return float(W[0].max())

    def kl_rate(self, iters=6000, tol=1e-10):
        """t -> 0 with Q = pi: growth of the relaxed maximum of KL(pi || pi_phi); max(TW - W) is an upper bound for E_inf."""
        grid, ip, fp, im, fm, pen = self._prep()
        W = {+1: np.zeros(self.G), -1: np.zeros(self.G)}; k = {b: self.kl_stage(b, grid) for b in (+1, -1)}; best = None
        for it in range(iters):
            Wp = W[+1][ip] * (1 - fp) + W[+1][ip + 1] * fp; Wm = W[-1][im] * (1 - fm) + W[-1][im + 1] * fm
            Wn = {}
            for b in (+1, -1):
                Pp, Pm = self.P[b]
                Wn[b] = k[b] + (Pp * Wp + Pm * Wm - pen).reshape(self.G, -1).max(axis=1)
            d = np.concatenate([Wn[+1] - W[+1], Wn[-1] - W[-1]])
            lo, hi = float(d.min()), float(d.max())
            if best is None or hi < best[1]: best = (lo, hi)
            if hi - lo < tol: break
            W = {b: 0.5 * (W[b] + Wn[b]) for b in Wn}
            m = max(W[+1].max(), W[-1].max()); W = {b: W[b] - m for b in W}
        return best
