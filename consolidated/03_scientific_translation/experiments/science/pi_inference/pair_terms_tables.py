#!/usr/bin/env python3
"""The tables of SCI-RES-0035, SCI-MSG-0033 and addendum part (24), generated from the committed logs of
pair_term_mixing.py (the theory division's inequality on our routing), held_pair_terms.py (what pair terms of held sites
would give, from the states) and held_pair_exact.py (the certified computation) -- no number of those tables typed by hand,
except the column of workstream R24's values, which is copied from its report (docs/science/workstreams/R24_REPORT.md,
finding M1) and compared here with ours.
Run: python3 -B pair_terms_tables.py > pair_terms_tables.log
"""
import os, re
D = os.path.dirname(os.path.abspath(__file__))
CASES = [("K5_m4_w2_enum", "Lys₅, order 4, band 2"), ("K5_m4_w3_enum", "Lys₅, order 4, band 3"), ("K5_m5_w3_enum", "Lys₅, order 5, band 3"), ("LKSEc5_m4_w2_enum", "LKSE:5, order 4, band 2"),
         ("K12_m4_w4", "Lys₁₂, order 4, band 4"), ("K12_m4_w7", "Lys₁₂, order 4, band 7")]
R24_UP = {"K5_m4_w2_enum": "0.415", "K5_m4_w3_enum": "0.196", "K5_m5_w3_enum": "0.538", "LKSEc5_m4_w2_enum": "0.470", "K12_m4_w4": "0.498 ± 0.002"}       # R24, M1: upper end, pair laws under the floor
R24_BOTH = {"K5_m4_w2_enum": "0.440", "K5_m4_w3_enum": "0.224", "K5_m5_w3_enum": "0.779", "LKSEc5_m4_w2_enum": "0.471", "K12_m4_w4": "0.664 ± 0.002"}   # R24, M1: pair terms on both sides, with the floor


def read(name):
    p = os.path.join(D, name)
    if not os.path.exists(p): return None
    t = open(p).read(); assert t.rstrip().split("\n")[-1].startswith("ALL DONE"), name
    return t


def table1():
    rows = ["| case | pairs of groups | share of the exact pair term in pairs whose windows overlap (the inequality gives 0) | … disjoint, one common held site | … disjoint, two held sites | conditional product given the held sites / exact, disjoint pairs | the inequality with the true `ψ` / exact, disjoint pairs | **the inequality with the best possible `ψ` recovers, of the whole pair term** |", "|" + "---|" * 8]
    for c, name in CASES:
        t = read(f"pair_term_mixing_{c}.log")
        if t is None: continue
        npairs = int(re.search(r"over (\d+) pairs", t).group(1)); sh = {}; cond = {}; bnd = {}
        for key, pat in (("ov", r"\| windows overlap[^|]*\| (\d+) \| \*\*([0-9.]+)\*\* \|"), ("one", r"\| disjoint windows, one common held site \| (\d+) \| \*\*([0-9.]+)\*\* \| ([^|]*)\| ([^|]*)\| ([^|]*)\|"),
                         ("two", r"\| disjoint windows, two held sites \| (\d+) \| \*\*([0-9.]+)\*\* \| ([^|]*)\| ([^|]*)\| ([^|]*)\|")):
            m = re.search(pat, t); sh[key] = (int(m.group(1)), m.group(2))
            if key != "ov": cond[key] = m.group(4).strip(); bnd[key] = m.group(5).strip().strip("*")
        m = re.search(r"recovers ([0-9.]+) of the exact pair term", t); enum = "enum" in c
        dis_c = ", ".join(v for v in (cond["one"], cond["two"]) if v not in ("—", "")) or "—"; dis_b = ", ".join(v for v in (bnd["one"], bnd["two"]) if v not in ("—", "")) or "—"
        rows.append(f"| {name} | {npairs} | {sh['ov'][1]} ({sh['ov'][0]} pairs) | {sh['one'][1]} ({sh['one'][0]}) | {sh['two'][1]} ({sh['two'][0]}) | {dis_c if enum else 'not computable from samples'} | {dis_b if enum else 'not computable from samples'} | "
                    f"{('**' + m.group(1) + '**') if m else 'at most ' + f'{1 - float(sh[chr(111) + chr(118)][1]):.3f}' + ' (the share of the disjoint pairs)'} |")
    return "\n".join(rows)


