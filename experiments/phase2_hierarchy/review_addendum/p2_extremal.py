#!/usr/bin/env python3
"""Reviewer's independent brute-force attack on Theorem P (HIERARCHY_ADDENDUM.md, section A2).

Own code; nothing is imported from the author's scripts.

On the lattice of types k in prod_c {0..n_c} (z_c = k_c/n_c, phi_c = n_c/n, psi = n F) we compute the
POINTWISE LARGEST U = -n F such that
   (L)   |U(k) - U(k')| <= u for lattice neighbours,
   (N)   U <= R := n r on the lattice points of the core K = [kappa, 1-kappa]^C      (i.e. nu_K <= 0),
   (H1)  U(k) = U(k') for k, k' in K with equal cell counts of G1,
   (H2)  U(k) = U(k') for k, k' in {n cost_1 <= Theta} with equal cell counts of G2.
Every continuous F satisfying the hypotheses of Theorem P (normalised to nu_K = 0) restricts to a lattice
function with (L), (N), (H1), (H2); hence   max_{hidden y} (U*(y) - R(y)) - (n h - Theta)  =: EXCESS
is an upper bound for the violation of the theorem at lattice types.  EXCESS <= 0 proves the theorem at these
types; EXCESS = O(u) is inconclusive (lattice effect); EXCESS growing linearly in n would refute it.
U* is the greatest fixed point below R|_K of two closure operators (Lipschitz regularisation = separable
L1 inf-convolution; minimum over identified groups); it equals a shortest-path distance, which is checked
against scipy's Dijkstra on small lattices (mode `validate`).

variants:  P      Theorem P exactly as stated (core K for (N) and (H1))
           alg    the weaker statement the author tested: {R <= Theta} instead of K in (N) and (H1)
           noH1   mutation: hypothesis (H1) dropped             (positive control)
           noH2   mutation: hypothesis (H2) dropped             (positive control)
           two    two-round analogue: (N) on {cost_1 <= Theta}, (H1) on {R <= Theta}, hidden = {cost_1 > Theta}
ident:     hub    all lattice points of the region with equal cell counts are identified (what (H1),(H2) say)
           comp   only points connected by single exchanges inside the region (weaker; over-estimates more)
"""
import sys, time
import numpy as np
from multiprocessing import Pool

LN2 = float(np.log(2.0))


def f(t):
    t = np.asarray(t, dtype=float)
    a = np.where(t > 0, t, 1.0)
    b = np.where(t < 1, 1.0 - t, 1.0)
    return LN2 + t * np.log(a) + (1.0 - t) * np.log(b)


def consts(u):
    pu = 1.0 / (1.0 + np.exp(u))
    L1 = float(np.log(2.0 / (1.0 + np.exp(-u))))
    kap = L1 / u
    return pu, L1, kap, float(f(kap)), float(f(pu))


def finv(theta):
    """smaller root of f(t) = theta, 0 <= theta <= ln 2"""
    lo, hi = 0.0, 0.5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if float(f(mid)) > theta:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def lip(U, u):
    """exact inf-convolution with u*||.||_1 on the box (separable: one forward/backward pass per axis)"""
    for ax in range(U.ndim):
        n = U.shape[ax]
        shp = [1] * U.ndim
        shp[ax] = n
        ar = (u * np.arange(n, dtype=float)).reshape(shp)
        A = np.minimum.accumulate(U - ar, axis=ax)
        A += ar
        B = np.minimum.accumulate(np.flip(U + ar, axis=ax), axis=ax)
        B = np.flip(B, axis=ax) - ar
        U = np.minimum(A, B)
    return U


def groups(key, mask):
    idx = np.flatnonzero(mask.reshape(-1))
    if idx.size == 0:
        return idx, np.zeros(0, int), np.zeros(0, int)
    k = key.reshape(-1)[idx]
    o = np.argsort(k, kind='stable')
    idx = idx[o]
    k = k[o]
    starts = np.r_[0, np.flatnonzero(np.diff(k)) + 1]
    cnt = np.diff(np.r_[starts, len(k)])
    return idx, starts, cnt


def apply_groups(Uflat, grp):
    idx, starts, cnt = grp
    if idx.size == 0:
        return
    m = np.minimum.reduceat(Uflat[idx], starts)
    Uflat[idx] = np.repeat(m, cnt)


