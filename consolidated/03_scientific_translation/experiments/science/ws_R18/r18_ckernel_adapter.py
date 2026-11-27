"""R18 ADAPTER -- NOT THE ENGINEERING DIVISION'S FILE.

Written by workstream R18 of the science division (2026-11-26) for the re-run of
``recheck_classification.py`` and ``nonproduct_bound.py`` from a scratch copy.  Their ``ckernel.py``
(kept beside this file as ``ckernel_THEIRS_not_used.py.txt``) compiles ``meanrun_kernel.c`` on first
use; the brief of R18 forbids building the kernel ("Python reference only").  This module offers the
same class name and the same ``run`` signature, and evaluates every run with THEIR Python reference
``meanrun.mean_run`` (unmodified copy).  Nothing is compiled, no shared library is loaded.

What is theirs and what is mine in a re-run through this adapter:
  theirs  the two scripts, ``run_search.design_params``, ``adversary.Family``, ``alg2l`` (constants,
          inner costs, C_max), ``tables``, ``meanrun.mean_run`` and ``meanrun.rung_positions``;
  mine    this file: the plumbing below, and for ``t0_range`` the substitution of the pair for
          ``inst.t0`` in the one call of ``rung_positions`` that ``mean_run`` makes -- which is what
          their ``ckernel.Evaluator.run`` does before it calls the kernel
          (``rung_positions(P, inst.t0 if t0_range is None else t0_range, oracle, positions, legacy)``).
"""
from __future__ import annotations

import math

import numpy as np

from . import meanrun as _mr
from .alg2l import Constants, Params, constants, inner_costs, lC_max
from .meanrun import Instance, Run
from .tables import TIE, CubeTables

_ORIG_RUNG_POSITIONS = _mr.rung_positions
N_RUNS = 0          # number of mean runs made through the adapter (printed by the R18 drivers)


def load_library(rebuild: bool = False):
    raise RuntimeError("R18 adapter: the C kernel is not built in this scratch copy")


class Evaluator:
    """Same interface as their ``ckernel.Evaluator``; every run is ``meanrun.mean_run``."""

    def __init__(self, P: Params, outer: CubeTables | None = None, *, lC: np.ndarray | None = None, harper: bool = True,
                 enforce_abort: bool = True, count_grid: tuple = (), tie: float = TIE):
        self.P = P
        self.outer = outer if outer is not None else CubeTables(P.n_o, P.u)
        self.C: Constants = constants(P, self.outer)
        self.count_grid = tuple(count_grid)
        self.harper, self.enforce_abort, self.tie = harper, enforce_abort, tie
        if P.n_i > 0:
            self.lC = np.ascontiguousarray(inner_costs(P, self.C) if lC is None else lC, dtype=np.float64)
            self.lCmax = lC_max(P, self.C, self.lC)
        else:
            self.lC = np.zeros(P.L + 1)
            self.lCmax = math.inf

    def run(self, inst: Instance, oracle: str = "bottom", record: bool = False, *, positions: tuple | None = None,
            legacy_classification: bool = False, t0_range: tuple | None = None) -> Run:
        global N_RUNS
        N_RUNS += 1
        kw = dict(C=self.C, lC=(self.lC if self.P.n_i > 0 else None), harper=self.harper, record=record,
                  count_grid=self.count_grid, enforce_abort=self.enforce_abort, tie=self.tie, positions=positions,
                  legacy_classification=legacy_classification)
        if t0_range is None:
            return _mr.mean_run(self.P, self.outer, inst, oracle, **kw)

        def _with_range(P, t0, oracle="bottom", positions=None, legacy_classification=False):
            return _ORIG_RUNG_POSITIONS(P, (float(t0_range[0]), float(t0_range[1])), oracle, positions, legacy_classification)

        _mr.rung_positions = _with_range
        try:
            return _mr.mean_run(self.P, self.outer, inst, oracle, **kw)
        finally:
            _mr.rung_positions = _ORIG_RUNG_POSITIONS
