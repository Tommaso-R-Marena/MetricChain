"""R7 OWN numerical checks of the reduction of ENG-RES-0008 section 5 (tail functions of u-Lipschitz landscapes on the
cube are exactly those with m(t e^-u) >= d(m(t)), d(k) = size of the closed neighbourhood of the initial segment of size k
of the simplicial order), written from the statement, not from engineering code.

  (T0) Harper's theorem itself, brute force over ALL subsets of Q_m, m <= 4: min |N(S)| over |S| = k equals |N(I_k)|,
       and N(I_k) is again an initial segment.
  (T1) claim (a): random real-valued u-Lipschitz g on Q_m, m <= 10: the inequality at every threshold.
  (T2) claim (b): random admissible tail functions -> W(x) = sup{t : x in I_{m(t)}} is u-Lipschitz and has tail function m.
  (T3) exhaustive converse on Q_3 (and Q_4 by depth-first enumeration): the set of level-size sequences
       (|{h<=0}|, |{h<=1}|, ...) of integer-valued 1-Lipschitz h with min h = 0 EQUALS the set of nondecreasing integer
       sequences with k_{j+1} >= d(k_j).
"""
import itertools, math, sys
import numpy as np
from own_harper import simplicial_order, popcount

def nbr_table(m):
    return np.array([[x ^ (1 << i) for i in range(m)] for x in range(1 << m)])

def closed_nbhd_size_initial(m):
    """d[k] = |N(I_k)| for k = 0..2^m, and a flag that N(I_k) is the initial segment of that size."""
    order = simplicial_order(m)
    pos = np.empty(1 << m, dtype=np.int64); pos[order] = np.arange(1 << m)
    nb = nbr_table(m)
    d = [0]; is_init = True
    inN = np.zeros(1 << m, dtype=bool)
    for k in range(1, (1 << m) + 1):
        x = order[k - 1]
        inN[x] = True; inN[nb[x]] = True
        size = int(inN.sum())
        d.append(size)
        if int(pos[inN].max()) != size - 1:
            is_init = False
    return np.array(d), is_init, order, pos, nb

def T0(m):
    N = 1 << m
    d, is_init, order, pos, nb = closed_nbhd_size_initial(m)
    lo_masks = [sum(1 << p for p in range(N) if not (p >> i) & 1) for i in range(m)]
    full = (1 << N) - 1
    best = [N + 1] * (N + 1)
    for A in range(1, full + 1):
        out = A
        for i in range(m):
            sh = 1 << i
            out |= ((A & lo_masks[i]) << sh) | ((A & ~lo_masks[i] & full) >> sh)
        k = popcount(A); s = popcount(out)
        if s < best[k]:
            best[k] = s
    ok = all(best[k] == d[k] for k in range(1, N + 1))
    return ok, is_init

