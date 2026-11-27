"""R28 — REPLICATION of the reductions of item 100 for one two-torsion block, with my own code
(ff_lib.py) on my own energy grid (ff_grid.py), compared number by number with a log of
continuous_cells_real.py.

Usage: python3 -B ff_reduce.py GRID.npz THEIR.log [--part total|vac|gb]
Controls (each can fail):
  C1  separable energy (sum of the two one-torsion slices): the remainder must vanish and the tilted
      Jensen gap and upper gap must be zero ("zero coupling error"); cell populations must factorise.
  C2  shuffled grid: the agreement with the log must break.
  C3  too-small oscillation (x 0.3) / Jensen as upper end / minima as lower end must be violated.
"""
import r28_common as rc
rc.cap()
import argparse
import re
import sys
import time
import numpy as np
from scipy.special import logsumexp
import ff_lib as fl

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("grid")
ap.add_argument("log")
ap.add_argument("--part", default="total")
args = ap.parse_args()
print("R28 ff_reduce.py  start", rc.utc(), vars(args))
npz = np.load(args.grid, allow_pickle=True)
E = fl.total_kT(npz, args.part)
N = E.shape[0]
n = 2
KS = (3, 6, 12, 18, 24, 36, 48, 72, 144)


def reductions(E, do_search=True):
    """every number of the (a)-(d) blocks of their log, from my code; returns a flat dict name -> value"""
    out = {}
    lz = fl.lnZ_grid(E)
    out["lnZ"] = lz
    out["lnZ_half"] = fl.lnZ_grid(E[::2, ::2])
    rm = fl.rotamer_models(E)
    out["rot_lnZ"] = rm["lnZ_rot"]
    out["rot_off_per_torsion"] = (rm["lnZ_rot"] - lz) / n
    out["min_lnZ"] = rm["lnZ_min"]
    out["min_off_per_torsion"] = (rm["lnZ_min"] - lz) / n
    out["tv_r"], out["tv_m"], out["max_r"], out["max_m"] = rm["tv_r"], rm["tv_m"], rm["max_r"], rm["max_m"]
    out["rot_gap"] = rm["rot_gap"]
    out["rot_min_cell"] = rm["rot_min_cell"]
    out["cont_min_cell"] = rm["cont_min_cell"]
    out["cont_min_deg"] = rm["cont_min_deg"]
    out["same_cell"] = rm["same_cell"]
    out["rigid_cell_min_above_global"] = rm["rigid_cell_min_above_global"]
    for c in range(3):
        for d in range(3):
            out[f"cell{c}{d}"] = (rm["Pg"][c, d], rm["Pr"][c, d], rm["Pm"][c, d], rm["Erot"][c, d] - rm["Emin"][c, d],
                                  rm["width_term"][c, d])
    out["wt_mean"] = float((rm["Pg"] * rm["width_term"]).sum())
    # (c) uniform reference, the whole energy as one term
    viol = 0
    nb = 0
    ctrl = dict(small=0, jens=0, minlow=0, parts=0)
    for k in KS:
        b = fl.Bracket2(E, k)
        sh = 0.0                                     # uniform reference: ln z_i = 0
        lo1, hi1, jl = b.maxima() + sh, b.minima() + sh, b.jensen() + sh
        hH = b.upper(np.ones(k, bool), np.ones(k, bool))
        best, thr, vals = b.best_threshold()
        out[f"c{k}"] = (lo1, hi1, jl, hH, best, thr)
        for v in list(vals.values()) + [hH, hi1]:
            nb += 1
            if not (lz <= v + 1e-9):
                viol += 1
        if not (lo1 <= lz + 1e-9 and jl <= lz + 1e-9 and lo1 <= jl + 1e-9):
            viol += 1
        ctrl["parts"] += 1
        if lz > b.upper(np.ones(k, bool), np.ones(k, bool), scale=0.3):
            ctrl["small"] += 1
        if jl < lz - 1e-12:
            ctrl["jens"] += 1
        if hi1 > lz + 1e-12:
            ctrl["minlow"] += 1
    # (d) tilted reference
    e1, e2, V, lzi, (i0, j0) = fl.tilted_parts(E)
    out["tilt_sum_lz"] = lzi[0] + lzi[1]
    out["tilt_rem"] = (float(V.min()), float(V.max()))
    out["tilt_ln_expV"] = lz - (lzi[0] + lzi[1])
    for k in KS:
        b = fl.Bracket2(V, k, -e1, -e2)
        jt = b.jensen() + lzi[0] + lzi[1]
        best, thr, vals = b.best_threshold()
        best += lzi[0] + lzi[1]
        ex = loc = np.nan
        if do_search:
            if k == 3:
                ex = b.best_exhaustive()[0] + lzi[0] + lzi[1]
            c1, c2 = b.cmax()
            loc = b.best_local(c1 <= thr, c2 <= thr)[0] + lzi[0] + lzi[1]
        out[f"d{k}"] = (jt, lz - jt, best, best - lz, thr, ex - lz, loc - lz)
        for v in vals.values():
            nb += 1
            if not (lz <= v + lzi[0] + lzi[1] + 1e-9):
                viol += 1
        if not (jt <= lz + 1e-9):
            viol += 1
        ctrl["parts"] += 1
        if lz > b.upper(np.ones(k, bool), np.ones(k, bool), scale=0.3) + lzi[0] + lzi[1]:
            ctrl["small"] += 1
        if jt < lz - 1e-12:
            ctrl["jens"] += 1
        if b.minima() + lzi[0] + lzi[1] > lz + 1e-12:
            ctrl["minlow"] += 1
    out["_viol"] = viol
    out["_nb"] = nb
    out["_ctrl"] = ctrl
    return out


