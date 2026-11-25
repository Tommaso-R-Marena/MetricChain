"""Profile classes of lattice chains and exact covering numbers in the profile format.

Independent implementation, from the definitions in docs/workstreams/P_REPORT.md (sections 0,
2.2 and 3.3) and docs/THEORY_REPORT.md section 11.17, of the quantities asked for in
THY-REQ-0002:

* a *profile class* is the set of conformations with the same pair-count vector
  ``h = (h_1, ..., h_D)``, ``h_k`` = number of pairs (p, q), q - p >= 3, at the k-th squared
  distance ``s_k < S_c``;
* the cumulative profile is the step function ``N(s) = sum_{k : s_k <= s} h_k`` on ``[0, S_c)``,
  and ``||N^x - N^y||_1 = sum_k w_k |C^x_k - C^y_k|`` with ``C_k = h_1 + ... + h_k`` and cell
  widths ``w_k = s_{k+1} - s_k`` (``s_{D+1} = S_c``) -- an integer for lattice chains;
* the profile envelope is ``d_P(x, y) = L ||N^x - N^y||_1``  (Lean: ``pairRes_sub_le``);
* **format P** (first-order class of ``d_P``), known part ``f = e * #gauche``, zero residual:
  a set ``A`` of evaluated conformations is a cover iff every conformation ``y`` has an
  ``a in A`` with ``d_P(a, y) <= gap(y) + eps``, ``gap(y) = e * #gauche(y)`` (theory report
  Theorem 11.4; Lean: ``isCertificate_iff_cover``).  The condition depends on ``y`` only through
  its class and its gauche count, so the binding member of a class is one with the fewest
  gauche torsions (``gmin``), and the covering number is a minimum set cover *on classes*.

All cover relations are decided in exact rational arithmetic (``fractions.Fraction``); only the
integer programme that minimises the cover uses a solver, and two independent solvers are
available (HiGHS through SciPy, CP-SAT through OR-Tools).
"""
from __future__ import annotations

import dataclasses
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np


@dataclasses.dataclass(frozen=True)
class ClassTable:
    """Profile classes of one chain model at one chain length."""

    n_torsions: int
    s_cut: int
    distances: tuple[int, ...]          # squared distances below the cutoff, ascending
    hist: np.ndarray                    # (classes, D) pair counts per distance
    count: np.ndarray                   # (classes,) number of conformations (Python ints, object dtype)
    gmin: np.ndarray                    # (classes,) smallest gauche count
    count_gmin: np.ndarray              # (classes,) conformations attaining gmin
    gmax: np.ndarray                    # (classes,) largest gauche count

    @property
    def n_beads(self) -> int:
        return self.n_torsions + 3

    @property
    def n_classes(self) -> int:
        return int(self.hist.shape[0])

    @property
    def n_conformations(self) -> int:
        return int(sum(int(c) for c in self.count))

    @property
    def widths(self) -> np.ndarray:
        """Cell widths ``w_k = s_{k+1} - s_k`` with ``s_{D+1} = S_c``."""
        edges = list(self.distances) + [self.s_cut]
        return np.array([edges[k + 1] - edges[k] for k in range(len(self.distances))], dtype=np.int64)

    @property
    def cumulative(self) -> np.ndarray:
        """Cumulative profiles ``C_k = h_1 + ... + h_k`` (classes, D)."""
        return np.cumsum(self.hist, axis=1)

    def l1_matrix(self) -> np.ndarray:
        """``||N^a - N^c||_1`` for all pairs of classes: exact integers, shape (classes, classes)."""
        c = self.cumulative.astype(np.int64)
        w = self.widths
        out = np.zeros((c.shape[0], c.shape[0]), dtype=np.int64)
        for k in range(c.shape[1]):
            out += w[k] * np.abs(c[:, k][:, None] - c[:, k][None, :])
        return out

    def l1_norms(self) -> np.ndarray:
        return (self.cumulative.astype(np.int64) * self.widths[None, :]).sum(axis=1)


