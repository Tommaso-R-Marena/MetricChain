"""Branch and bound on sites that leaves a "shares at the leaves" certificate behind.

A node of the search is a node of the certificate's tree: its box fixes the sites on its path.  For a node
the search computes integer messages on its box (``bound``: integer message passing, the rounded linear
programme, or both) and their exact dual value.  If the value reaches the target ``L`` the node becomes a
leaf node and its messages a leaf certificate; otherwise the node branches on a site, one child per state.

Sharing.  Take messages ``m`` on a box and a site ``i``.  After a *pull* at ``i`` (``kernel.c``) every pair at
``i`` has minimum zero for each state ``a`` of the whole alphabet of ``i``, so for any set ``B`` of states the
value of ``m`` on the box with ``D_i = B`` is ``rest + min_{a in B} theta_i(a)``, where ``rest`` collects the terms
that do not involve ``i``.  Hence all states ``a`` with ``rest + theta_i(a) >= L`` are certified by the *same*
messages.  This is used twice: when a node branches on ``i``, the children its own messages already
certify share one leaf certificate; and when a child is certified by its own messages, the siblings those
messages certify as well are closed with it.  In the certificate the children name the same leaf.

The target is the given ``L``, or else the energy of the best state found so far (so that the certificate
proves optimality); in the second case the target can only decrease, and a leaf certified for an earlier
target stays certified.  Nothing here is trusted by the caller: ``produce`` hands the assembled
certificate to both engines of the checker.
"""
from __future__ import annotations

import heapq
import time

import numpy as np

OPEN, LEAF, BRANCH = 0, 1, 2
_NEG = -(1 << 62)

BOUNDS = ("mp", "lp", "hybrid")
BRANCHINGS = ("maxdeg", "margin", "strong", "maxdom", "frac")
ORDERS = ("best", "dfs")


class ProducerError(RuntimeError):
    """An internal consistency check of the producer failed (never a statement about the instance)."""


class Node:
    __slots__ = ("path", "start", "est", "kind", "a", "b", "parent", "ops", "waiting")

    def __init__(self, path, start, est, parent):
        self.path, self.start, self.est, self.parent = path, start, est, parent
        self.kind, self.a, self.b = OPEN, -1, None      # LEAF: a = leaf certificate; BRANCH: a = site, b = children
        self.ops = 0                                    # checker operations of the node's box
        self.waiting = 0                                # BRANCH: number of children that are still open


class Cert:
    """A leaf certificate in sparse form: messages valid on the box of ``path`` with site ``site`` (if any)
    restricted to ``states``; ``total`` is its exact value there."""
    __slots__ = ("m", "path", "site", "states", "total")

    def __init__(self, m, path, site, states, total):
        self.m, self.path, self.site, self.states, self.total = m, path, site, states, total


