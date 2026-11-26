"""r10_tilt.py: the tilt-state recursion (Proposition G of Y_REPORT 5.2), re-derived in
R10_REPORT section 2 and implemented from scratch with a CELL-BASED discretisation whose
safety does not rest on a Lipschitz slack but on exact monotonicity.

Binary symmetric chain, flip probability p, Hamming slope u.  For a class member phi,
V_i(x_{<=i}) = E_pi[e^{-phi} | x_{<=i}],  lambda_i(x_{<i}) = ln V_i(x_{<i},+)/V_i(x_{<i},-),
the conditional law of x_i under pi_phi is tau_lambda(b,.) prop. P(b,.) e^{+-lambda/2}
(b = x_{i-1}), |lambda_i| <= u*, and with mu_a = lambda_{i+1}(x_{<i}, a):

    theta_-(lam,mu+,mu-) := lam + ln(p e^{mu-} + 1-p) - ln((1-p) e^{mu+} + p)       in [-u, u]
    theta_+(lam,mu+,mu-) := lam + ln(p + (1-p) e^{-mu-}) - ln(1-p + p e^{-mu+})     in [-u, u]

(this is (*) of Proposition G solved for theta_+-).  theta_- is increasing in lam and mu-,
decreasing in mu+;  theta_+ is increasing in lam and mu+, decreasing in mu-.  Hence over a
box of cells the ranges of theta_+- are attained at corners, and "the box contains a
feasible point" implies four explicit inequalities for the cell ends.  Using these
(necessary) inequalities as the feasibility test ENLARGES the adversary's choices: every
value computed in `safe` mode bounds the relaxed value on the safe side.

State: (previous letter b, tilt lam); by the global flip symmetry W(-,lam) = W(+,-lam), so
only w[k] ~ W(+, cell k) is stored on a symmetric uniform grid of G cells over [-u*, u*].
"""
import numpy as np


def ustar(p, u, iters=20000):
    x = u
    for _ in range(iters):
        x = u + np.log(((1 - p) * np.exp(x) + p) / (p * np.exp(x) + 1 - p))
    return x


