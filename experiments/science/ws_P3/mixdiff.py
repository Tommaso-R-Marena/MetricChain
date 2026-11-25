"""
Exact mixed differences on fully enumerated product grids (small instances only; this is the
ENUMERATION side, used to measure what the analysis must bound).

g: array of shape (k_1, ..., k_n), axis i = site i.
Delta_T g (x; y_T) = sum_{S subset T} (-1)^{|T|-|S|} g(x with x_S replaced by y_S).
"""
import itertools
import numpy as np


def pairdiff(G, axis):
    k = G.shape[axis]
    ia, ib = np.triu_indices(k, 1)
    return np.take(G, ia, axis=axis) - np.take(G, ib, axis=axis)


def mixed_all(g, T):
    """array of all mixed differences over the sites T: all unordered state pairs at each site of T,
    all states of the other sites.  Shape: (pairs_T1, ..., pairs_Tm, k_other...)."""
    G = np.moveaxis(g, T, range(len(T)))
    for ax in range(len(T)):
        G = pairdiff(G, ax)
    return G


def mixed_max(g, T):
    """sup over base points and state pairs of |Delta_T g|  (the class constant c_T)."""
    for i in T:
        if g.shape[i] < 2:
            return 0.0
    return float(np.abs(mixed_all(g, T)).max())


def mixed_minmax(g, T):
    """(min, max) of the signed mixed difference with the convention 'ordered pairs': because every
    unordered pair is taken once, the sign is not meaningful; use anchored_term for signed data."""
    D = mixed_all(g, T)
    return float(D.min()), float(D.max())


def anchored_term(g, x0, T):
    """d_T(x_T) = Delta_T g at the anchor x0 (the other sites at x0), as an array over the states of
    the sites T (zero whenever some x_i = x0_i).  Signed."""
    idx = list(x0)
    for i in T:
        idx[i] = slice(None)
    sub = g[tuple(idx)]                       # axes ordered as sorted(T)
    order = sorted(T)
    out = sub.copy()
    for a, i in enumerate(order):
        ref = np.take(out, [x0[i]], axis=a)
        out = out - ref
    return out


def mixed_at_context(g, x0, T):
    """max over state pairs of the sites T of |Delta_T g| with the OTHER sites fixed at x0."""
    idx = list(x0)
    for i in T:
        idx[i] = slice(None)
    sub = g[tuple(idx)]
    for a in range(len(T)):
        if sub.shape[a] < 2:
            return 0.0
        sub = pairdiff(sub, a)
    return float(np.abs(sub).max())


def anchored_interp(g, x0, order):
    """anchored (cut-HDMR) expansion of g at x0 truncated at `order`: sum_{|T| <= order} d_T."""
    n = g.ndim
    out = np.zeros(g.shape)
    for m in range(order + 1):
        for T in itertools.combinations(range(n), m):
            d = anchored_term(g, x0, T)
            sh = [1] * n
            for a, i in enumerate(sorted(T)):
                sh[i] = g.shape[i]
            out = out + d.reshape(sh)
    return out
