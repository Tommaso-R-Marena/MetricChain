"""Workstream K, numerical check (ii): the outer loop of Algorithm 2L+ (Theorem K1 of REPORT.md) with a SIMULATED inner
oracle, at small size, and every inequality of the proof checked on every run.

The true fibre average W(a) of a uniform outer point takes the value vals[t] with probability probs[t] (all 2^{n_o}
points of an enumerated cube, or the shells of a radial outer landscape).  A call of the inner procedure at accuracy x
returns a valid bracket [L, U], U = L e^x, around the true value; where the true value sits inside the bracket is
chosen by `mode` (0 random, 1 value at the top, 2 value at the bottom, 3 adversarial: keep the point undecided at the
current level as long as possible, then make it HIGH if possible, 4 adversarial: ..., then make it LOW if possible).

What is checked on each run (see REPORT.md, proof of Theorem K1; G = good event (V2) & (V3), verified exactly on the
realised sample, (V1) holds by construction):
  C1 validity      L <= A <= U                                        [must hold whenever G holds]
  C2 width         U/L <= (2 p_u)^n + e^b (e^lam (1+eta)/(1-eta) + eta' + theta)        [deterministic]
  C3 certificates  q_i >= p(s_i);  pbar_i <= p(s_i e^-b) at populated levels;  ell <= A at every update   [on G]
  C4 closure       every level that is left without stopping has r(q_j) > r_dagger                       [on G]
  C5 sample sizes  M_j <= max(K, 2 M_j^neg),  M_j^neg <= (1+eta) e^lam nu0 M_dagger,  M_j <= Mbar        [on G]
  C6 count lemma   M_j^neg p(s_j e^-x) <= nu e^lam (1+eta)/(1-eta) e^x  for x in the inner ladder        [on G]
                   #{i <= M_j : W_i > s_j e^-x} <= cnt(x) = max(K, 2 nu e^lam (1+eta)^2/(1-eta) e^x)     [on G]
  C7 calls         calls at accuracy x_l during level j <= #{i <= M_j : W_i > s_j e^-x_{l-1}}            [deterministic]
  C8 termination   closure within J+1 levels                                                             [on G]
Mutations (the test must have power): see `mutations()`.
"""
import math, sys, time
import numpy as np


# ---------------------------------------------------------------------------------------------------------------------
# exact tables of the outer cube (small n_o: python integers / floats)
# ---------------------------------------------------------------------------------------------------------------------
class Tables:
    def __init__(self, n_o, u, eta):
        self.n_o, self.u, self.eta = n_o, u, eta
        self.binom = [math.comb(n_o, j) for j in range(n_o + 1)]
        self.ball = [0]                                              # ball[r + 1] = |B(n_o, r)|, r = -1..n_o
        for j in range(n_o + 1):
            self.ball.append(self.ball[-1] + self.binom[j])
        self.E = [0.0] * (n_o + 1)                                   # E_r = e^u E_{r-1} + (e^u - 1)|B(r)|
        self.E[0] = math.expm1(u)
        for r in range(1, n_o + 1):
            self.E[r] = math.exp(u) * self.E[r - 1] + math.expm1(u) * self.ball[r + 1]
        S = [0.0] * (n_o + 1)                                        # S_k = sum_{j>k} C(n,j) e^{-u(j-k)}
        for k in range(n_o, 0, -1):
            S[k - 1] = math.exp(-u) * (self.binom[k] + S[k])
        self.T = [self.ball[k + 1] + S[k] for k in range(n_o + 1)]
        self.Gt = [math.expm1(u)] + [self.E[r] / self.ball[r] for r in range(1, n_o + 1)]
        c = (1 - eta) / (1 + eta)
        self.kappa = [0] + [self.kball(c * self.ball[r]) for r in range(1, n_o + 1)]
        self.G2 = [self.E[r] / self.T[self.kappa[r]] for r in range(n_o + 1)]

    def radius(self, q):
        """least r in 0..n_o with |B(r)| >= 2^{n_o} q"""
        target = q * 2.0 ** self.n_o
        for r in range(self.n_o + 1):
            if self.ball[r + 1] >= target:
                return r
        return self.n_o

    def kball(self, count):
        """largest k >= 0 with |B(k)| <= max(1, count)"""
        t = max(1.0, count)
        k = 0
        while k + 1 <= self.n_o and self.ball[k + 2] <= t:
            k += 1
        return k

    def rdagger(self, theta, nu0):
        eta = self.eta
        r = -1
        for rr in range(self.n_o):
            okN = self.Gt[rr] <= theta * (1 - eta) * nu0
            okP = min((1 + eta) / (1 - eta) * self.Gt[rr], self.G2[rr]) <= theta
            if okN and okP:
                r = rr
            else:
                break
        return r


