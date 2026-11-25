#!/usr/bin/env python3
"""Assistant B — own checks around Lemma 11.68 for findings m1 and m3 of SCI-REV-0002 (own code, mylat.py).

(1) m1: appending k = 1..5 beads to a bridge in the zigzag of the linker (l1 = P + c1, l2 = l1 + b, l3 = l2 + c1,
    l4 = l3 + b, l5 = l4 + c1; c1 = b' if b' is an up-bond, any up-bond out of P otherwise) gives a bridge whose
    (h3,h8,h11,g) exceeds that of the bridge by a vector in [0,1]x[0,6]x[0,10]x[0,1] of norm <= 28, 42, 44, 44, 44.
    Direct test: profile of the extended walk from coordinates, all bridges with at most NMAX1 beads.
(2) m3: the error vector of the concatenation is A(x1, c1) + B(x2) (linker-S1 pairs, linker-S2 pairs, minus chain
    neighbours; delta_g = [b' is a down-bond]).  (a) the decomposition and the lemma are tested by REAL concatenations
    (own implementation: unique height-preserving signed permutation, bridge, counts from coordinates) on all pairs
    with N1, N2 <= NPAIR and on random pairs; (b) the maxima of A and of B over all single bridges with at most
    NMAX2 beads give the exhaustive maxima over all pairs with N1, N2 <= NMAX2.
usage: concat_check.py NMAX1 NPAIR NMAX2 [NA [NB]]
       NA, NB (optional): A-part over bridges with at most NA beads, B-part over bridges with at most NB beads
       (for the reviewer's rows "N1 <= 16, N2 <= 8" and the reverse)
"""
import sys, itertools, random, time
sys.dont_write_bytecode = True
import mylat as ML

D = ML._disp()
PERMS = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        PERMS.append((perm, sg))


def act(g, v):
    perm, sg = g
    return (sg[0] * v[perm[0]], sg[1] * v[perm[1]], sg[2] * v[perm[2]])


def add(p, q):
    return (p[0] + q[0], p[1] + q[1], p[2] + q[2])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def up_bonds_out_of(p):
    return [sub(q, p) for q in ML.nbrs(p) if q[1] > p[1]]


def c1_choices(x):
    P = x[-1]
    b = sub(x[-1], x[-2])
    bp = sub(x[-2], x[-3])
    assert b[1] == 1
    if bp[1] == 1:
        return [bp], b, 0
    return up_bonds_out_of(P), b, 1


def zigzag(x, c1, b, k):
    out = []
    p = x[-1]
    for j in range(k):
        p = add(p, c1 if j % 2 == 0 else b)
        out.append(p)
    return out


def cross_counts(link, S):
    """number of pairs (linker site, site of S) at squared distance 3, 8, 11"""
    c = [0, 0, 0]
    for l in link:
        for t, d in enumerate((3, 8, 11)):
            for v in D[d]:
                if (l[0] + v[0], l[1] + v[1], l[2] + v[2]) in S:
                    c[t] += 1
    return c


def A_part(x, S, c1, b, dg, k=3):
    link = zigzag(x, c1, b, k)
    c = cross_counts(link, S)
    return (c[0] - 1, c[1] - (2 if k >= 2 else 1), c[2], dg)


def B_part(x, S):
    u1 = sub(x[1], x[0])
    u2 = sub(x[2], x[1])
    assert u1[1] == 1 and u2[1] == 1
    l3 = sub(x[0], u2)
    l2 = sub(l3, u1)
    l1 = sub(l2, u2)
    c = cross_counts([l1, l2, l3], S)
    return (c[0] - 1, c[1] - 2, c[2], 0)


def concat(x1, x2, c1, b):
    l = zigzag(x1, c1, b, 3)
    Q = add(l[2], b)
    u1 = sub(x2[1], x2[0])
    u2 = sub(x2[2], x2[1])
    gs = [g for g in PERMS if act(g, (0, 1, 0)) == (0, 1, 0) and act(g, u1) == c1 and act(g, u2) == b]
    gs_all = [g for g in PERMS if act(g, u1) == c1 and act(g, u2) == b and act(g, (0, 1, 0))[1] == 1]
    assert len(gs) == 1 and len(gs_all) == 1, (len(gs), len(gs_all))
    g = gs[0]
    img = [add(Q, act(g, sub(p, x2[0]))) for p in x2]
    return x1 + l + img


