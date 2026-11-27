# t21_thm14.py -- REVIEWER'S OWN TEST of Theorem 14 (reduction positive 1-in-3-SAT -> SPAN) and of (c)
import itertools, random, collections
from fractions import Fraction
from ising_mine import *

rng = random.Random(14)

def build(N, clauses):
    """states x^1..x^N, x^z, 1 on the sites {}, {k}, A_i, A_i+z, A_i+A_j+z (i<j); returns (states, sites)"""
    z = N
    sites = [frozenset()]
    sites += [frozenset([k]) for k in range(N)]
    sites += [frozenset(A) for A in clauses]
    sites += [frozenset(A) | {z} for A in clauses]
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            sites.append(frozenset(clauses[i]) | frozenset(clauses[j]) | {z})
    states = []
    for k in range(N + 1):
        states.append(tuple(-1 if k in s else 1 for s in sites))
    states.append(tuple(1 for s in sites))
    return states, sites

st = collections.Counter()
for trial in range(1500):
    N = rng.randint(3, 8)
    M = rng.randint(1, 6)
    clauses = [tuple(sorted(rng.sample(range(N), 3))) for _ in range(M)]
    if set(v for A in clauses for v in A) != set(range(N)):
        st['skipped (a variable in no clause)'] += 1
        continue
    states, sites = build(N, clauses)
    K = N + 2
    # pairwise different (up to sign) and linearly independent
    R, piv = rref(states)
    assert len(piv) == K, "states not linearly independent"
    V = [canon(s) for s in states]
    assert len(set(V)) == K
    sv = sign_vectors_in_span(states)
    other = sv - set(V)
    # exact hitting sets by brute force
    sols = [U for U in itertools.product((0, 1), repeat=N) if all(sum(U[v] for v in A) == 1 for A in clauses)]
    expect = set()
    for U in sols:
        vec = [sum(states[k][s] for k in range(N) if U[k]) - states[N][s] + (2 - sum(U)) * 1 for s in range(len(sites))]
        assert all(x in (1, -1) for x in vec), "the vector of the proof is not a sign vector"
        expect.add(canon(vec))
    st['instances'] += 1
    st['satisfiable'] += bool(sols)
    st['total solutions'] += len(sols)
    if other != expect:
        st['MISMATCH other sign vectors != exact hitting sets'] += 1
        print("MISMATCH", N, clauses, len(other), len(expect))
    if len(expect) != len(sols): st['two solutions give the same vector'] += 1
    # (c): exposed?  LP restricted to the sign vectors of the span (valid by Prop. 5 / Cor. 5a) ...
    t = exposed_lp(V, sorted(other), len(sites))
    if t <= 1e-7:
        st['(c) VIOLATED: not exposed (restricted LP)'] += 1
    # ... and, for small numbers of sites, the full LP over all states
    if len(sites) <= 13:
        Vs = set(V)
        tf = exposed_lp(V, [y for y in all_states(len(sites)) if y not in Vs], len(sites))
        st['full LP run'] += 1
        if tf <= 1e-7: st['(c) VIOLATED: not exposed (full LP)'] += 1
    st['max sites'] = max(st['max sites'], len(sites))
print(dict(st))