class Params:
    """All constants of Algorithm 2L+ (REPORT.md section 2.2)."""
    def __init__(self, n, n_o, u, lam, eta, etap, theta, b, ladder, delta, nu1=None, K=None):
        self.n, self.n_o, self.n_i, self.u = n, n_o, n - n_o, u
        self.lam, self.eta, self.etap, self.theta, self.b, self.delta = lam, eta, etap, theta, b, delta
        self.x = [2 * u * self.n_i] + list(ladder)                   # x_0 = 2 u n_i > x_1 > ... > x_L,  x_L <= b
        self.Lx = len(self.x) - 1
        assert all(self.x[i] > self.x[i + 1] for i in range(self.Lx)) and self.x[-1] <= b and self.Lx >= 1
        self.J = math.ceil((2 * u * n + b + n_o * math.log(2)) / lam)
        if theta is None:                                            # part (iii) of the suite: nu1 = 1, [N]-threshold = nu1 (target)
            theta = nu1 / ((self.J + 1) * math.expm1(lam) / etap)
            nu1 = 1.0
            self.theta = theta
        self.nu1 = (2 * math.exp(u) * n_o / theta) if nu1 is None else nu1
        self.nu0 = max((self.J + 1) * math.expm1(lam) / etap, self.nu1) / (1 - eta)
        self.tab = Tables(n_o, u, eta)
        self.rdag = self.tab.rdagger(theta, self.nu0)
        self.pidag = (self.tab.ball[self.rdag + 1] if self.rdag >= 0 else 0.5) / 2.0 ** n_o
        self.mmax = math.ceil(math.log2(2 * (1 + eta) * math.exp(lam) * self.nu0 / ((1 - eta) * self.pidag)))
        self.Nev = (self.J + 1) * (self.mmax + 1) * (self.Lx + 2)
        self.K = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(2 * self.Nev / delta)) if K is None else K
        self.nu = self.K * self.nu0
        self.Mdag = self.K / ((1 - eta) * self.pidag)
        self.Mbar = 2 * (1 + eta) * math.exp(lam) * self.nu0 * self.Mdag
        self.pu = 1 / (1 + math.exp(u))
        self.width_bound = (2 * self.pu) ** n + math.exp(b) * (math.exp(lam) * (1 + eta) / (1 - eta) + etap + theta)

    def cnt(self, x):
        return max(self.K, 2 * self.nu * math.exp(self.lam) * (1 + self.eta) ** 2 / (1 - self.eta) * math.exp(x))


