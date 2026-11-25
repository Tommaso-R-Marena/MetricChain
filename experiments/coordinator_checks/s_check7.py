#!/usr/bin/env python3
"""Coordinator spot checks of workstream S, part 7: own exact dual certificates for the path-cluster programme
(Proposition 11.72(c): the polytope K2 and the three gauche bounds).

Configurations: occupation pattern of the eight-site cluster (v, w; u1..u3; z1..z3) together with marks on its seven
bonds; a marked bond joins two occupied sites; an occupied centre has exactly two marked bonds (339 non-empty
configurations).  mu = (number of bonds with a given configuration, both orientations, point-group averaged)/(2N).
Used: mu(v occupied) = 1 (up to the two chain ends, mass O(1/N)); invariance under the 12 cluster symmetries;
invariance of the marginal on the star of v (occupancies of v and its four neighbours, marks on its four bonds)
under the transposition w <-> u1.

For each inequality  c3 p3 + c8 p8 + c11 p11 + cq q <= b  the script finds rational multipliers y_st of the star
relations and y0 = b + c3 + c8 with
    G(cfg) := c3*2[v][w] + c8*(C(d_v,2)+C(d_w,2))/2 + c11*sum_{j!=k} u_j z_k + cq*gauche(cfg) - sum y_st r_st(cfg) - y0 [v]
averaged over the 12 symmetries <= 0 on every configuration — verified with exact rational arithmetic.
(p3 = e3/N - 1, p8 = e8/N - 1, p11 = e11/N, q = gauche density = mu(gauche), gauche(cfg) = 2 if vw is marked and
the other marked bonds at v and at w have different indices, else 0.)"""
import itertools, sys
from fractions import Fraction as Fr
from math import comb
import numpy as np
from scipy.optimize import linprog

V, W, U, Z = 0, 1, (2, 3, 4), (5, 6, 7)
BONDS = [(V, W)] + [(V, u) for u in U] + [(W, z) for z in Z]
BIDX = {frozenset(b): i for i, b in enumerate(BONDS)}


def syms():
    out = []
    ex = {V: W, W: V}
    for j in range(3):
        ex[U[j]] = Z[j]; ex[Z[j]] = U[j]
    for pj in itertools.permutations(range(3)):
        m = list(range(8))
        for j in range(3):
            m[U[j]] = U[pj[j]]; m[Z[j]] = Z[pj[j]]
        out.append(m)
        out.append([ex[m[s]] for s in range(8)])
    return out


SYMS = syms()


def configs():
    out = []
    for s in itertools.product((0, 1), repeat=8):
        if not any(s):
            continue
        for marks in itertools.product((0, 1), repeat=7):
            if any(marks[i] and not (s[p] and s[q]) for i, (p, q) in enumerate(BONDS)):
                continue
            mv = marks[0] + marks[1] + marks[2] + marks[3]
            mw = marks[0] + marks[4] + marks[5] + marks[6]
            if (s[V] and mv != 2) or (s[W] and mw != 2) or (not s[V] and mv) or (not s[W] and mw):
                continue
            out.append((s, marks))
    return out


def act(g, c):
    s, marks = c
    t = [0] * 8
    for i in range(8):
        t[g[i]] = s[i]
    m2 = [0] * 7
    for bi, (p, q) in enumerate(BONDS):
        m2[BIDX[frozenset((g[p], g[q]))]] = marks[bi]
    return (tuple(t), tuple(m2))


def dv(s): return s[W] + s[2] + s[3] + s[4]
def dw(s): return s[V] + s[5] + s[6] + s[7]


def star(c):
    s, m = c
    return (s[V], s[W], s[2], s[3], s[4], m[0], m[1], m[2], m[3])


def gauche(c):
    s, m = c
    if not m[0]:
        return 0
    j = [i for i in range(3) if m[1 + i]][0]
    k = [i for i in range(3) if m[4 + i]][0]
    return 2 * (j != k)


