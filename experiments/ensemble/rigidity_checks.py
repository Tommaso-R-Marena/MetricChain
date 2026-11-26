#!/usr/bin/env python3
"""Numerical checks for Part II of docs/ensemble/ENSEMBLE_REPORT.md (laws of observables; ensemble rigidity).

R1  Rigidity matroids: rank function from the rigidity matrix at a random configuration; connectivity
    test r(J) + r(E \\ J) > r(E) for every proper non-empty J.
R2  Chimeras for complete graphs K_{d+2} in R^d (Cayley-Menger determinant): for random conformers every
    non-constant splice of their squared edge lengths has a non-zero Cayley-Menger determinant, hence is
    not realisable.  K = 2 and K = 3 conformers; d = 2 and d = 3.
R3  Chimeras for a globally rigid graph that is not complete (the wheel W_5 in the plane): least squares
    from many starts never realises a non-constant splice.
R4  Negative controls: (a) the triangle in the plane (globally rigid, 3 < d + 2 vertices, free matroid):
    splices are realisable and two different two-conformer ensembles have the same edge-length laws;
    (b) K_4 plus a vertex of degree two (two coloops): realisable chimeras.
R5  The explicit dual certificate f(p) = sum_e prod_i (l_e(p)^2 - l_e(x_i)^2)^2 for K_4 in the plane:
    every zero found by multi-start minimisation has the edge lengths of one of the conformers.
R6  Two toy feature maps R^2 -> R^4: connected matroid (no splice on the variety) and a direct sum
    (every splice realisable).
R7  "No chimera" is sufficient, not necessary (internal review ER1, finding F2): K_4 plus a vertex of
    degree two, an explicit pair of conformers and perturbations of it.  Three chimeras are realisable,
    every other non-constant splice is not, and a linear programme over the realisable splices shows that
    every ensemble with the eight edge-length laws puts no mass on a chimera.
R8  Genericity is needed in Theorem E7 already on the line (review ER1, finding F14): the 4-cycle with
    conformers (8,0,3,5) and (8,3,5,0); both complementary splices close up and form a twin ensemble.
R9  "Generic" must be jointly generic (science division, SCI-REV-0020, Example D1): two frameworks of K_4 in
    the plane with no edge length in common whose two-conformer ensemble has a twin; exact rational
    arithmetic.
R10 Conformers that share a rigid part (science division, Example D2): on the generically globally rigid
    graph K_5 minus an edge, two conformers that share a triangle have a twin ensemble with the same law on
    every measured edge; with the missing edge measured the laws differ.
Controls added after the science division's review: R3 now also searches for planted realisable vectors
(lengths of a third random framework) and reports how many the same search finds; R4(b) tests all six
non-constant colourings of the three blocks against the two-circle criterion.
Exit code 0 iff every check passes.
"""
import itertools, sys
from fractions import Fraction
import numpy as np
from scipy.optimize import least_squares, linprog

rng = np.random.default_rng(20261127)


