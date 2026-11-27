"""
P3 test 2: (a) the generating-function sums of gfbound.GFBound equal the sum over subsets of the
per-subset bound (same conventions) -- a test of the combinatorics; (b) VALIDITY: for every subset T
of order 3 and 4 the certified anchored bound chat_T is >= the exact anchored-pair constant
c_T^anch (sup over all contexts of |Delta_T g(z; x0_T -> x_T)|) obtained by full enumeration;
(c) tightness by order.
usage: python3 -B t02_gf.py SEQ BB TAU [maxorder]
"""
import sys, itertools, time
import numpy as np
from p3core import GBModel
from encl import EnvelopeSup
from gfbound import GFBound

seq, bb, tau = sys.argv[1], sys.argv[2], float(sys.argv[3])
maxorder = int(sys.argv[4]) if len(sys.argv) > 4 else 4
t0 = time.time()
G = GBModel(seq, bb, tau=tau)
n = G.ns; shape = tuple(G.k)
st = G.product_states()
g = G.energy(st).reshape(shape)
c0, h, J = G.fb.site_tables("ff14SB")
f = np.full(shape, c0)
for i in range(n):
    sh = [1] * n; sh[i] = shape[i]
    f = f + h[i][G.dom[i]].reshape(sh)
for (i, j), tab in J.items():
    sh = [1] * n; sh[i] = shape[i]; sh[j] = shape[j]
    f = f + tab[np.ix_(G.dom[i], G.dom[j])].reshape(sh)
x0 = tuple(int(v) for v in np.unravel_index(np.argmin(f + g), shape))
sup = EnvelopeSup(G, verbose=True)
GF = GFBound(G, x0, sup)
print(f"{seq} {bb} tau {tau}: sites {n}, domain {list(shape)}, anchor {x0}; setup {time.time() - t0:.1f}s", flush=True)


def anch_const(g, x0, T):
    """exact sup over contexts and x_T of |Delta_T g(z; x0_T -> x_T)|."""
    D = g
    for i in T:
        ref = np.take(D, [x0[i]], axis=i)
        D = D - ref                       # axis i now holds the difference to the anchor state (zero at x0_i)
    return float(np.abs(D).max())


for m in range(3, maxorder + 1):
    if m > n:
        break
    t1 = time.time()
    gs, gc = GF.total(m)
    t2 = time.time()
    ss = sc = 0.0; ex = 0.0; worst = np.inf; viol = 0
    rows = []
    for T in itertools.combinations(range(n), m):
        bs, bc = GF.total(m, T)
        e = anch_const(g, x0, T)
        ss += bs; sc += bc; ex += e
        if bs + bc < e:
            viol += 1
        rows.append((T, e, bs, bc))
    print(f"order {m}: Gamma_m (generating function, {t2 - t1:.1f}s) self {gs:.6e} cross {gc:.6e} | sum over the {len(rows)} subsets ({time.time() - t2:.1f}s) "
          f"self {ss:.6e} cross {sc:.6e} | rel. diff {abs(gs - ss) / ss:.1e}, {abs(gc - sc) / sc:.1e}")
    print(f"         exact sum of anchored-pair constants {ex:.4e}; certified/exact = {(ss + sc) / ex:.1f} (self part alone {ss / ex:.2f}); violations of bound >= exact: {viol}")
    for T, e, bs, bc in sorted(rows, key=lambda r: -r[1])[:3]:
        print(f"         T={T}: exact {e:.3e}, certified self {bs:.3e} + cross {bc:.3e} = {bs + bc:.3e} (x{(bs + bc) / e:.0f})")
print(f"total {time.time() - t0:.1f}s")
