"""Review item 1b: attempt to refute Lemma B (the relaxation lemma) numerically.

For given blocks, roles (P/Q/T per block), slope u and budget Theta the script computes the POINTWISE
LARGEST G = -F on the whole grid of types subject to exactly the hypotheses of the lemma:

  (adm)  |G(d) - G(d')| <= u for grid neighbours,
  (H1)   G(d) = G(d') for d, d' in V_0(Theta) with d_P = d'_P and d_j = d'_j (mod 2) for j not in P,
  (H2)   G(d) = G(d') for d, d' in V_P(Theta) with d_{P u Q} = d'_{P u Q} and d_j = d'_j (mod 2) for j in T,
  (norm) nu(d) = G(d) - t(d) <= 0 on V_0(Theta)            (i.e. nu_0 <= 0; it is attained, nu_0 = 0).

These are difference constraints, so the pointwise largest solution is a shortest-path distance: contract
the (H1)/(H2) classes (connected components of the union of the two relations), join neighbouring classes
by edges of length u and a virtual source to every class by the least t(d) over its members in V_0(Theta).
For every admissible F with (H1), (H2):  nu_F(y) - nu_0(F) <= nu*(y) for all y, with equality for F = -G*.
So Lemma B is equivalent to

  X := max_y [ nu*(y) - n phi_P h + min{ t_T(y), Theta - n (1 - phi_P) h } ]  <=  m (u + 5 ln(n+1)).

Exact binomial costs.  parity=True is the lemma as stated (profiles may depend on the parities of the
non-revealed coordinates); parity=False is the weaker family used by the author's script.

usage:  python3 r2_lemmaB.py selftest | small | scale2 | scale3 | scale4 | outside
"""
import math
import sys
import time
import itertools
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
from rv_common import consts, tcost


def extremal(ns, roles, u, Theta, parity=True, return_G=False):
    m = len(ns)
    n = sum(ns)
    shape = tuple(x + 1 for x in ns)
    N = int(np.prod(shape))
    ts = [tcost(x) for x in ns]
    grids = np.meshgrid(*[np.arange(x + 1) for x in ns], indexing='ij', sparse=True)
    P = [j for j in range(m) if roles[j] == 'P']
    Q = [j for j in range(m) if roles[j] == 'Q']
    T = [j for j in range(m) if roles[j] == 'T']
    zero = np.zeros(shape)
    tall = zero + sum(ts[j][grids[j]] for j in range(m))
    tQT = zero + sum(ts[j][grids[j]] for j in Q + T) if Q + T else zero.copy()
    tT = zero + sum(ts[j][grids[j]] for j in T) if T else zero.copy()
    V0 = tall <= Theta
    VP = tQT <= Theta
    idx = np.arange(N, dtype=np.int64).reshape(shape)

    def key_array(fixed):
        key = np.zeros(shape, dtype=np.int64)
        for j in range(m):
            if j in fixed:
                key = key * (ns[j] + 1) + grids[j]
            else:
                key = key * 2 + ((grids[j] % 2) if parity else 0)
        return key

    rows = []
    cols = []
    for region, fixed in ((V0, P), (VP, P + Q)):
        nodes = idx[region]
        keys = key_array(fixed)[region]
        uniq, inv = np.unique(keys, return_inverse=True)
        rep = np.empty(len(uniq), dtype=np.int64)
        rep[inv[::-1]] = nodes[::-1]          # first member of each class
        rows.append(nodes)
        cols.append(rep[inv])
    rows = np.concatenate(rows)
    cols = np.concatenate(cols)
    A = coo_matrix((np.ones(len(rows), dtype=np.int8), (rows, cols)), shape=(N, N)).tocsr()
    ncomp, lab = connected_components(A, directed=False)
    lab = lab.astype(np.int64)
    labg = lab.reshape(shape)
    # quotient edges
    pairs = []
    for j in range(m):
        sl_a = [slice(None)] * m
        sl_b = [slice(None)] * m
        sl_a[j] = slice(0, ns[j])
        sl_b[j] = slice(1, ns[j] + 1)
        a = labg[tuple(sl_a)].ravel()
        b = labg[tuple(sl_b)].ravel()
        keep = a != b
        a = a[keep]
        b = b[keep]
        lo = np.minimum(a, b)
        hi = np.maximum(a, b)
        pairs.append(np.unique(lo * ncomp + hi))
    pairs = np.unique(np.concatenate(pairs))
    ea = pairs // ncomp
    eb = pairs % ncomp
    cap = np.full(ncomp, np.inf)
    np.minimum.at(cap, lab[V0.ravel()], tall.ravel()[V0.ravel()])
    fin = np.isfinite(cap)
    src = ncomp
    OFF = 1.0     # keeps every edge weight strictly positive; subtracted again below
    r = np.concatenate([ea, np.full(int(fin.sum()), src, dtype=np.int64)])
    c = np.concatenate([eb, np.nonzero(fin)[0]])
    w = np.concatenate([np.full(len(ea), float(u)), cap[fin] + OFF])
    Gq = csr_matrix((w, (r, c)), shape=(ncomp + 1, ncomp + 1))
    dist = dijkstra(Gq, directed=False, indices=src)
    G = (dist[:ncomp] - OFF)[lab].reshape(shape)
    nu = G - tall
    nu0 = float(nu[V0].max())
    c0 = consts(u)
    h = c0['h']
    L = math.log(n + 1.0)
    phiP = sum(ns[j] for j in P) / n
    core = nu0 + n * phiP * h - np.minimum(tT, Theta - n * (1.0 - phiP) * h)
    exc = nu - core
    am = int(np.argmax(exc))
    X = float(exc.ravel()[am])
    ytype = np.unravel_index(am, shape)
    hidden = tT > Theta
    Xh = float((nu[hidden] - nu0 + (Theta - n * h)).max()) if hidden.any() else float('nan')
    # sanity: admissibility of the constructed function
    lip = 0.0
    for j in range(m):
        lip = max(lip, float(np.abs(np.diff(G, axis=j)).max()))
    out = dict(ns=ns, roles=roles, u=u, Theta=Theta, n=n, m=m, h=h, L=L, nu0=nu0, X=X, ytype=ytype,
               Xhidden=Xh, allow=m * (u + 5 * L), lip=lip, ncomp=ncomp, N=N,
               hyp_Theta=(Theta >= n * h + 2 * m * L - 1e-9), hyp_N=all(x >= c0['Nu'] for x in ns))
    if return_G:
        out['G'] = G
        out['V0'] = V0
        out['VP'] = VP
        out['tall'] = tall
    return out


