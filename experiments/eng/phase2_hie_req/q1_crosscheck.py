#!/usr/bin/env python3
"""Cross-checks of q1_lemma_b.solve by two routes that share no class/transform code with it:
  (1) Dijkstra (heapq) on the explicit graph: types + one node per class (edges of length 0), neighbour edges
      of length u, super-source with edge t(s) to every s in V_0.  Classes built with Python dicts of tuples.
  (2) HiGHS linear programmes (scipy.optimize.linprog): variables G(d); constraints enumerated from the
      definitions pairwise (every pair d, d' of the same region with the required agreement gets G(d) = G(d')
      via a chain to the first such d'); objective max sum_d G(d) (which yields the pointwise maximum),
      and separately max G(y) for a few single y.
Also the negative controls: the same lemma quantity with (H2) dropped, (H1) dropped, both dropped.
"""
import heapq
import itertools
import math
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import q1_lemma_b as q  # noqa: E402  (my own code, for the quantity being cross-checked)


def basics(ns, roles, u, th):
    c = q.consts(u)
    n = sum(ns)
    Theta = th * n * c["h"]
    tj = [q.tcost(x) for x in ns]
    types = list(itertools.product(*[range(x + 1) for x in ns]))
    P = [j for j, r in enumerate(roles) if r == "P"]
    Q = [j for j, r in enumerate(roles) if r == "Q"]
    T = [j for j, r in enumerate(roles) if r == "T"]
    t = {d: sum(tj[j][d[j]] for j in range(len(ns))) for d in types}
    tQT = {d: sum(tj[j][d[j]] for j in Q + T) for d in types}
    return c, n, Theta, tj, types, P, Q, T, t, tQT


def class_dicts(ns, roles, u, th, use_h1=True, use_h2=True):
    c, n, Theta, tj, types, P, Q, T, t, tQT = basics(ns, roles, u, th)
    groups = []
    if use_h1:
        g = {}
        for d in types:
            if t[d] <= Theta:
                key = tuple(d[j] if j in P else d[j] % 2 for j in range(len(ns)))
                g.setdefault(key, []).append(d)
        groups.append(g)
    if use_h2:
        g = {}
        for d in types:
            if tQT[d] <= Theta:
                key = tuple(d[j] if j in P + Q else d[j] % 2 for j in range(len(ns)))
                g.setdefault(key, []).append(d)
        groups.append(g)
    return groups


def dijkstra(ns, roles, u, th, **kw):
    c, n, Theta, tj, types, P, Q, T, t, tQT = basics(ns, roles, u, th)
    groups = class_dicts(ns, roles, u, th, **kw)
    member_of = {}
    for gi, g in enumerate(groups):
        for key, mem in g.items():
            for d in mem:
                member_of.setdefault(d, []).append((gi, key))
    dist = {}
    cdist = {}
    heap = [(t[d], 0, d) for d in types if t[d] <= Theta]
    heapq.heapify(heap)
    m = len(ns)
    while heap:
        dv, kind, v = heapq.heappop(heap)
        if kind == 0:
            if v in dist:
                continue
            dist[v] = dv
            for j in range(m):
                for s in (-1, 1):
                    w = list(v); w[j] += s
                    if 0 <= w[j] <= ns[j]:
                        w = tuple(w)
                        if w not in dist:
                            heapq.heappush(heap, (dv + u, 0, w))
            for ck in member_of.get(v, []):
                if ck not in cdist:
                    heapq.heappush(heap, (dv, 1, ck))
        else:
            if v in cdist:
                continue
            cdist[v] = dv
            gi, key = v
            for w in groups[gi][key]:
                if w not in dist:
                    heapq.heappush(heap, (dv, 0, w))
    return dist


def lp(ns, roles, u, th, single=()):
    c, n, Theta, tj, types, P, Q, T, t, tQT = basics(ns, roles, u, th)
    N = len(types)
    index = {d: i for i, d in enumerate(types)}
    rows, cols, vals, b = [], [], [], []
    r = 0
    m = len(ns)
    for d in types:  # Lipschitz, both directions
        for j in range(m):
            if d[j] < ns[j]:
                w = list(d); w[j] += 1; w = tuple(w)
                for s in (1, -1):
                    rows += [r, r]; cols += [index[d], index[w]]; vals += [s, -s]; b.append(u); r += 1
    for d in types:  # G <= t on V0
        if t[d] <= Theta:
            rows.append(r); cols.append(index[d]); vals.append(1.0); b.append(t[d]); r += 1
    A_ub = coo_matrix((vals, (rows, cols)), shape=(r, N)).tocsr()
    # equalities, enumerated pairwise from the definition (numpy over all pairs), chained to the first partner
    D = np.array(types)
    tv = np.array([t[d] for d in types])
    tqv = np.array([tQT[d] for d in types])
    erows, ecols, evals = [], [], []
    e = 0
    for region, exact in ((tv <= Theta, P), (tqv <= Theta, P + Q)):
        idx = np.flatnonzero(region)
        Dr = D[idx]
        same = np.ones((len(idx), len(idx)), dtype=bool)
        for j in range(m):
            if j in exact:
                same &= Dr[:, None, j] == Dr[None, :, j]
            else:
                same &= (Dr[:, None, j] % 2) == (Dr[None, :, j] % 2)
        for a in range(len(idx)):
            partners = np.flatnonzero(same[a, :a])
            if len(partners):
                erows += [e, e]; ecols += [idx[a], idx[partners[0]]]; evals += [1.0, -1.0]; e += 1
    A_eq = coo_matrix((evals, (erows, ecols)), shape=(e, N)).tocsr() if e else None
    b_eq = np.zeros(e) if e else None
    res = linprog(-np.ones(N), A_ub=A_ub, b_ub=np.array(b), A_eq=A_eq, b_eq=b_eq,
                  bounds=[(None, None)] * N, method="highs")
    assert res.status == 0, res.message
    Gsum = {d: res.x[i] for i, d in enumerate(types)}
    singles = {}
    for y in single:
        obj = np.zeros(N); obj[index[y]] = -1
        rs = linprog(obj, A_ub=A_ub, b_ub=np.array(b), A_eq=A_eq, b_eq=b_eq, bounds=[(None, None)] * N, method="highs")
        assert rs.status == 0, rs.message
        singles[y] = -rs.fun
    return Gsum, singles, (N, r, e)


