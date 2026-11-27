"""Leaf messages from the linear programme of the pairwise relaxation (``scipy.optimize.linprog``, HiGHS).

The relaxation of ``min_x E(x)`` on a box is the programme over "marginals" ``mu_i(a) >= 0``, ``mu_e(a, b) >= 0``

    minimise   sum_i sum_a H_i(a) mu_i(a) + sum_e sum_ab J_e(a, b) mu_e(a, b)
    subject to sum_a mu_i(a) = 1,    sum_b mu_e(a, b) = mu_u(a),    sum_a mu_e(a, b) = mu_v(b),

with ``mu = 0`` outside the box.  The multipliers of the two families of coupling rows are messages
``m_uv(a)``, ``m_vu(b)`` with which the dual value of ``kernel.c`` equals the optimum of the programme (the
multipliers of the first family are the ``U_i``; the pair terms are zero).  The solver works in floating
point, so its multipliers only *propose* messages: they are rounded to integers (to nearest, down and up;
the best of the three is kept) and the caller evaluates the result exactly.  Whatever the solver returns,
the leaf built from the rounded messages is valid; it may be weaker than the programme's optimum.
"""
from __future__ import annotations

import time

import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog


class LPBound:
    """The programme of one model; :meth:`solve` restricts it to a box through the bounds of the variables."""

    def __init__(self, model):
        mod = self.model = model
        n, S, ne, M = mod.n, mod.S, mod.ne, mod.M
        NJ = int(mod.joff[ne])
        rows = [np.repeat(np.arange(n), mod.k)]
        cols = [np.arange(S)]
        vals = [np.ones(S)]
        pu, pv = [], []                                # (site, state) index of the two ends of every pair variable
        for e in range(ne):
            u, v = int(mod.eu[e]), int(mod.ev[e])
            ku, kv = int(mod.k[u]), int(mod.k[v])
            mo, jo = n + int(mod.moff[e]), S + int(mod.joff[e])
            a = np.repeat(np.arange(ku), kv)
            b = np.tile(np.arange(kv), ku)
            pair = jo + np.arange(ku * kv)
            rows += [mo + a, mo + ku + b, mo + np.arange(ku), mo + ku + np.arange(kv)]
            cols += [pair, pair, int(mod.koff[u]) + np.arange(ku), int(mod.koff[v]) + np.arange(kv)]
            vals += [np.ones(2 * ku * kv), -np.ones(ku + kv)]
            pu.append(int(mod.koff[u]) + a)
            pv.append(int(mod.koff[v]) + b)
        self.A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                               shape=(n + M, S + NJ))
        self.b = np.zeros(n + M)
        self.b[:n] = 1.0
        self.c = np.concatenate([mod.H, mod.J[:NJ]]).astype(float)
        self.pu = np.concatenate(pu) if ne else np.zeros(0, dtype=np.int64)
        self.pv = np.concatenate(pv) if ne else np.zeros(0, dtype=np.int64)
        # (site, state) index of every message entry, to blank the entries of states outside the box
        self.mstate = (np.concatenate([np.concatenate([int(mod.koff[int(mod.eu[e])]) + np.arange(int(mod.k[int(mod.eu[e])])),
                                                       int(mod.koff[int(mod.ev[e])]) + np.arange(int(mod.k[int(mod.ev[e])]))])
                                       for e in range(ne)]) if ne else np.zeros(0, dtype=np.int64))
        self.calls = 0
        self.failures = 0
        self.seconds = 0.0

    def solve(self, dlen, dom, time_limit=None):
        """Solve the relaxation on the box.  Returns ``None`` if the solver did not reach an optimum, else a
        dict with ``value`` (float), ``messages`` (float vector of length ``M``; zero at states outside the
        box) and ``mu`` (the site marginals, length ``S``)."""
        mod = self.model
        allowed = np.zeros(mod.S, dtype=bool)
        idx = np.concatenate([mod.koff[i] + dom[mod.koff[i]:mod.koff[i] + dlen[i]] for i in range(mod.n)])
        allowed[idx] = True
        ub = np.concatenate([np.where(allowed, np.inf, 0.0), np.where(allowed[self.pu] & allowed[self.pv], np.inf, 0.0)])
        bounds = np.column_stack([np.zeros(len(ub)), ub])
        options = {"presolve": True}
        if time_limit is not None:
            options["time_limit"] = max(0.05, float(time_limit))
        t0 = time.perf_counter()
        try:
            res = linprog(self.c, A_eq=self.A, b_eq=self.b, bounds=bounds, method="highs-ds", options=options)
        except Exception:                               # the solver is only a source of proposals
            res = None
        self.calls += 1
        self.seconds += time.perf_counter() - t0
        if res is None or res.status != 0 or res.eqlin is None:
            self.failures += 1
            return None
        y = np.asarray(res.eqlin.marginals[mod.n:], dtype=float)
        if not np.all(np.isfinite(y)) or (y.size and np.abs(y).max() > 2.0 ** 50) or not np.isfinite(res.fun):
            self.failures += 1
            return None
        y = np.where(allowed[self.mstate], y, 0.0) if mod.M else np.zeros(1)
        return {"value": float(res.fun), "messages": y, "mu": np.asarray(res.x[:mod.S], dtype=float)}

    def rounded(self, kernel, dlen, dom, y):
        """The best of the three roundings of the proposal ``y``: ``(total, messages)``, evaluated exactly."""
        best = None
        for op in (np.rint, np.floor, np.ceil):
            m = op(y).astype(np.int64)
            total = kernel.eval(dlen, dom, m)[0]
            if best is None or total > best[0]:
                best = (total, m)
        return best