def edges_complete(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def sqlen(p, E):
    return np.array([np.sum((p[i] - p[j]) ** 2) for i, j in E])


def rigidity_matrix(p, E):
    n, d = p.shape
    R = np.zeros((len(E), n * d))
    for k, (i, j) in enumerate(E):
        R[k, i * d:(i + 1) * d] = p[i] - p[j]
        R[k, j * d:(j + 1) * d] = p[j] - p[i]
    return R


def rank_fn(E, n, d):
    p = rng.normal(size=(n, d))
    R = rigidity_matrix(p, E)
    cache = {}

    def r(J):
        J = tuple(sorted(J))
        if J not in cache:
            cache[J] = 0 if not J else int(np.linalg.matrix_rank(R[list(J)], tol=1e-9))
        return cache[J]
    return r


def matroid_connected(E, n, d):
    r = rank_fn(E, n, d)
    m = len(E); full = r(range(m))
    for mask in range(1, 2 ** (m - 1)):          # J and its complement: fix element m-1 in the complement
        J = [k for k in range(m) if mask >> k & 1]
        Jc = [k for k in range(m) if not mask >> k & 1]
        if r(J) + r(Jc) == full:
            return False, full
    return True, full


def cayley_menger(sq, n):
    """sq: dict/array of squared distances in the order of edges_complete(n)."""
    D = np.zeros((n, n)); E = edges_complete(n)
    for k, (i, j) in enumerate(E):
        D[i, j] = D[j, i] = sq[k]
    M = np.ones((n + 1, n + 1)); M[0, 0] = 0; M[1:, 1:] = D
    return np.linalg.det(M)


def test_R1():
    ok = True
    out = []
    K4 = edges_complete(4); K5 = edges_complete(5); K3 = edges_complete(3)
    wheel = [(0, i) for i in range(1, 6)] + [(i, i % 5 + 1) for i in range(1, 6)]
    k4pend = K4 + [(4, 0), (4, 1)]
    diamond = [e for e in K4 if e != (2, 3)]
    cases = [("K4 in R^2", K4, 4, 2, True, 5), ("K5 in R^3", K5, 5, 3, True, 9),
             ("wheel W5 in R^2", wheel, 6, 2, True, 9), ("K3 in R^2", K3, 3, 2, False, 3),
             ("K4 + degree-2 vertex in R^2", k4pend, 5, 2, False, 7), ("K4 - e in R^2", diamond, 4, 2, False, 5),
             ("K5 in R^2", K5, 5, 2, True, 7), ("K6 in R^3", edges_complete(6), 6, 3, True, 12)]
    for name, E, n, d, expect, rk in cases:
        c, full = matroid_connected(E, n, d)
        out.append(f"    {name}: rank {full}, connected = {c}")
        ok &= (c == expect) and (full == rk)
    return ok, out


def test_R2():
    ok = True; out = []
    for d, n, K in ((2, 4, 2), (2, 4, 3), (3, 5, 2), (3, 5, 3)):
        E = edges_complete(n); m = len(E)
        smallest = np.inf; count = 0; base = 0.0
        for _ in range(20 if K == 2 else 4):
            conf = [rng.normal(size=(n, d)) for _ in range(K)]
            L = np.array([sqlen(p, E) for p in conf])               # K x m
            for p in conf:
                base = max(base, abs(cayley_menger(sqlen(p, E), n)))  # should be ~ 0 (realisable)
            if K ** m <= 20000:
                cols = itertools.product(range(K), repeat=m)
            else:
                cols = (tuple(rng.integers(K, size=m)) for _ in range(20000))
            for a in cols:
                if len(set(a)) == 1:
                    continue
                q = L[list(a), range(m)]
                cm = abs(cayley_menger(q, n))
                smallest = min(smallest, cm); count += 1
        out.append(f"    K_{n} in R^{d}, {K} conformers: {count} non-constant splices, smallest |CM| = {smallest:.3e}; "
                   f"largest |CM| at true conformers = {base:.1e}")
        ok &= smallest > 1e4 * base and base < 1e-8
    return ok, out


def realise(E, n, d, q, starts=25, first=None):
    """min_p sum (l_e(p)^2 - q_e)^2 by multi-start least squares; returns the best residual norm.
    `first`: an optional first starting point (used where the theory predicts a solution nearby)."""
    best = np.inf
    for s in range(starts):
        x0 = first.ravel().copy() if (s == 0 and first is not None) else rng.normal(size=n * d) * 1.5
        res = least_squares(lambda x: sqlen(x.reshape(n, d), E) - q, x0, method="trf", xtol=1e-14, ftol=1e-14,
                            gtol=1e-14)
        best = min(best, np.linalg.norm(res.fun))
        if best < 1e-9:
            break
    return best


def test_R3():
    n, d = 6, 2
    wheel = [(0, i) for i in range(1, 6)] + [(i, i % 5 + 1) for i in range(1, 6)]
    m = len(wheel)
    worst = np.inf; sanity = 0.0
    for _ in range(3):
        x1 = rng.normal(size=(n, d)); x2 = rng.normal(size=(n, d))
        L = np.array([sqlen(x1, wheel), sqlen(x2, wheel)])
        sanity = max(sanity, realise(wheel, n, d, L[0]))
        for _ in range(60):
            a = rng.integers(2, size=m)
            if len(set(a.tolist())) == 1:
                continue
            q = L[a, range(m)]
            worst = min(worst, realise(wheel, n, d, q))
    # control: planted realisable vectors (the lengths of a third random framework, starting point not given)
    planted = found = 0
    for _ in range(20):
        z = rng.normal(size=(n, d)); planted += 1
        found += realise(wheel, n, d, sqlen(z, wheel)) < 1e-9
    return worst > 1e-6 and worst > 1e6 * sanity and sanity < 1e-8 and found >= 18, \
        [f"    wheel W5 in R^2: smallest least-squares residual over 180 random splices "
         f"= {worst:.3e} (true conformer: {sanity:.1e}); control: {found}/{planted} planted realisable vectors "
         f"found by the same search (a search that misses realisable vectors is not evidence of absence)"]


def test_R4():
    out = []; ok = True
    # (a) triangle: two ensembles with the same three edge-length laws
    A = np.array([3.0, 4.0, 5.0]); B = np.array([4.0, 5.0, 6.0])       # lengths (12, 13, 23)
    Cc = np.array([3.0, 5.0, 6.0]); Dd = np.array([4.0, 4.0, 5.0])     # splices; both satisfy the triangle inequality
    for t in (A, B, Cc, Dd):
        ok &= t[0] < t[1] + t[2] and t[1] < t[0] + t[2] and t[2] < t[0] + t[1]
    same = all(sorted([A[e], B[e]]) == sorted([Cc[e], Dd[e]]) for e in range(3))
    ok &= same and not (np.allclose(sorted(map(tuple, [A, B])), sorted(map(tuple, [Cc, Dd]))))
    out.append(f"    triangle: {{(3,4,5),(4,5,6)}} and {{(3,5,6),(4,4,5)}} have equal edge-length laws: {same}")
    # (b) K4 + a vertex of degree two in the plane: splice the two coloops
    K4 = edges_complete(4); E = K4 + [(4, 0), (4, 1)]
    n, d = 5, 2; cnt = 0; tot = 0; agree = 0
    for t in range(40):
        x1 = rng.normal(size=(n, d)); x2 = x1 + (0.05 if t < 20 else 1.0) * rng.normal(size=(n, d))
        L = np.array([sqlen(x1, E), sqlen(x2, E)]); conf = (x1, x2)
        # the three blocks: K4 (six edges), pendant edge 4-0, pendant edge 4-1; all six non-constant colourings
        for b, i, j in itertools.product(range(2), repeat=3):
            if b == i == j:
                continue
            q = np.concatenate([L[b, :6], [L[i, 6], L[j, 7]]])
            # exact criterion: circles of radii r0, r1 about the block's vertices 0, 1 meet
            r0, r1 = np.sqrt(q[6]), np.sqrt(q[7]); base = np.linalg.norm(conf[b][0] - conf[b][1])
            exact = abs(r0 - r1) < base < r0 + r1
            found = realise(E, n, d, q, first=conf[b]) < 1e-9
            tot += 1; cnt += found; agree += (found == exact)
    out.append(f"    K4 + degree-2 vertex: {cnt}/{tot} splices of the three blocks realised (all six non-constant "
               f"colourings; 20 nearby pairs, 20 independent pairs); agreement with the two-circle criterion "
               f"{agree}/{tot}")
    ok &= agree == tot and cnt >= 20
    return ok, out


def test_R5():
    n, d = 4, 2; E = edges_complete(n)
    x = [rng.normal(size=(n, d)) for _ in range(2)]
    L = np.array([sqlen(p, E) for p in x])

    def resid(v):
        l = sqlen(v.reshape(n, d), E)
        return (l - L[0]) * (l - L[1])
    hits = {0: 0, 1: 0}; other = 0; zeros = 0
    # 100 starts near each conformer (the zeros there are degenerate: f vanishes to fourth order) and 200
    # random starts (review ER1, finding F6: random starts alone almost never reach conformer 1)
    starts = [x[0].ravel() + 0.2 * rng.normal(size=n * d) for _ in range(100)] \
        + [x[1].ravel() + 0.2 * rng.normal(size=n * d) for _ in range(100)] \
        + [rng.normal(size=n * d) * 1.5 for _ in range(200)]
    for x0 in starts:
        res = least_squares(resid, x0, method="trf", xtol=1e-15, ftol=1e-15, gtol=1e-15)
        if np.linalg.norm(res.fun) < 1e-10:
            zeros += 1
            l = sqlen(res.x.reshape(n, d), E)
            m0 = np.allclose(l, L[0], atol=1e-5); m1 = np.allclose(l, L[1], atol=1e-5)
            if m0: hits[0] += 1
            elif m1: hits[1] += 1
            else: other += 1
    return other == 0 and hits[0] >= 20 and hits[1] >= 20, \
        [f"    certificate for K4, two conformers: {zeros} zeros found in {len(starts)} starts "
         f"(100 near each conformer, 200 random); {hits[0]} at conformer 1, {hits[1]} at conformer 2, "
         f"{other} elsewhere"]


def test_R6():
    ok = True
    # connected: F(x,y) = (x, y, x^2+y^2, xy); variety: y3 = y1^2 + y2^2, y4 = y1 y2
    F = lambda v: np.array([v[0], v[1], v[0] ** 2 + v[1] ** 2, v[0] * v[1]])
    viol = np.inf
    for _ in range(200):
        a, b = rng.normal(size=2), rng.normal(size=2)
        Fa, Fb = F(a), F(b)
        for col in itertools.product(range(2), repeat=4):
            if len(set(col)) == 1:
                continue
            q = np.array([(Fa, Fb)[c][k] for k, c in enumerate(col)])
            viol = min(viol, abs(q[2] - q[0] ** 2 - q[1] ** 2) + abs(q[3] - q[0] * q[1]))
    ok &= viol > 1e-6
    # direct sum: G(x,y) = (x, x^2, y, y^3): every splice along {1,2} | {3,4} is G(x_a, y_b)
    return ok, [f"    connected toy map: smallest violation of the equations of the variety over all splices = {viol:.2e}",
                "    direct-sum toy map (x, x^2, y, y^3): the splice of (x1,y1), (x2,y2) along {1,2}|{3,4} is G(x1,y2) (exact)"]


def k4_pendant_pair():
    """The review's pair: K_4 on vertices 0..3 plus vertex 4 joined to 0 and 1, in the plane."""
    x1 = np.array([[0, 0], [2, 0], [0.6, 1.1], [1.6, -0.9], [1.0, np.sqrt(1.25)]])                 # pendants 1.5, 1.5
    a = (25 + 9 - 6.25) / 10
    x2 = np.array([[0, 0], [5, 0], [1.5, 1.1], [4, -0.9], [a, np.sqrt(9 - a * a)]])                # pendants 3, 2.5
    return x1, x2


def test_R7():
    K4 = edges_complete(4); E = K4 + [(4, 0), (4, 1)]; n, d = 5, 2
    out = []; ok = True
    base1, base2 = k4_pendant_pair()
    worst_cm = np.inf; worst_margin = np.inf; worst_mass = 0.0; worst_real = 0.0; pairs = 0; cm0 = None
    for t in range(21):
        x1 = base1 + (0.0 if t == 0 else 0.005) * rng.normal(size=(n, d))
        x2 = base2 + (0.0 if t == 0 else 0.005) * rng.normal(size=(n, d))
        L = np.array([sqlen(x1, E), sqlen(x2, E)])                     # squared lengths, 2 x 8
        # (i) no mixed K_4 block is realisable in the plane: Cayley-Menger determinant of 4 points
        for a in itertools.product(range(2), repeat=6):
            if len(set(a)) == 1:
                continue
            worst_cm = min(worst_cm, abs(cayley_menger(L[list(a), range(6)], 4)))
        if t == 0:
            cm0 = worst_cm
        # (ii) pendant lengths (r0 from conformer i, r1 from conformer j) on the block of conformer b:
        #      realisable iff the two circles about the block's vertices 0, 1 meet
        realisable = []
        for b in range(2):
            base = np.sqrt(L[b, 0])                                    # edge (0,1) is the first edge of K_4
            for i in range(2):
                for j in range(2):
                    r0, r1 = np.sqrt(L[i, 6]), np.sqrt(L[j, 7])
                    lo, hi = abs(r0 - r1), r0 + r1
                    meets = lo < base < hi
                    worst_margin = min(worst_margin, abs(base - lo), abs(hi - base))
                    if meets:
                        realisable.append((b, i, j))
                        if (i, j) != (b, b):                           # a chimera: realise it to machine precision
                            q = np.concatenate([L[b, :6], [L[i, 6], L[j, 7]]])
                            worst_real = max(worst_real, realise(E, n, d, q, first=(x1, x2)[b]))
        expect = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 1, 1)]
        ok &= sorted(realisable) == expect
        # (iii) LP: largest total chimera mass of a table v >= 0 on the realisable splices with marginal w on
        #       every feature (the six block edges share the block colour)
        chim = [c for c in realisable if len(set(c)) > 1]
        for w in ((0.5, 0.5), (0.2, 0.8), (0.9, 0.1)):
            A = []; rhs = []
            for pos in range(3):                                       # block colour, colour of 4-0, colour of 4-1
                for col in range(2):
                    A.append([1.0 if c[pos] == col else 0.0 for c in realisable]); rhs.append(w[col])
            cost = [-1.0 if c in chim else 0.0 for c in realisable]
            res = linprog(cost, A_eq=np.array(A), b_eq=np.array(rhs), bounds=[(0, None)] * len(realisable),
                          method="highs")
            ok &= res.status == 0
            worst_mass = max(worst_mass, -res.fun)
        pairs += 1
    ok &= worst_cm > 1.0 and worst_margin > 0.05 and worst_mass < 1e-9 and worst_real < 1e-9
    out.append(f"    K4 + degree-2 vertex, the review's pair and 20 perturbations: realisable splices = the two "
               f"conformers and three chimeras in {pairs}/{pairs} pairs")
    out.append(f"    smallest |Cayley-Menger| of a mixed K4 block = {cm0:.2f} (the pair), {worst_cm:.2f} (all 21); "
               f"smallest margin of the two-circle criterion = {worst_margin:.2f}; chimeras realised to {worst_real:.1e}")
    out.append(f"    largest chimera mass compatible with the eight edge-length laws (LP, 3 weightings) = "
               f"{worst_mass:.1e}: identified although chimeras exist")
    return ok, out