def main():
    out = []
    pr = lambda s: (print(s, flush=True), out.append(s))
    t0 = time.time()
    pr("## (1) Dijkstra vs min-plus fixed point (all types compared)")
    for ns, roles, u, th in [((20, 30, 40), "PQT", 2.0, 1.1), ((24, 24, 24), "QQT", 1.0, 1.0),
                             ((16, 20, 24, 12), "PQTT", 4.0, 1.3), ((30, 30, 30), "QTT", 4.0, 1.0),
                             ((12, 30, 40), "TPQ", 0.5, 1.3), ((40, 40, 40), "PTT", 2.0, 1.0)]:
        sol = q.solve(ns, roles, u, th * sum(ns) * q.consts(u)["h"])
        dist = dijkstra(ns, roles, u, th)
        err = max(abs(sol["G"][d] - v) for d, v in dist.items())
        pr(f"ns={ns} roles={roles} u={u} th/h={th}: types={len(dist)} max|G_minplus - G_dijkstra|={err:.2e}")
    pr("## (2) LP (HiGHS) vs min-plus, tiny grids")
    for ns, roles, u, th in [((8, 9, 10), "PQT", 4.0, 1.0), ((8, 10, 12), "QQT", 4.0, 1.1),
                             ((12, 12, 12), "PTT", 2.0, 1.3), ((6, 8, 8, 10), "PQTT", 4.0, 1.0),
                             ((10, 10, 14), "QTT", 2.0, 1.0), ((9, 11, 13), "TPQ", 1.0, 1.3)]:
        c = q.consts(u)
        Theta = th * sum(ns) * c["h"]
        sol = q.solve(ns, roles, u, Theta)
        r = q.evaluate(ns, roles, u, th)
        ys = [tuple(r["argmax"]), tuple(0 for _ in ns), tuple(x for x in ns), tuple(x // 3 for x in ns)]
        Gsum, singles, size = lp(ns, roles, u, th, single=ys)
        err = max(abs(sol["G"][d] - v) for d, v in Gsum.items())
        serr = max(abs(sol["G"][y] - v) for y, v in singles.items())
        # lemma quantity recomputed from the LP solution
        nP = sum(ns[j] for j, x in enumerate(roles) if x == "P")
        tj = [q.tcost(x) for x in ns]
        T = [j for j, x in enumerate(roles) if x == "T"]
        Vlp = max(Gsum[d] - sum(tj[j][d[j]] for j in range(len(ns))) - nP * c["h"]
                  + min(sum(tj[j][d[j]] for j in T), Theta - (sum(ns) - nP) * c["h"]) for d in Gsum)
        pr(f"ns={ns} roles={roles} u={u} th/h={th}: LP vars/ineq/eq={size} max|G_minplus-G_LP(sum)|={err:.2e} "
           f"max|..-G_LP(single y, {len(ys)} y)|={serr:.2e}  V_minplus={r['V']:+.6f} V_LP={Vlp:+.6f} allow={r['allowance']:.2f}")
    pr("## (3) negative controls: hypotheses dropped (same quantity, same allowance)")
    for ns, roles, u, th in [((120, 120, 120), "PQT", 4.0, 1.1), ((120, 120, 120), "QQT", 4.0, 1.1),
                             ((40, 40, 320), "PQT", 4.0, 1.1), ((40, 40, 320), "QQT", 4.0, 1.3),
                             ((40, 40, 320), "PQT", 2.0, 1.1), ((20, 20, 360), "QQT", 4.0, 1.0),
                             ((36, 162, 162), "PQT", 1.0, 1.1), ((50, 50, 50, 50), "PQTT", 2.0, 1.1)]:
        for kw, lab in [({}, "full"), (dict(use_h2=False), "no H2"), (dict(use_h1=False), "no H1"),
                        (dict(use_h1=False, use_h2=False), "no H1,H2"), (dict(use_parity=False), "no parity (stronger hyp.)")]:
            r = q.evaluate(ns, roles, u, th, **kw)
            flag = "VIOLATES allowance" if r["V"] > r["allowance"] else ("> 5" if r["V"] > 5 else "")
            hflag = "hidden>0.01" if (th >= 1.1 and r["Vhid"] > 0.01) else ""
            pr(f"ns={ns} roles={roles} u={u} th/h={th} [{lab:>26}]: V={r['V']:+9.3f} allow={r['allowance']:7.2f} "
               f"Vhid={r['Vhid']:+9.3f} {flag} {hflag}")
    pr(f"# total time {time.time() - t0:.0f}s")
    (HERE / "out" / "q1_crosscheck.txt").write_text("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
