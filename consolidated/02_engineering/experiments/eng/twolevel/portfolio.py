"""X-011c: designs against instances as a game — one design for all instances, or a portfolio of designs run under
doubling budgets.

A *design* is a nested run of Algorithm 2L+ fixed before any evaluation: which procedure serves which rung.  Two
ways of fixing it:

  "flat"       the referee's rule (theory branch, r8_flat3.py; ENG-RES-0014): a rung is served by the cheaper, *at the
               flat fibre*, of the base bracket and the referee's two-level candidates;
  "certified"  the rule of THY-RES-0013 §4: by certified cost (``certified.Search``, family "theory").

An *instance* here is the global cone psi(x) = s u |x| on the n-cube, 0 <= s <= 1 (s = 0: the flat instance).  It is
additive over coordinates, hence a product instance for every split of every level of every design — the only
family on which designs with different splits can be run on the *same* function with the present evaluator.  Base
brackets give their own answers (reading (B)).  Everything is in the mean-run model.

For a finite set of designs D and instances I the cost matrix c[d][i] gives

    min_d max_i c    what the best single design guarantees over I,
    max_i min_d c    what a portfolio pays on its worst instance, up to the factor of the dovetailing (ENG-RES-0015 §3),

and the first is never below the second.  ``python experiments/eng/twolevel/portfolio.py`` writes
``results/x011_portfolio.json``.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import nested_bench as nb  # noqa: E402
from metricchain_eng.twolevel import certified as cert  # noqa: E402
from metricchain_eng.twolevel.alg2l import constants  # noqa: E402
from metricchain_eng.twolevel.tables import LN2, cube_constants  # noqa: E402

SLOPES = (0.0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
PHIS = (0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15)


def k0_only(u: float):
    return lambda d, x, lid: cert.k0_lcost(d, u, x, lid)


def flat_tuned_tree(u: float, n: int, phi: float, lid: float = nb.LID) -> cert.LevelBound:
    """The referee's three-level design at outer fraction phi: every rung served by the cheaper *at the flat fibre* of
    the base bracket and the referee's two-level candidates.  Returned as a ``LevelBound`` whose ``lC`` and ``lCmax``
    are the *certified* values of the chosen servers (so ``lCmax`` is the certified bound of this design)."""
    cc = cube_constants(u)
    top = cert.top_design(phi)
    P = cert.level_params(u, n, top, lid)
    C = constants(P, cert.tables(P.n_o, u))

    def server(d: int, x: float, lidp: float):
        c0, kind0 = cert.k0_lcost(d, u, x, lidp)
        if x / d >= 0.9 * cc.eps_star or d < 50:
            return c0, kind0
        best = None
        for D in cert.referee_candidates(u, d, x):
            lb = cert.level_bound(u, d, D, lidp, k0_only(u))
            if lb is None or lb.xout > x + 1e-9:
                continue
            flat_cost = nb.level_on_cone(lb, u, 0.0, "k0", lidp)[0]
            if best is None or flat_cost < best[0]:
                best = (flat_cost, lb)
        if best is not None and best[0] < c0:
            return best[1].lCmax, best[1]
        return c0, kind0

    return cert.level_bound(u, n, top, lid, server)


def certified_tree(u: float, n: int, phi: float, k: int, family: str = "theory", lid: float = nb.LID) -> cert.LevelBound:
    return cert.Search(u, family).top(n, cert.top_design(phi), lid, k)


def cone_cost(tree: cert.LevelBound, u: float, slope: float, lid: float = nb.LID):
    lcost, alpha, beta, ok = nb.level_on_cone(tree, u, slope, "k0", lid)
    return lcost, ok


def matrix(u: float, n: int, phis=PHIS, slopes=SLOPES, levels=(1, 2, 3)) -> dict:
    na = n * cube_constants(u).a
    designs = []
    for phi in phis:
        designs.append((f"flat-tuned, three levels, phi={phi:g}", "flat", 2, phi, flat_tuned_tree(u, n, phi)))
        for k in levels:
            designs.append((f"certified, {k + 1} levels, phi={phi:g}", "certified", k, phi, certified_tree(u, n, phi, k)))
    rows = []
    for name, rule, k, phi, tree in designs:
        costs, oks = [], []
        for s in slopes:
            c, ok = cone_cost(tree, u, s)
            costs.append(c / na)
            oks.append(bool(ok))
        nested = sum(isinstance(sv, cert.LevelBound) for sv in tree.servers)
        rows.append(dict(name=name, rule=rule, nested_levels=k, phi=phi, certified=tree.lCmax / na, levels_used=tree.depth(),
                         rungs_served_by_nested_runs=nested, cost=costs, ok=oks))
    M = np.array([r["cost"] for r in rows])
    out = dict(u=u, n=n, a=cube_constants(u).a, slopes=list(slopes), rows=rows)

    def game(mask):
        sub = M[mask]
        names = [r["name"] for r, m in zip(rows, mask) if m]
        worst = sub.max(axis=1)
        i = int(np.argmin(worst))
        best_per_instance = sub.min(axis=0)
        j = int(np.argmax(best_per_instance))
        return dict(designs=int(mask.sum()), minmax=float(worst[i]), minmax_design=names[i], minmax_slope=slopes[int(np.argmax(sub[i]))],
                    maxmin=float(best_per_instance[j]), maxmin_slope=slopes[j], maxmin_design=names[int(np.argmin(sub[:, j]))],
                    best_at_flat=float(sub[:, 0].min()), best_at_flat_design=names[int(np.argmin(sub[:, 0]))],
                    dovetail_overhead=math.log(4 * mask.sum()) / na)

    rule = np.array([r["rule"] for r in rows])
    kk = np.array([r["nested_levels"] for r in rows])
    out["games"] = {"all designs": game(np.ones(len(rows), bool)),
                    "flat-tuned only": game(rule == "flat"),
                    "certified only": game(rule == "certified"),
                    "certified, three levels": game((rule == "certified") & (kk == 2)),
                    "two levels": game((rule == "certified") & (kk == 1))}
    return out


def check() -> int:
    """The flat-tuned trees against the referee's published table (three_levels.REFEREE): flat cost of three levels,
    the bound with flat middle costs is not reproduced here (this module charges certified costs), and the number
    of rungs served by the middle level."""
    import three_levels

    bad = 0
    for (u, n, phi), (two, three, _, served) in sorted(three_levels.REFEREE.items()):
        if n > 4000:
            continue
        tree = flat_tuned_tree(u, n, phi)
        na = n * cube_constants(u).a
        flat3 = cone_cost(tree, u, 0.0)[0] / na
        nserved = sum(isinstance(sv, cert.LevelBound) for sv in tree.servers)
        ok = abs(flat3 - three) < 6e-5 and nserved == served
        bad += not ok
        print(f"u={u} n={n} phi={phi}: three levels at the flat instance {flat3:.4f} (referee {three}); rungs served by the middle level "
              f"{nserved} (referee {served}) {'ok' if ok else 'DIFFERS'}")
    return bad


def main() -> int:
    if "--check" in sys.argv:
        return check()
    out = []
    for n in (1000, 4000, 16000):
        t0 = time.time()
        m = matrix(1.0, n)
        m["seconds"] = time.time() - t0
        out.append(m)
        g = m["games"]["all designs"]
        print(f"n={n}: min-max {g['minmax']:.4f} ({g['minmax_design']}); max-min {g['maxmin']:.4f} at slope {g['maxmin_slope']}; "
              f"best at flat {g['best_at_flat']:.4f} ({g['best_at_flat_design']})  [{m['seconds']:.0f} s]", flush=True)
    path = ROOT / "experiments" / "eng" / "twolevel" / "results" / "x011_portfolio.json"
    path.write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
