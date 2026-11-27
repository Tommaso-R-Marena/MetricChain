"""R28 — READ-ONLY check of every number of the tables of items 100 (addendum) and of SCI-REV-0025 §3, and of the
numbers quoted in their texts, against the twelve committed logs of continuous_cells_real.py.

My own parser of the logs (the committed table generator is not used).  For the two cases I re-ran, the logs
are identical to the committed ones (diff), so this check covers them at re-run level and the other ten at
read-only level.
"""
import r28_common as rc
rc.cap()
import re
import sys
import time

t0 = time.time()
print("R28 check_tables.py  start", rc.utc())
PI = "/home/user/MetricChain/experiments/science/pi_inference/"
ADD = "/home/user/MetricChain/docs/science/INFERENCE_LIMITS_ADDENDA.md"
REV = "/home/user/MetricChain/docs/collaboration/messages/science/SCI-REV-0025.md"
CASES = [("VV", "H", 144), ("VV", "E", 144), ("VAV", "H", 144), ("VAV", "E", 144), ("VAAV", "H", 144), ("VAAAV", "H", 144),
         ("VVV", "H", 72), ("VVV", "E", 72), ("S", "H", 144), ("S", "E", 144), ("L", "H", 144), ("L", "E", 144)]
NAME = {"H": "helix", "E": "strand"}

logs = {}
for seq, bb, nf in CASES:
    t = open(PI + f"continuous_cells_real_{seq}_{bb}_{nf}.log").read()
    lines = t.rstrip().split("\n")
    d = {"complete": lines[-1].startswith("ALL DONE"), "computed": "computed in" in lines[0]}
    d["n"] = int(re.search(r"(\d+) side-chain torsions", t).group(1))
    d["nconf"] = int(re.search(r"deg\), (\d+) conformations", t).group(1))
    m = re.search(r"\(a\) ln Z .*?: ([-\d.]+); with every second grid point: ([-\d.]+) \(difference ([-+\d.e]+)\)", t)
    d["lnZ"], d["quad"] = float(m.group(1)), float(m.group(3))
    m = re.search(r"three-rotamer model.*?minus the grid: ([-+\d.]+) nats = ([-+\d.]+) per torsion", t)
    d["rot_tot"], d["rot"] = float(m.group(1)), float(m.group(2))
    m = re.search(r"minimised-rotamer model.*?minus the grid: ([-+\d.]+) nats = ([-+\d.]+) per torsion", t)
    d["min_tot"], d["min"] = float(m.group(1)), float(m.group(2))
    m = re.search(r"largest difference ([\d.]+), total variation ([\d.]+); grid against minimised rotamers: largest ([\d.]+), total variation ([\d.]+)", t)
    d["tv_r"], d["tv_m"] = float(m.group(2)), float(m.group(4))
    m = re.search(r"minimum-energy state: rigid rotamers — cell \(([\d, ]+)\) \(gap to the next rotamer state ([\d.]+) kT\); continuous energy — cell \(([\d, ]+)\)"
                  r" \(at torsions ([\d., ]+) deg\); the same cell: (True|False)(?:; the continuous minimum of the rigid model's cell lies ([\d.]+) kT)?", t)
    d["rot_cell"], d["gap"], d["cont_cell"], d["cont_at"], d["same"], d["above"] = m.group(1), float(m.group(2)), m.group(3), m.group(4), m.group(5) == "True", m.group(6)
    d["cells"] = [(mm.group(1), float(mm.group(2)), float(mm.group(3)), float(mm.group(4)), float(mm.group(5)), float(mm.group(6)))
                  for mm in re.finditer(r"^\s+\(([\d, ]+)\):\s+([\d.]+) / ([\d.]+) / ([\d.]+);\s+([\d.]+);\s+([-\d.]+)\s*$", t, flags=re.M)]
    tc = t[t.index("(c) brackets"):t.index("(d) tilted")]
    d["c"] = {}
    for mm in re.finditer(r"^\s+(\d+)\s+[\d.]+\s+\[.*?\]\s+[\d.e+-]+\s+[-\d.]+\s+[-\d.e+]+\s+\(\s*[\d.e+-]+\)\s+[-\d.]+\s+[\d.e+-]+\s+(?:all H|all M|[\d.]+)\s+\|\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)", tc, flags=re.M):
        d["c"][int(mm.group(1))] = (float(mm.group(2)), float(mm.group(3)), float(mm.group(4)))     # per torsion: first-order, all-H, best
    td = t[t.index("(d) tilted"):]
    m = re.search(r"remainder V over the grid: ([-\d.e+]+) \.\. ([-\d.e+]+) kT", td)
    d["rem"] = (float(m.group(1)), float(m.group(2)))
    d["d"] = {}
    for mm in re.finditer(r"^\s+(\d+)\s+[\d.]+\s+[-\d.]+\s+[\d.e+-]+\s+([\d.e+-]+)\s+[-\d.]+\s+[\d.e+-]+\s+([\d.e+-]+)\s+(?:all H|all M|[\d.]+)\s*$", td, flags=re.M):
        d["d"][int(mm.group(1))] = (float(mm.group(2)), float(mm.group(3)))                        # per torsion: Jensen gap, upper gap
    m = re.search(r"best certified bracket per torsion: (.*)", t)
    d["summ"] = dict((int(a), float(b)) for a, b in re.findall(r"k=(\d+): ([0-9.e+-]+)", m.group(1)))
    m = re.search(r"controls: the Jensen value as an upper end is violated in (\d+) of (\d+) partitions", t)
    d["ctrl"] = (int(m.group(1)), int(m.group(2)))
    logs[(seq, bb)] = d
