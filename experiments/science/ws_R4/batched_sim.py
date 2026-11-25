#!/usr/bin/env python3
"""R4 (SCI-REV-0003) -- Theorem 11.84 (a ladder is as many rounds as it has rungs), Claims A and B,
tested against my own implementation of Algorithm 2L+ as written in K_REPORT.md section 2.2
(= theory report Theorem 11.56) and of the batched schedule B2L+ as written in section 11.24.

Own code.  (The coordinator has no script for Theorem 11.84; the workstream's harness
`batched_ladder_sim.py` was NOT read before this file was written.)

Set-up of a run
  * product instance psi(a,b) = F_o(d(a,s_o)) + c_i d(b,s_i) on Q_{n_o} x Q_{n_i}: the fibre
    average is W(a) = exp(-F_o(d_a)) ((1+e^{-c_i})/2)^{n_i}, a function of d_a ~ Bin(n_o,1/2);
  * simulated inner oracle: the potential call (i,l) returns [W e^{-alpha x_l}, W e^{(1-alpha) x_l}],
    alpha = alpha(i,l) drawn in advance (uniform / all 0 / all 1 / mixed) -- a valid bracket of
    ratio exactly e^{x_l}; brackets are intersected;
  * all constants as in section 2.2 except K (reduced, so that samples fit in memory) and eta'
    (enlarged in some runs, so that negligible levels occur and the selection is not vacuous).

Checked on every run
  (S)  sanity of my 2L+: if it stops through the closure test, L <= A <= U on the good event and
       U <= e^{x_out} L always (Theorem 11.56);
  (A)  Claim A: on the good event G' = (V2) & (V3) & (V3') (V1 holds by construction) every call
       (i,l), l >= 2, of the sequential algorithm has i in C_l;
  (B)  Claim B: |C_l| <= N_l = K + (J+1) max{K, 4(1+eta) c_eta^-1 e^lambda nu e^{x_{l-1}}}, in EVERY run;
  (R)  the batched schedule asks rung l only on C_l and the replay never needs a missing bracket
       (equivalent to (A)), so the number of adaptive stages is L.
Two mutations of the schedule (lambda_j without the factor c_eta e^-b/(1+eta); M-hat_j without the
factor 2) are run on the same samples; they should violate (A) in some runs.
"""
import math
import sys
import numpy as np
from math import comb


class Tables:
    def __init__(self, m, u, eta):
        self.m, self.u = m, u
        j = np.arange(m + 1)
        self.binom = np.array([float(comb(m, int(x))) for x in j])
        self.ball = np.cumsum(self.binom)                                  # |B(m,r)|
        self.E = np.array([np.sum(self.binom[:r + 1] * (np.exp(u * (r + 1 - j[:r + 1])) - 1.0))
                           for r in range(m + 1)])                         # E_r(m)
        self.T = np.array([np.sum(self.binom * np.exp(-u * np.clip(j - k, 0, None)))
                           for k in range(m + 1)])                         # T_m(k)
        self.c_eta = (1 - eta) / (1 + eta)
        self.Gt = np.empty(m + 1)
        self.Gt[0] = math.exp(u) - 1.0
        for r in range(1, m + 1):
            self.Gt[r] = self.E[r] / self.ball[r - 1]
        self.kappa = np.zeros(m + 1, dtype=int)
        for r in range(m + 1):
            bound = max(1.0, self.c_eta * (self.ball[r - 1] if r >= 1 else 0.0))
            self.kappa[r] = self.largest_k(bound)
        self.G2 = self.E / self.T[self.kappa]

    def largest_k(self, x):
        """largest k >= 0 with |B(m,k)| <= max{1, x}"""
        bound = max(1.0, x)
        ks = np.nonzero(self.ball <= bound * (1 + 1e-12))[0]
        return int(ks[-1]) if len(ks) else 0

    def least_r(self, x):
        """least radius r with |B(m,r)| >= x   (x <= 2^m)"""
        return int(np.searchsorted(self.ball, x * (1 - 1e-12), side="left"))

    def r_dagger(self, theta, nu0, eta):
        r = -1
        for rp in range(0, self.m):
            if self.Gt[rp] <= theta * (1 - eta) * nu0 and min(self.Gt[rp] / self.c_eta, self.G2[rp]) <= theta:
                r = rp
            else:
                break
        return r


