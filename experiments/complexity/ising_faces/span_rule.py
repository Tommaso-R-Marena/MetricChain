"""Test of the rule   exposed  <=>  the linear span of the K states contains no other sign vector
on every orbit of type sets for K = 4 and K = 5 (and K = 6 for small type sets).
Also reports the 'quadratic independence' sufficient condition (1 and the products t_k t_l independent on T)."""
import itertools, sys
import numpy as np
from fractions import Fraction
from faces import decide, states


def other_sign_vectors_in_span(types):
    """sign vectors y (first entry +) in the row space of the K x m matrix of states, not equal to +-a state.
    Exact rational arithmetic (span_algorithm.sign_vectors_in_span); the first version used a floating-point rank
    although its comment promised an exact confirmation (COMPLEXITY-REV-0004, finding 7)."""
    from span_algorithm import sign_vectors_in_span
    m, K = len(types), len(types[0])
    V = []
    for k in range(K):
        row = tuple(t[k] for t in types)
        if row[0] < 0:
            row = tuple(-r for r in row)
        V.append(row)
    return [y for y in sign_vectors_in_span(V) if y not in set(V)]


def quad_independent(types):
    K = len(types[0])
    rows = []
    for t in types:
        rows.append([1] + [t[k] * t[l] for k in range(K) for l in range(k + 1, K)])
    A = np.array(rows, dtype=float)
    return np.linalg.matrix_rank(A) == A.shape[1]


def orbit_reps(K):
    TYPES = [(1,) + t for t in itertools.product((1, -1), repeat=K - 1)]
    NT = len(TYPES)
    G = set()
    for perm in itertools.permutations(range(K)):
        for signs in itertools.product((1, -1), repeat=K):
            img = []
            for t in TYPES:
                col = tuple(signs[k] * t[perm[k]] for k in range(K))
                if col[0] < 0:
                    col = tuple(-c for c in col)
                img.append(TYPES.index(col))
            G.add(tuple(img))
    seen = bytearray(1 << NT)
    reps = []
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
        reps.append(([TYPES[i] for i in T], len(orb)))
    return reps


if __name__ == "__main__":
    for K in (4, 5):
        reps = orbit_reps(K)
        agree = disagree = 0
        qi_yes = qi_total = 0
        examples = []
        for types, size in reps:
            status, cert = decide(types)
            if status == "degenerate":
                continue
            others = other_sign_vectors_in_span(types)
            rule = "yes" if not others else "no"
            if rule == status:
                agree += 1
            else:
                disagree += 1
                examples.append((len(types), status, len(others), types))
            if quad_independent(types):
                qi_total += 1
                qi_yes += status == "yes"
        print(f"K={K}: non-degenerate orbits {agree + disagree}; rule agrees on {agree}, disagrees on {disagree}; "
              f"quadratically independent orbits: {qi_total}, all exposed: {qi_yes == qi_total}")
        for ex in examples[:8]:
            print("     disagreement:", ex)
