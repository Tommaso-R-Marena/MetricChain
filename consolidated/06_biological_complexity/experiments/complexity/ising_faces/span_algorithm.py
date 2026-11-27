"""Deciding "are K given sign vectors exactly the ground states of an Ising pair energy?" in time 2^K * poly(n).

Pointed out by the referee of COMPLEXITY-REV-0004 (finding 3) as a consequence of Proposition 5 of
docs/complexity/ISING_GROUND_SETS.md:  every state occurring in a certificate of non-exposedness lies in the span L
of the K given states, and a K-dimensional subspace contains at most 2^(K-1) sign vectors up to sign (a vector of L
is determined by its values on rank(L) independent coordinates).  So it suffices to
   (1) list the sign vectors of L                      -- 2^(r-1) candidates, r = rank <= K, exact arithmetic;
   (2) solve the linear programme of Theorem 1 with the competitors restricted to these.
Both answers are certified exactly: 'no' by the rational certificate of Theorem 1; 'yes' by a rational J that
separates V strictly from all other sign vectors of L (which, by Proposition 5, excludes every certificate).

This module also contains the checks added after the review:
   * agreement with the full linear programme (all 2^(m-1) states) on all type sets for K = 4, on the orbit
     representatives for K = 5 with at most 9 types, and on random instances;
   * the family "m singleton states on m >= 4 sites, with or without the all-plus state" (never exposed);
   * the sufficient condition "the types form an isometric subgraph of the cube" (reported by the referee from
     the Deza-Laurent survey; not read by us) and Corollary 7, counted on the K = 5 table;
   * the referee's reduction from positive 1-in-3-SAT to "another sign vector in the span", and the fact that its
     instances are always exposed.

Usage:  python3 span_algorithm.py [all | agree | singletons | conditions | reduction | timing]
"""
import itertools
import random
import sys
import time
from fractions import Fraction

from faces import decide, reduce_types, states


