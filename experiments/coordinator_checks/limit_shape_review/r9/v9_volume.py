#!/usr/bin/env python3
"""V9 -- the ten explicit bridges of THEORY_REPORT 11.22: end corrections A, B from coordinates, exact points
q-hat/(N+3) of K^br, and the volume of the hull of the fourteen exact profile points (claim: vol K >= 1.6313).

Input: the coordinate files written by v9_gen_witness.py (our builder; nothing of the builder is used here).
For every bridge, with own code (mylat.py for the lattice and the two profile counts, v9_lib.py for A, B, clean):
  lattice walk, self-avoiding, bridge; (h3,h8,h11,g) by two counts, compared with the stored verified counts
  (experiments/coordinator_checks/limit_shape_review/wit/verified.json); A(x, c1) for every admissible c1 and B(x);
  clean or not; the cleaned bridge (head 2 + tail 3) is a clean bridge with (h,g) = q-hat.
Volume, all in exact rationals (Fractions):
  (i)  an exact brute-force convex hull of the 14 points: a plane through three non-collinear points is a facet plane
       iff all 14 points lie on one side of it; facets = point sets on such planes; volume = sum of the cones over the
       (triangulated) facets from an interior point.  No floating point, no Qhull.
  (ii) the facet list of Qhull (scipy.spatial.ConvexHull) with exact arithmetic on it; must agree with (i).
The same for the old points (h/N; the hull C of the report, 1.6317) as a check of the method against the stored number.
Bonus: the reviewer's four packings (weights stored in OUR repository, reviewer_packings/) on the exact vertices with
all radii zero: the pairwise condition L||p_k - p_l||_c > e (g_k + g_l) + 2 eps1 in exact rationals.
usage: v9_volume.py WITDIR
"""
import sys, os, json, glob, itertools, time
sys.dont_write_bytecode = True
from fractions import Fraction as Fr
import numpy as np
from v9_lib import *

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
REV = os.path.join(REPO, "experiments", "coordinator_checks", "limit_shape_review")
witdir = sys.argv[1]
stored = json.load(open(os.path.join(REV, "wit", "verified.json")))

rows = {}
print("1. the ten explicit bridges, from coordinates")
for f in sorted(glob.glob(os.path.join(witdir, "*.npy"))):
    t0 = time.time()
    name = os.path.basename(f)[:-4]
    X = np.load(f).astype(np.int64)
    okw, okb = ML.check_walk_np(X)
    x = [tuple(int(c) for c in r) for r in X]
    N = len(x)
    assert okw and okb
    check_bridge(x)                                   # scalar check of the whole walk as well
    hg = ML.profile_hash(x)
    assert hg == ML.profile_kdtree(x)
    assert stored[name]["N"] == N and tuple(stored[name]["hg"]) == hg, "differs from the stored verified counts"
    idx = index_of(x)
    Bx = B_of(x, idx)
    ad = admissible(x)
    As = [A_of(x, c, idx) for c in ad]
    cl = is_clean(x, idx)
    bp = sub(x[-2], x[-3])
    # cleaning with every admissible c1
    for c, Ax in zip(ad, As):
        xh = extend(x, c, 2, 3)
        check_bridge(xh)
        assert is_clean(xh)
        assert ML.profile_hash(xh) == vadd(hg, Ax, Bx)
    # the local picture of the two ends
    top = [p for p in x if p[1] >= x[-1][1] - 2]
    bot = [p for p in x if p[1] <= x[0][1] + 2]
    rows[name] = dict(N=N, hg=hg, A=As, B=Bx, c=ad, clean=cl)
    print(f"   {name:30s} N = {N:6d}  (h,g) = {hg}  b' {'up' if bp[1] == 1 else 'DOWN'}  admissible c1: {ad}  A = {As}  B = {Bx}  clean: {cl}"
          f"  | beads within 2 height units of the top/bottom bead: {len(top)}/{len(bot)}  | head 2 + tail 3: clean, (h,g) = q-hat  [{time.time()-t0:.1f} s]", flush=True)
ncl = sum(r["clean"] for r in rows.values())
print(f"   clean as built: {ncl} of {len(rows)};  not clean: {[n for n, r in rows.items() if not r['clean']]}")

