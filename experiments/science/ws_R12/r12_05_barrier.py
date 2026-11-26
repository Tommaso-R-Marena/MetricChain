#!/usr/bin/env python3
"""R12 item 5 — the small instances of proofs/Frontiers/BarrierCertificate.lean (theory branch at
9408e33) recomputed with code of my own, and the adjacency lemma by brute force.

Nothing of the theory division's code is imported.  The instances are re-typed from the Lean
definitions (`ferro` is our own, from experiments/science/ws_K/KineticsCertificates.lean).

Energy convention of `PairInstance.energy` (proofs/CertificateAlgebra.lean, identical in our tree):
    E(x) = sum_i h_i(x_i) + sum_i sum_{j != i} J(i, j, x_i, x_j)      (ordered pairs).

Checked here:
 1. the adjacency lemma: for ALL pairs of boxes (domains = arbitrary subsets, the empty set
    included) on small grids,
      (i)   "contain two configurations differing in at most one site" => "at most one site has
            disjoint domains"                                   (the direction soundness uses);
      (ii)  the converse of (i) (our text, SCI-MSG-0005 par. 5 and SK_REPORT par. 2.5 / T1) — where it fails;
      (iii) with the non-emptiness clause: equivalence (their `Dom.adjacent_iff`, n >= 1).
 2. `ferro`: exact minimax barrier 111 <-> 000.
 3. `maze`: exact minimax barrier 0000 <-> 1111; their cut tree `mazeCut` evaluated by my own
    implementation of the three checks (with the adjacency decided by enumerating actual moves);
    the best bound any box cut can certify around either end point (all boxes enumerated).
 4. `scan`: barrier (0,0) <-> (2,0) under nearest-state moves and under unrestricted moves.
 5. `ferroResidual`: the extremal residual for the robust barrier height 13/4.
 6. the empty-leaf example (`ferroEmptyLeafTree`): accepted with the clause, rejected with the
    literal criterion.

One command:  python3 r12_05_barrier.py
"""
import itertools
import time
from fractions import Fraction as Fr

T0 = time.time()


# ---------------------------------------------------------------- generic small-state machinery
def configs(n, k):
    return list(itertools.product(range(k), repeat=n))


def energy(h, J, x):
    n = len(x)
    e = sum(h(i, x[i]) for i in range(n))
    e += sum(J(i, j, x[i], x[j]) for i in range(n) for j in range(n) if j != i)
    return e


def single_site(x, y):
    """Differ in at most one site (the Lean `SingleSite`, which includes x = y)."""
    return sum(a != b for a, b in zip(x, y)) <= 1


def site_move(G, x, y):
    """One site i moves along an edge of G (G(i, s, t) True), the others keep their state."""
    n = len(x)
    for i in range(n):
        if G(i, x[i], y[i]) and all(x[j] == y[j] for j in range(n) if j != i):
            return True
    return False


def minimax_barrier(X, E, adj, a, b):
    """min over walks a -> b of the max energy on the walk (end points included); exact, by a
    bottleneck shortest-path iteration (Bellman-Ford on (max, min)); directed moves allowed."""
    INF = None
    best = {x: INF for x in X}
    best[a] = E[a]
    changed = True
    while changed:
        changed = False
        for x in X:
            if best[x] is INF:
                continue
            for y in X:
                if x != y and adj(x, y):
                    cand = max(best[x], E[y])
                    if best[y] is INF or cand < best[y]:
                        best[y] = cand
                        changed = True
    return best[b]


# ---------------------------------------------------------------- 1. the adjacency lemma
print("=" * 100)
print("1. Adjacency lemma, all pairs of boxes (empty domains allowed)")
print("=" * 100)


def subsets(k):
    return [frozenset(s) for r in range(k + 1) for s in itertools.combinations(range(k), r)]


def box_points(D, k):
    return list(itertools.product(*[sorted(d) for d in D]))