# ------------------------------------------------------------------ their log
def parse_log(path):
    t = open(path).read()
    assert t.rstrip().split("\n")[-1].startswith("ALL DONE"), "log did not reach its last line"
    L = {}
    m = re.search(r"\(a\) ln Z of the grid model .*?: ([-\d.]+); with every second grid point: ([-\d.]+) ", t)
    L["lnZ"], L["lnZ_half"] = (m.group(1), 5e-7), (m.group(2), 5e-7)
    m = re.search(r"three-rotamer model .*?: ln Z = ([-\d.]+); minus the grid: ([-+\d.]+) nats = ([-+\d.]+) per torsion", t)
    L["rot_lnZ"], L["rot_off_per_torsion"] = (m.group(1), 5e-5), (m.group(3), 5e-5)
    m = re.search(r"minimised-rotamer model .*?: ln Z = ([-\d.]+); minus the grid: ([-+\d.]+) nats = ([-+\d.]+) per torsion", t)
    L["min_lnZ"], L["min_off_per_torsion"] = (m.group(1), 5e-5), (m.group(3), 5e-5)
    m = re.search(r"largest difference ([\d.]+), total variation ([\d.]+); grid against minimised rotamers: largest ([\d.]+), total variation ([\d.]+)", t)
    L["max_r"], L["tv_r"], L["max_m"], L["tv_m"] = (m.group(1), 5e-5), (m.group(2), 5e-5), (m.group(3), 5e-5), (m.group(4), 5e-5)
    m = re.search(r"minimum-energy state: rigid rotamers — cell \((\d), (\d)\) \(gap to the next rotamer state ([\d.]+) kT\); continuous energy — cell \((\d), (\d)\)"
                  r" \(at torsions ([\d.]+), ([\d.]+) deg\); the same cell: (True|False)(?:; the continuous minimum of the rigid model's cell lies ([\d.]+) kT)?", t)
    L["rot_min_cell"] = (int(m.group(1)), int(m.group(2)))
    L["rot_gap"] = (m.group(3), 5e-4)
    L["cont_min_cell"] = (int(m.group(4)), int(m.group(5)))
    L["cont_min_deg"] = (float(m.group(6)), float(m.group(7)))
    L["same_cell"] = m.group(8) == "True"
    if m.group(9):
        L["rigid_cell_min_above_global"] = (m.group(9), 5e-4)
    for m in re.finditer(r"^\s+\((\d), (\d)\):\s+([\d.]+) / ([\d.]+) / ([\d.]+);\s+([\d.]+);\s+([-\d.]+)\s*$", t, flags=re.M):
        L[f"cell{m.group(1)}{m.group(2)}"] = [(m.group(3), 5e-5), (m.group(4), 5e-5), (m.group(5), 5e-5), (m.group(6), 5e-4), (m.group(7), 5e-4)]
    m = re.search(r"population-weighted width term: ([\d.]+) nats", t)
    L["wt_mean"] = (m.group(1), 5e-5)
    tc = t[t.index("(c) brackets"):t.index("(d) tilted")]
    for m in re.finditer(r"^\s+(\d+)\s+[\d.]+\s+\[\s*([-\d.]+),\s*([-\d.]+)\]\s+[\d.e+-]+\s+([-\d.]+)\s+([-\d.e+]+)\s+\(\s*[\d.e+-]+\)\s+([-\d.]+)\s+[\d.e+-]+\s+(all H|all M|[\d.]+)", tc, flags=re.M):
        L[f"c{int(m.group(1))}"] = [(m.group(2), 5e-5), (m.group(3), 5e-5), (m.group(4), 5e-5), (m.group(5), None), (m.group(6), 5e-5), m.group(7)]
    td = t[t.index("(d) tilted"):]
    m = re.search(r"sum of the one-site ln z_i = ([-\d.]+); ln <exp\(-V\)> = ([-+\d.]+); remainder V over the grid: ([-\d.e+]+) \.\. ([-\d.e+]+) kT", td)
    L["tilt_sum_lz"] = (m.group(1), 5e-5)
    L["tilt_ln_expV"] = (m.group(2), 5e-5)
    L["tilt_rem"] = (m.group(3), m.group(4))
    for m in re.finditer(r"^\s+(\d+)\s+[\d.]+\s+([-\d.]+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([-\d.]+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+(all H|all M|[\d.]+)\s*$", td, flags=re.M):
        L[f"d{int(m.group(1))}"] = [(m.group(2), 5e-5), (m.group(3), "sig4"), (m.group(5), 5e-5), (m.group(6), "sig4"), m.group(8)]
    return L


