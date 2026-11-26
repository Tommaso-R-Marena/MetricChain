"""X-005c: the worst *product* instance, re-examined after the science division's review SCI-REV-0018 (finding M1).

ENG-RES-0014 §4 compared two searches over the same family of radial instances: the largest number of evaluations
of a product instance (job M-008) and the largest value of the placement-free upper bound (job M-014), and read
the excess of the second over the first as "a bound and not the cost of an instance".  The review shows that in
the cells where the excess is visible a *product* instance has that cost: in the family the place of the fibres
in their trivial brackets and the position of the law relative to the reference value are one parameter
(``c_in``), the bound cuts that tie, and a product instance can cut it too by moving its reference point to a
shell of negligible probability at the end of a ramp.  This script does the three parts of the request R18-ENG-2:

    stored    (i)  per cell, every stored maximiser of the bound search decoded as the product instance it is
                   and evaluated with the kernel (no search); and the product instances stored by the review
    search    (ii) the product search at n <= 500 with added starting points: the reference point in the shells
                   0 and n_o behind a ramp of slope +-u of length Delta/u for Delta in {1/4, 1/2, 3/4, 1} u n_i,
                   c_in at both ends of its range; the stored maximisers of both earlier searches as seeds;
                   three times the earlier budgets.  The bound search is repeated with the same starting points,
                   so that the two are compared like for like.
    seeds     (iii) the same with seeds 2 and 3 at phi in {0.50, 0.85}
    large     a control beyond the request: the added starting points at n = 1000 and 4000 (phi = 0.35, 0.5; the
              earlier budgets), where the review found no visible shortfall

    python experiments/eng/twolevel/r18_products.py stored
    python experiments/eng/twolevel/r18_products.py search --workers 7
    python experiments/eng/twolevel/r18_products.py seeds --workers 7
    python experiments/eng/twolevel/r18_products.py large --workers 6
    python experiments/eng/twolevel/r18_products.py science --dir DIR   # DIR holds the review's data_cell_*.json
"""
from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_search  # noqa: E402
from metricchain_eng.twolevel.adversary import Family, Search  # noqa: E402
from metricchain_eng.twolevel.ckernel import Evaluator  # noqa: E402
from metricchain_eng.twolevel.meanrun import Instance, lipschitz_violation, radial_law  # noqa: E402
from metricchain_eng.twolevel.tables import cube_constants  # noqa: E402

RES = Path(__file__).resolve().parent / "results"
SMALL = (250, 350, 500)
ORACLES = ("bottom", "top")


def load(name: str) -> dict:
    out = {}
    for line in (RES / name).read_text().splitlines():
        r = json.loads(line)
        out[(r["u"], r["n"], r["phi"])] = r
    return out


def product_cost(ev: Evaluator, fam: Family, x) -> dict:
    """Both inner behaviours at the product instance that ``x`` decodes to in ``fam``."""
    F, d0, c_in = fam.decode(np.asarray(x, dtype=float))
    inst = fam.instance(F, d0, c_in)
    out = {}
    for orc in ORACLES:
        R = ev.run(inst, orc)
        out[orc] = dict(lcost=R.lcost, violations=R.violations())
    return out


# ------------------------------------------------------------------ (i) stored maximisers, no search

def stored_cell(key: tuple) -> dict:
    u, n, phi = key
    cost, anyp = load("x005_cost.jsonl")[key], load("x005_anyplacement.jsonl")[key]
    P, _ = run_search.design_params(n, u, phi)
    ev = Evaluator(P)
    fams = {True: Family(ev, k=cost["k"], monotone=True), False: Family(ev, k=cost["k"], monotone=False)}
    old = {orc: max(s["best_value"] for s in cost["searches"] if s["oracle"] == orc) for orc in ORACLES}
    bound = {orc: max(s["best_value"] for s in anyp["searches"] if s["oracle"] == orc) for orc in ORACLES}
    new = dict(old)
    nviol = 0
    source = {orc: "M-008" for orc in ORACLES}
    for s in anyp["searches"]:
        got = product_cost(ev, fams[s["family"] == "monotone"], s["best_x"])
        for orc in ORACLES:
            nviol += len(got[orc]["violations"])
            if got[orc]["lcost"] > new[orc]:
                new[orc] = got[orc]["lcost"]
                source[orc] = f"M-014 maximiser ({s['family']}, {s['oracle']})"
    # the stored product maximisers re-evaluated: the kernel must return the stored values
    recheck = 0.0
    for s in cost["searches"]:
        got = product_cost(ev, fams[s["family"] == "monotone"], s["best_x"])
        recheck = max(recheck, abs(got[s["oracle"]]["lcost"] - s["best_value"]))
    return dict(u=u, n=n, phi=phi, na=n * cost["a"], old=old, bound=bound, new=new, source=source, n_violations=nviol,
                recheck=recheck, lCmax=cost["constants"]["lCmax"])


