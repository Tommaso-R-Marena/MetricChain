"""Analysis of one class table of a lattice chain: covering numbers and entropy numbers.

Shared by the local driver ``experiments/eng/chain_cover/run_lattice.py`` and by the Modal job
``modal_jobs/chain_cover_app.py`` so that both compute exactly the same thing.
"""
from __future__ import annotations

import json
import time
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

from .profile_cover import ClassTable, covering_number_P, farthest_point_traversal, net_bracket

L_VALUES = (Fr(1), Fr(1, 5))
EPS1_VALUES = (Fr(1, 20), Fr(1, 10), Fr(1, 4), Fr(1, 2))
DELTAS = (Fr(4), Fr(2), Fr(1), Fr(1, 2), Fr(1, 4))


def analyse_table(tab: ClassTable, solvers=("highs", "cpsat"), exact_nets: bool = True,
                  net_time_limit: float = 30.0, cover_time_limit: float | None = None,
                  cpsat_max_centres: int | None = None) -> dict:
    """All numbers reported for one chain length (see ``run_lattice.py`` for their definitions)."""
    n, N = tab.n_torsions, tab.n_beads
    t0 = time.time()
    row: dict = {"n_torsions": n, "n_beads": N, "conformations": tab.n_conformations,
                 "classes": tab.n_classes,
                 "rank": int(np.linalg.matrix_rank(tab.cumulative.astype(float))),
                 "max_pairs_in_cutoff": int(tab.hist.sum(axis=1).max()),
                 "max_gmin": int(tab.gmin.max()), "cover": {}, "entropy": {}}
    for L in L_VALUES:
        eps_list = [("0", Fr(0)), ("1", Fr(1))] + [(f"{e1}*N", e1 * N) for e1 in EPS1_VALUES]
        for label, eps in eps_list:
            r = covering_number_P(tab, L, eps, solvers=solvers, time_limit=cover_time_limit,
                                  cpsat_max_centres=cpsat_max_centres)
            row["cover"][f"L={L},eps={label}"] = {
                "N_cov": r.size, "lower_certified": r.lower, "lower_solver": r.lower_solver,
                "proved_optimal": r.proved, "exact_certified": r.exact_certified, "solvers": r.solvers,
                "lp_bound": round(r.lp_bound, 6), "reduced": [r.n_centres_reduced, r.n_elements_reduced],
                "centres_hist": [tab.hist[c].tolist() for c in r.centres]}
    dist = tab.l1_matrix()
    start = int(np.nonzero((tab.hist == 0).all(axis=1))[0][0])      # the all-trans class has no pair inside the cutoff
    _, radii = farthest_point_traversal(dist, start)
    for delta in DELTAS:
        thr = delta * N                                             # m(delta): covering radius < delta * N
        below = radii * thr.denominator < thr.numerator
        ent: dict = {"m_fpt": int(np.argmax(below)) + 1 if below.any() else None}
        if exact_nets:
            ent["net_closed_radius"] = net_bracket(dist, thr, time_limit=net_time_limit)
        row["entropy"][f"delta={delta}"] = ent
    row["seconds"] = round(time.time() - t0, 2)
    return row


def merge_rows(path: Path, rows: list[dict], s_cut: int) -> None:
    """Merge rows (keyed by chain length) into the JSON result file."""
    existing = json.loads(path.read_text()) if path.exists() else {"rows": []}
    merged = {r["n_torsions"]: r for r in existing["rows"]}
    merged.update({r["n_torsions"]: r for r in rows})
    path.write_text(json.dumps({"model": "diamond lattice, self-avoiding, homopolymer", "s_cut": s_cut,
                                "known_part": "#gauche (e = 1)", "residual": "zero",
                                "rows": [merged[k] for k in sorted(merged)]}, indent=1) + "\n")


def format_row(row: dict) -> str:
    c = row["cover"]

    def cell(key: str) -> str:
        v = c[key]
        lo = max(v.get("lower_certified", v["N_cov"]), v.get("lower_solver", v["N_cov"])) if not v["proved_optimal"] else v["N_cov"]
        return f"{v['N_cov']}" if lo == v["N_cov"] else f"[{lo},{v['N_cov']}]"

    return (f"n={row['n_torsions']:2d} N={row['n_beads']:2d} confs={row['conformations']:>14d} classes={row['classes']:5d} rank={row['rank']} | "
            f"L=1: eps0={cell('L=1,eps=0')} eps1={cell('L=1,eps=1')} "
            + " ".join(f"{e1}N={cell(f'L=1,eps={e1}*N')}" for e1 in EPS1_VALUES)
            + f" | L=1/5: eps0={cell('L=1/5,eps=0')} eps1={cell('L=1/5,eps=1')} "
            + " ".join(f"{e1}N={cell(f'L=1/5,eps={e1}*N')}" for e1 in EPS1_VALUES)
            + f" | {row['seconds']}s")