def parse_enum_output(text: str) -> ClassTable:
    """Parse the text written by ``dia_enum`` (or a merge of several split runs)."""
    n_torsions = s_cut = None
    distances: tuple[int, ...] | None = None
    rows: dict[tuple[int, ...], list[int]] = {}
    for line in text.splitlines():
        if line.startswith("# dia_enum"):
            fields = dict(tok.split("=") for tok in line.split()[2:])
            nt, sc = int(fields["n_torsions"]), int(fields["s_cut"])
            if n_torsions is not None and (nt, sc) != (n_torsions, s_cut):
                raise ValueError("merging outputs of different models")
            n_torsions, s_cut = nt, sc
        elif line.startswith("# distances"):
            d = tuple(int(t) for t in line.split()[2:])
            if distances is not None and d != distances:
                raise ValueError("merging outputs with different distance classes")
            distances = d
        elif line.startswith("#") or not line.strip():
            continue
        else:
            vals = [int(t) for t in line.split()]
            assert distances is not None
            D = len(distances)
            key = tuple(vals[:D])
            count, gmin, count_gmin, gmax = vals[D:]
            if key not in rows:
                rows[key] = [count, gmin, count_gmin, gmax]
            else:                                   # merge split runs
                r = rows[key]
                r[0] += count
                if gmin < r[1]:
                    r[1], r[2] = gmin, count_gmin
                elif gmin == r[1]:
                    r[2] += count_gmin
                r[3] = max(r[3], gmax)
    if n_torsions is None or distances is None or s_cut is None:
        raise ValueError("no dia_enum header found")
    keys = sorted(rows)
    return ClassTable(
        n_torsions=n_torsions,
        s_cut=s_cut,
        distances=distances,
        hist=np.array(keys, dtype=np.int64).reshape(len(keys), len(distances)),
        count=np.array([rows[k][0] for k in keys], dtype=object),
        gmin=np.array([rows[k][1] for k in keys], dtype=np.int64),
        count_gmin=np.array([rows[k][2] for k in keys], dtype=object),
        gmax=np.array([rows[k][3] for k in keys], dtype=np.int64),
    )


def run_enumerator(binary: str | Path, n_torsions: int, s_cut: int = 12,
                   extra: Sequence[str] = ()) -> ClassTable:
    out = subprocess.run([str(binary), "-n", str(n_torsions), "-c", str(s_cut), *extra],
                         check=True, capture_output=True, text=True).stdout
    return parse_enum_output(out)


# --------------------------------------------------------------------------- format P

