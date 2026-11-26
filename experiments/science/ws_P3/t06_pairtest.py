"""
P3 test 6: a SHARP test of the pair formula of Theorem 3 (anchored mode).  All charges are set to
zero except those of two atoms, so that the cross part of g is a single pair term; the exact
anchored-pair constant of that single term (full enumeration) is compared with its certified bound
for every subset T of order 3 and 4.  With no sum over pairs there is no cancellation to lose, so the
ratio bound/exact should be O(1-10) and must never be < 1.  Likewise for the self term of one atom.
usage: python3 -B t06_pairtest.py SEQ BB TAU npairs
"""
import sys, itertools
import numpy as np
from p3core import GBModel
from encl import EnvelopeSup
from gfbound import GFBound

seq, bb, tau, npairs = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
G = GBModel(seq, bb, tau=tau)
n = G.ns; shape = tuple(G.k)
st = G.product_states()
sup = EnvelopeSup(G)
rng = np.random.default_rng(31)
host = np.zeros(G.nat, dtype=int) - 1
for l in range(n):
    host[G.mov[l]] = l
x0 = tuple(int(v) for v in np.unravel_index(np.argmin(G.energy(st)), shape))


def anch_const(g, T):
    D = g
    for i in T:
        D = D - np.take(D, [x0[i]], axis=i)
    return float(np.abs(D).max())


classes = {"fixed-fixed": [], "fixed-side": [], "side-side (same)": [], "side-side (different)": [], "self (fixed)": [], "self (side)": []}
ratios = {k: [] for k in classes}
viol = 0
q_orig = G.q.copy()
for trial in range(npairs):
    kind = list(classes)[trial % 6]
    fixed = np.flatnonzero(host < 0); side = np.flatnonzero(host >= 0)
    if kind == "fixed-fixed":
        p, q = rng.choice(fixed, 2, replace=False)
    elif kind == "fixed-side":
        p, q = rng.choice(fixed), rng.choice(side)
    elif kind == "side-side (same)":
        l = rng.integers(0, n); p, q = rng.choice(G.mov[l], 2, replace=False)
    elif kind == "side-side (different)":
        l, l2 = rng.choice(n, 2, replace=False); p, q = rng.choice(G.mov[l]), rng.choice(G.mov[l2])
    elif kind == "self (fixed)":
        p = q = rng.choice(fixed)
    else:
        p = q = rng.choice(side)
    qn = np.zeros(G.nat); qn[p] = 0.7; qn[q] = -0.6 if p != q else 0.7
    G.q = qn
    for attr in ("_iu", "_qq"):
        if hasattr(G, attr):
            delattr(G, attr)
    tot, sf, cr = G.energy(st, parts=True)
    part = (cr if p != q else sf).reshape(shape)
    GF = GFBound(G, x0, sup, K=4)
    for m in (3, 4):
        for T in itertools.combinations(range(n), m):
            e = anch_const(part, T)
            bs, bc = GF.total(m, T)
            b = bc if p != q else bs
            if e > 1e-12:
                ratios[kind].append(b / e)
                if b < e:
                    viol += 1
                    print("VIOLATION", kind, p, q, T, e, b)
G.q = q_orig
print(f"{seq} {bb} tau {tau}: single-term test, {npairs} random atoms/pairs, all subsets of order 3 and 4; violations: {viol}")
for k, v in ratios.items():
    if v:
        v = np.array(v)
        print(f"   {k:24s}: {len(v):4d} (pair, subset) cases; bound/exact: min {v.min():.2f}, median {np.median(v):.1f}, 90% {np.quantile(v, 0.9):.0f}, max {v.max():.0f}")
