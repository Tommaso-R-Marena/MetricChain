"""A computable localisation criterion for a product reference tilted by non-negative tables
(docs/complexity/PENALTY_THRESHOLD.md; question of THY-MSG-0017 section 5 item 3 / SCI-RES-0027 Q-CX3).

Model.  Sites 0..n-1, states 0 (anchor), 1..q-1 (off).  Product reference P0 with off-probabilities p[i][s];
tables gamma_U(x_U) >= 0, zero unless every site of U is off;  G(x) = sum_U gamma_U(x_U);
gain(lam) = ln < exp(lam * G) >_0.

Quantities.
  lam0 = min over site sets S of  h(S) / gmax(S),   h_i = ln(1/q_i),  q_i = P0(site i off),
         gmax(S) = sum of the table maxima over tables inside S           (max-flow / project selection)
  lam1 = min over configurations x != anchor of  ln(1/P0(x)) / G(x)      (brute force here)
  price bound:  for prices c_i >= 0 obtained by distributing every table maximum over its sites,
         gain(lam) <= sum_i ln(1 + q_i (exp(lam c_i) - 1));
         with the optimal distribution for lam < lam0:  gain(lam) <= sum_i ln(1 + q_i^(1 - lam/lam0) - q_i)
  lower bound:  gain(lam) >= max_x [ lam G(x) + ln P0(x) ]
  Finner-type bound (THY-RES-0016 section 5 (iii)) with p_U = d = max number of tables through a site.
Everything is compared with the exact gain by enumeration of all q^n states.
"""
import itertools, math, random, sys
import networkx as nx


def make_instance(n, q, window, arities, scale, rng, qoff=(0.05, 0.3)):
    p = []
    for i in range(n):
        tot = rng.uniform(*qoff)
        w = [rng.random() for _ in range(q - 1)]
        s = sum(w)
        p.append([1 - tot] + [tot * x / s for x in w])
    tables = {}
    for k in arities:
        for start in range(n):
            for U in itertools.combinations(range(start, min(n, start + window)), k):
                if U[0] != start or U in tables:
                    continue
                tables[U] = {xs: scale * rng.random() for xs in itertools.product(range(1, q), repeat=k)}
    return p, tables


def exact_gain(p, tables, q, lams):
    n = len(p)
    out = [0.0] * len(lams)
    best = [(-1e300, None)] * len(lams)
    ratios = []
    for x in itertools.product(range(q), repeat=n):
        P = 1.0
        for i in range(n):
            P *= p[i][x[i]]
        G = 0.0
        for U, tab in tables.items():
            xs = tuple(x[i] for i in U)
            if all(v > 0 for v in xs):
                G += tab[xs]
        if G > 0:
            ratios.append((-math.log(P) / G, x))
        for a, lam in enumerate(lams):
            out[a] += P * math.exp(lam * G)
            v = lam * G + math.log(P)
            if any(x) and v > best[a][0]:
                best[a] = (v, x)
    lam1, xstar = min(ratios)
    return [math.log(v) for v in out], [b[0] for b in best], lam1, xstar


def max_profit(lam, h, gmax):
    """max over site sets S of lam*gmax(S) - h(S), by project selection (max-flow); also the fractional loads."""
    G = nx.DiGraph()
    tot = 0.0
    for U, g in gmax.items():
        G.add_edge("s", ("t", U), capacity=lam * g)
        tot += lam * g
        for i in U:
            G.add_edge(("t", U), ("v", i))          # infinite capacity
    for i, hi in enumerate(h):
        G.add_edge(("v", i), "t", capacity=hi)
    flow, fd = nx.maximum_flow(G, "s", "t")
    return tot - flow, fd


def lam0_by_flow(h, gmax, iters=60):
    lo, hi = 0.0, sum(h) / min(g for g in gmax.values() if g > 0) + 1.0
    for _ in range(iters):                         # bisection on "max profit = 0"
        mid = (lo + hi) / 2
        if max_profit(mid, h, gmax)[0] > 1e-12:
            hi = mid
        else:
            lo = mid
    return lo


def lam0_bruteforce(h, gmax):
    n = len(h)
    best = float("inf")
    for r in range(1, n + 1):
        for S in itertools.combinations(range(n), r):
            Sset = set(S)
            g = sum(v for U, v in gmax.items() if set(U) <= Sset)
            if g > 0:
                best = min(best, sum(h[i] for i in S) / g)
    return best


