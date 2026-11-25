#!/usr/bin/env python3
"""Assistant B — the proved inner volume (N2 of SCI-REV-0002), recomputed in EXACT rational arithmetic.

P = profile densities of the 4 exact points and of the 10 bridges verified by verify_witness.py.
C = conv(P); delta = max_i 168/(N_i + 3).  Claim: vol(K) >= vol(C eroded by delta in ||.||_c).
 (argument, re-derived in NOTES: each measured p_i has p_i* in K with ||p_i* - p_i||_c <= delta, so
  h_C <= h_{conv p*} + delta h_B, and x + delta B in C implies x in conv{p_i*} subset K.)

Steps, all in Fractions:
 1. candidate facets of C from Qhull (floating point, only to propose triangles);
 2. for every triangle the exact plane n.x = b through its three points, oriented outwards; exact check that all
    14 points satisfy n.x <= b (supporting plane);
 3. completeness of the facet list: exact vertex enumeration of H = {n_f.x <= b_f}: every vertex of H is a point of P
    (then H = conv(vertices) subset C subset H);
 4. eroded polytope E = {n_f.x <= b_f - delta*hB(n_f)}, hB(n) = max_k |(U^{-T} n)_k| = dual norm of ||x||_c = |Ux|_1;
    exact vertex enumeration; exact volume by a fan of tetrahedra from an interior point over each facet polygon;
 5. the same with vertex-wise radii is NOT done (the reviewer uses the uniform delta; so do I).
Also prints the volume of the hull, of the exact points only, and floats for comparison with the reviewer's 1.6317 / 1.5632.
"""
import os, sys, json, itertools
from fractions import Fraction as Fr
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
import numpy as np
from scipy.spatial import ConvexHull


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def det3(a, b, c):
    return dot(a, cross(b, c))


def solve3(n1, n2, n3, b1, b2, b3):
    D = det3(n1, n2, n3)
    if D == 0:
        return None
    # Cramer
    x = det3((b1, n1[1], n1[2]), (b2, n2[1], n2[2]), (b3, n3[1], n3[2])) / D
    y = det3((n1[0], b1, n1[2]), (n2[0], b2, n2[2]), (n3[0], b3, n3[2])) / D
    z = det3((n1[0], n1[1], b1), (n2[0], n2[1], b2), (n3[0], n3[1], b3)) / D
    return (x, y, z)


def planes_of_hull(P):
    """exact outward planes (n, b), deduplicated up to positive scaling, each verified to support P"""
    hull = ConvexHull(np.array([[float(c) for c in p] for p in P]))
    cen = tuple(sum(p[k] for p in P) / len(P) for k in range(3))
    planes = {}
    for tri in hull.simplices:
        a, b, c = (P[i] for i in tri)
        n = cross(sub(b, a), sub(c, a))
        assert n != (0, 0, 0)
        off = dot(n, a)
        if dot(n, cen) > off:
            n = tuple(-x for x in n)
            off = -off
        assert all(dot(n, p) <= off for p in P), "not a supporting plane"
        # normalise: divide by the first non-zero |coordinate|
        s = next(abs(x) for x in n if x != 0)
        key = tuple(x / s for x in n) + (off / s,)
        planes[key] = planes.get(key, 0) + 1
    return [(k[:3], k[3]) for k in planes], len(hull.simplices), sorted(hull.vertices.tolist())


def vertices_of(planes):
    """exact vertex enumeration of {n.x <= b}; returns dict vertex -> set of tight plane indices"""
    V = {}
    m = len(planes)
    for i, j, k in itertools.combinations(range(m), 3):
        x = solve3(planes[i][0], planes[j][0], planes[k][0], planes[i][1], planes[j][1], planes[k][1])
        if x is None:
            continue
        if all(dot(n, x) <= b for n, b in planes):
            V.setdefault(x, set()).update(t for t, (n, b) in enumerate(planes) if dot(n, x) == b)
    return V


def volume(planes, V):
    """exact volume of the bounded polytope with vertex dict V: fan from the vertex centroid over every facet polygon"""
    c = tuple(sum(v[k] for v in V) / len(V) for k in range(3))
    vol = Fr(0)
    for f, (n, b) in enumerate(planes):
        vs = [v for v, tight in V.items() if f in tight]
        if len(vs) < 3:
            continue
        # order the polygon's vertices around its centroid in the plane
        g = tuple(sum(v[k] for v in vs) / len(vs) for k in range(3))
        e1 = sub(vs[0], g)
        e2 = cross(n, e1)
        import math
        vs.sort(key=lambda v: math.atan2(float(dot(sub(v, g), e2)), float(dot(sub(v, g), e1))))
        for t in range(len(vs)):
            a, bb = vs[t], vs[(t + 1) % len(vs)]
            vol += abs(det3(sub(g, c), sub(a, c), sub(bb, c))) / 6
    return vol


UinvT = None


