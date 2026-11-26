#!/usr/bin/env python3
"""Benchmark B10 / addendum A17 (12): the SPLIT matters more than the fit -- coordinator's script.

Reads the stored results of surrogate_divergence_real.py (models m0 = f, m1 = f + one-body fit of gb, m2 = f + pairwise fit
of gb; f = ff14SB vacuum energy, gb = GBn2 term) and of b10_fit_directions.py (product and nearest-neighbour chain
families fitted to the solvated energy g = f + gb), and prints D_2(pi_g || model) and D_inf side by side.  Then, from
workstream P2's grids, the uniform-measure ANOVA variances by order (one-body / pair / higher, in kT^2) of beta*f, beta*gb,
beta*(f + gb), and of the Coulomb part alone and with gb: how much of the vacuum pair interaction the solvent term cancels.
Also, from b10_fit_directions.json: the statistics quoted in addendum A17 (12).
Run:  python3 b10_split_table.py > b10_split_table.log      (needs the two JSON files; about 20 s)
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2"))
import anlib
B = anlib.BETA
a = json.load(open(os.path.join(HERE, "surrogate_divergence_real.json")))
b = json.load(open(os.path.join(HERE, "b10_fit_directions.json")))
name = lambda q: q["seq"][:1] + str(q["n"]) + "_" + q["bb"]
old = {(name(r), r["surrogate"].split(" ")[0]): r for r in a}
new = {(name(q), q["family"], q["fit"]): q for q in b}

print("(1) D_2(pi_g || model) [D_inf] for five models of the solvated ensemble")
print("    instance | m0: vacuum f alone | m1: f + one-body fit of gb | product measure, ML fit of g | nearest-neighbour chain, ML fit of g | m2: f + pairwise fit of gb")
ratios = []
for aa, ns in (("V", (2, 4, 6, 8, 10, 12)), ("L", (2, 4, 6, 8)), ("S", (2, 3, 4, 5, 6))):
    for bb in ("E", "P2", "H"):
        for n in ns:
            nm = f"{aa}{n}_{bb}"
            if (nm, "m0") not in old: continue
            o0, o1, o2 = old[(nm, "m0")], old[(nm, "m1")], old[(nm, "m2")]; p, c = new[(nm, "product", "ML")], new[(nm, "chain", "ML")]
            print(f"    {nm:7s} | {o0['D2']:9.3e} [{o0['Dinf']:6.2f}] | {o1['D2']:9.3e} [{o1['Dinf']:6.2f}] | {p['D2']:9.3e} [{p['Dinf']:5.2f}] | {c['D2']:9.3e} [{c['Dinf']:5.2f}] | {o2['D2']:9.3e} [{o2['Dinf']:5.2f}]")
            if aa == "S" and n >= 3: ratios.append((nm, o0["D2"], o1["D2"], p["D2"], c["D2"]))
print("    serine, 3-6 residues: D_2 ranges  m0 %.2f..%.2f | m1 %.3f..%.3f | product %.4f..%.4f | chain %.1e..%.1e" % (
    min(r[1] for r in ratios), max(r[1] for r in ratios), min(r[2] for r in ratios), max(r[2] for r in ratios),
    min(r[3] for r in ratios), max(r[3] for r in ratios), min(r[4] for r in ratios), max(r[4] for r in ratios)))
print("    serine, 3-6 residues: D_2(m1)/D_2(product): min %.1f max %.1f;   D_2(m0)/D_2(product): min %.0f max %.0f" % (
    min(r[2] / r[3] for r in ratios), max(r[2] / r[3] for r in ratios), min(r[1] / r[3] for r in ratios), max(r[1] / r[3] for r in ratios)))

def parts(x):
    x = B * x; f1 = anlib.anova_fit(x, 1); f2 = anlib.anova_fit(x, 2)
    return float(np.var(f1)), float(np.var(f2 - f1)), float(np.var(x - f2))
print("(2) uniform-measure ANOVA variances (kT^2) by order, one-body / pair / higher")
print("    instance | f (vacuum) | gb | f + gb | pair variance: Coulomb alone -> Coulomb + gb | pair variance of f+gb over that of f")
for tag in ("S4_E", "S6_E", "S4_P2", "S6_P2", "S4_H", "S6_H", "V12_E", "V12_P2", "L8_P2", "L8_H"):
    d = anlib.load_fb(f"fb_{tag}_R3_t0.60"); f = d["tors"] + d["lj"] + d["coul"]; gb = d["gb"]
    pf, pg, pt, pc, pcg = parts(f), parts(gb), parts(f + gb), parts(d["coul"]), parts(d["coul"] + gb)
    print(f"    {tag:7s} | {pf[0]:9.3f} / {pf[1]:7.3f} / {pf[2]:7.4f} | {pg[0]:8.3f} / {pg[1]:7.3f} / {pg[2]:7.4f} | {pt[0]:9.3f} / {pt[1]:7.3f} / {pt[2]:7.4f} | {pc[1]:7.3f} -> {pcg[1]:7.3f} | {pt[1] / max(pf[1], 1e-300):6.3f}")

print("(3) statistics of b10_fit_directions.json quoted in addendum A17 (12)")
g = {}
for q in b: g.setdefault((q["tag"], q["family"]), {})[q["fit"]] = q
nontriv = {k: {x: y for x, y in f.items() if x != "LSs"} for k, f in g.items() if max(v["D2"] for x, v in f.items() if x != "LSs") >= 1e-3}
print(f"    (instance, family) pairs: {len(g)}; with D_2 of the worst of LSu/VAR/ML/CHI at least 1e-3: {len(nontriv)}")
d2s = [max(v["D2"] for v in f.values()) - min(v["D2"] for v in f.values()) for f in nontriv.values()]
print(f"    D_2 spread across the four fits: median {np.median(d2s):.4f}, max {max(d2s):.4f} nats")
print(f"    D_2(VAR) - D_2(CHI): max {max(f['VAR']['D2'] - f['CHI']['D2'] for f in nontriv.values()):.2e};  D_2(ML) - D_2(CHI): max {max(f['ML']['D2'] - f['CHI']['D2'] for f in nontriv.values()):.2e};  D_2(LSu) - D_2(CHI): max {max(f['LSu']['D2'] - f['CHI']['D2'] for f in nontriv.values()):.2e}")
order = [tuple(sorted(f, key=lambda k: f[k]["D2"])) for f in nontriv.values()]
from collections import Counter
print("    order of the fits by D_2 (best first):", dict(Counter(order)))
r1 = [v["D2"] / v["rms"] ** 2 for f in nontriv.values() for v in f.values() if v["D2"] > 1e-3]
r2 = [v["D2"] / (2 * v["KLvar"]) for f in nontriv.values() for v in f.values() if v["D2"] > 1e-3]
print(f"    D_2 / rms^2 over {len(r1)} rows with D_2 > 1e-3: min {min(r1):.3f} median {np.median(r1):.3f} max {max(r1):.3f};  D_2 / (2 KL(q||pi_g)): min {min(r2):.3f} median {np.median(r2):.3f} max {max(r2):.3f}")
dis = [max(v["Dinf"] for v in f.values()) - min(v["Dinf"] for v in f.values()) for f in nontriv.values()]
r3 = [v["Dinf"] / v["rms"] for f in nontriv.values() for v in f.values()]
bestc = Counter(min(f, key=lambda k: f[k]["Dinf"]) for f in nontriv.values()); worstc = Counter(max(f, key=lambda k: f[k]["Dinf"]) for f in nontriv.values())
print(f"    D_inf spread across the four fits: median {np.median(dis):.3f}, max {max(dis):.3f} nats;  D_inf / rms: min {min(r3):.1f} median {np.median(r3):.1f} max {max(r3):.1f}")
print(f"    fit with the smallest D_inf: {dict(bestc)};  with the largest: {dict(worstc)}")
print(f"    largest over all {len(b)} rows: D_2 {max(q['D2'] for q in b):.3f}, D_inf {max(q['Dinf'] for q in b):.3f}, rms remainder {max(q['rms'] for q in b):.3f} kT")
lss = [(abs(f["LSs"]["D2"] - f["VAR"]["D2"]), bool(f["LSs"]["lss_iterations"])) for f in g.values() if "LSs" in f]
print(f"    LSs run on {len(lss)} pairs: converged in {sum(c for _, c in lss)}, largest |D_2(LSs) - D_2(VAR)| among the converged {max(d for d, c in lss if c):.1e}, among the others {max(d for d, c in lss if not c):.2e}")
print("ALL OK")
