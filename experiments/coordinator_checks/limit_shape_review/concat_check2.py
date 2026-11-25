#!/usr/bin/env python3
"""Assistant B — (i) real concatenations for every (x1, c1) with delta_3 = 1, N1 = 12, 13, against all bridges x2
with 3..6 beads: the error vector from coordinates, the decomposition, the lemma's intervals;
(ii) the reviewer's rows "N1 <= 16, N2 <= 8" and "N1 <= 8, N2 <= 16" through the decomposition."""
import sys, time
sys.dont_write_bytecode = True
import mylat as ML
import concat_check as C

t0 = time.time()
x2s = [x for N in range(3, 7) for x in ML.enum_bridges(N)]
B2 = [(x, C.B_part(x, set(x)), ML.profile_hash(x)) for x in x2s]
n = 0
mx = [0, 0, 0, 0, 0]
for N in (12, 13):
    for x1 in ML.enum_bridges(N):
        cs, b, dg = C.c1_choices(x1)
        S1 = set(x1)
        for c1 in cs:
            Ap = C.A_part(x1, S1, c1, b, dg)
            if Ap[0] != 1:
                continue
            h1 = ML.profile_hash(x1)
            for x2, Bp, h2 in B2:
                y = C.concat(x1, x2, c1, b)
                assert ML.check_walk(y) is None and ML.is_bridge(y) and len(y) == len(x1) + len(x2) + 3
                hg = ML.profile_hash(y)
                d = tuple(hg[i] - h1[i] - h2[i] for i in range(4))
                assert d == tuple(Ap[i] + Bp[i] for i in range(4)) and d[0] == 1
                assert d[1] <= 9 and d[2] <= 14 and d[3] == dg
                n += 1
                for i in range(4):
                    mx[i] = max(mx[i], d[i])
                mx[4] = max(mx[4], C.nrm(d))
print(f"(i) {n} real concatenations with delta_3 = 1 (every (x1, c1) with N1 = 12, 13 and A-part delta_3 = 1, against all {len(x2s)} bridges x2 with 3..6 beads):")
print(f"    each a self-avoiding bridge, error vector from coordinates = A + B, delta_3 = 1 in all; maxima {tuple(mx[:4])}, largest norm {mx[4]}   [{time.time()-t0:.0f} s]", flush=True)

t0 = time.time()
mA = {}
mB = {}
curA = [0, 0, 0, 0, 0]
curB = [0, 0, 0, 0, 0]
for N in range(3, 17):
    for x in ML.enum_bridges(N):
        S = set(x)
        cs, b, dg = C.c1_choices(x)
        for c1 in cs:
            Ap = C.A_part(x, S, c1, b, dg)
            for i in range(4):
                if Ap[i] > curA[i]:
                    curA[i] = Ap[i]
            v = 9 * Ap[0] + 4 * Ap[1] + Ap[2] + Ap[3]
            if v > curA[4]:
                curA[4] = v
        Bp = C.B_part(x, S)
        for i in range(4):
            if Bp[i] > curB[i]:
                curB[i] = Bp[i]
        v = 9 * Bp[0] + 4 * Bp[1] + Bp[2]
        if v > curB[4]:
            curB[4] = v
    mA[N] = list(curA)
    mB[N] = list(curB)
    print(f"    N <= {N:2d}: A max {tuple(curA[:4])} norm {curA[4]};  B max {tuple(curB[:4])} norm {curB[4]}   [{time.time()-t0:.0f} s]", flush=True)
for na, nb in ((13, 13), (16, 8), (8, 16), (16, 16)):
    print(f"(ii) N1 <= {na}, N2 <= {nb}: componentwise maxima {tuple(mA[na][i] + mB[nb][i] for i in range(4))}, largest norm {mA[na][4] + mB[nb][4]}")
print("     reviewer: (13,13): (1,6,8,1) norm 41;  (16,8): (1,6,9,1) norm 43;  (8,16): (0,3,5,1) norm 18")