def fmt(o, tag=''):
    return ('%-8s ns=%-22s roles=%-5s u=%-4g Theta=%9.3f (=%.3f n h; n h+2mL=%8.3f) hyp[Theta,N_u]=%d%d | nu0=%+.1e '
            'X=%+8.3f at y=%-18s Xhidden=%+8.3f | allowance m(u+5L)=%7.2f | lip/u=%.6f | classes %d of %d'
            % (tag, str(tuple(o['ns'])), o['roles'], o['u'], o['Theta'], o['Theta'] / (o['n'] * o['h']),
               o['n'] * o['h'] + 2 * o['m'] * o['L'], o['hyp_Theta'], o['hyp_N'], o['nu0'], o['X'],
               str(tuple(int(v) for v in o['ytype'])), o['Xhidden'], o['allow'], o['lip'] / o['u'], o['ncomp'], o['N']))


def selftest():
    """validate the shortest-path construction against a linear programme on tiny grids."""
    from scipy.optimize import linprog
    rng = np.random.default_rng(1)
    worst = 0.0
    for case in range(12):
        m = int(rng.integers(2, 4))
        ns = [int(rng.integers(3, 7)) for _ in range(m)]
        roles = ''.join(rng.choice(list('PQT'), size=m))
        u = float(rng.choice([0.7, 1.5, 3.0]))
        Theta = float(rng.uniform(0.5, 4.0))
        for parity in (True, False):
            o = extremal(ns, roles, u, Theta, parity=parity, return_G=True)
            G = o['G']
            shape = G.shape
            N = G.size
            idx = np.arange(N).reshape(shape)
            A_ub = []
            b_ub = []
            A_eq = []
            b_eq = []
            for j in range(m):
                sa = [slice(None)] * m
                sb = [slice(None)] * m
                sa[j] = slice(0, ns[j])
                sb[j] = slice(1, ns[j] + 1)
                for a, b in zip(idx[tuple(sa)].ravel(), idx[tuple(sb)].ravel()):
                    row = np.zeros(N); row[a] = 1; row[b] = -1
                    A_ub.append(row); b_ub.append(u)
                    A_ub.append(-row); b_ub.append(u)
            V0 = o['V0'].ravel(); VP = o['VP'].ravel(); tall = o['tall'].ravel()
            for d in range(N):
                if V0[d]:
                    row = np.zeros(N); row[d] = 1
                    A_ub.append(row); b_ub.append(tall[d])
            P = [j for j in range(m) if roles[j] == 'P']
            Q = [j for j in range(m) if roles[j] == 'Q']
            types = list(itertools.product(*[range(x + 1) for x in ns]))
            for region, fixed in ((V0, P), (VP, P + Q)):
                for a in range(N):
                    if not region[a]:
                        continue
                    for b in range(a + 1, N):
                        if not region[b]:
                            continue
                        ok = True
                        for j in range(m):
                            if j in fixed:
                                ok = ok and types[a][j] == types[b][j]
                            elif parity:
                                ok = ok and (types[a][j] - types[b][j]) % 2 == 0
                        if ok:
                            row = np.zeros(N); row[a] = 1; row[b] = -1
                            A_eq.append(row); b_eq.append(0.0)
            # one LP suffices: maximise the sum (the pointwise largest solution maximises every coordinate)
            res = linprog(-np.ones(N), A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                          A_eq=np.array(A_eq) if A_eq else None, b_eq=np.array(b_eq) if b_eq else None,
                          bounds=[(None, None)] * N, method='highs')
            dev = float(np.abs(res.x - G.ravel()).max())
            worst = max(worst, dev)
            print('selftest ns=%s roles=%s u=%g Theta=%.2f parity=%d: max |LP - shortest path| = %.2e'
                  % (ns, roles, u, Theta, parity, dev))
    print('selftest worst deviation %.2e' % worst)
    return worst < 1e-6


