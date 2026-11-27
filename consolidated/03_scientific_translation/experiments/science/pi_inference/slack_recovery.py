#!/usr/bin/env python3
"""Addendum A17 (19): RECOVERY of the KNOWN slack of a sandwich -- coordinator's module.

A certified sandwich m_- <= E <= m_+ of band models gives  ln Z(m_+) <= ln Z(E) <= ln Z(m_-),  and with workstream
P9's state-resolved tables the gap D = ln Z(m_-) - ln Z(m_+) is, to a few per cent, what the BAND gives up: the pairs
beyond the band and the evaluated terms that do not fit a window are replaced by a minimum (floor) or a maximum
(ceiling) over the sites that are given up.  That slack is not unknown -- it is a table: for a far pair,
(model's part) - P(x_i, x_j) is a function of two sites that the model cannot hold but anyone can evaluate.

Proposition (A17.19).  Let s_+ = sum_g S+_g and s_- = sum_g S-_g be sums of non-negative functions with
m_+ - E >= s_+ and E - m_- >= s_- pointwise; <.> is the mean under exp(-beta m_+)/Z(m_+), the CEILING model.  Then
  (LJ)   ln Z(E)  >=  ln Z(m_+) + beta sum_g <S+_g>
  (LP)   ln Z(E)  >=  ln Z(m_+) + ln( 1 + sum_g < e^{beta S+_g} - 1 > )
  (UE)   ln Z(E)  <=  u*,   the limit of   u_0 = ln Z(m_-),   u_{t+1} = ln Z(m_-) - beta C exp( ln Z(m_+) - u_t ),
                       C = sum_g < S-_g e^{beta S+_g} >     (every u_t is an upper bound).
  (UP)   ln Z(E)  <=  v*,   the limit of   v_0 = ln Z(m_-),   v_{t+1} = ln Z(m_-) - ln( 1 + C' exp( ln Z(m_+) - v_t ) ),
                       C' = sum_g < (e^{beta S-_g} - 1) e^{beta S+_g} >     (every v_t is an upper bound).
Proof.  Z(E)/Z(m_+) = <e^{beta (m_+ - E)}> >= <e^{beta s_+}>; Jensen gives (LJ); prod_g (1 + y_g) >= 1 + sum_g y_g for
y_g = e^{beta S+_g} - 1 >= 0 gives (LP).  For (UE): Z(m_-) = Z(E) <e^{beta (E - m_-)}>_E >= Z(E) exp(beta <s_->_E) by Jensen
under the TRUE ensemble, and for every g, since S-_g >= 0, e^{-beta E} >= e^{-beta m_+} e^{beta s_+} >= e^{-beta m_+} e^{beta S+_g}:
   <S-_g>_E = sum_x S-_g e^{-beta E} / Z(E)  >=  Z(m_+) <S-_g e^{beta S+_g}> / Z(E)  >=  <S-_g e^{beta S+_g}> exp( ln Z(m_+) - u )
for every upper bound u of ln Z(E).  For (UP) the same change of measure is applied to e^{beta S-_g} - 1 >= 0 after
Z(m_-)/Z(E) = <e^{beta (E - m_-)}>_E >= <e^{beta s_-}>_E >= 1 + sum_g <e^{beta S-_g} - 1>_E  (the product inequality again):
no Jensen step, so a slack that is rare but not small is recovered beyond first order within each group.  (LJ) and
(UE) are the Gibbs-Bogoliubov inequality in its two directions; the step that is not a textbook line is the change of
measure, which replaces a mean under the true ensemble by a mean under the ceiling model.  Everything needs means
under ONE model.

What must be computed: for tables t on site sets U that do NOT fit a window, the law of t(x_U) under a band model.
This module does it exactly for every U whose sites, except the first, lie in the last w sites of the chain ("fwd"),
or, except the last, in the first w sites ("rev", on the mirrored chain): the transfer matrix is run with that one
site held at each of its states in turn and the joint law of the last w sites is read from the final array.  All
items that share the held site form one GROUP g; S_g is a function of (held site, last window), so < phi(S_g) > is
exact for every phi.  For a chain of at most 2w sites this covers every far pair and every triple that does not fit
a window.  Items without a route are left out -- any subset of non-negative slack terms is a valid s.

Functions: clamped_last_windows, reverse_model, route, group_stats (the exact group means), items_value (pointwise
sum), solve_upper (the iteration of (UE)), bounds (the corrected bracket: two lower and two upper ends).  Checked against exhaustive enumeration by first_order_recovery.py --enum.
"""
import numpy as np


def _eliminate(model, t, msg, scale):
    A = model._A(t, msg, scale); mx = A.max(axis=0)
    return mx + np.log(np.exp(A - mx[None]).sum(axis=0))


