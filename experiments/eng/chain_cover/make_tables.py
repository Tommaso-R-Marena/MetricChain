#!/usr/bin/env python3
"""Generate the Markdown tables of ENG-RES-0002 from the stored artifacts.

Every number in the tables of ``docs/collaboration/responses/engineering/ENG-RES-0002.md`` is
produced by this script from ``data/`` and ``results/`` -- nothing is typed by hand.

    python experiments/eng/chain_cover/make_tables.py            # print the tables
    python experiments/eng/chain_cover/make_tables.py --write F  # replace the marked blocks in file F
    python experiments/eng/chain_cover/make_tables.py --verify F # exit 1 if F's blocks differ

A block in a document is delimited by ``<!-- TABLE:name -->`` and ``<!-- /TABLE:name -->``.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.chains.profile_cover import parse_enum_output  # noqa: E402

EPS_KEYS = ["eps=0", "eps=1", "eps=1/20*N", "eps=1/10*N", "eps=1/4*N", "eps=1/2*N"]
DELTA_KEYS = ["delta=4", "delta=2", "delta=1", "delta=1/2", "delta=1/4"]


def fmt_int(x: int) -> str:
    return f"{x:,}".replace(",", " ")


def table(n: int):
    p = HERE / "data" / f"dia_Sc12_n{n}.txt"
    return parse_enum_output(p.read_text()) if p.exists() else None


def cover_cell(v: dict) -> str:
    if v["proved_optimal"]:
        return str(v["N_cov"])
    lo = max(v.get("lower_certified", 1), v.get("lower_solver", 1))
    return str(v["N_cov"]) if lo >= v["N_cov"] else f"[{lo}, {v['N_cov']}]"


def net_cell(v: dict) -> str:
    b = v["net_closed_radius"]
    return str(b["upper"]) if b["exact"] else f"[{b['lower']}, {b['upper']}]"


def build() -> dict[str, str]:
    out: dict[str, str] = {}
    res = json.loads((HERE / "results" / "lattice_Sc12.json").read_text())
    rows = {r["n_torsions"]: r for r in res["rows"]}

    # ---- sequence of conformations and classes, n = 13..24 --------------------------------------
    ns = [n for n in range(13, 25) if table(n) is not None]
    tabs = {n: table(n) for n in ns}
    lines = ["| `n` | " + " | ".join(str(n) for n in ns) + " |", "|---|" + "---|" * len(ns),
             "| conformations | " + " | ".join(fmt_int(tabs[n].n_conformations) for n in ns) + " |",
             "| profile classes | " + " | ".join(fmt_int(tabs[n].n_classes) for n in ns) + " |"]
    out["sequence"] = "\n".join(lines)

    # ---- covering numbers -------------------------------------------------------------------------
    lines = ["| `n` | `N` | `L=1`: `ε=0` | `ε=1` | `ε=N/20` | `ε=N/10` | `ε=N/4` | `ε=N/2` | `L=1/5`: `ε=0` | `ε=1` | `ε=N/20` | `ε=N/10` | `ε=N/4` | `ε=N/2` |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for n in sorted(rows):
        if n < 5:
            continue
        c = rows[n]["cover"]
        cells = [cover_cell(c[f"L=1,{k}"]) for k in EPS_KEYS] + [cover_cell(c[f"L=1/5,{k}"]) for k in EPS_KEYS]
        lines.append(f"| {n} | {rows[n]['n_beads']} | " + " | ".join(cells) + " |")
    out["cover"] = "\n".join(lines)
    out["cover_range"] = f"{min(n for n in rows if n >= 5)}…{max(rows)}"

    # ---- finite-size expansion of the profile set ---------------------------------------------------
    sel = [n for n in (8, 12, 16, 18, 20, 22, 24) if table(n) is not None]
    hdr = "| `N` (beads) | " + " | ".join(str(n + 3) for n in sel) + " | bulk lattice |"
    l1, l2, l3 = [], [], []
    for n in sel:
        t = table(n)
        N = t.n_beads
        norms = t.l1_norms()
        i = int(np.argmax(norms))
        l1.append(f"{t.hist.sum(axis=1).max() / N:.2f}")
        l2.append(f"{norms.max() / N:.2f}")
        l3.append(f"{int(t.gmin[i])}/{n}")
    out["finite_size"] = "\n".join([
        hdr, "|---|" + "---|" * (len(sel) + 1),
        "| largest number of pairs inside the cutoff, per bead | " + " | ".join(l1) + " | 12 |",
        "| largest `‖N^x‖₁`, per bead | " + " | ".join(l2) + " | 35 |",
        "| fewest gauche torsions in that extreme class, of `n` | " + " | ".join(l3) + " | — |"])

    # ---- entropy -------------------------------------------------------------------------------------
    lines = ["| `n` | `δ = 4` | `δ = 2` | `δ = 1` | `δ = ½` | `δ = ¼` | traversal `m(δ)` at the same five radii |", "|---|---|---|---|---|---|---|"]
    for n in sorted(rows):
        if n not in (8, 10, 12, 13, 14, 16, 18, 20, 22, 24):
            continue
        e = rows[n]["entropy"]
        if "net_closed_radius" not in e[DELTA_KEYS[0]]:
            continue
        lines.append(f"| {n} | " + " | ".join(net_cell(e[k]) for k in DELTA_KEYS)
                     + " | " + ", ".join(str(e[k]["m_fpt"]) for k in DELTA_KEYS) + " |")
    out["entropy"] = "\n".join(lines)

    # ---- single-flip constants -----------------------------------------------------------------------
    fp = HERE / "results" / "lattice_Sc12_flip.json"
    if fp.exists():
        flip = json.loads(fp.read_text())["rows"]
        lines = ["| `n` | `c^{sf}` (first half; symmetric under chain reversal) | `min_j c_j / d_j` | sets `T` with budget below `D_max` | pairs enumerated | violations | worst excess |",
                 "|---|---|---|---|---|---|---|"]
        for r in flip:
            n = r["n_torsions"]
            if n < 8:
                continue
            c = r["c_sf"]
            half = c[: (n + 1) // 2]
            assert r["symmetric"]
            ratio = min(c[j] / min(j + 1, n - j) for j in range(n))      # d_j = distance from the nearer end, 1-based
            lines.append(f"| {n} | {', '.join(map(str, half))} | {ratio:.1f} | {r['sets_with_budget_below_Dmax']} | "
                         f"{fmt_int(r['pairs_checked'])} | {r['pairs_violating']} | {r['worst_excess'] if r['pairs_checked'] else '—'} |")
        out["flip"] = "\n".join(lines)
        out["flip_range"] = f"{flip[0]['n_torsions']}…{flip[-1]['n_torsions']}"
        out["flip_all_valid"] = str(all(r["valid_hamming_envelope"] for r in flip))
    return out


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
        pat = re.compile(rf"(<!-- TABLE:{re.escape(name)} -->\n).*?(\n<!-- /TABLE:{re.escape(name)} -->)", re.S)
        new = pat.sub(lambda m: m.group(1) + body + m.group(2), new)
    if args.verify:
        print("tables in", target.name, "match the artifacts" if new == text else "DIFFER from the artifacts")
        return 0 if new == text else 1
    target.write_text(new)
    print("updated", target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
