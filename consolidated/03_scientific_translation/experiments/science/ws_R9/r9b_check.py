#!/usr/bin/env python3
"""R9 follow-up (b): Proposition 11.69b of the theory report (theory commit 24a3c27) against Theorem R9.1.

OWN CODE (r9_lat.py, written in the first round from the Setting paragraph of section 11.22 and the statement of
Lemma 11.68) throughout.  The only foreign code is in part A: the theory division's membership test `in_S` (their
mylat.py and concat_check.py, imported read-only from the export, no bytecode written) is evaluated bridge by bridge
next to mine.

A. Definition.  All bridges from the origin WITHOUT fixing the first two bonds (their normalisation), 3..NMAX_A beads:
   numbers of bridges, of bridges with (i) [bond before the last is an up-bond], of clean bridges by three tests —
   mine (R9.1: b' up, A = 0, B = 0), theirs (their code), and the "rod test" of their second implementation written
   with my code (a three-bead bridge concatenated above, or below, changes (h,g) by nothing) — the number of
   bridges on which the tests disagree, and how often (ii), (iii) fail when (i) holds.
B. Exactness.  (B1) real concatenations (Lemma 11.68) of ALL ordered pairs of clean bridges with at most NPAIR beads,
   their normalisation: self-avoiding bridge with N1+N2+3 beads, (h,g) exactly additive, clean.  (B2) all ordered
   pairs ((x1, c1), x2) of ARBITRARY bridges with at most NPAIR beads: error = A(x1,c1) + B(x2); how many pairs of
   two non-clean bridges have error 0.
C. Heads and tails.  Zigzag head of kh and tail of kt beads, kh, kt in {1,2,3}, on every (bridge, admissible c1) with
   3..NMAX_C beads (their normalisation): how many become clean, the largest change of (h,g).  Then 11 and 12 beads
   (first two bonds fixed; head 2 + tail 2 and head 2 + tail 3 also counted directly without fixing them), an explicit
   12-bead bridge that head 2 + tail 2 does not clean, and a 38-bead bridge whose cleaning costs exactly (1,9,14;1),
   norm 60 (it needs out/extremal_raw.txt of the first round: the two extremal bridges found by r9_extremal.c).
D. Lattice.  Z-span of (h3,h8,h11,g; N+3) over the clean bridges with at most N beads, N = 3..NMAX_D: distinct vectors,
   largest h3, rank, index in Z^5 by my own integer row reduction; independent certificates: 5x5 minors with gcd 1 and
   five vectors with determinant 1 (my elimination and sympy).

Run from this directory:  python3 r9b_check.py > out/r9b_check.txt     (about 1.5 minutes)
E. Constants: arithmetic of the rates.

usage: r9b_check.py [NMAX_A [NPAIR [NMAX_D]]]      (defaults 12, 8, 12)
"""
import sys, itertools, math, time, random
sys.dont_write_bytecode = True
import r9_lat as L

THY = "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_24a3c27/experiments/coordinator_checks/limit_shape_review"
NMAX_A = int(sys.argv[1]) if len(sys.argv) > 1 else 12
NPAIR = int(sys.argv[2]) if len(sys.argv) > 2 else 8
NMAX_D = int(sys.argv[3]) if len(sys.argv) > 3 else 12
NMAX_C = 10


def P(*a):
    print(*a)
    sys.stdout.flush()


t00 = time.time()


def enum_all(n):
    """all bridges with n beads from the origin (an A site); the first two bonds are NOT fixed"""
    w = [(0, 0, 0)]
    occ = {(0, 0, 0)}

    def rec(maxy):
        if len(w) == n:
            if w[-1][1] >= maxy:
                yield list(w)
            return
        if w[-1][1] + (n - len(w)) < maxy:
            return
        for q in L.nbrs(w[-1]):
            if q in occ or q[1] <= 0:
                continue
            occ.add(q); w.append(q)
            yield from rec(max(maxy, q[1]))
            occ.discard(q); w.pop()
    yield from rec(0)


def norm(d):
    return 5 * abs(d[0]) + 3 * abs(d[0] + d[1]) + abs(d[0] + d[1] + d[2]) + abs(d[3])


