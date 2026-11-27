#!/usr/bin/env python3
"""Assistant B — a test for request T-4 of SCI-REV-0006 (can Lemma 11.68 be sharpened to an exact semigroup?).

Sub-family S of bridges: b' (the bond before the last) is an up-bond, A(x, c1) = (0,0,0,0) and B(x) = (0,0,0,0)
(no pair between the linker and the bridge beyond the chain neighbours, at either end).
Claims tested by REAL concatenations (own code, counts from coordinates):
 (1) for x1, x2 in S the concatenation of Lemma 11.68 has (h,g) = (h,g)(x1) + (h,g)(x2) EXACTLY and is again in S;
 (2) every bridge x becomes a member of S by a head and a tail of 5 beads each in the all-trans zigzag
     (N + 10 beads, (h,g) changed by a bounded vector).
So {((h,g)(x), N(x)+3) : x in S} is an additive semigroup of lattice points in Z^4 x N with the same limit shape.
"""
import sys, random, time
sys.dont_write_bytecode = True
import mylat as ML
import concat_check as C

def head(x, k):
    """prepend k beads below the first bead, continuing the zigzag of the first two bonds backwards"""
    u1 = C.sub(x[1], x[0]); u2 = C.sub(x[2], x[1])
    out = []; p = x[0]
    for j in range(k):
        p = C.sub(p, u2 if j % 2 == 0 else u1)
        out.append(p)
    return out[::-1]

def in_S(x):
    cs, b, dg = C.c1_choices(x)
    if dg != 0:
        return False
    S = set(x)
    return C.A_part(x, S, cs[0], b, dg) == (0, 0, 0, 0) and C.B_part(x, S) == (0, 0, 0, 0)

t0 = time.time()
rng = random.Random(7)
members = []
nb = 0; maxchange = [0, 0, 0, 0]; minchange = [0, 0, 0, 0]
frac = {}
for N in range(3, 11):
    tot = 0; ins = 0
    for x in ML.enum_bridges(N):
        nb += 1; tot += 1
        ins += in_S(x)
        cs, b, dg = C.c1_choices(x)
        for c1 in cs:
            y = head(x, 5) + x + C.zigzag(x, c1, b, 5)
            assert ML.check_walk(y) is None and ML.is_bridge(y) and len(y) == N + 10
            assert in_S(y), "head+tail does not put the bridge into S"
            if N <= 9 or rng.random() < 0.2:
                h0 = ML.profile_hash(x); h1 = ML.profile_hash(y)
                d = [h1[i] - h0[i] for i in range(4)]
                for i in range(4):
                    maxchange[i] = max(maxchange[i], d[i]); minchange[i] = min(minchange[i], d[i])
                if rng.random() < 0.03:
                    members.append(y)
    frac[N] = (ins, tot)
print(f"(2) all {nb} bridges with 3..10 beads, every admissible c1: head and tail of 5 zigzag beads give a bridge in S; change of (h,g): min {minchange}, max {maxchange}")
print("    bridges that are in S as they stand (in S, all) per N:", frac)
members += [x for N in range(3, 9) for x in ML.enum_bridges(N) if in_S(x)]
print(f"    test set: {len(members)} members of S (with 3..20 beads)")
n = 0
for _ in range(20000):
    x1 = rng.choice(members); x2 = rng.choice(members)
    cs, b, dg = C.c1_choices(x1)
    y = C.concat(x1, x2, cs[0], b)
    assert ML.check_walk(y) is None and ML.is_bridge(y) and len(y) == len(x1) + len(x2) + 3
    h = ML.profile_hash(y); h1 = ML.profile_hash(x1); h2 = ML.profile_hash(x2)
    assert tuple(h[i] - h1[i] - h2[i] for i in range(4)) == (0, 0, 0, 0), "not exactly additive"
    assert in_S(y), "concatenation left S"
    n += 1
print(f"(1) {n} random ordered pairs of members: the concatenation is a bridge with N1+N2+3 beads, (h,g) EXACTLY additive, and again in S")
print("time %.1f s" % (time.time() - t0))
