"""P4 item 2, tables from out/p4_02_third.json (no computation beyond counting and ratios).
usage: python3 -B p4_02b_tables.py  -> Markdown on stdout; last line 'DONE p4_02b_tables'."""
import os, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "out", "p4_02_third.json")))
TOL = 1e-9
lab = lambda r: f"{r['res']}{r['nres']}/{r['bb']} ({r['tau'][1:]})"
yn = lambda b: "yes" if b else "no"
med = lambda v: float(np.median(v)) if len(v) else float("nan")

print(f"instances: {len(rows)} (g_GB, at least three sites with more than one state); with LP allocations: {sum(1 for r in rows if r['lp'])}")
print("\n### T5 -- does the reference minimise the lower model?  (counts over all instances)\n")
print("| family | instances | env3 (three-body envelope) | pair form | site form | LP-A (best pair shares) | CV-A (best covering) | pair yes, site no | env3 yes, pair no |")
print("|---|---|---|---|---|---|---|---|---|")
fams = (("all", None), ("Ser", "S"), ("Lys", "K"), ("LKSE", "LKSE"), ("Val", "V"), ("Leu", "L"), ("Phe", "F"))
for nm, fam in fams:
    R = [r for r in rows if fam is None or r["res"] == fam]
    ok = lambda r, k: (r["models"][k] if k in r["models"] else r["lp"][k])["margin"] >= -TOL
    Rl = [r for r in R if r["lp"]]
    print(f"| {nm} | {len(R)} | {sum(ok(r, 'env3') for r in R)} | {sum(ok(r, 'pair') for r in R)} | {sum(ok(r, 'site') for r in R)} | "
          f"{sum(ok(r, 'LP-A') for r in Rl)} of {len(Rl)} | {sum(ok(r, 'CV-A') for r in Rl)} of {len(Rl)} | "
          f"{sum(ok(r, 'pair') and not ok(r, 'site') for r in R)} | {sum(ok(r, 'env3') and not ok(r, 'pair') for r in R)} |")
print("\ninstances in which the pair form certifies and the site form does not:",
      [f"{lab(r)}: margin site {r['models']['site']['margin']:.3f}, pair {r['models']['pair']['margin']:.3f}" for r in rows
       if r["models"]["pair"]["margin"] >= -TOL and r["models"]["site"]["margin"] < -TOL])
print("instances in which the envelope certifies and the pair form does not:",
      [lab(r) for r in rows if r["models"]["env3"]["margin"] >= -TOL and r["models"]["pair"]["margin"] < -TOL])
print("instances in which the envelope does not certify:",
      [f"{lab(r)}: env3 {r['models']['env3']['margin']:.3f}, pair {r['models']['pair']['margin']:.3f}, site {r['models']['site']['margin']:.3f}"
       + (f", LP-A {r['lp']['LP-A']['margin']:.3f}, CV-A {r['lp']['CV-A']['margin']:.3f}" if r['lp'] else "") for r in rows if r["models"]["env3"]["margin"] < -TOL])
d = [r["models"]["pair"]["margin"] - r["models"]["env3"]["margin"] for r in rows]
print(f"margin(pair) - margin(env3): min {min(d):.2e}, max {max(d):.2e}; margin(pair) = margin(env3) to 1e-9 in {sum(abs(x) < 1e-9 for x in d)} of {len(rows)}")
d = [r["models"]["pair"]["margin"] - r["models"]["site"]["margin"] for r in rows]
print(f"margin(pair) - margin(site): min {min(d):.4f}, median {med(d):.4f}, max {max(d):.4f} kcal/mol")
Rl = [r for r in rows if r["lp"]]
d = [r["lp"]["LP-A"]["margin"] - r["models"]["pair"]["margin"] for r in Rl]
print(f"margin(LP-A) - margin(pair thirds): max {max(d):.2e}; larger than 1e-9 in {sum(x > 1e-9 for x in d)} of {len(Rl)}:",
      [f"{lab(r)}: {r['models']['pair']['margin']:.4f} -> {r['lp']['LP-A']['margin']:.4f} (env3 {r['models']['env3']['margin']:.4f})" for r in Rl if r["lp"]["LP-A"]["margin"] - r["models"]["pair"]["margin"] > 1e-9])
d = [r["lp"]["CV-A"]["margin"] - r["lp"]["LP-A"]["margin"] for r in Rl]
print(f"margin(CV-A) - margin(LP-A): max {max(d):.2e}; larger than 1e-9 in {sum(x > 1e-9 for x in d)} of {len(Rl)}; largest covering violation of a CV solution {max(max(r['lp']['CV-A']['cover_violation'], r['lp']['CV-B']['cover_violation']) for r in Rl):.1e}")

