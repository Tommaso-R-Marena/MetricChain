#!/usr/bin/env python3
"""Addendum A17 (18): OCCUPANCY-AWARE REDUCTION of the evaluated terms that do not fit the band -- coordinator's module.

Why.  With workstream P8's constants the certified bracket of Lys12 at order 5 is limited by the band, not by the
constants: 0.14 of 0.19 nats (band 7) is the reduction of the 365 evaluated terms of order >= 3 whose sites do not
fit one window and of the 10 pairs beyond the band (P8_REPORT section 4.1).  Every such term is replaced, in the
floor, by its minimum over the sites that are given up (in the ceiling: maximum), and the rules so far choose WHICH
sites to keep by the sup-norm of what is lost (window_model.py: "pair" = P3's rule, "ext", "best").  But an anchored
term d_U vanishes as soon as one of its sites is at the anchor, so its reduced form min_{x_rest} d_U(x_keep, x_rest)
is non-zero only when ALL KEPT sites are off the anchor -- and by the first-order law of addendum A17 (16)
(Lemma A17.16) a reduction costs the bracket   beta E[ (max - min over the given-up sites)(x_keep) ]   under the
true ensemble.  For a peptide with mobile and nearly frozen side chains the kept sites should therefore be the ones
that are RARELY off the anchor.

Rule "occ".  For a term d_U that does not fit a window: among the maximal sub-tuples that fit a window (the same
candidates as rule "best") keep the one with the least MEAN, over a sample XG of the true ensemble, of
(max - min over the given-up sites)(x_keep); ties (e.g. no sampled state has all kept sites off the anchor) by the
sup-norm slack.  For a pair beyond the band: the ANCHORED split
    P(x_i, x_j) = P(x_i, x0_j) + [P(x0_i, x_j) - P(x0_i, x0_j)] + D(x_i, x_j),   D = 0 if x_i = x0_i or x_j = x0_j,
with D replaced by its minimum (maximum) over x_j as a function of x_i, or over x_i as a function of x_j; or P3's
split (column means and row minima of the rest, which charges a pair even when both sites are at the anchor) --
whichever of the three has the smallest sample mean of (max - min).
VALIDITY does not depend on the sample: every choice replaces a term by a pointwise minorant (floor) / majorant
(ceiling) of that term.  The sample only decides which valid model is built; it may be uncertified.
Checked against exhaustive enumeration by occ_reduction_test.py --enum.
"""
import itertools
import numpy as np


