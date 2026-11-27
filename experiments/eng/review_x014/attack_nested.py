"""Review of ENG-RES-0016, the nested use (items 1 and 4 of the brief): three levels end to end with the DIVISION's nested
simulator (``nested_literal.setup`` / ``three_level_run``) on block shapes and slope ratios that X-011f did not use, and on
the referee's instance kinds.  Top level: Algorithm 2L+ on n1 sites of slope u1; every rung is served by a real run of
Algorithm 2L+ on the fibre (outer block n2 sites of slope u2, a block with two slopes), whose rungs are served by exact
enumeration of the base block (n3 sites of slope u3).  The interface under test: the middle run is designed for a
certified accuracy at most the rung's and for the failure probability delta' the top level hands down.

Counted: invalid / too wide / aborted brackets at the top; aborted, invalid and too wide middle runs; queries (the
theorem's accounting) above the nested cost bound.

    python experiments/eng/review_x014/attack_nested.py [--minutes 12] [--procs 2]        # writes attack_nested.json
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "eng" / "twolevel"))
sys.path.insert(0, str(HERE))

import hetero_literal as hl  # noqa: E402
import nested_literal as nl  # noqa: E402
import review_sim as rs  # noqa: E402

CONFIGS = [  # (sizes (top outer, middle outer, base), slopes, tolerance of the top level)
    ((5, 4, 3), (0.1, 3.0, 1.0), 2.5),      # a nearly flat top block over steep fibres
    ((4, 4, 4), (3.0, 0.2, 1.0), 2.5),      # a steep top block over flat middle blocks
    ((6, 3, 2), (0.5, 0.05, 4.0), 2.5),     # middle slope 1/80 of the base slope
    ((3, 5, 3), (2.0, 1.0, 0.1), 2.5),      # a nearly flat base block: the middle ladder is short
    ((7, 2, 2), (1.0, 5.0, 0.3), 2.5),
    ((2, 6, 3), (1.5, 0.4, 2.2), 2.5),      # a top block of two sites
    ((5, 5, 2), (0.3, 1.0, 6.0), 1.0),      # a smaller top tolerance
    ((4, 3, 5), (1.0, 0.1, 0.5), 4.0),      # a larger one
    ((1, 6, 4), (2.5, 0.7, 1.3), 2.5),      # a top block of one site
    ((6, 1, 4), (0.8, 2.0, 0.6), 2.5),      # a middle outer block of one site
]
KINDS = rs.INSTANCE_KINDS
LN2 = math.log(2.0)


def three_level_run_strict(psi: np.ndarray, sizes, S: dict, rng) -> dict:
    """``nested_literal.three_level_run`` with one change in the bookkeeping.  The division's function hands the top level
    the number of queries a middle run ACTUALLY made (its nested results shared between equal sample points), so its
    "theorem's count" at the top multiplies unshared top-level calls by shared middle-level costs.  Here a middle run is
    charged its own theorem's count (every one of its sample points charged its own calls), and that count is also
    compared with the middle run's own bound.  Everything else — ``nested_literal.run_level`` at both levels, the
    designs, the tables — is the division's."""
    n1, n2, n3 = sizes
    tab = psi.reshape(2 ** (n2 + n3), 2 ** n1).T
    lA = float(np.logaddexp.reduce(-psi) - (n1 + n2 + n3) * LN2)
    stats = dict(mid_runs=0, mid_aborts=0, mid_invalid=0, mid_too_wide=0, mid_over_budget=0, mid_inverted=0)

    def serve_top(a: int, l: int):
        fibre = tab[a]
        ftab = fibre.reshape(2 ** n3, 2 ** n2).T
        base = np.logaddexp.reduce(-ftab, axis=1) - n3 * LN2
        D, C, lcm = S["mids"][l - 1]
        r = nl.run_level(float(fibre[0]), ftab[:, 0], n2, C, S["Tmid"], lambda c, _l: (float(base[c]), float(base[c]), 2 ** n3), rng)
        lw = float(np.logaddexp.reduce(base) - n2 * LN2)
        stats["mid_runs"] += 1
        if r["status"] != "closed":
            stats["mid_aborts"] += 1
        else:
            stats["mid_invalid"] += not (r["lL"] <= lw + 1e-9 and lw <= r["lU"] + 1e-9)
            stats["mid_too_wide"] += r["lU"] - r["lL"] > C.x_out + 1e-9
            stats["mid_inverted"] += r["lL"] > r["lU"]
        stats["mid_over_budget"] += math.log(r["q_thm"]) > lcm + 1e-9
        return r["lL"], r["lU"], r["q_thm"]

    r = nl.run_level(float(psi[0]), tab[:, 0], n1, S["Ctop"], S["Ttop"], serve_top, rng)
    return dict(status=r["status"], valid=bool(r["lL"] <= lA + 1e-9 and lA <= r["lU"] + 1e-9), width=r["lU"] - r["lL"], lq_thm=math.log(r["q_thm"]),
                level=r["level"], M=r["M"], nested_calls=r["nested_calls"], **stats)


