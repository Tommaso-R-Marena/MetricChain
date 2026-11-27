"""Plain-Python reference of ``kernel.c`` (Python integers; same interface as ``ckernel.Kernel``).

Written line by line after the description in the header of ``kernel.c`` so that the tests can require the
two to return identical messages and values.  Slow; ``produce(..., kernel="python")`` uses it.
"""
from __future__ import annotations

import numpy as np


class Kernel:
    name = "python"

    def __init__(self, model):
        self.model = model
        mod = model
        self.k = [int(v) for v in mod.k]
        self.koff = [int(v) for v in mod.koff]
        self.H = [int(v) for v in mod.H]
        self.edges = [(int(mod.eu[e]), int(mod.ev[e])) for e in range(mod.ne)]
        self.tables = [t.tolist() for t in mod.tables]
        self.moff = [int(v) for v in mod.moff]
        self.nbrs = mod.nbrs

    # ------------------------------------------------------------------------------------------ helpers
    def _mpos(self, e, i):
        """Offset of the message vector of site ``i`` on edge ``e``."""
        u, _ = self.edges[e]
        return self.moff[e] + (0 if u == i else self.k[u])

    def _jval(self, e, i, a, b):
        """Table of edge ``e`` at state ``a`` of site ``i`` and state ``b`` of the other endpoint."""
        u, _ = self.edges[e]
        return self.tables[e][a][b] if u == i else self.tables[e][b][a]

    def _dom(self, dlen, dom, i):
        return [int(dom[self.koff[i] + t]) for t in range(int(dlen[i]))]

    def _pull(self, dlen, dom, m, i, e, j, states):
        """``m_i,e(a) := min_{b in D_j} [J(a, b) - m_j,e(b)]`` for the given states; returns the new values."""
        pi, pj = self._mpos(e, i), self._mpos(e, j)
        dj = self._dom(dlen, dom, j)
        out = []
        for a in states:
            best = min(self._jval(e, i, a, b) - int(m[pj + b]) for b in dj)
            m[pi + a] = best
            out.append(best)
        return out

    # ------------------------------------------------------------------------------------------ interface
    def eval(self, dlen, dom, m):
        mod = self.model
        U = np.empty(mod.n, dtype=np.int64)
        P = np.empty(mod.ne, dtype=np.int64)
        arg = np.empty(mod.n, dtype=np.int64)
        total = 0
        for i in range(mod.n):
            best = None
            for a in self._dom(dlen, dom, i):
                v = self.H[self.koff[i] + a] + sum(int(m[self._mpos(e, i) + a]) for e, _ in self.nbrs[i])
                if best is None or v < best:
                    best, arg[i] = v, a
            U[i] = best
            total += best
        for e, (u, v) in enumerate(self.edges):
            pu, pv = self._mpos(e, u), self._mpos(e, v)
            best = min(self.tables[e][a][b] - int(m[pu + a]) - int(m[pv + b])
                       for a in self._dom(dlen, dom, u) for b in self._dom(dlen, dom, v))
            P[e] = best
            total += best
        return total, U, P, arg

    def pull_site(self, dlen, dom, m, i):
        states = list(range(self.k[i]))
        theta = [self.H[self.koff[i] + a] for a in states]
        for e, j in self.nbrs[i]:
            for a, g in zip(states, self._pull(dlen, dom, m, i, e, j, states)):
                theta[a] += g
        return np.array(theta, dtype=np.int64)

    def probe_all(self, dlen, dom, m):
        c = list(self.H)
        for i in range(self.model.n):
            for e, j in self.nbrs[i]:
                pj = self._mpos(e, j)
                dj = self._dom(dlen, dom, j)
                for a in range(self.k[i]):
                    c[self.koff[i] + a] += min(self._jval(e, i, a, b) - int(m[pj + b]) for b in dj)
        return np.array(c, dtype=np.int64)

    def ascent(self, dlen, dom, m, target, max_sweeps, patience, wmode=0):
        mod = self.model
        n = mod.n
        free = [int(dlen[i]) > 1 for i in range(n)]
        D = [self._dom(dlen, dom, i) for i in range(n)]
        cfixed = 0
        for e, (u, v) in enumerate(self.edges):                      # fold
            pu, pv = self._mpos(e, u), self._mpos(e, v)
            if not free[u] and free[v]:
                a = D[u][0]
                for b in D[v]:
                    m[pv + b] = self.tables[e][a][b] - int(m[pu + a])
            elif free[u] and not free[v]:
                b = D[v][0]
                for a in D[u]:
                    m[pu + a] = self.tables[e][a][b] - int(m[pv + b])
            elif not free[u] and not free[v]:
                cfixed += self.tables[e][D[u][0]][D[v][0]] - int(m[pu + D[u][0]]) - int(m[pv + D[v][0]])
        base, fadj = {}, {}
        for i in range(n):
            if not free[i]:
                a = D[i][0]
                cfixed += self.H[self.koff[i] + a] + sum(int(m[self._mpos(e, i) + a]) for e, _ in self.nbrs[i])
                continue
            base[i] = {a: self.H[self.koff[i] + a] + sum(int(m[self._mpos(e, i) + a]) for e, j in self.nbrs[i] if not free[j])
                       for a in D[i]}
            fadj[i] = [(e, j) for e, j in self.nbrs[i] if free[j]]
        order, pos = [], {}
        for s in range(n):                                           # breadth-first order of the free sites
            if not free[s] or s in pos:
                continue
            pos[s] = len(order)
            order.append(s)
            h = pos[s]
            while h < len(order):
                i = order[h]
                for e, j in fadj[i]:
                    if j not in pos:
                        pos[j] = len(order)
                        order.append(j)
                h += 1
        nfree = len(order)
        best = value = first = None
        stall = sweeps = passes = 0
        reached = False
        if nfree == 0:
            value = first = cfixed
            reached = value >= target
            max_sweeps = 0
        while sweeps < max_sweeps and not reached:
            for direction in (0, 1):
                if reached:
                    break
                value = cfixed
                for h in range(nfree):
                    i = order[h if direction == 0 else nfree - 1 - h]
                    theta = dict(base[i])
                    out = []
                    nin = 0
                    for e, j in fadj[i]:
                        for a, g in zip(D[i], self._pull(dlen, dom, m, i, e, j, D[i])):
                            theta[a] += g
                        if (direction == 0) == (pos[j] > pos[i]):
                            out.append(e)
                        else:
                            nin += 1
                    v = min(theta.values())
                    keep = 0
                    if out:
                        nout = len(out)
                        W = nin if (wmode == 1 and nin > nout) else nout
                        keep = None
                        for a in D[i]:
                            ex = theta[a] - v
                            share, rem = divmod(ex, W)
                            rot = 0 if wmode == 1 else (a + passes) % nout
                            for o, e in enumerate(out):
                                give = share
                                if wmode != 1 and (o + rot) % nout < rem:
                                    give += 1
                                m[self._mpos(e, i) + a] -= give
                            left = ex - share * nout if wmode == 1 else 0
                            keep = left if keep is None or left < keep else keep
                    value += v + keep
                passes += 1
                if first is None:
                    first = value
                if value >= target:
                    reached = True
            sweeps += 1
            if best is None or value > best:
                best, stall = value, 0
            else:
                stall += 1
                if stall >= patience:
                    break
        return value, sweeps, reached, nfree, first

    def decode(self, dlen, dom, m):
        mod = self.model
        n = mod.n
        free = [int(dlen[i]) > 1 for i in range(n)]
        x = np.zeros(n, dtype=np.int64)
        done = [not f for f in free]
        for i in range(n):
            if not free[i]:
                x[i] = int(dom[self.koff[i]])
        order, seen = [], set()
        for s in range(n):
            if not free[s] or s in seen:
                continue
            seen.add(s)
            order.append(s)
            h = len(order) - 1
            while h < len(order):
                for e, j in self.nbrs[order[h]]:
                    if free[j] and j not in seen:
                        seen.add(j)
                        order.append(j)
                h += 1
        for i in order:
            best = None
            for a in self._dom(dlen, dom, i):
                cost = self.H[self.koff[i] + a]
                for e, j in self.nbrs[i]:
                    cost += self._jval(e, i, a, int(x[j])) if done[j] else int(m[self._mpos(e, i) + a])
                if best is None or cost < best:
                    best, x[i] = cost, a
            done[i] = True
        return x

    def core(self, dlen):
        n = self.model.n
        alive = [int(dlen[i]) > 1 for i in range(n)]
        while True:
            deg = [sum(1 for _, j in self.nbrs[i] if alive[j]) if alive[i] else 0 for i in range(n)]
            drop = [i for i in range(n) if alive[i] and deg[i] <= 1]
            if not drop:
                return np.array(deg, dtype=np.int64)
            for i in drop:
                alive[i] = False

    def energy(self, x):
        return self.model.energy([int(v) for v in x])

    def icm(self, x, box=None, max_sweeps=1000):
        mod = self.model
        for _ in range(max_sweeps):
            changed = False
            for i in range(mod.n):
                if box is not None and int(box[0][i]) == 1:
                    continue
                cost = [self.H[self.koff[i] + a] + sum(self._jval(e, i, a, int(x[j])) for e, j in self.nbrs[i])
                        for a in range(self.k[i])]
                cur = int(x[i])
                besta = cur
                for a in (self._dom(box[0], box[1], i) if box is not None else range(self.k[i])):
                    if cost[a] < cost[besta]:
                        besta = a
                if besta != cur:
                    x[i] = besta
                    changed = True
            if not changed:
                break
        return self.energy(x)