def build_window_models_occ(WindowModel, k, x0, c0, h, J, d, w, const, M, gs, g2, eta, XG, far_pairs="anchored", out=None):
    """as window_model.build_window_models, with rule "occ" for the terms that do not fit a window and (far_pairs =
    "anchored") the anchored split for the pairs beyond the band.  XG: (N, n) states of a sample of the true ensemble.
    Returns (lo, up, info); info additionally has 'first_order': the sample mean of the summed (max - min) of all
    reduced terms and far pairs, in kcal/mol (the first-order cost of the reductions, times beta, in nats).
    out (optional dict; added for slack_recovery.py, changes nothing else): receives the choices made --
    out["choice"][U] = (sample mean, sup slack, kept positions, minimum, maximum over the given-up sites) and
    out["fchoice"][(i, j)] = (A, B, kept site "i" or "j", (minimum, maximum of the rest over the other site))."""
    n = len(k); XG = np.atleast_2d(XG)

    def maximal_windows(U):
        sets = []
        for a in range(len(U)):
            V = tuple(p for p in range(len(U)) if U[a] <= U[p] <= U[a] + w)
            if not any(set(V) <= set(V2) for V2 in sets):
                sets = [V2 for V2 in sets if not set(V2) <= set(V)] + [V]
        return sets
    lo, up = WindowModel(k, w), WindowModel(k, w)
    info = dict(exact=0, reduced=0, far_pairs=0, reduced_sup=0.0, first_order=0.0, far_first_order=0.0,
                far_kind={"anchored, kept site i": 0, "anchored, kept site j": 0, "P3": 0})
    choice = {}; fchoice = {}
    for U, arr in d.items():                                  # the choices, once, common to floor and ceiling
        s = len(U)
        if s < 3 or U[-1] - U[0] <= w: continue
        best = None
        for keep in maximal_windows(U):
            other = tuple(p for p in range(s) if p not in keep)
            rlo, rup = arr.min(axis=other), arr.max(axis=other)
            sc = float((rup - rlo)[tuple(XG[:, U[p]] for p in keep)].mean()); sl = float((rup - rlo).max())
            if best is None or (sc, sl) < best[:2]: best = (sc, sl, keep, rlo, rup)
        choice[U] = best; info["first_order"] += best[0]; info["reduced_sup"] += best[1]; info["reduced"] += 1
    for i in range(n):
        for j in range(i + 1, n):
            if j - i <= w: continue
            P = J[(i, j)] + d.get((i, j), 0.0); info["far_pairs"] += 1
            if far_pairs != "anchored": continue
            A = P[:, x0[j]].copy(); B = P[x0[i], :] - P[x0[i], x0[j]]; D = P - A[:, None] - B[None, :]
            ci = (D.min(axis=1), D.max(axis=1)); cj = (D.min(axis=0), D.max(axis=0))
            b3 = P.mean(axis=0); R3 = P - b3[None, :]; c3 = (R3.min(axis=1), R3.max(axis=1))                    # P3's split, as a third candidate
            cand = [(float((ci[1] - ci[0])[XG[:, i]].mean()), float((ci[1] - ci[0]).max()), 0, (A, B, "i", ci)),
                    (float((cj[1] - cj[0])[XG[:, j]].mean()), float((cj[1] - cj[0]).max()), 1, (A, B, "j", cj)),
                    (float((c3[1] - c3[0])[XG[:, i]].mean()), float((c3[1] - c3[0]).max()), 2, (np.zeros(k[i]), b3, "i", c3))]
            best = min(cand, key=lambda t: t[:3]); fchoice[(i, j)] = best[3]
            info["far_first_order"] += best[0]; info["far_kind"][("anchored, kept site i", "anchored, kept site j", "P3")[best[2]]] += 1
    if out is not None:
        out["choice"] = choice; out["fchoice"] = fchoice
    for mdl, sense in ((lo, -1), (up, +1)):
        mdl.const = c0 + float(d[()]) + sense * const
        for i in range(n):
            mdl.one[i] = mdl.one[i] + h[i] + d.get((i,), np.zeros(k[i]))
            pen = np.full(k[i], sense * float(gs[i])); pen[x0[i]] = 0.0
            mdl.one[i] = mdl.one[i] + pen
        for i in range(n):
            for j in range(i + 1, n):
                P = J[(i, j)] + d.get((i, j), 0.0)
                if j - i <= w:
                    mdl.add_pair(i, j, P)
                elif far_pairs == "anchored":
                    A, B, which, c = fchoice[(i, j)]; red = c[0] if sense < 0 else c[1]
                    mdl.one[i] = mdl.one[i] + A + (red if which == "i" else 0.0)
                    mdl.one[j] = mdl.one[j] + B + (red if which == "j" else 0.0)
                else:
                    b = P.mean(axis=0); R = P - b[None, :]; a = R.min(axis=1) if sense < 0 else R.max(axis=1)      # P3's split
                    mdl.one[i] = mdl.one[i] + a; mdl.one[j] = mdl.one[j] + b
        for U, arr in d.items():
            s = len(U)
            if s < 3: continue
            if U[-1] - U[0] <= w:
                mdl.add_multi(U, arr)
                if sense < 0: info["exact"] += 1
                continue
            sc, sl, keep, rlo, rup = choice[U]; red = rlo if sense < 0 else rup; V = tuple(U[p] for p in keep)
            if len(V) >= 3: mdl.add_multi(V, red)
            elif len(V) == 2: mdl.add_pair(V[0], V[1], red)
            else: mdl.one[V[0]] = mdl.one[V[0]] + red
        off = [np.ones(k[i]) for i in range(n)]
        for i in range(n): off[i][x0[i]] = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                v = float(g2[i, j])
                if v != 0.0:
                    assert j - i <= w, "pair penalty outside the band"
                    mdl.add_pair(i, j, sense * v * np.outer(off[i], off[j]))
        if eta:
            for (i, j, kk), v in eta.items():
                mdl.add_multi((i, j, kk), sense * v * off[i][:, None, None] * off[j][None, :, None] * off[kk][None, None, :])
    return lo, up, info


def gibbs_sample(pw, G, c0, h, J, x0, k, beta, rng, nchain=8, nsweep=150, burn=30):
    """heat-bath Gibbs sampling of exp(-beta (f + g)) (uncertified; as in serine_helix_reach.py): the states of all chains
    after every sweep past the burn-in."""
    n = len(k); X = np.tile(np.array(x0, dtype=np.int64), (nchain, 1)); keep = []
    for sw in range(nsweep):
        for i in range(n):
            C = np.repeat(X, k[i], axis=0); C[:, i] = np.tile(np.arange(k[i]), nchain)
            E = (pw.f_energy(C, c0, h, J) + G.bulk_energy(C)).reshape(nchain, k[i])
            P = np.exp(-beta * (E - E.min(1, keepdims=True))); P /= P.sum(1, keepdims=True)
            u = rng.random(nchain); X[:, i] = np.minimum((P.cumsum(1) < u[:, None]).sum(1), k[i] - 1)
        if sw >= burn: keep.append(X.copy())
    return np.concatenate(keep, axis=0)