def comp_labels(mask, G):
    """labels of the connected components of the single-exchange graph k -> k + e_c - e_d (c, d in one cell) inside mask"""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    shape = mask.shape
    N = mask.size
    ids = np.arange(N).reshape(shape)
    rows, cols = [], []
    for g in G:
        for c in g:
            for d in g:
                if c < d:
                    sa = [slice(None)] * len(shape)
                    sb = [slice(None)] * len(shape)
                    sa[c] = slice(0, -1)
                    sb[c] = slice(1, None)
                    sa[d] = slice(1, None)
                    sb[d] = slice(0, -1)
                    both = mask[tuple(sa)] & mask[tuple(sb)]
                    rows.append(ids[tuple(sa)][both])
                    cols.append(ids[tuple(sb)][both])
    if rows:
        rows = np.concatenate(rows)
        cols = np.concatenate(cols)
    else:
        rows = np.zeros(0, int)
        cols = np.zeros(0, int)
    g = coo_matrix((np.ones(rows.size, np.int8), (rows, cols)), shape=(N, N))
    _, lab = connected_components(g, directed=False)
    return lab.reshape(shape)


def build(sizes, G1, G2, u, th, variant, ident):
    sizes = tuple(int(s) for s in sizes)
    nC = len(sizes)
    n = sum(sizes)
    shape = tuple(s + 1 for s in sizes)
    pu, L1, kap, h, a = consts(u)
    Theta = th * n * h
    axs = []
    for c, s in enumerate(sizes):
        shp = [1] * nC
        shp[c] = s + 1
        axs.append(np.arange(s + 1, dtype=np.int64).reshape(shp))
    R = np.zeros(shape)
    for c, s in enumerate(sizes):
        R = R + s * f(axs[c] / s)

    def key_cost(G):
        key = np.zeros(shape, dtype=np.int64)
        C = R.copy()
        radix = 1
        for g in G:
            K = np.zeros(shape, dtype=np.int64)
            for c in g:
                K = K + axs[c]
            ng = sum(sizes[c] for c in g)
            C -= ng * f(K / ng)
            key += radix * K
            radix *= (ng + 1)
        return key, C

    key1, C1 = key_cost(G1)
    key2, C2 = key_cost(G2)
    core = np.ones(shape, dtype=bool)
    for c, s in enumerate(sizes):
        core = core & (axs[c] >= kap * s - 1e-9) & (axs[c] <= (1 - kap) * s + 1e-9)
    tol = 1e-9
    vis1 = C1 <= Theta + tol
    blind = R <= Theta + tol
    if variant == 'P':
        src, idl, hidden, norm = core, [(G1, key1, core), (G2, key2, vis1)], C2 > Theta + tol, core
    elif variant == 'Pout':
        # Theorem P with the core replaced by the smallest lattice box CONTAINING K (bracket from the other side)
        core_out = np.ones(shape, dtype=bool)
        for c, s in enumerate(sizes):
            lo = np.floor(kap * s + 1e-9)
            core_out = core_out & (axs[c] >= lo) & (axs[c] <= s - lo)
        src, idl, hidden, norm = core_out, [(G1, key1, core_out), (G2, key2, vis1)], C2 > Theta + tol, core_out
    elif variant == 'alg':
        src, idl, hidden, norm = blind, [(G1, key1, blind), (G2, key2, vis1)], C2 > Theta + tol, blind
    elif variant == 'noH1':
        src, idl, hidden, norm = core, [(G2, key2, vis1)], C2 > Theta + tol, core
    elif variant == 'noH2':
        src, idl, hidden, norm = core, [(G1, key1, core)], C2 > Theta + tol, core
    elif variant == 'two':
        src, idl, hidden, norm = vis1, [(G1, key1, blind)], C1 > Theta + tol, vis1
    else:
        raise ValueError(variant)
    grps = []
    for G, key, mask in idl:
        if ident == 'comp':
            key = comp_labels(mask, G)
        grps.append(groups(key, mask))
    return dict(sizes=sizes, n=n, shape=shape, h=h, kap=kap, pu=pu, L1=L1, Theta=Theta, R=R, src=src,
                grps=grps, hidden=hidden, norm=norm)


def solve(R, src, grps, u, tol=1e-9, maxit=2000):
    BIG = 1e12
    U = np.where(src, R, BIG)
    it = 0
    while True:
        it += 1
        Uold = U
        U = lip(U, u)
        Uf = U.reshape(-1)
        for grp in grps:
            apply_groups(Uf, grp)
        if it >= 2 and float(np.max(np.abs(U - Uold))) < tol:
            break
        if it >= maxit:
            raise RuntimeError('no convergence')
    return U, it


