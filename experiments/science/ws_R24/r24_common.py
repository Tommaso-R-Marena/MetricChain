#!/usr/bin/env python3
"""Workstream R24 -- helpers written by the referee (no line taken from the coordinator's scripts except the
frame-capture trick, which is the only way to obtain THEIR objects without rebuilding them).

  factors_of(model)            (const, [(scope, table)]) of a BandModel / WindowModel: its tables, nothing else
  energy_all(const, fac, k)    the energy at every state, as an array of shape k (broadcast sum of the tables)
  eliminate(fac, k, mode, s)   own variable elimination over the factor list (site 0 first):
                               mode "sum": ln sum_x exp(s * sum of tables);  mode "max": max_x s * sum of tables, with
                               an arg-max by back-substitution.  Knows nothing of windows or bands.
  capture(module, argv)        run module.main() with argv, stdout swallowed, and return its local variables
  rss()                        peak resident set size in MB
"""
import sys, io, contextlib, resource
import numpy as np


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def factors_of(model):
    fac = [((i,), np.asarray(model.one[i], dtype=float)) for i in range(model.n)]
    for (i, j), tab in model.pair.items():
        assert i < j
        fac.append(((i, j), np.asarray(tab, dtype=float)))
    for U, tab in getattr(model, "multi", {}).items():
        U = tuple(int(u) for u in U)
        assert all(U[a] < U[a + 1] for a in range(len(U) - 1))
        fac.append((U, np.asarray(tab, dtype=float)))
    return float(model.const), fac


def energy_all(const, fac, k):
    n = len(k)
    e = np.full(tuple(k), float(const))
    for U, tab in fac:
        sh = [1] * n
        for u, s in zip(U, tab.shape):
            sh[u] = s
        e = e + tab.reshape(sh)
    return e


def _combine(tabs, scope_all):
    """broadcast sum of tables given with their scopes over the sorted scope `scope_all`"""
    pos = {u: q for q, u in enumerate(scope_all)}
    out = None
    for U, tab in tabs:
        sh = [1] * len(scope_all)
        for u, s in zip(U, tab.shape):
            sh[pos[u]] = s
        t = tab.reshape(sh)
        out = t if out is None else out + t
    return out


def eliminate(fac, k, mode="sum", scale=1.0, want_arg=False):
    """sites eliminated in the order 0, 1, ..., n-1.  Returns value (and an arg-max state if want_arg, mode 'max')."""
    n = len(k)
    cur = [(tuple(U), scale * np.asarray(tab, dtype=float)) for U, tab in fac]
    const = 0.0
    keep = []
    for i in range(n):
        mine = [(U, t) for U, t in cur if i in U]
        cur = [(U, t) for U, t in cur if i not in U]
        if not mine:
            # a site without any table: a free sum / max over k[i] states
            if mode == "sum":
                const += np.log(k[i])
            keep.append((i, None, None))
            continue
        scope = tuple(sorted(set(u for U, _ in mine for u in U)))
        A = _combine(mine, scope)
        ax = scope.index(i)
        rest = tuple(u for u in scope if u != i)
        if mode == "max":
            red = A.max(axis=ax)
            if want_arg:
                keep.append((i, scope, A))
        else:
            mx = A.max(axis=ax, keepdims=True)
            red = np.squeeze(mx, axis=ax) + np.log(np.exp(A - mx).sum(axis=ax))
        if rest:
            cur.append((rest, red))
        else:
            const += float(red)
    assert not cur
    if mode == "max" and want_arg:
        x = [0] * n
        for i, scope, A in reversed(keep):
            if scope is None:
                x[i] = 0
                continue
            idx = tuple(slice(None) if u == i else x[u] for u in scope)
            x[i] = int(np.argmax(A[idx]))
        return const, np.array(x, dtype=int)
    return const


def capture(module, argv, name=None):
    """the local variables of module.main() at its return (the coordinator's own trick, the only reuse)."""
    got = {}
    code = module.main.__code__

    def prof(frame, event, arg):
        if event == "return" and frame.f_code is code:
            got.update(frame.f_locals)
    old = sys.argv
    sys.argv = [name or (module.__name__ + ".py")] + list(argv)
    buf = io.StringIO()
    sys.setprofile(prof)
    try:
        with contextlib.redirect_stdout(buf):
            module.main()
    finally:
        sys.setprofile(None)
        sys.argv = old
    return got, buf.getvalue()


def table_value(scope, tab, X):
    """a table on `scope` at the rows of X"""
    return tab[tuple(X[:, u] for u in scope)]


class OwnSampler:
    """exact independent samples from exp(scale * sum of tables) / Z by the referee's own forward elimination (site 0 first,
    all pre-reduction arrays kept) and backward sampling by inverse CDF.  Independent of BandModel.sample."""

    def __init__(self, fac, k, scale):
        self.k = list(k); n = len(k); self.steps = []
        cur = [(tuple(U), scale * np.asarray(tab, dtype=float)) for U, tab in fac]; const = 0.0
        for i in range(n):
            mine = [(U, t) for U, t in cur if i in U]; cur = [(U, t) for U, t in cur if i not in U]
            if not mine:
                self.steps.append((i, None, None)); const += np.log(k[i]); continue
            scope = tuple(sorted(set(u for U, _ in mine for u in U))); A = _combine(mine, scope)
            A = np.broadcast_to(A, tuple(self.k[u] for u in scope)).copy()
            ax = scope.index(i); mx = A.max(axis=ax, keepdims=True); red = np.squeeze(mx, axis=ax) + np.log(np.exp(A - mx).sum(axis=ax))
            rest = tuple(u for u in scope if u != i)
            self.steps.append((i, scope, np.moveaxis(A, ax, -1)))                 # site i last
            if rest: cur.append((rest, red))
            else: const += float(red)
        assert not cur
        self.lnZ = const

    def sample(self, N, rng):
        n = len(self.k); X = np.zeros((N, n), dtype=np.int64)
        for i, scope, A in reversed(self.steps):
            if scope is None:
                X[:, i] = rng.integers(0, self.k[i], size=N); continue
            rest = tuple(u for u in scope if u != i)
            lw = A[tuple(X[:, u] for u in rest)] if rest else np.broadcast_to(A, (N, self.k[i]))    # (N, k_i)
            lw = lw - lw.max(axis=1, keepdims=True); p = np.exp(lw); cdf = np.cumsum(p, axis=1); u = rng.random(N) * cdf[:, -1]
            X[:, i] = np.minimum((u[:, None] > cdf).sum(axis=1), self.k[i] - 1)
        return X
