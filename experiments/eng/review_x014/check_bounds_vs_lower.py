"""Review of ENG-RES-0016: a consistency check between the two halves of the message.

The certified bound of §2/§5 is a bound on the number of evaluations, in every run, of an algorithm whose bracket has
ratio e^{x_out} with probability 1 - delta; the midpoint of the bracket is (x_out/2, delta)-correct, so the bound must be
at least the lower bound of §3 for eps = x_out.  A certified bound BELOW the lower bound would refute one of the two
paper arguments (or the code of one of them).  Evaluated with the division's code (``hetero.HSearch``, ``hetero.constants``,
``hetero.hinted_lower_bound``) on blocks that the 75 cells of the message do not contain: slope ratios up to 80, three
site types, very unequal fractions, small and medium sizes, outer blocks of one type and mixed ones, one to three
nested levels; and with single levels at random parameters (not only the designs of the search).

    python experiments/eng/review_x014/check_bounds_vs_lower.py [--minutes 10]        # writes check_bounds_vs_lower.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE))

from review_sim import limit_memory  # noqa: E402
from metricchain_eng.twolevel import hetero as H  # noqa: E402

LID = math.log(20.0)
LN2 = math.log(2.0)


def lower(B, eps):
    if math.prod(n + 1 for _, n in B) > 2_000_000:          # hetero.weighted_shells enumerates that many shells
        return None
    return H.hinted_lower_bound(B, eps, 0.05)["lbound"]


def random_block(rng):
    kind = rng.integers(4)
    n = int(rng.choice([60, 200, 600, 1000, 2000]))
    if kind == 0:        # extreme ratio, two types
        uH, uL = float(rng.choice([2.0, 4.0, 8.0])), float(rng.choice([0.05, 0.1, 0.25]))
        f = float(rng.choice([0.02, 0.1, 0.5, 0.9, 0.98]))
        nH = min(max(int(round(f * n)), 1), n - 1)
        return H.make_block([(uH, nH), (uL, n - nH)])
    if kind == 1:        # moderate ratio
        uH, uL = float(rng.choice([1.0, 2.0, 3.0])), float(rng.choice([0.5, 0.7, 0.9]))
        nH = int(rng.integers(1, n))
        return H.make_block([(uH, nH), (uL, n - nH)])
    if kind == 2:        # three types (kept small enough for the lower bound's shell enumeration)
        n = min(n, 300)
        us = rng.choice([0.2, 0.5, 1.0, 2.0, 4.0], size=3, replace=False)
        cuts = np.sort(rng.integers(1, n, size=2))
        if cuts[0] == cuts[1]:
            cuts[1] = min(cuts[1] + 1, n - 1)
        parts = [cuts[0], cuts[1] - cuts[0], n - cuts[1]]
        return H.make_block([(float(u), int(k)) for u, k in zip(us, parts) if k > 0])
    u = float(rng.choice([0.5, 1.0, 2.0]))                   # one type: the homogeneous theory
    return H.make_block([(u, n)])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=10.0)
    args = ap.parse_args()
    limit_memory(2.5)
    t0 = time.time()
    rng = np.random.default_rng(1618)
    out = dict(searches=0, single_levels=0, contradictions=[], smallest_ratio_search=None, smallest_ratio_single=None, lower_bound_skipped=0, rows=[])
    deadline = t0 + args.minutes * 60
    # (1) the search, as in the message: top level of certified accuracy 0.8715, 1-3 nested levels, three families of outer blocks
    while time.time() < t0 + 0.6 * args.minutes * 60:
        B = random_block(rng)
        if H.dim(B) < 4:
            continue
        blocks = str(rng.choice(["aligned", "mixed", "both"]))
        depth = int(rng.integers(1, 4))
        choices = H.top_choices(B, blocks=blocks)
        if not choices:
            continue
        j, k, comp = choices[int(rng.integers(len(choices)))]
        D = H.top_design(j, k, comp=comp)
        S = H.HSearch(blocks=blocks)
        S.deadline = time.time() + 20.0
        try:
            res = S.top(B, D, LID, depth)
        except TimeoutError:
            continue
        if res is None:
            continue
        lb = lower(B, res.xout)
        out["searches"] += 1
        if lb is None:
            out["lower_bound_skipped"] += 1
            continue
        row = dict(block=[list(t) for t in B], blocks=blocks, depth=depth, outer=D.name, x_out=res.xout, lCmax=res.lCmax, lbound=lb, ratio=res.lCmax / lb if lb > 0 else None)
        out["rows"].append(row)
        if res.lCmax < lb - 1e-9:
            out["contradictions"].append(row)
        if lb > 0 and (out["smallest_ratio_search"] is None or row["ratio"] < out["smallest_ratio_search"]["ratio"]):
            out["smallest_ratio_search"] = row
    # (2) single levels with random parameters over base brackets (depth 1), any admissible accuracy
    while time.time() < deadline:
        B = random_block(rng)
        if H.dim(B) < 4:
            continue
        choices = H.top_choices(B, blocks="both")
        if not choices:
            continue
        j, k, comp = choices[int(rng.integers(len(choices)))]
        lam, eta = float(rng.choice([1.0, 0.5, 0.2])), float(rng.choice([0.5, 0.25, 0.05]))
        etap, theta = float(rng.choice([1.0, 0.25, 0.05])), float(rng.choice([0.05, 1.0, 20.0, 1e4, 1e12]))
        b = float(rng.choice([0.1, 0.5, 2.0, 10.0]))
        D = H.HDesign(j=j, k=k, comp=comp, lam=lam, eta=eta, etap=etap, b=b, Lr=int(rng.choice([1, 5, 30])), theta=theta, bounded=bool(rng.random() < 0.5))
        C = H.constants(B, D, LID)
        if C is None:
            continue
        lC = H.base_lcost_vec(C.inner, C.xs[1:], C.l_inv_delta_p)
        lCmax = float(np.logaddexp.reduce(np.concatenate([[0.0, LN2 + C.lM_bar], C.lmult() + lC])))
        lb = lower(B, C.x_out)
        out["single_levels"] += 1
        if lb is None:
            out["lower_bound_skipped"] += 1
            continue
        row = dict(block=[list(t) for t in B], outer=[list(t) for t in D.outer(B)], x_out=C.x_out, lCmax=lCmax, lbound=lb, ratio=lCmax / lb if lb > 0 else None,
                   design=dict(lam=lam, eta=eta, etap=etap, theta=theta, b=b))
        if lCmax < lb - 1e-9:
            out["contradictions"].append(row)
        if lb > 0 and (out["smallest_ratio_single"] is None or row["ratio"] < out["smallest_ratio_single"]["ratio"]):
            out["smallest_ratio_single"] = row
    out["seconds"] = time.time() - t0
    (HERE / "check_bounds_vs_lower.json").write_text(json.dumps(out, indent=1, default=float))
    print(f"{out['searches']} searches, {out['single_levels']} single levels, {len(out['contradictions'])} certified bounds below the lower bound; "
          f"lower bound not evaluated in {out['lower_bound_skipped']} cases (too many shells)")
    print("smallest ratio, search:", out["smallest_ratio_search"])
    print("smallest ratio, single level:", out["smallest_ratio_single"])
    for c in out["contradictions"][:10]:
        print("CONTRADICTION", c)
    print(f"[{time.time() - t0:.0f} s]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
