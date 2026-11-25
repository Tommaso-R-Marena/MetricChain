#!/usr/bin/env python3
"""Coordinator spot checks of workstream S, part 4: constructions and numbers (own code).
(a) rung-folded lamellae built from the description in Proposition 4.3: valid bridges; densities -> (1/2,2,3/2;0)
    (one row) and (1,5,6;0) (crystal) with a surface term N^(-1/3);
(b) hairpins t^a ggg t^b and the flip of the middle fold torsion: -15 <= D - 14 d <= -5 (Proposition 8.1);
(c) volume bounds of Proposition 7.1 (bulk box; K1; K2) and a greedy packing in the triangle T0 (Proposition 7.2);
(d) exact covering numbers at 15 and 21 beads with the cumulative norm and with the weighted norm of the brief."""
import sys, os, itertools
import numpy as np
from s_lat import *


# ---------- (a) lamellae
def rod_site(m, q, t):
    """rod (m,q): A_k = m(2,2,0)+q(2,0,2)+k(0,2,2), B_k = A_k+(1,1,1); position t = 2k (A_k) or 2k+1 (B_k)"""
    k, r = divmod(t, 2)
    x, y, z = 2 * m + 2 * q, 2 * m + 2 * k, 2 * q + 2 * k
    return (x + r, y + r, z + r)


def lamella(M, Q, ell):
    order = []
    for q in range(Q):
        order += [(m, q) for m in (range(M) if q % 2 == 0 else range(M - 1, -1, -1))]
    w = []
    up, t = True, -2                                    # start at A_{-1}
    for i, (m, q) in enumerate(order):
        if i == len(order) - 1:
            assert up
            t_end = 2 * ell + 1                         # B_ell
        else:
            m2, q2 = order[i + 1]
            plus = (m2 - m, q2 - q) in ((1, 0), (0, 1))
            k = ell - 1 if up else 0
            t_end = 2 * k + 1 if plus else 2 * k        # leave from B_k towards (m+1,q)/(m,q+1), from A_k towards (m-1,q)
        step = 1 if up else -1
        while True:
            w.append(rod_site(m, q, t))
            if t == t_end:
                break
            t += step
        if i < len(order) - 1:
            t = 2 * k if plus else 2 * k + 1            # arrive at A_k or B_k of the next rod
            up = not up
    return w


def part_a():
    print("(a) lamellae (own builder); N, (h3,h8,h11,g)/N, (1-h3/N) N^(1/3) or (1/2-h3/N) N^(1/2)")
    for (M, Q, ell) in [(9, 1, 16), (33, 1, 64), (65, 1, 128), (5, 5, 6), (9, 9, 10), (17, 17, 18), (25, 25, 26)]:
        w = lamella(M, Q, ell)
        assert valid_walk(w) and is_bridge(w)
        N = len(w); p = profile(w)
        assert p[3] <= 3 * (M * Q - 1)
        if Q == 1:
            extra = f"(1/2 - h3/N) N^(1/2) = {(0.5 - p[0] / N) * N ** 0.5:.3f}"
        else:
            extra = f"(1 - h3/N) N^(1/3) = {(1 - p[0] / N) * N ** (1 / 3):.3f};  (35 - ||N^x||_1/N) N^(1/3) = {(35 - (9*p[0]+4*p[1]+p[2]) / N) * N ** (1 / 3):.2f}"
        print(f"  M={M:2d} Q={Q:2d} ell={ell:3d}: N={N:6d}  ({p[0]/N:.4f}, {p[1]/N:.4f}, {p[2]/N:.4f}; {p[3]/N:.4f})  {extra}")


# ---------- (b) hairpins
def walk_from_bonds(bonds):
    p = (0, 0, 0)
    w = [p]
    for i in bonds:
        s = 1 if is_a(p) else -1
        p = (p[0] + s * BV[i][0], p[1] + s * BV[i][1], p[2] + s * BV[i][2])
        w.append(p)
    return w


def torsion_walk(states):
    """states: list of 't', 0, 1 (the two gauche choices in increasing order of the bond index); first bonds a_0, a_1"""
    b = [0, 1]
    for s in states:
        i, j = b[-2], b[-1]
        if s == 't':
            b.append(i)
        else:
            others = [k for k in range(4) if k not in (i, j)]
            b.append(others[s])
    return walk_from_bonds(b)


def part_b(amax=18):
    lo, hi = 10 ** 9, -10 ** 9
    cnt = 0
    for a in range(3, amax + 1):
        for b_ in range(3, amax + 1):
            best = None
            for fold in itertools.product((0, 1), repeat=3):
                w = torsion_walk(['t'] * a + list(fold) + ['t'] * b_)
                if not valid_walk(w):
                    continue
                p = profile(w)
                if best is None or p[0] > best[0][0]:
                    best = (p, fold)
            p, fold = best
            assert p[3] == 3
            w2 = torsion_walk(['t'] * a + [fold[0], 't', fold[2]] + ['t'] * b_)
            assert valid_walk(w2)
            p2 = profile(w2)
            D = cnorm((p[0] - p2[0], p[1] - p2[1], p[2] - p2[2]))
            d = min(a + 2, b_ + 2)
            if d >= 5:
                lo = min(lo, D - 14 * d); hi = max(hi, D - 14 * d)
                assert D <= 70 * (d + 3)
                cnt += 1
    print(f"(b) hairpins t^a g g g t^b, 3 <= a, b <= {amax}; flip of the middle fold torsion; {cnt} cases with d >= 5: "
          f"D - 14 d in [{lo}, {hi}]  (claimed [-15, -5]); D <= 70(d+3)")
    assert -15 <= lo and hi <= -5


