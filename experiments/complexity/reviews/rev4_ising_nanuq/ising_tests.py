"""Referee's tests of the statements of ISING_GROUND_SETS.md (own code, own instances)."""
import itertools, random, sys, time
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
import sympy
from ising_core import *

rng = random.Random(20261126)
S = lambda x: "".join("+" if v > 0 else "-" for v in x)


def rand_state(m):
    return canon([rng.choice([1, -1]) for _ in range(m)])


def rand_V(m, K):
    while True:
        V = list({rand_state(m) for _ in range(K)})
        if len(V) == K:
            return V


# ------------------------------------------------------------------ 0. the explicit K=5 certificate of the note
def test_sporadic():
    P = lambda s: tuple(1 if ch == "+" else -1 for ch in s)
    V = [P("+++++"), P("++---"), P("+-++-"), P("+-+-+"), P("+--++")]
    mu = {P("++++-"): Fraction(1, 6), P("++--+"): Fraction(1, 6), P("+-+++"): Fraction(1, 3),
          P("+-+--"): Fraction(1, 6), P("+--+-"): Fraction(1, 6)}
    alpha = [Fraction(1, 6), Fraction(1, 6), Fraction(1, 3), Fraction(1, 6), Fraction(1, 6)]
    print("[0] author's sporadic certificate verifies exactly:", verify_certificate(V, mu, alpha))
    # no four states with constant product
    quads = [Q for Q in itertools.combinations(range(5), 4)
             if len(set(int(np.prod([V[k][i] for k in Q])) for i in range(5))) == 1]
    print("    four states with constant product:", quads)
    # gauge to singletons: flip site 2 (index 1)
    g = (1, -1, 1, 1, 1)
    W = [canon(tuple(a * b for a, b in zip(x, g))) for x in V]
    minus = [sorted(i for i in range(5) if (w[i] == -1)) for w in W]
    minus = [mm if len(mm) <= 2 else sorted(set(range(5)) - set(mm)) for mm in minus]
    print("    after flipping site 2 the five states have minus-sets:", minus,
          "-> the five singleton cuts on five sites" if sorted(minus) == [[i] for i in range(5)] else "")
    # family: m singletons on m sites, and 1 + singletons
    for m in range(3, 11):
        sing = [canon([-1 if i == k else 1 for i in range(m)]) for k in range(m)]
        r1 = decide(sing)
        r2 = decide([tuple([1] * m)] + sing) if m >= 3 and m < 10 else None
        print("    m=%d: {m singletons} exposed=%s ; {1}+{m singletons} exposed=%s" %
              (m, r1.exposed, None if r2 is None else r2.exposed))


