"""
e2e.py -- workstream R6: Algorithm 2L+ END TO END with real inner brackets on explicit cubes Q_{n_o} x Q_{n_i}.

The inner procedure of every rung is the two-sample bracket of Proposition K0 (= 11.57(a)) run on the fibre with fresh
randomness (the two samples are drawn exactly as multinomial counts over the 2^{n_i} points of the fibre), with the constants
of the proposition for the failure probability delta' = delta/(4 L Mbar) of Theorem K1; if no radius qualifies the fibre is
enumerated.  Every point of the outer sample is individual (one unit per point).  psi is an explicit u-Lipschitz array.

Checked per run: every claim of Theorem K1 (checks.check_2LP), validity and width of EVERY inner bracket, and the number of
queries against C_max (the declared cost of a rung is 2 M_l or 2^{n_i}).

usage: python3 e2e.py <nruns> <seed> [Kdiv]     (Kdiv > 1 divides the inner and outer K: off the theorem, to make failures visible)
"""
import sys, json, time, os, math
import numpy as np
import mpmath as mp
from fractions import Fraction
import r6lib as R, checks as C
from check_tail_lemmas import random_lipschitz
import everyn as EV

HERE = os.path.dirname(os.path.abspath(__file__))


class ExplicitInstance:
    big_counts = False

    def __init__(self, n_o, n_i, u, psi):
        self.n_o, self.n_i, self.n, self.u = n_o, n_i, n_o + n_i, float(u)
        self.psi = psi.reshape(1 << n_o, 1 << n_i)              # psi[a, b]
        w = np.exp(-self.psi)
        self.Wfib = w.mean(axis=1)
        self.lnWfib = np.log(self.Wfib)
        self.A = mp.mpf(float(self.Wfib.mean()))
        self.psi0 = float(self.psi[0, 0])
        self.wsorted = -np.sort(-w, axis=1)                      # each fibre's weights, descending
        self._sorted = np.sort(self.lnWfib)[::-1]
        self.name = "explicit"

    def tail(self, lnt):
        k = int(np.searchsorted(-self._sorted, -float(lnt), side="left"))
        return mp.mpf(k) / len(self._sorted)

    def new_block(self, size, rng):
        a = rng.integers(0, 1 << self.n_o, size=size)
        return dict(cnt=np.ones(size, dtype=np.int64), lnW=self.lnWfib[a], lnL0=-self.psi[a, 0] - self.u * self.n_i,
                    lnU0=-self.psi[a, 0] + self.u * self.n_i, strat=np.zeros(size, dtype=np.int64), extra=a)


