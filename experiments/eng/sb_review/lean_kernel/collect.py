"""Turn the printed output of ``RunKernel.lean`` and the summaries written by ``export_for_kernel.py`` into one
result file, comparing what the Lean program saw with what the Python side computed from the published tables.

    python experiments/eng/sb_review/lean_kernel/collect.py --dir DIR --logs LOG [LOG ...] --out FILE

``DIR`` holds ``<name>.tokens`` and ``<name>.export.json``; a log is the standard output of one run of the Lean
program (lines ``file <path>`` followed by ``key value`` lines).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_log(text: str) -> dict:
    out, cur = {}, None
    for line in text.splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "file":
            cur = Path(parts[1]).name[: -len(".tokens")]
            out[cur] = {}
        elif cur is not None and parts[0] in ("verifyM_claimed_bound", "verifyM_bound_plus_one_unit", "verify_claimed_bound", "witness_in_box"):
            out[cur][parts[0]] = parts[1] == "true"
        elif cur is not None and parts[0] in ("claimed_bound", "witness_energy"):
            out[cur][parts[0]] = parts[1]
        elif cur is not None and parts[0] in ("digest_h", "digest_J", "non_integer_entries", "ms_verify", "ms_rest"):
            out[cur][parts[0]] = int(parts[1])
        elif cur is not None and parts[0] == "ms_verifyM":
            out[cur]["ms_verifyM"] = int(parts[1])
            out[cur]["ms_verifyM_plus_one"] = int(parts[3])
        elif cur is not None and parts[0] == "n":
            kv = dict(zip(parts[0::2], parts[1::2]))
            out[cur].update({k: int(v) for k, v in kv.items()})
        elif cur is not None and parts[0] == "error":
            out[cur]["error"] = " ".join(parts[1:])
    return out


def frac(text: str) -> tuple[int, int]:
    a, b = text.split("/")
    return int(a), int(b)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, required=True)
    ap.add_argument("--logs", type=Path, nargs="+", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--full-digest", nargs="*", default=None, help="names whose pair-table digest was computed (flag `full`)")
    args = ap.parse_args()
    seen = {}
    for log in args.logs:
        for name, row in parse_log(log.read_text()).items():
            seen.setdefault(name, {}).update(row)
    rows = []
    for name, lean in sorted(seen.items()):
        ex = json.loads((args.dir / f"{name}.export.json").read_text())
        row = dict(name=name, corrupt=ex["corrupt"], sites=ex["n"], states_max=ex["k"], leaf=ex["leaf"], branch=ex["branch"], prune=ex["prune"],
                   tokens=ex["tokens"], tables_sha256=ex["tables_sha256"], lean=lean)
        if "error" not in lean:
            num, den = frac(lean["claimed_bound"])
            wn, wd = frac(lean["witness_energy"])
            row.update(
                bound_matches_export=num * ex["den"] == ex["claimed_bound_num"] * den,
                digest_h_matches=lean["digest_h"] == ex["digest_h"],
                digest_J_matches=(lean["digest_J"] == ex["digest_J"]) if (args.full_digest is None or name in args.full_digest) else None,
                witness_energy_matches=(wd == 1 and wn == ex["witness_energy_table_units"]) if ex["corrupt"] != "witness-entry" else (wd == 1 and wn == ex["witness_energy_table_units"] - 1),
                witness_energy_equals_bound=wn * den == num * wd,
            )
        rows.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != "tables_sha256"})[:700])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(rows, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
