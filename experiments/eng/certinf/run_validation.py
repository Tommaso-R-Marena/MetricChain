"""The validation grid of PROTOCOL.md sections 2-4: families F1-F4 x targets x envelopes x n x methods x repetitions.

One JSON line per (family, target, envelope, region, n, method, repetition) in results/validation/*.jsonl.

    python experiments/eng/certinf/run_validation.py --workers 4            # the grid (resumes: finished chunks skipped)
    python experiments/eng/certinf/run_validation.py --probe                # one repetition per cell, timings only
    python experiments/eng/certinf/run_validation.py --memory               # peak memory per method, one cell
"""
from __future__ import annotations

import argparse
import functools
import json
import math
import os
import resource
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import instances as ins  # noqa: E402
from instances import ci  # noqa: E402
import baselines as bl  # noqa: E402

DELTA = 0.05
RES = HERE / "results" / "validation"
FAM_ID = {"F1": 1, "F2": 2, "F3": 3, "F4": 4}
TGT = {"F1": ["nnn_corr", "abs_mag"], "F2": ["pair_pop"], "F3": ["stress", "rg2"], "F4": ["ones_first20"]}
ENVS = {"F1": ins.RHOS + ["var"], "F2": ins.RHOS, "F3": ins.RHOS, "F4": ins.RHOS}
NS = [1000, 10000, 100000]
REPS_PROTOCOL = {1000: 200, 10000: 200, 100000: 50}
REPS = {1000: 100, 10000: 100, 100000: 30}           # cut for runtime (deviation D1 of the report)
METHODS = ["M1", "M2", "M3", "M4", "M5", "M6", "B1", "B2", "B3"]


def env_label(env):
    return env if isinstance(env, str) else f"{env:g}"


# ------------------------------------------------------------------------------------------------ cell context
@functools.lru_cache(maxsize=4)
def instance(fam):
    return ins.get(fam)


@functools.lru_cache(maxsize=8)
def context(fam, tgt, env, factor=1.0):
    t0 = time.perf_counter()
    if fam == "F4":
        c = ins.f4_cells(float(env), factor)
        pi, phi, f = c["prob"], c["phi"], c["f"]
        rho = np.full(pi.size, float(env))
        region = ci.Box(c["centre"], ins.HALF)
        true = float(c["true_f"])
        kind = "box"
    else:
        I = instance(fam)
        pi, phi, f = I.pi, I.phi, I.targets[tgt]
        rho = ins.rho_vec(I, env)
        region, p = ins.data_region(I, env, factor)
        true = float(p @ f)
        kind = I.region_kind
    l, u = pi * np.exp(-rho), pi * np.exp(rho)
    t_setup = time.perf_counter() - t0
    # M0: exact dual on the whole space (lumped by Proposition 8.1)
    t0 = time.perf_counter()
    P = ci.box_problem(l, u, f, phi, region)
    Pl = ci.lump(P)
    method = "lp" if kind == "box" else "descent"
    ex = ci.interval(Pl, method)
    t_m0 = time.perf_counter() - t0
    m0 = dict(lo=float(ex["lo"]), hi=float(ex["hi"]), empty=bool(ex["empty"]), eta_hi=list(map(float, ex["eta_hi"])),
              eta_lo=list(map(float, ex["eta_lo"])), t=t_m0, n_cells=int(Pl.f.size))
    # optimality check of the ends: the extremal ensemble of Theorem 4.1(c) at the returned multipliers
    chk = {}
    for side, sgn, eta in (("hi", 1.0, ex["eta_hi"]), ("lo", -1.0, ex["eta_lo"])):
        tau = sgn * (ex["hi"] if side == "hi" else ex["lo"])
        s = sgn * Pl.f - Pl.phi @ np.asarray(eta) + region.h(eta) - tau
        w = Pl.Lw + Pl.Gw * (s > 0)
        y = (w @ Pl.phi) / w.sum()
        chk[side] = dict(primal_value=float((w @ Pl.f) / w.sum()), in_region=bool(region.contains(y, 1e-6)))
    m0["extremal_check"] = chk
    if fam in ("F1", "F2"):                      # cross-check against the primal programme (Charnes-Cooper)
        t0 = time.perf_counter()
        pr = ci.lp_primal_box(Pl.Lw, Pl.Lw + Pl.Gw, Pl.f, Pl.phi, region)
        m0["primal"] = None if pr is None else [float(pr[0]), float(pr[1])]
        m0["t_primal"] = time.perf_counter() - t0
    # exact b, G for gap sampling (M1, M2, M4): preprocessing
    t0 = time.perf_counter()
    v = np.column_stack([np.ones(pi.size), phi, f])
    b = l @ v
    g = u - l
    G = float(g.sum())
    q = g / G
    t_bg = time.perf_counter() - t0
    t0 = time.perf_counter()
    b4 = bl.b4_information(pi, f, float(rho.max()))
    t_b4 = time.perf_counter() - t0
    t0 = time.perf_counter()
    b5 = bl.b5_no_data(pi, f, rho)
    t_b5 = time.perf_counter() - t0
    m = phi.shape[1]
    dec = ci.Declared(-1.0, 1.0, -np.ones(m), np.ones(m), float(np.exp(rho.max())))
    return dict(pi=pi, phi=phi, f=f, rho=rho, region=region, kind=kind, true=true, m0=m0, b=b, G=G, q=q, dec=dec,
                L_max=float(np.exp(-rho.min())), gamma=float(np.exp(2 * rho.max())), b4=b4, b5=b5,
                t=dict(setup=t_setup, m0=t_m0, bG=t_bg, b4=t_b4, b5=t_b5))


