#!/usr/bin/env python3
"""
Referee's brute-force tests of Lemma A1 (3-SAT -> 3DM, <= 21m triples) and Lemma A2 (3DM -> 4-PARTITION) of
STRANDS_NN_HARDNESS.md, Appendix A.  Own code, written from the text of the appendix; does not import the
author's test_eth_chain.py.
"""
import itertools, random, sys, time
sys.setrecursionlimit(100000)


# ------------------------------------------------------------------------------------------- Lemma A1
def build_3dm(clauses):
    """clauses: list of lists of non-zero ints (literal v or -v), 1..3 literals each (repeats allowed).
    Returns (W, X, Y, T) with elements as tuples and T a list of triples (w, x, y)."""
    slots = []                         # (clause index, position in clause, variable, positive?)
    for ci, cl in enumerate(clauses):
        for pos, lit in enumerate(cl):
            slots.append((ci, pos, abs(lit), lit > 0))
    # number the slots of each variable cyclically
    byvar = {}
    for s in slots:
        byvar.setdefault(s[2], []).append(s)
    W, X, Y, T = [], [], [], []
    for s in slots:
        W += [('p', s[0], s[1]), ('n', s[0], s[1])]
        X.append(('a', s[0], s[1]))
        Y.append(('b', s[0], s[1]))
    for ci, cl in enumerate(clauses):
        X.append(('c1', ci))
        Y.append(('c2', ci))
        for r in range(len(cl) - 1):
            X.append(('g1', ci, r))
            Y.append(('g2', ci, r))
    for v, sl in byvar.items():
        d = len(sl)
        for j in range(d):
            s = sl[j]
            nxt = sl[(j + 1) % d]
            T.append((('n', s[0], s[1]), ('a', s[0], s[1]), ('b', s[0], s[1])))          # true triple
            T.append((('p', s[0], s[1]), ('a', nxt[0], nxt[1]), ('b', s[0], s[1])))      # false triple
    for ci, cl in enumerate(clauses):
        for pos, lit in enumerate(cl):
            tip = ('p', ci, pos) if lit > 0 else ('n', ci, pos)
            T.append((tip, ('c1', ci), ('c2', ci)))
        for r in range(len(cl) - 1):
            for pos in range(len(cl)):
                for kind in ('p', 'n'):
                    T.append(((kind, ci, pos), ('g1', ci, r), ('g2', ci, r)))
    return W, X, Y, T


def has_perfect_matching(W, X, Y, T, count=False):
    """exact cover of W u X u Y by triples of T (DFS on the element with fewest candidates)"""
    elems = [('W', w) for w in W] + [('X', x) for x in X] + [('Y', y) for y in Y]
    if not (len(W) == len(X) == len(Y)):
        return 0 if count else False
    trip = [(('W', t[0]), ('X', t[1]), ('Y', t[2])) for t in T]
    by = {e: [] for e in elems}
    for i, t in enumerate(trip):
        for e in t:
            by[e].append(i)
    covered = set()
    total = 0

    def rec():
        nonlocal total
        best = None
        for e in elems:
            if e in covered:
                continue
            cand = [i for i in by[e] if not any(x in covered for x in trip[i])]
            if best is None or len(cand) < len(best[1]):
                best = (e, cand)
                if not cand:
                    return False
        if best is None:
            total += 1
            return True
        for i in best[1]:
            for x in trip[i]:
                covered.add(x)
            r = rec()
            for x in trip[i]:
                covered.discard(x)
            if r and not count:
                return True
        return False

    r = rec()
    return total if count else r


def satisfiable(clauses):
    vs = sorted({abs(l) for cl in clauses for l in cl})
    n = 0
    for bits in itertools.product([False, True], repeat=len(vs)):
        val = dict(zip(vs, bits))
        if all(any(val[abs(l)] == (l > 0) for l in cl) for cl in clauses):
            n += 1
    return n


