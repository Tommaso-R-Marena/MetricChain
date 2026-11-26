"""Block bounds of the Markov recursion from the exact vertex lists (R10-E1): capacity and sup_t F* per site,
on the science division's grid, with certificates.

For every block length L and every cell (p, u):

1. ``u*`` is enclosed rigorously and the ratio ``u*/u`` is located in a chamber of results/chambers_L<L>.json
   by exact comparison with the two walls (interval arithmetic);
2. capacity: column generation (floating point) gives weights M on a few vertices and a centre Q;
   certified lower bound = I(M) in interval arithmetic; certified upper bound = max over ALL vertices of
   KL(pi_phi || Q), either entirely in interval arithmetic ("iv-all", used for L <= 4) or by a floating-point
   scan whose near-maximal vertices are re-evaluated in interval arithmetic ("screened");
3. sup_t F*: the same at every point of an adaptively refined grid of t, and the interval rule
   (F*/t nonincreasing, F*/(1-t) nondecreasing) evaluated in interval arithmetic;
4. the cube's closed forms as enclosures; "below" is declared only if upper bound < lower end of the cube.

All per-site numbers are written with 12 decimals, lower bounds rounded down and upper bounds rounded up.

Usage (repository root):
    python experiments/eng/weighted_cube/run_bounds.py --L 3 4            # about 15 minutes
    python experiments/eng/weighted_cube/run_bounds.py --L 5 --part 0/2   # cells whose chamber was enumerated
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import numpy as np
from mpmath import iv

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.weighted_cube import chambers as CH  # noqa: E402
from metricchain_eng.weighted_cube import exponents as EX  # noqa: E402

RES = Path(__file__).resolve().parent / "results"
P_GRID = ["0.45", "0.4", "0.3", "0.2", "0.1"]
U_GRID = ["0.5", "1", "1.5", "2", "2.5", "3", "4", "6"]
ND = 12


def _fixed(n: int, nd: int) -> str:
    sign = "-" if n < 0 else ""
    q, r = divmod(abs(n), 10 ** nd)
    return f"{sign}{q}.{r:0{nd}d}"


def down(x, nd=ND) -> str:
    """Decimal string with nd decimals, not larger than x."""
    old = mp.mp.dps
    mp.mp.dps = 50
    try:
        return _fixed(int(mp.floor(mp.mpf(x) * mp.mpf(10) ** nd)), nd)
    finally:
        mp.mp.dps = old


def up(x, nd=ND) -> str:
    """Decimal string with nd decimals, not smaller than x."""
    old = mp.mp.dps
    mp.mp.dps = 50
    try:
        return _fixed(int(mp.ceil(mp.mpf(x) * mp.mpf(10) ** nd)), nd)
    finally:
        mp.mp.dps = old


def load_chambers(L: int):
    """The enumerated chambers of block length L (from the stored orbit representatives)."""
    rec = json.loads((RES / f"chambers_L{L}.json").read_text())
    out = []
    for e in rec["chambers"]:
        z = np.load(RES / e["file"])
        lo = Fraction(int(z["lo"][0]), int(z["lo"][1]))
        hi = None if int(z["hi"][1]) == 0 else Fraction(int(z["hi"][0]), int(z["hi"][1]))
        A, B = z["A"], z["B"]
        Pq, Qq = int(z["r0"][0]), int(z["r0"][1])
        CH.check_symbolic(A, B, Qq, Pq)                     # the stored data are symbolic vertices at r0
        lo2, hi2, at_lo, at_hi = CH.chamber_of(A, B)
        assert (lo2, hi2) == (lo, hi)
        ch = CH.Chamber(L, lo, hi, Qq, Pq, A, B, z["stab"].astype(np.int64), z["deg"], int(e["n_vertices"]), at_lo, at_hi)
        assert int(ch.orbit_sizes.sum()) == ch.n_vertices
        out.append(ch)
    return out, rec


def sup_bound_iv(grid):
    """The interval rule of ``exponents.sup_bound`` in interval arithmetic; grid = [(t as Fraction, upper bound
    as mpf)], sorted.  Returns an mpf upper bound of sup_t F(t)."""
    def one(t1, B1, t2, B2):
        t1i, t2i = EX._iv_frac(t1), EX._iv_frac(t2)
        a1 = iv.mpf(B1) / t1i
        a2 = iv.mpf(B2) / (1 - t2i)
        # on [t1, t2]:  F(t) <= min(t a1, (1 - t) a2).  Each of the three numbers below bounds that minimum on the
        # whole interval: t a1 <= t2 a1,  (1 - t) a2 <= (1 - t1) a2,  and min(t a1, (1 - t) a2) <= a1 a2 / (a1 + a2)
        # for every real t (the value where the increasing and the decreasing line cross).
        cands = [EX.iv_hi(a1 * a2 / (a1 + a2)), EX.iv_hi(a1 * t2i), EX.iv_hi(a2 * (1 - t1i))]
        return min(cands)

    best = max(EX.iv_hi(iv.mpf(grid[0][1]) / (1 - EX._iv_frac(grid[0][0]))), EX.iv_hi(iv.mpf(grid[-1][1]) / EX._iv_frac(grid[-1][0])))
    for (t1, B1), (t2, B2) in zip(grid[:-1], grid[1:]):
        best = max(best, one(t1, B1, t2, B2))
    return best


def certify_scan(ivb, prob, kind, Q, vals, A, B, t=None):
    """``exponents.certify_upper`` on the top of a scan; if all candidates of the scan lie within the margin of
    the largest value (many nearly active vertices), the scan is repeated with a longer list."""
    for K in (None, 1024, 8192, 65536):
        if K is not None:
            if kind == "kl":
                vals, A, B = prob.scan_kl(np.log(Q), K)
            else:
                vals, A, B = prob.scan_renyi([float(t)], [Q], K)[0]
        try:
            return EX.certify_upper(ivb, kind, Q, vals, A, B, t=t)
        except RuntimeError:
            continue
    raise RuntimeError("more than 65536 vertices within the margin of the maximum")


def compute_cell(L, chambers, p_str, u_str, expanded, do_h=True, h_rel_tol=2e-4, full_iv=None):
    t0 = time.time()
    pf, uf = Fraction(p_str), Fraction(u_str)
    ivb = EX.IvBlock(L, pf, uf, dps=30)
    inside = [c for c in chambers if ivb.in_chamber(c.lo, c.hi)]
    ratio = float(EX.iv_lo(ivb.ratio))
    cube_h, cube_a, cube_E = EX.iv_cube(uf)
    cell = dict(p=p_str, u=u_str, ustar=mp.nstr(EX.iv_lo(ivb.us), 15), ratio=mp.nstr(EX.iv_lo(ivb.ratio), 12),
                cube=dict(a_lo=down(EX.iv_lo(cube_a)), a_hi=up(EX.iv_hi(cube_a)), h_lo=down(EX.iv_lo(cube_h)),
                          h_hi=up(EX.iv_hi(cube_h))))
    if len(inside) != 1:
        cell["chamber"] = None
        cell["note"] = "the chamber of u*/u was not enumerated (vertex limit)"
        return cell
    c = inside[0]
    if full_iv is None:
        full_iv = c.n_vertices <= 30000
    key = id(c)
    if full_iv and key not in expanded:
        expanded[key] = CH.expand_orbits(c.A, c.B, CH.group_table(L))[:2]
    prob = EX.BlockProblem(c, float(pf), float(uf))
    assert abs(prob.us / prob.u - ratio) < 1e-9
    cap = EX.capacity_bound(prob)
    a_lo = EX.iv_lo(ivb.mutual_information(cap["support_A"], cap["support_B"], cap["support_M"])) / L
    if full_iv:
        a_up = ivb.kl_max(expanded[key][0], expanded[key][1], cap["Q"])[0] / L
        a_method, a_neval = "iv-all", int(c.n_vertices)
    else:
        v, a_neval = certify_scan(ivb, prob, "kl", cap["Q"], cap["top_vals"], cap["top_A"], cap["top_B"])
        a_up, a_method = v / L, "screened"
    cell.update(chamber=[str(c.lo), "inf" if c.hi is None else str(c.hi)], n_vertices=int(c.n_vertices), n_orbits=int(c.n_orbits))
    cell["a"] = dict(lower=down(a_lo), upper=up(a_up), method=a_method, n_interval_evaluations=a_neval,
                     float_lower=cap["lower"] / L, float_upper=cap["upper"] / L, support=int(len(cap["support_M"])),
                     rounds=int(cap["rounds"]), below_cube=bool(a_up < EX.iv_lo(cube_a)),
                     ratio_to_cube=float(a_up / EX.iv_lo(cube_a)))
    # the optimum over the 2^L site-wise labels alone (a lower bound of the capacity; informative)
    Aadd, Badd = EX.additive_rows(L)
    sw = EX.capacity_solve(prob.rows(Aadd, Badd))
    cell["a"]["sitewise_float"] = sw["lower"] / L
    cell["a"]["sitewise_is_optimal"] = bool(cap["lower"] - sw["lower"] < 1e-10)
    t1 = time.time()
    if do_h:
        hb = EX.h_bound(prob, rel_tol=h_rel_tol)
        grid_cert, lo_best, n_iv = [], None, 0
        for (t, lo_f, up_f) in hb["grid"]:
            d = hb["data"][t]
            lo_c = EX.iv_lo(ivb.G(d["support_A"], d["support_B"], d["support_M"], Fraction(t)))
            if full_iv and c.n_vertices <= 200:
                up_c = ivb.renyi_max(expanded[key][0], expanded[key][1], Fraction(t), d["Q"])[0]
                h_method = "iv-all"
                n_iv += c.n_vertices
            else:
                up_c, k = certify_scan(ivb, prob, "renyi", d["Q"], d["top_vals"], d["top_A"], d["top_B"], t=Fraction(t))
                h_method = "screened"
                n_iv += k
            grid_cert.append((Fraction(t), up_c))
            lo_best = lo_c if lo_best is None or lo_c > lo_best else lo_best
        h_up = sup_bound_iv(grid_cert) / L
        h_lo = lo_best / L
        cell["h"] = dict(lower=down(h_lo), upper=up(h_up), method=h_method, n_grid=len(grid_cert), n_interval_evaluations=n_iv,
                         t_best=float(hb["t_best"]), float_lower=hb["lower"] / L, float_upper=hb["upper"] / L,
                         below_cube=bool(h_up < EX.iv_lo(cube_h)), ratio_to_cube=float(h_up / EX.iv_lo(cube_h)))
    cell["seconds"] = dict(a=round(t1 - t0, 2), h=round(time.time() - t1, 2))
    return cell


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=int, nargs="+", default=[3, 4])
    ap.add_argument("--p", type=str, nargs="*", default=P_GRID)
    ap.add_argument("--u", type=str, nargs="*", default=U_GRID)
    ap.add_argument("--part", type=str, default="0/1", help="k/m: only the cells with index = k mod m")
    ap.add_argument("--no-h", action="store_true")
    ap.add_argument("--h-rel-tol", type=float, default=2e-4)
    ap.add_argument("--tag", type=str, default="")
    args = ap.parse_args()
    k, m = (int(v) for v in args.part.split("/"))
    for L in args.L:
        chambers, rec = load_chambers(L)
        expanded = {}
        cells = []
        idx = 0
        t_all = time.time()
        for p_str in args.p:
            for u_str in args.u:
                idx += 1
                if (idx - 1) % m != k:
                    continue
                cell = compute_cell(L, chambers, p_str, u_str, expanded, do_h=not args.no_h, h_rel_tol=args.h_rel_tol)
                cells.append(cell)
                if cell.get("chamber") is None:
                    print(f"L={L} p={p_str} u={u_str} ratio={cell['ratio']}: {cell['note']}", flush=True)
                    continue
                msg = (f"L={L} p={p_str} u={u_str} r={float(cell['ratio']):.4f} ch=({cell['chamber'][0]},{cell['chamber'][1]}) "
                       f"a in [{cell['a']['lower']}, {cell['a']['upper']}] cube {cell['cube']['a_lo']} "
                       f"{'BELOW' if cell['a']['below_cube'] else 'not below'}")
                if "h" in cell:
                    msg += (f" | h in [{cell['h']['lower']}, {cell['h']['upper']}] cube {cell['cube']['h_lo']} "
                            f"{'BELOW' if cell['h']['below_cube'] else 'not below'}")
                print(msg + f"  ({cell['seconds']})", flush=True)
        out = dict(L=L, p_grid=args.p, u_grid=args.u, part=args.part, per="site", decimals=ND, cells=cells,
                   seconds_total=round(time.time() - t_all, 1))
        name = f"bounds_L{L}{args.tag}.json" if m == 1 else f"bounds_L{L}{args.tag}_part{k}of{m}.json"
        (RES / name).write_text(json.dumps(out, indent=1) + "\n")
        print(f"wrote {(RES / name).relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