def prices_at(lam, h, gmax):
    """site prices c_i (a distribution of the table maxima over their sites) with lam*c_i <= h_i if lam <= lam0."""
    profit, fd = max_profit(lam, h, gmax)
    c = [0.0] * len(h)
    for U, g in gmax.items():
        sent = 0.0
        for i in U:
            f = fd[("t", U)].get(("v", i), 0.0)
            c[i] += f / lam
            sent += f / lam
        if g - sent > 1e-12:                        # not routed (only if lam > lam0): put the rest on the first site
            c[U[0]] += g - sent
    return c


def connected_sets(n, tables):
    """all site sets that are connected in the graph 'two sites are adjacent if some table contains both' and
    contain at least one table."""
    adj = {i: set() for i in range(n)}
    for U in tables:
        for i in U:
            adj[i] |= set(U) - {i}
    out = []
    for r in range(1, n + 1):
        for T in itertools.combinations(range(n), r):
            Tset = set(T)
            if not any(set(U) <= Tset for U in tables):
                continue
            seen = {T[0]}
            stack = [T[0]]
            while stack:
                v = stack.pop()
                for w in adj[v] & Tset:
                    if w not in seen:
                        seen.add(w); stack.append(w)
            if len(seen) == len(T):
                out.append(T)
    return out


def cluster_bound(lam, p, tables, q, csets, binary=False, gmax=None):
    """sum over connected site sets T of  E_0[ (exp(lam * G_T) - 1) ; all sites of T off ],
    G_T = the tables inside T.  binary=True: tables replaced by their maxima, P0 by the off-probabilities."""
    tot = 0.0
    for T in csets:
        Tset = set(T)
        inside = [U for U in tables if set(U) <= Tset]
        if binary:
            g = sum(gmax[U] for U in inside)
            tot += math.prod(1 - p[i][0] for i in T) * (math.exp(lam * g) - 1)
        else:
            pos = {i: k for k, i in enumerate(T)}
            for xs in itertools.product(range(1, q), repeat=len(T)):
                P = math.prod(p[i][v] for i, v in zip(T, xs))
                g = sum(tables[U][tuple(xs[pos[i]] for i in U)] for U in inside)
                tot += P * (math.exp(lam * g) - 1)
    return tot


def table_polymer_setup(p, tables, q):
    import numpy as np
    n = len(p)
    X = list(itertools.product(range(q), repeat=n))
    P0 = np.array([math.prod(p[i][x[i]] for i in range(n)) for x in X])
    keys = list(tables)
    gam = np.zeros((len(keys), len(X)))
    for a, U in enumerate(keys):
        tab = tables[U]
        for b, x in enumerate(X):
            xs = tuple(x[i] for i in U)
            if all(v > 0 for v in xs):
                gam[a, b] = tab[xs]
    adj = [0] * len(keys)
    for a, U in enumerate(keys):
        for b, W in enumerate(keys):
            if a != b and set(U) & set(W):
                adj[a] |= 1 << b
    # all connected sets of tables, as bitmasks (a set is connected if it grows from its lowest table)
    conn = []
    for mask in range(1, 1 << len(keys)):
        low = mask & -mask
        seen = low
        frontier = low
        while frontier:
            b = frontier.bit_length() - 1
            frontier &= ~(1 << b)
            new = adj[b] & mask & ~seen
            seen |= new
            frontier |= new
        if seen == mask:
            conn.append(mask)
    return P0, gam, conn


def table_polymer_bound(lam, setup):
    """sum over connected sets Gamma of tables of  E_0[ prod_{U in Gamma} (exp(lam * gamma_U) - 1) ]."""
    import numpy as np
    P0, gam, conn = setup
    F = np.expm1(lam * gam)
    tot = 0.0
    for mask in conn:
        v = P0.copy()
        m = mask
        while m:
            b = m.bit_length() - 1
            m &= ~(1 << b)
            v = v * F[b]
        tot += float(v.sum())
    return tot


def finner(lam, p, tables, q):
    n = len(p)
    d = max(sum(1 for U in tables if i in U) for i in range(n))
    tot = 0.0
    for U, tab in tables.items():
        e = 0.0
        for xs in itertools.product(range(q), repeat=len(U)):
            P = 1.0
            for i, v in zip(U, xs):
                P *= p[i][v]
            g = tab[xs] if all(v > 0 for v in xs) else 0.0
            e += P * math.exp(d * lam * g)
        tot += math.log(e) / d
    return tot


