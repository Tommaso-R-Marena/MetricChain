"""
r6lib.py -- workstream R6 (science division): an independent implementation of
  * Algorithm 2L   (theory report 5ed4072, section 11.18, Theorem 11.52, text lines 3616-3652)
  * Algorithm 2L+  (K_REPORT.md section 2.2, Theorem K1 = Theorem 11.56)
written from the specification only (no code of the theory division, of its referees or of the
engineering division was read before this file was written).

Design
------
The outer sample a_1, a_2, ... is held as "units".  A unit is a set of `cnt` outer points that share
(i) the block in which they were drawn (block 0 = points 1..K, block t>=1 = points K 2^(t-1)+1 .. K 2^t),
(ii) the true fibre average W, (iii) the rung-0 bracket and (iv) the inner behaviour.  Points of one unit
have identical histories (a block is classified at exactly the levels whose sample reaches it), so one
state per unit is exact.  With cnt = 1 for every unit this is an explicit list of points.

Real arithmetic: scalars that steer the control flow (levels, running bound, tails, thresholds) are mpmath
numbers with 40 digits; ball sizes and the closing radius are exact integers / Fractions (eta is a Fraction);
per-unit brackets are float64 logarithms.

Everything the theorems claim is recorded per level so that it can be checked run by run (checks.py).
"""
import math
from fractions import Fraction
import numpy as np
import mpmath as mp

mp.mp.dps = 40
LN2 = mp.log(2)


# ----------------------------------------------------------------------------------------------
# exact tables on the outer cube
# ----------------------------------------------------------------------------------------------
class Tables:
    """|B(m,r)|, E_r(m) = sum_{j<=r} C(m,j)(e^{u(r+1-j)} - 1), T_m(k) = sum_j C(m,j) e^{-u (j-k)_+}."""

    def __init__(self, m, u):
        self.m = m
        self.u = mp.mpf(u)
        self.binom = [math.comb(m, j) for j in range(m + 1)]
        self.ball = []
        s = 0
        for j in range(m + 1):
            s += self.binom[j]
            self.ball.append(s)                     # ball[r] = |B(m,r)|, exact integer
        eu = mp.e ** self.u
        emu = 1 / eu
        # S_r = sum_{j<=r} C(m,j) e^{u(r-j)};  E_r = e^u S_r - |B(r)|
        S = mp.mpf(0)
        self.E = []
        for r in range(m + 1):
            S = eu * S + self.binom[r]
            self.E.append(eu * S - self.ball[r])
        # R_k = sum_{j>k} C(m,j) e^{-u(j-k)};  R_{k-1} = e^{-u}(C(m,k) + R_k);  T_m(k) = |B(k)| + R_k
        R = mp.mpf(0)
        self.T = [None] * (m + 1)
        for k in range(m, -1, -1):
            self.T[k] = self.ball[k] + R
            R = emu * (self.binom[k] + R)
        self.two_m = 1 << m

    def ballm1(self, r):
        return 0 if r < 0 else self.ball[min(r, self.m)]

    def gamma_tilde(self, r):
        if r == 0:
            return mp.e ** self.u - 1
        return self.E[r] / self.ball[r - 1]

    def kappa(self, r, eta):
        """largest k >= 0 with |B(m,k)| <= max(1, c_eta |B(m,r-1)|), c_eta = (1-eta)/(1+eta) (exact)."""
        bound = Fraction(1 - eta, 1 + eta) * self.ballm1(r - 1)
        if bound < 1:
            bound = Fraction(1)
        return self.largest_ball_le(bound)

    def largest_ball_le(self, bound):
        """largest k >= 0 with |B(m,k)| <= bound (bound >= 1, Fraction or int)."""
        lo, hi = 0, self.m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.ball[mid] <= bound:
                lo = mid
            else:
                hi = mid - 1
        return lo

    def least_ball_ge(self, bound):
        """least r >= 0 with |B(m,r)| >= bound (bound <= 2^m)."""
        lo, hi = 0, self.m
        while lo < hi:
            mid = (lo + hi) // 2
            if self.ball[mid] >= bound:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def gamma_pp(self, r, eta):
        return self.E[r] / self.T[self.kappa(r, eta)]


