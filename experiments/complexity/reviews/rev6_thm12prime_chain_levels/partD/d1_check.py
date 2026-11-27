# d1_check.py -- REVIEW 6, referee's own toy check of PENALTY_THRESHOLD.md (Theorems 1, 2, Propositions 3, 4).
# Own code: random instances with n = 6 sites, 3 states (anchor 0, off 1, 2), product reference, non-negative tables
# that vanish unless all their sites are off; everything by exhaustive enumeration.
#   T1:  max(lam <G>, ln(1+W)) <= gain <= W
#   T2:  LEFT   = sum_{Gamma connected, |supp| > s} w(Gamma)
#        MID*   = sum_{S connected, |S| >= s'} q(S) exp(lam gmax(S))        s' = max(s+1, k_min)
#        MIDlit = sum_{S connected, |S| > s}   q(S) exp(lam gmax(S))        (the middle term as printed in the note)
#        RIGHT  = n eps^{s'} / (e Delta s' (1 - eps)),  eps = e Delta q_max^{1 - lam/lam0} < 1
#        checked: LEFT <= MID* <= RIGHT;  reported: whether MIDlit <= RIGHT (it need not be when s + 1 < k_min)
#   P3:  lam0 by brute force over site sets = largest lam with max_S (lam gmax(S) - h(S)) = 0  (bisection on brute force)
#   P4:  gain >= lam G(x) + ln P0(x) for all x;  lam0 <= lam1;  gain >= (lam/lam1 - 1) ln(1/P0(x*))
import itertools, math, random

def run(seed, arity, qrange):
    rng = random.Random(seed)
    n, q = 6, 3
    p = []
    for i in range(n):
        tot = rng.uniform(*qrange)
        a = rng.random()
        p.append([1 - tot, tot * a, tot * (1 - a)])
    tables = {}
    for start in range(n):
        for U in itertools.combinations(range(start, min(n, start + 3)), arity):
            if U[0] == start and U not in tables:
                tables[U] = {xs: rng.random() for xs in itertools.product((1, 2), repeat=arity)}
    keys = list(tables)
    X = list(itertools.product(range(q), repeat=n))
    P0 = [math.prod(p[i][x[i]] for i in range(n)) for x in X]
    def gam(U, x):
        xs = tuple(x[i] for i in U)
        return tables[U][xs] if all(v > 0 for v in xs) else 0.0
    Gx = [sum(gam(U, x) for U in keys) for x in X]
    qi = [1 - p[i][0] for i in range(n)]
    h = [math.log(1 / v) for v in qi]
    gmax = {U: max(tables[U].values()) for U in keys}
    def gmaxS(S):
        return sum(g for U, g in gmax.items() if set(U) <= S)
    subsets = [set(S) for r in range(1, n + 1) for S in itertools.combinations(range(n), r)]
    lam0 = min(sum(h[i] for i in S) / gmaxS(S) for S in subsets if gmaxS(S) > 0)
    # P3: bisection on the brute-force maximum
    lo, hi = 0.0, 10 * lam0
    for _ in range(60):
        mid = (lo + hi) / 2
        if max(mid * gmaxS(S) - sum(h[i] for i in S) for S in subsets) > 1e-12:
            hi = mid
        else:
            lo = mid
    assert abs(lo - lam0) < 1e-9 * lam0
    lam1, xstar = min((-math.log(P0[a]) / Gx[a], a) for a in range(len(X)) if Gx[a] > 0)
    assert lam0 <= lam1 + 1e-12
    # connected sets of tables
    adjT = {a: {b for b in range(len(keys)) if b != a and set(keys[a]) & set(keys[b])} for a in range(len(keys))}
    def connected(idx, adj):
        idx = set(idx)
        seen = {next(iter(idx))}
        st = list(seen)
        while st:
            v = st.pop()
            for w in adj[v] & idx:
                if w not in seen:
                    seen.add(w); st.append(w)
        return seen == idx
    conn = [c for r in range(1, len(keys) + 1) for c in itertools.combinations(range(len(keys)), r) if connected(c, adjT)]
    adjS = {i: set() for i in range(n)}
    for U in keys:
        for i in U:
            adjS[i] |= set(U) - {i}
    Delta = max(len(v) for v in adjS.values())
    connS = [S for S in subsets if connected(S, adjS)]
    # the standard count used in Theorem 2
    for k in range(1, n + 1):
        for v in range(n):
            assert sum(1 for S in connS if len(S) == k and v in S) <= (math.e * Delta) ** (k - 1) + 1e-9
    kmin = arity
    qmax = max(qi)
    first = sum(P0[a] * Gx[a] for a in range(len(X)))
    viol_lit = 0
    checked_T2 = 0
    for frac in (0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 0.9, 1.0, 1.25, 1.5):
        lam = frac * lam0
        gain = math.log(sum(P0[a] * math.exp(lam * Gx[a]) for a in range(len(X))))
        w = {}
        for c in conn:
            w[c] = sum(P0[a] * math.prod(math.expm1(lam * gam(keys[b], X[a])) for b in c) for a in range(len(X)))
        W = sum(w.values())
        assert max(lam * first, math.log1p(W)) <= gain * (1 + 1e-9) + 1e-15 and gain <= W * (1 + 1e-9) + 1e-15, (gain, W)
        assert all(gain >= lam * Gx[a] + math.log(P0[a]) - 1e-12 for a in range(len(X)))
        assert gain >= (lam / lam1 - 1) * (-math.log(P0[xstar])) - 1e-12
        if frac < 1:
            eps = math.e * Delta * qmax ** (1 - lam / lam0)
            if eps < 1:
                for s in range(0, n):
                    sp = max(s + 1, kmin)
                    left = sum(v for c, v in w.items() if len(set().union(*[set(keys[b]) for b in c])) > s)
                    midstar = sum(math.prod(qi[i] for i in S) * math.exp(lam * gmaxS(S)) for S in connS if len(S) >= sp)
                    midlit = sum(math.prod(qi[i] for i in S) * math.exp(lam * gmaxS(S)) for S in connS if len(S) > s)
                    right = n * eps ** sp / (math.e * Delta * sp * (1 - eps))
                    assert left <= midstar * (1 + 1e-9) and midstar <= right * (1 + 1e-9), (left, midstar, right)
                    checked_T2 += 1
                    if midlit > right * (1 + 1e-9):
                        viol_lit += 1
    return lam0, lam1, Delta, qmax, checked_T2, viol_lit

tot_chk = tot_viol = 0
for arity in (2, 3):
    for seed in range(8):
        lam0, lam1, Delta, qmax, chk, viol = run(100 * arity + seed, arity, (0.001, 0.004))
        tot_chk += chk; tot_viol += viol
        run(200 * arity + seed, arity, (0.05, 0.3))          # high-q regime: T1, P3, P4 only (criterion void)
print(f"Theorem 1, Propositions 3, 4 and the connected-set count: all assertions hold on 32 random instances x 10 values of lambda")
print(f"Theorem 2 (with the middle sum restricted to |S| >= s'): LEFT <= MID* <= RIGHT in all {tot_chk} applicable (instance, lambda, s) cases")
print(f"Theorem 2 as printed (middle sum over all connected S with |S| > s): MIDlit <= RIGHT fails in {tot_viol} of these cases "
      f"(all with s + 1 < k_min)")
