#!/usr/bin/env python3
"""R9, item 4: the semigroup statements on LONG bridges and on special ones (own code, r9_lat.py).

(T0) cross-check of r9_lat.py against the O(n^2) definition and against the counts of r9_semi.c (clean bridges per N).
(T1) random long bridges cut out of random walks with dense ends (sizes up to a few thousand beads): how many are clean; the
     end corrections A, B; cleaning by head 2 + tail 3 and by head 5 + tail 5.
(T2) random ordered pairs of long bridges, clean or not: real concatenation from coordinates;
       error = A(x1,c1) + B(x2);  ends inherited;  qhat = (h,g)+A+B exactly additive;  for clean pairs (h,g) additive, clean.
(T3) k-fold self-concatenation: (h,g)(x^k) = k (h,g)(x) + (k-1)(A+B), hence ((h,g)+A+B)/(N+3) is the limit density.
(T4) the all-gauche helix and the rod: bridge, counts, clean or not.
(T5) explicit clean bridges whose vectors (h3,h8,h11,g; N+3) generate Z^5 (determinant +-1), with coordinates.
"""
import sys, random, time, itertools
sys.dont_write_bytecode = True
import r9_lat as L

rng = random.Random(20261126)
t0 = time.time()
P = lambda *a: (print(*a), sys.stdout.flush())

# ---------------------------------------------------------------- T0
cnt = {}
for n in range(3, 12):
    tot = cl = 0
    for x in L.enum_bridges(n):
        tot += 1
        assert L.check_walk(x) is None and L.is_bridge(x)
        if n <= 9:
            assert L.profile(x) == L.profile_brute(x)
        cl += L.is_clean(x)
    cnt[n] = (tot, cl)
P("(T0) bridges and clean bridges per N (first two bonds fixed):", cnt)
P("     r9_semi.c: 3:(1,1) 4:(2,2) 5:(5,4) 6:(12,10) 7:(29,24) 8:(78,64) 9:(201,159) 10:(536,420) 11:(1433,1115)")
assert cnt == {3: (1, 1), 4: (2, 2), 5: (5, 4), 6: (12, 10), 7: (29, 24), 8: (78, 64), 9: (201, 159), 10: (536, 420), 11: (1433, 1115)}

# ---------------------------------------------------------------- T1
pool = []
sizes = []
stats = {"n": 0, "clean": 0, "topclean": 0, "botclean": 0, "bpdown": 0}
maxA = [0, 0, 0, 0]; maxB = [0, 0, 0]
t1 = time.time()
def scheduled_walk(n, rng, blob=80, beta_blob=1.6, beta_mid=0.3, drift_mid=0.15):
    """growth walk with a schedule: a dense blob (strong contact bias, no drift), a long drifting middle part, a dense blob.
    One-step look-ahead (a candidate with no free neighbour is avoided unless it is the only choice).  Not uniform."""
    w = [(0, 0, 0)]
    occ = {(0, 0, 0)}
    near = L.DISP[3] + L.DISP[8]
    while len(w) < n:
        k = len(w)
        inblob = k < blob or k >= n - blob
        beta, drift = (beta_blob, 0.0) if inblob else (beta_mid, drift_mid)
        cand = [q for q in L.nbrs(w[-1]) if q not in occ]
        if not cand:
            break
        live = [q for q in cand if any(r not in occ for r in L.nbrs(q))]
        if live:
            cand = live
        ws = []
        for q in cand:
            c = sum(1 for v in near if (q[0] + v[0], q[1] + v[1], q[2] + v[2]) in occ)
            ws.append(pow(2.718281828, beta * c + drift * (q[1] - w[-1][1])))
        r = rng.random() * sum(ws)
        for q, wt in zip(cand, ws):
            r -= wt
            if r <= 0:
                break
        w.append(q); occ.add(q)
    return w


