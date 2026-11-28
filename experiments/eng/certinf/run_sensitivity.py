"""Sensitivity runs of PROTOCOL.md section 4 and the n-sweep for H-D.

    python experiments/eng/certinf/run_sensitivity.py a      # true half-width 2 rho, declared rho          -> results/sens_a.jsonl
    python experiments/eng/certinf/run_sensitivity.py b      # no / one / uninformative observation         -> results/sens_b.jsonl
    python experiments/eng/certinf/run_sensitivity.py c      # displaced regions: detection, false alarms    -> results/sens_c.jsonl
    python experiments/eng/certinf/run_sensitivity.py d      # H-D: least n with median excess of M3 < 0.05 -> results/sens_d.jsonl

Level: each certified end at delta/2 = 0.025 (as in the grid); the inconsistency certificate at delta = 0.05.
Split: training = min(n/2, 5000) draws, the rest validation.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import instances as ins  # noqa: E402
from instances import ci  # noqa: E402
import run_validation as rv  # noqa: E402

DELTA = 0.05
OUT = HERE / "results"
N_SENS = 10000
REPS_SENS = 50
REPS_C = 50
D_GRID = [200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]
D_REPS = 20
D_TARGET = 0.05


def seed(*key):
    return np.random.default_rng(np.random.SeedSequence([int(k) for k in key] + [777]))


def m3(sample, region, dec, n):
    k = min(n // 2, 5000)
    tr, va = sample.part(slice(0, k)), sample.part(slice(k, None))
    up = ci.certify_upper(tr, va, region, dec, DELTA / 2)
    lo = ci.certify_lower(tr, va, region, dec, DELTA / 2)
    return lo, up, tr, va


def ref_sample(ctx, fam, rng, n):
    f, phi, r = rv.draw(ctx, fam, rng, n, "pi")
    return ci.Sample(f, phi, np.exp(-r), np.exp(r))


# ------------------------------------------------------------------------------------------------ (a)
def job_a(args):
    fam, tgt, env, rep0, rep1 = args
    ctx = rv.context(fam, tgt, env, 2.0)          # data from p_true with |R| <= 2 rho; declared envelope rho
    rows = []
    for rep in range(rep0, rep1):
        rng = seed(1, rv.FAM_ID[fam], rv.TGT[fam].index(tgt), int(env * 100), rep)
        s = ref_sample(ctx, fam, rng, N_SENS)
        lo, up, tr, va = m3(s, ctx["region"], ctx["dec"], N_SENS)
        inc = ci.certify_inconsistent(tr, va, ctx["region"], ctx["dec"], DELTA)
        rows.append(dict(run="a", family=fam, target=tgt, env=env, gamma=ctx["gamma"], n=N_SENS, rep=rep, lo=lo.value, hi=up.value,
                         st_lo=lo.status, st_hi=up.status, true=ctx["true"], V_lo=ctx["m0"]["lo"], V_hi=ctx["m0"]["hi"],
                         I_empty=ctx["m0"]["empty"], inc=inc.status, inc_val=float(inc.value)))
    return rows


def run_a(pool):
    jobs = [(fam, rv.TGT[fam][0], env, a, min(a + 25, REPS_SENS)) for fam in ("F1", "F2", "F3") for env in (0.2, 0.55, 1.15)
            for a in range(0, REPS_SENS, 25)]
    return jobs, job_a


# ------------------------------------------------------------------------------------------------ (b)
def job_b(args):
    variant, env, rep0, rep1 = args
    fam, tgt = "F1", "nnn_corr"
    ctx = rv.context(fam, tgt, env)
    full = ctx["region"]
    if variant == "none":
        cols, region = [], ci.Box()
    elif variant == "one":
        cols, region = [0], ci.Box(full.c[:1], ins.HALF)
    elif variant == "uninformative":
        cols, region = [0, 1], ci.Box([0.0, 0.0], 1.0)
    else:
        cols, region = [0, 1], full
    m = len(cols)
    dec = ci.Declared(-1.0, 1.0, -np.ones(m), np.ones(m), ctx["dec"].U_max)
    l, u = ctx["pi"] * np.exp(-ctx["rho"]), ctx["pi"] * np.exp(ctx["rho"])
    ex = ci.interval(ci.lump(ci.box_problem(l, u, ctx["f"], ctx["phi"][:, cols], region)), "lp")
    rows = []
    for rep in range(rep0, rep1):
        rng = seed(2, ["none", "one", "uninformative", "full"].index(variant), int(env * 100), rep)
        s = ref_sample(ctx, fam, rng, N_SENS)
        s = ci.Sample(s.f, s.phi[:, cols], s.L, s.U)
        lo, up, _, _ = m3(s, region, dec, N_SENS)
        rows.append(dict(run="b", variant=variant, family=fam, target=tgt, env=env, gamma=ctx["gamma"], n=N_SENS, rep=rep,
                         lo=lo.value, hi=up.value, st_lo=lo.status, st_hi=up.status, V_lo=float(ex["lo"]), V_hi=float(ex["hi"]),
                         true=ctx["true"]))
    return rows


def run_b(pool):
    jobs = [(v, env, a, min(a + 25, REPS_SENS)) for v in ("none", "one", "uninformative", "full") for env in (1.15,) for a in range(0, REPS_SENS, 25)]
    return jobs, job_b


# ------------------------------------------------------------------------------------------------ (c)
DISP = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5]


def displaced_region(ctx, fam, d):
    """d = 0: the consistent data region.  d > 0: the region moved along the first observable so that its lowest
    point in that coordinate lies d above the largest E_p phi_1 over the class (the reachable set's support)."""
    reg = ctx["region"]
    if d == 0:
        return reg, math.nan
    l, u = ctx["pi"] * np.exp(-ctx["rho"]), ctx["pi"] * np.exp(ctx["rho"])
    key, inv = np.unique(ctx["phi"][:, 0], return_inverse=True)
    inv = inv.reshape(-1)
    top = ci.interval(ci.box_problem(np.bincount(inv, weights=l), np.bincount(inv, weights=u), key, np.zeros((key.size, 0)), ci.Box()))["hi"]
    c = np.array(reg.c, dtype=float)
    if isinstance(reg, ci.Box):
        c[0] = top + d + ins.HALF
        return ci.Box(c, ins.HALF), float(top)
    c[0] = top + d + math.sqrt(reg.cov[0, 0]) * reg.radius
    return ci.Ellipsoid(c, reg.cov, reg.radius), float(top)


def job_c(args):
    fam, env, d, rep0, rep1 = args
    tgt = rv.TGT[fam][0]
    ctx = rv.context(fam, tgt, env)
    region, top = displaced_region(ctx, fam, d)
    rows = []
    for rep in range(rep0, rep1):
        rng = seed(3, rv.FAM_ID[fam], int(env * 100), int(d * 100), rep)
        s = ref_sample(ctx, fam, rng, N_SENS)
        k = min(N_SENS // 2, 5000)
        t0 = time.perf_counter()
        inc = ci.certify_inconsistent(s.part(slice(0, k)), s.part(slice(k, None)), region, ctx["dec"], DELTA)
        rows.append(dict(run="c", family=fam, env=env, gamma=ctx["gamma"], disp=d, n=N_SENS, rep=rep, inc=inc.status,
                         inc_val=float(inc.value), top=top, t=time.perf_counter() - t0))
    return rows


def run_c(pool):
    jobs = [(fam, env, d, a, a + 25) for fam in ("F1", "F2", "F3") for env in (0.2, 0.55) for d in DISP for a in range(0, REPS_C, 25)]
    return jobs, job_c


def exact_c():
    """Exact inconsistency on the whole space for every displaced region (ground truth for (c))."""
    out = []
    for fam in ("F1", "F2", "F3"):
        for env in (0.2, 0.55):
            ctx = rv.context(fam, rv.TGT[fam][0], env)
            l, u = ctx["pi"] * np.exp(-ctx["rho"]), ctx["pi"] * np.exp(ctx["rho"])
            for d in DISP:
                region, top = displaced_region(ctx, fam, d)
                P = ci.lump(ci.box_problem(l, u, np.zeros_like(ctx["f"]), ctx["phi"], region))      # the target does not enter
                val, _ = ci.find_inconsistency(P)
                out.append(dict(family=fam, env=env, disp=d, top=top, exact_phi=float(val), inconsistent=bool(val > 1e-9)))
    return out


# ------------------------------------------------------------------------------------------------ (d) H-D sweep
def job_d(env):
    fam, tgt = "F1", "nnn_corr"
    ctx = rv.context(fam, tgt, env)
    rows = []
    for n in D_GRID:
        ex = []
        for rep in range(D_REPS):
            rng = seed(4, int(env * 100), n, rep)
            s = ref_sample(ctx, fam, rng, n)
            t0 = time.perf_counter()
            lo, up, _, _ = m3(s, ctx["region"], ctx["dec"], n)
            e = (up.value - ctx["m0"]["hi"]) + (ctx["m0"]["lo"] - lo.value)
            ex.append(e)
            rows.append(dict(run="d", family=fam, target=tgt, env=env, gamma=ctx["gamma"], n=n, rep=rep, lo=lo.value, hi=up.value,
                             st_lo=lo.status, st_hi=up.status, V_lo=ctx["m0"]["lo"], V_hi=ctx["m0"]["hi"], excess=e,
                             t=time.perf_counter() - t0))
        if float(np.median(ex)) < D_TARGET:
            break
    return rows


def main():
    which = sys.argv[1]
    t0 = time.perf_counter()
    out = OUT / f"sens_{which}.jsonl"
    with Pool(4, maxtasksperchild=20) as pool:
        if which == "d":
            jobs, fn = list(reversed(ins.RHOS)), job_d
        else:
            jobs, fn = {"a": run_a, "b": run_b, "c": run_c}[which](pool)
        with open(out, "w") as fh:
            for i, rows in enumerate(pool.imap_unordered(fn, jobs)):
                for r in rows:
                    fh.write(json.dumps(r) + "\n")
                fh.flush()
                print(f"[{i + 1}/{len(jobs)}] {time.perf_counter() - t0:.0f}s", flush=True)
    if which == "c":
        (OUT / "sens_c_exact.json").write_text(json.dumps(exact_c(), indent=1))
    (OUT / f"sens_{which}_wall.json").write_text(json.dumps(dict(wall=time.perf_counter() - t0)))


if __name__ == "__main__":
    main()