for n, k in ((1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 2), (2, 4), (4, 2)):
    doms = subsets(k)
    boxes = list(itertools.product(doms, repeat=n))
    pts = {D: box_points(D, k) for D in boxes}
    pairs = fail_i = fail_ii = fail_ii_nonempty = fail_iii = 0
    example = None
    for D in boxes:
        for D2 in boxes:
            pairs += 1
            nb = any(single_site(x, y) for x in pts[D] for y in pts[D2])
            sep = sum(1 for i in range(n) if not (D[i] & D2[i]))
            crit = sep <= 1
            nonempty = all(len(D[i]) > 0 and len(D2[i]) > 0 for i in range(n))
            if nb and not crit:
                fail_i += 1
            if crit and not nb:
                fail_ii += 1
                if nonempty:
                    fail_ii_nonempty += 1
                if example is None:
                    example = (tuple(sorted(d) for d in D), tuple(sorted(d) for d in D2))
            if (crit and nonempty) != nb:
                fail_iii += 1
    print("n=%d k=%d: %6d ordered pairs of boxes | (i) fails: %d | (ii) 'criterion => neighbours' fails: %d "
          "(of these with both boxes non-empty: %d) | (iii) with the non-emptiness clause, iff fails: %d%s" % (
              n, k, pairs, fail_i, fail_ii, fail_ii_nonempty, fail_iii,
              ("   e.g. D=%s D'=%s" % example) if example else ""))
print("their witness (Dom 2 1): D = ([], [0]), D' = ([0], [0]): separated sites = 1, D empty -> no pair of configurations")

# ---------------------------------------------------------------- 2. ferro
print()
print("=" * 100)
print("2. ferro (three binary sites; ours)")
print("=" * 100)


def ferro_h(i, a):
    return Fr(-1, 2) if a == 1 else Fr(0)


def ferro_J(i, j, a, b):
    return Fr(2) if (i < j and a != b) else Fr(0)


X3 = configs(3, 2)
E_ferro = {x: energy(ferro_h, ferro_J, x) for x in X3}
print("energies:", {"".join(map(str, x)): str(e) for x, e in E_ferro.items()})
b1 = minimax_barrier(X3, E_ferro, single_site, (1, 1, 1), (0, 0, 0))
b2 = minimax_barrier(X3, E_ferro, single_site, (0, 0, 0), (1, 1, 1))
print("exact barrier 111 -> 000: %s ; 000 -> 111: %s   (Lean: ferro_barrier_exact, 7/2)" % (b1, b2))

# ---------------------------------------------------------------- 3. maze
print()
print("=" * 100)
print("3. maze (four binary sites)")
print("=" * 100)


def maze_h(i, s):
    return Fr(1) if (s == 1 and i != 0) else Fr(0)


def maze_J(i, j, s, t):
    if s == 1 and t == 1:
        if (i, j) == (0, 1):
            return Fr(-1)
        if (i, j) == (0, 2):
            return Fr(2)
        if (i, j) == (1, 2):
            return Fr(-2)
        if (i, j) == (2, 3):
            return Fr(-2)
    return Fr(0)


X4 = configs(4, 2)
E_maze = {x: energy(maze_h, maze_J, x) for x in X4}
closed = {x: x[1] + x[2] + x[3] - x[0] * x[1] + 2 * x[0] * x[2] - 2 * x[1] * x[2] - 2 * x[2] * x[3] for x in X4}
print("energy table equals the closed form x1+x2+x3-x0x1+2x0x2-2x1x2-2x2x3:", all(E_maze[x] == closed[x] for x in X4))
a, b = (0, 0, 0, 0), (1, 1, 1, 1)
bm = minimax_barrier(X4, E_maze, single_site, a, b)
print("E(0000) = %s, E(1111) = %s; exact barrier 0000 <-> 1111: %s   (Lean: maze_barrier_exact, 1)" % (E_maze[a], E_maze[b], bm))
basin = {x for x in X4 if minimax_barrier(X4, E_maze, single_site, a, x) < 1}
print("configurations reachable from 0000 below energy 1:", sorted("".join(map(str, x)) for x in basin),
      "(Lean comment: 0000, 1000, 1100)")


# my own implementation of the tree format (branch / split) and of the three checks
def leaves(tree, D, k):
    kind = tree[0]
    if kind in ("inside", "outside"):
        return [(D, kind)]
    if kind == "wall":
        return [(D, "wall")]
    if kind == "branch":
        _, i, children = tree
        out = []
        for s in sorted(D[i]):
            D2 = list(D)
            D2[i] = frozenset([s])
            out += leaves(children(s), tuple(D2), k)
        return out
    if kind == "split":
        _, i, T, yes, no = tree
        Dy = list(D)
        Dy[i] = D[i] & frozenset(T)
        Dn = list(D)
        Dn[i] = D[i] - frozenset(T)
        return leaves(yes, tuple(Dy), k) + leaves(no, tuple(Dn), k)
    raise ValueError(kind)


def in_box(D, x):
    return all(x[i] in D[i] for i in range(len(x)))