# ---------------------------------------------------------------------------------------------------------------------
# the algorithm (outer loop), with mutations for the power of the test
# ---------------------------------------------------------------------------------------------------------------------
def run_2L(rng, vals, probs, s0, ell_ref, P, mode, max_points=16_000_000, mut=()):
    """vals must be sorted increasingly.  mut: set of strings -- 'noharper' (no Harper lower bound in ell), 'maxform'
    (lower end = running ell only), 'close_at_no' (tail lemma applied at r = n_o), 'neg_tol' (negligibility threshold
    nu s/ell instead of nu s/(ell e^b): a tolerance mismatch), 'q_plain' (q = max(N,K)/M without the factor 1/(1-eta))."""
    tab, lam, eta, b, K = P.tab, P.lam, P.eta, P.b, P.K
    No = 2.0 ** P.n_o
    xs = np.array(P.x)
    cdf = np.cumsum(probs)
    Widx = np.zeros(0, dtype=np.int32)
    W = np.zeros(0); Lb = np.zeros(0); Ub = np.zeros(0); acc = np.zeros(0, dtype=np.int16)
    ell = ell_ref
    levels = []            # dicts: s, M, q, N, populated, pbar, ell_in, Mneg, r, calls[l]
    Lsum = 0.0             # (1 - e^-lam) e^-b sum over populated levels of s_i pbar_i
    eb = math.exp(-b)
    for j in range(P.J + 1):
        s = s0 * math.exp(j * lam)
        ell_in = ell
        Mneg = P.nu * s / (ell_in * (1.0 if "neg_tol" in mut else math.exp(b)))
        M = K
        calls = [0] * (P.Lx + 1)
        while True:
            if M > max_points:
                return dict(error="sample too large for the simulation", M=M, level=j)
            if len(W) < M:
                extra = M - len(W)
                idx = np.minimum(np.searchsorted(cdf, rng.uniform(size=extra)), len(vals) - 1).astype(np.int32)
                Widx = np.concatenate([Widx, idx])
                W = np.concatenate([W, vals[idx]])
                # trivial bracket from one query at (a, 0): ratio e^{2 u n_i}; placed like the inner brackets
                t0 = rng.uniform(size=extra) if mode == 0 else (np.ones(extra) if mode in (1, 4) else np.zeros(extra))
                Lb = np.concatenate([Lb, np.minimum(W[-extra:] * np.exp(-t0 * xs[0]), W[-extra:])])
                Ub = np.concatenate([Ub, np.maximum(W[-extra:] * np.exp((1 - t0) * xs[0]), W[-extra:])])
                acc = np.concatenate([acc, np.zeros(extra, dtype=np.int16)])
            while True:                                               # classify a_1..a_M at level j
                und = np.nonzero((Ub[:M] > s) & (Lb[:M] <= s * eb))[0]
                if len(und) == 0:
                    break
                if np.any(acc[und] >= P.Lx):
                    return dict(error="classification does not end at the last accuracy of the ladder")
                acc[und] += 1
                for l in np.unique(acc[und]):
                    calls[int(l)] += int((acc[und] == l).sum())
                x = xs[acc[und]]
                w = W[und]
                if mode == 0:
                    Lnew = w * np.exp(-rng.uniform(size=len(und)) * x)
                elif mode == 1:
                    Lnew = w * np.exp(-x)                             # value at the top of the bracket
                elif mode == 2:
                    Lnew = w.copy()                                   # value at the bottom
                else:
                    # adversarial: undecided iff L <= s e^-b and L e^x > s, with L in [w e^-x, w]
                    keep = (x > b) & (w > s * np.exp(-x)) & (w * np.exp(-x) <= s * eb)
                    Lkeep = np.minimum(w, s * eb)
                    Lelse = w.copy() if mode == 3 else w * np.exp(-x)  # 3: push U up (HIGH if possible); 4: U = w (LOW if possible)
                    Lnew = np.where(keep, Lkeep, Lelse)
                # a valid bracket in floating point: L <= w <= U exactly, U/L <= e^x up to rounding
                Lnew = np.minimum(Lnew, w)
                Unew = np.maximum(Lnew * np.exp(x), w)
                Lb[und] = np.maximum(Lb[und], Lnew)
                Ub[und] = np.minimum(Ub[und], Unew)
            N = int((Ub[:M] > s).sum())
            q = min(1.0, max(N, K) / ((1.0 if "q_plain" in mut else (1 - eta)) * M))
            pbar = None
            if N >= K:
                pbar = N / ((1 + eta) * M)
                k = tab.kball(No * pbar)
                ell = max(ell, s * eb * pbar)
                if "noharper" not in mut:
                    ell = max(ell, s * eb * tab.T[k] / No)
            if No * q < 1:
                tail, r = 0.0, -1
            else:
                r = tab.radius(q)
                if r <= P.n_o - 1 or "close_at_no" in mut:
                    tail = s * tab.E[min(r, P.n_o)] / No
                else:
                    tail = math.inf
            rec = dict(s=s, M=M, q=q, N=N, populated=(N >= K), pbar=pbar, ell_in=ell_in, ell_out=ell, Mneg=Mneg, r=r, calls=calls, tail=tail)
            if tail <= P.theta * math.exp(b) * ell:
                Lsum_final = Lsum + ((1 - math.exp(-lam)) * eb * s * pbar if N >= K else 0.0)
                upper = s0 + sum(math.expm1(lam) * lv["s"] * lv["q"] for lv in levels) + tail
                lower = ell if "maxform" in mut else max(ell, Lsum_final)
                return dict(lower=lower, upper=upper, levels=levels, last=rec, Widx=Widx, ell=ell, Lsum=Lsum_final, points=len(W))
            if N >= K:
                Lsum += (1 - math.exp(-lam)) * eb * s * pbar
                levels.append(rec)
                break
            if M >= Mneg:
                levels.append(rec)
                break
            M *= 2
    return dict(error="no closure within J + 1 levels")


