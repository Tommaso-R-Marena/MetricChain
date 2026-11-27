#!/usr/bin/env python3
"""Coordinator spot checks of workstream S, part 3: the two cluster linear programmes, re-derived and re-solved with
an own formulation (floating point, scipy/HiGHS) -- a check of the *values* b of Theorems 4.2 and 4.2' and of the
polytopes K1, K2; the exact certificates are the workstream's (lp_exact.py, lp4_exact.py).

Cluster of a lattice bond (v,w): sites v, w, u1..u3 (other neighbours of v), z1..z3 (other neighbours of w),
(u_j, v, w, z_j) trans.  mu = (number of bonds with a given pattern, both orientations averaged, point group
averaged) / (2N).  Necessary conditions used:
 (1) mu(v occupied) = 1;
 (2) invariance under the 12 cluster symmetries (S3 on the index j, exchange of the ends);
 (3) the marginal on the star (v; w,u1,u2,u3) is invariant under the transposition w <-> u1 (with (2): under S4).
Site programme: an occupied centre has >= 2 occupied neighbours.  Path programme: chain bonds are marked; an
occupied centre has exactly two marked bonds."""
import itertools, sys
import numpy as np
from math import comb
from scipy.optimize import linprog
from scipy.spatial import ConvexHull, HalfspaceIntersection

V, W, U, Z = 0, 1, (2, 3, 4), (5, 6, 7)


def perm_sites(pj, swap):
    """site permutation for index permutation pj (tuple of 3) and optional exchange of the ends"""
    m = list(range(8))
    for j in range(3):
        m[U[j]] = U[pj[j]]
        m[Z[j]] = Z[pj[j]]
    if swap:
        m2 = list(m)
        m2[V], m2[W] = m[W], m[V]
        for j in range(3):
            m2[U[j]], m2[Z[j]] = m[Z[j]], m[U[j]]
        # composition: first index permutation, then exchange: site s -> exch(perm(s))
        ex = {V: W, W: V}
        for j in range(3):
            ex[U[j]] = Z[j]; ex[Z[j]] = U[j]
        m = [ex[m[s]] for s in range(8)]
    return m


SYMS = [perm_sites(pj, sw) for pj in itertools.permutations(range(3)) for sw in (False, True)]
BONDS = [(V, W)] + [(V, u) for u in U] + [(W, z) for z in Z]     # 7 bonds of the cluster


def F3(s): return 2 * s[V] * s[W]
def dv(s): return s[W] + sum(s[u] for u in U)
def dw(s): return s[V] + sum(s[z] for z in Z)
def F8(s): return (comb(dv(s), 2) + comb(dw(s), 2)) / 2
def F11(s): return sum(s[U[j]] * s[Z[k]] for j in range(3) for k in range(3) if j != k)


def site_program():
    pats = [s for s in itertools.product((0, 1), repeat=8) if any(s)]
    allowed = [s for s in pats if not ((s[V] and dv(s) < 2) or (s[W] and dw(s) < 2))]
    idx = {s: i for i, s in enumerate(allowed)}
    A, b = [], []
    row = np.zeros(len(allowed))
    for s in allowed:
        row[idx[s]] = s[V]
    A.append(row); b.append(1.0)
    for g in SYMS:
        for s in allowed:
            t = tuple(s[g[i]] for i in range(8))          # pattern pulled back by g
            if t != s:
                assert t in idx
                r = np.zeros(len(allowed)); r[idx[s]] = 1; r[idx[t]] = -1
                A.append(r); b.append(0.0)
    # star relation: for star patterns (sv; sw, su1, su2, su3) != 0, transposition w <-> u1
    for st in itertools.product((0, 1), repeat=5):
        if not any(st):
            continue
        st2 = (st[0], st[2], st[1], st[3], st[4])
        if st2 == st:
            continue
        r = np.zeros(len(allowed))
        for s in allowed:
            cur = (s[V], s[W], s[U[0]], s[U[1]], s[U[2]])
            if cur == st: r[idx[s]] += 1
            if cur == st2: r[idx[s]] -= 1
        A.append(r); b.append(0.0)
    f3 = np.array([F3(s) for s in allowed]); f8 = np.array([F8(s) for s in allowed]); f11 = np.array([F11(s) for s in allowed])
    return np.array(A), np.array(b), f3, f8, f11, None


