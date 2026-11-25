#!/usr/bin/env python3
"""The path-cluster linear programme: outer bounds for the limit set of (h/N, #gauche/N) of ALL walks.

Cluster: a lattice bond (v,w) with the three other neighbours u1,u2,u3 of v and z1,z2,z3 of w ((u_j,z_j) trans).
A walk marks its N-1 chain bonds ("path bonds").  Configuration of a cluster: occupation of the 8 sites and the
marks of the 7 bonds vw, vu_j, wz_j.  Rules (true for every walk up to its two end beads):
   a marked bond joins occupied sites;  an occupied centre (v or w) has exactly two marked bonds.
Empirical cluster distribution of a walk (averaged over the lattice symmetries), divided by the density:
   mu >= 0,  mu(v occupied) = 1,  invariant under the 12 symmetries of the cluster,
   the marginal on the star of v (v, its four neighbours, its four bonds) is invariant under all permutations
   of the four neighbours.
Then   h3/N -> p3 = 2 mu(v w) - 1,     h8/N -> p8 = mu[(C(dv,2)+C(dw,2))/2] - 1,     h11/N -> p11 = mu[sum_{j!=k} u_j z_k],
       #gauche/N -> q = 2 mu[vw marked, the other marked bonds vu_j and wz_k have j != k].
The LP maximum of c.(p3,p8,p11,q) bounds the support function of the limit set of all walks from above.

usage: cluster_lp4.py NDIR3 NDIR4 OUT_PREFIX
"""
import sys, itertools
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

def C2(d):
    return d * (d - 1) // 2

def configs():
    out = []
    pairs4 = list(itertools.combinations(range(4), 2))       # bond slots at a centre: 0 = vw, 1..3 = outer j
    for v in (0, 1):
        for w in (0, 1):
            mv_opts = pairs4 if v else [()]
            mw_opts = pairs4 if w else [()]
            for mv in mv_opts:
                for mw in mw_opts:
                    cv = 0 in mv; cw = 0 in mw
                    if cv != cw:            # the central bond is marked from both ends or from neither
                        continue
                    if cv and not (v and w):
                        continue
                    for u in itertools.product((0, 1), repeat=3):
                        if any((j + 1) in mv and not u[j] for j in range(3)): continue
                        for z in itertools.product((0, 1), repeat=3):
                            if any((j + 1) in mw and not z[j] for j in range(3)): continue
                            out.append((v, w, u, z, tuple(sorted(mv)), tuple(sorted(mw))))
    return out

def perm_cfg(c, perm):
    v, w, u, z, mv, mw = c
    inv = {perm[i] + 1: i + 1 for i in range(3)}; inv[0] = 0     # new slot of old slot
    uu = tuple(u[perm[i]] for i in range(3)); zz = tuple(z[perm[i]] for i in range(3))
    # new position i holds old index perm[i]; an old mark on slot s moves to the position i with perm[i]+1 == s
    pos = {perm[i] + 1: i + 1 for i in range(3)}; pos[0] = 0
    return (v, w, uu, zz, tuple(sorted(pos[s] for s in mv)), tuple(sorted(pos[s] for s in mw)))

def inv_cfg(c):
    v, w, u, z, mv, mw = c
    return (w, v, z, u, mw, mv)

def build():
    CF = configs()
    IDX = {c: i for i, c in enumerate(CF)}
    n = len(CF)
    f3 = np.zeros(n); f8 = np.zeros(n); f11 = np.zeros(n); fg = np.zeros(n); fv = np.zeros(n)
    for i, (v, w, u, z, mv, mw) in enumerate(CF):
        dv = w + sum(u); dw = v + sum(z)
        f3[i] = v * w; f8[i] = (C2(dv) + C2(dw)) / 2
        f11[i] = sum(u[j] * z[k] for j in range(3) for k in range(3) if j != k)
        fv[i] = v
        if 0 in mv:
            j = [s for s in mv if s != 0][0]; k = [s for s in mw if s != 0][0]
            fg[i] = 1.0 if j != k else 0.0
    rows, cols, vals = [], [], []
    nr = 0
    def add_row(d):
        nonlocal nr
        d = {k: v for k, v in d.items() if v != 0}
        if not d: return
        for k, v in d.items():
            rows.append(nr); cols.append(k); vals.append(v)
        nr += 1
    # symmetries
    gens = [lambda c: perm_cfg(c, (1, 2, 0)), lambda c: perm_cfg(c, (1, 0, 2)), inv_cfg]
    for c in CF:
        for g in gens:
            t = g(c)
            if IDX[t] > IDX[c]:
                add_row({IDX[c]: 1, IDX[t]: -1})
    # star symmetry: swap the neighbour w (slot 0) with u1 (slot 1) in the marginal on (v, w, u, mv)
    star = {}
    for i, (v, w, u, z, mv, mw) in enumerate(CF):
        star.setdefault((v, w, u, mv), []).append(i)
    done = set()
    for key in star:
        v, w, u, mv = key
        sw = {0: 1, 1: 0, 2: 2, 3: 3}
        key2 = (v, u[0], (w, u[1], u[2]), tuple(sorted(sw[s] for s in mv)))
        if key2 == key or (key2, key) in done: continue
        done.add((key, key2))
        d = {}
        for i in star[key]: d[i] = d.get(i, 0) + 1
        for i in star.get(key2, []): d[i] = d.get(i, 0) - 1
        add_row(d)
    # normalisation
    for i in range(n):
        if fv[i]:
            rows.append(nr); cols.append(i); vals.append(1.0)
    nr += 1
    Aeq = csr_matrix((vals, (rows, cols)), shape=(nr, n))
    beq = np.zeros(nr); beq[-1] = 1
    return CF, f3, f8, f11, fg, Aeq, beq

