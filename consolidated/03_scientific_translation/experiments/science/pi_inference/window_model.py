#!/usr/bin/env python3
"""Addendum A17 (16), part B: EXACT IN-WINDOW EVALUATED TERMS -- coordinator's module (open problem D9(b)).

Workstream P3's sandwich replaces every evaluated term d_U of order 3..m-1 by a minorant / majorant that depends on
two in-band sites (pwmodel.build_band_models), because its model class is pairwise.  The transfer matrix it uses,
however, eliminates site i from an ARRAY over the sites i..i+w, so any function of sites that fit into one window
(max U - min U <= w) can be added to that array at no extra cost -- workstream P6 used this for its triple penalty.
Here every evaluated term whose sites fit into a window is kept EXACT, in the floor and in the ceiling alike; a term
that does not fit is reduced either as P3 does (to a pair) or to a maximal sub-tuple that fits a window (two rules:
"ext", pointwise at least as tight as P3's; "best", least sup-norm slack).  The penalties are unchanged (P3's site form, P6's banded pair and
triple forms), so the validity argument is unchanged: m_-/+ = f + [exact or minorised/majorised I_{m-1} g] -/+ penalty
and |g - I_{m-1} g| <= penalty.

What is whose: P3 -- BandModel, the reductions (copied below for the terms outside the window, marked); P6 -- the
penalty forms; mine -- WindowModel, build_window_models, diff_window, and triple_form_two_windows (P6's triple form with
a separate, narrower window for the triples).  Checked against exhaustive enumeration by window_model_check.py.
"""
import itertools
import numpy as np


def make(pw):
    """returns (WindowModel, build_window_models, diff_window) bound to workstream P3's pwmodel module `pw`."""

    class WindowModel(pw.BandModel):
        """P3's BandModel plus tables multi[U] on sets U of >= 3 sites with max U - min U <= w, attached to site min U."""

        def __init__(self, k, w):
            super().__init__(k, w)
            self.multi = {}

        def add_multi(self, U, tab):
            U = tuple(U)
            assert len(U) >= 3 and all(U[a] < U[a + 1] for a in range(len(U) - 1)) and U[-1] - U[0] <= self.w
            assert tuple(tab.shape) == tuple(self.k[u] for u in U)
            self.multi[U] = self.multi.get(U, 0.0) + tab

        def energy(self, st):
            st = np.atleast_2d(st)
            e = super().energy(st)
            for U, tab in self.multi.items():
                e += tab[tuple(st[:, u] for u in U)]
            return e

        def _A(self, i, msg, scale):
            A = super()._A(i, msg, scale)
            nax = A.ndim
            for U, tab in self.multi.items():
                if U[0] == i:
                    sh = [1] * nax
                    for u in U:
                        sh[u - i] = self.k[u]
                    A = A + scale * tab.reshape(sh)
            return A

    def build_window_models(k, x0, c0, h, J, d, w, const, M, gs, g2, eta=None, reduce="pair"):
        """floor and ceiling with exact in-window evaluated terms.  gs: site penalties; g2: in-band pair penalties
        (must vanish outside the band); eta: dict (i, j, k) -> in-window triple penalty, or None.  const: the constant
        allowance (P6's EPS_G).  A term that does not fit a window is replaced by its minimum (floor) / maximum
        (ceiling) over some of its sites:
          reduce = "pair": P3's rule -- over all but two in-band sites (the in-band pair of least sup-norm slack), or
                           over all but the first site when no pair is in band;
          reduce = "ext":  P3's choice, extended to a maximal sub-tuple that fits a window and contains it (the one of
                           least sup-norm slack).  A minimum over fewer sites of the same array is pointwise larger, so
                           this floor is pointwise >= P3's and this ceiling pointwise <= P3's (checked state by state);
          reduce = "best": the maximal sub-tuple that fits a window with the least sup-norm slack, whether or not it
                           contains P3's pair.  Per term its sup-norm slack is at most that of "ext", hence of P3's
                           rule; it is NOT pointwise tighter than P3's rule (a first version of this docstring said
                           so; the enumeration check found 22 725 states to the contrary).
        The maximal sub-tuples that fit a window are the sets {u in U : U[a] <= u <= U[a] + w}, a = 0, 1, ..., that
        are not contained in another such set.
        The default is P3's rule: on the twelve-residue serine helix the two others narrow the bracket by less than
        2 % (window_model_rules.log) -- the slack of a term that does not fit a window is its dependence on the far
        site, which every rule gives up.
        Returns (lo, up, info) with info = numbers of exact and of reduced terms and the sup-norm slack of the
        reduced ones."""
        assert reduce in ("best", "ext", "pair")

        def maximal_windows(U):
            sets = []
            for a in range(len(U)):
                V = tuple(p for p in range(len(U)) if U[a] <= U[p] <= U[a] + w)
                if not any(set(V) <= set(V2) for V2 in sets):
                    sets = [V2 for V2 in sets if not set(V2) <= set(V)] + [V]
            return sets

        def p3_choice(U, arr, sense):
            """positions kept by P3's rule: the in-band pair of least sup-norm slack, else the first site."""
            s_ = len(U); best = None
            for pa, pb in itertools.combinations(range(s_), 2):
                if U[pb] - U[pa] > w:
                    continue
                other = tuple(p for p in range(s_) if p not in (pa, pb))
                red = arr.min(axis=other) if sense < 0 else arr.max(axis=other)
                sl = float(np.abs(arr - np.expand_dims(red, other)).max())
                if best is None or sl < best[0]:
                    best = (sl, (pa, pb))
            return best[1] if best is not None else (0,)
        n = len(k)
        lo, up = WindowModel(k, w), WindowModel(k, w)
        info = dict(exact=0, reduced=0, far_pairs=0, reduced_sup=0.0)
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
                    else:                                             # P3's treatment of pairs beyond the band
                        a, b = pw._additive_split(P, sense)
                        mdl.one[i] = mdl.one[i] + a
                        mdl.one[j] = mdl.one[j] + b
                        if sense < 0: info["far_pairs"] += 1
            for U, arr in d.items():
                s = len(U)
                if s < 3:
                    continue
                if U[-1] - U[0] <= w:                                 # NEW: exact, identical in floor and ceiling
                    mdl.add_multi(U, arr)
                    if sense < 0: info["exact"] += 1
                    continue
                if reduce in ("best", "ext"):                          # NEW: a maximal sub-tuple that fits a window
                    must = set(p3_choice(U, arr, sense)) if reduce == "ext" else set()
                    best = None
                    for keep in maximal_windows(U):
                        if not must <= set(keep):
                            continue
                        other = tuple(p for p in range(s) if p not in keep)
                        red = arr.min(axis=other) if sense < 0 else arr.max(axis=other)
                        sl = float(np.abs(arr - np.expand_dims(red, other)).max())
                        if best is None or sl < best[0]:
                            best = (sl, keep, red)
                    sl, keep, red = best
                    V = tuple(U[p] for p in keep)
                    if len(V) >= 3:
                        mdl.add_multi(V, red)
                    elif len(V) == 2:
                        mdl.add_pair(V[0], V[1], red)
                    else:
                        mdl.one[V[0]] = mdl.one[V[0]] + red
                    if sense < 0:
                        info["reduced"] += 1; info["reduced_sup"] += sl
                    continue
                # ---- P3's reduction (pwmodel.build_band_models), unchanged, for the terms that do not fit a window
                best = None
                for pa, pb in itertools.combinations(range(s), 2):
                    if U[pb] - U[pa] > w:
                        continue
                    other = tuple(p for p in range(s) if p not in (pa, pb))
                    red = arr.min(axis=other) if sense < 0 else arr.max(axis=other)
                    sl = float(np.abs(arr - np.expand_dims(red, other)).max())
                    if best is None or sl < best[0]:
                        best = (sl, pa, pb, red)
                if best is not None:
                    mdl.add_pair(U[best[1]], U[best[2]], best[3])
                    sl = best[0]
                else:
                    other = tuple(range(1, s))
                    red = arr.min(axis=other) if sense < 0 else arr.max(axis=other)
                    mdl.one[U[0]] = mdl.one[U[0]] + red
                    sl = float(np.abs(arr - np.expand_dims(red, other)).max())
                if sense < 0:
                    info["reduced"] += 1; info["reduced_sup"] += sl
            # ---- penalties: P6's in-band pair part and in-window triple part
            off = [np.ones(k[i]) for i in range(n)]
            for i in range(n):
                off[i][x0[i]] = 0.0
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

    def diff_window(lo, up):
        """the model m_+ - m_- (for the sandwich sampler)."""
        dm = WindowModel(lo.k, lo.w)
        dm.const = up.const - lo.const
        dm.one = [up.one[i] - lo.one[i] for i in range(lo.n)]
        for key in set(lo.pair) | set(up.pair):
            dm.pair[key] = up.pair.get(key, 0.0) - lo.pair.get(key, 0.0)
        for key in set(lo.multi) | set(up.multi):
            t = up.multi.get(key, 0.0) - lo.multi.get(key, 0.0)
            if np.any(t != 0.0):
                dm.multi[key] = t
        return dm

    return WindowModel, build_window_models, diff_window


