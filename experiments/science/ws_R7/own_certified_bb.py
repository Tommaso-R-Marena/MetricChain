"""R7 OWN: a branch and bound for minimum set cover in which EVERY pruned node carries a tolerance-free certificate.

Purpose: 22 published lattice covering numbers (18 at n = 14..18, 4 at n >= 19) are optima only by a MILP solver's
branch and bound; the LP certificate is 1 or 2 below.  This script proves "no cover of size <= target-1 exists" for one
cell with exact arithmetic only:

  node = (set F1 of centres fixed in, set F0 of centres fixed out).
  bound(node) = |F1| + ceil( sum(w) / max_a load_a(w) ), where w >= 0 are INTEGER weights on the classes not covered by
      F1 (a floating-point dual LP solution, truncated), and load_a(w) = sum of w over the classes covered by centre a,
      maximised over the centres not in F0 and not in F1 -- evaluated in exact integer arithmetic.  By weak duality every
      cover of the residual instance that avoids F0 has at least sum(w)/max load centres, whatever the LP solver returned.
  A node is pruned if bound >= target, or if some uncovered class has no free centre (infeasible: checked exactly).
  Otherwise: branch on an uncovered class c with the fewest free covering centres a_1..a_k (ordered by LP value):
      child i fixes a_i in and a_1..a_{i-1} out.  The children partition the covers of the node (every cover contains
      some a_i; take the first).
  If the tree is exhausted without reaching a leaf where all classes are covered with |F1| <= target-1, then
  min cover >= target.  The only floating-point object is the dual vector, which is used as a hint.

Dominance reductions (exact, done once, with my own code): a centre whose covered set is contained in another centre's
may be removed (replace it by the other in any cover); a class whose set of covering centres contains that of another
class may be removed (it is covered whenever the other is).

   python3 own_certified_bb.py n "L=1,eps=1" [max_nodes] [max_seconds]
"""
import json
import math
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

import own_lattice_cert as lc


def reduce_instance(M):
    """Exact dominance reductions.  Returns reduced matrix and index maps."""
    M = M.copy()
    rows = np.arange(M.shape[0]); cols = np.arange(M.shape[1])
    changed = True
    while changed:
        changed = False
        # classes: drop c if cover(c) is a superset of cover(c') for another kept c'
        A = M.T.astype(np.int32)                       # (classes, centres)
        inter = A @ A.T
        size = A.sum(axis=1)
        keep = np.ones(len(cols), dtype=bool)
        for c in np.argsort(-size):                    # try to drop big ones first
            if not keep[c]:
                continue
            sub = (inter[c] == size) & keep            # cover(c') subset of cover(c)
            sub[c] = False
            # identical sets: keep the one with the smaller index
            ident = sub & (size == size[c])
            if (sub & ~ident).any() or (ident & (np.arange(len(cols)) < c)).any():
                keep[c] = False
        if not keep.all():
            M, cols, changed = M[:, keep], cols[keep], True
        # centres: drop a if covered(a) is a subset of covered(a') for another kept a'
        B = M.astype(np.int32)
        inter = B @ B.T
        size = B.sum(axis=1)
        keep = np.ones(len(rows), dtype=bool)
        for a in np.argsort(size):                     # try to drop small ones first
            if not keep[a]:
                continue
            sup = (inter[a] == size[a]) & keep         # covered(a) subset of covered(a')
            sup[a] = False
            ident = sup & (size == size[a])
            if (sup & ~ident).any() or (ident & (np.arange(len(rows)) < a)).any():
                keep[a] = False
        if not keep.all():
            M, rows, changed = M[keep, :], rows[keep], True
    return M, rows, cols


