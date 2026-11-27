#!/usr/bin/env python3
"""G5: chain-length independent upper bounds and packing lower bounds for the limiting covering numbers.

Profile norm (L1 distance of cumulative profiles): for densities p = (p3, p8, p11) put
     u(p) = (5 p3, 3 (p3 + p8), p3 + p8 + p11);     ||p - p'||_c = |u - u'|_1.
Covering problem at accuracy eps1 (e = 1): centre a covers the client (p, g) iff  L |u(a) - u(p)|_1 <= g + eps1.

Upper bounds (valid for every N up to the O(1/N) enlargement of the outer set; gauche credit ignored):
   N_cov <= Pack(X, r) <= N_ext(X, r/2),   r = eps1/L,   X = an outer set for the profile densities,
   (i)  volumetric:  Pack(X, r) <= vol(X + B(r/2)) / vol(B(r/2)),  B = l1 ball in u-coordinates,
   (ii) bcc lattice of octahedra of radius r/2 (l1 covering radius of a(Z^3 u Z^3+1/2) is 3a/4): the number of
        lattice points in X + B(r/2) for the best of a set of translates.
Lower bounds: a set of clients (p_i, g_i) of the limit set with  L |u_i - u_j|_1 > g_i + g_j + 2 eps1  pairwise
   (no centre covers two of them), found by a lattice start and greedy augmentation; verified in the script.

usage: g5_bounds.py OUT_DIR
"""
import sys, itertools
import numpy as np
from scipy.spatial import ConvexHull

def to_u(P):
    P = np.atleast_2d(P)
    return np.column_stack([5 * P[:, 0], 3 * (P[:, 0] + P[:, 1]), P[:, 0] + P[:, 1] + P[:, 2]])

E = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], float)

def minkowski(Vu, rho):
    """vertices of conv(V) + l1-ball(rho)"""
    return np.vstack([Vu + rho * e for e in E])

def vol_bound(Vu, r):
    rho = r / 2
    h = ConvexHull(minkowski(Vu, rho))
    return h.volume / (4 / 3 * rho ** 3)

def bcc_count(Vu, r, ntrans=30, seed=0):
    rho = r / 2
    a = 4 * rho / 3
    h = ConvexHull(minkowski(Vu, rho))
    A_, b_ = h.equations[:, :3], h.equations[:, 3]
    lo = h.points.min(axis=0); hi = h.points.max(axis=0)
    rng = np.random.default_rng(seed)
    best = None
    for t in range(ntrans):
        off = rng.random(3) * a
        cnt = 0
        for half in (0.0, 0.5):
            ax = [np.arange(np.floor((lo[k] - off[k]) / a) - 1, np.ceil((hi[k] - off[k]) / a) + 2) * a + off[k] + half * a for k in range(3)]
            G = np.array(np.meshgrid(*ax, indexing="ij")).reshape(3, -1).T
            cnt += int(((G @ A_.T + b_) <= 1e-9).all(axis=1).sum())
        best = cnt if best is None else min(best, cnt)
    return best

def inside(h, X, tol=1e-9):
    return ((X @ h.equations[:, :-1].T + h.equations[:, -1]) <= tol).all(axis=1)

def grid_in_polytope(Vu, step):
    """grid points of the convex hull of Vu (3D body, or a flat polygon given by its vertices)"""
    try:
        h = ConvexHull(Vu)
        lo = Vu.min(axis=0); hi = Vu.max(axis=0)
        ax = [np.arange(lo[k], hi[k] + step, step) for k in range(3)]
        G = np.array(np.meshgrid(*ax, indexing="ij")).reshape(3, -1).T
        return G[inside(h, G)]
    except Exception:
        # degenerate (planar): barycentric grid on a fan triangulation
        pts = []
        v0 = Vu[0]
        for i in range(1, len(Vu) - 1):
            a, b = Vu[i] - v0, Vu[i + 1] - v0
            n = int(max(np.abs(a).sum(), np.abs(b).sum()) / step) + 1
            for s in range(n + 1):
                for t in range(n + 1 - s):
                    pts.append(v0 + a * s / n + b * t / n)
        return np.array(pts)