def test_A1(ntests, seed, maxm=4, maxvars=4):
    rng = random.Random(seed)
    stats = {'tests': 0, 'sat': 0, 'unsat': 0, 'maxT': 0, 'degenerate': 0}
    for it in range(ntests):
        m = rng.randint(1, maxm)
        nv = rng.randint(1, maxvars)
        clauses = []
        for _ in range(m):
            k = rng.choice([1, 2, 3, 3])
            clauses.append([rng.choice([1, -1]) * rng.randint(1, nv) for _ in range(k)])   # repeats allowed
        W, X, Y, T = build_3dm(clauses)
        L = sum(len(c) for c in clauses)
        assert len(W) == len(X) == len(Y) == 2 * L <= 6 * m, (clauses, len(W), len(X), len(Y))
        assert len(T) == 3 * L + sum(2 * len(c) * (len(c) - 1) for c in clauses) <= 21 * m
        assert len(set(T)) == len(T)
        used = set()
        for t in T:
            used.update([('W', t[0]), ('X', t[1]), ('Y', t[2])])
        assert len(used) == 3 * len(W), 'an element lies in no triple'
        s = satisfiable(clauses) > 0
        pm = has_perfect_matching(W, X, Y, T)
        assert s == pm, ('LEMMA A1 FAILS', clauses, s, pm)
        stats['tests'] += 1
        stats['sat' if s else 'unsat'] += 1
        stats['maxT'] = max(stats['maxT'], len(T))
        if any(len(set(map(abs, c))) < len(c) for c in clauses) or any(len(c) < 3 for c in clauses):
            stats['degenerate'] += 1
    return stats


# ------------------------------------------------------------------------------------------- Lemma A2
def build_4partition(q, T):
    """T: list of triples (i, j, k), 1-based indices into W, X, Y of size q; every element in >= 1 triple.
    Returns (sizes list with labels, B)."""
    r = 32 * q
    B = 40 * r ** 4 + 15
    N = {}
    for (i, j, k) in T:
        for z in (('w', i), ('x', j), ('y', k)):
            N[z] = N.get(z, 0) + 1
    items = []
    for i in range(1, q + 1):
        for l in range(1, N[('w', i)] + 1):
            items.append((('w', i, l), (10 if l == 1 else 11) * r ** 4 + i * r + 1))
    for j in range(1, q + 1):
        for l in range(1, N[('x', j)] + 1):
            items.append((('x', j, l), (10 if l == 1 else 11) * r ** 4 + j * r ** 2 + 2))
    for k in range(1, q + 1):
        for l in range(1, N[('y', k)] + 1):
            items.append((('y', k, l), (10 if l == 1 else 8) * r ** 4 + k * r ** 3 + 4))
    for (i, j, k) in T:
        items.append((('u', i, j, k), 10 * r ** 4 - k * r ** 3 - j * r ** 2 - i * r + 8))
    return items, B


def exact_packing_exists(sizes, B, nbins):
    """generic search: no assumption on the number of items per bin"""
    n = len(sizes)
    order = sorted(range(n), key=lambda i: -sizes[i])
    sz = [sizes[i] for i in order]
    used = [False] * n

    def fill(start, remaining):
        """complete the current bin with items of index >= start"""
        if remaining == 0:
            return next_bin()
        seen = set()
        for i in range(start, n):
            if not used[i] and sz[i] <= remaining and sz[i] not in seen:
                seen.add(sz[i])
                used[i] = True
                if fill(i + 1, remaining - sz[i]):
                    used[i] = False
                    return True
                used[i] = False
        return False

    def next_bin():
        for i in range(n):
            if not used[i]:
                used[i] = True
                r = fill(i + 1, B - sz[i])
                used[i] = False
                return r
        return True

    return next_bin()


def pm_3dm_index(q, T):
    W = list(range(1, q + 1))
    return has_perfect_matching([('w', i) for i in W], [('x', i) for i in W], [('y', i) for i in W],
                                [(('w', i), ('x', j), ('y', k)) for (i, j, k) in T])