if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
    worst = 0.0
    for case in range(6):
        n, q = [8, 8, 6, 8, 8, 8][case], 3
        scale = [0.5, 1.0, 2.0, 1.0, 1.0, 1.0][case]
        arities = [(3,), (3,), (2, 3), (2,), (3,), (2,)][case]
        qoff = (0.05, 0.3) if case < 4 else (0.002, 0.01)          # cases 4, 5: low temperature
        p, tables = make_instance(n, q, 3, arities, scale, rng, qoff=qoff)
        qi = [1 - p[i][0] for i in range(n)]
        h = [math.log(1 / x) for x in qi]
        gmax = {U: max(tab.values()) for U, tab in tables.items()}
        l0 = lam0_by_flow(h, gmax)
        l0b = lam0_bruteforce(h, gmax)
        assert abs(l0 - l0b) < 1e-6 * l0b, (l0, l0b)
        lams = [f * l0 for f in (0.1, 0.25, 0.5, 0.75, 0.9, 1.0, 1.25, 1.5, 2.0, 3.0)]
        gain, low, l1, xstar = exact_gain(p, tables, q, lams)
        first = sum(sum(tab[xs] * math.prod(p[i][v] for i, v in zip(U, xs)) for xs in tab) for U, tab in tables.items())
        print(f"case {case}: n={n} q={q} tables of sizes {arities}, scale {scale}: {len(tables)} tables; "
              f"lam0 (max-flow) = {l0:.4f} = brute force; lam1 = {l1:.4f}; extremal state {xstar}")
        csets = connected_sets(n, tables)
        adjdeg = max(len(set().union(*[set(U) for U in tables if i in U]) - {i}) for i in range(n))
        qmax = max(qi)
        kmin = min(len(U) for U in tables)
        crit = 1 - math.log(math.e * adjdeg) / math.log(1 / qmax)
        print(f"    {len(csets)} connected site sets containing a table; max degree of the site graph {adjdeg}; q_max = {qmax:.3f}; "
              f"explicit criterion applies for lam/lam0 < {crit:.3f}")

        def explicit(lam):
            eps = math.e * adjdeg * qmax ** (1 - lam / l0)
            return n * eps ** kmin / (math.e * adjdeg * kmin * (1 - eps)) if eps < 1 else float("inf")
        setup = table_polymer_setup(p, tables, q)
        print(f"    {len(setup[2])} connected sets of tables")
        print("    lam/lam0   exact gain   first order   ln(1+W)   W=table polymers   site clusters   clusters(binary)   explicit   price bound   Finner(d)   max-term lower bound")
        c0 = prices_at(l0 * (1 - 1e-9), h, gmax)       # prices routed at the threshold: lam0 * c0_i <= h_i
        assert all(l0 * c0[i] <= h[i] * (1 + 1e-6) for i in range(n))
        assert abs(sum(c0) - sum(gmax.values())) < 1e-6 * sum(gmax.values())      # every table maximum is distributed
        for lam, g, lw in zip(lams, gain, low):
            pb = sum(math.log(1 + qi[i] * (math.exp(lam * c0[i]) - 1)) for i in range(n))
            cf = sum(math.log(1 + qi[i] ** (1 - lam / l0) - qi[i]) for i in range(n)) if lam < l0 else float("nan")
            try:
                fb = finner(lam, p, tables, q)
            except OverflowError:
                fb = float("inf")
            assert g <= pb + 1e-9, (g, pb)
            assert g >= max(0.0, lw) - 1e-9
            if lam < l0:
                assert pb <= cf + 1e-9, (pb, cf)
            cb = cluster_bound(lam, p, tables, q, csets)
            cbb = cluster_bound(lam, p, tables, q, csets, binary=True, gmax=gmax)
            tp = table_polymer_bound(lam, setup)
            assert g <= tp * (1 + 1e-9) + 1e-12 and tp <= cb * (1 + 1e-9) and cb <= cbb * (1 + 1e-9), (g, tp, cb, cbb)
            ex = explicit(lam)
            assert g >= math.log1p(tp) - 1e-9 and g >= lam * first - 1e-12
            assert cbb <= ex * (1 + 1e-9) or ex == float("inf"), (cbb, ex)
            print(f"    {lam/l0:7.2f}   {g:10.4g}   {lam*first:10.4g}   {math.log1p(tp):8.4g}   {tp:14.4g}   {cb:13.4g}   {cbb:16.4g}   {ex:8.3g}   {pb:11.4g}   {fb:10.4g}   {max(0.0, lw):10.4g}")
    print("all inequalities hold")
