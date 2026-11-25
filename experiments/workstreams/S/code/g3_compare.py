#!/usr/bin/env python3
"""G3 evidence: profile sets and lower boundaries of bridges against all walks, from exhaustive enumeration.

Reads  out/walk_N*.txt, out/bridge_N*.txt, out/hsw_N*.txt  (own enumerator, code/enum.c) and the other
division's class tables (n = N-3 torsions).  Prints
  1. validation of the own walk tables against the other division's (count, gmin, gmax per class);
  2. extreme values per bead for walks and bridges;
  3. one-sided distances walks -> bridges (bridges are walks, so the other side is zero), in the profile norm
     ||dh||_c = 5|dh3| + 3|dh3+dh8| + |dh3+dh8+dh11| (L1 distance of cumulative profiles), unnormalised and per
     bead, also against bridges with N+k beads;
  4. the same for the lower boundaries (h, gmin):  d = max over walk classes of the min over bridge classes of
     ||dh||_w + max(0, gmin_bridge - gmin_walk);
  5. nestedness in N and a convexity test of the walk class tables.
usage: g3_compare.py OUT_DIR ENG_DATA_DIR
"""
import sys, os
import numpy as np

W = np.array([9, 4, 1])          # ||N^x||_1 = 9 h3 + 4 h8 + h11 for a single profile
CW = np.array([5, 3, 1])         # weights of the cumulative coordinates

def load_own(path):
    t = {}
    with open(path) as f:
        for line in f:
            if line.startswith('#'): continue
            a = line.split()
            t[(int(a[0]), int(a[1]), int(a[2]))] = (int(a[3]), int(a[4]), int(a[5]), int(a[6], 16))
    return t

def load_eng(path):
    t = {}
    with open(path) as f:
        for line in f:
            if line.startswith('#'): continue
            a = list(map(int, line.split()))
            t[tuple(a[:3])] = (a[3], a[4], a[6], a[5])     # count, gmin, gmax, count_gmin
    return t

def onesided(Ah, Ag, Bh, Bg, chunk=512):
    """max over rows a of A of  min over rows b of B of  ||a-b||_w + max(0, Bg-Ag);  (Ag,Bg may be None)"""
    worst = 0.0; arg = None
    Ac = np.cumsum(Ah, axis=1); Bc = np.cumsum(Bh, axis=1)
    for s in range(0, len(Ah), chunk):
        d = (np.abs(Ac[s:s+chunk, None, :] - Bc[None, :, :]) * CW).sum(axis=2).astype(float)
        if Ag is not None:
            d = d + np.maximum(0, Bg[None, :] - Ag[s:s+chunk, None])
        m = d.min(axis=1)
        i = int(m.argmax())
        if m[i] > worst:
            worst = float(m[i]); arg = s + i
    return worst, arg

