"""Coverage, width and abstention of confidence statements for free-energy differences, on models
with exactly known free energies and exact independent samplers (development evidence; synthetic).

Methods, all at nominal error 0.05 and all given the same pooled sample:
  LR8      likelihood-ratio e-process region of this division, 8 batches (first one only trains)
  LR2      the same with 2 batches (split likelihood ratio)
  C1       handoff no-split cut-score certificate (observable_cut_radius at the MBAR fit)
  C2       handoff bridge intervals; pilot = MBAR fit of the first half, intervals from the second
  ASY      MBAR estimate +- 1.96 * asymptotic standard error (standard practice; no guarantee)
  BOOT     percentile bootstrap within states (no guarantee), fewer repetitions
For the contrast f_{K-1} - f_0 we record coverage and width; for LR8/LR2/C1/C2 also whether the
statement is simultaneously right for all pairs (their guarantee is simultaneous).

Run:  python experiments/mbar/bench/bench_certificates.py [--trials 200] [--out results/...json]
"""
import argparse
import importlib.util
import json
import os
import sys
import time
import warnings
from multiprocessing import Pool

import numpy as np

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
from d9mbar.certificates import asymptotic_interval, bootstrap_interval, lr_confidence_region  # noqa: E402
from d9mbar.estimators import mbar  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "handoff_ref", os.path.join(HERE, "..", "handoff", "MBAR_strengthened", "software", "mbar_certified.py"))
handoff = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handoff)


def discrete_model(overlap, K=4):
    P = np.full((K, K), overlap / (K - 1))
    np.fill_diagonal(P, 1 - overlap)
    fs = np.array([0.0, 0.7, -0.2, 1.1])[:K]
    Utable = -np.log(P * np.exp(-fs[:, None])).T          # U[x, k] = -log q_k(x), q_k = P_k exp(-f_k)
    return P, fs - fs[0], Utable


def sample_discrete(rng, P, Utable, n):
    K = P.shape[0]
    X = np.concatenate([rng.choice(P.shape[1], size=n[k], p=P[k]) for k in range(K)])
    return Utable[X], np.repeat(np.arange(K), n)


def harmonic_model(K=5, spread=0.5):
    ks = 2.0 ** np.arange(K)
    x0 = spread * np.arange(K)
    f = -0.5 * np.log(2 * np.pi / ks)
    return ks, x0, f - f[0]


def sample_harmonic(rng, ks, x0, n):
    K = len(ks)
    X = np.concatenate([rng.normal(x0[k], 1 / np.sqrt(ks[k]), n[k]) for k in range(K)])
    return 0.5 * ks[None, :] * (X[:, None] - x0[None, :]) ** 2, np.repeat(np.arange(K), n)