def dual_norm(n):
    # ||x||_c = |Ux|_1 with U = [[5,0,0],[3,3,0],[1,1,1]];  dual norm = |U^{-T} n|_inf.
    # U^{-1} = [[1/5,0,0],[-1/5,1/3,0],[0,-1/3,1]];  U^{-T} n = (n0/5 - n1/5, n1/3 - n2/3, n2)
    return max(abs(n[0] / 5 - n[1] / 5), abs(n[1] / 3 - n[2] / 3), abs(n[2]))


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    from verify_packing import my_points, cnorm
    pts = my_points()
    P = [p[:3] for p in pts]
    delta = max(p[4] for p in pts)
    # sanity of the dual norm: max of n.x over the six vertices of the unit ball of ||.||_c
    ball = []
    for k, col in enumerate([(Fr(1, 5), Fr(-1, 5), Fr(0)), (Fr(0), Fr(1, 3), Fr(-1, 3)), (Fr(0), Fr(0), Fr(1))]):
        for s in (1, -1):
            w = tuple(s * x for x in col)
            assert cnorm(w) == 1
            ball.append(w)
    import random
    rng = random.Random(1)
    for _ in range(200):
        n = tuple(Fr(rng.randint(-9, 9)) for _ in range(3))
        assert dual_norm(n) == max(dot(n, w) for w in ball)
    # exact points only
    pl4, _, _ = planes_of_hull(P[:4])
    V4 = vertices_of(pl4)
    print("exact points only: volume of the hull =", volume(pl4, V4), " (vertices:", len(V4), ")")
    planes, ntri, hv = planes_of_hull(P)
    V = vertices_of(planes)
    assert set(V) <= set(P), "a vertex of the halfspace intersection is not one of the points: facet list incomplete"
    nv = len(V)
    print(f"hull C of the 14 points: {ntri} Qhull triangles -> {len(planes)} distinct supporting planes (each exact, all 14 points on the inner side);")
    print(f"   exact vertex enumeration of the intersection of these halfspaces: {nv} vertices, all among the 14 points  => the facet list is complete")
    print(f"   Euler check (simplicial): triangles = 2*vertices - 4: {ntri} = {2*nv-4}: {ntri == 2*nv-4}")
    inner = [i for i, p in enumerate(P) if p not in V]
    print("   points of the list that are not vertices of C (indices):", inner)
    vC = volume(planes, V)
    print(f"   vol C = {vC} = {float(vC):.6f}")
    er = [(n, b - delta * dual_norm(n)) for n, b in planes]
    VE = vertices_of(er)
    vE = volume(er, VE)
    print(f"delta = {delta} = {float(delta):.6f};  eroded polytope: {len(VE)} vertices;  vol(C eroded) = {float(vE):.6f}")
    print(f"   exact value as a fraction has numerator/denominator of {len(str(vE.numerator))}/{len(str(vE.denominator))} digits;  vol >= 1.56: {vE >= Fr(156, 100)};  >= 1.563: {vE >= Fr(1563, 1000)}")
    # independent certificate that E + delta*B is inside C: every vertex of E, moved by delta times each of the six
    # vertices of the unit ball, satisfies all facet inequalities of C exactly
    ok = all(dot(n, tuple(v[k] + delta * w[k] for k in range(3))) <= b for v in VE for w in ball for n, b in planes)
    print("   certificate: (vertex of E) + delta*(vertex of the unit ball of ||.||_c) lies in C for all", len(VE) * 6, "combinations:", ok)
    # float cross-check with Qhull on the eroded vertices
    print("   float cross-check (Qhull volume of the eroded vertices):", ConvexHull(np.array([[float(c) for c in v] for v in VE])).volume,
          "; of C:", ConvexHull(np.array([[float(c) for c in p] for p in P])).volume)
    print(f"   per cent of the bulk box [0,1]x[0,5]x[0,6] (volume 30): {100*float(vE)/30:.2f} (inner), {100*3.125/30:.2f} (outer, K_2)")
    # how close are the bridges of the two unproved vertices of K_2
    for name, vert, idx in (("W3 woodpile -> (0,3,4)", (Fr(0), Fr(3), Fr(4)), None), ("crossed rods -> (1/2,4,9/2)", (Fr(1, 2), Fr(4), Fr(9, 2)), None)):
        best = min(P[4:], key=lambda p: cnorm(sub(p, vert)))
        dd = cnorm(sub(best, vert))
        print(f"   {name}: nearest verified bridge density ({float(best[0]):.4f},{float(best[1]):.4f},{float(best[2]):.4f}); "
              f"||diff||_c = {float(dd):.3f} = {100*float(dd/cnorm(vert)):.1f} % of ||vertex||_c = {cnorm(vert)}; "
              f"coordinatewise relative deviations p8: {100*float(abs(best[1]-vert[1])/vert[1]):.1f} %, p11: {100*float(abs(best[2]-vert[2])/vert[2]):.1f} %")