class CertifiedBB:
    def __init__(self, M, target, max_nodes=10 ** 6, max_seconds=600.0, den=1 << 24):
        self.M = M.astype(bool)
        self.Mi = M.astype(np.int64)
        self.target = target
        self.max_nodes, self.max_seconds, self.den = max_nodes, max_seconds, den
        self.nodes = self.pruned_bound = self.pruned_infeasible = self.leaves_cover = 0
        self.max_depth = 0
        self.t0 = time.time()
        self.incomplete = False
        self.found_cover = None

    def bound(self, free_rows, unc_cols):
        """(certified integer lower bound for the residual instance, LP primal hint x on free rows)."""
        R = self.M[np.ix_(free_rows, unc_cols)]
        res = linprog(c=-np.ones(len(unc_cols)), A_ub=csr_matrix(R.astype(np.float64)), b_ub=np.ones(len(free_rows)),
                      bounds=(0, None), method="highs")
        w = np.floor(np.maximum(res.x, 0.0) * self.den).astype(np.int64)
        load = self.Mi[np.ix_(free_rows, unc_cols)] @ w          # exact integers
        mx, tot = int(load.max()), int(w.sum())
        lb = 0 if mx == 0 else -((-tot) // mx)                   # ceil(tot / mx), exact
        x = -np.asarray(res.ineqlin.marginals)                   # primal hint
        return lb, x

    def solve(self, in_set, out_mask, covered):
        if self.incomplete:
            return
        self.nodes += 1
        self.max_depth = max(self.max_depth, len(in_set))
        if self.nodes > self.max_nodes or time.time() - self.t0 > self.max_seconds:
            self.incomplete = True
            return
        unc = np.nonzero(~covered)[0]
        if len(unc) == 0:
            if len(in_set) <= self.target - 1:
                self.found_cover = list(in_set)                  # a cover smaller than the target: the claim is false
                self.incomplete = True
            self.leaves_cover += 1
            return
        if len(in_set) >= self.target - 1:                       # one more centre would already reach the target... need >= 1 more
            self.pruned_bound += 1
            return
        free = np.nonzero(~out_mask)[0]
        free = free[~np.isin(free, in_set)] if in_set else free
        sub = self.M[np.ix_(free, unc)]
        cnt = sub.sum(axis=0)
        if (cnt == 0).any():                                     # some class cannot be covered any more (exact)
            self.pruned_infeasible += 1
            return
        lb, x = self.bound(free, unc)
        if len(in_set) + lb >= self.target:
            self.pruned_bound += 1
            return
        j = int(np.argmin(cnt))                                  # class with the fewest free covering centres
        cand = free[sub[:, j]]
        order = np.argsort(-x[sub[:, j]])                        # most LP-preferred centre first
        cand = cand[order]
        newly_out = []
        for a in cand:
            self.solve(in_set + [int(a)], out_mask, covered | self.M[a])
            out_mask[a] = True
            newly_out.append(a)
            if self.incomplete:
                break
        for a in newly_out:
            out_mask[a] = False


if __name__ == "__main__":
    n, key = int(sys.argv[1]), sys.argv[2]
    max_nodes = int(sys.argv[3]) if len(sys.argv) > 3 else 200000
    max_seconds = float(sys.argv[4]) if len(sys.argv) > 4 else 600.0
    res = json.loads((lc.ENG / "results" / "lattice_Sc12.json").read_text())
    cell = {r["n_torsions"]: r for r in res["rows"]}[n]["cover"][key]
    hist, count, gmin = lc.read_table(n)
    L, eps = lc.parse_key(key, n + 3)
    M = lc.cover_matrix(lc.l1_matrix(hist), gmin, L, eps)
    target = cell["N_cov"]
    R, rows, cols = reduce_instance(M)
    print(f"n={n} {key}: published N_cov = {target}; instance {M.shape} -> reduced {R.shape}", flush=True)
    sys.setrecursionlimit(10000)
    bb = CertifiedBB(R, target, max_nodes=max_nodes, max_seconds=max_seconds)
    bb.solve([], np.zeros(R.shape[0], dtype=bool), np.zeros(R.shape[1], dtype=bool))
    out = dict(n=n, key=key, target=target, reduced=list(R.shape), nodes=bb.nodes, pruned_by_certified_bound=bb.pruned_bound,
               pruned_infeasible=bb.pruned_infeasible, full_cover_leaves=bb.leaves_cover, max_depth=bb.max_depth,
               complete=not bb.incomplete, smaller_cover_found=bb.found_cover, seconds=round(time.time() - bb.t0, 1))
    out["conclusion"] = (f"PROVED with exact certificates: every cover has at least {target} centres" if not bb.incomplete
                         else ("REFUTED: a smaller cover exists" if bb.found_cover else "not finished within the limits"))
    print(out, flush=True)
    json.dump(out, open(f"out_own_certified_bb_n{n}.json", "w"), indent=1)