class Search:
    def __init__(self, model, kernel, lp, *, L, bound, branching, order, deadline, max_leaves, max_cert_integers,
                 max_check_ops, seed, keep, share, restarts, sweeps, patience, root_sweeps, root_patience, wmode,
                 strong_candidates, strong_sweeps):
        self.model, self.kernel, self.lp = model, kernel, lp
        self.L_user = L
        self.bound, self.branching, self.order = bound, branching, order
        self.deadline = deadline
        self.max_leaves, self.max_cert_integers, self.max_check_ops = max_leaves, max_cert_integers, max_check_ops
        self.rng = np.random.default_rng(seed)
        self.keep, self.share = keep, share
        self.restarts = restarts
        self.sweeps, self.patience, self.root_sweeps, self.root_patience, self.wmode = (
            sweeps, patience, root_sweeps, root_patience, wmode)
        self.strong_candidates, self.strong_sweeps = strong_candidates, strong_sweeps
        mod = model
        n = mod.n
        self.ksq = int((mod.k * mod.k).sum())
        self.npairs = n * (n - 1) // 2
        self.ints_per_leaf = n + self.npairs + (n - 1) * mod.S
        self.site_of_state = np.repeat(np.arange(n), mod.k)
        self.certs = []
        self.ncerts = 0                    # counted also when the certificates are not kept
        self.leaf_boxes = 0
        self.check_ops = 0
        self.depth = 0
        self.open_nodes = 0                # nodes not yet evaluated; every one will be at least one leaf box
        self.open_ops = 0                  # checker operations of their boxes (branching never lowers the sum)
        self.open_sets = 0                 # sets of open siblings: each needs at least one more leaf certificate
        self.stop = None                   # None, or the limit that ended the search, or "refuted"
        self.ub, self.x = None, None
        self.root = None
        self.stats = {"nodes": 0, "branch_nodes": 0, "ascents": 0, "sweeps": 0, "lp_calls": 0, "lp_failures": 0,
                      "lp_seconds": 0.0, "ub_updates": 0, "shared_by_parent": 0, "shared_by_sibling": 0,
                      "root_value": None, "root_lp_value": None, "root_first_pass": None, "initial_ub": None,
                      "anomalies": 0, "max_open": 0, "lp_rounding_loss_root": None}

    # ------------------------------------------------------------------------------------------ small helpers
    def target(self):
        return self.L_user if self.L_user is not None else self.ub

    def _offer(self, x, energy):
        if self.ub is None or energy < self.ub:
            if self.ub is not None:
                self.stats["ub_updates"] += 1
            self.ub, self.x = int(energy), x.copy()

    def _box_ops(self, path):
        """Additions plus comparisons the checker performs on the box of ``path`` (its closed formula)."""
        mod = self.model
        s1, q = mod.S, self.ksq
        for i, _ in path:
            ki = int(mod.k[i])
            s1 -= ki - 1
            q -= ki * ki - 1
        return mod.n * s1 + 3 * ((s1 * s1 - q) // 2) + mod.n + self.npairs

    def _guard(self, m):
        if m.size and int(np.abs(m).max()) > self.model.max_message:
            raise ProducerError("messages left the range in which int64 arithmetic is exact")

    def _key(self, node, seq):
        est = _NEG if node.est is None else node.est
        if self.order == "best":
            return (est, -len(node.path), seq)
        return (-len(node.path), est, seq)

    def _new_cert(self, m, path, site, states, total):
        self.ncerts += 1
        if self.keep:
            self.certs.append(Cert(m, path, site, states, int(total)))
            return len(self.certs) - 1
        return -1

    def _leaf(self, node, index):
        node.kind, node.a, node.start = LEAF, index, None
        self.leaf_boxes += 1
        self.check_ops += self._box_ops(node.path)
        if len(node.path) > self.depth:
            self.depth = len(node.path)

    def _open(self, node):
        node.ops = self._box_ops(node.path)
        self.open_nodes += 1
        self.open_ops += node.ops
        if node.parent is not None:
            if node.parent.waiting == 0:
                self.open_sets += 1
            node.parent.waiting += 1
        else:
            self.open_sets += 1

    def _unopen(self, node):
        self.open_nodes -= 1
        self.open_ops -= node.ops
        if node.parent is not None:
            node.parent.waiting -= 1
            if node.parent.waiting == 0:
                self.open_sets -= 1
        else:
            self.open_sets -= 1

    def _limits(self):
        """Stop as soon as the finished tree is known to exceed a size limit.  The bounds are rigorous: an open
        node ends as at least one leaf box; the open children of a node need at least one leaf certificate
        (they can share one at best); the checker operations of the boxes below a node are at least those of
        its own box (fixing a site of a box and summing over its states does not lower the count)."""
        if self.leaf_boxes + self.open_nodes > self.max_leaves:
            self.stop = "leaves"
        elif (self.ncerts + self.open_sets) * self.ints_per_leaf > self.max_cert_integers:
            self.stop = "cert_integers"
        elif self.max_check_ops is not None and self.check_ops + self.open_ops > self.max_check_ops:
            self.stop = "check_ops"

    # ------------------------------------------------------------------------------------------ the search
    def run(self):
        mod, ker = self.model, self.kernel
        x = np.zeros(mod.n, dtype=np.int64)
        self._offer(x, ker.icm(x))
        for _ in range(self.restarts):
            x = (self.rng.random(mod.n) * mod.k).astype(np.int64)
            self._offer(x, ker.icm(x))
        self.stats["initial_ub"] = self.ub
        self.stats["ub_updates"] = 0
        if self.L_user is not None and self.ub < self.L_user:
            self.stop = "refuted"
            return
        self.root = Node((), mod.zero_messages(), None, None)
        self._open(self.root)
        heap = [(self._key(self.root, 0), 0, self.root)]
        self.seq = 1
        while heap and self.stop is None:
            if time.perf_counter() > self.deadline:
                self.stop = "time"
                break
            if len(heap) > self.stats["max_open"]:
                self.stats["max_open"] = len(heap)
            node = heapq.heappop(heap)[2]
            if node.kind == OPEN:
                self._evaluate(node, heap)
        if self.lp is not None:
            self.stats["lp_calls"], self.stats["lp_failures"] = self.lp.calls, self.lp.failures
            self.stats["lp_seconds"] = self.lp.seconds

    def _messages(self, node, dlen, dom):
        """Messages for the box of ``node``: ``(m, mu)`` with ``mu`` the site marginals of the programme, if it
        was solved."""
        ker, lp = self.kernel, self.lp
        is_root = node.parent is None
        m = node.start.copy()
        mu = None
        target = self.target()
        if self.bound == "lp":
            sol = lp.solve(dlen, dom, self.deadline - time.perf_counter())
            if sol is not None:
                total, m = lp.rounded(ker, dlen, dom, sol["messages"])
                mu = sol["mu"]
                if is_root:
                    self.stats["root_lp_value"] = sol["value"]
                    self.stats["lp_rounding_loss_root"] = sol["value"] - total
            return m, mu
        sweeps, patience = (self.root_sweeps, self.root_patience) if is_root else (self.sweeps, self.patience)
        _, used, reached, _, first = ker.ascent(dlen, dom, m, target, sweeps, patience, self.wmode)
        self.stats["ascents"] += 1
        self.stats["sweeps"] += used
        if is_root:
            self.stats["root_first_pass"] = first
        if self.bound == "mp" or reached:
            return m, mu
        free = dlen > 1
        if int((free[self.model.eu] & free[self.model.ev]).sum()) < 3:
            return m, mu                               # the free sites form a forest: the ascent was exact
        sol = lp.solve(dlen, dom, self.deadline - time.perf_counter())
        if sol is None:
            return m, mu
        mu = sol["mu"]
        total = ker.eval(dlen, dom, m)[0]
        total2, m2 = lp.rounded(ker, dlen, dom, sol["messages"])
        if is_root:
            self.stats["root_lp_value"] = sol["value"]
            self.stats["lp_rounding_loss_root"] = sol["value"] - total2
        if total2 < target and sol["value"] > target - 1e-6 * max(1.0, abs(target)):
            _, used, _, _, _ = ker.ascent(dlen, dom, m2, target, sweeps, patience, self.wmode)   # polish
            self.stats["ascents"] += 1
            self.stats["sweeps"] += used
            total2 = ker.eval(dlen, dom, m2)[0]
        if total2 > total:
            m = m2
        return m, mu

    def _evaluate(self, node, heap):
        mod, ker = self.model, self.kernel
        self.stats["nodes"] += 1
        self._unopen(node)
        dlen, dom = mod.box(node.path)
        m, mu = self._messages(node, dlen, dom)
        self._guard(m)
        total, U, P, arg = ker.eval(dlen, dom, m)
        if node.est is not None and total < node.est:   # cannot be worse than the parent's messages: keep those
            if self.bound != "lp":
                self.stats["anomalies"] += 1
            m = node.start.copy()
            total, U, P, arg = ker.eval(dlen, dom, m)
        if node.parent is None:
            self.stats["root_value"] = int(total)
        # primal side: the state the messages point at, improved by local search
        x = ker.decode(dlen, dom, m)
        self._offer(x, ker.icm(x))
        if mu is not None:
            x = np.array([int(np.argmax(mu[mod.koff[i]:mod.koff[i + 1]])) for i in range(mod.n)], dtype=np.int64)
            for i, a in node.path:
                x[i] = a
            self._offer(x, ker.icm(x))
        if self.L_user is not None and self.ub < self.L_user:
            self.stop = "refuted"
            return
        target = self.target()
        if total >= target:
            self._close(node, m, total, dlen, dom)
            self._limits()
            return
        free = np.flatnonzero(dlen > 1)
        if free.size == 0:
            raise ProducerError("a box of one state has a value below the energy of that state")
        site = self._choose(node, free, dlen, dom, m, mu, target)
        theta = ker.pull_site(dlen, dom, m, site)
        total, U, P, _ = ker.eval(dlen, dom, m)
        if total >= target:                             # the pull alone closed the gap
            self._close(node, m, total, dlen, dom)
            self._limits()
            return
        rest = int(total) - int(U[site]) - sum(int(P[e]) for e, _ in mod.nbrs[site])
        self.stats["branch_nodes"] += 1
        node.kind, node.a, node.start = BRANCH, int(site), None
        node.b = children = []
        shared = []
        for a in range(int(mod.k[site])):
            est = rest + int(theta[a])
            child = Node(node.path + ((int(site), a),), m, est, node)
            children.append(child)
            if est >= target and self.share:
                shared.append(child)
        if shared:
            states = [child.path[-1][1] for child in shared]
            index = self._new_cert(m, node.path, int(site), states, min(child.est for child in shared))
            for child in shared:
                self._leaf(child, index)
            self.stats["shared_by_parent"] += len(shared)
        for child in children:
            if child.kind == OPEN:
                self._open(child)
                heapq.heappush(heap, (self._key(child, self.seq), self.seq, child))
                self.seq += 1
        self._limits()

    def _close(self, node, m, total, dlen, dom):
        """``m`` certifies the box of ``node``; close it, together with the open siblings ``m`` certifies too."""
        mod, ker = self.model, self.kernel
        parent = node.parent
        if parent is None:
            self._leaf(node, self._new_cert(m, (), None, None, total))
            return
        site = parent.a
        mine = node.path[-1][1]
        group = [node]
        others = [child for child in parent.b if child.kind == OPEN and child is not node] if self.share else []
        if others:
            target = self.target()
            theta = ker.pull_site(dlen, dom, m, site)
            total, U, P, _ = ker.eval(dlen, dom, m)
            rest = int(total) - int(U[site]) - sum(int(P[e]) for e, _ in mod.nbrs[site])
            extra = [child for child in others if rest + int(theta[child.path[-1][1]]) >= target]
            if extra:
                states = sorted([mine] + [child.path[-1][1] for child in extra])
                hull = mod.box(parent.path, (site, states))
                hull_total = ker.eval(hull[0], hull[1], m)[0]
                if hull_total >= target:
                    group += extra
                    total = hull_total
                    self.stats["shared_by_sibling"] += len(extra)
                    for child in extra:
                        self._unopen(child)
                else:                                    # cannot happen (the pull makes the formula exact)
                    self.stats["anomalies"] += 1
        states = sorted(child.path[-1][1] for child in group)
        index = self._new_cert(m, parent.path, site, states, total)
        for child in group:
            self._leaf(child, index)

    # ------------------------------------------------------------------------------------------ branching
    def _margins(self, dlen, dom, m):
        """For every site the difference between the two smallest values, over its alphabet, of the site term
        after a pull: how firmly the node's messages prefer one state (0: a tie)."""
        mod = self.model
        c = self.kernel.probe_all(dlen, dom, m)
        low = np.minimum.reduceat(c, mod.koff[:-1])
        hit = np.flatnonzero(c == low[self.site_of_state])
        _, first = np.unique(self.site_of_state[hit], return_index=True)
        c[hit[first]] = np.iinfo(np.int64).max
        second = np.minimum.reduceat(c, mod.koff[:-1])
        return np.where(mod.k > 1, second - low, 0)

    def _choose(self, node, free, dlen, dom, m, mu, target):
        """The site to branch on.  Candidates are the free sites in the 2-core of the graph of free sites
        (elsewhere the relaxation loses nothing); if the core is empty, all free sites."""
        mod, ker = self.model, self.kernel
        rule = self.branching
        core = ker.core(dlen)
        cand = np.flatnonzero(core > 0)
        if cand.size == 0:
            cand = free
        if cand.size == 1:
            return int(cand[0])
        if rule == "frac":
            if mu is not None:
                top = np.maximum.reduceat(mu, mod.koff[:-1])[cand]
                if float(top.min()) < 1.0 - 1e-6:
                    return int(cand[int(np.argmin(top))])
            rule = "maxdeg"                             # the programme was integral or not solved here
        deg, k = (-core[cand]).tolist(), mod.k[cand].tolist()
        if rule == "maxdom":
            return min(zip((-mod.k[cand]).tolist(), deg, cand.tolist()))[2]
        if rule == "maxdeg":
            return min(zip(deg, k, cand.tolist()))[2]
        margin = self._margins(dlen, dom, m)[cand].tolist()
        if rule == "margin":
            return min(zip(margin, deg, k, cand.tolist()))[3]
        ranked = sorted(zip(deg, margin, k, cand.tolist()))     # strong: re-optimise the children of the best few
        best = None
        for rank, (_, _, _, site) in enumerate(ranked[:self.strong_candidates]):
            mi = m.copy()
            theta = ker.pull_site(dlen, dom, mi, site)
            tot, Ui, Pi, _ = ker.eval(dlen, dom, mi)
            rest = int(tot) - int(Ui[site]) - sum(int(Pi[e]) for e, _ in mod.nbrs[site])
            low, total = None, 0
            for a in range(int(mod.k[site])):
                value = rest + int(theta[a])
                if value < target:
                    ma = mi.copy()
                    cd, cdom = mod.box(node.path + ((site, a),))
                    ker.ascent(cd, cdom, ma, target, self.strong_sweeps, self.strong_sweeps, self.wmode)
                    self.stats["ascents"] += 1
                    self.stats["sweeps"] += self.strong_sweeps
                    value = ker.eval(cd, cdom, ma)[0]
                value = min(value, target)
                low = value if low is None or value < low else low
                total += value
            score = (-low, -total / int(mod.k[site]), rank)
            if best is None or score < best[0]:
                best = (score, site)
        return best[1]

    # ------------------------------------------------------------------------------------------ what is left open
    def open_groups(self):
        """The open nodes, grouped by parent: ``(parent or None, [children])``.  All open children of a node
        are certified by that node's messages (their common ``start``) with the value ``est``."""
        groups, stack = [], [self.root]
        while stack:
            node = stack.pop()
            if node.kind == OPEN and node.parent is None:
                groups.append((None, [node]))
            elif node.kind == BRANCH:
                waiting = [child for child in node.b if child.kind == OPEN]
                if waiting:
                    groups.append((node, waiting))
                stack.extend(child for child in node.b if child.kind == BRANCH)
        return groups