def outer_profile(kind, m, u, rng):
    d = np.arange(m + 1, dtype=float)
    if kind == "flat":
        F = np.zeros(m + 1)
    elif kind == "cone":
        F = u * d
    elif kind == "dip":
        R = int(rng.integers(1, max(2, m // 2 + 1)))
        F = -u * np.clip(R - d, 0, None)
    elif kind == "trunc":
        R = int(rng.integers(1, max(2, m // 2 + 1)))
        F = u * np.maximum(d, R)
    elif kind == "walk":
        F = np.concatenate([[0.0], np.cumsum(rng.uniform(-u, u, size=m))])
    elif kind == "flathist":
        lp = np.array([math.lgamma(m + 1) - math.lgamma(x + 1) - math.lgamma(m - x + 1) for x in range(m + 1)])
        t = lp.max() - lp
        for i in range(1, m + 1):
            t[i] = min(t[i], t[i - 1] + u)
        for i in range(m - 1, -1, -1):
            t[i] = min(t[i], t[i + 1] + u)
        F = -t
    else:
        raise ValueError(kind)
    return F


class Run:
    def __init__(self, u, n_o, n_i, lam, eta, etap, theta, nu1, xs, Ksmall, kind, alpha_mode, delta, rng,
                 max_points=1_500_000):
        self.ok = False
        self.u, self.n_o, self.n_i = u, n_o, n_i
        n = n_o + n_i
        self.n = n
        self.lam, self.eta, self.etap, self.theta, self.nu1 = lam, eta, etap, theta, nu1
        self.xs = np.array([2 * u * n_i] + list(xs), dtype=float)        # x_0 > x_1 > ... > x_L
        assert np.all(np.diff(self.xs) < 0)
        self.L = len(xs)
        # tolerance b: the theorem needs x_L <= b; a hair above x_L avoids the floating-point tie at
        # the last rung that referee R8 recorded (a point exactly on a threshold stays unclassified)
        self.b = float(self.xs[-1]) * (1 + 1e-9) + 1e-12
        self.tab = Tables(n_o, u, eta)
        tab = self.tab
        self.c_eta = tab.c_eta
        self.J = math.ceil((2 * u * n + self.b + n_o * math.log(2)) / lam)
        self.nu0 = max((self.J + 1) * (math.exp(lam) - 1) / etap, nu1) / (1 - eta)
        self.rdag = tab.r_dagger(theta, self.nu0, eta)
        self.pidag = tab.ball[self.rdag] / 2.0 ** n_o if self.rdag >= 0 else 2.0 ** (-n_o - 1)
        self.m_max = math.ceil(math.log2(2 * (1 + eta) * math.exp(lam) * self.nu0 / ((1 - eta) * self.pidag)))
        self.K = Ksmall
        self.nu = self.K * self.nu0
        self.Mdag = self.K / ((1 - eta) * self.pidag)
        self.Mbar = 2 * (1 + eta) * math.exp(lam) * self.nu0 * self.Mdag
        self.M_max = self.K * 2 ** self.m_max
        if self.M_max > max_points:
            return
        self.sizes = [self.K * 2 ** m for m in range(self.m_max + 1)]
        # instance
        c_i = float(rng.uniform(0, u))
        s_o_weight = int(rng.integers(0, n_o + 1))       # d(0, s_o)
        s_i_weight = int(rng.integers(0, n_i + 1))       # d(0, s_i)
        Fo = outer_profile(kind, n_o, u, rng)
        self.Fo = Fo
        inner = ((1 + math.exp(-c_i)) / 2.0) ** n_i
        self.Wd = np.exp(-Fo) * inner                    # fibre average as a function of d_a
        psi0 = Fo[s_o_weight] + c_i * s_i_weight         # psi(0^n)
        self.psi0 = psi0
        self.s0 = math.exp(-psi0 - u * n)
        self.ell0 = math.exp(-psi0) * ((1 + math.exp(-u)) / 2.0) ** n
        self.levels = self.s0 * np.exp(lam * np.arange(self.J + 2))
        self.Pd = tab.binom / 2.0 ** n_o
        self.A = float(np.sum(self.Pd * self.Wd))
        # outer sample
        self.d = rng.binomial(n_o, 0.5, size=self.M_max)
        self.W = self.Wd[self.d]
        # trivial bracket: psi(a,0) = Fo(d_a) + c_i d(0,s_i)
        psia0 = Fo[self.d] + c_i * s_i_weight
        self.L0 = np.exp(-psia0 - u * n_i)
        self.U0 = np.exp(-psia0 + u * n_i)
        # alphas of the potential calls (i, l), l = 1..L
        if alpha_mode == "uniform":
            self.alpha = rng.uniform(0, 1, size=(self.L, self.M_max))
        elif alpha_mode == "zero":
            self.alpha = np.zeros((self.L, self.M_max))
        elif alpha_mode == "one":
            self.alpha = np.ones((self.L, self.M_max))
        else:
            self.alpha = rng.integers(0, 2, size=(self.L, self.M_max)).astype(float)
        self.delta = delta
        self.ok = True

    # the bracket returned by the potential call (i, l)
    def inner(self, idx, l):
        a = self.alpha[l - 1, idx]
        x = self.xs[l]
        return self.W[idx] * np.exp(-a * x), self.W[idx] * np.exp((1 - a) * x)

    # ---------------------------------------------------------------- sequential 2L+
    def sequential(self):
        K, eta, lam, b, theta = self.K, self.eta, self.lam, self.b, self.theta
        tab, n_o = self.tab, self.n_o
        Lb, Ub = self.L0.copy(), self.U0.copy()
        rung = np.zeros(self.M_max, dtype=np.int16)
        called = np.zeros((self.L + 1, self.M_max), dtype=bool)    # called[l, i]
        call_level = np.full((self.L + 1, self.M_max), -1, dtype=np.int32)
        ell = self.ell0
        Sig = 0.0
        qs, plows, kinds = [], [], []
        upper_sum = 0.0
        res = {"status": "abort", "level": None}
        ebm = math.exp(-b)
        for j in range(0, self.J + 1):
            sj = self.levels[j]
            M = K
            ell_entry = ell
            while True:
                # (a) classify a_1..a_M at level j
                while True:
                    need = (Ub[:M] > sj) & (Lb[:M] <= sj * ebm)
                    idx = np.nonzero(need)[0]
                    if len(idx) == 0:
                        break
                    if np.any(rung[idx] >= self.L):
                        res["status"] = "abort_unclassified"
                        return res, called, call_level
                    l = rung[idx] + 1
                    for ll in np.unique(l):
                        sub = idx[l == ll]
                        lo, hi = self.inner(sub, int(ll))
                        Lb[sub] = np.maximum(Lb[sub], lo)
                        Ub[sub] = np.minimum(Ub[sub], hi)
                        rung[sub] = ll
                        called[ll, sub] = True
                        call_level[ll, sub] = j
                N = int(np.count_nonzero(Ub[:M] > sj))
                q = min(1.0, max(N, K) / ((1 - eta) * M))
                populated = N >= K
                plow = None
                if populated:
                    plow = N / ((1 + eta) * M)
                    k = tab.largest_k(2.0 ** n_o * plow)
                    ell = max(ell, sj * ebm * plow, sj * ebm * tab.T[k] / 2.0 ** n_o)
                # (c) closure test
                if 2.0 ** n_o * q < 1:
                    tail = 0.0
                else:
                    r = tab.least_r(2.0 ** n_o * q)
                    tail = sj * tab.E[r] / 2.0 ** n_o if r <= n_o - 1 else math.inf
                if tail <= theta * math.exp(b) * ell:
                    Lout = max(ell, Sig + ((1 - math.exp(-lam)) * ebm * sj * plow if populated else 0.0))
                    Uout = self.s0 + upper_sum + tail
                    res.update(status="closed", level=j, L=Lout, U=Uout, qs=qs, kinds=kinds, M=M,
                               ell=ell)
                    return res, called, call_level
                if populated:
                    qs.append(q); plows.append(plow); kinds.append("P")
                    Sig += (1 - math.exp(-lam)) * ebm * sj * plow
                    upper_sum += (self.levels[j + 1] - sj) * q
                    break
                if M >= self.nu * sj / (ell_entry * math.exp(b)):
                    qs.append(q); plows.append(None); kinds.append("N")
                    upper_sum += (self.levels[j + 1] - sj) * q
                    break
                if 2 * M > self.M_max:
                    res["status"] = "abort_size"
                    return res, called, call_level
                M = 2 * M
        res["status"] = "abort_levelJ"
        return res, called, call_level

    # ---------------------------------------------------------------- batched B2L+
    def batched(self, mut=None):
        """Returns the candidate sets C_1..C_L (boolean masks) computed stage by stage from the stored
        brackets, exactly as in Theorem 11.84 / Theorem U1."""
        K, eta, lam, b = self.K, self.eta, self.lam, self.b
        c_eta = self.c_eta
        Mmax = self.M_max
        idx1 = np.arange(1, Mmax + 1)                     # 1-based indices of the outer points
        Lb, Ub = self.L0.copy(), self.U0.copy()
        C = [None, np.ones(Mmax, dtype=bool)]
        lo, hi = self.inner(np.arange(Mmax), 1)           # stage 1: rung 1 on all points
        Lb = np.maximum(Lb, lo); Ub = np.minimum(Ub, hi)
        sizes = np.array(self.sizes)
        lev = self.levels[: self.J + 1]
        ebm = math.exp(-b)
        for l in range(2, self.L + 1):
            Cprev = C[l - 1]
            # N_L(j, M) = #{i <= M, i in C_{l-1} : L_i > s_j}
            jl = np.searchsorted(lev, Lb, side="left")    # number of levels s_j < L_i  (L_i > s_j  <=>  j < jl)
            NL = np.zeros((self.J + 1, len(sizes)))
            prev = 0
            hist_cum = np.zeros(self.J + 2)
            for mi, M in enumerate(sizes):
                blk = slice(prev, M)
                sel = Cprev[blk]
                h = np.bincount(np.minimum(jl[blk][sel], self.J + 1), minlength=self.J + 2)
                hist_cum = hist_cum + h
                # N_L(j,M) = #points with jl > j
                tailc = np.cumsum(hist_cum[::-1])[::-1]   # tailc[t] = #points with jl >= t
                NL[:, mi] = tailc[1: self.J + 2]
                prev = M
            lam_j = np.full(self.J + 1, self.ell0)
            run = 0.0
            factor = 1.0 if mut == "lambda" else c_eta * ebm / (1 + eta)
            for j in range(self.J + 1):
                lam_j[j] = max(self.ell0, factor * run) if run > 0 else self.ell0
                ok = NL[j] >= K
                if ok.any():
                    run = max(run, float(np.max(lev[j] * NL[j][ok] / sizes[ok])))
            two = 1.0 if mut == "nofactor2" else 2.0
            Mhat = np.maximum(K, two * self.nu * lev / (lam_j * math.exp(b)))
            member = np.zeros(Mmax, dtype=bool)
            for j in range(self.J + 1):
                member |= (idx1 <= Mhat[j]) & (Ub > lev[j]) & (Lb <= lev[j] * ebm)
            Cl = Cprev & member
            C.append(Cl)
            sub = np.nonzero(Cl)[0]
            lo, hi = self.inner(sub, l)                   # stage l: rung l on C_l only
            Lb[sub] = np.maximum(Lb[sub], lo); Ub[sub] = np.minimum(Ub[sub], hi)
        return C

    def N_bound(self, l):
        return self.K + (self.J + 1) * max(self.K, 4 * (1 + self.eta) / self.c_eta * math.exp(self.lam)
                                           * self.nu * math.exp(self.xs[l - 1]))

    # ---------------------------------------------------------------- the events of the proofs
    def good_event(self):
        K, eta = self.K, self.eta
        sizes = self.sizes
        cnt = np.zeros((self.n_o + 1, len(sizes)))
        prev = 0
        acc = np.zeros(self.n_o + 1)
        for mi, M in enumerate(sizes):
            acc = acc + np.bincount(self.d[prev:M], minlength=self.n_o + 1)
            cnt[:, mi] = acc
            prev = M
        lev = self.levels[: self.J + 1]
        v2 = v3 = v3p = True
        thr_sets = [np.exp(-self.b)] + [math.exp(-x) for x in self.xs[: self.L]]
        for j in range(self.J + 1):
            # thresholds s_j (V2, V3'), s_j e^{-b}, s_j e^{-x_l} (V3)
            above = self.Wd > lev[j]
            p = float(np.sum(self.Pd[above]))
            X = cnt[above].sum(axis=0)
            for mi, M in enumerate(sizes):
                if not (M * p <= K / (1 - eta) or X[mi] >= (1 - eta) * M * p - 1e-9):
                    v2 = False
                if not (X[mi] < K or X[mi] <= (1 + eta) * M * p + 1e-9):
                    v3p = False
            for f_ in thr_sets:
                above = self.Wd > lev[j] * f_
                p = float(np.sum(self.Pd[above]))
                X = cnt[above].sum(axis=0)
                for mi, M in enumerate(sizes):
                    if not (X[mi] < K or X[mi] <= (1 + eta) * M * p + 1e-9):
                        v3 = False
        return v2, v3, v3p


def main():
    nruns = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261125
    u = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    rng = np.random.default_rng(seed)
    kinds = ["flat", "cone", "dip", "trunc", "walk", "flathist"]
    stats = dict(runs=0, closed=0, good=0, A_viol_good=0, A_viol_bad=0, B_viol=0, S_viol=0, width_viol=0,
                 mutL_viol=0, mutL_runs=0, mut2_viol=0, mut2_runs=0, neg_levels=0, pop_levels=0, calls_ge2=0,
                 skipped=0, aborts=0, B_nontrivial=0)
    maxratioB = 0.0
    maxratioB_nt = 0.0
    fracC = []
    print(f"# R4 own harness for Theorem 11.84 (Claims A, B); u={u}, seed={seed}")
    tries = 0
    while stats["runs"] < nruns and tries < 20 * nruns:
        tries += 1
        n_o = int(rng.choice([6, 7, 8, 9, 10]))
        n_i = int(rng.choice([3, 4, 5, 6]))
        Lr = int(rng.choice([2, 3, 4]))
        Ksmall = int(rng.choice([6, 10, 16]))
        etap = float(rng.choice([1.0, 20.0, 100.0]))
        theta = float(rng.choice([1.0, 3.0, 10.0]))
        lam = float(rng.choice([0.5, 1.0]))
        eta = 0.5
        top = 2 * u * n_i
        regime = "extensive" if rng.uniform() < 0.5 else "bounded"
        if regime == "extensive":
            # decreasing ladder x_1 > ... > x_L below x_0 = 2 u n_i, rungs a fixed fraction of x_0
            fr = np.sort(rng.uniform(0.08, 0.8, size=Lr))[::-1]
            xs = list(top * fr)
        else:
            # small rungs and a large outer cube: here N_l < M_max, so Claim B is a real constraint
            n_o = int(rng.choice([9, 10, 11]))
            Ksmall, etap = 6, 100.0
            x1 = float(rng.uniform(0.4, min(2.2, 0.9 * top)))
            xs = [x1]
            for _ in range(Lr - 1):
                xs.append(xs[-1] * float(rng.uniform(0.35, 0.8)))
        kind = kinds[int(rng.integers(len(kinds)))]
        amode = ["uniform", "zero", "one", "mixed"][int(rng.integers(4))]
        R = Run(u, n_o, n_i, lam, eta, etap, theta, 1.0, xs, Ksmall, kind, amode, 0.05, rng)
        if not R.ok:
            stats["skipped"] += 1
            continue
        stats["runs"] += 1
        res, called, call_level = R.sequential()
        v2, v3, v3p = R.good_event()
        good = v2 and v3 and v3p
        stats["good"] += int(good)
        if res["status"] == "closed":
            stats["closed"] += 1
            stats["neg_levels"] += res["kinds"].count("N")
            stats["pop_levels"] += res["kinds"].count("P")
            x_out = math.log((2 / (1 + math.exp(u))) ** R.n
                             + math.exp(R.b) * (math.exp(lam) * (1 + eta) / (1 - eta) + etap + theta))
            if res["U"] > math.exp(x_out) * res["L"] * (1 + 1e-9):
                stats["width_viol"] += 1
            if good and not (res["L"] <= R.A * (1 + 1e-9) and R.A <= res["U"] * (1 + 1e-9)):
                stats["S_viol"] += 1
        else:
            stats["aborts"] += 1
        C = R.batched()
        ncalls = 0
        violA = False
        for l in range(2, R.L + 1):
            cl = called[l]
            ncalls += int(cl.sum())
            if np.any(cl & ~C[l]):
                violA = True
            Nl = R.N_bound(l)
            ratio = C[l].sum() / Nl
            maxratioB = max(maxratioB, ratio)
            if C[l].sum() > Nl:
                stats["B_viol"] += 1
            if Nl < R.M_max:
                stats["B_nontrivial"] += 1
                maxratioB_nt = max(maxratioB_nt, ratio)
            fracC.append(C[l].sum() / R.M_max)
        stats["calls_ge2"] += ncalls
        if violA:
            if good:
                stats["A_viol_good"] += 1
            else:
                stats["A_viol_bad"] += 1
        # mutations (same sample, same sequential run)
        for mut, key in (("lambda", "mutL"), ("nofactor2", "mut2")):
            Cm = R.batched(mut=mut)
            stats[key + "_runs"] += 1
            if any(np.any(called[l] & ~Cm[l]) for l in range(2, R.L + 1)):
                stats[key + "_viol"] += 1
        if stats["runs"] <= 12 or stats["runs"] % 20 == 0:
            print(f"run {stats['runs']:3d}: n_o={n_o} n_i={n_i} L={Lr} K={Ksmall} eta'={etap} theta={theta} lam={lam} "
                  f"{regime:9s} {kind:8s} {amode:7s} M_max={R.M_max} J={R.J} status={res['status']} level={res['level']} "
                  f"good={good} |C_l|={[int(C[l].sum()) for l in range(2, R.L + 1)]} "
                  f"N_l={[int(R.N_bound(l)) for l in range(2, R.L + 1)]} seq.calls(l>=2)={ncalls} violA={violA}")
            sys.stdout.flush()
    print("# summary:", stats)
    print(f"# rungs with N_l < M_max (Claim B not implied by |C_l| <= M_max): {stats['B_nontrivial']}, "
          f"largest |C_l|/N_l among them = {maxratioB_nt:.4f}")
    print(f"# largest |C_l|/N_l = {maxratioB:.4f};  |C_l|/M_max: median {np.median(fracC):.4f}, "
          f"min {np.min(fracC):.5f}, max {np.max(fracC):.4f}")


if __name__ == "__main__":
    main()
