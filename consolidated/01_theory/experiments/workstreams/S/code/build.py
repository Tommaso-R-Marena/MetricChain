#!/usr/bin/env python3
"""Finite walks and bridges from periodic chain systems (generic "cut a box and link the strands" builder).

A periodic chain system is given by a witness line of code/pchain:
    hnf rows (a b c) (0 d e) (0 0 f); path bonds A(n)-type: A(i,j,l):aX,aY ...
(every A site whose fcc coordinate reduces to the coset (i,j,l) carries the two bonds +a_X, +a_Y).
The builder takes all bonds of the infinite structure with both ends in the box [0,W1)x[0,W2)x[0,W3) (Cartesian),
extracts the strands, and links them greedily into ONE self-avoiding walk by shortest lattice paths through free
sites (breadth-first search); then it adds two tails that make the walk a y-bridge.  The result is checked
(valid self-avoiding lattice walk; bridge) and its exact profile and gauche count are printed, next to the
ideal densities of the periodic structure.

usage: build.py "WITNESS" W1 W2 W3 [seed]
"""
import sys, re, collections, random
from lat import *

F = [(0, 2, 2), (2, 0, 2), (2, 2, 0)]

def parse(w):
    m = re.search(r"hnf rows \((\d+) (\d+) (\d+)\) \(0 (\d+) (\d+)\) \(0 0 (\d+)\)", w)
    a, b, c, d, e, f = map(int, m.groups())
    ch = {}
    for mm in re.finditer(r"A\((\d+),(\d+),(\d+)\):a(\d),a(\d)", w):
        i, j, l, x, y = map(int, mm.groups())
        ch[(i, j, l)] = (x, y)
    return (a, b, c, d, e, f), ch

def reduce(n, hnf):
    a, b, c, d, e, f = hnf
    n1, n2, n3 = n
    q = n1 // a; n1 -= q * a; n2 -= q * b; n3 -= q * c
    q = n2 // d; n2 -= q * d; n3 -= q * e
    n3 %= f
    return (n1, n2, n3)