def path_program():
    cfgs = []
    for s in itertools.product((0, 1), repeat=8):
        for marks in itertools.product((0, 1), repeat=7):
            ok = True
            for bi, (p, q) in enumerate(BONDS):
                if marks[bi] and not (s[p] and s[q]):
                    ok = False
            if not ok:
                continue
            mv = marks[0] + marks[1] + marks[2] + marks[3]
            mw = marks[0] + marks[4] + marks[5] + marks[6]
            if (s[V] and mv != 2) or (s[W] and mw != 2):
                continue
            if any(s):
                cfgs.append((s, marks))
    assert len(cfgs) == 339, len(cfgs)                     # 340 with the empty cluster
    idx = {c: i for i, c in enumerate(cfgs)}
    bond_index = {frozenset(bd): i for i, bd in enumerate(BONDS)}

    def act(g, c):
        s, marks = c
        # g maps site i -> g[i]; new pattern t with t[g[i]] = s[i]
        t = [0] * 8
        for i in range(8):
            t[g[i]] = s[i]
        m2 = [0] * 7
        for bi, (p, q) in enumerate(BONDS):
            m2[bond_index[frozenset((g[p], g[q]))]] = marks[bi]
        return (tuple(t), tuple(m2))

    A, b = [], []
    row = np.zeros(len(cfgs))
    for c in cfgs:
        row[idx[c]] = c[0][V]
    A.append(row); b.append(1.0)
    for g in SYMS:
        for c in cfgs:
            t = act(g, c)
            if t != c:
                assert t in idx
                r = np.zeros(len(cfgs)); r[idx[c]] = 1; r[idx[t]] = -1
                A.append(r); b.append(0.0)
    # star at v: occupancy of v and its four neighbours, marks on its four bonds; transposition w <-> u1
    def star(c):
        s, marks = c
        return (s[V], s[W], s[U[0]], s[U[1]], s[U[2]], marks[0], marks[1], marks[2], marks[3])
    stars = sorted(set(star(c) for c in cfgs))
    for st in stars:
        if not any(st[:5]):
            continue
        st2 = (st[0], st[2], st[1], st[3], st[4], st[6], st[5], st[7], st[8])
        if st2 == st:
            continue
        r = np.zeros(len(cfgs))
        for c in cfgs:
            cur = star(c)
            if cur == st: r[idx[c]] += 1
            if cur == st2: r[idx[c]] -= 1
        A.append(r); b.append(0.0)
    f3 = np.array([F3(c[0]) for c in cfgs]); f8 = np.array([F8(c[0]) for c in cfgs]); f11 = np.array([F11(c[0]) for c in cfgs])
    def G(c):
        s, m = c
        if not m[0]:
            return 0
        j = [i for i in range(3) if m[1 + i]]
        k = [i for i in range(3) if m[4 + i]]
        assert len(j) == 1 and len(k) == 1
        return 2 * (j[0] != k[0])
    fg = np.array([G(c) for c in cfgs])
    return np.array(A), np.array(b), f3, f8, f11, fg


def support(prog, c, cg=0.0):
    A, b, f3, f8, f11, fg = prog
    obj = c[0] * f3 + c[1] * f8 + c[2] * f11 + (cg * fg if fg is not None else 0)
    res = linprog(-obj, A_eq=A, b_eq=b, bounds=(0, None), method="highs")
    assert res.status == 0, res.message
    return -res.fun - c[0] - c[1]            # p = (e3/N - 1, e8/N - 1, e11/N)


ROWS1 = [((-1, 0, 0), 0), ((4, -1, 0), 0), ((6, -1, 0), 1), ((-2, 1, 0), 3), ((-1, 1, -1), 0), ((-1, 2, -1), 3),
         ((-4, 2, -1), 2), ((3, 4, -3), 5), ((6, -2, 1), 2), ((0, -1, 2), 7), ((-3, 0, 2), 9)]
VERT1 = [(0, 0, 0), (0, 0, 2), (0, 1, 4), (0, 2, 2), (0, 2, 4.5), (0, 3, 4), (0, 3, 4.5), (1 / 3, 3, 8 / 3), (1 / 3, 11 / 3, 4),
         (.5, 2, 1.5), (.5, 2, 3), (1, 5, 6)]
