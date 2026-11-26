"""P8 exploration: closed-form Gamma_m of P3 against the anchored-hosts closed form (type X -> A), 12-residue helices.
usage: python3 -B x02_ah_probe.py SEQ BB TAU [orders...]"""
import sys, time
import numpy as np
from p8lib import *
from p8sr import AHBound
sys.path.insert(0, os.path.join(SCI, "ws_P3"))
import pwmodel as pw
seq, bb, tau = sys.argv[1], sys.argv[2], float(sys.argv[3])
orders = [int(v) for v in sys.argv[4:]] or [4, 5, 6]
t0 = time.time()
G = GBModel(seq, bb, tau=tau)
c0, h, J = pw.known_tables(G)
x0, E0, nev = pw.icm_anchor(G, c0, h, J)
print(f"{seq}/{bb} tau {tau}: {G.nat} atoms, {G.ns} sites, k = {list(G.k)}; ICM anchor {tuple(int(v) for v in x0)}, E0 = {E0:.6f} [{time.time() - t0:.0f}s]", flush=True)
GF = AHBound(G, x0, EnvelopeSup(G), K=max(orders))
for m in orders:
    t1 = time.time()
    a = GF.total(m); b = GF.total_ah(m)
    print(f"  m = {m}: P3 Gamma = {sum(a):.5g} kcal/mol = {sum(a) * BETA:.5g} kT (self {a[0]:.3g});  anchored hosts: {sum(b):.5g} = {sum(b) * BETA:.5g} kT (self {b[0]:.3g});  ratio {sum(a) / sum(b):.2f}  [{time.time() - t1:.0f}s]", flush=True)
print("DONE")