def fib_sphere(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n); th = np.pi * (1 + 5 ** 0.5) * i
    return np.column_stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)])

def main():
    nd3 = int(sys.argv[1]); nd4 = int(sys.argv[2]); prefix = sys.argv[3]
    CF, f3, f8, f11, fg, Aeq, beq = build()
    print(f"# path-cluster LP: {len(CF)} configurations, {Aeq.shape[0]} equality constraints")
    def solve(c):
        obj = c[0] * 2 * f3 + c[1] * f8 + c[2] * f11 + c[3] * 2 * fg
        res = linprog(-obj, A_eq=Aeq, b_eq=beq, bounds=(0, None), method="highs")
        assert res.status == 0, res.message
        mu = res.x
        return np.array([2 * f3 @ mu - 1, f8 @ mu - 1, f11 @ mu, 2 * fg @ mu])
    # 3D polytope (profile part): directions with c_g = 0
    pts3 = {}
    dirs = [np.array(d + (0,), float) for d in itertools.product((-1, 0, 1), repeat=3) if any(d)]
    for d in fib_sphere(nd3):
        dirs.append(np.array([9 * d[0], 4 * d[1], d[2], 0.0]))
    for c in dirs:
        p = solve(c)
        pts3.setdefault(tuple(np.round(p[:3], 7)), []).append(p[3])
    P3 = np.array(sorted(pts3))
    from scipy.spatial import ConvexHull
    from fractions import Fraction
    h3 = ConvexHull(P3)
    print(f"# profile polytope of the path-cluster LP: {len(h3.vertices)} vertices, volume {h3.volume:.6f} (p-coordinates), x36 = {36*h3.volume:.4f}")
    for i in sorted(h3.vertices, key=lambda i: tuple(P3[i])):
        fr = [str(Fraction(float(x)).limit_denominator(120)) for x in P3[i]]
        print(f"  ({', '.join(f'{s:>7}' for s in fr)})")
    np.save(prefix + "_vertices3.npy", P3[h3.vertices])
    # gauche: smallest gauche density compatible with the LP at the 3D vertices and at sampled points:
    #   gamma_LP(p) = min q over the LP measures with profile p  (a lower bound for the true gamma(p))
    A2 = np.vstack([Aeq.toarray(), 2 * f3, f8, f11])
    def gamma_lp(p):
        b2 = np.concatenate([beq, [p[0] + 1, p[1] + 1, p[2]]])
        res = linprog(2 * fg, A_eq=A2, b_eq=b2, bounds=(0, None), method="highs")
        return res.fun if res.status == 0 else None
    print("# smallest gauche density allowed by the LP at its profile vertices (lower bound for gamma there):")
    for i in sorted(h3.vertices, key=lambda i: tuple(P3[i])):
        g = gamma_lp(P3[i])
        print(f"  {np.round(P3[i], 5)}  gamma_LP = {g if g is None else round(g, 6)}")
    # 4D support points
    rng = np.random.default_rng(3)
    pts4 = set()
    for _ in range(nd4):
        c = rng.normal(size=4) * np.array([9, 4, 1, 1])
        pts4.add(tuple(np.round(solve(c), 7)))
    P4 = np.array(sorted(pts4))
    np.save(prefix + "_vertices4.npy", P4)
    try:
        h4 = ConvexHull(P4)
        print(f"# 4D: {len(P4)} distinct support points, hull vertices {len(h4.vertices)}, 4-volume {h4.volume:.5f}")
    except Exception as ex:
        print("# 4D hull failed:", ex)

if __name__ == "__main__":
    main()
