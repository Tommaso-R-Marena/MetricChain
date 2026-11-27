"""Baseline: toulbar2 (exact cost-function-network solver; MIT licence; via `pytoulbar2`).

toulbar2 is the established exact solver for pairwise discrete energy minimisation on
fixed-backbone rotamer problems.  It proves optimality by exhaustive branch and bound with soft
local consistencies, in 64-bit integer arithmetic, and emits **no independently checkable
certificate**: its answer is label **[H]** for us (a solver's claim), and is used (i) as a
fair speed baseline for the same published instance and (ii) as an independent oracle that our
certified optimum must agree with.

The instance handed to toulbar2 is exactly the published integer instance: every table is shifted
by its own minimum so that all costs are nonnegative integers (the sum of the shifts is added
back), so no rounding is involved on either side.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

from ..model import PairModel

__all__ = ["Toulbar2Result", "solve_gmec"]


@dataclass
class Toulbar2Result:
    energy_int: int            # optimum claimed by toulbar2, in units of 2**-scale_bits (exact integer)
    x: tuple
    seconds: float
    nodes: int | None
    backtracks: int | None
    version: str


def solve_gmec(model: PairModel, time_limit: int = 0, vac: int = 1, seed: int = 1) -> Toulbar2Result:
    """Minimum of the published integer instance according to toulbar2 (no certificate)."""
    import pytoulbar2

    offset = 0
    unary, pair = [], {}
    for u in model.unary:
        vals = [int(v) for v in u.tolist()]
        lo = min(vals)
        offset += lo
        unary.append([v - lo for v in vals])
    for key, t in model.pair.items():
        rows = [[int(v) for v in row] for row in t.tolist()]
        lo = min(min(r) for r in rows)
        offset += lo
        pair[key] = [v - lo for r in rows for v in r]
    ub = sum(max(u) for u in unary) + sum(max(t) for t in pair.values()) + 1
    cfn = pytoulbar2.CFN(ubinit=ub, resolution=0, vac=vac, seed=seed, verbose=-1)
    for i, k in enumerate(model.sizes):
        cfn.AddVariable(f"x{i}", range(k))
    for i, u in enumerate(unary):
        cfn.AddFunction([i], u)
    for (i, j), t in pair.items():
        cfn.AddFunction([i, j], t)
    t0 = time.perf_counter()
    res = cfn.Solve(timeLimit=time_limit)
    seconds = time.perf_counter() - t0
    if not res:
        raise RuntimeError("toulbar2 returned no solution (time limit or inconsistency)")
    x = tuple(int(a) for a in res[0])
    energy = int(round(res[1])) + offset
    if model.energy_int(x) != energy:
        raise RuntimeError("toulbar2's reported cost differs from the exact energy of its own solution")
    nodes = backtracks = None
    try:
        nodes, backtracks = int(cfn.GetNbNodes()), int(cfn.GetNbBacktracks())
    except Exception:  # noqa: BLE001  (statistics are optional)
        pass
    return Toulbar2Result(energy_int=energy, x=x, seconds=seconds, nodes=nodes, backtracks=backtracks,
                          version=getattr(pytoulbar2, "__version__", "1.4.0.3 (pip)"))
