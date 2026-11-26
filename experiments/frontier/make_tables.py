#!/usr/bin/env python3
"""Generate the tables of docs/frontier_benchmarks/RESULTS.md from the stored result files.

Every number in RESULTS.md comes from one of these files; `--verify RESULTS.md` checks that
each generated table occurs verbatim in the document (so an edited number is detected).

usage: make_tables.py [--verify PATH]
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GMEC = ROOT / "exploratory_gmec" / "results" / "scp10_at_1756529.jsonl"
GMEC_OLD = ROOT / "exploratory_gmec" / "results" / "scp10_at_720e0ec_partial.jsonl"
IDENT = ROOT / "exploratory_identification" / "results" / "controls_pilot.json"
SCORES = ROOT / "freezes" / "FRONTIER-FRZ-0003_casp17_scoring_check"


def fmt_s(x):
    return "—" if x is None else (f"{x:.2f}" if x < 10 else f"{x:.0f}")


def gmec_table(path: Path) -> str:
    rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    out = ["| instance | residues | configurations | toulbar2: outcome | toulbar2 s | certified route: outcome | produce s | check s | ratio produce÷toulbar2 | branch / leaf / prune nodes | certificate MB | reloaded from file and accepted |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: r["n"]):
        tb, sb = r["toulbar2"], r["sb_certified"]
        a = sb.get("as_shipped", {})
        nodes = a.get("nodes", {})
        tb_out = {"optimum_claimed_by_solver": f"optimum {tb.get('cost')} (claimed)",
                  "best_found_at_time_limit_not_proved": f"time limit; best found {tb.get('cost')}, not proved"}.get(tb.get("status"), tb.get("status", "?"))
        if sb.get("status") == "certificate_accepted":
            agree = "= toulbar2" if r.get("values_agree") else "**≠ toulbar2**"
            sb_out = f"certificate accepted, gap 0, {a.get('witness_energy')} ({agree})"
        elif sb.get("status") == "abstained_budget":
            sb_out = "**abstained** (budget)"
        else:
            sb_out = sb.get("status", "?")
        ratio = "—"
        if sb.get("status") == "certificate_accepted" and tb.get("status") == "optimum_claimed_by_solver":
            ratio = f"{sb['seconds'] / tb['seconds']:.0f}×"
        out.append(f"| {r['instance']} | {r['n']} | 10^{r['log10_configurations']:.0f} | {tb_out} | {fmt_s(tb.get('seconds'))} | {sb_out} | "
                   f"{fmt_s(sb.get('seconds'))} | {fmt_s(a.get('check_seconds')) if a else '—'} | {ratio} | "
                   f"{nodes.get('branch', '—')} / {nodes.get('leaf', '—')} / {nodes.get('prune', '—')} | "
                   f"{a['certificate_bytes'] / 1e6:.1f}" + (" | yes |" if a.get("reloaded_from_text_accepted") else " | — |")
                   if a.get("certificate_bytes") else
                   f"| {r['instance']} | {r['n']} | 10^{r['log10_configurations']:.0f} | {tb_out} | {fmt_s(tb.get('seconds'))} | {sb_out} | "
                   f"{fmt_s(sb.get('seconds'))} | — | {ratio} | — | — | — |")
    return "\n".join(out)


def gmec_summary(path: Path) -> str:
    rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    n = len(rows)
    tb_ok = sum(r["toulbar2"].get("status") == "optimum_claimed_by_solver" for r in rows)
    sb_ok = sum(r["sb_certified"].get("status") == "certificate_accepted" for r in rows)
    both = [r for r in rows if r["toulbar2"].get("status") == "optimum_claimed_by_solver"
            and r["sb_certified"].get("status") == "certificate_accepted"]
    agree = sum(bool(r.get("values_agree")) for r in both)
    ratios = sorted(r["sb_certified"]["seconds"] / r["toulbar2"]["seconds"] for r in both)
    nobranch = sum(r["sb_certified"]["as_shipped"]["nodes"]["branch"] == 0 for r in both)
    lines = [f"* instances: {n}; toulbar2 claimed an optimum within the budget on {tb_ok}; the certified route returned an accepted certificate on {sb_ok} and abstained on {n - sb_ok}",
             f"* where both finished ({len(both)}): values agree on {agree}"]
    if ratios:
        lines.append(f"* production time ÷ toulbar2 time on those: min {ratios[0]:.0f}×, median {statistics.median(ratios):.0f}×, max {ratios[-1]:.0f}×")
        lines.append(f"* accepted certificates with **no branch node** (eliminations and one dual bound): {nobranch} of {len(both)}")
    return "\n".join(lines)


def ident_table(path: Path) -> str:
    rows = json.loads(path.read_text())
    out = ["| control | published verdict | recomputed here | published certificate checked exactly | maximum-entropy baseline: data misfit / distance to planted | least-squares baseline: data misfit / distance to planted |",
           "|---|---|---|---|---|---|"]
    for r in rows:
        got = r.get("verdict_recomputed") or f"interval {r.get('interval_recomputed')}"
        pub = r["expected"] + (f" {r['interval_published']}" if r.get("interval_published") else "")
        cert = {True: "yes", False: "**no**", None: "—"}[r.get("certificate_checked_exactly")]
        me = f"{r['maxent_data_misfit_max']:.0e} / " + (f"{r['maxent_tv_to_planted']:.2f}" if "maxent_tv_to_planted" in r else "—")
        ls = f"{r['nnls_data_misfit_max']:.0e} / " + (f"{r['nnls_tv_to_planted']:.2f}" if "nnls_tv_to_planted" in r else "—")
        out.append(f"| {r['id']} | {pub} | {got} | {cert} | {me} | {ls} |")
    return "\n".join(out)


def scores_table(folder: Path) -> str:
    out = ["| target (reference) | model files | groups | median GDT_TS | 10th–90th percentile GDT_TS | median GDT_HA | median lDDT (heavy atoms) | mean abs. difference of GDT_TS between reference chains A and B (max) |",
           "|---|---|---|---|---|---|---|---|"]
    for path in sorted(folder.glob("scores_*.csv")):
        rows = list(csv.DictReader(open(path)))
        col = lambda k: sorted(float(r[k]) for r in rows if r.get(k) not in (None, ""))
        q = lambda v, p: v[min(len(v) - 1, int(p * len(v)))]
        ts, ha, ld = col("gdt_ts_A"), col("gdt_ha_A"), col("lddt_heavy_A")
        diffs = [abs(float(r["gdt_ts_A"]) - float(r["gdt_ts_B"])) for r in rows if r.get("gdt_ts_A") and r.get("gdt_ts_B")]
        name = path.stem.replace("scores_", "").replace("_vs_", " (PDB ") + ")"
        out.append(f"| {name} | {len(rows)} | {len({r['model'].split('_')[0] for r in rows})} | {statistics.median(ts):.2f} | "
                   f"{q(ts, 0.1):.2f}–{q(ts, 0.9):.2f} | {statistics.median(ha):.2f} | {statistics.median(ld):.3f} | "
                   f"{statistics.mean(diffs):.2f} ({max(diffs):.2f}) |")
    return "\n".join(out)


def tables() -> dict:
    t = {}
    if GMEC.is_file():
        t["gmec"] = gmec_table(GMEC)
        t["gmec_summary"] = gmec_summary(GMEC)
    if IDENT.is_file():
        t["ident"] = ident_table(IDENT)
    if any(SCORES.glob("scores_*.csv")):
        t["scores"] = scores_table(SCORES)
    return t


def main() -> int:
    t = tables()
    if len(sys.argv) == 3 and sys.argv[1] == "--verify":
        text = Path(sys.argv[2]).read_text()
        missing = [k for k, v in t.items() if v not in text]
        print("verified" if not missing else f"NOT VERIFIED: tables {missing} differ from the stored results")
        return 1 if missing else 0
    for k, v in t.items():
        print(f"<!-- table: {k} -->\n{v}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