def test_R8():
    x = np.array([8.0, 0.0, 3.0, 5.0]); y = np.array([8.0, 3.0, 5.0, 0.0])
    E = [(0, 1), (1, 2), (2, 3), (3, 0)]
    lx = np.array([abs(x[i] - x[j]) for i, j in E]); ly = np.array([abs(y[i] - y[j]) for i, j in E])
    ok = list(lx) == [8, 3, 2, 3] and list(ly) == [5, 2, 5, 8]
    twins = []
    for a in itertools.product(range(2), repeat=4):
        if len(set(a)) == 1:
            continue
        q = np.where(np.array(a) == 0, lx, ly)
        closes = any(abs(sum(sg * l for sg, l in zip(signs, q))) < 1e-12
                     for signs in itertools.product((-1, 1), repeat=4))
        comp = np.where(np.array(a) == 0, ly, lx)
        closes_c = any(abs(sum(sg * l for sg, l in zip(signs, comp))) < 1e-12
                       for signs in itertools.product((-1, 1), repeat=4))
        if closes and closes_c and a[0] == 0:
            twins.append((tuple(int(v) for v in q), tuple(int(v) for v in comp)))
    ok &= ((8, 2, 2, 8), (5, 3, 5, 3)) in twins
    shared = any(lx[e] == ly[e] for e in range(4))
    ok &= not shared
    return ok, [f"    4-cycle on the line, x = (8,0,3,5), x' = (8,3,5,0): lengths {tuple(int(v) for v in lx)} and "
                f"{tuple(int(v) for v in ly)}, no shared length; complementary splices that both close up: {twins}"]