def check_tree(tree, n, k, E, adj, a, b, L, adjacency="moves"):
    X = configs(n, k)
    full = tuple(frozenset(range(k)) for _ in range(n))
    lv = leaves(tree, full, k)
    ins = [D for D, z in lv if z == "inside"]
    outs = [D for D, z in lv if z == "outside"]
    walls = [D for D, z in lv if z == "wall"]
    c1 = all(E[x] >= L for D in walls for x in X if in_box(D, x))

    def adjacent(D, D2):
        if adjacency == "moves":
            return any(adj(x, y) for x in X if in_box(D, x) for y in X if in_box(D2, y))
        sep = sum(1 for i in range(n) if not (D[i] & D2[i]))
        if adjacency == "literal":
            return sep <= 1
        if adjacency == "clause":
            return sep <= 1 and all(len(D[i]) > 0 and len(D2[i]) > 0 for i in range(n))
        raise ValueError

    c2 = not any(adjacent(D, D2) for D in ins for D2 in outs)
    c3 = any(in_box(D, a) for D in ins) and not any(in_box(D, b) for D in ins)
    cover = all(sum(1 for D, _ in lv if in_box(D, x)) == 1 for x in X)
    return c1, c2, c3, cover, lv


W = ("wall",)
I_ = ("inside",)
O_ = ("outside",)
mazeCut = ("split", 3, [1],
           ("split", 2, [1], O_, W),
           ("split", 2, [1],
            ("split", 1, [1], ("split", 0, [1], W, O_), W),
            ("split", 1, [1], ("split", 0, [1], I_, W), I_)))
c1, c2, c3, cover, lv = check_tree(mazeCut, 4, 2, E_maze, single_site, a, b, Fr(1))
print("mazeCut, bound 1: wall leaves all >= 1: %s; no move from an inside to an outside leaf: %s; "
      "a inside and b not: %s; leaves partition the grid: %s   => accepted: %s (Lean: maze_verified)" % (
          c1, c2, c3, cover, c1 and c2 and c3))
for adjacency in ("literal", "clause"):
    r = check_tree(mazeCut, 4, 2, E_maze, single_site, a, b, Fr(1), adjacency)
    print("   same tree with the box test '%s': checks (1,2,3) = %s" % (adjacency, r[:3]))
inside_set = sorted("".join(map(str, x)) for x in X4 if any(in_box(D, x) for D, z in lv if z == "inside"))
print("   region S of mazeCut:", inside_set)
c1b = check_tree(mazeCut, 4, 2, E_maze, single_site, a, b, Fr(1) + Fr(1, 1000))[0]
print("   same tree for the bound 1 + 1/1000: wall check passes: %s (so 1 is the largest bound this tree certifies)" % c1b)

# box cuts: every box D (non-empty domains) with a in D, b not in D; best L = min of E over the
# union of the wall boxes (wall box i: site i outside D_i, the other sites in their domains)
dom2 = [frozenset([0]), frozenset([1]), frozenset([0, 1])]


def best_box_cut(start, target, E, n=4, k=2):
    best = None
    arg = None
    count = 0
    for D in itertools.product(dom2, repeat=n):
        if not in_box(D, start) or in_box(D, target):
            continue
        count += 1
        wall_vals = []
        for i in range(n):
            comp = frozenset(range(k)) - D[i]
            if not comp:
                continue
            Dw = list(D)
            Dw[i] = comp
            wall_vals += [E[x] for x in configs(n, k) if in_box(tuple(Dw), x)]
        L = min(wall_vals)
        if best is None or L > best:
            best, arg = L, D
    return best, arg, count


Ls, Ds, cs = best_box_cut(a, b, E_maze)
Lt, Dt, ct = best_box_cut(b, a, E_maze)
print("box cuts around 0000 (not containing 1111): %d boxes; the largest certifiable bound is %s (Lean: maze_boxCut_start_le, L <= 0)" % (cs, Ls))
print("box cuts around 1111 (not containing 0000): %d boxes; the largest certifiable bound is %s (Lean: maze_boxCut_target_le, L <= 0)" % (ct, Lt))
print("trivial bound max(E(a), E(b)) = %s; barrier = %s" % (max(E_maze[a], E_maze[b]), bm))

# ---------------------------------------------------------------- 4. scan
print()
print("=" * 100)
print("4. scan (two sites, three states; site-graph product)")
print("=" * 100)


def scan_h(i, s):
    if i == 0:
        return Fr(3) if s == 1 else Fr(0)
    return {0: Fr(0), 1: Fr(1, 2), 2: Fr(2)}[s]


def scan_J(i, j, s, t):
    return Fr(-t) if (i == 0 and j == 1 and s == 1) else Fr(0)