class Tilt:
    def __init__(self, p, u, G, mode="safe", lam_max=None):
        self.p, self.u, self.G, self.mode = p, u, G, mode
        self.us = ustar(p, u) if lam_max is None else lam_max
        us = self.us
        self.edges = np.linspace(-us, us, G + 1)
        self.mid = 0.5 * (self.edges[1:] + self.edges[:-1])
        if mode == "safe":
            lamL, lamR = self.edges[:-1], self.edges[1:]          # cell ends of lambda
            mmL, mmR = self.edges[:-1], self.edges[1:]            # cell ends of mu-
            cellL, cellR = self.edges[:-1], self.edges[1:]        # cell ends of mu+
        else:                                                      # restricted: nodes = cell midpoints
            lamL = lamR = self.mid
            mmL = mmR = self.mid
            cellL = cellR = self.mid
        LamL, MmL = np.meshgrid(lamL, mmL, indexing="ij")
        LamR, MmR = np.meshgrid(lamR, mmR, indexing="ij")
        with np.errstate(divide="ignore", invalid="ignore"):
            # (1) theta_- min <= u   ->  mu+ (right end) >= a1(lamL, mmL)
            arg = (np.exp(LamL - u) * (p * np.exp(MmL) + 1 - p) - p) / (1 - p)
            a1 = np.where(arg > 0, np.log(np.maximum(arg, 1e-300)), -np.inf)
            # (2) theta_- max >= -u  ->  mu+ (left end) <= b2(lamR, mmR)
            arg = (np.exp(LamR + u) * (p * np.exp(MmR) + 1 - p) - p) / (1 - p)
            b2 = np.where(arg > 0, np.log(np.maximum(arg, 1e-300)), -np.inf)
            # (3) theta_+ min <= u   ->  mu+ (left end) <= b3(lamL, mmR)
            arg = (np.exp(LamL - u) * (p + (1 - p) * np.exp(-MmR)) - (1 - p)) / p
            b3 = np.where(arg > 0, -np.log(np.maximum(arg, 1e-300)), np.inf)
            # (4) theta_+ max >= -u  ->  mu+ (right end) >= a4(lamR, mmL)
            arg = (np.exp(LamR + u) * (p + (1 - p) * np.exp(-MmL)) - (1 - p)) / p
            a4 = np.where(arg > 0, -np.log(np.maximum(arg, 1e-300)), np.inf)
        lower = np.maximum(a1, a4)
        upper = np.minimum(b2, b3)
        # smallest j with cellR[j] >= lower ; largest j with cellL[j] <= upper
        jlo = np.searchsorted(cellR, lower.ravel(), side="left").reshape(G, G)
        jhi = (np.searchsorted(cellL, upper.ravel(), side="right") - 1).reshape(G, G)
        self.valid = (jlo <= jhi) & (jlo <= G - 1) & (jhi >= 0)
        jlo = np.clip(jlo, 0, G - 1)
        jhi = np.clip(jhi, 0, G - 1)
        ln = np.where(self.valid, jhi - jlo + 1, 1)
        lev = np.floor(np.log2(ln)).astype(np.int64)
        self.nlev = int(lev.max()) + 1
        self.I1 = (lev * G + jlo).astype(np.int32)
        self.I2 = (lev * G + jhi - (1 << lev) + 1).astype(np.int32)
        self.jlo, self.jhi = jlo, jhi
        # stage quantities
        if mode == "safe":
            self.lam_a, self.lam_b = self.edges[:-1], self.edges[1:]
        else:
            self.lam_a = self.lam_b = self.mid

    # ---------------------------------------------------------------- helpers
    def tau_plus(self, lam):
        p = self.p
        return (1 - p) * np.exp(lam / 2) / ((1 - p) * np.exp(lam / 2) + p * np.exp(-lam / 2))

    def _range_min(self, w):
        G = self.G
        st = np.empty((self.nlev, G))
        st[0] = w
        for l in range(1, self.nlev):
            half = 1 << (l - 1)
            st[l] = st[l - 1]
            st[l, : G - half] = np.minimum(st[l - 1, : G - half], st[l - 1, half:])
        flat = st.ravel()
        return np.minimum(flat[self.I1], flat[self.I2])

    def n_feasible(self):
        return int(self.valid.sum())

    # ---------------------------------------------------------------- (R) Renyi form
    def renyi_stage(self, t, qt):
        """alpha_+(k), alpha_-(k): lower bounds over the cell of tau^t q^(1-t)."""
        tp_min = self.tau_plus(self.lam_a)          # tau(+,+) is increasing in lambda
        tm_min = 1 - self.tau_plus(self.lam_b)      # tau(+,-) is decreasing
        return tp_min ** t * (1 - qt) ** (1 - t), tm_min ** t * qt ** (1 - t)

    def renyi_apply(self, w, ap, am):
        R = self._range_min(w)
        R = np.where(self.valid, R, np.inf)
        wt = w[::-1]                                 # W(-, cell j) = w[G-1-j]
        return (ap[:, None] * R + am[:, None] * wt[None, :]).min(axis=1)

    def renyi_rate(self, t, qt, sweeps=400, tol=1e-10, w=None, verbose=False):
        """Returns (-ln min_k (T w / w), -ln max_k (T w / w), w).
        safe mode:       F_inf(t) <= first value            (for ANY positive w)
        restricted mode: relaxed value >= second value      (for ANY positive w)"""
        ap, am = self.renyi_stage(t, qt)
        if w is None:
            w = np.ones(self.G)
        best = None
        for it in range(sweeps):
            Tw = self.renyi_apply(w, ap, am)
            fin = np.isfinite(Tw)
            if not fin.all():
                # states with an empty feasible set cannot occur: keep them out of the ratio
                Tw = np.where(fin, Tw, w * 1e30)
            ratio = Tw / w
            lo, hi = ratio[fin].min(), ratio[fin].max()
            best = (-np.log(lo), -np.log(hi))
            if verbose and it % 50 == 0:
                print("   sweep %d: [%.8f, %.8f]" % (it, best[1], best[0]))
            if hi - lo < tol * hi:
                break
            w = np.where(fin, Tw, w)
            w = w / w[fin].max()
        return best[0], best[1], w

    # ---------------------------------------------------------------- (E) threshold, reference Markov(qt)
    def kl_q_tau(self, lam, qt):
        tp = self.tau_plus(lam)
        return (1 - qt) * np.log((1 - qt) / tp) + qt * np.log(qt / (1 - tp))

    def thr_rate(self, qt=None, sweeps=2000, tol=1e-10, w=None):
        """Growth of W -> KL(q(b,.)||tau_lam(b,.)) + max sum_a q(b,a) W(a, mu_a).
        safe: E_inf <= first value;  restricted: relaxed value >= second value."""
        qt = self.p if qt is None else qt
        rew = np.maximum(self.kl_q_tau(self.lam_a, qt), self.kl_q_tau(self.lam_b, qt))  # convex in lambda
        if w is None:
            w = np.zeros(self.G)
        best = None
        for it in range(sweeps):
            R = -self._range_min(-w)                 # range max
            R = np.where(self.valid, R, -np.inf)
            wt = w[::-1]
            Tw = rew + ((1 - qt) * R + qt * wt[None, :]).max(axis=1)
            fin = np.isfinite(Tw)
            d = (Tw - w)[fin]
            best = (d.max(), d.min())
            if d.max() - d.min() < tol:
                break
            w = np.where(fin, Tw, w)
            w = w - w[fin].max()
        return best[0], best[1], w

    # ---------------------------------------------------------------- (A) capacity, reference Markov(qt)
    def kl_tau_q(self, lam, qt):
        tp = self.tau_plus(lam)
        return tp * np.log(tp / (1 - qt)) + (1 - tp) * np.log((1 - tp) / qt)

    def cap_rate(self, qt, sweeps=2000, tol=1e-10, w=None):
        """Growth of W -> KL(tau_lam(b,.)||q(b,.)) + max sum_a tau_lam(b,a) W(a, mu_a).
        safe: a_inf <= first value (W normalised <= 0, transition weights = minima over the cell,
        reward = max over the cell, attained at a cell end because KL(tau||q) is convex in tau(+)
        and tau(+) is monotone in lambda);  restricted: relaxed value >= second value."""
        rew = np.maximum(self.kl_tau_q(self.lam_a, qt), self.kl_tau_q(self.lam_b, qt))
        if self.mode == "safe":
            tp = self.tau_plus(self.lam_a)           # min of tau(+,+) over the cell
            tm = 1 - self.tau_plus(self.lam_b)       # min of tau(+,-) over the cell
        else:
            tp = self.tau_plus(self.mid)
            tm = 1 - tp
        if w is None:
            w = np.zeros(self.G)
        best = None
        for it in range(sweeps):
            w = w - w.max()                          # normalised <= 0
            R = -self._range_min(-w)
            R = np.where(self.valid, R, -np.inf)
            wt = w[::-1]
            Tw = rew + (tp[:, None] * R + tm[:, None] * wt[None, :]).max(axis=1)
            fin = np.isfinite(Tw)
            d = (Tw - w)[fin]
            best = (d.max(), d.min())
            if d.max() - d.min() < tol:
                break
            w = np.where(fin, Tw, w)
        return best[0], best[1], w