def test_R9():
    """Science division, SCI-REV-0020, Example D1 (exact)."""
    F = Fraction
    x1 = [(F(1, 2), F(2)), (F(3), F(3)), (F(-1), F(0)), (F(1), F(0))]
    x2 = [(F(1, 2), F(3, 2)), (F(3, 2), F(-4)), (F(-2), F(0)), (F(2), F(0))]
    refl = lambda P: [P[0], (P[1][0], -P[1][1]), P[2], P[3]]            # vertex 1 reflected in the line 2-3
    y, yp = refl(x1), refl(x2)
    E = edges_complete(4)
    sq = lambda P: tuple((P[i][0] - P[j][0]) ** 2 + (P[i][1] - P[j][1]) ** 2 for i, j in E)
    l1, l2, ly, lyp = sq(x1), sq(x2), sq(y), sq(yp)
    no_common = all(l1[e] != l2[e] for e in range(6))
    same_laws = all(sorted([l1[e], l2[e]]) == sorted([ly[e], lyp[e]]) for e in range(6))
    different = sorted([l1, l2]) != sorted([ly, lyp])
    return no_common and same_laws and different, \
        [f"    K4, Example D1: squared lengths {tuple(str(v) for v in l1)} and {tuple(str(v) for v in l2)}: no length "
         f"in common: {no_common}; the reflected pair has the same law on every edge: {same_laws}; and is a "
         f"different ensemble: {different}"]


