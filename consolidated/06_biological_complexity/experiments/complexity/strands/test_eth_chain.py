"""Brute-force sanity tests of the two reductions of Appendix A of docs/complexity/STRANDS_NN_HARDNESS.md
(the linear-size chain behind the ETH corollary).

 Lemma A1:  3-CNF formula with m clauses  ->  3DM instance with q = 2L elements per class and <= 21 m triples
            (Garey-Johnson's reduction with slot-sized variable wheels and *local* garbage collection);
            formula satisfiable  <=>  perfect matching.
 Lemma A2:  3DM instance (q, T)  ->  exact bin packing with 4|T| items, |T| bins, B = 40 r^4 + 15, r = 32 q
            (Garey-Johnson's reduction to 4-PARTITION);  perfect matching  <=>  exact packing.

Both sides are decided by exhaustive search on small random instances.
"""
import itertools, random, sys


# ---------------------------------------------------------------- Lemma A1
def sat_bruteforce(nvars, clauses):
    for bits in itertools.product((False, True), repeat=nvars):
        if all(any(bits[v] == sign for v, sign in cl) for cl in clauses):
            return True
    return False


def sat_to_3dm(clauses):
    """clauses: list of lists of (variable, sign).  Returns (W, X, Y, T) with elements as tuples."""
    slots = {}                      # variable -> list of (clause index, position, sign)
    for ci, cl in enumerate(clauses):
        for pos, (v, sign) in enumerate(cl):
            slots.setdefault(v, []).append((ci, pos, sign))
    W, X, Y, T = [], [], [], []
    tip_of = {}                     # (clause, pos) -> (positive tip, negative tip)
    for v, sl in slots.items():
        d = len(sl)
        for j, (ci, pos, sign) in enumerate(sl):
            p, n = ("p", v, j), ("n", v, j)
            W += [p, n]
            X.append(("a", v, j))
            Y.append(("b", v, j))
            tip_of[(ci, pos)] = (p, n)
        for j in range(d):
            T.append((("n", v, j), ("a", v, j), ("b", v, j)))                    # "true" triple
            T.append((("p", v, j), ("a", v, (j + 1) % d), ("b", v, j)))          # "false" triple
    for ci, cl in enumerate(clauses):
        c1, c2 = ("c1", ci), ("c2", ci)
        X.append(c1)
        Y.append(c2)
        for pos, (v, sign) in enumerate(cl):
            p, n = tip_of[(ci, pos)]
            T.append((p if sign else n, c1, c2))
        for r in range(len(cl) - 1):
            g1, g2 = ("g1", ci, r), ("g2", ci, r)
            X.append(g1)
            Y.append(g2)
            for pos in range(len(cl)):
                for t in tip_of[(ci, pos)]:
                    T.append((t, g1, g2))
    assert len(W) == len(X) == len(Y)
    return W, X, Y, T


def exact_cover(universe, sets):
    """is there a subfamily of `sets` (each an iterable of elements) partitioning `universe`?"""
    universe = list(universe)
    by_el = {u: [] for u in universe}
    for s in sets:
        for u in s:
            by_el[u].append(frozenset(s))
    covered = set()

    def rec():
        if len(covered) == len(universe):
            return True
        u = min((x for x in universe if x not in covered),
                key=lambda x: sum(1 for s in by_el[x] if not (s & covered)))
        for s in by_el[u]:
            if not (s & covered):
                covered.update(s)
                if rec():
                    return True
                covered.difference_update(s)
        return False
    return rec()


def test_A1(trials, rng):
    stats = {True: 0, False: 0}
    for _ in range(trials):
        nvars = rng.randint(1, 4)
        m = rng.randint(1, 7)
        clauses = []
        for _ in range(m):
            k = rng.choice((1, 2, 3, 3, 3))
            clauses.append([(rng.randrange(nvars), rng.random() < 0.5) for _ in range(k)])
        W, X, Y, T = sat_to_3dm(clauses)
        L = sum(len(c) for c in clauses)
        assert len(W) == 2 * L and len(T) <= 21 * m and len(set(T)) == len(T)
        a = sat_bruteforce(nvars, clauses)
        b = exact_cover(W + X + Y, T)
        assert a == b, (clauses, a, b)
        stats[a] += 1
    return stats


# ---------------------------------------------------------------- Lemma A2
def tdm_to_binpacking(q, T):
    """T: list of triples (i, j, k), 1 <= i,j,k <= q, every element in at least one triple.
    Returns (sizes, m, B)."""
    r = 32 * q
    Nw, Nx, Ny = {}, {}, {}
    for i, j, k in T:
        Nw[i] = Nw.get(i, 0) + 1
        Nx[j] = Nx.get(j, 0) + 1
        Ny[k] = Ny.get(k, 0) + 1
    sizes = []
    for i, c in Nw.items():
        sizes += [10 * r**4 + i * r + 1] + [11 * r**4 + i * r + 1] * (c - 1)
    for j, c in Nx.items():
        sizes += [10 * r**4 + j * r**2 + 2] + [11 * r**4 + j * r**2 + 2] * (c - 1)
    for k, c in Ny.items():
        sizes += [10 * r**4 + k * r**3 + 4] + [8 * r**4 + k * r**3 + 4] * (c - 1)
    for i, j, k in T:
        sizes.append(10 * r**4 - k * r**3 - j * r**2 - i * r + 8)
    B = 40 * r**4 + 15
    assert len(sizes) == 4 * len(T) and sum(sizes) == len(T) * B
    assert all(5 * s > B and 3 * s < B for s in sizes)
    return sizes, len(T), B


def exact_packing(sizes, m, B):
    """generic exact bin packing by exact cover over all subsets of sum B (found by meet-in-the-middle on pairs)."""
    n = len(sizes)
    pair = {}
    for a, b in itertools.combinations(range(n), 2):
        pair.setdefault(sizes[a] + sizes[b], []).append((a, b))
    quads = set()
    for s, lst in pair.items():
        for a, b in lst:
            for c, d in pair.get(B - s, ()):
                if len({a, b, c, d}) == 4:
                    quads.add(frozenset((a, b, c, d)))
    # sizes lie strictly between B/5 and B/3, so every bin of an exact packing has exactly four items
    return exact_cover(range(n), quads)


def test_A2(trials, rng):
    stats = {True: 0, False: 0}
    for _ in range(trials):
        q = rng.randint(1, 3)
        allt = list(itertools.product(range(1, q + 1), repeat=3))
        T = rng.sample(allt, rng.randint(q, min(len(allt), 9)))
        if (len({t[0] for t in T}) < q or len({t[1] for t in T}) < q or len({t[2] for t in T}) < q):
            continue
        a = exact_cover([("w", i) for i in range(1, q + 1)] + [("x", i) for i in range(1, q + 1)]
                        + [("y", i) for i in range(1, q + 1)],
                        [(("w", i), ("x", j), ("y", k)) for i, j, k in T])
        sizes, m, B = tdm_to_binpacking(q, T)
        b = exact_packing(sizes, m, B)
        assert a == b, (q, T, a, b)
        stats[a] += 1
    return stats


if __name__ == "__main__":
    rng = random.Random(11)
    s1 = test_A1(1500, rng)
    print("Lemma A1 (3-SAT -> 3DM, local garbage collection): satisfiable / unsatisfiable instances tested:", s1[True], "/", s1[False])
    s2 = test_A2(600, rng)
    print("Lemma A2 (3DM -> exact bin packing): solvable / unsolvable instances tested:", s2[True], "/", s2[False])
    print("ALL OK")