print(f"logs parsed: {len(logs)}; all reached 'ALL DONE': {all(d['complete'] for d in logs.values())}; all computed their energies (no cache): {all(d['computed'] for d in logs.values())}")
print(f"controls in the logs: Jensen-as-upper violated in {sum(d['ctrl'][0] for d in logs.values())} of {sum(d['ctrl'][1] for d in logs.values())} partitions")


def g(x):
    return f"{x:.3g}" if x < 1000 else f"{x:.2e}"


def row1(seq, bb, nf):
    d = logs[(seq, bb)]
    return [f"Ace-{seq}-NMe, {NAME[bb]} ({360/nf:g}°)", f"{d['rot']:+.3f}", f"{d['min']:+.3f}", f"{d['tv_r']:.4f}", f"{d['tv_m']:.4f}", "yes" if d["same"] else "**no**"]


def row2(seq, bb, nf):
    d = logs[(seq, bb)]
    br = d["summ"]
    vlo = g(d["rem"][0]) if d["rem"][0] > -1000 else f"{d['rem'][0]:.2e}"
    return [f"Ace-{seq}-NMe, {NAME[bb]}", g(br[3]), g(br[12]), g(br[72]), g(br[144]) if 144 in br else "—", f"{vlo} to {g(d['rem'][1])}",
            f"{d['d'][3][0]:.1e}", g(d["d"][3][1]), g(d["d"][12][1])]


def md_rows(path, first_cell_prefix="| Ace-"):
    out = []
    for ln in open(path):
        if ln.startswith(first_cell_prefix):
            out.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return out


add_rows = md_rows(ADD)
rev_rows = md_rows(REV)
t1_add = [r for r in add_rows if len(r) == 6]
t2_add = [r for r in add_rows if len(r) == 9]
t1_rev = [r for r in rev_rows if len(r) == 6]
print(f"markdown rows found: addendum table 1: {len(t1_add)}, table 2: {len(t2_add)}; SCI-REV-0025 table: {len(t1_rev)}")
ncell = nbad = 0
for label, rows, fn in (("addendum table 1", t1_add, row1), ("SCI-REV-0025 §3 table", t1_rev, row1), ("addendum table 2", t2_add, row2)):
    bad_here = []
    for (seq, bb, nf), r in zip(CASES, rows):
        mine = fn(seq, bb, nf)
        for a, b in zip(mine, r):
            ncell += 1
            if a != b:
                nbad += 1
                bad_here.append((seq, bb, a, b))
    print(f"   {label}: {len(rows)} rows; cells differing from what the logs give: {len(bad_here)} {bad_here}")
print(f"TABLE CHECK: {ncell} cells compared; {nbad} differ")
# does the double rounding (log 4 decimals -> table 3 decimals) change any digit?  flag entries whose 4th decimal is 5
flag = [(k, d["rot"], d["min"]) for k, d in logs.items() if f"{d['rot']:.4f}"[-1] == "5" or f"{d['min']:.4f}"[-1] == "5"]
print(f"   entries whose logged 4th decimal is a 5 (rounding to 3 decimals rests on unseen digits): {flag}")

