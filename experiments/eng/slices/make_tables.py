"""Tables of ENG-RES-0012 (experiment X-008), generated from ``results/ball_exponents.json``.

    python experiments/eng/slices/make_tables.py                      # print the blocks
    python experiments/eng/slices/make_tables.py --write  FILE.md     # replace <!-- TABLE:name --> ... <!-- /TABLE:name -->
    python experiments/eng/slices/make_tables.py --verify FILE.md     # exit 1 if FILE.md differs from the artifacts
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "results"


def build() -> dict[str, str]:
    d = json.loads((RESULTS / "ball_exponents.json").read_text())
    rows = d["rows"]
    lim = {float(k): v for k, v in d["limits"].items()}
    kappas = sorted({r["kappa"] for r in rows}, reverse=True)
    ns = sorted({r["n"] for r in rows})
    get = {(r["kappa"], r["n"]): r for r in rows}
    blocks = {}
    lines = ["| `n` | " + " | ".join(f"`κ = {k:g}`: `−ln q*/n` | excess `·n/ln n` | best centre type `m/n` | centre in the class" for k in kappas) + " |",
             "|---|" + "---|---|---|---|" * len(kappas)]
    for n in ns:
        cells = []
        for k in kappas:
            r = get[(k, n)]
            ex = r["exponent"] - lim[k]
            cells.append(f"{r['exponent']:.6f} | {ex * n / math.log(n):.3f} | {r['m'] / n:.4f} | {-r['lq_centre_in_class'] / n:.6f}")
        lines.append(f"| {n} | " + " | ".join(cells) + " |")
    lines.append("| limit (theory division) | " + " | ".join(f"{lim[k]:.6f} | — | — | —" for k in kappas) + " |")
    blocks["ball_exponents"] = "\n".join(lines)
    big = [get[(k, max(ns))] for k in kappas]
    blocks["ball_summary"] = (
        f"At `n = {max(ns):,}` the exact values are " + ", ".join(f"`{r['exponent']:.6f}` (`κ = {r['kappa']:g}`)" for r in big)
        + f" against the limits " + ", ".join(f"`{lim[k]:.6f}`" for k in kappas)
        + f": above the limit by " + ", ".join(f"`{(r['exponent'] - lim[r['kappa']]):.6f}`" for r in big)
        + f".  Between `n = 1000` and `n = {max(ns):,}` the excess times `n/ln n` stays between "
        + f"`{min((get[(k, n)]['exponent'] - lim[k]) * n / math.log(n) for k in kappas for n in ns if n >= 1000):.3f}` and "
        + f"`{max((get[(k, n)]['exponent'] - lim[k]) * n / math.log(n) for k in kappas for n in ns if n >= 1000):.3f}`.")
    ex = d["exact"]
    blocks["ball_exact"] = (f"Exact control: for the {len(ex)} cases with `n ≤ {max(e['n'] for e in ex)}` the optimum was recomputed with integer weights and a "
                            f"60-digit comparison; the same ball is selected in {sum(e['float_agrees'] for e in ex)} of {len(ex)} cases and the largest difference "
                            f"of `ln q*` is `{max(e['lq_difference'] for e in ex):.1e}`.")
    return blocks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", type=Path)
    ap.add_argument("--verify", type=Path)
    args = ap.parse_args()
    blocks = build()
    target = args.write or args.verify
    if target is None:
        for k, v in blocks.items():
            print(f"### {k}\n{v}\n")
        return 0
    text = target.read_text()
    new = text
    for name, body in blocks.items():
        pat = re.compile(rf"(<!-- TABLE:{re.escape(name)} -->\n)(?:.*?\n)?(<!-- /TABLE:{re.escape(name)} -->)", re.S)
        new = pat.sub(lambda m: m.group(1) + body + "\n" + m.group(2), new)
    if args.verify:
        print("tables in", target.name, "match the artifacts" if new == text else "DIFFER from the artifacts")
        return 0 if new == text else 1
    target.write_text(new)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
