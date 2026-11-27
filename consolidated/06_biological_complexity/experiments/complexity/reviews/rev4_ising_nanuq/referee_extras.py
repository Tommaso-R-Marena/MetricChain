"""Referee's own additional checks for ISING_GROUND_SETS.md (things the note does not say or says wrongly)."""
import itertools, random, sys, time
from fractions import Fraction
from collections import Counter
import numpy as np
import sympy
from ising_core import *

rng = random.Random(777)
S = lambda x: "".join("+" if v > 0 else "-" for v in x)


# ---------------------------------------------------------------- a. the "l1-rigidity" formulation of section 6
def test_rigidity():
    print("[a] section 6, 'equivalent formulation' (exposed <=> unique decomposition of the Hamming metric):")
    for name, V in [
        ("all 8 states of 4 sites", [tuple(int(v) for v in s) for s in all_states(4)]),
        ("the 12 roots of the triangle inequality x1x2+x1x3+x2x3 >= -1 on 5 sites",
         [tuple(int(v) for v in s) for s in all_states(5) if s[0] * s[1] + s[0] * s[2] + s[1] * s[2] == -1]),
    ]:
        res = decide(V)
        K, m = len(V), len(V[0])
        # gauge x^1 = all plus ; cuts S_k = {i : x^k_i = -1}; Hamming metric of the types = sum_k delta(S_k)
        x1 = V[0]
        W = [tuple(a * b for a, b in zip(x, x1)) for x in V]
        cuts = W[1:]
        pr = pairs(m)
        delta = lambda w: [int(w[i] != w[j]) for (i, j) in pr]
        D = [delta(w) for w in cuts]
        d = [sum(col) for col in zip(*D)]
        rank = sympy.Matrix(D).rank()
        # a second non-negative decomposition using ONLY the cuts of V: move along a linear dependency
        ns = sympy.Matrix(D).T.nullspace()
        second = None
        if ns:
            v = [Fraction(int(e.p), int(e.q)) for e in ns[0]]
            t = min(Fraction(1) / abs(e) for e in v if e != 0)
            lam = [1 + t * e for e in v]
            assert all(l >= 0 for l in lam) and any(l != 1 for l in lam)
            assert [sum(l * row[c] for l, row in zip(lam, D)) for c in range(len(pr))] == d
            second = lam
        print("    V = %s: K=%d, exposed=%s, cuts %d, rank of the cut vectors %d -> %s"
              % (name, K, res.exposed, len(cuts), rank,
                 "NOT l1-rigid: second decomposition with coefficients %s" % [str(l) for l in second] if second else "rigid"))


# ---------------------------------------------------------------- b. isometric subgraphs of the cube (known sufficient condition)
def isometric_base(types, k0):
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


def cor7(types):
    K = len(types[0])
    rows = [[1] + [t[k] * t[l] for k in range(K) for l in range(k + 1, K)] for t in types]
    return sympy.Matrix(rows).rank() == 1 + K * (K - 1) // 2


def test_isometric():
    import json
    res = json.load(open("k5_results.json"))
    K = 5
    types = [(1,) + t for t in itertools.product([1, -1], repeat=K - 1)]
    cnt = Counter()
    for r in res:
        ts = [types[i] for i in range(16) if r["mask"] >> i & 1]
        iso = any(isometric_base(ts, k0) for k0 in range(K))
        c7 = cor7(ts)
        w = r["orbit_size"]
        cnt["sets"] += w
        cnt["exposed"] += w * r["exposed"]
        cnt["Cor7 applies"] += w * c7
        cnt["isometric applies"] += w * iso
        cnt["either applies"] += w * (c7 or iso)
        cnt["no extra sign vector in span (Prop 5 certifies)"] += w * (r["n_extra_sign_vectors"] == 0)
        if iso and not r["exposed"]:
            cnt["ISOMETRIC BUT NOT EXPOSED"] += w
        if c7 and not r["exposed"]:
            cnt["COR7 BUT NOT EXPOSED"] += w
    print("[b] K=5, all 61719 non-degenerate type sets (by orbit):", dict(cnt))


