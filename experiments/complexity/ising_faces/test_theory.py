"""Tests of the statements of docs/complexity/ISING_GROUND_SETS.md against the exact decision procedure.

 (1) Theorem 2 (twin reduction): deciding on all n sites (twins kept) agrees with deciding on the type set.
 (2) K = 4 rule: exposed  <=>  not (product of the four states constant and four distinct column types).
 (3) Proposition 5: not exposed  =>  the span of the states contains another sign vector.
 (4) Corollary 7: 1 and the products t_k t_l linearly independent on the types  =>  exposed.
 (5) Proposition 10 (characters): for H in F_2^r the characters chi_h, h in H, are exposed  <=>  H has no four
     distinct elements with zero sum (all subsets of F_2^3 with at least 2 elements; random subsets of F_2^4).
"""
import itertools, random
import numpy as np
from faces import decide, reduce_types, states
from span_rule import other_sign_vectors_in_span, quad_independent


def columns(vectors):
    cols = []
    for i in range(len(vectors[0])):
        col = tuple(v[i] for v in vectors)
        if col[0] < 0:
            col = tuple(-c for c in col)
        cols.append(col)
    return cols


def test_reduction(rng, trials=300):
    cnt = {"yes": 0, "no": 0, "degenerate": 0}
    for _ in range(trials):
        K = rng.choice((3, 4, 4, 5))
        n = rng.randint(4, 9)
        # few distinct columns so that twins occur
        base = [tuple(rng.choice((1, -1)) for _ in range(K)) for _ in range(rng.randint(2, 6))]
        cols = [rng.choice(base) for _ in range(n)]
        cols = [tuple(s * c for c in col) for col, s in ((c, rng.choice((1, -1))) for c in cols)]
        vectors = [tuple(col[k] for col in cols) for k in range(K)]
        full = decide(columns(vectors))[0]                # all n sites, twins kept
        red = decide(reduce_types(vectors))[0]
        assert full == red, (vectors, full, red)
        cnt[red] += 1
    return cnt


def test_k4(rng, trials=400):
    cnt = {"yes": 0, "no": 0}
    for _ in range(trials):
        n = rng.randint(3, 9)
        if rng.random() < 0.5:                             # plant a constant product
            a = [rng.choice((1, -1)) for _ in range(n)]
            b = [rng.choice((1, -1)) for _ in range(n)]
            c = [rng.choice((1, -1)) for _ in range(n)]
            d = [a[i] * b[i] * c[i] for i in range(n)]
            vectors = [tuple(a), tuple(b), tuple(c), tuple(d)]
        else:
            vectors = [tuple(rng.choice((1, -1)) for _ in range(n)) for _ in range(4)]
        types = reduce_types(vectors)
        status = decide(types)[0]
        if status == "degenerate":
            continue
        prod_const = len({np.prod([v[i] for v in vectors]) for i in range(n)}) == 1
        rule = "no" if (prod_const and len(types) == 4) else "yes"
        assert status == rule, (vectors, status, rule)
        cnt[status] += 1
    return cnt


def test_span_and_quadratic(rng, trials=300):
    n_no = n_qi = 0
    for _ in range(trials):
        K = rng.choice((4, 5, 6))
        n = rng.randint(4, 9)
        vectors = [tuple(rng.choice((1, -1)) for _ in range(n)) for _ in range(K)]
        if rng.random() < 0.5 and K >= 4:                  # plant an obstruction
            v = list(vectors)
            v[3] = tuple(v[0][i] * v[1][i] * v[2][i] for i in range(n))
            vectors = v
        types = reduce_types(vectors)
        status = decide(types)[0]
        if status == "degenerate":
            continue
        if status == "no":
            assert other_sign_vectors_in_span(types), vectors
            n_no += 1
        if quad_independent(types):
            assert status == "yes", vectors
            n_qi += 1
    return n_no, n_qi


def test_characters(rng):
    out = []
    for r, subsets in ((3, None), (4, 12)):
        pts = list(itertools.product((0, 1), repeat=r))
        cases = 0
        if subsets is None:
            fams = [H for size in range(2, 2 ** r + 1) for H in itertools.combinations(pts, size)]
        else:
            fams = [tuple(rng.sample(pts, rng.randint(3, 6))) for _ in range(subsets)]
        for H in fams:
            vectors = [tuple((-1) ** sum(a * b for a, b in zip(h, s)) for s in pts) for h in H]
            status = decide(reduce_types(vectors))[0]
            sidon = not any(all((h1[i] + h2[i] + h3[i] + h4[i]) % 2 == 0 for i in range(r))
                            for h1, h2, h3, h4 in itertools.combinations(H, 4))
            assert status == ("yes" if sidon else "no"), (H, status, sidon)
            cases += 1
        out.append((r, cases))
    return out


if __name__ == "__main__":
    rng = random.Random(5)
    print("(1) twin reduction, full vs reduced:", test_reduction(rng))
    print("(2) K = 4 rule:", test_k4(rng))
    print("(3),(4) not exposed => other sign vector in span; quadratically independent => exposed: (cases)", test_span_and_quadratic(rng))
    print("(5) characters / Sidon sets (r, number of families):", test_characters(rng))
    print("ALL OK")