def run_stored(workers: int) -> None:
    keys = sorted(load("x005_anyplacement.jsonl"))
    t0 = time.time()
    with mp.Pool(workers) as pool:
        rows = pool.map(stored_cell, keys, chunksize=4)
    out = dict(commit=_commit(), seconds=time.time() - t0, rows=rows)
    (RES / "x005c_stored.json").write_text(json.dumps(out, indent=1))
    moved = [r for r in rows if max(r["new"][o] - r["old"][o] for o in ORACLES) > 1e-9]
    worst = lambda d: max(d.values())  # noqa: E731
    print(f"{len(rows)} cells in {time.time() - t0:.0f} s; stored product values reproduced to {max(r['recheck'] for r in rows):.1e};"
          f" violations {sum(r['n_violations'] for r in rows)}")
    print(f"cells where a stored bound-maximiser, as a product instance, costs more than the stored product maximum"
          f" (either behaviour): {len(moved)}")
    big = [r for r in rows if worst(r["bound"]) - worst(r["old"]) > 1e-4 * r["na"]]
    print(f"cells with bound - old product maximum > 1e-4 na: {len(big)};"
          f" of these still > 1e-4 na after (i): {sum(1 for r in big if worst(r['bound']) - worst(r['new']) > 1e-4 * r['na'])}")
    for r in sorted(big, key=lambda r: -(worst(r["bound"]) - worst(r["old"])) / r["na"])[:20]:
        print(f"  u={r['u']} n={r['n']} phi={r['phi']:.2f}: old {worst(r['old']):.6f}  bound {worst(r['bound']):.6f}"
              f"  new {worst(r['new']):.6f}  (bound-old)/na {(worst(r['bound']) - worst(r['old'])) / r['na']:.5f}"
              f"  (bound-new)/na {(worst(r['bound']) - worst(r['new'])) / r['na']:.5f}")


# ------------------------------------------------------------------ (ii), (iii) searches with added starting points

def encode(fam: Family, knots_r: list, slopes: list, d0_frac: float, c_in_frac: float) -> np.ndarray:
    """x for the profile with the given knots (radii) and slopes (in units of u, one more than knots; fewer than k
    knots are padded with the last one, which adds segments of length zero)."""
    k = fam.k
    knots_r = sorted(knots_r)
    assert len(slopes) == len(knots_r) + 1 and len(knots_r) <= k
    pad = k - len(knots_r)
    kn = list(knots_r) + [knots_r[-1] if knots_r else 0.0] * pad
    # padding at the last knot: the segments it adds have length zero and sit before the last segment
    sl = list(slopes[:-1]) + [slopes[-1]] * pad + [slopes[-1]]
    x = np.empty(fam.dim)
    x[:k] = [fam.unwarp(r) for r in kn]
    enc = (lambda v: (v + 0.1) / 1.2) if fam.monotone else (lambda v: ((v + 1.0) / 2.0 + 0.1) / 1.2)
    x[k:2 * k + 1] = [enc(v) for v in sl]
    x[2 * k + 1] = (d0_frac + 0.1) / 1.2
    x[2 * k + 2] = (c_in_frac + 0.1) / 1.2
    return np.clip(x, 0.0, 1.0)


