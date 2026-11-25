"""X-006: Algorithm 2L+ with real fluctuations of the outer sample (THY-REQ-0001, Part A, outer loop).

Literal runs (``metricchain_eng.twolevel.simulate``: the algorithm pass by pass, with the abort rule) on
radial outer landscapes, with the constants of Theorem 11.56 and with K scaled down, to see

  * whether any claim of the theorem fails on a run on which the good event (V2), (V3) holds;
  * how often the good event itself fails, and how often the returned bracket is invalid, as K shrinks
    (the theorem's K comes from a union bound; the request asks where the events start to fail);
  * how the number of evaluations of sampled runs compares with the mean run used in X-005.

The inner procedures are oracles returning valid brackets ("bottom", "top", "random"; all points of one
(block, shell) group share their brackets), so the event (V1) of the proof -- validity of the inner
brackets -- is true by construction and is NOT tested here.

    python experiments/eng/twolevel/run_sampled.py --case 0 --runs 200
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
import zlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.twolevel.alg2l import Params  # noqa: E402
from metricchain_eng.twolevel.ckernel import Evaluator  # noqa: E402
from metricchain_eng.twolevel.meanrun import Instance, radial_law  # noqa: E402
from metricchain_eng.twolevel.simulate import simulate  # noqa: E402
from metricchain_eng.twolevel.tables import cube_constants  # noqa: E402

SIZES = ((0.5, 300, 6), (1.0, 120, 6), (2.0, 48, 6))          # (u, n_o, n_i): samples stay below 2^61 points
DESIGN = dict(b=0.5, lam=0.5, eta=0.25, etap=0.1, theta=0.1, delta=0.05, rates=(0.9, 0.45, 0.2))
K_SCALES = (1.0, 1 / 4, 1 / 16, 1 / 64, 1 / 256)
ORACLES = ("bottom", "top", "random")


def params(u: float, n_o: int, n_i: int) -> Params:
    d = DESIGN
    xs = [2 * u * n_i] + [r * n_i for r in d["rates"] if d["b"] < r * n_i < 2 * u * n_i] + [d["b"]]
    return Params(n=n_o + n_i, n_o=n_o, u=u, lam=d["lam"], eta=d["eta"], etap=d["etap"], theta=d["theta"],
                  nu1=max(1.0, 2 * math.exp(u) * n_o / d["theta"]), b=d["b"], delta=d["delta"], xs=tuple(xs))


def profiles(u: float, n_o: int, r_dag: int, tables) -> dict[str, np.ndarray]:
    c = cube_constants(u)
    d = np.arange(n_o + 1, dtype=float)
    rng = np.random.default_rng(12345)
    out = {"flat": 0 * d, "cone": u * d, "cone slope u/2": 0.5 * u * d, "anti-cone": -u * d,
           "plateau below r_dag+1, cone above": u * np.maximum(d, r_dag + 1),
           "plateau below p_u n_o, cone above": u * np.maximum(d, int(c.p_u * n_o)),
           "2-periodic": (u / 2) * (-1.0) ** d}
    for frac in (0.9, 1.0, 1.1):
        R = int(frac * c.Lambda1 / u * n_o)
        out[f"dip R={frac:.1f} Lambda1 n_o/u"] = -u * np.maximum(R - d, 0)
    F = np.zeros(n_o + 1)
    F[1:] = np.cumsum(np.minimum(u, np.diff(tables.lball)))
    out["staircase W ~ 1/|B(d)|"] = F
    out["random walk"] = np.concatenate([[0.0], np.cumsum(rng.uniform(-u, u, size=n_o))])
    out["random monotone"] = np.concatenate([[0.0], np.cumsum(rng.uniform(0, u, size=n_o))])
    return out


def cases() -> list[dict]:
    out = []
    for (u, n_o, n_i) in SIZES:
        ev = Evaluator(params(u, n_o, n_i))
        for name in profiles(u, n_o, ev.C.r_dag, ev.outer):
            for oracle in ORACLES:
                for scale in K_SCALES:
                    out.append(dict(u=u, n_o=n_o, n_i=n_i, profile=name, oracle=oracle, k_scale=scale))
    return out


def run_case(case: dict, runs: int, seed: int) -> dict:
    t_start = time.time()
    u, n_o, n_i = case["u"], case["n_o"], case["n_i"]
    P = params(u, n_o, n_i)
    ev = Evaluator(P)
    C = ev.C
    F = profiles(u, n_o, C.r_dag, ev.outer)[case["profile"]]
    psi0, t0 = float(F[n_o // 2]), u * n_i
    K = max(4, int(round(C.K * case["k_scale"])))
    full = case["k_scale"] == 1.0
    mean = ev.run(Instance(radial_law(F, ev.outer), psi0=psi0, t0=t0), "bottom" if case["oracle"] == "random" else case["oracle"])
    # zlib.crc32, not hash(): the built-in hash of a string changes from process to process
    rng = np.random.default_rng([seed, int(u * 10), n_o, zlib.crc32(case["profile"].encode()), ORACLES.index(case["oracle"]), K])
    out = dict(case, K=K, K_theorem=C.K, runs=runs, seed=seed, closed=0, skipped=0, aborted=0, good_event_failed=0, invalid=0,
               invalid_on_good_event=0, width_violations=0, claim_violations_on_good_event=0, violation_examples=[],
               trivial_returned=0, last_rung_ties=0,
               mean_run_lcost=mean.lcost, mean_run_status=mean.status, lCmax=ev.lCmax)
    lq = []
    for _ in range(runs):
        R = simulate(P, ev.outer, C, F, psi0, t0, 0.0, case["oracle"], rng, lC=ev.lC, lCmax=ev.lCmax if full else math.inf,
                     K_override=None if full else K)
        if R.status.startswith("skipped"):
            out["skipped"] += 1
            continue
        closed = R.status.startswith("closed")
        out["closed"] += closed
        out["aborted"] += R.status.startswith("abort")
        out["good_event_failed"] += not R.good_event
        if closed and not R.valid:
            out["invalid"] += 1
            out["invalid_on_good_event"] += R.good_event
        out["width_violations"] += "width" in R.violations
        out["trivial_returned"] += R.trivial_returned
        out["last_rung_ties"] += R.last_rung_ties > 0
        others = [v for v in R.violations if v != "width"]
        if others:
            out["claim_violations_on_good_event"] += 1
            if len(out["violation_examples"]) < 3:
                out["violation_examples"].append(others)
        if closed:
            lq.append(R.lqueries)
    if lq:
        a = np.array(lq)
        out.update(lqueries_mean=float(a.mean()), lqueries_max=float(a.max()), lqueries_min=float(a.min()))
    out["seconds"] = time.time() - t_start
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", type=int, nargs="*")
    ap.add_argument("--runs", type=int, default=100)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    cs = cases()
    if args.list:
        print(len(cs), "cases")
        return 0
    for i in (args.case if args.case else range(len(cs))):
        r = run_case(cs[i], args.runs, args.seed)
        print(json.dumps({k: v for k, v in r.items() if k not in ("violation_examples",)}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