def draw(ctx, fam, rng, n, law):
    if fam == "F4":                              # site by site (uniform envelope: q = pi)
        phi, f = ins.f4_draw(rng, n)
        r = np.full(n, ctx["rho"][0])
        return f, phi, r
    p = ctx["pi"] if law == "pi" else ctx["q"]
    idx = rng.choice(p.size, size=n, p=p)
    return ctx["f"][idx], ctx["phi"][idx], ctx["rho"][idx]


def s3_lumped(b, G, f_q, phi_q, region, delta, bound):
    """ci.s3_interval with the draws lumped (Proposition 8.1): identical problem, fewer points."""
    n, dim = f_q.size, phi_q.shape[1] + 2
    eps = ci.s3_eps_net(n, dim, delta) if bound == "net" else ci.s3_eps_rademacher(n, dim, delta)
    kappa = 2 * eps * G / b[0] if b[0] > 0 else math.inf
    if not math.isfinite(kappa):
        return dict(lo=-1.0, hi=1.0, kappa=kappa, eps=eps, status="abstain")
    uf, uphi, _, _, cnt = bl.lump_sample(f_q, phi_q, np.zeros(n), np.zeros(n))
    P = ci.Problem(uf, uphi, Lw=0.0, Gw=G, region=region.enlarged(kappa), wt=cnt / n, b=b)
    hi, _ = ci.solve_upper(P)
    lo = -ci.solve_upper(P.negated())[0]
    if hi < lo:
        return dict(lo=lo, hi=hi, kappa=kappa, eps=eps, status="inconsistent")
    return dict(lo=max(lo - kappa, -1.0), hi=min(hi + kappa, 1.0), kappa=kappa, eps=eps, status="certified")


def combine(st_lo, st_hi, lo, hi):
    if "abstain" in (st_lo, st_hi):
        return "abstain"
    if "void" in (st_lo, st_hi):
        return "void"
    if st_lo == st_hi == "certified" and lo > hi:
        return "inconsistent"
    if "certified" in (st_lo, st_hi):
        return "certified"
    return "trivial"


