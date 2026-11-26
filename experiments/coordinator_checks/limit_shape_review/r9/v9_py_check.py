#!/usr/bin/env python3
"""V9 -- Python cross-checks of Theorem R9.1 (a), (b), (c) with the second implementation v9_lib.py.

 part 1  the C program's per-bridge data (dump of `v9_cobound single 10 0 1 10`) against the Python counts:
         (h,g), A(x,c1), B(x), clean flag for every (bridge, c1) with N <= 10 (reduced set).
 part 2  all ordered pairs of bridges with N1, N2 <= NP in the FULL set -- start at an A site and at a B site, all four
         choices of the first two bonds, every admissible c1 -- concatenated from coordinates; all identities of (a), (b).
 part 3  random long bridges (cut out of self-avoiding walks grown in a narrow tube with an attraction to occupied
         neighbours, so that the ends are dense): cleaning (c) for every admissible c1, identities of (a) on random
         ordered pairs, six-fold self-concatenations.

usage: v9_py_check.py DUMPFILE NP NRAND SEED
"""
import sys, random, time, math
sys.dont_write_bytecode = True
from v9_lib import *

dumpfile, NP, NRAND, SEED = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
t0 = time.time()

# ---------------------------------------------------------------- part 1
n1 = 0
perN = {}
for line in open(dumpfile):
    if not line.startswith("D "):
        continue
    f = line[2:].split("|")
    head = [int(t) for t in f[0].split()]
    N, hg_c = head[0], tuple(head[1:5])
    A_c = tuple(int(t) for t in f[1].split())
    B_c = tuple(int(t) for t in f[2].split())
    c1 = tuple(int(t) for t in f[3].split())
    cl_c = int(f[4])
    co = [int(t) for t in f[5].split()]
    x = [tuple(co[3 * i:3 * i + 3]) for i in range(N)]
    check_bridge(x)
    idx = index_of(x)
    assert c1 in admissible(x)
    assert ML.profile_hash(x) == hg_c == ML.profile_bruteforce(x)
    assert A_of(x, c1, idx) == A_c, (x, c1, A_of(x, c1, idx), A_c)
    assert B_of(x, idx) == B_c
    assert int(is_clean(x, idx)) == cl_c
    n1 += 1
    perN[N] = perN.get(N, 0) + 1
print(f"part 1: {n1} lines (bridge, c1) of the C dump, per N {perN}: (h,g) [two Python counts], A, B and the clean flag all agree with the C program   [{time.time()-t0:.1f} s]", flush=True)

# ---------------------------------------------------------------- part 2
t0 = time.time()


def to_B_start(x):
    """image under the height-preserving lattice symmetry (x,y,z) -> (1-x, y+1, z+1), which maps the origin (A) to (1,1,1) (B)"""
    return [(1 - p[0], p[1] + 1, p[2] + 1) for p in x]


full = []
for N in range(3, NP + 1):
    for x in ML.enum_bridges(N):
        full.append(list(x))
        xb = to_B_start(x)
        check_bridge(xb)
        assert not ML.is_A(xb[0])
        full.append(xb)
cnt = {}
for x in full:
    cnt[len(x)] = cnt.get(len(x), 0) + 1
cache = {}
nconc = npairs = nclean = 0
mx = [0, 0, 0, 0, 0]
for x1 in full:
    for c1 in admissible(x1):
        for x2 in full:
            y, err, nc2, cl = check_concat_identities(x1, c1, x2, cache=cache)
            nconc += 1
            npairs += nc2
            nclean += cl
            for k in range(4):
                mx[k] = max(mx[k], err[k])
            mx[4] = max(mx[4], nrm(err))
print(f"part 2: FULL set, N1, N2 <= {NP}: {len(full)} bridges (per N {cnt}); {nconc} concatenations from coordinates, {npairs} ordered pairs ((x1,c1),(x2,c1'')), "
      f"{nclean} pairs of clean bridges: every identity of (a) and (b) holds; error maxima {tuple(mx[:4])}, norm {mx[4]}   [{time.time()-t0:.1f} s]", flush=True)

# ---------------------------------------------------------------- part 3
t0 = time.time()
rng = random.Random(SEED)


def grow(rng, L, drift, attract):
    """self-avoiding walk from the origin in the half space y > 0, grown bead by bead; weight of a free neighbour q of
       the last bead p:  exp(drift * (y_q - y_p) + attract * (#occupied neighbours of q - 1)).
       Stops (i) as soon as it has at least L beads and its last bead is at the largest height so far -- then the whole
       walk is a bridge whose top end sits on the surface of the blob -- or (ii) when it is trapped or has 2L beads;
       in case (ii) the piece up to the FIRST bead of maximal height is returned (a bridge as well)."""
    w = [(0, 0, 0)]
    occ = {(0, 0, 0)}
    ymax = 0
    while True:
        p = w[-1]
        if len(w) >= L and p[1] >= ymax:
            return w
        if len(w) >= 2 * L:
            break
        cand = []
        for q in ML.nbrs(p):
            if q in occ or q[1] <= 0:
                continue
            k = sum(1 for r in ML.nbrs(q) if r in occ) - 1
            cand.append((q, math.exp(drift * (q[1] - p[1]) + attract * k)))
        if not cand:
            break
        tot = sum(c[1] for c in cand)
        u = rng.random() * tot
        for q, wt in cand:
            u -= wt
            if u <= 0:
                break
        w.append(q)
        occ.add(q)
        ymax = max(ymax, q[1])
    j = min(k for k, q in enumerate(w) if q[1] == ymax)
    return w[:j + 1]


