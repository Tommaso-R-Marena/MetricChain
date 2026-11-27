"""R28 — trying to make the leucine claim of item 100 (ii) go away.

The claim (helix backbone, 2.5 deg grid): the rigid-rotamer table (torsions at 60/180/300) has its
minimum-energy state at (180, 60) with a gap of 1.56 kT, while the minimum of the same energy with
continuous torsions is at (287.5, 157.5) in another 120-degree cell; strains 3.8 and 5.9 kT.

Variations (all on my own grids, my own code):
 V0  the claim itself, for the total energy, the vacuum part alone, the GBn2 part alone;
 V1  shifted cell boundaries;
 V2  wells defined without boundaries: basins of steepest descent on the grid;
 V3  other rotamer positions: (a) uniform offsets d1, d2 of the ideal values; (b) bottoms of the
     one-torsion slices through the global minimum; (c) minima of the one-torsion marginal free
     energies; (d) library-like positions quoted FROM MEMORY (not verified);
 Controls: a table whose rotamers sit at the 2-D cell minima must name the right cell (by
 construction) — printed; the same code on the valine dipeptide must NOT show the effect.
Usage: python3 -B ff_leucine.py GRID.npz [--label TEXT]
"""
import r28_common as rc
rc.cap()
import argparse
import sys
import time
import numpy as np
from scipy.special import logsumexp
import ff_lib as fl

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("grid")
ap.add_argument("--label", default="")
args = ap.parse_args()
print("R28 ff_leucine.py  start", rc.utc(), vars(args))
npz = np.load(args.grid, allow_pickle=True)
N = npz["vac"].shape[0]
step = 360.0 / N
IDEAL = (60.0, 180.0, 300.0)


def describe(E, tag):
    rm = fl.rotamer_models(E)
    a = rm["rot_min_state"]
    print(f"[{tag}] rigid table: minimum-energy state ({IDEAL[a[0]]:g}, {IDEAL[a[1]]:g}) deg, gap to the next state {rm['rot_gap']:.4f} kT;"
          f" continuous minimum at ({rm['cont_min_deg'][0]:g}, {rm['cont_min_deg'][1]:g}) deg, cell {rm['cont_min_cell']};"
          f" same cell: {rm['same_cell']}; TV(grid cells, rigid) = {rm['tv_r']:.4f}, TV(grid cells, cell-minimised) = {rm['tv_m']:.4f}")
    srt = np.argsort(rm["Erot"].ravel())[:4]
    print("      rigid table, four lowest states [kT above the continuous minimum]: "
          + "; ".join(f"({IDEAL[i // 3]:g}, {IDEAL[i % 3]:g}): {rm['Erot'].ravel()[i]:.3f}" for i in srt))
    srt = np.argsort(rm["Emin"].ravel())[:4]
    print("      cell minima, four lowest [kT]: " + "; ".join(f"cell ({i // 3}, {i % 3}): {rm['Emin'].ravel()[i]:.3f}" for i in srt))
    print("      strain of the ideal rotamer above its cell minimum [kT], cells by population: "
          + "; ".join(f"cell ({i // 3}, {i % 3}) pop {rm['Pg'].ravel()[i]:.4f}: {(rm['Erot'] - rm['Emin']).ravel()[i]:.3f}"
                      for i in np.argsort(-rm["Pg"].ravel())[:4]))
    return rm


# ------------------------------------------------------------------ V0
print("\n=== V0  the claim, by energy part", args.label)
E = fl.total_kT(npz, "total")
rm0 = describe(E, "total = vacuum + GBn2")
Ev = fl.total_kT(npz, "vac")
describe(Ev, "vacuum ff14SB alone")
Eg = fl.total_kT(npz, "gb")
describe(Eg, "GBn2 alone (no sterics: not a model, a diagnostic)")
for nm in ("tors", "lj"):
    if nm in npz:
        e = npz[nm] / fl.KT
        r = [int(round(a / step)) for a in IDEAL]
        g = np.unravel_index(E.argmin(), E.shape)
        print(f"      term '{nm}' [kT] at the ideal rotamers (300,180): {e[r[2], r[1]] - e[g]:+.3f}, (180,60): {e[r[1], r[0]] - e[g]:+.3f}"
              f"  (relative to its value at the continuous minimum)")
elec = (npz["nb"] - npz["lj"]) / fl.KT
gb = npz["gbn2"] / fl.KT
r = [int(round(a / step)) for a in IDEAL]
g = np.unravel_index(E.argmin(), E.shape)
print(f"      Coulomb [kT] at (300,180): {elec[r[2], r[1]] - elec[g]:+.3f}, (180,60): {elec[r[1], r[0]] - elec[g]:+.3f};"
      f"  GBn2 at (300,180): {gb[r[2], r[1]] - gb[g]:+.3f}, (180,60): {gb[r[1], r[0]] - gb[g]:+.3f}")

