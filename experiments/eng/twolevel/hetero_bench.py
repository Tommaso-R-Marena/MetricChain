"""X-014a: certified cost bounds at finite n for cubes with two site types (slopes u_H > u_L), against the lower
bound for every algorithm and against the homogeneous algorithm with the larger slope.

Per cell (u_H, u_L, fraction of heavy sites, n), in nats per site:

  asymptotic      h = max_t sum lambda_j F_j(t) (theory report §11.26: one common slope t), the average of the one-type
                  exponents (not an exponent of the mixed chain), a = sum lambda_j a(u_j), and h, a of u_H alone;
  lower bound     exact at this n (``hetero.hinted_lower_bound``: the smallest weighted dip that changes ln Z by more
                  than the accuracy);
  homogeneous     the certified bound of nested Algorithm 2L+ for the uniform cube with slope u_H — admissible because
                  the class is contained in L_{u_H}(Q_n) — minimised over the family "wide" and the outer fraction;
  type-aligned    the certified bound with every outer block made of sites of one type (``hetero.HSearch``), minimised
                  over the same kind of family and over the outer block of the top level.

    python experiments/eng/twolevel/hetero_bench.py [--procs 3]      # writes results/x014_hetero.jsonl (resumable)
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.twolevel import certified as cert  # noqa: E402
from metricchain_eng.twolevel import hetero as H  # noqa: E402

LID = math.log(20.0)
PHIS = (0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10)
SLOPES = ((2.0, 0.5), (1.0, 0.5), (2.0, 1.0), (4.0, 1.0), (4.0, 0.25))
FRACTIONS = (0.1, 0.25, 0.5, 0.75, 0.9)
SIZES = (1000, 4000, 16000)


def summary(hb: H.HBound) -> dict:
    kinds = Counter(("nested " + s.design.name.split("(")[0] + f", outer slope {s.block[s.design.j][0]:g}") if isinstance(s, H.HBound) else str(s)
                    for s in hb.servers)
    return dict(outer_slope=hb.block[hb.design.j][0], outer_sites=hb.design.k, levels=hb.depth(), servers=dict(kinds))


def cell(uH: float, uL: float, frac: float, n: int, max_levels: int = 3, time_limit: float = 1500.0) -> dict:
    t0 = time.time()
    nH = int(round(frac * n))
    B = H.make_block([(uH, nH), (uL, n - nH)])
    out = dict(kind="hetero", uH=uH, uL=uL, frac=frac, n=n, nH=nH, block=[list(p) for p in B], asymptotic=H.asymptotic(B), rows=[])
    hom_best = math.inf
    het_best = math.inf
    S = cert.Search(uH, "wide")
    HS = H.HSearch()
    S.deadline = HS.deadline = t0 + time_limit
    x_out = None
    for k in range(1, max_levels + 1):
        row = dict(nested_levels=k, complete=True)
        try:
            best = None
            for phi in PHIS:
                lb = S.top(n, cert.top_design(phi), LID, k, cutoff=min(hom_best, best.lCmax if best else math.inf) if k > 1 else (best.lCmax if best else math.inf))
                if lb is not None:
                    best = lb
            if best is not None:
                hom_best = min(hom_best, best.lCmax)
                row.update(homogeneous=best.lCmax / n, homogeneous_phi=best.design.phi)
            else:
                row.update(homogeneous=hom_best / n, homogeneous_phi=None)
            hbest = None
            for j, kk in H.outer_choices(B, PHIS):
                hb = HS.top(B, H.top_design(j, kk), LID, k, cutoff=min(het_best, hbest.lCmax if hbest else math.inf) if k > 1 else (hbest.lCmax if hbest else math.inf))
                if hb is not None:
                    hbest = hb
            if hbest is not None:
                het_best = min(het_best, hbest.lCmax)
                x_out = hbest.xout
                row.update(type_aligned=hbest.lCmax / n, tree=summary(hbest))
            else:
                row.update(type_aligned=het_best / n, tree=None)
        except TimeoutError:
            row["complete"] = False
        row["seconds"] = time.time() - t0
        out["rows"].append(row)
        if not row["complete"]:
            break
    x_out = 0.8715 if x_out is None else x_out
    lb = H.hinted_lower_bound(B, x_out, 0.05)
    out.update(x_out=x_out, lower_bound=lb["lbound"] / n, dip_radius=lb["rho"], seconds=time.time() - t0)
    return out


def tasks(job: str = "hetero1") -> list[dict]:
    """Task list for ``modal_jobs/bench_app.py`` (ids, tiers) and for the local driver."""
    out = []
    if job == "smoke":
        out.append(dict(func="cell", tier="s", kwargs=dict(uH=2.0, uL=0.5, frac=0.25, n=1000, max_levels=2, time_limit=600.0)))
    elif job == "hetero1":
        for n in SIZES:
            for (uH, uL) in SLOPES:
                for f in FRACTIONS:
                    tier = "m" if n <= 4000 else "l"
                    out.append(dict(func="cell", tier=tier, kwargs=dict(uH=uH, uL=uL, frac=f, n=n, max_levels=3,
                                                                       time_limit={"m": 3000.0, "l": 9900.0}[tier])))
    else:
        raise ValueError(job)
    for t_ in out:
        kw = t_["kwargs"]
        t_["id"] = "cell:" + ",".join(f"{k}={kw[k]}" for k in sorted(kw) if k != "time_limit")
    return out


def run_task(task: dict) -> dict:
    return cell(**task["kwargs"])


def _run(kw):
    return cell(**kw)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--procs", type=int, default=3)
    args = ap.parse_args()
    import subprocess
    from multiprocessing import Pool

    out = ROOT / "experiments" / "eng" / "twolevel" / "results" / "x014_hetero.jsonl"
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            r = json.loads(line)
            done.add((r["uH"], r["uL"], r["frac"], r["n"]))
    todo = [t["kwargs"] for t in tasks("hetero1") if (t["kwargs"]["uH"], t["kwargs"]["uL"], t["kwargs"]["frac"], t["kwargs"]["n"]) not in done]
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    print(f"{len(todo)} cells to run ({len(done)} stored) at {commit[:7]}", flush=True)
    with Pool(args.procs) as pool, out.open("a") as fh:
        for r in pool.imap_unordered(_run, todo):
            r["commit"] = commit
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            last = r["rows"][-1]
            print(f"u=({r['uH']:g},{r['uL']:g}) heavy {r['frac']:g} n={r['n']}: LB {r['lower_bound']:.5f} h {r['asymptotic']['h']:.5f} | "
                  + " ".join(f"k={x['nested_levels']}: hom {x.get('homogeneous', float('nan')):.5f} aligned {x.get('type_aligned', float('nan')):.5f}" for x in r["rows"])
                  + f" [{r['seconds']:.0f} s{'' if last['complete'] else ', incomplete'}]", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