# ----------------------------------------------------------------------------------------------
# parameters and constants of Algorithm 2L+   (K_REPORT 2.1-2.2)
# ----------------------------------------------------------------------------------------------
class Params2LP:
    def __init__(self, n, n_o, u, lam, eta, etap, theta, nu1, b, delta, xs, costs,
                 K_override=None, tables=None):
        """xs = [x_0 = 2 u n_i, x_1, ..., x_L] (x_L <= b); costs = [C_1..C_L] (queries per inner call)."""
        assert 1 <= n_o <= n - 1
        self.n, self.n_o, self.n_i = n, n_o, n - n_o
        self.u = mp.mpf(u)
        self.lam = mp.mpf(lam)
        self.eta = Fraction(eta)
        assert 0 < self.eta <= Fraction(1, 2)
        self.etaf = mp.mpf(self.eta.numerator) / self.eta.denominator
        self.etap = mp.mpf(etap)
        self.theta = mp.mpf(theta)
        self.nu1 = mp.mpf(nu1)
        self.b = mp.mpf(b)
        self.delta = mp.mpf(delta)
        self.xs = [mp.mpf(x) for x in xs]
        self.L = len(xs) - 1
        assert self.L >= 1
        assert all(self.xs[i] > self.xs[i + 1] for i in range(self.L)), "ladder must decrease"
        assert self.xs[self.L] <= self.b
        self.costs = [None] + [mp.mpf(c) for c in costs]
        assert len(self.costs) == self.L + 1
        self.tab = tables if tables is not None else Tables(n_o, u)
        m = n_o
        e = mp.e
        eta_ = self.etaf
        self.c_eta = (1 - eta_) / (1 + eta_)
        self.J = int(mp.ceil((2 * self.u * n + self.b + n_o * LN2) / self.lam))
        self.nu0 = max((self.J + 1) * (e ** self.lam - 1) / self.etap, self.nu1) / (1 - eta_)
        # r-dagger
        rd = -1
        for r in range(0, m):
            gt = self.tab.gamma_tilde(r)
            okN = gt <= self.theta * (1 - eta_) * self.nu0
            okP = min(gt / self.c_eta, self.tab.gamma_pp(r, self.eta)) <= self.theta
            if okN and okP:
                rd = r
            else:
                break
        self.rdag = rd
        if rd >= 0:
            self.pidag = mp.mpf(self.tab.ball[rd]) / self.tab.two_m
            self.pidag_frac = Fraction(self.tab.ball[rd], self.tab.two_m)
        else:
            self.pidag = mp.mpf(1) / (2 * self.tab.two_m)
            self.pidag_frac = Fraction(1, 2 * self.tab.two_m)
        self.m_max = int(mp.ceil(mp.log(2 * (1 + eta_) * e ** self.lam * self.nu0 / ((1 - eta_) * self.pidag), 2)))
        self.K_theorem = int(mp.ceil(3 * (1 + eta_) / eta_ ** 2 *
                                     mp.log(2 * (self.J + 1) * (self.m_max + 1) * (self.L + 2) / self.delta)))
        self.K = self.K_theorem if K_override is None else int(K_override)
        self.nu = self.K * self.nu0
        self.Mdag = self.K / ((1 - eta_) * self.pidag)
        self.Mbar = 2 * (1 + eta_) * e ** self.lam * self.nu0 * self.Mdag
        self.deltap = self.delta / (4 * self.L * self.Mbar)
        self.Cmax = 1 + 2 * self.Mbar + sum(min(2 * self.Mbar, (self.J + 1) * self.cnt(self.xs[l - 1])) * self.costs[l]
                                           for l in range(1, self.L + 1))
        # the tighter count that claim (vi) states before it is relaxed to C_max
        self.Cvi = 1 + self.Mbar + sum(min(self.Mbar, (self.J + 1) * self.cnt(self.xs[l - 1])) * self.costs[l]
                                       for l in range(1, self.L + 1))
        self.x_out = mp.log((2 / (1 + e ** self.u)) ** n + e ** self.b *
                            (e ** self.lam * (1 + eta_) / (1 - eta_) + self.etap + self.theta))
        # remark of checkpoint 40c5bd7: lowered cap 2 max{e^lam Mdag, Mddag}
        Delta = int(mp.ceil(self.lam / self.u))
        self.Delta = Delta
        if rd >= Delta:
            piddag = mp.mpf(self.tab.ball[rd - Delta]) / self.tab.two_m
            self.Mddag = self.K / ((1 - eta_) * piddag)
        else:
            self.Mddag = self.K * mp.mpf(self.tab.two_m) / (1 - eta_)
        self.cap_new = 2 * max(e ** self.lam * self.Mdag, self.Mddag)

    def cnt(self, x):
        eta_ = self.etaf
        return max(mp.mpf(self.K), 2 * (1 + eta_) ** 2 / (1 - eta_) * mp.e ** self.lam * self.nu * mp.e ** mp.mpf(x))


