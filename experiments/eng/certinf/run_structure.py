"""Structure runs of the protocol: F4 (level counts, exactness at scale, timing), F5 (bounded influence: the programme
against Corollary 9.3, timing, the box hull), F6 (the ensemble division's frozen controls B5-01/02/03 with l = 0).

    python experiments/eng/certinf/run_structure.py            # writes results/structure.json
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from fractions import Fraction
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import instances as ins  # noqa: E402
from instances import ci  # noqa: E402

REPO = HERE.parents[2]
CONTROLS = REPO.parent / "MetricChain-archive" / "consolidated" / "04_ensemble_identifiability" / "experiments" / "ensemble" / "benchmarks" / "controls_v1.json"


# ------------------------------------------------------------------------------------------------ F4
def run_f4():
    out = []
    for rho in ins.RHOS:
        t0 = time.perf_counter()
        c = ins.f4_cells(rho)
        t_counts = time.perf_counter() - t0
        l, u = c["prob"] * math.exp(-rho), c["prob"] * math.exp(rho)
        reg = ci.Box(c["centre"], ins.HALF)
        P = ci.box_problem(l, u, c["f"], c["phi"], reg)
        t0 = time.perf_counter()
        ex = ci.interval(P, "lp")
        t_lp = time.perf_counter() - t0
        t0 = time.perf_counter()
        de = ci.interval(P, "descent")
        t_de = time.perf_counter() - t0
        out.append(dict(rho=rho, gamma=math.exp(2 * rho), n_cells=c["ncells"], prob_sum=float(c["prob"].sum()), t_counts=t_counts,
                        lo=float(ex["lo"]), hi=float(ex["hi"]), t_lp=t_lp, lo_descent=float(de["lo"]), hi_descent=float(de["hi"]),
                        t_descent=t_de, true=float(c["true_f"]), states_log2=100))
    # check of the level counts on a small product (12 sites) against enumeration
    rng = np.random.default_rng(405)
    p = rng.uniform(0.2, 0.8, 12)
    st = ((np.arange(1 << 12)[:, None] >> np.arange(12)) & 1)
    pi = np.prod(np.where(st == 1, p, 1 - p), axis=1)
    law = ci.product_joint_law([[1 - q, q] for q in p], [[[0, 0], [int(i < 5), int(i >= 5)]] for i in range(12)])
    k1, k2 = st[:, :5].sum(1), st[:, 5:].sum(1)
    enum = np.zeros((6, 8))
    np.add.at(enum, (k1, k2), pi)
    return dict(rows=out, small_check_maxdiff=float(np.abs(enum - law).max()))


# ------------------------------------------------------------------------------------------------ F5
def f5_model(nsite, slope_kind, seed):
    rng = np.random.default_rng(seed)
    p = rng.uniform(0.2, 0.8, nsite)
    slope = np.full(nsite, 0.5) if slope_kind == "0.5" else rng.uniform(0.2, 1.0, nsite)
    a = rng.uniform(-1, 1, (2, nsite, 2))            # two additive observables: (1/n) sum_i a_k[i, x_i]
    cf = rng.uniform(-1, 1, (nsite, 2))              # additive target: (1/n) sum_i c[i, x_i]
    t = slope * rng.uniform(-0.8, 0.8, nsite)        # the true ensemble: product tilt, inside the class
    pt = 1 / (1 + np.exp(-(np.log(p / (1 - p)) + t)))
    centre = np.array([float(((1 - pt) * a[k, :, 0] + pt * a[k, :, 1]).sum() / nsite) for k in range(2)])
    return p, slope, a, cf, pt, centre


def f5_sites(nsite, p, a, cf, target):
    phis = [np.column_stack([a[0, i], a[1, i]]) / nsite for i in range(nsite)]
    if target == "additive":
        fs = [cf[i] / nsite for i in range(nsite)]
    elif target == "one_spin":
        fs = [np.array([-1.0, 1.0])] + [np.zeros(2) for _ in range(nsite - 1)]
    else:
        raise ValueError(target)
    return fs, phis


def run_f5():
    rows = []
    for nsite in (8, 12):
        states, edges, site = ci.hypercube(nsite)
        x = states.astype(int)
        for slope_kind in ("0.5", "random"):
            p, slope, a, cf, pt, centre = f5_model(nsite, slope_kind, 500 + nsite)
            pi = np.prod(np.where(states == 1, p, 1 - p), axis=1)
            C = np.exp(slope[site])
            phi = np.column_stack([sum(a[k, i][x[:, i]] for i in range(nsite)) / nsite for k in range(2)])
            box = ci.Box(centre, ins.HALF)
            tg = {"additive": sum(cf[i][x[:, i]] for i in range(nsite)) / nsite, "one_spin": 2 * states[:, 0] - 1,
                  "two_spin": (2 * states[:, 0] - 1) * (2 * states[:, 1] - 1)}
            for name, f in tg.items():
                for data in (False, True):
                    t0 = time.perf_counter()
                    pr = ci.lp_ratio_class(pi, edges, C, f, phi if data else None, box if data else None)
                    t_lp = time.perf_counter() - t0
                    row = dict(nsite=nsite, slope=slope_kind, target=name, data=data, lp_lo=pr[0], lp_hi=pr[1], t_lp=t_lp)
                    if name != "two_spin":
                        fs, phis = f5_sites(nsite, p, a, cf, name)
                        t0 = time.perf_counter()
                        ad = ci.additive_interval([[1 - q, q] for q in p], slope, fs, phis if data else None, box if data else None)
                        row.update(add_lo=ad["lo"], add_hi=ad["hi"], t_add=time.perf_counter() - t0,
                                   diff=max(abs(ad["lo"] - pr[0]), abs(ad["hi"] - pr[1])))
                    rows.append(row)
    big = []
    for nsite in (50, 200):
        for slope_kind in ("0.5", "random"):
            p, slope, a, cf, pt, centre = f5_model(nsite, slope_kind, 500 + nsite)
            box = ci.Box(centre, ins.HALF)
            for name in ("additive", "one_spin"):
                fs, phis = f5_sites(nsite, p, a, cf, name)
                t0 = time.perf_counter()
                ad = ci.additive_interval([[1 - q, q] for q in p], slope, fs, phis, box)
                t_add = time.perf_counter() - t0
                tv = float(((1 - pt) * cf[:, 0] + pt * cf[:, 1]).sum() / nsite) if name == "additive" else float(2 * pt[0] - 1)
                big.append(dict(nsite=nsite, slope=slope_kind, target=name, lo=ad["lo"], hi=ad["hi"], t=t_add, true=tv,
                                covers_true=bool(ad["lo"] - 1e-9 <= tv <= ad["hi"] + 1e-9)))
    # the box hull of the class (slope 0.5 per site): ratio e^{0.5 n}; target one spin, no data
    hull = []
    for nsite in (8, 12, 16, 20, 30, 50, 100, 200):
        p, slope, a, cf, pt, centre = f5_model(nsite, "0.5", 500 + nsite)
        gam = math.exp(0.5 * nsite)
        l = np.array([1 - p[0], p[0]])
        out = ci.interval(ci.box_problem(l, gam * l, [-1.0, 1.0], np.zeros((2, 0)), ci.Box()))
        th = math.log(p[0] / (1 - p[0]))
        cls = (2 / (1 + math.exp(-(th - 0.5))) - 1, 2 / (1 + math.exp(-(th + 0.5))) - 1)
        add = ci.additive_interval([[1 - q, q] for q in p], slope, f5_sites(nsite, p, a, cf, "one_spin")[0])
        hull.append(dict(nsite=nsite, hull_lo=float(out["lo"]), hull_hi=float(out["hi"]), gap_to_range=float(max(1 - out["hi"], out["lo"] + 1)),
                         class_lo=cls[0], class_hi=cls[1], add_lo=add["lo"], add_hi=add["hi"]))
    # one full-cube check of the hull at 8 sites (box class on all 256 states against the 2-cell lumping)
    states, _, _ = ci.hypercube(8)
    p, *_ = f5_model(8, "0.5", 508)
    pi = np.prod(np.where(states == 1, p, 1 - p), axis=1)
    full = ci.interval(ci.box_problem(pi, math.exp(4.0) * pi, 2 * states[:, 0] - 1, np.zeros((256, 0)), ci.Box()))
    return dict(rows=rows, big=big, hull=hull, hull_full_check=[float(full["lo"]), float(full["hi"])])


# ------------------------------------------------------------------------------------------------ F6
def run_f6():
    d = json.loads(CONTROLS.read_text())
    ctl = {c["id"]: c for c in d["controls"]}
    base = ctl["B5-01"]
    states = base["space"]["states"]
    table = np.array([[float(Fraction(v)) for v in row] for row in base["observables"]["table"]]).T     # (8, 3)
    out = []
    for cid in ("B5-01", "B5-02", "B5-03"):
        c = ctl[cid]
        y = np.array([float(Fraction(v)) for v in c["data"]])
        tau = float(Fraction(c["tolerance"]["tau"])) if "tolerance" in c else 0.0
        if cid == "B5-02":
            f = np.array([1.0 if s == "+++" else 0.0 for s in states])
        else:
            f = table[:, 0] * table[:, 1]
        box = ci.Box(y, tau)
        t0 = time.perf_counter()
        res = ci.interval(ci.Problem(f, table, Lw=0.0, Gw=1.0, region=box))
        dt = time.perf_counter() - t0
        pr = ci.lp_primal_box(np.zeros(8), np.ones(8), f, table, box)
        exp = [float(Fraction(v)) for v in c["expected"]["interval"]]
        out.append(dict(id=cid, lo=float(res["lo"]), hi=float(res["hi"]), expected=exp, expected_str=c["expected"]["interval"],
                        primal=list(pr) if pr else None, diff=max(abs(res["lo"] - exp[0]), abs(res["hi"] - exp[1])), t=dt))
    return out


if __name__ == "__main__":
    t0 = time.perf_counter()
    res = dict(F4=run_f4())
    print("F4 done", time.perf_counter() - t0, flush=True)
    res["F6"] = run_f6()
    print("F6", res["F6"], flush=True)
    res["F5"] = run_f5()
    res["wall"] = time.perf_counter() - t0
    (HERE / "results" / "structure.json").write_text(json.dumps(res, indent=1, default=float))
    (HERE / "results" / "structure_wall.json").write_text(json.dumps(dict(wall=res["wall"])))
    print("done", res["wall"])