def exact(c):
    t = read(f"held_pair_exact_{c}.log")
    if t is None: return None
    d = {}
    m = re.search(r"the driver's corrected bracket \[([0-9.]+), ([0-9.]+)\], width ([0-9.e-]+)", t); d["old"] = (m.group(1), m.group(2), m.group(3))
    m = re.search(r"\(5\) certified bracket with pair terms of held sites under the ceiling: \[([0-9.]+), ([0-9.]+)\], width ([0-9.e-]+), against .*?: narrowed by ([0-9.]+) of the width \(lower end \+([0-9.]+), upper end -([0-9.]+)\)", t)
    d["ceil"] = (m.group(4), m.group(5), m.group(6))
    m = re.search(r"\(6\) the floor side, (\d+) passes with one held site and (\d+) with two \((\d+) s\)", t); d["fl_passes"] = (int(m.group(1)), int(m.group(2)), m.group(3)) if m else None
    m = re.search(r"upper end from the second sum: ([0-9.]+)\*\*", t); d["fl_up"] = m.group(1) if m else None
    m = re.search(r"\(7\) \*\*certified bracket: \[([0-9.]+), ([0-9.]+)\], width ([0-9.e-]+)\*\* against .*?: narrowed by \*\*([0-9.]+)\*\* of the width \(lower end \+([0-9.]+), upper end -([0-9.]+)\)", t)
    d["new"] = (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6))
    m = re.search(r"; (\d+) s for (\d+) passes with", t); d["passes"] = (int(m.group(2)), m.group(1))
    m = re.search(r"\(4\) exact ln Z = ([0-9.]+); inside the new bracket: (True|False)", t); d["lnZ"] = (m.group(1), m.group(2)) if m else None
    m = re.search(r"computed exactly: (\d+) of them", t); d["quads"] = int(m.group(1))
    return d


def table2():
    rows = ["| case | first-order corrected bracket (width) | quadruples `(h, h′, s, t)`; passes under the ceiling; under the floor | (a), (b): narrowed by | (c): upper end under the floor | **certified bracket (width)** | **narrowed by** (lower end; upper end) | exact `ln Z` |", "|" + "---|" * 8]
    for c, name in CASES:
        d = exact(c)
        if d is None: continue
        fl = f"{d['fl_passes'][0] + d['fl_passes'][1]} ({d['fl_passes'][2]} s)" if d["fl_passes"] else "—"
        rows.append(f"| {name} | [{d['old'][0]}, {d['old'][1]}] ({d['old'][2]}) | {d['quads']}; {d['passes'][0]} ({d['passes'][1]} s); {fl} | {d['ceil'][0]} | {d['fl_up'] or '—'} | **[{d['new'][0]}, {d['new'][1]}] ({d['new'][2]})** | "
                    f"**{d['new'][3]}** (+{d['new'][4]}; −{d['new'][5]}) | {(d['lnZ'][0] + ', inside') if d['lnZ'] and d['lnZ'][1] == 'True' else 'not known'} |")
    return "\n".join(rows)


def table3():
    rows = ["| instance | upper end, pair laws under the floor — the referee (groups; enumeration, samples for Lys₁₂) | — the coordinator (held sites; exact passes) | both ends, floor above and ceiling below — the referee | — the coordinator | certified bracket (width) against the first-order one (width) |", "|" + "---|" * 6]
    for c, name in CASES:
        d = exact(c)
        if d is None or c not in R24_UP: continue
        rows.append(f"| {name} | {R24_UP[c]} | **{d['new'][5]}** | {R24_BOTH[c]} | **{d['new'][3]}** | [{d['new'][0]}, {d['new'][1]}] ({d['new'][2]}) against ({d['old'][2]}) |")
    return "\n".join(rows)


def would():
    out = []
    for c, name in CASES:
        t = read(f"held_pair_terms_{c}.log")
        if t is None: continue
        m = re.search(r"would narrow the corrected bracket by ([0-9.]+) of its width\*\* \(merging per held site alone: ([0-9.]+); the exact joint law of all groups: ([0-9.]+)\)", t)
        m3 = re.search(r"cost: (\d+) computations with one site held and (\d+) with two .*? the largest (\d+) carry 90 % of the lower pair term and (\d+) carry 99 %; upper pair term: (\d+) and (\d+)", t)
        out.append(f"{name}: pair terms of held sites under the ceiling would narrow the bracket by {m.group(1)} (merging per held site alone {m.group(2)}; the exact joint law of the groups {m.group(3)}); "
                   f"{m3.group(1)} held states, {m3.group(2)} pairs of held states; 90 % / 99 % of the lower pair term in the largest {m3.group(3)} / {m3.group(4)} pairs of held states, upper: {m3.group(5)} / {m3.group(6)}")
    return "\n".join(out)


if __name__ == "__main__":
    print("(1) the theory division's pair-term inequality on our routing (pair_term_mixing.py)\n" + table1() + "\n")
    print("(2) certified second-order recovery with two held sites (held_pair_exact.py)\n" + table2() + "\n")
    print("(3) the floor route: workstream R24's values against the coordinator's (fractions of the first-order corrected bracket)\n" + table3() + "\n")
    print("(4) from the states (held_pair_terms.py): what pair terms of held sites under the ceiling would give\n" + would() + "\n")
    print("ALL DONE")