def one_trial(args):
    regime, seed, do_boot = args
    rng = np.random.default_rng(seed)
    kind = regime["kind"]
    if kind == "discrete":
        P, ftrue, Ut = discrete_model(regime["overlap"])
        K = len(ftrue)
        n = np.full(K, regime["n"])
        U, y = sample_discrete(rng, P, Ut, n)
    else:
        ks, x0, ftrue = harmonic_model(regime["K"], regime["spread"])
        K = len(ftrue)
        n = np.full(K, regime["n"])
        U, y = sample_harmonic(rng, ks, x0, n)
    # independent samples: a random order within states is as good as any
    perm = rng.permutation(len(y))
    U, y = U[perm], y[perm]
    c = np.zeros(K)
    c[0], c[-1] = -1.0, 1.0
    truth = float(c @ ftrue)
    dtrue = ftrue[None, :] - ftrue[:, None]
    out = {}

    def rec(name, lo, hi, joint=None, t=None, extra=None):
        out[name] = dict(lo=float(lo), hi=float(hi), cover=bool(lo <= truth <= hi),
                         width=float(hi - lo), finite=bool(np.isfinite(hi - lo)), joint=joint, time=t)
        if extra:
            out[name].update(extra)

    try:
        fhat, _ = mbar(U, y)
    except (ValueError, RuntimeError):
        fhat = None
    out["mbar_error"] = None if fhat is None else float(c @ fhat - truth)
    for name, nb in (("LR8", 8), ("LR2", 2)):
        t0 = time.time()
        reg = lr_confidence_region(U, y, alpha=0.05, n_batches=nb)
        lo, hi = reg.interval(c)
        joint = bool(reg.contains(ftrue)) if reg.status == "OK" else (reg.status != "REJECT_MODEL")
        rec(name, lo, hi, joint, time.time() - t0, dict(status=reg.status, regret=reg.meta.get("regret")))
    # C1 at the MBAR fit
    t0 = time.time()
    if fhat is None:
        rec("C1", -np.inf, np.inf, True, 0.0)
    else:
        r = handoff.observable_cut_radius(U, y, fhat, 0.05)
        est = float(c @ fhat)
        rec("C1", est - r, est + r, bool(np.ptp(fhat - ftrue) <= r), time.time() - t0)
    # C2: pilot from the first half, validation on the second half
    t0 = time.time()
    half = np.zeros(len(y), bool)
    for k in range(K):
        idx = np.where(y == k)[0]
        half[idx[: len(idx) // 2]] = True
    try:
        pilot, _ = mbar(U[half], y[half])
        res = handoff.bridge_intervals(U[~half], y[~half], pilot, 0.05)
        lo, hi = res["lower"][0, K - 1], res["upper"][0, K - 1]
        joint = bool(np.all(dtrue >= res["lower"] - 1e-12) and np.all(dtrue <= res["upper"] + 1e-12))
        rec("C2", lo, hi, joint, time.time() - t0)
    except (ValueError, RuntimeError):
        rec("C2", -np.inf, np.inf, True, time.time() - t0)
    if fhat is not None:
        t0 = time.time()
        lo, hi = asymptotic_interval(U, y, c)
        rec("ASY", lo, hi, None, time.time() - t0)
        if do_boot:
            t0 = time.time()
            lo, hi = bootstrap_interval(U, y, c, B=100, rng=rng)
            rec("BOOT", lo, hi, None, time.time() - t0)
    return out


def summarise(rows, name):
    r = [x[name] for x in rows if name in x]
    if not r:
        return None
    fin = [x for x in r if x["finite"]]
    joint = [x["joint"] for x in r if x["joint"] is not None]
    return dict(trials=len(r), coverage=float(np.mean([x["cover"] for x in r])),
                finite=len(fin), median_width=float(np.median([x["width"] for x in fin])) if fin else None,
                joint_coverage=float(np.mean(joint)) if joint else None,
                median_time=float(np.median([x["time"] for x in r])),
                median_regret=float(np.median([x["regret"] for x in r if x.get("regret") is not None]))
                if any(x.get("regret") is not None for x in r) else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=200)
    ap.add_argument("--boot-trials", type=int, default=40)
    ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--out", default=os.path.join(HERE, "..", "results", "certificates_coverage.json"))
    a = ap.parse_args()
    regimes = [dict(kind="discrete", overlap=o, n=n) for n in (100, 1000, 10000) for o in (0.05, 0.35)]
    regimes += [dict(kind="harmonic", K=5, spread=0.5, n=n) for n in (100, 1000)]
    regimes += [dict(kind="harmonic", K=2, spread=1.0, n=n) for n in (100, 1000)]
    regimes += [dict(kind="harmonic", K=10, spread=0.25, n=500)]
    report = dict(seed_base=20261128, trials=a.trials, regimes=[])
    with Pool(a.procs) as pool:
        for ri, regime in enumerate(regimes):
            jobs = [(regime, 20261128 + 1000 * ri + t, t < a.boot_trials) for t in range(a.trials)]
            rows = pool.map(one_trial, jobs, chunksize=4)
            errs = [x["mbar_error"] for x in rows if x["mbar_error"] is not None]
            summ = dict(regime=regime, mbar_rmse=float(np.sqrt(np.mean(np.square(errs)))) if errs else None,
                        mbar_failures=len(rows) - len(errs),
                        methods={m: summarise(rows, m) for m in ("LR8", "LR2", "C1", "C2", "ASY", "BOOT")})
            report["regimes"].append(summ)
            line = {m: (None if v is None else (round(v["coverage"], 3), v["finite"],
                                                 None if v["median_width"] is None else round(v["median_width"], 3)))
                    for m, v in summ["methods"].items()}
            print(regime, "rmse", None if not errs else round(summ["mbar_rmse"], 4), line, flush=True)
    with open(a.out, "w") as fh:
        json.dump(report, fh, indent=1)
    print("written", a.out)


if __name__ == "__main__":
    main()
