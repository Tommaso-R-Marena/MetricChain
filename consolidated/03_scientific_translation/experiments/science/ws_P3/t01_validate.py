"""
P3 step 1 -- validation of p3core.GBModel on FRESH states (seed 20261125, systems partly different
from P2's test list):
  (a) table-based energy  vs  table-free direct evaluation (same formulas, full distance matrix);
  (b) table-based energy  vs  OpenMM 8.6.1 CustomGBForce on the Reference (double) platform;
  (c) table-based energy  vs  P2's fbmodel.gb_energy (independent block implementation);
  (d) pruned_domain reproduces the pruned product shapes stored in P2's JSON outputs (where present).
run:  OMP_NUM_THREADS=1 python3 -B t01_validate.py [gbn2|obc2]
"""
import sys, os, json, time
import numpy as np
from p3core import GBModel, pruned_domain, P2DIR, expand_seq

kind = sys.argv[1] if len(sys.argv) > 1 else "gbn2"
rng = np.random.default_rng(20261125)
cases = [("V6", "E"), ("V5", "P2"), ("S4", "H"), ("S5", "E"), ("L5", "E"), ("L6", "H"), ("F3", "P2"), ("F4", "E"),
         ("K3", "P2"), ("K2", "E"), ("LKSE:5", "E"), ("LKSE:7", "H"), ("V12", "P2"), ("L16", "H")]
worst = dict(direct=0.0, openmm=0.0, p2=0.0)
for seq, bb in cases:
    t0 = time.time()
    G = GBModel(seq, bb, kind=kind, platform="Reference")           # full R3 grid as domain
    fb = G.fb
    M = 60
    st = np.stack([rng.integers(0, k, M) for k in G.k], axis=1)
    # second half: states of the clash-free pruned product at tau = 0.60 (if non-empty)
    dom = pruned_domain(fb, 0.60)
    if min(len(d) for d in dom) > 0:
        for i in range(G.ns):
            st[M // 2:, i] = rng.choice(dom[i], M - M // 2)
    cl = fb.clash_of(st)
    ok = cl > 0.5
    e_tab, e_self, e_cross = G.energy(st, parts=True)
    e_dir = G.energy_direct(st[:20])
    e_omm = G.openmm_energy(st[:20])
    d_dir = np.abs(e_tab[:20] - e_dir).max()
    d_omm = np.abs(e_tab[:20] - e_omm)
    d_omm_ok = d_omm[ok[:20]].max() if ok[:20].any() else float("nan")
    line = (f"{seq:8s} {bb:3s} {kind}: atoms {G.nat:3d}, sites {G.ns:2d}, states/site {G.k[0]}; clash>0.5: {int(ok.sum()):2d}/{M}; "
            f"|tab-direct| {d_dir:.1e}; |tab-OpenMM(Reference)| all {d_omm.max():.1e}, clash-free {d_omm_ok:.1e}")
    worst["direct"] = max(worst["direct"], d_dir)
    worst["openmm"] = max(worst["openmm"], d_omm.max())
    if kind == "gbn2":
        e_p2 = fb.gb_energy(st)
        d_p2 = np.abs(e_tab - e_p2).max()
        worst["p2"] = max(worst["p2"], d_p2)
        line += f"; |tab-P2 block| {d_p2:.1e}"
    line += f"; E range [{e_tab.min():.2f}, {e_tab.max():.2f}] (self [{e_self.min():.1f}, {e_self.max():.1f}]) kcal/mol; {time.time() - t0:.1f}s"
    print(line, flush=True)
    # (d) pruned domain against P2's stored shapes
    tag = f"fb_{seq.replace(':', 'c')}_{bb}_R3_t0.60"
    for tau in (0.60, 0.70):
        fn = os.path.join(P2DIR, "out", f"an_{tag}_tau{tau:.2f}.json")
        if os.path.exists(fn):
            r = json.load(open(fn))
            mine = [len(d) for d in pruned_domain(fb, tau)]
            theirs = r.get("shape_pruned", "EMPTY" if r.get("empty") else None)
            flag = "OK" if (theirs == mine or (theirs == "EMPTY" and min(mine) == 0)) else "MISMATCH"
            print(f"      pruned product at tau={tau}: mine {mine}  P2 {theirs}  {flag}")
print("worst deviations (kcal/mol):", {k: f"{v:.1e}" for k, v in worst.items()})