def ramp_seeds(fam: Family) -> list[np.ndarray]:
    """The starting points of R18-ENG-2 (ii): a base shape in the bulk (flat, cone, plateau then cone, cone then
    flat at the radii that matter), the reference point in shell 0 or n_o behind a ramp of slope +-u and length
    Delta/u, and the inner offset at either end of its range."""
    P, C = fam.ev.P, fam.ev.C
    c = cube_constants(P.u)
    n_o = P.n_o
    s = math.sqrt(n_o)
    radii = sorted(set(float(min(max(r, 1.0), n_o - 1.0)) for r in
                       [C.r_dag + 1, C.r_dag + s, c.p_u * n_o, c.Lambda1 * n_o / P.u, n_o / 2]))
    shapes = [([], [0.0]), ([], [1.0]), ([], [0.5])]
    for R in radii:
        shapes.append(([R], [0.0, 1.0]))
        shapes.append(([R], [1.0, 0.0]))
    signs = (1.0,) if fam.monotone else (1.0, -1.0)
    out = []
    for knots, slopes in shapes:
        for frac in (0.25, 0.5, 0.75, 1.0):
            length = min(max(1.0, frac * P.n_i), n_o - 1.0)
            for sg in signs:
                for cf in (0.0, 1.0):
                    # the ramp at the far end, reference point in shell n_o
                    kn = [r for r in knots if r < n_o - length] + [n_o - length]
                    sl = slopes[:len(kn)] + [sg]
                    out.append(encode(fam, kn, sl, 1.0, cf))
                    # the ramp at the near end, reference point in shell 0
                    kn = [length] + [r for r in knots if r > length]
                    sl = [sg] + slopes[len(slopes) - len(kn):]
                    out.append(encode(fam, kn, sl, 0.0, cf))
    return out


class SeededSearch(Search):
    extra: list = []

    def seeds(self) -> list[np.ndarray]:
        return super().seeds() + list(self.extra)


def search_cell(task: dict) -> dict:
    u, n, phi, seed, mult = task["u"], task["n"], task["phi"], task["seed"], task["mult"]
    key = (u, n, phi)
    t_start = time.time()
    cell = task.get("cell") or cell_data(key)          # a remote task carries it: the result files are not in the image
    P, _ = run_search.design_params(n, u, phi)
    ev = Evaluator(P)
    out = dict(u=u, n=n, phi=phi, seed=seed, mult=mult, na=n * cell["a"], lCmax=cell["lCmax"], searches=[])
    for objective in ("cost", "cost_any_placement"):
        for monotone, bud in ((True, mult * cell["budget"]), (False, mult * cell["budget_general"])):
            fam = Family(ev, k=cell["k"], monotone=monotone)
            name = "monotone" if monotone else "general"
            stored = [np.array(x) for x in cell["stored"][name]]
            for orc in ORACLES:
                S = SeededSearch(fam, orc, objective)
                S.extra = ramp_seeds(fam) + stored
                n_seeds = len(S.seeds())
                for x in S.seeds():
                    S.evaluate(x)
                seeds_best = S.res.best_value
                res = S.run(bud + n_seeds, seed=seed)
                F, d0, c_in = fam.decode(res.best_x)
                out["searches"].append(dict(
                    objective=objective, family=name, oracle=orc, n_eval=res.n_eval, n_seeds=n_seeds,
                    best_value=res.best_value, seeds_best=seeds_best, best_x=res.best_x.tolist(), d0=d0, c_in=c_in,
                    c_in_frac=(c_in + P.n_i * cube_constants(u).Lambda1) / (P.n_i * u), psi0=float(F[d0]),
                    lipschitz_violation=lipschitz_violation(F, u), cost_over_cap=res.extremes["cost_over_cap"],
                    n_violations=len(res.violations) if objective == "cost" else None))
    out["seconds"] = time.time() - t_start
    return out


def cell_data(key: tuple) -> dict:
    """What a search of one cell takes from the two earlier jobs: budgets, the number of knots, the constants used
    for reporting, and the stored maximisers of both (starting points)."""
    cost, anyp = load("x005_cost.jsonl")[key], load("x005_anyplacement.jsonl")[key]
    return dict(a=cost["a"], lCmax=cost["constants"]["lCmax"], budget=cost["budget"], budget_general=cost["budget_general"], k=cost["k"],
                stored={name: [s["best_x"] for r in (cost, anyp) for s in r["searches"] if s["family"] == name]
                        for name in ("monotone", "general")})


def task_list(job: str) -> list[dict]:
    if job == "search":
        return [dict(u=u, n=n, phi=phi, seed=1, mult=3) for u in run_search.US for n in SMALL for phi in run_search.PHIS]
    if job == "large":
        return [dict(u=u, n=n, phi=phi, seed=1, mult=1) for u in run_search.US for n in (1000, 4000) for phi in (0.35, 0.5)]
    if job == "seeds":
        return [dict(u=u, n=n, phi=phi, seed=seed, mult=3) for u in run_search.US for n in SMALL for phi in (0.5, 0.85) for seed in (2, 3)]
    raise ValueError(job)