def clamped_last_windows(model, scale, i, terms=None):
    """for b = 0 .. k_i - 1: (b, Q_b), Q_b = log of the sum over all sites but i and the last w of exp(scale * (energy -
    const)) with x_i = b, as an array over the sites n-w .. n-1.  Requires i < n - w.  The eliminations before site i
    and the array at site i are shared by all b.  terms: optional dict, filled here, that keeps the arrays of the terms
    attached to the sites i+1 .. n-w-1 (one array over w + 1 sites each), so that an elimination with a held site
    costs one addition instead of one per table; the caller may pass the same dict for every held site of a model."""
    n, w = model.n, model.w
    assert 0 <= i < n - w
    terms = {} if terms is None else terms
    msg = None
    for t in range(i):
        msg = _eliminate(model, t, msg, scale)
    Ai = model._A(i, msg, scale)                                   # over the sites i .. i + w
    tail = None                                                    # the terms attached to the last w sites
    for t in range(n - w, n):
        At = model._A(t, None, scale); At = At.reshape((1,) * (t - (n - w)) + At.shape)
        tail = At if tail is None else tail + At
    for t in range(i + 1, n - w):
        if t not in terms:
            terms[t] = model._A(t, None, scale)
    for b in range(model.k[i]):
        mb = Ai[b]
        for t in range(i + 1, n - w):
            A = terms[t] + mb[..., None]; mx = A.max(axis=0); A -= mx[None]; np.exp(A, out=A)
            mb = mx + np.log(A.sum(axis=0))
        yield b, mb + tail


def reverse_model(WindowModel, mdl):
    """the same energy function on the mirrored chain (site i -> n - 1 - i)."""
    n = mdl.n; r = WindowModel(list(mdl.k)[::-1], mdl.w); r.const = mdl.const
    for i in range(n):
        r.one[n - 1 - i] = np.array(mdl.one[i], dtype=float)
    for (i, j), tab in mdl.pair.items():
        r.add_pair(n - 1 - j, n - 1 - i, np.asarray(tab).T)
    for U, tab in mdl.multi.items():
        r.add_multi(tuple(n - 1 - u for u in reversed(U)), np.transpose(tab, axes=tuple(range(len(U) - 1, -1, -1))))
    return r


def route(U, n, w, pref=None):
    """'fwd', 'rev' or None for a sorted tuple of sites U (len >= 2): which site can be held ('fwd': the first, the
    others in the last w sites; 'rev': the last, the others in the first w sites).  pref: the route to take when both
    exist.  The choice matters for tightness, not for validity: items whose slack occurs at the same states (e.g. all
    far pairs whose reduction keeps the same site) are treated exactly TOGETHER only if they share the held site."""
    ok = [r for r, c in (("fwd", U[0] < n - w and U[1] >= n - w), ("rev", U[-1] >= w and U[-2] <= w - 1)) if c]
    if not ok:
        return None
    return pref if pref in ok else ok[0]


def item_route(it, n, w):
    return route(it[0], n, w, it[2] if len(it) > 2 else None)


def _mirror(item, n):
    U, tab = item[0], item[1]
    return tuple(n - 1 - u for u in reversed(U)), np.transpose(tab, axes=tuple(range(len(U) - 1, -1, -1)))


def _stats_fwd(model, classes, beta, lnZ):
    """classes: list of (plus, minus), lists of items (U, tab) with route 'fwd' in `model`.  Returns a list, one entry per
    CUMULATIVE union of the classes (the first; the first two; ...), of {held site i: dict(a = <S+>, e = <exp(beta S+)
    - 1>, b = <S->, c = <S- exp(beta S+)>, cp = <(exp(beta S-) - 1) exp(beta S+)>, mass = total mass of the clamped
    runs)}.  One pass over the held sites
    serves all; the law is reduced to the sites the group's items use before anything is summed."""
    n, w = model.n, model.w; lnZ0 = lnZ + beta * model.const; terms = {}
    sites = sorted({it[0][0] for pl, mi in classes for it in list(pl) + list(mi)}); out = [dict() for _ in classes]

    def by_axes(items, i):
        """the items held at site i, summed by the axes of their other sites: dict axes -> table over (x_i, those axes)."""
        acc = {}
        for it in items:
            U, tab = it[0], it[1]
            if U[0] == i:
                ax = tuple(u - (n - w) for u in U[1:])
                acc[ax] = (acc[ax] + tab) if ax in acc else np.array(tab, dtype=float)
        return acc
    for i in sites:
        T = [(by_axes(pl, i), by_axes(mi, i)) for pl, mi in classes]
        used = sorted({a_ for tp, tm in T for ax in list(tp) + list(tm) for a_ in ax}); posn = {a_: q for q, a_ in enumerate(used)}
        drop = tuple(a_ for a_ in range(w) if a_ not in posn); shape = [model.k[n - w + a_] for a_ in used]
        st = [dict(a=0.0, e=0.0, b=0.0, c=0.0, cp=0.0, mass=0.0) for _ in classes]
        for b, Q in clamped_last_windows(model, -beta, i, terms):
            P = np.exp(Q - lnZ0); mass = float(P.sum())
            if drop: P = P.sum(axis=drop)                               # the law of (x_i = b, the sites the items use)
            S = [np.zeros(shape), np.zeros(shape)]
            for q, accs in enumerate(T):
                for acc, Sx in zip(accs, S):
                    for ax, tab in acc.items():
                        sh = [1] * len(used)
                        for a_, s_ in zip(ax, tab.shape[1:]): sh[posn[a_]] = s_
                        Sx += tab[b].reshape(sh)
                if not (accs[0] or accs[1]) and not any(tp or tm for tp, tm in T[:q]):
                    continue                                            # nothing yet for this group
                Ep = np.exp(beta * S[0]); r = st[q]; r["mass"] += mass
                r["a"] += float((P * S[0]).sum()); r["e"] += float((P * (Ep - 1.0)).sum()); r["b"] += float((P * S[1]).sum()); r["c"] += float((P * S[1] * Ep).sum())
                r["cp"] += float((P * np.expm1(beta * S[1]) * Ep).sum())
        for q in range(len(classes)):
            if st[q]["mass"] > 0.0:
                out[q][i] = st[q]
    return out


