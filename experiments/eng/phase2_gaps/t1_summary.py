"""T1 table: results/t1_runs.jsonl + our toulbar2 optima (results/export_summary_*.json) + the division's own result rows.

    python experiments/eng/phase2_gaps/t1_summary.py --results <sb-worktree>/experiments/structbio/gmec_dev/results.jsonl
Writes results/t1_summary.json and prints a Markdown table.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", type=Path, required=True)
    args = ap.parse_args()
    runs = {}
    for line in (RES / "t1_runs.jsonl").read_text().splitlines():
        r = json.loads(line)
        runs[(r["model"], r["pdb_id"], r["checker"])] = r
    tb = {}
    for m in ("v2", "v2-lib"):
        for r in json.loads((RES / f"export_summary_{m}.json").read_text()):
            tb[(m, r["pdb_id"])] = r
    theirs = {}
    for line in args.results.read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            if r.get("model") in ("v2", "v2-lib"):
                theirs[(r["model"], r["pdb_id"])] = r          # latest row wins
    rows = []
    print("| model | structure | sites / states / pairs | file, bytes | leaves / branches / eliminations | claimed minimum, kcal/mol "
          "| ours `check_files` | ours `indep_mincheck` (adapter) | SB `mincheck` (a5cc106) | tree proves = claim; witness gap | "
          "checksum of our regenerated tables = file's = SB row's | = SB row's bound; file sha = SB row's | = our toulbar2 optimum "
          "| seconds: check_files / indep / SB (SB row's) |")
    print("|" + "---|" * 14)
    for m in ("v2", "v2-lib"):
        for pid in ("1CRN", "5PTI", "1BPI", "1PGA", "2IGD", "1UBQ"):
            f, i, s = runs[(m, pid, "files")], runs[(m, pid, "indep")], runs[(m, pid, "sb")]
            th, t = theirs[(m, pid)], tb[(m, pid)]
            mb = f["unit_bits"] - 20
            row = dict(model=m, pdb_id=pid, sites=f["sites"], states_total=f["states_total"], pairs=f["pairs"], cert_bytes=f["cert_bytes"],
                       stats=f["stats"], claimed_kcal=f["claimed_lower_bound_kcal"],
                       files=f["accepted"], indep=i["accepted"], sb=s["accepted"],
                       full_box=(f["full_box"], i["full_box"], s["full_box"]),
                       proves_eq_claim=(f["proves"] == f["claimed_lower_bound"] and i["proves"] == i["claimed_lower_bound"]),
                       gap=f["gap"], same_stats=(f["stats"]["prune"] == i["stats"]["prune"] == s["stats"]["prune"] == th["cert_prunes"]
                                                  and f["stats"]["leaf"] == s["stats"]["leaf"] == th["cert_leaves"]
                                                  and f["stats"]["branch"] == s["stats"]["branch"] == th["cert_branches"]),
                       checksum=(f["tables_sha256"] == th["model_sha256"] and f["checksum_matches_certificate"]),
                       sb_row_bound=(abs(th["certified_lower_bound_float"] - f["claimed_lower_bound_kcal"]) == 0),
                       sb_row_bound_exact=(s["lower_bound_kcal"] == th["certified_lower_bound_kcal"]),
                       file_sha=(f["cert_sha256"] == th["cert_sha256"]),
                       toulbar2=(t["toulbar2_optimum_int"] * 2 ** mb == f["claimed_lower_bound"]),
                       seconds=(f["seconds_check"], i["seconds_check"], s["seconds_check"], th["seconds_check_certificate"]))
            rows.append(row)
            st = f["stats"]
            yn = lambda b: "yes" if b else "**no**"  # noqa: E731
            acc = lambda b, fb: ("accepted, full box" if fb else "accepted, partial box") if b else "**rejected**"  # noqa: E731
            print(f"| {m} | {pid} | {row['sites']} / {row['states_total']} / {row['pairs']} | {row['cert_bytes']:,} | "
                  f"{st['leaf']} / {st['branch']} / {st['prune']} | {row['claimed_kcal']:.6f} | {acc(row['files'], f['full_box'])} | "
                  f"{acc(row['indep'], i['full_box'])} | {acc(row['sb'], s['full_box'])} | {yn(row['proves_eq_claim'])}; {row['gap']} | "
                  f"{yn(row['checksum'])} | {yn(row['sb_row_bound'] and row['sb_row_bound_exact'])}; {yn(row['file_sha'])} | {yn(row['toulbar2'])} | "
                  f"{row['seconds'][0]} / {row['seconds'][1]} / {row['seconds'][2]} ({row['seconds'][3]}) |")
    (RES / "t1_summary.json").write_text(json.dumps(rows, indent=1))
    n = len(rows)
    print(f"\n{n} certificates: accepted by check_files {sum(r['files'] for r in rows)}, by indep_mincheck {sum(r['indep'] for r in rows)}, "
          f"by SB mincheck {sum(r['sb'] for r in rows)}; all on the full box {sum(all(r['full_box']) for r in rows)}; "
          f"tree proves exactly the claim {sum(r['proves_eq_claim'] for r in rows)}; zero witness gap {sum(r['gap'] == 0 for r in rows)}; "
          f"checksums agree {sum(r['checksum'] for r in rows)}; node counts agree across checkers and SB rows {sum(r['same_stats'] for r in rows)}; "
          f"= SB row bound {sum(r['sb_row_bound'] and r['sb_row_bound_exact'] for r in rows)}; = our toulbar2 {sum(r['toulbar2'] for r in rows)}; "
          f"verdict disagreements {sum(len({r['files'], r['indep'], r['sb']}) > 1 for r in rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
