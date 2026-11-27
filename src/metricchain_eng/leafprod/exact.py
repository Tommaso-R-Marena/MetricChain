"""Exact minimisation without certificates: enumeration and dynamic programming (variable elimination).

Test oracles of the producer and baselines of the benchmark.  Both compute with ``int64``; ``model.Model``
accepts an instance only if every energy (one entry per site and per edge) stays below ``2^62`` in absolute
value, so every sum formed here is exact.

``brute_force``   the energy of every state, built site by site (``prod k_i`` integers of memory).
``eliminate``     min-sum variable elimination along a greedy order (cheapest table first).  Exact on any
                  instance; the cost is the size of the largest table, ``k^(w+1)`` on a graph of induced
                  width ``w`` -- chains and trees (``w = 1``), bands of range ``w``, grids of side ``w``.
``plan``          the elimination order and the table sizes it leads to, without doing the work.
"""
from __future__ import annotations

import numpy as np

from .model import Model


def _model(instance):
    return instance if isinstance(instance, Model) else Model(instance)


def brute_force(instance, max_states=1 << 24):
    """``(minimum, a minimising state, number of states)`` by enumeration, or ``None`` if the domain has more
    than ``max_states`` states."""
    mod = _model(instance)
    states = 1
    for k in mod.k.tolist():
        states *= k
        if states > max_states:
            return None
    before = [[] for _ in range(mod.n)]                  # edges (i, t) with i < t, listed at t
    for e in range(mod.ne):
        before[int(mod.ev[e])].append((int(mod.eu[e]), e))
    energy = mod.H[:int(mod.k[0])].copy()
    for t in range(1, mod.n):
        kt = int(mod.k[t])
        energy = energy[..., None] + mod.H[mod.koff[t]:mod.koff[t + 1]]
        for i, e in before[t]:
            shape = [1] * (t + 1)
            shape[i], shape[t] = int(mod.k[i]), kt
            energy += mod.tables[e].reshape(shape)
    flat = int(np.argmin(energy))
    x = [int(v) for v in np.unravel_index(flat, energy.shape)]
    return int(energy.reshape(-1)[flat]), x, states


def plan(instance):
    """Greedy elimination order (the site whose elimination table is smallest first; ties: lowest index).
    Returns ``(order, largest table, sum of the table sizes)`` in numbers of entries."""
    mod = _model(instance)
    nb = [set(j for _, j in mod.nbrs[i]) for i in range(mod.n)]
    k = mod.k.tolist()
    alive = set(range(mod.n))
    order, largest, total = [], 0, 0

    def size(i):
        s = k[i]
        for j in nb[i]:
            s *= k[j]
        return s

    cost = {i: size(i) for i in alive}
    while alive:
        v = min(alive, key=lambda i: (cost[i], i))
        order.append(v)
        largest = max(largest, cost[v])
        total += cost[v]
        alive.discard(v)
        for a in nb[v]:
            nb[a].discard(v)
            nb[a] |= nb[v] - {a}
        for a in nb[v]:
            cost[a] = size(a)
    return order, largest, total


def eliminate(instance, max_table=1 << 24, order=None):
    """``(minimum, a minimising state)`` by variable elimination, or ``None`` if a table would have more than
    ``max_table`` entries."""
    mod = _model(instance)
    if order is None:
        order, largest, _ = plan(mod)
        if largest > max_table:
            return None
    k = mod.k.tolist()
    factors = [((i,), mod.H[mod.koff[i]:mod.koff[i + 1]].copy()) for i in range(mod.n)]
    factors += [((int(mod.eu[e]), int(mod.ev[e])), mod.tables[e]) for e in range(mod.ne)]
    buckets = {i: [] for i in range(mod.n)}
    position = {v: p for p, v in enumerate(order)}
    constant = 0

    def place(scope, table):
        nonlocal constant
        if not scope:
            constant += int(table)
        else:
            buckets[min(scope, key=position.__getitem__)].append((scope, table))

    for scope, table in factors:
        place(scope, table)
    trace = []
    for v in order:
        scope = sorted(set(i for s, _ in buckets[v] for i in s))
        entries = 1
        for i in scope:
            entries *= k[i]
        if entries > max_table:
            return None
        acc = np.zeros([k[i] for i in scope], dtype=np.int64)
        for s, table in buckets[v]:
            acc += table.reshape([k[i] if i in s else 1 for i in scope])
        axis = scope.index(v)
        rest = tuple(i for i in scope if i != v)
        trace.append((v, rest, np.argmin(acc, axis=axis)))
        place(rest, acc.min(axis=axis))
        buckets[v] = None
    x = [0] * mod.n
    for v, rest, arg in reversed(trace):
        x[v] = int(arg[tuple(x[i] for i in rest)]) if rest else int(arg)
    return constant, x
