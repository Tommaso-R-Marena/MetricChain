"""P8 probe: sizes of the instances named in the brief (atoms, sites, domain shape), charges by residue.
Run: python3 -B p8_00_probe.py > logs/p8_00_probe.log"""
import sys, os, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "ws_P3")))
import numpy as np
from p3core import GBModel
t0 = time.time()
for seq, bb, tau in [("K3", "H", 0.70), ("K4", "H", 0.70), ("K5", "H", 0.70), ("LKSE:4", "H", 0.60), ("LKSE:5", "H", 0.60), ("LKSE:6", "H", 0.60),
                     ("K3", "E", 0.70), ("K4", "E", 0.70), ("LKSE:4", "E", 0.60), ("LKSE:5", "E", 0.60), ("LKSE:6", "E", 0.60),
                     ("S5", "H", 0.70), ("L6", "H", 0.60)]:
    try:
        G = GBModel(seq, bb, tau=tau)
    except Exception as e:
        print(f"{seq}/{bb} tau {tau}: FAILED {type(e).__name__}: {e}", flush=True); continue
    S = int(np.prod([int(k) for k in G.k]))
    P = G.P
    resid = np.asarray(P.resid)
    qres = [round(float(G.q[resid == r].sum()), 4) for r in sorted(set(resid.tolist()))]
    print(f"{seq}/{bb} tau {tau}: seq {G.seq}, atoms {G.nat}, fixed {G.nf}, sites {G.ns}, k = {list(G.k)}, states {S}, moving atoms per site {[len(m) for m in G.mov]}, "
          f"charge by residue {qres}  [{time.time() - t0:.0f}s]", flush=True)
print("DONE", flush=True)
