"""w10: the isoperimetric statement of Theorem W2(b)/(c) at the flat-histogram instance H, tested on families of
sets with EXACT finite-n sums (the upper-bound side: no sensitive set may be thinner than the formula allows).

Sets: unions of cells of a block structure (sites of each type split into two label blocks; a cell = the vector of
block types).  For such a set D everything is exact:
   * exits: s(x) = min_{y not in D} [ d(y,x) + n v(P_y) ] - n v(P_x)   by a multi-source Dijkstra search on the
     graph of cells (edges = change of one letter in one block, weight d_j(old letter, new letter); shortest
     paths are block-wise transport costs because d_j satisfies the triangle inequality);
   * Phi_H^+(D) = sum_{x in D} mu_H(x) e^{s(x)},  mu_H(D),  maxdens(D) = largest density in a joint-type class.
For every set:  e_D = ln Phi_H^+(D) / n,  theta_D = -ln maxdens(D) / n,  theta'_D = -ln mu_H(D) / n,  and the least
omega >= 0 with  theta_D <= R^(e_D - omega) + omega  (Theorem W2(b); likewise with theta'_D: W2(c)).
Families: neighbourhoods {Phi_C < r} of the optimal and of random centre classes; unions of two neighbourhoods;
half-spaces of the cell lattice; sub-level sets of random admissible functions; slices (one joint type).
Mutations (the test must have teeth): the same check with a wrong exponent function (single dips only for the
triangle site beyond its label switch; the zero residual; the worst binary cut).

usage: python3 w10_isoperimetry.py <chain> <n> [seed]
"""
import itertools
import math
import sys
import time

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra

from wlib import *
from wfin import compositions, lmult, round_counts, v_types
from wprimal import dip_profile
from wsites import chains

name = sys.argv[1] if len(sys.argv) > 1 else "path"
n = int(sys.argv[2]) if len(sys.argv) > 2 else 24
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
t00 = time.time()
rng = np.random.default_rng(seed)
ch = chains()[name]
E, a = ch.E(), ch.a()[0]
nvec = np.rint(ch.lam * n).astype(int)
assert nvec.sum() == n

# ---- exponent functions on a grid ---------------------------------------------------------------------------
NT = 2001
ts = np.linspace(0, 1, NT)


def tab(fun):
    return np.array([fun(t) if 0 < t < 1 else 0.0 for t in ts])


def Rfun(F):
    def R(e):
        obj = F - ts * e
        k = int(np.argmax(obj))
        val = obj[k]
        if 0 < k < NT - 1:
            y0, y1, y2 = obj[k - 1], obj[k], obj[k + 1]
            den = y0 - 2 * y1 + y2
            if den < 0:
                val += min(-(y2 - y0) ** 2 / (8 * den), 1e-6)
        return float(val)
    return R


Ftrue = tab(ch.Fstar)
variants = {"R^ (all vertices)": Rfun(Ftrue)}
variants["mutation: zero residual"] = Rfun(sum(l * tab(lambda t, s=s: s.F(np.zeros(s.q), t)) for l, s in zip(ch.lam, ch.sites)))
variants["mutation: single dips only"] = Rfun(sum(l * tab(lambda t, s=s: s.Fstar(t, cols=np.where(s.is_dist)[0])) for l, s in zip(ch.lam, ch.sites)))


def least_omega(R, e, theta):
    if theta <= R(e):
        return 0.0
    lo, hi = 0.0, 1.0
    while R(e - hi) + hi < theta:
        hi *= 2
    for it in range(50):
        mid = 0.5 * (lo + hi)
        if R(e - mid) + mid < theta:
            lo = mid
        else:
            hi = mid
    return hi


# ---- cells --------------------------------------------------------------------------------------------------
blocks = []                         # (site index j, block size, array of types K)
for j, s in enumerate(ch.sites):
    half = nvec[j] // 2
    for nu in (half, nvec[j] - half):
        blocks.append((j, int(nu), compositions(int(nu), s.q)))
sizes = [len(b[2]) for b in blocks]
ncell = int(np.prod(sizes))
strides = np.array([int(np.prod(sizes[k + 1:])) for k in range(len(sizes))], dtype=np.int64)
grids = np.meshgrid(*[np.arange(sz) for sz in sizes], indexing="ij")
cidx = [g.ravel() for g in grids]                           # block-type index of every cell, per block
lcount = np.zeros(ncell)
for k, (j, nu, K) in enumerate(blocks):
    lcount += lmult(K)[cidx[k]]
