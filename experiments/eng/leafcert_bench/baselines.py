"""Baselines of the certificate benchmark: exact solvers that leave no certificate our checker can verify.

``cpsat``        OR-tools CP-SAT on one worker (a general exact solver; it proves optimality internally).
``milp``         the mixed-integer solver of HiGHS on the pairwise relaxation (a second general exact solver).
``brute``        enumeration of the whole domain (``metricchain_eng.leafprod.exact.brute_force``).
``dp``           variable elimination (``exact.eliminate``): dynamic programming on chains, trees and bands,
                 and on anything else whose elimination tables fit.
``plain_bnb``    the producer's own search with ``certificate=False``: the same nodes, bounds and branching,
                 nothing stored, assembled or checked.

Every function returns a dict with ``status``, ``value`` (the minimum, or ``None``) and ``seconds``.
"""
from __future__ import annotations

import time

from metricchain_eng.leafprod import exact, produce
from metricchain_eng.leafprod.model import Model


def cpsat(instance, time_limit, encoding="marginal", seed=0):
    """Minimise with CP-SAT, one worker, ``linearization_level = 2`` (the setting that was fastest on the
    development instances; with the default level the single worker was up to ten times slower).
    ``encoding="marginal"``: a Boolean per (site, state) and per (edge, state, state), tied by the equalities
    of the pairwise relaxation, so that the solver's own linear relaxation is the one our leaves use;
    ``"table"``: an integer per site and one table constraint with a cost variable per edge.  ``seconds``
    covers building the model and solving it."""
    from ortools.sat.python import cp_model
    t0 = time.perf_counter()
    mod = instance if isinstance(instance, Model) else Model(instance)
    cp = cp_model.CpModel()
    terms, coefs = [], []
    if encoding == "marginal":
        site = []
        for i in range(mod.n):
            row = [cp.NewBoolVar("") for _ in range(int(mod.k[i]))]
            cp.AddExactlyOne(row)
            site.append(row)
            for a, lit in enumerate(row):
                terms.append(lit)
                coefs.append(int(mod.H[mod.koff[i] + a]))
        for e in range(mod.ne):
            u, v, table = int(mod.eu[e]), int(mod.ev[e]), mod.tables[e]
            pair = [[cp.NewBoolVar("") for _ in range(table.shape[1])] for _ in range(table.shape[0])]
            for a in range(table.shape[0]):
                cp.Add(sum(pair[a]) == site[u][a])
            for b in range(table.shape[1]):
                cp.Add(sum(pair[a][b] for a in range(table.shape[0])) == site[v][b])
            for a in range(table.shape[0]):
                for b in range(table.shape[1]):
                    if table[a, b]:
                        terms.append(pair[a][b])
                        coefs.append(int(table[a, b]))
    elif encoding == "table":
        xs = [cp.NewIntVar(0, int(mod.k[i]) - 1, "") for i in range(mod.n)]
        for i in range(mod.n):
            row = [int(v) for v in mod.H[mod.koff[i]:mod.koff[i + 1]]]
            h = cp.NewIntVar(min(row), max(row), "")
            cp.AddElement(xs[i], row, h)
            terms.append(h)
            coefs.append(1)
        for e in range(mod.ne):
            u, v, table = int(mod.eu[e]), int(mod.ev[e]), mod.tables[e]
            c = cp.NewIntVar(int(table.min()), int(table.max()), "")
            cp.AddAllowedAssignments([xs[u], xs[v], c], [(a, b, int(table[a, b])) for a in range(table.shape[0])
                                                         for b in range(table.shape[1])])
            terms.append(c)
            coefs.append(1)
    else:
        raise ValueError("encoding must be 'marginal' or 'table'")
    cp.Minimize(cp_model.LinearExpr.WeightedSum(terms, coefs))
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.linearization_level = 2
    solver.parameters.max_time_in_seconds = float(time_limit)
    solver.parameters.random_seed = seed
    t1 = time.perf_counter()
    status = solver.Solve(cp)
    t2 = time.perf_counter()
    name = solver.StatusName(status)
    out = {"status": "optimal" if status == cp_model.OPTIMAL else ("limit" if status in (cp_model.FEASIBLE, cp_model.UNKNOWN) else name.lower()),
           "value": int(round(solver.ObjectiveValue())) if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
           "bound": int(round(solver.BestObjectiveBound())) if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
           "seconds": t2 - t0, "seconds_build": t1 - t0, "seconds_solve": t2 - t1, "encoding": encoding,
           "branches": int(solver.NumBranches()), "conflicts": int(solver.NumConflicts())}
    return out


def milp(instance, time_limit):
    """Minimise with the mixed-integer solver of HiGHS (``scipy.optimize.milp``): the programme of the
    pairwise relaxation with integral site marginals (branch and cut on the relaxation our leaves use)."""
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint
    from scipy.optimize import milp as scipy_milp
    from metricchain_eng.leafprod.lpbound import LPBound
    t0 = time.perf_counter()
    mod = instance if isinstance(instance, Model) else Model(instance)
    lp = LPBound(mod)
    integrality = np.zeros(len(lp.c))
    integrality[:mod.S] = 1
    t1 = time.perf_counter()
    try:
        res = scipy_milp(lp.c, constraints=LinearConstraint(lp.A, lp.b, lp.b), integrality=integrality,
                         bounds=Bounds(0, 1), options={"time_limit": float(time_limit), "disp": False, "mip_rel_gap": 0.0})
    except Exception as exc:                            # reported, never hidden
        return {"status": "error", "value": None, "seconds": time.perf_counter() - t0, "error": repr(exc)[:200]}
    t2 = time.perf_counter()
    optimal = res.status == 0 and res.x is not None
    value = None
    if res.x is not None:                               # the value of the state the solver returned, exactly
        x = [int(np.argmax(res.x[mod.koff[i]:mod.koff[i + 1]])) for i in range(mod.n)]
        value = mod.energy(x)
    return {"status": "optimal" if optimal else "limit", "value": value, "seconds": t2 - t0,
            "seconds_build": t1 - t0, "seconds_solve": t2 - t1, "highs_status": int(res.status),
            "reported_objective": None if res.x is None else float(res.fun),
            "nodes": int(getattr(res, "mip_node_count", -1) or -1)}


def brute(instance, max_states=1 << 24):
    t0 = time.perf_counter()
    res = exact.brute_force(instance, max_states)
    seconds = time.perf_counter() - t0
    if res is None:
        return {"status": "skipped", "value": None, "seconds": seconds}
    return {"status": "optimal", "value": res[0], "seconds": seconds, "states": res[2]}


def dp(instance, max_table=1 << 23):
    t0 = time.perf_counter()
    mod = instance if isinstance(instance, Model) else Model(instance)
    order, largest, total = exact.plan(mod)
    if largest > max_table:
        return {"status": "skipped", "value": None, "seconds": time.perf_counter() - t0, "largest_table": largest}
    res = exact.eliminate(mod, max_table, order)
    return {"status": "optimal", "value": res[0], "seconds": time.perf_counter() - t0, "largest_table": largest,
            "table_entries": total}


def plain_bnb(instance, time_limit, **options):
    res = produce(instance, time_limit=time_limit, certificate=False, **options)
    s = res.stats
    return {"status": "optimal" if res.status == "solved" else "limit", "value": res.L if res.status == "solved" else None,
            "seconds": s["time_total"], "nodes": s["nodes"], "leaf_boxes": s["leaf_boxes"],
            "leaf_certificates": s["leaf_certificates"], "depth": s["depth"], "best_bound": res.best_bound,
            "upper_bound": res.energy, "stop": s["stop"]}
