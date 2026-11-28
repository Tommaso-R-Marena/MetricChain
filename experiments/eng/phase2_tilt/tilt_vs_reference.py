"""Supplementary experiment S1 - NOT pre-registered (added after the independent review, finding M1).

Question: at the same total number of draws, how far above the exact upper end V+ is the certified upper bound

 (a) "ref"    from reference draws (Theorem 5.1, ``certify_upper``; half of the draws train the multipliers);
 (b) "tilt"   from draws of the extremal ensemble of the class (Theorem 5.4, ``certify_upper_tilted``), the pilot
              being found on separate draws in two earlier rounds: a quarter of the budget from the reference
              (multipliers and a first root), a quarter from the extremal ensemble at that root (a better root
              and the spread of the score); the remaining half is drawn from the extremal ensemble at
              root + the excess that half can certify to first order, and certifies;
 (c) "oracle" the last round of (b) with the exact optimal multipliers and V+ in place of the estimated root:
              the rate of Theorem 5.4 without the cost of finding the pilot (uses half of the budget).

All samplers are exact (enumerated spaces, lumped by the values of the observables, which changes nothing).
Level 0.025 for the one end, as for each end in the protocol.  "rejection cost" is the number of reference
proposals per draw that an exact rejection sampler of the extremal ensemble would need; it is NOT counted in
the budget, and is reported so that the comparison can be read either way.

Part A: the two-point instance of Theorem 6.1(a), f = x, pi(1) = 1/Gamma.
Part B: families F1 and F3 of the protocol (experiments/eng/certinf/instances.py), uniform envelopes.

    python experiments/eng/phase2_tilt/tilt_vs_reference.py [--workers 3] [--smoke]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "experiments" / "eng" / "certinf"))
from metricchain_eng import certinf as ci  # noqa: E402
import instances as I  # noqa: E402

DELTA_END = 0.025
_CACHE: dict = {}


def two_point(gamma: float) -> dict:
    a = 1.0 / gamma
    return dict(pi=np.array([1 - a, a]), f=np.array([0.0, 1.0]), phi=np.zeros((2, 0)), L=np.ones(2), U=np.full(2, gamma),
                region=ci.Box(), d=ci.Declared(0.0, 1.0, [], [], U_max=gamma), vplus=gamma * a / (1 + (gamma - 1) * a),
                eta_star=np.zeros(0))


def family(name: str, target: str, rho: float) -> dict:
    if name not in _CACHE:
        _CACHE[name] = I.get(name)
    inst = _CACHE[name]
    f = inst.targets[target]
    region, _ = I.data_region(inst, rho)
    uq, inv = np.unique(np.column_stack([inst.phi, f]), axis=0, return_inverse=True)
    pc = np.bincount(np.asarray(inv).reshape(-1), weights=inst.pi, minlength=len(uq))
    fc, phic = uq[:, -1].copy(), uq[:, :-1].copy()
    L, U = np.full(pc.size, math.exp(-rho)), np.full(pc.size, math.exp(rho))
    out = ci.interval(ci.box_problem(pc * L, pc * U, fc, phic, region))
    m = phic.shape[1]
    return dict(pi=pc, f=fc, phi=phic, L=L, U=U, region=region, d=ci.Declared(-1.0, 1.0, -np.ones(m), np.ones(m), U_max=math.exp(rho)),
                vplus=float(out["hi"]), eta_star=np.asarray(out["eta_hi"], dtype=float))


def draw(rng, w, n):
    return rng.choice(w.size, size=n, p=w / w.sum())


def one_rep(S: dict, n: int, rng) -> dict:
    pi, f, phi, L, U, region, d = (S[k] for k in ("pi", "f", "phi", "L", "U", "region", "d"))
    l, u, ratio = pi * L, pi * U, L / U
    lam = math.log(16 / DELTA_END)
    rec = {}
    # (a) reference draws, half to train the multipliers
    i = draw(rng, pi, n)
    smp = ci.Sample(f[i], phi[i], L[i], U[i])
    b = ci.certify_upper(smp.part(slice(0, n // 2)), smp.part(slice(n // 2, None)), region, d, DELTA_END)
    rec["ref"] = [b.value, b.status]
    # (b) draws from the extremal ensemble; the pilot is found on separate draws
    n0 = n1 = n // 4
    n2 = n - n0 - n1
    i = draw(rng, pi, n0)
    tau0, eta, _ = ci.train_multipliers(ci.Sample(f[i], phi[i], L[i], U[i]), region, d)
    if not math.isfinite(tau0):
        tau0, eta = d.f_hi, np.zeros(phi.shape[1])
    tau0 = min(max(tau0, d.f_lo), d.f_hi)
    w = np.where(ci.tilt_indicator(f, phi, region, eta, tau0), u, l)
    i = draw(rng, w, n1)
    root, sd = ci.tilted_root(f[i], phi[i], ratio[i], region, eta, tau0)
    tau2 = root + sd * math.sqrt(2 * lam / n2)
    w = np.where(ci.tilt_indicator(f, phi, region, eta, tau2), u, l)
    i = draw(rng, w, n2)
    b = ci.certify_upper_tilted(f[i], phi[i], ratio[i], region, eta, tau2, d, DELTA_END)
    rec["tilt"] = [b.value, b.status, tau0, root, tau2, float(U.max() * pi.sum() / w.sum())]
    # (c) the last round with an oracle pilot
    es, vp = S["eta_star"], S["vplus"]
    w = np.where(ci.tilt_indicator(f, phi, region, es, vp), u, l)
    z, p = ci.tilted_score(f, phi, ratio, region, es, vp, vp), w / w.sum()
    tau_o = vp + math.sqrt(max(float(p @ z ** 2) - float(p @ z) ** 2, 0.0)) * math.sqrt(2 * lam / n2)
    w = np.where(ci.tilt_indicator(f, phi, region, es, tau_o), u, l)
    i = draw(rng, w, n2)
    b = ci.certify_upper_tilted(f[i], phi[i], ratio[i], region, es, tau_o, d, DELTA_END)
    rec["oracle"] = [b.value, b.status, tau_o]
    return rec


def run_cell(cell):
    kind, par, n, reps, seed = cell
    S = two_point(par) if kind == "A" else family(*par)
    rng = np.random.default_rng(seed)
    t = time.time()
    recs = [one_rep(S, n, rng) for _ in range(reps)]
    return dict(kind=kind, par=par, n=n, reps=reps, seed=seed, vplus=S["vplus"], recs=recs, seconds=round(time.time() - t, 1))


def summarise(res: dict) -> dict:
    v = res["vplus"]
    row = dict(kind=res["kind"], par=res["par"], n=res["n"], reps=res["reps"], vplus=v, seconds=res["seconds"])
    for meth in ("ref", "tilt", "oracle"):
        vals = np.array([r[meth][0] for r in res["recs"]])
        st = [r[meth][1] for r in res["recs"]]
        row[meth] = dict(median_excess=float(np.median(vals) - v), q90_excess=float(np.quantile(vals, 0.9) - v),
                         misses=int(np.sum(vals < v - 1e-9)), trivial=int(sum(s == "trivial" for s in st)),
                         not_certified_or_trivial=int(sum(s not in ("certified", "trivial") for s in st)))
    row["rejection_cost_median"] = float(np.median([r["tilt"][5] for r in res["recs"]]))
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()
    if a.smoke:
        cells = [("A", 100.0, 1000, 3, 1), ("B", ("F1", "nnn_corr", 1.15), 2000, 2, 2)]
    else:
        cells = [("A", g, n, 200, 20261128 + 10 * k + j) for k, g in enumerate((10.0, 100.0, 1000.0, 10000.0)) for j, n in enumerate((1000, 4000, 16000))]
        cells += [("B", ("F1", "nnn_corr", rho), 10000, 100, 20261228 + k) for k, rho in enumerate(I.RHOS)]
        cells += [("B", ("F3", "stress", rho), 10000, 60, 20261328 + k) for k, rho in enumerate(I.RHOS)]
    with Pool(a.workers) as pool:
        results = list(pool.imap(run_cell, cells))
    rows = [summarise(r) for r in results]
    for r in rows:
        print(r["kind"], r["par"], "n", r["n"], "V+ %.4f" % r["vplus"],
              " | ".join("%s med %.4f q90 %.4f miss %d triv %d" % (m, r[m]["median_excess"], r[m]["q90_excess"], r[m]["misses"], r[m]["trivial"])
                         for m in ("ref", "tilt", "oracle")), "| rej %.1f" % r["rejection_cost_median"], "| %ss" % r["seconds"], flush=True)
    if not a.smoke:
        out = Path(__file__).resolve().parent / "results"
        out.mkdir(exist_ok=True)
        (out / "tilt_vs_reference.json").write_text(json.dumps(dict(delta_end=DELTA_END, rows=rows, raw=results), indent=1))


if __name__ == "__main__":
    main()