# joint types per site type, log pi, v
Pj, lTP, lpi_cell, nv_cell, typekey = [], [], np.zeros(ncell), np.zeros(ncell), np.zeros(ncell, dtype=np.int64)
for j, s in enumerate(ch.sites):
    ks = [k for k, b in enumerate(blocks) if b[0] == j]
    P = sum(blocks[k][2][cidx[k]] for k in ks)             # (ncell, q) counts
    Pj.append(P)
    lTP.append(lmult(P))
    lpi_cell += P @ np.log(s.pi)
    uniq, inv = np.unique(P, axis=0, return_inverse=True)
    nv_cell += nvec[j] * v_types(s, uniq / nvec[j])[inv.ravel()]
    typekey = typekey * (len(uniq) + 1) + inv.ravel()
lTPtot = sum(lTP)
lw = lcount + lpi_cell + nv_cell                            # ln [ pi(cell) e^{n v} ]
lZ = float(np.logaddexp.reduce(lw))
lmu = lw - lZ                                               # ln mu_H(cell)
dens_cell = np.exp(lcount - lTPtot)                         # density of the cell in its joint-type class
_, tkey = np.unique(typekey, return_inverse=True)

# graph of single-letter moves (edge from the cell with the old letter b to the cell with the new letter a, weight d(b, a))
rows, cols, wts = [], [], []
for k, (j, nu, K) in enumerate(blocks):
    s = ch.sites[j]
    lookup = {tuple(r): i for i, r in enumerate(K)}
    src, dst, ww = [], [], []
    for i, r in enumerate(K):
        for b in range(s.q):
            if r[b] == 0:
                continue
            for a_ in range(s.q):
                if a_ == b:
                    continue
                r2 = list(r)
                r2[b] -= 1
                r2[a_] += 1
                src.append(i)
                dst.append(lookup[tuple(r2)])
                ww.append(s.d[b, a_])
    src, dst, ww = np.array(src), np.array(dst), np.array(ww)
    # lift to cells: all cells, shifted in block k
    other = np.arange(ncell)[cidx[k] == 0]                  # representatives with block-k index 0
    base = (other[:, None] + src[None, :] * strides[k]).ravel()
    tgt = (other[:, None] + dst[None, :] * strides[k]).ravel()
    rows.append(base)
    cols.append(tgt)
    wts.append(np.tile(ww, len(other)))
rows, cols, wts = np.concatenate(rows), np.concatenate(cols), np.concatenate(wts)
print(f"=== w10 isoperimetry at H: chain {ch.name}, n = {n} ({nvec.tolist()}); {len(blocks)} blocks, {ncell} cells, {len(rows)} moves; E = {E:.5f}, a = {a:.5f}; setup {time.time()-t00:.1f} s ===")
zero_w = 1e-12                                              # csgraph drops explicit zeros: zero-cost moves get a tiny weight


def analyse(mask):
    """mask: boolean over cells (True = in D).  Returns (e_D, theta_D (maxdens), theta'_D (mu_H)) or None"""
    if mask.all() or not mask.any():
        return None
    out = np.nonzero(~mask)[0]
    off = nv_cell[out] - nv_cell[out].min()
    # super-source ncell -> outside cells with weight off (+tiny), then the move graph
    r = np.concatenate([rows, np.full(len(out), ncell)])
    c = np.concatenate([cols, out])
    w = np.concatenate([np.maximum(wts, zero_w), off + zero_w])
    G = coo_matrix((w, (r, c)), shape=(ncell + 1, ncell + 1)).tocsr()
    dist = dijkstra(G, directed=True, indices=ncell)[:ncell] + nv_cell[out].min()
    ins = np.nonzero(mask)[0]
    s = dist[ins] - nv_cell[ins]                            # slack out of D (>= 0)
    assert s.min() > -1e-6
    lphi = float(np.logaddexp.reduce(lmu[ins] + s))
    lmuD = float(np.logaddexp.reduce(lmu[ins]))
    d = np.bincount(tkey[ins], weights=dens_cell[ins])
    return lphi / n, -math.log(d.max()) / n, -lmuD / n


# cost to a centre class: transport per block
def Phi_C(centres):
    """sum over blocks of the transport cost from the cell to the centre types, plus n v(P_cell) - n v(P_C)"""
    tot = np.zeros(ncell)
    for k, (j, nu, K) in enumerate(blocks):
        s = ch.sites[j]
        c = np.max((K - centres[k][None, :]) @ s.V.T, axis=1)
        tot += c[cidx[k]]
    return tot


def cell_of(centres):
    i = 0
    for k, (j, nu, K) in enumerate(blocks):
        i += int(np.nonzero(np.all(K == centres[k][None, :], axis=1))[0][0]) * strides[k]
    return i