# ---------------------------------------------------------------------------------------------------------------------
# the checks
# ---------------------------------------------------------------------------------------------------------------------
class Counts:
    """#{i <= M : W_i > thr} for M in the doubling sequence, by counting sample indices (vals sorted increasingly)."""
    def __init__(self, Widx, vals, probs, K):
        self.vals = vals
        self.tailp = np.concatenate([np.cumsum(probs[::-1])[::-1], [0.0]])     # tailp[i] = P(W >= vals[i])
        self.suffix = {}
        M = K
        while M <= len(Widx):
            c = np.bincount(Widx[:M], minlength=len(vals))
            self.suffix[M] = np.concatenate([np.cumsum(c[::-1])[::-1], [0]])
            M *= 2
    def exceed(self, thr):                                                     # P(W > thr)
        return float(self.tailp[np.searchsorted(self.vals, thr, side="right")])
    def count(self, M, thr):                                                   # #{i <= M : W_i > thr}
        return int(self.suffix[M][np.searchsorted(self.vals, thr, side="right")])


def good_event(run, C, P):
    """(V2) and (V3) on the realised sample, for all levels visited and all M of the doubling sequence that were drawn."""
    eta, K = P.eta, P.K
    seq = run["levels"] + [run["last"]]
    for lv in seq:
        s = lv["s"]
        thr_list = [s * math.exp(-b_) for b_ in [P.b] + list(P.x[:-1])]
        ps = C.exceed(s)
        pt = [C.exceed(t) for t in thr_list]
        for M in C.suffix:
            # (V2): M p(s) <= K/(1-eta)  or  #{W > s} >= (1-eta) M p(s)
            if M * ps > K / (1 - eta) and C.count(M, s) < (1 - eta) * M * ps:
                return False
            # (V3): #{W > t} < K  or  #{W > t} <= (1+eta) M p(t)
            for t, p_t in zip(thr_list, pt):
                c = C.count(M, t)
                if c >= K and c > (1 + eta) * M * p_t:
                    return False
    return True