# ----------------------------------------------------------------------------------------------
# parameters and constants of Algorithm 2L   (theory report, Theorem 11.52)
# ----------------------------------------------------------------------------------------------
class Params2L:
    def __init__(self, n, n_o, u, G, delta, xs, costs, K_override=None, tables=None):
        """xs = [x_0 = 2 u n_i, ..., x_last]; tolerance b := x_last; G = g n; levels s_j = s_0 e^j."""
        assert 1 <= n_o <= n - 1
        self.n, self.n_o, self.n_i = n, n_o, n - n_o
        self.u = mp.mpf(u)
        self.G = mp.mpf(G)
        self.delta = mp.mpf(delta)
        self.xs = [mp.mpf(x) for x in xs]
        self.L = len(xs) - 1
        assert self.L >= 1
        assert all(self.xs[i] > self.xs[i + 1] for i in range(self.L))
        self.b = self.xs[self.L]
        self.lam = mp.mpf(1)
        self.costs = [None] + [mp.mpf(c) for c in costs]
        self.tab = tables if tables is not None else Tables(n_o, u)
        self.K_theorem = int(mp.ceil(24 * mp.log(mp.mpf(2) ** (n + 6) * n ** 3 / self.delta)))
        self.K = self.K_theorem if K_override is None else int(K_override)
        self.J = int(mp.ceil(2 * self.u * n + self.b + n_o * LN2 + 10))
        thr = mp.e ** (self.G - self.b) / 4
        rd = -1
        for r in range(0, n_o):
            if self.tab.gamma_tilde(r) <= thr:
                rd = r
            else:
                break
        self.rdag = rd
        if rd >= 0:
            self.Mdag = 2 * self.K * mp.mpf(self.tab.two_m) / self.tab.ball[rd]
        else:
            self.Mdag = mp.inf
        self.Mbar = 8 * self.J * mp.e ** 2 * self.Mdag            # "every M that is used is at most 8Je^2 M-dagger"
        self.cap_new = 2 * mp.e * self.Mdag                       # remark of 40c5bd7 for the constants of 11.52
        self.width_bound = mp.log(1 + 4 * self.J * mp.e ** (self.b + 1) + mp.e ** self.b + mp.e ** self.G)
        # displayed cost bound of 11.52: sum_{j<=J} sum_l min(8Je^2 Mdag, 32KJe^3 e^{x_{l-1}} + 4K)(l+1) C_l ;
        # the l = 0 term (one query per point) and the reference query are added here (finding m-e of my notes)
        if self.Mdag != mp.inf:
            self.Cmax = 1 + (self.J + 1) * (self.Mbar + sum(
                min(self.Mbar, 32 * self.K * self.J * mp.e ** 3 * mp.e ** self.xs[l - 1] + 4 * self.K) * (l + 1) * self.costs[l]
                for l in range(1, self.L + 1)))
        else:
            self.Cmax = mp.inf

    def cnt(self, x):
        """count of 11.52: at most 32 K J e^2 e^x + 4K points used at level j have W > s_j e^{-x} (x in b + N)."""
        return 32 * self.K * self.J * mp.e ** 2 * mp.e ** mp.mpf(x) + 4 * self.K

    def round_up(self, x):
        """least element of b + N that is >= x."""
        x = mp.mpf(x)
        return self.b + mp.ceil(x - self.b) if x > self.b else self.b