# ------------------------------------------------------------------ V1 shifted boundaries
print("\n=== V1  shifted cell boundaries (cells [s, s+120], [s+120, s+240], [s+240, s+360]); the ideal rotamers stay inside their cells for |s| < 60")
print("   shift   rigid minimum state in the cell of the continuous minimum?   TV(grid, rigid)   TV(grid, cell-minimised)   populations of the cells of (300,180) and (180,60): grid | rigid")
keep = 0
tot = 0
for s in np.arange(-57.5, 57.6, 2.5):
    rm = fl.rotamer_models(E, shift_deg=float(s))
    c_mt = (rm["cell_of_rot"][0][2], rm["cell_of_rot"][1][1])
    c_tp = (rm["cell_of_rot"][0][1], rm["cell_of_rot"][1][0])
    tot += 1
    keep += (not rm["same_cell"])
    if abs(s / 2.5) % 4 < 1e-9 or abs(s) > 54:
        print(f"   {s:+6.1f}   {str(rm['same_cell']):5s}   {rm['tv_r']:.4f}   {rm['tv_m']:.4f}   grid {rm['Pg'][c_mt]:.4f}, {rm['Pg'][c_tp]:.4f} | rigid {rm['Pr'][c_mt]:.4f}, {rm['Pr'][c_tp]:.4f}")
print(f"   the claim (different cells) is KEPT at {keep} of {tot} shifts between -57.5 and +57.5 deg")

# ------------------------------------------------------------------ V2 basins of steepest descent
print("\n=== V2  wells without boundaries: basins of steepest descent on the grid (8 neighbours, periodic)")
ii, jj = np.meshgrid(np.arange(N), np.arange(N), indexing="ij")
best_i, best_j, best_e = ii.copy(), jj.copy(), E.copy()
for di in (-1, 0, 1):
    for dj in (-1, 0, 1):
        if di == 0 and dj == 0:
            continue
        ni, nj = (ii + di) % N, (jj + dj) % N
        e = E[ni, nj]
        lower = e < best_e
        best_i[lower], best_j[lower], best_e[lower] = ni[lower], nj[lower], e[lower]