# ------------------------------------------------------------------------------------------------ one repetition
def one_rep(fam, tgt, env, n, rep, methods=METHODS, check_s3=False, time_opt=False):
    ctx = context(fam, tgt, env)
    region, dec = ctx["region"], ctx["dec"]
    ss = np.random.SeedSequence([FAM_ID[fam], TGT[fam].index(tgt), ENVS[fam].index(env), n, rep, 20261128])
    rng_ref, rng_gap, rng_boot = [np.random.default_rng(s) for s in ss.spawn(3)]
    base = dict(family=fam, target=tgt, env=env_label(env), gamma=ctx["gamma"], region=ctx["kind"], n=n, rep=rep,
                V_lo=ctx["m0"]["lo"], V_hi=ctx["m0"]["hi"], true=ctx["true"])
    rows = []

    def emit(method, lo, hi, st_lo, st_hi, status, t_pre=0.0, t_samp=0.0, t_opt=0.0, t_cert=0.0, **extra):
        rows.append(dict(base, method=method, lo=float(lo), hi=float(hi), st_lo=st_lo, st_hi=st_hi, status=status,
                         t_pre=t_pre, t_samp=t_samp, t_opt=t_opt, t_cert=t_cert, **extra))

    k = min(n // 2, 5000)
    need_ref = any(mm in methods for mm in ("M3", "M5", "M6", "B1", "B2", "B3"))
    if need_ref:
        t0 = time.perf_counter()
        f, phi, r = draw(ctx, fam, rng_ref, n, "pi")
        smp = ci.Sample(f, phi, np.exp(-r), np.exp(r))
        t_samp = time.perf_counter() - t0
        train, valid = smp.part(slice(0, k)), smp.part(slice(k, None))
    if any(mm in methods for mm in ("M3", "M5", "M6")):
        t_opt = 0.0
        if time_opt:                             # the optimisation alone, on the same training problem
            t0 = time.perf_counter()
            ci.solve_upper(ci.Problem(train.f, train.phi, Lw=train.L, Gw=train.U - train.L, region=region, wt=np.full(k, 1.0 / k)))
            ci.solve_upper(ci.Problem(-train.f, train.phi, Lw=train.L, Gw=train.U - train.L, region=region, wt=np.full(k, 1.0 / k)))
            t_opt = time.perf_counter() - t0
        t0 = time.perf_counter()
        up = ci.certify_upper(train, valid, region, dec, DELTA / 2)
        low = ci.certify_lower(train, valid, region, dec, DELTA / 2)
        t_tot = time.perf_counter() - t0
        if "M3" in methods:
            emit("M3", low.value, up.value, low.status, up.status, combine(low.status, up.status, low.value, up.value),
                 t_samp=t_samp, t_opt=t_opt if time_opt else math.nan, t_cert=(t_tot - t_opt) if time_opt else math.nan,
                 t_total=t_tot, tau_train_hi=float(up.tau_train), tau_train_lo=float(low.tau_train))
        for mm, kind in (("M5", "hoeffding"), ("M6", "bernstein")):
            if mm in methods:
                t0 = time.perf_counter()
                o = bl.m56_interval(valid, up, low, region, dec, ctx["L_max"], DELTA, kind)
                emit(mm, o["lo"], o["hi"], o["st_lo"], o["st_hi"], combine(o["st_lo"], o["st_hi"], o["lo"], o["hi"]),
                     t_samp=t_samp, t_cert=time.perf_counter() - t0)
    if "B1" in methods:
        t0 = time.perf_counter()
        o = bl.b1_bootstrap(smp.f, smp.phi, smp.L, smp.U, region, rng_boot)
        st = "empty" if not math.isfinite(o["lo"]) else "ok"
        emit("B1", o["lo"], o["hi"], st, st, st, t_samp=t_samp, t_opt=time.perf_counter() - t0, plug_lo=o["plug_lo"],
             plug_hi=o["plug_hi"], n_empty=o["n_empty"], n_unique=o["n_unique"])
    if "B2" in methods:
        t0 = time.perf_counter()
        o = bl.b2_maxent(smp.f, smp.phi, region.c)
        st = "ok" if o["ok"] else "fail"
        emit("B2", o["value"], o["value"], st, st, st, t_samp=t_samp, t_opt=time.perf_counter() - t0, kish=o["kish"], resid=o["resid"])
    if "B3" in methods:
        t0 = time.perf_counter()
        o = bl.b3_pool(smp.f, smp.phi, region)
        st = "empty" if o["empty"] else "ok"
        emit("B3", o["lo"], o["hi"], st, st, st, t_samp=t_samp, t_opt=time.perf_counter() - t0, n_unique=o["n_unique"])
    if any(mm in methods for mm in ("M1", "M2", "M4")):
        t0 = time.perf_counter()
        fq, phq, _ = draw(ctx, fam, rng_gap, n, "q")
        tq = time.perf_counter() - t0
        b, G = ctx["b"], ctx["G"]
        for mm, bound in (("M1", "net"), ("M2", "rademacher")):
            if mm in methods:
                t0 = time.perf_counter()
                o = s3_lumped(b, G, fq, phq, region, DELTA, bound)
                extra = {}
                if check_s3:
                    o2 = ci.s3_interval(b, G, fq, phq, region, DELTA, bound)
                    extra = dict(s3_check=max(abs(o2["lo"] - o["lo"]), abs(o2["hi"] - o["hi"])))
                emit(mm, o["lo"], o["hi"], o["status"], o["status"], o["status"], t_pre=ctx["t"]["bG"], t_samp=tq,
                     t_opt=time.perf_counter() - t0, kappa=o["kappa"], eps=o["eps"], **extra)
        if "M4" in methods:
            t0 = time.perf_counter()
            up = ci.certify_upper_gap(b, G, fq[:k], phq[:k], fq[k:], phq[k:], region, dec, DELTA / 2)
            bn = np.concatenate([b[:-1], [-b[-1]]])
            lw = ci.certify_upper_gap(bn, G, -fq[:k], phq[:k], -fq[k:], phq[k:], region, dec.negated(), DELTA / 2)
            lo = -lw.value
            emit("M4", lo, up.value, lw.status, up.status, combine(lw.status, up.status, lo, up.value), t_pre=ctx["t"]["bG"],
                 t_samp=tq, t_cert=time.perf_counter() - t0)
    return rows


# ------------------------------------------------------------------------------------------------ the grid
def methods_for(fam, env, n, tgt=None):
    """Methods run in a cell.  B1 and, on F3, B3 are restricted for runtime (deviations D2, D3 of the report)."""
    ms = ["M1", "M2", "M3", "M4", "M5", "M6", "B2"]
    if fam != "F3" or (n == 1000 and float(env) <= 1.15 and tgt == "stress"):
        ms.append("B3")
    if n == 1000 and (fam in ("F1", "F2") or (fam == "F3" and env == 1.15 and tgt == "stress")):
        ms.append("B1")
    return ms


def chunks(rep_scale=1.0):
    jobs = []
    for fam in ("F1", "F2", "F3", "F4"):
        for tgt in TGT[fam]:
            for env in ENVS[fam]:
                for n in NS:
                    reps = max(int(round(REPS[n] * rep_scale)), 1)
                    size = 20 if n < 100000 else 10
                    for s in range(0, reps, size):
                        jobs.append((fam, tgt, env, n, s, min(s + size, reps)))
    # expensive chunks first (F3 with B1), for load balance
    jobs.sort(key=lambda j: -(10 if j[0] == "F3" and "B1" in methods_for(j[0], j[2], j[3], j[1]) else 1) * (1 + j[3] / 1e4))
    return jobs


def job_path(job):
    fam, tgt, env, n, a, b = job
    return RES / f"{fam}_{tgt}_{env_label(env)}_{n}_{a:03d}-{b:03d}.jsonl"


def run_job(job):
    fam, tgt, env, n, a, b = job
    out = job_path(job)
    if out.exists():
        return str(out), 0.0
    t0 = time.perf_counter()
    rows = []
    for rep in range(a, b):
        rows += one_rep(fam, tgt, env, n, rep, methods=methods_for(fam, env, n, tgt), check_s3=(rep == 0 and n == 1000), time_opt=(rep < 5))
    tmp = out.with_suffix(".tmp")
    with open(tmp, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    tmp.rename(out)
    return str(out), time.perf_counter() - t0


def write_contexts():
    """Exact side of every cell (M0, B4, B5, timings) in results/contexts.json."""
    out = {}
    for fam in ("F1", "F2", "F3", "F4"):
        for tgt in TGT[fam]:
            for env in ENVS[fam]:
                c = context(fam, tgt, env)
                out[f"{fam}|{tgt}|{env_label(env)}"] = dict(gamma=c["gamma"], region=c["kind"], true=c["true"], m0=c["m0"],
                                                            b4=c["b4"], b5=c["b5"], t=c["t"], G=c["G"], b=c["b"].tolist())
    (HERE / "results" / "contexts.json").write_text(json.dumps(out, indent=1))


def memory_run(method):
    """Peak resident memory of one method on one representative cell (F1, nnn_corr, rho = 1.15, n = 10^5)."""
    fam, tgt, env, n = "F1", "nnn_corr", 1.15, 100000
    context(fam, tgt, env)
    base = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    t0 = time.perf_counter()
    one_rep(fam, tgt, env, n, 0, methods=[method])
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return dict(method=method, cell=f"{fam}|{tgt}|{env}|{n}", base_rss_kib=base, peak_rss_kib=peak, wall=time.perf_counter() - t0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--memory", default="")
    ap.add_argument("--contexts", action="store_true")
    ap.add_argument("--rep-scale", type=float, default=1.0)
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    if args.memory:
        print(json.dumps(memory_run(args.memory)))
        return
    if args.contexts:
        write_contexts()
        return
    if args.probe:
        fams = args.only.split(",") if args.only else ["F1", "F2", "F3", "F4"]
        for fam in fams:
            for n in NS:
                env = 1.15
                t0 = time.perf_counter()
                rows = one_rep(fam, TGT[fam][0], env, n, 0, check_s3=(n == 1000), time_opt=True)
                print(fam, n, f"{time.perf_counter() - t0:.2f}s",
                      {r["method"]: round(r["t_opt"] + r["t_cert"] if not math.isnan(r["t_cert"]) else r["t_total"], 3) for r in rows})
                for r in rows:
                    print("   ", r["method"], round(r["lo"], 4), round(r["hi"], 4), r["status"], "I=", round(r["V_lo"], 4), round(r["V_hi"], 4),
                          {k: r[k] for k in ("s3_check", "kappa") if k in r})
        return
    RES.mkdir(parents=True, exist_ok=True)
    jobs = chunks(rep_scale=args.rep_scale)
    if args.only:
        jobs = [j for j in jobs if j[0] in args.only.split(",")]
    todo = [j for j in jobs if not job_path(j).exists()]
    print(f"{len(todo)} of {len(jobs)} chunks to run", flush=True)
    from multiprocessing import Pool
    t0 = time.perf_counter()
    with Pool(args.workers, maxtasksperchild=40) as pool:
        for i, (p, dt) in enumerate(pool.imap_unordered(run_job, todo)):
            print(f"[{i + 1}/{len(todo)}] {Path(p).name} {dt:.1f}s  (elapsed {time.perf_counter() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
