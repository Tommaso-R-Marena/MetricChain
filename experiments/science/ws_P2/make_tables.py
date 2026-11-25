"""Collect out/an_*.json into Markdown tables (stdout).  usage: python3 -B make_tables.py [GRID]"""
import sys, os, json, re, glob
import numpy as np
from anlib import HERE, KT300, BETA

grid = sys.argv[1] if len(sys.argv) > 1 else "R3"
J = {}
for p in glob.glob(os.path.join(HERE, "out", f"an_fb_*_{grid}_t0.60_tau*.json")):
    m = re.match(rf"an_fb_([A-Z]+?)c?(\d+)_([A-Za-z0-9]+)_{grid}_t0\.60_tau([0-9.]+)\.json", os.path.basename(p))
    if not m:
        continue
    J[(m.group(1), int(m.group(2)), m.group(3), m.group(4))] = json.load(open(p))
res_order = ["S", "V", "F", "L", "K", "LKSE"]
bbs = ["H", "E", "P2"]


def get(r, key, *path, default=None):
    v = r.get(key)
    for p in path:
        if v is None:
            return default
        v = v.get(p) if isinstance(v, dict) else None
    return default if v is None else v


def fmt(v, nd=2):
    if v is None:
        return "—"
    if isinstance(v, str):
        return v
    if abs(v) < 0.0095 and v != 0:
        return f"{v:.1e}"
    return f"{v:.{nd}f}"


def lengths(res, bb, tau):
    return sorted(n for (r, n, b, t) in J if r == res and b == bb and t == tau)