def vadd(*vs):
    return tuple(sum(v[i] for v in vs) for i in range(4))


def vsub(a, b):
    return tuple(a[i] - b[i] for i in range(4))


# ------------------------------------------------------------------------------------------------ A
sys.path.insert(0, THY)
import mylat as TML            # the theory division's lattice module (THEIR code, read-only)
import concat_check as TC      # their concatenation helpers (THEIR code, read-only)


def their_in_S(x):
    """the membership test of their t4_semigroup.py / t4_head_tail.py, verbatim"""
    cs, b, dg = TC.c1_choices(x)
    if dg != 0:
        return False
    S = set(x)
    return TC.A_part(x, S, cs[0], b, dg) == (0, 0, 0, 0) and TC.B_part(x, S) == (0, 0, 0, 0)


ROD3 = L.rod(3)
assert L.is_bridge(ROD3) and L.profile(ROD3) == (0, 0, 0, 0)


def rod_test(x):
    """the definition of their second implementation (harness XVIII.7, t4_lattice_index.py), written with MY code"""
    if L.sub(x[-2], x[-3])[1] != 1:
        return False
    hx = L.profile(x)
    top, _ = L.concat(x, ROD3, L.admissible_c1(x)[0])
    bot, _ = L.concat(ROD3, x, L.admissible_c1(ROD3)[0])
    return L.profile(top) == hx and L.profile(bot) == hx


published = {3: (4, 4), 4: (8, 8), 5: (16, 20), 6: (40, 48), 7: (96, 116), 8: (256, 312), 9: (636, 804), 10: (1680, 2144)}
P("A. clean bridges; all bridges from the origin, first two bonds not fixed (the theory division's normalisation)")
P("    N  bridges  (i) holds  clean: mine  their in_S  rod test | tests disagree | (i) holds but (ii) fails, (iii) fails | published by them (clean, bridges)")
clean_by_N = {}
all_by_N = {}
ndis_total = 0
for N in range(3, NMAX_A + 1):
    tot = n_i = n_mine = n_theirs = n_rod = ndis = n_ii = n_iii = 0
    cl = []
    al = []
    for x in enum_all(N):
        assert L.check_walk(x) is None and L.is_bridge(x)
        assert TML.check_walk(x) is None and TML.is_bridge(x)
        tot += 1
        up = L.sub(x[-2], x[-3])[1] == 1
        mine = L.is_clean(x)
        th = their_in_S(x)
        rd = rod_test(x)
        n_i += up; n_mine += mine; n_theirs += th; n_rod += rd
        ndis += not (mine == th == rd)
        if up:
            n_ii += L.A_part(x, L.admissible_c1(x)[0]) != (0, 0, 0, 0)
            n_iii += L.B_part(x) != (0, 0, 0, 0)
        al.append(x)
        if mine:
            cl.append(x)
    clean_by_N[N] = cl
    all_by_N[N] = al
    ndis_total += ndis
    pub = published.get(N, "-")
    ok = "" if pub == "-" else ("  agrees" if pub == (n_mine, tot) else "  DIFFERS")
    P(f"   {N:2d}  {tot:6d}   {n_i:6d}      {n_mine:6d}     {n_theirs:6d}    {n_rod:6d}  |  {ndis:4d}          |  {n_ii:5d}, {n_iii:5d}                        | {pub}{ok}")
P(f"   bridges with 3..{NMAX_A} beads on which the three tests do not all agree: {ndis_total}      [{time.time()-t00:.0f} s]")

# ------------------------------------------------------------------------------------------------ B1
t0 = time.time()
pool = [(x, L.profile(x)) for N in range(3, NPAIR + 1) for x in clean_by_N[N]]
npair = nbrute = 0
fail = {"walk": 0, "bridge": 0, "additive": 0, "clean": 0}
for (x1, h1) in pool:
    c1 = L.admissible_c1(x1)[0]
    for (x2, h2) in pool:
        y, g = L.concat(x1, x2, c1)
        npair += 1
        if L.check_walk(y) is not None or len(y) != len(x1) + len(x2) + 3:
            fail["walk"] += 1
            continue
        if not L.is_bridge(y):
            fail["bridge"] += 1
        hy = L.profile(y)
        if hy != vadd(h1, h2):
            fail["additive"] += 1
        if not L.is_clean(y):
            fail["clean"] += 1
        if npair % 50 == 0:
            assert L.profile_brute(y) == hy
            nbrute += 1