# ------------------------------------------------------------------ exact hull volume


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def sub3(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def det3(a, b, c):
    return dot(a, cross(b, c))


def hull_bruteforce(P):
    """exact facets of conv(P) in R^3: list of (outward normal n, offset b, indices of the points on the plane)"""
    n = len(P)
    facets = {}
    for i, j, k in itertools.combinations(range(n), 3):
        nv = cross(sub3(P[j], P[i]), sub3(P[k], P[i]))
        if nv == (0, 0, 0):
            continue
        off = dot(nv, P[i])
        s = [dot(nv, p) - off for p in P]
        if all(t <= 0 for t in s):
            pass
        elif all(t >= 0 for t in s):
            nv = tuple(-c for c in nv)
            off = -off
        else:
            continue
        on = tuple(m for m in range(n) if dot(nv, P[m]) == off)
        facets[on] = (nv, off)
    return [(nv, off, on) for on, (nv, off) in facets.items()]


def volume_from_facets(P, facets):
    """sum of the cones from the centroid of the hull vertices over every facet (polygon ordered in its plane)"""
    verts = sorted(set(m for _, _, on in facets for m in on))
    c0 = tuple(sum(P[m][k] for m in verts) / len(verts) for k in range(3))
    for nv, off, on in facets:
        assert dot(nv, c0) < off, "the reference point is not strictly inside"
    vol = Fr(0)
    ntri = 0
    for nv, off, on in facets:
        pts = [P[m] for m in on]
        if len(pts) > 3:
            # order the polygon: exact, by repeatedly taking the next point with all others on the left of the edge
            order = [pts[0]]
            rest = pts[1:]
            while rest:
                cur = order[-1]
                nxt = None
                for q in rest:
                    if all(dot(nv, cross(sub3(q, cur), sub3(r, cur))) >= 0 for r in pts if r not in (cur, q)):
                        nxt = q
                        break
                assert nxt is not None
                order.append(nxt)
                rest.remove(nxt)
            pts = order
        for t in range(1, len(pts) - 1):
            vol += abs(det3(sub3(pts[0], c0), sub3(pts[t], c0), sub3(pts[t + 1], c0))) / 6
            ntri += 1
    return vol, verts, ntri


def volume_qhull_exact(P):
    """Qhull's triangles, each verified exactly to lie in a supporting plane; exact sum of cones; closedness check"""
    from scipy.spatial import ConvexHull
    hull = ConvexHull(np.array([[float(c) for c in p] for p in P]))
    verts = sorted(hull.vertices.tolist())
    c0 = tuple(sum(P[m][k] for m in verts) / len(verts) for k in range(3))
    vol = Fr(0)
    edges = {}
    for tri in hull.simplices:
        a, b, c = (P[int(i)] for i in tri)
        nv = cross(sub3(b, a), sub3(c, a))
        assert nv != (0, 0, 0)
        off = dot(nv, a)
        s = [dot(nv, p) - off for p in P]
        assert all(t <= 0 for t in s) or all(t >= 0 for t in s), "a Qhull triangle is not in a supporting plane"
        vol += abs(det3(sub3(a, c0), sub3(b, c0), sub3(c, c0))) / 6
        for e in itertools.combinations(sorted(int(i) for i in tri), 2):
            edges[e] = edges.get(e, 0) + 1
    assert all(v == 2 for v in edges.values()), "Qhull's triangles do not form a closed surface"
    assert len(verts) - len(edges) + len(hull.simplices) == 2, "Euler"
    return vol, verts, len(hull.simplices), hull.volume


EXACT4 = [(Fr(0), Fr(0), Fr(0), Fr(0)), (Fr(1, 2), Fr(2), Fr(3, 2), Fr(0)), (Fr(1), Fr(5), Fr(6), Fr(0)), (Fr(0), Fr(0), Fr(1), Fr(1))]
names = sorted(rows)


def report(label, pts4):
    P = [p[:3] for p in pts4]
    fac = hull_bruteforce(P)
    vol, verts, ntri = volume_from_facets(P, fac)
    vq, vertsq, ntq, vfloat = volume_qhull_exact(P)
    print(f"   {label}: exact brute-force hull: {len(fac)} facets ({ntri} triangles), {len(verts)} vertices; vol = {float(vol):.6f}")
    print(f"      Qhull facet list with exact arithmetic: {ntq} triangles, {len(vertsq)} vertices; vol = {float(vq):.6f}; agree exactly: {vol == vq and verts == vertsq}; Qhull's float volume {vfloat:.6f}")
    print(f"      points that are not vertices (index in the list of 14): {[i for i in range(len(P)) if i not in verts]}")
    print(f"      vol as a fraction: {vol.numerator}/{vol.denominator}" if len(str(vol.denominator)) < 80 else f"      vol is a fraction with a {len(str(vol.denominator))}-digit denominator")
    assert vol == vq
    return vol


print("\n2. volumes of hulls of profile points (exact rationals)")
old = EXACT4 + [tuple(Fr(c, rows[n]["N"]) for c in rows[n]["hg"]) for n in names]
v_old = report("old points h/N (the hull C of the report; stored value 1.6317, vol C = 1.631706)", old)
assert abs(float(v_old) - 1.631706) < 5e-7
# exact points: q-hat/(N+3) with the first admissible c1; and every choice of c1 where two are admissible
choices = [range(len(rows[n]["A"])) for n in names]
vols = []
for pick in itertools.product(*choices):
    ex = EXACT4 + [tuple(Fr(rows[n]["hg"][k] + rows[n]["A"][ci][k] + rows[n]["B"][k], rows[n]["N"] + 3) for k in range(4)) for n, ci in zip(names, pick)]
    v = report(f"EXACT points q-hat/(N+3), choice of c1 {pick}", ex)
    vols.append((v, pick, ex))
vmin = min(v for v, _, _ in vols)
vmax = max(v for v, _, _ in vols)
print(f"   => vol K >= {float(vmax):.6f} (largest over the admissible choices; smallest {float(vmin):.6f});  >= 1.6313: {vmax >= Fr(16313, 10000)};  >= 1.63134: {vmax >= Fr(163134, 100000)};  >= 1.63135: {vmax >= Fr(163135, 100000)}")
# without the end corrections but with the right normalisation (what one would get if all ten were clean)
nocorr = EXACT4 + [tuple(Fr(c, rows[n]["N"] + 3) for c in rows[n]["hg"]) for n in names]
report("for comparison: h/(N+3) without end corrections (NOT all exact points)", nocorr)
# hull of ALL exact points at once (both choices of c1 where free)
allex = list(EXACT4)
for n in names:
    for ci in range(len(rows[n]["A"])):
        q = tuple(Fr(rows[n]["hg"][k] + rows[n]["A"][ci][k] + rows[n]["B"][k], rows[n]["N"] + 3) for k in range(4))
        if q not in allex:
            allex.append(q)
if len(allex) > 14:
    report(f"all {len(allex)} exact points (both c1 where two are admissible)", allex)

# ------------------------------------------------------------------ bonus: the four packings on exact vertices
print("\n3. the reviewer's four packings on the exact vertices, all radii zero (exact rationals)")


def cn(d):
    return 5 * abs(d[0]) + 3 * abs(d[0] + d[1]) + abs(d[0] + d[1] + d[2])


SCI = os.path.join(REV, "reviewer_packings")
Vfile = [tuple(Fr(t) for t in line.split()) for line in open(os.path.join(SCI, "rigorous_packing_vertices.txt")) if not line.startswith("#")]
assert len(Vfile) == 14
# map every row of the reviewer's vertex file (old point (h,g)/N, delta) to the exact point of the same bridge
ex = vols[0][2]
newV = []
for r in Vfile:
    if r[4] == 0:
        assert r[:4] in EXACT4
        newV.append(r[:4])
    else:
        hit = [n for n in names if tuple(Fr(c, rows[n]["N"]) for c in rows[n]["hg"]) == r[:4] and Fr(168, rows[n]["N"] + 3) == r[4]]
        assert len(hit) == 1
        newV.append(ex[4 + names.index(hit[0])])
for tag, L, e1, claimed in (("L1_e12", Fr(1), Fr(1, 2), 116), ("L1_e14", Fr(1), Fr(1, 4), 451), ("L15_e12", Fr(1, 5), Fr(1, 2), 8), ("L15_e14", Fr(1, 5), Fr(1, 4), 19)):
    Pk = []
    for line in open(os.path.join(SCI, f"rigorous_packing_{tag}.txt")):
        if line.startswith("#"):
            continue
        lam = [Fr(t) for t in line.split()]
        assert len(lam) == 14 and all(t >= 0 for t in lam) and sum(lam) == 1
        Pk.append(tuple(sum(lam[i] * newV[i][k] for i in range(14)) for k in range(4)))
    worst = None
    ok = True
    for a, b in itertools.combinations(Pk, 2):
        m = L * cn([a[k] - b[k] for k in range(3)]) - (a[3] + b[3]) - 2 * e1
        ok = ok and m > 0
        worst = m if worst is None or m < worst else worst
    print(f"   (L, eps1) = ({L}, {e1}): {len(Pk)} points (claimed {claimed}); pairwise condition with zero radii holds exactly: {ok}; smallest margin {float(worst):.3e}")