def thr_str(thr):
    return "all H" if thr == np.inf else ("all M" if thr == -1.0 else f"{thr:g}")


def close(mine, tok, tol):
    """does my value agree with their printed token?  tol: absolute half-unit, 'sig4' (4 significant digits), or None (6 sig.)"""
    v = float(tok)
    if tol == "sig4":
        return abs(mine - v) <= 6e-4 * abs(v) + 1e-12
    if tol is None:
        return abs(mine - v) <= 6e-6 * abs(v)
    return abs(mine - v) <= tol * 1.02 + 1e-12


def compare(mine, L, verbose=True):
    n_items = n_bad = 0
    bad = []

    def chk(name, ok):
        nonlocal n_items, n_bad
        n_items += 1
        if not ok:
            n_bad += 1
            bad.append(name)
    for key in ("lnZ", "lnZ_half", "rot_lnZ", "rot_off_per_torsion", "min_lnZ", "min_off_per_torsion", "max_r", "tv_r", "max_m", "tv_m",
                "rot_gap", "wt_mean", "tilt_sum_lz", "tilt_ln_expV"):
        chk(key, close(mine[key], *L[key]))
    if "rigid_cell_min_above_global" in L:
        chk("rigid_cell_min_above_global", close(mine["rigid_cell_min_above_global"], *L["rigid_cell_min_above_global"]))
    chk("rot_min_cell", tuple(mine["rot_min_cell"]) == L["rot_min_cell"])
    chk("cont_min_cell", tuple(mine["cont_min_cell"]) == L["cont_min_cell"])
    chk("cont_min_deg", tuple(mine["cont_min_deg"]) == L["cont_min_deg"])
    chk("same_cell", mine["same_cell"] == L["same_cell"])
    for c in range(3):
        for d in range(3):
            for j in range(5):
                chk(f"cell{c}{d}[{j}]", close(mine[f"cell{c}{d}"][j], *L[f"cell{c}{d}"][j]))
    chk("tilt_rem_lo", close(mine["tilt_rem"][0], L["tilt_rem"][0], "sig4"))
    chk("tilt_rem_hi", close(mine["tilt_rem"][1], L["tilt_rem"][1], "sig4"))
    for k in KS:
        m_, l_ = mine[f"c{k}"], L[f"c{k}"]
        for j in range(5):
            chk(f"c{k}[{j}]", close(m_[j], *l_[j]))
        chk(f"c{k}[thr]", thr_str(m_[5]) == l_[5])
        m_, l_ = mine[f"d{k}"], L[f"d{k}"]
        chk(f"d{k}[jensen]", close(m_[0], *l_[0]))
        chk(f"d{k}[jensen gap]", close(m_[1], *l_[1]))
        chk(f"d{k}[upper]", close(m_[2], *l_[2]))
        chk(f"d{k}[upper gap]", close(m_[3], *l_[3]))
        chk(f"d{k}[thr]", thr_str(m_[4]) == l_[4])
    return n_items, n_bad, bad


L = parse_log(args.log)
mine = reductions(E)
print(f"\ngrid {E.shape}, part = {args.part}; energy range {E.max():.4g} kT")
print(f"(a) ln Z = {mine['lnZ']:.8f}; every second point {mine['lnZ_half']:.8f}")
print(f"(b) rigid rotamers: ln Z = {mine['rot_lnZ']:.6f}, minus grid per torsion {mine['rot_off_per_torsion']:+.6f};"
      f" cell-minimised: {mine['min_lnZ']:.6f}, per torsion {mine['min_off_per_torsion']:+.6f}")