P(f"\nB1. all {npair} ordered pairs of the {len(pool)} clean bridges with 3..{NPAIR} beads (first two bonds not fixed), real concatenations:")
P(f"    not a self-avoiding walk with N1+N2+3 beads: {fail['walk']}; not a bridge: {fail['bridge']}; (h,g) not exactly additive: {fail['additive']};"
  f" not clean: {fail['clean']}   (profile cross-checked against the O(n^2) definition on {nbrute} of them)   [{time.time()-t0:.0f} s]")

# ------------------------------------------------------------------------------------------------ B2
t0 = time.time()
left = []      # (x1, c1, profile, A(x1,c1), clean?)
right = []     # (x2, profile, B(x2), clean?)
for N in range(3, NPAIR + 1):
    for x in all_by_N[N]:
        hx = L.profile(x)
        cln = L.is_clean(x)
        right.append((x, hx, L.B_part(x), cln))
        for c1 in L.admissible_c1(x):
            left.append((x, c1, hx, L.A_part(x, c1), cln))
n2 = bad2 = 0
cat = {"both clean": [0, 0], "exactly one clean": [0, 0], "neither clean": [0, 0]}     # [pairs, pairs with error 0]
example = None
for (x1, c1, h1, A1, cl1) in left:
    for (x2, h2, B2, cl2) in right:
        y, g = L.concat(x1, x2, c1)
        assert L.check_walk(y) is None and L.is_bridge(y) and len(y) == len(x1) + len(x2) + 3
        err = vsub(L.profile(y), vadd(h1, h2))
        n2 += 1
        if err != vadd(A1, B2):
            bad2 += 1
        key = "both clean" if (cl1 and cl2) else ("neither clean" if not (cl1 or cl2) else "exactly one clean")
        cat[key][0] += 1
        if err == (0, 0, 0, 0):
            cat[key][1] += 1
            if key == "neither clean" and example is None:
                example = (x1, c1, x2, A1, L.B_part(x1), L.A_part(x2, L.admissible_c1(x2)[0]), B2)
P(f"\nB2. all {n2} ordered pairs ((x1, c1), x2) of arbitrary bridges with 3..{NPAIR} beads ({len(left)} pairs (bridge, c1), {len(right)} bridges):")
P(f"    error of the real concatenation different from A(x1, c1) + B(x2): {bad2}")
for k, v in cat.items():
    P(f"    {k:18s}: {v[0]:7d} pairs, error exactly 0 in {v[1]}")
k1 = sum(1 for t in left if not t[4] and t[3] == (0, 0, 0, 0))
k2 = sum(1 for t in right if not t[3] and t[2] == (0, 0, 0, 0))
P(f"    non-clean (x1, c1) with A(x1, c1) = 0: {k1};  non-clean x2 with B(x2) = 0: {k2};  product {k1 * k2}")
if example is not None:
    x1, c1, x2, A1, B1, A2, B2 = example
    P(f"    example of two NON-clean bridges with error 0: x1 ({len(x1)} beads) has A = {A1}, B = {B1}; x2 ({len(x2)} beads) has A = {A2}, B = {B2}")
    P(f"      x1 = {x1}")
    P(f"      x2 = {x2}")
P(f"    [{time.time()-t0:.0f} s]")