def packing(Cu, Cg, L, eps1, tries=6, seed=0):
    """greedy packing among candidate clients (u, g): pairwise L|u_i-u_j|_1 > g_i + g_j + 2 eps1"""
    rng = np.random.default_rng(seed)
    best = []
    n = len(Cu)
    for t in range(tries):
        if t == 0:
            order = np.lexsort((Cu[:, 2], Cu[:, 1], Cu[:, 0]))
        elif t == 1:
            order = np.argsort(Cu.sum(axis=1) + 1e-3 * Cg)
        elif t == 2:
            order = np.argsort(Cg + 1e-6 * Cu.sum(axis=1))          # small gauche credit first
        else:
            w = rng.normal(size=3)
            order = np.argsort(Cu @ w + 5 * Cg)
        alive = np.ones(n, bool)
        chosen = []
        for i in order:
            if not alive[i]: continue
            chosen.append(i)
            d = np.abs(Cu - Cu[i]).sum(axis=1)
            alive &= (L * d > Cg + Cg[i] + 2 * eps1 + 1e-9)
        if len(chosen) > len(best): best = chosen
    # verification
    B = np.array(best)
    D = np.abs(Cu[B][:, None, :] - Cu[B][None, :, :]).sum(axis=2)
    R = Cg[B][:, None] + Cg[B][None, :] + 2 * eps1
    ok = (L * D > R)[~np.eye(len(B), dtype=bool)].all() if len(B) > 1 else True
    assert ok
    return len(best)

def main():
    out = sys.argv[1]
    box = np.array(list(itertools.product((0, 1), (0, 5), (0, 6))), float)
    lp1 = np.load(f"{out}/lp_vertices_deg2.npy")
    lp4 = np.load(f"{out}/lp4_vertices3.npy")
    T0 = np.array([[0, 0, 0], [0.5, 2, 1.5], [1, 5, 6]], float)
    rod = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 1], [0, 1, 3], [0, 3, 4], [0.5, 2, 1.5], [0.5, 2, 2.5], [0.5, 4, 4.5], [1, 5, 6]], float)
    print("# volumes in u-coordinates (= 15 x volume in p):  bulk box %.1f,  site-cluster LP %.2f,  path-cluster LP %.2f,  rod hull (K<=12) %.2f"
          % (ConvexHull(to_u(box)).volume, ConvexHull(to_u(lp1)).volume, ConvexHull(to_u(lp4)).volume, ConvexHull(to_u(rod)).volume))
    cases = [(1.0, 0.5), (1.0, 0.25), (0.2, 0.5), (0.2, 0.25)]
    print("\n# UPPER bounds for N^P_cov(eps1 N) (limit N -> infinity of the outer sets; gauche credit ignored)")
    print("#  L    eps1 |  r=eps1/L | bulk box: volumetric   bcc cover | site-cluster LP [proved]: volumetric   bcc cover | path-cluster LP [numerical]: volumetric  bcc cover")
    for L, e1 in cases:
        r = e1 / L
        row = f"  {L:4.2f} {e1:5.2f} | {r:8.3f} |"
        for V in (box, lp1, lp4):
            Vu = to_u(V)
            row += f"   {vol_bound(Vu, r):12.0f} {bcc_count(Vu, r):10d}    |"
        print(row)
    print("\n# LOWER bounds for lim inf N^P_cov(eps1 N): packings of zero-gauche clients")
    print("#  L    eps1 | separation 2 eps1/L | segment rod-crystal | triangle T0 [proved] | rod hull, 9 vertices [sketch]")
    for L, e1 in cases:
        s = 2 * e1 / L
        seg = int(np.ceil(35 / s - 1e-12))          # points 0, d, 2d, ... with spacing d > s on a segment of l1 length 35
        seg = int(np.floor(35 / s - 1e-9)) + 1 if 35 / s != int(35 / s) else int(35 / s)   # strict separation
        res = []
        for V in (T0, rod):
            Vu = to_u(V)
            step = min(s / 6, 0.5)
            C = grid_in_polytope(Vu, step)
            res.append(packing(C, np.zeros(len(C)), L, e1))
        print(f"  {L:4.2f} {e1:5.2f} | {s:8.3f}            | {seg:8d}            | {res[0]:8d}             | {res[1]:8d}")

if __name__ == "__main__":
    main()
