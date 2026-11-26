#!/usr/bin/env python3
"""R18: the re-run of the engineering division's two checks (their scripts verbatim, their Python reference through
the R18 adapter, pieces of one (job, n[, u]) each) against (i) their stored outputs, cell by cell, and (ii) the
tables `recheck_classification` and `nonproduct` of ENG-RES-0014.

Only pieces whose log ends with "R18-RUNNER done ... exit=0" are used; the others are listed.

usage: python3 -I -B r18_compare_rerun.py
"""
import json
import resource
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENG = Path("/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/eng_ro_1cc4e1c")
RES = ENG / "experiments" / "eng" / "twolevel" / "results"
LOGS = HERE / "logs"


def finished(log: Path):
    if not log.exists():
        return False, "no log"
    lines = log.read_text().splitlines()
    last = lines[-1] if lines else ""
    return (last.startswith("R18-RUNNER done") and " exit=0 " in last), last[:160]


def pieces(script):
    out = []
    for js in sorted(LOGS.glob(f"{script}_*.json")):
        key = js.name[len(script) + 1:-5]
        ok, last = finished(LOGS / f"{script}_{key}.log")
        out.append((key, js, ok, last))
    return out


def main():
    stored_n = {}
    for job in ("cost", "claims", "converge", "converge2"):
        for line in (RES / f"x005_{job}.jsonl").read_text().splitlines():
            if line.strip():
                c = json.loads(line)
                stored_n.setdefault(job, {}).setdefault(c["n"], 0)
                stored_n[job][c["n"]] += len(c["searches"])
    print("stored searches per job and size:", {j: dict(sorted(v.items())) for j, v in stored_n.items()})
    print("total in the four result files:", sum(sum(v.values()) for v in stored_n.values()),
          "; in cost + claims + converge:", sum(sum(stored_n[j].values()) for j in ("cost", "claims", "converge")))

    # ------------------------------------------------------------------ recheck_classification
    theirs = json.loads((RES / "x005_recheck_classification.json").read_text())
    their_cells = {(c["job"], c["u"], c["n"], c["phi"], c.get("seed", 1)): c for c in theirs["cells"]}
    print("\n=== recheck_classification ===")
    print("their stored json: jobs", {j: {k: v[k] for k in ("searches", "in_corner", "legacy_reproduces_stored", "changed", "violations_exact")}
                                      for j, v in theirs["jobs"].items()}, f"; {theirs['seconds']:.0f} s with the C kernel")
    agg = {}
    cells_cmp = dict(n=0, max_stored=0.0, max_exact=0.0, missing=0)
    not_repro = []
    runs = 0
    for key, js, ok, last in pieces("recheck_classification"):
        if not ok:
            print("  NOT USED (log does not end with exit=0):", key, "|", last)
            continue
        d = json.loads(js.read_text())
        for job, v in d["jobs"].items():
            a = agg.setdefault(job, dict(searches=0, in_corner=0, legacy_reproduces_stored=0, changed=0, violations_exact=0, max_abs_legacy_minus_stored=0.0,
                                         max_increase=0.0, max_decrease=0.0, pieces=[]))
            for k in ("searches", "in_corner", "legacy_reproduces_stored", "changed", "violations_exact"):
                a[k] += v[k]
            a["max_abs_legacy_minus_stored"] = max(a["max_abs_legacy_minus_stored"], v["max_abs_legacy_minus_stored"])
            a["max_increase"] = max(a["max_increase"], v["max_increase"])
            a["max_decrease"] = min(a["max_decrease"], v["max_decrease"])
            a["pieces"].append(key)
            if v["legacy_reproduces_stored"] != v["searches"]:
                not_repro.append((key, v["searches"] - v["legacy_reproduces_stored"], v["max_abs_legacy_minus_stored"]))
        for c in d["cells"]:
            k = (c["job"], c["u"], c["n"], c["phi"], c.get("seed", 1))
            t = their_cells.get(k)
            if t is None:
                cells_cmp["missing"] += 1
                continue
            cells_cmp["n"] += 1
            cells_cmp["max_stored"] = max(cells_cmp["max_stored"], abs(c["stored_worst"] - t["stored_worst"]))
            cells_cmp["max_exact"] = max(cells_cmp["max_exact"], abs(c["exact_worst"] - t["exact_worst"]))
    tot = dict(searches=0, in_corner=0, legacy_reproduces_stored=0, changed=0, violations_exact=0)
    for job, a in agg.items():
        print(f"  re-run, job {job}: searches {a['searches']} (pieces: {len(a['pieces'])}); in a corner {a['in_corner']}; cost changed by the exact rule {a['changed']} "
              f"(largest increase {a['max_increase']:.3g}, decrease {a['max_decrease']:.3g}); claims violated under the exact rule {a['violations_exact']}; "
              f"old convention reproduces the stored value in {a['legacy_reproduces_stored']}; largest |difference| {a['max_abs_legacy_minus_stored']:.6g}")
        for k in tot:
            tot[k] += a[k]
    print(f"  RE-RUN TOTAL: {tot['searches']} of the 2,624 searches of the table; in a corner {tot['in_corner']}; changed {tot['changed']}; violated {tot['violations_exact']}; "
          f"reproduced {tot['legacy_reproduces_stored']} of {tot['searches']}")
    print("  pieces with stored values not reproduced by the old convention (piece, how many, largest |difference| in ln):", not_repro)
    print(f"  cells compared with their stored per-cell values: {cells_cmp['n']} (not in their file: {cells_cmp['missing']}); "
          f"largest |stored_worst - theirs| {cells_cmp['max_stored']:.3g}; largest |exact_worst - theirs| {cells_cmp['max_exact']:.3g}")
    print("  table of the message: 2,624 searches; in a corner 0; changed 0; violated 0; reproduced 2,615 of 2,624; others changed by at most 0.69")

    # ------------------------------------------------------------------ nonproduct_bound
    theirs = json.loads((RES / "x005_nonproduct_bound.json").read_text())
    their_cells = {(c["u"], c["n"], c["phi"]): c for c in theirs["cells"]}
    print("\n=== nonproduct_bound ===")
    mine = {}
    for key, js, ok, last in pieces("nonproduct_bound"):
        if not ok:
            print("  NOT USED (log does not end with exit=0):", key, "|", last)
            continue
        d = json.loads(js.read_text())
        for c in d["cells"]:
            mine[(c["u"], c["n"], c["phi"])] = c
    cmp_ = dict(n=0, product=0.0, bound=0.0, gap=0.0, viol=0)
    for k, c in mine.items():
        t = their_cells[k]
        cmp_["n"] += 1
        cmp_["product"] = max(cmp_["product"], abs(c["worst_product"] - t["worst_product"]))
        cmp_["bound"] = max(cmp_["bound"], abs(c["worst_bound"] - t["worst_bound"]))
        cmp_["gap"] = max(cmp_["gap"], abs(c["max_gap"] - t["max_gap"]))
        cmp_["viol"] += (c["violations"] != t["violations"])
    print(f"  cells re-run: {cmp_['n']} of {len(their_cells)}; largest |worst_product - theirs| {cmp_['product']:.3g}; |worst_bound - theirs| {cmp_['bound']:.3g}; "
          f"|max_gap - theirs| {cmp_['gap']:.3g}; cells with a different count of bounds above C_max: {cmp_['viol']}")
    sizes = sorted({k[1] for k in mine})
    print("  sizes re-run:", sizes, "; sizes not re-run:", sorted({k[1] for k in their_cells} - set(sizes)))

    def table(cells):
        by = {}
        for (u, n, phi), c in cells.items():
            b = by.setdefault(u, dict(cells=0, inc=-1.0, inc_at=None, inc_na=0.0, gap=0.0, gap_at=None, gap_na=0.0, above=0))
            b["cells"] += 1
            inc = c["worst_bound"] - c["worst_product"]
            if inc / c["na"] > b["inc_na"]:
                b["inc_na"], b["inc"], b["inc_at"] = inc / c["na"], inc, (n, phi)
            if c["max_gap"] > b["gap"]:
                b["gap"], b["gap_at"] = c["max_gap"], (n, phi)
            b["gap_na"] = max(b["gap_na"], c["max_gap"] / c["na"])
            b["above"] += c["violations"]
        return by
    for label, cells in (("re-run (cells re-run only)", mine), ("their stored json, the same cells", {k: their_cells[k] for k in mine}),
                         ("their stored json, all 468 cells", their_cells)):
        print(f"  {label}:")
        for u, b in sorted(table(cells).items()):
            print(f"    u = {u:g}: cells {b['cells']}; largest increase of a cell's worst cost {b['inc']:.1e} (ln), {b['inc_na']:.1e} (n a) at (n, phi) = {b['inc_at']}; "
                  f"largest gap at a single stored instance {b['gap']:.2g} (ln) at {b['gap_at']}, {b['gap_na']:.2g} (n a); bounds above C_max {b['above']}")
    print("  table of the message:  u = 0.5: 2.6e-12; 2.4e-13 | 1.2e-10; 1.6e-11     u = 1: 6.2e-07; 1.6e-08 | 6.2e-07; 1.6e-08     u = 2: 2.3e-13; 1.7e-16 | 13; 0.026")
    print("peak RSS MB: %.1f" % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))


if __name__ == "__main__":
    main()