def fcc_coords(p):
    """fcc coordinates of an A site p (Cartesian): p = n1 f1 + n2 f2 + n3 f3"""
    x, y, z = p
    return ((-x + y + z) // 4, (x - y + z) // 4, (x + y - z) // 4)

def strands_in_box(hnf, ch, W):
    adj = collections.defaultdict(list)
    for x in range(0, W[0], 2):
        for y in range(0, W[1], 2):
            for z in range(0, W[2], 2):
                if (x + y + z) % 4: continue
                p = (x, y, z)
                r = reduce(fcc_coords(p), hnf)
                if r not in ch: continue
                for t in ch[r]:
                    q = add(p, A[t])
                    if 0 <= q[0] < W[0] and 0 <= q[1] < W[1] and 0 <= q[2] < W[2]:
                        adj[p].append(q); adj[q].append(p)
    assert all(len(v) <= 2 for v in adj.values())
    seen = set(); strands = []
    for s in adj:
        if s in seen or len(adj[s]) != 1: continue
        path = [s]; seen.add(s); prev = None; cur = s
        while True:
            nxt = [t for t in adj[cur] if t != prev]
            if not nxt: break
            prev, cur = cur, nxt[0]
            path.append(cur); seen.add(cur)
        strands.append(path)
    return strands

def bfs(src, targets, blocked, maxdepth, box=None):
    """shortest path from src to any site of `targets` through sites not in `blocked` (targets may be blocked)"""
    if src in targets:
        return [src]
    par = {src: None}
    frontier = [src]
    for depth in range(maxdepth):
        nf = []
        for p in frontier:
            for q in nbrs(p):
                if q in par: continue
                if q in targets:
                    par[q] = p
                    path = [q]
                    while par[path[-1]] is not None: path.append(par[path[-1]])
                    return path[::-1]
                if q in blocked: continue
                if box is not None and not all(box[0][k] <= q[k] <= box[1][k] for k in range(3)): continue
                par[q] = p; nf.append(q)
        frontier = nf
        if not frontier: break
    return None

def link(strands, min_len=4, maxdepth=60, ncand=8):
    strands = [s for s in strands if len(s) >= min_len]
    occ = set()
    for s in strands: occ.update(s)
    ends = {}
    for i, s in enumerate(strands):
        ends[s[0]] = (i, 0); ends[s[-1]] = (i, 1)
    unused = set(range(len(strands)))
    # start at the lowest end
    e0 = min(ends, key=lambda p: (p[1], p[0], p[2]))
    i, side = ends[e0]
    walk = list(strands[i]) if side == 0 else list(strands[i][::-1])
    unused.discard(i)
    nlink = 0; dropped = 0
    while unused:
        e = walk[-1]
        cands = sorted((p for p in ends if ends[p][0] in unused), key=lambda p: d2(p, e))[:ncand]
        best = None
        for c in cands:
            path = bfs(e, {c}, occ, maxdepth)
            if path is not None and (best is None or len(path) < len(best)):
                best = path
                if len(path) <= 3: break
        if best is None:
            # nothing reachable among the nearest: try all remaining ends at once
            targ = {p for p in ends if ends[p][0] in unused}
            best = bfs(e, targ, occ, 4 * maxdepth)
            if best is None:
                dropped = len(unused); break
        c = best[-1]
        i, side = ends[c]
        mid = best[1:-1]
        occ.update(mid); nlink += len(mid)
        walk.extend(mid)
        walk.extend(strands[i] if side == 0 else strands[i][::-1])
        unused.discard(i)
    return walk, nlink, dropped, len(strands)

def make_bridge(walk):
    """add tails so that the first bead is strictly lowest and the last bead highest"""
    occ = set(walk)
    ymin = min(p[1] for p in walk); ymax = max(p[1] for p in walk)
    lo = (min(p[0] for p in walk) - 6, ymin - 6, min(p[2] for p in walk) - 6)
    hi = (max(p[0] for p in walk) + 6, ymax + 6, max(p[2] for p in walk) + 6)
    def tail(src, cond):
        # BFS to the nearest free site satisfying cond
        par = {src: None}; frontier = [src]
        while frontier:
            nf = []
            for p in frontier:
                for q in nbrs(p):
                    if q in par or q in occ: continue
                    if not all(lo[k] <= q[k] <= hi[k] for k in range(3)): continue
                    par[q] = p
                    if cond(q):
                        path = [q]
                        while par[path[-1]] is not None: path.append(par[path[-1]])
                        return path[::-1][1:]
                    nf.append(q)
            frontier = nf
        return None
    t1 = [] if all(p[1] > walk[0][1] for p in walk[1:]) else tail(walk[0], lambda q: q[1] < ymin)
    if t1 is None: return None
    occ.update(t1)
    w2 = t1[::-1] + walk
    # the tail towards the bottom ends strictly below everything; now the top
    ymax2 = max(p[1] for p in w2)
    t2 = [] if w2[-1][1] >= ymax2 else tail(w2[-1], lambda q: q[1] >= ymax2 + 1)
    if t2 is None: return None
    return w2 + t2

def ideal(hnf, ch):
    """densities of the infinite structure from a large periodic count is not needed: use the key of pchain"""
    return None

def main():
    w = sys.argv[1]; W = tuple(int(x) for x in sys.argv[2:5])
    hnf, ch = parse(w)
    strands = strands_in_box(hnf, ch, W)
    walk, nlink, dropped, ns = link(strands)
    assert is_walk(walk)
    N = len(walk); p = profile(walk)
    print(f"box {W}: strands {ns}, linker sites {nlink}, strands not linked {dropped}; walk: N = {N}, "
          f"(h3,h8,h11,g)/N = ({p[0]/N:.4f}, {p[1]/N:.4f}, {p[2]/N:.4f}, {p[3]/N:.4f})")
    b = make_bridge(walk)
    if b is None:
        print("  bridge tails: failed")
    else:
        assert is_walk(b) and is_bridge(b)
        N = len(b); p = profile(b)
        print(f"  bridge: N = {N}, (h3,h8,h11,g)/N = ({p[0]/N:.4f}, {p[1]/N:.4f}, {p[2]/N:.4f}, {p[3]/N:.4f})   [exact counts {p}]")

if __name__ == "__main__":
    main()