def group_stats(WindowModel, model, classes, beta, lnZ=None):
    """Exact group means under exp(-beta model)/Z.  classes: list of (plus, minus), lists of items (U sorted tuple of
    >= 2 sites, tab >= 0 array over U[, preferred route]); items without a route are ignored.  Returns a list with one entry per CUMULATIVE
    union of the classes; each entry maps (direction, held site) to dict(a = <S+_g>, e = <exp(beta S+_g) - 1>,
    b = <S-_g>, c = <S-_g exp(beta S+_g)>, cp = <(exp(beta S-_g) - 1) exp(beta S+_g)>, mass = total mass of the clamped
    runs, which must be one), S+-_g the sum of the plus / minus items of the group."""
    n, w = model.n, model.w
    if lnZ is None:
        lnZ = model.lnZ(beta)
    out = [dict() for _ in classes]
    fwd = [([it for it in pl if item_route(it, n, w) == "fwd"], [it for it in mi if item_route(it, n, w) == "fwd"]) for pl, mi in classes]
    if any(pl or mi for pl, mi in fwd):
        for q, g in enumerate(_stats_fwd(model, fwd, beta, lnZ)):
            for i, st in g.items():
                out[q][("fwd", i)] = st
    rev = [([_mirror(it, n) for it in pl if item_route(it, n, w) == "rev"], [_mirror(it, n) for it in mi if item_route(it, n, w) == "rev"]) for pl, mi in classes]
    if any(pl or mi for pl, mi in rev):
        rmodel = reverse_model(WindowModel, model)
        for q, g in enumerate(_stats_fwd(rmodel, rev, beta, lnZ)):
            for i, st in g.items():
                out[q][("rev", n - 1 - i)] = st
    return out


def items_value(items, X):
    """sum of the items at the rows of X."""
    X = np.atleast_2d(X); out = np.zeros(len(X))
    for it in items:
        out += it[1][tuple(X[:, u] for u in it[0])]
    return out


def solve_upper(lnZ_lo_model, lnZ_up_model, beta_C, iters=60):
    """(UE): lnZ_lo_model = ln Z(m_-), lnZ_up_model = ln Z(m_+), beta_C = beta sum_g <S-_g e^{beta S+_g}>.  Returns (u_1, u*)."""
    u = lnZ_lo_model; u1 = None
    for t in range(iters):
        u = lnZ_lo_model - beta_C * np.exp(lnZ_up_model - u)
        if t == 0:
            u1 = u
    return float(u1), float(u)


def bounds(lnZ_lo_model, lnZ_up_model, groups, beta, safe=1e-9):
    """the corrected bracket from the group statistics: dict(LJ, LP, UE, UP) -- two lower and two upper ends, all valid."""
    f = 1.0 - safe
    LJ = lnZ_up_model + f * beta * sum(g["a"] for g in groups.values())
    LP = lnZ_up_model + np.log1p(f * sum(g["e"] for g in groups.values()))
    u1, UE = solve_upper(lnZ_lo_model, lnZ_up_model, f * beta * sum(g["c"] for g in groups.values()))
    Cp = f * sum(g["cp"] for g in groups.values()); v = lnZ_lo_model
    for _ in range(60):
        v = lnZ_lo_model - np.log1p(Cp * np.exp(lnZ_up_model - v))
    return dict(LJ=float(LJ), LP=float(LP), UE=float(UE), UP=float(v))
