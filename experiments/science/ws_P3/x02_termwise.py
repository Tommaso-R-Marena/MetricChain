"""
P3 exploration 2: the term-by-term bound (termwise.TermBound with SAMPLED derivative suprema --
exploration only, not rigorous) against exact enumeration, orders 3 and 4, self and cross parts.

usage: python3 -B x02_termwise.py SEQ BB TAU
"""
import sys, itertools, time
import numpy as np
from p3core import GBModel
from mixdiff import mixed_max
from termwise import TermBound

seq, bb, tau = sys.argv[1], sys.argv[2], float(sys.argv[3])
t0 = time.time()
G = GBModel(seq, bb, tau=tau)
n = G.ns
shape = tuple(G.k)
st = G.product_states()
tot, sf, cr = G.energy(st, parts=True)
tot = tot.reshape(shape); sf = sf.reshape(shape); cr = cr.reshape(shape)
TB = TermBound(G)
print(f"{seq} on {bb}, tau {tau}: atoms {G.nat}, sites {n}, domain {list(shape)}; setup {time.time() - t0:.1f}s")
for order in (3, 4):
    if order > n:
        break
    rows = []
    t1 = time.time()
    for T in itertools.combinations(range(n), order):
        ex_t, ex_s, ex_c = mixed_max(tot, T), mixed_max(sf, T), mixed_max(cr, T)
        bs, bc = TB.self_bound(T), TB.cross_bound(T)
        rows.append((T, ex_t, ex_s, ex_c, bs, bc))
    a = np.array([r[1:] for r in rows])
    print(f"order {order} ({len(rows)} subsets, {time.time() - t1:.1f}s): sums over subsets: exact total {a[:, 0].sum():.4e}, exact self {a[:, 1].sum():.4e}, "
          f"exact cross {a[:, 2].sum():.4e} | bound self {a[:, 3].sum():.4e} (x{a[:, 3].sum() / a[:, 1].sum():.1f}), bound cross {a[:, 4].sum():.4e} (x{a[:, 4].sum() / a[:, 2].sum():.1f}); "
          f"bound total / exact total = {(a[:, 3].sum() + a[:, 4].sum()) / a[:, 0].sum():.1f}")
    for r in sorted(rows, key=lambda r: -r[1])[:5]:
        print(f"      T={r[0]}: exact total {r[1]:.3e} self {r[2]:.3e} cross {r[3]:.3e} | bound self {r[4]:.3e} (x{r[4] / max(r[2], 1e-300):.1f}) cross {r[5]:.3e} (x{r[5] / max(r[3], 1e-300):.1f}) "
              f"| (self+cross bound)/exact total = {(r[4] + r[5]) / r[1]:.1f}")