for target, beta, drift, reps in ((60, 1.2, 0.0, 600), (200, 1.5, 0.05, 300), (800, 1.5, 0.02, 60), (1500, -1, 0, 60), (4000, -1, 0, 40)):
    for _ in range(reps):
        if beta < 0:
            w = scheduled_walk(target, rng, blob=int(rng.choice([40, 80, 150])), beta_blob=rng.choice([1.2, 1.6, 2.2]),
                               beta_mid=rng.choice([0.0, 0.3, 0.8]), drift_mid=rng.choice([0.08, 0.15, 0.3]))
        else:
            w = L.random_compact_walk(target, rng, beta=beta, drift=drift)
        br = L.bridge_of(w)
        if br is None or len(br) < 8:
            continue
        assert L.check_walk(br) is None and L.is_bridge(br)
        idx = {p: i for i, p in enumerate(br)}
        cs = L.admissible_c1(br)
        Bv = L.B_part(br, idx)
        hg = L.profile(br)
        stats["n"] += 1
        stats["bpdown"] += len(cs) == 2
        stats["botclean"] += Bv == (0, 0, 0, 0)
        tc = False
        for c1 in cs:
            Av = L.A_part(br, c1, idx)
            for i in range(4):
                maxA[i] = max(maxA[i], Av[i])
            if len(cs) == 1 and Av == (0, 0, 0, 0):
                tc = True
            # cleaning
            for kh, kt in ((2, 3), (5, 5)):
                y = L.extend(br, c1, kh, kt)
                assert L.check_walk(y) is None and L.is_bridge(y) and len(y) == len(br) + kh + kt
                assert L.is_clean(y), "cleaning failed"
                hy = L.profile(y)
                d = tuple(hy[i] - hg[i] for i in range(4))
                if kh >= 3:
                    assert d == tuple(Av[i] + Bv[i] for i in range(4)), (d, Av, Bv)
                else:
                    assert all(0 <= d[i] <= Av[i] + Bv[i] for i in range(4)) and d[3] == Av[3]
            pool.append((br, c1, hg, Av, Bv))
        for i in range(3):
            maxB[i] = max(maxB[i], Bv[i])
        stats["topclean"] += tc
        stats["clean"] += tc and Bv == (0, 0, 0, 0)
        sizes.append(len(br))
sizes.sort()
P(f"(T1) {stats['n']} random bridges cut out of random compact walks; sizes: min {sizes[0]}, median {sizes[len(sizes)//2]}, max {sizes[-1]};"
  f" {sum(1 for s in sizes if s >= 300)} with >= 300 beads, {sum(1 for s in sizes if s >= 1000)} with >= 1000")
P(f"     clean as they stand: {stats['clean']} (top-clean {stats['topclean']}, bottom-clean {stats['botclean']}, b' down {stats['bpdown']});"
  f"  maxima: A = {tuple(maxA)}, B = {tuple(maxB)}")
P(f"     every (bridge, c1) becomes clean with head 2 + tail 3 and with head 5 + tail 5; cost = A + B (head >= 3) / <= A + B (head 2)   [{time.time()-t1:.0f} s]")

# ---------------------------------------------------------------- T2
t1 = time.time()
npair = 0; nclean = 0; maxlen = 0; maxerr = [0, 0, 0, 0]
longpool = [p for p in pool if len(p[0]) >= 300]
for it in range(1500):
    x1, c1, h1, A1, B1 = rng.choice(longpool if it % 2 == 0 else pool)
    x2, c2, h2, A2, B2 = rng.choice(longpool if it % 3 == 0 else pool)
    if len(x1) + len(x2) > 9000:
        continue
    y, g = L.concat(x1, x2, c1)
    assert len(y) == len(x1) + len(x2) + 3 and L.check_walk(y) is None and L.is_bridge(y)
    hy = L.profile(y)
    err = tuple(hy[i] - h1[i] - h2[i] for i in range(4))
    assert err == tuple(A1[i] + B2[i] for i in range(4)), (err, A1, B2)
    idx = {p: i for i, p in enumerate(y)}
    assert L.B_part(y, idx) == B1
    assert L.A_part(y, L._gact(g, c2), idx) == A2
    q1 = tuple(h1[i] + A1[i] + B1[i] for i in range(4)); q2 = tuple(h2[i] + A2[i] + B2[i] for i in range(4))
    qy = tuple(hy[i] + A2[i] + B1[i] for i in range(4))
    assert qy == tuple(q1[i] + q2[i] for i in range(4))
    if A1 == (0, 0, 0, 0) and B1 == (0, 0, 0, 0) and A2 == (0, 0, 0, 0) and B2 == (0, 0, 0, 0):
        assert err == (0, 0, 0, 0) and L.is_clean(y)
        nclean += 1
    for i in range(4):
        maxerr[i] = max(maxerr[i], err[i])
    npair += 1; maxlen = max(maxlen, len(y))
