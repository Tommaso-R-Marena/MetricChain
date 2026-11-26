"""
P3: certified remainder constants Gamma_m (m = 3..mmax) of the anchored expansion for a list of
instances; anchor from coordinate descent on E = f + g_GB started at the coordinate-descent
minimum of f.   usage: python3 -B x04_gamma.py mmax SEQ:BB:TAU [SEQ:BB:TAU ...]
"""
import sys, time, json, os
import numpy as np
from p3core import GBModel, KT300
from encl import EnvelopeSup
from gfbound import GFBound
from pwmodel import known_tables, icm_anchor

mmax = int(sys.argv[1])
out = {}
for spec in sys.argv[2:]:
    seq, bb, tau = spec.split(":")[0], spec.split(":")[1], float(spec.split(":")[2])
    t0 = time.time()
    G = GBModel(seq, bb, tau=tau)
    if min(G.k) == 0:
        print(f"{spec}: EMPTY domain"); continue
    c0, h, J = known_tables(G)
    x0, E0, nev = icm_anchor(G, c0, h, J)
    sup = EnvelopeSup(G)
    GF = GFBound(G, x0, sup, K=mmax)
    line = f"{spec}: atoms {G.nat}, sites {G.ns}, states {G.k[0]}..; anchor E = {E0:.3f} ({nev} evals); "
    res = {}
    for m in range(3, mmax + 1):
        if m > G.ns:
            break
        t1 = time.time()
        s, c = GF.total(m)
        res[m] = (s, c)
        line += f"Gamma_{m} = {s + c:.4e} (self {s:.2e}) [{(s + c) / KT300:.3g} kT, {time.time() - t1:.0f}s]; "
    out[spec] = res
    print(line + f" total {time.time() - t0:.0f}s", flush=True)