def check_run(run, vals, probs, s0, ell_ref, P, stats, mut=()):
    A = float((vals * probs).sum())
    lam, eta, b, K = P.lam, P.eta, P.b, P.K
    tol = 1 + 1e-9
    C = Counts(run["Widx"], vals, probs, K)
    exceed = C.exceed
    G = good_event(run, C, P)
    stats["good"] += int(G)
    stats["bad_event"] += int(not G)
    lower, upper = run["lower"], run["upper"]
    seq = run["levels"] + [run["last"]]
    fails = []
    # C2 width (deterministic), and its components
    if upper > P.width_bound * lower * tol:
        fails.append(("C2 width", math.log(upper / lower), math.log(P.width_bound)))
    negpart = sum(math.expm1(lam) * lv["s"] * lv["q"] for lv in run["levels"] if not lv["populated"])
    poppart = sum(math.expm1(lam) * lv["s"] * lv["q"] for lv in run["levels"] if lv["populated"])
    if negpart > P.etap * math.exp(b) * run["ell"] * tol:
        fails.append(("C2b negligible budget", negpart / (math.exp(b) * run["ell"]), P.etap))
    if "maxform" not in mut and poppart > math.exp(lam + b) * (1 + eta) / (1 - eta) * run["Lsum"] * tol:
        fails.append(("C2c populated part", poppart, run["Lsum"]))
    if s0 > (2 * P.pu) ** P.n * ell_ref * tol:
        fails.append(("C2d s0",))
    stats["widest"] = max(stats["widest"], math.log(upper / lower))
    stats["width_slack"] = min(stats["width_slack"], math.log(P.width_bound) - math.log(upper / lower))
    stats["neg_share"] = max(stats["neg_share"], negpart / (P.etap * math.exp(b) * run["ell"]))
    # C7 calls (deterministic): calls at accuracy x_l during level j <= #{i <= M_j : W_i > s_j e^{-x_{l-1}}}
    for jj, lv in enumerate(seq):
        for l in range(1, P.Lx + 1):
            if lv["calls"][l] > C.count(lv["M"], lv["s"] * math.exp(-P.x[l - 1]) * (1 - 1e-12)):
                fails.append(("C7 calls", jj, l))
    if G:
        if not (lower <= A * tol and A <= upper * tol):
            fails.append(("C1 validity", lower, A, upper))
        for jj, lv in enumerate(seq):
            s, M, q = lv["s"], lv["M"], lv["q"]
            if exceed(s) > q * tol:
                fails.append(("C3 q < p(s)", jj))
            if lv["populated"] and lv["pbar"] > exceed(s * math.exp(-b)) * tol:
                fails.append(("C3 pbar > p(s e^-b)", jj))
            if lv["ell_out"] > A * tol:
                fails.append(("C3 ell > A", jj))
            if M > max(K, 2 * lv["Mneg"]) * tol:
                fails.append(("C5 M > max(K, 2 Mneg)", jj))
            if lv["Mneg"] > (1 + eta) * math.exp(lam) * P.nu0 * P.Mdag * tol:
                fails.append(("C5 Mneg bound", jj, lv["Mneg"], (1 + eta) * math.exp(lam) * P.nu0 * P.Mdag))
            if M > P.Mbar * tol:
                fails.append(("C5 M > Mbar", jj))
            stats["largest_M_over_Mdag"] = max(stats["largest_M_over_Mdag"], M / P.Mdag)
            for l in range(0, P.Lx):
                x = P.x[l]
                lhs = lv["Mneg"] * exceed(s * math.exp(-x))
                rhs = P.nu * math.exp(lam) * (1 + eta) / (1 - eta) * math.exp(x)
                if lhs > rhs * tol:
                    fails.append(("C6 count lemma", jj, l, lhs, rhs))
                stats["tightest_count"] = max(stats["tightest_count"], lhs / rhs)
                c = C.count(M, s * math.exp(-x))
                if c > P.cnt(x) * tol:
                    fails.append(("C6 sample count", jj, l, c, P.cnt(x)))
            for l in range(1, P.Lx + 1):
                if lv["calls"][l] > min(M, P.cnt(P.x[l - 1])) * tol:
                    fails.append(("C8 calls bound", jj, l))
        # C4: every level that was LEFT (all but the last) has r(q_j) > r_dagger
        for jj, lv in enumerate(run["levels"]):
            if lv["r"] <= P.rdag:
                fails.append(("C4 closure radius", jj, lv["r"], P.rdag, "populated" if lv["populated"] else "negligible"))
            stats["populated" if lv["populated"] else "negligible"] += 1
        last = run["last"]
        key = "closed_empty" if last["r"] == -1 else ("closed_populated" if last["populated"] else "closed_unpopulated")
        stats[key] += 1
        stats["closing_radius"].append((last["r"], P.rdag, P.n_o))
        if any(not lv["populated"] for lv in run["levels"]):
            stats["runs_with_negligible_levels"] += 1
    stats["runs"] += 1
    stats["most_levels"] = max(stats["most_levels"], len(seq))
    stats["points"] = max(stats["points"], run["points"])
    return fails


def new_stats():
    return dict(runs=0, good=0, bad_event=0, widest=0.0, width_slack=math.inf, tightest_count=0.0, most_levels=0, points=0,
                largest_M_over_Mdag=0.0, populated=0, negligible=0, closed_empty=0, closed_populated=0, closed_unpopulated=0,
                closing_radius=[], skipped=0, neg_share=0.0, runs_with_negligible_levels=0)


# ---------------------------------------------------------------------------------------------------------------------
# instances
# ---------------------------------------------------------------------------------------------------------------------
def cube_dist(n):
    N = 2 ** n
    idx = np.arange(N)
    pop = np.array([bin(x).count("1") for x in range(N)], dtype=np.int16)
    return pop[idx[:, None] ^ idx[None, :]]