def group_small(us=(1.0, 2.0, 4.0, 8.0)):
    """many role patterns / odd-even sizes at small n, Theta exactly as the lemma requires."""
    worst = (-1e300, None)
    worstX = (-1e300, None)
    cnt = 0
    for u in us:
        c = consts(u)
        Nu = c['Nu']
        size_sets = [
            (Nu, Nu), (Nu + 1, Nu), (2 * Nu + 1, Nu), (3 * Nu, 2 * Nu + 1),
            (Nu, Nu, Nu), (Nu + 1, Nu, Nu + 2), (2 * Nu, Nu, 3 * Nu + 1),
            (Nu, Nu, Nu, Nu), (Nu + 1, Nu, 2 * Nu, Nu + 3),
        ]
        for ns in size_sets:
            m = len(ns)
            n = sum(ns)
            L = math.log(n + 1.0)
            for roles in itertools.product('PQT', repeat=m):
                roles = ''.join(roles)
                for mult in (0.0, 0.5, 1.5, 4.0):
                    Theta = n * c['h'] + 2 * m * L + mult * n * c['h']
                    o = extremal(list(ns), roles, u, Theta, parity=True)
                    cnt += 1
                    if o['X'] - o['allow'] > worst[0]:
                        worst = (o['X'] - o['allow'], o)
                    if o['X'] > worstX[0]:
                        worstX = (o['X'], o)
                    assert o['lip'] <= u + 1e-9 and abs(o['nu0']) < 1e-9
        print('u=%g done, cases so far %d, largest X - allowance so far %.3f' % (u, cnt, worst[0]), flush=True)
    print('small group: %d cases; largest X - m(u+5L) = %.3f in case:' % (cnt, worst[0]))
    print(fmt(worst[1], 'worst'))
    print('largest X itself = %.3f in case:' % worstX[0])
    print(fmt(worstX[1], 'maxX'))
    return worst[0] <= 0