def k0_params(d, u, x, deltap, tab, Kdiv=1):
    """parameters of the base bracket for (d, x, delta'): eta, K, r*, M  (None if no radius qualifies -> enumeration)."""
    eta = EV.eta_for(x)
    ef = mp.mpf(eta.numerator) / eta.denominator
    K = int(mp.ceil(3 * (1 + ef) / ef ** 2 * mp.log(4 / mp.mpf(deltap))))
    K = max(1, K // Kdiv)
    thr = mp.e ** (mp.mpf(x) - mp.log((1 + ef) / (1 - ef))) - 1
    rs = -1
    for r in range(0, d):
        if tab.gamma_pp(r, eta) <= thr:
            rs = r
        else:
            break
    if rs < 0:
        return None
    M = int(mp.ceil(K * mp.mpf(2) ** d / ((1 - ef) * tab.ball[rs])))
    # r-hat and the tail constant are functions of (K, M) only
    qplus = Fraction(K, 1) / ((1 - eta) * M)
    if qplus * tab.two_m < 1:
        tail_c = 0.0
        rhat = -1
    else:
        rhat = tab.least_ball_ge(qplus * tab.two_m)
        assert rhat <= d - 1
        tail_c = float(tab.E[rhat] / tab.two_m)
    return dict(eta=float(ef), K=K, rstar=rs, M=M, rhat=rhat, tail_c=tail_c,
                width_cert=float(mp.log((1 + ef) / (1 - ef)) + mp.log(1 + (tab.gamma_pp(rhat, eta) if rhat >= 0 else 0))))


class K0Oracle:
    """real two-sample brackets on the fibres; counts invalid / too wide answers (event (V1) of the proof)."""

    def __init__(self, inst, xs, pars, rng):
        self.inst, self.xs, self.pars, self.rng = inst, [float(x) for x in xs], pars, rng
        self.invalid_calls = 0
        self.calls = 0
        self.real_brackets = 0
        self.max_width_excess = -1e9

    def __call__(self, run, idx, l, j):
        a = run.extra_arr[idx]
        lnW = run.lnW[idx]
        p = self.pars[l]
        self.calls += len(idx)
        if p is None:                      # enumeration: exact
            return lnW.copy(), lnW.copy()
        nfib = 1 << self.inst.n_i
        pv = np.full(nfib, 1.0 / nfib)
        lnL = np.empty(len(idx))
        lnU = np.empty(len(idx))
        CH = 20000
        for s in range(0, len(idx), CH):
            aa = a[s:s + CH]
            ws = self.inst.wsorted[aa]                              # (k, nfib) descending
            c1 = self.rng.multinomial(p["M"], pv, size=len(aa))
            cum = np.cumsum(c1, axis=1)
            pos = (cum >= p["K"]).argmax(axis=1)                    # K-th largest weight of the first sample
            that = ws[np.arange(len(aa)), pos]
            c2 = self.rng.multinomial(p["M"], pv, size=len(aa))
            Ahat = (c2 * np.minimum(ws, that[:, None])).sum(axis=1) / p["M"]
            L = Ahat / (1 + p["eta"])
            U = Ahat / (1 - p["eta"]) + that * p["tail_c"]
            lnL[s:s + CH] = np.log(L)
            lnU[s:s + CH] = np.log(U)
        self.real_brackets += len(idx)
        bad = (lnL > lnW + 1e-12) | (lnU < lnW - 1e-12) | (lnU - lnL > self.xs[l] + 1e-12)
        self.invalid_calls += int(bad.sum())
        self.max_width_excess = max(self.max_width_excess, float(np.max(lnU - lnL - self.xs[l])))
        return lnL, lnU


def one_run(args):
    seed, Kdiv = args
    rng = np.random.default_rng(seed)
    n_o, n_i = [(6, 6), (7, 6), (6, 7), (7, 5), (8, 5), (5, 7)][int(rng.integers(0, 6))]
    u = float(rng.choice([0.5, 1.0, 2.0]))
    n = n_o + n_i
    psi = random_lipschitz(n, u, rng)
    # make the split non-trivial: random permutation of coordinates is implicit in the random constructions
    inst = ExplicitInstance(n_o, n_i, u, psi)
    b = float(rng.choice([0.6, 1.0, 2.0]))
    lam = float(rng.choice([0.5, 1.0]))
    eta = Fraction(rng.choice([2, 4]))
    eta = Fraction(1, int(eta))
    etap = float(rng.choice([0.5, 1.0]))
    theta = float(rng.choice([0.3, 1.0, 3.0]))
    x0 = 2 * u * n_i
    Lr = int(rng.integers(1, 4))
    mids = sorted(rng.uniform(b * 1.2, x0 * 0.9, size=Lr - 1), reverse=True) if x0 * 0.9 > b * 1.2 else []
    xs = [x0] + [float(v) for v in mids] + [b * (1 - 1e-9)]
    L = len(xs) - 1
    tab_o = R.Tables(n_o, u)
    tab_i = R.Tables(n_i, u)
    nu1 = float(rng.choice([1.0, 2 * math.e ** u * n_o / theta]))
    P0 = R.Params2LP(n, n_o, u, lam, eta, etap, theta, nu1, b, 0.05, xs, [1] * L, tables=tab_o)
    Kouter = max(2, P0.K // Kdiv) if Kdiv > 1 else None
    pars = [None] + [k0_params(n_i, u, xs[l], P0.deltap, tab_i, Kdiv) for l in range(1, L + 1)]
    costs = [(2 * p["M"] if p is not None else (1 << n_i)) for p in pars[1:]]
    P = R.Params2LP(n, n_o, u, lam, eta, etap, theta, nu1, b, 0.05, xs, costs, tables=tab_o, K_override=Kouter)
    orc = K0Oracle(inst, xs, pars, rng)
    t0 = time.time()
    run = R.Run(P, inst, orc, rng, max_units=6_000_000)
    run.extra_arr = np.zeros(0, dtype=np.int64)
    # the engine stores "extra" in a list; keep an array view for the oracle
    orig = run._ensure_blocks

    def ens(t):
        orig(t)
        if len(run.extra) != len(run.extra_arr):
            run.extra_arr = np.asarray(run.extra, dtype=np.int64)
    run._ensure_blocks = ens
    run.run()
    ck = C.check_2LP(run)
    st = [r["status"] for r in run.levels]
    rec = dict(seed=seed, n_o=n_o, n_i=n_i, u=u, b=b, lam=lam, eta=str(eta), etap=etap, theta=theta, L=L, Kdiv=Kdiv, K=P.K,
               status=run.status, abort=run.abort_reason, levels=len(run.levels), pop=st.count("populated"), neg=st.count("negligible"),
               points=int(run.points_drawn), real_brackets=orc.real_brackets, inner_calls=orc.calls, invalid_inner=orc.invalid_calls,
               rungs_real=sum(p is not None for p in pars[1:]), rungs=L, max_width_excess=orc.max_width_excess,
               G=ck["G"], Gfail=[str(x) for x in ck["Gfail"][:3]], det=[str(x) for x in ck["det"][:5]], good=[str(x) for x in ck["good"][:5]],
               lnq=float(mp.log(run.queries())), lnCmax=float(mp.log(P.Cmax)), q_over_Cmax=float(run.queries() / P.Cmax),
               ratios=ck["ratios"], secs=round(time.time() - t0, 1))
    if run.status == "closed":
        lo, up = run.result
        lnA = mp.log(inst.A)
        rec.update(lo=float(lo - lnA), up=float(up - lnA), width=float(up - lo), x_out=float(P.x_out))
    return rec


if __name__ == "__main__":
    from multiprocessing import Pool
    nruns, seed = int(sys.argv[1]), int(sys.argv[2])
    Kdiv = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rng = np.random.default_rng(seed)
    jobs = [(int(rng.integers(0, 2 ** 31)), Kdiv) for _ in range(nruns)]
    out = os.path.join(HERE, "data", "e2e_%d_K%d.jsonl" % (seed, Kdiv))
    recs = []
    t0 = time.time()
    with Pool(2) as pool, open(out, "w") as f:
        for rec in pool.imap_unordered(one_run, jobs, chunksize=1):
            recs.append(rec)
            f.write(json.dumps(rec) + "\n")
            f.flush()
    S = dict(runs=len(recs), closed=sum(r["status"] == "closed" for r in recs), abort=sum(r["status"] == "abort" for r in recs),
             real_brackets=sum(r["real_brackets"] for r in recs), inner_calls=sum(r["inner_calls"] for r in recs),
             invalid_inner=sum(r["invalid_inner"] for r in recs), Gfail=sum(not r["G"] for r in recs),
             det_viol=sum(bool(r["det"]) for r in recs), good_viol=sum(bool(r["good"]) for r in recs),
             invalid_final=sum(1 for r in recs if r["status"] == "closed" and (r["lo"] > 1e-9 or r["up"] < -1e-9)),
             too_wide_final=sum(1 for r in recs if r["status"] == "closed" and r["width"] > r["x_out"] + 1e-9),
             max_q_over_Cmax=max(r["q_over_Cmax"] for r in recs), neg=sum(r["neg"] for r in recs),
             rungs_real=sum(r["rungs_real"] for r in recs), rungs=sum(r["rungs"] for r in recs),
             max_width_excess=max(r["max_width_excess"] for r in recs))
    print("e2e seed", seed, "Kdiv", Kdiv, "time %.0fs" % (time.time() - t0))
    print(json.dumps(S, indent=1))
    for r in recs:
        if r["det"] or r["good"]:
            print("VIOLATION", {k: r[k] for k in ("seed", "n_o", "n_i", "u", "b", "status", "det", "good", "invalid_inner", "G")})
