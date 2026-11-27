"""Review of ENG-RES-0016 §2, item 4 of the brief: an attempt to produce a counterexample numerically.

The referee's simulator (``review_sim.py``) on block shapes, parameter sets, instances and inner oracles that the
division's experiment X-014b did not use: extreme slope ratios in both directions, an inner block of one site, outer
blocks of 1-5 sites, parameters at the edges of the theorem's range (eta = 1/2 and 1/20; lambda = 1 and 0.05; eta' = 1;
theta from 0.01 to e^8; tolerance down to 0.02; one to eight rungs), instances built against single steps of the proof
(the cone at the reference point: first lower bound an equality; dips on the outer cube with the extreme outer slope:
equality in the tail lemma; plateaus and cones on the outer cube: equality in the Harper term; fibres whose value at
the reference point is as far from the fibre average as the class allows), adversarial oracles.

Campaigns:
    theorem     the constants of the statement.  A violation of a deterministic claim in any run, or of any claim in a run
                on which the events (V2), (V3) used by the proof hold, is a counterexample.
    radius      the same on flat outer blocks of 6-11 sites, where runs close through the tail lemma at positive radii.
    tuned       instances built against the design (``tuned_dip``): the set {W > s_j} at the closing level is as large, and
                the fibre averages on it as high, as the closure test lets pass; with the claim's tables, and as a control
                with outer tables for half the outer slope.
    kdiv        K divided by 8 and by 32: the good event now fails in a visible fraction of the runs; the claims must
                still hold on the runs where the events used hold, and the deterministic ones always.
    mutations   negative controls: transfers that are WRONG (outer tables for another slope, the homogeneous Omega_Y,
                first lower bound, J) and two mutations of the original algorithm; each must be caught.

    python experiments/eng/review_x014/attack.py theorem|radius|kdiv|mutations [--minutes 14] [--procs 2]
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
sys.path.insert(0, str(HERE))

import review_sim as rs  # noqa: E402

F = Fraction
# (n_o, u_o, inner slopes): the outer block first
SHAPES = [
    (6, 0.05, (5.0, 5.0, 5.0)),            # inner slopes 100 times the outer slope
    (7, 0.05, (20.0,)),                    # an inner block of one very steep site
    (5, 3.0, (0.05, 0.05, 0.05, 0.05)),    # inner slopes 1/60 of the outer slope
    (4, 6.0, (0.1,) * 6),
    (8, 0.3, (10.0,)),
    (3, 0.1, (4.0, 0.2, 2.0, 0.01)),
    (2, 0.5, (3.0,) * 5),
    (5, 1.0, (1.0, 1.0, 2.0)),             # the inner block contains sites of the outer type
    (1, 2.0, (0.3,) * 8),                  # an outer block of one site
    (1, 0.2, (2.5, 2.5, 0.4)),
    (2, 4.0, (0.5,) * 8),
    (10, 0.7, (0.3,)),                     # an inner block of one site, flatter than the outer block
    (11, 1.0, (2.0,)),
    (4, 1.37, (0.83, 2.11, 0.29)),         # generic slopes: no structural ties
    (7, 0.61, (1.93, 0.37)),
    (3, 2.3, (1.1, 1.1, 1.1, 0.4, 0.4)),
    (9, 1.5, (0.2, 0.2, 0.2)),
    (6, 2.0, (2.0, 0.5, 0.5)),
]
N_BASE = len(SHAPES)
# campaign "radius": flat outer blocks, where the closure test passes at positive radii (so that the tail lemma with the
# OUTER slope carries the upper end) and levels are left as negligible
SHAPES += [
    (8, 0.3, (10.0,)),
    (10, 0.2, (2.0, 0.7)),
    (11, 0.15, (2.0,)),
    (9, 0.5, (3.0, 0.4)),
    (7, 0.1, (5.0, 5.0)),
    (11, 0.25, (1.5,)),
    (6, 0.4, (0.9, 2.2, 0.3)),
    (10, 0.35, (0.35, 0.35, 3.0)),          # the inner block contains sites of the outer type
]
# parameter sets: lam, eta, etap, theta, bounded (nu_1 = 2 e^{u_o} n_o / theta) or nu_1 = 1, tolerance b (None: a fraction of x_0), rungs
DESIGNS = [
    dict(name="EXT lam=1 eta=1/2 eta'=1 theta=1", lam=1.0, eta=F(1, 2), etap=1.0, theta=1.0, bounded=False, b=1.0, L=4),
    dict(name="generic lam eta=1/2", lam=0.6180339887, eta=F(1, 2), etap=1.0, theta=1.0, bounded=True, b=0.7310585786, L=3),
    dict(name="small eta=1/10", lam=0.5, eta=F(1, 10), etap=0.5, theta=0.5, bounded=True, b=0.5, L=2),
    dict(name="eta=1/20", lam=1.0, eta=F(1, 20), etap=1.0, theta=1.0, bounded=False, b=1.0, L=2),
    dict(name="small lam=0.05", lam=0.05, eta=F(1, 2), etap=1.0, theta=1.0, bounded=False, b=0.3, L=2),
    dict(name="large theta=e^8", lam=1.0, eta=F(1, 2), etap=1.0, theta=math.exp(8.0), bounded=False, b=1.0, L=3),
    dict(name="small theta=0.01", lam=0.3, eta=F(1, 3), etap=0.1, theta=0.01, bounded=True, b=0.2, L=5),
    dict(name="small theta=0.01, nu1=1", lam=0.3, eta=F(1, 3), etap=0.1, theta=0.01, bounded=False, b=0.2, L=5),
    dict(name="small b=0.02", lam=0.5, eta=F(1, 2), etap=1.0, theta=1.0, bounded=True, b=0.02, L=4),
    dict(name="one rung", lam=1.0, eta=F(1, 2), etap=1.0, theta=1.0, bounded=True, b=None, L=1),
    dict(name="eight rungs", lam=0.7, eta=F(1, 3), etap=0.3, theta=0.2, bounded=True, b=0.1, L=8),
    dict(name="small eta'=0.02", lam=1.0, eta=F(1, 2), etap=0.02, theta=1.0, bounded=False, b=0.5, L=3),
    dict(name="BND lam=1/2 eta=eta'=theta=1/4", lam=0.5, eta=F(1, 4), etap=0.25, theta=0.25, bounded=True, b=0.5, L=4),
]


def bulk_only(C):
    """The flat instance with the reference value lowered by eps_1 (a member of the class): every fibre average but one is
    t, and t lies eps_1 below a level of the ladder when Omega/lambda is an integer."""
    us = np.asarray(C.D.us)
    psi = np.zeros(2 ** len(us))
    psi[0] -= min(0.01, 0.5 * float(us.min()))
    return psi


def tuned_dip(C, rng, size: int):
    """An instance built against Step 3 (the upper end) of THIS design.  A pilot run on ``bulk_only`` tells at which sample
    size M the level just above the bulk closes, unpopulated, with q = K/((1 - eta) M) and radius r(q).  The instance adds a
    dip on a set D of ``size`` = 0.8 K 2^{n_o}/M outer points — an initial segment of a simplicial order around a random
    centre — on which the fibre averages are as large as the class allows, W = t e^{u_o dist_H(a, D^c)}.  The run is then
    the pilot's up to that pass (about 0.8 K sample points fall into D: the level stays unpopulated), it closes there, and
    the true tail E(W - s_j)_+ is as close to the bound s_j 2^-n_o E_r as the algorithm's own margins permit: {W > s_j} = D
    has 0.8 (1 - eta) 2^{n_o} q <= 0.8 (1 - eta) |B(r)| points.  Flat fibres."""
    us = np.asarray(C.D.us)
    n_o = C.D.n_o
    n = len(us)
    u_o = float(us[0])
    A = rs.all_points(n_o)
    idx = np.arange(2 ** n_o)
    for _ in range(50):
        c = A[rng.integers(2 ** n_o)]
        dH = np.abs(A - c[None, :]).sum(axis=1)
        rank = np.lexsort((rng.random(2 ** n_o), dH))            # a simplicial-type order around c: by distance, ties at random
        inD = np.zeros(2 ** n_o, dtype=bool)
        inD[rank[:size]] = True
        near = inD.copy()                                        # the reference outer point must be in the bulk, at distance >= 2 from D
        for i in range(n_o):
            near |= inD[idx ^ (1 << i)]
        if not near[0]:
            break
    else:
        return None
    g = -rs.lipschitz_minorant(np.where(inD, 1e6, 0.0), np.full(n_o, u_o))
    X = rs.all_points(n)
    code = X[:, :n_o].astype(np.int64) @ (1 << np.arange(n_o))
    psi = g[code].astype(float)
    psi[0] -= min(0.01, 0.5 * float(us.min()))
    return psi


def build(shape, design, table_slope=None, tune_lambda=False):
    n_o, u_o, inner = shape
    us = (u_o,) * n_o + tuple(inner)
    x0 = 2 * sum(inner)
    if tune_lambda:                                             # the largest lambda <= the design's with Omega/lambda an integer
        Om = float(np.sum(np.asarray(us)))
        design = dict(design, lam=Om / math.ceil(Om / design["lam"]))
    b = design["b"] if design["b"] is not None and design["b"] < 0.9 * x0 else 0.45 * x0     # the tolerance must be below x_0
    if not b < x0:
        return None
    nu1 = max(1.0, 2 * n_o * math.exp(u_o) / design["theta"]) if design["bounded"] else 1.0
    D = rs.Design(us=us, n_o=n_o, lam=design["lam"], eta=design["eta"], etap=design["etap"], lth=math.log(design["theta"]), nu1=nu1, b=b,
                  xs=rs.geometric_ladder(x0, b, design["L"]), table_slope=table_slope)
    return rs.make_consts(D)


def task(args):
    si, di, mode, kdiv, mutation, table_factor, seconds, seed = args
    shape, design = SHAPES[si], DESIGNS[di]
    n_o, u_o, inner = shape
    C = build(shape, design, table_slope=None if table_factor is None else u_o * table_factor, tune_lambda=(mode == "tuned"))
    out = dict(shape=[n_o, u_o, list(inner)], design=design["name"], mode=mode, kdiv=kdiv, mutation=mutation, table_factor=table_factor, seed=seed)
    if C is None:
        out["skipped"] = "x_0 <= b"
        return out
    K_thm = C.K
    if kdiv != 1:
        C.set_K(max(1, math.ceil(C.K / kdiv)))
    out.update(K=K_thm, K_used=C.K, J=C.J, r_dag=C.r_dag, m_max=C.m_max, x_out=C.x_out, lCmax=C.lCmax(), lM_bar=C.lM_bar, Omega=C.Omega,
               Omega_Y=C.Omega_Y, lPi=C.lPi)
    # a sample can reach K 2^{n_o+1}/(1-eta) points; skip parameter sets whose runs would not fit in memory or time
    worst = C.K * 2 ** (n_o + 1) / (1 - float(design["eta"]))
    if worst > 3e6:
        out["skipped"] = f"samples of up to {worst:.1e} points"
        return out
    us = np.asarray(C.D.us)
    rng = np.random.default_rng(seed)
    stat = dict(runs=0, closed=0, aborted=0, tie_aborts=0, good=0, ties_runs=0, viol_good={}, viol_bad={}, det_viol={}, invalid_good=0, invalid_bad=0,
                max_width=0.0, min_slack_width=math.inf, max_lcost=0.0, neg_levels=0, class_violation=-math.inf, by_kind={}, examples=[])
    t0 = time.time()
    combos = [(k, o) for k in rs.INSTANCE_KINDS for o in rs.ORACLES]
    if mode == "tuned":
        combos = [("tuned_dip", o) for o in ("top", "low", "sticky_low")]
        pilot = rs.run(bulk_only(C), C, "top", np.random.default_rng(seed))
        if pilot.status != "closed" or pilot.info["r_close"] < 1:
            out["skipped"] = "the pilot run closes with an empty tail or at radius 0: no dip to place"
            return out
        dip_size = max(1, int(0.8 * C.K * 2 ** n_o / pilot.M))
        out.update(pilot_M=pilot.M, pilot_radius=pilot.info["r_close"], dip_size=dip_size, ball_at_pilot_radius=C.T.ball[pilot.info["r_close"]])
    rng.shuffle(combos)
    i = 0
    while time.time() - t0 < seconds:
        kind, orc = combos[i % len(combos)]
        i += 1
        psi = tuned_dip(C, rng, dip_size) if kind == "tuned_dip" else rs.instance(kind, us, n_o, rng)
        if psi is None:
            continue
        if rng.random() < 0.5:
            psi = psi + rng.uniform(-3, 3)                       # the reference value is arbitrary
        stat["class_violation"] = max(stat["class_violation"], rs.class_violation(psi, us))
        s = int(rng.integers(2 ** 31))
        try:
            R = rs.run(psi, C, orc, np.random.default_rng(s), mutation=mutation)
        except MemoryError:                                     # the address-space cap of this process was reached: skip the run
            stat["memory_errors"] = stat.get("memory_errors", 0) + 1
            continue
        stat["runs"] += 1
        bk = stat["by_kind"].setdefault(kind, dict(runs=0, invalid=0, viol=0))
        bk["runs"] += 1
        stat["good"] += R.good
        stat["ties_runs"] += R.ties > 0
        stat["neg_levels"] += R.info.get("n_neg", 0)
        stat["max_lcost"] = max(stat["max_lcost"], math.log(R.queries))
        if R.status == "closed":
            stat["closed"] += 1
            rc = R.info["r_close"]
            key = "closed_empty_tail" if rc < 0 else ("closed_at_radius_0" if rc == 0 else "closed_at_radius_ge_1")
            stat[key] = stat.get(key, 0) + 1
            stat["closed_at_populated_pass"] = stat.get("closed_at_populated_pass", 0) + R.info["pop_close"]
            if R.info.get("tail_ratio") is not None:        # closest approach to equality in the upper tail lemma as used (<= 1 if valid)
                stat["max_tail_ratio"] = max(stat.get("max_tail_ratio", 0.0), R.info["tail_ratio"])
            stat["max_width"] = max(stat["max_width"], R.width)
            stat["min_slack_width"] = min(stat["min_slack_width"], C.x_out - R.width)
        elif R.info_tie_abort:
            stat["tie_aborts"] += 1
        else:
            stat["aborted"] += 1
        if R.info.get("harper_ratio") is not None:          # closest approach to equality in the lower tail lemma as used (>= 1 if valid)
            stat["min_harper_ratio"] = min(stat.get("min_harper_ratio", math.inf), R.info["harper_ratio"])
        invalid = any(k in R.viol for k in ("(ii) L <= A", "(ii) A <= U"))
        if invalid:
            stat["invalid_good" if R.good else "invalid_bad"] += 1
            bk["invalid"] += 1
        if R.viol:
            bk["viol"] += 1
            for claim, cnt in R.viol.items():
                if claim in rs.DETERMINISTIC:
                    stat["det_viol"][claim] = stat["det_viol"].get(claim, 0) + 1
                tgt = stat["viol_good"] if R.good else stat["viol_bad"]
                tgt[claim] = tgt.get(claim, 0) + 1
            if len(stat["examples"]) < 6 and (R.good or any(c in rs.DETERMINISTIC for c in R.viol)):
                stat["examples"].append(dict(kind=kind, oracle=orc, run_seed=s, status=R.status, level=R.level, good=R.good, ties=R.ties, viol=R.viol,
                                             lA=R.lA, lL=R.lL, lU=R.lU, width=R.width))
    stat["seconds"] = time.time() - t0
    out.update(stat)
    return out


def plan(mode: str, seconds_total: float, procs: int, seed0: int):
    jobs = []
    if mode == "theorem":
        for si in range(N_BASE):
            for di in range(len(DESIGNS)):
                jobs.append((si, di, mode, 1, None, None))
    elif mode == "radius":
        for si in range(N_BASE, len(SHAPES)):
            for di in (0, 1, 5, 9, 11, 12):
                jobs.append((si, di, mode, 1, None, None))
    elif mode == "tuned":
        for si in list(range(N_BASE, len(SHAPES))) + [0, 13, 14]:
            for di in (0, 5, 3, 12):
                for tf in (None, 0.5):
                    jobs.append((si, di, mode, 1, None, tf))
    elif mode == "kdiv":
        for si in range(N_BASE):
            for di in (0, 1, 4, 5, 6, 9, 12):
                for kdiv in (8, 32):
                    jobs.append((si, di, mode, kdiv, None, None))
    elif mode == "mutations":
        for si in (0, 1, 2, 4, 5, 6, 7, 10, 13, 14, 16, 17):
            for di in (0, 1, 12):
                for mut, tf in ((None, 0.25), (None, 0.5), ("omegaY_hom", None), ("ell_hom", None), ("J_hom", None), ("s0_hom", None),
                                ("no_harper", None), ("maxform", None)):
                    jobs.append((si, di, mode, 1, mut, tf))
    else:
        raise ValueError(mode)
    per = seconds_total * procs / len(jobs)
    return [j + (per, seed0 + 7919 * i) for i, j in enumerate(jobs)]


def summarise(rows: list) -> dict:
    tot = dict(configurations=0, skipped=0, runs=0, closed=0, aborted=0, tie_aborts=0, good=0, runs_with_ties=0, invalid_on_good_event=0,
               invalid_off_good_event=0, violations_on_good_event={}, violations_off_good_event={}, deterministic_violations={},
               max_class_violation=-math.inf, min_slack_width=math.inf, max_lcost_minus_lCmax=-math.inf, negligible_levels=0)
    for r in rows:
        if "skipped" in r:
            tot["skipped"] += 1
            continue
        tot["configurations"] += 1
        for a, b in (("runs", "runs"), ("closed", "closed"), ("aborted", "aborted"), ("tie_aborts", "tie_aborts"), ("good", "good"),
                     ("runs_with_ties", "ties_runs"), ("invalid_on_good_event", "invalid_good"), ("invalid_off_good_event", "invalid_bad"),
                     ("negligible_levels", "neg_levels")):
            tot[a] += r[b]
        for k in ("closed_empty_tail", "closed_at_radius_0", "closed_at_radius_ge_1", "closed_at_populated_pass", "memory_errors"):
            tot[k] = tot.get(k, 0) + r.get(k, 0)
        for a, b in (("violations_on_good_event", "viol_good"), ("violations_off_good_event", "viol_bad"), ("deterministic_violations", "det_viol")):
            for k, v in r[b].items():
                tot[a][k] = tot[a].get(k, 0) + v
        tot["max_class_violation"] = max(tot["max_class_violation"], r["class_violation"])
        if "max_tail_ratio" in r:
            tot["max_tail_ratio"] = max(tot.get("max_tail_ratio", 0.0), r["max_tail_ratio"])
        if "min_harper_ratio" in r:
            tot["min_harper_ratio"] = min(tot.get("min_harper_ratio", math.inf), r["min_harper_ratio"])
        tot["min_slack_width"] = min(tot["min_slack_width"], r["min_slack_width"])
        if r["runs"]:
            tot["max_lcost_minus_lCmax"] = max(tot["max_lcost_minus_lCmax"], r["max_lcost"] - r["lCmax"])
    return tot


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["theorem", "radius", "tuned", "kdiv", "mutations"])
    ap.add_argument("--minutes", type=float, default=14.0)
    ap.add_argument("--procs", type=int, default=2)
    ap.add_argument("--seed", type=int, default=20261126)
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    rs.limit_memory(1.3)                      # per process; the workers inherit it
    t0 = time.time()
    jobs = plan(args.mode, args.minutes * 60, args.procs, args.seed)
    with Pool(args.procs) as pool:
        rows = pool.map(task, jobs, chunksize=1)
    res = dict(mode=args.mode, seed=args.seed, minutes=args.minutes, summary=summarise(rows), rows=rows, seconds=time.time() - t0)
    if args.mode in ("mutations", "tuned"):
        by = {}
        for r in rows:
            if "skipped" in r:
                continue
            key = r["mutation"] or ("the claim's tables" if r["table_factor"] is None else f"outer tables for {r['table_factor']} of the outer slope")
            d = by.setdefault(key, dict(configurations=0, configurations_caught=0, runs=0, runs_with_a_violation=0, invalid=0, aborted=0, claims={}))
            d["configurations"] += 1
            nv = sum(v["viol"] for v in r["by_kind"].values())
            d["configurations_caught"] += nv > 0
            d["runs"] += r["runs"]
            d["runs_with_a_violation"] += nv
            d["invalid"] += r["invalid_good"] + r["invalid_bad"]
            d["aborted"] += r["aborted"]
            if "max_tail_ratio" in r:
                d["max_tail_ratio"] = max(d.get("max_tail_ratio", 0.0), r["max_tail_ratio"])
            for src in ("viol_good", "viol_bad"):
                for k, v in r[src].items():
                    d["claims"][k] = d["claims"].get(k, 0) + v
        res["by_mutation"] = by
    name = f"attack_{args.mode}{('_' + args.tag) if args.tag else ''}.json"
    (HERE / name).write_text(json.dumps(res, indent=1, default=float))
    s = res["summary"]
    print(json.dumps(s, indent=1, default=float))
    if args.mode in ("mutations", "tuned"):
        for k, d in res["by_mutation"].items():
            print(f"{k:45s} caught in {d['configurations_caught']}/{d['configurations']} configurations; {d['runs_with_a_violation']}/{d['runs']} runs; "
                  f"invalid {d['invalid']}, aborted {d['aborted']}; claims {d['claims']}")
    print(f"[{time.time() - t0:.0f} s] -> {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
