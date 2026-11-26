"""
P6: mean number of sites off the anchor under the exact Gibbs measure of E (enumerated instances; g from the cache
of p6_02_sandwich.py).  Supports the reading "gain of the pair form ~ 1 / (fraction of sites off the anchor)".
usage: python3 -B p6_08_occupancy.py
"""
import numpy as np, time
import p6lib as L
pw = L.pw; BETA = L.BETA
t0 = time.time()
for seq, bb, tau in (("V12", "E", 0.70), ("V12", "P2", 0.70), ("L12", "P2", 0.60), ("L16", "P2", 0.60), ("S6", "E", 0.70),
                     ("L8", "H", 0.60), ("L12", "H", 0.60), ("L16", "H", 0.60), ("S5", "H", 0.70), ("K4", "H", 0.70), ("LKSE:5", "H", 0.60)):
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau)
    st, g, src = L.enumerate_g(G, seq, bb, tau)
    E = pw.f_energy(st, c0, h, J) + g
    p = np.exp(-BETA * (E - E.min())); p /= p.sum()
    nch = (st != np.array(x0)[None]).sum(1)
    mean = float((p * nch).sum())
    print(f"{seq}/{bb} tau {tau}: {len(st)} states, n = {G.ns}; mean number of sites off the anchor under pi_E = {mean:.4f} (fraction p = {mean / G.ns:.4f}); "
          f"probability of the anchor {float(p[nch == 0].sum()):.4f}; of at most one changed site {float(p[nch <= 1].sum()):.4f}", flush=True)
print(f"DONE p6_08_occupancy [{time.time() - t0:.0f}s]")
