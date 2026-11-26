#!/usr/bin/env python3
"""Tables of addendum A17 (26) and of SCI-REV-0025, generated from the logs of continuous_cells_real.py (no number is typed).
Run:  python3 -B continuous_cells_real_tables.py > continuous_cells_real_tables.log"""
import re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
CASES = [("VV", "H", 144), ("VV", "E", 144), ("VAV", "H", 144), ("VAV", "E", 144), ("VAAV", "H", 144), ("VAAAV", "H", 144),
         ("VVV", "H", 72), ("VVV", "E", 72), ("S", "H", 144), ("S", "E", 144), ("L", "H", 144), ("L", "E", 144)]
NAME = {"H": "helix", "E": "strand"}
rows = []
for seq, bb, nf in CASES:
    f = os.path.join(HERE, f"continuous_cells_real_{seq}_{bb}_{nf}.log")
    if not os.path.exists(f):
        print(f"(log missing: {os.path.basename(f)})"); continue
    t = open(f).read()
    assert t.rstrip().split("\n")[-1].startswith("ALL DONE"), f
    assert "computed in" in t.split("\n")[0], ("the log must come from a run that computed its energies", f)
    d = dict(seq=seq, bb=bb, nf=nf)
    d["ntor"] = int(re.search(r"(\d+) side-chain torsions", t).group(1))
    d["rot"] = float(re.search(r"three-rotamer model.*?= ([+-][0-9.]+) per torsion", t).group(1))
    d["min"] = float(re.search(r"minimised-rotamer model.*?= ([+-][0-9.]+) per torsion", t).group(1))
    m = re.search(r"grid against rigid rotamers: largest difference ([0-9.]+), total variation ([0-9.]+); grid against minimised rotamers: largest ([0-9.]+), total variation ([0-9.]+)", t)
    d["tv_r"], d["tv_m"] = float(m.group(2)), float(m.group(4))
    d["same"] = re.search(r"the same cell: (True|False)", t).group(1) == "True"
    summ = re.search(r"best certified bracket per torsion: (.*)", t).group(1)
    d["br"] = dict((int(a), float(b)) for a, b in re.findall(r"k=(\d+): ([0-9.e+-]+)", summ))
    m = re.search(r"remainder V over the grid: ([-0-9.e+]+) \.\. ([-0-9.e+]+) kT", t)
    d["vlo"], d["vhi"] = float(m.group(1)), float(m.group(2))
    tt = t[t.index("(d) tilted"):]
    tl = re.findall(r"^\s+(\d+)\s+[0-9.]+\s+[-0-9.]+\s+([0-9.e+-]+)\s+([0-9.e+-]+)\s+[-0-9.]+\s+([0-9.e+-]+)\s+([0-9.e+-]+)\s+\S", tt, flags=re.M)
    d["tilt"] = {int(r[0]): (float(r[2]), float(r[4])) for r in tl}       # per torsion: Jensen gap, upper gap
    m = re.search(r"with every second grid point: [-0-9.]+ \(difference ([-+0-9.e]+)\)", t)
    d["quad"] = float(m.group(1))
    rows.append(d)

def g(x):
    return f"{x:.3g}" if x < 1000 else f"{x:.2e}"

print("TABLE 1 — the rotamer model against the continuous model (per torsion; nats)\n")
print("| block, backbone (grid) | rigid rotamers: `ln Z` minus the grid's | cell-minimised rotamers: the same | populations of rotamer cells, total variation from the grid's: rigid | minimised | minimum-energy state of the rigid table in the cell of the continuous minimum? |")
print("|---|---|---|---|---|---|")
for d in rows:
    print(f"| Ace-{d['seq']}-NMe, {NAME[d['bb']]} ({360/d['nf']:g}°) | {d['rot']:+.3f} | {d['min']:+.3f} | {d['tv_r']:.4f} | {d['tv_m']:.4f} | {'yes' if d['same'] else '**no**'} |")
print("\nTABLE 2 — certified brackets for the continuous `ln Z` from k cells per torsion (width per torsion; nats)\n")
print("| block, backbone | uniform reference, whole energy as one term: k = 3 | 12 | 72 | 144 | range of the remainder after one-site slices [kT] | tilted reference: Jensen end below the grid at k = 3 | certified upper end above the grid at k = 3 | at k = 12 |")
print("|---|---|---|---|---|---|---|---|---|")
for d in rows:
    br = d["br"]; tl = d["tilt"]
    vlo = g(d["vlo"]) if d["vlo"] > -1000 else f"{d['vlo']:.2e}"
    b144 = g(br[144]) if 144 in br else "—"
    print(f"| Ace-{d['seq']}-NMe, {NAME[d['bb']]} | {g(br[3])} | {g(br[12])} | {g(br[72])} | {b144} | {vlo} to {g(d['vhi'])} | {tl[3][0]:.1e} | {g(tl[3][1])} | {g(tl[12][1])} |")
vals = [d for d in rows if set(d["seq"]) <= set("VA")]
print("\nDERIVED (asserted from the rows above)")
r = {(d["seq"], d["bb"]): d for d in rows}
if ("VV", "H") in r and ("VV", "E") in r:
    print(f"valine dipeptide block, helix minus strand: rigid {r[('VV','H')]['rot']-r[('VV','E')]['rot']:+.3f}, minimised {r[('VV','H')]['min']-r[('VV','E')]['min']:+.3f} nats per torsion")
if ("VV", "H") in r and ("VAAV", "H") in r:
    print(f"valine on the helix, neighbours (VV) minus i,i+3 (VAAV): rigid {r[('VV','H')]['rot']-r[('VAAV','H')]['rot']:+.3f}, minimised {r[('VV','H')]['min']-r[('VAAV','H')]['min']:+.3f} nats per torsion")
print(f"valine blocks ({len(vals)} cases): rigid offset {min(d['rot'] for d in vals):+.3f} to {max(d['rot'] for d in vals):+.3f}; minimised offset {min(d['min'] for d in vals):+.3f} to {max(d['min'] for d in vals):+.3f}; "
      f"remainder within [{min(d['vlo'] for d in vals):.3g}, {max(d['vhi'] for d in vals):.3g}] kT; tilted upper end above the grid at k = 3: {min(d['tilt'][3][1] for d in vals):.2e} to {max(d['tilt'][3][1] for d in vals):.2e}; at k = 12: {min(d['tilt'][12][1] for d in vals):.2e} to {max(d['tilt'][12][1] for d in vals):.2e}; Jensen end at k = 3 at most {max(d['tilt'][3][0] for d in vals):.1e} below")
print(f"uniform-reference bracket at k = 3 over valine blocks: {min(d['br'][3] for d in vals):.3g} to {max(d['br'][3] for d in vals):.3g}; at the finest partition: {min(min(v for k, v in d['br'].items() if k == max(d['br'])) for d in vals):.3g} to {max(max(v for k, v in d['br'].items() if k == max(d['br'])) for d in vals):.3g}")
print(f"largest change of ln Z when every second grid point is dropped: {max(abs(d['quad']) for d in rows):.1e}")
print(f"ALL DONE  {len(rows)} of {len(CASES)} cases")