def path_move(i, s, t):
    return s <= t + 1 and t <= s + 1


X23 = configs(2, 3)
E_scan = {x: energy(scan_h, scan_J, x) for x in X23}
print("energies:", {"".join(map(str, x)): str(e) for x, e in E_scan.items()})
bs = minimax_barrier(X23, E_scan, lambda x, y: site_move(path_move, x, y), (0, 0), (2, 0))
bh = minimax_barrier(X23, E_scan, single_site, (0, 0), (2, 0))
print("barrier (0,0) -> (2,0): nearest-state moves %s (Lean: scan_barrier_exact, 5/2); unrestricted single-site moves %s "
      "(Lean: scan_hamming_direct: neighbours, both of energy 0)" % (bs, bh))
scanCut = ("split", 0, [0], I_, ("split", 0, [1], W, O_))
r_on = check_tree(scanCut, 2, 3, E_scan, lambda x, y: site_move(path_move, x, y), (0, 0), (2, 0), Fr(5, 2))
r_h = check_tree(scanCut, 2, 3, E_scan, single_site, (0, 0), (2, 0), Fr(5, 2))
print("scanCut for 5/2: on the site-graph product checks (1,2,3) = %s (accepted: %s; Lean: scan_verified); on the Hamming "
      "graph %s (accepted: %s; Lean: scan_hamming_rejected)" % (r_on[:3], all(r_on[:3]), r_h[:3], all(r_h[:3])))

# ---------------------------------------------------------------- 5. ferroResidual
print()
print("=" * 100)
print("5. ferroResidual (bounded differences 1/4 per site, anchor g(000) = 0)")
print("=" * 100)
# the residual g(x) = -|x|/4 is in the class; with it the height of the barrier 000 -> 111 is 13/4
g_ext = {x: Fr(-sum(x), 4) for x in X3}
ok_class = all(abs(g_ext[x] - g_ext[y]) <= Fr(sum(u != v for u, v in zip(x, y)), 4) for x in X3 for y in X3)
Etrue = {x: E_ferro[x] + g_ext[x] for x in X3}
hb = minimax_barrier(X3, Etrue, single_site, (0, 0, 0), (1, 1, 1)) - Etrue[(0, 0, 0)]
print("g(x) = -|x|/4 is in the class: %s; barrier height 000 -> 111 with it: %s (Lean: ferroWellR_trap, >= 13/4 for every residual)" % (ok_class, hb))
# lower bound for every residual of the class: every walk passes a weight-1 configuration
low = min(E_ferro[x] - Fr(1, 4) for x in X3 if sum(x) == 1)
print("lower bound for every residual: min over the weight-1 wall of E - 1/4 = %s, minus E(000) + g(000) = 0" % low)

# ---------------------------------------------------------------- 6. the empty leaf
print()
print("=" * 100)
print("6. An empty leaf: ferroWellTree below split 0 [0,1] with an empty 'outside' child")
print("=" * 100)


def ferroWellTree():
    def lvl2_a(c):
        return I_ if c == 0 else W

    def lvl2_b(c):
        return W if c == 0 else O_

    def lvl1_0(bb):
        return ("branch", 2, lvl2_a) if bb == 0 else ("branch", 2, lvl2_b)

    def lvl1_1(bb):
        return ("branch", 2, lvl2_b) if bb == 0 else O_

    def top(aa):
        return ("branch", 1, lvl1_0) if aa == 0 else ("branch", 1, lvl1_1)

    return ("branch", 0, top)


emptyLeaf = ("split", 0, [0, 1], ferroWellTree(), O_)
for adjacency in ("moves", "clause", "literal"):
    r = check_tree(emptyLeaf, 3, 2, E_ferro, single_site, (0, 0, 0), (1, 1, 1), Fr(7, 2), adjacency)
    print("box test '%s': checks (1,2,3) = %s  accepted: %s" % (adjacency, r[:3], all(r[:3])))
print("(Lean: ferroEmptyLeaf_verified = true with the clause; ferroEmptyLeaf_literal_rejected = false with the literal test)")
r = check_tree(ferroWellTree(), 3, 2, E_ferro, single_site, (0, 0, 0), (1, 1, 1), Fr(7, 2))
print("ferroWellTree, bound 7/2: accepted: %s (Lean: ferroWell_verified); for the bound 4: wall check %s" % (
    all(r[:3]), check_tree(ferroWellTree(), 3, 2, E_ferro, single_site, (0, 0, 0), (1, 1, 1), Fr(4))[0]))
print()
print("total elapsed %.1f s" % (time.time() - T0))
print("R12_05_DONE")