def main():
    cfgs = configs()
    assert len(cfgs) == 339
    idx = {c: i for i, c in enumerate(cfgs)}
    orbit_imgs = [[idx[act(g, c)] for g in SYMS] for c in cfgs]
    stars = sorted(set(star(c) for c in cfgs))
    rels = []
    for st in stars:
        if not any(st[:5]):
            continue
        st2 = (st[0], st[2], st[1], st[3], st[4], st[6], st[5], st[7], st[8])
        if st2 > st:
            rels.append((st, st2))
    # raw functions as integer vectors over configurations
    f3 = [2 * c[0][V] * c[0][W] for c in cfgs]
    f8x2 = [comb(dv(c[0]), 2) + comb(dw(c[0]), 2) for c in cfgs]          # twice F8
    f11 = [sum(c[0][U[j]] * c[0][Z[k]] for j in range(3) for k in range(3) if j != k) for c in cfgs]
    fq = [gauche(c) for c in cfgs]
    fv = [c[0][V] for c in cfgs]
    R = [[(1 if star(c) == a else 0) - (1 if star(c) == b_ else 0) for c in cfgs] for (a, b_) in rels]

    def avg(vec):                         # exact average over the 12 symmetries
        return [Fr(sum(vec[j] for j in orbit_imgs[i]), 12) for i in range(len(cfgs))]
    A3, A8, A11, AQ, AV = avg(f3), [x / 2 for x in avg(f8x2)], avg(f11), avg(fq), avg(fv)
    AR = [avg(r) for r in R]
    ARf = np.array([[float(x) for x in r] for r in AR])
    AVf = np.array([float(x) for x in AV])

    def certify(c, cq, b):
        obj = [c[0] * A3[i] + c[1] * A8[i] + c[2] * A11[i] + cq * AQ[i] for i in range(len(cfgs))]
        objf = np.array([float(x) for x in obj])
        y0 = Fr(b) + c[0] + c[1]
        # find y with  obj - y.AR - y0*AV <= 0  (feasibility LP with a small l1 objective to get a clean vertex)
        m = len(AR)
        # variables y = yp - ym >= 0
        res = linprog(np.ones(2 * m), A_ub=np.hstack([-ARf.T, ARf.T]), b_ub=-(objf - float(y0) * AVf) ,
                      bounds=(0, None), method="highs-ds")
        if res.status != 0:
            return None
        yf = res.x[:m] - res.x[m:]
        for den in (1, 2, 3, 4, 6, 12, 24):
            y = [Fr(float(v)).limit_denominator(den) for v in yf]
            worst = max(obj[i] - sum(y[k] * AR[k][i] for k in range(m) if y[k]) - y0 * AV[i] for i in range(len(cfgs)))
            if worst <= 0:
                return den, sum(1 for v in y if v), worst
        return None

    rows = [((-1, 0, 0), 0, 0), ((4, -1, 0), 0, 0), ((6, -1, 0), 0, 1), ((-2, 1, 0), 0, 3), ((-1, 1, -1), 0, 0), ((-1, 2, -1), 0, 3),
            ((-3, 2, -1), 0, 2), ((-3, 4, -3), 0, 2), ((3, 4, -3), 0, 5), ((6, -2, 1), 0, 2), ((0, -1, 2), 0, 7), ((-3, 0, 2), 0, 9),
            ((-5, 0, 2), -1, 8), ((0, -1, 2), -1, 7), ((-4, 1, 1), -1, 7)]
    print(f"{len(cfgs)} configurations, {len(rels)} star relations (with marks)")
    ok = True
    for c, cq, b in rows:
        r = certify(c, cq, b)
        name = f"{c[0]} p3 + {c[1]} p8 + {c[2]} p11" + (f" + ({cq}) q" if cq else "")
        if r is None:
            print(f"  {name} <= {b}:  NO EXACT CERTIFICATE FOUND"); ok = False
        else:
            print(f"  {name} <= {b}:  exact certificate (multipliers with denominators <= {r[0]}, {r[1]} non-zero; largest reduced cost {r[2]})")
        # sharpening by 1/100 must be impossible (float LP infeasible)
        if certify(c, cq, Fr(b) - Fr(1, 100)) is not None:
            print("     !! the bound is not tight"); ok = False
    assert ok
    print("PART 7 OK: the twelve rows of K2 and the three gauche bounds are certified in exact arithmetic with own multipliers")


if __name__ == "__main__":
    main()
