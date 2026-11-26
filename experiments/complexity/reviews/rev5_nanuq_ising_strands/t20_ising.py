# t20_ising.py -- REVIEWER'S OWN TESTS: Prop. 12, Prop. 13, Cor. 5a, Prop. 13' numbers
import itertools, random, math, collections, sys
from fractions import Fraction
from ising_mine import *

rng = random.Random(2026)

# ---- Proposition 12: singleton states are not exposed (full LP over all states) ----
for m in range(3, 9):
    S = []
    for i in range(m):
        s = [1] * m; s[i] = -1; S.append(canon(s))
    S = sorted(set(S))
    one = canon([1] * m)
    for V, name in ((S, 'singletons'), (S + [one], 'singletons + all-ones')):
        Vs = set(V)
        others = [y for y in all_states(m) if y not in Vs]
        t = exposed_lp(V, others, m)
        print("m = %d %-22s |V| = %d  margin %.6f -> %s" % (m, name, len(V), t, 'exposed' if t > 1e-7 else 'NOT exposed'))

# ---- Proposition 13: zero set of x^T (I - Pi_L) x ; rational coefficients; pair energy + constant ----
stats = collections.Counter()
for trial in range(400):
    n = rng.randint(4, 11); K = rng.randint(1, min(6, n))
    V = set()
    while len(V) < K:
        V.add(canon([rng.choice((1, -1)) for _ in range(n)]))
    V = sorted(V)
    Pi = projector(V)
    Q = [[(1 if i == j else 0) - Pi[i][j] for j in range(n)] for i in range(n)]
    zero = set()
    for y in all_states(n):
        val = sum(Q[i][j] * y[i] * y[j] for i in range(n) for j in range(n))
        assert val >= 0
        if val == 0:
            zero.add(y)
        # value as constant + pair energy
    sv = sign_vectors_in_span(V)
    sv2 = sign_vectors_in_span_bruteforce(V)
    assert sv == sv2, "two span enumerations disagree"
    stats['instances'] += 1
    if zero != sv: stats['ZERO SET != SIGN VECTORS OF L'] += 1
    other = sv - set(V)
    stats['span contains another sign vector'] += bool(other)
    # (ii) => (i): if no other sign vector, the ground-state set of the pair energy is exactly V
    if not other and zero != set(V): stats['(ii)=>(i) VIOLATED'] += 1
    # (i) => (ii) tested through its consequence: any PSD A with A x^k = 0 vanishes on all sign vectors of L
    #  (random PSD A = B^T B with B's rows orthogonal to L, exact integers)
    if other:
        # rows orthogonal to L: (I - Pi) e_i scaled
        B = [Q[i] for i in range(n)]
        w = [Fraction(rng.randint(1, 5)) for _ in range(n)]
        for y in other:
            val = sum(w[i] * (sum(B[i][j] * y[j] for j in range(n))) ** 2 for i in range(n))
            if val != 0: stats['(i)=>(ii) consequence VIOLATED'] += 1
print("Proposition 13 on random instances:", dict(stats))

# ---- Corollary 5a / Proposition 5: full LP (all states) versus LP restricted to the sign vectors of L ----
stats = collections.Counter()
for trial in range(600):
    n = rng.randint(4, 10); K = rng.randint(2, 6)
    # few column types so that non-exposed sets are frequent
    ntypes = rng.randint(2, min(n, 2 ** (K - 1)))
    types = []
    while len(types) < ntypes:
        t = tuple([1] + [rng.choice((1, -1)) for _ in range(K - 1)]) if rng.random() < 0.5 else tuple(rng.choice((1, -1)) for _ in range(K))
        if t not in types and tuple(-x for x in t) not in types:
            types.append(t)
    cols = [rng.choice(types) for _ in range(n)]
    cols[:len(types)] = types[:n]
    V = [canon([cols[i][k] for i in range(n)]) for k in range(K)]
    if len(set(V)) < K:
        stats['degenerate (skipped)'] += 1; continue
    Vs = set(V)
    full = exposed_lp(V, [y for y in all_states(n) if y not in Vs], n)
    sv = sign_vectors_in_span(V)
    restr = exposed_lp(V, sorted(sv - Vs), n)
    e1 = full > 1e-7; e2 = restr > 1e-7
    stats['instances'] += 1
    stats['exposed' if e1 else 'not exposed'] += 1
    if e1 != e2: stats['FULL LP != RESTRICTED LP'] += 1
    if not e1 and not (sv - Vs): stats['PROP 5 VIOLATED'] += 1
    if not (sv - Vs): stats['no other sign vector in span'] += 1
print("Corollary 5a (full LP vs LP over the sign vectors of the span):", dict(stats))

# ---- Proposition 13': the numbers ----
f = lambda c: c * (1 + math.log(1 / c) + math.log(2)) + (1 - c) * math.log(3 / 4)
print("exponent at c = 1/20: %.5f ;  d/dc at 1/20: %.4f (= ln(8/(3c)) = %.4f)" % (f(0.05), (f(0.05 + 1e-7) - f(0.05)) / 1e-7, math.log(8 / (3 * 0.05))))
for n, K in ((100, 5), (200, 10)):
    b = 2.0 ** (K - n) + math.comb(n, K) * 2 ** K * 0.75 ** (n - K)
    print("bound for n = %d, K = %d: %.3g" % (n, K, b))
print("4*C(3,3)*(3/4)^12 = %.3f ; 4*C(4,3)*(3/4)^16 = %.3f" % (4 * 0.75 ** 12, 16 * 0.75 ** 16))
# P(c.t in {+1,-1}) <= 3/4 for c with at least two non-zero entries: exhaustive over a grid of rational c
worst = Fraction(0)
vals = [Fraction(a, b) for a in range(-6, 7) for b in (1, 2, 3)]
vals = sorted(set(vals))
for K in (2, 3, 4):
    for c in itertools.product(vals, repeat=K):
        if sum(1 for x in c if x != 0) < 2: continue
        cnt = sum(1 for t in itertools.product((1, -1), repeat=K) if abs(sum(a * b for a, b in zip(c, t))) == 1)
        p = Fraction(cnt, 2 ** K)
        if p > worst: worst, wc = p, c
    print("K = %d: max over the grid of P(c.t = +-1) = %s (attained e.g. at c = %s)" % (K, worst, [str(x) for x in wc]))
# simulation: frequency of 'another sign vector in the span' for small systems
for n, K in ((12, 3), (16, 4), (12, 6)):
    hit = 0; T = 300
    for _ in range(T):
        V = [canon([rng.choice((1, -1)) for _ in range(n)]) for _ in range(K)]
        sv = sign_vectors_in_span(V)
        hit += bool(sv - set(V))
    print("n = %d, K = %d: span contains another sign vector in %d of %d trials (%.0f%%)" % (n, K, hit, T, 100 * hit / T))
