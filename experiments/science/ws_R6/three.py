"""
three.py -- workstream R6: THREE nested levels with real randomness at every level, on explicit cubes
Q_n = Q_{n_o} x (Q_{n_o'} x Q_{n_i'}):  outer Algorithm 2L+  ->  middle Algorithm 2L+ on every fibre  ->  bottom two-sample
brackets of Proposition K0 on every fibre of a fibre.  All constants are those of the theorems; the middle procedure of an
outer rung of accuracy x is run with parameters for which its CERTIFIED accuracy x_out is at most x and with the failure
probability delta' = delta/(4 L Mbar) of the outer level; its declared cost is its own C_max.

For run time, the bracket that an outer point receives at a rung is drawn from a pool of independent middle runs on that
point's fibre (as referee R8 did); so different outer points on the same fibre can share a middle run.

Checked: every claim of Theorem K1 at the outer level and in every middle run (checks.check_2LP); validity and width of every
bottom bracket and of every middle bracket.
usage: python3 three.py <outer runs> <seed> [pool]
"""
import sys, os, json, time, math
import numpy as np
import mpmath as mp
from fractions import Fraction
import r6lib as R, checks as C, e2e as E2
from check_tail_lemmas import random_lipschitz

HERE = os.path.dirname(os.path.abspath(__file__))


def middle_params(n_m, n_om, u, x, delta_mid, tab_o, tab_i):
    """Algorithm 2L+ on Q_{n_om} x Q_{n_im} with certified accuracy <= x (None if no choice on the list works)."""
    n_im = n_m - n_om
    for frac_b in (0.5, 0.65, 0.8):
        for c0 in (1 / 3, 0.2, 0.1, 0.05, 0.02):
            b = frac_b * x
            if b >= 2 * u * n_im * 0.95:
                continue
            xs = [2 * u * n_im, b * (1 - 1e-9)]
            eta = Fraction(c0).limit_denominator(100)
            P0 = R.Params2LP(n_m, n_om, u, c0, eta, c0, c0, 1.0, b, delta_mid, xs, [1], tables=tab_o)
            if P0.x_out <= x:
                par = E2.k0_params(n_im, u, xs[1], P0.deltap, tab_i)
                cost = 2 * par["M"] if par is not None else (1 << n_im)
                P = R.Params2LP(n_m, n_om, u, c0, eta, c0, c0, 1.0, b, delta_mid, xs, [cost], tables=tab_o)
                return P, xs, par
    return None


def middle_run(psi_fibre, n_om, n_im, u, P, xs, par, rng):
    inst = E2.ExplicitInstance(n_om, n_im, u, psi_fibre)
    orc = E2.K0Oracle(inst, xs, [None, par], rng)
    run = R.Run(P, inst, orc, rng, max_units=3_000_000)
    run.extra_arr = np.zeros(0, dtype=np.int64)
    orig = run._ensure_blocks

    def ens(t):
        orig(t)
        if len(run.extra) != len(run.extra_arr):
            run.extra_arr = np.asarray(run.extra, dtype=np.int64)
    run._ensure_blocks = ens
    run.run()
    ck = C.check_2LP(run)
    lo, up = run.result
    lnA = float(mp.log(inst.A))
    return dict(lnL=float(lo), lnU=float(up), lnA=lnA, status=run.status, bottom=orc.real_brackets, bottom_invalid=orc.invalid_calls,
                det=bool(ck["det"]), good=bool(ck["G"] and ck["good"]), G=ck["G"], queries=float(mp.log(run.queries())),
                valid=(float(lo) <= lnA + 1e-9 and float(up) >= lnA - 1e-9), width=float(up - lo))


class PoolOracle:
    def __init__(self, pools, xs, rng):
        self.pools, self.xs, self.rng = pools, [float(x) for x in xs], rng
        self.invalid_calls = 0
        self.calls = 0

    def __call__(self, run, idx, l, j):
        a = run.extra_arr[idx]
        lnL = np.empty(len(idx)); lnU = np.empty(len(idx))
        for k, aa in enumerate(a):
            pool = self.pools[(int(aa), l)]
            m = pool[int(self.rng.integers(0, len(pool)))]
            lnL[k], lnU[k] = m["lnL"], m["lnU"]
            if (not m["valid"]) or m["width"] > self.xs[l] + 1e-9:
                self.invalid_calls += 1
        self.calls += len(idx)
        return lnL, lnU


