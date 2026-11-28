#!/usr/bin/env python
"""The composed certificate of Theorem M1 (docs/engineering/phase2/MBAR_INTEGRATION.md) on enumerable models.

Design, methods and predictions: PREDICTIONS.md in this directory (written before this script was run).

    PYTHONPATH=src python experiments/eng/phase2_mbar/multistate_certificate.py            # full run
    PYTHONPATH=src python experiments/eng/phase2_mbar/multistate_certificate.py --quick    # 12 repetitions per cell
    PYTHONPATH=src python experiments/eng/phase2_mbar/multistate_certificate.py --lr       # second run, see below

Second run (--lr; post hoc, not in PREDICTIONS.md): the same draws (same seeds, same order of random calls), with
the free-energy intervals taken from the likelihood-ratio region of the label likelihood (``lr_intervals``; the
e-value property is Theorem B1 of the certified-MBAR division, published on its branch while the first run was
being written up) instead of bridge intervals with path sums.  Methods L-all, L-sel, L-pilot are P-all, P-sel,
P-pilot with those intervals.  P-sel is recomputed as a check that the two runs see the same draws.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np

from metricchain_eng.certinf.multistate import (bridge_intervals, certify_upper_pooled, closure, kl_bounds, lr_intervals,
                                                mbar_fit, weight_envelopes)

HERE = os.path.dirname(os.path.abspath(__file__))
M = 1000
CENTRES = (0.30, 0.35, 0.40, 0.44, 0.47, 0.50)
MODELS = {"R10": dict(h=10.0, kappa=1500.0), "R14": dict(h=14.0, kappa=2200.0)}
OBS = {"barrier": lambda x: ((x >= 0.45) & (x <= 0.55)).astype(float),
       "right": lambda x: (x > 0.5).astype(float),
       "position": lambda x: x.copy()}
ALPHA_F, DELTA_P, DELTA_T = 0.02, 0.03, 0.05
SEED = 20261128
METHODS = ("T", "P-all", "P-sel", "P-pilot", "G")


def model(name: str):
    p = MODELS[name]
    x = (np.arange(M) + 0.5) / M
    V = p["h"] * ((x - 0.25) * (x - 0.75) / 0.0625) ** 2 + 2.0 * x
    lq = np.empty((M, 1 + len(CENTRES)))
    lq[:, 0] = -V
    for j, c in enumerate(CENTRES, 1):
        lq[:, j] = -V - 0.5 * p["kappa"] * (x - c) ** 2
    P = np.exp(lq - lq.max(axis=0))
    P /= P.sum(axis=0)
    return x, lq, P


def root(w_up, w_lo, f, lo, hi):
    """Root in tau of sum [w_up (f - tau)_+ - w_lo (tau - f)_+] (non-increasing in tau)."""
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if np.sum(w_up * np.maximum(f - mid, 0.0) - w_lo * np.maximum(mid - f, 0.0)) > 0:
            lo = mid
        else:
            hi = mid
    return hi


def run_target(rng, P, f, lam, ups, N, indicator):
    idx = rng.choice(M, size=N, p=P[:, 0])
    pil, val = idx[: N // 2], idx[N // 2:]
    tau_lo = 0.0 if indicator else root(ups, lam, f[pil], float(f.min()), float(f.max()))
    big = ups * float(np.max(np.maximum(f - tau_lo, 0.0)))
    b = certify_upper_pooled(f[val], np.full(len(val), lam), np.full(len(val), ups), big, tau_lo, float(f.max()), DELTA_T)
    return dict(T=(b.value, b.status))


def run_pooled(rng, lq, P, f, lam, ups, N, indicator):
    K = P.shape[1]
    n = (N // K) // 2 * 2                                     # draws per state, even
    draws = [rng.choice(M, size=n, p=P[:, j]) for j in range(K)]
    pil = np.concatenate([d[: n // 2] for d in draws])
    val = np.concatenate([d[n // 2:] for d in draws])
    lab = np.repeat(np.arange(K), n // 2)                      # labels of both halves
    cnt = np.full(K, n // 2, dtype=float)
    f0 = mbar_fit(lq[pil], cnt)                                # centre: pilot only
    a = f0 + np.log(cnt / cnt.sum())
    point = f0[None, :] - f0[:, None]                          # the centre as degenerate intervals
    fmin, fmax = float(f.min()), float(f.max())
    out, extra = {}, {}

    cl = closure(*bridge_intervals(lq[val], lab, a, ALPHA_F))  # certified, from the validation half
    clp = closure(*bridge_intervals(lq[pil], lab, a, ALPHA_F)) # pilot rerun: only sizes the declared bound
    if cl is None:
        for name in ("P-all", "P-sel", "P-pilot", "G"):
            out[name] = (fmax, "abstain:inconsistent")
        return out, extra
    lo, hi = cl

    # reference threshold from the pilot with all states (point weights)
    Lp, Up = weight_envelopes(lq[pil], cnt, f0, 0, point, point, lam, ups)
    tau_ref = 0.0 if indicator else root(Up, Lp, f[pil], fmin, fmax)
    frac = np.array([np.mean(f[pil[lab == j]] > tau_ref) for j in range(K)])
    subsets = {"P-all": np.arange(K), "P-sel": np.array([0] + [j for j in range(1, K) if frac[j] >= 0.25]),
               "P-0": np.array([0])}
    extra["sel"] = [int(j) for j in subsets["P-sel"]]

    def setup(S):
        """Everything fixed by the pilot for the sub-mixture S: proportions, bracket start, declared bound."""
        cS = np.where(np.isin(np.arange(K), S), cnt, 0.0)
        mask = np.isin(lab, S)
        if indicator:
            tau_lo = 0.0
        else:
            Lq, Uq = weight_envelopes(lq[pil[mask]], cS, f0, 0, point, point, lam, ups)
            tau_lo = root(Uq, Lq, f[pil[mask]], fmin, fmax)
        pos = np.maximum(f - tau_lo, 0.0)
        _, Ug0 = weight_envelopes(lq, cS, f0, 0, point, point, lam, ups)          # on the whole grid, pilot only
        c = 1.0 if len(S) == 1 else 8.0
        if len(S) > 1 and clp is not None:
            hl = clp[0][0, S] - (f0[S] - f0[0])
            hl[S == 0] = 0.0
            if np.all(np.isfinite(hl)):
                c = 2.0 * math.exp(max(0.0, float(np.max(-hl))))
        return cS, mask, tau_lo, pos, c * float(np.max(Ug0 * pos))

    def cert(S, st, idx, iv, delta):
        """The certificate for the sub-mixture S from the draws idx with the free-energy intervals iv."""
        cS, mask, tau_lo, pos, big = st
        Lg, Ug = weight_envelopes(lq, cS, f0, 0, iv[0], iv[1], lam, ups)          # envelopes on the whole grid
        if not np.all(np.isfinite(Ug)) or float(np.max(Ug * pos)) > big:
            return fmax, "abstain:bound"
        v = idx[mask]
        b = certify_upper_pooled(f[v], Lg[v], Ug[v], big, tau_lo, fmax, delta)
        return b.value, b.status

    st = {name: setup(S) for name, S in subsets.items()}
    for name in ("P-all", "P-sel"):                                               # as registered
        out[name] = cert(subsets[name], st[name], val, (lo, hi), DELTA_P)
    S = subsets["P-sel"]
    hl = lo[0, S] - (f0[S] - f0[0])
    extra["width_lo"] = float(np.max(-hl[S != 0])) if len(S) > 1 else 0.0

    # Post hoc (not in PREDICTIONS.md): the pilot chooses among the three sub-mixtures by rehearsing the
    # certificate on the pilot half with the pilot's own intervals.  Any choice made from the pilot is sound.
    pred = {}
    for name, S in subsets.items():
        if len(S) == 1:
            pred[name] = cert(S, st[name], pil, (point, point), DELTA_T)[0]
        else:
            pred[name] = cert(S, st[name], pil, clp, DELTA_P)[0] if clp is not None else math.inf
    best = min(pred, key=lambda n: (pred[n], len(subsets[n])))
    out["P-pilot"] = (cert(subsets[best], st[best], val, (point, point), DELTA_T) if best == "P-0"
                      else out[best] if best in out else cert(subsets[best], st[best], val, (lo, hi), DELTA_P))
    extra["pilot_choice"] = best

    if indicator:                                              # the interval of the imported item G2
        H = hi - point                                         # upper bounds of h_j - h_i
        r = float(np.max(H))
        s0 = 1.0 / K
        _, W0 = weight_envelopes(lq[val], cnt, f0, 0, point, point, 1.0, 1.0)
        y0 = float(np.mean(s0 * W0 * f[val]))
        if not math.isfinite(r):
            mu = 1.0
        else:
            y_up = min(1.0, math.exp(r) * y0)
            mu = min(1.0, kl_bounds(y_up, len(val), math.log(2.0 / DELTA_P))[1] / s0)
        out["G"] = (ups * mu / (ups * mu + lam * (1.0 - mu)), "certified" if mu < 1.0 else "trivial")
        extra["r"] = r
    return out, extra


def run_pooled_lr(rng, lq, P, f, lam, ups, N, indicator):
    """The second run: the draws of ``run_pooled`` (same calls, same order), stored as multiplicities."""
    K = P.shape[1]
    n = (N // K) // 2 * 2
    draws = [rng.choice(M, size=n, p=P[:, j]) for j in range(K)]
    Cp = np.stack([np.bincount(d[: n // 2], minlength=M) for d in draws]).astype(float)
    Cv = np.stack([np.bincount(d[n // 2:], minlength=M) for d in draws]).astype(float)
    pil = np.concatenate([d[: n // 2] for d in draws])
    val = np.concatenate([d[n // 2:] for d in draws])
    lab = np.repeat(np.arange(K), n // 2)
    cnt = np.full(K, n // 2, dtype=float)
    f0 = mbar_fit(lq[pil], cnt)                                # the same centre as in the first run
    a = f0 + np.log(cnt / cnt.sum())
    point = f0[None, :] - f0[:, None]
    fmin, fmax = float(f.min()), float(f.max())
    out, extra = {}, {}
    cl = closure(*bridge_intervals(lq[val], lab, a, ALPHA_F))
    clp = closure(*bridge_intervals(lq[pil], lab, a, ALPHA_F))
    lr_v = lr_intervals(lq, cnt, f0, ALPHA_F, 0, weights=Cv.sum(axis=0))      # certified: validation half
    lr_p = lr_intervals(lq, cnt, f0, ALPHA_F, 0, weights=Cp.sum(axis=0))      # pilot half: sizes the bound only

    wp_all = Cp.sum(axis=0)
    Lp, Up = weight_envelopes(lq, cnt, f0, 0, point, point, lam, ups)
    tau_ref = 0.0 if indicator else root(Up * wp_all, Lp * wp_all, f, fmin, fmax)
    frac = np.array([(Cp[j] @ (f > tau_ref)) / cnt[j] for j in range(K)])
    subsets = {"all": np.arange(K), "sel": np.array([0] + [j for j in range(1, K) if frac[j] >= 0.25]), "0": np.array([0])}

    def setup(S, piv, mult):
        cS = np.where(np.isin(np.arange(K), S), cnt, 0.0)
        wSp, wSv = Cp[S].sum(axis=0), Cv[S].sum(axis=0)
        if indicator:
            tau_lo = 0.0
        else:
            Lq, Uq = weight_envelopes(lq, cS, f0, 0, point, point, lam, ups)
            tau_lo = root(Uq * wSp, Lq * wSp, f, fmin, fmax)
        pos = np.maximum(f - tau_lo, 0.0)
        _, Ug0 = weight_envelopes(lq, cS, f0, 0, point, point, lam, ups)
        c = 1.0 if len(S) == 1 else 8.0
        if len(S) > 1 and piv is not None:
            hl = piv[0][0, S] - (f0[S] - f0[0])
            hl[S == 0] = 0.0
            if np.all(np.isfinite(hl)):
                c = 2.0 * math.exp(mult * max(0.0, float(np.max(-hl))))
        return cS, wSp, wSv, tau_lo, pos, c * float(np.max(Ug0 * pos))

    def cert(st, w, iv, delta):
        cS, _, _, tau_lo, pos, big = st
        Lg, Ug = weight_envelopes(lq, cS, f0, 0, iv[0], iv[1], lam, ups)
        if not np.all(np.isfinite(Ug)) or float(np.max(Ug * pos)) > big:
            return fmax, "abstain:bound"
        b = certify_upper_pooled(f, Lg, Ug, big, tau_lo, fmax, delta, weights=w)
        return b.value, b.status

    # the check: P-sel of the first run, through the multiplicity form
    if cl is None:
        out["P-sel(check)"] = (fmax, "abstain:inconsistent")
    else:
        st = setup(subsets["sel"], clp, 1.0)
        out["P-sel(check)"] = cert(st, st[2], cl, DELTA_P)

    st = {name: setup(S, lr_p, 2.0) for name, S in subsets.items()}
    for name in ("all", "sel"):
        out["L-" + name] = cert(st[name], st[name][2], lr_v, DELTA_P)
    S = subsets["sel"]
    hl = lr_v[0][0, S] - (f0[S] - f0[0])
    extra["width_lo"] = float(np.max(-hl[S != 0])) if len(S) > 1 else 0.0
    pred = {name: (cert(st[name], st[name][1], (point, point), DELTA_T)[0] if name == "0"
                   else cert(st[name], st[name][1], lr_p, DELTA_P)[0]) for name in subsets}
    best = min(pred, key=lambda q: (pred[q], len(subsets[q])))
    out["L-pilot"] = cert(st["0"], st["0"][2], (point, point), DELTA_T) if best == "0" else out["L-" + best]
    extra["pilot_choice"] = best
    return out, extra


def run_cell_lr(args):
    ci, mname, oname, gamma, N, reps = args
    x, lq, P = model(mname)
    f = OBS[oname](x)
    eps = 0.5 * math.log(gamma)
    lam, ups = math.exp(-eps), math.exp(eps)
    indicator = oname != "position"
    truth = root(P[:, 0] * ups, P[:, 0] * lam, f, float(f.min()), float(f.max()))
    vals, stats, extras = {}, {}, []
    t0 = time.time()
    for child in np.random.SeedSequence([SEED, ci]).spawn(reps):
        rng = np.random.default_rng(child)
        rng.choice(M, size=N, p=P[:, 0])                       # the draws of method T in the first run, discarded
        res, extra = run_pooled_lr(rng, lq, P, f, lam, ups, N, indicator)
        extras.append(extra)
        for k, (v, st) in res.items():
            vals.setdefault(k, []).append(float(v))
            stats.setdefault(k, []).append(st)
    summary = {}
    for k in vals:
        v = np.array(vals[k])
        cert = np.array([q == "certified" for q in stats[k]])
        usable = np.array([q in ("certified", "trivial") for q in stats[k]])
        summary[k] = dict(certified=int(cert.sum()), trivial=int(sum(q == "trivial" for q in stats[k])),
                          abstain=int(sum(q.startswith("abstain") for q in stats[k])),
                          wrong=int(np.sum(v[cert] < truth * (1 - 1e-9))),
                          median_value=float(np.median(v[usable])) if usable.any() else None,
                          median_ratio=float(np.median(v[usable]) / truth) if usable.any() else None,
                          median_excess=float(np.median(v[usable]) - truth) if usable.any() else None)
    choice = {}
    for e in extras:
        choice[e["pilot_choice"]] = choice.get(e["pilot_choice"], 0) + 1
    return dict(cell=ci, model=mname, observable=oname, gamma=gamma, N=N, reps=reps, truth=truth, summary=summary,
                median_width_lo=float(np.median([e["width_lo"] for e in extras])), pilot_choice=choice,
                values=vals, status=stats, seconds=round(time.time() - t0, 1))


def run_cell(args):
    ci, mname, oname, gamma, N, reps = args
    x, lq, P = model(mname)
    f = OBS[oname](x)
    eps = 0.5 * math.log(gamma)
    lam, ups = math.exp(-eps), math.exp(eps)
    indicator = oname != "position"
    truth = root(P[:, 0] * ups, P[:, 0] * lam, f, float(f.min()), float(f.max()))
    ss = np.random.SeedSequence([SEED, ci])
    vals, stats, extras = {}, {}, []
    t0 = time.time()
    for child in ss.spawn(reps):
        rng = np.random.default_rng(child)
        res = run_target(rng, P, f, lam, ups, N, indicator)
        pooled, extra = run_pooled(rng, lq, P, f, lam, ups, N, indicator)
        res.update(pooled)
        extras.append(extra)
        for k, (v, st) in res.items():
            vals.setdefault(k, []).append(float(v))
            stats.setdefault(k, []).append(st)
    summary = {}
    for k in vals:
        v = np.array(vals[k])
        cert = np.array([s == "certified" for s in stats[k]])
        usable = np.array([s in ("certified", "trivial") for s in stats[k]])
        summary[k] = dict(certified=int(cert.sum()), trivial=int(sum(s == "trivial" for s in stats[k])),
                          abstain=int(sum(s.startswith("abstain") for s in stats[k])),
                          void=int(sum(s == "void" for s in stats[k])),
                          wrong=int(np.sum(v[cert] < truth * (1 - 1e-9))),
                          median_value=float(np.median(v[usable])) if usable.any() else None,
                          median_ratio=float(np.median(v[usable]) / truth) if usable.any() else None,
                          median_excess=float(np.median(v[usable]) - truth) if usable.any() else None)
    wl = [e["width_lo"] for e in extras if "width_lo" in e]
    rr = [e["r"] for e in extras if "r" in e and math.isfinite(e["r"])]
    sel, choice = {}, {}
    for e in extras:
        if "sel" in e:
            sel[str(e["sel"])] = sel.get(str(e["sel"]), 0) + 1
        if "pilot_choice" in e:
            choice[e["pilot_choice"]] = choice.get(e["pilot_choice"], 0) + 1
    return dict(cell=ci, model=mname, observable=oname, gamma=gamma, N=N, reps=reps, truth=truth, summary=summary,
                median_width_lo=float(np.median(wl)) if wl else None, median_r=float(np.median(rr)) if rr else None,
                selected=sel, pilot_choice=choice, values=vals, status=stats, seconds=round(time.time() - t0, 1))


def cells(quick: bool):
    out = []
    for mname in ("R10", "R14"):
        for gamma in (1.0, 3.0):
            for N in (40000, 200000):
                out.append((mname, "barrier", gamma, N, 12 if quick else (200 if N <= 40000 else 100)))
    for oname in ("right", "position"):
        for gamma in (1.0, 3.0):
            for N in (4000, 40000):
                out.append(("R10", oname, gamma, N, 12 if quick else 200))
    return [(i,) + c for i, c in enumerate(out)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--lr", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    todo = cells(a.quick)
    t0 = time.time()
    if a.lr:
        with ProcessPoolExecutor(max_workers=a.workers) as ex:
            res = list(ex.map(run_cell_lr, sorted(todo, key=lambda c: -c[4] * c[5])))
        res.sort(key=lambda r: r["cell"])
        first = os.path.join(HERE, "results", "multistate_certificate.json")
        worst = None
        if os.path.exists(first) and not a.quick:              # the same draws?  P-sel of the first run against its recomputation
            with open(first) as fh:
                old = {c["cell"]: c for c in json.load(fh)["cells"]}
            worst = 0.0
            for r in res:
                v1, v2 = np.array(old[r["cell"]]["values"]["P-sel"]), np.array(r["values"]["P-sel(check)"])
                assert old[r["cell"]]["status"]["P-sel"] == r["status"]["P-sel(check)"], r["cell"]
                worst = max(worst, float(np.max(np.abs(v1 - v2) / np.abs(v1))))
        with open(os.path.join(HERE, "results", "multistate_certificate_lr_quick.json" if a.quick else "multistate_certificate_lr.json"), "w") as fh:
            json.dump(dict(seed=SEED, alpha_f=ALPHA_F, delta_pooled=DELTA_P, delta_target=DELTA_T,
                           largest_relative_difference_of_P_sel_from_first_run=worst, cells=res), fh, indent=1)
        names = ("P-sel(check)", "L-all", "L-sel", "L-pilot")
        print(f"{'model':5s} {'obs':8s} {'G':>3s} {'N':>7s} {'truth':>10s} | " + " | ".join(f"{m:>26s}" for m in names))
        for r in res:
            row = [f"x{q['median_ratio']:9.3f} +{q['median_excess']:8.2e} w{q['wrong']} a{q['abstain']}" for q in (r["summary"][m] for m in names)]
            print(f"{r['model']:5s} {r['observable']:8s} {r['gamma']:3.0f} {r['N']:7d} {r['truth']:10.3e} | " + " | ".join(row)
                  + f" | lo-width {r['median_width_lo']:.3f}, pilot {r['pilot_choice']}, {r['seconds']} s")
        print(f"largest relative difference of P-sel between the two runs: {worst}")
        print(f"total {time.time() - t0:.0f} s")
        return
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        res = list(ex.map(run_cell, sorted(todo, key=lambda c: -c[4] * c[5])))
    res.sort(key=lambda r: r["cell"])
    name = "multistate_certificate_quick.json" if a.quick else "multistate_certificate.json"
    with open(os.path.join(HERE, "results", name), "w") as fh:
        json.dump(dict(seed=SEED, alpha_f=ALPHA_F, delta_pooled=DELTA_P, delta_target=DELTA_T, cells=res), fh, indent=1)
    print(f"{'model':5s} {'obs':8s} {'G':>3s} {'N':>7s} {'truth':>10s} | " + " | ".join(f"{m:>26s}" for m in METHODS))
    for r in res:
        row = []
        for m in METHODS:
            s = r["summary"].get(m)
            row.append(f"{'':26s}" if s is None else
                       f"x{s['median_ratio']:9.3f} +{s['median_excess']:8.2e} w{s['wrong']} a{s['abstain']}")
        print(f"{r['model']:5s} {r['observable']:8s} {r['gamma']:3.0f} {r['N']:7d} {r['truth']:10.3e} | " + " | ".join(row)
              + f" | lo-width {r['median_width_lo']}, r {r['median_r']}, sel {r['selected']}, pilot {r['pilot_choice']}, {r['seconds']} s")
    print(f"total {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