def rand_lipschitz(rng, n, u, D, kind):
    """u-Lipschitz functions on the n-cube: McShane upper / lower extensions of random data, mixtures, truncated cones,
    Lipschitz regularisation of noise, cone, flat."""
    N = D.shape[0]
    m = int(rng.integers(1, 9))
    idx = rng.choice(N, size=min(m, N), replace=False)
    scale = u * n * float(rng.choice([0.2, 0.5, 1.0, 2.0]))
    v = rng.uniform(0, scale, size=len(idx))
    if kind == 0:
        return (v[:, None] + u * D[idx, :]).min(0)
    if kind == 1:
        return (v[:, None] - u * D[idx, :]).max(0)
    if kind == 2:
        a_ = (v[:, None] + u * D[idx, :]).min(0)
        b_ = (v[::-1][:, None] - u * D[idx, :]).max(0)
        t = float(rng.uniform())
        return t * a_ + (1 - t) * b_
    if kind == 3:
        return u * np.minimum(D[int(rng.integers(N))], int(rng.integers(0, n + 1))).astype(float)
    if kind == 4:
        z = rng.normal(0, u * n * 0.3, size=N)
        return (z[:, None] + u * D).min(0)
    if kind == 5:
        return u * D[int(rng.integers(N))].astype(float)
    if kind == 6:
        return -u * np.maximum(int(rng.integers(1, n)) - D[int(rng.integers(N))], 0).astype(float)   # dip
    return np.zeros(N)


