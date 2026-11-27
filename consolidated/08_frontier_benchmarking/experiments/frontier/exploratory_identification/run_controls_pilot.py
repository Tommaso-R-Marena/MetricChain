#!/usr/bin/env python3
"""EXPLORATORY pilot of protocol FB-P-04 (assessment class A-EXP, stage "development").

Input: the ensemble division's planted-truth controls (`controls_v1.json`, pinned commit).
Only the controls on a FINITE space with LINEAR averaged data are used here (B1-01, B1-02,
B2-01, B2-02, B2-03, B4-01, B5-01, B5-02, B5-03); the geometric, torus, thermal and noise
controls need their own forward maps and are left to the full protocol.

Two things are done, and kept apart:

(1) REPLICATION, by code written here from the definitions (not from the division's
    generator): the published data are recomputed in exact rational arithmetic; the
    published certificates are checked in exact arithmetic; the verdict IDENTIFIED / NOT
    IDENTIFIED is re-derived by a linear programme (floating point, HiGHS) plus an exact rank
    test; the published intervals are recomputed by linear programming.

(2) BASELINES of the kind practitioners use, run on the same data from a uniform prior over
    the stated space: maximum-entropy reweighting (the dual problem of Bayesian/maximum-entropy
    reweighting with a small regularisation), and non-negative least squares (a "minimal
    ensemble").  Each returns ONE ensemble.  We record how far that ensemble is from the
    planted one (total variation) and how well it fits the data — on instances where the
    planted truth is, by construction, not determined by the data.

The baselines are our own few-line implementations of the published algorithms, not the
established packages: this is a pilot, labelled as such, and the full protocol names the
packages to be run by the engineering division.

usage: run_controls_pilot.py CONTROLS_JSON OUT_JSON
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog, minimize, nnls

LINEAR_FINITE = ["B1-01", "B1-02", "B2-01", "B2-02", "B2-03", "B4-01", "B5-01", "B5-02", "B5-03"]


def frac(x) -> Fraction:
    return Fraction(x) if not isinstance(x, (int, float)) else Fraction(x)


def exact_rank(rows) -> int:
    """Rank of a matrix of Fractions by exact Gaussian elimination."""
    m = [list(r) for r in rows]
    rank, col, ncols = 0, 0, len(m[0]) if m else 0
    while rank < len(m) and col < ncols:
        pivot = next((r for r in range(rank, len(m)) if m[r][col] != 0), None)
        if pivot is None:
            col += 1
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        for r in range(rank + 1, len(m)):
            if m[r][col] != 0:
                factor = m[r][col] / m[rank][col]
                m[r] = [a - factor * b for a, b in zip(m[r], m[rank])]
        rank += 1
        col += 1
    return rank


def lp(c, A_eq, b_eq, A_ub=None, b_ub=None):
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=(0, None), method="highs")
    if res.status != 0:
        raise RuntimeError(f"linear programme failed: {res.message}")
    return res.fun, res.x


def max_entropy(Phi, y, theta=1e-6):
    """Maximum-entropy reweighting of a uniform prior: minimise over lambda
    log Z(lambda) + lambda.y + (theta/2)|lambda|^2 with w(x) ~ exp(-lambda.Phi(x))."""
    def gamma(lam):
        a = -Phi.T @ lam
        m = a.max()
        logz = m + np.log(np.exp(a - m).sum())
        w = np.exp(a - m)
        w /= w.sum()
        return logz + lam @ y + 0.5 * theta * lam @ lam, y - Phi @ w + theta * lam
    res = minimize(gamma, np.zeros(Phi.shape[0]), jac=True, method="L-BFGS-B", options={"maxiter": 20000})
    a = -Phi.T @ res.x
    w = np.exp(a - a.max())
    return w / w.sum()


def tv(p, q) -> float:
    return 0.5 * float(np.abs(np.asarray(p) - np.asarray(q)).sum())


def main() -> int:
    controls = {c["id"]: c for c in json.load(open(sys.argv[1]))["controls"]}
    out = []
    for cid in LINEAR_FINITE:
        c = dict(controls[cid])
        base = controls["B5-01"]               # B5-02 and B5-03 say "the same data" and omit what they share
        if cid in ("B5-02", "B5-03"):
            if not isinstance(c.get("space", {}).get("states"), list):
                c["space"] = base["space"]
            if not isinstance(c.get("observables", {}).get("table"), list):
                c["observables"] = base["observables"]
            if "data" not in c:
                c["data"] = base["data"]
        states = c["space"]["states"]
        if isinstance(c["observables"].get("table"), list):
            table = [[frac(v) for v in row] for row in c["observables"]["table"]]
        else:
            # B4-01 describes its space and observables in words: the cube modulo the global flip
            # (first sign +) with all pair products x_i x_j, i < j, in lexicographic order.
            m = len(c["ensemble"]["support"][0])
            states = ["+" + "".join("+" if not (v >> (m - 2 - j)) & 1 else "-" for j in range(m - 1)) for v in range(2 ** (m - 1))]
            sign = lambda s, i: Fraction(1) if s[i] == "+" else Fraction(-1)
            table = [[sign(s, i) * sign(s, j) for s in states] for i in range(m) for j in range(i + 1, m)]
        n, k = len(states), len(table)
        Phi = np.array([[float(v) for v in row] for row in table])
        rec = {"id": cid, "family": c["family"], "states": n, "observables": k, "expected": c["expected"].get("verdict")}
        planted = None
        if "ensemble" in c:
            raw = c["ensemble"]["weights"]
            if isinstance(raw, str):            # "any positive weights": we choose some, recorded in the output
                raw = ["2/5", "3/10", "1/5", "1/10"][:len(c["ensemble"]["support"])]
                rec["weights_chosen_by_us"] = raw
            weights = dict(zip(c["ensemble"]["support"], (frac(w) for w in raw)))
            planted_exact = [weights.get(s, Fraction(0)) for s in states]
            planted = np.array([float(w) for w in planted_exact])
            data_exact = [sum(t * w for t, w in zip(row, planted_exact)) for row in table]
        if "data" in c:
            published = [frac(v) for v in c["data"]]
            if planted is not None:
                rec["data_recomputed_exactly_equal"] = (published == data_exact)
            data_exact = published
        y = np.array([float(v) for v in data_exact])
        A = np.vstack([np.ones(n), Phi])
        b = np.concatenate([[1.0], y])
        tol = c.get("tolerance", 0)
        tol = float(frac(tol["tau"] if isinstance(tol, dict) else tol))

        # ---- (1) replication ------------------------------------------------------------
        if planted is not None:
            support = [i for i, w in enumerate(planted) if w > 0]
            cols = [[Fraction(1)] + [table[r][i] for r in range(k)] for i in support]
            independent = exact_rank(cols) == len(support)
            # widest range of any single population over all ensembles with the same data
            spread = 0.0
            for i in range(n):
                e = np.zeros(n)
                e[i] = 1.0
                lo, _ = lp(e, A, b)
                hi, _ = lp(-e, A, b)
                spread = max(spread, -hi - lo)
            identified = independent and spread < 1e-9
            rec.update({"support_columns_independent_exact": independent, "max_population_spread_lp": round(spread, 12),
                        "verdict_recomputed": "IDENTIFIED" if identified else "NOT IDENTIFIED"})
            cert = c["expected"].get("certificate")
            lam_key = next((key for key in cert if key.startswith("lambda") and isinstance(cert[key], list)), None) if isinstance(cert, dict) else None
            if lam_key:
                lam = [frac(v) for v in cert[lam_key]]
                f = [frac(cert["c"]) + sum(l * table[r][i] for r, l in enumerate(lam)) for i in range(n)]
                rec["certificate_checked_exactly"] = (all(v >= 0 for v in f)
                                                      and {i for i, v in enumerate(f) if v == 0} == set(support))
                if "gamma" in cert:
                    rec["certificate_gap_exact"] = str(min(v for v in f if v != 0))
                    rec["certificate_gap_published"] = cert["gamma"]
        if "interval" in c["expected"]:
            question = c["question"]
            if "x1*x2" in question:
                target = Phi[0] * Phi[1]
            else:                                   # population of the all-plus state
                target = np.array([1.0 if set(s) == {"+"} else 0.0 for s in states])
            if tol:
                A_ub = np.vstack([Phi, -Phi])
                b_ub = np.concatenate([y + tol, -(y - tol)])
                lo, _ = lp(target, np.ones((1, n)), [1.0], A_ub, b_ub)
                hi, _ = lp(-target, np.ones((1, n)), [1.0], A_ub, b_ub)
            else:
                lo, _ = lp(target, A, b)
                hi, _ = lp(-target, A, b)
            want = [float(frac(v)) for v in c["expected"]["interval"]]
            rec.update({"interval_recomputed": [round(lo, 10), round(-hi, 10)], "interval_published": c["expected"]["interval"],
                        "interval_agrees": abs(lo - want[0]) < 1e-8 and abs(-hi - want[1]) < 1e-8})

        # ---- (2) baselines --------------------------------------------------------------
        w_me = max_entropy(Phi, y)
        w_ls, _ = nnls(np.vstack([A, np.zeros((0, n))]) * 1.0, b)
        w_ls = w_ls / w_ls.sum() if w_ls.sum() > 0 else w_ls
        rec["maxent_data_misfit_max"] = float(np.abs(Phi @ w_me - y).max())
        rec["nnls_data_misfit_max"] = float(np.abs(Phi @ w_ls - y).max())
        rec["maxent_support_size"] = int((w_me > 1e-6).sum())
        rec["nnls_support_size"] = int((w_ls > 1e-9).sum())
        if planted is not None:
            rec["maxent_tv_to_planted"] = round(tv(w_me, planted), 6)
            rec["nnls_tv_to_planted"] = round(tv(w_ls, planted), 6)
        out.append(rec)
        print(json.dumps(rec, sort_keys=True))
    json.dump(out, open(sys.argv[2], "w"), indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
