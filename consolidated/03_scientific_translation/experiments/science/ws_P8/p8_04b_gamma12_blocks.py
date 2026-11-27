"""
P8 step 3 -- per-subset constants at twelve residues in the BLOCK-WISE state-resolved forms 'Sb' and 'SAb'
(p8sr.BlockBound.total_T_blocks: the maximum over host states is taken of the sum over the atom pairs of a block --
P3's own per-subset form, termwise.TermBound, in anchored mode; 'SAb' in addition keeps a host outside T at its anchor).

usage: python3 -B p8_04b_gamma12_blocks.py SEQ BB TAU M [--budget SECONDS]
needs out/g12_<tag>_m<M>.npz (the same subsets, anchor; for the comparison with the pair-wise variants).
writes logs/g12b_<tag>_m<M>.log, out/g12b_<tag>_m<M>.npz
"""
import sys, os, time, itertools
import numpy as np
from p8lib import *
from p8sr import AHBound
import pwmodel as pw

a = sys.argv[1:]
seq, bb, tau, m = a[0], a[1], float(a[2]), int(a[3])
BUDGET = float(a[a.index("--budget") + 1]) if "--budget" in a else 1e18
tag = tagname(seq, bb, tau) + f"_m{m}"
if os.path.exists(os.path.join(HERE, "out", f"g12b_{tag}.npz")) and "--force" not in a:
    print(f"out/g12b_{tag}.npz exists: this run is complete (use --force to redo it); nothing done"); sys.exit(0)
ckpt = os.path.join(MYCACHE, f"g12b_{tag}_ckpt.npz")
resume = os.path.exists(ckpt)
log = Log(os.path.join(HERE, "logs", f"g12b_{tag}.log"), append=resume)
t0 = time.time()
Z = np.load(os.path.join(HERE, "out", f"g12_{tag}.npz"))
G = GBModel(seq, bb, tau=tau)
n = G.ns
c0, h, J = pw.known_tables(G)
x0, E0, nev = pw.icm_anchor(G, c0, h, J)
x0 = tuple(int(v) for v in x0)
assert list(Z["anchor"]) == list(x0)
Tall = [tuple(int(v) for v in T) for T in Z["T"]]
nT = len(Tall)
log(f"=== p8_04b_gamma12_blocks: {seq} on {bb}, tau {tau}: atoms {G.nat}, sites {n}; anchor {x0}; order {m}: {nT} subsets" + ("; RESUMING" if resume else ""))
SR = AHBound(G, x0, EnvelopeSup(G), K=m)
if resume:
    z = np.load(ckpt); i_next = int(z["i_next"]); Cb = z["Cb"]
else:
    i_next = 0; Cb = np.zeros((nT, 2))               # [subset, (Sb, SAb)]
tlast = time.time(); stopped = False
for i in range(i_next, nT):
    out = SR.total_T_blocks(m, Tall[i])
    Cb[i, 0] = sum(out["Sb"].values()); Cb[i, 1] = sum(out["SAb"].values())
    now = time.time()
    if now - tlast > 60 or i == nT - 1 or now - t0 > BUDGET:
        tmp = ckpt + ".tmp.npz"
        np.savez(tmp, i_next=i + 1, Cb=Cb); os.replace(tmp, ckpt); tlast = now
        log(f"    subset {i + 1}/{nT} done, checkpoint written, {now - t0:.0f} s")
    if now - t0 > BUDGET and i < nT - 1:
        stopped = True
        break
if stopped:
    log(f"BUDGET REACHED at subset {i + 1}/{nT}: checkpoint on disk, run the same command again to continue (not a complete run)")
    log.f.close(); sys.exit(0)
V = [str(v) for v in Z["variants"]]
tot = Z["C"].sum(axis=2)
S_ = tot[:, V.index("S")]; SA_ = tot[:, V.index("SA")]; P3_ = tot[:, V.index("P3")]
nviol = int((Cb[:, 0] > S_ * (1 + 1e-9)).sum() + (Cb[:, 1] > SA_ * (1 + 1e-9)).sum() + (Cb[:, 1] > Cb[:, 0] * (1 + 1e-9)).sum())
log(f"    per-subset chains Sb <= S, SAb <= SA, SAb <= Sb: {3 * nT} comparisons, {nviol} violations")
for j, v in enumerate(("Sb", "SAb")):
    r = P3_ / Cb[:, j]
    log(f"    Gamma_{m}[{v:3s}] = {Cb[:, j].sum():12.6g} kcal/mol = {Cb[:, j].sum() * BETA:12.6g} kT;  P3 / {v}: sums {P3_.sum() / Cb[:, j].sum():.3f}; per subset min {r.min():.2f}, median {np.median(r):.2f}, max {r.max():.2f};  "
        f"pair-wise / block-wise: {(S_.sum() if j == 0 else SA_.sum()) / Cb[:, j].sum():.3f}")
np.savez_compressed(os.path.join(HERE, "out", f"g12b_{tag}.npz"), T=np.array(Tall), Cb=Cb, anchor=np.array(x0), variants=np.array(["Sb", "SAb"]))
log.done()
