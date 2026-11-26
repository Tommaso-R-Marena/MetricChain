#!/usr/bin/env python3
"""Addendum A17 (20): HELD-SITE PASSES FOR A WINDOW ANYWHERE ON THE CHAIN -- coordinator's module.

slack_recovery.py computes, for a band model, the exact joint law of one HELD site and the LAST w sites of the chain
(or, on the mirrored chain, the first w).  That serves every pair beyond the band and every triple that fits no
window as long as the chain has at most 2w sites.  This module does the same for a window of w consecutive sites
ANYWHERE to the right of the held site (and, mirrored, to its left), so that the recovery of Proposition A17.19
applies to chains of any length:

    law( x_i = b, x_s .. x_{s+w-1} )  proportional to  exp( F_b + B + I ),            t = s - 1 >= i,
      F_b  the message of the forward elimination of the sites 0 .. t with x_i held at b      (terms whose first site is <= t),
      B    the message of the backward elimination of the sites n-1 .. t+w+1                  (terms whose last site is >= t+w+1),
      I    the terms that lie inside the window                                               (first site >= s, last site <= s+w-1);
every term of a band model (max site - min site <= w) is in exactly one of the three.  The backward messages are the
forward messages of the mirrored chain; they are computed once per model.

Routing of an item (a table on sites U that fit no window): first the routes of slack_recovery.route (held end site,
the other sites in the last / first w sites), so that chains of at most 2w sites are treated exactly as before; else
the first site is held if the other sites span at most w - 1, or the last site if the others do ("fwd" / "rev", the
preferred one where both exist).  Items with the same direction, held site and window form one GROUP and are treated
exactly together; windows are shared greedily among the items of a held site.  Items without a route are left out,
which keeps every bound valid.  The statistics and the bounds are those of slack_recovery (Proposition A17.19).
Checked against exhaustive enumeration by first_order_recovery.py --enum (band 2 on five residues: items through
windows inside the chain; every group mean against the enumerated one).
"""
import numpy as np
import slack_recovery as SR


def forward_messages(model, scale):
    """[m_0, ..., m_{n-w-1}]: m_t = log of the sum over the sites 0..t of exp(scale * terms attached to the sites <= t),
    an array over the sites t+1 .. t+w."""
    msgs = []; msg = None
    for t in range(model.n - model.w):
        msg = SR._eliminate(model, t, msg, scale); msgs.append(msg)
    return msgs


def inside_terms(model, s, scale):
    """scale * (all terms of the model whose sites lie in s .. s+w-1), as an array over those w sites."""
    w, k = model.w, model.k; hi = s + w - 1; A = np.zeros([k[u] for u in range(s, hi + 1)])
    for u in range(s, hi + 1):
        sh = [1] * w; sh[u - s] = k[u]; A += scale * np.asarray(model.one[u]).reshape(sh)
    for (i, j), tab in model.pair.items():
        if s <= i and j <= hi:
            sh = [1] * w; sh[i - s] = k[i]; sh[j - s] = k[j]; A += scale * np.asarray(tab).reshape(sh)
    for U, tab in getattr(model, "multi", {}).items():
        if s <= U[0] and U[-1] <= hi:
            sh = [1] * w
            for u in U: sh[u - s] = k[u]
            A += scale * np.asarray(tab).reshape(sh)
    return A


def assign_routes(items, n, w):
    """per item: (direction, held site, window start s) in the coordinates of the direction's chain ('rev': mirrored), or None."""
    out = [None] * len(items); pend = {"fwd": {}, "rev": {}}
    for q, it in enumerate(items):
        U = it[0]; pref = it[2] if len(it) > 2 else None
        r = SR.route(U, n, w, pref)
        if r is not None:                                               # the routes of slack_recovery: the last (first) w sites
            out[q] = (r, U[0] if r == "fwd" else n - 1 - U[-1], n - w); continue
        ok = [d for d, c in (("fwd", U[-1] - U[1] <= w - 1), ("rev", U[-2] - U[0] <= w - 1)) if c]
        if not ok: continue
        d = pref if pref in ok else ok[0]
        V = U if d == "fwd" else tuple(n - 1 - u for u in reversed(U))
        pend[d].setdefault(V[0], []).append((V[1], V[-1], q))
    for d, by_held in pend.items():
        for held, lst in by_held.items():
            cur = None
            for first, last, q in sorted(lst):                          # greedy: one window serves the following items as long as they fit
                if cur is None or last > cur + w - 1:
                    cur = min(first, n - w)
                out[q] = (d, held, cur)
    return out


