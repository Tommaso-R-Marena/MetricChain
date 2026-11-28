"""Three robustness experiments for the likelihood-ratio certificate (synthetic; development evidence).

A. ANYTIME + ADAPTIVE: rounds of sampling whose allocation is chosen from earlier rounds (plug-in
   optimal design with safeguard); the region is recomputed after every round and sampling halts the
   first time the interval of the target contrast is narrower than a threshold.  Recorded: whether
   the truth ever left the region at any round (must be <= alpha), coverage at the halting round,
   halting round, final width.
B. MODEL CHECK: one state's sampler is trapped in one well of a double-well system (not equilibrium).
   Recorded: how often the classifier e-test rejects (power), its false-alarm rate under correct
   sampling, and what the confidence statements do when the assumption is violated.  Third scenario:
   every state trapped in the same well (undetectable in principle).
C. CORRELATED SAMPLES: stationary AR(1) samplers with known contraction; the certificate applied
   naively, after thinning by the certified factor, and after thinning by an estimated statistical
   inefficiency; and a slow hidden mode that the estimate cannot see.

Run:  python experiments/mbar/bench/bench_robustness.py [--trials 300]
"""
import argparse
import json
import os
import sys
import warnings
from multiprocessing import Pool

import numpy as np

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
from d9mbar.certificates import (asymptotic_interval, classifier_evalue,  # noqa: E402
                                 lr_confidence_region)
from d9mbar.estimators import mbar, pilot_allocation  # noqa: E402
from scipy.special import logsumexp  # noqa: E402

ALPHA = 0.05


# ------------------------------------------------------------------ A. anytime + adaptive
def discrete_model(overlap, K=4):
    P = np.full((K, K), overlap / (K - 1))
    np.fill_diagonal(P, 1 - overlap)
    fs = np.array([0.0, 0.7, -0.2, 1.1])
    return P, fs - fs[0], -np.log(P * np.exp(-fs[:, None])).T


