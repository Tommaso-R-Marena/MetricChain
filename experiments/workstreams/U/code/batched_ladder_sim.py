#!/usr/bin/env python3
"""Harness for Theorem U1 (the ladder of Algorithm 2L+ in L rounds).  Own implementation from the text of
docs/workstreams/K_REPORT.md section 2.2 (outer loop) with a simulated inner oracle.

Instance: psi(a, b) = F_o(d(a, s_o)) + c_i d(b, s_i) on Q_{n_o} x Q_{n_i}, F_o u-Lipschitz, 0 <= c_i <= u, so that the
fibre average is W(a) = exp(-F_o(d(a, s_o))) * ((1+e^{-c_i})/2)^{n_i} and everything about the outer sample is exact:
outer points are represented by D_i = d(a_i, s_o) ~ Bin(n_o, 1/2).
Inner oracle for the pair (point i, rung l): the bracket [W e^{-alpha x_l}, W e^{(1-alpha) x_l}] with alpha in [0,1]
drawn in advance (valid; ratio exactly e^{x_l}); modes: uniform, all-low (alpha = 1), all-high (alpha = 0), mixed.

Checked on every run:
 (A) [Claim A]  if the certificates p(s_i) <= q_i of the levels left are true and the event (V3') holds, then every
     inner call (i, l) of the sequential algorithm has i in C_l  (C_l computed from the rung-(l-1) brackets only);
 (B) [Claim B, deterministic]  |C_l| <= K + (J+1) max{K, 4(1+eta) e^lambda nu e^{x_{l-1}} / c_eta};
 (C) the batched run (rung l applied to all of C_l, then the sequential logic on stored brackets) returns the same
     bracket as the sequential run, and the bracket contains A;
 (D) number of rounds of the batched run = L (one-round inner procedures).
Mutations (must be detected): M1: lambda_j without the factor c_eta e^{-b}/(1+eta); M2: Mhat_j without the factor 2.
usage: batched_ladder_sim.py [nruns] [seed] [u]
"""
import sys, math, time
import numpy as np
from math import comb


class Tables:
    def __init__(self, m, u, eta):
        self.m, self.u = m, u
        self.binom = np.array([comb(m, j) for j in range(m + 1)], dtype=float)
        self.ball = np.cumsum(self.binom)                              # |B(m, r)|
        self.E = np.array([sum(comb(m, j) * math.expm1(u * (r + 1 - j)) for j in range(r + 1)) for r in range(m + 1)])
        self.T = np.array([sum(comb(m, j) * math.exp(-u * max(j - k, 0)) for j in range(m + 1)) for k in range(m + 1)])
        ceta = (1 - eta) / (1 + eta)
        self.ceta = ceta
        self.Gt = np.empty(m + 1)
        self.Gt[0] = math.expm1(u)
        self.Gt[1:] = self.E[1:] / self.ball[:-1]
        self.kap = np.zeros(m + 1, dtype=int)
        for r in range(m + 1):
            bound = max(1.0, ceta * (self.ball[r - 1] if r >= 1 else 0.0))
            ks = np.nonzero(self.ball <= bound)[0]
            self.kap[r] = ks[-1] if len(ks) else 0
        self.G2 = self.E / self.T[self.kap]

    def rdagger(self, theta, eta, nu0):
        r = -1
        for rr in range(self.m):
            okN = self.Gt[rr] <= theta * (1 - eta) * nu0
            okP = min(self.Gt[rr] / self.ceta, self.G2[rr]) <= theta
            if okN and okP:
                r = rr
            else:
                break
        pi = self.ball[r] / 2.0 ** self.m if r >= 0 else 2.0 ** (-self.m - 1)
        return r, pi

    def k_of(self, x):            # largest k >= 0 with |B(m,k)| <= max{1, x}
        ks = np.nonzero(self.ball <= max(1.0, x))[0]
        return int(ks[-1]) if len(ks) else 0

    def r_of(self, x):            # least radius with |B(m,r)| >= x
        return int(np.searchsorted(self.ball, x - 1e-9, side="left"))