print("\nNUMBERS QUOTED IN THE TEXTS, recomputed from the logs")
L = logs
val = [k for k in L if set(k[0]) <= set("VA")]
two_val = [k for k in val if k[0] != "VVV"]
print(f" protocol: conformations {sorted(set(d['nconf'] for d in L.values()))} (text: 20 736 and 373 248)")
print(f" protocol: |change of ln Z when every second point is dropped|: 2.5-deg grids max {max(abs(L[k]['quad']) for k in L if k[0] != 'VVV'):.2e} (text: at most 6e-4);"
      f" 5-deg grids max {max(abs(L[k]['quad']) for k in L if k[0] == 'VVV'):.2e} (text: 1.2e-3)")
print(f" 100(i): rigid offsets per torsion over all cases: {min(d['rot'] for d in L.values()):+.3f} .. {max(d['rot'] for d in L.values()):+.3f}"
      f" (texts: 'one to three nats per torsion'; '-3.2 to +2.0'); smallest |offset| {min(abs(d['rot']) for d in L.values()):.3f}")
print(f" 100(i): VV helix minus VV strand, rigid: {L[('VV','H')]['rot'] - L[('VV','E')]['rot']:+.4f} (text 0.143);"
      f" VV H {L[('VV','H')]['rot']:+.4f} and VAAV H {L[('VAAV','H')]['rot']:+.4f} (text +2.001, -3.177)")
d = L[("VAAV", "H")]
print(f" 100(i): VAAV helix: continuous minimum at torsions {d['cont_at']} deg; cell {d['cont_cell']}: " +
      "; ".join(f"cell ({c[0]}) E_rot - E_min = {c[4]:.3f} kT" for c in d["cells"][:2]) + "  (text: minimum at 167.5 deg, ideal rotamer 10.9 kT up, both torsions together)")
print(f" 100(i): cell-minimised offsets, valine: {min(L[k]['min'] for k in val):+.3f} .. {max(L[k]['min'] for k in val):+.3f} (text +1.89 to +2.28);"
      f" all cases: {min(d['min'] for d in L.values()):+.3f} .. {max(d['min'] for d in L.values()):+.3f} (SCI-REV-0025: 'about 2 nats per torsion')")
print(f" 100(i): VVV helix rigid {L[('VVV','H')]['rot']:+.4f}, minimised {L[('VVV','H')]['min']:+.4f}; continuous minimum at {L[('VVV','H')]['cont_at']} (text: falls on the ideal rotamers)")
d = L[("L", "H")]
cells = {c[0]: c for c in d["cells"]}
print(f" 100(ii): L helix: cell (2, 1): grid {cells['2, 1'][1]}, rigid {cells['2, 1'][2]}; cell (1, 0): grid {cells['1, 0'][1]}, rigid {cells['1, 0'][2]} (text 0.55, 0.35; 0.17, 0.83);"
      f" TV {d['tv_r']} (0.48); gap {d['gap']} (1.56); minimum at {d['cont_at']} (287.5, 157.5); {d['above']} kT (0.56);"
      f" strains {cells['2, 1'][4]} and {cells['1, 0'][4]} (5.9, 3.8)")
print(f" 100(ii): cells with 4-6 % of the weight and a clashing ideal rotamer: " + "; ".join(f"({c[0]}): population {c[1]}, E_rot - E_min {c[4]}" for c in d["cells"] if 0.03 < c[1] < 0.07))
print(f" 100(ii): TV rigid: L strand {L[('L','E')]['tv_r']} (0.27); S helix {L[('S','H')]['tv_r']}, S strand {L[('S','E')]['tv_r']} (0.06, 0.15); valine max {max(L[k]['tv_r'] for k in val)} (0.012)")
print(f" 100(ii): TV minimised, largest over all cases: {max(d['tv_m'] for d in L.values())} (text: within 0.08)")
print(f" 100(iii): uniform-reference bracket per torsion at k = 3: valine {min(L[k]['summ'][3] for k in val):.3g} .. {max(L[k]['summ'][3] for k in val):.3g} (text 8 to 57);"
      f" leucine {L[('L','H')]['summ'][3]:.3g}, {L[('L','E')]['summ'][3]:.3g} (thousands)")
print(f" 100(iii): at 5-deg cells (k = 72): valine {min(L[k]['summ'][72] for k in val):.3g} .. {max(L[k]['summ'][72] for k in val):.3g} (text 0.07 to 0.2);"
      f" all cases {min(d['summ'][72] for d in L.values()):.3g} .. {max(d['summ'][72] for d in L.values()):.3g}")