ptr = best_i * N + best_j
for _ in range(64):
    nxt = ptr[ptr // N, ptr % N]
    if np.array_equal(nxt, ptr):
        break
    ptr = nxt
w = np.exp(-E)
w = w / w.sum()
labels, inv = np.unique(ptr, return_inverse=True)
pop = np.bincount(inv.ravel(), weights=w.ravel())
order = np.argsort(-pop)
print(f"   {len(labels)} basins; the six most populated:")
basin_of = lambda a, b: ptr[int(round(a / step)) % N, int(round(b / step)) % N]
rot_states = [(a, b) for a in IDEAL for b in IDEAL]
for o in order[:6]:
    lab = labels[o]
    mi, mj = lab // N, lab % N
    members = [(a, b) for a, b in rot_states if basin_of(a, b) == lab]
    ms = "; ".join(f"({a:g}, {b:g}) at {E[int(round(a/step)), int(round(b/step))]:.3f} kT" for a, b in members) or "none"
    print(f"     minimum at ({mi*step:g}, {mj*step:g}) deg, {E[mi, mj]:.3f} kT, population {pop[o]:.4f}; ideal rotamers inside: {ms}")
gmin = np.unravel_index(E.argmin(), E.shape)
lab_g = ptr[gmin]
a = rm0["rot_min_state"]
lab_r = basin_of(IDEAL[a[0]], IDEAL[a[1]])
print(f"   basin of the rigid table's minimum-energy state ({IDEAL[a[0]]:g}, {IDEAL[a[1]]:g}): minimum at ({(lab_r//N)*step:g}, {(lab_r%N)*step:g}) deg,"
      f" {E[lab_r//N, lab_r%N]:.3f} kT above the global minimum, population {pop[list(labels).index(lab_r)]:.4f};"
      f" basin of the global minimum: population {pop[list(labels).index(lab_g)]:.4f};  same basin: {lab_r == lab_g}")
# the rigid table's populations summed by basin, against the basin populations
prig = {}
Erot = rm0["Erot"]
pr = np.exp(-(Erot - Erot.min()))
pr /= pr.sum()
for (x, (a_, b_)) in enumerate(rot_states):
    prig[basin_of(a_, b_)] = prig.get(basin_of(a_, b_), 0.0) + pr.ravel()[x]
tv = 0.5 * sum(abs(pop[k] - prig.get(labels[k], 0.0)) for k in range(len(labels)))
print(f"   total variation between basin populations (continuous) and the rigid table's weights summed by basin: {tv:.4f}")

# ------------------------------------------------------------------ V3 other rotamer positions
print("\n=== V3a  uniform offsets of the ideal positions: rotamers at (60+d1, 180+d1, 300+d1) x (60+d2, 180+d2, 300+d2)")
offs = np.arange(-30.0, 30.1, 2.5)
wrong = np.zeros((len(offs), len(offs)), bool)
gapm = np.zeros((len(offs), len(offs)))
tvm = np.zeros((len(offs), len(offs)))
for x, d1 in enumerate(offs):
    for y, d2 in enumerate(offs):
        rm = fl.rotamer_models(E, rot_deg=(tuple(a + d1 for a in IDEAL), tuple(a + d2 for a in IDEAL)))
        wrong[x, y] = not rm["same_cell"]
        gapm[x, y] = rm["rot_gap"]
        tvm[x, y] = rm["tv_r"]
print(f"   the rigid table names a cell other than that of the continuous minimum at {wrong.sum()} of {wrong.size} offsets (d1, d2) in [-30, 30]^2 (step 2.5)")
print("   map (rows d1 = chi_1 offset from -30 to +30; columns d2 from -30 to +30; X = wrong cell, . = right cell):")
for x, d1 in enumerate(offs):
    print(f"   {d1:+6.1f}  " + "".join("X" if wrong[x, y] else "." for y in range(len(offs))))
right = [(abs(d1) + abs(d2), max(abs(d1), abs(d2)), d1, d2) for x, d1 in enumerate(offs) for y, d2 in enumerate(offs) if not wrong[x, y]]
if right:
    r = min(right, key=lambda t: (t[1], t[0]))
    print(f"   smallest offset (in max norm) that removes the claim: d1 = {r[2]:+.1f}, d2 = {r[3]:+.1f} deg")
x0 = list(offs).index(0.0)
print(f"   total variation at (0, 0): {tvm[x0, x0]:.4f}; smallest over the offsets: {tvm.min():.4f} at d1 = {offs[np.unravel_index(tvm.argmin(), tvm.shape)[0]]:+.1f},"
      f" d2 = {offs[np.unravel_index(tvm.argmin(), tvm.shape)[1]]:+.1f}")
# +-5 and +-10 degree neighbourhoods
for rad in (5.0, 10.0, 15.0):
    sel = (np.abs(offs)[:, None] <= rad) & (np.abs(offs)[None, :] <= rad)
    print(f"   within |d1|, |d2| <= {rad:g} deg: wrong cell at {wrong[sel].sum()} of {sel.sum()} offsets")

idx, tw = fl.closed_cells(N, 3)
i0, j0 = np.unravel_index(E.argmin(), E.shape)


def table_at(pos1, pos2, tag):
    rm = fl.rotamer_models(E, rot_deg=(tuple(pos1), tuple(pos2)))
    a = rm["rot_min_state"]
    print(f"   {tag}: positions chi_1 {tuple(float(p) for p in pos1)}, chi_2 {tuple(float(p) for p in pos2)}: minimum-energy state ({pos1[a[0]]:g}, {pos2[a[1]]:g}),"
          f" gap {rm['rot_gap']:.3f} kT; in the cell of the continuous minimum: {rm['same_cell']}; TV(grid cells, table) = {rm['tv_r']:.4f};"
          f" ln Z offset per torsion {(rm['lnZ_rot'] - rm['lnZ']) / 2:+.4f}")
    return rm


print("\n=== V3b  product library at the bottoms of the one-torsion slices through the global minimum")
p1 = [idx[c][np.argmin(E[idx[c], j0])] * step for c in range(3)]
p2 = [idx[c][np.argmin(E[i0, idx[c]])] * step for c in range(3)]
table_at(p1, p2, "slice bottoms")
print("=== V3c  product library at the minima of the one-torsion marginal free energies")
F1 = -logsumexp(-E, axis=1)
F2 = -logsumexp(-E, axis=0)
q1 = [idx[c][np.argmin(F1[idx[c]])] * step for c in range(3)]
q2 = [idx[c][np.argmin(F2[idx[c]])] * step for c in range(3)]
table_at(q1, q2, "marginal minima")
print("=== V3d  library-like positions quoted FROM MEMORY (leucine 'mt' about (-65, 175), 'tp' about (-177, 65); not verified against any source)")
for (a_, b_), nm in (((295.0, 175.0), "mt (295, 175)"), ((182.5, 65.0), "tp (182.5, 65)"), ((185.0, 65.0), "tp (185, 65)"),
                     ((300.0, 180.0), "ideal (300, 180)"), ((180.0, 60.0), "ideal (180, 60)")):
    print(f"      E at {nm}: {E[int(round(a_/step)) % N, int(round(b_/step)) % N]:.3f} kT above the continuous minimum")
print("=== control: a table with one rotamer at each 2-D cell minimum (the 'minimised' model) names the cell of the continuous minimum by construction:",
      rm0["cont_min_cell"] == tuple(int(x) for x in np.unravel_index(rm0["Emin"].argmin(), (3, 3))))
rc.finish(t0)
