"""T3 table from results/kernel_v2.json (written by t3_collect.py).

    python experiments/eng/phase2_gaps/t3_table.py
"""
from __future__ import annotations

import json
from pathlib import Path

RES = Path(__file__).resolve().parent / "results"
rows = json.loads((RES / "kernel_v2.json").read_text())
yn = lambda b: "yes" if b else ("n/a" if b is None else "**no**")  # noqa: E731
print("| token file | sites / k | leaves / branches / eliminations | `verifyM` on the claimed bound | on bound + 1 unit | witness in box; kernel energy = bound | digests = Python side (unary; pair) | bound = export | `verifyM`, ms (bound + 1) | wall s of the file (run) |")
print("|" + "---|" * 10)
for r in rows:
    L = r["lean"]
    if "error" in L:
        print(f"| {r['name']} | error: {L['error']} |")
        continue
    t = r.get("timing") or {}
    wall = t.get("wall_s")
    wall = f"{wall}" if wall is not None else f"first block at {t.get('first_block_s')} s incl. loading"
    print(f"| {r['name']} | {r['sites']} / {r['states_max']} | {r['leaf']} / {r['branch']} / {r['prune']} | "
          f"{'**accepted**' if L['verifyM_claimed_bound'] else 'refused'} | {'accepted' if L['verifyM_bound_plus_one_unit'] else 'refused'} | "
          f"{yn(L['witness_in_box'])}; {yn(r.get('witness_energy_equals_bound'))} | {yn(r.get('digest_h_matches'))}; {yn(r.get('digest_J_matches'))} | "
          f"{yn(r.get('bound_matches_export'))} | {L['ms_verifyM']} ({L['ms_verifyM_plus_one']}) | {wall} ({t.get('log', '')}) |")
real = [r for r in rows if r["corrupt"] is None and "error" not in r["lean"]]
ctl = [r for r in rows if r["corrupt"] is not None]
print(f"\n{len(real)} certificates run: accepted {sum(r['lean']['verifyM_claimed_bound'] for r in real)}; bound + 1 refused "
      f"{sum(not r['lean']['verifyM_bound_plus_one_unit'] for r in real)}; witness energy = bound {sum(bool(r.get('witness_energy_equals_bound')) for r in real)}; "
      f"both digests match {sum(bool(r.get('digest_h_matches') and r.get('digest_J_matches')) for r in real)}.  "
      f"Negative controls: {len(ctl)}, refused {sum(not r['lean']['verifyM_claimed_bound'] for r in ctl)}.")