# ----------------------------------------------------------------------------------------------
# instances for the unit engine: "tail-function" instances (classes of equal fibre average)
# ----------------------------------------------------------------------------------------------
class ClassInstance:
    """
    An instance seen through the law of the fibre averages.  Classes c = 0..C-1:
      lnW[c]   true ln of the fibre average,
      prob[c]  probability that a uniform outer point falls in the class (mp numbers summing to 1),
      kap[c]   anchor offset:  -psi(a, 0_i) = lnW[c] + kap[c]  (|kap| <= u n_i),
      strat[c] inner behaviour (see SimOracle).
    ref: the class of the outer origin (psi_0 = -(lnW[ref] + kap[ref])).
    """

    def __init__(self, n, n_o, u, lnW, prob, kap, strat, ref, name=""):
        self.n, self.n_o, self.n_i, self.u = n, n_o, n - n_o, float(u)
        self.lnW = np.asarray(lnW, dtype=np.float64)
        self.prob = [mp.mpf(p) for p in prob]
        tot = mp.fsum(self.prob)
        assert abs(tot - 1) < mp.mpf(10) ** (-25), tot
        self.kap = np.broadcast_to(np.asarray(kap, dtype=np.float64), self.lnW.shape).copy()
        assert np.all(np.abs(self.kap) <= self.u * self.n_i + 1e-9)
        self.strat = np.broadcast_to(np.asarray(strat, dtype=np.int64), self.lnW.shape).copy()
        self.ref = ref
        self.name = name
        self.psi0 = -(float(self.lnW[ref]) + float(self.kap[ref]))
        self.A = mp.fsum(p * mp.e ** mp.mpf(float(w)) for p, w in zip(self.prob, self.lnW))
        order = np.argsort(-self.lnW, kind="stable")
        self._sorted_lnW = self.lnW[order]
        cum = []
        s = mp.mpf(0)
        for c in order:
            s += self.prob[c]
            cum.append(s)
        self._cum = cum
        self._probf = np.array([float(p) for p in self.prob])

    def tail(self, lnt):
        """P(W > t) exactly (mp), for t = e^lnt compared in float64 like the algorithm does."""
        k = int(np.searchsorted(-self._sorted_lnW, -float(lnt), side="left"))   # number of classes with lnW > lnt
        return mp.mpf(0) if k == 0 else self._cum[k - 1]

    def new_block(self, size, rng):
        """multinomial counts of a block of `size` fresh uniform points; sequential binomials."""
        counts = np.zeros(len(self.lnW), dtype=object)
        remaining = int(size)
        rem_p = mp.mpf(1)
        order = np.argsort(-self._probf, kind="stable")
        for idx, c in enumerate(order):
            if remaining == 0:
                break
            if idx == len(order) - 1:
                counts[c] = remaining
                break
            pc = self.prob[c] / rem_p
            pcf = float(min(mp.mpf(1), max(mp.mpf(0), pc)))
            x = big_binomial(remaining, pcf, rng)
            counts[c] = x
            remaining -= x
            rem_p -= self.prob[c]
            if rem_p <= 0:
                break
        nz = np.array([c for c in range(len(counts)) if counts[c] > 0], dtype=np.int64)
        return dict(cls=nz, cnt=counts[nz], lnW=self.lnW[nz],
                    lnL0=self.lnW[nz] + self.kap[nz] - self.u * self.n_i,
                    lnU0=self.lnW[nz] + self.kap[nz] + self.u * self.n_i,
                    strat=self.strat[nz])


def big_binomial(n, p, rng):
    """Binomial(n, p) as a Python int, for any n: chunks of 2^61 (the numpy Generator sampler was checked in
    test_binomial.py for n up to 2^62 and n p from 0.1 to 5000; a sum of independent binomials with the same p is binomial)."""
    if p <= 0.0 or n == 0:
        return 0
    if p >= 1.0:
        return n
    CH = 1 << 61
    if n <= CH:
        return int(rng.binomial(n, p))
    full, rest = divmod(n, CH)
    assert full <= (1 << 22), "block too large for the sampler"
    tot = 0
    done = 0
    while done < full:
        k = min(full - done, 1 << 16)
        tot += int(rng.binomial(CH, p, size=k).astype(object).sum())
        done += k
    if rest:
        tot += int(rng.binomial(rest, p))
    return tot


# ----------------------------------------------------------------------------------------------
# simulated inner oracle (valid or deliberately invalid)
# ----------------------------------------------------------------------------------------------
S_CENTER, S_TOP, S_BOTTOM, S_ADV_HI, S_ADV_LO, S_EXACT, S_RANDOM, S_NARROW = 0, 1, 2, 3, 4, 5, 6, 7
S_INV_ABOVE, S_INV_BELOW, S_TOO_WIDE, S_TRIVIAL = 20, 21, 22, 23
VALID_STRATS = [S_CENTER, S_TOP, S_BOTTOM, S_ADV_HI, S_ADV_LO, S_EXACT, S_RANDOM, S_NARROW]


