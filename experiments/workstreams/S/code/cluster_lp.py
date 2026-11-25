#!/usr/bin/env python3
"""Outer bounds for the limit profile set: the bond-cluster linear programme.

For ANY finite set S of lattice sites (hence for the site set of every walk, bridge or ring):
   e3  = number of occupied bonds,
   e8  = sum over ALL lattice sites m (occupied or not) of C(d(m), 2),  d(m) = number of occupied neighbours
         (two second neighbours have exactly one common neighbour: the lattice has girth 6),
   e11 = (1/2) sum over all lattice bonds (v,w) of the number of occupied gauche pairs (u_j, z_k), j != k,
         u_j = the three other neighbours of v, z_k = the three other neighbours of w, (u_j, z_j) trans
         (two sites at squared distance 11 are opposite corners of exactly one six-ring, hence joined by
         exactly two three-bond paths: the factor 1/2).
So (e3, e8, e11)/|S| is an average over the lattice bonds of functions of the occupation of the 8-site
cluster {v, w, u1,u2,u3, z1,z2,z3}.  Necessary conditions on the empirical distribution of cluster
configurations (after averaging over the lattice symmetries, which does not change the averages):
invariance under the 12 symmetries of the cluster, and symmetry of the 5-site star marginal (v; w,u1,u2,u3)
under all permutations of the four neighbours.  With mu = distribution / density:
   p3 = 2 mu(v w) - 1,   p8 = mu[(C(dv,2) + C(dw,2))/2] - 1,   p11 = mu[sum_{j != k} u_j z_k].
Option deg2: an occupied centre has at least two occupied neighbours (true for all but two sites of a
traceable set; the O(1/N) correction vanishes in the limit).

The LP maximum of c.(p3,p8,p11) is an upper bound for the support function of the limit set in direction c.
usage: cluster_lp.py [ndir] [deg2=1]
"""
import sys, itertools
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

IDX = {s: i for i, s in enumerate(itertools.product((0, 1), repeat=8))}
CFG = list(IDX.keys())           # (v, w, u1, u2, u3, z1, z2, z3)

def C2(d):
    return d * (d - 1) // 2

def build(deg2=True):
    n = len(CFG)
    f3 = np.zeros(n); f8 = np.zeros(n); f11 = np.zeros(n); fv = np.zeros(n)
    allowed = np.ones(n, dtype=bool)
    for i, s in enumerate(CFG):
        v, w, u, z = s[0], s[1], s[2:5], s[5:8]
        dv = w + sum(u); dw = v + sum(z)
        f3[i] = v * w
        f8[i] = (C2(dv) + C2(dw)) / 2
        f11[i] = sum(u[j] * z[k] for j in range(3) for k in range(3) if j != k)
        fv[i] = v
        if deg2 and ((v and dv < 2) or (w and dw < 2)):
            allowed[i] = False
    rows = []
    def eq(pairs):
        r = np.zeros(n)
        for i, c in pairs:
            r[i] += c
        if np.any(r != 0):
            rows.append(r)
    # cluster symmetries
    for s in CFG:
        v, w, u, z = s[0], s[1], s[2:5], s[5:8]
        t1 = (v, w, u[1], u[2], u[0], z[1], z[2], z[0])
        t2 = (v, w, u[1], u[0], u[2], z[1], z[0], z[2])
        t3 = (w, v) + z + u
        for t in (t1, t2, t3):
            if IDX[t] > IDX[s]:
                eq([(IDX[s], 1), (IDX[t], -1)])
    # star symmetry: swap w and u1 in the marginal on (v, w, u1, u2, u3)
    for (v, w, u1, u2, u3) in itertools.product((0, 1), repeat=5):
        if w == u1 or w < u1:
            continue
        pr = []
        for z in itertools.product((0, 1), repeat=3):
            pr.append((IDX[(v, w, u1, u2, u3) + z], 1))
            pr.append((IDX[(v, u1, w, u2, u3) + z], -1))
        eq(pr)
    Aeq = np.array(rows + [fv])
    beq = np.zeros(len(rows) + 1); beq[-1] = 1
    bounds = [(0, None) if a else (0, 0) for a in allowed]
    return f3, f8, f11, Aeq, beq, bounds

def support(c, data):
    f3, f8, f11, Aeq, beq, bounds = data
    obj = c[0] * 2 * f3 + c[1] * f8 + c[2] * f11
    res = linprog(-obj, A_eq=Aeq, b_eq=beq, bounds=bounds, method="highs")
    if res.status != 0:
        return None, None, res
    mu = res.x
    p = np.array([2 * f3 @ mu - 1, f8 @ mu - 1, f11 @ mu])
    return float(c @ p), p, res

def fib_sphere(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n); th = np.pi * (1 + 5 ** 0.5) * i
    return np.column_stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)])

def main():
    ndir = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    deg2 = (int(sys.argv[2]) if len(sys.argv) > 2 else 1) == 1
    data = build(deg2)
    print(f"# bond-cluster LP, deg2={deg2}: {data[3].shape[0]} equality constraints, "
          f"{sum(1 for b in data[5] if b[1] is None)} free variables")
    # directions: Fibonacci sphere in the scaled coordinates (9 p3, 4 p8, p11) plus the coordinate directions
    dirs = [np.array(d, float) for d in itertools.product((-1, 0, 1), repeat=3) if any(d)]
    for d in fib_sphere(ndir):
        dirs.append(d * np.array([9, 4, 1]))       # c.(p) = d.(9 p3, 4 p8, p11)
    pts = {}
    for c in dirs:
        val, p, res = support(c, data)
        if p is None:
            print("LP failed", c, res.message); continue
        key = tuple(np.round(p, 7))
        pts.setdefault(key, 0); pts[key] += 1
    P = np.array(sorted(pts))
    from scipy.spatial import ConvexHull
    hull = ConvexHull(P)
    print(f"# distinct optimal points: {len(P)}; hull vertices: {len(hull.vertices)}; volume (p-coordinates): {hull.volume:.6f}; "
          f"volume in weighted coordinates (x36): {36*hull.volume:.4f}")
    print("# vertices (p3, p8, p11) [as fractions where recognisable], number of directions that returned them")
    from fractions import Fraction
    for i in sorted(hull.vertices, key=lambda i: tuple(P[i])):
        fr = [str(Fraction(float(x)).limit_denominator(60)) for x in P[i]]
        print(f"  ({P[i][0]:9.6f}, {P[i][1]:9.6f}, {P[i][2]:9.6f})   ~ ({', '.join(fr)})   hits {pts[tuple(P[i])]}")
    np.save(sys.argv[3] if len(sys.argv) > 3 else "/dev/null", P[hull.vertices]) if len(sys.argv) > 3 else None

if __name__ == "__main__":
    main()