def run_case(args):
    sizes, G1, G2, u, th, variant, ident = args
    t0 = time.time()
    b = build(sizes, G1, G2, u, th, variant, ident)
    if not b['src'].any():
        return dict(args=args, empty=True)
    U, it = solve(b['R'], b['src'], b['grps'], u)
    gap = U - b['R']
    nu = float(gap[b['norm']].max())
    nh = b['n'] * b['h']
    hid = b['hidden']
    nhid = int(hid.sum())
    if nhid:
        gh = np.where(hid, gap, -np.inf).reshape(-1)
        j = int(np.argmax(gh))
        gain = float(gh[j])
        at = tuple(int(x) for x in np.unravel_index(j, b['shape']))
    else:
        gain, at = float('-inf'), None
    excess = gain - nu - (nh - b['Theta'])
    return dict(args=args, empty=False, n=b['n'], nh=nh, nu=nu, nhid=nhid, gain=gain, excess=excess, at=at, it=it,
                nodes=int(U.size), secs=time.time() - t0)


def fmt(r):
    sizes, G1, G2, u, th, variant, ident = r['args']
    if r['empty']:
        return "%-5s %-4s u=%-4g %-22s G1=%-22s G2=%-26s Th/nh=%-5g : lattice core empty" % (
            variant, ident, u, sizes, G1, G2, th)
    return ("%-5s %-4s u=%-4g n=%-5d %-22s G1=%-22s G2=%-26s Th/nh=%-5g nh/u=%6.1f hidden=%-9d gain=%+9.3f "
            "excess=%+9.3f = %+7.3f u  at %s  [nu=%+.1e it=%d nodes=%d %.0fs]" % (
                variant, ident, u, r['n'], sizes, G1, G2, th, r['nh'] / u, r['nhid'], r['gain'], r['excess'],
                r['excess'] / u, r['at'], r['nu'], r['it'], r['nodes'], r['secs']))


def run_all(cases, procs=4, title=None):
    if title:
        print(title)
        sys.stdout.flush()
    res = []
    if procs > 1:
        with Pool(procs) as pool:
            for r in pool.imap(run_case, cases, chunksize=1):
                print("  " + fmt(r))
                sys.stdout.flush()
                res.append(r)
    else:
        for c in cases:
            r = run_case(c)
            print("  " + fmt(r))
            sys.stdout.flush()
            res.append(r)
    return res


def summarize(res, label):
    ok = [r for r in res if not r['empty'] and r['args'][4] >= 1.0 and r['nhid'] > 0]
    if not ok:
        return
    w = max(ok, key=lambda r: r['excess'] / r['args'][3])
    print("  >> %s: %d cases with Theta >= n h and hidden types; largest excess = %+.3f u  (%s)" % (
        label, len(ok), w['excess'] / w['args'][3], fmt(w).split(' nh/u')[0]))
    sys.stdout.flush()


# ---------------------------------------------------------------- validation against Dijkstra
def dijkstra_reference(shape, R, src, grps, u):
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import dijkstra
    N = R.size
    ids = np.arange(N).reshape(shape)
    rows, cols, w = [], [], []
    for ax in range(len(shape)):
        sa = [slice(None)] * len(shape)
        sb = [slice(None)] * len(shape)
        sa[ax] = slice(0, -1)
        sb[ax] = slice(1, None)
        i = ids[tuple(sa)].ravel()
        j = ids[tuple(sb)].ravel()
        rows += [i, j]
        cols += [j, i]
        w += [np.full(i.size, u), np.full(i.size, u)]
    nxt = N
    EPS = 1e-12
    for idx, starts, cnt in grps:
        gid = np.repeat(np.arange(len(starts)), cnt) + nxt
        rows += [idx, gid]
        cols += [gid, idx]
        w += [np.full(idx.size, EPS), np.full(idx.size, EPS)]
        nxt += len(starts)
    s = nxt
    sidx = np.flatnonzero(src.ravel())
    rows.append(np.full(sidx.size, s))
    cols.append(sidx)
    w.append(R.ravel()[sidx] + 1.0)
    G = csr_matrix((np.concatenate(w), (np.concatenate(rows), np.concatenate(cols))), shape=(s + 1, s + 1))
    d = dijkstra(G, directed=True, indices=s)
    return (d[:N] - 1.0).reshape(shape)