class SimOracle:
    """
    Inner behaviour chosen per unit by its strategy code.  A valid answer at rung l is any [L', U'] with
    L' <= W <= U' and U' <= e^{x_l} L'; write L' = W e^{-t}, U' = W e^{w - t}, 0 <= t <= w <= x_l.
      CENTER  t = x_l/2, w = x_l           TOP     t = x_l  (U' = W)        BOTTOM  t = 0  (L' = W)
      ADV_HI / ADV_LO   keep the point unclassified at the current level j if that is possible, with the
                        largest possible upper end; otherwise answer BOTTOM (ADV_HI) or TOP (ADV_LO)
      EXACT   L' = U' = W                  RANDOM  t uniform                 NARROW  width uniform, centred
    Invalid behaviours (to test the statements "in every run, on or off the good event"):
      INV_ABOVE  bracket of the right width entirely above W;   INV_BELOW  entirely below W;
      TOO_WIDE   contains W but has width 2.5 x_l;              TRIVIAL    returns the rung-0 bracket again.
    """

    def __init__(self, xs, rng):
        self.xs = [float(x) for x in xs]
        self.rng = rng

    def __call__(self, run, idx, l, j):
        x = self.xs[l]
        lnW = run.lnW[idx]
        st = run.strat[idx]
        lns = run.ln_s(j)
        b = run.b_f
        g = lns - lnW                      # gap of the point below the level (negative: above)
        t = np.full(lnW.shape, x / 2)
        w = np.full(lnW.shape, x)
        t = np.where(st == S_TOP, x, t)
        t = np.where(st == S_BOTTOM, 0.0, t)
        # adversarial: unclassified iff U' > s_j and L' <= s_j e^{-b}:  t < x - g  and  t >= b - g ; t in [0, x]
        lo = np.maximum(0.0, b - g)
        hi = np.minimum(x, x - g)
        feas = lo < hi
        adv = (st == S_ADV_HI) | (st == S_ADV_LO)
        t = np.where(adv & feas, lo, t)
        t = np.where((st == S_ADV_HI) & ~feas, 0.0, t)
        t = np.where((st == S_ADV_LO) & ~feas, x, t)
        if np.any(st == S_RANDOM):
            t = np.where(st == S_RANDOM, self.rng.uniform(0, x, size=lnW.shape), t)
        if np.any(st == S_NARROW):
            ww = self.rng.uniform(0, x, size=lnW.shape)
            w = np.where(st == S_NARROW, ww, w)
            t = np.where(st == S_NARROW, ww / 2, t)
        w = np.where(st == S_EXACT, 0.0, w)
        t = np.where(st == S_EXACT, 0.0, t)
        lnL = lnW - t
        lnU = lnW + (w - t)
        # invalid behaviours
        lnL = np.where(st == S_INV_ABOVE, lnW + 0.5 * x + 0.3, lnL)
        lnU = np.where(st == S_INV_ABOVE, lnW + 1.5 * x + 0.3, lnU)
        lnL = np.where(st == S_INV_BELOW, lnW - 1.5 * x - 0.3, lnL)
        lnU = np.where(st == S_INV_BELOW, lnW - 0.5 * x - 0.3, lnU)
        lnL = np.where(st == S_TOO_WIDE, lnW - 1.25 * x, lnL)
        lnU = np.where(st == S_TOO_WIDE, lnW + 1.25 * x, lnU)
        lnL = np.where(st == S_TRIVIAL, run.lnL0[idx], lnL)
        lnU = np.where(st == S_TRIVIAL, run.lnU0[idx], lnU)
        return lnL, lnU


# ----------------------------------------------------------------------------------------------
# the engine
# ----------------------------------------------------------------------------------------------
class Abort(Exception):
    pass