print("\n### T6 -- ln Z(m) - ln Z(E) (nats): how tight are the lower models\n")
print("| family | instances | env3: median (max) | pair: median (max) | site: median (max) | site/pair: median (range) | pair/env3: median (range) | LZ (best found pair shares)/pair: median (range) |")
print("|---|---|---|---|---|---|---|---|")
for nm, fam in fams:
    R = [r for r in rows if (fam is None or r["res"] == fam) and r["models"]["env3"]["dlnZ"] > 1e-12]
    if not R:
        continue
    e = [r["models"]["env3"]["dlnZ"] for r in R]; p_ = [r["models"]["pair"]["dlnZ"] for r in R]; s = [r["models"]["site"]["dlnZ"] for r in R]
    sp = [a / b for a, b in zip(s, p_)]; pe = [a / b for a, b in zip(p_, e)]
    lz = [r["lp"]["LZ"]["dlnZ"] / r["models"]["pair"]["dlnZ"] for r in R if r["lp"] and "LZ" in r["lp"]]
    print(f"| {nm} | {len(R)} | {med(e):.2e} ({max(e):.2e}) | {med(p_):.2e} ({max(p_):.2e}) | {med(s):.2e} ({max(s):.2e}) | {med(sp):.1f} ({min(sp):.1f}-{max(sp):.1f}) | "
          f"{med(pe):.1f} ({min(pe):.1f}-{max(pe):.1f}) | {med(lz):.2f} ({min(lz):.2f}-{max(lz):.2f}) [{len(lz)}] |")
print("\ninstances with ln Z(site) - ln Z(E) > 0.1 nats:", sum(r["models"]["site"]["dlnZ"] > 0.1 for r in rows), "; pair:", sum(r["models"]["pair"]["dlnZ"] > 0.1 for r in rows),
      "; env3:", sum(r["models"]["env3"]["dlnZ"] > 0.1 for r in rows))

print("\n### T7 -- largest gap max_x (E - m), kcal/mol\n")
same = sum(abs(r["models"]["site"]["maxgap"] - r["models"]["env3"]["maxgap"]) < 1e-9 and abs(r["models"]["pair"]["maxgap"] - r["models"]["env3"]["maxgap"]) < 1e-9 for r in rows)
print(f"the largest gap is the same for env3, pair and site (to 1e-9) in {same} of {len(rows)} instances")
print("instances where it differs:", [f"{lab(r)}: env3 {r['models']['env3']['maxgap']:.4f}, pair {r['models']['pair']['maxgap']:.4f}, site {r['models']['site']['maxgap']:.4f}" for r in rows
                                      if not (abs(r["models"]["site"]["maxgap"] - r["models"]["env3"]["maxgap"]) < 1e-9 and abs(r["models"]["pair"]["maxgap"] - r["models"]["env3"]["maxgap"]) < 1e-9)])
print("a state of largest gap has every multi-state site changed: env3", sum(r["models"]["env3"]["maxgap_all_changed"] for r in rows), ", pair", sum(r["models"]["pair"]["maxgap_all_changed"] for r in rows),
      ", site", sum(r["models"]["site"]["maxgap_all_changed"] for r in rows), f"of {len(rows)}")
d = [r["models"]["pair"]["maxgap"] - r["lp"]["LP-B"]["maxgap"] for r in Rl]
print(f"maxgap(pair thirds) - maxgap(LP-B): max {max(d):.2e}; larger than 1e-9 in {sum(x > 1e-9 for x in d)} of {len(Rl)}")

print("\n### T8 -- selected instances (those of P2's table 5(c)); energies kcal/mol, free energies nats\n")
print("| instance | X' | sum c_T | max c_T | margin env3 / pair / site | ln Z(m) - ln Z(E): env3 / pair / site / LZ | cost number Z(m)/Z(E) - 1: pair / site | largest gap env3 / pair / site | share certificate 11.18b(c): pair / site | state-dependent shares: pair / site |")
print("|---|---|---|---|---|---|---|---|---|---|")
sel = [("S", 6, "E", "0.70"), ("S", 6, "P2", "0.70"), ("S", 6, "H", "0.70"), ("S", 6, "H", "0.60"), ("V", 8, "E", "0.70"), ("L", 8, "H", "0.60"), ("F", 7, "P2", "0.60"),
       ("K", 4, "H", "0.70"), ("K", 3, "E", "0.70"), ("K", 4, "E", "0.70"), ("K", 4, "P2", "0.70"), ("K", 4, "H", "0.60"), ("K", 4, "E", "0.60"), ("K", 4, "P2", "0.60"),
       ("LKSE", 5, "H", "0.60"), ("LKSE", 6, "H", "0.60"), ("LKSE", 6, "P2", "0.60"), ("LKSE", 6, "E", "0.60"), ("L", 16, "H", "0.60"), ("V", 12, "P2", "0.70")]