def trial_A(args):
    overlap, seed, rounds, per_round, target_width = args
    rng = np.random.default_rng(seed)
    P, ftrue, Ut = discrete_model(overlap)
    K = 4
    c = np.array([-1.0, 0, 0, 1.0])
    truth = float(c @ ftrue)
    U = np.zeros((0, K))
    y = np.zeros(0, int)
    batches, ever_out, halt, cover_at_halt, width_at_halt = [], False, None, None, None
    widths = []
    for r in range(rounds):
        if r == 0:
            counts = np.full(K, per_round // K)
        else:
            try:
                counts, _ = pilot_allocation(U, y, c, total_budget=len(y) + per_round, safeguard=0.4)
            except (ValueError, RuntimeError):
                counts = np.full(K, per_round // K)
            counts = np.maximum(counts, 2)
        X = np.concatenate([rng.choice(K, size=int(counts[k]), p=P[k]) for k in range(K)])
        lab = np.repeat(np.arange(K), counts.astype(int))
        batches.append(np.arange(len(y), len(y) + len(lab)))
        U = np.vstack([U, Ut[X]])
        y = np.concatenate([y, lab])
        if r == 0:
            continue
        reg = lr_confidence_region(U, y, alpha=ALPHA, batches=batches)
        if reg.status == "OK":
            inside = reg.contains(ftrue)
            ever_out |= not inside
            lo, hi = reg.interval(c)
            widths.append(hi - lo)
            if halt is None and hi - lo <= target_width:
                halt, cover_at_halt, width_at_halt = r + 1, bool(lo <= truth <= hi), hi - lo
        elif reg.status == "REJECT_MODEL":
            ever_out = True
            widths.append(np.nan)
        else:
            widths.append(np.inf)
    return dict(ever_out=ever_out, halt=halt, cover_at_halt=cover_at_halt, width_at_halt=width_at_halt,
                final_width=widths[-1], n_total=len(y), counts=np.bincount(y, minlength=K).tolist())


# ------------------------------------------------------------------ B. model check
GRID = np.linspace(-2.6, 2.6, 4001)
CENTERS = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
KB = 6.0


def dw_energy(x):
    """U[n, k]: double well 4 (x^2-1)^2 plus harmonic bias KB (x - c_k)^2 / 2, k = 0..4."""
    return 4.0 * (x[:, None] ** 2 - 1) ** 2 + 0.5 * KB * (x[:, None] - CENTERS[None, :]) ** 2


_DW = np.exp(-dw_energy(GRID))
_DWZ = _DW.sum(axis=0)
DW_F = -np.log(_DWZ)
DW_F -= DW_F[0]
_DWP = _DW / _DWZ


def dw_sample(rng, k, n, side=None):
    p = _DWP[:, k].copy()
    if side == "left":
        p[GRID > 0] = 0
    p /= p.sum()
    return rng.choice(GRID, size=n, p=p) + rng.uniform(-0.5, 0.5, n) * (GRID[1] - GRID[0])


def hist_classifier(x_all, y_all, U_all, K, bins=24, tau=20.0):
    def prob(b, prev, cur):
        fprev, _ = mbar(U_all[prev], y_all[prev])
        nprev = np.bincount(y_all[prev], minlength=K)
        Z = np.log(nprev / nprev.sum())[None, :] + fprev[None, :] - U_all[cur]
        pm = np.exp(Z - logsumexp(Z, axis=1)[:, None])            # MBAR's own label predictor
        edges = np.quantile(x_all[prev], np.linspace(0, 1, bins + 1)[1:-1])
        bp, bc = np.searchsorted(edges, x_all[prev]), np.searchsorted(edges, x_all[cur])
        cnt = np.zeros((bins, K))
        np.add.at(cnt, (bp, y_all[prev]), 1.0)
        return (cnt[bc] + tau * pm) / (cnt[bc].sum(axis=1, keepdims=True) + tau)
    return prob


def trial_B(args):
    scenario, n, seed = args
    rng = np.random.default_rng(seed)
    K = len(CENTERS)
    xs = []
    for k in range(K):
        side = None
        if scenario == "one_trapped" and k == 2:
            side = "left"
        if scenario == "all_trapped":
            side = "left"
        xs.append(dw_sample(rng, k, n, side))
    x = np.concatenate(xs)
    y = np.repeat(np.arange(K), n)
    perm = rng.permutation(len(y))
    x, y = x[perm], y[perm]
    U = dw_energy(x)
    c = np.zeros(K)
    c[0], c[-1] = -1.0, 1.0
    truth = float(c @ DW_F)
    out = dict(scenario=scenario, n=n)
    try:
        f, _ = mbar(U, y)
        out["mbar_error"] = float(c @ f - truth)
        out["mbar_error_state2"] = float((f[2] - f[0]) - (DW_F[2] - DW_F[0]))
        logE, _ = classifier_evalue(U, y, hist_classifier(x, y, U, K), n_batches=8)
        out["logE"] = float(logE)
        out["reject"] = bool(logE >= np.log(1 / ALPHA))
        reg = lr_confidence_region(U, y, alpha=ALPHA, n_batches=8)
        out["region_contains_truth"] = bool(reg.contains(DW_F)) if reg.status == "OK" else None
        lo, hi = asymptotic_interval(U, y, c)
        out["asy_covers"] = bool(lo <= truth <= hi)
        c2 = np.zeros(K)
        c2[0], c2[2] = -1.0, 1.0
        lo, hi = asymptotic_interval(U, y, c2)
        out["asy_covers_state2"] = bool(lo <= DW_F[2] - DW_F[0] <= hi)
    except (ValueError, RuntimeError) as err:
        out["failed"] = repr(err)
    return out


# ------------------------------------------------------------------ C. correlated samples
def ar1(rng, x0, sig, phi, n):
    e = rng.normal(size=n)
    x = np.empty(n)
    x[0] = e[0]
    s = np.sqrt(1 - phi * phi)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + s * e[t]
    return x0 + sig * x


def stat_ineff(series):
    """Statistical inefficiency by the initial-positive-sequence rule (as in pymbar.timeseries)."""
    a = series - series.mean()
    v = a @ a / len(a)
    if v == 0:
        return 1.0
    g, t = 1.0, 1
    while t < len(a) - 1:
        cc = (a[:-t] @ a[t:]) / ((len(a) - t) * v)
        if cc <= 0 and t > 3:
            break
        g += 2 * cc * (1 - t / len(a))
        t += 1 if t < 20 else max(1, t // 10)
    return max(1.0, g)


def trial_C(args):
    mode, n, phi, seed = args
    rng = np.random.default_rng(seed)
    K = 5
    ks = 2.0 ** np.arange(K)
    x0 = 0.5 * np.arange(K)
    ftrue = -0.5 * np.log(2 * np.pi / ks)
    ftrue -= ftrue[0]
    c = np.zeros(K)
    c[0], c[-1] = -1.0, 1.0
    truth = float(c @ ftrue)
    series = [ar1(rng, x0[k], 1 / np.sqrt(ks[k]), phi, n) for k in range(K)]

    def energies(x):
        return 0.5 * ks[None, :] * (x[:, None] - x0[None, :]) ** 2

    out = dict(mode=mode, n=n, phi=phi)
    if mode == "naive":
        keep = [np.arange(n)] * K
    elif mode == "certified":                      # stride so that the remaining correlation phi^m <= 0.01
        m = int(np.ceil(np.log(0.01) / np.log(phi)))
        keep = [np.arange(0, n, m)] * K
    elif mode == "iact":                           # stride = known integrated autocorrelation time of x
        m = int(np.ceil((1 + phi) / (1 - phi)))
        keep = [np.arange(0, n, m)] * K
    else:                                          # estimated statistical inefficiency of own-state energy
        keep = []
        for k in range(K):
            g = stat_ineff(energies(series[k])[:, k])
            keep.append(np.arange(0, n, int(np.ceil(g))))
    x = np.concatenate([series[k][keep[k]] for k in range(K)])
    y = np.concatenate([np.full(len(keep[k]), k) for k in range(K)])
    U = energies(x)
    out["kept"] = int(len(y))
    try:
        reg = lr_confidence_region(U, y, alpha=ALPHA, n_batches=8)
        lo, hi = reg.interval(c)
        out["lr_cover"] = bool(lo <= truth <= hi)
        out["lr_joint"] = bool(reg.contains(ftrue)) if reg.status == "OK" else None
        out["lr_width"] = float(hi - lo)
        lo, hi = asymptotic_interval(U, y, c)
        out["asy_cover"] = bool(lo <= truth <= hi)
        out["asy_width"] = float(hi - lo)
    except (ValueError, RuntimeError) as err:
        out["failed"] = repr(err)
    return out


def rate(rows, key):
    v = [r[key] for r in rows if r.get(key) is not None]
    return (float(np.mean(v)), len(v)) if v else (None, 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=300)
    ap.add_argument("--procs", type=int, default=3)
    ap.add_argument("--parts", default="ABC")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "results", "robustness.json"))
    a = ap.parse_args()
    report = dict(alpha=ALPHA, trials=a.trials)
    with Pool(a.procs) as pool:
        if "A" in a.parts:
            report["A"] = []
            for overlap, tw in ((0.35, 0.6), (0.05, 1.5)):
                rows = pool.map(trial_A, [(overlap, 9000 + 7 * i + int(1000 * overlap), 12, 400, tw)
                                          for i in range(a.trials)], chunksize=2)
                halts = [r["halt"] for r in rows if r["halt"] is not None]
                summ = dict(overlap=overlap, target_width=tw, trials=len(rows),
                            ever_excluded_truth=float(np.mean([r["ever_out"] for r in rows])),
                            halted=len(halts), median_halt_round=float(np.median(halts)) if halts else None,
                            coverage_at_halt=rate(rows, "cover_at_halt")[0],
                            median_final_width=float(np.median([r["final_width"] for r in rows])),
                            mean_final_counts=np.mean([r["counts"] for r in rows], axis=0).round(1).tolist())
                report["A"].append(summ)
                print("A", summ, flush=True)
        if "B" in a.parts:
            report["B"] = []
            for scenario in ("equilibrium", "one_trapped", "all_trapped"):
                for n in (200, 1000):
                    rows = pool.map(trial_B, [(scenario, n, 31000 + i) for i in range(a.trials)], chunksize=2)
                    ok = [r for r in rows if "failed" not in r]
                    summ = dict(scenario=scenario, n=n, trials=len(ok),
                                reject_rate=rate(ok, "reject")[0],
                                median_logE=float(np.median([r["logE"] for r in ok])),
                                mbar_rmse_end_to_end=float(np.sqrt(np.mean([r["mbar_error"] ** 2 for r in ok]))),
                                mbar_mean_error_state2=float(np.mean([r["mbar_error_state2"] for r in ok])),
                                lr_region_contains_truth=rate(ok, "region_contains_truth")[0],
                                asymptotic_covers_end_to_end=rate(ok, "asy_covers")[0],
                                asymptotic_covers_state2=rate(ok, "asy_covers_state2")[0])
                    report["B"].append(summ)
                    print("B", summ, flush=True)
        if "C" in a.parts:
            report["C"] = []
            for phi in (0.9, 0.99):
                for mode in ("naive", "iact", "certified", "estimated"):
                    n = 20000
                    rows = pool.map(trial_C, [(mode, n, phi, 52000 + i) for i in range(a.trials)], chunksize=2)
                    ok = [r for r in rows if "failed" not in r]
                    summ = dict(phi=phi, mode=mode, n=n, trials=len(ok),
                                median_kept=float(np.median([r["kept"] for r in ok])),
                                lr_coverage=rate(ok, "lr_cover")[0], lr_joint=rate(ok, "lr_joint")[0],
                                lr_median_width=float(np.median([r["lr_width"] for r in ok])),
                                asy_coverage=rate(ok, "asy_cover")[0],
                                asy_median_width=float(np.median([r["asy_width"] for r in ok])))
                    report["C"].append(summ)
                    print("C", summ, flush=True)
    with open(a.out, "w") as fh:
        json.dump(report, fh, indent=1)
    print("written", a.out)


if __name__ == "__main__":
    main()
