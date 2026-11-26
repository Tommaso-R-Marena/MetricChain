"""
P7 item 2, exactness of the NEGATIVE statements: "branching on site i does not certify".

p7_02_branch.py decides that a leaf is not certified from a floating-point LP (no certificate was found whose
integer check passes).  Here every such failure is turned into an exact statement: for each gap analysis and
each site i whose branching fails, one failing leaf box B is taken (the leaf with x_i = a), the primal
pairwise relaxation on B is solved, its vertex is read as a rational point (common denominator found, then
every normalisation / marginalisation constraint and the support inside B are re-checked in integer
arithmetic), and its value is computed exactly on the published integer instance and on the float-table
model.  A feasible fractional point of the leaf with value < 0 = L(x0) - L(x0) proves, by weak duality
(Proposition P7.1), that NO leaf certificate exists for that leaf, hence that no tree whose root branches on
site i with one leaf per state and no further branching certifies the root.

usage: python3 -B p7_02b_exact.py > logs/p7_02b_exact.log   (writes out/p7_02b_exact.json; last line "DONE p7_02b_exact")
"""
import sys, os, json, time
sys.dont_write_bytecode = True
import numpy as np
import p7lib as L7
from p7lib import PM, IPM, L4

t00 = time.time()
print(f"p7_02b_exact  started {L7.now()}")
five = json.load(open(os.path.join(L7.HERE, "out", "p7_01_five.json")))["gaps"]
branch = {(r["instance"], r["tau"]): r for r in json.load(open(os.path.join(L7.HERE, "out", "p7_02_branch.json")))}
rows = []
nfail = nexact = 0
for g in five:
    iname = f"{g['family']}{g['nres']}/{g['bb']}"
    br = branch[(iname, g["tau"])]
    inst = L4.load_instance(g["tag"], float(g["tau"]))
    Lmod, x0, E, C = L7.second_order_grid(inst, g["split"])
    pm = PM.from_grid(Lmod, x0); ipm = IPM(pm); Dfull = pm.full_domain()
    print(f"\n=== {iname} tau {g['tau']} split {g['split']}: sites that certify {br['working']}")
    for i_s, leaves in br["site_leaves"].items():
        i = int(i_s)
        bad = [x for x in leaves if not x["ok"]]
        if not bad:
            continue
        nfail += 1
        # the failing leaf with the most negative LP value (for a reference leaf "lp" is the slack t of the share LP)
        x = min(bad, key=lambda v: v["lp"])
        a = x["state"]
        D = L7.fix(Dfull, i, a)
        p = L7.primal_lp(pm, D)
        rp = L7.rationalise_point(pm, ipm, p["mu1"], p["mu2"])
        ok = False
        if rp is not None:
            inside = all(not rp["N1"][j][[s for s in range(pm.shape[j]) if s not in set(int(v) for v in D[j])]].any() for j in range(pm.n))
            ok = bool(inside and rp["value_int"] < 0 and rp["value"] < 0)
        nexact += ok
        rows.append(dict(instance=iname, tau=g["tau"], split=g["split"], site=i, state=int(a), kind=x["kind"], n_failing_leaves=len(bad), lp_value=p["val"],
                         den=(rp["den"] if rp else None), exact_value_published=(float(rp["value_int"]) * L7.UNIT if rp else None),
                         exact_value_model=(float(rp["value"]) if rp else None), exact=ok))
        print(f"  site {i:2d}: {len(bad)} failing leaf/leaves; leaf x_{i} = {a} ({'contains x0' if x['kind'] == 'R' else 'does not contain x0'}): relaxation value {p['val']:.9f}; "
              + (f"rational vertex with denominator {rp['den']}, exact value {float(rp['value_int']) * L7.UNIT:.12f} (published), {float(rp['value']):.12f} (float-table model) -> "
                 f"{'EXACT: no leaf certificate exists' if ok else 'NOT exact'}" if rp else "no small denominator found -> NOT exact"))
json.dump(rows, open(os.path.join(L7.HERE, "out", "p7_02b_exact.json"), "w"), indent=1)
print(f"\n{nfail} (analysis, site) pairs whose branching fails; for {nexact} of them a failing leaf has an exactly verified fractional point with negative value")
print(f"[{time.time() - t00:.0f}s] wrote out/p7_02b_exact.json   finished {L7.now()}")
print("DONE p7_02b_exact")