class Run:
    """
    One run of Algorithm 2L+ (variant='2L+', P a Params2LP) or Algorithm 2L (variant='2L', P a Params2L).
    inst must provide: psi0, n, n_o, n_i, new_block(size, rng) -> dict(cnt, lnW, lnL0, lnU0, strat[, ...]).
    oracle(run, idx, l, j) -> (lnL', lnU') for the units idx at rung l (called during level j).
    cost_of(l) queries are charged per point per inner call (P.costs[l]) unless oracle has attribute
    `charges` (then the oracle adds its real number of queries to run.inner_queries itself).
    """

    def __init__(self, P, inst, oracle, rng, variant="2L+", abort_on_cost=True, max_units=4_000_000, mutation=None):
        self.P, self.inst, self.oracle, self.rng, self.variant = P, inst, oracle, rng, variant
        self.mutation = mutation          # None, or one of: neg_tol, noharper, maxform, close_at_no, q_no_eta (2L+ only)
        self.abort_on_cost = abort_on_cost
        self.max_units = max_units
        n = P.n
        self.n_o = P.n_o
        self.tab = P.tab
        u = P.u
        self.lam = P.lam
        self.b = P.b
        self.b_f = float(P.b)
        self.ln_s0 = mp.mpf(-inst.psi0) - u * n
        self._lns_cache = {}
        if variant == "2L+":
            self.ln_ell = mp.mpf(-inst.psi0) + n * mp.log((1 + mp.e ** (-u)) / 2)
        else:
            self.ln_ell = self.ln_s0
        self.Sigma = mp.mpf(0)            # in units of e^{ln_s0}: all "absolute" quantities are stored as mp multiples of s_0
        # units
        self.cnt_dtype = object if getattr(inst, "big_counts", True) else np.int64
        self.cnt = np.zeros(0, dtype=self.cnt_dtype)
        self.blk = np.zeros(0, dtype=np.int64)
        self.lnW = np.zeros(0)
        self.lnL = np.zeros(0)
        self.lnU = np.zeros(0)
        self.lnL0 = np.zeros(0)
        self.lnU0 = np.zeros(0)
        self.rung = np.zeros(0, dtype=np.int64)
        self.strat = np.zeros(0, dtype=np.int64)
        self.extra = []
        self.nblocks = 0
        self.block_end = []
        self.points_drawn = 0
        self.calls = [0] * (P.L + 1)                 # total inner calls per rung
        self.inner_queries = mp.mpf(0)
        self.levels = []                             # per-level records
        self.status = None
        self.result = None
        self.abort_reason = None

    # -- helpers
    def ln_s(self, j):
        v = self._lns_cache.get(j)
        if v is None:
            v = float(self.ln_s0 + j * self.lam)
            self._lns_cache[j] = v
        return v

    def queries(self):
        return 1 + self.points_drawn + self.inner_queries

    def _ensure_blocks(self, t):
        while self.nblocks <= t:
            tb = self.nblocks
            size = self.P.K if tb == 0 else self.P.K * (1 << (tb - 1))
            d = self.inst.new_block(size, self.rng)
            k = len(d["cnt"])
            if len(self.cnt) + k > self.max_units:
                raise Abort("harness: too many units")
            self.cnt = np.concatenate([self.cnt, np.asarray(d["cnt"], dtype=self.cnt_dtype)])
            self.blk = np.concatenate([self.blk, np.full(k, tb, dtype=np.int64)])
            self.lnW = np.concatenate([self.lnW, d["lnW"]])
            self.lnL = np.concatenate([self.lnL, d["lnL0"]])
            self.lnU = np.concatenate([self.lnU, d["lnU0"]])
            self.lnL0 = np.concatenate([self.lnL0, d["lnL0"]])
            self.lnU0 = np.concatenate([self.lnU0, d["lnU0"]])
            self.rung = np.concatenate([self.rung, np.zeros(k, dtype=np.int64)])
            self.strat = np.concatenate([self.strat, np.asarray(d["strat"], dtype=np.int64)])
            if "extra" in d:
                self.extra.extend(d["extra"])
            self.nblocks += 1
            self.block_end.append(len(self.cnt))
            self.points_drawn += size

    def _classify(self, j, t, rec):
        """classify all units of blocks <= t at level j; returns N (#high points).  Units of blocks <= t are a prefix."""
        lns = self.ln_s(j)
        hi = self.block_end[t]
        P = self.P
        lnU = self.lnU[:hi]
        lnL = self.lnL[:hi]
        rung = self.rung[:hi]
        while True:
            need = (lnU > lns) & (lnL <= lns - self.b_f)
            if not need.any():
                break
            if (need & (rung >= P.L)).any():
                raise Abort("unclassified at the last rung")
            idx = np.nonzero(need)[0]
            newr = rung[idx] + 1
            for l in np.unique(newr):
                sel = idx[newr == l]
                npts = self._sum_cnt_idx(sel)
                if not getattr(self.oracle, "charges", False):
                    add = npts * P.costs[int(l)]
                    if self.abort_on_cost and self.queries() + add > P.Cmax:
                        raise Abort("query budget C_max")
                    self.inner_queries += add
                self.calls[int(l)] += npts
                rec["calls"][int(l)] += npts
                lnLp, lnUp = self.oracle(self, sel, int(l), j)
                self.lnL[sel] = np.maximum(self.lnL[sel], lnLp)
                self.lnU[sel] = np.minimum(self.lnU[sel], lnUp)
                self.rung[sel] = l
        high = np.nonzero(~(lnU <= lns))[0]
        return self._sum_cnt_idx(high)

    def _sum_cnt_idx(self, idx):
        if len(idx) == 0:
            return 0
        if self.cnt_dtype is object:
            return int(sum(self.cnt[idx].tolist()))
        return int(self.cnt[idx].sum())          # explicit points: cnt = 1 each, no overflow

    def count_above(self, t, lnthr):
        """#points among the first K 2^t with true W > e^lnthr (for the checks)."""
        hi = self.block_end[t]
        return self._sum_cnt_idx(np.nonzero(self.lnW[:hi] > lnthr)[0])

    # -- the algorithm
    def run(self):
        try:
            if self.variant == "2L+":
                self._run_2LP()
            else:
                self._run_2L()
        except Abort as e:
            self.status = "abort"
            self.abort_reason = str(e)
            # trivial bracket [s_0, s_0 e^{2un}]
            self.result = (self.ln_s0, self.ln_s0 + 2 * self.P.u * self.P.n)
        return self

    def _run_2LP(self):
        P, tab = self.P, self.tab
        m = self.n_o
        eta = P.eta
        e = mp.e
        K = P.K
        two_m = tab.two_m
        s0 = mp.mpf(1)                      # absolute scale: everything in units of s_0
        ell = e ** (self.ln_ell - self.ln_s0)
        Sigma = mp.mpf(0)
        upper_terms = mp.mpf(0)             # sum_{i<j} (s_{i+1} - s_i) q_i
        for j in range(0, P.J + 1):
            sj = e ** (j * P.lam)
            M = K
            t = 0
            rec = dict(j=j, ell_entry=ell, passes=[], calls=[0] * (P.L + 1), status=None,
                       Mneg=P.nu * sj / (ell * e ** P.b), sj=sj)
            if self.mutation == "neg_tol":
                rec["Mneg"] = P.nu * sj / ell
            self.levels.append(rec)
            while True:
                self._ensure_blocks(t)
                N = self._classify(j, t, rec)
                # q = min{1, max(N,K)/((1-eta) M)}  (exact Fraction)
                qF = Fraction(max(N, K), 1) / ((1 - eta) * M)
                if self.mutation == "q_no_eta":
                    qF = Fraction(max(N, K), M)
                if qF > 1:
                    qF = Fraction(1)
                q = mp.mpf(qF.numerator) / qF.denominator
                populated = N >= K
                plow = None
                kH = None
                if populated:
                    plowF = Fraction(N, 1) / ((1 + eta) * M)
                    plow = mp.mpf(plowF.numerator) / plowF.denominator
                    bound = plowF * two_m
                    if bound < 1:
                        bound = Fraction(1)
                    kH = tab.largest_ball_le(bound)
                    if self.mutation == "noharper":
                        ell = max(ell, sj * e ** (-P.b) * plow)
                    else:
                        ell = max(ell, sj * e ** (-P.b) * plow, sj * e ** (-P.b) * tab.T[kH] / two_m)
                # closure test
                if qF * two_m < 1:
                    tail = mp.mpf(0)
                    r = -1
                else:
                    r = tab.least_ball_ge(qF * two_m)
                    tail = sj * tab.E[r] / two_m if r <= m - 1 else mp.inf
                    if self.mutation == "close_at_no" and r == m:
                        tail = sj * tab.E[r] / two_m
                closed = tail <= P.theta * e ** P.b * ell
                rec["passes"].append(dict(M=M, t=t, N=N, q=q, qF=qF, r=r, tail=tail, populated=populated,
                                          plow=plow, kH=kH, ell_after=ell, closed=closed))
                if closed:
                    Lo = max(ell, Sigma + ((1 - e ** (-P.lam)) * e ** (-P.b) * sj * plow if populated else 0))
                    if self.mutation == "maxform":
                        Lo = ell
                    Up = s0 + upper_terms + tail
                    rec["status"] = "closed"
                    self.status = "closed"
                    self.result = (self.ln_s0 + mp.log(Lo), self.ln_s0 + mp.log(Up))
                    self.final = dict(Lo=Lo, Up=Up, ell=ell, Sigma=Sigma, j=j, tail=tail)
                    if Lo > Up:          # erratum m1 of K_REPORT: off the good event the pair can have L > U
                        self.status = "closed_L>U"
                    return
                if populated:
                    rec["status"] = "populated"
                    rec["q"] = q; rec["qF"] = qF; rec["plow"] = plow; rec["M"] = M; rec["t"] = t; rec["N"] = N
                    Sigma += (1 - e ** (-P.lam)) * e ** (-P.b) * sj * plow
                    upper_terms += (e ** P.lam - 1) * sj * q
                    break
                if M >= rec["Mneg"]:
                    rec["status"] = "negligible"
                    rec["q"] = q; rec["qF"] = qF; rec["M"] = M; rec["t"] = t; rec["N"] = N
                    upper_terms += (e ** P.lam - 1) * sj * q
                    break
                if t + 1 > P.m_max:
                    raise Abort("M would exceed K 2^m_max")
                M *= 2
                t += 1
        raise Abort("level J left")

    def _run_2L(self):
        P, tab = self.P, self.tab
        m = self.n_o
        e = mp.e
        K = P.K
        two_m = tab.two_m
        ell = mp.mpf(1)                      # = s_0 (units of s_0)
        upper_terms = mp.mpf(0)              # sum_{i<j} s_{i+1} q_i
        for j in range(0, P.J + 2):
            if j == P.J + 1:
                raise Abort("level J+1 reached")
            sj = e ** mp.mpf(j)
            M = K
            t = 0
            rec = dict(j=j, ell_entry=ell, passes=[], calls=[0] * (P.L + 1), status=None,
                       Mneg=2 * K * P.J * e * sj / (ell * e ** P.b), sj=sj)
            self.levels.append(rec)
            while True:
                self._ensure_blocks(t)
                N = self._classify(j, t, rec)
                qF = Fraction(2 * max(N, K), M)
                if qF > 1:
                    qF = Fraction(1)
                q = mp.mpf(qF.numerator) / qF.denominator
                populated = N >= K
                if populated:
                    ell = max(ell, sj * e ** (-P.b) * mp.mpf(N) / (2 * M))
                r = tab.least_ball_ge(qF * two_m) if qF * two_m >= 1 else -1
                if r == m:
                    closed = False
                    tail = mp.inf
                else:
                    tail = mp.mpf(0) if qF * two_m < 1 else sj * tab.E[r] / two_m
                    closed = tail <= e ** P.G * ell
                rec["passes"].append(dict(M=M, t=t, N=N, q=q, qF=qF, r=r, tail=tail, populated=populated,
                                          ell_after=ell, closed=closed))
                if closed:
                    Lo = ell
                    Up = 1 + upper_terms + tail
                    rec["status"] = "closed"
                    self.status = "closed"
                    self.result = (self.ln_s0 + mp.log(Lo), self.ln_s0 + mp.log(Up))
                    self.final = dict(Lo=Lo, Up=Up, ell=ell, j=j, tail=tail)
                    return
                # M_j^neg with the current ell (at an unpopulated pass this is the entry value)
                if populated or M >= rec["Mneg"]:
                    rec["status"] = "populated" if populated else "negligible"
                    rec["q"] = q; rec["qF"] = qF; rec["M"] = M; rec["t"] = t; rec["N"] = N
                    upper_terms += e * sj * q
                    break
                M *= 2
                t += 1
                if K * (1 << t) > 4 * K * two_m * 2:          # "M <= 4K 2^{n_o} always" (text of 11.52); safety net
                    raise Abort("M beyond 4K 2^{n_o}")