def nrm(d):
    return ML.cnorm(d[:3]) + abs(d[3])


if __name__ == "__main__":
    NMAX1, NPAIR, NMAX2 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    NA = int(sys.argv[4]) if len(sys.argv) > 4 else None
    NB = int(sys.argv[5]) if len(sys.argv) > 5 else None
    t0 = time.time()
    # ---------- (1) appending k beads
    mx = {k: [0, 0, 0, 0, 0] for k in range(1, 6)}
    mn = {k: [0, 0, 0, 0] for k in range(1, 6)}
    cnt = 0
    for N in range(3, NMAX1 + 1):
        for x in ML.enum_bridges(N):
            hg0 = ML.profile_hash(x)
            S = set(x)
            cs, b, dg = c1_choices(x)
            for c1 in cs:
                for k in range(1, 6):
                    y = x + zigzag(x, c1, b, k)
                    assert ML.check_walk(y) is None and ML.is_bridge(y)
                    hg = ML.profile_hash(y)
                    d = tuple(hg[i] - hg0[i] for i in range(4))
                    assert d == A_part(x, S, c1, b, dg, k), (d, A_part(x, S, c1, b, dg, k))
                    cnt += 1
                    for i in range(4):
                        mx[k][i] = max(mx[k][i], d[i])
                        mn[k][i] = min(mn[k][i], d[i])
                    mx[k][4] = max(mx[k][4], nrm(d))
    print(f"(1) appending k beads in the linker zigzag, all bridges with 3..{NMAX1} beads, every admissible c1: {cnt} extended walks,")
    print("    each a self-avoiding bridge; cost vector from coordinates = linker/S1 count.  componentwise maxima (d3,d8,d11,dg | largest norm), minima:")
    for k in range(1, 6):
        print(f"      k = {k}: max {tuple(mx[k][:4])} | {mx[k][4]}   min {tuple(mn[k])}   (proved bounds: {[(1,3,6,1),(1,6,8,1),(1,6,10,1),(1,6,10,1),(1,6,10,1)][k-1]} | {[28,42,44,44,44][k-1]})")
    print("    time %.1f s" % (time.time() - t0), flush=True)
    # ---------- (2a) real concatenations
    t0 = time.time()
    br = {N: list(ML.enum_bridges(N)) for N in range(3, max(NPAIR, 11) + 1)}
    prof = {}
    def hgof(x):
        k = tuple(x)
        if k not in prof:
            prof[k] = ML.profile_hash(x)
        return prof[k]
    npairs = 0
    nconc = 0
    mxd = [0, 0, 0, 0, 0]
    def one(x1, x2):
        global nconc
        cs, b, dg = c1_choices(x1)
        S1 = set(x1)
        Bp = B_part(x2, set(x2))
        for c1 in cs:
            y = concat(x1, x2, c1, b)
            assert len(y) == len(x1) + len(x2) + 3
            assert ML.check_walk(y) is None and ML.is_bridge(y)
            hg = ML.profile_hash(y)
            h1, h2 = hgof(x1), hgof(x2)
            d = tuple(hg[i] - h1[i] - h2[i] for i in range(4))
            Ap = A_part(x1, S1, c1, b, dg)
            assert d == tuple(Ap[i] + Bp[i] for i in range(4)), (d, Ap, Bp)
            assert 0 <= d[0] <= 1 and 0 <= d[1] <= 9 and 0 <= d[2] <= 14 and d[3] == dg
            nconc += 1
            for i in range(4):
                mxd[i] = max(mxd[i], d[i])
            mxd[4] = max(mxd[4], nrm(d))
    for N1 in range(3, NPAIR + 1):
        for N2 in range(3, NPAIR + 1):
            for x1 in br[N1]:
                for x2 in br[N2]:
                    one(x1, x2)
                    npairs += 1
    rng = random.Random(20261125)
    nrand = 3000
    for _ in range(nrand):
        N1 = rng.randint(3, 11)
        N2 = rng.randint(3, 11)
        one(rng.choice(br[N1]), rng.choice(br[N2]))
    print(f"(2a) real concatenations: all {npairs} ordered pairs with 3 <= N1, N2 <= {NPAIR} and {nrand} random pairs with N1, N2 <= 11 (seed 20261125):")
    print(f"     {nconc} concatenations (both c1 where free); in every case exactly one height-preserving signed permutation, a self-avoiding bridge with N1+N2+3 beads,")
    print(f"     error vector = A(x1,c1) + B(x2), inside [0,1]x[0,9]x[0,14], delta_g = [b' down].  maxima {tuple(mxd[:4])}, largest norm {mxd[4]}")
    print("     time %.1f s" % (time.time() - t0), flush=True)
    # ---------- (2b) exhaustive maxima through the decomposition
    t0 = time.time()

    def scan(nmaxA, nmaxB):
        mA = [0, 0, 0, 0, 0]
        mB = [0, 0, 0, 0, 0]
        first_d3 = None
        nb = {}
        n_d3 = {}
        for N in range(3, max(nmaxA, nmaxB) + 1):
            c = 0
            for x in ML.enum_bridges(N):
                c += 1
                S = set(x)
                if N <= nmaxA:
                    cs, b, dg = c1_choices(x)
                    for c1 in cs:
                        Ap = A_part(x, S, c1, b, dg)
                        assert min(Ap) >= 0
                        for i in range(4):
                            mA[i] = max(mA[i], Ap[i])
                        mA[4] = max(mA[4], 9 * Ap[0] + 4 * Ap[1] + Ap[2] + Ap[3])
                        if Ap[0] == 1:
                            n_d3[N] = n_d3.get(N, 0) + 1
                            if first_d3 is None:
                                first_d3 = (N, list(x), c1)
                if N <= nmaxB:
                    Bp = B_part(x, S)
                    assert min(Bp) >= 0
                    for i in range(4):
                        mB[i] = max(mB[i], Bp[i])
                    mB[4] = max(mB[4], 9 * Bp[0] + 4 * Bp[1] + Bp[2])
            nb[N] = c
        return mA, mB, first_d3, nb, n_d3

    mA, mB, first_d3, nb, n_d3 = scan(NMAX2, NMAX2)
    tot = sum(nb.values())
    print(f"(2b) decomposition, all bridges from the origin with 3..{NMAX2} beads ({tot} bridges; {tot*tot} ordered pairs, x4 with the other sublattice/orientation conventions):")
    print(f"     A-part (linker against x1): componentwise maxima {tuple(mA[:4])}, largest norm {mA[4]};  B-part (linker against x2): {tuple(mB[:4])}, largest norm {mB[4]}")
    print(f"     => over all pairs: componentwise maxima {tuple(mA[i]+mB[i] for i in range(4))}, largest norm {mA[4]+mB[4]}   (reviewer, N <= 13: (1, 6, 8, 1), norm 41)")
    print(f"     delta_3 = 1 first occurs at N1 = {first_d3[0] if first_d3 else None}; number of (x1, c1) with delta_3 = 1 per N1: {n_d3}")
    if first_d3:
        print(f"     smallest example: x1 = {first_d3[1]}, c1 = {first_d3[2]}")
    print("     bridges per N:", nb)
    print("     time %.1f s" % (time.time() - t0), flush=True)
    if NA is not None:
        t0 = time.time()
        for (na, nbb) in ((NA, NB), (NB, NA)):
            mA, mB, _, nbr, _ = scan(na, nbb)
            print(f"(2c) N1 <= {na}, N2 <= {nbb}: A max {tuple(mA[:4])} norm {mA[4]}; B max {tuple(mB[:4])} norm {mB[4]}; "
                  f"pairs: maxima {tuple(mA[i]+mB[i] for i in range(4))}, largest norm {mA[4]+mB[4]}   [{time.time()-t0:.0f} s]", flush=True)