# ------------------------------------------------------------------ 1. Theorem 1: certificate / Theorem 2: twins
def test_theorem2(trials=400):
    """random instances WITH twins and anti-twins; the unreduced problem is solved by the full LP over all
    2^(n-1) states and compared with the reduced problem."""
    mism = 0
    nexp = 0
    sizes = []
    maxsupp = 0
    for it in range(trials):
        K = rng.choice([3, 4, 4, 5, 5, 6])
        mt = rng.randint(2, 6)                       # number of types
        n = rng.randint(mt + 1, min(11, mt + 5))
        # choose mt different types, then n sites with random types and random signs
        alltypes = [(1,) + t for t in itertools.product([1, -1], repeat=K - 1)]
        if mt > len(alltypes):
            continue
        ts = rng.sample(alltypes, mt)
        V0 = states_from_types(ts)
        if not distinct_states(V0):
            continue
        cols = ts + [rng.choice(ts) for _ in range(n - mt)]
        rng.shuffle(cols)
        cols = [tuple(v * s for v in c) for c, s in zip(cols, [rng.choice([1, -1]) for _ in cols])]
        V = states_from_types(cols)
        Vr, T = twin_reduce(V)
        assert len(Vr[0]) == mt
        assert distinct_states(Vr)                   # first claim of Theorem 2
        full = decide(V)
        red = decide(Vr)
        sizes.append((K, mt, n))
        if full.exposed != red.exposed:
            mism += 1
            print("   MISMATCH", [S(x) for x in V])
        if not full.exposed:
            nexp += 1
            maxsupp = max(maxsupp, len(full.mu))
            assert len(full.mu) <= n * (n - 1) // 2 + 1
        else:
            # the construction in the proof: E(x) = E_J'(x|T) - c * sum_{twins} sigma_ij x_i x_j, ANY c > 0
            for c in (Fraction(1, 1000), Fraction(1), Fraction(1000)):
                Jp = red.J
                J = np.zeros((n, n), dtype=object)
                for a, i in enumerate(T):
                    for b, j in enumerate(T):
                        if a != b:
                            J[i, j] = Fraction(int(Jp[a, b]))
                for i in range(n):
                    for j in range(i + 1, n):
                        ti, tj = type_of_site(V, i), type_of_site(V, j)
                        if ti == tj:
                            sg = 1 if tuple(x[i] for x in V) == tuple(x[j] for x in V) else -1
                            J[i, j] += -c * sg
                            J[j, i] += -c * sg
                st = all_states(n)
                en = [energy(J, x) for x in st]
                mn = min(en)
                gs = set(tuple(int(v) for v in x) for x, e in zip(st, en) if e == mn)
                if gs != set(canon(x) for x in V):
                    mism += 1
                    print("   CONSTRUCTION FAILS c=", c, [S(x) for x in V])
    print("[1] Theorem 2: %d instances with twins (n<=11), mismatches reduced vs unreduced / construction: %d ;"
          " not exposed: %d ; max certificate support %d" % (len(sizes), mism, nexp, maxsupp))


# ------------------------------------------------------------------ 2. Prop 5 / Theorem 6 / Cor 7 on random instances
def C_set(V):
    """Theorem 6: all c (other than +-e_k) with c.t in {+-1} for all types, V linearly independent."""
    Y, _ = sign_vectors_in_span(V)
    Vc = set(canon(x) for x in V)
    out = []
    for y in Y:
        if y in Vc:
            continue
        out.append((y, coefficients(V, y)))
    return out


def theorem6_diag(V):
    """is some convex combination of c c^T (c in C) diagonal?  exact answer via LP + exact check"""
    C = C_set(V)
    K = len(V)
    if not C:
        return False, 0
    prs = [(k, l) for k in range(K) for l in range(k + 1, K)]
    A = [[c[k] * c[l] for (_, c) in C] for (k, l) in prs] + [[1] * len(C)]
    b = [0] * len(prs) + [1]
    x = exact_feasible_nonneg(A, b)
    return x is not None, len(C)


def cor7_condition(types):
    K = len(types[0])
    rows = [[1] + [t[k] * t[l] for k in range(K) for l in range(k + 1, K)] for t in types]
    return sympy.Matrix(rows).rank() == 1 + K * (K - 1) // 2


def test_structure(trials=1500):
    cnt = dict(total=0, nexp=0, prop5_viol=0, thm6_viol=0, cor7_viol=0, cor7_applies=0, indep=0,
               full_vs_span=0, converse5_fails=0)
    for it in range(trials):
        K = rng.choice([4, 5, 5, 6, 6, 7])
        m = rng.randint(max(3, K - 2), 12)
        alltypes = [(1,) + t for t in itertools.product([1, -1], repeat=K - 1)]
        if m > len(alltypes):
            m = len(alltypes)
        # biased generators so that non-exposed sets are common
        mode = rng.random()
        if mode < 0.5:
            ts = rng.sample(alltypes, m)
        else:
            Q = rng.sample(range(K), 4)
            pool = [t for t in alltypes if t[Q[0]] * t[Q[1]] * t[Q[2]] * t[Q[3]] == 1]
            ts = rng.sample(pool, min(m, len(pool)))
        V = states_from_types(ts)
        if not distinct_states(V):
            continue
        cnt["total"] += 1
        full = decide(V)
        span = decide_span(V)
        if full.exposed != span.exposed:
            cnt["full_vs_span"] += 1
        Y, _ = sign_vectors_in_span(V)
        Yset = set(Y)
        extra = Yset - set(canon(x) for x in V)
        if not full.exposed:
            cnt["nexp"] += 1
            if not extra or any(y not in Yset for y in full.mu):
                cnt["prop5_viol"] += 1
        else:
            if extra:
                cnt["converse5_fails"] += 1
        indep = rank_exact([list(x) for x in V]) == K
        if indep:
            cnt["indep"] += 1
            diag, nC = theorem6_diag(V)
            if diag == full.exposed:
                cnt["thm6_viol"] += 1
                print("   THEOREM 6 VIOLATION", [S(x) for x in V])
        if cor7_condition(ts):
            cnt["cor7_applies"] += 1
            if not full.exposed:
                cnt["cor7_viol"] += 1
    print("[2] random instances K=4..7, m<=12:", cnt)