print(f"## Table A — domains (grid {grid})\n")
print("| residue | backbone | tau | n: states per site -> raw product / pair-clash-free / pruned product |")
print("|---|---|---|---|")
for res in res_order:
    for bb in bbs:
        for tau in ("0.70", "0.60"):
            ns = lengths(res, bb, tau)
            if not ns:
                continue
            cells = []
            for n in ns:
                r = J[(res, n, bb, tau)]
                if r.get("empty"):
                    cells.append(f"{n}: empty {r['shape']}")
                else:
                    cells.append(f"{n}: {r['shape']} -> {r['size']} / {r['clashfree']} / {r['size_pruned']}")
            keep = [cells[0]] + ([cells[len(cells) // 2]] if len(cells) > 2 else []) + ([cells[-1]] if len(cells) > 1 else [])
            print(f"| {res} | {bb} | {tau} | " + "; ".join(keep) + " |")

for resid, label in (("GB", "g_GB"), ("coul+GB", "Coulomb + GB (alternative split)"), ("ff03-ff14SB", "ff03 - ff14SB"), ("ff15ipq-ff14SB", "ff15ipq - ff14SB"), ("ff99SB-ff14SB", "ff99SB - ff14SB")):
    print(f"\n## Table B[{resid}] — max_i c_i of {label} by chain length n, kcal/mol (on the pruned product X'; in brackets on X_tau where it differs)\n")
    print("| residue | backbone | tau | " + " | ".join(f"n={n}" for n in (1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16)) + " |")
    print("|---|---|---|" + "---|" * 12)
    for res in res_order:
        for bb in bbs:
            for tau in ("0.70", "0.60"):
                ns = lengths(res, bb, tau)
                if not ns or all(J[(res, n, bb, tau)].get("empty") for n in ns):
                    continue
                row = []
                for n in (1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16):
                    r = J.get((res, n, bb, tau))
                    if r is None:
                        row.append(""); continue
                    if r.get("empty"):
                        row.append("empty"); continue
                    c = get(r, f"Xp|{resid}", "c")
                    ct = get(r, f"Xtau|{resid}", "c")
                    cell = fmt(max(c)) if c else "—"
                    if ct:
                        cell += f" [{fmt(max(ct))}]"
                    row.append(cell)
                print(f"| {res} | {bb} | {tau} | " + " | ".join(row) + " |")

print("\n## Table C — second and third order of g_GB on the pruned product X' (kcal/mol), longest enumerated chain of each kind\n")
print("| residue | bb | tau | n | X' | max c_i | rms flip | max c_ij | c_ij by separation 1,2,3,4,... (max) | max half row sum | max Dobrushin sum | min excitation of E at argmin E | max c_ijk | sum c_ijk | two-site fit rms / max / Chebyshev |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for res in res_order:
    for bb in bbs:
        for tau in ("0.70", "0.60"):
            ns = [n for n in lengths(res, bb, tau) if not J[(res, n, bb, tau)].get("empty") and get(J[(res, n, bb, tau)], "Xp|GB", "C")]
            if not ns:
                continue
            for n in ([ns[-1]] if len(ns) < 3 else [ns[len(ns) // 2], ns[-1]]):
                r = J[(res, n, bb, tau)]
                g = r["Xp|GB"]
                sep = " ".join(fmt(g["bysep"][str(s)][0]) for s in range(1, min(n, 9)))
                fit = g.get("fit", {})
                ifc = r.get("iface|GB", {})
                exc = min(ifc["star_argmin_E"]["min_excitation"]) if "star_argmin_E" in ifc else None
                print(f"| {res} | {bb} | {tau} | {n} | {r['size_pruned']} | {fmt(max(g['c']))} | {fmt(float(np.mean(g['rms'])))} | {fmt(float(np.max(g['C'])))} | {sep} | "
                      f"{fmt(max(g['half_rowsum']))} | {fmt(max(g['dobrushin']))} | {fmt(exc)} | {fmt(g.get('c3max'), 3)} | {fmt(g.get('c3sum'), 3)} | "
                      f"{fmt(fit.get('ls2_rms'), 4)} / {fmt(fit.get('ls2_max'), 4)} / {fmt(fit.get('sup2'), 4)} |")

for resid in ("GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB"):
    print(f"\n## Table D[{resid}] — interfaces on X' (energies kcal/mol, free energies nats)\n")
    print("| residue | bb | tau | n | X' | sharp sites (argmin E) | lambda* | sum ln cosh | Jensen gap | star: evals | row-sum cond. | half row sum max / min excitation | star eps* | star bracket | ball: evals | ball eps | ball bracket |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for res in res_order:
        for bb in bbs:
            for tau in ("0.70", "0.60"):
                for n in lengths(res, bb, tau):
                    r = J[(res, n, bb, tau)]
                    ifc = r.get(f"iface|{resid}")
                    if not ifc:
                        continue
                    s = ifc["star_argmin_E"]
                    b = ifc.get("ball2", {})
                    print(f"| {res} | {bb} | {tau} | {n} | {r['size_pruned']} | {ifc['sharp_argmin_E']}/{n} | {fmt(ifc['lambda_star'], 3)} | {fmt(ifc['lncosh'], 1)} | {fmt(ifc['jensen'])} | "
                          f"{s['nstar']} | {'yes' if s['rowsum_plain_ok'] else 'no'} | {fmt(max(s['half_rowsum']))} / {fmt(min(s['min_excitation']))} | {fmt(s['eps_star'])} | {fmt(s['bracket'])} | "
                          f"{b.get('nball', '—')} | {fmt(b.get('eps'), 4)} | {fmt(b.get('bracket'), 4)} |")

print("\n## Table E — decay of c_ij(g_GB) with sequence separation and with CB-CB distance (max over pairs at that separation; X')\n")
print("| system | separation: CB-CB distance (A) -> max c_ij (kcal/mol) |")
print("|---|---|")
for (res, n, bb, tau) in (("S", 6, "E", "0.70"), ("S", 6, "H", "0.70"), ("S", 6, "P2", "0.70"), ("V", 12, "E", "0.70"), ("V", 12, "P2", "0.70"),
                           ("L", 16, "H", "0.60"), ("L", 16, "E", "0.60"), ("F", 10, "H", "0.60"), ("K", 4, "H", "0.70"), ("K", 4, "E", "0.70"),
                           ("LKSE", 6, "H", "0.60")):
    r = J.get((res, n, bb, tau))
    if not r or "Xp|GB" not in r or "C" not in r["Xp|GB"]:
        continue
    C = np.array(r["Xp|GB"]["C"]); D = np.array(r["cb_dist"])
    cells = []
    for s in range(1, n):
        v = [(C[i, i + s], D[i, i + s]) for i in range(n - s)]
        k = int(np.argmax([x[0] for x in v]))
        cells.append(f"{s}: {np.mean([x[1] for x in v]):.1f} -> {fmt(v[k][0], 3)}")
    print(f"| {res}{n} on {bb}, tau {tau} | " + "; ".join(cells) + " |")