ROWS2 = [((-1, 0, 0), 0), ((4, -1, 0), 0), ((6, -1, 0), 1), ((-2, 1, 0), 3), ((-1, 1, -1), 0), ((-1, 2, -1), 3),
         ((-3, 2, -1), 2), ((-3, 4, -3), 2), ((3, 4, -3), 5), ((6, -2, 1), 2), ((0, -1, 2), 7), ((-3, 0, 2), 9)]
VERT2 = [(0, 0, 0), (0, 0, 2), (0, 1, 4), (0, 2, 2), (0, 2, 4.5), (0, 3, 4), (0, 3, 4.5), (.5, 2, 1.5), (.5, 2, 3), (.5, 3.5, 3.5),
         (.5, 4, 4.5), (1, 5, 6)]


def polytope(rows, verts, name):
    A = np.array([list(c) + [-b] for c, b in rows], float)
    hs = HalfspaceIntersection(A, np.array([0.3, 2.5, 3.0]))
    vs = np.unique(np.round(hs.intersections, 9), axis=0)
    want = np.unique(np.round(np.array(verts, float), 9), axis=0)
    assert vs.shape == want.shape and np.allclose(vs, want), (vs, want)
    vol = ConvexHull(vs).volume
    print(f"{name}: the rows cut out exactly the {len(verts)} listed vertices; volume = {vol:.4f} "
          f"({100 * vol / 30:.1f} % of the bulk box; {15 * vol:.2f} in u-coordinates)")
    return vs


def main():
    rng = np.random.default_rng(7)
    sp = site_program()
    print(f"site programme: {sp[0].shape[1]} allowed non-empty patterns, {sp[0].shape[0]} equality rows")
    for c, b in ROWS1:
        val = support(sp, c)
        assert abs(val - b) < 1e-7, (c, b, val)
    print("Theorem 4.2: LP optimum equals b for each of the eleven rows (|diff| < 1e-7)")
    v1 = polytope(ROWS1, VERT1, "K1")
    worst = 0
    for _ in range(400):
        c = rng.normal(size=3) * np.array([9, 4, 1])
        worst = max(worst, abs(support(sp, c) - max(c @ v for v in v1)))
    print(f"  support function of the LP set = support function of K1 in 400 random directions (max |diff| = {worst:.1e})")
    pp = path_program()
    print(f"path programme: {pp[0].shape[1]} non-empty configurations, {pp[0].shape[0]} equality rows")
    for c, b in ROWS2:
        val = support(pp, c)
        assert abs(val - b) < 1e-7, (c, b, val)
    print("Theorem 4.2'(i): LP optimum equals b for each of the twelve rows")
    v2 = polytope(ROWS2, VERT2, "K2")
    worst = 0
    for _ in range(400):
        c = rng.normal(size=3) * np.array([9, 4, 1])
        worst = max(worst, abs(support(pp, c) - max(c @ v for v in v2)))
    print(f"  support function of the path-LP set = support function of K2 in 400 random directions (max |diff| = {worst:.1e})")
    for c, b in [((-5, 0, 2), 8), ((0, -1, 2), 7), ((-4, 1, 1), 7)]:
        val = support(pp, c, cg=-1.0)
        assert abs(val - b) < 1e-7, (c, b, val)
    print("Theorem 4.2'(ii): max of 2p11-5p3-q, 2p11-p8-q, p11+p8-4p3-q over the path programme = 8, 7, 7")
    # gamma_LP at two points: min q subject to p fixed
    A, b, f3, f8, f11, fg = pp
    for p, want in [((0, 12 / 5, 22 / 5), 4 / 5), ((0, 18 / 7, 61 / 14), 5 / 7), ((1, 5, 6), 0.0), ((.5, 2, 1.5), 0.0)]:
        A2 = np.vstack([A, f3, f8, f11]); b2 = np.concatenate([b, [p[0] + 1, p[1] + 1, p[2]]])
        res = linprog(fg, A_eq=A2, b_eq=b2, bounds=(0, None), method="highs")
        assert res.status == 0 and abs(res.fun - want) < 1e-7, (p, res.status, res.fun)
        print(f"  gamma_LP{p} = {res.fun:.6f}")
    print("PART 3 OK")


if __name__ == "__main__":
    main()
