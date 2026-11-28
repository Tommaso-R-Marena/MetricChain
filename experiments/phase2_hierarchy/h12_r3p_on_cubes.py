"""
Phase II (adaptive hierarchy) -- Algorithm R3P of the addendum (section A4), run literally on real cubes.

The energy is a table on all 2^n points; it is a function of the numbers of ones in the classes of a hidden
partition.  The algorithm sees it only through evaluations and is told n and m only.
Tests:  (a) the partitions it chooses: no pair separated so far inside a cell, at most m (resp. m^2) cells, G2 refines G1;
            coordinates of one hidden class are never separated;
        (b) unbiasedness: the mean of the estimate over repeated runs equals A within sampling error;
        (c) exactness: whenever the energy is constant on every shell of G2 the estimate equals A up to rounding
            (and how often that happens);
        (d) mutation "uniform shell weights" -> biased (must be caught);
        (e) mutation "learn nothing" (one cell throughout) -> still unbiased.
Profiles: minima of cones in the class counts (hidden centres of blocks, overlapping centres), a profile
that couples two classes through their sum, a 2-periodic profile.
These sizes test the logic of the algorithm, not its exponent.
"""
import sys, itertools, math
import numpy as np

def make_instance(rng, sizes, u, kind):
    n = sum(sizes); m = len(sizes)
    perm = rng.permutation(n)
    cls = np.empty(n, int); start = 0
    for j, nj in enumerate(sizes):
        cls[perm[start:start + nj]] = j; start += nj
    grids = np.meshgrid(*[np.arange(nj + 1) for nj in sizes], indexing='ij')
    if kind == 'cones':                     # minimum of cones in the class counts
        F = np.zeros(grids[0].shape)
        for _ in range(4):
            c = [rng.integers(0, nj + 1) for nj in sizes]; w = rng.random(m) < 0.8
            F = np.minimum(F, u * sum(np.abs(g - ci) * wi for g, ci, wi in zip(grids, c, w)) - rng.uniform(0, 0.5) * u * n)
    elif kind == 'coupled':                 # depends on k_0 + k_1 near the typical counts, on k_0 alone when k_0 is small
        s = grids[0] + grids[1]
        F = 0.5 * u * np.abs(s - (sizes[0] + sizes[1]) // 3) - 0.5 * u * np.maximum(2 - grids[0], 0)
        if m > 2: F = F + 0.5 * u * np.abs(grids[2] - 1)
    elif kind == 'periodic':                # 2-periodic in class 0, a cone in the others
        F = 0.5 * u * (grids[0] % 2) + u * sum(grids[1:])
    else:
        raise ValueError(kind)
    X = ((np.arange(2 ** n)[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int8)
    counts = [X[:, cls == j].sum(axis=1) for j in range(m)]
    psi = F[tuple(counts)]
    edge = max(np.abs(psi - psi[np.arange(2 ** n) ^ (1 << i)]).max() for i in range(n))
    assert edge <= u + 1e-9, edge
    return dict(n=n, m=m, cls=cls, psi=psi, A=float(np.mean(np.exp(-psi))), X=X)

def idx(x): return int(np.dot(x, 1 << np.arange(len(x))))

def separate(inst, x, sep, q):
    """evaluate all neighbours of x; record the separated pairs (same bit, different value)"""
    n = inst['n']; vals = np.array([inst['psi'][idx(x) ^ (1 << i)] for i in range(n)]); q[0] += n
    for b in (0, 1):
        I = np.flatnonzero(x == b)
        if len(I) > 1:
            d = np.abs(vals[I][:, None] - vals[I][None, :]) > 1e-12
            sep[np.ix_(I, I)] |= d

def clique_partition(sep, base, max_cells):
    """a partition refining `base` (list of index arrays) into at most max_cells cells without separated pairs;
    greedy first, exhaustive backtracking if greedy needs too many cells"""
    def greedy(order_cells):
        cells = []
        for g in order_cells:
            mine = []
            for i in g:
                for c in mine:
                    if not sep[i, c].any(): c.append(i); break
                else: mine.append([i])
            cells += mine
        return cells
    cells = greedy(base)
    if len(cells) <= max_cells: return [np.array(c) for c in cells]
    sites = [i for g in base for i in g]; owner = {i: gi for gi, g in enumerate(base) for i in g}
    best = [None]
    def rec(t, cells):
        if best[0] is not None: return
        if t == len(sites): best[0] = [list(c) for c in cells]; return
        i = sites[t]
        for c in cells:
            if owner[c[0]] == owner[i] and not sep[i, c].any():
                c.append(i); rec(t + 1, cells); c.pop()
                if best[0] is not None: return
        if len(cells) < max_cells:
            cells.append([i]); rec(t + 1, cells); cells.pop()
    rec(0, [])
    assert best[0] is not None, "no admissible partition (input not in the class?)"
    return [np.array(c) for c in best[0]]

def sample_shell(rng, n, cells, a):
    x = np.zeros(n, np.int8)
    for g, ag in zip(cells, a):
        x[rng.choice(g, size=ag, replace=False)] = 1
    return x

def R3P(inst, M, rng, mutate=None):
    n, m = inst['n'], inst['m']; q = [0]
    sep = np.zeros((n, n), bool)
    for _ in range(M):                                              # round 1
        x = rng.integers(0, 2, n).astype(np.int8); q[0] += 1
        if mutate != 'no_learning': separate(inst, x, sep, q)
    G1 = clique_partition(sep, [np.arange(n)], m); sep1 = sep.copy()
    for a in itertools.product(*[range(len(g) + 1) for g in G1]):   # round 2
        for _ in range(M):
            x = sample_shell(rng, n, G1, a); q[0] += 1
            if mutate != 'no_learning': separate(inst, x, sep, q)
    G2 = clique_partition(sep, G1, m * m)
    est = 0.0                                                       # round 3
    for b in itertools.product(*[range(len(g) + 1) for g in G2]):
        if mutate == 'uniform_weights': w = 1.0 / np.prod([len(g) + 1 for g in G2])
        else: w = np.prod([math.comb(len(g), bg) / 2.0 ** len(g) for g, bg in zip(G2, b)])
        tot = 0.0
        for _ in range(M):
            x = sample_shell(rng, n, G2, b); q[0] += 1; tot += math.exp(-inst['psi'][idx(x)])
        est += w * tot / M
    return est, G1, G2, sep1, sep, q[0]

def shell_constant(inst, G2):
    """is the energy constant on every shell of G2 ?"""
    key = np.zeros(2 ** inst['n'], np.int64)
    for g in G2: key = key * (len(g) + 1) + inst['X'][:, g].sum(axis=1)
    order = np.argsort(key, kind='stable'); ks = key[order]; ps = inst['psi'][order]
    starts = np.r_[0, np.flatnonzero(np.diff(ks)) + 1]
    return bool(np.all(np.maximum.reduceat(ps, starts) - np.minimum.reduceat(ps, starts) < 1e-12))

if __name__ == "__main__":
    rng = np.random.default_rng(20261128)
    u = 1.0; runs = 40
    print("Algorithm R3P on real cubes (u = %g, %d runs per line).  z = (mean estimate - A)/standard error." % (u, runs))
    bad = 0
    for kind in ('cones', 'coupled', 'periodic'):
        for sizes in ((6, 6), (4, 3, 5), (2, 5, 2, 3)):
            inst = make_instance(rng, sizes, u, kind); m = inst['m']
            for M in (2, 12):
                ests = []; ok_part = True; ncell = []; nexact = 0; exact_ok = True
                for _ in range(runs):
                    est, G1, G2, sep1, sep, q = R3P(inst, M, rng)
                    ests.append(est); ncell.append(len(G2))
                    ok_part &= len(G1) <= m and len(G2) <= m * m
                    ok_part &= all(not sep1[np.ix_(g, g)].any() for g in G1)      # G1 against the pairs separated in round 1
                    ok_part &= all(not sep[np.ix_(g, g)].any() for g in G2)       # G2 against all separated pairs
                    ok_part &= all(len(set(inst['cls'][g])) >= 1 for g in G2) and not sep[inst['cls'][:, None] == inst['cls'][None, :]].any()
                    lab1 = np.empty(inst['n'], int)
                    for gi, g in enumerate(G1): lab1[g] = gi
                    ok_part &= all(len(set(lab1[g])) == 1 for g in G2)
                    if shell_constant(inst, G2):
                        nexact += 1; exact_ok &= abs(est - inst['A']) <= 1e-9 * inst['A']
                ests = np.array(ests); se = ests.std(ddof=1) / np.sqrt(runs)
                relerr = np.abs(ests - inst['A']).max() / inst['A']
                z = 0.0 if relerr < 1e-9 else (ests.mean() - inst['A']) / se
                mut = np.array([R3P(inst, M, rng, mutate='uniform_weights')[0] for _ in range(runs)])
                zm = (mut.mean() - inst['A']) / (mut.std(ddof=1) / np.sqrt(runs) + 1e-300)
                nl = np.array([R3P(inst, M, rng, mutate='no_learning')[0] for _ in range(runs)])
                zn = (nl.mean() - inst['A']) / (nl.std(ddof=1) / np.sqrt(runs) + 1e-300)
                ok = ok_part and exact_ok and abs(z) < 3.5
                bad += (not ok)
                print("  %-8s classes %-12s M=%2d | partitions ok %s, cells of G2: %.1f | shells constant in %2d runs, exact there %s | max rel. error %.1e | z = %+5.2f | mutation uniform weights |z| = %.3g | no learning z = %+5.2f" % (
                    kind, sizes, M, ok_part, np.mean(ncell), nexact, exact_ok, relerr, z, abs(zm), zn))
                sys.stdout.flush()
    print("failures of (a), (b), (c):", bad)