# ---------------------------------------------------------------- c. 'another sign vector in the span' is NP-complete
def span_instance(N, clauses):
    """states: variables 0..N-1, then z1, then the all-plus state.  Sites: empty set, {k}, A_i, A_i+z1, A_i+A_j+z1."""
    z1 = N
    sets = [frozenset()] + [frozenset([k]) for k in range(N)]
    for A in clauses:
        sets.append(frozenset(A))
        sets.append(frozenset(A) | {z1})
    for A, B in itertools.combinations(clauses, 2):
        sets.append(frozenset(A) | frozenset(B) | {z1})
    sets = list(dict.fromkeys(sets))
    V = [tuple(-1 if k in s else 1 for s in sets) for k in range(N + 1)] + [tuple(1 for _ in sets)]
    return V


def test_span_hardness(trials=60):
    mism = 0
    with_sol = 0
    not_exposed = 0
    for it in range(trials):
        N = rng.randint(4, 7)
        M = rng.randint(2, 4)
        clauses = []
        while len(clauses) < M:
            A = tuple(sorted(rng.sample(range(N), 3)))
            if A not in clauses:
                clauses.append(A)
        if set(k for A in clauses for k in A) != set(range(N)):
            continue
        V = span_instance(N, clauses)
        assert distinct_states(V)
        hitting = [U for r in range(1, N + 1) for U in itertools.combinations(range(N), r)
                   if all(len(set(U) & set(A)) == 1 for A in clauses)]
        Y, _ = sign_vectors_in_span(V)
        extra = set(Y) - set(canon(x) for x in V)
        # predicted extra vectors
        pred = set()
        Xn = np.array(V)
        for U in hitting:
            y = Xn[list(U)].sum(axis=0) - Xn[N] + (2 - len(U)) * Xn[N + 1]
            assert set(np.abs(y)) == {1}
            pred.add(canon(y))
        if pred != extra:
            mism += 1
        with_sol += bool(hitting)
        res = decide_span(V)
        not_exposed += (not res.exposed)
    print("[c] reduction from positive 1-in-3-SAT to 'another sign vector in the span': %d instances, %d satisfiable; "
          "extra sign vectors != exact hitting sets in %d cases; instances NOT exposed: %d (expected 0)"
          % (trials, with_sol, mism, not_exposed))


