"""P3 exploration 3: where does the term-by-term cross bound come from?  Breakdown of the order-3
cross bound by number of blocks of the partition (1: h' * D_ijk, 2: h'' * D_ij D_k, 3: h''' D_i D_j D_k)
and by pair class, without the host combination (plain sums over group pairs at fixed host states,
maximised over host states afterwards per class).   usage: x03_breakdown.py SEQ BB TAU i j k"""
import sys, itertools
import numpy as np
from p3core import GBModel, KAPPA, KCAL
from termwise import TermBound, set_partitions

seq, bb, tau = sys.argv[1], sys.argv[2], float(sys.argv[3])
T = tuple(int(v) for v in sys.argv[4:7])
G = GBModel(seq, bb, tau=tau)
TB = TermBound(G)

def pair_parts(i1, i2, B):
    g1, g2 = TB.groups[i1], TB.groups[i2]
    coef, supH = TB._pair_data(i1, i2)
    d1, d2 = g1.delta_class, g2.delta_class
    def DB(block):
        p1 = np.ones(len(g1.atoms)); p2 = np.ones(len(g2.atoms))
        for i in block:
            p1 = p1 * d1[i]; p2 = p2 * d2[i]
        k = len(block)
        return (g1.supL[k] * p1)[:, None] + (g2.supL[k] * p2)[None, :]
    out = np.zeros(4)
    for part in set_partitions(B):
        term = supH[len(part)].copy()
        for block in part:
            term = term * DB(block)
        out[len(part)] += float((coef * term).sum()) / KCAL
    return out

print(f"{seq} {bb} tau {tau}, T = {T}")
ff = pair_parts(0, 0, T)
print("fixed-fixed pairs: by number of blocks 1,2,3:", ff[1:])
for l in range(G.ns):
    B = tuple(i for i in T if i != l)
    vals = np.array([pair_parts(0, TB.gid[(l, b)], B) + pair_parts(TB.gid[(l, b)], TB.gid[(l, b)], B) for b in range(G.k[l])])
    print(f"fixed-site{l} + site{l}-site{l} (free sites {B}): max over states by blocks:", vals.max(0)[1:], " in T" if l in T else "")
for l in range(G.ns):
    for l2 in range(l + 1, G.ns):
        B = tuple(i for i in T if i != l and i != l2)
        if not B:
            continue
        vals = np.array([pair_parts(TB.gid[(l, b)], TB.gid[(l2, b2)], B) for b in range(G.k[l]) for b2 in range(G.k[l2])])
        print(f"site{l}-site{l2} (free sites {B}): max over states by blocks:", vals.max(0)[1:])