def cover_matrix_P(tab: ClassTable, L: Fraction, eps: Fraction, e: Fraction = Fraction(1)) -> np.ndarray:
    """Boolean matrix ``M[a, c]``: an evaluation in class ``a`` covers every member of class ``c``.

    Condition (exact):  ``L * ||N^a - N^c||_1  <=  e * gmin(c) + eps``.
    """
    L, eps, e = Fraction(L), Fraction(eps), Fraction(e)
    den = L.denominator * eps.denominator * e.denominator
    lhs_scale = L.numerator * (den // L.denominator)               # integer: L * den
    e_scale = e.numerator * (den // e.denominator)                 # integer: e * den
    eps_scale = eps.numerator * (den // eps.denominator)           # integer: eps * den
    dist = tab.l1_matrix()
    # exact integer comparison; guard against int64 overflow before using machine integers
    bound = max(abs(lhs_scale) * int(dist.max(initial=0)), abs(e_scale) * int(tab.gmin.max(initial=0)) + abs(eps_scale))
    if bound >= 2 ** 62:
        rhs = e_scale * tab.gmin.astype(object) + eps_scale
        return np.asarray((lhs_scale * dist.astype(object)) <= rhs[None, :], dtype=bool)
    rhs = e_scale * tab.gmin.astype(np.int64) + eps_scale
    return (lhs_scale * dist) <= rhs[None, :]


def reduce_cover(M: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Standard exact reductions of a set-cover instance (rows = centres, columns = elements).

    Drops elements whose covering set contains that of another element (they are then covered
    automatically) and centres whose covered set is contained in that of another centre.
    Returns (reduced matrix, kept centre indices, kept element indices).
    """
    M = np.asarray(M, dtype=bool)
    if max(M.shape) >= 2 ** 24:
        raise ValueError("instance too large for the float32 inclusion test")
    rows = np.arange(M.shape[0])
    cols = np.arange(M.shape[1])
    changed = True
    while changed:
        changed = False
        # element c is redundant if some other element c' has cover(c') subset of cover(c)
        colsets = M.T.astype(np.float32)                      # counts < 2**24: exact in float32
        inter = np.rint(colsets @ colsets.T).astype(np.int64) # |cover(c) & cover(c')|
        size = M.T.sum(axis=1).astype(np.int64)
        sub = inter == size[None, :]                          # sub[c, c']: cover(c') subset of cover(c)
        np.fill_diagonal(sub, False)
        keep = np.ones(M.shape[1], dtype=bool)
        for c in range(M.shape[1]):
            if not keep[c]:
                continue
            dom = np.nonzero(sub[c] & keep)[0]
            for c2 in dom:
                # ties (identical covering sets): keep the smaller index
                if size[c2] < size[c] or c2 < c:
                    keep[c] = False
                    break
        if not keep.all():
            M, cols, changed = M[:, keep], cols[keep], True
        # centre a is redundant if some other centre covers a superset
        rowsets = M.astype(np.float32)
        inter = np.rint(rowsets @ rowsets.T).astype(np.int64)
        size = M.sum(axis=1).astype(np.int64)
        sub = inter == size[:, None]                          # sub[a, a']: covered(a) subset of covered(a')
        np.fill_diagonal(sub, False)
        keep = np.ones(M.shape[0], dtype=bool)
        for a in range(M.shape[0]):
            if not keep[a]:
                continue
            dom = np.nonzero(sub[a] & keep)[0]
            for a2 in dom:
                if size[a2] > size[a] or a2 < a:
                    keep[a] = False
                    break
        if not keep.all():
            M, rows, changed = M[keep, :], rows[keep], True
    return M, rows, cols


def min_cover_highs(M: np.ndarray, time_limit: float | None = None) -> tuple[int, list[int], bool, float]:
    """Minimum set cover by HiGHS (SciPy ``milp``).

    Returns (size of the best cover found, its centres, optimality proved, solver's lower bound).
    """
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import csr_matrix

    M = np.asarray(M, dtype=bool)
    nA, nC = M.shape
    if not M.any(axis=0).all():
        raise ValueError("some element cannot be covered")
    cons = LinearConstraint(csr_matrix(M.T.astype(float)), lb=np.ones(nC), ub=np.inf)
    opts = {"mip_rel_gap": 0.0, "presolve": True}
    if time_limit is not None:
        opts["time_limit"] = time_limit
    res = milp(c=np.ones(nA), constraints=cons, integrality=np.ones(nA), bounds=Bounds(0, 1), options=opts)
    if res.x is None:
        raise RuntimeError(f"HiGHS returned no solution: {res.message}")
    chosen = [int(i) for i in np.nonzero(res.x > 0.5)[0]]
    if not M[chosen].any(axis=0).all():
        raise RuntimeError("HiGHS solution is not a cover")
    bound = float(getattr(res, "mip_dual_bound", len(chosen) if res.status == 0 else 0.0))
    return len(chosen), chosen, bool(res.status == 0), bound


def min_cover_cpsat(M: np.ndarray, time_limit: float | None = None, workers: int = 8) -> tuple[int, list[int], bool, float]:
    """Minimum set cover by OR-Tools CP-SAT.  Returns (size, centres, optimality proved, lower bound)."""
    from ortools.sat.python import cp_model

    M = np.asarray(M, dtype=bool)
    nA, nC = M.shape
    model = cp_model.CpModel()
    x = [model.NewBoolVar(f"x{a}") for a in range(nA)]
    for c in range(nC):
        centres = np.nonzero(M[:, c])[0]
        if len(centres) == 0:
            raise ValueError("some element cannot be covered")
        model.AddBoolOr([x[int(a)] for a in centres])
    model.Minimize(sum(x))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    if time_limit is not None:
        solver.parameters.max_time_in_seconds = time_limit
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(f"CP-SAT status {solver.StatusName(status)}")
    chosen = [a for a in range(nA) if solver.Value(x[a])]
    if not M[chosen].any(axis=0).all():
        raise RuntimeError("CP-SAT solution is not a cover")
    return len(chosen), chosen, status == cp_model.OPTIMAL, float(solver.BestObjectiveBound())


def certified_lower_bound(M: np.ndarray, M_reduced: np.ndarray, cols: np.ndarray) -> int:
    """Lower bound on the minimum cover of ``M`` that does not depend on any solver tolerance.

    The dual of the covering LP on the reduced instance is solved in floating point; its
    solution ``y >= 0`` (one weight per element) is truncated to integers ``floor(y * 2**40)``,
    extended by zeros to the elements removed by the reductions, and the quantity
    ``lam = max_a sum_{c covered by a} y_c`` is evaluated in exact integer arithmetic on the
    *unreduced* matrix.  Then ``y / lam`` is dual feasible for ``M``, so every cover of ``M`` has
    at least ``ceil(sum(y) / lam)`` centres -- whatever the solver or the reductions did.
    """
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix

    R = np.asarray(M_reduced, dtype=bool)
    res = linprog(c=np.ones(R.shape[0]), A_ub=-csr_matrix(R.T.astype(float)), b_ub=-np.ones(R.shape[1]),
                  bounds=(0, 1), method="highs")
    if res.status != 0:
        return 1
    y_red = np.maximum(-np.asarray(res.ineqlin.marginals, dtype=float), 0.0)
    y = np.zeros(M.shape[1], dtype=object)
    for c, v in zip(cols, y_red):
        y[int(c)] = int(v * (1 << 40))                       # truncation keeps y >= 0
    total = int(sum(int(v) for v in y))
    if total == 0:
        return 1
    Mi = np.asarray(M, dtype=bool)
    lam = 0
    nz = np.nonzero(np.array([int(v) > 0 for v in y]))[0]
    ynz = np.array([int(y[i]) for i in nz], dtype=object)
    sub = Mi[:, nz]
    for a in range(Mi.shape[0]):                             # exact integer row sums
        sa = int(sum(int(v) for v in ynz[sub[a]]))
        if sa > lam:
            lam = sa
    if lam == 0:
        return 1
    return max(1, (total + lam - 1) // lam)


def lp_cover_bound(M: np.ndarray) -> float:
    """Value of the linear relaxation (fractional covering number) -- a lower bound."""
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix

    M = np.asarray(M, dtype=bool)
    res = linprog(c=np.ones(M.shape[0]), A_ub=-csr_matrix(M.T.astype(float)), b_ub=-np.ones(M.shape[1]),
                  bounds=(0, 1), method="highs")
    return float(res.fun)


def greedy_cover(M: np.ndarray) -> list[int]:
    M = np.asarray(M, dtype=bool)
    uncovered = np.ones(M.shape[1], dtype=bool)
    chosen: list[int] = []
    while uncovered.any():
        gains = (M & uncovered[None, :]).sum(axis=1)
        a = int(np.argmax(gains))
        if gains[a] == 0:
            raise ValueError("some element cannot be covered")
        chosen.append(a)
        uncovered &= ~M[a]
    return chosen


@dataclasses.dataclass
class CoverResult:
    size: int                          # size of the best verified cover (an upper bound, and the value if exact)
    lower: int                         # certified lower bound (rational dual certificate; see certified_lower_bound)
    lower_solver: int                  # best lower bound reported by a solver (>= lower when a solver proved more)
    centres: list[int]                 # indices of classes (in the ClassTable) of the best cover
    proved: bool                       # size == max(lower, lower_solver)
    exact_certified: bool              # size == lower: optimality independent of solver tolerances
    solvers: dict[str, int]            # solver name -> size found
    lp_bound: float
    n_centres_reduced: int
    n_elements_reduced: int


def covering_number_P(tab: ClassTable, L, eps, e=1, solvers: Iterable[str] = ("highs", "cpsat"),
                      time_limit: float | None = None, cpsat_max_centres: int | None = None) -> CoverResult:
    """``N^P_cov`` for known part ``e * #gauche`` and zero residual (see module docstring).

    The returned cover is verified on the unreduced instance, and ``lower`` is a certified lower
    bound, so ``[lower, size]`` is a rigorous bracket; it is a single value when a solver proves
    optimality within ``time_limit`` (per solver).  CP-SAT is skipped on reduced instances with
    more than ``cpsat_max_centres`` centres.
    """
    import math

    M = cover_matrix_P(tab, Fraction(L), Fraction(eps), Fraction(e))
    assert M.diagonal().all(), "a class always covers itself"
    R, rows, cols = reduce_cover(M)
    lower = certified_lower_bound(M, R, cols)
    greedy = [int(rows[i]) for i in greedy_cover(R)]
    best = greedy
    sizes: dict[str, int] = {"greedy": len(greedy)}
    lower_solver = lower
    for name in solvers:
        if len(best) == max(lower, lower_solver):
            break                                              # already optimal
        if name == "cpsat" and cpsat_max_centres is not None and R.shape[0] > cpsat_max_centres:
            continue
        fn = {"highs": min_cover_highs, "cpsat": min_cover_cpsat}[name]
        try:
            size, chosen, ok, bound = fn(R, time_limit=time_limit)
        except RuntimeError:
            continue
        sizes[name] = size
        centres = [int(rows[i]) for i in chosen]
        if len(centres) < len(best):
            best = centres
        lower_solver = max(lower_solver, math.ceil(bound - 1e-6), size if ok else 0)
    assert M[best].any(axis=0).all(), "solution must cover the unreduced instance"
    lower_solver = min(lower_solver, len(best))
    return CoverResult(size=len(best), lower=lower, lower_solver=lower_solver, centres=best,
                       proved=len(best) == max(lower, lower_solver), exact_certified=len(best) == lower,
                       solvers=sizes, lp_bound=lp_cover_bound(R),
                       n_centres_reduced=R.shape[0], n_elements_reduced=R.shape[1])


# --------------------------------------------------------------------------- entropy of the profile set

def farthest_point_traversal(dist: np.ndarray, start: int = 0) -> tuple[list[int], np.ndarray]:
    """Greedy farthest-point order and the covering radius after each added point.

    ``radii[m - 1]`` is the covering radius of the first ``m`` points.  The traversal is the one
    used in P_REPORT section 3.2 for ``m(delta)`` (smallest ``m`` with covering radius < delta).
    """
    n = dist.shape[0]
    order = [start]
    d = dist[start].astype(np.int64).copy()
    radii = [int(d.max())]
    while radii[-1] > 0 and len(order) < n:
        nxt = int(np.argmax(d))
        order.append(nxt)
        d = np.minimum(d, dist[nxt])
        radii.append(int(d.max()))
    return order, np.array(radii, dtype=np.int64)


def net_bracket(dist: np.ndarray, radius, time_limit: float = 30.0) -> dict:
    """Internal covering number of a finite metric space at a closed radius, as a rigorous bracket.

    ``upper`` is the size of a verified cover, ``lower`` a certified lower bound (rational dual
    certificate) or the optimum when HiGHS proves it within ``time_limit``; ``exact`` whether the
    two coincide.
    """
    import math

    r = Fraction(radius)
    M = np.asarray((dist.astype(np.int64) * r.denominator) <= r.numerator, dtype=bool)
    R, rows, cols = reduce_cover(M)
    upper = len(greedy_cover(R))
    lower = certified_lower_bound(M, R, cols)
    if lower < upper:
        try:
            size, _, ok, bound = min_cover_highs(R, time_limit=time_limit)
            upper = min(upper, size)
            lower = max(lower, min(upper, math.ceil(bound - 1e-6)), size if ok else 0)
        except RuntimeError:
            pass
    return {"lower": int(lower), "upper": int(upper), "exact": lower == upper}