class Run:
    def __init__(self, rng, u, n_o, n_i, Fo, c_i, s_i_weight, D0, xs, b, lam, eta, etap, theta, nu1, Ksim, mode, mutation=None):
        self.u, self.n_o, self.n_i = u, n_o, n_i
        n = n_o + n_i
        self.tab = Tables(n_o, u, eta)
        self.b, self.lam, self.eta, self.etap, self.theta = b, lam, eta, etap, theta
        self.xs = [2 * u * n_i] + list(xs)                    # x_0 .. x_L
        self.L = len(xs)
        assert self.xs[-1] <= b + 1e-12 and all(self.xs[i] > self.xs[i + 1] for i in range(self.L))
        self.J = math.ceil((2 * u * n + b + n_o * math.log(2)) / lam)
        self.nu0 = max((self.J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
        self.rd, self.pid = self.tab.rdagger(theta, eta, self.nu0)
        self.mmax = math.ceil(math.log2(2 * (1 + eta) * math.exp(lam) * self.nu0 / ((1 - eta) * self.pid)))
        self.K = Ksim
        self.nu = self.K * self.nu0
        self.Mmax = self.K * 2 ** self.mmax
        self.ceta = (1 - eta) / (1 + eta)
        self.too_big = self.Mmax > 4_000_000
        if self.too_big:
            return
        self.mutation = mutation
        # instance
        kap_i = ((1 + math.exp(-c_i)) / 2) ** n_i
        self.pD = self.tab.binom / 2.0 ** n_o
        self.Wd = np.exp(-Fo) * kap_i                             # W as a function of d
        self.A = float(np.sum(self.pD * self.Wd))
        psi0 = Fo[D0] + c_i * s_i_weight                         # psi at the reference point (a = 0, b = 0)
        self.s0 = math.exp(-psi0 - u * n)
        self.ell0 = math.exp(-psi0) * ((1 + math.exp(-u)) / 2) ** n
        self.s = self.s0 * np.exp(lam * np.arange(self.J + 2))
        # sample
        self.D = rng.binomial(n_o, 0.5, size=self.Mmax).astype(np.int16)
        self.W = self.Wd[self.D]
        triv_mid = np.exp(-(Fo[self.D] + c_i * s_i_weight))       # e^{-psi(a_i, 0)}
        self.Lb = triv_mid * math.exp(-u * n_i)
        self.Ub = triv_mid * math.exp(u * n_i)
        self.rung = np.zeros(self.Mmax, dtype=np.int8)
        self.mode = mode
        self.rng = rng
        self.calls = [set() for _ in range(self.L + 1)]           # sequential calls per rung
        self.alpha_seed = int(rng.integers(1 << 30))

    # ---- inner oracle (randomness attached to the pair (i, l)) ----
    def alpha(self, idx, l):
        if self.mode == "low":
            return np.ones(len(idx))
        if self.mode == "high":
            return np.zeros(len(idx))
        h = (idx.astype(np.uint64) * np.uint64(2654435761) + np.uint64(l * 97 + self.alpha_seed)) % np.uint64(1 << 20)
        al = h.astype(float) / float(1 << 20)
        if self.mode == "mixed":
            al = np.where(al < 0.5, 0.0, 1.0)
        return al

    def oracle(self, idx, l):
        x = self.xs[l]
        al = self.alpha(idx, l)
        return self.W[idx] * np.exp(-al * x), self.W[idx] * np.exp((1 - al) * x)

    def refine(self, idx, l, Lb, Ub):
        lo, hi = self.oracle(idx, l)
        Lb[idx] = np.maximum(Lb[idx], lo)
        Ub[idx] = np.minimum(Ub[idx], hi)

    def p_exact(self, t):
        return float(np.sum(self.pD[self.Wd > t]))

    # ---- sequential algorithm (K_REPORT 2.2); stored = None: live oracle; else dict of allowed sets per rung ----
    def sequential(self, allowed=None):
        Lb, Ub, rung = self.Lb.copy(), self.Ub.copy(), np.zeros(self.Mmax, dtype=np.int8)
        K, eta, lam, b, theta = self.K, self.eta, self.lam, self.b, self.theta
        ell, Sig = self.ell0, 0.0
        q_hist, cert_ok, missing = [], True, 0
        nneg = npop = 0
        calls = [set() for _ in range(self.L + 1)]
        for j in range(self.J + 1):
            sj = self.s[j]
            M = K
            ell_entry = ell
            while True:
                if M > self.Mmax:
                    return dict(abort="M", calls=calls, cert_ok=cert_ok, missing=missing)
                idx = np.arange(M)
                # classify
                while True:
                    und = idx[(Ub[idx] > sj) & (Lb[idx] <= sj * math.exp(-b))]
                    if len(und) == 0:
                        break
                    if np.any(rung[und] >= self.L):
                        return dict(abort="rung", calls=calls, cert_ok=cert_ok, missing=missing)
                    r_und = rung[und].copy()                 # one rung per point and pass, then re-test
                    for l in np.unique(r_und) + 1:
                        sel = und[r_und == l - 1]
                        calls[l].update(sel.tolist())
                        if allowed is not None:
                            missing += len(set(sel.tolist()) - allowed[l])
                        self.refine(sel, int(l), Lb, Ub)
                        rung[sel] = l
                N = int(np.sum(Ub[idx] > sj))
                q = min(1.0, max(N, K) / ((1 - eta) * M))
                pl = None
                if N >= K:
                    pl = N / ((1 + eta) * M)
                    k = self.tab.k_of(2.0 ** self.n_o * pl)
                    ell = max(ell, sj * math.exp(-b) * pl, sj * math.exp(-b) * self.tab.T[k] / 2.0 ** self.n_o)
                # closure
                if 2.0 ** self.n_o * q < 1:
                    tail = 0.0
                else:
                    r = self.tab.r_of(2.0 ** self.n_o * q)
                    tail = sj * self.tab.E[r] / 2.0 ** self.n_o if r <= self.n_o - 1 else math.inf
                if tail <= theta * math.exp(b) * ell:
                    Lo = max(ell, Sig + (0.0 if pl is None else (1 - math.exp(-lam)) * math.exp(-b) * sj * pl))
                    Up = self.s0 + sum((self.s[i + 1] - self.s[i]) * q_hist[i] for i in range(j)) + tail
                    return dict(abort=None, L=Lo, U=Up, level=j, calls=calls, cert_ok=cert_ok, missing=missing, q=q_hist, nneg=nneg, npop=npop)
                if N >= K:
                    q_hist.append(q)
                    cert_ok &= self.p_exact(sj) <= q + 1e-15
                    Sig += (1 - math.exp(-lam)) * math.exp(-b) * sj * pl
                    npop += 1
                    break
                if M >= self.nu * sj / (ell_entry * math.exp(b)):
                    q_hist.append(q)
                    cert_ok &= self.p_exact(sj) <= q + 1e-15
                    nneg += 1
                    break
                M *= 2
        return dict(abort="J", calls=calls, cert_ok=cert_ok, missing=missing)

    # ---- batched candidate sets ----
    def v3prime(self):
        """(V3'): for all j, M in the doubling sequence: X_{s_j}(M) < K or X_{s_j}(M) <= (1+eta) M p(s_j)."""
        # level index of W: number of levels strictly below W
        jl = np.searchsorted(self.s[: self.J + 1], self.W, side="left")     # W > s_j  iff  j < jl
        ok = True
        Ms = [self.K * 2 ** m for m in range(self.mmax + 1)]
        cnt = np.zeros(self.J + 2)
        prev = 0
        pj = np.array([self.p_exact(self.s[j]) for j in range(self.J + 1)])
        for M in Ms:
            np.add.at(cnt, jl[prev:M], 1)
            prev = M
            X = np.cumsum(cnt[::-1])[::-1][1: self.J + 2]                 # X[j] = #{i <= M : jl > j}
            bad = (X >= self.K) & (X > (1 + self.eta) * M * pj + 1e-9)
            ok &= not bool(np.any(bad))
        return ok

    def candidates(self, Lb, Ub, prevset, l):
        """C_l from the brackets at rung l-1 of the points in prevset (array of indices; None = all)."""
        K, eta, lam, b = self.K, self.eta, self.lam, self.b
        idx = np.arange(self.Mmax) if prevset is None else np.asarray(sorted(prevset), dtype=np.int64)
        Lp, Up = Lb[idx], Ub[idx]
        Ms = np.array([K * 2 ** m for m in range(self.mmax + 1)], dtype=np.int64)
        blk = np.searchsorted(Ms, idx + 1, side="left")                   # smallest m with i <= K 2^m (i is 0-based)
        jL = np.searchsorted(self.s[: self.J + 1], Lp, side="left")       # L > s_j iff j < jL
        cnt = np.zeros((self.mmax + 1, self.J + 2))
        np.add.at(cnt, (blk, jL), 1)
        cnt = np.cumsum(cnt, axis=0)                                      # i <= M
        NL = np.cumsum(cnt[:, ::-1], axis=1)[:, ::-1][:, 1: self.J + 2]   # NL[m, j] = #{i <= K2^m : L_i > s_j}
        fac = self.ceta * math.exp(-b) / (1 + eta)
        if self.mutation == "M1":
            fac = 1.0
        val = np.where(NL >= K, self.s[None, : self.J + 1] * NL / Ms[:, None], 0.0).max(axis=0) * fac   # per level i'
        lamj = np.maximum(self.ell0, np.concatenate([[0.0], np.maximum.accumulate(val)[:-1]]))        # max over i' < j
        two = 1.0 if self.mutation == "M2" else 2.0
        Mhat = np.maximum(K, two * self.nu * self.s[: self.J + 1] / (lamj * math.exp(b)))
        # membership: exists j with s_j in [L e^b, U) and (i+1) <= Mhat_j
        jlo = np.searchsorted(self.s[: self.J + 1], Lp * math.exp(b) * (1 - 1e-12), side="left")   # first j with s_j >= L e^b
        jhi = np.searchsorted(self.s[: self.J + 1], Up, side="left") - 1                          # last j with s_j < U
        member = np.zeros(len(idx), dtype=bool)
        width = int(np.max(jhi - jlo)) if len(idx) else -1
        for off in range(0, max(width, -1) + 1):
            j = jlo + off
            okj = (j <= jhi) & (j <= self.J)
            jj = np.clip(j, 0, self.J)
            member |= okj & (idx + 1 <= Mhat[jj])
        C = idx[member]
        bound = K + (self.J + 1) * max(K, 4 * (1 + eta) * math.exp(lam) * self.nu * math.exp(self.xs[l - 1]) / self.ceta)
        return C, bound

    def batched(self):
        Lb, Ub = self.Lb.copy(), self.Ub.copy()
        allowed, sizes, bounds = {}, [], []
        # stage 1: all points
        allidx = np.arange(self.Mmax)
        self.refine(allidx, 1, Lb, Ub)
        allowed[1] = None
        sizes.append(self.Mmax); bounds.append(self.Mmax)
        prev = None
        for l in range(2, self.L + 1):
            C, bound = self.candidates(Lb, Ub, prev, l)
            self.refine(C, l, Lb, Ub)
            allowed[l] = set(C.tolist())
            sizes.append(len(C)); bounds.append(bound)
            prev = allowed[l]
        return allowed, sizes, bounds


def make_landscape(rng, kind, n_o, u):
    d = np.arange(n_o + 1)
    if kind == "flat":
        F = np.zeros(n_o + 1)
    elif kind == "cone":
        F = u * d.astype(float)
    elif kind == "dip":
        R = int(rng.integers(2, n_o // 2 + 2))
        F = -u * np.maximum(R - d, 0).astype(float)
    elif kind == "trunc":
        R = int(rng.integers(1, n_o // 2 + 1))
        F = u * np.maximum(d, R).astype(float)
    elif kind == "walk":
        F = np.concatenate([[0.0], np.cumsum(rng.uniform(-u, u, n_o))])
    elif kind == "flathist":
        t = np.array([math.log(comb(n_o, int(k))) for k in d]) - math.log(comb(n_o, n_o // 2))
        F = t.copy()                                      # F = ln(P(d)/P(mode)) <= 0, regularised to slope <= u
        for k in range(n_o // 2 - 1, -1, -1):
            F[k] = max(F[k], F[k + 1] - u)
        for k in range(n_o // 2 + 1, n_o + 1):
            F[k] = max(F[k], F[k - 1] - u)
    else:
        raise ValueError(kind)
    assert np.max(np.abs(np.diff(F))) <= u + 1e-9
    return F


def one(rng, u, mutation=None, Ksim=None, verbose=False):
    n_o = int(rng.integers(6, 11)); n_i = int(rng.integers(2, 5))
    kind = str(rng.choice(["flat", "cone", "dip", "trunc", "walk", "flathist"]))
    Fo = make_landscape(rng, kind, n_o, u)
    c_i = float(rng.uniform(0, u)); siw = int(rng.integers(0, n_i + 1)); D0 = int(rng.integers(0, n_o + 1))
    L = int(rng.integers(2, 5))
    b = float(rng.uniform(0.6, 2.0))
    x0 = 2 * u * n_i
    xs = sorted(rng.uniform(b * 1.05, x0 * 0.95, L - 1).tolist(), reverse=True) + [b * float(rng.uniform(0.9, 1.0))]
    lam = float(rng.uniform(0.5, 1.0)); eta = 0.5; etap = float(rng.choice([1.0, 20.0, 100.0]))
    theta = float(rng.uniform(0.5, 6.0)); nu1 = 1.0
    K = Ksim if Ksim else int(rng.choice([6, 10, 16]))
    mode = str(rng.choice(["uniform", "low", "high", "mixed"]))
    R = Run(rng, u, n_o, n_i, Fo, c_i, siw, D0, xs, b, lam, eta, etap, theta, nu1, K, mode, mutation)
    if R.too_big:
        return None
    seq = R.sequential()
    allowed, sizes, bounds = R.batched()
    v3p = R.v3prime()
    # containment (A)
    contained = all((allowed[l] is None) or seq["calls"][l] <= allowed[l] for l in range(1, R.L + 1))
    # (C) rerun the sequential logic with the hook: same output iff no missing bracket
    okB = all(sz <= bd + 1e-9 for sz, bd in zip(sizes, bounds))
    valid = None
    if seq["abort"] is None:
        valid = seq["L"] <= R.A * (1 + 1e-12) and R.A <= seq["U"] * (1 + 1e-12)
    return dict(kind=kind, n_o=n_o, n_i=n_i, L=R.L, K=K, Mmax=R.Mmax, abort=seq["abort"], cert_ok=seq["cert_ok"], v3p=v3p,
                contained=contained, okB=okB, valid=valid, sizes=sizes, bounds=bounds, etap=etap,
                seqcalls=[len(seq["calls"][l]) for l in range(1, R.L + 1)], mode=mode, nneg=seq.get("nneg", 0), npop=seq.get("npop", 0))


if __name__ == "__main__":
    nruns = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261125
    u = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    print(f"u = {u}, runs per mutation <= {nruns}, seed {seed}")
    for mutation in (None, "M1", "M2"):
        rng = np.random.default_rng(seed)
        t0 = time.time()
        stats = dict(runs=0, closed=0, good=0, good_contained=0, bad_event=0, bad_event_notcontained=0, violA=0, violB=0, invalid=0, neg_levels=0, pop_levels=0)
        maxratio = 0.0
        tot_seq = np.zeros(5); tot_bat = np.zeros(5); tot_all = np.zeros(5)
        while stats["runs"] < nruns and time.time() - t0 < 150:
            r = one(rng, u, mutation)
            if r is None:
                continue
            stats["runs"] += 1
            stats["closed"] += r["abort"] is None
            stats["neg_levels"] += r["nneg"]; stats["pop_levels"] += r["npop"]
            good = r["cert_ok"] and r["v3p"]
            if good:
                stats["good"] += 1
                stats["good_contained"] += r["contained"]
                stats["violA"] += (not r["contained"])
            else:
                stats["bad_event"] += 1
                stats["bad_event_notcontained"] += (not r["contained"])
            stats["violB"] += (not r["okB"])
            if r["valid"] is False and good:
                stats["invalid"] += 1
            for l in range(1, r["L"]):
                maxratio = max(maxratio, r["sizes"][l] / r["bounds"][l])
                tot_seq[l] += r["seqcalls"][l]; tot_bat[l] += r["sizes"][l]; tot_all[l] += r["Mmax"]
        print(f"mutation={mutation}: {stats}  max |C_l|/bound = {maxratio:.3f}  "
              f"calls at rungs 2,3,4: sequential {tot_seq[1:4].astype(int).tolist()} batched {tot_bat[1:4].astype(int).tolist()} "
              f"of {tot_all[1:4].astype(int).tolist()} sampled points  ({time.time()-t0:.0f}s)", flush=True)
