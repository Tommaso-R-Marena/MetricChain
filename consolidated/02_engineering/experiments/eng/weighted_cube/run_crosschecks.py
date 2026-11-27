"""Independent cross-checks of the vertex enumeration (results/crosschecks.json).

1. L <= 3, every chamber and the walls: five methods give the same vertex set (breadth-first search over the
   polytope graph, the same by orbits, depth-first search over attachment orders, brute force over bases with
   exact rank tests, the kernel) and, when pplpy is installed, the Parma Polyhedra Library.
2. L = 4, every chamber: the kernel's orbits, expanded, against the vertex set of the Parma Polyhedra Library
   (double description, exact integers), and against the reference implementation's orbits.
3. L = 5: (a) the uniform cube (weights 1,1,1,1,1) must give the known number 395 094 of height functions;
   (b) the unbounded chamber must have 2 x 990^2 vertices (parity argument, docstring of chambers.py);
   (c) closure: for a random sample of orbit representatives of every enumerated chamber (and the ones of
   largest degree) ALL neighbours are recomputed with the reference implementation (pure Python) and must lie
   in the enumerated orbits; (d) a sample of representatives is tested with the exact rank criterion of a
   vertex (independent of the tight-graph criterion).

Usage (repository root):   python experiments/eng/weighted_cube/run_crosschecks.py      # about 6 minutes
"""
from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from metricchain_eng.weighted_cube import chambers as CH  # noqa: E402
from metricchain_eng.weighted_cube import ckernel as CK  # noqa: E402
from metricchain_eng.weighted_cube import polytope as P  # noqa: E402
from run_bounds import load_chambers  # noqa: E402

RES = Path(__file__).resolve().parent / "results"


def kernel_vertex_set(wts):
    res = CK.enumerate_orbits(wts)
    assert res.complete
    table = P.node_perm_table(len(wts), list(res.perms))
    out = set()
    for rep in res.reps:
        out |= P.orbit(tuple(int(v) for v in rep), table)
    assert len(out) == res.n_vertices
    return out, res


def main():
    out = dict(ppl_available=P.ppl_available(), small=[], four=[], five={})
    t_all = time.time()
    # 1. L <= 3
    for wts in [(1,), (4, 5), (1, 1), (4, 4, 5), (2, 2, 3), (7, 7, 13), (4, 4, 9), (1, 1, 2), (1, 1, 1)]:
        t0 = time.time()
        bfs = P.enumerate_bfs(wts)
        sets = dict(dfs=P.enumerate_dfs(wts), bases=P.enumerate_bases(wts), kernel=kernel_vertex_set(wts)[0])
        if P.ppl_available():
            sets["ppl"] = P.enumerate_ppl(wts)
        rank_ok = all(P.is_vertex_by_rank(v, wts) for v in bfs)
        rec = dict(weights=list(wts), n_vertices=len(bfs), n_orbits=len(P.enumerate_bfs_orbits(wts)[0]),
                   all_equal=all(s == bfs for s in sets.values()), methods=["bfs", "bfs_orbits"] + sorted(sets),
                   every_vertex_passes_rank_test=rank_ok, seconds=round(time.time() - t0, 2))
        out["small"].append(rec)
        print(rec, flush=True)
        assert rec["all_equal"] and rank_ok
    # 2. L = 4
    chambers4, _ = load_chambers(4)
    for c in chambers4:
        wts = (c.Q,) * 3 + (c.P,)
        t0 = time.time()
        kv, res = kernel_vertex_set(wts)
        rec = dict(chamber=[str(c.lo), "inf" if c.hi is None else str(c.hi)], weights=list(wts), n_vertices=len(kv))
        if P.ppl_available():
            ppl = P.enumerate_ppl(wts)
            rec["ppl_n_vertices"] = len(ppl)
            rec["ppl_same_set"] = ppl == kv
            assert rec["ppl_same_set"]
        reps, total = P.enumerate_bfs_orbits(wts)
        got = {tuple(int(v) for v in r): (int(s), int(d)) for r, s, d in zip(res.reps, res.stab, res.deg)}
        rec["reference_orbits_same"] = got == reps
        rec["seconds"] = round(time.time() - t0, 1)
        assert rec["reference_orbits_same"]
        out["four"].append(rec)
        print(rec, flush=True)
    # 3. L = 5
    t0 = time.time()
    res = CK.enumerate_orbits((1,) * 5)
    out["five"]["uniform_cube"] = dict(n_vertices=int(res.n_vertices), n_orbits=int(len(res.reps)), expected=395094,
                                       ok=bool(res.complete and res.n_vertices == 395094), seconds=round(time.time() - t0, 1))
    print(out["five"]["uniform_cube"], flush=True)
    assert out["five"]["uniform_cube"]["ok"]
    chambers5, _ = load_chambers(5)
    out["five"]["chambers"] = []
    rng = np.random.default_rng(20261126)
    for c in chambers5:
        t0 = time.time()
        wts = (c.Q,) * 4 + (c.P,)
        N = CH.evaluate(c.A, c.B, c.Q, c.P)
        keys = {tuple(int(v) for v in row) for row in N}
        assert len(keys) == c.n_orbits
        order = np.argsort(-c.deg)
        sample = sorted(set(order[:3].tolist()) | set(rng.choice(c.n_orbits, size=40, replace=False).tolist()))
        n_nb = 0
        for k in sample:
            v = tuple(int(x) for x in N[k])
            assert CK.canonical(v, wts, CH.site_perms(5))[0] == v            # stored representatives are canonical
            nbs = P.neighbours(v, wts)                                        # reference implementation
            assert len(nbs) == c.deg[k]
            for w in nbs:
                assert CK.canonical(w, wts, CH.site_perms(5))[0] in keys
            n_nb += len(nbs)
        rank_sample = rng.choice(c.n_orbits, size=25, replace=False)
        rank_ok = all(P.is_vertex_by_rank(tuple(int(x) for x in N[k]), wts) for k in rank_sample)
        rec = dict(chamber=[str(c.lo), "inf" if c.hi is None else str(c.hi)], n_vertices=int(c.n_vertices),
                   n_orbits=int(c.n_orbits), closure_sample_orbits=len(sample), closure_neighbours_checked=int(n_nb),
                   closure_ok=True, rank_test_sample=int(len(rank_sample)), rank_test_ok=bool(rank_ok),
                   seconds=round(time.time() - t0, 1))
        if c.hi is None:
            rec["equals_2_times_990_squared"] = bool(c.n_vertices == 2 * 990 ** 2)
            assert rec["equals_2_times_990_squared"]
        assert rank_ok
        out["five"]["chambers"].append(rec)
        print(rec, flush=True)
    out["seconds_total"] = round(time.time() - t_all, 1)
    (RES / "crosschecks.json").write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", (RES / "crosschecks.json").relative_to(ROOT))


if __name__ == "__main__":
    main()