# ------------------------------------------------------------------ 3. Lemma 8 and its Householder generalisation
def test_lemma8(trials=600):
    viol = 0
    n_not_all_in_V = 0
    n_all_in_V = 0
    n_all_in_V_exposed = 0
    for it in range(trials):
        K = rng.choice([4, 5, 6])
        m = rng.randint(3, 10)
        # four states with product 1: choose columns with even number of -1 among the first four states
        cols = []
        for i in range(m):
            while True:
                c = [rng.choice([1, -1]) for _ in range(K)]
                if c[0] * c[1] * c[2] * c[3] == 1:
                    break
            cols.append(tuple(c))
        V = states_from_types(cols)
        if not distinct_states(V):
            continue
        X = np.array(V[:4])
        Yk = [tuple(int(v) for v in (X.sum(axis=0) // 2 - X[k])) for k in range(4)]
        if any(abs(v) != 1 for y in Yk for v in y):
            viol += 1
            continue
        # identity sum P(y^k) = sum P(x^k)
        if not (Pmat(np.array(Yk)).sum(axis=0) == Pmat(X).sum(axis=0)).all():
            viol += 1
        Vc = set(canon(x) for x in V)
        allin = all(canon(y) in Vc for y in Yk)
        res = decide(V)
        if not allin:
            n_not_all_in_V += 1
            if res.exposed:
                viol += 1
                print("   LEMMA 8 VIOLATION", [S(x) for x in V])
        else:
            n_all_in_V += 1
            n_all_in_V_exposed += res.exposed
    print("[3] Lemma 8: violations %d ; cases with some y^k outside V: %d (all not exposed) ; "
          "cases with all y^k in V: %d, of which exposed %d" % (viol, n_not_all_in_V, n_all_in_V, n_all_in_V_exposed))
    # Householder generalisation (referee): K' states, every site constant or exactly balanced
    viol = 0
    cases = 0
    for it in range(300):
        Kp = rng.choice([6, 8])
        m = rng.randint(4, 9)
        cols = []
        for i in range(m):
            if rng.random() < 0.2:
                c = [1] * Kp
            else:
                c = [1] * (Kp // 2) + [-1] * (Kp // 2)
                rng.shuffle(c)
            cols.append(tuple(c))
        V = states_from_types(cols)
        if not distinct_states(V):
            continue
        X = np.array(V)
        tot = X.sum(axis=0) * 2
        Y2 = [tuple(int(v) for v in (Fraction(1, Kp) * tot - X[k])) if all((tot % Kp) == 0) else None for k in range(Kp)]
        if any(y is None or any(abs(v) != 1 for v in y) for y in Y2):
            viol += 1
            continue
        Vc = set(canon(x) for x in V)
        if all(canon(y) in Vc for y in Y2):
            continue
        cases += 1
        if decide(V).exposed:
            viol += 1
    print("    Householder generalisation (K'=6,8 balanced-or-constant columns): %d cases, violations %d" % (cases, viol))


# ------------------------------------------------------------------ 4. Lemma 9
def test_lemma9(trials=500):
    applicable = 0
    viol = 0
    closed = 0
    for it in range(trials):
        K = rng.choice([4, 5, 6])
        m = rng.randint(4, 7)
        V = rand_V(m, K)
        X = np.array(V)
        res = None
        for r in range(1, m // 2 + 1):
            for Sset in itertools.combinations(range(m), r):
                Sc = [j for j in range(m) if j not in Sset]
                # p > 0 with sum_k p_k x_i x_j = 0 for i in S, j not in S : maximise min p
                A_eq = np.array([[X[k, i] * X[k, j] for k in range(K)] + [0] for i in Sset for j in Sc] +
                                [[1] * K + [0]], dtype=float)
                b_eq = np.zeros(A_eq.shape[0]); b_eq[-1] = 1
                A_ub = np.hstack([-np.eye(K), np.ones((K, 1))])
                lp = linprog([0] * K + [-1], A_ub=A_ub, b_ub=np.zeros(K), A_eq=A_eq, b_eq=b_eq,
                             bounds=[(0, None)] * K + [(None, None)], method="highs")
                if lp.status != 0 or lp.x[-1] < 1e-7:
                    continue
                # exact p: solve the equalities exactly near the LP solution
                Aex = [[int(X[k, i] * X[k, j]) for k in range(K)] for i in Sset for j in Sc] + [[1] * K]
                p = exact_feasible_nonneg(Aex, [0] * (len(Aex) - 1) + [1])
                # need strictly positive p: take the LP's support; verify exactly by rational rounding
                pf = [Fraction(v).limit_denominator(1000) for v in lp.x[:K]]
                ok = all(v > 0 for v in pf) and all(sum(a * v for a, v in zip(row, pf)) == 0 for row in Aex[:-1])
                if not ok:
                    continue
                flip = [canon(tuple(-v if i in Sset else v for i, v in enumerate(x))) for x in V]
                Vc = set(V)
                if set(flip) == Vc:
                    closed += 1
                    continue
                applicable += 1
                if res is None:
                    res = decide(V)
                if res.exposed:
                    viol += 1
                    print("   LEMMA 9 VIOLATION", [S(x) for x in V], Sset, pf)
                # the certificate of the lemma, checked directly
                w = sum(pk for pk, f in zip(pf, flip) if f not in Vc)
                mu = {}
                for pk, f in zip(pf, flip):
                    if f not in Vc:
                        mu[f] = mu.get(f, 0) + pk / w
                alpha = [pk / w for pk in pf]
                for pk, f in zip(pf, flip):
                    if f in Vc:
                        alpha[V.index(f)] -= pk / w
                if not verify_certificate(V, mu, alpha):
                    viol += 1
                    print("   LEMMA 9 CERTIFICATE FAILS")
    print("[4] Lemma 9: (V,S,p) with decoupling and flip(V) != V: %d, violations %d ; flip-closed cases %d"
          % (applicable, viol, closed))


# ------------------------------------------------------------------ 5. Characters / Sidon / Proposition 10
def chars(r, H):
    pts = list(itertools.product([0, 1], repeat=r))
    return [tuple((-1) ** sum(a * b for a, b in zip(h, p)) for p in pts) for h in H]


def is_sidon(H):
    H = [tuple(h) for h in H]
    for q in itertools.combinations(H, 4):
        if all(sum(c) % 2 == 0 for c in zip(*q)):
            return False
    return True


def test_sidon():
    r = 3
    pts = list(itertools.product([0, 1], repeat=r))
    mism = 0
    tot = 0
    with0 = 0
    for k in range(2, 9):
        for H in itertools.combinations(pts, k):
            V = chars(r, H)
            res = decide(V)
            tot += 1
            with0 += (0, 0, 0) in H
            if res.exposed != is_sidon(H):
                mism += 1
    print("[5] characters on F_2^3: %d subsets with >=2 elements (%d contain 0), mismatches with Sidon: %d" % (tot, with0, mism))
    r = 4
    pts = list(itertools.product([0, 1], repeat=r))
    mism = 0
    tot = 0
    ns = 0
    for it in range(60):
        k = rng.randint(2, 9)
        H = rng.sample(pts, k)
        V = chars(r, H)
        res = decide(V)                 # full LP: 32768 states
        res2 = decide_span(V)
        tot += 1
        ns += is_sidon(H)
        if res.exposed != is_sidon(H) or res2.exposed != res.exposed:
            mism += 1
    print("    F_2^4: %d random subsets (sizes 2..9, %d Sidon), full LP; mismatches: %d" % (tot, ns, mism))
    r = 5
    pts = list(itertools.product([0, 1], repeat=r))
    mism = tot = ns = 0
    for it in range(200):
        k = rng.randint(2, 12)
        H = rng.sample(pts, k)
        V = chars(r, H)
        res2 = decide_span(V)
        tot += 1
        ns += is_sidon(H)
        if res2.exposed != is_sidon(H):
            mism += 1
    print("    F_2^5: %d random subsets (sizes 2..12, %d Sidon), span-reduced LP; mismatches: %d" % (tot, ns, mism))


def test_prop10(trials=300):
    """general pair-separating instances: sites F_2^r x [q], state k = (eps_kj chi_{h_k})_j ;
    claim: exposed iff the span contains no sign vector other than +-V."""
    mism = 0
    tot = 0
    nexp = 0
    for it in range(trials):
        r = rng.choice([2, 3])
        q = rng.choice([1, 2, 2, 3])
        pts = list(itertools.product([0, 1], repeat=r))
        k = rng.randint(2, len(pts))
        H = rng.sample(pts, k)
        base = chars(r, H)
        V = []
        for x in base:
            row = []
            for j in range(q):
                e = 1 if j == 0 else rng.choice([1, -1])
                row += [e * v for v in x]
            V.append(tuple(row))
        if not distinct_states(V):
            continue
        tot += 1
        Y, _ = sign_vectors_in_span(V)
        extra = set(Y) - set(canon(x) for x in V)
        if len(V[0]) <= 16:
            res = decide(V)
        else:
            res = decide_span(V)
        nexp += (not res.exposed)
        if res.exposed != (len(extra) == 0):
            mism += 1
            print("   PROP 10 VIOLATION", r, q, H)
    print("[6] Proposition 10 on twisted character instances (sites F_2^r x [q]): %d instances, %d not exposed, "
          "mismatches %d" % (tot, nexp, mism))
    # product symmetrisation (referee): V' = { x^k (x) chi_{h_k} } for arbitrary V
    mism = tot = nexp = 0
    for it in range(200):
        K = rng.choice([3, 4, 5, 6])
        m = rng.randint(2, 4)
        V = rand_V(m, K) if K <= 2 ** (m - 1) else None
        if V is None:
            continue
        r = 3
        pts = list(itertools.product([0, 1], repeat=r))
        H = rng.sample(pts, K)
        ch = chars(r, H)
        Vp = [tuple(a * b for a in x for b in c) for x, c in zip(V, ch)]
        tot += 1
        Y, _ = sign_vectors_in_span(Vp)
        extra = set(Y) - set(canon(x) for x in Vp)
        res = decide_span(Vp)
        nexp += (not res.exposed)
        if res.exposed != (len(extra) == 0):
            mism += 1
    print("    product symmetrisation x^k (x) chi_{h_k}: %d instances, %d not exposed, mismatches with 'C empty': %d"
          % (tot, nexp, mism))


if __name__ == "__main__":
    which = sys.argv[1:] or ["0", "1", "2", "3", "4", "5", "6"]
    t0 = time.time()
    if "0" in which: test_sporadic()
    if "1" in which: test_theorem2()
    if "2" in which: test_structure()
    if "3" in which: test_lemma8()
    if "4" in which: test_lemma9()
    if "5" in which: test_sidon()
    if "6" in which: test_prop10()
    print("time %.0f s" % (time.time() - t0))