# ---------------------------------------------------------------- d. K = 6 sampling
def test_k6(trials=4000):
    K = 6
    alltypes = [(1,) + t for t in itertools.product([1, -1], repeat=K - 1)]
    cnt = Counter()
    examples = []
    t0 = time.time()
    for it in range(trials):
        m = rng.randint(5, 20)
        mode = rng.random()
        if mode < 0.4:
            ts = rng.sample(alltypes, m)
        elif mode < 0.7:
            # types with a prescribed linear relation to make the span rich: t.c in {+-1} for a random small c
            cs = rng.choice([(1, 1, -1, 0, 0, 0), (1, 1, 1, -1, 0, 0), (1, 1, 1, 1, -1, 0), (1, 1, 1, 1, 1, -1), (1, 1, 1, 1, 1, 1)])
            perm = rng.sample(range(K), K)
            c = [0] * K
            for i, p in enumerate(perm):
                c[p] = cs[i]
            nz = sum(1 for v in c if v)
            target = {3: 1, 4: 2, 5: 3, 6: 4}[nz]
            pool = [t for t in alltypes if abs(sum(a * b for a, b in zip(c, t))) == target]
            ts = rng.sample(pool, min(m, len(pool)))
        else:
            Q = rng.sample(range(K), 4)
            pool = [t for t in alltypes if t[Q[0]] * t[Q[1]] * t[Q[2]] * t[Q[3]] == 1]
            ts = rng.sample(pool, min(m, len(pool)))
        V = states_from_types(ts)
        if not distinct_states(V):
            continue
        cnt["instances"] += 1
        res = decide_span(V)
        Y, _ = sign_vectors_in_span(V)
        extra = set(Y) - set(canon(x) for x in V)
        if len(ts) <= 13:
            full = decide(V)
            cnt["full LP also run"] += 1
            if full.exposed != res.exposed:
                cnt["FULL vs SPAN MISMATCH"] += 1
        quads = [Q for Q in itertools.combinations(range(K), 4)
                 if len(set(t[Q[0]] * t[Q[1]] * t[Q[2]] * t[Q[3]] for t in ts)) == 1]
        if not res.exposed:
            cnt["not exposed"] += 1
            if not extra:
                cnt["PROP 5 VIOLATION"] += 1
            if not quads:
                cnt["not exposed, no 4 states with constant product"] += 1
                # does it contain five states that are 'singleton-like' (every column has exactly one deviant among them)?
                five = False
                for Q in itertools.combinations(range(K), 5):
                    for sg in itertools.product([1, -1], repeat=4):
                        s = (1,) + sg
                        if all(abs(sum(s[i] * t[q] for i, q in enumerate(Q))) == 3 for t in ts):
                            five = True
                if five:
                    cnt["  ... of these, containing 5 singleton-like states"] += 1
                else:
                    cnt["  ... of these, with neither obstruction"] += 1
                    if len(examples) < 3:
                        examples.append([S(x) for x in V])
            if cor7(ts):
                cnt["COR 7 VIOLATION"] += 1
            if any(isometric_base(ts, k0) for k0 in range(K)):
                cnt["ISOMETRIC CONDITION VIOLATION"] += 1
        else:
            cnt["exposed"] += 1
            if quads:
                # Lemma 8: then all four y^k must be in V for every such quadruple
                Xn = np.array(V)
                Vc = set(canon(x) for x in V)
                for Q in quads:
                    X4 = Xn[list(Q)].copy()
                    if int(np.prod(X4[:, 0])) * 1 != 1 or True:
                        # make the product +1 by negating one state if needed
                        if np.prod(X4, axis=0)[0] == -1:
                            X4[0] *= -1
                    Yk = [tuple(int(v) for v in (X4.sum(axis=0) // 2 - X4[k])) for k in range(4)]
                    if not all(canon(y) in Vc for y in Yk):
                        cnt["LEMMA 8 VIOLATION"] += 1
        if rank_exact([list(x) for x in V]) == K:
            from ising_tests import theorem6_diag
            diag, nC = theorem6_diag(V)
            cnt["Theorem 6 checked"] += 1
            if diag == res.exposed:
                cnt["THEOREM 6 VIOLATION"] += 1
    print("[d] K=6 sampling:", dict(cnt), "time %.0f s" % (time.time() - t0))
    for e in examples:
        print("     example with neither obstruction:", e)


# ---------------------------------------------------------------- e. the 2^K poly(n) algorithm
def test_fpt():
    print("[e] span-reduced algorithm (at most 2^(K-1) candidate states instead of 2^(n-1)):")
    for K, n in [(8, 40), (10, 60), (12, 60), (14, 80)]:
        t0 = time.time()
        V = []
        while len(V) < K:
            x = canon([rng.choice([1, -1]) for _ in range(n)])
            if x not in V:
                V.append(x)
        res = decide_span(V)
        Y, _ = sign_vectors_in_span(V)
        # a structured non-exposed instance of the same size: plant four states with constant product
        W = list(V)
        W[3] = canon(tuple(a * b * c for a, b, c in zip(W[0], W[1], W[2])))
        res2 = decide_span(W)
        print("    K=%d n=%d: random states exposed=%s (sign vectors in span: %d) ; with a planted constant-product "
              "quadruple exposed=%s ; %.1f s" % (K, n, res.exposed, len(Y), res2.exposed, time.time() - t0))


if __name__ == "__main__":
    which = sys.argv[1:] or ["a", "b", "c", "d", "e"]
    if "a" in which: test_rigidity()
    if "b" in which: test_isometric()
    if "c" in which: test_span_hardness()
    if "e" in which: test_fpt()
    if "d" in which: test_k6()