def task(args):
    ci, seconds, seed = args
    sizes, slopes, b_top = CONFIGS[ci]
    out = dict(config=ci, sizes=list(sizes), slopes=list(slopes), b_top=b_top, seed=seed)
    try:
        S = nl.setup(sizes, slopes, b_top=b_top)
    except (AssertionError, ValueError) as e:
        out["skipped"] = f"no admissible middle design: {e!r}"
        return out
    us = np.array([slopes[0]] * sizes[0] + [slopes[1]] * sizes[1] + [slopes[2]] * sizes[2])
    rng = np.random.default_rng(seed)
    out.update(x_out=S["Ctop"].x_out, lCmax=S["lCmax"], K_top=S["Ctop"].K, J_top=S["Ctop"].J, top_ladder=list(S["Ctop"].xs),
               mid=[dict(design=D.name, b=D.b, x_out=C.x_out, K=C.K, J=C.J, l_inv_delta=S["Ctop"].l_inv_delta_p) for D, C, _ in S["mids"]],
               runs=0, closed=0, invalid=0, too_wide=0, aborted=0, over_budget=0, mid_runs=0, mid_aborts=0, mid_invalid=0, mid_too_wide=0,
               mid_over_budget=0, mid_inverted=0, max_width=0.0, max_lq_thm=0.0, class_violation=-math.inf, by_kind={}, examples=[])
    t0 = time.time()
    i = 0
    while time.time() - t0 < seconds:
        kind = KINDS[i % len(KINDS)]
        i += 1
        psi = rs.instance(kind, us, sizes[0], rng)
        out["class_violation"] = max(out["class_violation"], hl.check_class(psi, us))
        r = three_level_run_strict(psi, sizes, S, rng)
        out["runs"] += 1
        bk = out["by_kind"].setdefault(kind, dict(runs=0, bad=0))
        bk["runs"] += 1
        for key in ("mid_runs", "mid_aborts", "mid_invalid", "mid_too_wide", "mid_over_budget", "mid_inverted"):
            out[key] += r[key]
        bad = False
        if r["status"] != "closed":
            out["aborted"] += 1
            bad = True
        else:
            out["closed"] += 1
            out["invalid"] += not r["valid"]
            out["too_wide"] += r["width"] > S["Ctop"].x_out + 1e-9
            out["max_width"] = max(out["max_width"], r["width"])
            bad = (not r["valid"]) or r["width"] > S["Ctop"].x_out + 1e-9
        out["max_lq_thm"] = max(out["max_lq_thm"], r["lq_thm"])
        if r["lq_thm"] > S["lCmax"] + 1e-9:
            out["over_budget"] += 1
            bad = True
        bad = bad or r["mid_aborts"] or r["mid_invalid"] or r["mid_too_wide"] or r["mid_over_budget"]
        bk["bad"] += bool(bad)
        if bad and len(out["examples"]) < 5:
            out["examples"].append(dict(kind=kind, **{k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in r.items()}))
    out["seconds"] = time.time() - t0
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=12.0)
    ap.add_argument("--procs", type=int, default=2)
    ap.add_argument("--seed", type=int, default=4242)
    args = ap.parse_args()
    rs.limit_memory(1.3)                      # per process; the workers inherit it
    t0 = time.time()
    per = args.minutes * 60 * args.procs / len(CONFIGS)
    with Pool(args.procs) as pool:
        rows = pool.map(task, [(ci, per, args.seed + 31 * ci) for ci in range(len(CONFIGS))], chunksize=1)
    tot = dict(configurations=0, skipped=0)
    for k in ("runs", "closed", "invalid", "too_wide", "aborted", "over_budget", "mid_runs", "mid_aborts", "mid_invalid", "mid_too_wide", "mid_over_budget", "mid_inverted"):
        tot[k] = sum(r.get(k, 0) for r in rows)
    tot["configurations"] = sum("skipped" not in r for r in rows)
    tot["skipped"] = sum("skipped" in r for r in rows)
    tot["max_lq_thm_minus_lCmax"] = max((r["max_lq_thm"] - r["lCmax"] for r in rows if "skipped" not in r and r["runs"]), default=None)
    tot["min_slack_width"] = min((r["x_out"] - r["max_width"] for r in rows if "skipped" not in r and r["closed"]), default=None)
    res = dict(summary=tot, rows=rows, seconds=time.time() - t0)
    (HERE / "attack_nested.json").write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps(tot, indent=1, default=float))
    for r in rows:
        if "skipped" in r:
            print("SKIPPED", r["sizes"], r["slopes"], r["skipped"])
        else:
            print(r["sizes"], r["slopes"], "b_top", r["b_top"], {k: r[k] for k in ("runs", "closed", "invalid", "too_wide", "aborted", "over_budget", "mid_runs", "mid_aborts", "mid_invalid", "mid_too_wide", "mid_over_budget")},
                  f"max width {r['max_width']:.3f} (x_out {r['x_out']:.3f}); ln queries (theorem's count) {r['max_lq_thm']:.1f} (bound {r['lCmax']:.1f})")
    print(f"[{time.time() - t0:.0f} s]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