def radial_profile(rng, n_o, u, kind):
    """-ln W as a function of the outer distance d = 0..n_o (|increments| <= u)."""
    d = np.arange(n_o + 1)
    if kind == 0:
        F = np.zeros(n_o + 1)                                                # flat
    elif kind == 1:
        F = -u * np.maximum(int(rng.integers(1, max(2, n_o // 3))) - d, 0)   # dip / bump of random radius
    elif kind == 2:
        F = u * d.astype(float)                                              # cone
    elif kind == 3:
        F = u * np.minimum(d, int(rng.integers(1, max(2, n_o // 2)))).astype(float)   # cone flattened outside (mesa)
    elif kind == 4:
        F = u * np.maximum(d, int(rng.integers(1, max(2, n_o // 2)))).astype(float)   # cone with a flattened bottom
    elif kind == 5:
        F = np.concatenate([[0.0], np.cumsum(rng.uniform(-u, u, size=n_o))])  # random walk
    elif kind == 6:
        # "staircase": s p(s) constant over many levels:  W(d) = 1/|B(n_o, d)| where the ball grows by at most e^u per step
        lball = np.log(np.cumsum([math.comb(n_o, int(k)) for k in d], dtype=float))
        F = np.zeros(n_o + 1)
        for k in range(1, n_o + 1):
            F[k] = F[k - 1] + min(u, lball[k] - lball[k - 1])
    else:
        F = (u / 2) * (-1.0) ** d                                            # alternating
    return F.astype(float)


def binom_probs(n_o):
    return np.array([math.comb(n_o, k) for k in range(n_o + 1)], dtype=float) / 2.0 ** n_o


# ---------------------------------------------------------------------------------------------------------------------
def suite(rng, reps_cube, reps_radial, out, mut=(), verbose=True, max_points=16_000_000):
    stats = new_stats()
    allfails = []
    t0 = time.time()
    # (i) arbitrary Lipschitz functions on an enumerated cube, n = n_o + n_i
    n_o, n_i = 8, 4
    n = n_o + n_i
    D = cube_dist(n)
    for rep in range(reps_cube):
        u = float(rng.choice([0.5, 1.0, 2.0]))
        kind = rep % 8
        psi = rand_lipschitz(rng, n, u, D, kind) + float(rng.uniform(-3, 3))
        if np.max(np.abs(psi[:, None] - psi[None, :]) - u * D) > 1e-9:
            allfails.append(("instance not Lipschitz", kind)); continue
        vals = np.sort(np.exp(-psi).reshape(2 ** n_o, 2 ** n_i).mean(axis=1))   # outer coordinates = high bits
        probs = np.full(2 ** n_o, 2.0 ** -n_o)
        psi0 = float(psi[0])
        s0 = math.exp(-psi0 - u * n)
        ell_ref = math.exp(-psi0) * ((1 + math.exp(-u)) / 2) ** n
        b = min(float(rng.choice([0.25, 0.5, 1.0, 3.0])), 0.9 * 2 * u * n_i)   # bounded tolerances, and one 'large' one
        lam = float(rng.choice([0.25, 0.5, 1.0]))
        eta = float(rng.choice([0.25, 0.5]))
        etap = float(rng.choice([0.1, 0.5, 1.0]))
        theta = float(rng.choice([0.1, 0.5, 2.0, 20.0]))
        nu1 = None if rng.uniform() < 0.5 else 1.0                               # bounded-regime value 2 e^u n_o/theta, or 1
        lam *= float(rng.uniform(0.9, 1.0))                                      # no exact ties between values and levels
        ladder = [x for x in np.arange(2 * u * n_i - 1.0, b, -1.0) * float(rng.uniform(0.95, 1.0)) if x > b] + [b * (1 - 1e-9)]
        P = Params(n, n_o, u, lam, eta, etap, theta, b, ladder, delta=0.05, nu1=nu1)
        run = run_2L(rng, vals, probs, s0, ell_ref, P, mode=rep % 5, mut=mut, max_points=max_points)
        if "error" in run:
            if run["error"].startswith("sample too large"):
                stats["skipped"] += 1; continue
            allfails.append(("cube", kind, run["error"])); continue
        f = check_run(run, vals, probs, s0, ell_ref, P, stats, mut=mut)
        if f:
            allfails.append(("cube", kind, rep % 5, f[:3]))
    # (ii) radial outer landscapes (exact binomial law of the outer distance), nominal inner dimension n_i
    for rep in range(reps_radial):
        u = float(rng.choice([0.5, 1.0, 2.0]))
        n_o = int(rng.choice([12, 16, 20, 24] if u >= 1.0 else [16, 24, 32, 40]))
        n_i = int(rng.choice([2, 6]))
        n = n_o + n_i
        kind = rep % 8
        F = radial_profile(rng, n_o, u, kind) + float(rng.uniform(-2, 2))
        dref = int(rng.integers(0, n_o + 1))                                 # outer distance of the reference point
        psi0 = float(F[dref])
        order = np.argsort(np.exp(-F), kind="stable")
        vals = np.exp(-F)[order]
        probs = binom_probs(n_o)[order]
        s0 = math.exp(-psi0 - u * n)
        ell_ref = math.exp(-psi0) * ((1 + math.exp(-u)) / 2) ** n
        b = min(float(rng.choice([0.25, 0.5, 1.0, 3.0])), 0.9 * 2 * u * n_i)   # bounded tolerances, and one 'large' one
        lam = float(rng.choice([0.25, 0.5, 1.0]))
        eta = float(rng.choice([0.25, 0.5]))
        etap = float(rng.choice([0.1, 0.5, 1.0]))
        theta = float(rng.choice([0.1, 0.5, 2.0, 20.0]))
        nu1 = None if rng.uniform() < 0.5 else 1.0
        lam *= float(rng.uniform(0.9, 1.0))
        targeted = (rep % 4 == 3)                                                # part (iii): negligible levels are left
        if targeted:
            # nu1 = 1, eta' = 1 and theta such that the [N]-threshold theta (1-eta) nu0 lies between Gt(r1 - 1) and Gt(r1),
            # r1 = the radius reached at the negligibility threshold of the first level above a flat bulk: that level
            # cannot be closed and is left as negligible; closure follows one or two radii further down.
            u, n_o = [(2.0, 40), (2.0, 36), (1.5, 44)][int(rng.integers(3))]
            n = n_o + n_i
            kind = int(rng.choice([0, 1, 3]))
            F = radial_profile(rng, n_o, u, kind) + float(rng.uniform(-2, 2))
            dref = int(rng.integers(0, n_o + 1))
            psi0 = float(F[dref])
            order = np.argsort(np.exp(-F), kind="stable")
            vals = np.exp(-F)[order]
            probs = binom_probs(n_o)[order]
            s0 = math.exp(-psi0 - u * n)
            ell_ref = math.exp(-psi0) * ((1 + math.exp(-u)) / 2) ** n
            etap, eta = 1.0, 0.5
            J_ = math.ceil((2 * u * n + b + n_o * math.log(2)) / lam)
            nu0_ = (J_ + 1) * math.expm1(lam) / (1 - eta)
            tab_ = Tables(n_o, u, eta)
            r1 = tab_.radius(1 / ((1 - eta) * nu0_ * 3.0))
            theta, nu1 = None, math.sqrt(tab_.Gt[r1 - 1] * tab_.Gt[r1])           # Params turns this into theta, with nu1 = 1
        top = 2 * u * n_i
        jit = float(rng.uniform(0.95, 1.0))
        ladder = [x * jit for x in (top / 2, top / 4, 8.0, 4.0, 2.0, 1.0) if b < x * jit < top]
        ladder = sorted(set(ladder), reverse=True) + [b * (1 - 1e-9)]
        P = Params(n, n_o, u, lam, eta, etap, theta, b, ladder, delta=0.05, nu1=nu1)
        theta = P.theta
        run = run_2L(rng, vals, probs, s0, ell_ref, P, mode=(rep // 8) % 5, mut=mut, max_points=max_points)
        if "error" in run:
            if run["error"].startswith("sample too large"):
                stats["skipped"] += 1; continue
            allfails.append(("radial", kind, run["error"])); continue
        f = check_run(run, vals, probs, s0, ell_ref, P, stats, mut=mut)
        if f:
            allfails.append(("radial", kind, (rep // 8) % 5, dict(u=u, n_o=n_o, b=b, lam=lam, eta=eta, theta=theta, nu1=nu1), f[:3]))
    cr = stats.pop("closing_radius")
    stats["closed_by_tail_lemma_at_r<=n_o-2"] = sum(1 for (r, rd, no) in cr if 0 <= r <= no - 2)
    stats["closed_at_r<=r_dagger"] = sum(1 for (r, rd, no) in cr if 0 <= r <= rd)
    stats["seconds"] = round(time.time() - t0, 1)
    for key in ("widest", "width_slack", "tightest_count", "largest_M_over_Mdag", "neg_share"):
        stats[key] = round(stats[key], 4)
    if verbose:
        out(f"  stats: {stats}")
        out(f"  failures: {len(allfails)}" + ("" if not allfails else f"   first: {allfails[:3]}"))
    return stats, allfails


def fail_kinds(fl):
    kinds = set()
    for item in fl:
        last = item[-1]
        if isinstance(last, list):
            for f0 in last:
                kinds.add(f0[0])
        else:
            kinds.add(str(last))
    return sorted(kinds)


def main():
    lines = []
    def out(s=""):
        print(s); lines.append(s); sys.stdout.flush()
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "seed" else 20261125
    rc, rr = (24, 40) if quick else (120, 320)
    mp = 4_000_000 if quick else 16_000_000
    out(f"Algorithm 2L+ with the constants of Theorem K1 (K, nu, J from the formulas; delta = 0.05); seed {seed}")
    rng = np.random.default_rng(seed)
    stats, fails = suite(rng, rc, rr, out, max_points=mp)
    ok = (len(fails) == 0 and stats["populated"] > 0 and stats["negligible"] > 0 and stats["closed_by_tail_lemma_at_r<=n_o-2"] > 0
          and stats["closed_populated"] > 0 and stats["closed_unpopulated"] > 0)
    out(f"main suite passed (no failure; populated and negligible levels occur; closures at populated and at unpopulated levels occur): {ok}")
    if seed != 20261125:                                   # a second seed: main suite only, no mutations
        open(f"out_sim_outer_loop_seed{seed}.txt", "w").write("\n".join(lines) + "\n")
        return ok
    # mutations: each must be detected by the check that it is meant to break
    out("\nmutations (each must produce failures of the stated kind):")
    rcm, rrm = (24, 40) if quick else (48, 120)
    for mut, expect in ((("maxform",), "C2 width"), (("noharper",), "C4 closure radius"), (("close_at_no",), "C1 validity"),
                        (("neg_tol",), "C6 count lemma"), (("q_plain",), "C3 q < p(s)")):
        rng = np.random.default_rng(7)
        st, fl = suite(rng, rcm, rrm, out, mut=mut, verbose=False, max_points=4_000_000)
        kinds = fail_kinds(fl)
        hit = any(expect in k for k in kinds)
        out(f"  mutation {mut[0]:12s}: {len(fl):4d} failing runs of {st['runs']}, kinds {kinds}   expected '{expect}': {'DETECTED' if hit else 'not detected'}")
        ok = ok and hit
    out(f"\nall as expected: {ok}")
    open("out_sim_outer_loop.txt" if not quick else "out_sim_outer_loop_quick.txt", "w").write("\n".join(lines) + "\n")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
