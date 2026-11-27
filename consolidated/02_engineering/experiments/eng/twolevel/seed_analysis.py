"""X-005: which structured instance is the worst one, cell by cell.

For every (u, n, phi) of job M-008 the 63 structured starting points of the search (flat; cone; cone of slope
u/2; plateau-then-cone and cone-then-flat at nine radii; reference point at the median distance, at the centre
and at the antipode) are evaluated under both inner behaviours and the best one is recorded with its type,
together with the gain of the stored search result over it.  Output: results/x005_seeds.json.

    python experiments/eng/twolevel/seed_analysis.py [--workers 4]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_search  # noqa: E402
from metricchain_eng.twolevel.adversary import Family  # noqa: E402
from metricchain_eng.twolevel.ckernel import Evaluator  # noqa: E402
from metricchain_eng.twolevel.tables import cube_constants  # noqa: E402


def labelled_seeds(fam: Family) -> list[tuple[str, float, float, object]]:
    """(type, radius / (Lambda_1 n_o / u), reference fraction, x) in the order of ``Search.seeds``."""
    P, C = fam.ev.P, fam.ev.C
    c = cube_constants(P.u)
    n_o = P.n_o
    s = math.sqrt(n_o)
    crit = c.Lambda1 * n_o / P.u
    radii = sorted(set(float(min(max(r, 0.0), n_o)) for r in
                       [C.r_dag + 1, C.r_dag + s, c.p_u * n_o, c.p_u * n_o + s, 0.9 * crit, crit, 1.1 * crit, 1.3 * crit, n_o / 2]))
    out = []
    for d0f in (0.5, 0.0, 1.0):
        out.append(("flat", 0.0, d0f, fam.encode_two_slope(n_o / 2, 0.0, 0.0, d0f)))
        out.append(("cone", 0.0, d0f, fam.encode_two_slope(n_o / 2, 1.0, 1.0, d0f)))
        out.append(("cone of slope u/2", 0.0, d0f, fam.encode_two_slope(n_o / 2, 0.5, 0.5, d0f)))
        for R in radii:
            out.append(("plateau then cone", R / crit, d0f, fam.encode_two_slope(R, 0.0, 1.0, d0f)))
            out.append(("cone then flat", R / crit, d0f, fam.encode_two_slope(R, 1.0, 0.0, d0f)))
    return out


def one(task: tuple) -> dict:
    u, n, phi, stored = task
    P, _ = run_search.design_params(n, u, phi)
    ev = Evaluator(P)
    fam = Family(ev, k=8, monotone=True)
    best = (-math.inf, None)
    for typ, rel, d0f, x in labelled_seeds(fam):
        F, d0, c_in = fam.decode(x)
        inst = fam.instance(F, d0, c_in)
        for orc in ("bottom", "top"):
            v = ev.run(inst, orc).lcost
            if v > best[0]:
                best = (v, dict(type=typ, radius_over_critical=rel, reference_fraction=d0f, oracle=orc))
    return dict(u=u, n=n, phi=phi, best_seed_value=best[0], best_seed=best[1], stored_best=stored,
                gain_of_search=(stored - best[0]) / (n * cube_constants(u).a))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--nmax", type=int, default=10 ** 9)
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    tasks = []
    for line in (here / "results" / "x005_cost.jsonl").read_text().splitlines():
        c = json.loads(line)
        if c["n"] <= args.nmax:
            stored = max(max(s["best_value"] for s in c["searches"]), max(c["flat"][o]["lcost"] for o in c["flat"]))
            tasks.append((c["u"], c["n"], c["phi"], stored))
    tasks.sort(key=lambda t: -t[1])
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(one, tasks, chunksize=1))
    rows.sort(key=lambda r: (r["u"], r["n"], r["phi"]))
    (here / "results" / "x005_seeds.json").write_text(json.dumps(rows, indent=1))
    print(len(rows), "cells; largest gain of the search over the structured points:", max(r["gain_of_search"] for r in rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
