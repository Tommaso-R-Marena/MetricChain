"""Validation of fbmodel.FBModel (run: python3 -B test_fbmodel.py).

For each system: random rotamer assignments (all R3 states, clashing or not) ->
 (a) assembled coordinates == full internal-coordinate build;
 (b) table sums of every pair-additive component == P's FastFF on the full conformation
     (this is the numerical statement "the vacuum energy is exactly pairwise in the sites");
 (c) table-based GBn2 == FastFF's GBn2, and == OpenMM's own CustomGBForce on the Reference
     (double precision) platform for a subset;
 (d) decomposed clash score == FastFF's clash score.
"""
import math, time, sys
import numpy as np
from fbmodel import FBModel, BACKBONES

rng = np.random.default_rng(3)
cases = [("VVVV", "H"), ("VVVV", "E"), ("LLL", "H"), ("LLL", "P2"), ("SSS", "E"), ("FFF", "H"), ("KKK", "H"),
         ("KKK", "E"), ("LKSE", "H"), ("LKSE", "P2"), ("LKSELKSE", "H"), ("LLLLLL", "Hp")]
if len(sys.argv) > 1:
    cases = [tuple(a.split(":")) for a in sys.argv[1:]]
worst = {}
for seq, bb in cases:
    t0 = time.time()
    Mdl = FBModel(seq, bb, grid="R3", extra_ffs=("ff99SB", "ff03", "ff15ipq"), platform="Reference")
    P, F = Mdl.P, Mdl.F
    t1 = time.time()
    M = 200
    st = np.stack([rng.integers(0, k, M) for k in Mdl.k], axis=1)
    # half of the sample: only one-site clash-free states (if any exist at the site)
    dom = Mdl.domain(0.70)
    for i in range(Mdl.ns):
        if len(dom[i]):
            st[M // 2:, i] = rng.choice(dom[i], M - M // 2)
    X = Mdl.assemble(st)
    Xfull = P.coords(np.repeat(Mdl.phi, M, 0), np.repeat(Mdl.psi, M, 0), Mdl.chi_of(st))
    dcoord = np.abs(X - Xfull).max()
    with np.errstate(divide="ignore"):
        Ef = F.energies(X, gb=("gbn2",))
    t2 = time.time()
    cl = Mdl.clash_of(st)
    dclash = np.abs(cl - Ef["clash"]).max()
    ok = cl > 0.5
    dev = {}
    for c in ("tors", "lj", "coul"):
        dev[c] = np.abs(Mdl.table_energy(st, "ff14SB", (c,)) - Ef[c])
    for ff in P.extra:
        for c in ("tors", "lj", "coul"):
            dev[ff + "_" + c] = np.abs(Mdl.table_energy(st, ff, (c,)) - Ef[ff + "_" + c])
    t3 = time.time()
    gb = Mdl.gb_energy(st)
    t4 = time.time()
    dev["gbn2(tables) vs FastFF"] = np.abs(gb - Ef["gbn2"])
    sub = np.flatnonzero(ok)[:25]
    Eo = P.energies(X[sub])
    dev_omm = np.abs(gb[sub] - Eo["gbn2"]).max() if len(sub) else float("nan")
    dev_omm_f = np.abs(Mdl.table_energy(st[sub]) - (Eo["tors"] + Eo["nb"])).max() if len(sub) else float("nan")
    print(f"\n{seq} on {bb} {BACKBONES[bb]}: atoms {P.natoms}, sites {Mdl.ns}, states/site {Mdl.k}; fixed-atom clash score {Mdl.s_fixed:.3f}; "
          f"states with one-site score > 0.70: {[len(d) for d in dom]}")
    print(f"   {int(ok.sum())} of {M} random assignments with clash score > 0.5;  max |assembled - full build| = {dcoord:.1e} A;  "
          f"max |clash(tables) - clash(FastFF)| = {dclash:.1e}")
    line = "   max |tables - FastFF| (kcal/mol; clash-free | relative on all): "
    for k, d in dev.items():
        a = d[ok].max() if ok.any() else float("nan")
        ref = np.abs(Ef[k if k in Ef else "gbn2"])
        rel = (d / np.maximum(1.0, ref)).max()
        worst[k] = max(worst.get(k, 0.0), a if a == a else 0.0)
        line += f"{k} {a:.1e}|{rel:.0e}; "
    print(line)
    print(f"   GBn2(tables) vs OpenMM Reference CustomGBForce on {len(sub)} conformations: {dev_omm:.1e} kcal/mol;  "
          f"f(tables) vs OpenMM (torsion + nonbonded groups): {dev_omm_f:.1e}")
    worst["gbn2 vs OpenMM"] = max(worst.get("gbn2 vs OpenMM", 0.0), dev_omm if dev_omm == dev_omm else 0.0)
    worst["f vs OpenMM"] = max(worst.get("f vs OpenMM", 0.0), dev_omm_f if dev_omm_f == dev_omm_f else 0.0)
    print(f"   timing: setup {t1-t0:.1f}s; FastFF {1e3*(t2-t1)/M:.2f} ms/conf; table GB {1e6*(t4-t3)/M:.0f} us/conf (first call includes the tables)")
print("\nworst over all systems (clash-free conformations):", {k: f"{v:.1e}" for k, v in worst.items()})
