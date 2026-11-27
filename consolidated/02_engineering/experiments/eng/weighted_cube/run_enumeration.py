"""Exact vertex enumeration of the weighted cubes (1, ..., 1, r) by chambers of the slope ratio r (R10-E1).

For every block length L requested:

* walk over the chambers of r from the wall given by --start upwards (kernel, orbits), with the exact checks
  of ``chambers.chamber_at`` (every representative is a symbolic vertex, feasible and generic at r0);
* for consecutive chambers: the symbolic vertices that survive the common wall must be the same set of orbits
  on both sides (two independent enumerations agree on what they must share);
* the order-independent SHA-256 checksum of the full vertex list;
* results/chambers_L<L>.json (every number of the tables) and results/orbits_L<L>_<k>.npz (orbit
  representatives in symbolic form, orders of the stabilisers, degrees).

A chamber whose enumeration exceeds --max-vertices (or --max-orbits) is recorded as "stopped" with what was
found; the walk cannot continue past it (its upper wall is unknown), so further walks are started at the walls
given by --also-start.

Usage (repository root):
    python experiments/eng/weighted_cube/run_enumeration.py --L 2 3 4
    python experiments/eng/weighted_cube/run_enumeration.py --L 5 --start 1 --also-start 3/2 2 --max-vertices 20000000
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.weighted_cube import chambers as CH  # noqa: E402
from metricchain_eng.weighted_cube import ckernel as CK  # noqa: E402

RES = Path(__file__).resolve().parent / "results"


def frac_str(x):
    return "inf" if x is None else str(x)


def canonical_symbolic_keys(L, A, B, Q, P):
    """Orbit keys that do not depend on the ratio used for the enumeration: the canonical member of the orbit of
    the integer vector N = Q A + P B at common reference weights (Q, P)."""
    wts = (Q,) * (L - 1) + (P,)
    perms = CH.site_perms(L)
    N = CH.evaluate(A, B, Q, P).astype(np.int32)
    keys = set()
    for row in N:
        key, _ = CK.canonical(row, wts, perms)
        keys.add(key)
    return keys


def probe(L, Q, P, max_orbits, max_vertices):
    wts = (Q,) * (L - 1) + (P,)
    t0 = time.time()
    res = CK.enumerate_orbits(wts, perms=CH.site_perms(L), max_orbits=max_orbits, max_vertices=max_vertices)
    return dict(r0=f"{P}/{Q}", status=CK.STATUS[res.status], orbits_found=int(len(res.reps)),
                orbits_processed=int(res.n_processed), vertices_found=int(res.n_vertices),
                seconds=round(time.time() - t0, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=int, nargs="+", default=[2, 3, 4])
    ap.add_argument("--start", type=str, default="1")
    ap.add_argument("--also-start", type=str, nargs="*", default=[])
    ap.add_argument("--max-vertices", type=int, default=10 ** 7)
    ap.add_argument("--max-orbits", type=int, default=4_000_000)
    ap.add_argument("--Q", type=int, default=101)
    ap.add_argument("--no-checksum", action="store_true")
    args = ap.parse_args()
    RES.mkdir(exist_ok=True)
    for L in args.L:
        t_all = time.time()
        table = CH.group_table(L)
        record = dict(L=L, dimension=(1 << L) - 1, inequalities=L * (1 << L), group_order=2 * len(CH.site_perms(L)) * (1 << L),
                      max_vertices=args.max_vertices, chambers=[], stopped=[], wall_checks=[])
        chambers = []
        for start in [args.start] + list(args.also_start):
            c = Fraction(start)
            if any(ch.lo <= c and (ch.hi is None or c < ch.hi) for ch in chambers):
                continue
            while True:
                q = args.Q
                while True:
                    Qq, Pp = CH.generic_ratio(c, None, q)
                    t0 = time.time()
                    ch = CH.chamber_at(L, Qq, Pp, max_orbits=args.max_orbits, max_vertices=args.max_vertices)
                    if ch is None or ch.lo <= c:
                        break
                    q = 2 * q + 1
                if ch is None:
                    pr = probe(L, Qq, Pp, args.max_orbits, args.max_vertices)
                    pr["just_above_wall"] = str(c)
                    record["stopped"].append(pr)
                    print(f"L={L}: enumeration just above r = {c} (r0 = {Pp}/{Qq}) stopped: {pr}", flush=True)
                    break
                dt = time.time() - t0
                chambers.append(ch)
                sizes = ch.orbit_sizes
                entry = dict(lo=frac_str(ch.lo), hi=frac_str(ch.hi), r0=f"{ch.P}/{ch.Q}", n_vertices=int(ch.n_vertices),
                             n_orbits=int(ch.n_orbits), sum_degree_over_orbits=int(ch.deg.sum()),
                             degree_min=int(ch.deg.min()), degree_max=int(ch.deg.max()),
                             degree_mean_over_vertices=float((ch.deg * sizes).sum() / sizes.sum()),
                             A_range=[int(ch.A.min()), int(ch.A.max())], B_range=[int(ch.B.min()), int(ch.B.max())],
                             vertices_ending_at_lo=int(sizes[ch.at_lo].sum()), vertices_ending_at_hi=int(sizes[ch.at_hi].sum()),
                             orbits_ending_at_lo=int(ch.at_lo.sum()), orbits_ending_at_hi=int(ch.at_hi.sum()),
                             seconds=round(dt, 2))
                if not args.no_checksum:
                    cs, cnt = CH.multiset_checksum(ch.A, ch.B, table)
                    assert cnt == ch.n_vertices
                    entry["sha256_multiset"] = cs
                k = len(record["chambers"])
                fname = f"orbits_L{L}_{k}.npz"
                np.savez_compressed(RES / fname, A=ch.A, B=ch.B, stab=ch.stab.astype(np.int16), deg=ch.deg.astype(np.int32),
                                    lo=np.array([ch.lo.numerator, ch.lo.denominator]),
                                    hi=np.array([0, 0] if ch.hi is None else [ch.hi.numerator, ch.hi.denominator]),
                                    r0=np.array([ch.P, ch.Q]))
                entry["file"] = fname
                record["chambers"].append(entry)
                print(f"L={L}: chamber ({frac_str(ch.lo)}, {frac_str(ch.hi)}): {ch.n_vertices} vertices in {ch.n_orbits} orbits "
                      f"({dt:.1f} s)", flush=True)
                if ch.hi is None:
                    break
                c = ch.hi
        # consistency across walls: the survivors must be the same orbits on both sides
        chambers.sort(key=lambda ch: ch.lo)
        for c1, c2 in zip(chambers[:-1], chambers[1:]):
            if c1.hi != c2.lo:
                continue
            Qr, Pr = 1009, 2003          # any common coprime reference weights: only used to label orbits
            k1 = canonical_symbolic_keys(L, c1.A[~c1.at_hi], c1.B[~c1.at_hi], Qr, Pr)
            k2 = canonical_symbolic_keys(L, c2.A[~c2.at_lo], c2.B[~c2.at_lo], Qr, Pr)
            ok = k1 == k2
            record["wall_checks"].append(dict(wall=str(c1.hi), orbits_surviving=len(k1), same_set=bool(ok),
                                              vertices_surviving=int(c1.orbit_sizes[~c1.at_hi].sum())))
            print(f"L={L}: wall r = {c1.hi}: {len(k1)} orbits survive, same set on both sides: {ok}", flush=True)
            if not ok:
                raise AssertionError("survivors differ across a wall")
        record["seconds_total"] = round(time.time() - t_all, 1)
        out = RES / f"chambers_L{L}.json"
        out.write_text(json.dumps(record, indent=1) + "\n")
        print(f"wrote {out.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
