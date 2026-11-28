#!/usr/bin/env python3
"""Markdown table of the Q1 results (from out/q1_main.txt and out/q1_main_noparity.txt) -> out/q1_table.md."""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def parse(fn):
    rows = {}
    for l in (HERE / "out" / fn).read_text().splitlines():
        if not l.startswith("u="):
            continue
        g = lambda k: re.search(k + r"=\s*([-+\d.inf]+)", l).group(1)
        key = (g("u"), re.search(r"ns=(\([\d, ]+\))", l).group(1), re.search(r"roles=(\w+)", l).group(1), g("th/h"))
        theirs = re.search(r"theirs viol=\s*([-+\d.]+)", l)
        rows[key] = dict(V=float(g(" V")), allow=float(g("allow")), Vhid=float(g("Vhid")),
                         theirs=float(theirs.group(1)) if theirs else None, hypNu=g("hypNu") if False else re.search(r"hypNu=(\w)", l).group(1))
    return rows


par = parse("q1_main.txt")
nop = parse("q1_main_noparity.txt")
out = ["| u | blocks | roles | Θ/(nh) | V (parities, report reading) | V (no parities) | allowance m(u+5L) | theirs (stored `viol`) | V(par) − theirs | V(nopar) − theirs | hidden bracket (par) | n_j ≥ N_u |",
       "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for key, r in par.items():
    s = nop[key]
    th = f"{r['theirs']:+.3f}" if r["theirs"] is not None else "—"
    d1 = f"{r['V'] - r['theirs']:+.4f}" if r["theirs"] is not None else "—"
    d2 = f"{s['V'] - r['theirs']:+.4f}" if r["theirs"] is not None else "—"
    hid = f"{r['Vhid']:+.4f}" if r["Vhid"] > -1e300 else "none"
    out.append(f"| {key[0]} | {key[1]} | {key[2]} | {key[3]} | {r['V']:+.4f} | {s['V']:+.4f} | {r['allow']:.2f} | {th} | {d1} | {d2} | {hid} | {r['hypNu']} |")
(HERE / "out" / "q1_table.md").write_text("\n".join(out) + "\n")
print(len(out) - 2, "rows")
