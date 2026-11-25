"""
P3 exploration 1 (numerics before theory): on small enumerated instances, how large are the
third-order constants of the SELF part and of the CROSS part of GBn2 separately, compared with the
total?  How much does c_ijk depend on the context (other sites)?  How large are fourth-order
constants?  Is the anchored third-order term one-signed?

usage: python3 -B x01_explore.py SEQ BB TAU
"""
import sys, itertools, time
import numpy as np
from p3core import GBModel, KT300
from mixdiff import *

seq, bb, tau = sys.argv[1], sys.argv[2], float(sys.argv[3])
t0 = time.time()
G = GBModel(seq, bb, tau=tau)
n = G.ns
shape = tuple(G.k)
size = int(np.prod(shape))
print(f"{seq} on {bb}, tau {tau}: atoms {G.nat}, sites {n}, domain {list(shape)} = {size} assignments")
st = G.product_states()
tot, sf, cr = G.energy(st, parts=True)
tot = tot.reshape(shape); sf = sf.reshape(shape); cr = cr.reshape(shape)
print(f"   enumerated in {time.time() - t0:.1f}s; ranges: total {np.ptp(tot):.3f}, self {np.ptp(sf):.3f}, cross {np.ptp(cr):.3f} kcal/mol")
# known part f for the anchor
c0, h, J = G.fb.site_tables("ff14SB")
f = np.full(shape, c0)
for i in range(n):
    sh = [1] * n; sh[i] = shape[i]
    f = f + h[i][G.dom[i]].reshape(sh)
for (i, j), tab in J.items():
    sh = [1] * n; sh[i] = shape[i]; sh[j] = shape[j]
    f = f + tab[np.ix_(G.dom[i], G.dom[j])].reshape(sh)
E = f + tot
x0 = tuple(int(v) for v in np.unravel_index(np.argmin(E), shape))
print(f"   anchor x0 = argmin E = {x0}")
for order in (1, 2, 3, 4, 5):
    if order > n:
        break
    rows = []
    for T in itertools.combinations(range(n), order):
        ct, cs, cc = mixed_max(tot, T), mixed_max(sf, T), mixed_max(cr, T)
        cref = mixed_at_context(tot, x0, T)
        d = anchored_term(tot, x0, T)
        rows.append((T, ct, cs, cc, cref, float(d.min()), float(d.max())))
    ct = np.array([r[1] for r in rows]); cs = np.array([r[2] for r in rows]); cc = np.array([r[3] for r in rows])
    cref = np.array([r[4] for r in rows]); dmin = np.array([r[5] for r in rows]); dmax = np.array([r[6] for r in rows])
    print(f"order {order}: {len(rows)} subsets;  total: max {ct.max():.4e} sum {ct.sum():.4e} | self: max {cs.max():.4e} sum {cs.sum():.4e} | "
          f"cross: max {cc.max():.4e} sum {cc.sum():.4e} | at anchor context: max {cref.max():.4e} sum {cref.sum():.4e} | "
          f"anchored term: min {dmin.min():.4e} max {dmax.max():.4e}; sum of negative parts {-np.minimum(dmin, 0).sum():.4e}, of positive parts {np.maximum(dmax, 0).sum():.4e}")
    if order == 3:
        k = int(np.argmax(ct))
        for r in sorted(rows, key=lambda r: -r[1])[:6]:
            print(f"      T={r[0]}: c_T total {r[1]:.4e} self {r[2]:.4e} cross {r[3]:.4e}  at anchor ctx {r[4]:.4e}  anchored d_T in [{r[5]:.4e}, {r[6]:.4e}]")
# remainder beyond the anchored interpolants
for order in (2, 3):
    if order >= n:
        break
    rem = tot - anchored_interp(tot, x0, order)
    print(f"remainder g - I_{order} g at the anchor: min {rem.min():.4e} max {rem.max():.4e} kcal/mol")
print(f"   total time {time.time() - t0:.1f}s")