def rref(rows):
    """reduced row echelon form over Q of a list of integer rows; returns (nonzero rows, pivot columns)."""
    M = [[Fraction(v) for v in row] for row in rows]
    piv = []
    r = 0
    ncol = len(M[0])
    for c in range(ncol):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c]
        M[r] = [v * inv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def sign_vectors_in_span(vectors):
    """all sign vectors (first entry +1) in the linear span of the given sign vectors; exact."""
    R, piv = rref(vectors)
    r, m = len(R), len(vectors[0])
    out = []
    # a vector of the span is a.R with a = its values on the pivot columns
    for a in itertools.product((1, -1), repeat=r - 1):
        a = (1,) + a
        v = [sum(a[i] * R[i][c] for i in range(r)) for c in range(m)]
        if all(x == 1 or x == -1 for x in v):
            w = tuple(int(x) for x in v)
            if w[0] < 0:
                w = tuple(-x for x in w)
            out.append(w)
    return sorted(set(out))


def decide_span(types):
    """types: distinct columns (tuples of length K, first entry +1).  Same return values as faces.decide, but the
    competitors are the sign vectors of the span only.  Time 2^K * poly(number of types)."""
    m, K = len(types), len(types[0])
    V = []
    for k in range(K):
        row = tuple(t[k] for t in types)
        if row[0] < 0:
            row = tuple(-x for x in row)
        V.append(row)
    if len(set(V)) < K or m == 1:
        return "degenerate", None
    cand = sign_vectors_in_span(V)
    return decide(types, candidates=cand)


def is_exposed_span(vectors):
    return decide_span(reduce_types(vectors))


# ------------------------------------------------------------------------------------------------- checks
def all_types(K):
    return [(1,) + t for t in itertools.product((1, -1), repeat=K - 1)]


def check_agree(seed=5):
    rng = random.Random(seed)
    mism = cnt = no = 0
    T4 = all_types(4)
    for mask in range(1, 1 << 8):
        ts = [T4[i] for i in range(8) if (mask >> i) & 1]
        a, b = decide(ts)[0], decide_span(ts)[0]
        cnt += 1
        mism += a != b
        no += a == "no"
    print(f"   K = 4: all 255 type sets, full LP against span LP: mismatches {mism} (not exposed: {no})")
    for K, trials, mmax in ((5, 400, 10), (6, 300, 10), (7, 200, 10)):
        TK = all_types(K)
        mm = c = n_no = n_deg = 0
        while c < trials:
            m = rng.randint(K - 1, mmax)
            ts = rng.sample(TK, m)
            a = decide(ts)[0]
            if a == "degenerate":
                n_deg += 1
                if n_deg > 10 * trials:
                    break
                continue
            b = decide_span(ts)[0]
            c += 1
            mm += a != b
            n_no += a == "no"
        mism += mm
        print(f"   K = {K}: {c} random non-degenerate type sets with at most {mmax} types: mismatches {mm} "
              f"(not exposed: {n_no})")
    return mism == 0


def singleton_states(m, with_all_plus):
    V = [tuple(-1 if i == k else 1 for i in range(m)) for k in range(m)]
    if with_all_plus:
        V.append(tuple(1 for _ in range(m)))
    return V


def check_singletons(mmax=8):
    ok = True
    for m in range(3, mmax + 1):
        for wp in (False, True):
            V = singleton_states(m, wp)
            status = is_exposed_span(V)[0]
            expect = "yes" if (m == 3 and not wp) else "no"
            # m = 3 with the all-plus state: all four states of three sites, exposed (J = 0)
            if m == 3 and wp:
                expect = "yes"
            ok &= status == expect
            print(f"   m = {m}, {'with' if wp else 'without'} the all-plus state: {status}")
    return ok


def isometric_for_base(types, k0):
    """gauge the state k0 to all-plus; are the types, as points of the cube {0,1}^(K-1) with edges at Hamming
    distance 1, an isometric subgraph (graph distance = Hamming distance)?"""
    K = len(types[0])
    pts = [tuple(t[k] * t[k0] for k in range(K) if k != k0) for t in types]
    n = len(pts)
    ham = [[sum(a != b for a, b in zip(p, q)) for q in pts] for p in pts]
    INF = 10 ** 6
    dist = [[0 if i == j else (1 if ham[i][j] == 1 else INF) for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist == ham


def cor7_applies(types):
    K = len(types[0])
    rows = [[1] + [t[k] * t[l] for k in range(K) for l in range(k + 1, K)] for t in types]
    return len(rref(rows)[0]) == 1 + K * (K - 1) // 2


def check_conditions():
    """K = 5: over all type sets (by orbit, using the orbit enumeration of table_k5.py), count how many are certified
    exposed by Corollary 7, by the isometric condition, by 'no other sign vector in the span'; and verify that
    each condition implies 'exposed'."""
    import table_k5 as t5
    G = t5.symmetries()
    NT = t5.NT
    seen = bytearray(1 << NT)
    cnt = {"non-degenerate type sets": 0, "exposed": 0, "Corollary 7 applies": 0, "isometric condition applies": 0,
           "either applies": 0, "no other sign vector in the span": 0, "VIOLATIONS": 0}
    for mask in range(1, 1 << NT):
        if seen[mask]:
            continue
        T = [i for i in range(NT) if (mask >> i) & 1]
        orb = set()
        for g in G:
            m2 = 0
            for i in T:
                m2 |= 1 << g[i]
            orb.add(m2)
        for o in orb:
            seen[o] = 1
        ts = [t5.TYPES[i] for i in T]
        status = decide_span(ts)[0]
        if status == "degenerate":
            continue
        w = len(orb)
        V = [tuple(t[k] for t in ts) for k in range(5)]
        V = [v if v[0] > 0 else tuple(-x for x in v) for v in V]
        extra = [y for y in sign_vectors_in_span(V) if y not in set(V)]
        c7 = cor7_applies(ts)
        iso = any(isometric_for_base(ts, k0) for k0 in range(5))
        cnt["non-degenerate type sets"] += w
        cnt["exposed"] += w * (status == "yes")
        cnt["Corollary 7 applies"] += w * c7
        cnt["isometric condition applies"] += w * iso
        cnt["either applies"] += w * (c7 or iso)
        cnt["no other sign vector in the span"] += w * (not extra)
        if (c7 or iso or not extra) and status != "yes":
            cnt["VIOLATIONS"] += w
    print("   K = 5, all type sets by orbit:", cnt)
    return cnt["VIOLATIONS"] == 0 and cnt["non-degenerate type sets"] == 61719


def reduction_instance(N, clauses):
    """The referee's reduction from positive 1-in-3-SAT.  States: one per variable 0..N-1, one extra state z, and
    the all-plus state.  Sites: the empty set, {k}, each clause A, A + z, and A + B + z for two clauses; the state
    of a variable (or of z) is -1 exactly on the sites that contain it."""
    z = N
    sets = [frozenset()] + [frozenset([k]) for k in range(N)]
    for A in clauses:
        sets += [frozenset(A), frozenset(A) | {z}]
    for A, B in itertools.combinations(clauses, 2):
        sets.append(frozenset(A) | frozenset(B) | {z})
    sets = list(dict.fromkeys(sets))
    return [tuple(-1 if k in s else 1 for s in sets) for k in range(N + 1)] + [tuple(1 for _ in sets)]


def check_reduction(trials=60, seed=3):
    rng = random.Random(seed)
    mism = sat = notexp = done = 0
    while done < trials:
        N, M = rng.randint(4, 7), rng.randint(2, 4)
        clauses = []
        while len(clauses) < M:
            A = tuple(sorted(rng.sample(range(N), 3)))
            if A not in clauses:
                clauses.append(A)
        if set(k for A in clauses for k in A) != set(range(N)):
            continue
        done += 1
        V = reduction_instance(N, clauses)
        hitting = [U for r in range(1, N + 1) for U in itertools.combinations(range(N), r)
                   if all(len(set(U) & set(A)) == 1 for A in clauses)]
        canon = lambda v: tuple(v) if v[0] > 0 else tuple(-x for x in v)
        extra = set(sign_vectors_in_span(V)) - set(canon(v) for v in V)
        pred = set()
        for U in hitting:
            y = [sum(V[k][i] for k in U) - V[N][i] + (2 - len(U)) * V[N + 1][i] for i in range(len(V[0]))]
            pred.add(canon(y))
        mism += pred != extra
        sat += bool(hitting)
        notexp += is_exposed_span(V)[0] != "yes"
    print(f"   {trials} instances ({sat} with an exact hitting set): extra sign vectors differ from the exact hitting "
          f"sets in {mism} cases; instances that are not exposed: {notexp} (expected 0)")
    return mism == 0 and notexp == 0


def check_timing():
    rng = random.Random(11)
    for K, n in ((8, 40), (10, 60), (12, 80)):
        V = [tuple(rng.choice((1, -1)) for _ in range(n)) for _ in range(K)]
        t0 = time.time()
        status = is_exposed_span(V)[0]
        cand = len(sign_vectors_in_span([v if v[0] > 0 else tuple(-x for x in v) for v in V]))
        print(f"   K = {K}, n = {n} random states: {status}; sign vectors in the span: {cand}; {time.time() - t0:.1f} s")
    return True


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = []
    if which in ("all", "agree"):
        print("[agree] span-restricted LP against the full LP"); res.append(check_agree())
    if which in ("all", "singletons"):
        print("[singletons] m singleton states on m sites"); res.append(check_singletons())
    if which in ("all", "conditions"):
        print("[conditions] sufficient conditions on the K = 5 table"); res.append(check_conditions())
    if which in ("all", "reduction"):
        print("[reduction] positive 1-in-3-SAT -> another sign vector in the span"); res.append(check_reduction())
    if which in ("all", "timing"):
        print("[timing]"); res.append(check_timing())
    print("ALL OK" if all(res) else "FAILURE")