P(f"(T2) {npair} random ordered pairs of these bridges (longest concatenation {maxlen} beads): error = A(x1,c1) + B(x2), ends inherited,"
  f" qhat additive, in all; {nclean} pairs of clean bridges: exactly additive and clean.  largest error vector {tuple(maxerr)}   [{time.time()-t1:.0f} s]")

# ---------------------------------------------------------------- T3
t1 = time.time()
nk = 0
for _ in range(25):
    x, c1, h, A, B = rng.choice([p for p in pool if len(p[0]) <= 400])
    y = list(x); cy = c1
    k = 6
    for r in range(k - 1):
        y, g = L.concat(y, x, cy)
        cy = L._gact(g, c1)
    hy = L.profile(y)
    assert len(y) == k * len(x) + 3 * (k - 1)
    assert hy == tuple(k * h[i] + (k - 1) * (A[i] + B[i]) for i in range(4)), (hy, h, A, B)
    nk += 1
P(f"(T3) {nk} bridges concatenated with themselves 6 times: (h,g) = 6 (h,g) + 5 (A + B) exactly   [{time.time()-t1:.0f} s]")

# ---------------------------------------------------------------- T4
for n in (4, 5, 8, 12, 50, 200, 1001):
    hx = L.helix(n)
    assert L.check_walk(hx) is None and L.is_bridge(hx)
    hg = L.profile(hx)
    assert hg == (0, 0, n - 3, n - 3), hg
    cs = L.admissible_c1(hx)
    r = L.rod(n)
    assert L.check_walk(r) is None and L.is_bridge(r) and L.profile(r) == (0, 0, 0, 0) and L.is_clean(r)
    if n in (8, 200, 1001):
        P(f"(T4) helix with {n} beads: bridge, (h,g) = {hg}; b' up: {len(cs) == 1}; A = {L.A_part(hx, cs[0])}, B = {L.B_part(hx)}; clean: {L.is_clean(hx)};"
          f"  exact point of K^br: ((h,g)+A+B)/(N+3) = {tuple(round((hg[i] + L.A_part(hx, cs[0])[i] + L.B_part(hx)[i]) / (n + 3), 5) for i in range(4))}")
P("     rods with 4..1001 beads: bridges, (h,g) = 0, clean")

# ---------------------------------------------------------------- T5
want = {}
found = {}
vecs = {}
for n in range(3, 13):
    for x in L.enum_bridges(n):
        if L.is_clean(x):
            v = L.profile(x) + (n + 3,)
            vecs.setdefault(v, x)
import numpy as np
V = sorted(vecs)
best = None
rg = np.random.default_rng(3)
arr = np.array(V, dtype=np.int64)
small = arr[arr[:, 4] <= 15]
for _ in range(400000):
    ids = rg.choice(len(small), size=5, replace=False)
    M = small[ids]
    d = round(float(np.linalg.det(M)))
    if abs(d) == 1:
        from sympy import Matrix
        if abs(Matrix(M.tolist()).det()) == 1:
            tot = int(M[:, 4].sum())
            if best is None or tot < best[0]:
                best = (tot, [tuple(int(t) for t in r) for r in M])
P("(T5) five clean bridges whose (h3,h8,h11,g; N+3) have determinant +-1 (exact, sympy), smallest total size found:")
for v in best[1]:
    P(f"     {v}:  {vecs[v]}")
M4 = None
for _ in range(400000):
    ids = rg.choice(len(small), size=4, replace=False)
    M = small[ids][:, [0, 1, 2, 4]]
    if abs(round(float(np.linalg.det(M)))) == 1:
        from sympy import Matrix
        if abs(Matrix(M.tolist()).det()) == 1:
            M4 = [tuple(int(t) for t in r) for r in small[ids]]
            break
P("     four of them whose (h3,h8,h11; N+3) have determinant +-1:", M4)
P(f"total time {time.time()-t0:.0f} s")
