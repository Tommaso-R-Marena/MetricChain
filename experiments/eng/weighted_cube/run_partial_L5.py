"""The 5-site block where the vertex enumeration does NOT finish within the stopping rule (10^7 vertices):
what the enumerated part supports.

For a cell (p, u) whose chamber was not enumerated:

1. the breadth-first search over orbits is run at a rational ratio r0 next to u*/u and stopped by the vertex
   limit; every orbit found is a symbolic vertex at r0 (exact checks);
2. of these, the ones that are vertices at the true ratio u*/u are selected rigorously (interval enclosure of
   u*/u against the rational interval of validity of every edge);  their number is a rigorous LOWER bound of
   the number of vertices of the polytope at this cell;
3. column generation over this PARTIAL vertex set, followed by "local pricing" (all polytope neighbours of the
   support vertices are examined and added when they improve), gives weights M on genuine vertices;
   I(M)/5 in interval arithmetic is a rigorous LOWER bound of capacity/5, i.e. of the bound the 5-site block
   could give for a_inf.  It is NOT an upper bound of a_inf.  The same for sup_t F* with max_t G_t(M_t).

Consequence that is rigorous: where this lower bound is >= the cube's exponent, the Markov recursion with L = 5
cannot show that the chain's exponent is below the cube's.  Where it is below the cube's, the 5-site block would
show it IF the partial optimum were the true one; that is numerical evidence only (the largest objective over
the part scanned, and over all neighbours of the support, equals the lower bound).

Usage (repository root):
    python experiments/eng/weighted_cube/run_partial_L5.py --p 0.3 0.4 --u 1.5 2 2.5 3 [--h]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from math import gcd
from pathlib import Path

import mpmath as mp
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from metricchain_eng.weighted_cube import chambers as CH  # noqa: E402
from metricchain_eng.weighted_cube import ckernel as CK  # noqa: E402
from metricchain_eng.weighted_cube import exponents as EX  # noqa: E402
from run_bounds import P_GRID, U_GRID, down, load_chambers, up  # noqa: E402

RES = Path(__file__).resolve().parent / "results"
L = 5


def partial_set(ivb, max_vertices: int, Q: int = 211):
    """Steps 1-2: (pseudo-chamber of the vertices found that are valid at the cell, r0, statistics)."""
    r = float(EX.iv_lo(ivb.ratio))
    Pn = int(round(r * Q))
    while gcd(Pn, Q) != 1:
        Pn += 1
    wts = (Q,) * (L - 1) + (Pn,)
    t0 = time.time()
    res = CK.enumerate_orbits(wts, perms=CH.site_perms(L), max_vertices=max_vertices)
    assert res.status in (0, 2), CK.STATUS[res.status]
    A, B = CH.to_symbolic(res.reps, Q, Pn)
    CH.check_symbolic(A, B, Q, Pn)
    ok = CH.valid_at(A, B, ivb.in_chamber)
    sizes = res.orbit_sizes
    lo, hi, at_lo, at_hi = CH.chamber_of(A[ok], B[ok])
    assert ivb.in_chamber(lo, hi)
    pc = CH.Chamber(L, lo, hi, Q, Pn, A[ok], B[ok], res.stab[ok].astype(np.int64), res.deg[ok], int(sizes[ok].sum()), at_lo,
                    at_hi)
    stats = dict(r0=f"{Pn}/{Q}", search_status=CK.STATUS[res.status], orbits_found=int(len(res.reps)),
                 orbits_processed=int(res.n_processed), vertices_found=int(res.n_vertices),
                 orbits_valid_at_cell=int(ok.sum()), vertices_valid_at_cell=int(sizes[ok].sum()),
                 common_validity_interval=[str(lo), "inf" if hi is None else str(hi)], seconds=round(time.time() - t0, 1))
    return pc, wts, stats


def neighbours_valid(ivb, wts, A_rows, B_rows):
    """All polytope neighbours (at r0) of the given vertices that are vertices at the cell: symbolic rows."""
    Q, Pn = wts[0], wts[-1]
    outA, outB = [], []
    for a, b in zip(A_rows, B_rows):
        N = CH.evaluate(a[None], b[None], Q, Pn)[0]
        nb = CK.neighbours(N, wts)
        if len(nb) == 0:
            continue
        An, Bn = CH.to_symbolic(nb, Q, Pn)
        ok = CH.valid_at(An, Bn, ivb.in_chamber) & CH.identically_tight_connected(An, Bn)
        outA.append(An[ok])
        outB.append(Bn[ok])
    if not outA:
        return np.zeros((0, 1 << L), dtype=np.int8), np.zeros((0, 1 << L), dtype=np.int8)
    return np.concatenate(outA), np.concatenate(outB)


def analyse_cell(p_str, u_str, max_vertices, do_h, local_rounds=6):
    t0 = time.time()
    pf, uf = Fraction(p_str), Fraction(u_str)
    ivb = EX.IvBlock(L, pf, uf, dps=30)
    cube_h, cube_a, _ = EX.iv_cube(uf)
    pc, wts, stats = partial_set(ivb, max_vertices)
    prob = EX.BlockProblem(pc, float(pf), float(uf))
    ws = EX.WorkingSet.empty(1 << L)
    ws.add(*EX.additive_rows(L))
    cap = EX.capacity_bound(prob, ws=ws)
    n_local, n_improving = 0, 0
    for _ in range(local_rounds):
        An, Bn = neighbours_valid(ivb, wts, cap["support_A"], cap["support_B"])
        n_local += len(An)
        W = prob.rows(An, Bn)
        kl = np.einsum("ij,ij->i", W, np.log(W) - np.log(cap["Q"])[None, :])
        viol = kl > cap["lower"] + 1e-11
        if not viol.any():
            break
        order = np.argsort(-kl[viol])[:512]
        n_improving += ws.add(An[viol][order], Bn[viol][order])
        cap = EX.capacity_bound(prob, ws=ws)
    a_lo = EX.iv_lo(ivb.mutual_information(cap["support_A"], cap["support_B"], cap["support_M"])) / L
    Aadd, Badd = EX.additive_rows(L)
    sw = EX.capacity_solve(prob.rows(Aadd, Badd))
    cell = dict(p=p_str, u=u_str, ratio=mp.nstr(EX.iv_lo(ivb.ratio), 12), search=stats,
                cube=dict(a_lo=down(EX.iv_lo(cube_a)), a_hi=up(EX.iv_hi(cube_a)), h_lo=down(EX.iv_lo(cube_h)),
                          h_hi=up(EX.iv_hi(cube_h))))
    cell["a"] = dict(lower_bound_of_block_capacity=down(a_lo), partial_optimum_float=cap["lower"] / L,
                     largest_value_in_scanned_part_float=cap["upper"] / L, sitewise_float=sw["lower"] / L,
                     support=int(len(cap["support_M"])), neighbours_examined=int(n_local),
                     improving_neighbours_added=int(n_improving),
                     block_cannot_show_below_cube=bool(a_lo >= EX.iv_hi(cube_a)),
                     ratio_to_cube=float(a_lo / EX.iv_hi(cube_a)))
    t1 = time.time()
    if do_h:
        ts = [round(0.1 + 0.05 * k, 4) for k in range(17)]
        warm = {}
        data = EX.renyi_bounds(prob, ts, ws=ws, warm=warm, K=32, tol=1e-9)
        tb = max(data, key=lambda t: data[t]["lower"])
        fine = [round(tb - 0.045 + 0.005 * k, 4) for k in range(19) if abs(0.005 * k - 0.045) > 1e-9]
        data.update(EX.renyi_bounds(prob, [t for t in fine if 0.02 < t < 0.98], ws=ws, warm=warm, K=32, tol=1e-9))
        tb = max(data, key=lambda t: data[t]["lower"])
        d = data[tb]
        # local pricing at the best order
        An, Bn = neighbours_valid(ivb, wts, d["support_A"], d["support_B"])
        W = prob.rows(An, Bn)
        val = -np.log((W ** tb) @ (d["Q"] ** (1.0 - tb)))
        viol = val > d["lower"] + 1e-10
        n_h_impr = 0
        if viol.any():
            order = np.argsort(-val[viol])[:512]
            n_h_impr = ws.add(An[viol][order], Bn[viol][order])
            near = sorted(data, key=lambda t: abs(t - tb))[:9]
            data.update(EX.renyi_bounds(prob, near, ws=ws, warm=warm, K=32, tol=1e-9))
            tb = max(data, key=lambda t: data[t]["lower"])
            d = data[tb]
        h_lo = EX.iv_lo(ivb.G(d["support_A"], d["support_B"], d["support_M"], Fraction(tb))) / L
        cell["h"] = dict(lower_bound_of_block_sup=down(h_lo), t=float(tb), partial_optimum_float=d["lower"] / L,
                         largest_value_in_scanned_part_float=d["upper"] / L, neighbours_examined=int(len(An)),
                         improving_neighbours_added=int(n_h_impr),
                         block_cannot_show_below_cube=bool(h_lo >= EX.iv_hi(cube_h)),
                         ratio_to_cube=float(h_lo / EX.iv_hi(cube_h)))
    cell["seconds"] = dict(a=round(t1 - t0, 1), h=round(time.time() - t1, 1))
    return cell


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=str, nargs="*", default=P_GRID)
    ap.add_argument("--u", type=str, nargs="*", default=U_GRID)
    ap.add_argument("--max-vertices", type=int, default=10 ** 7)
    ap.add_argument("--h", action="store_true")
    ap.add_argument("--tag", type=str, default="")
    args = ap.parse_args()
    chambers, _ = load_chambers(L)
    cells = []
    t_all = time.time()
    for p_str in args.p:
        for u_str in args.u:
            ivb = EX.IvBlock(L, Fraction(p_str), Fraction(u_str), dps=30)
            if any(ivb.in_chamber(c.lo, c.hi) for c in chambers):
                continue                                    # enumerated completely: see run_bounds.py
            cell = analyse_cell(p_str, u_str, args.max_vertices, args.h)
            cells.append(cell)
            a = cell["a"]
            msg = (f"L=5 p={p_str} u={u_str} r={float(cell['ratio']):.4f}: >= {cell['search']['vertices_valid_at_cell']} vertices; "
                   f"block capacity/5 >= {a['lower_bound_of_block_capacity']} (cube {cell['cube']['a_hi']}; "
                   f"{'CANNOT show below' if a['block_cannot_show_below_cube'] else 'might show below'}; "
                   f"site-wise {a['sitewise_float']:.9f}; neighbours {a['neighbours_examined']}, improving {a['improving_neighbours_added']})")
            if "h" in cell:
                h = cell["h"]
                msg += (f" | sup_t F*/5 >= {h['lower_bound_of_block_sup']} (cube {cell['cube']['h_hi']}; "
                        f"{'CANNOT show below' if h['block_cannot_show_below_cube'] else 'might show below'})")
            print(msg + f"  ({cell['seconds']})", flush=True)
    out = dict(L=L, max_vertices=args.max_vertices, per="site", cells=cells, seconds_total=round(time.time() - t_all, 1))
    name = f"partial_L5{args.tag}.json"
    (RES / name).write_text(json.dumps(out, indent=1) + "\n")
    print(f"wrote {(RES / name).relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