def one(seed, pool):
    rng = np.random.default_rng(seed)
    n_o, n_om, n_im = [(3, 3, 3), (3, 3, 4), (4, 3, 3), (3, 4, 3)][int(rng.integers(0, 4))]
    n_m = n_om + n_im
    n = n_o + n_m
    u = float(rng.choice([0.5, 1.0]))
    psi = random_lipschitz(n, u, rng).reshape(1 << n_o, 1 << n_m)
    b = float(rng.choice([1.0, 2.0]))
    lam = 1.0; eta = Fraction(1, 2); etap = 1.0; theta = float(rng.choice([1.0, 3.0]))
    xs = [2 * u * n_m, b * (1 - 1e-9)]
    tab_o = R.Tables(n_o, u); tab_mo = R.Tables(n_om, u); tab_mi = R.Tables(n_im, u)
    P0 = R.Params2LP(n, n_o, u, lam, eta, etap, theta, 1.0, b, 0.05, xs, [1], tables=tab_o)
    mp_ = middle_params(n_m, n_om, u, xs[1], P0.deltap, tab_mo, tab_mi)
    if mp_ is None:
        return dict(seed=seed, skipped="no middle parameters with certified accuracy <= x")
    Pm, xsm, par = mp_
    P = R.Params2LP(n, n_o, u, lam, eta, etap, theta, 1.0, b, 0.05, xs, [Pm.Cmax], tables=tab_o)
    t0 = time.time()
    pools = {}
    mids = []
    for a in range(1 << n_o):
        pl = [middle_run(psi[a], n_om, n_im, u, Pm, xsm, par, rng) for _ in range(pool)]
        pools[(a, 1)] = pl
        mids += pl
    inst = E2.ExplicitInstance(n_o, n_m, u, psi)
    orc = PoolOracle(pools, xs, rng)
    run = R.Run(P, inst, orc, rng, max_units=3_000_000)
    run.extra_arr = np.zeros(0, dtype=np.int64)
    orig = run._ensure_blocks

    def ens(t):
        orig(t)
        if len(run.extra) != len(run.extra_arr):
            run.extra_arr = np.asarray(run.extra, dtype=np.int64)
    run._ensure_blocks = ens
    run.run()
    ck = C.check_2LP(run)
    lo, up = run.result
    lnA = mp.log(inst.A)
    return dict(seed=seed, sizes=(n_o, n_om, n_im), u=u, b=b, theta=theta, status=run.status, abort=run.abort_reason,
                outer_valid=bool(lo <= lnA + mp.mpf(10) ** (-9) and up >= lnA - mp.mpf(10) ** (-9)), width=float(up - lo), x_out=float(P.x_out),
                outer_det=bool(ck["det"]), outer_good=bool(ck["G"] and ck["good"]), outer_G=ck["G"], outer_calls=orc.calls,
                outer_invalid_calls=orc.invalid_calls, K_outer=P.K, K_middle=Pm.K, x_mid=float(Pm.x_out), x_rung=float(xs[1]),
                middle_runs=len(mids), middle_closed=sum(m["status"] == "closed" for m in mids), middle_invalid=sum(not m["valid"] for m in mids),
                middle_too_wide=sum(m["width"] > float(xs[1]) + 1e-9 for m in mids), middle_det=sum(m["det"] for m in mids),
                middle_good=sum(m["good"] for m in mids), middle_Gfail=sum(not m["G"] for m in mids), bottom=sum(m["bottom"] for m in mids),
                bottom_invalid=sum(m["bottom_invalid"] for m in mids), bottom_real=par is not None,
                lnq_outer=float(mp.log(run.queries())), lnCmax_outer=float(mp.log(P.Cmax)), secs=round(time.time() - t0, 1))


if __name__ == "__main__":
    nruns, seed = int(sys.argv[1]), int(sys.argv[2])
    pool = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    tlim = float(os.environ.get("R6_THREE_SECONDS", "400"))
    t0 = time.time()
    out = os.path.join(HERE, "data", "three_%d.jsonl" % seed)
    recs = []
    with open(out, "w") as f:
        for i in range(nruns):
            if time.time() - t0 > tlim:
                break
            r = one(seed * 1000 + i, pool)
            recs.append(r)
            f.write(json.dumps(r) + "\n")
            f.flush()
    ok = [r for r in recs if "skipped" not in r]
    S = dict(outer_runs=len(ok), skipped=len(recs) - len(ok), outer_closed=sum(r["status"] == "closed" for r in ok),
             outer_invalid=sum(not r["outer_valid"] for r in ok), outer_too_wide=sum(r["status"] == "closed" and r["width"] > r["x_out"] + 1e-9 for r in ok),
             outer_det=sum(r["outer_det"] for r in ok), outer_good=sum(r["outer_good"] for r in ok),
             middle_runs=sum(r["middle_runs"] for r in ok), middle_closed=sum(r["middle_closed"] for r in ok),
             middle_invalid=sum(r["middle_invalid"] for r in ok), middle_too_wide=sum(r["middle_too_wide"] for r in ok),
             middle_det=sum(r["middle_det"] for r in ok), middle_good=sum(r["middle_good"] for r in ok),
             bottom_brackets=sum(r["bottom"] for r in ok), bottom_invalid=sum(r["bottom_invalid"] for r in ok),
             runs_with_real_bottom=sum(r["bottom_real"] for r in ok), secs=round(time.time() - t0, 1))
    print(json.dumps(S, indent=1))