# ---------- (c) volume bounds and a packing
def to_u(P):
    P = np.atleast_2d(np.array(P, float))
    return np.column_stack([5 * P[:, 0], 3 * (P[:, 0] + P[:, 1]), P[:, 0] + P[:, 1] + P[:, 2]])


E6 = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], float)
VERT2 = [(0, 0, 0), (0, 0, 2), (0, 1, 4), (0, 2, 2), (0, 2, 4.5), (0, 3, 4), (0, 3, 4.5), (.5, 2, 1.5), (.5, 2, 3), (.5, 3.5, 3.5),
         (.5, 4, 4.5), (1, 5, 6)]
VERT1 = [(0, 0, 0), (0, 0, 2), (0, 1, 4), (0, 2, 2), (0, 2, 4.5), (0, 3, 4), (0, 3, 4.5), (1 / 3, 3, 8 / 3), (1 / 3, 11 / 3, 4),
         (.5, 2, 1.5), (.5, 2, 3), (1, 5, 6)]
BOX = list(itertools.product((0, 1), (0, 5), (0, 6)))


def vol_bound(verts, r):
    from scipy.spatial import ConvexHull
    Vu = to_u(verts)
    rho = r / 2
    pts = np.vstack([Vu + rho * e for e in E6])
    return ConvexHull(pts).volume / (4 / 3 * rho ** 3)


def greedy_packing_T0(r, step):
    """points of T0 = conv{(0,0,0),(1/2,2,3/2),(1,5,6)} with pairwise cumulative-norm distance > 2r (gauche credit 0)"""
    v0, v1, v2 = to_u([(0, 0, 0)])[0], to_u([(.5, 2, 1.5)])[0], to_u([(1, 5, 6)])[0]
    n = int(35 / step) + 1
    cand = [v0 + (v1 - v0) * s / n + (v2 - v0) * t / n for s in range(n + 1) for t in range(n + 1 - s)]
    cand = np.array(cand)
    best = 0
    for key in (lambda c: (c[2], c[1], c[0]), lambda c: (c[0], c[1], c[2]), lambda c: (c[0] + c[1] + c[2],)):
        order = sorted(range(len(cand)), key=lambda i: key(cand[i]))
        chosen = []
        for i in order:
            c = cand[i]
            if all(np.abs(c - cand[j]).sum() > 2 * r + 1e-12 for j in chosen):
                chosen.append(i)
        best = max(best, len(chosen))
    return best


def part_c():
    print("(c) volume bounds  vol(X + B(r/2)) / vol B(r/2)  and a greedy packing in T0  [claimed: box, K1 (N->inf), K2; T0]")
    claims = {(1, .5): (26437, 3719, 3627, 50), (1, .25): (191833, 23936, 23272, 157), (.2, .5): (392, 94, 93, 7), (.2, .25): (2195, 401, 393, 14)}
    for (L, e1), cl in claims.items():
        r = e1 / L
        vb = [vol_bound(BOX, r), vol_bound(VERT1, r), vol_bound(VERT2, r)]
        pk = greedy_packing_T0(r, step=min(r / 4, 0.25))
        print(f"  L={L}, eps1={e1}: box {vb[0]:.1f} (claimed {cl[0]}), K1 {vb[1]:.1f} ({cl[1]}), K2 {vb[2]:.1f} ({cl[2]});"
              f"  own greedy packing in T0: {pk} (claimed lower bound {cl[3]})")
        for a, b in zip(vb, cl[:3]):
            assert abs(np.floor(a) - b) <= 1, (a, b)


# ---------- (d) exact covering numbers with the two norms
def cover_number(classes, N, L, eps, norm):
    from scipy.optimize import milp, LinearConstraint, Bounds
    from scipy.sparse import lil_matrix
    hs = list(classes.keys())
    n = len(hs)
    H = np.array(hs)
    g = np.array([classes[h] for h in hs])
    A = lil_matrix((n, n))
    for i in range(n):                                  # client i
        d = H - H[i]
        if norm == "c":
            dist = 5 * np.abs(d[:, 0]) + 3 * np.abs(d[:, 0] + d[:, 1]) + np.abs(d[:, 0] + d[:, 1] + d[:, 2])
        else:
            dist = 9 * np.abs(d[:, 0]) + 4 * np.abs(d[:, 1]) + np.abs(d[:, 2])
        A[i, np.nonzero(L * dist <= g[i] + eps + 1e-9)[0]] = 1
    res = milp(np.ones(n), constraints=LinearConstraint(A.tocsr(), lb=np.ones(n), ub=np.inf), integrality=np.ones(n),
               bounds=Bounds(0, 1), options={"time_limit": 300})
    return int(round(res.fun)), res.status


def load_classes(path):
    cl = {}
    for line in open(path):
        if line.startswith("#") or not line.strip():
            continue
        f = line.split()
        cl[(int(f[0]), int(f[1]), int(f[2]))] = int(f[4])
    return cl


def part_d(datadir):
    print("(d) exact covering numbers (set cover by MILP; clients = classes with their smallest gauche count, e = 1)")
    for n_t, claims in [(12, {(1, "c"): 8, (1, "w"): 10, (.2, "c"): 2}), (18, {(1, "c"): 11})]:
        N = n_t + 3
        cl = load_classes(os.path.join(datadir, f"dia_Sc12_n{n_t}.txt"))
        for (L, norm), want in claims.items():
            val, st = cover_number(cl, N, L, N / 2, norm)
            print(f"  N={N} beads, L={L}, eps=N/2, norm {norm}: N_cov = {val} (status {st}); claimed {want}")
            assert st == 0 and val == want


if __name__ == "__main__":
    part_a()
    part_b()
    part_c()
    if len(sys.argv) > 1:
        part_d(sys.argv[1])
    print("PART 4 OK")
