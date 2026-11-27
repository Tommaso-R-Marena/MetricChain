"""P3: ablation -- certified remainder constants of GBn2 with the neck term switched off (m0 := 0; NOT a model
anyone uses; it isolates what the neck contributes to the constants), next to full GBn2 and to OBC2.
usage: python3 -B x05_neck.py SEQ:BB:TAU ..."""
import sys, numpy as np
from p3core import GBModel, KT300
from encl import EnvelopeSup
from gfbound import GFBound
from pwmodel import known_tables, icm_anchor
for spec in sys.argv[1:]:
    seq, bb, tau = spec.split(":")[0], spec.split(":")[1], float(spec.split(":")[2])
    out = []
    for label, kind, neck in (("GBn2", "gbn2", True), ("GBn2 without neck", "gbn2", False), ("OBC2", "obc2", True)):
        G = GBModel(seq, bb, tau=tau, kind=kind)
        if not neck:
            G.m0 = np.zeros_like(G.m0)
            G._tables()
        c0, h, J = known_tables(G)
        x0, E0, nev = icm_anchor(G, c0, h, J)
        GF = GFBound(G, x0, EnvelopeSup(G), K=5)
        g = [sum(GF.total(m)) for m in (3, 4, 5)]
        # relative range of the Born radii over single-site changes at the anchor (a measure of the small parameter)
        st = np.repeat(np.array(x0)[None], sum(G.k), 0); r = 0
        for i in range(G.ns):
            for a in range(G.k[i]):
                st[r, i] = a; r += 1
        ib = G.invB(G.descreening(st))
        spread = float((np.log(ib).max(0) - np.log(ib).min(0)).max())
        out.append(f"{label}: Gamma_3,4,5 = {g[0]:.3e}, {g[1]:.3e}, {g[2]:.3e} kcal/mol; largest single-flip change of ln B at the anchor {spread:.3f}")
    print(spec + "\n   " + "\n   ".join(out), flush=True)
