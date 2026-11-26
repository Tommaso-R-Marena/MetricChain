"""
P8 step 3 -- at twelve residues, my block-wise state-resolved constants 'Sb' against workstream P3's OWN per-subset
bound termwise.TermBound in anchored mode (an independent code path of P3: explicit set partitions, Python loops over
host states), on a random sample of subsets.  They must agree to rounding.

usage: python3 -B p8_04c_termwise12.py SEQ BB TAU M NSUB      -> logs/tw12_<tag>_m<M>.log, out/tw12_<tag>_m<M>.json
"""
import sys, os, json, time, itertools
import numpy as np
from p8lib import *
from p8sr import AHBound
from termwise import TermBound                         # P3 (read-only)
import pwmodel as pw

seq, bb, tau, m, nsub = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
tag = tagname(seq, bb, tau) + f"_m{m}"
log = Log(os.path.join(HERE, "logs", f"tw12_{tag}.log"))
G = GBModel(seq, bb, tau=tau)
c0, h, J = pw.known_tables(G)
x0, E0, nev = pw.icm_anchor(G, c0, h, J)
x0 = tuple(int(v) for v in x0)
sup = EnvelopeSup(G)
SR = AHBound(G, x0, sup, K=m)
TB = TermBound(G, sup=sup, anchor=x0, kmax=m, pad_I=G.ns * PAD_TAB)
Ts = list(itertools.combinations(range(G.ns), m))
rng = np.random.default_rng(12)
pick = [Ts[i] for i in sorted(rng.choice(len(Ts), size=min(nsub, len(Ts)), replace=False))]
log(f"=== p8_04c_termwise12: {seq} on {bb}, tau {tau}: {G.nat} atoms, anchor {x0}; order {m}; {len(pick)} random subsets of {len(Ts)}")
rows = []; worst = 0.0
t_mine = t_p3 = 0.0
for T in pick:
    t1 = time.time(); b = SR.total_T_blocks(m, T); mine = sum(b["Sb"].values()); t_mine += time.time() - t1
    t1 = time.time(); p3 = (TB.self_bound(T, mode="anchored") + TB.cross_bound(T, mode="anchored")) * RND; t_p3 += time.time() - t1
    gf = sum(SR.total(m, list(T)))
    dev = abs(mine - p3) / p3
    worst = max(worst, dev)
    rows.append(dict(T=list(T), Sb=mine, termwise=p3, gfbound=gf, SAb=sum(b["SAb"].values())))
    log(f"    T = {T}: mine (Sb) {mine:.10e}, P3 termwise anchored {p3:.10e}, relative deviation {dev:.1e};  P3 closed-form summand (gfbound) {gf:.4e} = {gf / p3:.1f} x")
log(f"    largest relative deviation over {len(pick)} subsets: {worst:.1e};  time per subset: mine {t_mine / len(pick):.2f} s, P3's termwise {t_p3 / len(pick):.1f} s")
assert worst < 1e-9
with open(os.path.join(HERE, "out", f"tw12_{tag}.json"), "w") as fh:
    json.dump(dict(seq=seq, bb=bb, tau=tau, m=m, worst=worst, rows=rows, time_mine=t_mine / len(pick), time_termwise=t_p3 / len(pick)), fh, indent=1)
log.done()