print(f"    total variation grid/rigid {mine['tv_r']:.6f} (largest {mine['max_r']:.6f}); grid/minimised {mine['tv_m']:.6f} (largest {mine['max_m']:.6f})")
print(f"    rigid minimum-energy state in cell {mine['rot_min_cell']}, gap {mine['rot_gap']:.5f} kT; continuous minimum at {mine['cont_min_deg']} deg in cell {mine['cont_min_cell']};"
      f" same cell: {mine['same_cell']}; cell minimum of the rigid model's cell above the global minimum: {mine['rigid_cell_min_above_global']:.5f} kT")
print("    cell: population grid / rigid / minimised;  E_rot - E_cellmin [kT];  width term")
for c in range(3):
    for d in range(3):
        v = mine[f"cell{c}{d}"]
        print(f"      ({c}, {d}): {v[0]:.5f} / {v[1]:.5f} / {v[2]:.5f};  {v[3]:12.4f};  {v[4]:.4f}")
print("(c) uniform reference, whole energy one term: k: [maxima, minima] Jensen | all-H | best (thr) | per torsion: first-order, best")
for k in KS:
    lo1, hi1, jl, hH, best, thr = mine[f"c{k}"]
    print(f"   {k:4d}  [{lo1:.4f}, {hi1:.4f}]  {jl:.4f} | {hH:.6g} | {best:.4f} ({thr_str(thr)}) | {(hi1-lo1)/n:.4g}  {(best-jl)/n:.4g}")
print(f"(d) tilted reference: sum ln z_i = {mine['tilt_sum_lz']:.6f}; remainder {mine['tilt_rem'][0]:.5g} .. {mine['tilt_rem'][1]:.5g} kT")
print("   k: Jensen gap per torsion | upper gap per torsion (threshold rule, thr) | exhaustive over all 4^k mode assignments (k = 3) | local search")
for k in KS:
    jt, gj, best, gu, thr, gex, gloc = mine[f"d{k}"]
    print(f"   {k:4d}  {gj/n:.4e} | {gu/n:.4e} ({thr_str(thr)}) | {gex/n:.4e} | {gloc/n:.4e}")
ni, nbad, bad = compare(mine, L)
print(f"\nCOMPARISON with {args.log.split('/')[-1]}: {ni} items; disagreements: {nbad} {bad[:12]}")
print(f"brackets checked: {mine['_nb']}; violated: {mine['_viol']} (must be 0)")
c = mine["_ctrl"]
print(f"C3 controls over {c['parts']} partitions (uniform and tilted): all-H with oscillations x 0.3 excludes the grid value in {c['small']};"
      f" Jensen as an upper end violated in {c['jens']}; cell minima as a lower end violated in {c['minlow']}")

# ------------------------------------------------------------------ C1 separable energy
e1, e2, V, lzi, _ = fl.tilted_parts(E)
Es = e1[:, None] + e2[None, :]
Es = Es - Es.min()
s1, s2, Vs, lzs, _ = fl.tilted_parts(Es)
worst_gap = 0.0
for k in KS:
    b = fl.Bracket2(Vs, k, -s1, -s2)
    jt = b.jensen() + sum(lzs)
    up = b.best_threshold()[0] + sum(lzs)
    worst_gap = max(worst_gap, abs(fl.lnZ_grid(Es) - jt), abs(up - fl.lnZ_grid(Es)))
rms = fl.rotamer_models(Es)
fac = np.abs(rms["Pg"] - np.outer(rms["Pg"].sum(axis=1), rms["Pg"].sum(axis=0))).max()
print(f"C1 separable energy (sum of the two slices): remainder range {Vs.min():.1e} .. {Vs.max():.1e}; largest |Jensen gap|, |upper gap| over k: {worst_gap:.1e}"
      f"; cell populations minus product of marginals: {fac:.1e}   -> zero coupling error: {worst_gap < 1e-9 and fac < 1e-12 and abs(Vs).max() < 1e-9}")
real_fac = np.abs(fl.rotamer_models(E)["Pg"] - np.outer(fl.rotamer_models(E)["Pg"].sum(axis=1), fl.rotamer_models(E)["Pg"].sum(axis=0))).max()
print(f"   (the real energy: remainder {V.min():.4g} .. {V.max():.4g} kT; cell populations minus product of marginals {real_fac:.2e} — so C1 can fail)")

# ------------------------------------------------------------------ C2 shuffled grid
rng = np.random.default_rng(2804)
Esh = rng.permutation(E.ravel()).reshape(E.shape)
ms = reductions(Esh, do_search=False)
ni2, nbad2, _ = compare(ms, L)
print(f"C2 shuffled grid: {ni2} items compared with the same log; disagreements: {nbad2} (must be many);"
      f" brackets violated on the shuffled grid: {ms['_viol']} (the inequalities hold for ANY table: must be 0)")
rc.finish(t0)
