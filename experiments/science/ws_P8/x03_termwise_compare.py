"""P8: P3's own per-subset bound in ANCHORED mode (termwise.TermBound, maximum over host states of the bound taken
block by block) against P3's closed form (gfbound, merged ingredients) and my pair-wise state-resolved variant 'S'.
usage: python3 -B x03_termwise_compare.py SEQ BB TAU      (needs out/m1_<tag>.npz, out/sr_<tag>.npz)
writes logs/x03_<tag>.log"""
import sys, os, time
import numpy as np
from p8lib import *
from termwise import TermBound                         # P3 (read-only)
seq, bb, tau = sys.argv[1], sys.argv[2], float(sys.argv[3])
tag = tagname(seq, bb, tau)
log = Log(os.path.join(HERE, "logs", f"x03_{tag}.log"))
Z = np.load(os.path.join(HERE, "out", f"m1_{tag}.npz")); Zs = np.load(os.path.join(HERE, "out", f"sr_{tag}.npz"))
G = GBModel(seq, bb, tau=tau)
x0 = tuple(int(v) for v in Z["anchor"])
Tlist = [tuple(int(v) for v in row if v >= 0) for row in Z["Tlist"]]
orders = np.array([len(T) for T in Tlist])
TB = TermBound(G, sup=EnvelopeSup(G), anchor=x0, kmax=int(orders.max()), pad_I=G.ns * PAD_TAB)
log(f"=== x03_termwise_compare: {seq} on {bb}, tau {tau}; anchor {x0}; {len(Tlist)} subsets")
tw = np.zeros(len(Tlist))
t0 = time.time()
for ti, T in enumerate(Tlist):
    tw[ti] = (TB.self_bound(T, mode="anchored") + TB.cross_bound(T, mode="anchored")) * RND
log(f"    P3's termwise bound (anchored mode) of {len(Tlist)} subsets: {time.time() - t0:.0f} s")
nviol = int((tw < Z["C_total"] - 1e-12).sum() + (tw < Z["C_allplus"] - 1e-12).sum())
log(f"    termwise >= c_T(g) and >= c_T(g_|q|): {2 * len(Tlist)} comparisons, {nviol} violations")
for m in sorted(set(orders.tolist())):
    sel = orders == m
    a, b, c, d = Z["C_P3"][sel].sum(), tw[sel].sum(), Zs["T_S"][sel].sum(), Z["C_total"][sel].sum()
    r = Zs["T_S"][sel] / tw[sel]
    log(f"    order {m}: truth {d:.4e} | P3 closed form (gfbound) {a:.4e} | P3 per-subset termwise, anchored, block-wise maxima {b:.4e} | my 'S', pair-wise maxima {c:.4e} | "
        f"gfbound/termwise {a / b:.2f}; S/termwise {c / b:.3f} (per subset {r.min():.3f}..{r.max():.3f})")
log.done()