def scaling(patterns, n_list, us, ratios, parities=(True, False)):
    """fixed proportions and fixed Theta/(n h), growing n: does X stay bounded (lemma) or grow like n (refutation)?"""
    ok = True
    gmaxX = -1e300
    gmaxXh = -1e300
    for u in us:
        c = consts(u)
        for roles, props in patterns:
            m = len(roles)
            for ratio in ratios:
                for parity in parities:
                    row = []
                    for n in n_list:
                        ns = [max(c['Nu'], int(round(p * n))) for p in props]
                        ns[-1] += n - sum(ns)
                        if ns[-1] < c['Nu']:
                            continue
                        L = math.log(sum(ns) + 1.0)
                        Theta = ratio * sum(ns) * c['h'] + 2 * m * L
                        o = extremal(ns, roles, u, Theta, parity=parity)
                        ok = ok and (o['X'] <= o['allow'])
                        gmaxX = max(gmaxX, o['X'])
                        if o['Xhidden'] == o['Xhidden']:
                            gmaxXh = max(gmaxXh, o['Xhidden'])
                        row.append((sum(ns), o['X'], o['Xhidden'], o['allow']))
                    s = ' | '.join('n=%d: %+.3f, %+.2f (%.0f)' % r for r in row)
                    print('u=%g %s %s Theta=%.2f n h+2mL par=%d :: %s' % (u, roles, tuple(round(p, 3) for p in props), ratio, parity, s), flush=True)
    print('columns per n:  X, Xhidden (allowance m(u+5L));  X = max_y [nu*(y) - n phi_P h + min{t_T(y), Theta - n(1-phi_P)h}],')
    print('                Xhidden = max over y with t_T(y) > Theta of [nu*(y) + (Theta - n h)];  the lemma claims both <= allowance')
    print('largest X in this group: %+.3f; largest Xhidden: %+.3f' % (gmaxX, gmaxXh))
    return ok


def group_outside():
    """outside the hypothesis Theta >= n h + 2 m L (the range the author's script used: Theta = ratio * n h)."""
    for u in (1.0, 2.0, 4.0):
        c = consts(u)
        for roles, ns in (('PQT', (80, 80, 80)), ('PTT', (60, 100, 120)), ('QTT', (81, 99, 100)), ('TTT', (70, 90, 80)),
                          ('PT', (300, 301)), ('QT', (301, 300)), ('TT', (299, 300))):
            for ratio in (1.0, 1.1, 1.3):
                n = sum(ns)
                Theta = ratio * n * c['h']
                res = []
                for parity in (True, False):
                    o = extremal(list(ns), roles, u, Theta, parity=parity)
                    res.append(o)
                print('u=%g roles=%s ns=%s Theta=%.2f n h (hyp Theta: %d) | parity: X=%+.3f Xhid=%+.3f | no parity: X=%+.3f Xhid=%+.3f | allowance %.1f'
                      % (u, roles, ns, ratio, res[0]['hyp_Theta'], res[0]['X'], res[0]['Xhidden'], res[1]['X'], res[1]['Xhidden'], res[0]['allow']),
                      flush=True)


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'selftest'
    t0 = time.time()
    if what == 'selftest':
        ok = selftest()
    elif what == 'small':
        ok = group_small(tuple(float(x) for x in sys.argv[2:])) if len(sys.argv) > 2 else group_small()
    elif what == 'scale2':
        pats = [('PT', (0.5, 0.5)), ('QT', (0.5, 0.5)), ('TT', (0.5, 0.5)), ('PT', (0.25, 0.75)), ('PT', (0.75, 0.25)),
                ('QT', (0.3, 0.7)), ('PQ', (0.5, 0.5))]
        us = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else [1.0, 4.0]
        ok = scaling(pats, [500, 1000, 2000, 4000], us, [1.0, 1.15, 1.3, 2.0], parities=(True,))
    elif what == 'scale3':
        pats = [('PQT', (1 / 3, 1 / 3, 1 / 3)), ('PQT', (0.2, 0.3, 0.5)), ('PTT', (0.3, 0.3, 0.4)), ('QQT', (0.25, 0.25, 0.5)),
                ('QTT', (0.3, 0.3, 0.4)), ('PPT', (0.2, 0.3, 0.5)), ('TTT', (1 / 3, 1 / 3, 1 / 3))]
        ok = scaling(pats, [90, 180, 360], [1.0, 4.0], [1.0, 1.3, 2.0], parities=(True,))
    elif what == 'scale4':
        pats = [('PQTT', (0.25, 0.25, 0.25, 0.25)), ('PPQT', (0.2, 0.2, 0.3, 0.3)), ('PQQT', (0.25, 0.25, 0.25, 0.25)),
                ('QTTT', (0.25, 0.25, 0.25, 0.25))]
        ok = scaling(pats, [84, 168], [2.0, 4.0], [1.0, 1.3], parities=(True,))
    elif what == 'outside':
        group_outside()
        ok = True
    else:
        raise SystemExit('unknown group')
    print('group %s finished in %.1f s; lemma respected in every case of this group: %s' % (what, time.time() - t0, ok))