v144 = [L[k]['summ'][144] for k in val if 144 in L[k]['summ']]
a144 = [d['summ'][144] for d in L.values() if 144 in d['summ']]
print(f" 100(iii): at 2.5-deg cells (k = 144): valine {min(v144):.3g} .. {max(v144):.3g} (text 0.016 to 0.046); all cases {min(a144):.3g} .. {max(a144):.3g}")
print(f" 100(iii): 'the toy chain was kinder by a factor of about twenty at fine cells': toy 0.00105 per angle at 144 cells -> ratios valine {min(v144)/0.00105:.1f} .. {max(v144)/0.00105:.1f}; all cases {min(a144)/0.00105:.1f} .. {max(a144)/0.00105:.1f}")
print(f" 100(iv): remainder ranges, two-valine blocks: " + "; ".join(f"{k[0]} {k[1]} [{L[k]['rem'][0]:.3g}, {L[k]['rem'][1]:.3g}]" for k in two_val)
      + f"; within +-0.5 in {sum(1 for k in two_val if max(abs(L[k]['rem'][0]), abs(L[k]['rem'][1])) <= 0.5)} of {len(two_val)} (text: five of six)")
print(f" 100(iv): tilted Jensen gap per torsion at k = 3, two-valine blocks: max {max(L[k]['d'][3][0] for k in two_val):.2e} (text: at most 1.2e-5);"
      f" upper gap at k = 3: {min(L[k]['d'][3][1] for k in two_val):.2e} .. {max(L[k]['d'][3][1] for k in two_val):.2e} (4e-4 to 2e-2); at k = 12: max {max(L[k]['d'][12][1] for k in two_val):.2e} (9e-4)")
print(f" 100(iv): VVV: remainder H [{L[('VVV','H')]['rem'][0]:.3g}, {L[('VVV','H')]['rem'][1]:.3g}], E [{L[('VVV','E')]['rem'][0]:.3g}, {L[('VVV','E')]['rem'][1]:.3g}];"
      f" upper gap k = 3: {L[('VVV','H')]['d'][3][1]:.3g}, {L[('VVV','E')]['d'][3][1]:.3g} (0.036, 0.0086); k = 12: {L[('VVV','H')]['d'][12][1]:.2g}, {L[('VVV','E')]['d'][12][1]:.2g} (5e-5, 3e-4)")
print(f" 100(iv)/101(b)/SCI-REV-0025 point 4: upper gap at k = 3 over all eight valine blocks: {min(L[k]['d'][3][1] for k in val):.2e} .. {max(L[k]['d'][3][1] for k in val):.2e} (texts: 4e-4 to 4e-2)")
print(f" 100(v): remainder, serine: H [{L[('S','H')]['rem'][0]:.3g}, {L[('S','H')]['rem'][1]:.3g}], E [{L[('S','E')]['rem'][0]:.3g}, {L[('S','E')]['rem'][1]:.3g}] (text: +-9 kT);"
      f" leucine H up to {L[('L','H')]['rem'][1]:.3g}, E up to {L[('L','E')]['rem'][1]:.3g}")
print(f" 100(vi): rigid offset 'between 0.5 and 2 nats per residue — missed at the upper end by 0.0006 on the helix': VV H {L[('VV','H')]['rot']:+.4f};"
      f" 'the bracket is wider than 2, 0.5, 0.05 at 3, 12, 72 cells': smallest over valine: {min(L[k]['summ'][3] for k in val):.3g}, {min(L[k]['summ'][12] for k in val):.3g}, {min(L[k]['summ'][72] for k in val):.3g};"
      f" over ALL cases: {min(d['summ'][3] for d in L.values()):.3g}, {min(d['summ'][12] for d in L.values()):.3g}, {min(d['summ'][72] for d in L.values()):.3g}")
print(f" SCI-REV-0025 point 2: TV leucine {L[('L','H')]['tv_r']}, {L[('L','E')]['tv_r']} (0.48, 0.27); serine {L[('S','H')]['tv_r']}, {L[('S','E')]['tv_r']} (0.06, 0.15); valine max {max(L[k]['tv_r'] for k in val)} (0.012)")
print(f" same-cell column: 'no' only for {[k for k in L if not L[k]['same']]}")
print(f" valine: population of the dominant cell in the grid model, per case: " + ", ".join(f"{k[0]} {k[1]}: {max(c[1] for c in L[k]['cells']):.4f}" for k in val))
rc.finish(t0)