def _stats_dir(model, msgs, bwd_msgs, classes, beta, lnZ):
    """classes: list of (plus, minus); items (U, tab, s) in the coordinates of `model`; U[0] is held, U[1:] inside s..s+w-1.
    msgs: forward messages of `model`; bwd_msgs: forward messages of its mirror.  Returns a list (one entry per cumulative
    union of the classes) of {(held site, s): statistics}."""
    n, w, k = model.n, model.w, model.k; lnZ0 = lnZ + beta * model.const; scale = -beta
    out = [dict() for _ in classes]; terms = {}; inside = {}; bwd = {}
    held_sites = sorted({it[0][0] for pl, mi in classes for it in list(pl) + list(mi)})

    def backward(t):                                                    # over the sites t+1 .. t+w, original order
        if t not in bwd:
            q = n - 2 - w - t
            bwd[t] = 0.0 if q < 0 else np.transpose(bwd_msgs[q], axes=tuple(range(w - 1, -1, -1)))
        return bwd[t]
    for i in held_sites:
        starts = sorted({it[2] for pl, mi in classes for it in list(pl) + list(mi) if it[0][0] == i})
        T = {}
        for s in starts:
            def by_axes(items):
                acc = {}
                for U, tab, s_ in items:
                    if U[0] == i and s_ == s:
                        ax = tuple(u - s for u in U[1:]); acc[ax] = (acc[ax] + tab) if ax in acc else np.array(tab, dtype=float)
                return acc
            Ts = [(by_axes(pl), by_axes(mi)) for pl, mi in classes]
            used = sorted({a_ for tp, tm in Ts for ax in list(tp) + list(tm) for a_ in ax}); posn = {a_: q for q, a_ in enumerate(used)}
            T[s] = (Ts, used, posn, tuple(a_ for a_ in range(w) if a_ not in posn), [k[s + a_] for a_ in used])
            if s not in inside: inside[s] = inside_terms(model, s, scale)
        st = {s: [dict(a=0.0, e=0.0, b=0.0, c=0.0, cp=0.0, mass=0.0) for _ in classes] for s in starts}
        Ai = model._A(i, msgs[i - 1] if i > 0 else None, scale)         # over the sites i .. i+w
        for b in range(k[i]):
            mb = Ai[b]; cur = i
            for s in starts:
                while cur < s - 1:
                    cur += 1
                    if cur not in terms: terms[cur] = model._A(cur, None, scale)
                    A = terms[cur] + mb[..., None]; mx = A.max(axis=0); A -= mx[None]; np.exp(A, out=A)
                    mb = mx + np.log(A.sum(axis=0))
                P = np.exp(mb + backward(s - 1) + inside[s] - lnZ0); mass = float(P.sum())
                Ts, used, posn, drop, shape = T[s]
                if drop: P = P.sum(axis=drop)
                S = [np.zeros(shape), np.zeros(shape)]; seen = False
                for q, accs in enumerate(Ts):
                    for acc, Sx in zip(accs, S):
                        for ax, tab in acc.items():
                            sh = [1] * len(used)
                            for a_, s_ in zip(ax, tab.shape[1:]): sh[posn[a_]] = s_
                            Sx += tab[b].reshape(sh)
                    seen = seen or bool(accs[0] or accs[1])
                    if not seen: continue
                    Ep = np.exp(beta * S[0]); r = st[s][q]; r["mass"] += mass
                    r["a"] += float((P * S[0]).sum()); r["e"] += float((P * (Ep - 1.0)).sum()); r["b"] += float((P * S[1]).sum())
                    r["c"] += float((P * S[1] * Ep).sum()); r["cp"] += float((P * np.expm1(beta * S[1]) * Ep).sum())
        for s in starts:
            for q in range(len(classes)):
                if st[s][q]["mass"] > 0.0: out[q][(i, s)] = st[s][q]
    return out


def group_stats(WindowModel, model, classes, beta, lnZ=None):
    """Exact group means under exp(-beta model)/Z, for chains of any length.  classes: list of (plus, minus), lists of
    items (U sorted tuple of >= 2 sites, tab >= 0 array over U[, preferred route]).  Returns (stats, routes): stats is
    a list with one entry per CUMULATIVE union of the classes, each mapping (direction, held site, window start) to
    dict(a, e, b, c, cp, mass) as in slack_recovery.group_stats (feed it to slack_recovery.bounds); routes[c] =
    (routes of the plus items, routes of the minus items) of class c, None where an item has no route."""
    n, w = model.n, model.w
    if lnZ is None: lnZ = model.lnZ(beta)
    routes = [(assign_routes(pl, n, w), assign_routes(mi, n, w)) for pl, mi in classes]
    rmodel = SR.reverse_model(WindowModel, model)
    msgs = forward_messages(model, -beta); rmsgs = forward_messages(rmodel, -beta)
    out = [dict() for _ in classes]
    for d, mdl, fm, bm in (("fwd", model, msgs, rmsgs), ("rev", rmodel, rmsgs, msgs)):
        cls = []
        for (pl, mi), (rp, rm_) in zip(classes, routes):
            sel = []
            for items, rts in ((pl, rp), (mi, rm_)):
                lst = []
                for it, rt in zip(items, rts):
                    if rt is not None and rt[0] == d:
                        U, tab = (it[0], it[1]) if d == "fwd" else SR._mirror(it, n)
                        assert U[0] == rt[1] and rt[2] <= U[1] and U[-1] <= rt[2] + w - 1 and rt[2] <= n - w and rt[2] >= U[0] + 1
                        lst.append((U, tab, rt[2]))
                sel.append(lst)
            cls.append(tuple(sel))
        if any(pl or mi for pl, mi in cls):
            for q, g in enumerate(_stats_dir(mdl, fm, bm, cls, beta, lnZ)):
                for (held, s), stt in g.items():
                    out[q][(d, held if d == "fwd" else n - 1 - held, s)] = stt
    return out, routes
