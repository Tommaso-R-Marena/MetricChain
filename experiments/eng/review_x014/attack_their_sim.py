"""Review of ENG-RES-0016, item 4 of the brief: the DIVISION's simulator (``hetero_literal.run_2l``) and constants
(``hetero.constants``) on shapes, parameter sets and energy tables that X-014b did not use.

Instances: the referee's generator (``review_sim.instance``: products "outer landscape x inner profile" that make the
tail lemma, the Harper term and the first lower bound equalities, largest class members below noise, fibres whose value
at the reference point is unrepresentative) and the division's own kinds.  Oracles: the division's three.

Counted per configuration, as the division does: invalid brackets, brackets wider than x_out, aborts, costs above
C_max (unit inner costs), false certificates.  The theorem allows invalid brackets with probability at most 0.05 and
nothing else; aborts caused by an exact floating-point tie (K_REPORT erratum m10) are identified by a re-run of the
same sample in the referee's simulator, which reports the tie.

    python experiments/eng/review_x014/attack_their_sim.py [--minutes 12] [--procs 2]      # writes attack_their_sim.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from fractions import Fraction
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "eng" / "twolevel"))
sys.path.insert(0, str(HERE))

import hetero_literal as hl  # noqa: E402
import review_sim as rs  # noqa: E402
from metricchain_eng.twolevel import hetero as H  # noqa: E402
from metricchain_eng.twolevel.certified import tables  # noqa: E402

LID = math.log(20.0)
SHAPES = [  # (n_o, u_o, inner block as (slope, count) pairs)
    (6, 0.05, [(5.0, 3)]), (7, 0.05, [(20.0, 1)]), (5, 3.0, [(0.05, 4)]), (4, 6.0, [(0.1, 6)]), (8, 0.3, [(10.0, 1)]),
    (3, 0.1, [(4.0, 1), (0.2, 1), (2.0, 1), (0.01, 1)]), (2, 0.5, [(3.0, 5)]), (5, 1.0, [(1.0, 2), (2.0, 1)]), (1, 2.0, [(0.3, 8)]),
    (1, 0.2, [(2.5, 2), (0.4, 1)]), (2, 4.0, [(0.5, 8)]), (10, 0.7, [(0.3, 1)]), (11, 1.0, [(2.0, 1)]), (4, 1.37, [(0.83, 1), (2.11, 1), (0.29, 1)]),
    (7, 0.61, [(1.93, 1), (0.37, 1)]), (9, 1.5, [(0.2, 3)]), (6, 2.0, [(2.0, 1), (0.5, 2)]), (12, 0.4, [(1.5, 2)]),
]
DESIGNS = [  # keyword arguments of hetero.HDesign (b = None: 0.45 x_0)
    dict(lam=1.0, eta=0.5, etap=1.0, b=1.0, Lr=4, theta=1.0, bounded=False, name="EXT"),
    dict(lam=0.5, eta=0.25, etap=0.25, b=0.5, Lr=4, theta=0.25, bounded=True, name="BND"),
    dict(lam=0.6180339887, eta=0.5, etap=1.0, b=0.7310585786, Lr=3, theta=1.0, bounded=True, name="generic lam, eta=1/2"),
    dict(lam=0.05, eta=0.5, etap=1.0, b=0.3, Lr=2, theta=1.0, bounded=False, name="lam=0.05"),
    dict(lam=1.0, eta=0.5, etap=1.0, b=1.0, Lr=3, theta=math.exp(8.0), bounded=False, name="theta=e^8"),
    dict(lam=0.3, eta=1 / 3, etap=0.1, b=0.2, Lr=5, theta=0.01, bounded=True, name="theta=0.01"),
    dict(lam=0.5, eta=0.5, etap=1.0, b=0.02, Lr=4, theta=1.0, bounded=True, name="b=0.02"),
    dict(lam=1.0, eta=0.5, etap=1.0, b=None, Lr=1, theta=1.0, bounded=True, name="one rung"),
    dict(lam=0.7, eta=1 / 3, etap=0.3, b=0.1, Lr=8, theta=0.2, bounded=True, name="eight rungs"),
    dict(lam=0.5, eta=0.1, etap=0.5, b=0.5, Lr=2, theta=0.5, bounded=True, name="eta=1/10"),
]
THEIR_KINDS = ("flat", "cone", "cone0", "dip", "wells", "ridges", "linear", "mixed")


def build(shape, design):
    n_o, u_o, inner = shape
    B = H.make_block([(u_o, n_o)] + list(inner))
    j = [i for i, (u, _) in enumerate(B) if u == u_o][0]
    x0 = 2 * sum(u * k for u, k in inner)
    kw = dict(design)
    if kw["b"] is None or kw["b"] >= 0.9 * x0:
        kw["b"] = 0.45 * x0
    D = H.HDesign(j=j, k=n_o, **kw)
    C = H.constants(B, D, LID)
    # the simulator's site order: outer block first, then the inner sites; any order of the inner sites is a member of the class
    us = np.array([u_o] * n_o + [u for u, k in inner for _ in range(k)], dtype=float)
    return C, us


def referee_consts(C, us, n_o, design):
    """The same constants for the referee's simulator, with the division's floats (ties are then resolved alike)."""
    eta = Fraction(design["eta"]).limit_denominator(1000)
    nu1 = max(1.0, 2 * n_o * math.exp(us[0]) / design["theta"]) if design["bounded"] else 1.0
    D = rs.Design(us=tuple(us), n_o=n_o, lam=design["lam"], eta=eta, etap=design["etap"], lth=math.log(design["theta"]), nu1=nu1, b=C.b, xs=tuple(C.xs))
    return rs.make_consts(D, override=dict(Omega=C.omega, Omega_Y=C.xs[0] / 2, lPi=C.l2p))


def task(args):
    si, di, seconds, seed = args
    shape, design = SHAPES[si], DESIGNS[di]
    n_o, u_o, inner = shape
    C, us = build(shape, design)
    out = dict(shape=[n_o, u_o, inner], design=design["name"], seed=seed)
    if C is None:
        out["skipped"] = "no level (x_0 <= b)"
        return out
    if C.K * 2 ** (n_o + 1) / (1 - design["eta"]) > 3e6:
        out["skipped"] = "samples too large for a literal run"
        return out
    T = tables(n_o, u_o)
    lCmax = hl.lcmax_unit(C)
    out.update(K=C.K, J=C.J, x_out=C.x_out, lCmax_unit=lCmax, r_dag=C.r_dag)
    Cr = None
    rng = np.random.default_rng(seed)
    st = dict(runs=0, closed=0, invalid=0, too_wide=0, aborted=0, aborted_tie=0, aborted_other=0, over_budget=0, bad_certificates=0, max_width=0.0,
              max_lcost=0.0, class_violation=-math.inf, by_kind={}, examples=[])
    kinds = [("ref", k) for k in rs.INSTANCE_KINDS] + [("div", k) for k in THEIR_KINDS]
    t0 = time.time()
    i = 0
    while time.time() - t0 < seconds:
        src, kind = kinds[i % len(kinds)]
        i += 1
        psi = rs.instance(kind, us, n_o, rng) if src == "ref" else hl.make_instance(kind, us, rng)
        st["class_violation"] = max(st["class_violation"], hl.check_class(psi, us))
        for orc in hl.ORACLES:
            s = int(rng.integers(2 ** 31))
            try:
                r = hl.run_2l(psi, n_o, C, T, orc, np.random.default_rng(s))
            except MemoryError:                                 # the address-space cap of this process was reached: skip the run
                st["memory_errors"] = st.get("memory_errors", 0) + 1
                continue
            st["runs"] += 1
            bk = st["by_kind"].setdefault(f"{src}:{kind}", dict(runs=0, invalid=0, aborted=0))
            bk["runs"] += 1
            lc = math.log(r["cost"])
            st["max_lcost"] = max(st["max_lcost"], lc)
            st["over_budget"] += lc > lCmax + 1e-9
            if r["status"] != "closed":
                st["aborted"] += 1
                bk["aborted"] += 1
                tie = None
                if orc in ("bottom", "top"):            # deterministic oracle: the referee's simulator repeats the run on the same sample
                    Cr = Cr or referee_consts(C, us, n_o, design)
                    rr = rs.run(psi, Cr, orc, np.random.default_rng(s))
                    tie = rr.info_tie_abort
                st["aborted_tie" if tie else "aborted_other"] += 1
                if len(st["examples"]) < 5:
                    st["examples"].append(dict(what=r["status"], kind=f"{src}:{kind}", oracle=orc, run_seed=s, level=r["level"], floating_point_tie=tie))
                continue
            st["closed"] += 1
            st["max_width"] = max(st["max_width"], r["width"])
            if not r["valid"]:
                st["invalid"] += 1
                bk["invalid"] += 1
                if len(st["examples"]) < 5:
                    st["examples"].append(dict(what="invalid", kind=f"{src}:{kind}", oracle=orc, run_seed=s, lA=r["lA"], lL=r["lL"], lU=r["lU"]))
            st["too_wide"] += r["width"] > C.x_out + 1e-9
            st["bad_certificates"] += not r["certificates_ok"]
    st["seconds"] = time.time() - t0
    out.update(st)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=12.0)
    ap.add_argument("--procs", type=int, default=2)
    ap.add_argument("--seed", type=int, default=977)
    args = ap.parse_args()
    rs.limit_memory(1.3)                      # per process; the workers inherit it
    t0 = time.time()
    jobs = [(si, di) for si in range(len(SHAPES)) for di in range(len(DESIGNS))]
    per = args.minutes * 60 * args.procs / len(jobs)
    with Pool(args.procs) as pool:
        rows = pool.map(task, [j + (per, args.seed + 104729 * i) for i, j in enumerate(jobs)], chunksize=1)
    tot = dict(configurations=0, skipped=0, runs=0, closed=0, invalid=0, too_wide=0, aborted=0, aborted_tie=0, aborted_other=0, over_budget=0,
               bad_certificates=0, max_class_violation=-math.inf, min_slack_width=math.inf, max_lcost_minus_lCmax=-math.inf,
               largest_invalid_fraction_in_a_configuration=0.0)
    for r in rows:
        if "skipped" in r:
            tot["skipped"] += 1
            continue
        tot["configurations"] += 1
        for k in ("runs", "closed", "invalid", "too_wide", "aborted", "aborted_tie", "aborted_other", "over_budget", "bad_certificates"):
            tot[k] += r[k]
        tot["max_class_violation"] = max(tot["max_class_violation"], r["class_violation"])
        if r["closed"]:
            tot["min_slack_width"] = min(tot["min_slack_width"], r["x_out"] - r["max_width"])
        if r["runs"]:
            tot["max_lcost_minus_lCmax"] = max(tot["max_lcost_minus_lCmax"], r["max_lcost"] - r["lCmax_unit"])
            tot["largest_invalid_fraction_in_a_configuration"] = max(tot["largest_invalid_fraction_in_a_configuration"], r["invalid"] / r["runs"])
    res = dict(summary=tot, rows=rows, seconds=time.time() - t0)
    (HERE / "attack_their_sim.json").write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps(tot, indent=1, default=float))
    for r in rows:
        if "skipped" not in r and (r["invalid"] or r["too_wide"] or r["aborted"] or r["over_budget"] or r["bad_certificates"]):
            print(r["shape"], r["design"], {k: r[k] for k in ("runs", "invalid", "too_wide", "aborted", "aborted_tie", "aborted_other", "over_budget", "bad_certificates")}, r["examples"][:2])
    print(f"[{time.time() - t0:.0f} s]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