def validate():
    print("VALIDATION: closure iteration against scipy Dijkstra on the explicit graph (max |difference| of U*)")
    worst = 0.0
    cases = [((12, 14), [[0, 1]], [[0, 1]]), ((8, 10, 12), [[0, 1, 2]], [[0], [1, 2]]),
             ((6, 8, 10, 8), [[0, 1, 2, 3]], [[0], [1], [2, 3]]), ((6, 8, 6, 10), [[0, 1], [2, 3]], [[0, 1], [2], [3]]),
             ((4, 6, 6, 4, 6), [[0, 1, 2, 3, 4]], [[0, 1], [2, 3], [4]])]
    for sizes, G1, G2 in cases:
        for u in (1.0, 4.0):
            for th in (0.7, 1.0, 1.6):
                for variant in ('P', 'alg', 'noH1', 'noH2', 'two'):
                    for ident in ('hub', 'comp'):
                        b = build(sizes, G1, G2, u, th, variant, ident)
                        if not b['src'].any():
                            continue
                        U, it = solve(b['R'], b['src'], b['grps'], u)
                        D = dijkstra_reference(b['shape'], b['R'], b['src'], b['grps'], u)
                        worst = max(worst, float(np.max(np.abs(U - D))))
    print("  %d-class lattices, 5 variants x 2 identification modes x 2 slopes x 3 budgets: max |U_closure - U_dijkstra| = %.2e"
          % (5, worst))
    print("  PASS" if worst < 1e-7 else "  FAIL")


# ---------------------------------------------------------------- experiment lists
CONF = {
    'c1 three classes in one cell, never split':            ((40, 60, 80), [[0, 1, 2]], [[0, 1, 2]]),
    'c2 class of weight 3.3% in a cell of three':           ((6, 84, 90), [[0, 1, 2]], [[0, 1, 2]]),
    'c3 3.3% class stays with a big one after the split':   ((6, 84, 90), [[0, 1, 2]], [[0, 1], [2]]),
    'c4 cell split into three {0},{1},{2,3}':               ((30, 34, 38, 42), [[0, 1, 2, 3]], [[0], [1], [2, 3]]),
    'c5 five classes, split into {0,1},{2,3},{4}':          ((14, 16, 18, 20, 22), [[0, 1, 2, 3, 4]], [[0, 1], [2, 3], [4]]),
    'c6 nested {0,1},{2,3} -> {0,1},{2},{3}':               ((30, 34, 38, 42), [[0, 1], [2, 3]], [[0, 1], [2], [3]]),
    'c7 three hidden classes left in a cell after split':   ((24, 30, 36, 54), [[0, 1, 2, 3]], [[0, 1, 2], [3]]),
    'c8 2.5% class with one big class':                     ((6, 234), [[0, 1]], [[0, 1]]),
    'c9 two equal classes (reference, tight at Theta=nh)':  ((120, 120), [[0, 1]], [[0, 1]]),
    'c10 four classes in one cell, never split':            ((30, 34, 38, 42), [[0, 1, 2, 3]], [[0, 1, 2, 3]]),
    'c11 two cells of G1, each hiding a pair forever':      ((30, 34, 38, 42), [[0, 1], [2, 3]], [[0, 1], [2, 3]]),
    'c12 2% class + 3 classes, split {0,1},{2,3}':          ((4, 60, 64, 72), [[0, 1, 2, 3]], [[0, 1], [2, 3]]),
}
THS = (0.7, 1.0, 1.05, 1.2, 1.5, 2.5)


def sweep(which, variant='P', ident='hub', us=(1.0, 2.0, 4.0)):
    names = [k for k in CONF if k.split()[0] in which]
    cases = []
    for name in names:
        sizes, G1, G2 = CONF[name]
        for u in us:
            for th in THS:
                cases.append((sizes, G1, G2, u, th, variant, ident))
    print("SWEEP variant=%s ident=%s; configurations:" % (variant, ident))
    for name in names:
        print("   " + name + "  sizes %s" % (CONF[name][0],))
    res = run_all(cases)
    summarize(res, "sweep %s/%s %s" % (variant, ident, ",".join(which)))
    return res