def opt_centres(e_frac):
    R, tt = ch.R(e_frac * E, return_t=True)
    prof, phis, Ms, gam = dip_profile(ch, tt)
    cs = []
    for j, s in enumerate(ch.sites):
        ks = [k for k, b in enumerate(blocks) if b[0] == j]
        order = np.argsort(-prof.P[j])[:2]                  # the two heaviest labels (two blocks per type)
        if len(order) < 2:
            order = np.array([order[0], order[0]])
        for kk, u in zip(ks, order):
            cs.append(round_counts(blocks[kk][1], prof.mu[j][u]))
    return cs


def random_centres():
    return [round_counts(nu, rng.dirichlet(rng.choice([0.4, 1.0, 3.0]) * np.ones(ch.sites[j].q))) for (j, nu, K) in blocks]


families = {}


def add(fam, mask):
    res = analyse(mask)
    if res is not None:
        families.setdefault(fam, []).append(res)


t0 = time.time()
# F1: neighbourhoods of the optimal centre classes
for ef in (0.0, 0.2, 0.5):
    cs = opt_centres(ef)
    ph = Phi_C(cs) + nv_cell - nv_cell[cell_of(cs)]
    for r in np.quantile(ph, [0.002, 0.01, 0.03, 0.1, 0.3]):
        add("F1 neighbourhoods {Phi_C < r} of the optimal centre classes", ph < r)
# F2: neighbourhoods of random centre classes
for it in range(8):
    cs = random_centres()
    ph = Phi_C(cs) + nv_cell - nv_cell[cell_of(cs)]
    for r in np.quantile(ph, [0.005, 0.05, 0.25]):
        add("F2 neighbourhoods of random centre classes", ph < r)
# F3: unions of two neighbourhoods
for it in range(8):
    c1, c2 = (opt_centres(0.0) if it % 2 == 0 else random_centres()), random_centres()
    p1 = Phi_C(c1) + nv_cell - nv_cell[cell_of(c1)]
    p2 = Phi_C(c2) + nv_cell - nv_cell[cell_of(c2)]
    for qq in (0.01, 0.1):
        add("F3 unions of two neighbourhoods", (p1 < np.quantile(p1, qq)) | (p2 < np.quantile(p2, qq)))
# F4: half-spaces of the cell lattice
for it in range(10):
    f = np.zeros(ncell)
    for k, (j, nu, K) in enumerate(blocks):
        f += (K @ rng.normal(size=ch.sites[j].q))[cidx[k]]
    for qq in (0.01, 0.1, 0.4):
        add("F4 half-spaces of the cell lattice", f < np.quantile(f, qq))
# F5: sub-level sets of random admissible functions min_c [offset_c + cost to centre c]
for it in range(8):
    f = np.full(ncell, np.inf)
    for c in range(int(rng.integers(2, 6))):
        f = np.minimum(f, Phi_C(random_centres()) + rng.uniform(0, 0.3 * n))
    for qq in (0.01, 0.1, 0.4):
        add("F5 sub-level sets of random admissible functions", f < np.quantile(f, qq))
# F6: slices: a neighbourhood restricted to one joint type (not a sub-level set of anything natural)
cs = opt_centres(0.0)
ph = Phi_C(cs) + nv_cell - nv_cell[cell_of(cs)]
for it in range(8):
    tk = int(rng.choice(tkey[ph < np.quantile(ph, 0.1)]))
    add("F6 neighbourhoods restricted to one joint type", (ph < np.quantile(ph, float(rng.choice([0.02, 0.1, 0.3])))) & (tkey == tk))

print(f"sets analysed in {time.time()-t0:.1f} s")
for label, R in variants.items():
    print(f"\n exponent function: {label}")
    for fam, res in families.items():
        om = [least_omega(R, e, th) for (e, th, thm) in res]
        omm = [least_omega(R, e, thm) for (e, th, thm) in res]
        k = int(np.argmax(om))
        print(f"   {fam:58s} {len(res):3d} sets: e_D in [{min(r_[0] for r_ in res):+.3f}, {max(r_[0] for r_ in res):+.3f}];"
              f" least omega (maxdens form): max {max(om):.5f} = {max(om)*n/math.log(n):.3f} ln n/n (at e_D = {res[k][0]:+.4f}, theta_D = {res[k][1]:.4f}, R(e_D) = {R(res[k][0]):.4f});"
              f" (mu_H form): max {max(omm):.5f} = {max(omm)*n/math.log(n):.3f} ln n/n")
print(f"time {time.time()-t00:.0f} s")