bridges = []
tries = 0
while len(bridges) < NRAND:
    tries += 1
    L = rng.choice([30, 60, 120, 250, 500, 1000, 2000, 4000])
    x = grow(rng, L, rng.choice([0.0, 0.0, 0.05, 0.2]), rng.choice([0.0, 0.3, 0.7, 1.2, 2.0]))
    if len(x) >= 12:
        check_bridge(x)
        bridges.append(x)
lens = sorted(len(x) for x in bridges)
info = []
nA = nB = ncl = 0
maxA = [0, 0, 0, 0]
maxB = [0, 0, 0, 0]
for x in bridges:
    idx = index_of(x)
    Bx = B_of(x, idx)
    As = [A_of(x, c, idx) for c in admissible(x)]
    nA += any(a != (0, 0, 0, 0) for a in As)
    nB += Bx != (0, 0, 0, 0)
    ncl += is_clean(x, idx)
    for a in As:
        for k in range(4):
            maxA[k] = max(maxA[k], a[k])
    for k in range(4):
        maxB[k] = max(maxB[k], Bx[k])
print(f"part 3: {len(bridges)} random bridges from {tries} walks (seed {SEED}); beads: min {lens[0]}, median {lens[len(lens)//2]}, max {lens[-1]}, "
      f"{sum(1 for l in lens if l >= 1000)} with >= 1000; with A != 0: {nA}, with B != 0: {nB}, clean as they stand: {ncl}; max A {tuple(maxA)}, max B {tuple(maxB)}", flush=True)

# (c) cleaning, every admissible c1; profiles by the hash count, and by the k-d tree count as a second method
ncase = 0
nfail_13 = nfail_22 = 0
hgc = {}
for x in bridges:
    idx = index_of(x)
    hx = ML.profile_hash(x)
    hgc[id(x)] = hx
    Bx = B_of(x, idx)
    for c1 in admissible(x):
        Ax = A_of(x, c1, idx)
        qh = vadd(hx, Ax, Bx)
        xh = extend(x, c1, 2, 3)
        check_bridge(xh)
        assert len(xh) == len(x) + 5
        hh = ML.profile_hash(xh)
        assert hh == qh, ("(h,g)(x-hat) != q-hat", hh, qh)
        if len(xh) <= 3000:
            assert ML.profile_kdtree(xh) == hh
        assert is_clean(xh), "head 2 + tail 3 is not clean"
        ncase += 1
        nfail_13 += not is_clean(extend(x, c1, 1, 3))
        nfail_22 += not is_clean(extend(x, c1, 2, 2))
print(f"   (c): {ncase} pairs (bridge, c1): head 2 + tail 3 is a clean bridge with (h,g) = q-hat in every case; "
      f"head 1 + tail 3 not clean in {nfail_13}, head 2 + tail 2 not clean in {nfail_22}   [{time.time()-t0:.1f} s]", flush=True)

# (a) random ordered pairs
t0 = time.time()
npr = 0
ncl2 = 0
nerr = 0
longest = 0
for _ in range(3 * NRAND):
    x1 = rng.choice(bridges)
    x2 = rng.choice(bridges)
    c1 = rng.choice(admissible(x1))
    y, err, nc2, cl = check_concat_identities(x1, c1, x2)
    npr += 1
    ncl2 += cl
    nerr += err != (0, 0, 0, 0)
    longest = max(longest, len(y))
print(f"   (a): {npr} random ordered pairs concatenated from coordinates (longest concatenation {longest} beads): every identity holds; "
      f"nonzero error vector in {nerr}; both bridges clean in {ncl2}   [{time.time()-t0:.1f} s]", flush=True)

# six-fold self-concatenation
t0 = time.time()
nself = 0
for x in rng.sample(bridges, min(40, len(bridges))):
    if len(x) > 1500:
        continue
    idx = index_of(x)
    c1 = rng.choice(admissible(x))
    Ax, Bx, hx = A_of(x, c1, idx), B_of(x, idx), ML.profile_hash(x)
    y = list(x)
    c = c1
    for k in range(5):
        y, g = concat(y, c, x)
        c = act(g, c1)          # the image of the same c1 under the symmetry that carried the last copy
    check_bridge(y)
    assert len(y) == 6 * len(x) + 15
    hy = ML.profile_hash(y)
    assert hy == tuple(6 * hx[i] + 5 * (Ax[i] + Bx[i]) for i in range(4)), "six-fold self-concatenation"
    nself += 1
print(f"   {nself} six-fold self-concatenations (same c1 carried along): (h,g) = 6 (h,g)(x) + 5 (A + B) exactly   [{time.time()-t0:.1f} s]")