def lipschitz_random(m, u, rng, kind):
    """Random INTEGER-valued function on Q_m that is u-Lipschitz (u a positive integer = number of grid units per unit
    slope), so that every comparison below is exact.  Real-valued landscapes are approximated by a fine grid (u = 1000)."""
    N = 1 << m
    nb = nbr_table(m)
    if kind == 0:      # largest u-Lipschitz minorant of random data
        g = rng.integers(0, u * m + 1, size=N)
    elif kind == 1:    # sparse deep dips
        g = np.full(N, u * m, dtype=np.int64); idx = rng.choice(N, size=max(1, N // 16), replace=False)
        g[idx] = rng.integers(0, u * m + 1, size=len(idx))
    else:              # multiples of u (many ties between levels)
        g = u * rng.integers(0, m + 1, size=N)
    g = g.astype(np.int64)
    for _ in range(m + 1):                       # g <- min(g, min over neighbours g + u)
        g = np.minimum(g, (g[nb] + u).min(axis=1))
    assert np.abs(g[:, None] - g[nb]).max() <= u
    return g

def T1(m, u, trials, rng):
    """claim (a): for every real c, #{g < c + u} >= d(#{g < c}).  Integer g: enough to test integer c at and next to atoms."""
    d, is_init, order, pos, nb = closed_nbhd_size_initial(m)
    worst = None
    for t in range(trials):
        g = lipschitz_random(m, u, rng, t % 3)
        gs = np.sort(g)
        cs = np.unique(np.concatenate([gs, gs + 1, gs - u, gs - u + 1]))
        k = np.searchsorted(gs, cs, side="left")          # #{g < c}
        k2 = np.searchsorted(gs, cs + u, side="left")     # #{g < c + u}
        w = int((k2 - d[k]).min())
        worst = w if worst is None else min(worst, w)
    return worst      # must be >= 0

def T2(m, q, trials, rng):
    """claim (b): random admissible tail functions on a grid of q levels per unit slope (u = q grid units):
    sizes[i] = #{g <= i}, admissible iff nondecreasing and sizes[i+q] >= d(sizes[i]).  The landscape with initial-segment
    level sets, g(x) = min{i : pos(x) < sizes[i]}, must be q-Lipschitz."""
    d, is_init, order, pos, nb = closed_nbhd_size_initial(m)
    N = 1 << m
    bad = made = 0
    for t in range(trials):
        sizes = [int(rng.integers(1, 3))]
        while sizes[-1] < N and len(sizes) < 60 * m * q:
            i = len(sizes)
            lower = sizes[-1] if i < q else max(sizes[-1], int(d[sizes[i - q]]))
            sizes.append(int(min(N, lower + rng.integers(0, 3) * rng.integers(0, 1 + N // 8))))
        if sizes[-1] < N:
            continue
        made += 1
        g = np.empty(N, dtype=np.int64)
        g[order] = np.searchsorted(np.array(sizes), np.arange(N), side="right")
        if np.abs(g[:, None] - g[nb]).max() > q:
            bad += 1
        # and its tail function is the prescribed one
        assert all(int((g <= i).sum()) == sizes[i] for i in range(len(sizes)))
    return bad, made

def T3(m):
    d, is_init, order, pos, nb = closed_nbhd_size_initial(m)
    N = 1 << m
    achieved = set()
    h = [-1] * N
    count = 0
    def rec(x):
        nonlocal count
        if x == N:
            if min(h) != 0: return
            count += 1
            achieved.add(tuple(sum(1 for v in h if v <= k) for k in range(m)))
            return
        lo, hi = 0, m
        for i in range(m):
            y = x ^ (1 << i)
            if y < x:
                lo = max(lo, h[y] - 1); hi = min(hi, h[y] + 1)
        for v in range(lo, hi + 1):
            h[x] = v
            rec(x + 1)
        h[x] = -1
    rec(0)
    admissible = set()
    def gen(seq):
        if len(seq) == m:
            if d[seq[-1]] <= N: admissible.add(tuple(seq))     # last level {h <= m} is everything
            return
        lo = max(seq[-1], int(d[seq[-1]])) if seq else 1
        for k in range(lo, N + 1):
            gen(seq + [k])
    gen([])
    # {h <= m-1} must have closed neighbourhood = everything is NOT required; but |{h<=m}| = N requires d(k_{m-1}) <= N: always.
    return count, len(achieved), len(admissible), achieved == admissible, sorted(admissible - achieved)[:5], sorted(achieved - admissible)[:5]

if __name__ == "__main__":
    rng = np.random.default_rng(7)
    for m in (2, 3, 4):
        print("T0 Harper brute force, m =", m, "-> (min |N(S)| = |N(I_k)| for all k, N(I_k) initial segment):", T0(m), flush=True)
    for m in range(5, 13):
        print("    nestedness of neighbourhoods of initial segments, m =", m, ":", closed_nbhd_size_initial(m)[1])
    for m, trials in ((3, 3000), (4, 3000), (6, 1500), (8, 600), (10, 150)):
        for u in (1, 7, 1000):
            print(f"T1 claim (a): m={m} grid units per slope u={u} trials={trials}: min over thresholds of m(t e^-u) - d(m(t)) = {T1(m, u, trials, rng)}", flush=True)
    for m, trials in ((3, 3000), (4, 3000), (6, 2000), (8, 1000), (10, 300)):
        for q in (1, 2, 5):
            print(f"T2 claim (b): m={m} q={q} trials={trials}: (constructed landscapes that are NOT u-Lipschitz, landscapes made) = {T2(m, q, trials, rng)}", flush=True)
    for m in (2, 3, 4):
        print(f"T3 exhaustive converse, m={m}: (#functions, #achieved sequences, #admissible sequences, equal, examples) =", T3(m), flush=True)