def main():
    out, eng = sys.argv[1], sys.argv[2]
    walk, bridge, hsw, engt = {}, {}, {}, {}
    for N in range(4, 28):
        p = f"{out}/walk_N{N}.txt"
        if os.path.exists(p): walk[N] = load_own(p)
        p = f"{out}/bridge_N{N}.txt"
        if os.path.exists(p): bridge[N] = load_own(p)
        p = f"{out}/hsw_N{N}.txt"
        if os.path.exists(p): hsw[N] = load_own(p)
        p = f"{eng}/dia_Sc12_n{N-3}.txt"
        if os.path.exists(p): engt[N] = load_eng(p)
    print("== 1. validation: own walk tables against the other division's class tables")
    for N in sorted(walk):
        a = {k: v[:3] for k, v in walk[N].items()}
        b = {k: v[:3] for k, v in engt[N].items()}
        print(f"  N={N:2d} classes own={len(a):5d} other={len(b):5d} identical (count, gmin, gmax per class): {a == b}")
        assert a == b
    # use the other division's tables for walks beyond own range
    wt = {N: {k: (v[0], v[1], v[2]) for k, v in engt[N].items()} for N in engt}

    print("\n== 2. extremes per bead (walks W, bridges B, half-space walks H);  wnorm = 9 h3 + 4 h8 + h11")
    print("   N   cls_W cls_B  | max h3/N  W      B   | max h8/N  W     B   | max h11/N W     B   | max wnorm/N W      B      H")
    for N in sorted(wt):
        kw = np.array(list(wt[N].keys()))
        row = f"  {N:2d}  {len(kw):5d} "
        if N in bridge:
            kb = np.array(list(bridge[N].keys()))
            kh = np.array(list(hsw[N].keys())) if N in hsw else None
            row += f"{len(kb):5d}  |"
            for c in range(3):
                row += f"        {kw[:,c].max()/N:5.3f} {kb[:,c].max()/N:5.3f} |"
            row += f"          {(kw@W).max()/N:6.3f} {(kb@W).max()/N:6.3f}"
            if kh is not None: row += f" {(kh@W).max()/N:6.3f}"
        else:
            row += "    -  |"
            for c in range(3):
                row += f"        {kw[:,c].max()/N:5.3f}   -   |"
            row += f"          {(kw@W).max()/N:6.3f}"
        print(row)

    print("\n== 3./4. one-sided distances  walks(N) -> bridges(N+k)   [profile sets | lower boundaries (h, gmin)]")
    print("   unnormalised profile distance ||.||_c; in brackets the distance per bead of the walk")
    print("   N   k=0: sets        lower bdry      k=1: sets        lower bdry      k=2: sets       lower bdry     k=3: sets       lower bdry")
    for N in sorted(wt):
        kw = np.array(list(wt[N].keys())); gw = np.array([wt[N][tuple(k)][1] for k in kw])
        row = f"  {N:2d} "
        any_ = False
        for k in range(4):
            if N + k in bridge:
                any_ = True
                kb = np.array(list(bridge[N + k].keys())); gb = np.array([bridge[N + k][tuple(q)][1] for q in kb])
                d1, _ = onesided(kw, None, kb, None)
                d2_, _ = onesided(kw, gw, kb, gb)
                row += f"  {d1:5.0f} ({d1/N:5.3f})  {d2_:5.0f} ({d2_/N:5.3f}) "
            else:
                row += "        -              -        "
        if any_: print(row)

    print("\n== 5a. nestedness of the walk class tables:  classes of N that are classes of N+1 / N+2 / N+3;")
    print("       and (N -> N+1) classes with gmin_{N+1}(h) <= gmin_N(h) + 1")
    for N in sorted(wt):
        if N + 1 not in wt: continue
        a = wt[N]
        r = []
        for k in (1, 2, 3):
            if N + k in wt:
                b = wt[N + k]
                r.append(sum(1 for h in a if h in b) / len(a))
        b = wt[N + 1]
        ok = sum(1 for h in a if h in b and b[h][1] <= a[h][1] + 1) / len(a)
        print(f"  N={N:2d}: " + " ".join(f"{x:6.3f}" for x in r) + f"   gmin-nested: {ok:6.3f}")

    print("\n== 5b. convexity of the walk profile sets (3D): lattice points of the convex hull that are classes,")
    print("       largest weighted distance from a hull lattice point to the set (unnormalised and per bead)")
    from scipy.spatial import ConvexHull, Delaunay
    for N in sorted(wt):
        if N < 9: continue
        kw = np.array(list(wt[N].keys()))
        try:
            hull = ConvexHull(kw)
        except Exception as ex:
            print(f"  N={N}: hull failed"); continue
        mx = kw.max(axis=0)
        grid = np.array([(a, b, c) for a in range(mx[0] + 1) for b in range(mx[1] + 1) for c in range(mx[2] + 1)])
        A_, b_ = hull.equations[:, :3], hull.equations[:, 3]
        inside = (grid @ A_.T + b_ <= 1e-9).all(axis=1)
        pts = grid[inside]
        S = set(map(tuple, kw))
        miss = np.array([p for p in pts if tuple(p) not in S])
        if len(miss):
            d, _ = onesided(miss, None, kw, None)
        else:
            d = 0.0
        print(f"  N={N:2d}: hull lattice points {len(pts):6d}, classes {len(kw):5d}, realised fraction {len(kw)/len(pts):5.3f}, "
              f"hull volume {hull.volume:9.1f} (per N^3: {hull.volume/N**3:7.4f}), max dist hull->set {d:4.0f} ({d/N:5.3f}/bead), "
              f"hull vertices {len(hull.vertices)}")

    print("\n== 5c. convexity of the lower boundary gmin (walks): largest gap between gmin(h) and the lower convex envelope")
    print("       of {(h, gmin(h))} at realised h  (computed by an LP per class is too slow; use the 4D hull facets)")
    for N in sorted(wt):
        if N < 12 or N % 3 != 0: continue
        kw = np.array(list(wt[N].keys())); gw = np.array([wt[N][tuple(k)][1] for k in kw])
        P4 = np.column_stack([kw, gw]).astype(float)
        try:
            hull = ConvexHull(P4)
        except Exception as ex:
            print(f"  N={N}: 4D hull failed: {ex}"); continue
        # lower envelope at point h: max over facets with normal pointing down in g (n_g < 0) of the g-value of the facet plane
        eq = hull.equations
        low = eq[eq[:, 3] < -1e-9]
        # facet: n.h + n_g g + c <= 0 inside;  g >= -(n.h + c)/n_g ... with n_g < 0: g >= (n.h + c)/(-n_g)
        env = ((kw @ low[:, :3].T + low[:, 4]) / (-low[:, 3])).max(axis=1)
        gap = gw - env
        i = int(gap.argmax())
        print(f"  N={N:2d}: max gap gmin - envelope = {gap.max():5.2f} ({gap.max()/N:5.3f} per bead) at h={tuple(kw[i])}, gmin={gw[i]}; "
              f"mean gap {gap.mean():5.2f}; classes on the envelope (gap < 1e-6): {(gap < 1e-6).sum()}")

if __name__ == "__main__":
    main()