# ------------------------------------------------------------------------------------------------ C
t0 = time.time()
P(f"\nC. zigzag head of kh and tail of kt beads on every (bridge, admissible c1) with 3..{NMAX_C} beads (first two bonds not fixed)")
res = {(kh, kt): dict(tot=0, clean=0, mx_clean=[0, 0, 0, 0], mx_all=[0, 0, 0, 0], nrm=0, neq=0) for kh in (1, 2, 3) for kt in (1, 2, 3)}
for N in range(3, NMAX_C + 1):
    for x in all_by_N[N]:
        hx = L.profile(x)
        Bx = L.B_part(x)
        for c1 in L.admissible_c1(x):
            qhat = vadd(hx, L.A_part(x, c1), Bx)
            for (kh, kt), r in res.items():
                y = L.extend(x, c1, kh, kt)
                assert L.check_walk(y) is None and L.is_bridge(y) and len(y) == N + kh + kt
                r["tot"] += 1
                hy = L.profile(y)
                d = vsub(hy, hx)
                cln = L.is_clean(y)
                r["clean"] += cln
                r["neq"] += hy != qhat
                for i in range(4):
                    r["mx_all"][i] = max(r["mx_all"][i], d[i])
                    if cln:
                        r["mx_clean"][i] = max(r["mx_clean"][i], d[i])
                r["nrm"] = max(r["nrm"], norm(d))
P("   kh kt   clean / all     largest change of (h,g), componentwise, among the clean ones | among all | largest norm | (h,g) of the result differs from qhat = (h,g) + A + B")
for (kh, kt), r in sorted(res.items()):
    P(f"    {kh}  {kt}   {r['clean']:4d} / {r['tot']:4d}     {tuple(r['mx_clean'])}   |   {tuple(r['mx_all'])}   |   {r['nrm']:3d}   |   {r['neq']}")
P("   theirs (out_t4_head_tail.txt, equal lengths only): k = 1: 3832 of 3964, [0, 1, 4, 1];  k = 2 and 3: 3964 of 3964, [0, 2, 6, 1]")
P(f"   [{time.time()-t0:.0f} s]")

t0 = time.time()
first22 = None
for N in (11, 12):
    nb = 0
    nf = {(kh, kt): 0 for kh in (1, 2, 3) for kt in (1, 2, 3)}
    for x in L.enum_bridges(N):
        for c1 in L.admissible_c1(x):
            nb += 1
            for (kh, kt) in nf:
                y = L.extend(x, c1, kh, kt)
                if not L.is_clean(y):
                    nf[(kh, kt)] += 1
                    if (kh, kt) == (2, 2) and first22 is None:
                        first22 = (x, c1, y)
    P(f"   N = {N}, first two bonds FIXED (multiply by 4 for their normalisation): {nb} pairs (bridge, c1); NOT clean after head kh + tail kt:")
    P("        " + ";  ".join(f"{kh}+{kt}: {nf[(kh, kt)]}" for (kh, kt) in sorted(nf)))
for N in range(11, NMAX_A + 1):
    nb = n22 = n23 = 0
    for x in all_by_N[N]:
        for c1 in L.admissible_c1(x):
            nb += 1
            n22 += not L.is_clean(L.extend(x, c1, 2, 2))
            n23 += not L.is_clean(L.extend(x, c1, 2, 3))
    P(f"   N = {N}, first two bonds NOT fixed (their normalisation, counted directly): {nb} pairs (bridge, c1); head 2 + tail 2 NOT clean: {n22}; head 2 + tail 3 NOT clean: {n23}")
if first22 is not None:
    x, c1, y = first22
    idx = {p: i for i, p in enumerate(y)}
    cy = L.admissible_c1(y)[0]
    top = L.top_sites(y, cy, 3)
    spoil = []
    for j, s in enumerate(top, start=1):
        for d in (3, 8, 11):
            for v in L.DISP[d]:
                q = (s[0] + v[0], s[1] + v[1], s[2] + v[2])
                if q in idx and abs(len(y) - 1 + j - idx[q]) >= 3:
                    spoil.append((j, s, idx[q], q, d))
    H = x[-1][1]
    P(f"   a bridge with {len(x)} beads that head 2 + tail 2 does not clean (first found):")
    P(f"      x  = {x}")
    P(f"      c1 = {c1};   b' of x is an up-bond: {L.sub(x[-2], x[-3])[1] == 1};   A(x, c1) = {L.A_part(x, c1)}, B(x) = {L.B_part(x)}")
    P(f"      beads of x at the height of its last bead ({H}): indices {[i for i, p in enumerate(x) if p[1] == H]}")
    P(f"      extended bridge y = s2, s1, x, t1, t2 ({len(y)} beads): (i) holds: {L.sub(y[-2], y[-3])[1] == 1};  A(y) = {L.A_part(y, cy)},  B(y) = {L.B_part(y)}")
    for (j, s, i, q, d) in spoil:
        P(f"      site {j} above y, {s} (it is t{j + 2} of x), and bead {i} of y, {q} (bead {i - 2} of x): squared distance {d}, chain separation {len(y) - 1 + j - i}")
    y3 = L.extend(x, c1, 2, 3)
    P(f"      with head 2 + tail 3 the result is clean: {L.is_clean(y3)};  (h,g): x {L.profile(x)}, head 2 + tail 2 {L.profile(y)}, head 2 + tail 3 {L.profile(y3)}")