def test_R10():
    """Science division, Example D2: K5 minus the edge 3-4, conformers sharing the triangle 0-1-2."""
    E = [e for e in edges_complete(5) if e != (3, 4)]
    same = 0; differ34 = 0; trials = 200
    for _ in range(trials):
        T = rng.normal(size=(3, 2)); P3, P4, Q3, Q4 = (rng.normal(size=2) for _ in range(4))
        x1 = np.vstack([T, P3, P4]); x2 = np.vstack([T, Q3, Q4])
        y = np.vstack([T, P3, Q4]); yp = np.vstack([T, Q3, P4])
        A = np.sort(np.array([sqlen(x1, E), sqlen(x2, E)]), axis=0)
        B = np.sort(np.array([sqlen(y, E), sqlen(yp, E)]), axis=0)
        same += np.allclose(A, B)
        d34 = lambda P: np.sum((P[3] - P[4]) ** 2)
        differ34 += not np.allclose(sorted([d34(x1), d34(x2)]), sorted([d34(y), d34(yp)]))
    rk = np.linalg.matrix_rank(rigidity_matrix(rng.normal(size=(5, 2)), E), tol=1e-9)
    return same == trials and differ34 == trials and rk == 7, \
        [f"    K5 minus an edge (rigidity rank {rk} = 2*5 - 3), two conformers sharing a triangle: the exchanged pair "
         f"has the same law on every measured edge in {same}/{trials}; the law of the unmeasured edge differs in "
         f"{differ34}/{trials}"]


def main():
    allok = True
    for name, fn in (("R1 rigidity matroids", test_R1), ("R2 chimeras, complete graphs", test_R2),
                     ("R3 chimeras, wheel", test_R3), ("R4 negative controls", test_R4),
                     ("R5 explicit certificate", test_R5), ("R6 toy feature maps", test_R6),
                     ("R7 identified with chimeras", test_R7), ("R8 non-generic twin on the line", test_R8),
                     ("R9 joint genericity (Example D1)", test_R9), ("R10 a shared rigid part (Example D2)", test_R10)):
        ok, out = fn()
        print(f"{name}: {'ok' if ok else 'FAILED'}")
        for line in out:
            print(line)
        allok &= ok
    print("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