def test_A2(ntests, seed, maxq=3, maxT=7):
    rng = random.Random(seed)
    stats = {'tests': 0, 'yes': 0, 'no': 0, 'max_items': 0, 'single_triple_elements': 0}
    while stats['tests'] < ntests:
        q = rng.randint(1, maxq)
        allt = [(i, j, k) for i in range(1, q + 1) for j in range(1, q + 1) for k in range(1, q + 1)]
        nt = rng.randint(q, min(maxT, len(allt)))
        if rng.random() < 0.5:
            # plant a perfect matching to get yes-instances with distractors
            pj = list(range(1, q + 1)); pk = list(range(1, q + 1)); rng.shuffle(pj); rng.shuffle(pk)
            T = {(i, pj[i - 1], pk[i - 1]) for i in range(1, q + 1)}
            while len(T) < nt:
                T.add(rng.choice(allt))
            T = sorted(T)
        else:
            T = sorted(rng.sample(allt, nt))
        cover = {('w', t[0]) for t in T} | {('x', t[1]) for t in T} | {('y', t[2]) for t in T}
        if len(cover) < 3 * q:
            continue        # the lemma assumes every element lies in a triple
        items, B = build_4partition(q, T)
        sizes = [s for _, s in items]
        assert len(items) == 4 * len(T)
        assert sum(sizes) == len(T) * B
        assert all(5 * s > B and 3 * s < B for s in sizes), 'size not strictly between B/5 and B/3'
        pm = pm_3dm_index(q, T)
        ep = exact_packing_exists(sizes, B, len(T))
        assert pm == ep, ('LEMMA A2 FAILS', q, T, pm, ep)
        stats['tests'] += 1
        stats['yes' if pm else 'no'] += 1
        stats['max_items'] = max(stats['max_items'], len(items))
        cnt = {}
        for t in T:
            for z in (('w', t[0]), ('x', t[1]), ('y', t[2])):
                cnt[z] = cnt.get(z, 0) + 1
        if any(v == 1 for v in cnt.values()):
            stats['single_triple_elements'] += 1
    return stats


def test_chain(clause_sets):
    """A1 followed by A2 on tiny formulas: satisfiable iff exact packing exists"""
    res = []
    for clauses in clause_sets:
        W, X, Y, T = build_3dm(clauses)
        q = len(W)
        wi = {w: i + 1 for i, w in enumerate(W)}
        xi = {x: i + 1 for i, x in enumerate(X)}
        yi = {y: i + 1 for i, y in enumerate(Y)}
        Ti = [(wi[t[0]], xi[t[1]], yi[t[2]]) for t in T]
        items, B = build_4partition(q, Ti)
        sizes = [s for _, s in items]
        assert all(5 * s > B and 3 * s < B for s in sizes) and sum(sizes) == len(Ti) * B
        t0 = time.time()
        ep = exact_packing_exists(sizes, B, len(Ti))
        s = satisfiable(clauses) > 0
        res.append((clauses, len(Ti), len(items), s, ep, time.time() - t0))
        assert s == ep, ('CHAIN FAILS', clauses)
    return res


if __name__ == '__main__':
    t0 = time.time()
    # exhaustive small formulas for A1: all formulas with <= 2 clauses over 2 variables, clause sizes 1..3 (with repeats)
    lits = [1, -1, 2, -2]
    cls = [list(c) for k in (1, 2, 3) for c in itertools.product(lits, repeat=k)]
    n = 0
    for c1 in cls:
        for c2 in [None] + cls:
            clauses = [c1] if c2 is None else [c1, c2]
            W, X, Y, T = build_3dm(clauses)
            assert (satisfiable(clauses) > 0) == has_perfect_matching(W, X, Y, T), ('LEMMA A1 FAILS', clauses)
            n += 1
    print('Lemma A1: exhaustive over all', n, 'formulas with 1-2 clauses (1-3 literals, repeats allowed) on 2 variables: OK [%.0fs]' % (time.time() - t0), flush=True)
    for seed in (1, 2, 3):
        st = test_A1(700, seed)
        print('Lemma A1 random, seed', seed, st, '[%.0fs]' % (time.time() - t0), flush=True)
    st = test_A1(150, 9, maxm=6, maxvars=5)
    print('Lemma A1 random larger (m <= 6, 5 variables)', st, '[%.0fs]' % (time.time() - t0), flush=True)
    for seed in (1, 2):
        st = test_A2(400, seed)
        print('Lemma A2 random, seed', seed, st, '[%.0fs]' % (time.time() - t0), flush=True)
    st = test_A2(60, 5, maxq=4, maxT=9)
    print('Lemma A2 random larger (q <= 4, |T| <= 9)', st, '[%.0fs]' % (time.time() - t0), flush=True)
    res = test_chain([[[1]], [[-1]], [[1, 1]], [[1, -1]], [[1, 2]], [[1], [-1]], [[1], [1]], [[1], [2]], [[-1], [1, 1]]])
    for r in res:
        print('chain A1 o A2:', r[0], 'triples', r[1], 'items', r[2], 'satisfiable', r[3], 'exact packing', r[4], '[%.1fs]' % r[5])
    print('ALL OK')