P(f"   [{time.time()-t0:.0f} s]")

rows = {}
for line in open("out/extremal_raw.txt"):
    a = line.split()
    n = int(a[1]); co = [int(t) for t in a[5:]]
    rows[a[0]] = (tuple(int(t) for t in a[2:5]), [tuple(co[3 * i:3 * i + 3]) for i in range(n)])
cA, xA = rows["A"]
_, xB = rows["B"]
assert L.check_walk(xA) is None and L.is_bridge(xA) and L.check_walk(xB) is None and L.is_bridge(xB)
z, _ = L.concat(xB, xA, L.admissible_c1(xB)[0])
assert L.check_walk(z) is None and L.is_bridge(z) and len(z) == len(xA) + len(xB) + 3
hz = L.profile(z)
assert hz == L.profile_brute(z)
P(f"   the sharp cost: z = (the 14-bead bridge with B = {L.B_part(xB)}) o (the 21-bead bridge with A = {L.A_part(xA, cA)}), {len(z)} beads, (h,g) = {hz}")
for c in L.admissible_c1(z):
    for (kh, kt) in ((3, 3), (2, 3)):
        y = L.extend(z, c, kh, kt)
        assert L.check_walk(y) is None and L.is_bridge(y)
        d = vsub(L.profile_brute(y), hz)
        P(f"      c1 = {c}: A(z, c1) = {L.A_part(z, c)}, B(z) = {L.B_part(z)}; head {kh} + tail {kt}: clean {L.is_clean(y)}, change of (h,g) = {d}, norm {norm(d)}")


# ------------------------------------------------------------------------------------------------ D
def hnf(vecs, dim):
    """basis of the Z-span in row echelon form (Euclid on the columns, integers only)"""
    rows_ = [list(v) for v in vecs]
    basis = []
    for col in range(dim):
        while True:
            cand = [r for r in rows_ if r[col] != 0]
            if len(cand) <= 1:
                break
            cand.sort(key=lambda r: abs(r[col]))
            p = cand[0]
            for r in cand[1:]:
                q = r[col] // p[col]
                for i in range(dim):
                    r[i] -= q * p[i]
        if cand:
            basis.append(list(cand[0]))
            rows_ = [r for r in rows_ if r is not cand[0]]
        rows_ = [r for r in rows_ if any(r)]
    assert not rows_
    return basis


def det_int(Mx):
    """exact determinant of an integer matrix (fraction-free elimination)"""
    M = [list(r) for r in Mx]
    n = len(M)
    sign, prev = 1, 1
    for k in range(n - 1):
        if M[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
            if sw is None:
                return 0
            M[k], M[sw] = M[sw], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]