def task_id(job: str, t: dict) -> str:
    return f"{job}:u={t['u']:g},n={t['n']},phi={t['phi']:g},seed={t['seed']}"


def tasks(job: str) -> list[dict]:
    """Driver interface of modal_jobs/bench_app.py: one task per cell, with what it needs from the stored files."""
    return [dict(t, id=task_id(job, t), tier="m", cell=cell_data((t["u"], t["n"], t["phi"]))) for t in task_list(job)]


def run_task(task: dict) -> dict:
    return search_cell({k: v for k, v in task.items() if k not in ("id", "tier")})


def run_searches(job: str, workers: int) -> None:
    out_path = RES / f"x005c_{job}.jsonl"
    done = set()
    if out_path.exists():
        for line in out_path.read_text().splitlines():
            r = json.loads(line)
            done.add((r["u"], r["n"], r["phi"], r["seed"]))
    todo = [t for t in task_list(job) if (t["u"], t["n"], t["phi"], t["seed"]) not in done]
    todo.sort(key=lambda t: -t["n"])
    commit = _commit()
    print(f"{len(todo)} cells to do ({len(done)} stored), commit {commit[:7]}", flush=True)
    t0 = time.time()
    with mp.Pool(workers) as pool, out_path.open("a") as fh:
        for k, r in enumerate(pool.imap_unordered(search_cell, todo), 1):
            r.update(commit=commit, job=job, ran="local", task_id=task_id(job, r))
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            if k % 12 == 0 or k == len(todo):
                print(f"[{k}/{len(todo)}] {time.time() - t0:.0f} s", flush=True)


# ------------------------------------------------------------------ the review's stored product instances

def run_science(directory: Path) -> None:
    rows = []
    for path in sorted(directory.glob("data_cell_*.json")):
        d = json.loads(path.read_text())
        if "product" not in d:
            continue
        u, n, phi = float(d["u"]), int(d["n"]), float(d["phi"])
        P, _ = run_search.design_params(n, u, phi)
        ev = Evaluator(P)
        pr = d["product"]
        F = np.array(pr["F"], dtype=float)
        d1 = int(pr.get("d1", pr.get("d0", d.get("d0", 0))))
        c_in = float(pr["c_in"])
        c = cube_constants(u)
        assert len(F) == P.n_o + 1
        lip = lipschitz_violation(F, u)
        lo, hi = -P.n_i * c.Lambda1, P.n_i * (u - c.Lambda1)
        inst = Instance(radial_law(F, ev.outer, shift=c_in), psi0=float(F[d1]), t0=u * P.n_i + c_in)
        R = ev.run(inst, d["oracle"])
        rows.append(dict(file=path.name, u=u, n=n, phi=phi, oracle=d["oracle"], lcost_kernel=R.lcost,
                         lcost_review=pr.get("lcost_their_reference"), bound_searched=d.get("bound_searched"),
                         worst_product_found=d.get("worst_product_found"), lipschitz_violation=lip,
                         monotone=bool(np.all(np.diff(F) >= -1e-12)), c_in=c_in, c_in_range=(lo, hi),
                         violations=R.violations(), cost_over_cap=R.lcost - R.lCmax, d_ref=d1))
        r = rows[-1]
        print(f"{path.name}: kernel {r['lcost_kernel']:.9f}  review {r['lcost_review']}  bound {r['bound_searched']}"
              f"  earlier product maximum {r['worst_product_found']}  Lipschitz violation {lip:.1e}"
              f"  monotone {r['monotone']}  c_in in range {lo - 1e-9 <= c_in <= hi + 1e-9}  violations {r['violations']}")
    (RES / "x005c_science_instances.json").write_text(json.dumps(dict(commit=_commit(), rows=rows), indent=1))


def _commit() -> str:
    return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("job", choices=("stored", "search", "seeds", "large", "science"))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--dir", type=Path)
    args = ap.parse_args()
    if args.job == "stored":
        run_stored(args.workers)
    elif args.job == "science":
        run_science(args.dir)
    else:
        run_searches(args.job, args.workers)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