idx = {(r["res"], r["nres"], r["bb"], r["tau"]): r for r in rows}


def ss(c):
    if c["shares"]:
        return "(shares)"
    return "—" if c["sshares_slack"] is None else ("yes" if c["sshares_slack"] >= 0 else "no")


for key in sel:
    r = idx.get(key)
    if r is None:
        continue
    m = r["models"]; lz = r["lp"].get("LZ") if r["lp"] else None
    print(f"| {lab(r)} | {r['size']} | {r['c3sum']:.3f} | {r['c3max']:.4f} | {m['env3']['margin']:.3f} / {m['pair']['margin']:.3f} / {m['site']['margin']:.3f} | "
          f"{m['env3']['dlnZ']:.1e} / {m['pair']['dlnZ']:.1e} / {m['site']['dlnZ']:.1e} / {('%.1e' % lz['dlnZ']) if lz else '—'} | {m['pair']['cost']:.2e} / {m['site']['cost']:.2e} | "
          f"{m['env3']['maxgap']:.3f} / {m['pair']['maxgap']:.3f} / {m['site']['maxgap']:.3f} | {yn(r['cert']['pair']['shares'])} / {yn(r['cert']['site']['shares'])} | {ss(r['cert']['pair'])} / {ss(r['cert']['site'])} |")

print("\n### T9 -- share certificates of Proposition 11.18b(c)/(d) on the third-order lower models\n")
print("| family | instances | pair form: reference minimises | ..shares exist | ..row-sum | ..state-dependent shares | site form: reference minimises | ..shares exist | ..row-sum | ..state-dependent shares |")
print("|---|---|---|---|---|---|---|---|---|---|")
for nm, fam in fams:
    R = [r for r in rows if fam is None or r["res"] == fam]
    cells = []
    for form in ("pair", "site"):
        M = [r for r in R if r["models"][form]["margin"] >= -TOL]
        sh = sum(r["cert"][form]["shares"] for r in M)
        rs = sum(r["cert"][form]["rowsum"] for r in M)
        st = sum(1 for r in M if r["cert"][form]["shares"] or (r["cert"][form]["sshares_slack"] is not None and r["cert"][form]["sshares_slack"] >= 0))
        cells.append(f"{len(M)} | {sh} | {rs} | {st}")
    bad = sum(1 for r in R for form in ("pair", "site") if r["cert"][form]["shares"] and r["models"][form]["margin"] < -TOL)
    assert bad == 0
    print(f"| {nm} | {len(R)} | {cells[0]} | {cells[1]} |")
print("\npolar and charged instances (Ser, Lys, LKSE) in which the second-order star fails but the third-order pair model certifies: see T9 rows Ser, Lys, LKSE;")
P = [r for r in rows if r["res"] in ("S", "K", "LKSE")]
print("  largest deficit w_ij of the pair form by family (kcal/mol):", {f: round(max(r["cert"]["pair"]["wmax"] for r in P if r["res"] == f), 2) for f in ("S", "K", "LKSE")},
      "; smallest:", {f: round(min(r["cert"]["pair"]["wmax"] for r in P if r["res"] == f), 3) for f in ("S", "K", "LKSE")})
print("\n### T10 -- pair form: every instance in which the reference minimises the model and the share certificate fails\n")
print("| instance | X' | margin of the pair model | min Delta_i | largest deficit w_ij | over-dense set: excess | state-dependent shares: exact slack |")
print("|---|---|---|---|---|---|---|")
for r in rows:
    c = r["cert"]["pair"]
    if r["models"]["pair"]["margin"] >= -TOL and not c["shares"]:
        sl = c["sshares_slack"]
        print(f"| {lab(r)} | {r['size']} | {r['models']['pair']['margin']:.4f} | {min(d for d in r['Delta'] if d is not None):.4f} | {c['wmax']:.3f} | {c['overdense']}: {c['excess']:.3f} | {('%.4f' % sl) if sl is not None else 'LP failed'} |")
print("\nsite form, reference minimises and shares fail:", [lab(r) for r in rows if r["models"]["site"]["margin"] >= -TOL and not r["cert"]["site"]["shares"]])
print("DONE p4_02b_tables")
