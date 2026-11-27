"""P8 exploration: block-wise against pair-wise state-resolved maxima on a few subsets (timing and gain).
usage: python3 -B x04_block_probe.py SEQ BB TAU M NSUB"""
import sys, time, itertools
import numpy as np
from p8lib import *
from p8sr import AHBound
import pwmodel as pw
seq, bb, tau, m, nsub = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
log = Log(os.path.join(HERE, "logs", f"x04_{tagname(seq, bb, tau)}_m{m}.log"))
G = GBModel(seq, bb, tau=tau)
c0, h, J = pw.known_tables(G)
x0, E0, nev = pw.icm_anchor(G, c0, h, J)
x0 = tuple(int(v) for v in x0)
SR = AHBound(G, x0, EnvelopeSup(G), K=m)
Ts = list(itertools.combinations(range(G.ns), m))
rng = np.random.default_rng(1)
pick = [Ts[i] for i in sorted(rng.choice(len(Ts), size=min(nsub, len(Ts)), replace=False))]
tot = dict(P3=0.0, S=0.0, SA=0.0, Sb=0.0, SAb=0.0)
t0 = time.time()
for T in pick:
    a = SR.total_T(m, T); b = SR.total_T_blocks(m, T)
    v = dict(P3=sum(a["P3"]), S=sum(a["S"]), SA=sum(a["SA"]), Sb=sum(b["Sb"].values()), SAb=sum(b["SAb"].values()))
    assert v["Sb"] <= v["S"] * (1 + 1e-9) and v["SAb"] <= v["SA"] * (1 + 1e-9) and v["SAb"] <= v["Sb"] * (1 + 1e-9)
    for k in tot:
        tot[k] += v[k]
log(f"{seq}/{bb} order {m}: {len(pick)} random subsets, {time.time() - t0:.1f} s: sums " + ", ".join(f"{k} {v:.5g}" for k, v in tot.items()) +
    f";  S/Sb = {tot['S'] / tot['Sb']:.3f}, SA/SAb = {tot['SA'] / tot['SAb']:.3f}, P3/SAb = {tot['P3'] / tot['SAb']:.2f}")
log.done()
