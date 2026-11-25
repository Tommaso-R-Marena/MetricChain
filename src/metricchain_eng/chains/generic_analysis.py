"""Covering numbers of the generic (off-lattice) chain in the profile format.

Same question as ``lattice_analysis`` (THY-REQ-0002, question 1) for the model "gen" of
P_REPORT section 0.  Floating point throughout; every cover is verified on the unreduced
instance and every lower bound is the certified one of ``profile_cover.certified_lower_bound``
(or a solver's proof), so each cell is a bracket ``[lower, upper]`` relative to the cover
relation as decided with tolerance ``generic_chain.TOL``.  ``nearest_tie`` is the smallest
distance of an off-diagonal comparison from equality.
"""
from __future__ import annotations

import math
import time
from fractions import Fraction as Fr

import numpy as np

from .generic_chain import TOL, GenericClassTable, enumerate_generic
from .profile_cover import certified_lower_bound, greedy_cover, min_cover_highs, reduce_cover

L_VALUES = (Fr(1), Fr(1, 5))
EPS1_VALUES = (Fr(1, 20), Fr(1, 10), Fr(1, 4), Fr(1, 2))


def cover_bracket(M: np.ndarray, time_limit: float) -> dict:
    R, rows, cols = reduce_cover(M)
    lower = certified_lower_bound(M, R, cols)
    best = [int(rows[i]) for i in greedy_cover(R)]
    proved = len(best) == lower
    if not proved:
        try:
            size, chosen, ok, bound = min_cover_highs(R, time_limit=time_limit)
            if size < len(best):
                best = [int(rows[i]) for i in chosen]
            lower = max(lower, min(len(best), math.ceil(bound - 1e-6)), len(best) if ok else 0)
        except RuntimeError:
            pass
    assert M[best].any(axis=0).all()
    return {"lower": int(lower), "upper": len(best), "exact": lower == len(best),
            "reduced": [int(R.shape[0]), int(R.shape[1])]}


def analyse_generic(n: int, cover_time_limit: float = 300.0, tab: GenericClassTable | None = None) -> dict:
    t0 = time.time()
    tab = enumerate_generic(n) if tab is None else tab
    N = tab.n_beads
    D = tab.l1_matrix(chunk=max(1, int(2e8 // (tab.n_classes * tab.n_pairs * 8)) or 1))
    row = {"n_torsions": n, "n_beads": N, "conformations": int(tab.n_conformations), "classes": tab.n_classes,
           "min_core_margin": tab.min_core_margin, "min_rejected_margin": tab.min_rejected_margin,
           "max_pairs_below_cutoff_per_bead": max(len(v) for v in tab.below) / N,
           "enumeration_seconds": round(time.time() - t0, 1), "cover": {}}
    g = tab.gmin[None, :].astype(np.float64)
    off = ~np.eye(tab.n_classes, dtype=bool)
    for L in L_VALUES:
        for label, eps in [("0", Fr(0)), ("1", Fr(1))] + [(f"{e1}*N", e1 * N) for e1 in EPS1_VALUES]:
            slack = g + float(eps) - float(L) * D
            cell = cover_bracket(slack >= -TOL, cover_time_limit)
            cell["nearest_tie"] = float(np.abs(slack[off]).min()) if off.any() else None
            row["cover"][f"L={L},eps={label}"] = cell
    row["seconds"] = round(time.time() - t0, 1)
    return row
