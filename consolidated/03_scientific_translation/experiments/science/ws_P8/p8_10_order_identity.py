"""
P8 -- numerical check of step (a) of the proof of Theorem AH: P3's Proposition 1 for an ARBITRARY total order of the sites.

For a function F on a product grid, an anchor x0, a total order (a permutation: rank[i] = position of site i), every
state x and every m:
    F(x) - I_{m-1} F(x)  =  sum over T subset S(x), |T| = m, of  Delta_T F(z^{T,x}; x_T),
    z^{T,x}_i = x_i if rank[i] < min_{t in T} rank[t], and x0_i otherwise.
Checked on (a) random functions on a 3 x 2 x 4 x 3 x 2 grid, 20 random orders each, and (b) the GBn2 energy g of Lys4 on
the helix (16 464 states; from out/m1_K4_H_0.70.npz) with the 24 orders of its four sites.  Also checks the consequence
used in the proof: with the hosts of a term last, a host outside T is at its anchor state in z^{T,x} (all T, |T| >= 3).

usage: python3 -B p8_10_order_identity.py      -> logs/p8_10_order_identity.log
"""
import sys, os, itertools
import numpy as np
from p8lib import *

log = Log(os.path.join(HERE, "logs", "p8_10_order_identity.log"))
rng = np.random.default_rng(7)


def mixed_diff(F, T, z, y):
    """Delta_T F(z; y_T): sum over U subset T of (-1)^(|T|-|U|) F(y_U, z_-U)."""
    tot = 0.0
    for r in range(len(T) + 1):
        for U in itertools.combinations(T, r):
            x = list(z)
            for i in U:
                x[i] = y[i]
            tot += (-1.0) ** (len(T) - r) * F[tuple(x)]
    return tot


def check(F, x0, rank, mlist, states):
    n = F.ndim
    worst = 0.0; ncheck = 0
    Iint = {m: anchored_interp(F, x0, m - 1) for m in mlist}
    for x in states:
        S = [i for i in range(n) if x[i] != x0[i]]
        for m in mlist:
            lhs = F[tuple(x)] - Iint[m][tuple(x)]
            rhs = 0.0
            for T in itertools.combinations(S, m):
                rmin = min(rank[t] for t in T)
                z = [x[i] if rank[i] < rmin else x0[i] for i in range(n)]
                rhs += mixed_diff(F, T, z, x)
            worst = max(worst, abs(lhs - rhs)); ncheck += 1
    return worst, ncheck


# (a) random functions
shape = (3, 2, 4, 3, 2)
allst = list(itertools.product(*[range(k) for k in shape]))
worst = 0.0; nch = 0
for trial in range(3):
    F = rng.normal(size=shape)
    x0 = tuple(int(rng.integers(0, k)) for k in shape)
    for _ in range(20):
        rank = list(rng.permutation(len(shape)))
        w_, c_ = check(F, x0, rank, [1, 2, 3, 4, 5], allst)
        worst = max(worst, w_); nch += c_
log(f"(a) random functions on a {'x'.join(map(str, shape))} grid, 3 functions x 20 random orders, m = 1..5, every state: {nch} (state, order, m) checks, largest |lhs - rhs| = {worst:.1e}")
assert worst < 1e-10
# (b) the GBn2 energy of Lys4
Z = np.load(os.path.join(HERE, "out", "m1_K4_H_0.70.npz"))
shape = tuple(int(v) for v in Z["shape"]); x0 = tuple(int(v) for v in Z["anchor"])
g = Z["g"].reshape(shape)
states = [tuple(int(v) for v in np.unravel_index(i, shape)) for i in rng.choice(g.size, size=400, replace=False)]
worst = 0.0; nch = 0
for perm in itertools.permutations(range(4)):
    w_, c_ = check(g, x0, list(perm), [3, 4], states)
    worst = max(worst, w_); nch += c_
log(f"(b) GBn2 energy of Lys4 on the helix, all 24 orders of the four sites, m = 3, 4, 400 random states: {nch} checks, largest |lhs - rhs| = {worst:.1e} kcal/mol")
assert worst < 1e-8
# (c) hosts last => a host outside T is at its anchor in z^{T,x}
n = 7; bad = 0; cnt = 0
for hosts in [(2,), (0, 5), (3, 4), (6,), (1, 6)]:
    order = [i for i in range(n) if i not in hosts] + list(hosts)
    rank = [order.index(i) for i in range(n)]
    for m in (3, 4, 5):
        for T in itertools.combinations(range(n), m):
            rmin = min(rank[t] for t in T)
            for l in hosts:
                if l not in T:
                    cnt += 1
                    if rank[l] < rmin:                 # would mean z_l = x_l (not the anchor)
                        bad += 1
log(f"(c) hosts ordered last, 7 sites, 5 host sets, all T with |T| = 3, 4, 5: {cnt} (T, host outside T) cases, host NOT at its anchor in {bad}")
assert bad == 0
log.done()