t0 = time.time()
P("\nD. the lattice generated by (h3, h8, h11, g; N+3) of the clean bridges with at most N beads (own enumeration with the first two bonds fixed)")
theirs_D = {3: (1, 1), 4: (3, 2), 5: (6, 2), 6: (10, 2), 7: (16, 3), 8: (28, 4), 9: (45, 4), 10: (82, 5), 11: (146, 5)}
vecs = set()
vec10 = None
for N in range(3, NMAX_D + 1):
    nclean = maxh3 = 0
    for x in L.enum_bridges(N):
        if L.is_clean(x):
            nclean += 1
            v = L.profile(x) + (N + 3,)
            maxh3 = max(maxh3, v[0])
            vecs.add(v)
    Bm = hnf(sorted(vecs), 5)
    idx_ = math.prod(abs([t for t in r if t != 0][0]) for r in Bm) if len(Bm) == 5 else None
    th = theirs_D.get(N)
    P(f"   N <= {N:2d}: {nclean:5d} clean bridges with N beads (largest h3 among them: {maxh3}); {len(vecs):3d} distinct vectors so far; rank {len(Bm)}; index in Z^5: "
      f"{idx_ if idx_ is not None else 'not of full rank'}" + (f"      theirs: {th[0]} vectors, rank {th[1]}" if th else ""))
    if N == 10:
        vec10 = sorted(vecs)
        P(f"            basis (N <= 10): {Bm}")
rng = random.Random(20261126)
gcd_, tries, used = 0, 0, []
while gcd_ != 1 and tries < 200000:
    S5 = rng.sample(vec10, 5)
    dt = det_int(S5)
    tries += 1
    if dt != 0 and math.gcd(gcd_, dt) != gcd_:
        gcd_ = math.gcd(gcd_, dt)
        used.append((dt, S5))
P(f"   certificate independent of the row reduction (N <= 10): gcd of {len(used)} 5x5 minors = {gcd_} after {tries} random 5-subsets:")
for dt, S5 in used:
    P(f"      det = {dt:5d}  for  {S5}")
uni = None
for _ in range(400000):
    S5 = rng.sample(vec10, 5)
    if abs(det_int(S5)) == 1:
        uni = S5
        break
P(f"   five clean bridges with at most 10 beads whose vectors have determinant +-1: {uni if uni is not None else 'none found in 400000 random 5-subsets'}")
if uni is not None:
    import sympy
    P(f"      determinant by my elimination: {det_int(uni)};  by sympy (exact rational arithmetic): {sympy.Matrix(uni).det()}")
    P("      determinants by sympy of the minors above: " + ", ".join(str(sympy.Matrix(S5).det()) for _, S5 in used))
P(f"   [{time.time()-t0:.0f} s]")

# ------------------------------------------------------------------------------------------------ E
R, beta, betap = 36, 60, 28
P("\nE. constants (R = 36, beta = 60, beta' = 28; M = N + 3)")
P(f"   cost of making a bridge clean: theirs, 11.69b(b): at most 6 beta' = {6 * betap};  exactly A + B <= (1,9,14;1), norm {norm((1, 9, 14, 1))} (attained, part C)")
P("   one-sided rate, dist((h,g)/N, K^br) for an arbitrary bridge with N beads:")
P(f"     Theorem 11.69 (unchanged at 24a3c27): (beta + 3R)/(N+3) = {beta + 3 * R}/(N+3)")
P(f"     through 11.69b(b) with its constant (clean bridge with N+6 beads, level N+9): (9R + 6 beta')/(N+9) = {9 * R + 6 * betap}/(N+9)")
P(f"     the same with the exact cost A + B >= 0 (each coordinate of 9(h,g)/N - (A+B) is at most the larger): 9R/(N+9) = {9 * R}/(N+9)")
P(f"     R9.1(d), exact point qhat/(N+3) of the bridge itself: 3R/(N+3) = {3 * R}/(N+3)")
P("   interior rate:")
P(f"     theirs: dist(p, S_M/M) <= 6 (m+1) R / M = {6 * R} (m(p)+1)/M for every M >= 6, plus 3R/(M-3) = {3 * R}/(M-3) for the normalisation")
P(f"     R9.1(f): (7.5 + {3 * R})/(N+3) for N >= N0(compact set); rounding in the cumulative coordinates gives 5 in place of 7.5:")
h = 0.5
P(f"       rounding (h3,h8,h11,g) coordinatewise: at most 5*{h} + 3*{2 * h} + {3 * h} + {h} = {5 * h + 3 * 2 * h + 3 * h + h};"
  f"  rounding (h3, h3+h8, h3+h8+h11, g): at most (5 + 3 + 1 + 1)/2 = {(5 + 3 + 1 + 1) / 2}")
P(f"total time {time.time()-t00:.0f} s")