def triple_form_two_windows(window_triples, RND, n, m, w, w3, Gp, H, psi1, psi2, absG, absH):
    """Workstream P6's banded triple form (p6_09_triple.triple_form; its Lemma A') with TWO windows: a triple with
    max - min <= w3 is charged as a triple; every other triple through its three pairs in thirds
    (s_i s_j s_k <= (s_i s_j + s_i s_k + s_j s_k) / 3); a pair with |a - b| <= w is in band, every other pair goes in halves
    to its two sites.  P6's function is the case w3 = w (its lemma holds for any set of triples declared "in window").
    Needed when the band w of the model is wide (two-state sites) and the closed-form triple sums H are affordable only
    for near triples.  H: dict (i, j, k) -> raw triple sum, at least for the triples within w3.
    Returns (site part gs, in-band pair part g2, triple part eta), as P6's function."""
    import math
    assert w3 <= w
    c3 = math.comb(m, 3)
    eta = {}
    insum = np.zeros((n, n)); nin = np.zeros((n, n))
    for (i, j, kk) in window_triples(n, w3):
        v = H[(i, j, kk)]
        eta[(i, j, kk)] = (max(v, 0.0) + absH) / c3 * RND
        for a, b in ((i, j), (i, kk), (j, kk)):
            insum[a, b] += v; insum[b, a] += v; nin[a, b] += 1; nin[b, a] += 1
    gs = psi1.copy(); g2 = np.zeros((n, n))
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            rho = (max((m - 2) * max(Gp[a, b], 0.0) - insum[a, b], 0.0) + (m - 2) * absG + nin[a, b] * absH) / (3.0 * c3) * RND
            if abs(a - b) <= w:
                g2[a, b] = rho + psi2[a, b]
            else:
                gs[a] += 0.5 * (rho + psi2[a, b])
    return gs, g2, eta