def scaling(series, variant='P', ident='hub', us=(2.0, 4.0), ths=(1.0, 1.1), procs=4):
    cases = []
    for name, base, G1, G2, scales in series:
        for u in us:
            for th in ths:
                for s in scales:
                    cases.append((tuple(b * s for b in base), G1, G2, u, th, variant, ident))
    print("SCALING variant=%s ident=%s (same proportions, n growing): a violation of the theorem shows as an excess growing linearly in n"
          % (variant, ident))
    res = run_all(cases, procs=procs)
    summarize(res, "scaling %s/%s" % (variant, ident))
    return res


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == 'validate':
        validate()
    elif mode == 'sweep':
        sweep(sys.argv[2].split(','), variant=sys.argv[3] if len(sys.argv) > 3 else 'P',
              ident=sys.argv[4] if len(sys.argv) > 4 else 'hub')
    elif mode == 'controls':
        # (i) below h: the plain dip of Remark 4 must be found
        print("CONTROL (i): Theta = 0.7 n h, two equal classes in one cell: excess must be >= that of the plain dip, "
              "n[D(theta) - (h - theta)], D = u f^{-1}(theta) - Lambda_1, and grow linearly")
        for u in (2.0, 4.0):
            pu, L1, kap, h, a = consts(u)
            pred = (u * finv(0.7 * h) - L1) - 0.3 * h
            res = run_all([((s, s), [[0, 1]], [[0, 1]], u, 0.7, 'P', 'hub') for s in (60, 120, 240, 480)], procs=4)
            print("     plain-dip prediction per coordinate: %+.5f ;  measured excess/n: %s" % (
                pred, ", ".join("%+.5f" % (r['excess'] / r['n']) for r in res)))
        # (ii) mutations of the hypotheses
        print("CONTROL (ii): hypothesis (H1) dropped, G1 = one cell, G2 = {0,1},{2,3}; Theta = n h and 1.2 n h")
        run_all([((s, s, s, s), [[0, 1, 2, 3]], [[0, 1], [2, 3]], u, th, 'noH1', 'hub')
                 for u in (2.0, 4.0) for th in (1.0, 1.2) for s in (12, 24, 36)], procs=4)
        print("CONTROL (ii'): same structure with (H1) kept (Theorem P)")
        run_all([((s, s, s, s), [[0, 1, 2, 3]], [[0, 1], [2, 3]], u, th, 'P', 'hub')
                 for u in (2.0, 4.0) for th in (1.0, 1.2) for s in (12, 24, 36)], procs=4)
        print("CONTROL (iii): hypothesis (H2) dropped, same structure")
        run_all([((s, s, s, s), [[0, 1, 2, 3]], [[0, 1], [2, 3]], u, th, 'noH2', 'hub')
                 for u in (2.0, 4.0) for th in (1.0, 1.2) for s in (12, 24, 36)], procs=4)
        # (iv) the two-round situation: blocks A (centre found in round 1) and B (centre hidden), phi_A = 0.64
        print("CONTROL (iv): two rounds only (final batch = shells of G1), classes (A0,A1,B0,B1), G1 = {A0},{A1},{B0,B1}, phi_A = 0.64:")
        print("              the archive's two-round separation (Theorem 11.86) says the hidden mass exceeds the visible one for Theta up to ~1.3 n h")
        run_all([((16 * s, 16 * s, 9 * s, 9 * s), [[0], [1], [2, 3]], [[0], [1], [2, 3]], u, th, 'two', 'hub')
                 for u in (2.0, 4.0) for th in (1.0, 1.2, 1.5) for s in (1, 2, 3)], procs=4)
    elif mode == 'scale1':
        scaling([('two classes 1:3', (1, 3), [[0, 1]], [[0, 1]], (60, 120, 240, 480)),
                 ('three classes 2:3:4 in one cell', (2, 3, 4), [[0, 1, 2]], [[0, 1, 2]], (10, 20, 40, 60)),
                 ('3.3% class, split {0,1},{2}', (1, 14, 15), [[0, 1, 2]], [[0, 1], [2]], (6, 12, 24, 36))])
    elif mode == 'scale2':
        scaling([('cell split into three', (1, 1, 1, 1), [[0, 1, 2, 3]], [[0], [1], [2, 3]], (12, 24, 36, 48)),
                 ('three hidden classes after split', (2, 3, 4, 5), [[0, 1, 2, 3]], [[0, 1, 2], [3]], (4, 8, 12, 15)),
                 ('nested', (3, 4, 4, 5), [[0, 1], [2, 3]], [[0, 1], [2], [3]], (3, 6, 9, 12))])
    elif mode == 'scale3':
        scaling([('five classes split into three', (1, 1, 1, 1, 1), [[0, 1, 2, 3, 4]], [[0, 1], [2, 3], [4]], (8, 14, 20, 26)),
                 ('G1 = G2 = two cells with hidden pairs', (2, 3, 3, 4), [[0, 1], [2, 3]], [[0, 1], [2, 3]], (4, 8, 12, 16))])
    elif mode == 'big':
        scaling([('cell split into three', (1, 1, 1, 1), [[0, 1, 2, 3]], [[0], [1], [2, 3]], (64,)),
                 ('pairs {0,1},{2,3} after split', (1, 1, 1, 1), [[0, 1, 2, 3]], [[0, 1], [2, 3]], (64,))],
                us=(4.0,), ths=(1.0, 1.1), procs=4)
    else:
        raise SystemExit("unknown mode")
